"""Matematica de combate y progresion -- implementacion directa de
vintage-telnet/GAMEPLAY.md, seccion 20 (combate/HP/fatiga), seccion 22
(XP/recompensas/antifarmeo) y seccion 24 (cadencia/fatiga/heridas/
recuperacion v1, cerrada en el commit 6c764442206d7aeb31ac9daf6e7a084c27ee80c6).
Funciones puras, sin acceso a base de datos ni Flask, para que sean faciles
de probar y de auditar contra el documento.

No inventa mecanicas: cada formula cita la seccion de GAMEPLAY.md de la que
sale. Lo que GAMEPLAY.md sigue dejando abierto (estadisticas de Cornalomo,
rondas semi-automaticas/defensa contextual de 24.1-24.2 -- diferidas al
Issue #43 por decision del Arquitecto) NO se implementa aqui -- ver
NECESIDAD DE JUGABILIDAD en server/README.md.
"""
import math
import random

ATTRIBUTES = (
    "fuerza", "resistencia", "agilidad", "percepcion",
    "intelecto", "voluntad", "destreza", "presencia",
)

BASE_ARMA = 10  # GAMEPLAY.md 20.4: referencia de arma basica para arrancar.

CATEGORIES = ("trivial", "favorable", "comparable", "peligroso", "abrumador")

# GAMEPLAY.md 22.4: coeficiente base de XP de combate por categoria.
XP_COMBAT_COEFFICIENT = {
    "trivial": 0.02,
    "favorable": 0.07,
    "comparable": 0.12,
    "peligroso": 0.20,
    "abrumador": 0.25,
}

# GAMEPLAY.md 22.6: multiplicador antifarmeo segun repeticiones de familia
# dentro de las ultimas 10 victorias PvE (contando la victoria actual).
ANTIFARM_MULTIPLIER_BY_REPEATS = {1: 1.0, 2: 1.0, 3: 1.0, 4: 0.6, 5: 0.6}
ANTIFARM_MULTIPLIER_BEYOND = 0.25

# GAMEPLAY.md 22.5: bono de primera victoria de familia.
FIRST_FAMILY_VICTORY_BONUS = 0.05

# GAMEPLAY.md 22.8: multiplicador de cooperacion por numero de participantes.
COOPERATION_MULTIPLIER = {1: 1.0, 2: 0.8, 3: 0.7}
COOPERATION_MULTIPLIER_BEYOND = 0.6

# GAMEPLAY.md 22.7: categorias de descubrimiento/hito y su fraccion de XP.
DISCOVERY_XP_FRACTION = {
    "descubrimiento_significativo": 0.05,
    "descubrimiento_mayor": 0.10,
    "hito_narrativo_menor": 0.10,
    "hito_narrativo_importante": 0.15,
    "hito_narrativo_excepcional": 0.25,
}


def clamp(value, low, high):
    return max(low, min(high, value))


def competencia_general(level):
    """GAMEPLAY.md 20.2: CG = 8 x (nivel-1) / 99."""
    return 8 * (level - 1) / 99


def xp_for_next_level(level):
    """GAMEPLAY.md 22.1: XP_siguiente(L) = redondear(100 + 18(L-1) + 0.25(L-1)^2)."""
    return round(100 + 18 * (level - 1) + 0.25 * (level - 1) ** 2)


def hp_max(level, resistencia, voluntad):
    """GAMEPLAY.md 20.3."""
    return 100 + 1.25 * (level - 1) + 2.5 * (resistencia - 10) + 0.5 * (voluntad - 10)


def accuracy(attacker_destreza, attacker_percepcion, attacker_cg, defender_cg):
    """GAMEPLAY.md 20.4: probabilidad base de impacto, limitada a [25, 90]."""
    value = (55
             + 0.45 * (attacker_destreza - 10)
             + 0.18 * (attacker_percepcion - 10)
             + 0.5 * (attacker_cg - defender_cg))
    return clamp(value, 25, 90)


def raw_damage(attacker_fuerza, attacker_destreza, attacker_cg, base_arma=BASE_ARMA):
    """GAMEPLAY.md 20.4: dano fisico bruto con arma base 10."""
    return (base_arma
            + 0.48 * (attacker_fuerza - 10)
            + 0.12 * (attacker_destreza - 10)
            + 0.25 * attacker_cg)


def expected_dps(destreza, percepcion, fuerza, cg_self, cg_other, base_arma=BASE_ARMA):
    """Dano esperado por ronda sin defensa activa (impacto% x dano bruto)."""
    return (accuracy(destreza, percepcion, cg_self, cg_other) / 100.0
            * raw_damage(fuerza, destreza, cg_self, base_arma))


