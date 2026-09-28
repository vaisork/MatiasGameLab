"""Pruebas exhaustivas para VT-SERVER: HOSHAI-WEAPON-01 (#287).

Contrato autoritativo (HOSHAI_WEAPON_SCENE.md / PR #426 / GAMEPLAY.md §§22, 32):
1. Aren (khariel_taller_hoshai_01) presente en khariel_forja.
2. Petición inicial de ayuda si el jugador no ha ayudado ("Si vas a quedarte un momento, sujeta desde ahí...").
3. Resolución de ayuda (hoshai_paso_ayudado) al ofrecer colaboración o usar comando 'ayudar'/'sujetar'.
4. Entrega única de Hoja de Hoshai (hoshai_hoja_recibida, item_key="hoja_hoshai", forge_validated=False).
5. Sin autoequipar, sin XP, sin alteración de nivel ni atributos.
6. Idempotencia y revisitas: no duplica el objeto, respuesta sobria de cumplimiento.
7. Sin requisitos de especie o clase.
8. Persistencia y aislamiento entre personajes.
"""
import os
import tempfile
import unittest

from server.app import create_app
from server import npc_dialogue, store, world


class HoshaiWeaponSceneTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "vintage.sqlite3")
        store.initialize(self.db_path)

        self.app = create_app({
            "TESTING": True,
            "DATA_DIR": self.temp_dir.name,
            "SECRET_KEY": "test-secret-" * 4,
            "SESSION_COOKIE_SECURE": False,
        })
        self.client = self.app.test_client()

        # Crear jugador de prueba en khariel_forja
        self.token = store.register(self.db_path, "felaryn_tester", "Kaelen", "pass123456")
        self.player = dict(store.player_for_token(self.db_path, self.token))
        self.player_id = self.player["id"]
        with store.connect(self.db_path) as db:
            db.execute(
                "UPDATE players SET status = 'approved', species = 'felaryn', player_class = 'sombra', room = 'khariel_forja' WHERE id = ?",
                (self.player_id,)
            )
        self.player = dict(store.player_for_token(self.db_path, self.token))

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_aren_present_in_khariel_forja(self):
        """Aren debe estar registrado y presente como NPC en khariel_forja."""
        registry = npc_dialogue.get_registry()
        aren = registry.get("khariel_taller_hoshai_01")
        self.assertIsNotNone(aren)
        self.assertEqual(aren["name"], "Aren")
        self.assertEqual(aren["location"], "khariel_forja")
        self.assertEqual(aren["town"], "Khariel")

        in_room = registry.get_in_room("khariel_forja")
        self.assertTrue(any(n["id"] == "khariel_taller_hoshai_01" for n in in_room))

    def test_initial_talk_requests_help(self):
        """Al hablar con Aren sin haber ayudado, Aren pide sujetar el amarre."""
        result = npc_dialogue.converse(
            self.player,
            "khariel_taller_hoshai_01",
            message="Buenos días",
            room_id="khariel_forja",
            db_path=self.db_path,
        )
        self.assertTrue(result.success)
        self.assertIn("sujeta desde ahí", result.text)
        self.assertFalse(store.get_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado"))
        self.assertFalse(store.get_story_flag(self.db_path, self.player_id, "hoshai_hoja_recibida"))
        self.assertEqual(len(store.list_inventory(self.db_path, self.player_id)), 0)

    def test_talk_offering_help_resolves_scene_and_grants_weapon(self):
        """Ofrecer ayuda en el diálogo resuelve el amarre y entrega la Hoja de Hoshai."""
        char_before = store.character_by_player_id(self.db_path, self.player_id)
        initial_xp = char_before["xp"]
        initial_level = char_before["level"]

        result = npc_dialogue.converse(
            self.player,
            "Aren",
            message="Te ayudo a sujetar el paso",
            room_id="khariel_forja",
            db_path=self.db_path,
        )
        self.assertTrue(result.success)
        self.assertIn("vuelven a tensar el amarre", result.text)
        self.assertIn("No todos los que pasan se detienen", result.text)
        self.assertIn("Te confían una Hoja de Hoshai todavía pendiente de Forja", result.text)

        # Verificar flags
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado"))
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_hoja_recibida"))

        # Verificar inventario
        inv = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual(len(inv), 1)
        self.assertEqual(inv[0]["item_key"], "hoja_hoshai")
        self.assertEqual(inv[0]["category"], "weapon")
        self.assertEqual(inv[0]["forge_validated"], 0, "Debe entrar con forge_validated=False")

        # Verificar que NO se autoequipa ni altera nivel/XP
        char_after = store.character_by_player_id(self.db_path, self.player_id)
        self.assertNotEqual(char_after["equipped_weapon_id"], inv[0]["id"], "No debe autoequiparse")
        self.assertEqual(char_after["xp"], initial_xp)
        self.assertEqual(char_after["level"], initial_level)

    def test_revisit_talk_does_not_duplicate_weapon(self):
        """Al hablar con Aren después de recibir la hoja, no entrega otra y responde con texto canónico."""
        # Primera interacción: ayuda
        npc_dialogue.converse(
            self.player,
            "khariel_taller_hoshai_01",
            message="ayudo a tensar",
            room_id="khariel_forja",
            db_path=self.db_path,
        )
        self.assertEqual(len(store.list_inventory(self.db_path, self.player_id)), 1)

        # Segunda interacción / revisita
        result_revisit = npc_dialogue.converse(
            self.player,
            "khariel_taller_hoshai_01",
            message="¿Tienes más trabajo?",
            room_id="khariel_forja",
            db_path=self.db_path,
        )
        self.assertTrue(result_revisit.success)
        self.assertIn("Ya cumpliste aquí", result_revisit.text)
        self.assertIn("no hay otra esperando", result_revisit.text)

        # El inventario debe seguir conteniendo únicamente 1 hoja
        inv_after = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual(len(inv_after), 1)

    def test_terminal_command_ayudar_resolves_scene_in_khariel_forja(self):
        """El comando de terminal 'ayudar' resuelve la escena si el jugador está en khariel_forja."""
        with self.client.session_transaction() as sess:
            sess["token"] = self.token
            sess["csrf"] = "test-csrf"

        resp = self.client.post("/api/intent", json={"text": "ayudar", "csrf": "test-csrf"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertTrue(data["accepted"])
        self.assertEqual(data["intent"], "help_scene")
        self.assertEqual(data["npc"], "khariel_taller_hoshai_01")
        self.assertIn("vuelven a tensar el amarre", data["reply"])
        self.assertIn("Te confían una Hoja de Hoshai", data["reply"])

        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_paso_ayudado"))
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_hoja_recibida"))
        inv = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual(len(inv), 1)
        self.assertEqual(inv[0]["item_key"], "hoja_hoshai")

    def test_terminal_command_ayudar_rejected_in_other_rooms(self):
        """El comando 'ayudar' en otra sala donde no hay escena es rechazado limpiamente."""
        store.move_player(self.db_path, self.player_id, "khariel_centro")
        with self.client.session_transaction() as sess:
            sess["token"] = self.token
            sess["csrf"] = "test-csrf"

        resp = self.client.post("/api/intent", json={"text": "ayudar", "csrf": "test-csrf"})
        self.assertEqual(resp.status_code, 400)
        data = resp.json
        self.assertFalse(data["accepted"])
        self.assertIn("No hay ninguna tarea o paso que asegurar aquí", data["reason"])

    def test_player_isolation(self):
        """Los hitos y la recompensa de un jugador no afectan a otros personajes."""
        token2 = store.register(self.db_path, "humano_p2", "Valen", "pass123456")
        p2 = dict(store.player_for_token(self.db_path, token2))
        with store.connect(self.db_path) as db:
            db.execute(
                "UPDATE players SET status = 'approved', species = 'humano', player_class = 'juramentado', room = 'khariel_forja' WHERE id = ?",
                (p2["id"],)
            )
        p2 = dict(store.player_for_token(self.db_path, token2))

        # Jugador 1 ayuda y recibe la hoja
        npc_dialogue.converse(self.player, "Aren", message="ayudo", room_id="khariel_forja", db_path=self.db_path)
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "hoshai_hoja_recibida"))

        # Jugador 2 NO tiene flags ni hoja
        self.assertFalse(store.get_story_flag(self.db_path, p2["id"], "hoshai_paso_ayudado"))
        self.assertFalse(store.get_story_flag(self.db_path, p2["id"], "hoshai_hoja_recibida"))
        self.assertEqual(len(store.list_inventory(self.db_path, p2["id"])), 0)

        # Jugador 2 habla con Aren y recibe la petición inicial
        result_p2 = npc_dialogue.converse(p2, "Aren", message="hola", room_id="khariel_forja", db_path=self.db_path)
        self.assertIn("sujeta desde ahí", result_p2.text)


if __name__ == "__main__":
    unittest.main()
