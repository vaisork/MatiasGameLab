import os
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import store


class GameplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def register(self, username="matias", client=None, name="Matías"):
        return self.post("/register", dict(username=username, name=name, password="una clave de prueba"), client)

    def approve(self, username, dm_client=None):
        dm_client = dm_client or self.dm_client()
        self.post("/dm/approve", dict(username=username), dm_client, csrf_path="/dm")
        return dm_client

    def dm_client(self, password="dm-secret-value"):
        client = self.app.test_client()
        self.post("/dm/login", dict(dm_password=password), client, csrf_path="/dm")
        return client

    # --- Estado pendiente por defecto ------------------------------------

    def test_registration_defaults_to_pending_and_blocks_gameplay(self):
        self.register()
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["status"], "pending")
        self.assertIsNone(me["species"])
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn("pendiente de aprobación", page)
        self.assertEqual(self.post("/species", dict(species="humano")).status_code, 403)
        self.assertEqual(self.post("/move", dict(direction="north")).status_code, 403)
        self.assertEqual(self.client.get("/api/room").status_code, 403)

    # --- Panel del Dungeon Master -----------------------------------------

    def test_dm_panel_disabled_without_password_configured(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("VT_DM_PASSWORD", None)
            page = self.client.get("/dm").get_data(as_text=True)
            self.assertIn("no está configurado", page)
            response = self.post("/dm/login", dict(dm_password="cualquiera"), csrf_path="/dm")
            self.assertEqual(response.status_code, 503)

    @patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
    def test_dm_login_wrong_password_rejected(self):
        response = self.post("/dm/login", dict(dm_password="incorrecta"), csrf_path="/dm")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.post("/dm/approve", dict(username="matias"), csrf_path="/dm").status_code, 403)

    @patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
    def test_dm_can_see_and_approve_pending_account(self):
        self.register()
        dm = self.dm_client()
        panel = dm.get("/dm").get_data(as_text=True)
        self.assertIn("matias", panel)
        self.approve("matias", dm)
        self.assertEqual(self.client.get("/api/me").json["player"]["status"], "approved")

    @patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
    def test_dm_reject_blocks_without_revoking_session(self):
        self.register()
        dm = self.dm_client()
        self.post("/dm/reject", dict(username="matias"), dm, csrf_path="/dm")
        me = self.client.get("/api/me")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json["player"]["status"], "rejected")
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn("no está habilitada", page)

    @patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
    def test_dm_remove_revokes_session_immediately(self):
        self.register()
        self.approve("matias")
        self.post("/species", dict(species="humano"))
        dm = self.dm_client()
        self.post("/dm/remove", dict(username="matias"), dm, csrf_path="/dm")
        self.assertEqual(self.client.get("/api/me").status_code, 401)
        # Y no puede volver a entrar con las mismas credenciales.
        login = self.post("/login", dict(username="matias", password="una clave de prueba"))
        self.assertEqual(login.status_code, 303)
        self.assertEqual(self.client.get("/api/me").json["player"]["status"], "removed")

    # --- Especie y pueblo de inicio -----------------------------------------

    @patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
    def test_species_choice_sets_starting_room_once(self):
        self.register()
        self.approve("matias")
        self.post("/species", dict(species="felaryn"))
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["species"], "felaryn")
        self.assertEqual(me["room"], "khariel")
        # Elegir de nuevo no debe cambiar nada (ya tiene especie).
        self.post("/species", dict(species="humano"))
        me_again = self.client.get("/api/me").json["player"]
        self.assertEqual(me_again["species"], "felaryn")

    @patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
    def test_species_choice_rejects_unknown_species(self):
        self.register()
        self.approve("matias")
        response = self.post("/species", dict(species="elfo-clasico"))
        self.assertEqual(response.status_code, 400)

    # --- Movimiento y chat --------------------------------------------------

    @patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
    def test_movement_between_rooms_and_invalid_direction(self):
        self.register()
        self.approve("matias")
        self.post("/species", dict(species="felaryn"))  # starts in khariel, exit: west -> vaisgard
        self.assertEqual(self.client.get("/api/room").json["room"]["id"], "khariel")
        invalid = self.post("/move", dict(direction="north"))
        self.assertEqual(invalid.status_code, 400)
        self.assertEqual(self.client.get("/api/room").json["room"]["id"], "khariel")
        moved = self.post("/move", dict(direction="west"))
        self.assertEqual(moved.status_code, 303)
        self.assertEqual(self.client.get("/api/room").json["room"]["id"], "vaisgard")

    @patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
    def test_chat_is_local_to_room_and_visible_to_others(self):
        self.register("matias", name="Matías")
        self.approve("matias")
        self.post("/species", dict(species="felaryn"))  # khariel

        other = self.app.test_client()
        self.post("/register", dict(username="javier", name="Javier", password="otra clave de prueba"), other)
        self.approve("javier")
        self.post("/species", dict(species="felaryn"), other)  # también khariel

        self.post("/room/say", dict(body="Hola desde Khariel"))
        room = other.get("/api/room").json["room"]
        self.assertIn("Matías", room["others_present"])
        bodies = [m["body"] for m in room["messages"]]
        self.assertIn("Hola desde Khariel", bodies)

        # Se mueve y ya no debería verse en la sala anterior como presente.
        self.post("/move", dict(direction="west"))
        room_after = other.get("/api/room").json["room"]
        self.assertNotIn("Matías", room_after["others_present"])


if __name__ == "__main__":
    unittest.main()
