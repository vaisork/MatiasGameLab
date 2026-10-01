#!/usr/bin/env python3
"""
Auto-mapear fichas de arte a visual_context_id basándose en nombres.

Usa patrones en los nombres de las fichas para determinar a qué zona pertenecen.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
ART_REQUESTS = ROOT / "vintage-telnet" / "art_requests"
WORLD_PY = ROOT / "vintage-telnet" / "server" / "world.py"

# Mapeos explícitos de nombre_ficha → visual_context_id
EXPLICIT_MAPPING = {
    "claro-cielo-estrecho-nhal-hoshai": "zone.nhal.claro_cielo_estrecho",
    "claro-niebla-baja": "zone.nhal",  # Genérico de Nhal si no hay más específico
    "garganta-lajas-hoshai-korven": "zone.hoshai.garganta_lajas",
    "brumak-patio-recepcion": "zone.brumak.patio_recepcion",
    "khariel-terraza-comunitaria": "zone.khariel.terraza_comunitaria",
    "narevia-mercado-acuatico": "zone.narevia.mercado_acuatico",
    "valdren-forja-daro": "zone.valdren.forja_daro",
    "velmora-forja-taller": "zone.velmora.forja_taller",
    "velmora-cruce-reunion": "zone.velmora.cruce_reunion",
    "primeros-juncos-edran-lethra": "zone.edran.primeros_juncos",
    "pinzajunco-lethra": "zone.lethra",  # Genérico si no hay específico
    "canal-quieto": "zone.lethra.canal_bajo_islas",
    "saltacresta-hoshai": "zone.hoshai",
    "cornisa-ciega": "zone.hoshai",
    "rasgacumbres-hoshai": "zone.hoshai",
    "escaleras-rotas": "zone.korven",
    "colagrieta-korven": "zone.korven",
    "quebrarrocas-korven": "zone.korven",
    "tres-marcas-korven-edran": "zone.korven",
    "mark-nhal": "zone.nhal",
    "marca-nhal": "zone.nhal",
    "sendero-copas": "zone.nhal",
    "sendero-sin-marca": "zone.nhal",
}

# Mapeos por región basados en palabras clave en el nombre
REGION_KEYWORDS = {
    "hoshai": ("zone.hoshai", 100),
    "korven": ("zone.korven", 100),
    "nhal": ("zone.nhal", 100),
    "khariel": ("zone.khariel", 100),
    "valdren": ("zone.valdren", 100),
    "velmora": ("zone.velmora", 100),
    "narevia": ("zone.narevia", 100),
    "edran": ("zone.edran", 100),
    "lethra": ("zone.lethra", 100),
    "veyra": ("zone.veyra", 100),
    "brumak": ("zone.brumak", 100),
}


def get_available_zones() -> set[str]:
    """Obtener todos los visual_context_id disponibles de world.py"""
    content = WORLD_PY.read_text()
    zones = set(re.findall(r'"(zone\.[^"]+)"', content))
    return zones


def map_ficha_to_zone(ficha_name: str) -> str | None:
    """Mapear nombre de ficha a visual_context_id"""
    # 1. Revisar mapeo explícito
    if ficha_name in EXPLICIT_MAPPING:
        return EXPLICIT_MAPPING[ficha_name]

    # 2. Buscar por keywords de región
    normalized_name = ficha_name.lower().replace("-", " ")
    matches = []

    for keyword, (zone, score) in REGION_KEYWORDS.items():
        if keyword in normalized_name:
            matches.append((score, zone))

    if matches:
        matches.sort(reverse=True)
        return matches[0][1]

    return None


def main() -> int:
    """Analizar y mapear fichas de arte"""
    available_zones = get_available_zones()
    print(f"🗺️  Zonas disponibles en world.py: {len(available_zones)}\n")

    unmapped = []
    mapped = defaultdict(list)

    for ficha in sorted(ART_REQUESTS.glob("*.json")):
        if ficha.name == "template.json":
            continue

        ficha_name = ficha.stem
        zone = map_ficha_to_zone(ficha_name)

        try:
            data = json.loads(ficha.read_text())
            current_visual_context = data.get("visual_context_id")
        except (json.JSONDecodeError, OSError):
            continue

        if current_visual_context:
            # Ya tiene visual_context_id
            print(f"  ✅ {ficha_name}: {current_visual_context}")
            mapped[zone].append(ficha_name)
        elif zone:
            # Tenemos una propuesta
            print(f"  ⚠️  {ficha_name}")
            print(f"     → Propuesta: {zone}")
            mapped[zone].append(ficha_name)
            unmapped.append((ficha_name, zone))
        else:
            # No podemos mapear
            print(f"  ❌ {ficha_name}: no se puede mapear automáticamente")
            unmapped.append((ficha_name, None))

    if unmapped:
        print(f"\n⚠️  {len(unmapped)} ficha(s) necesitan revisión:\n")
        for ficha_name, proposed_zone in unmapped:
            if proposed_zone:
                print(f"   • {ficha_name} → {proposed_zone} (revisar)")
            else:
                print(f"   • {ficha_name} → ??? (revisar manualmente)")

        print("\nEjecuta con --apply para actualizar las fichas automáticamente.")
    else:
        print("\n✅ Todas las fichas están mapeadas.")

    return 1 if unmapped else 0


if __name__ == "__main__":
    raise SystemExit(main())
