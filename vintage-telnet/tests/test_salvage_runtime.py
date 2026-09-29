"""#482: material por victoria, antifarmeo y venta sin duplicación."""
import tempfile
import unittest
from unittest.mock import patch

from server import salvage, store


class SalvageRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = self.temp.name + "/vintage.sqlite3"
        store.initialize(self.path)
        self.player_id = "salvage-tester"
        with store.connect(self.path) as db:
            db.execute("""INSERT INTO players(id, username, name, name_key, password_hash, status, created_at, last_access_at, sellos)
                          VALUES (?, 'salvage-tester', 'Salvage Tester', 'salvage tester', '', 'approved', '', '', 20)""",
                       (self.player_id,))

    def tearDown(self):
        self.temp.cleanup()

    def test_drop_and_atomic_sale_with_replay(self):
        with patch("server.salvage.random.random", return_value=0.0):
            store.record_pve_victory(self.path, self.player_id, "mordelinde")
        material = salvage.list_materials(self.path, self.player_id)[0]
        self.assertEqual(material["price"], 3)
        self.assertIn("Retazo", salvage.victory_message(self.path, self.player_id, "mordelinde"))
        self.assertFalse(salvage.sell(self.path, self.player_id, "valdren_forja", material["id"])[0])
        ok, _, result = salvage.sell(self.path, self.player_id, salvage.MARKET, material["id"])
        self.assertTrue(ok)
        self.assertEqual(result["balance"], 23)
        replay = salvage.sell(self.path, self.player_id, salvage.MARKET, material["id"])
        self.assertTrue(replay[2]["idempotent_replay"])
        self.assertEqual(salvage.list_materials(self.path, self.player_id), [])
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM economy_ledger WHERE reason_code = 'salvage_sale'").fetchone()[0], 1)

    def test_antifarming_uses_last_ten_victories(self):
        with patch("server.salvage.random.random", return_value=.5):
            for _ in range(6):
                store.record_pve_victory(self.path, self.player_id, "mordelinde")
        # 70% en las tres primeras; 42%/17.5% en las siguientes.
        self.assertEqual(len(salvage.list_materials(self.path, self.player_id)), 3)
        with patch("server.salvage.random.random", return_value=0.0):
            store.record_pve_victory(self.path, self.player_id, "cornalomo")
        self.assertEqual(len(salvage.list_materials(self.path, self.player_id)), 3)

    def test_material_can_be_sold_at_another_town_market(self):
        with patch("server.salvage.random.random", return_value=0.0):
            store.record_pve_victory(self.path, self.player_id, "mordelinde")
        material = salvage.list_materials(self.path, self.player_id)[0]
        ok, _message, result = salvage.sell(self.path, self.player_id, "khariel_mercado", material["id"])
        self.assertTrue(ok)
        self.assertEqual(result["balance"], 23)

    def test_upgrade_from_v23_preserves_player_and_equipment(self):
        with store.connect(self.path) as db:
            db.execute("DROP TABLE salvage_items")
            db.execute("PRAGMA user_version = 23")
        store.initialize(self.path)
        self.assertEqual(store.SCHEMA_VERSION, 24)
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 24)
            self.assertEqual(db.execute("SELECT sellos FROM players WHERE id = ?", (self.player_id,)).fetchone()[0], 20)
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])


if __name__ == "__main__":
    unittest.main()
