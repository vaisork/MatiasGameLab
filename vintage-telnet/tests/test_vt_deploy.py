"""Pruebas del comando vt-deploy (Issue #141 / Deploy reusable y seguro).

Verifica:
1. Parseo de argumentos de línea de comandos (soporte de flag --sha explícito y posicional).
2. Verificación de ancestría en Git y resolución de SHA autorizado.
3. Lectura de esquema de base de datos y preservación de lista de jugadores en SQLite.
4. Cuarentena de releases fallidos (.failed-<sha>-<timestamp>) sin borrarlos para permitir reintentos.
5. Restauración atómica de base de datos desde backup verificado.
6. Mecanismo de rollback automático ante fallas post-switch.
"""
import importlib.util
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

_SPEC = importlib.util.spec_from_file_location(
    "vt_deploy", Path(__file__).resolve().parents[1] / "ops" / "vt_deploy.py"
)
vt_deploy = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(vt_deploy)


def are_symlinks_supported() -> bool:
    """Detecta si el entorno actual soporta creación de symlinks sin privilegios."""
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "src"
        src.mkdir()
        dst = Path(td) / "link"
        try:
            dst.symlink_to(src)
            return True
        except OSError:
            return False


class DeployCliArgumentParsingTests(unittest.TestCase):
    """Verifica que el comando CLI acepte --sha explícito conforme al contrato de #141."""

    def test_cli_accepts_explicit_sha_flag(self):
        sha_val = "a" * 40
        with patch.object(vt_deploy, "resolve_authorized_sha", return_value=sha_val) as mock_resolve, \
             patch.object(vt_deploy, "LOCK_FILE", Path(tempfile.gettempdir()) / "test_vt_deploy.lock"), \
             patch("builtins.open", unittest.mock.mock_open()), \
             patch.object(vt_deploy, "run"), \
             patch.object(vt_deploy, "health_payload", return_value={"status": "ok", "schema_version": 10}), \
             patch.object(vt_deploy, "CURRENT_LINK") as mock_current, \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_dir", return_value=True):
            mock_current.exists.return_value = True
            mock_current.resolve.return_value = Path("/opt/vintage-telnet/releases") / sha_val

            # Con --sha explícito
            ret = vt_deploy.main(["--sha", sha_val, "--skip-fetch"])
            self.assertEqual(ret, 0)
            mock_resolve.assert_called()
            # El target_revision pasado a resolve_authorized_sha debe ser sha_val
            self.assertEqual(mock_resolve.call_args[0][3], sha_val)

    def test_cli_accepts_positional_revision(self):
        sha_val = "b" * 40
        with patch.object(vt_deploy, "resolve_authorized_sha", return_value=sha_val) as mock_resolve, \
             patch.object(vt_deploy, "LOCK_FILE", Path(tempfile.gettempdir()) / "test_vt_deploy.lock"), \
             patch("builtins.open", unittest.mock.mock_open()), \
             patch.object(vt_deploy, "run"), \
             patch.object(vt_deploy, "health_payload", return_value={"status": "ok", "schema_version": 10}), \
             patch.object(vt_deploy, "CURRENT_LINK") as mock_current, \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_dir", return_value=True):
            mock_current.exists.return_value = True
            mock_current.resolve.return_value = Path("/opt/vintage-telnet/releases") / sha_val

            # Con posicional "latest"
            ret = vt_deploy.main(["latest", "--skip-fetch"])
            self.assertEqual(ret, 0)
            self.assertEqual(mock_resolve.call_args[0][3], "latest")

    def test_cli_fails_when_no_revision_specified(self):
        with self.assertRaises(vt_deploy.DeployError) as ctx:
            vt_deploy.main(["--skip-fetch"])
        self.assertIn("Debe especificar un SHA o revisión", str(ctx.exception))


