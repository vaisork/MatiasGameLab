"""Criatura a la vista vs. pelea (GAMEPLAY.md §26.5, RANDOM_ENCOUNTER §4):
ver una criatura no obliga a pelear —se puede seguir de largo—, pero una vez
que peleaste, caminar no sustituye a Huir, ni con botón ni con comando."""
import re
import tempfile
import unittest

from server.app import create_app
from server import store


class SeguirDeLargoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self.post("/register", dict(username="matias", name="Matías", password="una clave de prueba"))
        store.set_status(self.path, "matias", "approved")
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class="juramentado"))
        self.post("/move", dict(direction="north"))  # sendero
        self.post("/move", dict(direction="north"))  # parcela: Mordelinde a la vista

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self):
        return re.search(r'name="csrf" value="([^"]+)"', self.client.get("/").get_data(as_text=True))[1]

    def post(self, route, data):
        return self.client.post(route, data={**data, "csrf": self.csrf()})

    def me(self):
        return self.client.get("/api/me").json["player"]

    def test_you_can_walk_past_a_creature_you_only_saw(self):
        self.assertIsNotNone(store.get_encounter(self.path, self.me()["id"], "valdren_camino_parcela"))
        self.assertEqual(self.post("/move", dict(direction="north")).status_code, 303)
        self.assertEqual(self.me()["room"], "valdren_camino_cerca")
        # La criatura se quedó atrás: al volver aparece de nuevo, entera.
        self.assertIsNone(store.get_encounter(self.path, self.me()["id"], "valdren_camino_parcela"))
        self.post("/move", dict(direction="north"))  # deja también al Espinajo
        self.post("/move", dict(direction="south"))
        self.post("/move", dict(direction="south"))
        html = self.client.get("/").get_data(as_text=True)
        self.assertEqual(self.me()["room"], "valdren_camino_parcela")
        self.assertIn("entero / apenas afectado", html)

    def test_evaluating_is_not_fighting(self):
        self.post("/evaluate", {})
        self.assertEqual(self.post("/move", dict(direction="south")).status_code, 303)
        self.assertEqual(self.me()["room"], "valdren_sendero")

    def test_once_you_fight_walking_away_requires_fleeing(self):
        self.post("/attack", {})
        response = self.post("/move", dict(direction="south"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("para irte tienes que huir", response.get_data(as_text=True))
        self.assertEqual(self.me()["room"], "valdren_camino_parcela")
        # Ni escribiendo la dirección ni por la API.
        self.post("/command", dict(text="sur"))
        self.assertEqual(self.me()["room"], "valdren_camino_parcela")
        api = self.client.post("/api/move", json={"direction": "sur", "csrf": self.csrf()})
        self.assertEqual(api.status_code, 400)
        self.assertEqual(self.me()["room"], "valdren_camino_parcela")
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("¡COMBATE!", html)
        self.assertIn('action="/flee"', html)


if __name__ == "__main__":
    unittest.main()
