#!/usr/bin/env python3
"""Read-only preflight for the Vintage Telnet Raspberry deployment.

This script does not deploy, restart services, change configuration, or touch SQLite.
It gathers the checks the Raspberry operator repeatedly needs into one command.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
DEFAULT_EXTERNAL = "https://raspberrypi.tail3d212e.ts.net"
_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


def deployed_revision() -> tuple[bool, str]:
    """Return deployed revision from Git checkout or archived release path."""
    code, head = run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)
    if code == 0 and _SHA_RE.fullmatch(head):
        return True, head

    # Production releases are created with git archive, so there is no .git.
    # Path.resolve() follows /opt/vintage-telnet/current into releases/<sha>/...
    for parent in (ROOT, *ROOT.parents):
        candidate = parent.name.lower()
        if _SHA_RE.fullmatch(candidate):
            return True, candidate

    return False, "no se pudo determinar SHA (sin .git ni directorio de release con SHA)"




def run(cmd: list[str], *, cwd: Path | None = None, timeout: int = 30) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout.strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 125, str(exc)


def http_get(url: str, *, timeout: int = 15) -> tuple[int | None, dict[str, str], bytes | str]:
    request = urllib.request.Request(url, headers={"Accept": "*/*", "User-Agent": "vt-preflight/1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, {k.lower(): v for k, v in response.headers.items()}, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, exc.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, {}, str(exc)


def item(name: str, ok: bool, detail: str) -> bool:
    print(f"[{'OK' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def check_http_origin(origin: str, *, label: str) -> list[bool]:
    checks: list[bool] = []

    status, _, body = http_get(origin.rstrip("/") + "/healthz")
    health_ok = status == 200
    detail = f"HTTP {status}" if status is not None else str(body)
    if health_ok:
        try:
            payload = json.loads(body.decode("utf-8"))
            detail += f" {payload}"
        except Exception:
            pass
    checks.append(item(f"{label} healthz", health_ok, detail))

    status, headers, body = http_get(origin.rstrip("/") + "/vintage-telnet.webmanifest")
    manifest_ok = status == 200 and "application/manifest+json" in headers.get("content-type", "")
    manifest_detail = f"HTTP {status}; content-type={headers.get('content-type', '-')}"
    if status == 200:
        try:
            payload = json.loads(body.decode("utf-8"))
            manifest_ok = manifest_ok and payload.get("name") == "Vintage Telnet"
            manifest_ok = manifest_ok and payload.get("start_url") == "/"
            manifest_ok = manifest_ok and payload.get("display") == "standalone"
            manifest_detail += (
                f"; name={payload.get('name')!r}; start_url={payload.get('start_url')!r}; "
                f"display={payload.get('display')!r}"
            )
        except Exception as exc:
            manifest_ok = False
            manifest_detail += f"; JSON inválido: {exc}"
    checks.append(item(f"{label} manifest", manifest_ok, manifest_detail))

    status, headers, body = http_get(origin.rstrip("/") + "/assets/app-icon/vintage-telnet.webp")
    icon_ok = status == 200 and "image/webp" in headers.get("content-type", "") and isinstance(body, bytes) and len(body) > 1000
    checks.append(item(
        f"{label} app icon",
        icon_ok,
        f"HTTP {status}; content-type={headers.get('content-type', '-')}; bytes={len(body) if isinstance(body, bytes) else 0}",
    ))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", help="SHA que se espera tener desplegado (prefijo o completo).")
    parser.add_argument("--external-url", default=DEFAULT_EXTERNAL)
    parser.add_argument("--skip-external", action="store_true")
    parser.add_argument("--tests", action="store_true", help="Ejecuta la suite completa de Vintage Telnet.")
    args = parser.parse_args()

    checks: list[bool] = []

    head_ok, head = deployed_revision()
    if args.expected_head and head_ok:
        head_ok = head.startswith(args.expected_head) or args.expected_head.startswith(head)
    checks.append(item("Release HEAD", head_ok, head))

    code, service = run(["systemctl", "is-active", "vintage-telnet.service"])
    checks.append(item("vintage-telnet.service", code == 0 and service == "active", service or f"error {code}"))

    code, sockets = run(["ss", "-ltn"])
    bind_ok = code == 0 and any("127.0.0.1:8080" in line for line in sockets.splitlines())
    exposed_8080 = any(
        token in line
        for line in sockets.splitlines()
        for token in ("0.0.0.0:8080", "[::]:8080", "*:8080")
    )
    checks.append(item("Puerto 8080 loopback", bind_ok and not exposed_8080, "127.0.0.1:8080" if bind_ok else "no detectado/incorrecto"))

    checks.extend(check_http_origin("http://127.0.0.1:8080", label="local"))

    if not args.skip_external:
        checks.extend(check_http_origin(args.external_url, label="Funnel"))

    code, ollama = run(["systemctl", "is-active", "ollama.service"])
    item("ollama.service (informativo)", code == 0 and ollama == "active", ollama or f"error {code}")
    status, _, body = http_get("http://127.0.0.1:11434/api/tags", timeout=5)
    if status == 200:
        try:
            models = [m.get("name") for m in json.loads(body.decode("utf-8")).get("models", [])]
            print("[INFO] Ollama models: " + ", ".join(filter(None, models)))
        except Exception:
            print("[INFO] Ollama /api/tags respondió, pero no se pudo listar modelos.")
    else:
        print(f"[INFO] Ollama /api/tags: HTTP {status}; no bloquea gameplay normal.")

    if args.tests:
        code, output = run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=ROOT,
            timeout=180,
        )
        tail = "\n".join(output.splitlines()[-8:])
        checks.append(item("Suite Vintage Telnet", code == 0, tail))

    passed = sum(bool(x) for x in checks)
    print(f"\nResultado: {passed}/{len(checks)} checks críticos OK")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
