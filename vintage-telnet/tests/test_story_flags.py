"""Pruebas exhaustivas para VT-SERVER: STORY-FLAGS-01 (#427).

Contrato autoritativo:
1. set/get/clear de flags persistentes por personaje sin recompensa de XP.
2. grant_story_item_once atómico e idempotente (1 sola hoja_hoshai u objeto único).
3. Rollback de flag ante fallo de grant.
4. Persistencia tras reinicio/reconexión.
5. Aislamiento entre múltiples jugadores.
6. Concurrencia y protección contra doble submit.
7. Migración de esquema v14 -> v15.
"""
from concurrent.futures import ThreadPoolExecutor
import os
import sqlite3
import tempfile
import unittest

from server import store


class StoryFlagsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "vintage_test.sqlite3")
        store.initialize(self.db_path)
        self.player_id = "test-player-001"
        self._create_test_player(self.player_id, "matias_tester")

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def _create_test_player(self, player_id, username):
        with store.connect(self.db_path) as db:
            db.execute(
                """INSERT INTO players (id, username, name, password_hash, status, created_at, last_access_at,
                                       level, xp, pa_unspent, hp_current, hp_max, fatigue, wound)
                   VALUES (?, ?, 'Matías', 'hash', 'approved', '2026-09-28T00:00:00Z', '2026-09-28T00:00:00Z',
                           1, 0, 0, 20.0, 20.0, 0, 'ninguna')""",
                (player_id, username),
            )

    def test_set_and_get_story_flag(self):
        """Verifica fijar y consultar un flag narrativo por jugador."""
        # Inicialmente el flag no existe
        self.assertFalse(store.get_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado"))

        # Fijar por primera vez -> True (cambió)
        changed = store.set_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado", True)
        self.assertTrue(changed)
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado"))

        # Fijar de nuevo con el mismo valor -> False (idempotente)
        changed_again = store.set_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado", True)
        self.assertFalse(changed_again)
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado"))

        # Consultar diccionario de flags
        flags = store.get_player_story_flags(self.db_path, self.player_id)
        self.assertEqual(flags, {"hoshai_paso_ayudado": True})

    def test_clear_story_flag(self):
        """Verifica la eliminación limpia de un flag narrativo."""
        store.set_story_flag(self.db_path, self.player_id, "flag_temporal", True)
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "flag_temporal"))

        store.clear_story_flag(self.db_path, self.player_id, "flag_temporal")
        self.assertFalse(store.get_story_flag(self.db_path, self.player_id, "flag_temporal"))
        self.assertNotIn("flag_temporal", store.get_player_story_flags(self.db_path, self.player_id))

    def test_grant_story_item_once_idempotence(self):
        """Caso primer consumidor #287 (HOSHAI-WEAPON-01): entrega única e idempotente de hoja_hoshai."""
        # 1. Flag previo de ayuda
        store.set_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado", True)

        # 2. Primera entrega de hoja_hoshai con forge_validated=False
        success, item_id = store.grant_story_item_once(
            self.db_path,
            self.player_id,
            "hoshai_hoja_recibida",
            "hoja_hoshai",
            forge_validated=False,
        )
        self.assertTrue(success)
        self.assertIsNotNone(item_id)
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_hoja_recibida"))

        # Verificar inventario
        inv = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual(len(inv), 1)
        self.assertEqual(inv[0]["item_key"], "hoja_hoshai")
        self.assertEqual(inv[0]["category"], "weapon")
        self.assertEqual(inv[0]["forge_validated"], 0)

        # 3. Reintento / refresh / doble submit
        success_retry, item_id_retry = store.grant_story_item_once(
            self.db_path,
            self.player_id,
            "hoshai_hoja_recibida",
            "hoja_hoshai",
            forge_validated=False,
        )
        self.assertFalse(success_retry)
        self.assertIsNone(item_id_retry)

        # El inventario no debe contener duplicados
        inv_after = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual(len(inv_after), 1)
        self.assertEqual(inv_after[0]["id"], item_id)

    def test_story_flags_do_not_grant_xp_or_level(self):
        """Garantiza el requisito de aceptación 6: ninguna operación concede XP ni altera nivel."""
        char_before = store.character_by_player_id(self.db_path, self.player_id)
        initial_xp = char_before["xp"]
        initial_level = char_before["level"]

        store.set_story_flag(self.db_path, self.player_id, "mision_hoshai_flag", True)
        store.grant_story_item_once(
            self.db_path,
            self.player_id,
            "recompensa_entregada",
            "hoja_hoshai",
            forge_validated=False,
        )

        char_after = store.character_by_player_id(self.db_path, self.player_id)
        self.assertEqual(char_after["xp"], initial_xp, "Story flags no deben otorgar XP")
        self.assertEqual(char_after["level"], initial_level, "Story flags no deben alterar el nivel")

    def test_grant_story_item_failure_rollback(self):
        """Garantiza consistencia transaccional: si el grant falla, el flag no queda activo."""
        self.assertFalse(store.get_story_flag(self.db_path, self.player_id, "flag_fallido"))

        # Intentar otorgar un objeto no existente en el catálogo
        with self.assertRaises(ValueError):
            store.grant_story_item_once(
                self.db_path,
                self.player_id,
                "flag_fallido",
                "objeto_inexistente_en_catalogo",
            )

        # El flag NO debe haber quedado guardado tras la excepción
        self.assertFalse(store.get_story_flag(self.db_path, self.player_id, "flag_fallido"))
        self.assertNotIn("flag_fallido", store.get_player_story_flags(self.db_path, self.player_id))
        self.assertEqual(len(store.list_inventory(self.db_path, self.player_id)), 0)

    def test_story_flags_isolation_between_players(self):
        """Aislamiento estricto: los flags y grants de un personaje no afectan a otros."""
        player2_id = "test-player-002"
        self._create_test_player(player2_id, "otro_jugador")

        store.set_story_flag(self.db_path, self.player_id, "flag_exclusivo", True)
        store.grant_story_item_once(self.db_path, self.player_id, "hoja_p1", "hoja_hoshai")

        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "flag_exclusivo"))
        self.assertFalse(store.get_story_flag(self.db_path, player2_id, "flag_exclusivo"))

        self.assertEqual(len(store.list_inventory(self.db_path, self.player_id)), 1)
        self.assertEqual(len(store.list_inventory(self.db_path, player2_id)), 0)

    def test_persistence_across_reconnection_and_restart(self):
        """Los flags sobreviven al reinicio de la conexión y re-inicialización del almacén."""
        store.set_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado", True)
        store.grant_story_item_once(self.db_path, self.player_id, "hoshai_hoja_recibida", "hoja_hoshai")

        # Simular reinicio del servicio
        store.initialize(self.db_path)

        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado"))
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_hoja_recibida"))
        self.assertEqual(len(store.list_inventory(self.db_path, self.player_id)), 1)

    def test_concurrent_double_submit_protection(self):
        """Protección contra condición de carrera / doble submit concurrente."""
        flag = "hoshai_hoja_concurrente"
        results = []

        def worker():
            return store.grant_story_item_once(
                self.db_path,
                self.player_id,
                flag,
                "hoja_hoshai",
            )

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(worker) for _ in range(10)]
            results = [f.result() for f in futures]

        # Exactamente uno debió retornar True
        true_results = [r for r in results if r[0] is True]
        false_results = [r for r in results if r[0] is False]

        self.assertEqual(len(true_results), 1, "Solo una transacción concurrente debe tener éxito")
        self.assertEqual(len(false_results), 9, "Las llamadas concurrentes restantes deben ser rechazadas")

        # Exactamente 1 ítem en el inventario
        items_in_inv = [it for it in store.list_inventory(self.db_path, self.player_id) if it["item_key"] == "hoja_hoshai"]
        self.assertEqual(len(items_in_inv), 1)

    def test_schema_migration_v14_to_v15(self):
        """Verifica que una base de datos existente en v14 se actualiza limpiamente a v15."""
        mig_path = os.path.join(self.temp_dir.name, "mig_v14.sqlite3")
        # Crear base de datos simulada en v14 sin la tabla player_story_flags
        with sqlite3.connect(mig_path) as db:
            db.execute("CREATE TABLE players (id TEXT PRIMARY KEY, username TEXT, name TEXT, password_hash TEXT, status TEXT, created_at TEXT, last_access_at TEXT)")
            db.execute("PRAGMA user_version = 14")

        # Ejecutar initialize()
        store.initialize(mig_path)

        with sqlite3.connect(mig_path) as db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            self.assertEqual(version, 15)
            # La tabla player_story_flags existe
            tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
            self.assertIn("player_story_flags", tables)


if __name__ == "__main__":
    unittest.main()
