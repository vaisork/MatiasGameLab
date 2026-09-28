"""Motor de población ambiental N0 (GAMEPLAY §39.6-39.10, WORLD_POPULATION_NARRATIVE.md).

Proporciona presencia de fondo no hostil, no conversacional (sin LLM) y efímera (sin DB).
Características clave:
- Fase temporal compartida: population_epoch = floor(unix_time / 900) (epochs de 15 minutos).
- Densidad determinista por perfiles: none (0%), sparse (15%), normal (30%), busy (55%), hub (75%).
- Máximo 1 presencia N0 por sala (los NPCs scripted tienen prioridad y no son sustituidos).
- Cero almacenamiento en base de datos; determinismo puro por epoch + room_id + role_table.
- Barks y respuestas predefinidas según WORLD_POPULATION_NARRATIVE.md.
- Ocultación automática durante combate activo.
"""

from __future__ import annotations

import hashlib
import math
import time
from typing import Any, Dict, List, Optional

# Ventana temporal de fase compartida (15 minutos reales = 900 segundos)
POPULATION_EPOCH_SECONDS: int = 900

# Perfiles canónicos de probabilidad (GAMEPLAY §39.7)
DENSITY_PROFILES: Dict[str, float] = {
    "population_none": 0.0,
    "none": 0.0,
    "population_sparse": 0.15,
    "sparse": 0.15,
    "population_normal": 0.30,
    "normal": 0.30,
    "population_busy": 0.55,
    "busy": 0.55,
    "population_hub": 0.75,
    "hub": 0.75,
}

# Definiciones canónicas de voces y respuestas N0 (WORLD_POPULATION_NARRATIVE.md)
CANONICAL_N0_DATA: Dict[str, Dict[str, Any]] = {
    "habitante": {
        "role_id": "habitante",
        "label": "Habitante",
        "barks": [
            "Buen camino.",
            "Hoy hay más movimiento de lo normal.",
            "Si buscas pasar, deja libre el centro.",
            "Todavía queda día para ir y volver.",
        ],
        "reply": "No necesito nada, gracias. Solo estoy siguiendo con mi día.",
        "regions": [],
        "room_tags": [],
        "exclusions": [],
    },
    "trabajador": {
        "role_id": "trabajador",
        "label": "Trabajador",
        "barks": [
            "Un momento; termino esto y dejo libre el paso.",
            "Siempre aparece algo que reparar.",
            "Mejor hacerlo bien una vez.",
            "Por aquí pasa más gente de la que parece.",
        ],
        "reply": "Estoy trabajando. Puedes pasar, solo ten cuidado por dónde pisas.",
        "regions": [],
        "room_tags": [],
        "exclusions": [],
    },
    "cargador": {
        "role_id": "cargador",
        "label": "Cargador",
        "barks": [
            "Despacio. Esto pesa más de lo que parece.",
            "Déjame sitio y en un momento queda libre.",
            "Lo difícil no es cargarlo; es llevarlo sin estorbar a todos.",
            "Ya casi llego.",
        ],
        "reply": "Voy de paso con la carga. No hay ningún encargo.",
        "regions": [],
        "room_tags": [],
        "exclusions": [],
    },
    "viajero": {
        "role_id": "viajero",
        "label": "Viajero",
        "barks": [
            "Aún me queda camino.",
            "Vengo de más lejos de lo que parece.",
            "Conviene mirar bien antes de dejar atrás un cruce.",
            "Hoy prefiero avanzar mientras haya buena visibilidad.",
            "Nos veremos en otro tramo, quizá.",
        ],
        "reply": "Solo estoy de camino. Que tengas buen viaje.",
        "regions": [],
        "room_tags": [],
        "exclusions": [],
    },
    "recolector": {
        "role_id": "recolector",
        "label": "Recolector",
        "barks": [
            "Aquí todavía se encuentra algo si sabes mirar.",
            "No hace falta llevarse todo lo que uno ve.",
            "Estoy terminando por esta zona.",
            "El terreno cambia mucho de un tramo a otro.",
        ],
        "reply": "Solo recojo lo habitual de la zona. No estoy buscando ayuda.",
        "regions": [],
        "room_tags": [],
        "exclusions": [],
    },
}

# Tabla de roles activos en el runtime del mundo.
# Por diseño (Issue #380 / regla de entrega):
# Comienza vacía por defecto para no poblar salas de producción hasta que
# Historia entregue su tabla canónica de asignaciones por sala/región.
_ACTIVE_ROLES: List[Dict[str, Any]] = []


def get_registered_roles() -> List[Dict[str, Any]]:
    """Devuelve copia de la lista de roles registrados actualmente."""
    return [dict(r) for r in _ACTIVE_ROLES]


def set_registered_roles(roles: List[Dict[str, Any]]) -> None:
    """Reemplaza la lista de roles registrados."""
    global _ACTIVE_ROLES
    _ACTIVE_ROLES = [dict(r) for r in roles]


