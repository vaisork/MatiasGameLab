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
                """SELECT hp_current, hp_max, fatigue, wound,
                          field_rest_budget_max, field_rest_healed
                   FROM players WHERE id = ?""", (self.player_id,)).fetchone())

    def test_schema_v14_persists_rest_cycle_and_encounter_commitment_columns(self):
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 14)
            columns = {row["name"] for row in db.execute("PRAGMA table_info(players)").fetchall()}
            encounter_columns = {row["name"] for row in db.execute("PRAGMA table_info(room_encounters)").fetchall()}
        self.assertIn("field_rest_budget_max", columns)
        self.assertIn("field_rest_healed", columns)
        self.assertIn("engaged", encounter_columns)
        state = self.raw()
        self.assertIsNone(state["field_rest_budget_max"])
        self.assertEqual(state["field_rest_healed"], 0)

    def test_v13_migration_resumes_when_columns_already_exist_or_partially_exist(self):
        # Older fixtures or an interrupted deployment can contain one or both
        # v13 columns while user_version still reports v12.
        for missing_columns in ((), ("field_rest_healed",), ("field_rest_budget_max",)):
            with self.subTest(missing_columns=missing_columns), tempfile.TemporaryDirectory() as temp:
                path = f"{temp}/vt.sqlite3"
                store.initialize(path)
                with store.connect(path) as db:
                    for column in missing_columns:
                        db.execute(f"ALTER TABLE players DROP COLUMN {column}")
                    db.execute("PRAGMA user_version = 12")

                store.initialize(path)

                with store.connect(path) as db:
                    columns = {row["name"] for row in db.execute("PRAGMA table_info(players)")}
                    self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 14)
                self.assertIn("field_rest_budget_max", columns)
                self.assertIn("field_rest_healed", columns)

    def test_budget_is_30_percent_of_missing_hp_at_cycle_start(self):
        self.set_state(hp_current=60, hp_max=100, fatigue=100, wound="ninguna",
                       field_rest_budget_max=None, field_rest_healed=0)
        results = [store.apply_field_rest(self.path, self.player_id) for _ in range(3)]
        self.assertEqual([r["healed"] for r in results], [10, 2, 0])
        state = self.raw()
        self.assertEqual(state["hp_current"], 72)
        self.assertEqual(state["field_rest_budget_max"], 12)
        self.assertEqual(state["field_rest_healed"], 12)

    def test_75_hp_fixes_budget_at_7_point_5(self):
        self.set_state(hp_current=75, hp_max=100, fatigue=100, wound="ninguna",
                       field_rest_budget_max=None, field_rest_healed=0)
        first = store.apply_field_rest(self.path, self.player_id)
        second = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(first["healed"], 7.5)
        self.assertEqual(second["healed"], 0)
        state = self.raw()
        self.assertEqual(state["hp_current"], 82.5)
        self.assertEqual(state["field_rest_budget_max"], 7.5)
        self.assertEqual(state["field_rest_healed"], 7.5)

    def test_damage_movement_restart_and_level_up_do_not_reset_or_expand_budget(self):
        self.set_state(hp_current=60, hp_max=100, fatigue=0, wound="ninguna",
                       field_rest_budget_max=None, field_rest_healed=0)
        store.apply_field_rest(self.path, self.player_id)
        first = self.raw()
        self.assertEqual(first["field_rest_budget_max"], 12)
        self.assertEqual(first["field_rest_healed"], 10)

        # Daño posterior aumenta el HP faltante pero no puede ampliar el ciclo.
        store.update_combat_state(self.path, self.player_id, hp_current=40)
        store.move_player(self.path, self.player_id, "valdren_centro")
        store.award_xp(self.path, self.player_id, combat.xp_for_next_level(1))
        after_level = self.raw()
        self.assertEqual(after_level["field_rest_budget_max"], 12)
        self.assertEqual(after_level["field_rest_healed"], 10)

        # Reinicializar la app sobre el mismo DATA_DIR simula restart.
        restarted = create_app(self.config)
        self.assertEqual(restarted.config["DATABASE"], self.path)
        after_restart = self.raw()
        self.assertEqual(after_restart["field_rest_budget_max"], 12)
        self.assertEqual(after_restart["field_rest_healed"], 10)

    def test_wound_caps_consume_only_hp_really_restored(self):
        self.set_state(hp_current=84, hp_max=100, fatigue=0, wound="moderada",
                       field_rest_budget_max=None, field_rest_healed=0)
        moderate = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(moderate["hp_current"], 85)
        self.assertEqual(moderate["healed"], 1)
        state = self.raw()
        self.assertEqual(state["field_rest_budget_max"], 4.8)
        self.assertEqual(state["field_rest_healed"], 1)

        # Nuevo ciclo simulado para el caso grave.
        self.set_state(hp_current=64, hp_max=100, fatigue=0, wound="grave",
                       field_rest_budget_max=None, field_rest_healed=0)
        grave = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(grave["hp_current"], 65)
        self.assertEqual(grave["healed"], 1)
        state = self.raw()
        self.assertAlmostEqual(state["field_rest_budget_max"], 10.8)
        self.assertEqual(state["field_rest_healed"], 1)

    def test_wound_that_blocks_healing_does_not_start_cycle(self):
        self.set_state(hp_current=90, hp_max=100, fatigue=50, wound="moderada",
                       field_rest_budget_max=None, field_rest_healed=0)
        result = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(result["healed"], 0)
        state = self.raw()
        self.assertIsNone(state["field_rest_budget_max"])
        self.assertEqual(state["field_rest_healed"], 0)
        self.assertLess(state["fatigue"], 50)

    def test_exhausted_budget_still_reduces_fatigue(self):
        self.set_state(hp_current=50, hp_max=100, fatigue=80, wound="ninguna",
                       field_rest_budget_max=12, field_rest_healed=12)
        result = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(result["healed"], 0)
        self.assertEqual(result["hp_current"], 50)
        self.assertEqual(result["fatigue"], 55)
        state = self.raw()
        self.assertEqual(state["field_rest_budget_max"], 12)
        self.assertEqual(state["field_rest_healed"], 12)

    def test_full_hp_does_not_start_cycle_or_consume_budget(self):
        self.set_state(hp_current=100, hp_max=100, fatigue=30, wound="ninguna",
                       field_rest_budget_max=None, field_rest_healed=0)
        result = store.apply_field_rest(self.path, self.player_id)
        self.assertEqual(result["healed"], 0)
        self.assertEqual(result["fatigue"], 5)
        state = self.raw()
        self.assertIsNone(state["field_rest_budget_max"])
        self.assertEqual(state["field_rest_healed"], 0)

    def test_double_requests_cannot_exceed_fixed_cycle_budget(self):
        self.set_state(hp_current=60, hp_max=100, fatigue=100, wound="ninguna",
                       field_rest_budget_max=None, field_rest_healed=0)

        def rest_once(_):
            return store.apply_field_rest(self.path, self.player_id)["healed"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            healed = list(pool.map(rest_once, range(4)))

        self.assertEqual(sum(healed), 12)
        state = self.raw()
        self.assertEqual(state["hp_current"], 72)
        self.assertEqual(state["field_rest_budget_max"], 12)
        self.assertEqual(state["field_rest_healed"], 12)


if __name__ == "__main__":
    unittest.main()
