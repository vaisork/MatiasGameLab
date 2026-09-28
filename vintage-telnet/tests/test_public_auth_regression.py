import re
import tempfile
import unittest

from server.app import create_app
from server import store


class PublicAuthRegressionTests(unittest.TestCase):
    """Issue #221: regresiones del borde público/autenticado.

    Esta suite añade solo huecos que no estaban cubiertos de forma directa:
    acceso anónimo a APIs protegidas y ausencia de mutación persistente al
    navegar/autenticarse inválidamente desde la superficie pública.
    """

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(
            TESTING=True,
            SECRET_KEY="test-secret-key-32-chars-long-abcde",
            DATA_DIR=self.temp.name,
            SESSION_COOKIE_SECURE=False,
        )
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def persistent_auth_counts(self):
        with store.connect(self.path) as db:
            return {
                table: db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                for table in ("accounts", "players", "sessions", "access_events")
            }

    def csrf_from(self, path="/"):
        html = self.client.get(path).get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', html)
        self.assertIsNotNone(match)
        return match[1]

    def test_public_navigation_does_not_create_persistent_auth_state(self):
        self.assertEqual(
            self.persistent_auth_counts(),
            {"accounts": 0, "players": 0, "sessions": 0, "access_events": 0},
        )

        for path in ("/", "/?view=login", "/?view=register", "/mundo", "/guia"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.persistent_auth_counts(),
            {"accounts": 0, "players": 0, "sessions": 0, "access_events": 0},
        )

    def test_guest_cannot_read_player_protected_apis(self):
        for path in ("/api/me", "/api/room", "/api/character", "/api/inventory", "/api/map"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 401)

        self.assertEqual(
            self.persistent_auth_counts(),
            {"accounts": 0, "players": 0, "sessions": 0, "access_events": 0},
        )

    def test_unknown_login_fails_without_creating_account_or_session(self):
        response = self.client.post(
            "/login",
            data={
                "username": "usuario_inexistente",
                "password": "clave-incorrecta-y-suficientemente-larga",
                "csrf": self.csrf_from("/?view=login"),
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Usuario o contraseña incorrectos.", response.get_data(as_text=True))
        self.assertEqual(
            self.persistent_auth_counts(),
            {"accounts": 0, "players": 0, "sessions": 0, "access_events": 0},
        )


if __name__ == "__main__":
    unittest.main()
