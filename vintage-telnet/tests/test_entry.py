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
from server import store


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
        self.assertEqual(response.json, dict(status="ok", schema_version=2))
        self.assertNotIn("Set-Cookie", response.headers)

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
            db.execute("PRAGMA user_version = 3")
        with self.assertRaises(RuntimeError):
            create_app(self.config)


if __name__ == "__main__":
    unittest.main()
