from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.vt_art.github_runner import copy_request_to_version, resolve_request_path


class GitHubRunnerTests(unittest.TestCase):
    def test_request_path_must_be_existing_json_in_request_directory(self):
        path = resolve_request_path("vintage-telnet/art_requests/velozanco-edran-fase2.json")
        self.assertTrue(path.is_file())
        with self.assertRaisesRegex(ValueError, "ficha JSON"):
            resolve_request_path("../../AGENTS.md")
        with self.assertRaisesRegex(ValueError, "ficha JSON"):
            resolve_request_path("vintage-telnet/art_requests/template.json")

    def test_copy_request_keeps_exact_brief_next_to_draft(self):
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "approved-request.json"
            source.write_text('{"asset_id":"velozanco_edran"}\n', encoding="utf-8")
            version = temp / "v001"
            version.mkdir()
            output = copy_request_to_version(source, version)
            self.assertEqual(output.read_text(encoding="utf-8"), source.read_text(encoding="utf-8"))

    def test_copy_request_never_overwrites_a_version_brief(self):
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "approved-request.json"
            source.write_text("new brief", encoding="utf-8")
            version = temp / "v001"
            version.mkdir()
            destination = version / "request.json"
            destination.write_text("old brief", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "ya existe"):
                copy_request_to_version(source, version)
            self.assertEqual(destination.read_text(encoding="utf-8"), "old brief")


if __name__ == "__main__":
    unittest.main()
