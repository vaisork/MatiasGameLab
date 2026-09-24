"""vt-deploy: un release que falló se aparta (sin borrarse) para que el
reintento del mismo SHA no quede bloqueado tras un rollback (Issue #141)."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

_SPEC = importlib.util.spec_from_file_location(
    "vt_deploy", Path(__file__).resolve().parents[1] / "ops" / "vt_deploy.py")
vt_deploy = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(vt_deploy)


class QuarantineFailedReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.releases = self.root / "releases"
        self.releases.mkdir()
        self.current = self.root / "current"

    def tearDown(self):
        self.temp.cleanup()

    def test_failed_release_is_moved_aside_not_deleted(self):
        good = self.releases / ("a" * 40)
        failed = self.releases / ("b" * 40)
        good.mkdir(); failed.mkdir(); (failed / "evidencia.txt").write_text("log")
        self.current.symlink_to(good)
        with patch.object(vt_deploy, "CURRENT_LINK", self.current):
            moved = vt_deploy.quarantine_failed_release(failed)
        self.assertFalse(failed.exists())  # el reintento ya no choca con "ya existe"
        self.assertTrue(moved.name.startswith(".failed-" + "b" * 40 + "-"))
        self.assertEqual((moved / "evidencia.txt").read_text(), "log")

    def test_current_release_is_never_moved(self):
        good = self.releases / ("a" * 40)
        good.mkdir()
        self.current.symlink_to(good)
        with patch.object(vt_deploy, "CURRENT_LINK", self.current):
            self.assertIsNone(vt_deploy.quarantine_failed_release(good))
        self.assertTrue(good.exists())

    def test_missing_release_is_a_no_op(self):
        with patch.object(vt_deploy, "CURRENT_LINK", self.current):
            self.assertIsNone(vt_deploy.quarantine_failed_release(self.releases / "nada"))


if __name__ == "__main__":
    unittest.main()