def register_role(role_dict: Dict[str, Any]) -> None:
    """Registra una definición de rol N0 adicional."""
    _ACTIVE_ROLES.append(dict(role_dict))


def clear_roles() -> None:
    """Limpia los roles registrados (útil para pruebas o reseteo)."""
    global _ACTIVE_ROLES
    _ACTIVE_ROLES = []


def reset_roles() -> None:
    """Alias para clear_roles."""
    clear_roles()


def load_canonical_roles() -> None:
    """Carga los 5 roles canónicos de WORLD_POPULATION_NARRATIVE.md en el registro activo."""
    set_registered_roles(list(CANONICAL_N0_DATA.values()))


def get_current_time() -> float:
    """Devuelve el timestamp unix actual; punto desacoplado para pruebas."""
    return time.time()


def get_population_epoch(timestamp: Optional[float] = None) -> int:
    """Calcula la época temporal compartida según GAMEPLAY §39.8:
    population_epoch = floor(unix_time / 900)
    (ventanas sincronizadas de 15 minutos reales)."""
    if timestamp is None:
        timestamp = get_current_time()
    return int(math.floor(timestamp / POPULATION_EPOCH_SECONDS))


def _is_role_eligible(role: Dict[str, Any], room_id: str, room_data: Optional[Dict[str, Any]]) -> bool:
    """Verifica si un rol es admisible en una sala considerando regiones, tags y exclusiones."""
    data = room_data or {}

    # Exclusiones específicas de sala o tags
    exclusions = role.get("exclusions") or []
    if room_id in exclusions:
        return False
    room_tags = data.get("tags") or []
    if any(tag in exclusions for tag in room_tags):
        return False

    # Filtro por regiones si el rol define regiones permitidas
    role_regions = role.get("regions") or []
    if role_regions:
        room_region = data.get("region")
        if not room_region:
            for r in role_regions:
                if room_id.startswith(f"{r}_") or room_id == r:
                    room_region = r
                    break
        if room_region not in role_regions:
            return False

    # Filtro por room_tags requeridos
    required_tags = role.get("room_tags") or []
    if required_tags:
        if not all(tag in room_tags for tag in required_tags):
            return False

    return True


def get_room_n0_presence(
    room_id: str,
    timestamp: Optional[float] = None,
    room_data: Optional[Dict[str, Any]] = None,
    profile: Optional[str] = None,
    role_table: Optional[List[Dict[str, Any]]] = None,
) -> Optional[Dict[str, Any]]:
    """Calcula de forma determinista y efímera la presencia N0 en una sala.

    Reglas de GAMEPLAY §39.6-39.10:
    - 0 DB mutations: no persiste estado en SQLite ni en memoria persistente.
    - Determinismo estricto: mismo epoch + room_id + role_table -> mismo resultado.
    - Máximo 1 presencia N0 por sala.
    - Retorna None si no hay roles elegibles, si la sala tiene densidad none (0%),
      o si el roll probabilístico no supera el umbral del perfil.
    """
    roles = role_table if role_table is not None else _ACTIVE_ROLES
    if not roles:
        return None

    density_profile = profile
    if density_profile is None and room_data:
        density_profile = room_data.get("population_profile")
    if density_profile is None:
        return None

    prob = DENSITY_PROFILES.get(density_profile, 0.0)
    if prob <= 0.0:
        return None

    epoch = get_population_epoch(timestamp)

    # Semilla determinista SHA-256
    seed = f"n0:{epoch}:{room_id}".encode("utf-8")
    digest = hashlib.sha256(seed).digest()

    # Roll uniforme en [0.0, 1.0)
    roll = int.from_bytes(digest[0:4], byteorder="big") / 0xFFFFFFFF
    if roll >= prob:
        return None

    # Filtrado de roles elegibles
    eligible_roles = [r for r in roles if _is_role_eligible(r, room_id, room_data)]
    if not eligible_roles:
        return None

    # Selección determinista del rol
    role_idx = int.from_bytes(digest[4:8], byteorder="big") % len(eligible_roles)
    chosen_role = eligible_roles[role_idx]

    # Selección determinista de la frase (bark)
    barks = chosen_role.get("barks") or []
    bark = ""
    if barks:
        bark_idx = int.from_bytes(digest[8:12], byteorder="big") % len(barks)
        bark = barks[bark_idx]

    role_id = chosen_role["role_id"]
    name = chosen_role.get("label") or role_id.capitalize()
    reply = chosen_role.get("reply", "")

    return {
        "id": f"n0_{role_id}",
        "role_id": role_id,
        "name": name,
        "role": chosen_role.get("label") or role_id.capitalize(),
        "bark": bark,
        "reply": reply,
        "is_n0": True,
        "epoch": epoch,
    }
