"""Single-generation GitHub Actions entry point with direct private Drive delivery."""
from __future__ import annotations

import json
import mimetypes
import os
import uuid
from pathlib import Path
from typing import Any

from .pipeline import ArtPipeline, ArtRequest, DEFAULT_GENERATIONS, OpenAIImageClient, ROOT


REFERENCE_FILE_ID = "1HW2UGtBk-VzCqhyBdwD9u-lcl5Fp617V"
REQUEST_PATH = ROOT / "vintage-telnet" / "art_requests" / "velozanco-edran-fase2.json"
REFERENCE_PATH = REQUEST_PATH.parent / "velozanco-edran-fase1-anatomia.png"
DRIVE_API = "https://www.googleapis.com/drive/v3/files"
DRIVE_UPLOAD_API = "https://www.googleapis.com/upload/drive/v3/files"


def _session():
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import AuthorizedSession
    except ImportError as exc:
        raise RuntimeError("Falta google-auth para conectar con Drive.") from exc
    raw = os.environ.get("VT_ART_DRIVE_OAUTH_JSON", "")
    if not raw:
        raise RuntimeError("Falta el secreto VT_ART_DRIVE_OAUTH_JSON.")
    try:
        info = json.loads(raw)
        scope = "https://www.googleapis.com/auth/drive"
        if not info.get("refresh_token"):
            raise ValueError("OAuth de usuario requiere refresh_token")
        credentials = Credentials.from_authorized_user_info(info, scopes=[scope])
    except (ValueError, KeyError) as exc:
        raise RuntimeError("El secreto de acceso a Drive no contiene credenciales válidas.") from exc
    return AuthorizedSession(credentials)


def download_reference(session: Any, path: Path = REFERENCE_PATH) -> None:
    response = session.get(
        f"{DRIVE_API}/{REFERENCE_FILE_ID}", params={"alt": "media"}, timeout=60
    )
    if response.status_code != 200:
        raise RuntimeError(f"No se pudo descargar la referencia de Drive (HTTP {response.status_code}).")
    if not response.content.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("La referencia aprobada de Drive no es un PNG válido.")
    path.write_bytes(response.content)


def upload_file(session: Any, path: Path, folder_id: str, drive_name: str | None = None) -> str:
    boundary = f"vt-art-{uuid.uuid4().hex}"
    metadata = json.dumps({"name": drive_name or path.name, "parents": [folder_id]}).encode("utf-8")
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body = (
        b"--" + boundary.encode() + b"\r\n"
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n" + metadata + b"\r\n"
        b"--" + boundary.encode() + b"\r\n"
        + f"Content-Type: {content_type}\r\n\r\n".encode()
        + path.read_bytes() + b"\r\n"
        + b"--" + boundary.encode() + b"--"
    )
    response = session.post(
        DRIVE_UPLOAD_API,
        params={"uploadType": "multipart", "fields": "id,name"},
        data=body,
        headers={"Content-Type": f"multipart/related; boundary={boundary}"},
        timeout=120,
    )
    if response.status_code not in {200, 201}:
        raise RuntimeError(f"No se pudo guardar {path.name} en Drive (HTTP {response.status_code}).")
    try:
        result = response.json()
        return str(result["id"])
    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(f"Drive no confirmó el archivo {path.name}.") from exc


def run() -> int:
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        raise RuntimeError("Falta el secreto OPENAI_API_KEY.")
    folder_id = os.environ.get("VT_ART_DRIVE_FOLDER_ID", "").strip()
    if not folder_id:
        raise RuntimeError("Falta VT_ART_DRIVE_FOLDER_ID con la carpeta destino de Drive.")
    session = _session()
    try:
        download_reference(session)
        request = ArtRequest.load(REQUEST_PATH)
        model = os.environ.get("VT_ART_MODEL", "gpt-image-2.5-flare")
        result = ArtPipeline(OpenAIImageClient(os.environ["OPENAI_API_KEY"]), model).generate(request)
        image_path = ROOT / result["image"]
        version_dir = image_path.parent
        files = (
            (image_path, image_path.name),
            (version_dir / "metadata.json", f"{request.asset_id}_{result['version']}_metadata.json"),
            (REQUEST_PATH, f"{request.asset_id}_{result['version']}_request.json"),
        )
        uploaded = [(name, upload_file(session, path, folder_id, name)) for path, name in files]
        print(f"Generación terminada: {request.asset_id} {result['version']} (draft).")
        for name, file_id in uploaded:
            print(f"Guardado en Drive: {name} (id {file_id}).")
        print("La imagen sigue siendo borrador; no se aprobó, publicó ni integró al juego.")
        return 0
    finally:
        REFERENCE_PATH.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except Exception as exc:
        # Never echo exception payloads: provider errors can carry request content.
        print(f"Fallo del piloto: {type(exc).__name__}.", file=__import__("sys").stderr)
        raise SystemExit(1)
