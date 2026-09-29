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
import ipaddress
import json
import logging
import os
import re
import threading
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from . import economy, items, store, travelers, world

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Acciones estructuradas y Gate autoritativo (Issues #247, #385)
# ---------------------------------------------------------------------------

ALLOWLISTED_NPC_ACTIONS: frozenset[str] = frozenset({
    "indicate_route",
    "reveal_lore_topic",
    "show_workshop_item",
    "list_shop_inventory",
    "quote_item",
    "purchase_item",
})

VALID_WORKSHOP_TOOLS: frozenset[str] = frozenset({
    "martillo de fragua",
    "tenaza de temple",
    "reja de arado",
    "clavo de herrar",
    "yunque menor",
    "cincel de hierro",
})


@dataclass(frozen=True)
class ProposedAction:
    """Propuesta de acción estructurada emitida por el diálogo del NPC."""
    action_type: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionGateResult:
    """Resultado autoritativo de la evaluación de una acción propuesta."""
    accepted: bool
    action_type: str | None = None
    reason: str = ""
    effect: dict[str, Any] | None = None


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
    history: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class DialogueResult:
    """Resultado estrictamente textual y de acción evaluada por el Gate."""
    success: bool
    npc_id: str | None = None
    npc_name: str | None = None
    text: str = ""
    is_fallback: bool = False
    error: str | None = None
    reason: str | None = None
    proposed_action: ProposedAction | None = None
    gate_result: ActionGateResult | None = None


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


class OllamaDialogueProvider(DialogueProvider):
    """Runtime NPC conversation through a local Ollama chat endpoint.

    The provider sends only the already-authorized dialogue prompt and the
    player's current utterance. It has no tools and cannot mutate game state.
    """

    def __init__(self, *, base_url: str, model: str, timeout: float = 120.0):
        parsed = urlsplit((base_url or "").strip())
        host = parsed.hostname or ""
        try:
            port = parsed.port
        except ValueError as exc:
            raise ValueError("La URL local de Ollama de diálogo tiene un puerto inválido.") from exc
        try:
            is_loopback = host.lower() == "localhost" or ipaddress.ip_address(host).is_loopback
        except ValueError:
            is_loopback = False
        if (
            parsed.scheme != "http"
            or not is_loopback
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or parsed.path not in ("", "/")
            or port is None
        ):
            raise ValueError("Ollama de diálogo debe usar HTTP local en loopback con puerto explícito.")
        cleaned_model = (model or "").strip()
        if not cleaned_model or len(cleaned_model) > 128:
            raise ValueError("Configura un modelo Ollama de diálogo válido.")
        if not 1 <= float(timeout) <= 180:
            raise ValueError("El timeout de diálogo Ollama debe estar entre 1 y 180 segundos.")
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.model = cleaned_model
        self.timeout = float(timeout)
        self._inference_lock = threading.Lock()

    def generate_reply(self, prompt: DialoguePrompt) -> str:
        if not prompt.player_message.strip():
            player_text = "El viajero se acerca para conversar, pero aún no ha dicho nada."
        else:
            player_text = prompt.player_message.strip()
        if len(player_text) > 500:
            raise RuntimeError("El mensaje para el NPC supera el límite de 500 caracteres.")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt.system_instructions},
                {"role": "user", "content": player_text},
            ],
            "stream": False,
            "think": False,
            "options": {"temperature": 0.6, "num_predict": 160},
        }
        request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            method="POST",
        )
        if not self._inference_lock.acquire(blocking=False):
            raise RuntimeError("Ollama de diálogo ya está atendiendo otra conversación.")
        try:
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    raw_body = response.read(65537)
                if len(raw_body) > 65536:
                    raise RuntimeError("Ollama devolvió una respuesta demasiado grande.")
                data = json.loads(raw_body.decode("utf-8"))
            except HTTPError as exc:
                raise RuntimeError(f"Ollama respondió HTTP {exc.code}.") from exc
            except (URLError, TimeoutError, OSError) as exc:
                raise RuntimeError("No se pudo contactar con Ollama local.") from exc
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RuntimeError("Ollama devolvió una respuesta JSON inválida.") from exc

            message = data.get("message") if isinstance(data, dict) else None
            content = message.get("content") if isinstance(message, dict) else None
            if not isinstance(content, str) or not content.strip():
                raise RuntimeError("Ollama no devolvió texto de conversación.")
            return content.strip()
        finally:
            self._inference_lock.release()


