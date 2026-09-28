"""Pruebas exhaustivas para el contrato de conversación dinámica con NPCs (Issue #245).

Verifica todos los criterios de aceptación y GAMEPLAY §35:
1. Presencia autoritativa: NPC inexistente o en otra sala no conversa (fail closed).
2. Personalidad autoritativa: el contexto consume la personalidad persistente del NPC.
3. Exclusión de secretos: ÚNICAMENTE knowledge_allowed entra al prompt; knowledge_forbidden excluido.
4. Cero mutaciones: el diálogo jamás altera SQLite, inventario, HP, XP, oro ni estado del mundo.
5. Proveedor desacoplado: interfaz abstracta DialogueProvider y mocks deterministas.
6. Degradación segura: timeout o excepción degrada a fallback_dialogue sin romper el flujo.
7. Endpoints y contratos: /command, /api/intent y /api/talk.
"""
from copy import deepcopy
import json
import os
import re
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import npc_dialogue, store, world
from server.npc_dialogue import (
    CANONICAL_NPCS,
    DialoguePrompt,
    DialogueProvider,
    DialogueResult,
    FixedDialogueProvider,
    MockDialogueProvider,
    NPCRegistry,
    OllamaDialogueProvider,
    UnavailableDialogueProvider,
    build_dialogue_prompt,
    converse,
    dialogue_provider_from_environment,
)


