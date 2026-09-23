from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import sys


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "publish-assets.py"
spec = importlib.util.spec_from_file_location("publish_assets", MODULE_PATH)
pub = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = pub
spec.loader.exec_module(pub)


def png_bytes(width=2, height=3):
    # The validator only needs a valid PNG signature + IHDR dimensions.
    return (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\x0dIHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x06\x00\x00\x00"
        + b"\x00\x00\x00\x00"
    )


def webp_vp8x_bytes(width=4, height=5):
    w = (width - 1).to_bytes(3, "little")
    h = (height - 1).to_bytes(3, "little")
    payload = b"\x00\x00\x00\x00" + b"\x00\x00\x00" + w + h
    size = (4 + 8 + len(payload)).to_bytes(4, "little")
    return b"RIFF" + size + b"WEBP" + b"VP8X" + len(payload).to_bytes(4, "little") + payload


class AssetPublisherTests(unittest.TestCase):
    def git(self, repo, *args):
        return subprocess.run(
            ["git", *args], cwd=repo, check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.strip()

    def make_repo(self):
        td = tempfile.TemporaryDirectory()
        repo = Path(td.name)
        self.git(repo, "init", "-b", "main")
        self.git(repo, "config", "user.email", "test@example.invalid")
        self.git(repo, "config", "user.name", "Asset Test")
        (repo / "README.md").write_text("test\n", encoding="utf-8")
        self.git(repo, "add", "README.md")
        self.git(repo, "commit", "-m", "initial")
        self.git(repo, "switch", "-c", "assets/test-batch")
        return td, repo

    def test_valid_asset_passes_and_has_dimensions(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "valid.png"
            source.write_bytes(png_bytes(24, 24))
            fmt, width, height, size, digest = pub.inspect_image(source)
            self.assertEqual((fmt, width, height), ("PNG", 24, 24))
            self.assertGreater(size, 0)
            self.assertEqual(len(digest), 64)

    def test_webp_required_for_vaisgard_pilot_is_supported(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "vaisgard.webp"
            source.write_bytes(webp_vp8x_bytes(320, 180))
            fmt, width, height, _size, _digest = pub.inspect_image(source)
            self.assertEqual((fmt, width, height), ("WEBP", 320, 180))

    def test_invalid_file_fails(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "bad.png"
            source.write_bytes(b"not an image")
            with self.assertRaises(pub.AssetBatchError):
                pub.inspect_image(source)

    def test_outside_allowlist_fails(self):
        with self.assertRaises(pub.AssetBatchError):
            pub.normalize_target("vintage-telnet/server/")
        with self.assertRaises(pub.AssetBatchError):
            pub.normalize_target("../assets/vintage-telnet/locations/")
        with self.assertRaises(pub.AssetBatchError):
            pub.normalize_target("/tmp/assets/")

    def test_duplicate_names_in_manifest_fail_before_publish(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "one.png").write_bytes(png_bytes())
            (base / "two.png").write_bytes(png_bytes())
            manifest = base / "batch.json"
            manifest.write_text(json.dumps({
                "target": "assets/vintage-telnet/locations/",
                "files": [
                    {"source": "one.png", "name": "same.png"},
                    {"source": "two.png", "name": "same.png"},
                ],
            }), encoding="utf-8")
            target, replace, entries = pub.load_batch(manifest, None)
            fake_repo = base / "repo"
            fake_repo.mkdir()
            with self.assertRaises(pub.AssetBatchError):
                pub.validate_batch(fake_repo, target, entries, replace=replace)

    def test_existing_destination_rejected_without_replace(self):
        td, repo = self.make_repo()
        self.addCleanup(td.cleanup)
        dest = repo / "assets/vintage-telnet/locations/exists.png"
        dest.parent.mkdir(parents=True)
        dest.write_bytes(png_bytes())
        source = repo / "source.png"
        source.write_bytes(png_bytes())
        with self.assertRaises(pub.AssetBatchError):
            pub.validate_batch(
                repo,
                "assets/vintage-telnet/locations/",
                [(source, "exists.png")],
                replace=False,
            )

    def test_dry_run_does_not_modify_repo(self):
        td, repo = self.make_repo()
        self.addCleanup(td.cleanup)
        incoming = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(incoming, ignore_errors=True))
        (incoming / "new.png").write_bytes(png_bytes())
        target, replace, entries = pub.load_batch(
            incoming, "assets/vintage-telnet/locations/"
        )
        assets = pub.validate_batch(repo, target, entries, replace=replace)
        before = self.git(repo, "status", "--porcelain")
        pub.print_summary(assets, target, dry_run=True, commit=None)
        after = self.git(repo, "status", "--porcelain")
        self.assertEqual(before, after)
        self.assertFalse((repo / "assets/vintage-telnet/locations/new.png").exists())

    def test_invalid_batch_publishes_nothing(self):
        td, repo = self.make_repo()
        self.addCleanup(td.cleanup)
        incoming = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(incoming, ignore_errors=True))
        (incoming / "good.png").write_bytes(png_bytes())
        (incoming / "bad.png").write_bytes(b"broken")
        target, replace, entries = pub.load_batch(
            incoming, "assets/vintage-telnet/locations/"
        )
        with self.assertRaises(pub.AssetBatchError):
            pub.validate_batch(repo, target, entries, replace=replace)
        self.assertFalse((repo / "assets").exists())
        self.assertEqual(self.git(repo, "rev-list", "--count", "HEAD"), "1")

    def test_publish_creates_one_commit_for_batch(self):
        td, repo = self.make_repo()
        self.addCleanup(td.cleanup)
        incoming = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(incoming, ignore_errors=True))
        (incoming / "one.png").write_bytes(png_bytes(8, 8))
        (incoming / "two.webp").write_bytes(webp_vp8x_bytes(16, 16))
        target, replace, entries = pub.load_batch(
            incoming, "assets/vintage-telnet/locations/"
        )
        assets = pub.validate_batch(repo, target, entries, replace=replace)
        before = int(self.git(repo, "rev-list", "--count", "HEAD"))
        commit = pub.publish(repo, assets, "test asset batch", replace=False)
        after = int(self.git(repo, "rev-list", "--count", "HEAD"))
        self.assertEqual(after, before + 1)
        self.assertEqual(commit, self.git(repo, "rev-parse", "HEAD"))
        self.assertTrue((repo / "assets/vintage-telnet/locations/one.png").exists())
        self.assertTrue((repo / "assets/vintage-telnet/locations/two.webp").exists())

    def test_batch_hash_is_reproducible_independent_of_input_order(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            p1 = base / "a.png"
            p2 = base / "b.png"
            p1.write_bytes(png_bytes(2, 2))
            p2.write_bytes(png_bytes(3, 3))
            def asset(path, dest):
                fmt, w, h, size, sha = pub.inspect_image(path)
                return pub.Asset(path, dest, w, h, fmt, size, sha)
            a = asset(p1, "assets/vintage-telnet/maps/a.png")
            b = asset(p2, "assets/vintage-telnet/maps/b.png")
            self.assertEqual(pub.batch_digest([a, b]), pub.batch_digest([b, a]))

    def test_pr_validation_reuses_same_rules(self):
        td, repo = self.make_repo()
        self.addCleanup(td.cleanup)
        # Create a base ref that points to the initial main commit.
        self.git(repo, "branch", "base-for-pr", "main")
        good = repo / "assets/vintage-telnet/maps/map.png"
        good.parent.mkdir(parents=True)
        good.write_bytes(png_bytes(10, 12))
        self.git(repo, "add", good.relative_to(repo).as_posix())
        self.git(repo, "commit", "-m", "add valid asset")
        self.assertEqual(pub.validate_pr(repo, "base-for-pr"), 0)


if __name__ == "__main__":
    unittest.main()