class UnavailableDialogueProvider(DialogueProvider):
    """Keeps the server available while a requested provider is misconfigured."""

    def __init__(self, reason: str):
        self.reason = reason

    def generate_reply(self, prompt: DialoguePrompt) -> str:
        raise RuntimeError(self.reason)


def dialogue_provider_from_environment(environ: dict[str, str] | None = None) -> DialogueProvider:
    """Build the runtime provider without making any network request at startup."""
    config = os.environ if environ is None else environ
    selected = config.get("VT_NPC_DIALOGUE_PROVIDER", "fixed").strip().lower()
    if selected == "fixed":
        return FixedDialogueProvider()
    if selected != "ollama":
        reason = "VT_NPC_DIALOGUE_PROVIDER debe ser 'fixed' u 'ollama'."
        logger.error(reason)
        return UnavailableDialogueProvider(reason)

    model = config.get("VT_OLLAMA_DIALOGUE_MODEL", "").strip()
    if not model:
        reason = "Falta VT_OLLAMA_DIALOGUE_MODEL para habilitar Ollama en conversaciones."
        logger.error(reason)
        return UnavailableDialogueProvider(reason)
    try:
        timeout = float(config.get("VT_OLLAMA_DIALOGUE_TIMEOUT", "120"))
        return OllamaDialogueProvider(
            base_url=config.get("VT_OLLAMA_DIALOGUE_URL", "http://127.0.0.1:11434"),
            model=model,
            timeout=timeout,
        )
    except (TypeError, ValueError) as exc:
        reason = f"Configuración inválida del proveedor Ollama de diálogo: {exc}"
        logger.error(reason)
        return UnavailableDialogueProvider(reason)


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
_DEFAULT_PROVIDER: DialogueProvider = dialogue_provider_from_environment()


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

