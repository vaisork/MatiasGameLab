"""Catálogo de armas y armaduras v1 -- GAMEPLAY.md §§30 y 32 (Issue #57).

Valores e identidad ya validados por Historiador/Jugabilidad en
`../WEAPON_CATALOG.md` y `../ARMOR_CATALOG.md`. Este módulo solo estructura
esas cifras aprobadas para que store.py/app.py las usen; no inventa objetos,
nombres ni números nuevos. Funciones puras, sin acceso a base de datos ni
Flask -- mismo principio que combat.py.
"""
import unicodedata


def _fold(text):
    """minusculas y sin acentos -- mismo criterio que app._normalize, para
    poder resolver 'equipar espada de juramento' sin depender de tildes."""
    folded = unicodedata.normalize("NFKD", (text or "").strip().lower())
    return "".join(c for c in folded if not unicodedata.combining(c))


# WEAPON_CATALOG.md, tabla "Resumen validado para implementación".
WEAPONS = {
    "varita_aprendiz": {"name": "Varita de aprendiz", "base_damage": 7,
                         "can_block": False, "forge_required": False},
    "punal_camino": {"name": "Puñal de camino", "base_damage": 8,
                      "can_block": False, "forge_required": False},
    "arco_ruta": {"name": "Arco de ruta", "base_damage": 9,
                  "can_block": False, "forge_required": False},
    "espada_juramento": {"name": "Espada de juramento", "base_damage": 10,
                          "can_block": True, "forge_required": False},
    "hoja_hoshai": {"name": "Hoja de Hoshai", "base_damage": 11,
                     "can_block": True, "forge_required": True},
    "martillo_korven": {"name": "Martillo de Korven", "base_damage": 12,
                         "can_block": True, "forge_required": True},
}

# ARMOR_CATALOG.md, tabla "Resumen para Jugabilidad". `armor_reduction` es
# la fracción decimal ya validada por Jugabilidad (0-0.35, GAMEPLAY.md 30.2).
ARMORS = {
    "acolchado_camino": {"name": "Acolchado de Camino", "armor_reduction": 0.10,
                          "forge_required": False},
    "coselete_lethra": {"name": "Coselete de Lethra", "armor_reduction": 0.10,
                         "forge_required": False},
    "malla_nhal": {"name": "Malla de Nhal", "armor_reduction": 0.10,
                    "forge_required": False},
    "lamas_hoshai": {"name": "Lamas de Hoshai", "armor_reduction": 0.20,
                      "forge_required": False},
    "cota_cinco_rutas": {"name": "Cota de las Cinco Rutas", "armor_reduction": 0.20,
                          "forge_required": False},
    "coraza_edran": {"name": "Coraza de Edran", "armor_reduction": 0.20,
                      "forge_required": False},
    "arnes_korven": {"name": "Arnés de Korven", "armor_reduction": 0.30,
                      "forge_required": True},
    "arnes_mayor_cinco_rutas": {"name": "Arnés Mayor de las Cinco Rutas", "armor_reduction": 0.35,
                                 "forge_required": True},
}

# No existe todavía ningún objeto de bloqueo puro (p. ej. escudo) en el
# catálogo del Historiador -- GAMEPLAY.md 32.2 lo deja condicionado a "si el
# contenido lo permite". Bloquear/desviar en v1 depende de si el ARMA
# equipada lo permite (columna "Bloquear/desviar" de WEAPON_CATALOG.md), no
# de una ranura de objeto de bloqueo separada; no se inventa esa ranura
# hasta que exista un objeto real que la necesite (NECESIDAD DEL HISTORIADOR
# si se quiere un escudo independiente).
ITEMS = {}
for _key, _data in WEAPONS.items():
    ITEMS[_key] = {"key": _key, "category": "weapon", "normalized_name": _fold(_data["name"]), **_data}
for _key, _data in ARMORS.items():
    ITEMS[_key] = {"key": _key, "category": "armor", "normalized_name": _fold(_data["name"]), **_data}
del _key, _data


def get_item(item_key):
    """Registro completo del catálogo para `item_key`, o None si no existe."""
    return ITEMS.get(item_key)


def category_of(item_key):
    item = ITEMS.get(item_key)
    return item["category"] if item else None


def find_key_by_name(text):
    """Busca un objeto del catálogo por su nombre en español, ignorando
    mayúsculas/tildes (para 'equipar <objeto>'/'desequipar <objeto>',
    GAMEPLAY.md 32.8). Devuelve la clave de catálogo o None."""
    normalized = _fold(text)
    if not normalized:
        return None
    for key, item in ITEMS.items():
        if item["normalized_name"] == normalized:
            return key
    return None
