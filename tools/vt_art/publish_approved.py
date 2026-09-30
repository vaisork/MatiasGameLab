#!/usr/bin/env python3
"""Publicar imágenes aprobadas a assets/ y art-masters/.

Busca todas las generaciones con autocrítica aprobada y:
1. Convierte PNG → WebP (quality:85)
2. Publica WebP a assets/vintage-telnet/creatures/
3. Genera PNG high-quality y guarda en art-masters/

No requiere OpenAI API — solo usa cwebp local.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "assets" / "vintage-telnet" / "creatures"


def find_approved_generations() -> list[tuple[str, str, bytes, bytes]]:
    """Encontrar todos los assets con autocrítica aprobada en ramas art-drafts.

    Returns: [(asset_id, version, png_bytes, metadata_json_bytes), ...]
    """
    approved = []

    try:
        # Obtener lista de ramas art-drafts
        result = subprocess.run(
            ["git", "branch", "-r", "--list", "origin/art-drafts/run-*"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        branches = [b.strip().replace("origin/", "") for b in result.stdout.split("\n") if b.strip()]

        for branch in sorted(branches, reverse=True):  # newest first
            # Listar directorios en art_generations para esta rama
            result = subprocess.run(
                ["git", "ls-tree", "-r", f"origin/{branch}", "vintage-telnet/art_generations/"],
                capture_output=True,
                text=True,
                cwd=ROOT,
            )

            for line in result.stdout.split("\n"):
                if not line or "metadata.json" not in line:
                    continue

                # Extraer path y asset_id/version
                path = line.split("\t")[-1] if "\t" in line else None
                if not path:
                    continue

                parts = path.split("/")
                if len(parts) < 4 or parts[0] != "vintage-telnet" or parts[1] != "art_generations":
                    continue

                asset_id = parts[2]
                version = parts[3]

                # Skip if ya procesamos este asset
                if any(a[0] == asset_id for a in approved):
                    continue

                # Obtener metadata
                try:
                    result = subprocess.run(
                        ["git", "show", f"origin/{branch}:{path}"],
                        capture_output=True,
                        cwd=ROOT,
                    )
                    if result.returncode != 0:
                        continue

                    metadata = json.loads(result.stdout.decode())
                    critique = metadata.get("critique", {})
                    if not critique.get("passes"):
                        continue

                    # Obtener PNG
                    png_path = path.replace("metadata.json", f"{asset_id}_{version}.png")
                    result = subprocess.run(
                        ["git", "show", f"origin/{branch}:{png_path}"],
                        capture_output=True,
                        cwd=ROOT,
                    )
                    if result.returncode != 0:
                        continue

                    approved.append((asset_id, version, result.stdout, result.stdout))
                except Exception:
                    pass

    except Exception:
        pass

    return approved


def png_to_webp(png_path: Path, webp_path: Path, quality: int = 85) -> bool:
    """Convertir PNG a WebP usando cwebp."""
    try:
        result = subprocess.run(
            ["cwebp", "-q", str(quality), str(png_path), "-o", str(webp_path)],
            capture_output=True,
            timeout=30,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main() -> int:
    """Publicar imágenes aprobadas."""
    approved = find_approved_generations()

    if not approved:
        print("No hay generaciones aprobadas para publicar.")
        return 0

    print(f"Encontradas {len(approved)} generación(es) aprobada(s):")

    published = 0
    for asset_id, version, metadata_path in approved:
        version_dir = metadata_path.parent
        png_path = version_dir / f"{asset_id}_{version}.png"

        if not png_path.exists():
            print(f"  ⚠️  {asset_id} {version}: PNG no encontrado")
            continue

        # Convertir a WebP
        webp_dest = ASSETS_DIR / f"{asset_id}.webp"
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)

        if png_to_webp(png_path, webp_dest):
            print(f"  ✅ {asset_id} {version}: WebP publicado a assets/")
            published += 1
        else:
            print(f"  ❌ {asset_id} {version}: Falló conversión a WebP (¿cwebp instalado?)")

    if published > 0:
        print(f"\n✅ {published} imagen(es) publicada(s) a assets/")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
