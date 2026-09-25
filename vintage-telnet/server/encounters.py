"""Motor de encuentros aleatorios (Issue #160, petición de Javier).

Objetivo: que la fauna común pueda aparecer al azar en caminos y campo sin
asignar cada criatura a mano sala por sala en `world.ROOM_ENCOUNTER`.

Orden al resolver el encuentro de una sala (regla arquitectónica de #160):
  1. si la sala tiene encuentro fijo/narrativo en `world.ROOM_ENCOUNTER`,
     ese manda siempre (El lindero roto sigue igual);
  2. si no, y la sala pertenece a un pool aleatorio, se tira el dado del pool;
  3. si no, no hay criatura.

Este módulo es solo el motor. **No decide balance, hábitat ni canon.**
Reglas aprobadas: `GAMEPLAY.md` §33 y `RANDOM_ENCOUNTER_GAMEPLAY.md`.
  - La tirada ocurre **solo al entrar con éxito** a una sala elegible (§33.2);
    nunca por esperar, mirar ni durante un combate activo.
  - Se reutiliza el enfriamiento de ~5 min por sala tras vencer (§33.4).
  - La probabilidad sale de un perfil de densidad (`DENSITY`, §2 del
    documento de estrategia). La banda ordinaria es 10–35 %; fuera de ella
    el pool debe declarar `"gameplay_override": True` (aprobación explícita
    de Jugabilidad).
  - Qué salas son elegibles y qué criaturas viven ahí lo entregan
    Historia/Narrativa (§8). Hasta recibir ese mapeo, `RANDOM_ENCOUNTER_POOLS`
    **sigue vacío** y el juego se comporta exactamente como antes (§10).

Formato de un pool:

    "nombre_del_pool": {
        "rooms": {"sala_a", "sala_b"},          # salas elegibles
        "chance": DENSITY["camino"],             # probabilidad por entrada
        "creatures": [("mordelinde", 70),        # (creature_id, peso relativo > 0)
                      ("espinajo_rastrojo", 30)],
    }
"""
import random

from . import creatures, world

# Perfiles de densidad de Jugabilidad (RANDOM_ENCOUNTER_GAMEPLAY.md §2).
DENSITY = {
    "borde_habitado": 0.10,
    "camino": 0.20,        # referencia v1 (GAMEPLAY.md §33.3)
    "silvestre": 0.30,
    "riesgo_alto": 0.35,
}
ORDINARY_BAND = (0.10, 0.35)

RANDOM_ENCOUNTER_POOLS = {}

_rng = random.Random()


class InvalidPoolConfig(ValueError):
    pass


def validate_pools(pools):
    """Rechaza cualquier configuración rota en vez de ignorarla en silencio:
    criatura inexistente, sala inexistente, peso o probabilidad inválidos,
    pool vacío o una sala repetida en dos pools."""
    seen_rooms = {}
    for pool_id, pool in pools.items():
        rooms = pool.get("rooms")
        entries = pool.get("creatures")
        chance = pool.get("chance")
        if not rooms:
            raise InvalidPoolConfig(f"{pool_id}: sin salas elegibles")
        if not entries:
            raise InvalidPoolConfig(f"{pool_id}: sin criaturas")
        if (isinstance(chance, bool) or not isinstance(chance, (int, float))
                or not 0 < chance <= 1):
            raise InvalidPoolConfig(f"{pool_id}: chance debe estar entre 0 (sin incluir) y 1")
        low, high = ORDINARY_BAND
        if not low <= chance <= high and not pool.get("gameplay_override"):
            raise InvalidPoolConfig(
                f"{pool_id}: chance {chance} fuera de la banda 10–35 %; necesita "
                "\"gameplay_override\": True con aprobación de Jugabilidad (GAMEPLAY.md §33.3)")
        for room_id in rooms:
            if world.get_room(room_id) is None:
                raise InvalidPoolConfig(f"{pool_id}: sala inexistente {room_id!r}")
            if room_id in seen_rooms:
                raise InvalidPoolConfig(
                    f"{pool_id}: la sala {room_id!r} ya está en el pool {seen_rooms[room_id]!r}")
            seen_rooms[room_id] = pool_id
        for entry in entries:
            if not isinstance(entry, (tuple, list)) or len(entry) != 2:
                raise InvalidPoolConfig(f"{pool_id}: cada criatura va como (creature_id, peso)")
            creature_id, weight = entry
            if creatures.get_creature(creature_id) is None:
                raise InvalidPoolConfig(f"{pool_id}: criatura inexistente {creature_id!r}")
            if isinstance(weight, bool) or not isinstance(weight, (int, float)) or weight <= 0:
                raise InvalidPoolConfig(f"{pool_id}: peso inválido para {creature_id!r}")
    return pools


def pool_for_room(room_id, pools=None):
    pools = RANDOM_ENCOUNTER_POOLS if pools is None else pools
    for pool in pools.values():
        if room_id in pool["rooms"]:
            return pool
    return None


def get_encounter_for_room(room_id, rng=None, pools=None):
    """creature_id que aparece al entrar a room_id, o None."""
    fixed = world.get_room_encounter(room_id)
    if fixed:
        return fixed
    pool = pool_for_room(room_id, pools)
    if pool is None:
        return None
    rng = rng or _rng
    if rng.random() >= pool["chance"]:
        return None
    ids = [creature_id for creature_id, _weight in pool["creatures"]]
    weights = [weight for _creature_id, weight in pool["creatures"]]
    return rng.choices(ids, weights=weights, k=1)[0]


# La configuración real se valida al importar: un error de tipeo en un
# creature_id tumba el arranque (y las pruebas) en lugar de desaparecer.
validate_pools(RANDOM_ENCOUNTER_POOLS)
