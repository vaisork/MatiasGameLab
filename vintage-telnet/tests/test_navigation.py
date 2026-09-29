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
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class="sombra"))
        self.post("/move", dict(direction="south"))

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
        # Geometría coherente: cada salida lleva exactamente a la celda vecina.
        step = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
        for room_id, room in world.ROOMS.items():
            for direction, destination in room["exits"].items():
                dx, dy = step[direction]
                self.assertEqual(layout[destination], (layout[room_id][0] + dx, layout[room_id][1] + dy),
                                 (room_id, direction, destination))
        # REGIONS.md: Khariel al norte, Brumak al oeste, Velmora al este,
        # Valdren al suroeste y Narevia al sureste de Vaisgard.
        x = lambda r: layout[r][0]
        y = lambda r: layout[r][1]
        self.assertLess(y("khariel_centro"), y("vaisgard"))
        self.assertLess(x("brumak_centro"), x("vaisgard"))
        self.assertGreater(x("velmora_centro"), x("vaisgard"))
        self.assertTrue(x("valdren_centro") < 0 < y("valdren_centro"))
        self.assertTrue(x("narevia_centro") > 0 and y("narevia_centro") > 0)

    def test_minimap_only_exposes_known_places(self):
        data = self.client.get("/api/map").json
        self.assertEqual(data["current_room"], "valdren_centro")
        names = {p["id"]: p["name"] for p in data["places"]}
        self.assertEqual(names["valdren_centro"], "Valdren")
        self.assertEqual(names[world.get_home_room_id(self._player_id())], "Tu hogar")
        self.assertTrue(next(p for p in data["places"] if p["id"] == "valdren_centro")["current"])
        # Salidas sin explorar: solo dirección, nunca destino ni nombre.
        stubs = data["unexplored_exits"]
        self.assertEqual({s["direction"] for s in stubs}, {"north", "east", "west"})
        for stub in stubs:
            self.assertEqual(set(stub), {"from", "direction"})
        self.assertNotIn("Mercado de Valdren", str(data))

        self.post("/move", dict(direction="east"))
        data = self.client.get("/api/map").json
        names = {p["id"]: p["name"] for p in data["places"]}
        names.pop(world.get_home_room_id(self._player_id()))
        self.assertEqual(names, {"valdren_centro": "Valdren", "valdren_mercado": "Mercado de Valdren"})
        self.assertEqual(data["current_room"], "valdren_mercado")
        self.assertNotIn({"from": "valdren_centro", "direction": "east"}, data["unexplored_exits"])
        # Claves anteriores intactas para clientes existentes.
        self.assertIn("visited_rooms", data)
        self.assertEqual(data["current_heading"], "east")

    def test_exit_names_appear_only_after_visiting(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("Salidas: <b>norte</b>", html.replace("\n", ""))
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


    def test_map_places_and_tabs_resolve_home_and_current_room_without_id_leak(self):
        # Issue #417: evitar fuga de home:<uuid> y asegurar que la cabecera del modal
        # refleje la sala actual y que las pestañas de mapa y ayuda no queden ocultas.
        data = self.client.get("/api/map").json
        self.assertEqual(data["current_room"], "valdren_centro")
        self.assertEqual(data["current_room_name"], "Valdren")
        self.assertIn("room_names", data)
        home_ids = [r for r in data["visited_rooms"] if world.is_home_room(r)]
        self.assertTrue(home_ids)
        self.assertEqual(data["room_names"][home_ids[0]], "Tu hogar")
        self.assertEqual(data["room_names"]["valdren_centro"], "Valdren")

        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('id="mapCurrentRoomName"', html)
        self.assertIn('activateTabs("[data-map-tab]", "[data-map-panel]", "mapTab", "mapPanel")', html)
        self.assertIn('activateTabs("[data-help-tab]", "[data-help-panel]", "helpTab", "helpPanel")', html)
        self.assertIn('startsWith("home:")', html)

    def _player_id(self):
        return self.client.get("/api/me").json["player"]["id"]

    def test_personal_home_is_a_private_minimap_node_linked_to_species_town(self):
        player_id = self._player_id()
        data = self.client.get("/api/map").json
        homes = [place for place in data["places"] if place.get("kind") == "home"]
        self.assertEqual(len(homes), 1)
        home = homes[0]
        self.assertEqual(home["id"], world.get_home_room_id(player_id))
        self.assertEqual(home["name"], "Tu hogar")
        self.assertNotEqual(home["x"] % 1, 0)
        self.assertEqual(data["home_links"], [{"home": home["id"], "community": "valdren_centro",
                                                "traversed": True}])

        with store.connect(self.path) as db:
            db.execute("UPDATE players SET room = ? WHERE id = ?", (home["id"], player_id))
        home_map = self.client.get("/api/map").json
        home_marker = next(p for p in home_map["places"] if p.get("kind") == "home")
        self.assertTrue(home_marker["current"])

        self.assertEqual(home_map["room_names"][home["id"]], "Tu hogar")
        template = self.client.get("/").get_data(as_text=True)
        self.assertIn('startsWith("home:")', template)
        self.assertIn('return "Tu hogar";', template)

        for species, community_id in world.STARTING_ROOM_BY_SPECIES.items():
            with self.subTest(species=species):
                with store.connect(self.path) as db:
                    db.execute("UPDATE players SET species = ? WHERE id = ?", (species, player_id))
                species_map = self.client.get("/api/map").json
                self.assertEqual(species_map["home_links"][0]["community"], community_id)
                self.assertIn(community_id, {place["id"] for place in species_map["places"]})

    def test_home_art_uses_approved_species_assets(self):
        player_id = self._player_id()
        expected = {
            "humano": "/assets/locations/valdren-vivienda-patio.webp",
            "felaryn": "/assets/locations/khariel-vivienda-felaryn-terraza.webp",
            "dravak": "/assets/locations/brumak-taller-domestico.webp",
            "marevyn": "/assets/locations/narevia-vivienda-marevyn-canal.webp",
            "vesperi": "/assets/locations/velmora-vivienda-vesperi-raices.webp",
        }
        home_id = world.get_home_room_id(player_id)
        for species, asset in expected.items():
            with self.subTest(species=species):
                with store.connect(self.path) as db:
                    db.execute("UPDATE players SET species = ?, room = ? WHERE id = ?",
                               (species, home_id, player_id))
                room = world.describe_room(home_id, [])
                self.assertEqual(room["art"]["src"], asset)
                response = self.client.get(asset)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, "image/webp")
                response.close()

    def test_home_with_unresolved_species_uses_neutral_art_fallback(self):
        player_id = self._player_id()
        home_id = world.get_home_room_id(player_id)
        world.set_home_species_resolver(lambda _player_id: None)
        try:
            room = world.describe_room(home_id, [])
            self.assertEqual(room["name"], "Tu hogar")
            self.assertIsNone(room["art"])
            self.assertIsNone(room["visual_context_id"])
        finally:
            world.set_home_species_resolver(lambda pid: store.get_player_species(self.path, pid))


if __name__ == "__main__":
    unittest.main()
