#!/usr/bin/env python3
"""Publicar arte aprobado a main: PNG high → art-masters/, WebP → assets/."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run_git(cmd: str, check: bool = True) -> str:
    """Ejecutar comando git y retornar output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Git failed: {result.stderr}")
    return result.stdout.strip()


def publish_approved_art(asset_id: str, version: str) -> int:
    """Publicar PNG aprobado a main."""
    import json

    png_file = ROOT / "vintage-telnet" / "art_generations" / asset_id / version / f"{asset_id}_{version}.png"

    if not png_file.exists():
        print(f"❌ PNG no encontrado: {png_file}")
        return 1

    # Obtener asset_type de la ficha
    asset_type = "creature"
    for request_file in (ROOT / "vintage-telnet" / "art_requests").glob(f"{asset_id}*.json"):
        try:
            with open(request_file) as f:
                data = json.load(f)
                asset_type = data.get("asset_type", "creature")
                if asset_type == "environment":
                    asset_type = "location"
                break
        except (json.JSONDecodeError, OSError):
            pass

    try:
        # Usar Pillow en lugar de cwebp (no requiere instalación)
        from PIL import Image

        # Configurar git
        run_git('git config user.name "github-actions[bot]"')
        run_git('git config user.email "41898282+github-actions[bot]@users.noreply.github.com"')

        # 1. PNG high-quality → art-masters/
        art_masters_dir = ROOT / "art-masters" / (asset_type + "s")
        art_masters_dir.mkdir(parents=True, exist_ok=True)
        hq_path = art_masters_dir / f"{asset_id}_hq.png"
        shutil.copy2(png_file, hq_path)
        print(f"✅ PNG guardado: {hq_path.relative_to(ROOT)}")

        # 2. PNG → WebP → assets/
        assets_dir = ROOT / "assets" / "vintage-telnet" / (asset_type + "s")
        assets_dir.mkdir(parents=True, exist_ok=True)
        webp_path = assets_dir / f"{asset_id}.webp"

        # Convertir con Pillow
        img = Image.open(png_file)
        img.save(webp_path, "WEBP", quality=85)
        print(f"✅ WebP creado: {webp_path.relative_to(ROOT)}")

        # 3. Commitear a main
        run_git(f'git add "{hq_path.relative_to(ROOT)}" "{webp_path.relative_to(ROOT)}"')
        run_git(
            f"""git commit -m "Publish approved art: {asset_id} {version}

- PNG high-quality → art-masters/{asset_type}s/
- WebP → assets/vintage-telnet/{asset_type}s/" """
        )
        print("✅ Commit creado")

        # 4. Push a main
        run_git("git push origin HEAD:main")
        print("✅ Pusheado a main")

        return 0

    except Exception as exc:
        print(f"❌ Error: {exc}")
        import traceback
        traceback.print_exc()
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Publicar arte aprobado a main")
    parser.add_argument("asset_id", help="Asset ID (e.g., lamelon_korven)")
    parser.add_argument("version", help="Version (e.g., v002)")
    args = parser.parse_args()

    return publish_approved_art(args.asset_id, args.version)


if __name__ == "__main__":
    raise SystemExit(main())
