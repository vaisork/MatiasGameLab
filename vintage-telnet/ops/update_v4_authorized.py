"""Operator update of the running deployment to the SHA that merges the
"El lindero roto" playable pilot (Issue #45 / PR #49): combat, creatures,
XP, discoveries, progressive map. Schema bumps 2 -> 5 (additive migration,
see server/store.py initialize()).

Run locally with sudo. Backs up before touching anything, installs a new
release, swaps `current`, restarts the main service, verifies the schema
migrated correctly and that existing player accounts are still intact and
unmodified in their identity/created_at fields (only schema-level new
columns should appear, values unchanged for pre-existing rows).

Usage: sudo python3 ops/update_v4_authorized.py
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

SHA = "7de889ac7c3940d83e0f0b844532054f00b06bae"
REPO = Path("/home/jdiaz/MatiasGameLab")
ROOT = Path("/opt/vintage-telnet")
DATA = Path("/var/lib/vintage-telnet")
BACKUPS = Path("/var/backups/vintage-telnet")
RELEASE = ROOT / "releases" / SHA
APP = RELEASE / "vintage-telnet"
PYTHON = APP / ".venv/bin/python"
BASE = "http://" + os.environ.get("VT_HEALTH_HOST", "127.0.0.1") + ":8080"
UNIT = Path("/etc/systemd/system/vintage-telnet.service")
EXPECTED_SCHEMA = 5


def run(*args, cwd=None, capture=False):
    return subprocess.run([str(a) for a in args], cwd=cwd, check=True,
                          text=True, capture_output=capture)


def health():
    for _ in range(50):
        try:
            with urllib.request.urlopen(BASE + "/healthz", timeout=2) as response:
                result = json.load(response)
            assert result == {"status": "ok", "schema_version": EXPECTED_SCHEMA}
            return result
        except (OSError, urllib.error.URLError, AssertionError):
            time.sleep(.2)
    raise RuntimeError(f"El servicio no responde correctamente (schema_version {EXPECTED_SCHEMA}) en loopback")


def main():
    if os.geteuid() != 0:
        raise SystemExit("Ejecutar localmente con sudo.")
    os.umask(0o077)

    git = ["runuser", "-u", "jdiaz", "--", "git", "-C", REPO]
    if run(*git, "rev-parse", "HEAD", capture=True).stdout.strip() != SHA:
        raise SystemExit("HEAD de /home/jdiaz/MatiasGameLab distinto del autorizado; "
                         "hacer git checkout main && git pull primero.")
    run(*git, "diff", "--exit-code", SHA, "--", "vintage-telnet/server",
        "vintage-telnet/tests", "vintage-telnet/requirements.txt", "vintage-telnet/ops")

    if RELEASE.exists():
        raise SystemExit(f"Ya existe {RELEASE}; inspeccionar antes de continuar.")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    current_app = ROOT / "current/vintage-telnet"
    current_python = current_app / ".venv/bin/python"

    # Estado de jugadores ANTES, para comparar identidad/created_at después de migrar.
    players_before = run("runuser", "-u", "vintage-telnet", "--", current_python, "-m",
                         "server.admin", "--data-dir", DATA, "players",
                         cwd=current_app, capture=True).stdout
    print("Jugadores antes de migrar:", players_before, flush=True)

    # Backup previo por seguridad, antes de tocar nada.
    run("install", "-d", "-m", "0700", "-o", "vintage-telnet", "-g", "vintage-telnet", BACKUPS)
    pre_update_backup = BACKUPS / f"pre-lindero-{stamp}.sqlite3"
    run("runuser", "-u", "vintage-telnet", "--", current_python, "-m", "server.admin",
        "--data-dir", DATA, "backup", pre_update_backup, cwd=current_app)
    print("Backup previo a la migración:", pre_update_backup, flush=True)

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

    # --- Swap y reinicio (la migracion de esquema 2->5 corre sola al arrancar) ---
    ROOT.joinpath("current").unlink()
    ROOT.joinpath("current").symlink_to(RELEASE)
    run("install", "-m", "0644", APP / "ops/vintage-telnet.service", UNIT)
    run("systemctl", "daemon-reload")
    run("systemctl", "restart", "vintage-telnet.service")
    result = health()

    # --- Verificacion post-migracion: los jugadores existentes siguen ahi ---
    players_after = run("runuser", "-u", "vintage-telnet", "--", PYTHON, "-m",
                        "server.admin", "--data-dir", DATA, "players",
                        cwd=APP, capture=True).stdout
    check_after = run("runuser", "-u", "vintage-telnet", "--", PYTHON, "-m",
                      "server.admin", "--data-dir", DATA, "check",
                      cwd=APP, capture=True).stdout.strip()

    before_ids = sorted(p["id"] for p in json.loads(players_before))
    after_ids = sorted(p["id"] for p in json.loads(players_after))
    if before_ids != after_ids:
        raise RuntimeError(
            f"Los jugadores no coinciden despues de migrar. Antes: {before_ids} "
            f"Despues: {after_ids}. NO declarar exito; investigar antes de seguir."
        )

    print(json.dumps({
        "sha": SHA,
        "utc": stamp,
        "health": result,
        "pre_update_backup": str(pre_update_backup),
        "players_preserved": True,
        "player_ids": after_ids,
        "post_migration_check": check_after,
    }, indent=2))
    print("Actualización completada (El lindero roto desplegado). Raspberry sin reiniciar.")


if __name__ == "__main__":
    main()
