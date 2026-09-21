#!/usr/bin/env python3
"""Audita ramas remotas contra origin/main sin decidir su estado semántico.

Uso:
    python scripts/audit-branches.py
    python scripts/audit-branches.py --fetch

La salida es determinista para un mismo estado de Git. Clasificar una rama como
ACTIVA, SUPERADA o RESCATAR sigue siendo una decisión del arquitecto responsable.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} falló")
    return proc.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Ejecuta git fetch --prune origin antes de comparar.",
    )
    args = parser.parse_args()

    try:
        if args.fetch:
            subprocess.run(["git", "fetch", "--prune", "origin"], check=True)

        main_ref = "origin/main"
        git("rev-parse", "--verify", main_ref)

        refs = git(
            "for-each-ref",
            "--format=%(refname:short)",
            "refs/remotes/origin",
        ).splitlines()

        rows: list[tuple[str, int, int, str]] = []
        for ref in refs:
            if ref in {"origin", "origin/HEAD", main_ref}:
                continue
            counts = git("rev-list", "--left-right", "--count", f"{main_ref}...{ref}")
            behind_s, ahead_s = counts.split()
            behind, ahead = int(behind_s), int(ahead_s)

            if ahead == 0:
                relation = "ABSORBIDA/DETRÁS"
            elif behind == 0:
                relation = "ADELANTADA"
            else:
                relation = "DIVERGIDA"

            rows.append((ref.removeprefix("origin/"), ahead, behind, relation))

        rows.sort(key=lambda item: item[0])

        print("| Rama | Ahead | Behind | Relación Git |")
        print("|---|---:|---:|---|")
        for name, ahead, behind, relation in rows:
            print(f"| `{name}` | {ahead} | {behind} | {relation} |")

        return 0
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
