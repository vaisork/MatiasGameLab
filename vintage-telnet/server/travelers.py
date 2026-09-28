"""Mundo vivo ambiental — Sistema de NPCs viajeros N5-lite (Issue #338 / GAMEPLAY §39.11).

Contrato autoritativo (GAMEPLAY §39.11 / WORLD_POPULATION_CANON.md):
- Movimiento gobernado por el tiempo, nunca por acciones del jugador ni por LLM.
- Cadencia de referencia inicial: 10 minutos reales por paso (step_seconds = 600), configurable por NPC.
- Recorrido estricto sobre conexiones reales de la ruta (sin saltos ni teleport).
- Sin acceso a interiores privados, forjas, mercados ni mazmorras no autorizadas.
- Terminal de ruta:
  * "reverse": invierte el sentido al llegar al extremo (ida y vuelta continua).
  * "stop": se detiene en la última sala.
  * "vanish": desaparece al completar el trayecto.
- Persistencia:
  * Solo los NPCs con persistent_traveler=True registran y avanzan estado en SQLite.
  * Viajeros ambientales efímeros (persistent_traveler=False, como Loren) calculan su
    posición de forma 100% determinista a partir del tiempo y la ruta, sin queries a DB.
- Integración N1/N2:
  * Diálogo N1 con fallback canónico sobrio.
  * La presencia dinámica se refleja en room_view y permite la acción 'hablar'.
"""
from dataclasses import dataclass, field
import logging
import time
from typing import Any, Optional

from . import store

logger = logging.getLogger(__name__)

DEFAULT_STEP_SECONDS = 600  # 10 minutos por paso


@dataclass
class Traveler:
    npc_id: str
    name: str
    role: str
    species: str
    town: str
    route_id: str
    route: list[str]
    step_seconds: int = DEFAULT_STEP_SECONDS
    terminal: str = "reverse"  # "reverse" | "stop" | "vanish"
    persistent_traveler: bool = False
    pauses: list[str] = field(default_factory=list)
    fallback_dialogue: str = ""
    phrases: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.npc_id,
            "name": self.name,
            "role": self.role,
            "species": self.species,
            "town": self.town,
            "route_id": self.route_id,
            "is_traveler": True,
            "persistent_traveler": self.persistent_traveler,
            "fallback_dialogue": self.fallback_dialogue,
        }


