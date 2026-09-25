"""El panel del DM no existe desde internet (Tailscale Funnel); sí desde la
red privada o la propia Raspberry. Petición de Javier, 2026-09-25."""
import os
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import store

FUNNEL = {"Tailscale-Funnel-Request": "?1"}


@patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
class DmPrivateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, client, path="/"):
        return re.search(r'name="csrf" value="([^"]+)"', client.get(path).get_data(as_text=True))[1]

    def test_dm_panel_is_hidden_from_the_internet(self):
        client = self.app.test_client()
        self.assertEqual(client.get("/dm", headers=FUNNEL).status_code, 404)
        token = self.csrf(client)
        for route in ("/dm/login", "/dm/logout", "/dm/approve", "/dm/reject", "/dm/remove"):
            response = client.post(route, data={"csrf": token, "dm_password": "dm-secret-value",
                                                "username": "x"}, headers=FUNNEL)
            self.assertEqual(response.status_code, 404, route)

    def test_dm_panel_still_works_from_private_network(self):
        client = self.app.test_client()
        self.assertEqual(client.get("/dm").status_code, 200)
        client.post("/dm/login", data={"csrf": self.csrf(client, "/dm"), "dm_password": "dm-secret-value"})
        self.assertIn("Cerrar sesión", client.get("/dm").get_data(as_text=True))

    def test_private_dm_session_gives_no_power_over_the_internet(self):
        player = self.app.test_client()
        player.post("/register", data={"csrf": self.csrf(player), "username": "matias", "name": "Matías",
                                       "password": "una clave de prueba"})
        dm = self.app.test_client()
        dm.post("/dm/login", data={"csrf": self.csrf(dm, "/dm"), "dm_password": "dm-secret-value"})
        # La misma sesión de DM, pero la petición llega por Funnel: 404, sin aprobar a nadie.
        response = dm.post("/dm/approve", data={"csrf": self.csrf(dm, "/dm"), "username": "matias"},
                           headers=FUNNEL)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(store.list_by_status(self.path, "pending")[0]["username"], "matias")

    def test_players_are_unaffected_by_funnel(self):
        client = self.app.test_client()
        self.assertEqual(client.get("/", headers=FUNNEL).status_code, 200)
        self.assertEqual(client.get("/healthz", headers=FUNNEL).status_code, 200)


if __name__ == "__main__":
    unittest.main()
