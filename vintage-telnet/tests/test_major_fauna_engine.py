"""Pruebas exhaustivas para VT-GAME/DEV: MAJOR-FAUNA-ENGINE-01 (#336).

Contrato autoritativo (GAMEPLAY §38 / Issue #336 / Issue #339):
1. Registro exacto del perfil y estadísticas canónicas de Cargallanura v1 (§38.7).
2. Evaluación como Abrumador por un personaje de nivel 1 (§38.10 criterio 2).
3. Presencia compartida determinista por major_epoch (30 min) sin reroll por entrar/salir/reconnect.
4. Territorio en 3 anillos:
   - Anillo I (borde): señales, 0 combate forzado, retirada libre (§38.3, §38.10).
   - Anillo II (activo): rastro reciente / avistamiento, 0 combate forzado (§38.3, §38.10).
   - Anillo III (crítico): decisión real previa (observar, retirarse, provocar). NUNCA emboscada (§38.3).
5. Acción preparada 'cargallanura_charge': señal previa (telegraph) e intervención/defensa (§38.8).
6. Huida durante combate: huida exitosa corta la persecución y no persigue entre salas (§38.4, §38.9).
7. Derrota del jugador: muerte/respawn en Valdren, NO pérdida de arma ni equipo (§38.5).
8. Derrota de la criatura: XP normal con antifarmeo regular de familia, NO trofeo de jefe (§38.6).
9. Aislamiento absoluto de pools aleatorios ordinarios C1/C2 (§38.10 criterio 9).
10. Integración con room_view en el servidor web/API.
"""
import os
import random
import tempfile
import unittest

from server.app import create_app
from server import combat, creatures, encounters, major_fauna, store, world


class MajorFaunaEngineTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "vintage.sqlite3")
        store.initialize(self.db_path)

        self.app = create_app({
            "TESTING": True,
            "DATA_DIR": self.temp_dir.name,
            "SECRET_KEY": "test-secret-" * 4,
            "SESSION_COOKIE_SECURE": False,
        })
        self.client = self.app.test_client()

        # Crear jugador aprobado para pruebas
        self.token = store.register(self.db_path, "tester_c4", "Boran", "pass123456")
        self.player = dict(store.player_for_token(self.db_path, self.token))
        self.player_id = self.player["id"]
        with store.connect(self.db_path) as db:
            db.execute(
                "UPDATE players SET status = 'approved', species = 'humano', player_class = 'juramentado', room = 'valdren_centro' WHERE id = ?",
                (self.player_id,)
            )
        self.player = dict(store.player_for_token(self.db_path, self.token))

    def tearDown(self):
        try:
            major_fauna.get_registry().reset()
        except Exception:
            pass
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_cargallanura_spec_and_registration(self):
        """Cargallanura debe estar registrada en creatures y major_fauna con los números de GAMEPLAY §38.7."""
        # 1. En creatures.py
        c = creatures.get_creature("cargallanura")
        self.assertIsNotNone(c)
        self.assertEqual(c["name"], "Cargallanura")
        self.assertEqual(c["reference_level"], 12)
        self.assertEqual(c["hp"], 210)
        self.assertEqual(c["precision"], 58)
        self.assertEqual(c["damage"], 26)
        self.assertEqual(c["armor_reduction"], 0.25)
        self.assertEqual(c["flee_agilidad"], 10)
        self.assertEqual(c["flee_percepcion"], 12)

        # 2. En major_fauna.py
        spec = major_fauna.get_registry().get_spec("cargallanura")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.reference_level, 12)
        self.assertEqual(spec.hp, 210)
        self.assertTrue(spec.no_weapon_loss, "Fauna mayor nunca causa pérdida de arma")
        self.assertTrue(spec.no_boss_reward, "Fauna mayor nunca otorga trofeo de jefe")

    def test_evaluation_overwhelming_at_level_1(self):
        """Un personaje de nivel 1 debe evaluar a Cargallanura como Abrumador (GAMEPLAY §38.10)."""
        spec = major_fauna.get_registry().get_spec("cargallanura")
        diff = major_fauna.evaluate_encounter_difficulty(player_level=1, spec=spec)
        self.assertEqual(diff, "abrumador")

    def test_deterministic_shared_presence_by_epoch(self):
        """La presencia compartida es determinista por major_epoch (30 min) y no rerollea por jugador."""
        zone = major_fauna.get_registry().get_zone("edran_corredor_cargallanura")
        self.assertIsNotNone(zone)

        epoch_0 = major_fauna.get_major_epoch(now=0)
        epoch_1 = major_fauna.get_major_epoch(now=1800)
        epoch_2 = major_fauna.get_major_epoch(now=3600)

        # El resultado para t=0 y t=100 (misma epoch) debe ser exactamente el mismo
        p0_a = major_fauna.is_major_fauna_present(zone, now=0)
        p0_b = major_fauna.is_major_fauna_present(zone, now=100)
        p0_c = major_fauna.is_major_fauna_present(zone, now=1799)
        self.assertEqual(p0_a, p0_b)
        self.assertEqual(p0_a, p0_c)

        # Distintas épocas pueden tener distintos valores según la probabilidad del 40%
        results = [major_fauna.is_major_fauna_present(zone, now=i * 1800) for i in range(100)]
        true_count = sum(1 for r in results if r)
        # En 100 épocas al 40%, esperamos entre 25 y 55 resultados verdaderos
        self.assertTrue(25 <= true_count <= 55, f"Distribución observada: {true_count}/100")

    def test_ring_1_signals_and_no_forced_combat(self):
        """Anillo I muestra rastros de borde, retirada libre y 0 combate forzado."""
        zone = major_fauna.get_registry().get_zone("edran_corredor_cargallanura")
        room_r1 = zone.ring_1_rooms[0]  # edran_senda_viento_bajo

        view_data = major_fauna.get_zone_view_data(room_r1, now=0, db_path=self.db_path)
        self.assertIsNotNone(view_data)
        self.assertEqual(view_data["ring"], 1)
        self.assertFalse(view_data["forced_combat"], "Anillo I nunca fuerza combate")
        self.assertIn("retirarse", view_data["options"])
        self.assertTrue(any("Huellas" in s or "fauna menor" in s for s in view_data["signals"]))

    def test_ring_2_active_territory_and_no_forced_combat(self):
        """Anillo II muestra territorio activo y avistamiento si está presente, 0 combate forzado."""
        zone = major_fauna.get_registry().get_zone("edran_corredor_cargallanura")
        room_r2 = zone.ring_2_rooms[0]

        # Encontrar una epoch donde esté presente
        present_epoch_time = None
        for i in range(50):
            t = i * 1800
            if major_fauna.is_major_fauna_present(zone, now=t):
                present_epoch_time = t
                break
        self.assertIsNotNone(present_epoch_time)

        view_data = major_fauna.get_zone_view_data(room_r2, now=present_epoch_time, db_path=self.db_path)
        self.assertEqual(view_data["ring"], 2)
        self.assertTrue(view_data["present"])
        self.assertFalse(view_data["forced_combat"], "Anillo II nunca fuerza combate")
        self.assertIn("retirarse", view_data["options"])
        self.assertTrue(any("silueta maciza" in s or "Cargallanura" in s for s in view_data["signals"]))

    def test_ring_3_critical_proximity_and_explicit_decision(self):
        """Anillo III concede decisión real previa (observar/retirarse/provocar). NUNCA emboscada."""
        zone = major_fauna.get_registry().get_zone("edran_corredor_cargallanura")
        room_r3 = zone.ring_3_rooms[0]

        # Buscar epoch presente
        present_t = next(t for t in (i * 1800 for i in range(50)) if major_fauna.is_major_fauna_present(zone, now=t))
        view_present = major_fauna.get_zone_view_data(room_r3, now=present_t, db_path=self.db_path)
        self.assertEqual(view_present["ring"], 3)
        self.assertTrue(view_present["present"])
        self.assertFalse(view_present["forced_combat"], "NUNCA emboscada automática")
        self.assertTrue(view_present["decision_required"])
        self.assertIn("observar", view_present["options"])
        self.assertIn("retirarse", view_present["options"])
        self.assertIn("provocar_combate", view_present["options"])

        # Buscar epoch ausente
        absent_t = next(t for t in (i * 1800 for i in range(50)) if not major_fauna.is_major_fauna_present(zone, now=t))
        view_absent = major_fauna.get_zone_view_data(room_r3, now=absent_t, db_path=self.db_path)
        self.assertEqual(view_absent["ring"], 3)
        self.assertFalse(view_absent["present"])
        self.assertFalse(view_absent["decision_required"])
        self.assertNotIn("provocar_combate", view_absent["options"])

    def test_prepared_action_charge_telegraph_and_intervention(self):
        """La carga de Cargallanura anuncia señal previa y puede ser interrumpida o defendida."""
        spec = major_fauna.get_registry().get_spec("cargallanura")
        charge = spec.prepared_actions["cargallanura_charge"]

        self.assertTrue(charge.frontal)
        self.assertTrue(charge.interruptible)
        self.assertEqual(charge.precision, 70)
        self.assertEqual(charge.damage, 38)
        self.assertIn("baja la cabeza", charge.telegraph_text)

        # 1. Intervención con interrupción exitosa
        rng_success = random.Random(1)
        res_int = major_fauna.resolve_major_fauna_charge_round(
            spec, "cargallanura_charge", player_action="interrumpir", player_attrs={"destreza": 18, "percepcion": 18}, rng=rng_success
        )
        self.assertTrue(res_int["interrupted"])
        self.assertFalse(res_int["hits"])
        self.assertEqual(res_int["damage"], 0)

        # 2. Defensa activa con esquivar
        rng_dodge = random.Random(42)
        res_dodge = major_fauna.resolve_major_fauna_charge_round(
            spec, "cargallanura_charge", player_action="esquivar", player_attrs={"agilidad": 16, "percepcion": 14}, rng=rng_dodge
        )
        self.assertIn("Esquiva" in res_dodge["message"] or "apartas" in res_dodge["message"] or "esquivar" in res_dodge["message"], [True])

        # 3. Resolución sin defensa: daño bruto de 38 si impacta
        rng_hit = random.Random(10)
        res_hit = major_fauna.resolve_major_fauna_charge_round(
            spec, "cargallanura_charge", player_action="esperar", rng=rng_hit
        )
        if res_hit["hits"]:
            self.assertEqual(res_hit["damage"], 38)

    def test_flee_terminates_pursuit(self):
        """Huida exitosa corta la persecución y no persigue entre salas (GAMEPLAY §38.4)."""
        spec = major_fauna.get_registry().get_spec("cargallanura")
        player_mock = {"attr_agilidad": 16, "attr_percepcion": 14, "wound": "ninguna", "fatigue": 0}

        # Con agilidad y percepción altas se logra escapar
        rng = random.Random(7)
        res_flee = major_fauna.resolve_major_fauna_flee(player_mock, spec, rng=rng)
        self.assertTrue(res_flee["success"])
        self.assertTrue(res_flee["pursuit_ended"])
        self.assertIn("no te persigue", res_flee["message"])

    def test_player_defeat_respawns_and_preserves_weapons(self):
        """Muerte frente a fauna mayor NO activa pérdida de arma ni equipo (GAMEPLAY §38.5)."""
        spec = major_fauna.get_registry().get_spec("cargallanura")

        res_defeat = major_fauna.resolve_major_fauna_player_defeat(self.db_path, self.player, spec)
        self.assertEqual(res_defeat["outcome"], "player_defeated")
        self.assertFalse(res_defeat["weapon_lost"], "No hay pérdida de arma por fauna mayor")
        self.assertTrue(res_defeat["equipment_preserved"])
        self.assertEqual(res_defeat["respawn_room"], "valdren_centro")

        # Comprobar en DB que el jugador está en valdren_centro y vivo
        p_after = store.player_for_token(self.db_path, self.token)
        self.assertEqual(p_after["room"], "valdren_centro")
        self.assertEqual(p_after["hp_current"], 20)

    def test_creature_defeat_awards_xp_and_no_boss_trophies(self):
        """Victoria otorga XP regular con antifarmeo, sin loot de jefe ni trofeos, y fija cooldown."""
        spec = major_fauna.get_registry().get_spec("cargallanura")
        zone = major_fauna.get_registry().get_zone("edran_corredor_cargallanura")

        # Estado inicial de XP
        initial_xp = self.player["xp"]
        epoch_t = 1800 * 5

        res_win = major_fauna.resolve_major_fauna_defeat(self.db_path, self.player, spec, zone, now=epoch_t)
        self.assertEqual(res_win["outcome"], "creature_defeated")
        self.assertFalse(res_win["boss_reward"])
        self.assertFalse(res_win["trophy_granted"])
        self.assertGreater(res_win["xp_awarded"], 0)

        # Verificar cooldown registrado en DB
        state = store.get_major_fauna_state(self.db_path, zone.zone_id)
        self.assertIsNotNone(state)
        self.assertEqual(state["last_defeated_epoch"], 5)

        # Ahora en esa misma epoch la presencia debe ser False independientemente del hash
        self.assertFalse(major_fauna.is_major_fauna_present(zone, now=epoch_t, db_path=self.db_path))

    def test_cargallanura_isolated_from_c1_pools(self):
        """Cargallanura nunca puede entrar en pools ordinarios C1 (GAMEPLAY §38.10)."""
        self.assertIn("cargallanura", encounters.C4_MAJOR_FAUNA_IDS)
        for pool_id, pool in encounters.RANDOM_ENCOUNTER_POOLS.items():
            creature_ids = [c_id for c_id, _ in pool["creatures"]]
            self.assertNotIn(
                "cargallanura",
                creature_ids,
                f"Cargallanura no puede estar en pool ordinario {pool_id}"
            )

        # Validar que intentar añadirla a un pool arroja InvalidPoolConfig
        invalid_pool = {
            "test_illegal_pool": {
                "rooms": {"valdren_sendero"},
                "chance": 0.20,
                "creatures": [("cargallanura", 50)],
            }
        }
        with self.assertRaises(encounters.InvalidPoolConfig):
            encounters.validate_pools(invalid_pool)

    def test_room_view_major_fauna_integration(self):
        """room_view expone major_fauna y las acciones contextualmente."""
        zone = major_fauna.get_registry().get_zone("edran_corredor_cargallanura")
        room_r1 = zone.ring_1_rooms[0]

        # Mover al jugador a la sala de Anillo 1
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET room = ? WHERE id = ?", (room_r1, self.player_id))

        with self.client.session_transaction() as sess:
            sess["token"] = self.token
            sess["csrf"] = "test-csrf"

        resp = self.client.get("/api/room")
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertIn("room", data)
        self.assertIn("major_fauna", data["room"])
        self.assertEqual(data["room"]["major_fauna"]["ring"], 1)
        self.assertFalse(data["room"]["major_fauna"]["forced_combat"])


if __name__ == "__main__":
    unittest.main()