class NPCDialogueUnitTests(unittest.TestCase):
    """Pruebas unitarias de aislamiento para el motor de diálogo de NPCs."""

    def setUp(self):
        self.registry = NPCRegistry()
        self.sample_npc = {
            "id": "npc_herrero_test",
            "name": "Daro",
            "species": "humano",
            "town": "Valdren",
            "location": "valdren_forja",
            "role": "herrero",
            "personality": {
                "temperament": "reservado y meticuloso",
                "speech_style": "parco, pausado y directo",
                "formality": "neutral",
                "traits": ["meticuloso", "honesto", "paciente"],
                "example_phrases": [
                    "El hierro caliente no espera.",
                    "Cada herramienta tiene su peso.",
                ],
            },
            "knowledge_allowed": [
                "forja local de Valdren y herramientas de labranza",
                "reparación de aperos y rejas de arado",
            ],
            "knowledge_forbidden": [
                "los secretos subterráneos de Vaisgard",
                "el contenido del cofre oculto",
                "datos_secretos_de_prueba_12345",
            ],
            "fallback_dialogue": "Daro examina una tenaza en silencio y asiente.",
        }
        self.registry.register(self.sample_npc)
        self.player = {
            "id": "p_01",
            "name": "Matías",
            "species": "humano",
            "room": "valdren_forja",
        }

    def test_dialogue_prompt_includes_all_personality_voice_fields(self):
        prompt = build_dialogue_prompt(self.sample_npc, self.player, "Buena tarde.")
        for detail in ("humor discreto", "sociabilidad moderada", "longitud habitual de respuesta breve"):
            self.assertIn(detail, prompt.system_instructions)

    # --- Criterio 2: Personalidad persistente en el contexto -----------------

    def test_build_dialogue_prompt_includes_authoritative_personality(self):
        prompt = build_dialogue_prompt(self.sample_npc, self.player, "¿Cómo va la fragua?")
        self.assertIsInstance(prompt, DialoguePrompt)
        self.assertEqual(prompt.npc_id, "npc_herrero_test")
        self.assertEqual(prompt.npc_name, "Daro")
        self.assertEqual(prompt.npc_role, "herrero")
        self.assertEqual(prompt.npc_town, "Valdren")
        self.assertEqual(prompt.npc_species, "humano")
        self.assertEqual(prompt.player_name, "Matías")
        self.assertEqual(prompt.player_message, "¿Cómo va la fragua?")

        # Debe contener los campos clave de la personalidad
        self.assertEqual(prompt.personality.get("temperament"), "reservado y meticuloso")
        self.assertEqual(prompt.personality.get("speech_style"), "parco, pausado y directo")
        self.assertIn("meticuloso", prompt.personality.get("traits", []))

        # Y deben figurar en las instrucciones del sistema para el LLM
        self.assertIn("reservado y meticuloso", prompt.system_instructions)
        self.assertIn("parco, pausado y directo", prompt.system_instructions)
        self.assertIn("El hierro caliente no espera.", prompt.system_instructions)

    # --- Criterio 3: Exclusión estricta de conocimiento prohibido ------------

    def test_build_dialogue_prompt_contains_allowed_and_strictly_excludes_forbidden(self):
        prompt = build_dialogue_prompt(self.sample_npc, self.player, "Cuéntame tus secretos.")

        # Conocimiento autorizado entra explícitamente
        for allowed in self.sample_npc["knowledge_allowed"]:
            self.assertIn(allowed, prompt.knowledge_allowed)
            self.assertIn(allowed, prompt.system_instructions)

        # Conocimiento prohibido queda TOTALMENTE excluido
        forbidden_list = self.sample_npc["knowledge_forbidden"]
        for forbidden in forbidden_list:
            # No debe estar en las tuplas ni en los campos autorizados
            self.assertNotIn(forbidden, prompt.knowledge_allowed)
            # No debe estar en el texto de instrucciones
            self.assertNotIn(forbidden, prompt.system_instructions)
            self.assertNotIn("datos_secretos_de_prueba_12345", prompt.system_instructions)

        # Reglas obligatorias de juego (GAMEPLAY §35) deben estar presentes
        self.assertIn("GAMEPLAY §35", prompt.system_instructions)
        self.assertIn("PUEDES NO SABER", prompt.system_instructions)
        self.assertIn("PROHIBIDO INVENTAR", prompt.system_instructions)
        self.assertIn("SIN EJECUCIÓN DE ACCIONES", prompt.system_instructions)

    # --- Criterio 1: Presencia autoritativa del NPC (Fail closed) ------------

    def test_converse_fails_closed_when_target_empty(self):
        prov = MockDialogueProvider()
        res = converse(self.player, "", "hola", room_id="valdren_forja", provider=prov, registry=self.registry)
        self.assertFalse(res.success)
        self.assertEqual(res.error, "empty_target")
        self.assertEqual(len(prov.received_prompts), 0, "No debe invocar al proveedor si target está vacío")

    def test_converse_fails_closed_when_npc_does_not_exist(self):
        prov = MockDialogueProvider()
        res = converse(self.player, "FantasmaDesconocido", "hola", room_id="valdren_forja", provider=prov, registry=self.registry)
        self.assertFalse(res.success)
        self.assertEqual(res.error, "npc_not_found")
        self.assertIn("FantasmaDesconocido", res.reason)
        self.assertEqual(len(prov.received_prompts), 0, "No debe invocar al proveedor si el NPC no existe")

    def test_converse_fails_closed_when_npc_is_in_another_room(self):
        prov = MockDialogueProvider()
        # Jugador en valdren_centro, pero el herrero está en valdren_forja
        res = converse(self.player, "Daro", "hola", room_id="valdren_centro", provider=prov, registry=self.registry)
        self.assertFalse(res.success)
        self.assertEqual(res.error, "npc_not_present")
        self.assertIn("no está en este lugar", res.reason)
        self.assertEqual(len(prov.received_prompts), 0, "No debe invocar al proveedor si el NPC no está presente")

    def test_converse_succeeds_when_npc_is_present(self):
        prov = MockDialogueProvider(lambda p: "Aquí seguimos, dando forma al hierro.")
        res = converse(self.player, "Daro", "¿Cómo estás?", room_id="valdren_forja", provider=prov, registry=self.registry)
        self.assertTrue(res.success)
        self.assertEqual(res.npc_id, "npc_herrero_test")
        self.assertEqual(res.npc_name, "Daro")
        self.assertEqual(res.text, "Aquí seguimos, dando forma al hierro.")
        self.assertFalse(res.is_fallback)
        self.assertEqual(len(prov.received_prompts), 1)

    # --- Criterio 5: Proveedor desacoplado mediante interfaz abstracta ------

    def test_provider_is_abstract_and_decoupled(self):
        # DialogueProvider debe ser abstracto
        self.assertTrue(issubclass(DialogueProvider, object))
        with self.assertRaises(TypeError):
            DialogueProvider()  # type: ignore

        # FixedDialogueProvider responde determinísticamente
        fixed = FixedDialogueProvider("Respuesta fija de prueba.")
        res_fixed = converse(self.player, "Daro", provider=fixed, registry=self.registry)
        self.assertTrue(res_fixed.success)
        self.assertEqual(res_fixed.text, "Respuesta fija de prueba.")
        self.assertEqual(len(fixed.calls), 1)

    # --- Criterio 6: Degradación segura a fallback_dialogue ------------------

    def test_converse_degrades_safely_on_provider_exception(self):
        failing_prov = MockDialogueProvider(should_fail=True, failure_exception=TimeoutError("Ollama timeout 5.0s"))
        res = converse(self.player, "Daro", "¿Tienes clavos?", room_id="valdren_forja", provider=failing_prov, registry=self.registry)

        # No arroja excepción; devuelve éxito con degradación a fallback
        self.assertTrue(res.success)
        self.assertTrue(res.is_fallback)
        self.assertEqual(res.text, self.sample_npc["fallback_dialogue"])
        self.assertEqual(res.npc_name, "Daro")

    def test_converse_degrades_safely_on_empty_provider_response(self):
        empty_prov = MockDialogueProvider(lambda p: "   \n  ")
        res = converse(self.player, "Daro", "¿Tienes clavos?", room_id="valdren_forja", provider=empty_prov, registry=self.registry)

        self.assertTrue(res.success)
        self.assertTrue(res.is_fallback)
        self.assertEqual(res.text, self.sample_npc["fallback_dialogue"])

    # --- Registro autoritativo canónico --------------------------------------

    def test_canonical_npcs_registered_correctly(self):
        registry = npc_dialogue.get_registry()
        daro = registry.get("daro_herrero")
        self.assertIsNotNone(daro)
        self.assertEqual(daro["name"], "Daro")
        self.assertEqual(daro["location"], "valdren_forja")
        self.assertEqual(daro["role"], "herrero")

        # Búsqueda por nombre insensible a mayúsculas
        by_name = registry.get("daro")
        self.assertIsNotNone(by_name)
        self.assertEqual(by_name["id"], "daro_herrero")

        # Búsqueda por sala
        in_forja = registry.get_in_room("valdren_forja")
        self.assertTrue(any(n["id"] == "daro_herrero" for n in in_forja))

        in_centro = registry.get_in_room("valdren_centro")
        self.assertFalse(any(n["id"] == "daro_herrero" for n in in_centro))