def calculate_deterministic_position(
    route: list[str],
    step_seconds: int,
    terminal: str,
    now: float,
) -> tuple[Optional[str], int, int]:
    """Calcula matemáticamente la sala actual, el índice y la dirección (+1 o -1)
    de un viajero efímero sin consultar la base de datos."""
    n = len(route)
    if n == 0:
        return None, 0, 1
    if n == 1:
        return route[0], 0, 1

    steps = int(now // max(1, step_seconds))

    if terminal == "reverse":
        cycle_len = 2 * n - 2
        phase = steps % cycle_len
        if phase < n:
            return route[phase], phase, 1
        else:
            idx = (2 * n - 2) - phase
            return route[idx], idx, -1
    elif terminal == "stop":
        idx = min(steps, n - 1)
        return route[idx], idx, 1
    elif terminal == "vanish":
        if steps >= n:
            return None, steps, 1
        return route[steps], steps, 1
    else:
        # Loop circular por defecto
        idx = steps % n
        return route[idx], idx, 1


class TravelerRegistry:
    def __init__(self):
        self._travelers: dict[str, Traveler] = {}

    def register(self, traveler: Traveler) -> None:
        self._travelers[traveler.npc_id] = traveler

    def reset(self) -> None:
        self._travelers.clear()
        if "LOREN" in globals():
            self.register(globals()["LOREN"])

    def get(self, npc_id: str) -> Optional[Traveler]:
        return self._travelers.get(npc_id)

    def is_traveler(self, npc_id: str) -> bool:
        if not npc_id:
            return False
        clean = npc_id.strip().lower()
        return any(clean in (t.npc_id.lower(), t.name.lower()) for t in self._travelers.values())

    def get_by_name_or_id(self, target: str) -> Optional[Traveler]:
        if not target:
            return None
        clean = target.strip().lower()
        for t in self._travelers.values():
            if clean in (t.npc_id.lower(), t.name.lower()):
                return t
        return None

    def list_all(self) -> list[Traveler]:
        return list(self._travelers.values())

    def get_position(
        self,
        traveler_or_id: str | Traveler,
        now: Optional[float] = None,
        db_path: Optional[str] = None,
    ) -> Optional[str]:
        traveler = traveler_or_id if isinstance(traveler_or_id, Traveler) else self.get_by_name_or_id(traveler_or_id)
        if not traveler:
            return None

        current_time = now if now is not None else time.time()

        if not traveler.persistent_traveler:
            room, _idx, _dir = calculate_deterministic_position(
                traveler.route,
                traveler.step_seconds,
                traveler.terminal,
                current_time,
            )
            return room

        # Viajero persistente (con almacenamiento en store)
        if not db_path:
            room, _idx, _dir = calculate_deterministic_position(
                traveler.route,
                traveler.step_seconds,
                traveler.terminal,
                current_time,
            )
            return room

        state = store.get_traveler_state(db_path, traveler.npc_id)
        if not state:
            initial_room = traveler.route[0] if traveler.route else ""
            store.save_traveler_state(
                db_path,
                traveler.npc_id,
                traveler.route_id,
                initial_room,
                step_index=0,
                direction=1,
                last_step_time=current_time,
            )
            return initial_room

        # Avanzar según tiempo transcurrido
        elapsed = current_time - state["last_step_time"]
        steps_to_advance = int(elapsed // max(1, traveler.step_seconds))
        if steps_to_advance <= 0:
            return state["current_room"]

        route = traveler.route
        n = len(route)
        if n <= 1:
            return route[0] if n == 1 else None

        idx = state["step_index"]
        direction = state["direction"]

        for _ in range(steps_to_advance):
            if traveler.terminal == "reverse":
                next_idx = idx + direction
                if next_idx >= n:
                    direction = -1
                    next_idx = n - 2
                elif next_idx < 0:
                    direction = 1
                    next_idx = 1
                idx = next_idx
            elif traveler.terminal == "stop":
                idx = min(idx + 1, n - 1)
            elif traveler.terminal == "vanish":
                idx += 1
                if idx >= n:
                    break

        new_room = route[idx] if idx < n else None
        new_last_step = state["last_step_time"] + steps_to_advance * traveler.step_seconds
        store.save_traveler_state(
            db_path,
            traveler.npc_id,
            traveler.route_id,
            new_room or "",
            step_index=idx,
            direction=direction,
            last_step_time=new_last_step,
        )
        return new_room

    def get_in_room(
        self,
        room_id: str,
        now: Optional[float] = None,
        db_path: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        if not room_id:
            return []
        current_time = now if now is not None else time.time()
        present = []
        for traveler in self._travelers.values():
            pos = self.get_position(traveler, now=current_time, db_path=db_path)
            if pos == room_id:
                data = traveler.to_dict()
                data["location"] = pos
                present.append(data)
        return present


_REGISTRY = TravelerRegistry()


def get_registry() -> TravelerRegistry:
    return _REGISTRY


def get_travelers_in_room(room_id: str, now: Optional[float] = None, db_path: Optional[str] = None) -> list[dict[str, Any]]:
    return _REGISTRY.get_in_room(room_id, now=now, db_path=db_path)


def get_traveler_position(target: str, now: Optional[float] = None, db_path: Optional[str] = None) -> Optional[str]:
    return _REGISTRY.get_position(target, now=now, db_path=db_path)


def is_traveler(target: str) -> bool:
    return _REGISTRY.is_traveler(target)


# ---------------------------------------------------------------------------
# Definición canónica del piloto: Loren (Issue #338 / WORLD_POPULATION_CANON.md)
# ---------------------------------------------------------------------------
LOREN = Traveler(
    npc_id="viajero_loren",
    name="Loren",
    role="viajero de camino y mensajero informal entre Valdren y las rutas hacia Veyra",
    species="Humano",
    town="Valdren",
    route_id="valdren_camino_corto_01",
    route=[
        "valdren_centro",
        "valdren_sendero",
        "valdren_camino_parcela",
        "valdren_camino_cerca",
        "valdren_camino_lindero",
        "valdren_lindero_tres_piedras",
        "valdren_camino_hundido",
        "valdren_cobertizos_viejos",
        "valdren_cruce_cercas",
        "valdren_campo_rastrojo",
        "valdren_zanja_vieja",
        "valdren_arbol_descanso",
    ],
    step_seconds=DEFAULT_STEP_SECONDS,
    terminal="reverse",
    persistent_traveler=False,
    pauses=["valdren_centro", "valdren_cobertizos_viejos", "valdren_arbol_descanso"],
    fallback_dialogue="Loren asiente con una leve inclinación de cabeza y sigue atento al camino.",
    phrases=[
        "Las cercas de Valdren quedan atrás; el camino hacia Veyra está despejado hoy.",
        "Solo llevo recados sencillos de los campos. Buen viaje en el camino.",
        "El viento sopla limpio desde los llanos. No hay novedad en las parcelas.",
    ],
)

_REGISTRY.register(LOREN)
