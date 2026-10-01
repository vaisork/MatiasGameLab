"""Operator update of the running claude/vintage-telnet-server-v2 deployment
to a new SHA, explicitly authorized by Javier: fixes the stale schema log
message and adds the periodic SQLite backup timer requested in HANDOFF.md.

Run locally with sudo. Does NOT touch live data (/var/lib/vintage-telnet);
only adds a new release dir, swaps the `current` symlink, restarts the main
service, and installs+enables the new backup timer.

Usage: sudo python3 ops/update_v2_authorized.py
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

SHA = "6c6a1bf56691b94ea6748c6b740e6da49d97f773"
REPO = Path("/home/jdiaz/MatiasGameLab")
ROOT = Path("/opt/vintage-telnet")
DATA = Path("/var/lib/vintage-telnet")
BACKUPS = Path("/var/backups/vintage-telnet")
RELEASE = ROOT / "releases" / SHA
APP = RELEASE / "vintage-telnet"
PYTHON = APP / ".venv/bin/python"
BASE = "http://" + os.environ.get("VT_HEALTH_HOST", "127.0.0.1") + ":8080"
UNIT = Path("/etc/systemd/system/vintage-telnet.service")
BACKUP_UNIT = Path("/etc/systemd/system/vintage-telnet-backup.service")
BACKUP_TIMER = Path("/etc/systemd/system/vintage-telnet-backup.timer")


def run(*args, cwd=None, capture=False):
    return subprocess.run([str(a) for a in args], cwd=cwd, check=True,
                          text=True, capture_output=capture)


def health():
    for _ in range(50):
        try:
            with urllib.request.urlopen(BASE + "/healthz", timeout=2) as response:
                result = json.load(response)
            assert result == {"status": "ok", "schema_version": 2}
            return result
        except (OSError, urllib.error.URLError, AssertionError):
            time.sleep(.2)
    raise RuntimeError("El servicio no responde correctamente (schema_version 2) en loopback")


def main():
    if os.geteuid() != 0:
        raise SystemExit("Ejecutar localmente con sudo.")
    os.umask(0o077)

    git = ["runuser", "-u", "jdiaz", "--", "git", "-C", REPO]
    if run(*git, "rev-parse", "HEAD", capture=True).stdout.strip() != SHA:
        raise SystemExit("HEAD de /home/jdiaz/MatiasGameLab distinto del autorizado; "
                         "hacer git checkout claude/vintage-telnet-server-v2 && git pull primero.")
    run(*git, "diff", "--exit-code", SHA, "--", "vintage-telnet/server",
        "vintage-telnet/tests", "vintage-telnet/requirements.txt", "vintage-telnet/ops")

    if RELEASE.exists():
        raise SystemExit(f"Ya existe {RELEASE}; inspeccionar antes de continuar.")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # Backup previo por seguridad, antes de tocar nada (no reemplaza el timer nuevo).
    run("install", "-d", "-m", "0700", "-o", "vintage-telnet", "-g", "vintage-telnet", BACKUPS)
    pre_update_backup = BACKUPS / f"pre-update-{stamp}.sqlite3"
    current_app = ROOT / "current/vintage-telnet"
    current_python = current_app / ".venv/bin/python"
    run("runuser", "-u", "vintage-telnet", "--", current_python, "-m", "server.admin",
        "--data-dir", DATA, "backup", pre_update_backup, cwd=current_app)
    print("Backup previo a la actualización:", pre_update_backup, flush=True)

    # --- Nuevo release ---
    run("install", "-d", "-m", "0755", RELEASE)
    with tempfile.TemporaryFile() as archive:
        subprocess.run([str(a) for a in [*git, "archive", SHA]], stdout=archive, check=True)
        archive.seek(0)
        run_env = os.umask(0o022)
        try:
            subprocess.run(["tar", "-x", "-C", str(RELEASE)], stdin=archive, check=True)
            run("python3", "-m", "venv", APP / ".venv")
            run(PYTHON, "-m", "pip", "install", "-r", APP / "requirements.txt")
        finally:
            os.umask(run_env)

    run("runuser", "-u", "vintage-telnet", "--", PYTHON, "-B", "-m",
        "unittest", "discover", "-s", "tests", "-v", cwd=APP)
    run(PYTHON, "-m", "pip", "check", cwd=APP)

    # --- Swap y reinicio del servicio principal ---
    ROOT.joinpath("current").unlink()
    ROOT.joinpath("current").symlink_to(RELEASE)
    run("install", "-m", "0644", APP / "ops/vintage-telnet.service", UNIT)
    run("systemctl", "daemon-reload")
    run("systemctl", "restart", "vintage-telnet.service")
    result = health()

    # --- Timer de respaldo (nuevo) ---
    run("chmod", "0755", APP / "ops/backup.sh")  # git archive conserva el modo, pero lo forzamos
    run("install", "-m", "0644", APP / "ops/vintage-telnet-backup.service", BACKUP_UNIT)
    run("install", "-m", "0644", APP / "ops/vintage-telnet-backup.timer", BACKUP_TIMER)
    run("systemctl", "daemon-reload")
    run("systemctl", "enable", "--now", "vintage-telnet-backup.timer")

    run("systemctl", "show", "vintage-telnet.service", "-p", "ActiveState", "-p", "SubState")
    run("systemctl", "show", "vintage-telnet-backup.timer", "-p", "ActiveState")
    run("systemctl", "list-timers", "vintage-telnet-backup.timer", "--no-pager")
    print(json.dumps({"sha": SHA, "utc": stamp, "health": result,
                      "pre_update_backup": str(pre_update_backup),
                      "backup_timer_enabled": True}, indent=2))
    print("Actualización completada. Raspberry sin reiniciar.")


if __name__ == "__main__":
    main()
