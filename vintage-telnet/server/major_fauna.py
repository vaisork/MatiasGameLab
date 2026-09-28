"""Motor reutilizable de Fauna Mayor C4 (Issue #336 / GAMEPLAY §38).

Contrato autoritativo (GAMEPLAY §38, §330, §339, §358):
1. Fauna Mayor NO es jefe, NO es única, NO activa pérdida de arma ni otorga trofeos especiales.
2. Sin escalado automático: estadísticas fijas por especie y nivel de referencia.
3. Territorio en tres anillos:
   - Anillo I (borde): rastros físicos, cambio leve en fauna, 0 combate forzado, retirada libre.
   - Anillo II (territorio activo): señales recientes, avistamiento lejano posible si está presente,
     0 combate forzado, retirada disponible antes de compromiso.
   - Anillo III (proximidad crítica): última señal inequívoca, decisión real previa del jugador
     (observar/evaluar, retirarse sin penalización, o provocar/iniciar combate). NUNCA emboscada automática.
4. Presencia compartida de referencia por fase global (major_epoch de 30 minutos: floor(now / 1800)):
   - Estado determinista por major_epoch + zone_id.
   - Probabilidad de presencia configurable (piloto Cargallanura = 40%).
   - Mismo resultado para todos los jugadores en esa fase; entrar/salir/reconnect no rerollea.
5. Acciones preparadas e intención (GAMEPLAY §36, §38.8):
   - Carga comprometida (cargallanura_charge): frontal=True, interruptible=True, precisión 70%, daño 38.
   - Emite señal previa (telegraph) y concede una intervención de respuesta.
6. Huida y control de espacio:
   - Huida exitosa corta la persecución; no persigue a través de múltiples salas.
7. Derrota del jugador:
   - Respawn normal; NO pérdida de arma ni equipo (GAMEPLAY §38.5).
8. Derrota de la criatura:
   - XP de familia normal con antifarmeo regular (nivel de referencia 12); no drop de jefe ni trofeo.
   - Registro de estado por epoch para evitar farmeo repetitivo inmediato.
9. No entra en pools aleatorios ordinarios C1 ni C2 (GAMEPLAY §38.10).
"""
from dataclasses import dataclass, field
import hashlib
import logging
import math
import random
import time
from typing import Any, Optional

from . import combat, creatures, encounters, items, respawn as respawn_logic, store, world

logger = logging.getLogger(__name__)

DEFAULT_MAJOR_EPOCH_SECONDS = 1800  # 30 minutos (GAMEPLAY §38 / Issue #358)


@dataclass
class PreparedActionDef:
    action_id: str
    name: str
    frontal: bool = True
    interruptible: bool = True
    precision: int = 70
    damage: int = 38
    telegraph_text: str = ""
    resolution_text: str = ""
    interrupted_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "name": self.name,
            "frontal": self.frontal,
            "interruptible": self.interruptible,
            "precision": self.precision,
            "damage": self.damage,
            "telegraph_text": self.telegraph_text,
            "resolution_text": self.resolution_text,
            "interrupted_text": self.interrupted_text,
        }


@dataclass
class MajorFaunaPhase:
    phase_id: str
    name: str
    hp_threshold_pct: float  # e.g. 1.0 para inicial, 0.4 para enfurecida
    precision: int
    damage: int
    prepared_action_id: Optional[str] = None
    flavor_text: str = ""


@dataclass
class MajorFaunaSpec:
    creature_id: str
    name: str
    family: str
    reference_level: int = 12
    hp: int = 210
    precision: int = 58
    damage: int = 26
    armor_reduction: float = 0.25
    flee_agilidad: int = 10
    flee_percepcion: int = 12
    behavior_text: str = ""
    phases: list[MajorFaunaPhase] = field(default_factory=list)
    prepared_actions: dict[str, PreparedActionDef] = field(default_factory=dict)
    flee_terminates_pursuit: bool = True
    no_weapon_loss: bool = True
    no_boss_reward: bool = True

    def get_phase_for_hp(self, current_hp: float) -> MajorFaunaPhase:
        if not self.phases:
            return MajorFaunaPhase(
                phase_id="base",
                name="Base",
                hp_threshold_pct=1.0,
                precision=self.precision,
                damage=self.damage,
            )
        hp_pct = max(0.0, current_hp / max(1, self.hp))
        # Ordenadas de menor a mayor umbral
        sorted_phases = sorted(self.phases, key=lambda p: p.hp_threshold_pct)
        for phase in sorted_phases:
            if hp_pct <= phase.hp_threshold_pct:
                return phase
        return sorted_phases[-1]


