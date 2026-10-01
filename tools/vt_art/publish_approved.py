#!/usr/bin/env python3
"""Publicar imágenes aprobadas a assets/ y art-masters/.

Busca todas las generaciones con autocrítica aprobada y:
1. Convierte PNG → WebP (quality:85)
2. Publica WebP a assets/vintage-telnet/{creatures|locations}/ según asset_type
3. Genera PNG high-quality y guarda en art-masters/{creatures|locations}/

No requiere OpenAI API — solo usa Pillow local.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def find_approved_generations() -> list[tuple[str, str, str, bytes]]:
    """Encontrar todos los assets con autocrítica aprobada en ramas art-drafts.

    Returns: [(asset_id, version, asset_type, png_bytes), ...]
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

                    # Extraer asset_type de metadata (por defecto "creature" si falta)
                    asset_type = metadata.get("asset_type", "creature")
                    if asset_type == "environment":
                        asset_type = "location"

                    # Obtener PNG
                    png_path = path.replace("metadata.json", f"{asset_id}_{version}.png")
                    result = subprocess.run(
                        ["git", "show", f"origin/{branch}:{png_path}"],
                        capture_output=True,
                        cwd=ROOT,
                    )
                    if result.returncode != 0:
                        continue

                    approved.append((asset_id, version, asset_type, result.stdout))
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
    for asset_id, version, asset_type, png_bytes in approved:
        # Determinar carpeta de destino según asset_type
        if asset_type not in ("creature", "location"):
            asset_type = "creature"

        assets_dir = ROOT / "assets" / "vintage-telnet" / asset_type + "s"
        art_masters_dir = ROOT / "art-masters" / asset_type + "s"

        assets_dir.mkdir(parents=True, exist_ok=True)
        art_masters_dir.mkdir(parents=True, exist_ok=True)

        # Escribir PNG temporalmente para conversión
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(png_bytes)
            png_path = Path(tmp.name)

        try:
            # Convertir a WebP
            webp_dest = assets_dir / f"{asset_id}.webp"

            if png_to_webp(png_path, webp_dest):
                print(f"  ✅ {asset_id} {version} ({asset_type}): WebP publicado")

                # Guardar original en art-masters
                art_masters_dest = art_masters_dir / f"{asset_id}_hq.png"
                art_masters_dest.write_bytes(png_bytes)

                published += 1
            else:
                print(f"  ❌ {asset_id} {version}: Falló conversión a WebP")
        finally:
            png_path.unlink()

    if published > 0:
        print(f"\n✅ {published} imagen(es) publicada(s)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
