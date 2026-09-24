from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

ADAPTER_PATH = Path(__file__).resolve().parents[1] / "npc_generator_adapter.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "npc-authoritative-synthetic.json"

adapter_spec = importlib.util.spec_from_file_location(
    "npc_generator_adapter",
    ADAPTER_PATH,
)
adapter = importlib.util.module_from_spec(adapter_spec)
assert adapter_spec and adapter_spec.loader
adapter_spec.loader.exec_module(adapter)

try:
    from server.npc_personality import (
        PersonalityError,
        enrich_personality_once,
        validate_personality,
    )
except ImportError:
    PersonalityError = None
    enrich_personality_once = None
    validate_personality = None


GOOD_PERSONALITY = {
    "temperament": "Paciente y observador.",
    "speech_style": "Frases breves y claras.",
    "formality": "neutral",
    "humor": "Seco y ligero.",
    "sociability": "Reservado al inicio.",
    "response_length": "breve",
    "expressive_reactions": [
        "Hace una pausa antes de responder."
    ],
    "traits": [
        "prudente",
        "constante"
    ],
    "example_phrases": [
        "Mira primero.",
        "No lo sé todavía.",
        "Eso es lo que puedo decir."
    ],
}


@unittest.skipIf(
    enrich_personality_once is None,
    "PR #20 server.npc_personality is not present on this branch",
)
class NpcGeneratorBridgeIntegrationTests(unittest.TestCase):
    class FakeClient:
        def __init__(self, payload=None):
            self.calls = 0
            self.model = "fake-integration:3b"
            self.payload = payload or GOOD_PERSONALITY

        def generate_personality(self, authoritative_npc):
            self.calls += 1
            self.last_input = deepcopy(authoritative_npc)
            return validate_personality(self.payload)

    def fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_real_bridge_generates_once_and_preserves_authority(self):
        client = self.FakeClient()
        original = self.fixture()

        first = adapter.enrich_generated_npc(
            original,
            client,
            enrich_fn=enrich_personality_once,
        )

        self.assertEqual(client.calls, 1)
        self.assertTrue(first["personality_locked"])
        self.assertEqual(
            first["personality_provenance"]["ollama_model"],
            "fake-integration:3b",
        )
        self.assertEqual(
            first["personality_provenance"]["personality_prompt_version"],
            "vt-npc-personality-v1",
        )
        for key, value in original.items():
            self.assertEqual(first[key], value)

        calls_before_second_pass = client.calls
        second = adapter.enrich_generated_npc(
            first,
            client,
            enrich_fn=enrich_personality_once,
        )

        self.assertEqual(second, first)
        self.assertEqual(client.calls, calls_before_second_pass)

    def test_real_bridge_rejects_authoritative_field_from_personality(self):
        payload = dict(GOOD_PERSONALITY)
        payload["knowledge_allowed"] = ["invented"]
        client = self.FakeClient(payload)

        with self.assertRaises(PersonalityError):
            adapter.enrich_generated_npc(
                self.fixture(),
                client,
                enrich_fn=enrich_personality_once,
            )


if __name__ == "__main__":
    unittest.main()
