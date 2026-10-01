"""One-time operator install/update to claude/vintage-telnet-server-v2 (PR #6),
explicitly authorized by Javier to replace the historical codex/vintage-telnet-server
(PR #1) deployment.

Run locally with sudo. Decommissions (stops/disables) the old vintage-telnet.service
and moves its data dir aside (does not delete it) because the new server uses an
incompatible schema_version. Then installs the new release fresh.

Usage: sudo VT_DM_PASSWORD='...' python3 ops/install_v2_authorized.py
(VT_DM_PASSWORD is read from the environment, never hardcoded in this file.)
"""
import grp
import json
import os
from pathlib import Path
import pwd
import secrets
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

SHA = "8b1e13859fc02c636963d93c1533e482d1565dc9"
REPO = Path("/home/jdiaz/MatiasGameLab")
ROOT = Path("/opt/vintage-telnet")
DATA = Path("/var/lib/vintage-telnet")
BACKUPS = Path("/var/backups/vintage-telnet")
CONFIG = Path("/etc/vintage-telnet")
UNIT = Path("/etc/systemd/system/vintage-telnet.service")
RELEASE = ROOT / "releases" / SHA
APP = RELEASE / "vintage-telnet"
PYTHON = APP / ".venv/bin/python"
BASE = "http://127.0.0.1:8080"


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
        raise SystemExit("Ejecutar localmente con sudo; no enviar contraseñas al chat.")
    dm_password = os.environ.get("VT_DM_PASSWORD")
    if not dm_password:
        raise SystemExit("Falta VT_DM_PASSWORD en el entorno (no la pases en la línea de comandos en texto plano si podés evitarlo).")
    os.umask(0o077)

    git = ["runuser", "-u", "jdiaz", "--", "git", "-C", REPO]
    if run(*git, "rev-parse", "HEAD", capture=True).stdout.strip() != SHA:
        raise SystemExit("HEAD de /home/jdiaz/MatiasGameLab distinto del autorizado; hacer git checkout/pull primero.")
    run(*git, "diff", "--exit-code", SHA, "--", "vintage-telnet/server",
        "vintage-telnet/tests", "vintage-telnet/requirements.txt",
        "vintage-telnet/ops/server.env.example", "vintage-telnet/ops/vintage-telnet.service")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # --- Decommission the old codex/vintage-telnet-server (PR #1) deployment ---
    state = run("systemctl", "show", "vintage-telnet.service", "-p", "ActiveState",
                "--value", capture=True).stdout.strip()
    print("Estado previo del servicio:", state, flush=True)
    subprocess.run(["systemctl", "stop", "vintage-telnet.service"], check=False)
    subprocess.run(["systemctl", "disable", "vintage-telnet.service"], check=False)
    if DATA.exists():
        moved = DATA.parent / f"vintage-telnet-codex-old-{stamp}"
        shutil.move(str(DATA), str(moved))
        print("Datos viejos (schema codex) movidos a:", moved, flush=True)
    if UNIT.exists():
        backup_unit = UNIT.with_name(f"vintage-telnet.service.codex-old-{stamp}")
        shutil.copy2(UNIT, backup_unit)
        print("Unit anterior respaldada en:", backup_unit, flush=True)

    # --- Fresh install of the new release ---
    run("install", "-d", "-m", "0755", ROOT, ROOT / "releases", RELEASE)
    run("install", "-d", "-m", "0700", CONFIG)
    try:
        pwd.getpwnam("vintage-telnet")
    except KeyError:
        run("useradd", "--system", "--user-group", "--home-dir", DATA,
            "--shell", "/usr/sbin/nologin", "vintage-telnet")
    run("install", "-d", "-m", "0700", "-o", "vintage-telnet", "-g",
        "vintage-telnet", DATA, BACKUPS)

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

    config = (APP / "ops/server.env.example").read_text()
    config = config.replace("REPLACE_WITH_RANDOM_SECRET_AT_LEAST_32_CHARACTERS",
                            secrets.token_hex(32))
    config = config.replace("REPLACE_WITH_A_PASSWORD_ONLY_JAVIER_KNOWS", dm_password)
    old_env = CONFIG / "server.env"
    if old_env.exists():
        shutil.move(str(old_env), str(CONFIG / f"server.env.codex-old-{stamp}"))
        print("server.env viejo (Codex) movido a server.env.codex-old-" + stamp, flush=True)
    with old_env.open("x") as stream:
        stream.write(config)

    if ROOT.joinpath("current").exists() or ROOT.joinpath("current").is_symlink():
        ROOT.joinpath("current").unlink()
    ROOT.joinpath("current").symlink_to(RELEASE)
    run("install", "-m", "0644", APP / "ops/vintage-telnet.service", UNIT)
    run("systemctl", "daemon-reload")
    run("systemctl", "enable", "--now", "vintage-telnet.service")
    result = health()

    run("systemctl", "show", "vintage-telnet.service", "-p", "ActiveState", "-p", "SubState")
    run("ss", "-ltnp", "sport = :8080")
    print(json.dumps({"sha": SHA, "utc": stamp, "health": result,
                      "old_service_decommissioned": True}, indent=2))
    print("Instalación completada. Raspberry sin reiniciar.")


if __name__ == "__main__":
    main()
