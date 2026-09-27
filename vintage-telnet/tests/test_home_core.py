"""HOME-CORE (#280): hogar privado mínimo, persistente y sin ruta regional."""
import re
import tempfile
import unittest
from werkzeug.security import generate_password_hash

from server.app import create_app
from server import store, world


class HomeCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="home-core-test-secret-" * 3,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self):
        page = self.client.get("/").get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data):
        return self.client.post(route, data={**data, "csrf": self.csrf()})

    def enter_new_character(self, username="matias", species="humano"):
        self.post("/register", dict(username=username, name=username.title(), password="clave de prueba"))
        store.set_status(self.path, username, "approved")
        self.assertEqual(self.post("/species", dict(species=species)).status_code, 303)
        self.assertEqual(self.post("/class", dict(player_class="arcano")).status_code, 303)
        return self.client.get("/api/me").json["player"]

    def test_new_character_starts_in_its_private_home_with_species_town_exit(self):
        player = self.enter_new_character(species="felaryn")
        self.assertEqual(player["room"], f"home:{player['id']}")
        room = self.client.get("/api/room").json["room"]
        self.assertEqual(room["name"], "Tu hogar")
        self.assertEqual(room["description"],
                         "Este es tu hogar. Aquí comienza tu viaje y aquí conservas "
                         "un lugar propio dentro del mundo. La salida conduce hacia tu comunidad.")
        self.assertEqual([exit_["direction"] for exit_ in room["exits"]], ["south"])
        self.assertIsNone(room["encounter"])
        self.assertEqual(room["available_actions"], [{"action": "descansar"}])
        self.assertIsNone(store.get_encounter(self.path, player["id"], player["room"]))
        move = self.client.post("/api/move", json={"direction": "south", "csrf": self.client.get("/api/me").json["csrf"]})
        self.assertTrue(move.json["accepted"])
        self.assertEqual(move.json["current_room"]["id"], world.get_starting_room_for_species("felaryn"))

    def test_each_species_home_exit_targets_its_authoritative_starting_town(self):
        for index, species in enumerate(world.SPECIES_IDS):
            with self.subTest(species=species):
                if index:
                    self.tearDown()
                    self.setUp()
                player = self.enter_new_character(f"traveler{index}", species)
                csrf = self.client.get("/api/me").json["csrf"]
                response = self.client.post("/api/move", json={"direction": "south", "csrf": csrf})
                self.assertTrue(response.json["accepted"])
                self.assertEqual(response.json["current_room"]["id"],
                                 world.get_starting_room_for_species(species))

    def test_home_ids_are_unique_between_characters_and_accounts(self):
        first = self.enter_new_character("matias")
        with store.connect(self.path) as db:
            account = store.account_by_username(db, "matias")
        second_id = store.create_character(self.path, account["id"], "Segundo")
        token = store.register(self.path, "sofia", "Sofía", generate_password_hash("clave de prueba"))
        other_account = store.account_for_token(self.path, token)
        third_id = store.create_character(self.path, other_account["id"], "Otro personaje")
        self.assertNotEqual(f"home:{first['id']}", f"home:{second_id}")
        self.assertNotEqual(f"home:{first['id']}", f"home:{third_id}")
        self.assertNotEqual(f"home:{second_id}", f"home:{third_id}")

    def test_existing_character_keeps_valid_location_when_choosing_class(self):
        self.post("/register", dict(username="oldplayer", name="Antiguo", password="clave de prueba"))
        store.set_status(self.path, "oldplayer", "approved")
        self.assertEqual(self.post("/species", dict(species="dravak")).status_code, 303)
        before = self.client.get("/api/me").json["player"]
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET home_onboarding = 0 WHERE id = ?", (before["id"],))
        self.assertEqual(self.post("/class", dict(player_class="sombra")).status_code, 303)
        after = self.client.get("/api/me").json["player"]
        self.assertEqual(after["room"], world.get_starting_room_for_species("dravak"))

    def test_v12_migration_preserves_existing_position_and_marks_character_legacy(self):
        self.post("/register", dict(username="legacy", name="Legado", password="clave de prueba"))
        store.set_status(self.path, "legacy", "approved")
        self.assertEqual(self.post("/species", dict(species="vesperi")).status_code, 303)
        before = self.client.get("/api/me").json["player"]
        with store.connect(self.path) as db:
            db.execute("ALTER TABLE players DROP COLUMN home_onboarding")
            db.execute("PRAGMA user_version = 12")
        create_app(self.config)
        with store.connect(self.path) as db:
            row = db.execute("SELECT room, home_onboarding FROM players WHERE id = ?",
                             (before["id"],)).fetchone()
        self.assertEqual(row["room"], before["room"])
        self.assertEqual(row["home_onboarding"], 0)

    def test_home_survives_app_recreation_and_normal_rest(self):
        player = self.enter_new_character()
        saved_room = player["room"]
        store.update_combat_state(self.path, player["id"], hp_current=20)
        rest = self.client.post("/api/intent", json={
            "text": "descansar", "csrf": self.client.get("/api/me").json["csrf"]
        })
        self.assertEqual(rest.json["outcome"], "rested")
        self.assertNotIn("plaza de Valdren", " ".join(rest.json["messages"]))
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        # The persisted character remains at home after a fresh app instance.
        character = store.character_by_player_id(self.path, player["id"])
        self.assertEqual(character["room"], saved_room)
        self.assertIsNone(store.get_encounter(self.path, player["id"], saved_room))

    def test_reconnect_after_leaving_home_keeps_the_town_location(self):
        player = self.enter_new_character(species="marevyn")
        csrf = self.client.get("/api/me").json["csrf"]
        response = self.client.post("/api/move", json={"direction": "south", "csrf": csrf})
        self.assertEqual(response.json["current_room"]["id"], "narevia_centro")
        create_app(self.config)
        character = store.character_by_player_id(self.path, player["id"])
        self.assertEqual(character["room"], "narevia_centro")


if __name__ == "__main__":
    unittest.main()
