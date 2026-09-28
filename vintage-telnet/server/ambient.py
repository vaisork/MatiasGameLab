"""Motor C0 (#379 / GAMEPLAY §39.1–39.5), sin catálogo productivo.

El adaptador de sala aporta contexto canónico y estado de sesión. Este módulo
no importa combate, store ni proveedores LLM y nunca crea entidades persistentes.
"""
from dataclasses import dataclass
import hashlib
import json
import math
import time


DENSITY = {
    "ambient_none": 0.0,
    "ambient_sparse": 0.15,
    "ambient_normal": 0.30,
    "ambient_rich": 0.45,
}
EPOCH_SECONDS = 600
SESSION_KEY = "ambient_c0"
# Historia #333 entregará especies y mapping. No activar fixtures en producción.
CATALOG = ()


@dataclass(frozen=True)
class Habitat:
    room_id: str
    habitat_id: str
    region: str
    tags: frozenset[str]
    profile: str = "ambient_none"

    def __post_init__(self):
        if not all(isinstance(value, str) and value.strip()
                   for value in (self.room_id, self.habitat_id, self.region)):
            raise ValueError("room_id, habitat_id y region son obligatorios")
        if self.profile not in DENSITY:
            raise ValueError("perfil C0 desconocido")
        object.__setattr__(self, "tags", _strings(self.tags, "tags"))


@dataclass(frozen=True)
class Presence:
    ambient_id: str
    name: str
    behavior_text: str
    room_id: str
    epoch: int


def _strings(values, field):
    if not isinstance(values, (list, tuple, set, frozenset)):
        raise ValueError(f"{field} debe ser una colección de identificadores")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError(f"{field} contiene un identificador inválido")
    return frozenset(values)


def validate_catalog(catalog):
    """Contrato de #333: rechaza datos ambiguos; vacío es válido.

    Regiones/habitat_tags son allowlists no vacías. Exclusions veta cualquier
    coincidencia con room_id, habitat_id, región o tags del contexto.
    """
    seen = set()
    fields = {"ambient_id", "name", "regions", "habitat_tags", "behavior_text", "exclusions"}
    for entry in catalog:
        if not isinstance(entry, dict) or set(entry) != fields:
            raise ValueError("registro C0 debe contener solo los seis campos del contrato")
        for field in ("ambient_id", "name", "behavior_text"):
            if not isinstance(entry[field], str) or not entry[field].strip():
                raise ValueError(f"{field} es obligatorio")
        if entry["ambient_id"] in seen:
            raise ValueError("ambient_id duplicado")
        seen.add(entry["ambient_id"])
        for field in ("regions", "habitat_tags"):
            if not _strings(entry[field], field):
                raise ValueError(f"{field} no puede estar vacío")
        _strings(entry["exclusions"], "exclusions")
    return catalog


def _number(parts, hash_fn):
    # JSON evita colisiones por concatenación; SHA-256 evita el hash aleatorio
    # de Python y da el mismo resultado en procesos/dispositivos distintos.
    key = json.dumps(parts, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    digest = hash_fn(key)
    if not isinstance(digest, bytes) or len(digest) != 32:
        raise ValueError("hash_fn debe devolver 32 bytes")
    return int.from_bytes(digest, "big")


def stable_hash(key):
    return hashlib.sha256(key).digest()


def select_presence(habitat, *, catalog=None, now=None, hash_fn=stable_hash,
                    combat_active=False, scripted=False, encounter=False):
    """Una observación compartida o None. No consulta ni modifica sesiones/DB.

    Tiempo Unix y hash son inyectables. Cada registro compatible tiene el mismo
    peso; no hay rareza ni pesos regionales implícitos. El orden del catálogo no
    cambia la selección. Las prioridades se suministran desde estado autoritativo.
    """
    if combat_active or scripted or encounter:
        return None
    records = tuple(CATALOG if catalog is None else catalog)
    validate_catalog(records)
    chance = DENSITY[habitat.profile]
    if not records or chance == 0:
        return None
    context = habitat.tags | {habitat.room_id, habitat.habitat_id, habitat.region}
    eligible = sorted((entry for entry in records
                       if habitat.region in entry["regions"]
                       and habitat.tags.intersection(entry["habitat_tags"])
                       and not context.intersection(entry["exclusions"])),
                      key=lambda entry: entry["ambient_id"])
    if not eligible:
        return None
    timestamp = time.time() if now is None else now
    if not math.isfinite(timestamp) or timestamp < 0:
        raise ValueError("tiempo Unix inválido")
    epoch = math.floor(timestamp / EPOCH_SECONDS)
    key = [epoch, habitat.room_id, habitat.habitat_id]
    scale = 1 << 256
    # Un único roll de presencia; añadir especies no incrementa la densidad.
    if _number(["c0-presence", *key], hash_fn) >= int(chance * scale):
        return None
    index = _number(["c0-species", *key], hash_fn) * len(eligible) // scale
    entry = eligible[index]
    return Presence(entry["ambient_id"], entry["name"], entry["behavior_text"],
                    habitat.room_id, epoch)


def _state(session_state, epoch):
    previous = session_state.get(SESSION_KEY, {})
    if previous.get("epoch") != epoch:
        return {"epoch": epoch, "rooms": {}}
    # Reasignar el valor superior también funciona con sesiones Flask firmadas.
    return {"epoch": epoch, "rooms": dict(previous.get("rooms", {}))}


def observe(presence, session_state, *, explicit=False):
    """Anti-spam por sesión/sala/fase; observar explícitamente puede repetir.

    Guardar este estado solo en sesión, nunca en la DB del personaje. El llamador
    entrega una Presence recién seleccionada (no una observación caducada).
    """
    if presence is None:
        return None
    state = _state(session_state, presence.epoch)
    status = state["rooms"].get(presence.room_id)
    if status == "withdrawn" or (status == "seen" and not explicit):
        return None
    state["rooms"][presence.room_id] = "seen"
    session_state[SESSION_KEY] = state
    return presence


def withdraw(presence, session_state):
    """Intentar atacar C0 retira la observación local durante esta fase.

    Devuelve datos para una respuesta legible del adaptador; no ejecuta ataque,
    coste, recompensa o mutación del mundo compartido. No afecta a otras sesiones.
    """
    if presence is None:
        return None
    state = _state(session_state, presence.epoch)
    if state["rooms"].get(presence.room_id) == "withdrawn":
        return None
    state["rooms"][presence.room_id] = "withdrawn"
    session_state[SESSION_KEY] = state
    return {"outcome": "ambient_withdrawn", "ambient_id": presence.ambient_id,
            "name": presence.name}


validate_catalog(CATALOG)
