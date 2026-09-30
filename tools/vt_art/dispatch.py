#!/usr/bin/env python3
"""Dispatch one approved art request to the isolated GitHub Actions runner."""
from __future__ import annotations

import argparse
from pathlib import PurePosixPath
import subprocess
import sys
from typing import Sequence


REPOSITORY = "vaisork/MatiasGameLab"
WORKFLOW = "vt-art-pilot.yml"
RUN_URL = f"https://github.com/{REPOSITORY}/actions/workflows/{WORKFLOW}"
REQUEST_ROOT = PurePosixPath("vintage-telnet/art_requests")


class DispatchError(Exception):
    """A safe-to-display dispatch error."""


def validate_request_path(value: str) -> str:
    path = PurePosixPath(value)
    if (
        path.parent != REQUEST_ROOT
        or path.suffix.lower() != ".json"
        or path.name == "template.json"
        or ".." in path.parts
    ):
        raise DispatchError("Selecciona un JSON directo dentro de vintage-telnet/art_requests/.")
    return path.as_posix()


def _run(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, text=True, capture_output=True, check=False)
    except FileNotFoundError as exc:
        raise DispatchError("Falta GitHub CLI (gh); instálalo y autentícalo en esta Raspberry.") from exc


def dispatch(request_file: str, *, runner=_run) -> None:
    request_file = validate_request_path(request_file)
    auth = runner(["gh", "auth", "status", "--hostname", "github.com"])
    if auth.returncode:
        raise DispatchError("GitHub CLI no está autenticado para iniciar workflows.")

    # Check the exact request on main before asking GitHub to start a billable run.
    request_check = runner([
        "gh", "api", f"repos/{REPOSITORY}/contents/{request_file}",
        "--field", "ref=main", "--jq", ".path",
    ])
    if request_check.returncode or request_check.stdout.strip() != request_file:
        raise DispatchError("La ficha no existe en main; súbela y fusiónala antes de generarla.")

    result = runner([
        "gh", "workflow", "run", WORKFLOW,
        "--repo", REPOSITORY,
        "--ref", "main",
        "--field", f"request_file={request_file}",
    ])
    if result.returncode:
        raise DispatchError("GitHub rechazó el inicio del workflow; revisa Actions y el permiso Actions: write.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inicia una generación individual de arte en GitHub Actions; la clave OpenAI permanece en GitHub."
    )
    parser.add_argument("request_file", help="Ficha JSON que ya está en main.")
    parser.add_argument("--yes", action="store_true", help="Confirma sin pregunta interactiva.")
    args = parser.parse_args(argv)
    try:
        request_file = validate_request_path(args.request_file)
        if not args.yes:
            print(f"Se solicitará UNA generación facturable para: {request_file}")
            if input("Escribe GENERAR para continuar: ").strip() != "GENERAR":
                print("Cancelado; no se inició ninguna generación.")
                return 0
        dispatch(request_file)
    except DispatchError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print("Solicitud enviada a GitHub Actions. La clave OpenAI permanece en GitHub.")
    print(f"Revisa la ejecución y su PR de borrador en: {RUN_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