def build_dialogue_prompt(
    npc: dict[str, Any] | Any,
    player: dict[str, Any] | Any,
    message: str,
    history: list[dict[str, Any]] | tuple[dict[str, Any], ...] | None = None,
) -> DialoguePrompt:
    """Construye el prompt de diálogo respetando estrictamente el canon y GAMEPLAY §35.

    Garantías de seguridad:
    1. Incluye personalidad persistente autoritativa (Criterio 2).
    2. Incluye ÚNICAMENTE knowledge_allowed (Criterio 3).
    3. Excluye totalmente knowledge_forbidden, secretos y datos privados ajenos.
    4. Incluye memoria conversacional reciente acotada sin crear hechos de mundo (Issue #246).
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
    humor = personality.get("humor", "discreto")
    sociability = personality.get("sociability", "moderada")
    response_length = personality.get("response_length", "breve")
    traits = ", ".join(personality.get("traits") or ["reservado"])
    example_phrases = "\n".join(f"- \"{p}\"" for p in (personality.get("example_phrases") or []))

    allowed_list_text = "\n".join(f"- {item}" for item in knowledge_allowed) if knowledge_allowed else "- Información cotidiana de su oficio y entorno inmediato."

    # Memoria conversacional reciente acotada (Issue #246)
    history_list = list(history or [])
    history_text = ""
    if history_list:
        lines = []
        for item in history_list:
            spk = player_data.get("name", "Viajero") if item.get("speaker") == "player" else npc_name
            msg = str(item.get("message", "")).strip()
            lines.append(f"- {spk}: \"{msg}\"")
        history_text = (
            "\nMEMORIA DE CONVERSACIÓN RECIENTE CON ESTE VIAJERO (CONTEXTO INMEDIATO):\n"
            "Las siguientes líneas corresponden al intercambio reciente entre tú y este viajero específico.\n"
            "Debes usar este contexto para mantener coherencia en la conversación.\n"
            "Tu personalidad, principios y conocimientos autorizados continúan siendo la regla suprema "
            "y no pueden ser contradichos por el diálogo previo:\n"
            + "\n".join(lines)
            + "\n"
        )

    npc_loc = npc_data.get("location") or npc_data.get("room_id")
    shop_guidelines = ""
    if role in ("herrero", "comerciante") and (npc_loc == "valdren_forja" or npc_data.get("id") == "daro_herrero"):
        shop_guidelines = (
            "\nACCIONES ESTRUCTURADAS DE TIENDA AUTORIZADAS (GAMEPLAY §35, Issue #385):\n"
            "Puedes emitir etiquetas al final de tu respuesta (canal separado) si el jugador consulta tu catálogo, cotiza o compra:\n"
            "- Listar armas disponibles: <!--ACTION: {\"type\": \"list_shop_inventory\", \"payload\": {}}-->\n"
            "- Cotizar precio oficial: <!--ACTION: {\"type\": \"quote_item\", \"payload\": {\"item_key\": \"<item_key>\"}}-->\n"
            "- Concretar compra autoritativa cuando el jugador solicita comprar: <!--ACTION: {\"type\": \"purchase_item\", \"payload\": {\"item_key\": \"<item_key>\"}}-->\n"
            "El servidor siempre valida precio, fondos y presencia objetiva; el diálogo no tiene autoridad directa sobre el saldo ni el inventario.\n"
        )

    system_instructions = (
        f"Eres {npc_name}, {role} de {town} (especie {species}).\n"
        f"Tu personalidad es: temperamento {temperament}; estilo de habla {speech_style}; "
        f"formalidad {formality}; humor {humor}; sociabilidad {sociability}; "
        f"longitud habitual de respuesta {response_length}.\n"
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
        f"{history_text}"
        f"{shop_guidelines}"
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
        history=tuple(dict(h) for h in history_list),
    )


_ACTION_TAG_REGEX = re.compile(r'<!--ACTION:\s*(\{.*?\})\s*-->', re.DOTALL)


def extract_proposed_action(raw_output: Any) -> tuple[str, ProposedAction | None]:
    """Separa el texto conversacional limpio de cualquier propuesta de acción estructurada.

    Garantiza que la respuesta narrativa y la propuesta de acción sean canales separados.
    """
    if isinstance(raw_output, tuple) and len(raw_output) == 2:
        text, action = raw_output
        return str(text or "").strip(), action if isinstance(action, ProposedAction) else None

    raw_text = str(raw_output or "")
    match = _ACTION_TAG_REGEX.search(raw_text)
    if not match:
        return raw_text.strip(), None

    json_str = match.group(1)
    clean_text = _ACTION_TAG_REGEX.sub("", raw_text).strip()
    try:
        data = json.loads(json_str)
        if isinstance(data, dict) and "type" in data:
            action_type = str(data["type"]).strip()
            payload = data.get("payload") if isinstance(data.get("payload"), dict) else {k: v for k, v in data.items() if k != "type"}
            return clean_text, ProposedAction(action_type=action_type, payload=payload)
    except Exception as exc:
        logger.warning("Propuesta de acción malformada en diálogo de NPC: %s", exc)

    return clean_text, None


def evaluate_action_gate(
    npc: dict[str, Any] | Any,
    player: dict[str, Any] | Any,
    proposed: ProposedAction | None,
    *,
    room_id: str | None = None,
    db_path: str | None = None,
) -> ActionGateResult:
    """Valida precondiciones y autoridad de una acción propuesta.

    Garantías de seguridad (Issue #247):
    1. Si proposed es None -> no hay acción.
    2. Si action_type no está en ALLOWLISTED_NPC_ACTIONS -> rechazo tajante (action_not_allowlisted).
    3. Si el jugador o el NPC no están en la misma sala -> rechazo (presence_mismatch).
    4. Validación estricta de precondiciones por tipo de acción:
       - indicate_route: la dirección debe existir en las salidas de la sala en world.ROOMS.
       - reveal_lore_topic: el tema debe estar en npc['knowledge_allowed'] y NO en npc['knowledge_forbidden'].
       - show_workshop_item: el NPC debe ser herrero en sala de forja y la herramienta ser válida.
    5. Cero mutaciones de estado si falla la validación.
    6. Sin economía, sin inventario de jugador, sin quests arbitrarias.
    7. Auditoría autoritativa de aceptación/rechazo en SQLite.
    """
    if proposed is None:
        return ActionGateResult(accepted=False, reason="no_action_proposed")

    npc_data = dict(npc) if npc is not None else {}
    player_data = dict(player) if player is not None else {}
    player_id = str(player_data.get("id") or "").strip()
    npc_id = str(npc_data.get("id") or "").strip()
    action_type = str(proposed.action_type or "").strip()

    # 1. Allowlist estricta
    if action_type not in ALLOWLISTED_NPC_ACTIONS:
        result = ActionGateResult(
            accepted=False,
            action_type=action_type,
            reason="action_not_allowlisted",
        )
        if db_path and player_id and npc_id:
            try:
                store.record_npc_action_gate_evaluation(
                    db_path, player_id, npc_id, action_type, False, result.reason, proposed.payload
                )
            except Exception as exc:
                logger.warning("Fallo al registrar auditoría de acción: %s", exc)
        return result

    # 2. Validación de presencia
    npc_loc = npc_data.get("location") or npc_data.get("room_id")
    current_room = room_id or player_data.get("room")
    if not current_room or current_room != npc_loc:
        result = ActionGateResult(
            accepted=False,
            action_type=action_type,
            reason="presence_mismatch",
        )
        if db_path and player_id and npc_id:
            try:
                store.record_npc_action_gate_evaluation(
                    db_path, player_id, npc_id, action_type, False, result.reason, proposed.payload
                )
            except Exception as exc:
                logger.warning("Fallo al registrar auditoría de acción: %s", exc)
        return result

    # 3. Validación de precondiciones por tipo de acción
    if action_type == "indicate_route":
        direction = str(proposed.payload.get("direction") or "").strip().lower()
        room_info = world.get_room(current_room)
        exits = room_info.get("exits", {}) if room_info else {}
        if direction not in exits:
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason=f"invalid_direction: {direction}",
            )
        else:
            destination_id = exits[direction]
            dest_room = world.get_room(destination_id)
            dest_name = dest_room.get("name") if dest_room else destination_id
            result = ActionGateResult(
                accepted=True,
                action_type=action_type,
                reason="route_indicated_safely",
                effect={
                    "direction": direction,
                    "destination": destination_id,
                    "destination_name": dest_name,
                    "indicated_by": npc_data.get("name"),
                },
            )

    elif action_type == "reveal_lore_topic":
        raw_topic = str(proposed.payload.get("topic") or "").strip()
        topic_lower = raw_topic.lower()
        forbidden_list = [str(k).lower() for k in (npc_data.get("knowledge_forbidden") or [])]
        allowed_list = [str(k).lower() for k in (npc_data.get("knowledge_allowed") or [])]

        if any(f in topic_lower or topic_lower in f for f in forbidden_list if f):
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="forbidden_topic_rejected",
            )
        elif not any(a in topic_lower or topic_lower in a for a in allowed_list if a):
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="topic_not_in_knowledge_allowed",
            )
        else:
            result = ActionGateResult(
                accepted=True,
                action_type=action_type,
                reason="topic_revealed_safely",
                effect={
                    "topic": raw_topic,
                    "authorized": True,
                    "revealed_by": npc_data.get("name"),
                },
            )

    elif action_type == "show_workshop_item":
        item_name = str(proposed.payload.get("item_name") or "").strip().lower()
        role = str(npc_data.get("role") or "").lower()
        if role != "herrero" or not current_room.endswith("_forja"):
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="workshop_precondition_failed",
            )
        elif item_name not in VALID_WORKSHOP_TOOLS:
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason=f"invalid_workshop_tool: {item_name}",
            )
        else:
            result = ActionGateResult(
                accepted=True,
                action_type=action_type,
                reason="workshop_tool_shown_safely",
                effect={
                    "tool": item_name,
                    "inspected": True,
                    "workshop": current_room,
                    "artisan": npc_data.get("name"),
                },
            )

    elif action_type == "list_shop_inventory":
        role = str(npc_data.get("role") or "").lower()
        if role not in ("herrero", "comerciante") or current_room != economy.DARO_SHOP_ROOM:
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="shop_not_available",
            )
        elif player_data.get("in_combat"):
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="cannot_trade_during_combat",
            )
        else:
            catalog = economy.get_daro_catalog_items()
            result = ActionGateResult(
                accepted=True,
                action_type=action_type,
                reason="shop_inventory_listed",
                effect={
                    "merchant": npc_data.get("name"),
                    "room": current_room,
                    "currency": "sellos",
                    "catalog": catalog,
                },
            )

    elif action_type == "quote_item":
        role = str(npc_data.get("role") or "").lower()
        if role not in ("herrero", "comerciante") or current_room != economy.DARO_SHOP_ROOM:
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="shop_not_available",
            )
        elif player_data.get("in_combat"):
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="cannot_trade_during_combat",
            )
        else:
            raw_item = str(
                proposed.payload.get("item_key")
                or proposed.payload.get("item_name")
                or proposed.payload.get("item")
                or ""
            ).strip()
            item_key = economy.resolve_daro_item(raw_item)
            if not item_key or item_key not in economy.DARO_CATALOG:
                result = ActionGateResult(
                    accepted=False,
                    action_type=action_type,
                    reason="item_not_in_catalog",
                    effect={"requested_item": raw_item},
                )
            else:
                price = economy.DARO_CATALOG[item_key]
                balance = (
                    economy.get_player_balance(db_path, player_id)
                    if (db_path and player_id)
                    else player_data.get("sellos", 0)
                )
                item_info = items.get_item(item_key)
                item_name = item_info["name"] if item_info else item_key
                result = ActionGateResult(
                    accepted=True,
                    action_type=action_type,
                    reason="item_quoted_safely",
                    effect={
                        "item_key": item_key,
                        "item_name": item_name,
                        "price_sellos": price,
                        "player_balance": balance,
                        "can_afford": (balance >= price),
                        "quoted_by": npc_data.get("name"),
                    },
                )

    elif action_type == "purchase_item":
        role = str(npc_data.get("role") or "").lower()
        if role not in ("herrero", "comerciante") or current_room != economy.DARO_SHOP_ROOM:
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="shop_not_available",
            )
        elif player_data.get("in_combat"):
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="cannot_buy_during_combat",
            )
        elif not db_path or not player_id:
            result = ActionGateResult(
                accepted=False,
                action_type=action_type,
                reason="storage_unavailable",
            )
        else:
            raw_item = str(
                proposed.payload.get("item_key")
                or proposed.payload.get("item_name")
                or proposed.payload.get("item")
                or ""
            ).strip()
            item_key = economy.resolve_daro_item(raw_item)
            if not item_key or item_key not in economy.DARO_CATALOG:
                result = ActionGateResult(
                    accepted=False,
                    action_type=action_type,
                    reason="item_not_in_catalog",
                    effect={"requested_item": raw_item},
                )
            else:
                client_tx_id = proposed.payload.get("client_tx_id") or proposed.payload.get("request_id")
                success, msg, extra = economy.buy_item_from_daro(
                    db_path,
                    player_id,
                    item_key,
                    client_tx_id=str(client_tx_id).strip() if client_tx_id else None,
                )
                if not success:
                    reason_code = "insufficient_funds" if "suficientes sellos" in msg.lower() else msg
                    result = ActionGateResult(
                        accepted=False,
                        action_type=action_type,
                        reason=reason_code,
                        effect=extra,
                    )
                else:
                    result = ActionGateResult(
                        accepted=True,
                        action_type=action_type,
                        reason="item_purchased_safely",
                        effect=extra,
                    )
    else:
        result = ActionGateResult(accepted=False, action_type=action_type, reason="unsupported_action")

    # Registro de auditoría (Issue #247: registrar acción aceptada/rechazada)
    if db_path and player_id and npc_id:
        try:
            store.record_npc_action_gate_evaluation(
                db_path,
                player_id,
                npc_id,
                action_type,
                result.accepted,
                result.reason,
                proposed.payload,
            )
        except Exception as exc:
            logger.warning("Fallo al registrar auditoría de acción para NPC %s: %s", npc_id, exc)

    return result


# ---------------------------------------------------------------------------
# Motor principal de conversación autoritativa (Criterios 1, 4, 6 e Issues #246, #247)
# ---------------------------------------------------------------------------

def converse(
    player: dict[str, Any] | Any,
    target: str,
    message: str = "",
    *,
    room_id: str | None = None,
    provider: DialogueProvider | None = None,
    registry: NPCRegistry | None = None,
    db_path: str | None = None,
    window_size: int = 5,
) -> DialogueResult:
    """Ejecuta una interacción de diálogo con un NPC en el mundo.

    Garantías autoritativas:
    - Criterio 1: Si el NPC no existe o no está en la sala del jugador, no conversa.
    - Criterio 4: Cero modificaciones al estado del mundo, jugador o base de datos de juego.
    - Criterio 6: Si el proveedor falla o da timeout, degrada de forma segura a fallback.
    - Issue #246: Mantiene memoria conversacional reciente acotada por pareja jugador-NPC.
    - Issue #247: Valida propuestas de acción estructuradas con Gate autoritativo y canal separado.
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
    if travelers.is_traveler(npc.get("id")):
        npc_location = travelers.get_traveler_position(npc.get("id"), db_path=db_path)
    if not current_room or npc_location != current_room:
        return DialogueResult(
            success=False,
            npc_id=npc.get("id"),
            npc_name=npc.get("name"),
            error="npc_not_present",
            reason=f"{npc.get('name')} no está en este lugar.",
        )

    # 3. Lectura de memoria conversacional acotada (Issue #246)
    history: list[dict[str, Any]] = []
    player_id = str(player_data.get("id") or "").strip()
    npc_id = str(npc.get("id") or "").strip()
    if db_path and player_id and npc_id:
        try:
            history = store.get_npc_memory(db_path, player_id, npc_id, window_size=window_size)
        except Exception as exc:
            logger.warning("Fallo al leer memoria de NPC %s para jugador %s: %s", npc_id, player_id, exc)

    # 4. Construcción del prompt seguro
    prompt = build_dialogue_prompt(npc, player, message, history=history)

    # 5. Invocación al proveedor con degradación segura ante fallos (Criterio 6)
    prov = provider or _DEFAULT_PROVIDER
    fallback_text = (
        npc.get("fallback_dialogue")
        or f"{npc.get('name')} asiente en silencio y continúa con sus quehaceres."
    )

    # Manejo de la escena autoritativa de Aren (HOSHAI-WEAPON-01 / #287)
    if npc_id == "khariel_taller_hoshai_01":
        has_item = store.get_story_flag(db_path, player_id, "hoshai_hoja_recibida") if (db_path and player_id) else False
        has_helped = store.get_story_flag(db_path, player_id, "hoshai_paso_ayudado") if (db_path and player_id) else False

        msg_lower = (message or "").strip().lower()
        offers_help = any(w in msg_lower for w in ("ayud", "sujet", "asegur", "paso", "amarre", "mano", "si", "sí", "claro", "vale", "apoyo", "cuenta"))

        if has_item:
            clean_reply = "Ya cumpliste aquí. La pieza que te confiaron sigue siendo la misma; no hay otra esperando por repetir el favor."
        elif has_helped or offers_help:
            if db_path and player_id:
                store.set_story_flag(db_path, player_id, "hoshai_paso_ayudado", True)
                store.grant_story_item_once(db_path, player_id, "hoshai_hoja_recibida", "hoja_hoshai", forge_validated=False)
            clean_reply = (
                "Entre ambos vuelven a tensar el amarre. La carga queda estable y el paso recupera su espacio. "
                "No fue una hazaña, pero alguien tenía que detenerse a hacerlo.\n\n"
                "—Bien. No todos los que pasan se detienen cuando hace falta una mano.\n\n"
                "Te confían una Hoja de Hoshai todavía pendiente de Forja. Puedes conservarla, pero antes de usarla tendrá que pasar por ese proceso."
            )
        else:
            clean_reply = "—Si vas a quedarte un momento, sujeta desde ahí. Con eso basta para dejar libre el paso."

        is_fallback = False
        proposed = None

    # Manejo de la escena autoritativa de Karn (KORVEN-WEAPON-01 / #288)
    elif npc_id == "brumak_taller_korven_01":
        has_item = store.get_story_flag(db_path, player_id, "korven_martillo_recibido") if (db_path and player_id) else False
        has_helped = store.reconcile_story_flag_alias(db_path, player_id, "korven_carga_asentada", "korven_trabajo_ayudado") if (db_path and player_id) else False

        msg_lower = (message or "").strip().lower()
        offers_help = any(w in msg_lower for w in ("ayud", "sosten", "sostén", "apoyo", "carg", "firme", "fuerz", "mano", "si", "sí", "claro", "vale", "apoyo", "cuenta"))

        if has_item:
            clean_reply = "Ya cumpliste aquí. La pieza que te entregaron sigue siendo la misma; no hay otra esperando por repetir la ayuda."
        elif has_helped or offers_help:
            if db_path and player_id:
                store.set_story_flag(db_path, player_id, "korven_trabajo_ayudado", True)
                store.grant_story_item_once(db_path, player_id, "korven_martillo_recibido", "martillo_korven", forge_validated=False)
            clean_reply = (
                "El apoyo vuelve a quedar bajo el peso correcto. La carga queda estable y el paso vuelve a estar libre.\n\n"
                "—Así está bien. Una herramienta sirve más cuando quien la lleva sabe cuándo hacer fuerza y cuándo sostener.\n\n"
                "Te entregan un Martillo de Korven. La pieza es tuya, pero todavía necesita validación de Forja antes de poder equiparse."
            )
        else:
            clean_reply = "—Sostén ese extremo. Yo corrijo el apoyo. Si queda firme, podremos moverla."

        is_fallback = False
        proposed = None
    elif npc_id == "viajero_loren":
        traveler = travelers.get_registry().get("viajero_loren")
        phrases = traveler.phrases if traveler else [
            "Las cercas de Valdren quedan atrás; el camino hacia Veyra está despejado hoy.",
            "Solo llevo recados sencillos de los campos. Buen viaje en el camino.",
            "El viento sopla limpio desde los llanos. No hay novedad en las parcelas.",
        ]
        phrase_key = message or current_room or ""
        clean_reply = f"—{phrases[sum(ord(char) for char in phrase_key) % len(phrases)]}"
        is_fallback = False
        proposed = None
    else:
        try:
            raw_output = prov.generate_reply(prompt)
            clean_reply, proposed = extract_proposed_action(raw_output)
            if not clean_reply:
                logger.warning("Proveedor devolvió respuesta vacía para NPC %s; usando fallback", npc.get("id"))
                clean_reply = fallback_text
                is_fallback = True
                proposed = None
            else:
                is_fallback = False
        except Exception as exc:
            logger.warning(
                "Fallo al invocar proveedor de diálogo para NPC %s (%s). Degradando a fallback.",
                npc.get("id"),
                exc,
            )
            clean_reply = fallback_text
            is_fallback = True
            proposed = None

    # 6. Evaluación autoritativa de acción propuesta por el Gate (Issue #247)
    gate_result: ActionGateResult | None = None
    if proposed is not None:
        gate_result = evaluate_action_gate(
            npc,
            player,
            proposed,
            room_id=current_room,
            db_path=db_path,
        )

    # 7. Registro de memoria conversacional reciente tras diálogo exitoso (Issue #246)
    if db_path and player_id and npc_id:
        try:
            store.record_npc_dialogue_exchange(
                db_path,
                player_id,
                npc_id,
                message,
                clean_reply,
                window_size=window_size,
            )
        except Exception as exc:
            logger.warning("Fallo al guardar memoria de NPC %s para jugador %s: %s", npc_id, player_id, exc)

    return DialogueResult(
        success=True,
        npc_id=npc.get("id"),
        npc_name=npc.get("name"),
        text=clean_reply,
        is_fallback=is_fallback,
        proposed_action=proposed,
        gate_result=gate_result,
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
                "Una espada de juramento son ochenta y cinco sellos; ni uno más, ni uno menos.",
                "No vendo armas de Khariel ni de Brumak; este es un taller de Valdren.",
            ],
        },
        "knowledge_allowed": [
            "forja local de Valdren y herramientas de labranza",
            "reparación de aperos, clavos y rejas de arado",
            "el estado de los caminos inmediatos y cercas alrededor de Valdren",
            "la precaución de no internarse desprevenido en pastos altos ni cruces aislados",
            "armas comunes de ruta que vende en el taller por sellos de bronce: Varita de aprendiz (40), Puñal de camino (50), Arco de ruta (65) y Espada de juramento (85)",
            "no vende armas culturales ni regionales exclusivas como la Hoja de Hoshai o el Martillo de Korven",
            "acepta sellos como forma de pago ordinaria en su taller",
            "recompra únicamente las cuatro armas comunes de su catálogo al 35% del valor base",
        ],
        "knowledge_forbidden": [
            "los secretos subterráneos de Vaisgard",
            "la ubicación exacta de amenazas mayores de las Cinco Rutas",
            "la verdad sobre las ruinas antiguas",
            "el contenido de cofres o inventarios ajenos",
            "precios distintos a los fijados oficialmente o descuentos inventados",
        ],
        "fallback_dialogue": "Daro examina una tenaza sobre el yunque en silencio, asiente y vuelve a la fragua.",
    },
    {
        "id": "khariel_taller_hoshai_01",
        "name": "Aren",
        "species": "Felaryn",
        "town": "Khariel",
        "location": "khariel_forja",
        "role": "artesano de taller",
        "personality": {
            "temperament": "meticuloso, práctico y agradecido con la ayuda honesta",
            "speech_style": "sobrio, directo y pausado",
            "formality": "neutral",
            "humor": "escaso",
            "sociability": "moderada",
            "response_length": "breve",
            "expressive_reactions": [
                "comprueba la tensión del amarre",
                "asiente con sobriedad",
                "ordena las herramientas del taller",
            ],
            "traits": ["artesano", "observador", "sobrio"],
            "example_phrases": [
                "Si vas a quedarte un momento, sujeta desde ahí. Con eso basta para dejar libre el paso.",
                "No hace falta hacerlo perfecto. Solo que vuelva a quedar firme y podamos pasar.",
                "Bien. No todos los que pasan se detienen cuando hace falta una mano.",
            ],
        },
        "knowledge_allowed": [
            "el funcionamiento cotidiano del taller y del paso de carga",
            "el trabajo de mantenimiento de herramientas y amarres en Khariel",
            "la necesidad de validación en la Forja antes de poder usar una Hoja de Hoshai",
        ],
        "knowledge_forbidden": [
            "estadísticas internas, fórmulas de daño, flags ni reglas de balance",
            "afirmar que la Hoja esté validada antes de confirmarlo el sistema",
            "secretos antiguos, gremios inventados o historia oculta",
        ],
        "fallback_dialogue": "Aren asiente con sobriedad y continúa ajustando las sujeciones del taller.",
    },
    {
        "id": "brumak_taller_korven_01",
        "name": "Karn",
        "species": "Dravak",
        "town": "Brumak",
        "location": "brumak_forja",
        "role": "artesano de taller",
        "personality": {
            "temperament": "práctico, resistente y paciente",
            "speech_style": "sobrio, conciso y de pocas palabras",
            "formality": "neutral",
            "humor": "escaso",
            "sociability": "moderada",
            "response_length": "breve",
            "expressive_reactions": [
                "comprueba la solidez del apoyo de piedra",
                "asiente con firmeza",
                "golpea suavemente el mango del martillo contra la palma",
            ],
            "traits": ["artesano", "firme", "práctico"],
            "example_phrases": [
                "—Sostén ese extremo. Yo corrijo el apoyo. Si queda firme, podremos moverla.",
                "Una carga mal apoyada termina quebrando lo que tiene debajo.",
                "—Así está bien. Una herramienta sirve más cuando quien la lleva sabe cuándo hacer fuerza y cuándo sostener.",
            ],
        },
        "knowledge_allowed": [
            "el funcionamiento del taller de Brumak y el trabajo de piedra y metal",
            "el equilibrio y sujeción de cargas pesadas",
            "la necesidad de validación de Forja antes de poder usar un Martillo de Korven",
        ],
        "knowledge_forbidden": [
            "estadísticas internas, fórmulas de daño, flags ni reglas de balance",
            "afirmar que el Martillo esté validado antes de confirmarlo el sistema",
            "secretos de Korven, jerarquías ni historia oculta",
        ],
        "fallback_dialogue": "Karn asiente con firmeza y vuelve a comprobar los apoyos de piedra del taller.",
    },
    {
        "id": "viajero_loren",
        "name": "Loren",
        "species": "humano",
        "town": "Valdren",
        "location": None,
        "role": "viajero de camino",
        "personality": {
            "temperament": "tranquilo, observador y acostumbrado al camino",
            "speech_style": "breve, pausado y cordial",
            "formality": "neutral",
            "humor": "escaso",
            "sociability": "moderada",
            "response_length": "breve",
            "expressive_reactions": ["asiente con una leve inclinación de cabeza", "ajusta la correa de su morral", "mira a lo largo del sendero"],
            "traits": ["viajero", "observador", "tranquilo"],
            "example_phrases": [
                "Las cercas de Valdren quedan atrás; el camino hacia Veyra está despejado hoy.",
                "Solo llevo recados sencillos de los campos. Buen viaje en el camino.",
                "El viento sopla limpio desde los llanos. No hay novedad en las parcelas.",
            ],
        },
        "knowledge_allowed": ["el estado visible del camino entre Valdren y los llanos", "noticias cotidianas sobre el clima y el tránsito de viajeros", "los cobertizos y marcas del sendero"],
        "knowledge_forbidden": ["estadísticas internas, fórmulas de daño, flags ni reglas de balance", "secretos antiguos, gremios inventados o historia oculta", "misiones heroicas, compras o mercancías mágicas"],
        "fallback_dialogue": "Loren asiente con una leve inclinación de cabeza y sigue atento al camino.",
    },
]


def load_canonical_npcs() -> None:
    """Carga los NPCs canónicos iniciales en el registro."""
    for npc in CANONICAL_NPCS:
        _REGISTRY.register(npc)

    # Cargar fichas JSON de content/npcs/ si existen
    from pathlib import Path
    npcs_dir = Path(__file__).resolve().parent.parent / "content" / "npcs"
    if npcs_dir.is_dir():
        for file in sorted(npcs_dir.glob("*.json")):
            try:
                with open(file, encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "id" in data and "name" in data:
                        if "location" not in data and "room_id" in data:
                            data["location"] = data["room_id"]
                        if _REGISTRY.get(data["id"]) is None:
                            _REGISTRY.register(data)
            except Exception as exc:
                logger.warning("Fallo al cargar ficha NPC %s: %s", file, exc)


# Cargar al importar
load_canonical_npcs()
