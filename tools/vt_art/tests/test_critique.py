from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.vt_art.critique import (
    build_critique_brief,
    critique_generation,
    estimate_critique_cost_usd,
)
from tools.vt_art.pipeline import ArtPipelineError, ArtRequest


class FakeCritic:
    def __init__(self, verdicts):
        self.verdicts = list(verdicts)
        self.calls = []

    def critique(self, *, image_bytes, image_format, brief, model):
        self.calls.append({"image_bytes": image_bytes, "image_format": image_format, "brief": brief, "model": model})
        verdict = self.verdicts.pop(0)
        return verdict, {"input_tokens": 500, "output_tokens": 40}


class CritiqueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.generations = self.root / "vintage-telnet" / "art_generations"
        self.requests = self.root / "requests"
        self.requests.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def make_request(self, **overrides):
        raw = {
            "asset_id": "cascapedernal",
            "asset_type": "creature",
            "target": "approved brief",
            "canonical_name": "Cascapedernal",
            "art_direction": "Low rounded body, no wings.",
            "prompt": "Create one landscape wildlife scene.",
            "references": [],
            "negative_constraints": ["No wings", "No glowing eyes"],
            "aspect_ratio": "landscape",
            "output_destination": "vintage-telnet/art_generations",
            "status": "draft",
        }
        raw.update(overrides)
        path = self.requests / "cascapedernal.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        return ArtRequest.load(path, self.root, self.generations)

    def test_brief_includes_art_direction_and_negative_constraints(self):
        request = self.make_request()
        brief = build_critique_brief(request)
        self.assertIn("Cascapedernal", brief)
        self.assertIn("Low rounded body", brief)
        self.assertIn("No wings", brief)
        self.assertIn("No glowing eyes", brief)

    def test_passing_verdict_is_parsed_with_cost(self):
        request = self.make_request()
        critic = FakeCritic([{"passes": True, "issues": [], "reasoning": "Matches the brief."}])
        result = critique_generation(critic, "gpt-5-mini", request, b"fake png bytes", "png")
        self.assertTrue(result.passes)
        self.assertEqual(result.issues, ())
        self.assertEqual(result.reasoning, "Matches the brief.")
        self.assertIsNotNone(result.cost_estimate)
        self.assertGreater(result.cost_estimate, 0)

    def test_failing_verdict_carries_issues(self):
        request = self.make_request()
        critic = FakeCritic([{"passes": False, "issues": ["Has wings"], "reasoning": "Violates constraint."}])
        result = critique_generation(critic, "gpt-5-mini", request, b"fake png bytes", "png")
        self.assertFalse(result.passes)
        self.assertEqual(result.issues, ("Has wings",))

    def test_missing_passes_field_is_rejected(self):
        request = self.make_request()
        critic = FakeCritic([{"issues": [], "reasoning": "no verdict"}])
        with self.assertRaisesRegex(ArtPipelineError, "veredicto"):
            critique_generation(critic, "gpt-5-mini", request, b"fake png bytes", "png")

    def test_cost_is_none_for_unknown_model(self):
        self.assertIsNone(estimate_critique_cost_usd("unknown-model", {"input_tokens": 10, "output_tokens": 10}))

    def test_cost_is_none_without_usage(self):
        self.assertIsNone(estimate_critique_cost_usd("gpt-5-mini", None))

    def test_cost_matches_official_rate(self):
        cost = estimate_critique_cost_usd("gpt-5-mini", {"input_tokens": 1_000_000, "output_tokens": 1_000_000})
        self.assertAlmostEqual(cost, 0.25 + 2.00)


if __name__ == "__main__":
    unittest.main()
