"""Toda imagen que el juego muestra debe existir y servirse (Issue #151):
un src roto dejaría el marco de arte vacío sin que nadie se entere."""
import re
import tempfile
import unittest
from pathlib import Path

from server.app import create_app
from server import creatures, store, world

ASSETS = Path(__file__).resolve().parent.parent.parent / "assets" / "vintage-telnet"
FOLDERS = {"/assets/locations/": "locations", "/assets/creatures/": "creatures"}


def disk_path(src):
    for prefix, folder in FOLDERS.items():
        if src.startswith(prefix):
            return ASSETS / folder / src[len(prefix):]
    raise AssertionError(f"ruta de arte desconocida: {src}")


class PublishedArtTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def art_rows(self):
        return list(world.VISUAL_CONTEXT_ART.items()) + list(creatures.CREATURE_ART.items())

    def test_every_referenced_image_exists_and_is_served_as_webp(self):
        for key, art in self.art_rows():
            with self.subTest(key=key):
                self.assertTrue(disk_path(art["src"]).is_file(), art["src"])
                response = self.client.get(art["src"])
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, "image/webp")
                self.assertIn("max-age", response.headers["Cache-Control"])
                response.close()

    def test_first_combat_creatures_and_veyra_road_have_art(self):
        self.assertIn("mordelinde", creatures.CREATURE_ART)
        self.assertIn("espinajo_rastrojo", creatures.CREATURE_ART)
        self.assertEqual(world.get_visual_context_id("road_north"), "zone.veyra.road")
        self.assertIn("zone.veyra.road", world.VISUAL_CONTEXT_ART)
        for creature_id in creatures.CREATURE_ART:
            self.assertIsNotNone(creatures.get_creature(creature_id))

    def test_combat_frame_shows_the_creature(self):
        page = self.client.get("/").get_data(as_text=True)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
        self.client.post("/register", data=dict(csrf=csrf, username="matias", name="Matías",
                                                password="una clave de prueba"))
        path = self.app.config["DATABASE"]
        store.set_status(path, "matias", "approved")
        # Al entrar, la sesión estrena un token CSRF nuevo.
        csrf = re.search(r'name="csrf" value="([^"]+)"', self.client.get("/").get_data(as_text=True))[1]
        self.client.post("/species", data=dict(csrf=csrf, species="humano"))
        self.client.post("/class", data=dict(csrf=csrf, player_class="juramentado"))
        self.client.post("/move", data=dict(csrf=csrf, direction="west"))  # sendero
        self.client.post("/move", data=dict(csrf=csrf, direction="west"))  # parcela: Mordelinde
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("/assets/creatures/mordelinde.webp", html)


if __name__ == "__main__":
    unittest.main()