@dataclass
class MajorFaunaZone:
    zone_id: str
    species_id: str
    ring_1_rooms: list[str]  # Borde: rastros, 0 combate forzado, retirada libre
    ring_2_rooms: list[str]  # Territorio activo: señales recientes, avistamiento si presente
    ring_3_rooms: list[str]  # Proximidad crítica: decisión real antes de combate
    presence_probability: float = 0.40
    epoch_seconds: int = DEFAULT_MAJOR_EPOCH_SECONDS
    cooldown_seconds: int = DEFAULT_MAJOR_EPOCH_SECONDS
    signals: dict[str, Any] = field(default_factory=dict)


class MajorFaunaRegistry:
    def __init__(self):
        self._specs: dict[str, MajorFaunaSpec] = {}
        self._zones: dict[str, MajorFaunaZone] = {}

    def register_spec(self, spec: MajorFaunaSpec) -> None:
        self._specs[spec.creature_id] = spec

    def register_zone(self, zone: MajorFaunaZone) -> None:
        self._zones[zone.zone_id] = zone

    def get_spec(self, creature_id: str) -> Optional[MajorFaunaSpec]:
        return self._specs.get(creature_id)

    def get_zone(self, zone_id: str) -> Optional[MajorFaunaZone]:
        return self._zones.get(zone_id)

    def get_zone_for_room(self, room_id: str) -> Optional[MajorFaunaZone]:
        if not room_id:
            return None
        for zone in self._zones.values():
            if (
                room_id in zone.ring_1_rooms
                or room_id in zone.ring_2_rooms
                or room_id in zone.ring_3_rooms
            ):
                return zone
        return None

    def list_specs(self) -> list[MajorFaunaSpec]:
        return list(self._specs.values())

    def list_zones(self) -> list[MajorFaunaZone]:
        return list(self._zones.values())

    def reset(self) -> None:
        self._specs.clear()
        self._zones.clear()
        if "CARGALLANURA_SPEC" in globals():
            self.register_spec(globals()["CARGALLANURA_SPEC"])
        if "EDRAN_CORREDOR_CARGALLANURA_ZONE" in globals():
            self.register_zone(globals()["EDRAN_CORREDOR_CARGALLANURA_ZONE"])


_REGISTRY = MajorFaunaRegistry()


def get_registry() -> MajorFaunaRegistry:
    return _REGISTRY


# ---------------------------------------------------------------------------
# Algoritmo determinista de presencia por epoch global (GAMEPLAY §38 / Issue #358)
# ---------------------------------------------------------------------------