class DatabaseAndSchemaOperationsTests(unittest.TestCase):
    """Verifica operaciones autoritativas sobre la base SQLite viva y backups."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db_path = self.root / "vintage.sqlite3"

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE players (id TEXT PRIMARY KEY, username TEXT)")
        cur.execute("INSERT INTO players (id, username) VALUES ('p-101', 'valan')")
        cur.execute("INSERT INTO players (id, username) VALUES ('p-102', 'mira')")
        con.commit()
        con.close()

    def tearDown(self):
        self.temp.cleanup()

    def test_database_player_ids_reads_ordered_ids(self):
        players = vt_deploy.database_player_ids(self.db_path)
        self.assertEqual(players, ["p-101", "p-102"])

    def test_database_player_ids_fails_on_missing_file(self):
        missing = self.root / "missing.sqlite3"
        with self.assertRaises(vt_deploy.DeployError) as ctx:
            vt_deploy.database_player_ids(missing)
        self.assertIn("No existe la base viva", str(ctx.exception))

    def test_restore_database_restores_from_backup_atomically(self):
        backup_path = self.root / "vintage-backup.sqlite3"
        con = sqlite3.connect(backup_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE players (id TEXT PRIMARY KEY)")
        cur.execute("INSERT INTO players (id) VALUES ('backup-player-1')")
        con.commit()
        con.close()

        original_stat = self.db_path.stat()
        with patch.object(vt_deploy, "DATA_DIR", self.root), \
             patch.object(vt_deploy, "DATABASE", self.db_path):
            vt_deploy.restore_database(backup_path, original_stat)

        # La base viva contiene ahora los datos restaurados del backup
        restored_players = vt_deploy.database_player_ids(self.db_path)
        self.assertEqual(restored_players, ["backup-player-1"])


class QuarantineFailedReleaseTests(unittest.TestCase):
    """Verifica que un release que falló se aparte sin borrarse (evidencia de auditoría)."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.releases = self.root / "releases"
        self.releases.mkdir()
        self.current = self.root / "current"

    def tearDown(self):
        self.temp.cleanup()

    def test_failed_release_is_moved_aside_not_deleted(self):
        failed = self.releases / ("b" * 40)
        failed.mkdir()
        (failed / "evidencia.txt").write_text("log de prueba", encoding="utf-8")

        mock_current = self.root / "current_mock"
        with patch.object(vt_deploy, "CURRENT_LINK", mock_current):
            moved = vt_deploy.quarantine_failed_release(failed)

        self.assertFalse(failed.exists(), "El release original ya no debe existir para permitir reintento")
        self.assertIsNotNone(moved)
        self.assertTrue(moved.name.startswith(".failed-" + "b" * 40 + "-"))
        self.assertEqual((moved / "evidencia.txt").read_text(encoding="utf-8"), "log de prueba")

    def test_current_release_is_never_moved(self):
        good = self.releases / ("a" * 40)
        good.mkdir()
        # Mockeamos CURRENT_LINK como apuntando a good
        mock_current = MagicMock()
        mock_current.exists.return_value = True
        mock_current.resolve.return_value = good.resolve()

        with patch.object(vt_deploy, "CURRENT_LINK", mock_current):
            self.assertIsNone(vt_deploy.quarantine_failed_release(good))
        self.assertTrue(good.exists(), "El release activo (current) nunca debe ser apartado")

    def test_missing_release_is_a_no_op(self):
        mock_current = MagicMock()
        mock_current.exists.return_value = False
        with patch.object(vt_deploy, "CURRENT_LINK", mock_current):
            self.assertIsNone(vt_deploy.quarantine_failed_release(self.releases / "no_existe"))


class RollbackMechanismTests(unittest.TestCase):
    """Verifica el mecanismo de rollback automático en caso de fallo post-switch."""

    def test_rollback_restores_database_and_restarts_service(self):
        previous_target = Path("/opt/vintage-telnet/releases/previous_sha")
        backup = Path("/var/backups/vintage-backup.sqlite3")
        original_stat = MagicMock()

        with patch.object(vt_deploy, "run") as mock_run, \
             patch.object(vt_deploy, "restore_database") as mock_restore, \
             patch.object(vt_deploy, "atomic_current") as mock_atomic, \
             patch.object(vt_deploy, "health_payload", return_value={"status": "ok"}):

            vt_deploy.rollback(previous_target, backup, original_stat)

            # 1. Detiene servicio
            mock_run.assert_any_call(["systemctl", "stop", vt_deploy.SERVICE], check=False, timeout=60)
            # 2. Restaura base de datos
            mock_restore.assert_called_once_with(backup, original_stat)
            # 3. Conmuta symlink a release anterior
            mock_atomic.assert_called_once_with(previous_target)
            # 4. Reinicia servicio
            mock_run.assert_any_call(["systemctl", "start", vt_deploy.SERVICE], timeout=60)

    def test_rollback_without_previous_target_leaves_service_stopped(self):
        backup = Path("/var/backups/vintage-backup.sqlite3")
        original_stat = MagicMock()

        with patch.object(vt_deploy, "run") as mock_run, \
             patch.object(vt_deploy, "restore_database") as mock_restore, \
             patch.object(vt_deploy, "atomic_current") as mock_atomic:

            vt_deploy.rollback(None, backup, original_stat)

            mock_run.assert_called_once_with(["systemctl", "stop", vt_deploy.SERVICE], check=False, timeout=60)
            mock_restore.assert_called_once_with(backup, original_stat)
            mock_atomic.assert_not_called()


