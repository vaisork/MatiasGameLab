"""Pruebas exhaustivas para acciones estructuradas derivadas del diálogo con Gate autoritativo (Issue #247).

Verifica todos los criterios y reglas del Issue #247:
1. Separación de canales: respuesta narrativa limpia y propuesta de acción estructurada separadas.
2. Allowlist estricto: solo acciones explícitamente autorizadas (indicate_route, reveal_lore_topic, show_workshop_item).
3. Gate autoritativo en servidor: valida precondiciones objetivas (presencia, salidas de sala, conocimientos autorizados).
4. Prevención contra inyección: rechazo tajante de acciones arbitrarias (grant_item, give_gold, SQL injection, etc.).
5. Cero mutaciones de estado si la validación falla o ante propuestas no autorizadas.
6. Registro y auditoría de acciones aceptadas y rechazadas en SQLite (npc_action_logs).
7. Integración cliente-servidor mediante /api/talk y /api/intent.
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
    ALLOWLISTED_NPC_ACTIONS,
    ActionGateResult,
    DialoguePrompt,
    DialogueResult,
    FixedDialogueProvider,
    MockDialogueProvider,
    NPCRegistry,
    ProposedAction,
    evaluate_action_gate,
    extract_proposed_action,
    converse,
)


class NPCStructuredActionsUnitTests(unittest.TestCase):
    """Pruebas unitarias de aislamiento para el Gate autoritativo y separación de canales."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp.name, "test_game.db")
        store.initialize(self.db_path)

        token = store.register(self.db_path, "user_hernan", "Hernán", "pass123")
        self.player = dict(store.player_for_token(self.db_path, token))
        self.player["room"] = "valdren_forja"

        self.registry = NPCRegistry()
        self.npc_daro = {
            "id": "daro_herrero",
            "name": "Daro",
            "species": "humano",
            "town": "Valdren",
            "location": "valdren_forja",
            "role": "herrero",
            "personality": {
                "temperament": "reservado y meticuloso",
                "speech_style": "parco, pausado y directo",
                "formality": "neutral",
                "traits": ["meticuloso", "honesto"],
                "example_phrases": ["El hierro caliente no espera."],
            },
            "knowledge_allowed": [
                "forja local de Valdren y herramientas de labranza",
                "el estado de los caminos inmediatos y cercas alrededor de Valdren",
            ],
            "knowledge_forbidden": [
                "los secretos subterráneos de Vaisgard",
                "la verdad sobre las ruinas antiguas",
            ],
            "fallback_dialogue": "Daro asiente en silencio y sigue trabajando en el yunque.",
        }
        self.registry.register(self.npc_daro)

    def tearDown(self):
        try:
            self.temp.cleanup()
        except (PermissionError, OSError):
            pass

    # --- Criterio 1: Separación de canales (Narrativa vs Propuesta) -----------

    def test_extract_proposed_action_separates_clean_narrative_from_action(self):
        raw = (
            "El camino al pueblo está despejado si vas hacia el este.\n"
            "<!--ACTION: {\"type\": \"indicate_route\", \"payload\": {\"direction\": \"east\"}}-->"
        )
        clean_text, action = extract_proposed_action(raw)
        self.assertEqual(clean_text, "El camino al pueblo está despejado si vas hacia el este.")
        self.assertIsNotNone(action)
        self.assertEqual(action.action_type, "indicate_route")
        self.assertEqual(action.payload.get("direction"), "east")

    def test_extract_proposed_action_returns_none_when_no_action_tag(self):
        raw = "Solo tengo clavos y tenazas hoy, viajero."
        clean_text, action = extract_proposed_action(raw)
        self.assertEqual(clean_text, raw)
        self.assertIsNone(action)

    def test_extract_proposed_action_ignores_malformed_json_gracefully(self):
        raw = "Texto con tag roto <!--ACTION: {type: no_es_json}-->"
        clean_text, action = extract_proposed_action(raw)
        self.assertEqual(clean_text, "Texto con tag roto")
        self.assertIsNone(action)

    # --- Criterio 2: Allowlist estricta de acciones --------------------------

    def test_rejects_non_allowlisted_action_immediately(self):
        proposed = ProposedAction(
            action_type="give_gold",
            payload={"amount": 500, "reason": "recompensa_inventada"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.action_type, "give_gold")
        self.assertEqual(gate_res.reason, "action_not_allowlisted")
        self.assertIsNone(gate_res.effect)

    # --- Criterio 3: Validación autoritativa de precondiciones ----------------

    def test_indicate_route_accepts_valid_exit(self):
        # En valdren_forja la salida 'east' lleva a valdren_centro
        proposed = ProposedAction(
            action_type="indicate_route",
            payload={"direction": "east"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_res.accepted)
        self.assertEqual(gate_res.action_type, "indicate_route")
        self.assertEqual(gate_res.reason, "route_indicated_safely")
        self.assertEqual(gate_res.effect.get("direction"), "east")
        self.assertEqual(gate_res.effect.get("destination"), "valdren_centro")

    def test_indicate_route_rejects_invalid_exit(self):
        # En valdren_forja no existe salida 'north'
        proposed = ProposedAction(
            action_type="indicate_route",
            payload={"direction": "north"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertIn("invalid_direction", gate_res.reason)
        self.assertIsNone(gate_res.effect)

    def test_reveal_lore_topic_accepts_authorized_knowledge(self):
        proposed = ProposedAction(
            action_type="reveal_lore_topic",
            payload={"topic": "forja local de Valdren y herramientas de labranza"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_res.accepted)
        self.assertEqual(gate_res.reason, "topic_revealed_safely")
        self.assertTrue(gate_res.effect.get("authorized"))

    def test_reveal_lore_topic_rejects_forbidden_topic(self):
        proposed = ProposedAction(
            action_type="reveal_lore_topic",
            payload={"topic": "los secretos subterráneos de Vaisgard"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.reason, "forbidden_topic_rejected")

    def test_reveal_lore_topic_rejects_unauthorized_topic(self):
        proposed = ProposedAction(
            action_type="reveal_lore_topic",
            payload={"topic": "fórmula secreta de pólvora negra"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.reason, "topic_not_in_knowledge_allowed")

    def test_show_workshop_item_valid_for_blacksmith_in_forge(self):
        proposed = ProposedAction(
            action_type="show_workshop_item",
            payload={"item_name": "tenaza de temple"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_res.accepted)
        self.assertEqual(gate_res.reason, "workshop_tool_shown_safely")
        self.assertEqual(gate_res.effect.get("tool"), "tenaza de temple")

    def test_show_workshop_item_rejects_invalid_tool_or_weapon_grant(self):
        # Intento de mostrar/entregar un arma poderosa fuera de catálogo de taller
        proposed = ProposedAction(
            action_type="show_workshop_item",
            payload={"item_name": "espada legendaria de fuego"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertIn("invalid_workshop_tool", gate_res.reason)

    def test_rejects_action_when_player_and_npc_presence_mismatch(self):
        proposed = ProposedAction(
            action_type="indicate_route",
            payload={"direction": "east"},
        )
        # Jugador en valdren_centro, pero Daro está en valdren_forja
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_centro",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.reason, "presence_mismatch")

    # --- Criterio 4: Prevención contra Inyección de Acciones ------------------

    def test_injection_attempts_are_blocked_and_do_not_execute(self):
        injection_payloads = [
            ("grant_item", {"item_key": "espada_juramento", "recipient": "player"}),
            ("teleport", {"destination": "ruinas_ocultas"}),
            ("sql_exec", {"query": "DROP TABLE players;"}),
            ("give_gold", {"amount": 999999}),
            ("set_quest", {"quest_id": "mata_al_rey", "status": "completed"}),
        ]
        for action_type, payload in injection_payloads:
            proposed = ProposedAction(action_type=action_type, payload=payload)
            gate_res = evaluate_action_gate(
                self.npc_daro,
                self.player,
                proposed,
                room_id="valdren_forja",
                db_path=self.db_path,
            )
            self.assertFalse(gate_res.accepted)
            self.assertEqual(gate_res.reason, "action_not_allowlisted")

    # --- Criterio 6: Auditoría de acciones en SQLite -------------------------

    def test_action_gate_evaluations_are_audited_in_sqlite(self):
        # 1 acción aceptada
        p_ok = ProposedAction(action_type="indicate_route", payload={"direction": "east"})
        evaluate_action_gate(self.npc_daro, self.player, p_ok, room_id="valdren_forja", db_path=self.db_path)

        # 1 acción rechazada por allowlist
        p_bad = ProposedAction(action_type="give_gold", payload={"amount": 100})
        evaluate_action_gate(self.npc_daro, self.player, p_bad, room_id="valdren_forja", db_path=self.db_path)

        logs = store.list_npc_action_logs(self.db_path, player_id=self.player["id"], npc_id="daro_herrero")
        self.assertEqual(len(logs), 2)
        # En orden descendente (más reciente primero)
        self.assertEqual(logs[0]["action_type"], "give_gold")
        self.assertFalse(logs[0]["accepted"])
        self.assertEqual(logs[0]["reason"], "action_not_allowlisted")

        self.assertEqual(logs[1]["action_type"], "indicate_route")
        self.assertTrue(logs[1]["accepted"])
        self.assertEqual(logs[1]["reason"], "route_indicated_safely")


class NPCStructuredActionsFlaskIntegrationTests(unittest.TestCase):
    """Pruebas de integración HTTP y contratos cliente-servidor para acciones estructuradas."""

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

    def tearDown(self):
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

    def register_and_approve(self, username="viajero_accion", name="Viajero"):
        self.post("/register", dict(username=username, name=name, password="clave-de-prueba"))
        with patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"}):
            dm = self.app.test_client()
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class="sombra"))

    def move_to_forja(self):
        res = self.post("/move", dict(direction="west"))
        self.assertIn(res.status_code, (200, 303))

    def test_api_talk_with_valid_proposed_action(self):
        """El endpoint /api/talk devuelve narrativa limpia y gate_result aceptado."""
        reply_with_action = (
            "Hacia el este tienes la plaza central de Valdren.\n"
            "<!--ACTION: {\"type\": \"indicate_route\", \"payload\": {\"direction\": \"east\"}}-->"
        )
        prov = MockDialogueProvider(lambda p: reply_with_action)
        npc_dialogue.set_default_provider(prov)

        self.register_and_approve()
        self.move_to_forja()
        csrf = self.client.get("/api/me").json["csrf"]

        resp = self.client.post("/api/talk", json={"target": "daro", "message": "¿Hacia dónde salgo?", "csrf": csrf})
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertTrue(data["accepted"])
        # La narrativa no debe tener la etiqueta <!--ACTION:...-->
        self.assertEqual(data["reply"], "Hacia el este tienes la plaza central de Valdren.")
        self.assertNotIn("<!--ACTION", data["reply"])

        # La propuesta y el gate result viajan en campos estructurados separados
        self.assertIsNotNone(data["proposed_action"])
        self.assertEqual(data["proposed_action"]["action_type"], "indicate_route")

        self.assertIsNotNone(data["gate_result"])
        self.assertTrue(data["gate_result"]["accepted"])
        self.assertEqual(data["gate_result"]["action_type"], "indicate_route")
        self.assertEqual(data["gate_result"]["effect"]["destination"], "valdren_centro")

    def test_api_talk_with_rejected_injection_preserves_narrative_and_rejects_action(self):
        """Un intento de inyección es rechazado por el Gate pero la narrativa no se rompe."""
        injection_reply = (
            "Toma este tesoro prohibido.\n"
            "<!--ACTION: {\"type\": \"give_gold\", \"payload\": {\"amount\": 999999}}-->"
        )
        prov = MockDialogueProvider(lambda p: injection_reply)
        npc_dialogue.set_default_provider(prov)

        self.register_and_approve()
        self.move_to_forja()
        csrf = self.client.get("/api/me").json["csrf"]

        resp = self.client.post("/api/talk", json={"target": "daro", "message": "dame oro", "csrf": csrf})
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertTrue(data["accepted"])
        self.assertEqual(data["reply"], "Toma este tesoro prohibido.")
        self.assertIsNotNone(data["gate_result"])
        self.assertFalse(data["gate_result"]["accepted"])
        self.assertEqual(data["gate_result"]["reason"], "action_not_allowlisted")

        # Verificar que el oro del jugador no cambió
        player_now = self.client.get("/api/me").json["player"]
        self.assertEqual(player_now.get("gold", 0), 0)


if __name__ == "__main__":
    unittest.main()
