"""One-time interactive creation of the OAuth JSON used by the private art workflow."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from .pipeline import ROOT


def main() -> int:
    parser = argparse.ArgumentParser(description="Autoriza el pipeline de arte a guardar borradores en tu Drive.")
    parser.add_argument("client_secrets", type=Path, help="JSON OAuth de aplicación de escritorio descargado de Google Cloud.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "vintage-telnet" / "drive-oauth-user.json",
        help="Archivo local para la credencial; nunca lo subas al repositorio.",
    )
    args = parser.parse_args()
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        parser.error("Instala primero tools/vt_art/requirements-drive-auth.txt en un virtualenv.")

    flow = InstalledAppFlow.from_client_secrets_file(
        str(args.client_secrets), scopes=["https://www.googleapis.com/auth/drive"]
    )
    credentials = flow.run_local_server(host="127.0.0.1", port=0, open_browser=True, access_type="offline", prompt="consent")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(credentials.to_json() + "\n", encoding="utf-8")
    try:
        os.chmod(args.output, 0o600)
    except OSError:
        pass
    print(f"OAuth guardado de forma local en {args.output}; no se mostró su contenido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
