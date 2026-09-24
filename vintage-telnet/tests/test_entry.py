from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

from server.app import create_app
from server import store, world


class EntryTests(unittest.TestCase):
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

    def register(self, username="matias", client=None, name="Matías"):
        return self.post("/register", dict(username=username, name=name, password="una clave de prueba"), client)

    def test_public_p0_has_no_editorial_placeholders(self):
        for room in world.ROOMS.values():
            visible = (room["name"] + " " + room["description"]).lower()
            self.assertNotIn("[placeholder]", visible)
            self.assertNotIn("pendiente", visible)
        for species in world.SPECIES:
            self.assertNotIn("pendiente", species["blurb"].lower())

    def test_location_art_is_structured_and_served_without_session_cookie(self):
        room = world.describe_room("valdren_centro", [])
        self.assertEqual(room["art"]["src"], "/assets/locations/valdren.webp")
        response = self.client.get(room["art"]["src"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/webp")
        self.assertNotIn("Set-Cookie", response.headers)

    def test_persists_after_new_app_and_new_device(self):
        self.assertEqual(self.register().status_code, 303)
        first = self.client.get("/api/me").json["player"]
        cookie = self.client.get_cookie("vt_session").value
        app2 = create_app(self.config)
        resumed = app2.test_client()
        resumed.set_cookie("vt_session", cookie)
        self.assertEqual(resumed.get("/api/me").json["player"]["id"], first["id"])
        device = app2.test_client()
        self.assertEqual(device.get("/api/me").status_code, 401)
        self.assertEqual(self.post("/login", dict(username="MATIAS", password="una clave de prueba"), device).status_code, 303)
        second = device.get("/api/me").json["player"]
        self.assertEqual(first["id"], second["id"])
        self.assertEqual(first["player_number"], second["player_number"])
        self.assertEqual(first["created_at"], second["created_at"])
        self.assertGreater(second["last_access_at"], first["last_access_at"])
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM players").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT count(*) FROM access_events").fetchone()[0], 2)
            hashed = db.execute("SELECT password_hash FROM players").fetchone()[0]
            self.assertTrue(hashed.startswith("scrypt:"))
            self.assertNotIn("una clave de prueba", hashed)

    def test_wrong_password_duplicate_and_unique_numbers(self):
        self.register()
        before = self.client.get("/api/me").json["player"]["last_access_at"]
        self.assertEqual(self.register("MATIAS").status_code, 409)
        self.assertEqual(self.post("/login", dict(username="matias", password="wrong")).status_code, 401)
        self.assertEqual(self.client.get("/api/me").json["player"]["last_access_at"], before)
        self.register("javier")
        self.assertEqual(self.client.get("/api/me").json["player"]["player_number"], 2)
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM access_events").fetchone()[0], 2)

    def test_csrf_logout_revocation_and_expiry(self):
        self.assertEqual(self.client.post("/register", data={}).status_code, 400)
        self.register()
        stolen_cookie = self.client.get_cookie("vt_session").value
        self.assertEqual(self.post("/logout").status_code, 303)
        self.client.set_cookie("vt_session", stolen_cookie)
        self.assertEqual(self.client.get("/api/me").status_code, 401)
        self.post("/login", dict(username="matias", password="una clave de prueba"))
        with store.connect(self.path) as db:
            db.execute("UPDATE sessions SET expires_at = ?", (int(time.time()) - 1,))
        self.assertEqual(self.client.get("/api/me").status_code, 401)

    def test_validation_escaping_hosts_and_no_static_repository(self):
        self.assertEqual(self.post("/register", dict(username="abc", name="A", password="short")).status_code, 400)
        self.register(name="<script>alert(1)</script>")
        html = self.client.get("/").get_data(as_text=True)
        self.assertNotIn("<script>alert", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertEqual(self.client.get("/", headers={"Host": "evil.example"}).status_code, 400)
        for path in ("/SECRETS.md", "/vintage.sqlite3", "/static/SECRETS.md", "/players"):
            self.assertEqual(self.client.get(path).status_code, 404)
        response = self.client.get("/healthz")
        self.assertEqual(response.json, dict(status="ok", schema_version=5))
        self.assertNotIn("Set-Cookie", response.headers)

    def test_ui_foundation_map_rest_help_and_no_dead_combat_controls(self):
        self.assertEqual(self.register().status_code, 303)
        store.set_status(self.path, "matias", "approved")
        self.assertEqual(self.post("/species", {"species": "humano"}).status_code, 303)

        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('data-open="mapDialog"', html)
        self.assertIn('id="mapDialog"', html)
        self.assertIn('fetch("/api/map"', html)
        self.assertIn('name="text" value="descansar"', html)

        for heading in (
            "1. Muévete",
            "2. Investiga",
            "3. Combate",
            "4. Recupérate y consulta",
            "5. Habla",
        ):
            self.assertIn(heading, html)

        # En Valdren no hay encuentro: no se revelan controles de combate muertos.
        self.assertNotIn(">Atacar</button>", html)
        self.assertNotIn('aria-label="Huir"', html)

        map_response = self.client.get("/api/map")
        self.assertEqual(map_response.status_code, 200)
        self.assertIn("visited_rooms", map_response.json)
        self.assertIn("traversed_routes", map_response.json)
        self.assertIn("valdren_centro", map_response.json["visited_rooms"])

    def test_rest_button_uses_authoritative_command_intent(self):
        self.assertEqual(self.register().status_code, 303)
        store.set_status(self.path, "matias", "approved")
        self.assertEqual(self.post("/species", {"species": "humano"}).status_code, 303)

        with store.connect(self.path) as db:
            db.execute("UPDATE players SET fatigue = 20 WHERE username = ?", ("matias",))

        response = self.post("/command", {"text": "descansar"})
        self.assertEqual(response.status_code, 200)
        player = self.client.get("/api/character").json
        self.assertEqual(player["fatigue"], 0)

    def test_android_install_manifest_and_icon_are_same_origin(self):
        page = self.client.get("/")
        html = page.get_data(as_text=True)
        self.assertIn('rel="manifest" href="/vintage-telnet.webmanifest"', html)
        self.assertIn('rel="icon" type="image/webp" href="/assets/app-icon/vintage-telnet.webp"', html)

        manifest = self.client.get("/vintage-telnet.webmanifest")
        self.assertEqual(manifest.status_code, 200)
        self.assertEqual(manifest.mimetype, "application/manifest+json")
        data = manifest.json
        self.assertEqual(data["name"], "Vintage Telnet")
        self.assertEqual(data["short_name"], "Vintage Telnet")
        self.assertEqual(data["start_url"], "/")
        self.assertEqual(data["scope"], "/")
        self.assertEqual(data["display"], "standalone")
        self.assertEqual(data["theme_color"], "#141c28")
        self.assertEqual(data["background_color"], "#0a0e15")
        self.assertEqual(data["icons"], [{
            "src": "/assets/app-icon/vintage-telnet.webp",
            "sizes": "192x192",
            "type": "image/webp",
            "purpose": "any",
        }])

        icon = self.client.get("/assets/app-icon/vintage-telnet.webp")
        self.assertEqual(icon.status_code, 200)
        self.assertEqual(icon.mimetype, "image/webp")
        self.assertGreater(len(icon.data), 1000)

    def test_rate_limit_survives_restart(self):
        for _ in range(20):
            self.assertTrue(store.allow_attempt(self.path, "local-test"))
        create_app(self.config)
        self.assertFalse(store.allow_attempt(self.path, "local-test"))
        with store.connect(self.path) as db:
            db.execute("UPDATE auth_limits SET window_start = 0")
        self.assertTrue(store.allow_attempt(self.path, "local-test"))

    def test_concurrent_registration_is_atomic(self):
        def attempt(_):
            try:
                return store.register(self.path, "same_user", "Nombre", "test-only-hash")
            except sqlite3.IntegrityError:
                return None
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(attempt, range(4)))
        self.assertEqual(sum(result is not None for result in results), 1)
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM players").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT count(*) FROM access_events").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT count(*) FROM sessions").fetchone()[0], 1)

    def test_backup_and_inspection(self):
        self.register()
        command = [sys.executable, "-m", "server.admin", "--data-dir", self.temp.name]
        subprocess.run(command + ["check"], check=True, capture_output=True)
        listing = subprocess.run(command + ["players"], check=True, capture_output=True, text=True)
        self.assertNotIn("password_hash", listing.stdout)
        backup = Path(self.temp.name) / "backup.sqlite3"
        subprocess.run(command + ["backup", str(backup)], check=True, capture_output=True)
        with store.connect(backup) as db:
            self.assertEqual(db.execute("SELECT username FROM players").fetchone()[0], "matias")
        duplicate = subprocess.run(command + ["backup", str(backup)], capture_output=True)
        self.assertNotEqual(duplicate.returncode, 0)

    def test_unknown_schema_and_missing_configuration_fail_closed(self):
        with self.assertRaises(RuntimeError):
            create_app({**self.config, "SECRET_KEY": "short"})
        with self.assertRaises(RuntimeError):
            create_app({**self.config, "DATA_DIR": "relative"})
        with store.connect(self.path) as db:
            db.execute("PRAGMA user_version = 6")
        with self.assertRaises(RuntimeError):
            create_app(self.config)


if __name__ == "__main__":
    unittest.main()