def resolve_attack_roll(attacker_destreza, attacker_percepcion, attacker_fuerza,
                         attacker_cg, defender_cg, base_arma=BASE_ARMA, rng=None,
                         accuracy_penalty=0, damage_multiplier=1.0):
    """Tira un golpe de verdad (no el DPS esperado) para resolver una ronda
    de combate real: GAMEPLAY.md 20.4. `accuracy_penalty`/`damage_multiplier`
    aplican los efectos de fatiga (24.4) y heridas (24.6) del atacante sobre
    su propio golpe. Devuelve (impacta, dano)."""
    rng = rng or random.Random()
    hit_chance = max(0, accuracy(attacker_destreza, attacker_percepcion, attacker_cg, defender_cg)
                      - accuracy_penalty)
    hits = rng.uniform(0, 100) < hit_chance
    damage = (raw_damage(attacker_fuerza, attacker_destreza, attacker_cg, base_arma) * damage_multiplier
              if hits else 0.0)
    return hits, damage


def fixed_expected_dps(precision_pct, damage):
    """Dano esperado por ronda de una criatura con perfil de combate fijo
    (precision%/dano de vintage-telnet/STARTER_CREATURE_BALANCE.md), en vez
    del modelo generico de atributos de 20.4. Ver resolve_fixed_attack_roll."""
    return precision_pct / 100.0 * damage


def resolve_fixed_attack_roll(precision_pct, damage, rng=None):
    """Tira un golpe de una criatura de perfil fijo aprobado en
    STARTER_CREATURE_BALANCE.md: precision%/dano directos, sin derivarlos
    del modelo generico de atributos de 20.4 (la revision de Arquitectura
    de PR #49 senalo que ese modelo derivado divergia demasiado del balance
    aprobado). Devuelve (impacta, dano), igual forma que resolve_attack_roll."""
    rng = rng or random.Random()
    hits = rng.uniform(0, 100) < precision_pct
    return hits, float(damage) if hits else 0.0


def encounter_category(player_dps, player_hp, enemy_dps, enemy_hp):
    """Clasifica el encuentro en las 5 categorias de GAMEPLAY.md 22.3 usando
    el margen esperado de tiempo hasta la muerte de cada lado (referencia
    tecnica explicitamente autorizada por el documento; los umbrales son
    afinables de balance, no un cambio de las 5 categorias).

    R = (rondas para que el enemigo mate al jugador) / (rondas para que el
    jugador mate al enemigo). R alto = el jugador sobrevive mucho mas de lo
    que tarda en ganar (encuentro facil); R bajo = el jugador podria morir
    antes de ganar (encuentro peligroso).

    Umbrales calibrados (revision de Arquitectura de PR #49) para que el
    perfil fijo aprobado de vintage-telnet/STARTER_CREATURE_BALANCE.md
    reproduzca la banda que ese mismo documento describe contra un
    personaje nivel 1 de referencia: Mordelinde Favorable, Espinajo de
    rastrojo Comparable."""
    if enemy_dps <= 0:
        rounds_to_kill_player = math.inf
    else:
        rounds_to_kill_player = player_hp / enemy_dps
    if player_dps <= 0:
        rounds_to_kill_enemy = math.inf
    else:
        rounds_to_kill_enemy = enemy_hp / player_dps
    if rounds_to_kill_enemy <= 0:
        ratio = math.inf
    else:
        ratio = rounds_to_kill_player / rounds_to_kill_enemy
    if ratio >= 10:
        return "trivial"
    if ratio >= 5:
        return "favorable"
    if ratio >= 1.8:
        return "comparable"
    if ratio >= 0.4:
        return "peligroso"
    return "abrumador"


def combat_xp(enemy_ref_level, category, player_level, is_first_family_victory,
              repeats_in_last_10, participants=1):
    """GAMEPLAY.md 22.4 (base + tope del 25%), 22.5 (primera familia),
    22.6 (antifarmeo) y 22.8 (cooperacion). Devuelve un entero de XP."""
    enemy_xp_next = xp_for_next_level(enemy_ref_level)
    player_xp_next = xp_for_next_level(player_level)
    base = enemy_xp_next * XP_COMBAT_COEFFICIENT[category]
    base = min(base, 0.25 * player_xp_next)
    if repeats_in_last_10 <= 5:
        antifarm = ANTIFARM_MULTIPLIER_BY_REPEATS[repeats_in_last_10]
    else:
        antifarm = ANTIFARM_MULTIPLIER_BEYOND
    total = base * antifarm
    if is_first_family_victory:
        total += enemy_xp_next * FIRST_FAMILY_VICTORY_BONUS
    if participants <= 3:
        total *= COOPERATION_MULTIPLIER[participants]
    else:
        total *= COOPERATION_MULTIPLIER_BEYOND
    return round(total)


