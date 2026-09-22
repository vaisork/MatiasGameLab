from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "npc_generator_adapter.py"
spec = importlib.util.spec_from_file_location("npc_generator_adapter", MODULE_PATH)
adapter = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(adapter)


PERSONALITY = {
    "temperament": "calm",
    "speech_style": "brief",
    "formality": "neutral",
    "humor": "dry",
    "sociability": "reserved",
    "response_length": "breve",
    "expressive_reactions": ["pauses"],
    "traits": ["patient", "observant"],
    "example_phrases": ["A", "B", "C"],
}


def synthetic_npc(npc_id="test_npc_001"):
    return {
        "id": npc_id,
        "name": "Synthetic NPC",
        "species": "test_species",
        "settlement": "test_settlement",
        "location": "test_location",
        "role": "test_role",
        "relationships": [{"npc_id": "test_other", "relation": "knows"}],
        "knowledge_allowed": ["test_allowed_fact"],
        "knowledge_forbidden": ["test_forbidden_fact"],
        "beliefs_uncertain": ["test_uncertain_belief"],
        "initial_talk": ["test_initial_topic"],
        "conditional_knowledge": [
            {"requires": ["test_flag"], "knowledge": ["test_conditional_fact"]}
        ],
        "narrative_function": "test_narrative_function",
        "gameplay_function": "test_gameplay_function",
        "capabilities": ["test_capability"],
        "limits": ["test_limit"],
        "memory_hooks": ["test_memory_hook"],
        "status": "synthetic-test-only",
    }


class FakeClient:
    def __init__(self):
        self.calls = 0


class FakeBridge:
    def __init__(self):
        self.calls = 0

    def __call__(self, npc, client):
        if npc.get("personality_locked") is True:
            return deepcopy(npc)
        self.calls += 1
        client.calls += 1
        result = deepcopy(npc)
        result["personality"] = deepcopy(PERSONALITY)
        result["personality_provenance"] = {
            "ollama_model": "fake-model",
            "personality_prompt_version": "test-v1",
            "personality_generated_at": "2026-09-22T00:00:00+00:00",
        }
        result["personality_locked"] = True
        return result


class NpcGeneratorAdapterTests(unittest.TestCase):
    def test_normalizes_authoritative_contract(self):
        npc = adapter.normalize_authoritative_npc(synthetic_npc())
        self.assertEqual(npc["id"], "test_npc_001")
        self.assertEqual(npc["knowledge_forbidden"], ["test_forbidden_fact"])

    def test_rejects_missing_authoritative_field(self):
        npc = synthetic_npc()
        del npc["knowledge_allowed"]
        with self.assertRaises(adapter.NpcGeneratorContractError):
            adapter.normalize_authoritative_npc(npc)

    def test_rejects_missing_capabilities(self):
        npc = synthetic_npc()
        del npc["capabilities"]
        with self.assertRaises(adapter.NpcGeneratorContractError):
            adapter.normalize_authoritative_npc(npc)

    def test_rejects_missing_limits(self):
        npc = synthetic_npc()
        del npc["limits"]
        with self.assertRaises(adapter.NpcGeneratorContractError):
            adapter.normalize_authoritative_npc(npc)

    def test_rejects_generator_personality_fields(self):
        npc = synthetic_npc()
        npc["personality"] = {}
        with self.assertRaises(adapter.NpcGeneratorContractError):
            adapter.normalize_authoritative_npc(npc)

    def test_end_to_end_generator_to_locked_personality(self):
        client = FakeClient()
        bridge = FakeBridge()
        original = synthetic_npc()
        enriched = adapter.enrich_generated_npc(
            original, client, enrich_fn=bridge
        )
        self.assertTrue(enriched["personality_locked"])
        self.assertEqual(enriched["personality"], PERSONALITY)
        self.assertEqual(client.calls, 1)
        self.assertNotIn("personality", original)

    def test_second_pass_does_not_generate_again(self):
        client = FakeClient()
        bridge = FakeBridge()
        first = adapter.enrich_generated_npc(
            synthetic_npc(), client, enrich_fn=bridge
        )
        first_calls = client.calls
        second = adapter.enrich_generated_npc(
            first, client, enrich_fn=bridge
        )
        self.assertEqual(second, first)
        self.assertEqual(client.calls, first_calls)

    def test_authoritative_fields_do_not_change(self):
        client = FakeClient()
        bridge = FakeBridge()
        original = synthetic_npc()
        enriched = adapter.enrich_generated_npc(
            original, client, enrich_fn=bridge
        )
        for key, value in original.items():
            self.assertEqual(enriched[key], value)

    def test_detects_bridge_mutating_authoritative_field(self):
        def bad_bridge(npc, client):
            result = FakeBridge()(npc, client)
            result["role"] = "changed_role"
            return result

        with self.assertRaises(adapter.NpcGeneratorContractError):
            adapter.enrich_generated_npc(
                synthetic_npc(), FakeClient(), enrich_fn=bad_bridge
            )

    def test_batch_enrichment(self):
        client = FakeClient()
        bridge = FakeBridge()
        result = adapter.enrich_generated_batch(
            [synthetic_npc("test_npc_001"), synthetic_npc("test_npc_002")],
            client,
            enrich_fn=bridge,
        )
        self.assertEqual(len(result), 2)
        self.assertTrue(all(item["personality_locked"] for item in result))
        self.assertEqual(client.calls, 2)

    def test_batch_rejects_duplicate_ids(self):
        with self.assertRaises(adapter.NpcGeneratorContractError):
            adapter.enrich_generated_batch(
                [synthetic_npc(), synthetic_npc()],
                FakeClient(),
                enrich_fn=FakeBridge(),
            )


if __name__ == "__main__":
    unittest.main()
