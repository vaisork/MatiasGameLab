"""Motor reusable de jefes únicos C5 v1 (GAMEPLAY §41 / Issue #362).

Implementa la arquitectura y reglas para jefes únicos C5:
1. Declaración explícita mediante BossContract (§41.1).
2. Jefe único y persistencia global (boss_defeated compartido en el mundo, §41.2).
3. Intento activo: encounter, HP y fase compartidos por participantes legítimos (§41.3).
4. Advertencia previa y punto de retirada en entry_room (§41.4).
5. Fases data-driven con prepared_actions (§41.5 / §36).
6. Muerte del jugador: respawn general y preservación de personaje, nivel, inventario (§41.6).
7. Pérdida de arma opt-in: weapon_loss_on_defeat (default False, §41.7).
8. Gate de pérdida: sin arma no sustituye penalización por otro objeto (§41.8, §41.9).
9. Recompensas data-driven con scope 'world' o 'character' y filtro de contribución (§41.10, §41.11).
10. Reintento tras derrota: reset default de HP y fase al terminar el intento (§41.3, §41.12).
"""

from dataclasses import dataclass, field
import random
import time
from typing import Dict, List, Optional

from server import combat, items, store, world


@dataclass
class BossPhase:
    """Fase específica de un jefe C5 (§41.5)."""
    phase_index: int
    name: str
    min_hp_pct: float  # e.g. 0.0
    max_hp_pct: float  # e.g. 0.50
    precision: int
    damage: int
    armor_reduction: float = 0.0
    prepared_actions: List[dict] = field(default_factory=list)
    behavior_text: str = ""
    description: str = ""


@dataclass
class BossReward:
    """Recompensa data-driven explícita (§41.10)."""
    reward_key: str
    reward_type: str  # 'xp', 'discovery', 'item', 'flag'
    target: str
    amount: int = 1
    scope: str = "character"  # 'character' | 'world'


@dataclass
class BossContract:
    """Contrato autoritativo de un jefe C5 (§41.1)."""
    boss_id: str
    name: str
    entry_room_id: str   # Sala de advertencia y último retorno (§41.4)
    arena_room_id: str   # Sala de combate / encounter
    max_hp: int
    phases: List[BossPhase]
    warning_signal: str = ""
    close_signal: str = ""
    defeated_signal: str = ""
    weapon_loss_on_defeat: bool = False  # §41.7: default False
    flee_possible: bool = True
    flee_agilidad: int = 10
    flee_percepcion: int = 10
    rewards: List[BossReward] = field(default_factory=list)
    min_contribution_damage: float = 1.0  # §41.11


@dataclass
class BossEvaluation:
    """Resultado de consultar el estado de un jefe para una sala."""
    boss_id: str
    name: str
    stage: str  # 'warning' | 'arena' | 'defeated' | 'none'
    close_encounter: bool = False
    message: str = ""
    current_hp: Optional[float] = None
    max_hp: Optional[float] = None
    current_phase: Optional[int] = None
    available_actions: List[dict] = field(default_factory=list)


# Registro de jefes C5
_BOSS_REGISTRY: Dict[str, BossContract] = {}


def register_boss(contract: BossContract) -> None:
    """Registra un contrato de jefe único C5."""
    _BOSS_REGISTRY[contract.boss_id] = contract


def get_boss(boss_id: str) -> Optional[BossContract]:
    """Obtiene el contrato de un jefe por su identificador."""
    return _BOSS_REGISTRY.get(boss_id)


def get_all_bosses() -> List[BossContract]:
    """Lista todos los contratos de jefes registrados."""
    return list(_BOSS_REGISTRY.values())


def get_boss_by_room(room_id: str) -> Optional[BossContract]:
    """Busca si una sala está asociada a un jefe (entry o arena)."""
    for b in _BOSS_REGISTRY.values():
        if room_id in (b.entry_room_id, b.arena_room_id):
            return b
    return None


def get_boss_by_arena(room_id: str) -> Optional[BossContract]:
    """Busca si una sala es el arena de combate de un jefe."""
    for b in _BOSS_REGISTRY.values():
        if room_id == b.arena_room_id:
            return b
    return None


