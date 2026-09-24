from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "validate-vintage-content.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_vintage_content",
    SCRIPT,
)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validator)


class ContentFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.files: dict[str, object] = {}

    def add(self, rel: str, data: object) -> None:
        self.files[rel] = data

    def write(
        self,
        *,
        manifest_files: list[str] | None = None,
        content_version: str = "0.0.1",
    ) -> None:
        for rel, data in self.files.items():
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(data, indent=2),
                encoding="utf-8",
            )

        manifest = {
            "schema_version": 1,
            "content_version": content_version,
            "files": sorted(
                manifest_files
                if manifest_files is not None
                else self.files
            ),
        }
        (self.root / "manifest.json").write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8",
        )


def valid_fixture(root: Path) -> ContentFixture:
    fixture = ContentFixture(root)

    fixture.add(
        "settlements/test-settlement.json",
        {
            "id": "test_settlement",
            "name": "Synthetic Settlement",
            "starting_room": "test_room_a",
            "rooms": [
                {
                    "id": "test_room_a",
                    "settlement": "test_settlement",
                    "name": "Synthetic Room A",
                    "description": "Synthetic room A description.",
                    "exits": {"north": "test_room_b"},
                    "tags": ["synthetic-test"],
                },
                {
                    "id": "test_room_b",
                    "settlement": "test_settlement",
                    "name": "Synthetic Room B",
                    "description": "Synthetic room B description.",
                    "exits": {"south": "test_room_a"},
                    "tags": ["synthetic-test"],
                },
            ],
        },
    )

    fixture.add(
        "species.json",
        {
            "species": [
                {
                    "id": "test_species",
                    "name": "Synthetic Species",
                    "starting_settlement": "test_settlement",
                    "starting_room": "test_room_a",
                }
            ]
        },
    )

    fixture.add(
        "narrative/test-arrival.json",
        {
            "narrative": [
                {
                    "id": "test_narrative_arrival",
                    "room": "test_room_a",
                    "trigger": "first_entry",
                    "once_per_player": True,
                    "text": (
                        "Synthetic narrative text "
                        "for validator tests only."
                    ),
                    "requires": [],
                    "sets": ["seen.test_narrative_arrival"],
                }
            ]
        },
    )

    return fixture


class ValidateVintageContentTests(unittest.TestCase):
    def run_fixture(self, mutate=None) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = valid_fixture(root)
            if mutate:
                mutate(fixture)
            fixture.write()
            return validator.validate_content(root)

    def test_valid_synthetic_content(self):
        self.assertEqual(self.run_fixture(), [])

    def test_invalid_json_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "manifest.json").write_text(
                '{"schema_version": 1,',
                encoding="utf-8",
            )
            errors = validator.validate_content(root)
            self.assertTrue(
                any("invalid JSON" in error for error in errors)
            )

    def test_duplicate_ids_are_reported(self):
        def mutate(fixture: ContentFixture):
            settlement = fixture.files[
                "settlements/test-settlement.json"
            ]
            settlement["rooms"][1]["id"] = "test_room_a"

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                "duplicate id 'test_room_a'" in error
                for error in errors
            )
        )

    def test_exit_to_missing_room_is_reported(self):
        def mutate(fixture: ContentFixture):
            settlement = fixture.files[
                "settlements/test-settlement.json"
            ]
            settlement["rooms"][0]["exits"]["north"] = (
                "test_missing_room"
            )

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                "points to missing room 'test_missing_room'" in error
                for error in errors
            )
        )

    def test_unsupported_exit_direction_is_reported(self):
        def mutate(fixture: ContentFixture):
            settlement = fixture.files[
                "settlements/test-settlement.json"
            ]
            settlement["rooms"][0]["exits"]["up"] = "test_room_b"

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                "exit direction 'up' is not allowed" in error
                for error in errors
            )
        )

    def test_narrative_missing_room_is_reported(self):
        def mutate(fixture: ContentFixture):
            fixture.files[
                "narrative/test-arrival.json"
            ]["narrative"][0]["room"] = "test_missing_room"

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                "room 'test_missing_room' does not exist" in error
                for error in errors
            )
        )

    def test_species_missing_settlement_is_reported(self):
        def mutate(fixture: ContentFixture):
            fixture.files["species.json"]["species"][0][
                "starting_settlement"
            ] = "test_missing_settlement"

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                (
                    "starting_settlement "
                    "'test_missing_settlement' does not exist"
                )
                in error
                for error in errors
            )
        )

    def test_species_missing_starting_room_is_reported(self):
        def mutate(fixture: ContentFixture):
            fixture.files["species.json"]["species"][0][
                "starting_room"
            ] = "test_missing_room"

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                "starting_room 'test_missing_room' does not exist"
                in error
                for error in errors
            )
        )

    def test_missing_description_is_reported(self):
        def mutate(fixture: ContentFixture):
            del fixture.files[
                "settlements/test-settlement.json"
            ]["rooms"][0]["description"]

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                (
                    "required field 'description' "
                    "must be a non-empty string"
                )
                in error
                for error in errors
            )
        )

    def test_empty_description_is_reported(self):
        def mutate(fixture: ContentFixture):
            fixture.files[
                "settlements/test-settlement.json"
            ]["rooms"][0]["description"] = "   "

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                (
                    "required field 'description' "
                    "must be a non-empty string"
                )
                in error
                for error in errors
            )
        )

    def test_empty_required_field_is_reported(self):
        def mutate(fixture: ContentFixture):
            fixture.files[
                "settlements/test-settlement.json"
            ]["rooms"][0]["name"] = "   "

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                (
                    "required field 'name' "
                    "must be a non-empty string"
                )
                in error
                for error in errors
            )
        )

    def test_manifest_unlisted_json_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = valid_fixture(root)
            fixture.write(
                manifest_files=[
                    "species.json",
                    "settlements/test-settlement.json",
                ]
            )
            errors = validator.validate_content(root)
            self.assertTrue(
                any(
                    "not listed in manifest" in error
                    for error in errors
                )
            )

    def test_manifest_invalid_version_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = valid_fixture(root)
            fixture.write(content_version="version-one")
            errors = validator.validate_content(root)
            self.assertTrue(
                any("MAJOR.MINOR.PATCH" in error for error in errors)
            )

    def test_public_private_reference_is_reported(self):
        def mutate(fixture: ContentFixture):
            fixture.files[
                "narrative/test-arrival.json"
            ]["narrative"][0]["requires"] = [
                "private-content/secret.json"
            ]

        errors = self.run_fixture(mutate)
        self.assertTrue(
            any(
                "must not reference private-content" in error
                for error in errors
            )
        )

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = valid_fixture(root)
            fixture.write()

            ok = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--content-dir",
                    str(root),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(ok.returncode, 0, ok.stderr)

            fixture.files[
                "settlements/test-settlement.json"
            ]["rooms"][0]["exits"]["north"] = "test_missing_room"
            fixture.write()

            bad = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--content-dir",
                    str(root),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("test_missing_room", bad.stderr)


if __name__ == "__main__":
    unittest.main()
