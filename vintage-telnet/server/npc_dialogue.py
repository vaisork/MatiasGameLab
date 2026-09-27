"""Capa técnica desacoplada para conversación dinámica con NPCs (Issue #245).

Reglas de Jugabilidad: GAMEPLAY.md §35.
- Consumir personalidad persistente del NPC (conforme a npc_personality.py).
- Consumir ÚNICAMENTE conocimiento explícitamente autorizado (knowledge_allowed).
- Exclusión estricta de conocimientos prohibidos (knowledge_forbidden), secretos del DM y datos no autorizados.
- Entrada: jugador + NPC presente + mensaje.
- Salida: texto conversacional (DialogueResult).
- Separación estricta: el texto jamás ejecuta acciones ni altera estado del mundo (GAMEPLAY §35.7).
- Proveedor desacoplado mediante interfaz abstracta (DialogueProvider), testeable con mocks deterministas.
- Fallo o timeout degrada de forma segura a fallback_dialogue sin romper el flujo (GAMEPLAY §35.9).
- NPC no presente o inexistente no conversa (GAMEPLAY §35.1).
"""
from __future__ import annotations

import abc
from copy import deepcopy
from dataclasses import dataclass, field
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Estructuras de datos para el contrato de diálogo
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DialoguePrompt:
    """Contexto autorizado e inmutable enviado al proveedor de diálogo."""
    npc_id: str
    npc_name: str
    npc_role: str
    npc_town: str
    npc_species: str
    personality: dict[str, Any]
    knowledge_allowed: tuple[str, ...]
    player_name: str
    player_species: str
    player_message: str
    system_instructions: str


@dataclass(frozen=True)
class DialogueResult:
    """Resultado estrictamente textual de la conversación con el NPC."""
    success: bool
    npc_id: str | None = None
    npc_name: str | None = None
    text: str = ""
    is_fallback: bool = False
    error: str | None = None
    reason: str | None = None


# ---------------------------------------------------------------------------
# Interfaz desacoplada del proveedor de diálogo (Criterio 5)
# ---------------------------------------------------------------------------

class DialogueProvider(abc.ABC):
    """Interfaz abstracta para proveedores de lenguaje natural de NPCs."""

    @abc.abstractmethod
    def generate_reply(self, prompt: DialoguePrompt) -> str:
        """Genera respuesta textual para el NPC a partir del prompt autorizado.

        Debe ser una llamada síncrona o bloqueada con timeout controlado.
        Si falla o excede el tiempo, debe lanzar una excepción para que el
        motor de diálogo degrade limpiamente a fallback.
        """
        raise NotImplementedError


class FixedDialogueProvider(DialogueProvider):
    """Proveedor determinista con respuestas preconfiguradas o fija."""

    def __init__(self, reply: str = "Te escucho con atención, pero ahora debo atender mis tareas."):
        self.reply = reply
        self.calls: list[DialoguePrompt] = []

    def generate_reply(self, prompt: DialoguePrompt) -> str:
        self.calls.append(prompt)
        return self.reply


class MockDialogueProvider(DialogueProvider):
    """Proveedor configurable para pruebas de aislamiento, validación y latencia."""

    def __init__(
        self,
        handler: Callable[[DialoguePrompt], str] | None = None,
        *,
        should_fail: bool = False,
        failure_exception: Exception | None = None,
    ):
        self.handler = handler
        self.should_fail = should_fail
        self.failure_exception = failure_exception or RuntimeError("Simulated provider failure")
        self.received_prompts: list[DialoguePrompt] = []

    def generate_reply(self, prompt: DialoguePrompt) -> str:
        self.received_prompts.append(prompt)
        if self.should_fail:
            raise self.failure_exception
        if self.handler:
            return self.handler(prompt)
        return f"{prompt.npc_name} responde brevemente sobre lo consultado."


# ---------------------------------------------------------------------------
# Registro autoritativo de NPCs en el mundo
# ---------------------------------------------------------------------------

class NPCRegistry:
    """Registro autoritativo en memoria de NPCs presentes en el mundo."""

    def __init__(self) -> None:
        self._npcs: dict[str, dict[str, Any]] = {}
        self._by_name: dict[str, str] = {}

    def register(self, npc_data: dict[str, Any]) -> None:
        npc_id = str(npc_data.get("id") or "").strip()
        name = str(npc_data.get("name") or "").strip()
        if not npc_id:
            raise ValueError("El NPC requiere un 'id' válido.")
        if not name:
            raise ValueError("El NPC requiere un 'name' válido.")

        # Almacenar copia profunda para evitar mutaciones accidentales
        entry = deepcopy(npc_data)
        self._npcs[npc_id] = entry
        self._by_name[name.lower()] = npc_id

    def get(self, identifier: str) -> dict[str, Any] | None:
        if not identifier:
            return None
        cleaned = identifier.strip().lower()
        # Búsqueda directa por id
        if cleaned in self._npcs:
            return deepcopy(self._npcs[cleaned])
        # Búsqueda insensible a mayúsculas en ids
        for npc_id, npc in self._npcs.items():
            if npc_id.lower() == cleaned:
                return deepcopy(npc)
        # Búsqueda por nombre normalizado
        if cleaned in self._by_name:
            return deepcopy(self._npcs[self._by_name[cleaned]])
        return None

    def get_in_room(self, room_id: str) -> list[dict[str, Any]]:
        if not room_id:
            return []
        matching = []
        for npc in self._npcs.values():
            loc = npc.get("location") or npc.get("room_id")
            if loc == room_id:
                matching.append(deepcopy(npc))
        return matching

    def all_npcs(self) -> list[dict[str, Any]]:
        return [deepcopy(npc) for npc in self._npcs.values()]

    def clear(self) -> None:
        self._npcs.clear()
        self._by_name.clear()