def get_boss_by_entry(room_id: str) -> Optional[BossContract]:
    """Busca si una sala es el acceso/advertencia de un jefe."""
    for b in _BOSS_REGISTRY.values():
        if room_id == b.entry_room_id:
            return b
    return None


def clear_bosses() -> None:
    """Limpia el registro de jefes (para pruebas unitarias)."""
    _BOSS_REGISTRY.clear()


def is_boss_defeated(db_path: str, boss_id: str) -> bool:
    """Comprueba si el jefe fue derrotado de forma persistente en el mundo (§41.2)."""
    state = store.get_world_boss_state(db_path, boss_id)
    return state["defeated"]


def determine_current_phase(boss: BossContract, current_hp: float) -> BossPhase:
    """Determina la fase activa según el porcentaje actual de HP (§41.5)."""
    if not boss.phases:
        # Fallback genérico si no se especificaron fases
        return BossPhase(
            phase_index=0,
            name="Principal",
            min_hp_pct=0.0,
            max_hp_pct=1.0,
            precision=50,
            damage=15,
            behavior_text=f"{boss.name} te ataca de frente.",
        )
    hp_pct = max(0.0, min(1.0, current_hp / float(boss.max_hp)))
    for p in boss.phases:
        if p.min_hp_pct <= hp_pct <= p.max_hp_pct:
            return p
    # Si por redondeo cayó por debajo o arriba, retornar la fase correspondiente al extremo
    if hp_pct <= 0.0:
        return boss.phases[-1]
    return boss.phases[0]


def get_room_boss_view(
    db_path: str,
    player_id: str,
    room_id: str,
    now: Optional[float] = None,
) -> Optional[BossEvaluation]:
    """Consulta estructurada de presencia de jefe C5 para room_view (§41.4, §41.5)."""
    boss = get_boss_by_room(room_id)
    if not boss:
        return None

    defeated = is_boss_defeated(db_path, boss.boss_id)

    # 1. Sala de entrada / advertencia (§41.4)
    if room_id == boss.entry_room_id:
        if defeated:
            return BossEvaluation(
                boss_id=boss.boss_id,
                name=boss.name,
                stage="defeated",
                message="El rastro del peligro se ha apagado. El camino parece seguro.",
            )
        return BossEvaluation(
            boss_id=boss.boss_id,
            name=boss.name,
            stage="warning",
            message=boss.warning_signal or "Se percibe una presencia abrumadora más adelante. Un último sendero permite retroceder.",
        )

    # 2. Sala arena de combate (§41.3, §41.5)
    if room_id == boss.arena_room_id:
        if defeated:
            return BossEvaluation(
                boss_id=boss.boss_id,
                name=boss.name,
                stage="defeated",
                message=boss.defeated_signal or "La arena permanece en calma. La bestia ha caído definitivamente.",
            )

        attempt = store.get_boss_attempt(db_path, boss.boss_id)
        current_hp = attempt["current_hp"] if attempt else float(boss.max_hp)
        phase = determine_current_phase(boss, current_hp)

        actions = [
            {"action": "atacar", "targets": [boss.boss_id]},
            {"action": "evaluar", "targets": [boss.boss_id]},
            {"action": "huir"},
            {"action": "esquivar"},
            {"action": "resistir"},
        ]

        return BossEvaluation(
            boss_id=boss.boss_id,
            name=boss.name,
            stage="arena",
            close_encounter=True,
            message=boss.close_signal or f"{boss.name} se alza en la arena. Su presencia domina todo el espacio.",
            current_hp=current_hp,
            max_hp=float(boss.max_hp),
            current_phase=phase.phase_index,
            available_actions=actions,
        )

    return None


def get_or_create_boss_attempt(
    db_path: str,
    boss: BossContract,
    player_id: str,
    now: Optional[float] = None,
) -> dict:
    """Obtiene el intento activo compartido o inicia uno nuevo a HP máximo (§41.3)."""
    now = now if now is not None else time.time()
    attempt = store.get_boss_attempt(db_path, boss.boss_id)
    if not attempt:
        store.save_boss_attempt(
            db_path,
            boss.boss_id,
            boss.arena_room_id,
            current_hp=float(boss.max_hp),
            current_phase=0,
            started_at=now,
            now=now,
        )
        attempt = store.get_boss_attempt(db_path, boss.boss_id)

    store.add_boss_participant(db_path, boss.boss_id, player_id, now=now)
    return attempt


