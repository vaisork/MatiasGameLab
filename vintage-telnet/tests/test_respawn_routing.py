"""Regresiones del selector autoritativo de respawn (#478/#479)."""

import os
import tempfile
import unittest

from server import respawn, store, world


class RespawnRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.temp.name, "vintage.sqlite3")
        store.initialize(self.path)
        self.token = store.register(self.path, "respawn_tester", "Respawn Tester", "pass123456")
        self.player = dict(store.player_for_token(self.path, self.token))
        self.player_id = self.player["id"]
        with store.connect(self.path) as db:
            db.execute(
                """UPDATE players
                   SET status = 'approved', species = 'humano',
                       player_class = 'juramentado'
                   WHERE id = ?""",
                (self.player_id,),
            )
        self.player = dict(store.player_for_token(self.path, self.token))

    def tearDown(self):
        self.temp.cleanup()

    def test_edran_uses_authorized_valdren_anchor(self):
        self.assertEqual(world.get_room_region("valdren_camino_parcela"), "edran")
        self.assertEqual(
            respawn.select_respawn_room(self.player_id, "valdren_camino_parcela"),
            "valdren_centro",
        )

    def test_region_without_anchor_falls_back_to_personal_home(self):
        self.assertEqual(world.get_room_region("alto_terrazas"), "hoshai")
        self.assertEqual(
            respawn.select_respawn_room(self.player_id, "alto_terrazas"),
            world.get_home_room_id(self.player_id),
        )

    def test_apply_respawn_persists_canonical_state_and_resets_rest_budget(self):
        with store.connect(self.path) as db:
            db.execute(
                """UPDATE players
                   SET room = 'alto_terrazas', wound = 'grave',
                       field_rest_budget_max = 12, field_rest_healed = 12
                   WHERE id = ?""",
                (self.player_id,),
            )
        player = dict(store.player_for_token(self.path, self.token))
        result = respawn.apply_player_respawn(
            self.path,
            player,
            current_wound="grave",
            death_room_id="alto_terrazas",
        )

        expected_home = world.get_home_room_id(self.player_id)
        self.assertEqual(result["room_id"], expected_home)
        self.assertEqual(result["hp_current"], round(player["hp_max"] * 0.60))
        self.assertEqual(result["fatigue"], 40)
        self.assertEqual(result["wound"], "moderada")

        persisted = dict(store.player_for_token(self.path, self.token))
        self.assertEqual(persisted["room"], expected_home)
        self.assertEqual(persisted["hp_current"], round(player["hp_max"] * 0.60))
        self.assertEqual(persisted["fatigue"], 40)
        self.assertEqual(persisted["wound"], "moderada")
        self.assertIsNone(persisted["field_rest_budget_max"])
        self.assertEqual(persisted["field_rest_healed"], 0)

        # Reconnect lógico: la misma sesión/token conserva el destino y estado.
        reconnected = dict(store.player_for_token(self.path, self.token))
        self.assertEqual(reconnected["room"], expected_home)
        self.assertEqual(reconnected["hp_current"], persisted["hp_current"])
        self.assertEqual(reconnected["fatigue"], 40)

    def test_home_fallback_is_a_real_safe_dynamic_room(self):
        home_id = respawn.select_respawn_room(self.player_id, "alto_terrazas")
        room = world.get_room(home_id)
        self.assertIsNotNone(room)
        self.assertEqual(room["id"], home_id)
        self.assertTrue(world.is_home_room(home_id))


if __name__ == "__main__":
    unittest.main()