def discovery_xp(reference_level, category):
    """GAMEPLAY.md 22.7."""
    return round(xp_for_next_level(reference_level) * DISCOVERY_XP_FRACTION[category])


def apply_xp(level, xp, gained):
    """GAMEPLAY.md 22.1: el exceso de XP se conserva al cruzar de nivel; en
    nivel 100 no se acumula progreso hacia 101 en la v1. Devuelve
    (nuevo_nivel, nuevo_xp, niveles_ganados)."""
    xp += gained
    levels_gained = 0
    while level < 100 and xp >= xp_for_next_level(level):
        xp -= xp_for_next_level(level)
        level += 1
        levels_gained += 1
    if level >= 100:
        level = 100
        xp = 0
    return level, xp, levels_gained


def flee_chance(player_agilidad, player_percepcion, enemy_agilidad, enemy_percepcion,
                 attacker_level_advantage, previous_failed_attempts, fatigue):
    """GAMEPLAY.md 20.10."""
    delta_agilidad = player_agilidad - enemy_agilidad
    delta_percepcion = player_percepcion - enemy_percepcion
    proteccion_desnivel = min(30, 0.6 * max(0, attacker_level_advantage))
    bonus_fallos = 15 * previous_failed_attempts
    penalizacion_fatiga = 10 if fatigue > 70 else 0
    value = (50
             + 0.45 * delta_agilidad
             + 0.15 * delta_percepcion
             + proteccion_desnivel
             + bonus_fallos
             - penalizacion_fatiga)
    return clamp(value, 20, 95)


def respawn_wound(current_wound):
    """GAMEPLAY.md 20.9: grave->moderada, moderada->leve, leve->ninguna. Como
    regla de simplicidad no debe persistir mas de una herida tras respawn
    (ya lo garantiza esta funcion al operar sobre una sola herida)."""
    downgrade = {"grave": "moderada", "moderada": "leve", "leve": "ninguna", "ninguna": "ninguna"}
    return downgrade.get(current_wound, "ninguna")


def respawn_state(hp_max_value):
    """GAMEPLAY.md 20.9: 60% HP maximo, 40 de fatiga al reaparecer."""
    return {"hp_current": round(hp_max_value * 0.6), "fatigue": 40}


# --- GAMEPLAY.md 24: fatiga, heridas y recuperacion (cerrado 2026-09-23) --

# 24.3: costes base de fatiga por accion, antes del modificador de
# Resistencia de 20.7. Solo las acciones que este piloto puede ejecutar
# (ataque basico, huir); defensa contextual/poderes quedan para el Issue #43
# y para cuando Jugabilidad valide cada poder.
FATIGUE_BASE_COST = {
    "ataque_basico": 4,
    "huir": 8,
}

WOUND_ORDER = ("ninguna", "leve", "moderada", "grave")
WOUND_RANK = {name: index for index, name in enumerate(WOUND_ORDER)}

# 24.6: multiplicador de fatiga generada y penalizaciones de precision/dano
# segun la herida mecanica principal (maximo una a la vez, ver 24.5).
WOUND_FATIGUE_MULTIPLIER = {"ninguna": 1.0, "leve": 1.10, "moderada": 1.20, "grave": 1.35}
WOUND_ACCURACY_PENALTY = {"ninguna": 0, "leve": 0, "moderada": 5, "grave": 10}
WOUND_DAMAGE_MULTIPLIER = {"ninguna": 1.0, "leve": 1.0, "moderada": 1.0, "grave": 0.90}
# 24.6: tope de HP que puede recuperar un descanso de campo segun herida.
WOUND_REST_HP_CAP_FRACTION = {"ninguna": 1.0, "leve": 1.0, "moderada": 0.85, "grave": 0.65}

# 24.4: penalizaciones de precision/dano segun estado de fatiga (20.7 fija
# los umbrales 70/90).
FATIGUE_ACCURACY_PENALTY = {"operativo": 0, "cansado": 5, "agotado": 10}
FATIGUE_DAMAGE_MULTIPLIER = {"operativo": 1.0, "cansado": 0.90, "agotado": 0.80}


