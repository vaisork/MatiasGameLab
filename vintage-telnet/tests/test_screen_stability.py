"""La pantalla no debe reacomodarse (petición de Javier, 2026-09-25): la
ilustración se guarda en el celular, el marco de arte siempre existe con el
mismo tamaño y el texto se revela sin cambiar de altura."""
import re
import tempfile
import unittest

from server.app import create_app
from server import store


class ScreenStabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()
        self.post("/register", dict(username="matias", name="Matías", password="una clave de prueba"))
        store.set_status(self.app.config["DATABASE"], "matias", "approved")
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class="sombra"))

    def tearDown(self):
        self.temp.cleanup()

    def post(self, route, data):
        page = self.client.get("/").get_data(as_text=True)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
        return self.client.post(route, data={**data, "csrf": csrf})

    def test_art_is_cached_but_pages_and_api_are_not(self):
        art = self.client.get("/assets/locations/valdren.webp")
        self.assertEqual(art.status_code, 200)
        self.assertEqual(art.headers["Cache-Control"], "public, max-age=86400")
        self.assertEqual(self.client.get("/").headers["Cache-Control"], "no-store")
        self.assertEqual(self.client.get("/api/room").headers["Cache-Control"], "no-store")

    def test_art_frame_is_always_present(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('<figure class="location-art">', html)
        self.assertIn('fetchpriority="high"', html)
        self.assertNotIn('loading="lazy" decoding="async">\n          <div class="location-art-fallback"', html)
        self.post("/move", dict(direction="west"))  # sendero: sin arte aprobado
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('<figure class="location-art no-art">', html)
        self.assertIn('<span>Sendero de Valdren</span>', html)

    def test_text_reveal_reserves_full_height(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('hiddenPart.style.visibility = "hidden"', html)
        self.assertIn(".game-shell .log{height:30dvh;height:30svh}", html)


if __name__ == "__main__":
    unittest.main()
