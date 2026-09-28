"""Pruebas exhaustivas para VT-SERVER: KORVEN-WEAPON-01 (#288).

Contrato autoritativo (KORVEN_WEAPON_SCENE.md / PR #288 / GAMEPLAY.md §§22, 32):
1. Karn (brumak_taller_korven_01) presente en brumak_forja.
2. Petición inicial de ayuda si el jugador no ha ayudado ("—Sostén ese extremo. Yo corrijo el apoyo...").
3. Resolución de ayuda (korven_trabajo_ayudado) al ofrecer colaboración o usar comando 'ayudar'/'sostener'.
4. Entrega única de Martillo de Korven (korven_martillo_recibido, item_key="martillo_korven", forge_validated=False).
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


class KorvenWeaponSceneTests(unittest.TestCase):
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

        # Crear jugador de prueba en brumak_forja
        self.token = store.register(self.db_path, "dravak_tester", "Drokhar", "pass123456")
        self.player = dict(store.player_for_token(self.db_path, self.token))
        self.player_id = self.player["id"]
        with store.connect(self.db_path) as db:
            db.execute(
                "UPDATE players SET status = 'approved', species = 'dravak', player_class = 'juramentado', room = 'brumak_forja' WHERE id = ?",
                (self.player_id,)
            )
        self.player = dict(store.player_for_token(self.db_path, self.token))

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_karn_present_in_brumak_forja(self):
        """Karn debe estar registrado y presente como NPC en brumak_forja."""
        registry = npc_dialogue.get_registry()
        karn = registry.get("brumak_taller_korven_01")
        self.assertIsNotNone(karn)
        self.assertEqual(karn["name"], "Karn")
        self.assertEqual(karn["location"], "brumak_forja")
        self.assertEqual(karn.get("settlement", karn.get("town")), "Brumak")

        in_room = registry.get_in_room("brumak_forja")
        self.assertTrue(any(n["id"] == "brumak_taller_korven_01" for n in in_room))

    def test_initial_talk_requests_help(self):
        """Al hablar con Karn sin haber ayudado, Karn pide sostener el extremo del apoyo."""
        result = npc_dialogue.converse(
            self.player,
            "brumak_taller_korven_01",
            message="Buenos días",
            room_id="brumak_forja",
            db_path=self.db_path,
        )
        self.assertTrue(result.success)
        self.assertIn("Sostén ese extremo", result.text)
        self.assertFalse(store.get_story_flag(self.db_path, self.player_id, "korven_trabajo_ayudado"))
        self.assertFalse(store.get_story_flag(self.db_path, self.player_id, "korven_martillo_recibido"))
        self.assertEqual(len(store.list_inventory(self.db_path, self.player_id)), 0)

    def test_talk_offering_help_resolves_scene_and_grants_weapon(self):
        """Ofrecer ayuda en el diálogo resuelve la carga y entrega el Martillo de Korven."""
        char_before = store.character_by_player_id(self.db_path, self.player_id)
        initial_xp = char_before["xp"]
        initial_level = char_before["level"]

        result = npc_dialogue.converse(
            self.player,
            "Karn",
            message="Te ayudo a sostener el apoyo de la carga",
            room_id="brumak_forja",
            db_path=self.db_path,
        )
        self.assertTrue(result.success)
        self.assertIn("El apoyo vuelve a quedar bajo el peso correcto", result.text)
        self.assertIn("sabe cuándo hacer fuerza y cuándo sostener", result.text)
        self.assertIn("Te entregan un Martillo de Korven", result.text)

        # Verificar flags
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "korven_trabajo_ayudado"))
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "korven_martillo_recibido"))

        # Verificar inventario
        inv = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual(len(inv), 1)
        self.assertEqual(inv[0]["item_key"], "martillo_korven")
        self.assertEqual(inv[0]["category"], "weapon")
        self.assertEqual(inv[0]["forge_validated"], 0, "Debe entrar con forge_validated=False")

        # Verificar que NO se autoequipa ni altera nivel/XP
        char_after = store.character_by_player_id(self.db_path, self.player_id)
        self.assertNotEqual(char_after["equipped_weapon_id"], inv[0]["id"], "No debe autoequiparse")
        self.assertEqual(char_after["xp"], initial_xp)
        self.assertEqual(char_after["level"], initial_level)

    def test_revisit_talk_does_not_duplicate_weapon(self):
        """Al hablar con Karn después de recibir el martillo, no entrega otro y responde con texto canónico."""
        # Primera interacción: ayuda
        npc_dialogue.converse(
            self.player,
            "brumak_taller_korven_01",
            message="ayudo a sostener",
            room_id="brumak_forja",
            db_path=self.db_path,
        )
        self.assertEqual(len(store.list_inventory(self.db_path, self.player_id)), 1)

        # Segunda interacción / revisita
        result_revisit = npc_dialogue.converse(
            self.player,
            "brumak_taller_korven_01",
            message="¿Hay algo más que hacer?",
            room_id="brumak_forja",
            db_path=self.db_path,
        )
        self.assertTrue(result_revisit.success)
        self.assertIn("Ya cumpliste aquí", result_revisit.text)
        self.assertIn("no hay otra esperando", result_revisit.text)

        # El inventario debe seguir conteniendo únicamente 1 martillo
        inv_after = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual(len(inv_after), 1)

    def test_terminal_command_ayudar_resolves_scene_in_brumak_forja(self):
        """El comando de terminal 'ayudar' o 'sostener' resuelve la escena si el jugador está en brumak_forja."""
        with self.client.session_transaction() as sess:
            sess["token"] = self.token
            sess["csrf"] = "test-csrf"

        resp = self.client.post("/api/intent", json={"text": "sostener", "csrf": "test-csrf"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertTrue(data["accepted"])
        self.assertEqual(data["intent"], "help_scene")
        self.assertEqual(data["npc"], "brumak_taller_korven_01")
        self.assertIn("El apoyo vuelve a quedar bajo el peso correcto", data["reply"])
        self.assertIn("Te entregan un Martillo de Korven", data["reply"])

        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "korven_trabajo_ayudado"))
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "korven_martillo_recibido"))
        inv = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual(len(inv), 1)
        self.assertEqual(inv[0]["item_key"], "martillo_korven")

    def test_terminal_command_ayudar_rejected_in_other_rooms(self):
        """El comando 'ayudar' en otra sala donde no hay escena es rechazado limpiamente."""
        store.move_player(self.db_path, self.player_id, "brumak_centro")
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
                "UPDATE players SET status = 'approved', species = 'humano', player_class = 'artifice', room = 'brumak_forja' WHERE id = ?",
                (p2["id"],)
            )
        p2 = dict(store.player_for_token(self.db_path, token2))

        # Jugador 1 ayuda y recibe el martillo
        npc_dialogue.converse(self.player, "Karn", message="ayudo", room_id="brumak_forja", db_path=self.db_path)
        self.assertTrue(store.get_story_flag(self.db_path, self.player_id, "korven_martillo_recibido"))

        # Jugador 2 NO tiene flags ni martillo
        self.assertFalse(store.get_story_flag(self.db_path, p2["id"], "korven_trabajo_ayudado"))
        self.assertFalse(store.get_story_flag(self.db_path, p2["id"], "korven_martillo_recibido"))
        self.assertEqual(len(store.list_inventory(self.db_path, p2["id"])), 0)

        # Jugador 2 habla con Karn y recibe la petición inicial
        result_p2 = npc_dialogue.converse(p2, "Karn", message="hola", room_id="brumak_forja", db_path=self.db_path)
        self.assertIn("Sostén ese extremo", result_p2.text)


    def test_legacy_help_flag_is_migrated_and_progress_is_preserved(self):
        """Un jugador antiguo conserva progreso sin mantener dos flags ni ganar XP."""
        char_before = store.character_by_player_id(self.db_path, self.player_id)
        xp_before = char_before["xp"]
        level_before = char_before["level"]

        # Simula estado producido por la implementación anterior a #466.
        store.set_story_flag(self.db_path, self.player_id, "korven_carga_asentada", True)
        self.assertFalse(store.get_story_flag(
            self.db_path, self.player_id, "korven_trabajo_ayudado"
        ))

        result = npc_dialogue.converse(
            self.player,
            "brumak_taller_korven_01",
            message="hola",
            room_id="brumak_forja",
            db_path=self.db_path,
        )

        self.assertTrue(result.success)
        self.assertTrue(store.get_story_flag(
            self.db_path, self.player_id, "korven_trabajo_ayudado"
        ))
        self.assertFalse(store.get_story_flag(
            self.db_path, self.player_id, "korven_carga_asentada"
        ))
        self.assertTrue(store.get_story_flag(
            self.db_path, self.player_id, "korven_martillo_recibido"
        ))
        inv = store.list_inventory(self.db_path, self.player_id)
        self.assertEqual([item["item_key"] for item in inv], ["martillo_korven"])

        char_after = store.character_by_player_id(self.db_path, self.player_id)
        self.assertEqual(char_after["xp"], xp_before)
        self.assertEqual(char_after["level"], level_before)

        # Restart/retry: el estado canónico persiste y no entrega otro martillo.
        store.initialize(self.db_path)
        retry = npc_dialogue.converse(
            dict(store.character_by_player_id(self.db_path, self.player_id)),
            "brumak_taller_korven_01",
            message="ayudo otra vez",
            room_id="brumak_forja",
            db_path=self.db_path,
        )
        self.assertIn("Ya cumpliste aquí", retry.text)
        self.assertEqual(
            [item["item_key"] for item in store.list_inventory(self.db_path, self.player_id)],
            ["martillo_korven"],
        )
        self.assertFalse(store.get_story_flag(
            self.db_path, self.player_id, "korven_carga_asentada"
        ))

    def test_room_view_migrates_legacy_flag_and_does_not_offer_help_again(self):
        """La lectura autoritativa de la forja reconcilia legacy sin reabrir la tarea."""
        store.set_story_flag(self.db_path, self.player_id, "korven_carga_asentada", True)
        with self.client.session_transaction() as sess:
            sess["token"] = self.token
            sess["csrf"] = "test-csrf"

        room = self.client.get("/api/room").json["room"]
        help_actions = [
            action for action in room.get("available_actions", [])
            if action.get("action") == "ayudar"
        ]
        self.assertEqual(help_actions, [])
        self.assertTrue(store.get_story_flag(
            self.db_path, self.player_id, "korven_trabajo_ayudado"
        ))
        self.assertFalse(store.get_story_flag(
            self.db_path, self.player_id, "korven_carga_asentada"
        ))


if __name__ == "__main__":
    unittest.main()
