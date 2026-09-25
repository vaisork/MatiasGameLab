"""Cuentas con varios personajes (petición de Javier, 2026-09-25): un usuario
para entrar puede tener hasta 5 personajes; el nombre de cada personaje es
único en el mundo; el Dungeon Master aprueba cada personaje; por ahora el
jugador no puede borrar personajes."""
import re
import sqlite3
import tempfile
import unittest

from werkzeug.security import generate_password_hash

from server.app import create_app
from server import store
from legacy_schema import undo_v11

PASSWORD = "una clave de prueba"


class MultiCharacterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def post(self, route, data=None, client=None):
        client = client or self.client
        page = client.get("/").get_data(as_text=True)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
        return client.post(route, data={**(data or {}), "csrf": csrf})

    def register(self, username="matias", name="Matías", client=None):
        return self.post("/register", dict(username=username, name=name, password=PASSWORD), client)

    def page(self, client=None):
        return (client or self.client).get("/").get_data(as_text=True)

    def handles(self):
        with store.connect(self.path) as db:
            return {row["name"]: row["username"] for row in db.execute("SELECT name, username FROM players")}

    def test_register_creates_account_with_first_character_and_login_enters_directly(self):
        self.assertEqual(self.register().status_code, 303)
        self.assertEqual(self.post("/logout").status_code, 303)
        self.assertEqual(self.post("/login", dict(username="matias", password=PASSWORD)).status_code, 303)
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["name"], "Matías")
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM accounts").fetchone()[0], 1)
            # La contraseña vive solo en la cuenta.
            self.assertEqual(db.execute("SELECT password_hash FROM players").fetchone()[0], "")

    def test_second_character_needs_its_own_approval_and_login_asks_which_one(self):
        self.register()
        store.set_status(self.path, "matias", "approved")
        self.post("/characters/switch")
        page = self.page()
        self.assertIn("Tus personajes", page)
        self.assertIn('action="/characters/new"', page)
        self.assertEqual(self.post("/characters/new", dict(name="Rayo")).status_code, 303)

        pending = store.list_by_status(self.path, "pending")
        self.assertEqual([(p["name"], p["account_username"]) for p in pending], [("Rayo", "matias")])

        self.post("/logout")
        self.post("/login", dict(username="matias", password=PASSWORD))
        self.assertEqual(self.client.get("/api/me").status_code, 409)
        page = self.page()
        self.assertIn("Matías", page)
        self.assertIn("Rayo", page)
        self.assertIn("Esperando aprobación del Dungeon Master", page)

        with store.connect(self.path) as db:
            rayo = db.execute("SELECT id FROM players WHERE name = 'Rayo'").fetchone()["id"]
        self.post("/characters/select", dict(player_id=rayo))
        self.assertIn("Rayo fue recibido", self.page())
        self.assertEqual(self.client.get("/api/room").status_code, 403)

        store.set_status(self.path, self.handles()["Rayo"], "approved")
        self.assertIn('action="/species"', self.page())

    def test_at_most_five_characters_per_account(self):
        self.register()
        self.post("/characters/switch")
        for name in ("Dos", "Tres", "Cuatro", "Cinco"):
            self.assertEqual(self.post("/characters/new", dict(name=name)).status_code, 303)
        response = self.post("/characters/new", dict(name="Seis"))
        self.assertEqual(response.status_code, 409)
        self.assertIn("el máximo por cuenta", response.get_data(as_text=True))
        self.assertNotIn('action="/characters/new"', self.page())
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM players").fetchone()[0], 5)

    def test_character_names_are_unique_across_accounts_ignoring_accents_and_case(self):
        self.register()
        other = self.app.test_client()
        response = self.register("javier", "  MATIAS ", client=other)
        self.assertEqual(response.status_code, 409)
        page = response.get_data(as_text=True)
        self.assertIn("Ya hay un personaje llamado", page)
        # El formulario sigue abierto con lo que ya escribió (sin la contraseña).
        self.assertIn('data-view="register"', page)
        self.assertIn('value="javier"', page)
        self.assertNotIn(PASSWORD, page)
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM accounts").fetchone()[0], 1)

        self.register("javier", "Javier", client=other)
        self.post("/characters/switch", client=other)
        response = self.post("/characters/new", dict(name="matías"), client=other)
        self.assertEqual(response.status_code, 409)
        self.assertIn('value="matías"', response.get_data(as_text=True))

    def test_duplicate_username_keeps_register_form_open_with_clear_message(self):
        self.register()
        other = self.app.test_client()
        response = self.register("MATIAS", "Otro nombre", client=other)
        self.assertEqual(response.status_code, 409)
        page = response.get_data(as_text=True)
        self.assertIn("ya existe. Si es tuyo, usa Entrar", page)
        self.assertIn('data-view="register"', page)
        self.assertIn('value="Otro nombre"', page)
        self.assertRegex(page, r'data-onboarding-view="welcome" hidden')
        # La cuenta original sigue intacta.
        self.assertEqual(self.post("/login", dict(username="matias", password=PASSWORD), other).status_code, 303)

    def test_failed_login_keeps_login_form_open(self):
        self.register()
        other = self.app.test_client()
        response = self.post("/login", dict(username="matias", password="equivocada"), other)
        self.assertEqual(response.status_code, 401)
        page = response.get_data(as_text=True)
        self.assertIn('data-view="login"', page)
        self.assertIn('value="matias"', page)
        self.assertIn("Usuario o contraseña incorrectos.", page)

    def test_cannot_select_a_character_from_another_account(self):
        self.register()
        other = self.app.test_client()
        self.register("javier", "Javier", client=other)
        with store.connect(self.path) as db:
            javier = db.execute("SELECT id FROM players WHERE name = 'Javier'").fetchone()["id"]
        self.post("/characters/switch")
        self.assertEqual(self.post("/characters/select", dict(player_id=javier)).status_code, 404)
        self.assertEqual(self.client.get("/api/me").status_code, 409)

    def test_dm_removing_one_character_keeps_the_account_and_its_other_characters(self):
        self.register()
        store.set_status(self.path, "matias", "approved")
        self.post("/characters/switch")
        self.post("/characters/new", dict(name="Rayo"))
        with store.connect(self.path) as db:
            matias = db.execute("SELECT id FROM players WHERE name = 'Matías'").fetchone()["id"]
        self.post("/characters/select", dict(player_id=matias))
        store.set_status(self.path, "matias", "removed", revoke_sessions=True)
        page = self.page()
        self.assertIn("Tus personajes", page)
        self.assertIn("No habilitado", page)
        self.assertIn("Rayo", page)

    def test_characters_keep_separate_progress(self):
        self.register()
        store.set_status(self.path, "matias", "approved")
        self.post("/characters/switch")
        self.post("/characters/new", dict(name="Rayo"))
        with store.connect(self.path) as db:
            ids = {r["name"]: r["id"] for r in db.execute("SELECT id, name FROM players")}
        store.award_xp(self.path, ids["Matías"], 40)
        self.post("/characters/select", dict(player_id=ids["Rayo"]))
        self.assertEqual(self.client.get("/api/me").json["player"]["xp"], 0)
        self.post("/characters/switch")
        self.post("/characters/select", dict(player_id=ids["Matías"]))
        self.assertEqual(self.client.get("/api/me").json["player"]["xp"], 40)


