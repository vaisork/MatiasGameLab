"""Regresiones para el camino de esquema 14/17 a 18 sin perder estado vivo."""
import tempfile
import unittest
from pathlib import Path

from server import store


class SchemaReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "game.sqlite3")
        store.initialize(self.db_path)
        store.register(self.db_path, "migracion", "Jugador Migracion", "hash")
        with store.connect(self.db_path) as db:
            self.player_id = db.execute("SELECT id FROM players").fetchone()["id"]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_new_database_has_all_schema_22_features(self):
        with store.connect(self.db_path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
            tables = {r["name"] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertTrue({"player_story_flags", "economy_ledger", "player_threat_states",
                             "world_boss_states", "boss_attempts", "boss_attempt_participants",
                             "player_lost_weapons", "boss_rewards_claimed", "traveler_states",
                             "major_fauna_states", "player_presence"} <= tables)
            encounter_cols = {r["name"] for r in db.execute("PRAGMA table_info(room_encounters)")}
            self.assertTrue({"engaged", "signature_cooldown", "apertura", "prepared_action"} <= encounter_cols)

    def test_v17_upgrade_preserves_wallet_flags_and_player_data(self):
        store.set_story_flag(self.db_path, self.player_id, "migration_test")
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET sellos=47, level=3 WHERE id=?", (self.player_id,))
            db.execute("DROP TABLE player_threat_states")
            db.execute("PRAGMA user_version=17")
        store.initialize(self.db_path)
        with store.connect(self.db_path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
            player = db.execute("SELECT id, name, level, sellos FROM players").fetchone()
            self.assertEqual((player["id"], player["name"], player["level"], player["sellos"]),
                             (self.player_id, "Jugador Migracion", 3, 47))
            self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "migration_test"))
            ledger = db.execute("SELECT COUNT(*) AS n FROM economy_ledger WHERE player_id=?", (self.player_id,)).fetchone()["n"]
            self.assertEqual(ledger, 1)
            self.assertIsNotNone(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player_threat_states'").fetchone())

    def test_v14_upgrade_applies_all_steps_and_keeps_encounter(self):
        store.start_encounter(self.db_path, self.player_id, "valdren_centro", "mordelinde", 31)
        with store.connect(self.db_path) as db:
            db.execute("DELETE FROM economy_ledger")
            db.execute("DROP TABLE economy_ledger")
            db.execute("DROP TABLE player_story_flags")
            db.execute("ALTER TABLE players DROP COLUMN sellos")
            for column in ("signature_cooldown", "apertura", "prepared_action"):
                db.execute(f"ALTER TABLE room_encounters DROP COLUMN {column}")
            db.execute("PRAGMA user_version=14")
        store.initialize(self.db_path)
        with store.connect(self.db_path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
            encounter = db.execute("SELECT creature_id, hp_current, engaged, signature_cooldown, apertura, prepared_action FROM room_encounters").fetchone()
            self.assertEqual((encounter["creature_id"], encounter["hp_current"], encounter["engaged"]),
                             ("mordelinde", 31, 1))
            self.assertEqual((encounter["signature_cooldown"], encounter["apertura"], encounter["prepared_action"]),
                             (0, 0, None))
            player = db.execute("SELECT id, sellos FROM players").fetchone()
            self.assertEqual((player["id"], player["sellos"]), (self.player_id, 20))
            seed = db.execute("SELECT delta, balance_after FROM economy_ledger WHERE player_id=?", (self.player_id,)).fetchone()
            self.assertEqual((seed["delta"], seed["balance_after"]), (20, 20))
            self.assertIsNotNone(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player_threat_states'").fetchone())

    def test_v18_upgrade_creates_boss_tables_without_changing_player_data(self):
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET level=4, sellos=63 WHERE id=?", (self.player_id,))
            db.execute("PRAGMA user_version=18")
        store.initialize(self.db_path)
        with store.connect(self.db_path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
            player = db.execute("SELECT id, name, level, sellos FROM players WHERE id=?", (self.player_id,)).fetchone()
            self.assertEqual((player["id"], player["name"], player["level"], player["sellos"]),
                             (self.player_id, "Jugador Migracion", 4, 63))
            tables = {row["name"] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertTrue({"world_boss_states", "boss_attempts", "boss_attempt_participants",
                             "player_lost_weapons", "boss_rewards_claimed"} <= tables)

    def test_v19_upgrade_adds_traveler_and_major_fauna_state_without_changing_player_data(self):
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET level=5, sellos=71 WHERE id=?", (self.player_id,))
            db.execute("DROP TABLE traveler_states")
            db.execute("PRAGMA user_version=19")
        store.initialize(self.db_path)
        with store.connect(self.db_path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
            player = db.execute("SELECT id, name, level, sellos FROM players WHERE id=?", (self.player_id,)).fetchone()
            self.assertEqual((player["id"], player["name"], player["level"], player["sellos"]),
                             (self.player_id, "Jugador Migracion", 5, 71))
            self.assertIsNotNone(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='traveler_states'").fetchone())
            self.assertIsNotNone(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='major_fauna_states'").fetchone())

    def test_v20_upgrade_adds_major_fauna_state_without_changing_player_data(self):
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET level=6, sellos=82 WHERE id=?", (self.player_id,))
            db.execute("DROP TABLE major_fauna_states")
            db.execute("PRAGMA user_version=20")
        store.initialize(self.db_path)
        with store.connect(self.db_path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
            player = db.execute("SELECT id, name, level, sellos FROM players WHERE id=?", (self.player_id,)).fetchone()
            self.assertEqual((player["id"], player["name"], player["level"], player["sellos"]),
                             (self.player_id, "Jugador Migracion", 6, 82))
            self.assertIsNotNone(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='major_fauna_states'").fetchone())


    def test_v21_upgrade_adds_presence_without_changing_player_data(self):
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET level=7, sellos=91 WHERE id=?", (self.player_id,))
            db.execute("DROP TABLE player_presence")
            db.execute("PRAGMA user_version=21")
        store.initialize(self.db_path)
        with store.connect(self.db_path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
            player = db.execute("SELECT id, name, level, sellos FROM players WHERE id=?", (self.player_id,)).fetchone()
            self.assertEqual((player["id"], player["name"], player["level"], player["sellos"]),
                             (self.player_id, "Jugador Migracion", 7, 91))
            self.assertIsNotNone(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player_presence'").fetchone())



if __name__ == "__main__":
    unittest.main()
