#!/usr/bin/env python3
"""
Actualizar fichas de arte con visual_context_id automáticamente.

Solo actualiza fichas que se pueden mapear con confianza.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART_REQUESTS = ROOT / "vintage-telnet" / "art_requests"

# Mapeos confirmados (nombre_ficha → visual_context_id)
CONFIRMED_MAPPINGS = {
    "claro-cielo-estrecho-nhal-hoshai": "zone.nhal.claro_cielo_estrecho",
    "garganta-lajas-hoshai-korven": "zone.hoshai.garganta_lajas",
    "brumak-patio-recepcion": "zone.brumak.patio_recepcion",
    "khariel-terraza-comunitaria": "zone.khariel.terraza_comunitaria",
    "velmora-cruce-reunion": "zone.velmora.cruce_reunion",
    "primeros-juncos-edran-lethra": "zone.edran.primeros_juncos",
    "pinzajunco-lethra": "zone.lethra",
    "canal-quieto": "zone.lethra.canal_bajo_islas",
    "saltacresta-hoshai": "zone.hoshai",
    "cornisa-ciega": "zone.hoshai",
    "rasgacumbres-hoshai": "zone.hoshai",
    "escaleras-rotas": "zone.korven",
    "colagrieta-korven": "zone.korven",
    "quebrarrocas-korven": "zone.korven",
    "tres-marcas-korven-edran": "zone.korven",
    "marca-nhal": "zone.nhal",
    "sendero-copas": "zone.nhal",
    "sendero-sin-marca": "zone.nhal",
    "claro-niebla-baja": "zone.nhal",
    "dorsalodo-lethra": "zone.lethra",
}


def update_ficha(ficha_path: Path, visual_context_id: str) -> bool:
    """Actualizar una ficha JSON con visual_context_id"""
    try:
        data = json.loads(ficha_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False

    # No sobrescribir si ya tiene visual_context_id
    if data.get("visual_context_id"):
        return False

    data["visual_context_id"] = visual_context_id

    # Reescribir JSON con indentación
    ficha_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    return True


def main() -> int:
    """Aplicar mapeos a fichas"""
    updated = 0
    skipped = 0

    for ficha_name, visual_context_id in CONFIRMED_MAPPINGS.items():
        ficha_path = ART_REQUESTS / f"{ficha_name}.json"

        if not ficha_path.exists():
            print(f"  ⚠️  {ficha_name}.json no encontrado")
            continue

        if update_ficha(ficha_path, visual_context_id):
            print(f"  ✅ {ficha_name} → {visual_context_id}")
            updated += 1
        else:
            print(f"  ⊘ {ficha_name} (ya tiene visual_context_id o error)")
            skipped += 1

    print(f"\n✅ Actualizadas {updated} ficha(s)")
    if skipped:
        print(f"⊘ Saltadas {skipped} ficha(s)")

    print("\n⚠️  Las siguientes fichas NO tienen mapeo automático:")
    print("   (necesitan revision manual en art_requests/)")
    unmapped = [
        "alto-raices", "boca-montana", "borde-cardos", "campos-bajos",
        "cantera-abandonada", "charcos-negros", "cruce-carro-viejo",
        "cuenca-polvo-quieto", "embarcadero-ultimo-claro", "grieta-eco-seco",
        "mirador-dos-piedras", "molino-hundido", "orilla-partida",
        "orilla-velada", "parada-cardos", "pendiente-raices-altas",
        "piedra-hundida", "piedra-resguardo", "piedra-viento-verde",
        "puente-madera-ancha", "raices-del-agua", "refugio-de-lajas",
        "terraza-bosque-alto", "vado-de-juncos"
    ]
    for name in sorted(unmapped):
        print(f"   • {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