# Registro global y proveedor global por defecto
_REGISTRY = NPCRegistry()
_DEFAULT_PROVIDER: DialogueProvider = FixedDialogueProvider()


def get_registry() -> NPCRegistry:
    return _REGISTRY


def set_default_provider(provider: DialogueProvider) -> None:
    global _DEFAULT_PROVIDER
    _DEFAULT_PROVIDER = provider


def get_default_provider() -> DialogueProvider:
    return _DEFAULT_PROVIDER


# ---------------------------------------------------------------------------
# Construcción del contexto del diálogo (Criterios 2 y 3)
# ---------------------------------------------------------------------------

def build_dialogue_prompt(npc: dict[str, Any] | Any, player: dict[str, Any] | Any, message: str) -> DialoguePrompt:
    """Construye el prompt de diálogo respetando estrictamente el canon y GAMEPLAY §35.

    Garantías de seguridad:
    1. Incluye personalidad persistente autoritativa (Criterio 2).
    2. Incluye ÚNICAMENTE knowledge_allowed (Criterio 3).
    3. Excluye totalmente knowledge_forbidden, secretos y datos privados ajenos.
    """
    player_data = dict(player) if player is not None else {}
    npc_data = dict(npc) if npc is not None else {}

    personality = deepcopy(npc_data.get("personality") or {})
    # Solo los conocimientos expresamente autorizados entran al prompt
    raw_allowed = npc_data.get("knowledge_allowed") or []
    if isinstance(raw_allowed, (list, tuple)):
        knowledge_allowed = tuple(str(k) for k in raw_allowed if isinstance(k, str) and k.strip())
    else:
        knowledge_allowed = ()

    npc_name = str(npc_data.get("name", "Habitante"))
    role = str(npc_data.get("role", "habitante"))
    town = str(npc_data.get("town", "el asentamiento"))
    species = str(npc_data.get("species", "humano"))

    temperament = personality.get("temperament", "calmado y reservado")
    speech_style = personality.get("speech_style", "sencillo y directo")
    formality = personality.get("formality", "neutral")
    traits = ", ".join(personality.get("traits") or ["reservado"])
    example_phrases = "\n".join(f"- \"{p}\"" for p in (personality.get("example_phrases") or []))

    allowed_list_text = "\n".join(f"- {item}" for item in knowledge_allowed) if knowledge_allowed else "- Información cotidiana de su oficio y entorno inmediato."

    system_instructions = (
        f"Eres {npc_name}, {role} de {town} (especie {species}).\n"
        f"Tu personalidad es: temperamento {temperament}; estilo de habla {speech_style}; formalidad {formality}.\n"
        f"Rasgos: {traits}.\n"
        f"Ejemplos de cómo te expresas:\n{example_phrases}\n\n"
        "REGLAS OBLIGATORIAS DE JUEGO (GAMEPLAY §35):\n"
        "1. FUENTE DE VERDAD: Solo puedes hablar con certeza sobre los hechos en tus CONOCIMIENTOS AUTORIZADOS.\n"
        "2. PUEDES NO SABER: Si el jugador pregunta sobre algo que no está en tus conocimientos autorizados, "
        "debes responder que no lo sabes, que no tienes certeza o que no te concierne. \"No sé\" es preferible a inventar.\n"
        "3. PROHIBIDO INVENTAR: No inventes nombres de lugares, criaturas, artefactos, secretos antiguos ni acontecimientos.\n"
        "4. SIN EJECUCIÓN DE ACCIONES: Tu respuesta es exclusivamente diálogo en ficción. "
        "No puedes dar objetos, dinero, magia, misiones mecánicas ni alterar el mundo.\n\n"
        f"CONOCIMIENTOS AUTORIZADOS PARA {npc_name.upper()}:\n"
        f"{allowed_list_text}\n"
    )

    return DialoguePrompt(
        npc_id=str(npc_data.get("id", "")),
        npc_name=npc_name,
        npc_role=role,
        npc_town=town,
        npc_species=species,
        personality=personality,
        knowledge_allowed=knowledge_allowed,
        player_name=str(player_data.get("name", "Viajero")),
        player_species=str(player_data.get("species", "humano")),
        player_message=(message or "").strip(),
        system_instructions=system_instructions,
    )


