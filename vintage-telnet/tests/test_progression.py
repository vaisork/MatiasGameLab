"""Pruebas de progresión y recuperación (GAMEPLAY.md §19, §24.7 y §25):
coste de atributos, gasto de PA desde el panel Personaje, PP por nivel
múltiplo de 5, subida de nivel sin curación completa y recuperación
pasiva de fatiga calculada por tiempo en servidor."""
import re
import sqlite3
import tempfile
import time
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, store


# --- combat.py: reglas puras -------------------------------------------------

class ProgressionMathTests(unittest.TestCase):
    def test_attribute_cost_matches_gameplay_19_table(self):
        for value, cost in [(10, 1), (19, 1), (20, 2), (34, 2), (35, 3), (44, 3),
                            (45, 4), (59, 4), (60, 5), (80, 5)]:
            self.assertEqual(combat.attribute_cost(value), cost, value)

    def test_pp_gained_counts_levels_multiple_of_five(self):
        self.assertEqual(combat.pp_gained(1, 4), 0)
        self.assertEqual(combat.pp_gained(4, 5), 1)
        self.assertEqual(combat.pp_gained(5, 6), 0)
        self.assertEqual(combat.pp_gained(3, 11), 2)
        self.assertEqual(combat.pp_gained(99, 100), 1)

    def test_hp_after_max_change_follows_gameplay_25_6_examples(self):
        # 100/100 -> max 102: queda 102/102.
        self.assertEqual(combat.hp_after_max_change(100, 100, 102), 102)
        # 60/100 -> max 102: queda 62/102, no curación completa.
        self.assertEqual(combat.hp_after_max_change(60, 100, 102), 62)
        # Un máximo que no sube no cura nada.
        self.assertEqual(combat.hp_after_max_change(60, 100, 100), 60)


# --- Integración contra el servidor real ------------------------------------

class ProgressionIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self.register_and_enter_world()

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def register_and_enter_world(self, username="matias", name="Matías"):
        self.post("/register", dict(username=username, name=name, password="una clave de prueba"))
        dm = self.app.test_client()
        with patch.dict("os.environ", {"VT_DM_PASSWORD": "dm-secret-value"}):
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))  # arranca en valdren_centro

    def player_id(self):
        return self.client.get("/api/me").json["player"]["id"]

    def character(self):
        return self.client.get("/api/character").json

    def spend(self, attribute, current_value):
        return self.client.post("/api/character/attributes", json=dict(
            attribute=attribute, current_value=current_value, csrf=self.csrf()))

    def set_columns(self, **values):
        assignments = ", ".join(f"{name} = ?" for name in values)
        with store.connect(self.path) as db:
            db.execute(f"UPDATE players SET {assignments} WHERE id = ?",
                       (*values.values(), self.player_id()))

    # --- 25.1 / 25.6 / 25.8: subir de nivel ---------------------------------

    def test_level_up_does_not_fully_heal_and_grants_pa(self):
        player_id = self.player_id()
        self.set_columns(hp_current=60)
        state = store.award_xp(self.path, player_id, combat.xp_for_next_level(1))
        self.assertEqual(state["level"], 2)
        self.assertEqual(state["pa_gained"], 2)
        new_max = combat.hp_max(2, 10, 10)
        self.assertAlmostEqual(state["hp_max"], new_max)
        self.assertAlmostEqual(state["hp_current"], 60 + (new_max - 100))
        character = self.character()
        self.assertEqual(character["pa_unspent"], 2)
        self.assertLess(character["hp_current"], character["hp_max"])

    def test_reaching_level_five_grants_one_pp(self):
        xp_to_five = sum(combat.xp_for_next_level(level) for level in range(1, 5))
        state = store.award_xp(self.path, self.player_id(), xp_to_five)
        self.assertEqual(state["level"], 5)
        self.assertEqual(state["pp_gained"], 1)
        self.assertEqual(state["pa_gained"], 8)
        self.assertEqual(self.character()["pp_unspent"], 1)

    # --- 25.4 / 25.5 / 25.7: gasto de PA -------------------------------------

    def test_character_exposes_costs_pp_and_combat_flag(self):
        character = self.character()
        self.assertEqual(character["pp_unspent"], 0)
        self.assertEqual(character["attribute_costs"], {name: 1 for name in combat.ATTRIBUTES})
        self.assertFalse(character["in_combat"])

    def test_spend_pa_raises_attribute_and_charges_cost(self):
        self.set_columns(pa_unspent=3, attr_fuerza=19)
        response = self.spend("fuerza", 19)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["accepted"])
        self.assertEqual(response.json["value"], 20)
        self.assertEqual(response.json["cost"], 1)
        self.assertEqual(response.json["next_cost"], 2)
        character = self.character()
        self.assertEqual(character["attributes"]["fuerza"], 20)
        self.assertEqual(character["pa_unspent"], 2)
        self.assertEqual(character["attribute_costs"]["fuerza"], 2)

    def test_spend_pa_rejects_insufficient_points_without_changes(self):
        self.set_columns(pa_unspent=1, attr_fuerza=20)
        response = self.spend("fuerza", 20)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json["reason"], "not_enough_pa")
        character = self.character()
        self.assertEqual(character["attributes"]["fuerza"], 20)
        self.assertEqual(character["pa_unspent"], 1)

    def test_spend_pa_requires_matching_confirmation(self):
        self.set_columns(pa_unspent=2)
        missing = self.client.post("/api/character/attributes",
                                   json=dict(attribute="fuerza", csrf=self.csrf()))
        self.assertEqual(missing.status_code, 400)
        self.assertEqual(missing.json["reason"], "confirmation_required")
        stale = self.spend("fuerza", 11)  # el jugador vio un valor que ya no es el actual
        self.assertEqual(stale.status_code, 409)
        self.assertEqual(stale.json["reason"], "stale_confirmation")
        self.assertEqual(self.character()["pa_unspent"], 2)

    def test_same_confirmation_cannot_spend_twice(self):
        self.set_columns(pa_unspent=2)
        self.assertTrue(self.spend("agilidad", 10).json["accepted"])
        repeated = self.spend("agilidad", 10)
        self.assertEqual(repeated.json["reason"], "stale_confirmation")
        character = self.character()
        self.assertEqual(character["attributes"]["agilidad"], 11)
        self.assertEqual(character["pa_unspent"], 1)

    def test_spend_pa_rejects_unknown_attribute(self):
        self.set_columns(pa_unspent=2)
        response = self.spend("suerte", 10)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["reason"], "unknown_attribute")

    def test_spend_pa_blocked_in_combat(self):
        self.set_columns(pa_unspent=2)
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela: aparece Mordelinde
        self.assertTrue(self.character()["in_combat"])
        response = self.spend("fuerza", 10)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json["reason"], "in_combat")
        self.assertEqual(self.character()["pa_unspent"], 2)

    def test_spending_resistencia_raises_hp_by_difference_only(self):
        self.set_columns(pa_unspent=1, hp_current=50)
        before = self.character()
        response = self.spend("resistencia", 10)
        self.assertTrue(response.json["accepted"])
        new_max = combat.hp_max(1, 11, 10)
        self.assertAlmostEqual(response.json["hp_max"], new_max)
        self.assertAlmostEqual(response.json["hp_current"], 50 + (new_max - before["hp_max"]))

    def test_spend_pa_requires_login(self):
        anonymous = self.app.test_client()
        response = anonymous.post("/api/character/attributes",
                                  json=dict(attribute="fuerza", current_value=10,
                                            csrf=self.csrf(client=anonymous)))
        self.assertEqual(response.status_code, 401)

    # --- 24.7: recuperación pasiva de fatiga ---------------------------------

    def test_fatigue_recovers_one_point_per_ten_seconds_out_of_combat(self):
        self.set_columns(fatigue=40, fatigue_updated_at=time.time() - 95)
        self.assertEqual(self.character()["fatigue"], 31)
        # El resto del intervalo (5 s) se conserva: no se recupera de nuevo al instante.
        self.assertEqual(self.character()["fatigue"], 31)

    def test_fatigue_recovery_stops_at_zero_and_ignores_hp_and_wounds(self):
        self.set_columns(fatigue=5, fatigue_updated_at=time.time() - 600,
                         hp_current=40, wound="leve")
        character = self.character()
        self.assertEqual(character["fatigue"], 0)
        self.assertEqual(character["hp_current"], 40)
        self.assertEqual(character["wound"], "leve")

    def test_fatigue_does_not_recover_during_combat(self):
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # combate activo con Mordelinde
        self.set_columns(fatigue=40, fatigue_updated_at=time.time() - 300)
        self.assertEqual(self.character()["fatigue"], 40)

    def test_explicit_fatigue_change_restarts_recovery_clock(self):
        store.update_combat_state(self.path, self.player_id(), fatigue=30)
        # Justo después de un esfuerzo, todavía no hay recuperación.
        self.assertEqual(self.character()["fatigue"], 30)
        with store.connect(self.path) as db:
            clock = db.execute("SELECT fatigue_updated_at FROM players WHERE id = ?",
                               (self.player_id(),)).fetchone()[0]
        self.assertAlmostEqual(clock, time.time(), delta=5)


class SchemaV8MigrationTests(unittest.TestCase):
    def test_v7_players_receive_pp_for_levels_already_reached(self):
        with tempfile.TemporaryDirectory() as temp:
            path = f"{temp}/vt.sqlite3"
            store.initialize(path)
            with store.connect(path) as db:
                db.execute(
                    """INSERT INTO players(id, username, name, password_hash, status, species, room,
                                           created_at, last_access_at, level)
                       VALUES ('p1', 'veterano', 'Veterano', 'x', 'approved', 'humano',
                               'valdren_centro', 'now', 'now', 12)""")
            # Simula una base v7 real: sin las columnas de v8.
            raw = sqlite3.connect(path)
            raw.execute("ALTER TABLE players DROP COLUMN pp_unspent")
            raw.execute("ALTER TABLE players DROP COLUMN fatigue_updated_at")
            raw.execute("PRAGMA user_version = 7")
            raw.commit()
            raw.close()
            store.initialize(path)
            with store.connect(path) as db:
                self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
                row = db.execute("SELECT pp_unspent, fatigue_updated_at FROM players WHERE id = 'p1'").fetchone()
            self.assertEqual(row["pp_unspent"], 2)  # niveles 5 y 10
            self.assertIsNone(row["fatigue_updated_at"])


if __name__ == "__main__":
    unittest.main()
