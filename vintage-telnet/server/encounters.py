"""Motor de encuentros aleatorios (Issue #160, petición de Javier).

Objetivo: que la fauna común pueda aparecer al azar en caminos y campo sin
asignar cada criatura a mano sala por sala en `world.ROOM_ENCOUNTER`.

Orden al resolver el encuentro de una sala (regla arquitectónica de #160):
  1. si la sala tiene encuentro fijo/narrativo en `world.ROOM_ENCOUNTER`,
     ese manda siempre (El lindero roto sigue igual);
  2. si no, y la sala pertenece a un pool aleatorio, se tira el dado del pool;
  3. si no, no hay criatura.

Este módulo es solo el motor. **No decide balance, hábitat ni canon.** Qué
salas son elegibles, qué criaturas viven ahí, con qué peso y con qué
probabilidad aparecen corresponde a Jugabilidad (tasas) y a
Historiador/Narrador (qué criatura vive dónde). Por eso
`RANDOM_ENCOUNTER_POOLS` empieza vacío: el juego se comporta exactamente
como antes hasta que esas funciones lo llenen.

Formato de un pool:

    "nombre_del_pool": {
        "rooms": {"sala_a", "sala_b"},          # salas elegibles
        "chance": 0.25,                          # probabilidad por tirada, 0 < chance <= 1
        "creatures": [("mordelinde", 3),         # (creature_id, peso > 0)
                      ("espinajo_rastrojo", 1)],
    }

Parámetros v1 ya definidos por Jugabilidad (`GAMEPLAY.md` §33, aprobado tras
la revisión de la PR #165):
  - la tirada ocurre únicamente **al entrar con éxito** a una sala elegible;
    nunca por tiempo, por `mirar`/examinar ni durante un combate ya activo;
  - probabilidad de referencia **20%** por entrada elegible; los pools
    ordinarios pueden ajustarla en la banda **10%–35%** (perfiles de zona en
    `RANDOM_ENCOUNTER_GAMEPLAY.md` §2). Fuera de esa banda hace falta
    validación explícita de Jugabilidad;
  - repetición: se reutiliza el enfriamiento por sala que ya existe tras
    vencer a una criatura, ~5 min
    (`store.CREATURE_RESPAWN_COOLDOWN_SECONDS`). No se añade un segundo
    cooldown propio de la tirada aleatoria en esta etapa (§33.4).

Sigue pendiente de Historiador/Narrador (Issue #166): qué salas son
elegibles y qué criaturas canónicas viven en cada zona. Por eso
`RANDOM_ENCOUNTER_POOLS` sigue vacío aquí: el juego se comporta exactamente
como antes hasta que esa ecología regional se entregue y se cargue.
"""
import random

from . import creatures, world

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