def check_and_clear_attempt_if_wiped(db_path: str, boss_id: str) -> bool:
    """Si no quedan participantes vivos en la arena, concluye el intento con reset (§41.3, §41.12)."""
    boss = get_boss(boss_id)
    if not boss:
        return False
    participants = store.get_boss_participants(db_path, boss_id)
    if not participants:
        store.clear_boss_attempt(db_path, boss_id)
        return True

    # Comprobar si al menos un participante sigue vivo en la arena
    alive_in_arena = False
    for p in participants:
        char = store.character_by_player_id(db_path, p["player_id"])
        if char and char["room"] == boss.arena_room_id and char["hp_current"] > 0:
            alive_in_arena = True
            break

    if not alive_in_arena:
        store.clear_boss_attempt(db_path, boss_id)
        return True
    return False


def resolve_boss_attack_round(
    db_path: str,
    player: dict,
    boss: BossContract,
    rng: Optional[random.Random] = None,
    now: Optional[float] = None,
) -> dict:
    """Ejecuta una ronda de combate del jugador contra el jefe en la arena (§41.3, §41.5)."""
    player = dict(player)
    now = now if now is not None else time.time()
    if is_boss_defeated(db_path, boss.boss_id):
        return {"outcome": "no_target", "messages": ["El jefe ya ha sido derrotado."]}

    attempt = get_or_create_boss_attempt(db_path, boss, player["id"], now=now)
    current_hp = attempt["current_hp"]
    phase = determine_current_phase(boss, current_hp)

    # Atributos y equipo del jugador
    attrs = {name: player[f"attr_{name}"] for name in combat.ATTRIBUTES}
    weapon_key, armor_key = store.equipped_item_keys(
        db_path, player["equipped_weapon_id"], player["equipped_armor_id"]
    )
    weapon_data = items.get_item(weapon_key) if weapon_key else None
    armor_data = items.get_item(armor_key) if armor_key else None
    weapon_damage = weapon_data["base_damage"] if weapon_data else combat.BASE_ARMA
    armor_red = armor_data["armor_reduction"] if armor_data else 0.0
    cg_player = combat.competencia_general(player["level"])
    cg_boss = combat.competencia_general(10)  # Nivel de referencia de jefe

    wound = player["wound"]
    fatigue = min(
        100,
        player["fatigue"]
        + combat.fatigue_gained("ataque_basico", attrs["resistencia"], wound, armor_reduction=armor_red),
    )
    accuracy_penalty = combat.combined_accuracy_penalty(player["fatigue"], wound)
    damage_multiplier = combat.combined_damage_multiplier(player["fatigue"], wound)

    # 1. Ataque del jugador
    player_hits, player_damage = combat.resolve_attack_roll(
        attrs["destreza"],
        attrs["percepcion"],
        attrs["fuerza"],
        cg_player,
        cg_boss,
        rng=rng,
        base_arma=weapon_damage,
        accuracy_penalty=accuracy_penalty,
        damage_multiplier=damage_multiplier,
    )

    messages = []
    if player_hits:
        player_damage = combat.apply_armor_reduction(player_damage, phase.armor_reduction)
        messages.append(f"Golpeas a {boss.name} por {round(player_damage)} de daño.")
        store.update_boss_participant_damage(db_path, boss.boss_id, player["id"], player_damage)
    else:
        messages.append(f"Tu ataque no logra alcanzar a {boss.name}.")

    boss_new_hp = current_hp - player_damage

    # 2. Comprobar victoria (§41.2, §41.10)
    if boss_new_hp <= 0:
        return resolve_boss_victory(db_path, boss, player, messages=messages, now=now)

    # Guardar nuevo HP y verificar cambio de fase
    new_phase = determine_current_phase(boss, boss_new_hp)
    if new_phase.phase_index != phase.phase_index:
        messages.append(f"¡{boss.name} entra en cólera! {new_phase.description or 'Su conducta cambia drásticamente.'}")
    store.save_boss_attempt(
        db_path, boss.boss_id, boss.arena_room_id, boss_new_hp, new_phase.phase_index, now=now
    )

    # 3. Contragolpe del jefe (usando stats de la fase activa)
    boss_hits, boss_damage = combat.resolve_fixed_attack_roll(
        new_phase.precision, new_phase.damage, rng=rng
    )

    new_wound = wound
    if boss_hits:
        boss_damage = combat.apply_armor_reduction(boss_damage, armor_red)
        messages.append(f"{boss.name} te asesta un golpe tremendo por {round(boss_damage)} de daño.")
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(boss_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
    else:
        messages.append(f"{boss.name} falla su ataque.")

    player_hp = player["hp_current"] - (boss_damage if boss_hits else 0)

    # 4. Comprobar derrota del jugador (§41.6, §41.7)
    if player_hp <= 0:
        return resolve_boss_player_defeat(db_path, player, boss, messages=messages, now=now)

    # Personaje sigue en pie
    store.update_combat_state(
        db_path, player["id"], hp_current=round(player_hp), fatigue=round(fatigue), wound=new_wound
    )
    return {"outcome": "ongoing", "messages": messages, "current_hp": boss_new_hp, "phase": new_phase.phase_index}


def resolve_boss_player_defeat(
    db_path: str,
    player: dict,
    boss: BossContract,
    messages: List[str] = None,
    now: Optional[float] = None,
) -> dict:
    """Resuelve la caída de un jugador ante el jefe C5 (§41.6, §41.7)."""
    player = dict(player)
    now = now if now is not None else time.time()
    messages = list(messages or [])
    messages.append(f"{boss.name} te asesta el golpe definitivo.")

    lost_weapon_info = None
    # §41.7: Pérdida de arma opt-in por jefe
    if boss.weapon_loss_on_defeat:
        equipped_weapon = player.get("equipped_weapon_id")
        if equipped_weapon:
            # Registrar pérdida persistente y desequipar
            store.record_lost_weapon(db_path, player["id"], equipped_weapon, boss.boss_id, now=now)
            messages.append(f"¡{boss.name} hace pedazos tu guardia y tu arma cae arrebatada!")
            lost_weapon_info = equipped_weapon
        else:
            # §41.9: Sin arma equipada: no sustituye la penalización por armadura, inventario, etc.
            messages.append("No llevabas ningún arma que el jefe pudiera arrebatar.")

    # Muerte y respawn canónicos (60% HP, 40 fatiga, herida degradada 1 grado, lugar seguro)
    respawn = combat.respawn_state(player["hp_max"])
    respawn_wound = combat.respawn_wound(player.get("wound", "ninguna"))
    store.update_combat_state(
        db_path,
        player["id"],
        hp_current=respawn["hp_current"],
        fatigue=respawn["fatigue"],
        wound=respawn_wound,
    )
    safe_room = world.get_room("valdren_centro")
    safe_room_name = safe_room["name"] if safe_room else "un lugar seguro"
    store.move_player(db_path, player["id"], "valdren_centro", None)
    messages.append(f"Vuelves en ti en {safe_room_name}.")
    messages.append("Conservas tu equipo e inventario." if not lost_weapon_info else "Conservas el resto de tu equipo e inventario.")

    # Comprobar si todos los participantes cayeron para reiniciar intento (§41.3, §41.12)
    check_and_clear_attempt_if_wiped(db_path, boss.boss_id)

    return {
        "outcome": "defeat",
        "messages": messages,
        "weapon_lost": bool(lost_weapon_info),
        "death_event": {
            "heading": "HAS MUERTO",
            "combat_messages": messages,
            "defeat_message": f"{boss.name} te derrota.",
            "fall_message": "Caes al suelo desprovisto de fuerzas.",
            "respawn_message": f"Vuelves en ti en {safe_room_name}.",
            "preservation_message": "Conservas tu equipo e inventario." if not lost_weapon_info else "Conservas el resto de tu equipo e inventario.",
        },
    }


def resolve_boss_player_flee(
    db_path: str,
    player: dict,
    boss: BossContract,
    rng: Optional[random.Random] = None,
    now: Optional[float] = None,
) -> dict:
    """Resuelve el intento de huida de la arena del jefe (§41.4)."""
    player = dict(player)
    now = now if now is not None else time.time()
    if not boss.flee_possible:
        return {"outcome": "blocked", "messages": [f"Es imposible huir de la presencia de {boss.name}."]}

    attrs = {name: player[f"attr_{name}"] for name in combat.ATTRIBUTES}
    chance = combat.flee_chance(
        attrs["agilidad"],
        attrs["percepcion"],
        boss.flee_agilidad,
        boss.flee_percepcion,
        attacker_level_advantage=10 - player["level"],
        previous_failed_attempts=0,
        fatigue=player["fatigue"],
    )
    rng = rng or random.Random()
    success = rng.uniform(0, 100) < chance

    if success:
        # Huida exitosa: el jugador retrocede a entry_room_id
        store.move_player(db_path, player["id"], boss.entry_room_id, None)
        check_and_clear_attempt_if_wiped(db_path, boss.boss_id)
        return {
            "outcome": "success",
            "messages": [f"Logras zafarte del alcance de {boss.name} y huyes a terreno seguro."],
        }

    # Huida fallida: el jefe conecta un contragolpe
    attempt = store.get_boss_attempt(db_path, boss.boss_id)
    current_hp = attempt["current_hp"] if attempt else float(boss.max_hp)
    phase = determine_current_phase(boss, current_hp)

    boss_hits, boss_damage = combat.resolve_fixed_attack_roll(phase.precision, phase.damage, rng=rng)
    wound = player["wound"]
    messages = ["Intentas huir pero la bestia te corta el paso."]
    if boss_hits:
        weapon_key, armor_key = store.equipped_item_keys(
            db_path, player["equipped_weapon_id"], player["equipped_armor_id"]
        )
        armor_data = items.get_item(armor_key) if armor_key else None
        armor_red = armor_data["armor_reduction"] if armor_data else 0.0
        boss_damage = combat.apply_armor_reduction(boss_damage, armor_red)
        messages.append(f"{boss.name} te alcanza en la retirada por {round(boss_damage)} de daño.")
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(boss_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
    else:
        new_wound = wound
        messages.append(f"{boss.name} intenta alcanzarte pero falla.")

    player_hp = player["hp_current"] - (boss_damage if boss_hits else 0)
    if player_hp <= 0:
        return resolve_boss_player_defeat(db_path, player, boss, messages=messages, now=now)

    store.update_combat_state(db_path, player["id"], hp_current=round(player_hp), wound=new_wound)
    return {"outcome": "failed", "messages": messages}


def resolve_boss_victory(
    db_path: str,
    boss: BossContract,
    killer_player: dict,
    messages: List[str] = None,
    now: Optional[float] = None,
) -> dict:
    """Marca la victoria del mundo y distribuye recompensas con filtro de contribución (§41.10, §41.11)."""
    killer_player = dict(killer_player)
    now = now if now is not None else time.time()
    messages = list(messages or [])
    messages.append(f"¡{boss.name} lanza un estertor desgarrador y se desploma sin vida!")
    messages.append("El mundo ha sido liberado de esta gran amenaza.")

    # 1. Marcar derrota persistente y compartida en el mundo (§41.2)
    store.set_world_boss_defeated(db_path, boss.boss_id, defeated=True, now=now)

    # 2. Distribución de recompensas autorizadas (§41.10, §41.11)
    participants = store.get_boss_participants(db_path, boss.boss_id)
    participants_by_id = {p["player_id"]: p for p in participants}

    for reward in boss.rewards:
        if reward.scope == "world":
            # Recompensa global: solo se cobra una vez en el mundo
            if not store.is_boss_reward_claimed(db_path, boss.boss_id, "world", None, reward.reward_key):
                store.record_boss_reward_claimed(db_path, boss.boss_id, "world", None, reward.reward_key, now=now)
                # Si otorga descubrimiento o flag al mundo
                if reward.reward_type == "discovery":
                    disc = world.get_discovery(reward.target)
                    disc_cat = disc["category"] if disc and "category" in disc else "hito_narrativo_importante"
                    disc_ref = disc["reference_level"] if disc and "reference_level" in disc else 1
                    store.award_discovery(db_path, killer_player["id"], reward.target, disc_cat, disc_ref)
        elif reward.scope == "character":
            # Recompensa individual: solo para participantes con contribución significativa (§41.11)
            for pid, pdata in participants_by_id.items():
                if pdata["damage_dealt"] < boss.min_contribution_damage:
                    # Espectador sin contribución: no cobra (§41.11)
                    continue
                if not store.is_boss_reward_claimed(db_path, boss.boss_id, "character", pid, reward.reward_key):
                    store.record_boss_reward_claimed(db_path, boss.boss_id, "character", pid, reward.reward_key, now=now)
                    if reward.reward_type == "xp":
                        store.award_xp(db_path, pid, reward.amount)
                    elif reward.reward_type == "discovery":
                        disc = world.get_discovery(reward.target)
                        disc_cat = disc["category"] if disc and "category" in disc else "hito_narrativo_importante"
                        disc_ref = disc["reference_level"] if disc and "reference_level" in disc else 1
                        store.award_discovery(db_path, pid, reward.target, disc_cat, disc_ref)
                    elif reward.reward_type == "item":
                        store.grant_item(db_path, pid, reward.target, forge_validated=True)

    # 3. Limpiar intento activo
    store.clear_boss_attempt(db_path, boss.boss_id)

    return {"outcome": "victory", "messages": messages}


def resolve_boss_dodge_round(
    db_path: str,
    player: dict,
    boss: BossContract,
    rng: Optional[random.Random] = None,
    now: Optional[float] = None,
) -> dict:
    """Resuelve la acción defensiva esquivar contra el ataque del jefe."""
    player = dict(player)
    now = now if now is not None else time.time()
    if is_boss_defeated(db_path, boss.boss_id):
        return {"outcome": "no_target", "messages": ["El jefe ya ha sido derrotado."]}

    attempt = get_or_create_boss_attempt(db_path, boss, player["id"], now=now)
    current_hp = attempt["current_hp"]
    phase = determine_current_phase(boss, current_hp)

    attrs = {name: player[f"attr_{name}"] for name in combat.ATTRIBUTES}
    weapon_key, armor_key = store.equipped_item_keys(
        db_path, player["equipped_weapon_id"], player["equipped_armor_id"]
    )
    armor_data = items.get_item(armor_key) if armor_key else None
    armor_red = armor_data["armor_reduction"] if armor_data else 0.0

    wound = player["wound"]
    fatigue = min(
        100,
        player["fatigue"]
        + combat.fatigue_gained("esquivar", attrs["resistencia"], wound, armor_reduction=armor_red),
    )
    accuracy_penalty = combat.combined_accuracy_penalty(player["fatigue"], wound)
    rng = rng or random.Random()
    boss_hits, boss_damage = combat.resolve_dodged_attack_roll(
        phase.precision,
        phase.damage,
        attrs["agilidad"],
        attrs["percepcion"],
        accuracy_penalty=accuracy_penalty,
        rng=rng,
    )
    if not boss_hits:
        store.update_combat_state(db_path, player["id"], fatigue=round(fatigue))
        return {"outcome": "success", "messages": [f"Esquivas el ataque de {boss.name}."]}

    boss_damage = combat.apply_armor_reduction(boss_damage, armor_red)
    messages = [f"No logras esquivar y {boss.name} te golpea por {round(boss_damage)} de daño."]
    new_wound = combat.worse_wound(wound, combat.wound_from_hit(boss_damage, player["hp_max"]))
    if new_wound != wound:
        messages.append(f"Sufres una herida {new_wound}.")
    player_hp = player["hp_current"] - boss_damage
    if player_hp <= 0:
        return resolve_boss_player_defeat(db_path, player, boss, messages=messages, now=now)

    store.update_combat_state(
        db_path, player["id"], hp_current=round(player_hp), fatigue=round(fatigue), wound=new_wound
    )
    return {"outcome": "failed", "messages": messages}


def resolve_boss_resist_round(
    db_path: str,
    player: dict,
    boss: BossContract,
    rng: Optional[random.Random] = None,
    now: Optional[float] = None,
) -> dict:
    """Resuelve la acción defensiva resistir contra el ataque del jefe."""
    player = dict(player)
    now = now if now is not None else time.time()
    if is_boss_defeated(db_path, boss.boss_id):
        return {"outcome": "no_target", "messages": ["El jefe ya ha sido derrotado."]}

    attempt = get_or_create_boss_attempt(db_path, boss, player["id"], now=now)
    current_hp = attempt["current_hp"]
    phase = determine_current_phase(boss, current_hp)

    attrs = {name: player[f"attr_{name}"] for name in combat.ATTRIBUTES}
    weapon_key, armor_key = store.equipped_item_keys(
        db_path, player["equipped_weapon_id"], player["equipped_armor_id"]
    )
    armor_data = items.get_item(armor_key) if armor_key else None
    armor_red = armor_data["armor_reduction"] if armor_data else 0.0

    wound = player["wound"]
    fatigue = min(
        100,
        player["fatigue"]
        + combat.fatigue_gained("resistir", attrs["resistencia"], wound, armor_reduction=armor_red),
    )
    rng = rng or random.Random()
    boss_hits, boss_damage = combat.resolve_resisted_attack_roll(
        phase.precision, phase.damage, attrs["resistencia"], rng=rng
    )
    if not boss_hits:
        store.update_combat_state(db_path, player["id"], fatigue=round(fatigue))
        return {"outcome": "success", "messages": [f"Te preparas y {boss.name} falla su ataque."]}

    boss_damage = combat.apply_armor_reduction(boss_damage, armor_red)
    messages = [
        f"Resistes el golpe de {boss.name}, que aun así te hace {round(boss_damage)} de daño."
    ]
    new_wound = combat.worse_wound(wound, combat.wound_from_hit(boss_damage, player["hp_max"]))
    if new_wound != wound:
        messages.append(f"Sufres una herida {new_wound}.")
    player_hp = player["hp_current"] - boss_damage
    if player_hp <= 0:
        return resolve_boss_player_defeat(db_path, player, boss, messages=messages, now=now)

    store.update_combat_state(
        db_path, player["id"], hp_current=round(player_hp), fatigue=round(fatigue), wound=new_wound
    )
    return {"outcome": "failed", "messages": messages}


def resolve_boss_block_round(
    db_path: str,
    player: dict,
    boss: BossContract,
    rng: Optional[random.Random] = None,
    now: Optional[float] = None,
) -> dict:
    """Resuelve la acción defensiva bloquear contra el ataque del jefe."""
    player = dict(player)
    now = now if now is not None else time.time()
    if is_boss_defeated(db_path, boss.boss_id):
        return {"outcome": "no_target", "messages": ["El jefe ya ha sido derrotado."]}

    weapon_key, armor_key = store.equipped_item_keys(
        db_path, player["equipped_weapon_id"], player["equipped_armor_id"]
    )
    weapon_data = items.get_item(weapon_key) if weapon_key else None
    if not (weapon_data and weapon_data.get("can_block")):
        return {"outcome": "unavailable", "messages": ["Todavía no tienes equipo adecuado para bloquear."]}

    attempt = get_or_create_boss_attempt(db_path, boss, player["id"], now=now)
    current_hp = attempt["current_hp"]
    phase = determine_current_phase(boss, current_hp)

    attrs = {name: player[f"attr_{name}"] for name in combat.ATTRIBUTES}
    armor_data = items.get_item(armor_key) if armor_key else None
    armor_red = armor_data["armor_reduction"] if armor_data else 0.0

    wound = player["wound"]
    fatigue = min(
        100,
        player["fatigue"]
        + combat.fatigue_gained("bloquear", attrs["resistencia"], wound, armor_reduction=armor_red),
    )
    rng = rng or random.Random()
    boss_hits, boss_damage = combat.resolve_blocked_attack_roll(
        phase.precision, phase.damage, attrs["destreza"], rng=rng
    )
    if not boss_hits:
        store.update_combat_state(db_path, player["id"], fatigue=round(fatigue))
        return {"outcome": "success", "messages": [f"Bloqueas el ataque de {boss.name}."]}

    boss_damage = combat.apply_armor_reduction(boss_damage, armor_red)
    messages = [
        f"Bloqueas parcialmente a {boss.name}, que aun así te hace {round(boss_damage)} de daño."
    ]
    new_wound = combat.worse_wound(wound, combat.wound_from_hit(boss_damage, player["hp_max"]))
    if new_wound != wound:
        messages.append(f"Sufres una herida {new_wound}.")
    player_hp = player["hp_current"] - boss_damage
    if player_hp <= 0:
        return resolve_boss_player_defeat(db_path, player, boss, messages=messages, now=now)

    store.update_combat_state(
        db_path, player["id"], hp_current=round(player_hp), fatigue=round(fatigue), wound=new_wound
    )
    return {"outcome": "failed", "messages": messages}
