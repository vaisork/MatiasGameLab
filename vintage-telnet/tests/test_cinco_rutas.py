"""Las Cinco Rutas (NARRATIVE_ROUTES.md, #163/#164) con la geografía de
REGIONS.md: cada pueblo llega a Vaisgard por su camino, sin saltos."""
import re
import sqlite3
import tempfile
import unittest

from server.app import create_app
from server import store, world

CENTERS = {"A": "valdren_centro", "B": "khariel_centro", "C": "brumak_centro",
           "D": "narevia_centro", "E": "velmora_centro"}


def shortest_path(start, goal):
    previous, queue = {start: None}, [start]
    while queue:
        room_id = queue.pop(0)
        if room_id == goal:
            break
        for destination in world.ROOMS[room_id]["exits"].values():
            if destination not in previous:
                previous[destination] = room_id
                queue.append(destination)
    path, node = [], goal
    while node is not None:
        path.append(node)
        node = previous[node]
    return path[::-1]


class RouteStructureTests(unittest.TestCase):
    def test_every_route_joins_its_town_with_vaisgard(self):
        for letter, (chain, letters) in world.ROUTE_CHAINS.items():
            with self.subTest(route=letter):
                self.assertEqual(chain[0], CENTERS[letter])
                self.assertIn(chain[-1], ("vaisgard", "cuenca_aproximacion_sur"))
                self.assertEqual(len(letters), len(chain) - 1)
        self.assertEqual(world.ROOMS["vaisgard"]["exits"], {
            "north": "alto_aproximacion", "west": "piedra_aproximacion",
            "east": "sombra_aproximacion", "south": "cuenca_aproximacion_sur"})

    def test_no_town_is_a_short_hop_from_vaisgard(self):
        # "Valdren → Vaisgard deja de ser un salto": cada viaje cruza al menos
        # 17 estaciones.
        for center in CENTERS.values():
            with self.subTest(town=center):
                self.assertGreaterEqual(len(shortest_path(center, "vaisgard")) - 2, 17)

    def test_old_technical_roads_are_gone_and_every_room_is_reachable(self):
        self.assertNotIn("road_north", world.ROOMS)
        self.assertNotIn("road_west", world.ROOMS)
        self.assertEqual(set(world.map_layout()), set(world.ROOMS))
        for room_id, room in world.ROOMS.items():
            for destination in room["exits"].values():
                self.assertIn(destination, world.ROOMS, room_id)

    def test_route_rooms_have_no_fixed_encounters_besides_el_lindero_roto(self):
        route_rooms = {r for chain, _ in world.ROUTE_CHAINS.values() for r in chain}
        self.assertEqual(route_rooms & set(world.ROOM_ENCOUNTER),
                         {"valdren_camino_parcela", "valdren_camino_cerca"})

    def test_route_text_is_spanish_with_accents(self):
        for letter, (chain, _letters) in world.ROUTE_CHAINS.items():
            for room_id in chain:
                room = world.ROOMS[room_id]
                with self.subTest(room=room_id):
                    self.assertTrue(room["name"] and room["description"])
                    for bare in (" mas ", "division", "epocas", "pequeno", "arbol", "ultim"):
                        self.assertNotIn(bare, room["description"].lower().replace("más", ""))

    def test_visual_contexts_follow_the_canon(self):
        ctx = world.get_visual_context_id
        self.assertEqual(ctx("alto_terrazas"), "zone.khariel.terrazas")
        self.assertEqual(ctx("valdren_camino_hundido"), "zone.edran.valdren_outskirts")
        self.assertEqual(ctx("alto_puente_viento"), "zone.hoshai.khariel_approach")
        self.assertEqual(ctx("piedra_pared_partida"), None)  # Korven: sin paisaje aprobado todavía
        for room_id in ("campos_acceso", "alto_aproximacion", "piedra_aproximacion",
                        "juncos_aproximacion", "sombra_aproximacion", "cuenca_aproximacion_sur"):
            self.assertEqual(ctx(room_id), "zone.veyra.road", room_id)

    def test_dynamic_habitats_point_to_real_rooms_without_fixed_encounters(self):
        for room_id in world.DYNAMIC_HABITAT_ROOMS:
            self.assertIn(room_id, world.ROOMS)
            self.assertNotIn(room_id, world.ROOM_ENCOUNTER)


class RouteWalkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self):
        return re.search(r'name="csrf" value="([^"]+)"', self.client.get("/").get_data(as_text=True))[1]

    def enter(self, species):
        self.client.post("/register", data=dict(csrf=self.csrf(), username="viajero", name="Viajero",
                                                password="una clave de prueba"))
        store.set_status(self.path, "viajero", "approved")
        self.client.post("/species", data=dict(csrf=self.csrf(), species=species))
        self.client.post("/class", data=dict(csrf=self.csrf(), player_class="artifice"))

    def test_felaryn_walks_the_camino_alto_from_khariel_to_vaisgard(self):
        self.enter("felaryn")
        for _ in range(18):
            self.assertEqual(self.client.post("/move", data=dict(csrf=self.csrf(), direction="south")).status_code, 303)
        self.assertEqual(self.client.get("/api/me").json["player"]["room"], "vaisgard")
        visited = set(store.get_map_state(self.path, self.client.get("/api/me").json["player"]["id"])["visited_rooms"])
        self.assertIn("alto_puente_viento", visited)

    def test_players_left_on_removed_roads_are_sent_home(self):
        self.enter("marevyn")
        player_id = self.client.get("/api/me").json["player"]["id"]
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE players SET room = 'road_west' WHERE id = ?", (player_id,))
        create_app(self.config)  # el arranque recoloca
        self.assertEqual(self.client.get("/api/me").json["player"]["room"], "narevia_centro")
        self.assertEqual(store.relocate_players_outside_world(
            self.path, set(world.ROOMS), world.get_starting_room_for_species), 0)


if __name__ == "__main__":
    unittest.main()
