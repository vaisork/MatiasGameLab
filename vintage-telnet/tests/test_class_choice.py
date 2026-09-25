"""Clase inicial (Issue #112, GAMEPLAY.md 2, CONFIRMED_IDEAS.md).

Cubre: el paso de clase aparece después de la especie, se elige una sola vez,
bloquea el mundo mientras falta, entrega el arma inicial del catálogo y
personajes existentes (esquema v8) la eligen al volver sin perder nada.
"""
from concurrent.futures import ThreadPoolExecutor
import re
import sqlite3
import tempfile
import unittest

from server.app import create_app
from legacy_schema import undo_v11
from server import items, store, world


class ClassChoiceTests(unittest.TestCase):
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
        page = self.client.get("/").get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None):
        return self.client.post(route, data={**(data or {}), "csrf": self.csrf()})

    def enter_with_species(self, species="humano"):
        self.post("/register", dict(username="matias", name="Matías", password="una clave de prueba"))
        store.set_status(self.path, "matias", "approved")
        self.assertEqual(self.post("/species", dict(species=species)).status_code, 303)

    def me(self):
        return self.client.get("/api/me").json["player"]

    def test_class_step_appears_after_species_and_blocks_the_world(self):
        self.enter_with_species()
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn('action="/class"', page)
        for c in world.CLASSES:
            self.assertIn(f'value="{c["id"]}"', page)
            self.assertIn(c["name"], page)
        self.assertNotIn('id="placeTitle"', page)
        self.assertEqual(self.post("/move", dict(direction="north")).status_code, 403)
        self.assertEqual(self.post("/command", dict(text="mirar")).status_code, 403)
        self.assertEqual(self.client.get("/api/room").json, {"error": "class_required"})
        self.assertEqual(self.client.get("/api/room").status_code, 409)

    def test_class_cannot_be_chosen_before_species(self):
        self.post("/register", dict(username="matias", name="Matías", password="una clave de prueba"))
        store.set_status(self.path, "matias", "approved")
        self.assertEqual(self.post("/class", dict(player_class="arcano")).status_code, 303)
        self.assertIsNone(self.me()["player_class"])
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn('action="/species"', page)
        self.assertNotIn('action="/class"', page)

    def test_each_class_receives_its_catalog_starter_weapon_equipped(self):
        for class_id, weapon_key in items.STARTER_WEAPON_BY_CLASS.items():
            with self.subTest(class_id=class_id):
                self.tearDown()
                self.setUp()
                self.enter_with_species()
                self.assertEqual(self.post("/class", dict(player_class=class_id)).status_code, 303)
                self.assertEqual(self.me()["player_class"], class_id)
                inventory = self.client.get("/api/inventory").json
                self.assertEqual([row["item_key"] for row in inventory["items"]], [weapon_key])
                self.assertTrue(inventory["items"][0]["equipped"])
                self.assertEqual(inventory["equipped"]["weapon"]["item_key"], weapon_key)
                page = self.client.get("/").get_data(as_text=True)
                self.assertIn('id="placeTitle"', page)
                self.assertIn(world.CLASSES[world.CLASS_IDS.index(class_id)]["name"], page)

    def test_starter_weapons_exist_in_catalog_and_never_need_forge(self):
        self.assertEqual(set(items.STARTER_WEAPON_BY_CLASS), set(world.CLASS_IDS))
        for weapon_key in items.STARTER_WEAPON_BY_CLASS.values():
            weapon = items.get_item(weapon_key)
            self.assertEqual(items.category_of(weapon_key), "weapon")
            self.assertFalse(weapon["forge_required"])

    def test_class_is_chosen_only_once(self):
        self.enter_with_species()
        self.post("/class", dict(player_class="sombra"))
        self.assertEqual(self.post("/class", dict(player_class="arcano")).status_code, 303)
        self.assertEqual(self.me()["player_class"], "sombra")
        self.assertEqual(len(self.client.get("/api/inventory").json["items"]), 1)

    def test_unknown_class_is_rejected(self):
        self.enter_with_species()
        response = self.post("/class", dict(player_class="vigia"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Elige una clase de la lista.", response.get_data(as_text=True))
        self.assertIsNone(self.me()["player_class"])
        self.assertEqual(self.client.get("/api/inventory").json["items"], [])

    def test_api_class_contract(self):
        self.enter_with_species("felaryn")
        csrf = self.client.get("/api/me").json["csrf"]
        response = self.client.post("/api/class", json={"player_class": "artifice", "csrf": csrf})
        self.assertEqual(response.status_code, 200)
        body = response.json
        self.assertTrue(body["accepted"])
        self.assertEqual(body["player_class"], "artifice")
        self.assertEqual(body["starter_weapon"], {"item_key": "arco_ruta", "name": "Arco de ruta"})
        self.assertEqual(body["player"]["player_class"], "artifice")
        again = self.client.post("/api/class", json={"player_class": "arcano", "csrf": csrf})
        self.assertEqual(again.status_code, 400)
        self.assertEqual(again.json, {"accepted": False, "reason": "Ya elegiste tu clase."})
        self.assertEqual(self.client.get("/api/character").json["player_class"], "artifice")

    def test_concurrent_class_selection_is_atomic_and_grants_one_weapon(self):
        self.enter_with_species()
        player_id = self.me()["id"]

        def attempt(class_id):
            return store.set_player_class(self.path, player_id, class_id,
                                          items.STARTER_WEAPON_BY_CLASS[class_id])

        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(attempt, list(world.CLASS_IDS)))
        self.assertEqual(sum(results), 1)
        self.assertEqual(len(store.list_inventory(self.path, player_id)), 1)

    def test_starter_weapon_does_not_replace_an_already_equipped_weapon(self):
        self.enter_with_species()
        player_id = self.me()["id"]
        granted = store.grant_item(self.path, player_id, "espada_juramento")
        store.equip_item(self.path, player_id, granted)
        self.post("/class", dict(player_class="arcano"))
        inventory = self.client.get("/api/inventory").json
        self.assertEqual(inventory["equipped"]["weapon"]["item_key"], "espada_juramento")
        self.assertEqual({row["item_key"] for row in inventory["items"]},
                         {"espada_juramento", "varita_aprendiz"})

    def test_existing_v8_character_keeps_progress_and_chooses_class_on_return(self):
        # Simula un personaje ya jugado en esquema v8 (antes de #112).
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET player_class = NULL")
        self.enter_with_species("dravak")
        player_id = self.me()["id"]
        store.award_xp(self.path, player_id, 40)
        with sqlite3.connect(self.path) as db:
            undo_v11(db)
            db.execute("ALTER TABLE players DROP COLUMN player_class")
            db.execute("DROP TABLE combat_log")  # llega en v10
            db.execute("PRAGMA user_version = 8")
        app = create_app(self.config)
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
            row = db.execute("SELECT species, room, xp, player_class FROM players WHERE id = ?",
                             (player_id,)).fetchone()
        self.assertEqual((row["species"], row["room"], row["xp"], row["player_class"]),
                         ("dravak", "brumak_centro", 40, None))
        self.client = app.test_client()
        self.post("/login", dict(username="matias", password="una clave de prueba"))
        self.assertIn('action="/class"', self.client.get("/").get_data(as_text=True))
        self.post("/class", dict(player_class="juramentado"))
        me = self.me()
        self.assertEqual((me["player_class"], me["room"], me["xp"]), ("juramentado", "brumak_centro", 40))


if __name__ == "__main__":
    unittest.main()