def fatigue_state(fatigue):
    """GAMEPLAY.md 20.7/24.4: 0-69 operativo, 70-89 cansado, 90-100 agotado."""
    if fatigue >= 90:
        return "agotado"
    if fatigue >= 70:
        return "cansado"
    return "operativo"


def fatigue_modifier(resistencia):
    """GAMEPLAY.md 20.7: ModFatiga = max(0.55, 1 - 0.007x(Resistencia-10))."""
    return max(0.55, 1 - 0.007 * (resistencia - 10))


def fatigue_gained(action, resistencia, wound):
    """GAMEPLAY.md 20.7 (ModFatiga) x 24.3 (coste base) x 24.6 (multiplicador
    de herida). `action` es una clave de FATIGUE_BASE_COST."""
    base = FATIGUE_BASE_COST[action]
    return base * fatigue_modifier(resistencia) * WOUND_FATIGUE_MULTIPLIER[wound]


def combined_accuracy_penalty(fatigue, wound):
    """Suma las penalizaciones de precision de fatiga (24.4) y herida (24.6)
    que afectan a quien las sufre sobre su propio golpe/esquiva/huida."""
    return FATIGUE_ACCURACY_PENALTY[fatigue_state(fatigue)] + WOUND_ACCURACY_PENALTY[wound]


def combined_damage_multiplier(fatigue, wound):
    """Combina los multiplicadores de dano de fatiga (24.4) y herida (24.6)."""
    return FATIGUE_DAMAGE_MULTIPLIER[fatigue_state(fatigue)] * WOUND_DAMAGE_MULTIPLIER[wound]


def wound_from_hit(damage, hp_max_value):
    """GAMEPLAY.md 24.5: disparador de herida por un solo impacto, comparado
    contra el HP maximo del objetivo."""
    if hp_max_value <= 0:
        return "ninguna"
    fraction = damage / hp_max_value
    if fraction >= 0.5:
        return "grave"
    if fraction >= 0.35:
        return "moderada"
    if fraction >= 0.2:
        return "leve"
    return "ninguna"


def worse_wound(current, candidate):
    """GAMEPLAY.md 24.5: una herida mayor reemplaza a una menor; nunca se
    mantiene mas de una herida mecanica principal a la vez."""
    return candidate if WOUND_RANK[candidate] > WOUND_RANK[current] else current


def rest_result(hp_current, hp_max_value, fatigue, resistencia, wound):
    """GAMEPLAY.md 24.8: accion explicita `descansar` fuera de combate.
    Cura 10% del HP maximo (respetando el tope de 24.6 segun herida) y
    reduce fatiga en 25 + 0.2x(Resistencia-10)."""
    cap = hp_max_value * WOUND_REST_HP_CAP_FRACTION[wound]
    healed = min(cap, hp_current + hp_max_value * 0.10)
    fatigue_reduction = 25 + 0.2 * (resistencia - 10)
    new_fatigue = max(0, fatigue - fatigue_reduction)
    return {"hp_current": round(healed), "fatigue": round(new_fatigue)}


# --- GAMEPLAY.md 31: informacion visible de enemigos -----------------------

# 31.1: bandas cualitativas de condicion segun porcentaje de HP restante.
# El limite inferior de cada banda es inclusive.
ENEMY_CONDITION_BANDS = (
    (76, "entero / apenas afectado"),
    (51, "herido"),
    (26, "malherido"),
    (1, "al borde de caer"),
)


def enemy_condition(hp_current, hp_max_value):
    """GAMEPLAY.md 31.1: condicion cualitativa de una criatura visible segun
    HP restante, sin revelar nunca el HP numerico (31.3). El jugador sigue
    viendo su propio HP exacto; esto es solo para enemigos."""
    if hp_max_value <= 0 or hp_current <= 0:
        return "derrotado"
    fraction = hp_current / hp_max_value * 100
    for threshold, label in ENEMY_CONDITION_BANDS:
        if fraction >= threshold:
            return label
    return "derrotado"


def safe_recovery_result(hp_max_value, wound):
    """GAMEPLAY.md 24.9: recuperacion segura completa en un punto que
    Narrativa/Historia marque como valido -- restaura 100% HP, fatiga a 0 y
    mejora la herida un grado. Funcion pura lista para usarse en cuanto el
    Narrador entregue el ID concreto pedido en Issue #46; ver NECESIDAD
    NARRATIVA en server/README.md -- no se ata todavia a ninguna sala para
    no inventar esa decision."""
    return {"hp_current": round(hp_max_value), "fatigue": 0, "wound": respawn_wound(wound)}
