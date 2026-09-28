"""REST-01 (#377): presupuesto persistente de curación gratuita de campo."""
import concurrent.futures
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, store


class RestBudgetIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self._register()

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def _register(self):
        self.post("/register", dict(username="resttest", name="Rest Test",
                                    password="una clave de prueba"))
        dm = self.app.test_client()
        with patch.dict("os.environ", {"VT_DM_PASSWORD": "dm-secret-value"}):
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username="resttest"), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        self.player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.path, self.player_id, "juramentado")

    def set_state(self, **values):
        assignments = ", ".join(f"{name} = ?" for name in values)
        with store.connect(self.path) as db:
            db.execute(f"UPDATE players SET {assignments} WHERE id = ?",
                       (*values.values(), self.player_id))

    def raw(self):
        with store.connect(self.path) as db:
            return dict(db.execute(
                """SELECT hp_current, hp_max, fatigue, wound, field_rest_healed
                   FROM players WHERE id = ?""", (self.player_id,)).fetchone())

    def test_schema_v13_persists_rest_budget_column(self):
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 13)
            columns = {row["name"] for row in db.execute("PRAGMA table_info(players)").fetchall()}
        self.assertIn("field_rest_healed", columns)
        self.assertEqual(self.raw()["field_rest_healed"], 0)

    def test_three_full_rests_exhaust_30_percent_budget(self):
        self.set_state(hp_current=60, hp_max=100, fatigue=100, wound="ninguna",
                       field_rest_healed=0)
        results = [store.apply_field_rest(self.path, self.player_id) for _ in range(4)]
        self.assertEqual([round(r["healed"]) for r in results], [10, 10, 10, 0])
        state = self.raw()
        self.assertEqual(state["hp_current"], 90)
        self.assertEqual(state["field_rest_healed"], 30)

    def test_partial_heal_consumes_only_actual_hp(self):
        self.set_state(hp_current=75, hp_max=100, fatigue=100, wound="ninguna",
                       field_rest_healed=0)
        results = [store.apply_field_rest(self.path, self.player_id) for _ in range(3)]
        self.assertEqual([round(r["healed"]) for r in results], [10, 10, 5])
        state = self.raw()
        self.assertEqual(state["hp_current"], 100)
        self.assertEqual(state["field_rest_healed"], 25)
        self.assertEqual(round(results[-1]["budget_remaining"]), 5)

    def test_damage_movement_restart_and_level_up_do_not_reset_budget(self):
        self.set_state(hp_current=60, hp_max=100, fatigue=0, wound="ninguna",
                       field_rest_healed=0)
        store.apply_field_rest(self.path, self.player_id)
        store.update_combat_state(self.path, self.player_id, hp_current=50)
        store.move_player(self.path, self.player_id, "valdren_centro")
        store.award_xp(self.path, self.player_id, combat.xp_for_next_level(1))
        self.assertEqual(self.raw()["field_rest_healed"], 10)

        # Reinicializar la app sobre el mismo DATA_DIR simula restart; la
        # migración no debe tocar el contador ya persistido.
        restarted = create_app(self.config)
        self.assertEqual(restarted.config["DATABASE"], self.path)
        self.assertEqual(self.raw()["field_rest_healed"], 10)

    def test_wound_caps_do_not_burn_blocked_budget(self):
        self.set_state(hp_current=84, hp_max=100, fatigue=0, wound="moderada",
                       field_rest_healed=0)
        moderate = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(moderate["hp_current"], 85)
        self.assertEqual(moderate["healed"], 1)
        self.assertEqual(self.raw()["field_rest_healed"], 1)

        self.set_state(hp_current=64, hp_max=100, fatigue=0, wound="grave",
                       field_rest_healed=0)
        grave = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(grave["hp_current"], 65)
        self.assertEqual(grave["healed"], 1)
        self.assertEqual(self.raw()["field_rest_healed"], 1)

    def test_exhausted_budget_still_reduces_fatigue(self):
        self.set_state(hp_current=50, hp_max=100, fatigue=80, wound="ninguna",
                       field_rest_healed=30)
        result = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(result["healed"], 0)
        self.assertEqual(result["hp_current"], 50)
        self.assertEqual(result["fatigue"], 55)
        self.assertEqual(self.raw()["field_rest_healed"], 30)

    def test_full_hp_does_not_consume_budget(self):
        self.set_state(hp_current=100, hp_max=100, fatigue=30, wound="ninguna",
                       field_rest_healed=10)
        result = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(result["healed"], 0)
        self.assertEqual(result["fatigue"], 5)
        self.assertEqual(self.raw()["field_rest_healed"], 10)

    def test_double_requests_cannot_exceed_budget(self):
        self.set_state(hp_current=60, hp_max=100, fatigue=100, wound="ninguna",
                       field_rest_healed=0)

        def rest_once(_):
            return store.apply_field_rest(self.path, self.player_id)["healed"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            healed = list(pool.map(rest_once, range(4)))

        self.assertEqual(round(sum(healed)), 30)
        state = self.raw()
        self.assertEqual(state["hp_current"], 90)
        self.assertEqual(state["field_rest_healed"], 30)


if __name__ == "__main__":
    unittest.main()