# ---------------------------------------------------------------------------
# Motor principal de conversación autoritativa (Criterios 1, 4, 6)
# ---------------------------------------------------------------------------

def converse(
    player: dict[str, Any],
    target: str,
    message: str = "",
    *,
    room_id: str | None = None,
    provider: DialogueProvider | None = None,
    registry: NPCRegistry | None = None,
) -> DialogueResult:
    """Ejecuta una interacción de diálogo con un NPC en el mundo.

    Garantías autoritativas:
    - Criterio 1: Si el NPC no existe o no está en la sala del jugador, no conversa.
    - Criterio 4: Cero modificaciones al estado del mundo, jugador o base de datos.
    - Criterio 6: Si el proveedor falla o da timeout, degrada de forma segura a fallback.
    """
    reg = registry or _REGISTRY
    player_data = dict(player) if player is not None else {}
    current_room = room_id or player_data.get("room")
    target_clean = (target or "").strip()

    if not target_clean:
        return DialogueResult(
            success=False,
            error="empty_target",
            reason="Debes indicar con quién deseas hablar.",
        )

    # 1. Búsqueda del NPC
    npc = reg.get(target_clean)
    if not npc:
        return DialogueResult(
            success=False,
            error="npc_not_found",
            reason=f"No hay nadie con el nombre '{target_clean}' aquí.",
        )

    # 2. Verificación de presencia en la misma sala (Criterio 1)
    npc_location = npc.get("location") or npc.get("room_id")
    if not current_room or npc_location != current_room:
        return DialogueResult(
            success=False,
            npc_id=npc.get("id"),
            npc_name=npc.get("name"),
            error="npc_not_present",
            reason=f"{npc.get('name')} no está en este lugar.",
        )

    # 3. Construcción del prompt seguro
    prompt = build_dialogue_prompt(npc, player, message)

    # 4. Invocación al proveedor con degradación segura ante fallos (Criterio 6)
    prov = provider or _DEFAULT_PROVIDER
    fallback_text = (
        npc.get("fallback_dialogue")
        or f"{npc.get('name')} asiente en silencio y continúa con sus quehaceres."
    )

    try:
        raw_reply = prov.generate_reply(prompt)
        cleaned_reply = (raw_reply or "").strip()
        if not cleaned_reply:
            logger.warning("Proveedor devolvió respuesta vacía para NPC %s; usando fallback", npc.get("id"))
            return DialogueResult(
                success=True,
                npc_id=npc.get("id"),
                npc_name=npc.get("name"),
                text=fallback_text,
                is_fallback=True,
            )
        return DialogueResult(
            success=True,
            npc_id=npc.get("id"),
            npc_name=npc.get("name"),
            text=cleaned_reply,
            is_fallback=False,
        )
    except Exception as exc:
        logger.warning(
            "Fallo al invocar proveedor de diálogo para NPC %s (%s). Degradando a fallback.",
            npc.get("id"),
            exc,
        )
        return DialogueResult(
            success=True,
            npc_id=npc.get("id"),
            npc_name=npc.get("name"),
            text=fallback_text,
            is_fallback=True,
        )


# ---------------------------------------------------------------------------
# Poblado canónico inicial de NPCs
# ---------------------------------------------------------------------------

CANONICAL_NPCS: list[dict[str, Any]] = [
    {
        "id": "daro_herrero",
        "name": "Daro",
        "species": "humano",
        "town": "Valdren",
        "location": "valdren_forja",
        "role": "herrero",
        "personality": {
            "temperament": "reservado y meticuloso",
            "speech_style": "parco, pausado y directo",
            "formality": "neutral",
            "humor": "seco",
            "sociability": "moderada",
            "response_length": "breve",
            "expressive_reactions": [
                "asiente con lentitud",
                "mira el fuego de la fragua",
                "comprueba el temple de una pieza con el pulgar",
            ],
            "traits": ["meticuloso", "honesto", "paciente"],
            "example_phrases": [
                "El hierro caliente no espera.",
                "Cada herramienta tiene su peso y su labor.",
                "Si buscas alboroto, este no es el taller adecuado.",
            ],
        },
        "knowledge_allowed": [
            "forja local de Valdren y herramientas de labranza",
            "reparación de aperos, clavos y rejas de arado",
            "el estado de los caminos inmediatos y cercas alrededor de Valdren",
            "la precaución de no internarse desprevenido en pastos altos ni cruces aislados",
        ],
        "knowledge_forbidden": [
            "los secretos subterráneos de Vaisgard",
            "la ubicación exacta de amenazas mayores de las Cinco Rutas",
            "la verdad sobre las ruinas antiguas",
            "el contenido de cofres o inventarios ajenos",
        ],
        "fallback_dialogue": "Daro examina una tenaza sobre el yunque en silencio, asiente y vuelve a la fragua.",
    }
]


def load_canonical_npcs() -> None:
    """Carga los NPCs canónicos iniciales en el registro."""
    for npc in CANONICAL_NPCS:
        _REGISTRY.register(npc)


# Cargar al importar
load_canonical_npcs()
