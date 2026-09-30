from __future__ import annotations

import json
import base64
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.vt_art.cli import _run_batch, _run_variants, _sum_usage, load_local_config, main
from tools.vt_art.pipeline import ArtPipeline, ArtPipelineError, ArtRequest, OpenAIImageClient, size_for_aspect


class FakeClient:
    def __init__(self, fail_on: int | None = None):
        self.calls = 0
        self.fail_on = fail_on

    def generate(self, *, prompt, model, request):
        self.calls += 1
        if self.calls == self.fail_on:
            raise TimeoutError("secret text must never be logged")
        return b"fake image bytes", {"input_tokens": 4, "output_tokens": 7}, f"req-{self.calls}"


class ArtPipelineTests(unittest.TestCase):
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
            "asset_id": "valden_architecture",
            "asset_type": "environment",
            "target": "approved art brief",
            "canonical_name": "Valdren",
            "art_direction": "Warm pixel art, readable silhouette.",
            "prompt": "Create a draft from the approved description.",
            "references": [],
            "negative_constraints": ["No text"],
            "aspect_ratio": "landscape",
            "output_destination": "vintage-telnet/art_generations",
            "status": "draft",
        }
        raw.update(overrides)
        path = self.requests / "valden.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        return ArtRequest.load(path, self.root, self.generations)

    def test_request_fields_prompt_and_default_output_are_loaded(self):
        request = self.make_request()
        self.assertEqual(request.asset_id, "valden_architecture")
        self.assertEqual(request.output_destination, self.generations)
        from tools.vt_art.pipeline import build_prompt
        prompt = build_prompt(request)
        self.assertIn("Canonical name: Valdren", prompt)
        self.assertIn("Do not include: No text", prompt)

    def test_runtime_assets_destination_is_rejected(self):
        with self.assertRaisesRegex(ArtPipelineError, "art_generations"):
            self.make_request(output_destination="assets/vintage-telnet/rooms")

    def test_invalid_asset_id_is_rejected(self):
        with self.assertRaisesRegex(ArtPipelineError, "asset_id"):
            self.make_request(asset_id="../valdren")

    def test_new_generation_versions_without_overwriting_and_persists_metadata(self):
        request = self.make_request()
        pipeline = ArtPipeline(FakeClient(), "gpt-image-2.5-flare")
        first = pipeline.generate(request)
        second = pipeline.generate(request)
        self.assertEqual((first["version"], second["version"]), ("v001", "v002"))
        self.assertNotEqual(first["generation_id"], second["generation_id"])
        self.assertEqual((request.output_destination / "valden_architecture" / "v001" / "valden_architecture_v001.png").read_bytes(), b"fake image bytes")
        self.assertEqual(first["status"], "draft")
        self.assertEqual(first["request_id"], "req-1")

    def test_cost_estimate_uses_official_token_rates(self):
        class PricedClient:
            def generate(self, *, prompt, model, request):
                usage = {
                    "input_tokens_details": {"text_tokens": 1_000_000, "image_tokens": 0},
                    "output_tokens_details": {"image_tokens": 1_000_000, "text_tokens": 0},
                }
                return b"fake image bytes", usage, "req-priced"
        request = self.make_request()
        pipeline = ArtPipeline(PricedClient(), "gpt-image-2.5-flare")
        result = pipeline.generate(request)
        self.assertAlmostEqual(result["cost_estimate"], 5.00 + 30.00)

    def test_cost_estimate_is_none_for_unrecognized_model(self):
        request = self.make_request()
        pipeline = ArtPipeline(FakeClient(), "some-future-model")
        result = pipeline.generate(request)
        self.assertIsNone(result["cost_estimate"])

    def test_generate_with_critique_stops_at_first_pass(self):
        class FakeCritic:
            def __init__(self):
                self.calls = []

            def critique(self, *, image_bytes, image_format, brief, model):
                self.calls.append(brief)
                return {"passes": True, "issues": [], "reasoning": "ok"}, {"input_tokens": 10, "output_tokens": 5}

        request = self.make_request()
        pipeline = ArtPipeline(FakeClient(), "gpt-image-2.5-flare")
        critic = FakeCritic()
        result = pipeline.generate_with_critique(request, critic, "gpt-5-mini", max_attempts=2)
        self.assertEqual(len(critic.calls), 1)
        self.assertEqual(len(result["attempts"]), 1)
        self.assertTrue(result["critique"]["passes"])
        self.assertEqual(result["version"], "v001")
        saved = json.loads((request.output_destination / "valden_architecture" / "v001" / "metadata.json").read_text())
        self.assertTrue(saved["critique"]["passes"])

    def test_generate_with_critique_retries_once_then_stops(self):
        class FailThenPassCritic:
            def __init__(self):
                self.calls = 0

            def critique(self, *, image_bytes, image_format, brief, model):
                self.calls += 1
                if self.calls == 1:
                    return {"passes": False, "issues": ["Has wings"], "reasoning": "bad"}, {"input_tokens": 1, "output_tokens": 1}
                return {"passes": True, "issues": [], "reasoning": "fixed"}, {"input_tokens": 1, "output_tokens": 1}

        request = self.make_request()
        pipeline = ArtPipeline(FakeClient(), "gpt-image-2.5-flare")
        critic = FailThenPassCritic()
        result = pipeline.generate_with_critique(request, critic, "gpt-5-mini", max_attempts=2)
        self.assertEqual(critic.calls, 2)
        self.assertEqual([a["version"] for a in result["attempts"]], ["v001", "v002"])
        self.assertTrue(result["critique"]["passes"])
        first_metadata = json.loads((request.output_destination / "valden_architecture" / "v001" / "metadata.json").read_text())
        self.assertFalse(first_metadata["critique"]["passes"])

    def test_generate_with_critique_gives_up_after_max_attempts(self):
        class AlwaysFailsCritic:
            def __init__(self):
                self.calls = 0

            def critique(self, *, image_bytes, image_format, brief, model):
                self.calls += 1
                return {"passes": False, "issues": ["Still wrong"], "reasoning": "bad"}, {}

        request = self.make_request()
        pipeline = ArtPipeline(FakeClient(), "gpt-image-2.5-flare")
        critic = AlwaysFailsCritic()
        result = pipeline.generate_with_critique(request, critic, "gpt-5-mini", max_attempts=2)
        self.assertEqual(critic.calls, 2)
        self.assertFalse(result["critique"]["passes"])
        self.assertEqual(len(result["attempts"]), 2)

    def test_explicit_version_hint_is_unique_and_never_overwrites(self):
        request = self.make_request()
        client = FakeClient()
        pipeline = ArtPipeline(client, "gpt-image-2.5-flare")
        result = pipeline.generate(request, "v023")
        self.assertEqual(result["version"], "v023")
        with self.assertRaisesRegex(ArtPipelineError, "ya existe"):
            pipeline.generate(request, "v023")
        with self.assertRaisesRegex(ArtPipelineError, "formato"):
            pipeline.generate(request, "latest")
        self.assertEqual(client.calls, 1)

    def test_status_updates_only_latest_unless_version_is_selected(self):
        request = self.make_request()
        pipeline = ArtPipeline(FakeClient(), "gpt-image-2.5-flare")
        pipeline.generate(request)
        pipeline.generate(request)
        rows = pipeline.status(self.generations, request.asset_id, "review")
        self.assertEqual((len(rows), rows[0]["version"], rows[0]["status"]), (1, "v002", "review"))
        all_rows = pipeline.status(self.generations, request.asset_id)
        self.assertEqual([row["status"] for row in all_rows], ["draft", "review"])

    def test_rejected_is_a_recordable_review_status(self):
        request = self.make_request()
        pipeline = ArtPipeline(FakeClient(), "gpt-image-2.5-flare")
        generated = pipeline.generate(request)
        rows = pipeline.status(self.generations, request.asset_id, "rejected", generated["version"])
        self.assertEqual((len(rows), rows[0]["status"]), (1, "rejected"))

    def test_partial_variants_are_preserved_and_failure_summary_has_no_exception_text(self):
        request = self.make_request()
        client = FakeClient(fail_on=2)
        summary = _run_variants(ArtPipeline(client, "gpt-image-2.5-flare"), request, 3)
        self.assertEqual(summary["request_count"], 2)
        self.assertEqual(summary["generation_count"], 1)
        self.assertEqual(summary["completed"][0]["version"], "v001")
        self.assertNotIn("secret text", json.dumps(summary))
        files = list(self.generations.glob("batch-*.json"))
        self.assertEqual(len(files), 1)

    def test_usage_totals_accumulate_numeric_fields(self):
        total = _sum_usage([
            {"input_tokens": 3, "image_tokens": {"output": 10}},
            {"input_tokens": 5, "image_tokens": {"output": 7}},
        ])
        self.assertEqual(total, {"input_tokens": 8, "image_tokens": {"output": 17}})

    def test_batch_keeps_completed_generations_when_a_later_request_fails(self):
        batch_dir = self.requests / "batch"
        batch_dir.mkdir()
        for name, asset_id in (("first", "first_art"), ("second", "second_art"), ("third", "third_art")):
            data = {
                "asset_id": asset_id,
                "asset_type": "environment",
                "target": "test",
                "canonical_name": asset_id,
                "art_direction": "test direction",
                "prompt": "test prompt",
                "aspect_ratio": "square",
                "output_destination": str(self.generations),
            }
            (batch_dir / f"{name}.json").write_text(json.dumps(data), encoding="utf-8")
        summary = _run_batch(ArtPipeline(FakeClient(fail_on=2), "model"), batch_dir, self.generations)
        self.assertEqual(summary["generation_count"], 1)
        self.assertEqual(summary["request_count"], 2)
        self.assertTrue((self.generations / "first_art" / "v001" / "metadata.json").is_file())
        self.assertEqual(len(summary["failures"]), 2)
        self.assertEqual(summary["failures"][1]["status"], "not_attempted_after_error")

    def test_aspect_sizes_map_to_supported_dimensions(self):
        self.assertEqual(size_for_aspect("square"), "1024x1024")
        self.assertEqual(size_for_aspect("landscape"), "1536x1024")
        self.assertEqual(size_for_aspect("16:9"), "1536x864")

    def test_dotenv_loader_does_not_override_environment(self):
        with tempfile.TemporaryDirectory() as folder:
            env_file = Path(folder) / ".env"
            env_file.write_text("OPENAI_API_KEY=should-not-win\nVT_ART_MODEL=gpt-image-2.5-sunburst\n", encoding="utf-8")
            with patch("tools.vt_art.cli.ENV_FILE", env_file), patch.dict("os.environ", {"OPENAI_API_KEY": "external", "VT_ART_MODEL": "custom-model"}):
                load_local_config()
                import os
                self.assertEqual(os.environ["OPENAI_API_KEY"], "external")
                self.assertEqual(os.environ["VT_ART_MODEL"], "custom-model")

    def test_dotenv_loader_reads_key_without_displaying_it(self):
        with tempfile.TemporaryDirectory() as folder:
            env_file = Path(folder) / ".env"
            env_file.write_text("OPENAI_API_KEY='local-secret-value'\n", encoding="utf-8")
            with patch("tools.vt_art.cli.ENV_FILE", env_file), patch.dict("os.environ", {}, clear=True):
                load_local_config()
                import os
                self.assertEqual(os.environ["OPENAI_API_KEY"], "local-secret-value")

    def test_preferred_user_named_env_file_is_read(self):
        with tempfile.TemporaryDirectory() as folder:
            env_file = Path(folder) / "Imagenesapykey.env"
            env_file.write_text("OPENAI_API_KEY=local-secret-value\n", encoding="utf-8")
            with patch("tools.vt_art.cli.ENV_FILE", env_file), patch("tools.vt_art.cli.LEGACY_ENV_FILE", Path(folder) / ".env"), patch.dict("os.environ", {}, clear=True):
                load_local_config()
                import os
                self.assertEqual(os.environ["OPENAI_API_KEY"], "local-secret-value")

    def test_openai_wrapper_sends_parameters_and_decodes_image_response(self):
        calls = []

        class FakeImages:
            def generate(self, **params):
                calls.append(params)
                return SimpleNamespace(
                    data=[SimpleNamespace(b64_json=base64.b64encode(b"image-bytes").decode())],
                    usage={"output_tokens": 9},
                    _request_id="request-123",
                )

        class FakeOpenAI:
            def __init__(self, **kwargs):
                self.kwargs = kwargs
                self.images = FakeImages()

        fake_module = SimpleNamespace(OpenAI=FakeOpenAI)
        with patch.dict(sys.modules, {"openai": fake_module}):
            client = OpenAIImageClient("test-api-key")
            image, usage, request_id = client.generate(
                prompt="test prompt", model="gpt-image-2.5-flare", request=self.make_request()
            )
        self.assertEqual(image, b"image-bytes")
        self.assertEqual(usage, {"output_tokens": 9})
        self.assertEqual(request_id, "request-123")
        self.assertEqual(calls[0]["model"], "gpt-image-2.5-flare")
        self.assertEqual(calls[0]["size"], "1536x1024")
        self.assertEqual(calls[0]["quality"], "low")

    @unittest.skipUnless(importlib.util.find_spec("openai"), "OpenAI SDK se instala en el entorno de la herramienta")
    def test_official_sdk_serializes_image_request_without_network(self):
        import httpx
        from openai import OpenAI

        seen = {}

        def respond(request):
            seen["url"] = str(request.url)
            seen["authorization"] = request.headers.get("authorization")
            seen["body"] = json.loads(request.content)
            return httpx.Response(
                200,
                headers={"x-request-id": "sdk-request-1"},
                json={"data": [{"b64_json": base64.b64encode(b"sdk-image").decode()}], "usage": {"output_tokens": 3}},
            )

        http = httpx.Client(transport=httpx.MockTransport(respond))
        sdk = OpenAI(api_key="test-key-never-log", http_client=http, max_retries=0)
        try:
            client = OpenAIImageClient("unused", sdk_client=sdk)
            image, usage, request_id = client.generate(
                prompt="approved visual brief", model="gpt-image-2.5-flare", request=self.make_request()
            )
        finally:
            sdk.close()
        self.assertTrue(seen["url"].endswith("/images/generations"))
        self.assertEqual(seen["authorization"], "Bearer test-key-never-log")
        self.assertEqual(seen["body"]["model"], "gpt-image-2.5-flare")
        self.assertEqual(seen["body"]["size"], "1536x1024")
        self.assertEqual(image, b"sdk-image")
        self.assertEqual(request_id, "sdk-request-1")
        self.assertEqual(usage["output_tokens"], 3)

    def test_missing_api_key_fails_without_calling_api_or_echoing_key(self):
        with patch.dict("os.environ", {}, clear=True), patch("tools.vt_art.cli.ENV_FILE", self.root / "missing.env"):
            self.assertEqual(main(["generate", str(self.requests / "valden.json")]), 2)


class CostsCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.generations = Path(self.temp.name) / "art_generations"

    def tearDown(self):
        self.temp.cleanup()

    def write_metadata(self, asset_id, version, model_id, usage, cost_estimate, status="draft"):
        version_dir = self.generations / asset_id / version
        version_dir.mkdir(parents=True)
        (version_dir / "metadata.json").write_text(json.dumps({
            "asset_id": asset_id, "version": version, "model_id": model_id,
            "status": status, "usage": usage, "cost_estimate": cost_estimate,
        }), encoding="utf-8")

    def test_sums_precomputed_and_recomputes_missing_cost_estimates(self):
        from tools.vt_art.cli import _collect_costs
        self.write_metadata("velozanco_edran", "v001", "gpt-image-2.5-flare", {
            "input_tokens_details": {"text_tokens": 398, "image_tokens": 1536},
            "output_tokens_details": {"image_tokens": 158, "text_tokens": 0},
        }, cost_estimate=None)  # como quedaron las dos piezas reales ya generadas
        self.write_metadata("agujaumbria_nhal", "v002", "gpt-image-2.5-flare", {}, cost_estimate=0.0199)
        report = _collect_costs(self.generations)
        self.assertEqual(len(report["rows"]), 2)
        self.assertGreater(report["total_usd"], 0)
        self.assertEqual(report["unknown_model"], [])

    def test_unknown_model_is_reported_not_silently_dropped(self):
        from tools.vt_art.cli import _collect_costs
        self.write_metadata("mystery", "v001", "some-future-model", {"input_tokens": 10}, cost_estimate=None)
        report = _collect_costs(self.generations)
        self.assertEqual(report["total_usd"], 0)
        self.assertEqual(len(report["unknown_model"]), 1)

    def test_empty_generations_directory_reports_nothing(self):
        from tools.vt_art.cli import _collect_costs
        self.generations.mkdir()
        report = _collect_costs(self.generations)
        self.assertEqual(report["rows"], [])
        self.assertEqual(report["total_usd"], 0)


if __name__ == "__main__":
    unittest.main()
