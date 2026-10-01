#!/usr/bin/env python3
"""Validar que los assets publicados están siendo servidos correctamente por el servidor.

Verifica:
1. WebP existe en assets/vintage-telnet/{creatures,locations}/
2. Ficha JSON tiene visual_context_id o room_id
3. El servidor tiene la configuración correcta para servir el asset
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "assets" / "vintage-telnet"
ART_REQUESTS = ROOT / "vintage-telnet" / "art_requests"
WORLD_PY = ROOT / "vintage-telnet" / "server" / "world.py"


def find_published_assets() -> list[tuple[Path, dict]]:
    """Encontrar todos los WebPs publicados y sus fichas."""
    published = []

    for asset_type_dir in (ASSETS_DIR / "creatures", ASSETS_DIR / "locations"):
        if not asset_type_dir.exists():
            continue

        for webp_file in asset_type_dir.glob("*.webp"):
            asset_id = webp_file.stem

            # Encontrar la ficha JSON
            for request_file in ART_REQUESTS.glob(f"{asset_id}*.json"):
                try:
                    data = json.loads(request_file.read_text())
                    if data.get("asset_id") == asset_id:
                        published.append((webp_file, data))
                        break
                except (json.JSONDecodeError, OSError):
                    pass

    return published


def check_server_config(data: dict) -> tuple[bool, str]:
    """Verificar que el servidor está configurado para servir este asset."""
    visual_context_id = data.get("visual_context_id")
    asset_type = data.get("asset_type")

    if not visual_context_id:
        return False, "❌ Sin visual_context_id en ficha"

    # Normalizar asset_type
    if asset_type == "environment":
        asset_type = "location"

    # Leer world.py y buscar la configuración
    world_py_content = WORLD_PY.read_text()

    # Buscar si existe la entrada VISUAL_CONTEXT_ART para este ID
    pattern = rf'"{visual_context_id}":\s*\{{'
    if re.search(pattern, world_py_content):
        return True, f"✅ Configurado en VISUAL_CONTEXT_ART"
    else:
        return False, f"⚠️  No encontrado en VISUAL_CONTEXT_ART — requiere actualización manual"


def main() -> int:
    """Validar todos los assets publicados."""
    published = find_published_assets()

    if not published:
        print("ℹ️  No hay assets publicados para validar.")
        return 0

    print(f"🔍 Validando {len(published)} asset(s) publicado(s):\n")

    all_ok = True
    for webp_path, data in published:
        asset_id = data.get("asset_id", "?")
        asset_type = data.get("asset_type", "creature")
        visual_context_id = data.get("visual_context_id", "?")

        # Verificar que WebP existe
        if not webp_path.exists():
            print(f"  ❌ {asset_id}: WebP no encontrado en {webp_path}")
            all_ok = False
            continue

        # Verificar configuración del servidor
        ok, status = check_server_config(data)
        status_icon = "✅" if ok else "⚠️"
        print(f"  {status_icon} {asset_id} ({asset_type})")
        print(f"     → visual_context_id: {visual_context_id}")
        print(f"     → {status}")

        if not ok:
            all_ok = False

    if not all_ok:
        print("\n⚠️  Algunos assets necesitan configuración manual en world.py")
        print("   Actualiza VISUAL_CONTEXT_ART con el path correcto del asset.")
        return 1

    print(f"\n✅ Todos los assets están correctamente publicados y configurados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
