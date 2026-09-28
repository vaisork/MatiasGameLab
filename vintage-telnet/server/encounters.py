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
    Historia/Narrativa (§8, Issue #166). `RANDOM_ENCOUNTER_POOLS` contiene
    únicamente mapeos regionales aprobados por las funciones responsables.

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

# GAMEPLAY.md §40: amenazas regionales C3 v1. Estas criaturas usan el motor
# especial de amenazas y nunca pueden entrar en un pool C1 ordinario.
C3_THREAT_IDS = frozenset({
    "cornalomo",
    "rasgacumbres",
    "quebrarrocas",
    "dorsalodo",
    "rasgacorteza",
})

# GAMEPLAY.md §38: fauna mayor C4. No entra en pools aleatorios ordinarios.
C4_MAJOR_FAUNA_IDS = frozenset({
    "cargallanura",
})

# EDRAN-01 (#207) y fauna regional aprobada en #314/#315/#317.
# Las salas con chance 0%, reservadas, civiles o de transición no aparecen
# en ningún pool; cada entrega conserva su tabla contractual en el issue.
RANDOM_ENCOUNTER_POOLS = {
    "edran_01_borde_habitado": {
        "rooms": {"valdren_sendero"},
        "chance": DENSITY["borde_habitado"],
        "creatures": [("mordelinde", 85), ("espinajo_rastrojo", 15)],
    },
    "edran_01_campos_transitados": {
        "rooms": {"valdren_camino_hundido", "valdren_parcelas_exteriores"},
        "chance": DENSITY["camino"],
        "creatures": [("mordelinde", 75), ("espinajo_rastrojo", 25)],
    },
    "edran_01_campo_abierto": {
        "rooms": {"valdren_campo_rastrojo", "valdren_campos_sin_cerca"},
        "chance": DENSITY["silvestre"],
        "creatures": [("mordelinde", 65), ("espinajo_rastrojo", 35)],
    },
    # KORVEN-POOL-01 (#314): solo rooms con chance aprobada > 0.
    "korven_01_pared_anclajes": {
        "rooms": {"piedra_pared_anclajes"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("cascapedernal", 100)],
    },
    "korven_01_paso_corto": {
        "rooms": {"piedra_paso_corto"}, "chance": DENSITY["camino"],
        "creatures": [("cascapedernal", 60), ("colagrieta", 40)],
    },
    "korven_01_patio_abierto": {
        "rooms": {"piedra_patio_abierto"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("cascapedernal", 100)],
    },
    "korven_01_hendiduras": {
        "rooms": {"piedra_hendiduras"}, "chance": DENSITY["silvestre"],
        "creatures": [("cascapedernal", 40), ("colagrieta", 60)],
    },
    "korven_01_pared_partida": {
        "rooms": {"piedra_pared_partida"}, "chance": DENSITY["camino"],
        "creatures": [("cascapedernal", 50), ("colagrieta", 50)],
    },
    "korven_01_meseta_baja": {
        "rooms": {"piedra_meseta_baja"}, "chance": DENSITY["camino"],
        "creatures": [("cascapedernal", 100)],
    },
    "korven_01_cruce_montones": {
        "rooms": {"piedra_cruce_montones"}, "chance": DENSITY["camino"],
        "creatures": [("cascapedernal", 100)],
    },
    "korven_01_cavidades": {
        "rooms": {"piedra_cavidades"}, "chance": DENSITY["silvestre"],
        "creatures": [("cascapedernal", 35), ("colagrieta", 65)],
    },
    "korven_01_ultimo_corredor": {
        "rooms": {"piedra_ultimo_corredor"}, "chance": DENSITY["silvestre"],
        "creatures": [("cascapedernal", 40), ("colagrieta", 60)],
    },
    "korven_01_suelo_quebrado": {
        "rooms": {"piedra_suelo_quebrado"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("cascapedernal", 100)],
    },
    # LETHRA-POOL-01 (#315).
    "lethra_01_postes": {
        "rooms": {"juncos_postes"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("pinzajunco", 100)],
    },
    "lethra_01_juncal": {
        "rooms": {"juncos_juncal"}, "chance": DENSITY["camino"],
        "creatures": [("pinzajunco", 55), ("saltalodo", 45)],
    },
    "lethra_01_paso_raices": {
        "rooms": {"juncos_paso_raices"}, "chance": DENSITY["silvestre"],
        "creatures": [("pinzajunco", 50), ("saltalodo", 50)],
    },
    "lethra_01_agua_entre_caminos": {
        "rooms": {"juncos_agua_entre_caminos"}, "chance": DENSITY["silvestre"],
        "creatures": [("pinzajunco", 55), ("saltalodo", 45)],
    },
    "lethra_01_pasarela_larga": {
        "rooms": {"juncos_pasarela_larga"}, "chance": DENSITY["camino"],
        "creatures": [("saltalodo", 100)],
    },
    "lethra_01_islas_bajas": {
        "rooms": {"juncos_islas_bajas"}, "chance": DENSITY["camino"],
        "creatures": [("pinzajunco", 50), ("saltalodo", 50)],
    },
    "lethra_01_canal_ancho": {
        "rooms": {"juncos_canal_ancho"}, "chance": DENSITY["silvestre"],
        "creatures": [("pinzajunco", 55), ("saltalodo", 45)],
    },
    "lethra_01_ultimos": {
        "rooms": {"juncos_ultimos"}, "chance": DENSITY["silvestre"],
        "creatures": [("pinzajunco", 40), ("saltalodo", 60)],
    },
    "lethra_01_corrientes": {
        "rooms": {"juncos_corrientes"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("pinzajunco", 100)],
    },
    # NHAL-POOL-01 (#317): Hilaria solo donde Historia confirma anclajes.
    "nhal_01_raices_cruzadas": {
        "rooms": {"sombra_raices_cruzadas"}, "chance": DENSITY["camino"],
        "creatures": [("rondamusgo", 50), ("hilaria_niebla", 50)],
    },
    "nhal_01_claro_pequeno": {
        "rooms": {"sombra_claro_pequeno"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("rondamusgo", 100)],
    },
    "nhal_01_sendero_doble": {
        "rooms": {"sombra_sendero_doble"}, "chance": DENSITY["camino"],
        "creatures": [("rondamusgo", 55), ("hilaria_niebla", 45)],
    },
    "nhal_01_niebla_baja": {
        "rooms": {"sombra_niebla_baja"}, "chance": DENSITY["silvestre"],
        "creatures": [("rondamusgo", 40), ("hilaria_niebla", 60)],
    },
    "nhal_01_arbol_caido": {
        "rooms": {"sombra_arbol_caido"}, "chance": DENSITY["silvestre"],
        "creatures": [("rondamusgo", 40), ("hilaria_niebla", 60)],
    },
    "nhal_01_raiz_alta": {
        "rooms": {"sombra_raiz_alta"}, "chance": DENSITY["silvestre"],
        "creatures": [("rondamusgo", 50), ("hilaria_niebla", 50)],
    },
    "nhal_01_bosque_abierto": {
        "rooms": {"sombra_bosque_abierto"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("rondamusgo", 100)],
    },
    # BM-01: Boca de la Montaña superficial (#424 / BOCA_MONTANA_APPROACH.md)
    "bm_02_raices_sobre_roca": {
        "rooms": {"bm_02_raices_sobre_roca"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("rondamusgo", 30), ("hilaria_niebla", 20), ("silbarisco", 50)],
    },
    "bm_04_ladera_grava": {
        "rooms": {"bm_04_ladera_grava"}, "chance": DENSITY["camino"],
        "creatures": [("silbarisco", 100)],
    },
    "bm_05_saliente_raices": {
        "rooms": {"bm_05_saliente_raices"}, "chance": DENSITY["silvestre"],
        "creatures": [("hilaria_niebla", 35), ("silbarisco", 65)],
    },
    "bm_06_terraza_exterior": {
        "rooms": {"bm_06_terraza_exterior"}, "chance": DENSITY["camino"],
        "creatures": [("silbarisco", 30), ("unapiedra", 35), ("saltacresta", 35)],
    },
    "bm_07_risco_sombreado": {
        "rooms": {"bm_07_risco_sombreado"}, "chance": DENSITY["riesgo_alto"],
        "creatures": [("unapiedra", 65), ("saltacresta", 35)],
    },
    "bm_08_antesala_boca": {
        "rooms": {"bm_08_antesala_boca"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("unapiedra", 100)],
    },
    # CQ-01: Canal Quieto superficial (#423 / CANAL_QUIETO_APPROACH.md)
    "cq_02_orilla_juncos_bajos": {
        "rooms": {"cq_02_orilla_juncos_bajos"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("pinzajunco", 55), ("saltalodo", 45)],
    },
    "cq_04_raices_ribera": {
        "rooms": {"cq_04_raices_ribera"}, "chance": DENSITY["silvestre"],
        "creatures": [("pinzajunco", 35), ("velacauce", 65)],
    },
    "cq_05_recodo_tronco": {
        "rooms": {"cq_05_recodo_tronco"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("rondamusgo", 100)],
    },
    "cq_06_paso_raices": {
        "rooms": {"cq_06_paso_raices"}, "chance": DENSITY["camino"],
        "creatures": [("pinzajunco", 25), ("rondamusgo", 30), ("hilaria_niebla", 25), ("velacauce", 20)],
    },
    "cq_07_orilla_blanda": {
        "rooms": {"cq_07_orilla_blanda"}, "chance": DENSITY["riesgo_alto"],
        "creatures": [("pinzajunco", 25), ("saltalodo", 30), ("velacauce", 45)],
    },
    "cq_08_recodo_sin_vista": {
        "rooms": {"cq_08_recodo_sin_vista"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("velacauce", 100)],
    },
    # CA-01: Cantera Abandonada superficial (#422 / CANTERA_ABANDONADA_APPROACH.md)
    "ca_02_patio_grava": {
        "rooms": {"ca_02_patio_grava"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("mordelinde", 60), ("espinajo_rastrojo", 40)],
    },
    "ca_03_plataforma_baja": {
        "rooms": {"ca_03_plataforma_baja"}, "chance": DENSITY["camino"],
        "creatures": [("cascapedernal", 100)],
    },
    "ca_04_montones_descarte": {
        "rooms": {"ca_04_montones_descarte"}, "chance": DENSITY["silvestre"],
        "creatures": [("cascapedernal", 40), ("cavapolvo", 60)],
    },
    "ca_06_plataforma_alta": {
        "rooms": {"ca_06_plataforma_alta"}, "chance": DENSITY["camino"],
        "creatures": [("cascapedernal", 50), ("colagrieta", 50)],
    },
    "ca_07_frente_quebrado": {
        "rooms": {"ca_07_frente_quebrado"}, "chance": DENSITY["riesgo_alto"],
        "creatures": [("cascapedernal", 20), ("colagrieta", 35), ("cavapolvo", 45)],
    },
    "ca_08_paso_bloques": {
        "rooms": {"ca_08_paso_bloques"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("cascapedernal", 40), ("colagrieta", 60)],
    },
    # GE-01: Grieta del Eco Seco superficial (#419 / GRIETA_ECO_SECO_APPROACH.md)
    "ge_02_terrazas_rotas": {
        "rooms": {"ge_02_terrazas_rotas"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("unapiedra", 45), ("saltacresta", 25), ("garralaja", 30)],
    },
    "ge_03_repisa_viento": {
        "rooms": {"ge_03_repisa_viento"}, "chance": DENSITY["camino"],
        "creatures": [("unapiedra", 30), ("cascapedernal", 15), ("garralaja", 55)],
    },
    "ge_04_quiebre_lajas": {
        "rooms": {"ge_04_quiebre_lajas"}, "chance": DENSITY["silvestre"],
        "creatures": [("unapiedra", 15), ("cascapedernal", 35), ("garralaja", 50)],
    },
    "ge_06_fisuras_paralelas": {
        "rooms": {"ge_06_fisuras_paralelas"}, "chance": DENSITY["silvestre"],
        "creatures": [("cascapedernal", 15), ("colagrieta", 50), ("garralaja", 35)],
    },
    "ge_07_grava_fondo": {
        "rooms": {"ge_07_grava_fondo"}, "chance": DENSITY["riesgo_alto"],
        "creatures": [("cascapedernal", 20), ("colagrieta", 35), ("garralaja", 45)],
    },
    "ge_08_ultima_luz_directa": {
        "rooms": {"ge_08_ultima_luz_directa"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("unapiedra", 35), ("cascapedernal", 20), ("colagrieta", 10), ("garralaja", 35)],
    },
    # MH-01: Molino Hundido superficial (#341)
    "mh_02_bordes_vencidos": {
        "rooms": {"mh_02_bordes_vencidos"}, "chance": DENSITY["borde_habitado"],
        "creatures": [("mordelinde", 50), ("pinzajunco", 20), ("saltalodo", 10), ("remojunco", 20)],
    },
    "mh_03_juncos_partidos": {
        "rooms": {"mh_03_juncos_partidos"}, "chance": DENSITY["camino"],
        "creatures": [("mordelinde", 10), ("pinzajunco", 25), ("saltalodo", 20), ("remojunco", 45)],
    },
    "mh_05_terreno_dos_aguas": {
        "rooms": {"mh_05_terreno_dos_aguas"}, "chance": DENSITY["camino"],
        "creatures": [("mordelinde", 15), ("pinzajunco", 30), ("saltalodo", 25), ("remojunco", 30)],
    },
    "mh_06_restos_cauce": {
        "rooms": {"mh_06_restos_cauce"}, "chance": DENSITY["silvestre"],
        "creatures": [("pinzajunco", 30), ("saltalodo", 25), ("remojunco", 45)],
    },
    "mh_08_rodeo_base": {
        "rooms": {"mh_08_rodeo_base"}, "chance": DENSITY["riesgo_alto"],
        "creatures": [("pinzajunco", 30), ("saltalodo", 35), ("remojunco", 35)],
    },
    "mh_09_plataforma_caida": {
        "rooms": {"mh_09_plataforma_caida"}, "chance": DENSITY["camino"],
        "creatures": [("pinzajunco", 20), ("saltalodo", 40), ("remojunco", 40)],
    },
}

_rng = random.Random()


class InvalidPoolConfig(ValueError):
    pass


def validate_pools(pools):
    """Rechaza cualquier configuración rota en vez de ignorarla en silencio:
    criatura inexistente, amenaza C3 dentro de C1, sala inexistente,
    peso o probabilidad inválidos, pool vacío o una sala repetida en dos pools."""
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
            if creature_id in C3_THREAT_IDS:
                raise InvalidPoolConfig(
                    f"{pool_id}: amenaza C3 {creature_id!r} no puede entrar en pool C1 ordinario "
                    "(GAMEPLAY.md §40.5)")
            if creature_id in C4_MAJOR_FAUNA_IDS:
                raise InvalidPoolConfig(
                    f"{pool_id}: fauna mayor C4 {creature_id!r} no puede entrar en pool C1 ordinario "
                    "(GAMEPLAY.md §38.10)")
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