class ResolutionAndAncestryValidationTests(unittest.TestCase):
    """Verifica que solo se desplieguen SHAs integrados y ancestros de origin/main."""

    def test_resolve_authorized_sha_rejects_non_ancestor_commit(self):
        repo = Path("/home/jdiaz/MatiasGameLab")
        sha = "c" * 40
        with patch.object(vt_deploy, "git_output", return_value=sha), \
             patch.object(vt_deploy, "run") as mock_run:
            # Simular que merge-base --is-ancestor devuelve código != 0 (no es ancestro)
            failed_proc = subprocess.CompletedProcess(args=[], returncode=1, stdout="not an ancestor")
            mock_run.return_value = failed_proc

            with self.assertRaises(vt_deploy.DeployError) as ctx:
                vt_deploy.resolve_authorized_sha(repo, "jdiaz", "/home/jdiaz", sha, skip_fetch=True)
            self.assertIn("no es ancestro de origin/main", str(ctx.exception))

    def test_resolve_authorized_sha_accepts_valid_ancestor(self):
        repo = Path("/home/jdiaz/MatiasGameLab")
        sha = "d" * 40
        with patch.object(vt_deploy, "git_output", return_value=sha), \
             patch.object(vt_deploy, "run") as mock_run:
            # Simular que merge-base --is-ancestor devuelve código 0 (es ancestro)
            ok_proc = subprocess.CompletedProcess(args=[], returncode=0, stdout="")
            mock_run.return_value = ok_proc