class AccountsMigrationTests(unittest.TestCase):
    def test_v10_players_become_accounts_without_losing_login_sessions_or_progress(self):
        with tempfile.TemporaryDirectory() as temp:
            config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                          DATA_DIR=temp, SESSION_COOKIE_SECURE=False)
            app = create_app(config)
            path = app.config["DATABASE"]
            # Dos jugadores con cuentas separadas.
            store.register(path, "matias", "Matías", generate_password_hash(PASSWORD))
            store.register(path, "javier", "Javier", generate_password_hash("otra clave larga"))
            raw = sqlite3.connect(path)
            undo_v11(raw)
            # En v10 los nombres podían repetirse: el más antiguo conserva el suyo.
            raw.execute("UPDATE players SET name = 'matias', level = 7 WHERE username = 'javier'")
            raw.execute("PRAGMA user_version = 10")
            raw.commit()
            self.assertEqual(raw.execute("SELECT count(*) FROM sessions").fetchone()[0], 2)
            raw.close()

            app = create_app(config)
            with store.connect(path) as db:
                self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
                accounts = {r["username"] for r in db.execute("SELECT username FROM accounts")}
                players = {r["username"]: dict(r) for r in db.execute(
                    "SELECT username, name, level, account_id, password_hash FROM players")}
                sessions = db.execute("SELECT count(*) FROM sessions WHERE account_id IS NOT NULL "
                                      "AND player_id IS NOT NULL").fetchone()[0]
                self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])
            self.assertEqual(accounts, {"matias", "javier"})
            self.assertEqual(players["matias"]["name"], "Matías")
            self.assertEqual(players["javier"]["name"], "matias 2")
            self.assertEqual(players["javier"]["level"], 7)
            self.assertTrue(all(p["password_hash"] == "" and p["account_id"] for p in players.values()))
            self.assertEqual(sessions, 2)

            client = app.test_client()
            page = client.get("/").get_data(as_text=True)
            csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
            response = client.post("/login", data=dict(username="javier", password="otra clave larga", csrf=csrf))
            self.assertEqual(response.status_code, 303)
            self.assertEqual(client.get("/api/me").json["player"]["level"], 7)


if __name__ == "__main__":
    unittest.main()
