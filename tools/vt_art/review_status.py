"""Sync a GitHub art PR review decision to its draft metadata."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
METADATA_PATH = re.compile(
    r"^vintage-telnet/art_generations/[A-Za-z0-9_-]+/v[0-9]{3,}/metadata\.json$"
)
REVIEW_STATUS = {"approved": "approved", "changes_requested": "rejected", "dismissed": "draft"}


class ReviewStatusError(Exception):
    """A safe-to-display failure applying an art review decision."""


def metadata_paths(files: list[dict[str, Any]]) -> list[str]:
    paths = sorted(
        file["filename"]
        for file in files
        if isinstance(file, dict)
        and isinstance(file.get("filename"), str)
        and METADATA_PATH.fullmatch(file["filename"])
    )
    if not paths:
        raise ReviewStatusError("La PR no contiene metadata de una generación de arte reconocida.")
    return paths


def status_for_review(review_state: str) -> str:
    try:
        return REVIEW_STATUS[review_state]
    except KeyError as exc:
        raise ReviewStatusError("La revisión no representa aprobación, rechazo o retiro de decisión.") from exc


def is_current_review(review_state: str, review_commit: str, current_head: str) -> bool:
    # Dismissal often refers to a review made against the parent commit before
    # this workflow's metadata-only commit, so it must still reset the status.
    return review_state == "dismissed" or not review_commit or review_commit == current_head


def run(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, text=True, capture_output=True, check=False)
    except FileNotFoundError as exc:
        raise ReviewStatusError("No está disponible GitHub CLI en este runner.") from exc


def update_metadata_file(path: Path, new_status: str) -> bool:
    if new_status not in {"draft", "review", "approved", "rejected", "published"}:
        raise ReviewStatusError("El estado solicitado no es válido.")
    try:
        metadata = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewStatusError("El metadata.json del borrador no es válido.") from exc
    if not isinstance(metadata, dict) or metadata.get("status") not in {"draft", "review", "approved", "rejected", "published"}:
        raise ReviewStatusError("El metadata.json no contiene un estado reconocido.")
    if metadata["status"] == new_status:
        return False
    metadata["status"] = new_status
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def gh_json(endpoint: str, *, runner=run) -> Any:
    response = runner(["gh", "api", endpoint])
    if response.returncode:
        raise ReviewStatusError("No se pudo leer la PR y su revisión en GitHub.")
    try:
        return json.loads(response.stdout)
    except json.JSONDecodeError as exc:
        raise ReviewStatusError("GitHub devolvió una respuesta inválida.") from exc


def sync_review(repository: str, pr_number: int, review_state: str, review_commit: str, *, runner=run) -> bool:
    new_status = status_for_review(review_state)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ReviewStatusError("Repositorio inválido.")

    pr = gh_json(f"repos/{repository}/pulls/{pr_number}", runner=runner)
    head = pr.get("head", {})
    branch = head.get("ref")
    if (
        pr.get("base", {}).get("ref") != "main"
        or not isinstance(head.get("repo"), dict)
        or head["repo"].get("full_name") != repository
        or not isinstance(branch, str)
        or not re.fullmatch(r"art-drafts/run-[0-9]+", branch)
    ):
        raise ReviewStatusError("Sólo se actualizan PRs de borrador generadas en este repositorio.")
    if not is_current_review(review_state, review_commit, pr.get("head", {}).get("sha", "")):
        print("Revisión antigua; no se aplicó al borrador actual.")
        return False

    files = gh_json(f"repos/{repository}/pulls/{pr_number}/files?per_page=100", runner=runner)
    if not isinstance(files, list):
        raise ReviewStatusError("GitHub devolvió una lista de archivos inválida.")
    paths = metadata_paths(files)

    fetch = runner(["git", "fetch", "origin", branch])
    if fetch.returncode:
        raise ReviewStatusError("No se pudo descargar la rama del borrador.")
    checkout = runner(["git", "checkout", "-B", f"art-review-{pr_number}", "FETCH_HEAD"])
    if checkout.returncode:
        raise ReviewStatusError("No se pudo abrir la rama del borrador.")

    changed = False
    for relative in paths:
        path = (ROOT / relative).resolve()
        if ROOT.resolve() not in path.parents or not path.is_file():
            raise ReviewStatusError("Falta un metadata.json esperado en la PR.")
        changed = update_metadata_file(path, new_status) or changed

    if not changed:
        print(f"El metadata del borrador ya indica {new_status}.")
        return False
    for command in (
        ["git", "config", "user.name", "github-actions[bot]"],
        ["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"],
        ["git", "add", "--", *paths],
        ["git", "commit", "-m", f"Record art review status: {new_status}"],
        ["git", "push", "origin", f"HEAD:{branch}"],
    ):
        result = runner(command)
        if result.returncode:
            raise ReviewStatusError("No se pudo guardar el estado de revisión en la PR.")
    print(f"Estado del borrador actualizado: {new_status}.")
    return True


def main() -> int:
    try:
        repository = os.environ["GITHUB_REPOSITORY"]
        pr_number = int(os.environ["VT_ART_PR_NUMBER"])
        review_state = os.environ["VT_ART_REVIEW_STATE"]
        review_commit = os.environ.get("VT_ART_REVIEW_COMMIT", "")
        sync_review(repository, pr_number, review_state, review_commit)
    except (KeyError, ValueError, ReviewStatusError) as exc:
        message = str(exc) if isinstance(exc, ReviewStatusError) else "Faltan datos válidos de la revisión."
        print(f"Error: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
