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

# Detectar raíz del proyecto buscando hacia arriba
def find_project_root(start_path: Path = None) -> Path:
    """Buscar raíz del proyecto detectando vintage-telnet/"""
    if start_path is None:
        start_path = Path(__file__).resolve().parent

    current = start_path
    while current != current.parent:
        if (current / "vintage-telnet").exists():
            return current
        current = current.parent

    # Fallback si no encuentra
    return start_path

ROOT = find_project_root()
ART_REQUESTS_DIR = ROOT / "vintage-telnet" / "art_requests"
ART_MASTERS_DIR = ROOT / "art-masters"  # PNG high-quality respaldo
ASSETS_DIR = ROOT / "assets" / "vintage-telnet"  # WebP para el servidor

# Crear carpetas si no existen
for subdir in ["creatures", "locations"]:
    (ART_MASTERS_DIR / subdir).mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / subdir).mkdir(parents=True, exist_ok=True)

def main():
    print("=" * 60)
    print("🎨 Generador de Arte — Vintage Telnet")
    print("=" * 60)
    print()

    # Listar fichas disponibles (excluir template y las ya generadas)
    generated_assets = set()
    for webp in ASSETS_DIR.glob("*/*.webp"):
        # Extraer asset_id del nombre del archivo (ej: narevia_mercado_acuatico.webp -> narevia_mercado_acuatico)
        generated_assets.add(webp.stem)

    fichas = sorted([
        f for f in ART_REQUESTS_DIR.glob("*.json")
        if f.name != "template.json" and f.stem not in generated_assets
    ])

    if not fichas:
        print("❌ No hay fichas de arte para generar.")
        return 1

    print(f"📋 Fichas encontradas: {len(fichas)}")
    for i, ficha in enumerate(fichas, 1):
        print(f"  {i}) {ficha.name}")

    print()
    print("Opción: T/Todas para todas, <números> (ej: 1,2,3 o 1 2 3), 0 para cancelar")
    choice = input("Elige: ").strip()

    if choice == "0":
        print("❌ Cancelado.")
        return 0

    if choice.upper() in ("T", "TODAS"):
        selected = fichas
    else:
        # Aceptar múltiples números separados por comas o espacios
        import re
        numbers = re.findall(r'\d+', choice)
        if not numbers:
            print("❌ Entrada inválida.")
            return 1

        selected = []
        for num_str in numbers:
            try:
                idx = int(num_str) - 1
                if 0 <= idx < len(fichas):
                    selected.append(fichas[idx])
                else:
                    print(f"❌ Opción {num_str} inválida.")
                    return 1
            except ValueError:
                print("❌ Entrada inválida.")
                return 1

        if not selected:
            print("❌ No se seleccionaron fichas.")
            return 1

    print()
    confirmation = input("Escribe GEN para continuar: ").strip()
    if confirmation.upper() != "GEN":
        print("❌ Cancelado.")
        return 0

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
            from tools.vt_art.pipeline import ArtRequest, ArtPipeline, OpenAIImageClient
            from tools.vt_art.critique import OpenAIVisionCritic

            # Cargar con ruta absoluta del proyecto
            request = ArtRequest.load(ficha_path, project_root=ROOT)

            # Crear pipeline y crítico
            api_key = os.getenv("OPENAI_API_KEY")
            pipeline = ArtPipeline(OpenAIImageClient(api_key), "gpt-image-2.5-flare")
            critic = OpenAIVisionCritic(api_key=api_key)

            # Generar con crítica automática (máx 4 intentos)
            result = pipeline.generate_with_critique(
                request=request,
                critic=critic,
                critic_model="gpt-5-mini",
                max_attempts=4
            )

            # Determinar subdirectorio según asset_type
            subdir = "locations" if request.asset_type == "architecture" else "creatures"

            # El resultado es un dict con la ruta de imagen relativa a ROOT
            image_rel_path = result.get("image", "")
            if not image_rel_path:
                raise ValueError("El pipeline no devolvió una ruta de imagen.")

            image_path = ROOT / image_rel_path
            if not image_path.exists():
                raise FileNotFoundError(f"No existe la imagen generada: {image_path}")

            # Guardar PNG high-quality en art-masters (respaldo)
            hq_path = ART_MASTERS_DIR / subdir / f"{request.asset_id}_hq.png"
            hq_path.write_bytes(image_path.read_bytes())
            print(f"  ✅ PNG: art-masters/{subdir}/{hq_path.name}")

            # Convertir a WebP y guardar en assets/ (lo que usa el servidor)
            webp_path = ASSETS_DIR / subdir / f"{request.asset_id}.webp"
            convert_to_webp(hq_path, webp_path)
            print(f"  ✅ WebP: assets/vintage-telnet/{subdir}/{webp_path.name}")

            critique = result.get("critique")
            generated_assets.append({
                "asset_id": request.asset_id,
                "hq": str(hq_path.relative_to(ROOT)),
                "webp": str(webp_path.relative_to(ROOT)),
                "verdict": critique.get("passes", False) if critique else None,
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
    print(f"📁 PNG (respaldo): art-masters/creatures/ y art-masters/locations/")
    print(f"📁 WebP (servidor): assets/vintage-telnet/creatures/ y assets/vintage-telnet/locations/")
    print()

    if generated_assets:
        print("Assets generados:")
        for asset in generated_assets:
            verdict = "✅ APROBADO" if asset["verdict"] else "⚠️ NECESITA REVISIÓN" if asset["verdict"] is False else "ℹ️ SIN CRÍTICA"
            print(f"  - {asset['asset_id']}: {verdict}")

    print()
    print("💡 Próximo: los WebP están listos en assets/ para el servidor")
    print("💡 PNG respaldo guardados en art-masters/")
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
    try:
        sys.exit(main())
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ ERROR CRÍTICO: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        print()
        input("Presiona Enter para cerrar...")
        sys.exit(1)
