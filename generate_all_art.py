#!/usr/bin/env python3
"""
Generador de arte local para Vintage Telnet.
Crea dos carpetas: generated-hq/ (PNG) y generated-webp/ (WebP comprimido).
Ejecutar: python3 generate_all_art.py
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART_REQUESTS_DIR = ROOT / "vintage-telnet" / "art_requests"
OUTPUT_HQ_DIR = ROOT / "generated-hq"
OUTPUT_WEBP_DIR = ROOT / "generated-webp"

# Crear carpetas si no existen
for subdir in ["creatures", "locations"]:
    (OUTPUT_HQ_DIR / subdir).mkdir(parents=True, exist_ok=True)
    (OUTPUT_WEBP_DIR / subdir).mkdir(parents=True, exist_ok=True)

def main():
    print("=" * 60)
    print("🎨 Generador de Arte — Vintage Telnet")
    print("=" * 60)
    print()

    # Listar fichas disponibles
    fichas = sorted([f for f in ART_REQUESTS_DIR.glob("*.json") if f.name != "template.json"])

    if not fichas:
        print("❌ No hay fichas de arte para generar.")
        return 1

    print(f"📋 Fichas encontradas: {len(fichas)}")
    for i, ficha in enumerate(fichas, 1):
        print(f"  {i}) {ficha.name}")

    print()
    print("Opción: T para generar todas, <número> para seleccionar, 0 para cancelar")
    choice = input("Elige: ").strip()

    if choice == "0":
        print("❌ Cancelado.")
        return 0

    if choice.upper() == "T":
        selected = fichas
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(fichas):
                selected = [fichas[idx]]
            else:
                print("❌ Opción inválida.")
                return 1
        except ValueError:
            print("❌ Entrada inválida.")
            return 1

    print()
    print(f"✅ Generando {len(selected)} ficha(s)...")
    print()

    # Generar cada ficha usando el pipeline
    generated_assets = []
    for ficha_path in selected:
        asset_name = ficha_path.stem
        print(f"🔄 Generando {asset_name}...")

        try:
            # Usar el pipeline del proyecto
            from tools.vt_art.pipeline import ArtRequest, generate_with_critique
            from tools.vt_art.critique import OpenAIVisionCritic

            request = ArtRequest.load(ficha_path)
            critic = OpenAIVisionCritic(api_key=os.getenv("OPENAI_API_KEY"))

            # Generar con crítica automática (máx 4 intentos)
            result = generate_with_critique(
                request=request,
                critic=critic,
                critic_model="gpt-5-mini",
                max_attempts=4
            )

            # Determinar subdirectorio según asset_type
            subdir = "locations" if request.asset_type == "architecture" else "creatures"

            # Guardar PNG high-quality
            hq_path = OUTPUT_HQ_DIR / subdir / f"{request.asset_id}_hq.png"
            hq_path.write_bytes(result.image_bytes)
            print(f"  ✅ PNG: {subdir}/{hq_path.name}")

            # Convertir a WebP
            webp_path = OUTPUT_WEBP_DIR / subdir / f"{request.asset_id}.webp"
            convert_to_webp(hq_path, webp_path)
            print(f"  ✅ WebP: {subdir}/{webp_path.name}")

            generated_assets.append({
                "asset_id": request.asset_id,
                "hq": str(hq_path.relative_to(ROOT)),
                "webp": str(webp_path.relative_to(ROOT)),
                "verdict": result.critique.get("passes", False) if result.critique else None,
            })

            print()

        except Exception as e:
            print(f"  ❌ Error: {e}")
            print()
            continue

    # Resumen
    print("=" * 60)
    print("📊 Resumen")
    print("=" * 60)
    print(f"✅ Generadas: {len(generated_assets)}")
    print(f"📁 HQ (PNG): {OUTPUT_HQ_DIR.name}/")
    print(f"📁 WebP: {OUTPUT_WEBP_DIR.name}/")
    print()

    if generated_assets:
        print("Assets generados:")
        for asset in generated_assets:
            verdict = "✅ APROBADO" if asset["verdict"] else "⚠️ NECESITA REVISIÓN" if asset["verdict"] is False else "ℹ️ SIN CRÍTICA"
            print(f"  - {asset['asset_id']}: {verdict}")

    print()
    print("💡 Siguiente: sube las carpetas a GitHub")
    print()

    return 0


def convert_to_webp(png_path: Path, webp_path: Path, quality: int = 85):
    """Convertir PNG a WebP con cwebp."""
    try:
        from PIL import Image
        img = Image.open(png_path)
        img.save(str(webp_path), "WebP", quality=quality)
    except ImportError:
        # Fallback a cwebp CLI
        result = subprocess.run(
            ["cwebp", "-q", str(quality), str(png_path), "-o", str(webp_path)],
            capture_output=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"cwebp failed: {result.stderr.decode()}")


if __name__ == "__main__":
    sys.exit(main())
