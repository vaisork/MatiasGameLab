from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.vt_art.github_runner import download_reference, upload_file


class FakeResponse:
    def __init__(self, status_code: int, content: bytes = b"", payload: dict | None = None):
        self.status_code = status_code
        self.content = content
        self._payload = payload or {}

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, get_response: FakeResponse | None = None, post_response: FakeResponse | None = None):
        self.get_response = get_response
        self.post_response = post_response
        self.post_args = None

    def get(self, *args, **kwargs):
        return self.get_response

    def post(self, *args, **kwargs):
        self.post_args = (args, kwargs)
        return self.post_response


class GitHubRunnerTests(unittest.TestCase):
    def test_download_reference_accepts_png_and_writes_it(self):
        image = b"\x89PNG\r\n\x1a\nreference"
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "reference.png"
            download_reference(FakeSession(get_response=FakeResponse(200, image)), path)
            self.assertEqual(path.read_bytes(), image)

    def test_download_reference_rejects_non_png(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "reference.png"
            with self.assertRaisesRegex(RuntimeError, "no es un PNG"):
                download_reference(FakeSession(get_response=FakeResponse(200, b"not png")), path)
            self.assertFalse(path.exists())

    def test_upload_sends_file_to_requested_drive_folder_without_overwrite(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "velozanco_v001.png"
            path.write_bytes(b"image bytes")
            session = FakeSession(post_response=FakeResponse(200, payload={"id": "drive-id", "name": path.name}))
            self.assertEqual(upload_file(session, path, "folder-id"), "drive-id")
            args, kwargs = session.post_args
            self.assertIn("uploadType", kwargs["params"])
            self.assertIn('"parents": ["folder-id"]', kwargs["data"].decode())
            self.assertIn(b"image bytes", kwargs["data"])

    def test_upload_fails_closed_on_drive_error(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "draft.png"
            path.write_bytes(b"image bytes")
            session = FakeSession(post_response=FakeResponse(403))
            with self.assertRaisesRegex(RuntimeError, "HTTP 403"):
                upload_file(session, path, "folder-id")


if __name__ == "__main__":
    unittest.main()
