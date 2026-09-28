"""Rescate #177 / contrato #147: recompensa única, atómica y visible."""
from concurrent.futures import ThreadPoolExecutor
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import store, world


class RewardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="reward-tests-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self.post("/register", username="matias", name="Matías", password="una clave de prueba")
        store.set_status(self.path, "matias", "approved")
        self.post("/species", species="humano")
        self.pid = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.path, self.pid, "juramentado")
        store.move_player(self.path, self.pid, "valdren_sendero")
        self.discovery = world.get_discovery("regreso_valdren_lindero")

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self):
        return re.search(r'name="csrf" value="([^"]+)"', self.client.get("/").text)[1]

    def post(self, route, **data):
        return self.client.post(route, data={**data, "csrf": self.csrf()})

    def discovered(self):
        store.award_discovery(self.path, self.pid, "lindero_roto", "descubrimiento_mayor", 1)

    def award(self):
        return store.award_discovery(self.path, self.pid, "regreso_valdren_lindero",
                                    self.discovery["category"], 1, reward_item="acolchado_camino")

    def armor_count(self):
        return sum(item["item_key"] == "acolchado_camino"
                   for item in store.list_inventory(self.path, self.pid))

    def test_no_reward_before_discovery(self):
        self.post("/move", direction="south")
        self.assertEqual(self.armor_count(), 0)

    def test_form_return_shows_reward_once_and_persists_unequipped(self):
        self.discovered()
        response = self.post("/move", direction="south")
        self.assertEqual(response.status_code, 303)
        self.assertIn(self.discovery["reward_text"], self.client.get("/").text)
        self.assertNotIn(self.discovery["reward_text"], self.client.get("/").text)
        self.assertEqual(self.armor_count(), 1)
        player = self.client.get("/api/me").json["player"]
        self.assertIsNone(player["equipped_armor_id"])
        reopened = create_app(dict(TESTING=True, SECRET_KEY="reward-tests-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.assertEqual(len(store.list_inventory(reopened.config["DATABASE"], self.pid)), 1)
        store.move_player(self.path, self.pid, "valdren_sendero")
        self.post("/move", direction="south")
        self.assertEqual(self.armor_count(), 1)
        self.assertNotIn(self.discovery["reward_text"], self.client.get("/").text)

    def test_written_command_shows_reward(self):
        self.discovered()
        self.post("/command", text="sur")
        self.assertIn(self.discovery["reward_text"], self.client.get("/").text)

    def test_json_move_and_intent_only_return_current_reward(self):
        for route, payload in (("/api/move", {"direction": "south"}),
                               ("/api/intent", {"text": "sur"})):
            with self.subTest(route=route):
                # Cada variante obtiene un hito limpio dentro de su DB temporal.
                with store.connect(self.path) as db:
                    db.execute("DELETE FROM discoveries WHERE player_id = ?", (self.pid,))
                    db.execute("DELETE FROM inventory_items WHERE player_id = ?", (self.pid,))
                store.move_player(self.path, self.pid, "valdren_sendero")
                self.discovered()
                response = self.client.post(route, json={**payload, "csrf": self.csrf()})
                self.assertEqual(response.status_code, 200)
                self.assertIn(self.discovery["reward_text"], response.json["reward_message"])
                self.assertEqual(self.armor_count(), 1)
                self.assertNotIn(self.discovery["reward_text"], self.client.get("/").text)
                store.move_player(self.path, self.pid, "valdren_sendero")
                response = self.client.post(route, json={**payload, "csrf": self.csrf()})
                self.assertIsNone(response.json["reward_message"])

    def test_parallel_awards_only_grant_one_item(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: self.award(), range(8)))
        self.assertEqual(sum(result[0] for result in results), 1)
        self.assertEqual(self.armor_count(), 1)

    def test_failed_item_grant_rolls_back_discovery_for_retry(self):
        with patch.object(store, "grant_item", side_effect=RuntimeError("simulated failure")):
            with self.assertRaises(RuntimeError):
                self.award()
        self.assertFalse(store.has_discovery(self.path, self.pid, "regreso_valdren_lindero"))
        self.assertEqual(self.armor_count(), 0)
        self.assertTrue(self.award()[0])
        self.assertEqual(self.armor_count(), 1)

    def test_existing_milestone_does_not_retroactively_grant_item(self):
        store.award_discovery(self.path, self.pid, "regreso_valdren_lindero",
                              self.discovery["category"], 1)
        self.assertFalse(self.award()[0])
        self.assertEqual(self.armor_count(), 0)


if __name__ == "__main__":
    unittest.main()
