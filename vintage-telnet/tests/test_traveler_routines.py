"""Pruebas exhaustivas para VT-NPC/DEV: TRAVELER-ROUTINES-01 (#338).

Contrato autoritativo (GAMEPLAY §39.11 / WORLD_POPULATION_CANON.md):
1. Registro y configuración del primer viajero N5-lite Loren (viajero_loren).
2. Cálculo determinista de posición en base al tiempo para persistent_traveler=False (sin DB).
3. Continuidad geométrica estricta: cada paso conecta con una sala vecina válida (sin teleport).
4. Comportamiento terminal: 'reverse' invierte el sentido al llegar al extremo.
5. Presencia en room_view y lista de acciones disponibles solo cuando el viajero está en esa sala.
6. Interacción conversacional N1 con Loren cuando está presente en la sala.
7. Rechazo limpio (npc_not_present) si el jugador intenta hablar con un viajero ausente de la sala.
8. Soporte para viajeros persistentes (persistent_traveler=True) con almacenamiento en tabla SQLite traveler_states.
9. Aislamiento entre múltiples viajeros y preservación de NPCs estáticos.
"""
import os
import tempfile
import time
import unittest

from server.app import create_app
from server import npc_dialogue, store, travelers, world


class TravelerRoutinesTests(unittest.TestCase):
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

        # Crear jugador aprobado en valdren_centro
        self.token = store.register(self.db_path, "tester_traveler", "Mael", "pass123456")
        self.player = dict(store.player_for_token(self.db_path, self.token))
        self.player_id = self.player["id"]
        with store.connect(self.db_path) as db:
            db.execute(
                "UPDATE players SET status = 'approved', species = 'humano', player_class = 'sombra', room = 'valdren_centro' WHERE id = ?",
                (self.player_id,)
            )
        self.player = dict(store.player_for_token(self.db_path, self.token))

    def tearDown(self):
        try:
            travelers.get_registry().reset()
        except Exception:
            pass
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_loren_registered_as_traveler(self):
        """Loren debe estar registrado con los parámetros canónicos de WORLD_POPULATION_CANON.md."""
        loren = travelers.get_registry().get("viajero_loren")
        self.assertIsNotNone(loren)
        self.assertEqual(loren.name, "Loren")
        self.assertEqual(loren.route_id, "valdren_camino_corto_01")
        self.assertEqual(len(loren.route), 12)
        self.assertEqual(loren.route[0], "valdren_centro")
        self.assertEqual(loren.route[-1], "valdren_arbol_descanso")
        self.assertEqual(loren.terminal, "reverse")
        self.assertFalse(loren.persistent_traveler, "Loren debe ser efímero y determinista sin DB")
        self.assertEqual(loren.step_seconds, 600, "10 minutos por paso según GAMEPLAY §39.11")

    def test_deterministic_position_advances_over_time(self):
        """La posición de Loren avanza paso a paso en el tiempo e invierte al llegar al final."""
        loren = travelers.get_registry().get("viajero_loren")
        step_sec = loren.step_seconds  # 600

        # Paso 0: valdren_centro
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=0), "valdren_centro")
        # Paso 1: valdren_sendero
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=step_sec * 1), "valdren_sendero")
        # Paso 2: valdren_camino_parcela
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=step_sec * 2), "valdren_camino_parcela")
        # Paso 11 (última sala de ida): valdren_arbol_descanso
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=step_sec * 11), "valdren_arbol_descanso")
        # Paso 12 (comienza regreso): valdren_zanja_vieja
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=step_sec * 12), "valdren_zanja_vieja")
        # Paso 21 (penúltima sala de regreso): valdren_sendero
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=step_sec * 21), "valdren_sendero")
        # Paso 22 (ciclo completo de 22 pasos vuelve a inicio): valdren_centro
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=step_sec * 22), "valdren_centro")
        # Paso 23 (comienza segundo ciclo hacia adelante): valdren_sendero
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=step_sec * 23), "valdren_sendero")

    def test_route_continuity_no_teleports(self):
        """En ningún momento un viajero salta entre salas no conectadas directamente."""
        loren = travelers.get_registry().get("viajero_loren")
        step_sec = loren.step_seconds

        prev_room = travelers.get_traveler_position("viajero_loren", now=0)
        # Simular 45 pasos consecutivos (más de 2 ciclos completos de ida y vuelta)
        for step in range(1, 46):
            current_room = travelers.get_traveler_position("viajero_loren", now=step * step_sec)
            prev_room_data = world.get_room(prev_room)
            self.assertIsNotNone(prev_room_data)
            # Debe existir una salida directa desde prev_room a current_room
            has_exit = any(dest == current_room for dest in prev_room_data.get("exits", {}).values())
            self.assertTrue(
                has_exit,
                f"Paso {step}: Salto ilegal sin conexión entre {prev_room} y {current_room}"
            )
            prev_room = current_room

    def test_terminal_behaviors(self):
        """Comportamientos terminales: reverse, stop, vanish."""
        route = ["sala_a", "sala_b", "sala_c"]
        # reverse: 0 -> A, 1 -> B, 2 -> C, 3 -> B, 4 -> A, 5 -> B
        t_rev = travelers.Traveler(
            npc_id="t_rev", name="TRev", role="r", species="s", town="t",
            route_id="r1", route=route, step_seconds=10, terminal="reverse"
        )
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "reverse", 0)[0], "sala_a")
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "reverse", 10)[0], "sala_b")
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "reverse", 20)[0], "sala_c")
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "reverse", 30)[0], "sala_b")
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "reverse", 40)[0], "sala_a")

        # stop: 0 -> A, 1 -> B, 2 -> C, 3 -> C, 4 -> C
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "stop", 0)[0], "sala_a")
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "stop", 20)[0], "sala_c")
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "stop", 50)[0], "sala_c")

        # vanish: 0 -> A, 1 -> B, 2 -> C, 3 -> None
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "vanish", 0)[0], "sala_a")
        self.assertEqual(travelers.calculate_deterministic_position(route, 10, "vanish", 20)[0], "sala_c")
        self.assertIsNone(travelers.calculate_deterministic_position(route, 10, "vanish", 30)[0])

    def test_loren_in_room_view_only_when_present(self):
        """Loren aparece en room_view de valdren_centro en t=0, y desaparece cuando avanza de sala."""
        # En t=0, Loren está en valdren_centro
        present_at_centro = travelers.get_travelers_in_room("valdren_centro", now=0)
        self.assertTrue(any(t["id"] == "viajero_loren" for t in present_at_centro))

        present_at_sendero = travelers.get_travelers_in_room("valdren_sendero", now=0)
        self.assertFalse(any(t["id"] == "viajero_loren" for t in present_at_sendero))

        # En t=600 (paso 1), Loren está en valdren_sendero
        present_at_centro_later = travelers.get_travelers_in_room("valdren_centro", now=600)
        self.assertFalse(any(t["id"] == "viajero_loren" for t in present_at_centro_later))

        present_at_sendero_later = travelers.get_travelers_in_room("valdren_sendero", now=600)
        self.assertTrue(any(t["id"] == "viajero_loren" for t in present_at_sendero_later))

    def test_converse_with_loren_when_present(self):
        """Hablar con Loren cuando está presente responde con su diálogo sobrio de viajero."""
        pos = travelers.get_traveler_position("viajero_loren")
        # Asegurar que el jugador está en la sala actual de Loren
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET room = ? WHERE id = ?", (pos, self.player_id))
        self.player = dict(store.player_for_token(self.db_path, self.token))

        result = npc_dialogue.converse(
            self.player,
            "viajero_loren",
            message="¿Qué noticias traes del camino?",
            room_id=pos,
            db_path=self.db_path,
        )
        self.assertTrue(result.success)
        self.assertEqual(result.npc_name, "Loren")
        self.assertFalse(result.is_fallback)
        self.assertTrue(any(w in result.text for w in ("Valdren", "camino", "campos", "llanos", "recados", "Veyra")))

    def test_converse_with_loren_fails_when_not_present(self):
        """Intentar hablar con Loren cuando no está en la misma sala del jugador es rechazado limpiamente."""
        loren_pos = travelers.get_traveler_position("viajero_loren")
        other_room = "valdren_arbol_descanso" if loren_pos != "valdren_arbol_descanso" else "valdren_centro"

        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET room = ? WHERE id = ?", (other_room, self.player_id))
        self.player = dict(store.player_for_token(self.db_path, self.token))

        result = npc_dialogue.converse(
            self.player,
            "viajero_loren",
            message="Hola Loren",
            room_id=other_room,
            db_path=self.db_path,
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error, "npc_not_present")
        self.assertIn("no está en este lugar", result.reason)

    def test_terminal_api_talk_loren_integration(self):
        """El endpoint /api/talk con Loren funciona de forma autoritativa cuando está presente."""
        pos = travelers.get_traveler_position("viajero_loren")
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET room = ? WHERE id = ?", (pos, self.player_id))

        with self.client.session_transaction() as sess:
            sess["token"] = self.token
            sess["csrf"] = "test-csrf"

        resp = self.client.post("/api/talk", json={"target": "Loren", "message": "saludos", "csrf": "test-csrf"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertTrue(data["accepted"])
        self.assertEqual(data["npc"], "viajero_loren")
        self.assertEqual(data["npc_name"], "Loren")
        self.assertTrue(len(data["reply"]) > 0)

    def test_persistent_traveler_advances_and_persists_in_db(self):
        """Un viajero configurado con persistent_traveler=True almacena su avance en la base de datos."""
        custom_route = ["valdren_centro", "valdren_sendero", "valdren_camino_parcela"]
        custom_traveler = travelers.Traveler(
            npc_id="mensajero_test_01",
            name="Mensajero",
            role="mensajero de prueba",
            species="Humano",
            town="Valdren",
            route_id="ruta_prueba_01",
            route=custom_route,
            step_seconds=100,
            terminal="reverse",
            persistent_traveler=True,
        )
        travelers.get_registry().register(custom_traveler)

        # Primer acceso en t=1000: se inicializa en ruta[0]
        pos0 = travelers.get_traveler_position("mensajero_test_01", now=1000.0, db_path=self.db_path)
        self.assertEqual(pos0, "valdren_centro")

        state0 = store.get_traveler_state(self.db_path, "mensajero_test_01")
        self.assertIsNotNone(state0)
        self.assertEqual(state0["current_room"], "valdren_centro")
        self.assertEqual(state0["step_index"], 0)

        # Transcurren 150 segundos (1 paso): debe avanzar a valdren_sendero
        pos1 = travelers.get_traveler_position("mensajero_test_01", now=1150.0, db_path=self.db_path)
        self.assertEqual(pos1, "valdren_sendero")

        state1 = store.get_traveler_state(self.db_path, "mensajero_test_01")
        self.assertEqual(state1["current_room"], "valdren_sendero")
        self.assertEqual(state1["step_index"], 1)

        # Transcurren otros 100 segundos: debe avanzar a valdren_camino_parcela
        pos2 = travelers.get_traveler_position("mensajero_test_01", now=1250.0, db_path=self.db_path)
        self.assertEqual(pos2, "valdren_camino_parcela")

        state2 = store.get_traveler_state(self.db_path, "mensajero_test_01")
        self.assertEqual(state2["current_room"], "valdren_camino_parcela")
        self.assertEqual(state2["step_index"], 2)

    def test_traveler_isolation(self):
        """Múltiples viajeros tienen rutas y estados independientes."""
        loren_pos = travelers.get_traveler_position("viajero_loren", now=600)
        self.assertEqual(loren_pos, "valdren_sendero")

        other_route = ["khariel_centro", "khariel_terrazas"]
        t2 = travelers.Traveler(
            npc_id="viajero_khariel_01",
            name="Caminante",
            role="viajero",
            species="Felaryn",
            town="Khariel",
            route_id="khariel_ruta_01",
            route=other_route,
            step_seconds=300,
            persistent_traveler=False,
        )
        travelers.get_registry().register(t2)

        t2_pos = travelers.get_traveler_position("viajero_khariel_01", now=600)
        self.assertEqual(t2_pos, "khariel_centro")  # 600 // 300 = 2 pasos en ciclo de 2 -> vuelta al inicio

        # Loren no fue afectado
        self.assertEqual(travelers.get_traveler_position("viajero_loren", now=600), "valdren_sendero")

    def test_static_npcs_unaffected(self):
        """Los NPCs estáticos tradicionales (como Daro) siguen funcionando normalmente."""
        registry = npc_dialogue.get_registry()
        daro = registry.get("daro_herrero")
        self.assertIsNotNone(daro)
        self.assertEqual(daro["location"], "valdren_forja")
        self.assertFalse(travelers.is_traveler("daro_herrero"))


if __name__ == "__main__":
    unittest.main()