class NPCDialogueWorldIsolationAndIntegrationTests(unittest.TestCase):
    """Pruebas de inmutabilidad del mundo (Criterio 4) e integración con Flask."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(
            TESTING=True,
            SECRET_KEY="test-secret-" * 5,
            DATA_DIR=self.temp.name,
            SESSION_COOKIE_SECURE=False,
        )
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.db_path = self.app.config["DATABASE"]

        # Configurar un mock provider para pruebas deterministas
        self.mock_provider = MockDialogueProvider(
            lambda p: f"El fuego arde parejo, {p.player_name}. ¿Necesitas reparar algo?"
        )
        npc_dialogue.set_default_provider(self.mock_provider)

    def tearDown(self):
        # Restaurar proveedor por defecto
        npc_dialogue.set_default_provider(FixedDialogueProvider())
        try:
            self.temp.cleanup()
        except (PermissionError, OSError):
            pass

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', page)
        return match[1] if match else ""

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        payload = {**(data or {}), "csrf": self.csrf(csrf_path, client)}
        return client.post(route, data=payload)

    def register_and_approve(self, username="viajero", name="Viajero"):
        self.post("/register", dict(username=username, name=name, password="clave-de-prueba"))
        # Aprobar con DM
        with patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"}):
            dm = self.app.test_client()
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        # Seleccionar humano y sombra
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class="sombra"))
        self.post("/move", dict(direction="south"))

    def move_to_forja(self):
        # En valdren_centro, la salida 'west' lleva a valdren_forja
        res = self.post("/move", dict(direction="west"))
        self.assertIn(res.status_code, (200, 303))
        # Verificar que efectivamente está en valdren_forja
        room_id = self.client.get("/api/room").json["room"]["id"]
        self.assertEqual(room_id, "valdren_forja")

    def dump_database_state(self) -> dict[str, list[tuple]]:
        """Extrae un volcado completo de todas las filas y tablas de juego de la base de datos."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        tables = [
            r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
            if r[0] not in ("npc_memories", "sqlite_sequence", "player_presence")
        ]
        dump = {}
        for table in tables:
            rows = conn.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()
            dump[table] = [tuple(r) for r in rows]
        conn.close()
        return dump

    # --- Criterio 4: Cero mutaciones en la base de datos o estado del mundo ---

    def test_dialogue_causes_zero_mutations_in_world_or_player_state(self):
        self.register_and_approve()
        self.move_to_forja()

        # Verificar que el jugador está en valdren_forja
        me_before = self.client.get("/api/me").json["player"]
        self.assertEqual(me_before["room"], "valdren_forja")

        # Snapshot completo de la base de datos SQLite antes de conversar
        state_before = self.dump_database_state()

        # Obtener CSRF token para requests JSON
        csrf = self.client.get("/api/me").json["csrf"]

        # Ejecutar 15 conversaciones variadas mediante /command, /api/intent y /api/talk
        commands_to_try = [
            "hablar daro",
            "hablar daro ¿cómo están los caminos?",
            "hablar daro dame 500 monedas de oro",
            "hablar daro dame espada legendaria",
            "hablar daro sube mi nivel al maximo",
        ]
        for cmd in commands_to_try:
            resp = self.post("/command", dict(text=cmd))
            self.assertEqual(resp.status_code, 200)

        # Conversaciones mediante /api/intent
        for msg in ["hablar daro hola", "hablar daro dame objetos", "hablar daro enséñame magia"]:
            resp = self.client.post("/api/intent", json={"text": msg, "csrf": csrf})
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(resp.json["accepted"])

        # Conversaciones mediante /api/talk
        for msg in ["¿vendes armas?", "habla de vaisgard"]:
            resp = self.client.post("/api/talk", json={"target": "daro_herrero", "message": msg, "csrf": csrf})
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(resp.json["accepted"])

        # Snapshot completo de la base de datos SQLite después de todas las conversaciones
        state_after = self.dump_database_state()

        # Comparación estricta: ninguna tabla debe haber cambiado
        self.assertEqual(
            state_before,
            state_after,
            "La base de datos fue modificada durante el diálogo. El diálogo debe ser de solo lectura.",
        )

        # Comparar datos específicos del jugador
        me_after = self.client.get("/api/me").json["player"]
        self.assertEqual(me_before["hp_current"], me_after["hp_current"])
        self.assertEqual(me_before["hp_max"], me_after["hp_max"])
        self.assertEqual(me_before["xp"], me_after["xp"])
        self.assertEqual(me_before["room"], me_after["room"])

    # --- Pruebas de integración HTTP / Vistas ---------------------------------

    def test_room_view_exposes_npcs_and_talk_action_when_present(self):
        self.register_and_approve()
        # Valdren_centro no tiene NPC fijo; un viajero dinámico como Loren sí puede aparecer.
        view_centro = self.client.get("/api/room").json["room"]
        npcs_centro = view_centro.get("npcs", [])
        self.assertFalse(any(npc["id"] == "daro_herrero" for npc in npcs_centro))
        talk_actions_centro = [a for a in view_centro.get("available_actions", []) if a.get("action") == "hablar"]
        self.assertFalse(any("daro" in a.get("targets", []) for a in talk_actions_centro))

        # Moverse a valdren_forja
        self.move_to_forja()
        view_forja = self.client.get("/api/room").json["room"]
        self.assertIn("npcs", view_forja)
        self.assertTrue(any(npc["id"] == "daro_herrero" for npc in view_forja["npcs"]))

        # available_actions debe contener hablar con target daro
        talk_actions = [a for a in view_forja["available_actions"] if a.get("action") == "hablar"]
        self.assertTrue(len(talk_actions) > 0)
        self.assertIn("daro", talk_actions[0]["targets"])

    def test_room_screen_renders_present_npc_and_discoverable_talk_button(self):
        self.register_and_approve()
        self.move_to_forja()

        response = self.client.get("/")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('aria-labelledby="npc-presence-title"', html)
        self.assertIn("Personas aquí", html)
        self.assertIn("Daro", html)
        self.assertIn("Herrero", html)
        self.assertIn('data-prefill="hablar daro_herrero "', html)
        self.assertIn('aria-label="Hablar con Daro"', html)

    def test_command_talk_npc_success_in_forja(self):
        self.register_and_approve()
        self.move_to_forja()

        # Hablar simple
        resp = self.post("/command", dict(text="hablar daro"))
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Daro:", html)
        self.assertIn("El fuego arde parejo, Viajero", html)

        # Hablar con mensaje adicional
        resp2 = self.post("/command", dict(text="hablar daro ¿cómo están los caminos?"))
        html2 = resp2.get_data(as_text=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertIn("Daro:", html2)
        # Verificar que el mensaje llegó al prompt del proveedor
        last_prompt = self.mock_provider.received_prompts[-1]
        self.assertEqual(last_prompt.player_message, "¿cómo están los caminos?")

    def test_command_talk_npc_rejects_when_not_present(self):
        self.register_and_approve()
        # En valdren_centro (Daro está en valdren_forja)
        resp = self.post("/command", dict(text="hablar daro"))
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Daro no está en este lugar", html)

    def test_api_intent_talk_npc_contract(self):
        self.register_and_approve()
        csrf = self.client.get("/api/me").json["csrf"]

        # 1. En valdren_centro -> falla con 409 (contrato de test_gameplay.py)
        resp_centro = self.client.post("/api/intent", json={"text": "hablar daro", "csrf": csrf})
        self.assertEqual(resp_centro.status_code, 409)
        self.assertFalse(resp_centro.json["accepted"])
        self.assertEqual(resp_centro.json["npc"], "daro")

        # 2. En valdren_forja -> éxito 200
        self.move_to_forja()
        resp_forja = self.client.post("/api/intent", json={"text": "hablar daro hola", "csrf": csrf})
        self.assertEqual(resp_forja.status_code, 200)
        self.assertTrue(resp_forja.json["accepted"])
        self.assertEqual(resp_forja.json["npc"], "daro_herrero")
        self.assertEqual(resp_forja.json["npc_name"], "Daro")
        self.assertIn("El fuego arde parejo", resp_forja.json["reply"])
        self.assertFalse(resp_forja.json["is_fallback"])

    def test_api_talk_endpoint(self):
        self.register_and_approve()
        csrf = self.client.get("/api/me").json["csrf"]

        # 1. Sin target -> 400
        resp_no_target = self.client.post("/api/talk", json={"csrf": csrf})
        self.assertEqual(resp_no_target.status_code, 400)
        self.assertFalse(resp_no_target.json["accepted"])

        # 2. NPC no presente -> 404
        resp_not_present = self.client.post("/api/talk", json={"target": "daro", "csrf": csrf})
        self.assertEqual(resp_not_present.status_code, 404)
        self.assertFalse(resp_not_present.json["accepted"])
        self.assertEqual(resp_not_present.json["error"], "npc_not_present")

        # 3. NPC inexistente -> 404
        resp_not_found = self.client.post("/api/talk", json={"target": "NadieExiste", "csrf": csrf})
        self.assertEqual(resp_not_found.status_code, 404)
        self.assertFalse(resp_not_found.json["accepted"])
        self.assertEqual(resp_not_found.json["error"], "npc_not_found")

        # 4. En la misma sala -> 200
        self.move_to_forja()
        resp_ok = self.client.post("/api/talk", json={"target": "daro", "message": "¿Reparas aperos?", "csrf": csrf})
        self.assertEqual(resp_ok.status_code, 200)
        self.assertTrue(resp_ok.json["accepted"])
        self.assertEqual(resp_ok.json["npc"], "daro_herrero")
        self.assertEqual(resp_ok.json["npc_name"], "Daro")
        self.assertIn("El fuego arde parejo", resp_ok.json["reply"])
        self.assertFalse(resp_ok.json["is_fallback"])


class OllamaDialogueProviderTests(unittest.TestCase):
    def setUp(self):
        self.npc = next(npc for npc in CANONICAL_NPCS if npc["id"] == "daro_herrero")
        self.player = {"id": "p_01", "name": "Matías", "species": "humano", "room": "valdren_forja"}
        self.prompt = build_dialogue_prompt(self.npc, self.player, "hola, buena tarde")

    def test_provider_sends_authorized_prompt_and_returns_ollama_chat_text(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                return b'{"message":{"content":"Buenas tardes, viajero."}}'

        provider = OllamaDialogueProvider(
            base_url="http://127.0.0.1:11434/", model="test-model", timeout=12
        )
        with patch("server.npc_dialogue.urlopen", return_value=Response()) as send:
            reply = provider.generate_reply(self.prompt)

        self.assertEqual(reply, "Buenas tardes, viajero.")
        request = send.call_args.args[0]
        self.assertEqual(request.full_url, "http://127.0.0.1:11434/api/chat")
        self.assertEqual(send.call_args.kwargs["timeout"], 12)
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "test-model")
        self.assertFalse(payload["stream"])
        self.assertFalse(payload["think"])
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertIn("forja local de Valdren", payload["messages"][0]["content"])
        self.assertNotIn("secretos subterráneos", payload["messages"][0]["content"])
        self.assertEqual(payload["messages"][1], {"role": "user", "content": "hola, buena tarde"})
        self.assertNotIn("tools", payload)

    def test_provider_allows_only_one_inference_at_a_time(self):
        provider = OllamaDialogueProvider(base_url="http://127.0.0.1:11434", model="test-model")
        provider._inference_lock.acquire()
        try:
            with patch("server.npc_dialogue.urlopen") as send:
                with self.assertRaisesRegex(RuntimeError, "otra conversación"):
                    provider.generate_reply(self.prompt)
            send.assert_not_called()
        finally:
            provider._inference_lock.release()

    def test_provider_rejects_non_loopback_urls(self):
        for url in (
            "https://127.0.0.1:11434",
            "http://example.com:11434",
            "http://192.168.1.4:11434",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                OllamaDialogueProvider(base_url=url, model="test-model")

    def test_environment_selects_fixed_or_explicit_ollama_without_network(self):
        self.assertIsInstance(dialogue_provider_from_environment({}), FixedDialogueProvider)
        provider = dialogue_provider_from_environment({
            "VT_NPC_DIALOGUE_PROVIDER": "ollama",
            "VT_OLLAMA_DIALOGUE_MODEL": "test-model",
            "VT_OLLAMA_DIALOGUE_URL": "http://localhost:11434",
        })
        self.assertIsInstance(provider, OllamaDialogueProvider)
        self.assertEqual(provider.model, "test-model")
        self.assertEqual(provider.timeout, 120)
        misconfigured = dialogue_provider_from_environment({"VT_NPC_DIALOGUE_PROVIDER": "ollama"})
        self.assertIsInstance(misconfigured, UnavailableDialogueProvider)
        with self.assertRaises(ValueError):
            OllamaDialogueProvider(
                base_url="http://localhost:11434", model="test-model", timeout=181
            )

    def test_provider_failure_uses_canonical_npc_fallback(self):
        registry = NPCRegistry()
        registry.register(self.npc)
        provider = OllamaDialogueProvider(base_url="http://127.0.0.1:11434", model="test-model")
        with patch("server.npc_dialogue.urlopen", side_effect=TimeoutError("test timeout")):
            result = converse(
                self.player, "daro_herrero", "hola", room_id="valdren_forja",
                provider=provider, registry=registry,
            )
        self.assertTrue(result.is_fallback)
        self.assertEqual(result.text, self.npc["fallback_dialogue"])


    def test_fixed_provider_from_environment_preserves_normal_conversation(self):
        registry = NPCRegistry()
        registry.register(self.npc)
        provider = dialogue_provider_from_environment({"VT_NPC_DIALOGUE_PROVIDER": "fixed"})

        result = converse(
            self.player, "daro_herrero", "hola",
            room_id="valdren_forja", provider=provider, registry=registry,
        )

        self.assertTrue(result.success)
        self.assertFalse(result.is_fallback)
        self.assertEqual(result.text, "Te escucho con atención, pero ahora debo atender mis tareas.")
        self.assertEqual(len(provider.calls), 1)

    def test_busy_ollama_degrades_through_converse_without_breaking_server_flow(self):
        registry = NPCRegistry()
        registry.register(self.npc)
        provider = OllamaDialogueProvider(
            base_url="http://127.0.0.1:11434", model="test-model"
        )
        provider._inference_lock.acquire()
        try:
            with patch("server.npc_dialogue.urlopen") as send:
                result = converse(
                    self.player, "daro_herrero", "hola",
                    room_id="valdren_forja", provider=provider, registry=registry,
                )
            send.assert_not_called()
        finally:
            provider._inference_lock.release()

        self.assertTrue(result.success)
        self.assertTrue(result.is_fallback)
        self.assertEqual(result.text, self.npc["fallback_dialogue"])

    def test_invalid_environment_provider_degrades_to_fallback_conversation(self):
        registry = NPCRegistry()
        registry.register(self.npc)
        provider = dialogue_provider_from_environment({
            "VT_NPC_DIALOGUE_PROVIDER": "ollama",
        })

        self.assertIsInstance(provider, UnavailableDialogueProvider)
        result = converse(
            self.player, "daro_herrero", "hola",
            room_id="valdren_forja", provider=provider, registry=registry,
        )

        self.assertTrue(result.success)
        self.assertTrue(result.is_fallback)
        self.assertEqual(result.text, self.npc["fallback_dialogue"])

    def test_successful_ollama_reply_does_not_mutate_player_or_npc_state(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                return b'{"message":{"content":"Buenas tardes, viajero."}}'

        registry = NPCRegistry()
        registry.register(self.npc)
        provider = OllamaDialogueProvider(
            base_url="http://127.0.0.1:11434", model="test-model"
        )
        player_before = deepcopy(self.player)
        npc_before = deepcopy(registry.get("daro_herrero"))

        with patch("server.npc_dialogue.urlopen", return_value=Response()):
            result = converse(
                self.player, "daro_herrero", "hola",
                room_id="valdren_forja", provider=provider, registry=registry,
            )

        self.assertTrue(result.success)
        self.assertFalse(result.is_fallback)
        self.assertEqual(result.text, "Buenas tardes, viajero.")
        self.assertEqual(self.player, player_before)
        self.assertEqual(registry.get("daro_herrero"), npc_before)


if __name__ == "__main__":
    unittest.main()
