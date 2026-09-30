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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATIONS_DIR = ROOT / "vintage-telnet" / "art_generations"
ASSETS_DIR = ROOT / "assets" / "vintage-telnet" / "creatures"


def find_approved_generations() -> list[tuple[str, str, Path]]:
    """Encontrar todos los assets con autocrítica aprobada.

    Returns: [(asset_id, version, metadata_path), ...]
    """
    approved = []
    for asset_dir in GENERATIONS_DIR.iterdir():
        if not asset_dir.is_dir():
            continue
        asset_id = asset_dir.name

        for version_dir in sorted(asset_dir.iterdir()):
            if not version_dir.is_dir():
                continue
            version = version_dir.name

            metadata_path = version_dir / "metadata.json"
            if not metadata_path.exists():
                continue

            try:
                data = json.loads(metadata_path.read_text(encoding="utf-8"))
                critique = data.get("critique", {})
                if critique.get("passes"):
                    approved.append((asset_id, version, metadata_path))
            except (OSError, json.JSONDecodeError):
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
