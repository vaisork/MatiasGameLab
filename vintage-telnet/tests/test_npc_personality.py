import unittest

from server.npc_personality import (
    OllamaPersonalityClient,
    PersonalityError,
    enrich_personality_once,
    validate_personality,
)


GOOD_PERSONALITY = {
    "temperament": "Paciente, observador y poco impulsivo.",
    "speech_style": "Frases claras, con comparaciones tomadas de su oficio.",
    "formality": "neutral",
    "humor": "Humor seco y ocasional, nunca burlón con desconocidos.",
    "sociability": "Reservado al inicio; se vuelve cordial con visitas repetidas.",
    "response_length": "breve",
    "expressive_reactions": [
        "Hace una pausa antes de responder.",
        "Baja la voz cuando algo le preocupa.",
    ],
    "traits": ["prudente", "constante", "curioso"],
    "example_phrases": [
        "Mira dos veces antes de dar un paso.",
        "Ese camino parece tranquilo; parecer no es lo mismo que serlo.",
        "Si vuelves mañana, quizá recuerde algo más.",
    ],
}


class FakeClient:
    def __init__(self, payload=None):
        self.payload = payload or GOOD_PERSONALITY
        self.calls = 0
        self.model = "modelo-prueba:3b"

    def generate_personality(self, authoritative_npc):
        self.calls += 1
        self.last_input = authoritative_npc
        return validate_personality(self.payload)


class CaptureOllamaClient(OllamaPersonalityClient):
    def __init__(self):
        super().__init__(model="modelo-prueba:3b")
        self.captured = None

    def _json_request(self, path, *, method="GET", payload=None):
        self.captured = {"path": path, "method": method, "payload": payload}
        return {"response": __import__("json").dumps(GOOD_PERSONALITY, ensure_ascii=False)}


class NpcPersonalityTests(unittest.TestCase):
    def npc(self):
        return {
            "id": "valdren_herrero_01",
            "name": "Daro",
            "species": "humano",
            "town": "Valdren",
            "role": "herrero",
            "knowledge_allowed": ["forja local", "caminos cercanos"],
            "knowledge_forbidden": ["secreto_de_prueba"],
            "relationships": [],
        }

    def test_generates_once_and_locks_personality(self):
        client = FakeClient()
        original = self.npc()
        enriched = enrich_personality_once(
            original, client, generated_at="2026-09-22T07:00:00+00:00"
        )

        self.assertEqual(client.calls, 1)
        self.assertTrue(enriched["personality_locked"])
        self.assertEqual(enriched["personality"], GOOD_PERSONALITY)
        self.assertEqual(
            enriched["personality_provenance"]["ollama_model"], "modelo-prueba:3b"
        )
        self.assertEqual(
            enriched["personality_provenance"]["personality_prompt_version"],
            "vt-npc-personality-v2",
        )
        self.assertNotIn("personality", original)

    def test_locked_npc_never_calls_ollama_again(self):
        first_client = FakeClient()
        enriched = enrich_personality_once(self.npc(), first_client)
        second_client = FakeClient()

        again = enrich_personality_once(enriched, second_client)

        self.assertEqual(second_client.calls, 0)
        self.assertEqual(again, enriched)

    def test_authoritative_fields_are_unchanged(self):
        client = FakeClient()
        original = self.npc()
        enriched = enrich_personality_once(original, client)

        for key, value in original.items():
            self.assertEqual(enriched[key], value)
        self.assertNotIn("personality", client.last_input)
        self.assertNotIn("personality_locked", client.last_input)

    def test_rejects_unlocked_existing_personality_instead_of_overwriting(self):
        npc = self.npc()
        npc["personality"] = GOOD_PERSONALITY
        with self.assertRaises(PersonalityError):
            enrich_personality_once(npc, FakeClient())

    def test_rejects_extra_authoritative_fields_from_ollama(self):
        bad = dict(GOOD_PERSONALITY)
        bad["knowledge_allowed"] = ["algo inventado"]
        with self.assertRaises(PersonalityError):
            validate_personality(bad)

    def test_examples_are_required(self):
        bad = dict(GOOD_PERSONALITY)
        bad["example_phrases"] = []
        with self.assertRaises(PersonalityError):
            validate_personality(bad)

    def test_real_client_uses_schema_no_thinking_and_long_timeout(self):
        client = CaptureOllamaClient()
        personality = client.generate_personality(self.npc())

        self.assertEqual(personality, GOOD_PERSONALITY)
        self.assertEqual(client.timeout, 180.0)
        payload = client.captured["payload"]
        self.assertEqual(client.captured["path"], "/api/generate")
        self.assertEqual(client.captured["method"], "POST")
        self.assertIs(payload["think"], False)
        self.assertEqual(payload["options"]["temperature"], 0)
        self.assertIsInstance(payload["format"], dict)
        self.assertEqual(payload["format"]["type"], "object")
        self.assertFalse(payload["format"]["additionalProperties"])
        self.assertIn("expressive_reactions", payload["format"]["required"])
        self.assertEqual(payload["format"]["properties"]["expressive_reactions"]["minItems"], 1)


if __name__ == "__main__":
    unittest.main()