def get_major_epoch(now: Optional[float] = None, epoch_seconds: int = DEFAULT_MAJOR_EPOCH_SECONDS) -> int:
    """Devuelve la fase global actual (major_epoch = floor(unix_time / epoch_seconds))."""
    t = now if now is not None else time.time()
    return int(t // max(1, epoch_seconds))


def is_major_fauna_present(
    zone_or_id: MajorFaunaZone | str,
    now: Optional[float] = None,
    db_path: Optional[str] = None,
) -> bool:
    """Calcula de forma 100% determinista si la fauna mayor está físicamente presente
    en la zona durante la epoch actual.

    Invariantes:
    - Mismo resultado para todos los jugadores en la misma fase de 30 minutos.
    - Entrar, salir, recargar o reconectar no rerollea el resultado.
    - Si la criatura fue derrotada en esta misma epoch, permanece ausente (cooldown).
    """
    zone = zone_or_id if isinstance(zone_or_id, MajorFaunaZone) else _REGISTRY.get_zone(zone_or_id)
    if not zone:
        return False

    epoch = get_major_epoch(now=now, epoch_seconds=zone.epoch_seconds)

    # Cooldown tras derrota en la misma epoch
    if db_path:
        state = store.get_major_fauna_state(db_path, zone.zone_id)
        if state and state.get("last_defeated_epoch") == epoch:
            return False

    # Cálculo pseudoaleatorio determinista por semilla (zone_id + epoch)
    seed_str = f"major_fauna:{zone.zone_id}:{epoch}"
    digest = hashlib.sha256(seed_str.encode("utf-8")).hexdigest()
    # Tomar los primeros 8 caracteres hexadecimales como entero normalizado [0, 1)
    val = int(digest[:8], 16) / 0xFFFFFFFF
    return val < zone.presence_probability


def get_room_ring(zone: MajorFaunaZone, room_id: str) -> Optional[int]:
    """Devuelve el anillo territorial de la sala dentro de la zona (1, 2, 3 o None)."""
    if room_id in zone.ring_1_rooms:
        return 1
    if room_id in zone.ring_2_rooms:
        return 2
    if room_id in zone.ring_3_rooms:
        return 3
    return None


def get_zone_view_data(
    room_id: str,
    now: Optional[float] = None,
    db_path: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """Devuelve la información ambiental y opciones de interacción de fauna mayor
    para la sala dada. Cumple estrictamente el contrato de los 3 anillos."""
    zone = _REGISTRY.get_zone_for_room(room_id)
    if not zone:
        return None

    ring = get_room_ring(zone, room_id)
    if not ring:
        return None

    spec = _REGISTRY.get_spec(zone.species_id)
    present = is_major_fauna_present(zone, now=now, db_path=db_path)
    signals = zone.signals

    if ring == 1:
        # Anillo I — Borde
        sig = signals.get("ring_1", [
            "Huellas anchas de pisadas pesadas en la tierra batida.",
            "Hierba aplastada en los bordes del pastizal.",
        ])
        return {
            "zone_id": zone.zone_id,
            "species_id": zone.species_id,
            "species_name": spec.name if spec else "Fauna mayor",
            "ring": 1,
            "ring_name": "borde",
            "present": present,
            "forced_combat": False,
            "signals": sig if isinstance(sig, list) else [sig],
            "options": ["avanzar", "retirarse"],
        }
    elif ring == 2:
        # Anillo II — Territorio activo
        if present:
            sig = signals.get("ring_2_present", (
                "Un rastro ancho de hierba trillada y tierra removida avanza por el corredor. "
                "Se percibe a lo lejos una mole maciza en movimiento."
            ))
        else:
            sig = signals.get("ring_2_absent", (
                "Un rastro ancho de hierba trillada atraviesa el pasto, pero no se divisa "
                "movimiento reciente en la distancia."
            ))
        return {
            "zone_id": zone.zone_id,
            "species_id": zone.species_id,
            "species_name": spec.name if spec else "Fauna mayor",
            "ring": 2,
            "ring_name": "territorio_activo",
            "present": present,
            "forced_combat": False,
            "signals": [sig] if isinstance(sig, str) else sig,
            "options": ["avanzar", "retirarse"],
        }
    else:
        # Anillo III — Proximidad crítica
        if present:
            sig = signals.get("ring_3_present", (
                "A escasa distancia, la imponente silueta de una Cargallanura pasta atenta, "
                "ocupando el paso con calma territorial pero sin iniciar combate por simple presencia."
            ))
            options = ["observar", "retirarse", "provocar_combate"]
            decision_required = True
        else:
            sig = signals.get("ring_3_absent", (
                "Tierra recién escarbada y rastrojos aplastados indican que una bestia masiva "
                "estuvo aquí hace poco, pero el paso está momentáneamente despejado."
            ))
            options = ["avanzar", "retirarse"]
            decision_required = False

        return {
            "zone_id": zone.zone_id,
            "species_id": zone.species_id,
            "species_name": spec.name if spec else "Fauna mayor",
            "ring": 3,
            "ring_name": "proximidad_critica",
            "present": present,
            "forced_combat": False,
            "decision_required": decision_required,
            "signals": [sig] if isinstance(sig, str) else sig,
            "options": options,
        }


# ---------------------------------------------------------------------------
# Mecánica de Combate C4: Carga e Intervención (GAMEPLAY §38.8)
# ---------------------------------------------------------------------------

def evaluate_encounter_difficulty(player_level: int, spec: MajorFaunaSpec) -> str:
    """Evalúa la categoría de encuentro para un jugador frente a la fauna mayor.
    Un personaje nivel 1 siempre debe percibir a Cargallanura (ref 12, HP 210, Dmg 26)
    como 'abrumador'."""
    player_hp = combat.hp_max(player_level, 10, 10)
    player_dps = combat.expected_dps(10, 10, 10, 0, 0, base_arma=combat.BASE_ARMA)
    enemy_hp = spec.hp
    enemy_dps = (spec.precision / 100.0) * spec.damage
    return combat.encounter_category(player_dps, player_hp, enemy_dps, enemy_hp)


def resolve_major_fauna_charge_round(
    spec: MajorFaunaSpec,
    action_id: str,
    player_action: str = "esperar",  # "esperar" | "esquivar" | "bloquear" | "resistir" | "interrumpir"
    player_attrs: Optional[dict[str, int]] = None,
    rng: Optional[random.Random] = None,
) -> dict[str, Any]:
    """Resuelve la ejecución de una acción preparada (ej: cargallanura_charge).
    Concede una intervención de respuesta al jugador conforme a GAMEPLAY §38.8.

    Si el jugador usa 'interrumpir' (tiro técnico / golpe certero) o defensa activa,
    la carga puede ser mitigada, esquivada o completamente interrumpida."""
    action_def = spec.prepared_actions.get(action_id)
    if not action_def:
        # Fallback a golpe normal si la acción no está registrada
        return {
            "action_id": action_id,
            "interrupted": False,
            "hits": True,
            "damage": spec.damage,
            "message": f"{spec.name} arremete contra ti.",
        }

    rng = rng or random.Random()
    attrs = player_attrs or {name: 10 for name in combat.ATTRIBUTES}

    # Intervención por acción del jugador
    if player_action == "interrumpir" and action_def.interruptible:
        # Tiro técnico o interrupción de clase: tirada basada en destreza + percepción
        int_chance = 40 + (attrs.get("destreza", 10) - 10) * 2 + (attrs.get("percepcion", 10) - 10) * 2
        int_chance = max(20, min(80, int_chance))
        if rng.uniform(0, 100) < int_chance:
            return {
                "action_id": action_id,
                "interrupted": True,
                "hits": False,
                "damage": 0,
                "message": action_def.interrupted_text or f"¡Interrumpes la carga de {spec.name} a tiempo!",
            }

    if player_action == "esquivar":
        # Defensa activa esquivar
        hits, dmg = combat.resolve_dodged_attack_roll(
            action_def.precision, action_def.damage, attrs.get("agilidad", 10), attrs.get("percepcion", 10), rng=rng
        )
        if not hits:
            return {
                "action_id": action_id,
                "interrupted": False,
                "hits": False,
                "damage": 0,
                "message": f"Te apartas en el último instante y esquivas la embestida de {spec.name}.",
            }
        return {
            "action_id": action_id,
            "interrupted": False,
            "hits": True,
            "damage": dmg,
            "message": f"No logras esquivar completamente y sufres el impacto de {spec.name}.",
        }

    if player_action == "bloquear":
        hits, dmg = combat.resolve_blocked_attack_roll(
            action_def.precision, action_def.damage, attrs.get("destreza", 10), rng=rng
        )
        return {
            "action_id": action_id,
            "interrupted": False,
            "hits": hits,
            "damage": dmg,
            "message": f"Plantas defensa y absorbes parcialmente la carga de {spec.name}." if hits else f"Bloqueas limpiamente la embestida de {spec.name}.",
        }

    if player_action == "resistir":
        hits, dmg = combat.resolve_resisted_attack_roll(
            action_def.precision, action_def.damage, attrs.get("resistencia", 10), rng=rng
        )
        return {
            "action_id": action_id,
            "interrupted": False,
            "hits": hits,
            "damage": dmg,
            "message": f"Aguantas el impacto bruto de {spec.name}." if hits else f"{spec.name} no logra derribarte.",
        }

    # Resolución estándar sin defensa activa
    hits = rng.uniform(0, 100) < action_def.precision
    damage = action_def.damage if hits else 0
    return {
        "action_id": action_id,
        "interrupted": False,
        "hits": hits,
        "damage": damage,
        "message": action_def.resolution_text if hits else f"{spec.name} embiste con fuerza pero falla el golpe.",
    }


def resolve_major_fauna_flee(
    player: dict[str, Any],
    spec: MajorFaunaSpec,
    rng: Optional[random.Random] = None,
) -> dict[str, Any]:
    """Resuelve la huida del jugador frente a una fauna mayor (GAMEPLAY §38.4, §38.9).
    Una huida exitosa corta la persecución: la criatura NO persigue a través de múltiples salas."""
    rng = rng or random.Random()
    agilidad = player.get("attr_agilidad", 10)
    percepcion = player.get("attr_percepcion", 10)
    wound = player.get("wound", "ninguna")
    fatigue = player.get("fatigue", 0)

    penalty = combat.combined_accuracy_penalty(fatigue, wound)
    chance = combat.flee_chance(
        agilidad,
        percepcion,
        spec.flee_agilidad,
        spec.flee_percepcion,
        attacker_level_advantage=0,
        previous_failed_attempts=0,
        fatigue=fatigue,
    )
    success = rng.uniform(0, 100) < chance

    if success:
        return {
            "success": True,
            "pursuit_ended": True,
            "message": f"Logras romper el contacto con {spec.name} y ponerte a salvo. La criatura no te persigue.",
        }
    else:
        # Contraataque de oportunidad si la huida falla
        hits = rng.uniform(0, 100) < spec.precision
        dmg = spec.damage if hits else 0
        return {
            "success": False,
            "pursuit_ended": False,
            "counter_hits": hits,
            "damage": dmg,
            "message": f"No logras escapar de {spec.name} y sufres un golpe al retroceder." if hits else f"No logras escapar de {spec.name}, pero esquivas su ataque de oportunidad.",
        }


def resolve_major_fauna_player_defeat(
    db_path: str,
    player: dict[str, Any],
    spec: MajorFaunaSpec,
    current_wound: Optional[str] = None,
) -> dict[str, Any]:
    """Resuelve C4 con el mismo estado y routing canónicos de cualquier muerte."""
    player_id = player["id"]
    # Limpiar encounter activo, conservando el estado/cooldown C4 externo.
    with store.connect(db_path) as db:
        db.execute("DELETE FROM room_encounters WHERE player_id = ?", (player_id,))

    respawn_result = respawn_logic.apply_player_respawn(
        db_path,
        player,
        current_wound=current_wound if current_wound is not None else player.get("wound", "ninguna"),
        death_room_id=player.get("room"),
    )
    return {
        "outcome": "player_defeated",
        "weapon_lost": False,
        "equipment_preserved": True,
        "respawn_room": respawn_result["room_id"],
        "message": (
            f"{spec.name} te ha derribado con su masa implacable. "
            f"Vuelves en ti en {respawn_result['room_name']}."
        ),
    }


def resolve_major_fauna_defeat(
    db_path: str,
    player: dict[str, Any],
    spec: MajorFaunaSpec,
    zone: MajorFaunaZone,
    now: Optional[float] = None,
) -> dict[str, Any]:
    """Resuelve la victoria del jugador sobre la fauna mayor (GAMEPLAY §38.6).
    Invariantes estrictos:
    - XP de combate calculada por categoría (ref_level 12) con antifarmeo regular de familia.
    - NO loot especial automático, NO material de crafting, NO trofeo de jefe.
    - Registra el estado de la zona en SQLite para cooldown por epoch.
    """
    player_id = player["id"]
    current_time = now if now is not None else time.time()
    epoch = get_major_epoch(now=current_time, epoch_seconds=zone.epoch_seconds)

    # 1. Registrar cooldown de zona en la DB
    store.record_major_fauna_defeat(db_path, zone.zone_id, epoch, current_time)

    # 2. Concesión de XP normal de combate con antifarmeo
    player_level = player.get("level", 1)
    diff = evaluate_encounter_difficulty(player_level, spec)

    is_first, repeats = store.record_pve_victory(db_path, player_id, spec.family)
    xp_to_award = combat.combat_xp(
        enemy_ref_level=spec.reference_level,
        category=diff,
        player_level=player_level,
        is_first_family_victory=is_first,
        repeats_in_last_10=repeats,
        participants=1,
    )

    xp_state = store.award_xp(db_path, player_id, xp_to_award)

    return {
        "outcome": "creature_defeated",
        "xp_awarded": xp_to_award,
        "difficulty": diff,
        "boss_reward": False,
        "trophy_granted": False,
        "new_level": xp_state.get("new_level", player_level),
        "levels_gained": xp_state.get("levels_gained", 0),
        "message": f"Has abatido a {spec.name}. El pastizal vuelve al silencio.",
    }


# ---------------------------------------------------------------------------
# Definición canónica del piloto: Cargallanura v1 (GAMEPLAY §38.7 / Issue #339)
# ---------------------------------------------------------------------------

CARGALLANURA_CHARGE = PreparedActionDef(
    action_id="cargallanura_charge",
    name="Carga comprometida",
    frontal=True,
    interruptible=True,
    precision=70,
    damage=38,
    telegraph_text="Cargallanura se coloca de frente, baja la cabeza, fija las pezuñas y golpea el suelo con un resoplido sordo.",
    resolution_text="Cargallanura se lanza en una estampida frontal atronadora y te arrolla sin piedad.",
    interrupted_text="Una reacción decidida desvía la trayectoria de Cargallanura, haciendo que su carga pase de largo.",
)

CARGALLANURA_SPEC = MajorFaunaSpec(
    creature_id="cargallanura",
    name="Cargallanura",
    family="cargallanura",
    reference_level=12,
    hp=210,
    precision=58,
    damage=26,
    armor_reduction=0.25,
    flee_agilidad=10,
    flee_percepcion=12,
    behavior_text="Cargallanura resopla con lentitud y te evalúa con indiferencia territorial mientras mantengas la distancia.",
    phases=[
        MajorFaunaPhase(
            phase_id="cargallanura_fase_1",
            name="Territorial",
            hp_threshold_pct=1.0,
            precision=58,
            damage=26,
            prepared_action_id="cargallanura_charge",
            flavor_text="Cargallanura defiende su paso con calma pesada.",
        ),
        MajorFaunaPhase(
            phase_id="cargallanura_fase_2",
            name="Enfurecida",
            hp_threshold_pct=0.4,
            precision=64,
            damage=30,
            prepared_action_id="cargallanura_charge",
            flavor_text="Herida y acorralada, Cargallanura sacude la testa y embiste con furia ciega.",
        ),
    ],
    prepared_actions={
        "cargallanura_charge": CARGALLANURA_CHARGE,
    },
    flee_terminates_pursuit=True,
    no_weapon_loss=True,
    no_boss_reward=True,
)

# Zona canónica piloto: Corredor de Cargallanura (Issue #358 / PR #404 / PR #433)
EDRAN_CORREDOR_CARGALLANURA_ZONE = MajorFaunaZone(
    zone_id="edran_corredor_cargallanura",
    species_id="cargallanura",
    ring_1_rooms=[
        "edran_senda_viento_bajo",
        "edran_borde_cardos",
    ],
    ring_2_rooms=[
        "edran_cargallanura_paso_hierba",
        "edran_cargallanura_hondonada_trillada",
    ],
    ring_3_rooms=[
        "edran_cargallanura_corredor_central",
        "edran_cargallanura_varea_abierta",
    ],
    presence_probability=0.40,
    epoch_seconds=DEFAULT_MAJOR_EPOCH_SECONDS,
    cooldown_seconds=DEFAULT_MAJOR_EPOCH_SECONDS,
    signals={
        "ring_1": [
            "Huellas anchas y profundas de pezuñas hendidas marcan el pastizal aplastado.",
            "La fauna menor parece haber abandonado este tramo del camino.",
        ],
        "ring_2_present": (
            "Un sendero ancho de hierba trillada y tierra removida atraviesa la llanura. "
            "A la distancia se recorta la silueta maciza de una Cargallanura pastando atenta."
        ),
        "ring_2_absent": (
            "Un sendero ancho de hierba trillada atraviesa la llanura. La hierba está pisoteada "
            "pero no se divisa movimiento inmediato en el horizonte."
        ),
        "ring_3_present": (
            "A corta distancia, una Cargallanura de proporciones colosales ocupa el centro del paso. "
            "Baja la cabeza y resopla con lentitud, evaluando tu presencia sin iniciar combate inmediato."
        ),
        "ring_3_absent": (
            "Tierra recién escarbada y restos de matorral trinchado demuestran que la bestia frecuenta "
            "este paso estrecho, pero en este momento el paso permanece despejado."
        ),
    },
)

_REGISTRY.register_spec(CARGALLANURA_SPEC)
_REGISTRY.register_zone(EDRAN_CORREDOR_CARGALLANURA_ZONE)
