"""Navegación (Issue #135): minimapa de lugares conocidos, línea de salidas
con nombres solo de lo visitado y flechas del teclado."""
import re
import tempfile
import unittest

from server.app import create_app
from server import store, world


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self.post("/register", dict(username="matias", name="Matías", password="una clave de prueba"))
        store.set_status(self.path, "matias", "approved")
        self.post("/species", dict(species="humano"))  # valdren_centro
        self.post("/class", dict(player_class="sombra"))

    def tearDown(self):
        self.temp.cleanup()

    def post(self, route, data):
        page = self.client.get("/").get_data(as_text=True)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
        return self.client.post(route, data={**data, "csrf": csrf})

    def test_layout_covers_every_room_without_collisions_and_is_stable(self):
        layout = world.map_layout()
        self.assertEqual(set(layout), set(world.ROOMS))
        self.assertEqual(len(set(layout.values())), len(layout))
        self.assertIs(world.map_layout(), layout)
        # Las salidas reales se respetan: Valdren queda al norte del Camino del Norte.
        self.assertEqual(layout["road_north"][1] - layout["valdren_centro"][1], 1)

    def test_minimap_only_exposes_known_places(self):
        data = self.client.get("/api/map").json
        self.assertEqual(data["current_room"], "valdren_centro")
        self.assertEqual([p["id"] for p in data["places"]], ["valdren_centro"])
        self.assertTrue(data["places"][0]["current"])
        self.assertEqual(data["places"][0]["name"], "Valdren")
        # Salidas sin explorar: solo dirección, nunca destino ni nombre.
        stubs = data["unexplored_exits"]
        self.assertEqual({s["direction"] for s in stubs}, {"north", "south", "east", "west"})
        for stub in stubs:
            self.assertEqual(set(stub), {"from", "direction"})
        self.assertNotIn("Mercado de Valdren", str(data))

        self.post("/move", dict(direction="east"))
        data = self.client.get("/api/map").json
        names = {p["id"]: p["name"] for p in data["places"]}
        self.assertEqual(names, {"valdren_centro": "Valdren", "valdren_mercado": "Mercado de Valdren"})
        self.assertEqual(data["current_room"], "valdren_mercado")
        self.assertNotIn({"from": "valdren_centro", "direction": "east"}, data["unexplored_exits"])
        # Claves anteriores intactas para clientes existentes.
        self.assertIn("visited_rooms", data)
        self.assertEqual(data["current_heading"], "east")

    def test_exit_names_appear_only_after_visiting(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("Salidas: <b>sur</b>", html.replace("\n", ""))
        self.assertNotIn("(Mercado de Valdren)", html)
        self.post("/move", dict(direction="east"))
        self.post("/move", dict(direction="west"))
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("<b>este</b> (Mercado de Valdren)", html)
        self.assertIn('aria-label="Ir al este — Mercado de Valdren"', html)
        self.assertNotIn("(Forja de Valdren)", html)
        room = self.client.get("/api/room").json["room"]
        known = {e["direction"]: e["known_name"] for e in room["exits"]}
        self.assertEqual(known["east"], "Mercado de Valdren")
        self.assertIsNone(known["north"])

    def test_map_panel_and_keyboard_navigation_are_wired(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('id="minimapScroll"', html)
        self.assertIn("Salida sin explorar", html)
        self.assertIn("renderMinimap(data)", html)
        self.assertIn('ArrowUp: "north"', html)
        self.assertIn('document.querySelector("dialog[open]")', html)


if __name__ == "__main__":
    unittest.main()