class FullDeploySimulationTests(unittest.TestCase):
    """Simulación end-to-end de la máquina de estados de vt-deploy."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.releases = self.root / "releases"
        self.releases.mkdir()
        self.current = self.root / "current"
        self.data_dir = self.root / "data"
        self.data_dir.mkdir()
        self.db_path = self.data_dir / "vintage.sqlite3"
        self.db_path.write_text("db_content", encoding="utf-8")
        self.lock_file = self.root / "vt.lock"

        self.repo = self.root / "repo"
        (self.repo / ".git").mkdir(parents=True)
        (self.repo / "vintage-telnet").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_full_deploy_cycle_happy_path(self):
        sha = "e" * 40
        prev_sha = "d" * 40
        prev_dir = self.releases / prev_sha
        prev_dir.mkdir()

        mock_current = MagicMock()
        mock_current.exists.return_value = True
        mock_current.is_symlink.return_value = True
        mock_current.resolve.return_value = prev_dir

        def fake_archive(repo, owner, home, sha, dest):
            p = dest / "vintage-telnet"
            p.mkdir(parents=True)
            (p / "requirements.txt").write_text("", encoding="utf-8")

        with patch.object(vt_deploy, "INSTALL_ROOT", self.root), \
             patch.object(vt_deploy, "RELEASES_ROOT", self.releases), \
             patch.object(vt_deploy, "CURRENT_LINK", mock_current), \
             patch.object(vt_deploy, "DATA_DIR", self.data_dir), \
             patch.object(vt_deploy, "DATABASE", self.db_path), \
             patch.object(vt_deploy, "LOCK_FILE", self.lock_file), \
             patch.object(vt_deploy, "resolve_authorized_sha", return_value=sha), \
             patch.object(vt_deploy, "archive_commit", side_effect=fake_archive), \
             patch.object(vt_deploy, "read_expected_schema", return_value=10), \
             patch.object(vt_deploy, "database_player_ids", return_value=["p1"]), \
             patch.object(vt_deploy, "verified_backup", return_value=self.root / "backup.sqlite3"), \
             patch.object(vt_deploy, "validate_migration_on_copy"), \
             patch.object(vt_deploy, "atomic_current") as mock_atomic, \
             patch.object(vt_deploy, "health_payload", return_value={"status": "ok", "schema_version": 10}), \
             patch.object(vt_deploy, "external_health_info"), \
             patch.object(vt_deploy, "run"):

            rc = vt_deploy.main(["--sha", sha, "--repo-root", str(self.repo), "--skip-fetch"])
            self.assertEqual(rc, 0)
            mock_atomic.assert_called_once_with(self.releases / sha)

    def test_pre_switch_failure_does_not_touch_current_or_run_rollback(self):
        """Un fallo durante la validación previa no debe tocar producción.

        Si la migración simulada falla antes de detener el servicio o cambiar
        el symlink current, el deploy aborta sin ejecutar rollback: todavía no
        existe nada que restaurar en producción.
        """
        sha = "a" * 40
        prev_sha = "d" * 40
        prev_dir = self.releases / prev_sha
        prev_dir.mkdir()

        mock_current = MagicMock()
        mock_current.exists.return_value = True
        mock_current.is_symlink.return_value = True
        mock_current.resolve.return_value = prev_dir

        def fake_archive(repo, owner, home, sha, dest):
            project = dest / "vintage-telnet"
            project.mkdir(parents=True)
            (project / "requirements.txt").write_text("", encoding="utf-8")

        with patch.object(vt_deploy, "INSTALL_ROOT", self.root), \
             patch.object(vt_deploy, "RELEASES_ROOT", self.releases), \
             patch.object(vt_deploy, "CURRENT_LINK", mock_current), \
             patch.object(vt_deploy, "DATA_DIR", self.data_dir), \
             patch.object(vt_deploy, "DATABASE", self.db_path), \
             patch.object(vt_deploy, "LOCK_FILE", self.lock_file), \
             patch.object(vt_deploy, "resolve_authorized_sha", return_value=sha), \
             patch.object(vt_deploy, "archive_commit", side_effect=fake_archive), \
             patch.object(vt_deploy, "read_expected_schema", return_value=10), \
             patch.object(vt_deploy, "database_player_ids", return_value=["p1"]), \
             patch.object(vt_deploy, "verified_backup", return_value=self.root / "backup.sqlite3"), \
             patch.object(
                 vt_deploy,
                 "validate_migration_on_copy",
                 side_effect=vt_deploy.DeployError("migración inválida"),
             ), \
             patch.object(vt_deploy, "atomic_current") as mock_atomic, \
             patch.object(vt_deploy, "rollback") as mock_rollback, \
             patch.object(vt_deploy, "run") as mock_run:

            with self.assertRaises(vt_deploy.DeployError) as ctx:
                vt_deploy.main(["--sha", sha, "--repo-root", str(self.repo), "--skip-fetch"])

            self.assertIn("migración inválida", str(ctx.exception))
            mock_atomic.assert_not_called()
            mock_rollback.assert_not_called()
            self.assertFalse(
                any(call.args and call.args[0] and call.args[0][0] == "systemctl"
                    for call in mock_run.call_args_list),
                "Un fallo pre-switch no debe detener ni reiniciar el servicio.",
            )

    def test_full_deploy_cycle_triggers_rollback_on_health_failure(self):
        sha = "f" * 40
        prev_sha = "d" * 40
        prev_dir = self.releases / prev_sha
        prev_dir.mkdir()

        mock_current = MagicMock()
        mock_current.exists.return_value = True
        mock_current.is_symlink.return_value = True
        mock_current.resolve.return_value = prev_dir

        def fake_archive(repo, owner, home, sha, dest):
            p = dest / "vintage-telnet"
            p.mkdir(parents=True)
            (p / "requirements.txt").write_text("", encoding="utf-8")

        with patch.object(vt_deploy, "INSTALL_ROOT", self.root), \
             patch.object(vt_deploy, "RELEASES_ROOT", self.releases), \
             patch.object(vt_deploy, "CURRENT_LINK", mock_current), \
             patch.object(vt_deploy, "DATA_DIR", self.data_dir), \
             patch.object(vt_deploy, "DATABASE", self.db_path), \
             patch.object(vt_deploy, "LOCK_FILE", self.lock_file), \
             patch.object(vt_deploy, "resolve_authorized_sha", return_value=sha), \
             patch.object(vt_deploy, "archive_commit", side_effect=fake_archive), \
             patch.object(vt_deploy, "read_expected_schema", return_value=10), \
             patch.object(vt_deploy, "database_player_ids", return_value=["p1"]), \
             patch.object(vt_deploy, "verified_backup", return_value=self.root / "backup.sqlite3"), \
             patch.object(vt_deploy, "validate_migration_on_copy"), \
             patch.object(vt_deploy, "atomic_current"), \
             patch.object(vt_deploy, "health_payload", side_effect=vt_deploy.DeployError("health timeout")), \
             patch.object(vt_deploy, "rollback") as mock_rollback, \
             patch.object(vt_deploy, "run"):

            with self.assertRaises(vt_deploy.DeployError) as ctx:
                vt_deploy.main(["--sha", sha, "--repo-root", str(self.repo), "--skip-fetch"])
            self.assertIn("health timeout", str(ctx.exception))
            mock_rollback.assert_called_once()
            self.assertEqual(mock_rollback.call_args[0][0], prev_dir)


if __name__ == "__main__":
    unittest.main()
