"""Regresiones post-PR #386 para la frontera del proveedor de diálogo NPC.

No prueba un modelo real ni Raspberry. Protege únicamente integración/configuración:
- fixed sigue siendo el comportamiento predeterminado;
- provider ocupado o mal configurado degrada a fallback;
- Ollama sólo produce texto y no muta el estado jugable recibido.
"""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from server.npc_dialogue import (
    FixedDialogueProvider,
    OllamaDialogueProvider,
    NPCRegistry,
    UnavailableDialogueProvider,
    converse,
    dialogue_provider_from_environment,
)


NPC = {
    "id": "daro_herrero",
    "name": "Daro",
    "species": "humano",
    "town": "Valdren",
    "location": "valdren_forja",
    "role": "herrero",
    "personality": {
        "temperament": "reservado",
        "speech_style": "directo",
        "traits": ["honesto"],
    },
    "knowledge_allowed": ["forja local de Valdren"],
    "knowledge_forbidden": ["secreto de prueba que no debe salir"],
    "fallback_dialogue": "Daro asiente y vuelve a la fragua.",
}

PLAYER = {
    "id": "player-qa",
    "name": "Viajero QA",
    "species": "humano",
    "room": "valdren_forja",
    "hp_current": 73,
    "xp": 17,
    "level": 2,
}


class _Response:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _limit):
        return json.dumps({
            "message": {"content": "La fragua está ocupada, pero puedo escucharte."}
        }).encode("utf-8")


class OllamaProviderRegressionTests(unittest.TestCase):
    def setUp(self):
        self.registry = NPCRegistry()
        self.registry.register(NPC)

    def test_fixed_from_environment_preserves_normal_dialogue(self):
        provider = dialogue_provider_from_environment({})
        self.assertIsInstance(provider, FixedDialogueProvider)

        result = converse(
            PLAYER,
            "daro",
            "hola",
            room_id="valdren_forja",
            provider=provider,
            registry=self.registry,
        )

        self.assertTrue(result.success)
        self.assertFalse(result.is_fallback)
        self.assertIn("Te escucho con atención", result.text)

    def test_busy_ollama_degrades_through_converse_without_raising(self):
        provider = OllamaDialogueProvider(
            base_url="http://127.0.0.1:11434",
            model="modelo-prueba",
        )
        provider._inference_lock.acquire()
        try:
            result = converse(
                PLAYER,
                "daro",
                "hola",
                room_id="valdren_forja",
                provider=provider,
                registry=self.registry,
            )
        finally:
            provider._inference_lock.release()

        self.assertTrue(result.success)
        self.assertTrue(result.is_fallback)
        self.assertEqual(result.text, NPC["fallback_dialogue"])

    def test_invalid_runtime_configuration_fails_safe_to_fallback(self):
        cases = (
            {"VT_NPC_DIALOGUE_PROVIDER": "proveedor-inventado"},
            {"VT_NPC_DIALOGUE_PROVIDER": "ollama"},
            {
                "VT_NPC_DIALOGUE_PROVIDER": "ollama",
                "VT_OLLAMA_DIALOGUE_MODEL": "modelo-prueba",
                "VT_OLLAMA_DIALOGUE_URL": "http://192.168.1.50:11434",
            },
        )
        for config in cases:
            with self.subTest(config=config):
                provider = dialogue_provider_from_environment(config)
                self.assertIsInstance(provider, UnavailableDialogueProvider)
                result = converse(
                    PLAYER,
                    "daro",
                    "hola",
                    room_id="valdren_forja",
                    provider=provider,
                    registry=self.registry,
                )
                self.assertTrue(result.success)
                self.assertTrue(result.is_fallback)
                self.assertEqual(result.text, NPC["fallback_dialogue"])

    def test_successful_ollama_reply_does_not_mutate_player_state(self):
        player = deepcopy(PLAYER)
        before = deepcopy(player)
        provider = OllamaDialogueProvider(
            base_url="http://127.0.0.1:11434",
            model="modelo-prueba",
        )

        with patch("server.npc_dialogue.urlopen", return_value=_Response()):
            result = converse(
                player,
                "daro",
                "¿cómo va la forja?",
                room_id="valdren_forja",
                provider=provider,
                registry=self.registry,
            )

        self.assertTrue(result.success)
        self.assertFalse(result.is_fallback)
        self.assertEqual(result.text, "La fragua está ocupada, pero puedo escucharte.")
        self.assertEqual(player, before)


if __name__ == "__main__":
    unittest.main()
