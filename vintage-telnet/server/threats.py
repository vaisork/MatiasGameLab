"""Motor de amenazas regionales C3 v1 (GAMEPLAY §40 / REGIONAL_THREAT_PROFILES.md / Issue #335).

C3 representa amenazas superiores regionales (Cornalomo, Rasgacumbres, Quebrarrocas,
Dorsalodo, Rasgacorteza) que operan fuera de los pools C1 ordinarios.
Reglas clave:
- threat_zone_id obligatorio con salas de advertencia y salas de proximidad crítica.
- Advertencia obligatoria: NUNCA inicia desde estado 'unknown' (§40.3).
- Proximidad crítica ('close'): NO inicia combate forzado; ofrece decisión:
  evitar/retroceder, observar/evaluar o iniciar/atacar (§40.4).
- Cooldown anti-spam de 30 minutos reales (1800s) tras resolución (§40.6):
  evitar, huir, victoria, derrota o abandono de zona.
- Reutiliza combate e infraestructura normal (§36, §40.7).
- Derrota conserva equipo e inventario (§40.9).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random
import time
from typing import Any, Dict, List, Optional, Set

from . import creatures, store

# Cooldown por defecto: 30 minutos reales = 1800 segundos (§40.6)
DEFAULT_THREAT_COOLDOWN_SECONDS: float = 1800.0

# Perfiles de probabilidad canónicos (§40.5)
THREAT_PRESENCE_CHANCES: Dict[str, float] = {
    "threat_scripted": 1.0,
    "threat_rare": 0.10,
    "threat_uncommon": 0.20,
}


@dataclass
class ThreatZone:
    threat_zone_id: str
    region: str
    creature_id: str
    warning_rooms: Set[str]
    encounter_rooms: Set[str]
    cooldown_seconds: float = DEFAULT_THREAT_COOLDOWN_SECONDS
    presence_mode: str = "threat_rare"
    warning_signal: str = "Un rastro inquietante en el terreno delata la presencia cercana de algo grande."
    close_signal: str = "Una silueta masiva e imponente domina el paso frente a ti."
    inactive_trail_signal: str = "Percibes huellas y marcas antiguas en el terreno, pero la criatura no está aquí ahora."


@dataclass
class ThreatEvaluation:
    zone_id: str
    creature_id: str
    stage: str  # "warning", "close", "cooldown", "none"
    message: Optional[str] = None
    close_encounter: bool = False
    cooldown_active: bool = False
    available_actions: List[Dict[str, Any]] = field(default_factory=list)


# Registro de zonas de amenaza C3 configuradas en el servidor
_REGISTERED_THREAT_ZONES: Dict[str, ThreatZone] = {}


def register_threat_zone(zone: ThreatZone) -> None:
    """Registra una zona de amenaza C3."""
    _REGISTERED_THREAT_ZONES[zone.threat_zone_id] = zone


def get_threat_zone(threat_zone_id: str) -> Optional[ThreatZone]:
    """Obtiene una zona de amenaza por su ID."""
    return _REGISTERED_THREAT_ZONES.get(threat_zone_id)


def get_all_threat_zones() -> List[ThreatZone]:
    """Devuelve todas las zonas de amenaza registradas."""
    return list(_REGISTERED_THREAT_ZONES.values())


def get_threat_zones_for_room(room_id: str) -> List[ThreatZone]:
    """Devuelve las zonas de amenaza asociadas a una sala (warning o encounter)."""
    return [
        z for z in _REGISTERED_THREAT_ZONES.values()
        if room_id in z.warning_rooms or room_id in z.encounter_rooms
    ]


def clear_threat_zones() -> None:
    """Limpia el registro de zonas (para pruebas o reset)."""
    _REGISTERED_THREAT_ZONES.clear()


def reset_threat_zones() -> None:
    """Alias para clear_threat_zones."""
    clear_threat_zones()


def load_canonical_threat_zones() -> None:
    """Carga las zonas de amenaza canónicas iniciales aprobadas (Edran/Cornalomo)."""
    clear_threat_zones()
    register_threat_zone(
        ThreatZone(
            threat_zone_id="tz_edran_cornalomo",
            region="edran",
            creature_id="cornalomo",
            warning_rooms={"valdren_pastos_altos"},
            encounter_rooms={"valdren_pastos_cornalomo"},
            cooldown_seconds=DEFAULT_THREAT_COOLDOWN_SECONDS,
            presence_mode="threat_scripted",
            warning_signal="El suelo tiembla ligeramente y la hierba alta aplastada delata el paso de un animal enorme.",
            close_signal="Un Cornalomo sacude su cresta ósea entre los pastos altos. Te mira de frente, evaluando si te retiras.",
            inactive_trail_signal="La hierba muestra señales de pisadas aplastadas, pero el Cornalomo se ha alejado por ahora.",
        )
    )


def evaluate_room_threat(
    db_path: str,
    player_id: str,
    room_id: str,
    now: Optional[float] = None,
    rng: Optional[random.Random] = None,
) -> Optional[ThreatEvaluation]:
    """Evalúa la presencia de amenazas regionales C3 al entrar en una sala.

    Cumple rigurosamente las reglas de GAMEPLAY §40:
    - No C3 desde estado 'unknown' (§40.3).
    - Proximidad crítica ('close') no inicia combate forzado; ofrece decisión (§40.4).
    - Cooldown anti-spam de 30 minutos reales por personaje y zona (§40.6).
    - No mezclar dos amenazas C3 en la misma sala (§40.10).
    """
    if now is None:
        now = time.time()

    zones = get_threat_zones_for_room(room_id)
    if not zones:
        return None

    # REGLA §40.10: Un solo evento C3 por sala
    zone = zones[0]

    record = store.get_threat_state(db_path, player_id, zone.threat_zone_id)
    current_state = record["state"] if record else "unknown"
    cooldown_until = record["cooldown_until"] if record else None

    # Comprobación de cooldown activo (§40.6)
    if cooldown_until is not None and cooldown_until > now:
        return ThreatEvaluation(
            zone_id=zone.threat_zone_id,
            creature_id=zone.creature_id,
            stage="cooldown",
            cooldown_active=True,
            message=zone.inactive_trail_signal,
        )

    # 1. Sala de advertencia (§40.3)
    if room_id in zone.warning_rooms:
        if current_state != "warned":
            store.set_threat_state(db_path, player_id, zone.threat_zone_id, "warned", now=now)
        return ThreatEvaluation(
            zone_id=zone.threat_zone_id,
            creature_id=zone.creature_id,
            stage="warning",
            message=zone.warning_signal,
        )

    # 2. Sala de proximidad crítica / encuentro (§40.3, §40.4)
    if room_id in zone.encounter_rooms:
        # REGLA §40.3: NUNCA iniciar desde 'unknown' sin advertencia previa
        if current_state == "unknown":
            return ThreatEvaluation(
                zone_id=zone.threat_zone_id,
                creature_id=zone.creature_id,
                stage="none",
                message=None,
            )

        # Si el jugador ya fue advertido ('warned' o ya estaba en 'close')
        if current_state in ("warned", "close"):
            trigger = True
            if current_state == "warned":
                chance = THREAT_PRESENCE_CHANCES.get(zone.presence_mode, 0.10)
                roll = rng.random() if rng else random.random()
                trigger = (roll < chance)

            if trigger:
                store.set_threat_state(db_path, player_id, zone.threat_zone_id, "close", now=now)
                # REGLA §40.4: Ofrecer decisiones explícitas: evitar/retroceder, observar/evaluar o iniciar/atacar
                return ThreatEvaluation(
                    zone_id=zone.threat_zone_id,
                    creature_id=zone.creature_id,
                    stage="close",
                    close_encounter=True,
                    message=zone.close_signal,
                    available_actions=[
                        {"action": "atacar", "targets": [zone.creature_id]},
                        {"action": "evaluar", "targets": [zone.creature_id]},
                        {"action": "evitar"},
                    ],
                )
            else:
                # Roll fallido: rastro ≠ aparición garantizada (§40.5)
                return ThreatEvaluation(
                    zone_id=zone.threat_zone_id,
                    creature_id=zone.creature_id,
                    stage="warning",
                    message="Señales frescas marcan la zona, pero la criatura no se deja ver de momento.",
                )

    return None


def resolve_threat_avoid(
    db_path: str,
    player_id: str,
    threat_zone_id: str,
    now: Optional[float] = None,
) -> float:
    """Resuelve la retirada/evasión ante una amenaza en proximidad crítica (§40.4, §40.6).
    Activa cooldown de 30 minutos reales."""
    if now is None:
        now = time.time()
    zone = get_threat_zone(threat_zone_id)
    cooldown_secs = zone.cooldown_seconds if zone else DEFAULT_THREAT_COOLDOWN_SECONDS
    cooldown_until = now + cooldown_secs
    store.set_threat_state(db_path, player_id, threat_zone_id, "resolved", cooldown_until=cooldown_until, now=now)
    return cooldown_until


def resolve_threat_combat_end(
    db_path: str,
    player_id: str,
    threat_zone_id: str,
    outcome: str,  # "victory", "flee", "defeat"
    now: Optional[float] = None,
) -> float:
    """Activa cooldown de 30 minutos reales al terminar el combate C3 (§40.6, §40.8, §40.9)."""
    if now is None:
        now = time.time()
    zone = get_threat_zone(threat_zone_id)
    cooldown_secs = zone.cooldown_seconds if zone else DEFAULT_THREAT_COOLDOWN_SECONDS
    cooldown_until = now + cooldown_secs
    store.set_threat_state(db_path, player_id, threat_zone_id, "resolved", cooldown_until=cooldown_until, now=now)
    return cooldown_until


def get_room_threat_view(
    db_path: str,
    player_id: str,
    room_id: str,
    now: Optional[float] = None,
) -> Optional[ThreatEvaluation]:
    """Consulta de sólo lectura del estado de amenaza en una sala (para room_view).
    No realiza tiradas de dados ni altera el estado de la BD.
    """
    if now is None:
        now = time.time()

    zones = get_threat_zones_for_room(room_id)
    if not zones:
        return None

    zone = zones[0]
    record = store.get_threat_state(db_path, player_id, zone.threat_zone_id)
    current_state = record["state"] if record else "unknown"
    cooldown_until = record["cooldown_until"] if record else None

    # Comprobación de cooldown activo (§40.6)
    if cooldown_until is not None and cooldown_until > now:
        return ThreatEvaluation(
            zone_id=zone.threat_zone_id,
            creature_id=zone.creature_id,
            stage="cooldown",
            cooldown_active=True,
            message=zone.inactive_trail_signal,
        )

    # 1. Sala de advertencia (§40.3)
    if room_id in zone.warning_rooms:
        return ThreatEvaluation(
            zone_id=zone.threat_zone_id,
            creature_id=zone.creature_id,
            stage="warning",
            message=zone.warning_signal,
        )

    # 2. Sala de proximidad crítica / encuentro (§40.3, §40.4)
    if room_id in zone.encounter_rooms:
        if current_state == "close":
            return ThreatEvaluation(
                zone_id=zone.threat_zone_id,
                creature_id=zone.creature_id,
                stage="close",
                close_encounter=True,
                message=zone.close_signal,
                available_actions=[
                    {"action": "atacar", "targets": [zone.creature_id]},
                    {"action": "evaluar", "targets": [zone.creature_id]},
                    {"action": "evitar"},
                ],
            )
        elif current_state == "warned":
            return ThreatEvaluation(
                zone_id=zone.threat_zone_id,
                creature_id=zone.creature_id,
                stage="warning",
                message="Señales frescas marcan la zona, pero la criatura no se deja ver de momento.",
            )

    return None


# Carga canónica inicial al importar
load_canonical_threat_zones()

