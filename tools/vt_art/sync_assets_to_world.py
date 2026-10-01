#!/usr/bin/env python3
"""
Sincronizar fichas de arte publicadas con VISUAL_CONTEXT_ART en world.py

Cuando se publican assets nuevos, este script:
1. Lee las fichas JSON de art_requests/
2. Busca visual_context_id en cada ficha
3. Verifica que el WebP existe en assets/vintage-telnet/
4. Genera entradas para VISUAL_CONTEXT_ART
5. Actualiza world.py si faltan entradas
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART_REQUESTS = ROOT / "vintage-telnet" / "art_requests"
ASSETS_DIR = ROOT / "assets" / "vintage-telnet"
WORLD_PY = ROOT / "vintage-telnet" / "server" / "world.py"


def get_published_assets() -> dict[str, dict]:
    """Retorna {visual_context_id: {asset_id, asset_type, ficha_data}}"""
    assets = {}

    for request_file in ART_REQUESTS.glob("*.json"):
        try:
            data = json.loads(request_file.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        visual_context_id = data.get("visual_context_id")
        asset_id = data.get("asset_id")
        asset_type = data.get("asset_type", "creature")

        if not visual_context_id or not asset_id:
            continue

        # Normalizar asset_type
        if asset_type == "environment":
            asset_type = "location"

        # Verificar que WebP existe
        webp_path = ASSETS_DIR / (asset_type + "s") / f"{asset_id}.webp"
        if not webp_path.exists():
            continue

        # Obtener dimensiones del JSON
        width = data.get("aspect_ratio", "").split("x")[0] if "x" in data.get("aspect_ratio", "") else "1536"
        height = data.get("aspect_ratio", "").split("x")[1] if "x" in data.get("aspect_ratio", "") else "1024"

        try:
            width = int(width)
            height = int(height)
        except (ValueError, IndexError):
            width, height = 1536, 1024

        assets[visual_context_id] = {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "width": width,
            "height": height,
            "canonical_name": data.get("canonical_name", asset_id),
            "ficha_path": str(request_file.relative_to(ROOT)),
        }

    return assets


def check_world_py_has_entry(visual_context_id: str) -> bool:
    """Verificar si VISUAL_CONTEXT_ART ya tiene esta entrada"""
    world_py_content = WORLD_PY.read_text()
    pattern = rf'"{re.escape(visual_context_id)}":\s*\{{'
    return bool(re.search(pattern, world_py_content))


def generate_world_py_entry(visual_context_id: str, asset_info: dict) -> str:
    """Generar una entrada VISUAL_CONTEXT_ART formateada"""
    asset_id = asset_info["asset_id"]
    asset_type = asset_info["asset_type"]
    width = asset_info["width"]
    height = asset_info["height"]
    canonical_name = asset_info["canonical_name"]

    return f'''    "{visual_context_id}": {{
        "src": "/assets/{asset_type}s/{asset_id}.webp",
        "alt": "{canonical_name}",
        "width": {width},
        "height": {height},
    }},'''


def main() -> int:
    """Verificar y reportar qué assets necesitan entradas en world.py"""
    published = get_published_assets()

    if not published:
        print("ℹ️  No hay fichas de arte con visual_context_id para sincronizar.")
        return 0

    print(f"🔍 Analizando {len(published)} asset(s) publicado(s)...\n")

    missing = {}
    for visual_context_id, asset_info in published.items():
        if not check_world_py_has_entry(visual_context_id):
            missing[visual_context_id] = asset_info
            print(f"  ⚠️  {visual_context_id}")
            print(f"     → {asset_info['asset_id']} ({asset_info['asset_type']})")

    if not missing:
        print("✅ Todos los assets ya están configurados en world.py")
        return 0

    print(f"\n❌ {len(missing)} asset(s) necesitan ser agregado(s) a VISUAL_CONTEXT_ART:\n")

    print("Agregar esto a vintage-telnet/server/world.py en VISUAL_CONTEXT_ART:")
    print("=" * 60)
    for visual_context_id, asset_info in missing.items():
        print(generate_world_py_entry(visual_context_id, asset_info))
    print("=" * 60)

    print(f"\n💡 Edita world.py manualmente o ejecuta con --fix para agregar automáticamente")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
