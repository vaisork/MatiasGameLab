"""One-shot Ollama personality bridge for Vintage Telnet NPCs.

The NPC generator is authoritative. Ollama may only add personality/voice once.
This module does not expose Ollama to gameplay routes and does not let the
model modify canon, knowledge, relationships, abilities, inventory or state.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROMPT_VERSION = "vt-npc-personality-v1"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"

_RESERVED_KEYS = {
    "personality",
    "personality_locked",
    "personality_provenance",
}

_ALLOWED_PERSONALITY_KEYS = {
    "temperament",
    "speech_style",
    "formality",
    "humor",
    "sociability",
    "response_length",
    "expressive_reactions",
    "traits",
    "example_phrases",
}

_REQUIRED_PERSONALITY_KEYS = set(_ALLOWED_PERSONALITY_KEYS)

_ENUMS = {
    "formality": {"muy_informal", "informal", "neutral", "formal", "muy_formal"},
    "response_length": {"breve", "media", "amplia"},
}


class PersonalityError(RuntimeError):
    """Raised when personality generation or validation cannot be completed."""


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _require_text(value: Any, field: str, *, max_length: int = 400) -> str:
    if not isinstance(value, str):
        raise PersonalityError(f"{field} debe ser texto.")
    value = value.strip()
    if not value:
        raise PersonalityError(f"{field} no puede estar vacío.")
    if len(value) > max_length:
        raise PersonalityError(f"{field} excede {max_length} caracteres.")
    return value


def _require_text_list(
    value: Any,
    field: str,
    *,
    min_items: int,
    max_items: int,
    max_length: int = 220,
) -> list[str]:
    if not isinstance(value, list):
        raise PersonalityError(f"{field} debe ser una lista.")
    if not min_items <= len(value) <= max_items:
        raise PersonalityError(
            f"{field} debe contener entre {min_items} y {max_items} elementos."
        )
    return [
        _require_text(item, f"{field}[{index}]", max_length=max_length)
        for index, item in enumerate(value)
    ]


def validate_personality(payload: Any) -> dict[str, Any]:
    """Validate the only data Ollama is allowed to create."""
    if not isinstance(payload, dict):
        raise PersonalityError("La respuesta de personalidad debe ser un objeto JSON.")

    keys = set(payload)
    missing = _REQUIRED_PERSONALITY_KEYS - keys
    extra = keys - _ALLOWED_PERSONALITY_KEYS
    if missing:
        raise PersonalityError(
            "Faltan campos de personalidad: " + ", ".join(sorted(missing))
        )
    if extra:
        raise PersonalityError(
            "Ollama intentó devolver campos no autorizados: " + ", ".join(sorted(extra))
        )

    result = {
        "temperament": _require_text(payload["temperament"], "temperament"),
        "speech_style": _require_text(payload["speech_style"], "speech_style"),
        "formality": _require_text(payload["formality"], "formality", max_length=32),
        "humor": _require_text(payload["humor"], "humor"),
        "sociability": _require_text(payload["sociability"], "sociability"),
        "response_length": _require_text(
            payload["response_length"], "response_length", max_length=16
        ),
        "expressive_reactions": _require_text_list(
            payload["expressive_reactions"],
            "expressive_reactions",
            min_items=1,
            max_items=6,
        ),
        "traits": _require_text_list(
            payload["traits"], "traits", min_items=2, max_items=6, max_length=120
        ),
        "example_phrases": _require_text_list(
            payload["example_phrases"],
            "example_phrases",
            min_items=3,
            max_items=6,
            max_length=220,
        ),
    }

    for field, allowed in _ENUMS.items():
        if result[field] not in allowed:
            raise PersonalityError(
                f"{field} debe ser uno de: {', '.join(sorted(allowed))}."
            )
    return result


def _authoritative_view(npc: dict[str, Any]) -> dict[str, Any]:
    """Everything except personality fields remains generator-owned and immutable."""
    return {key: deepcopy(value) for key, value in npc.items() if key not in _RESERVED_KEYS}


def _validate_npc_identity(npc: Any) -> None:
    if not isinstance(npc, dict):
        raise PersonalityError("El NPC debe ser un objeto JSON.")
    npc_id = npc.get("id") or npc.get("npc_id")
    if not isinstance(npc_id, str) or not npc_id.strip():
        raise PersonalityError("El NPC necesita id o npc_id antes de generar personalidad.")
    name = npc.get("name") or npc.get("nombre")
    if not isinstance(name, str) or not name.strip():
        raise PersonalityError("El NPC necesita name o nombre antes de generar personalidad.")


class OllamaPersonalityClient:
    """Minimal stdlib-only client for a local Ollama server."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float = 45.0,
    ):
        self.base_url = (base_url or os.environ.get("VT_OLLAMA_URL") or DEFAULT_OLLAMA_URL).rstrip("/")
        self.model = model or os.environ.get("VT_OLLAMA_NPC_MODEL") or None
        self.timeout = timeout

    def _json_request(self, path: str, *, method: str = "GET", payload: Any = None) -> Any:
        data = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(
            self.base_url + path,
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise PersonalityError(
                f"Ollama respondió HTTP {exc.code}: {detail[:300]}"
            ) from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise PersonalityError(f"No se pudo contactar Ollama en {self.base_url}: {exc}") from exc
        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise PersonalityError("Ollama devolvió una respuesta HTTP que no es JSON.") from exc

    def resolve_model(self) -> str:
        if self.model:
            return self.model
        tags = self._json_request("/api/tags")
        models = [
            item.get("name")
            for item in tags.get("models", [])
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        ]
        models = [name for name in models if name]
        if not models:
            raise PersonalityError(
                "Ollama está disponible pero no tiene modelos instalados."
            )
        if len(models) > 1:
            raise PersonalityError(
                "Hay varios modelos Ollama instalados. Define VT_OLLAMA_NPC_MODEL "
                "o usa --model. Disponibles: " + ", ".join(models)
            )
        self.model = models[0]
        return self.model

    def generate_personality(self, authoritative_npc: dict[str, Any]) -> dict[str, Any]:
        model = self.resolve_model()
        system = (
            "Eres la capa de actuación de NPCs de Vintage Telnet. "
            "La ficha recibida es AUTORITATIVA e INMUTABLE. "
            "No inventes ni cambies hechos del mundo, identidad, especie, oficio, "
            "relaciones, conocimientos, secretos, capacidades, objetos, poderes, "
            "ubicaciones, eventos ni estado. Solo crea personalidad y voz. "
            "Responde exclusivamente con JSON usando exactamente estos campos: "
            "temperament, speech_style, formality, humor, sociability, "
            "response_length, expressive_reactions, traits, example_phrases. "
            "formality debe ser uno de muy_informal, informal, neutral, formal, muy_formal. "
            "response_length debe ser breve, media o amplia. "
            "example_phrases contiene entre 3 y 6 frases de muestra coherentes con la ficha; "
            "las frases no pueden añadir hechos nuevos."
        )
        prompt = (
            "Genera una personalidad estable para este NPC. "
            "No repitas ni reescribas la ficha autoritativa.\n\n"
            + json.dumps(authoritative_npc, ensure_ascii=False, sort_keys=True)
        )
        raw = self._json_request(
            "/api/generate",
            method="POST",
            payload={
                "model": model,
                "system": system,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.65},
            },
        )
        response_text = raw.get("response")
        if not isinstance(response_text, str) or not response_text.strip():
            raise PersonalityError("Ollama no devolvió el campo response esperado.")
        try:
            personality = json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise PersonalityError("Ollama no devolvió JSON válido en response.") from exc
        return validate_personality(personality)


def enrich_personality_once(
    npc: dict[str, Any],
    client: OllamaPersonalityClient,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Add a personality exactly once without changing generator-owned fields."""
    _validate_npc_identity(npc)

    if npc.get("personality_locked") is True:
        if "personality" not in npc:
            raise PersonalityError(
                "personality_locked=true pero falta personality; registro inconsistente."
            )
        validate_personality(npc["personality"])
        return deepcopy(npc)

    if "personality" in npc or "personality_provenance" in npc:
        raise PersonalityError(
            "El NPC ya contiene datos de personalidad sin lock. "
            "No se sobrescriben automáticamente."
        )

    before = _authoritative_view(npc)
    personality = client.generate_personality(before)
    result = deepcopy(npc)
    result["personality"] = personality
    result["personality_provenance"] = {
        "ollama_model": client.model,
        "personality_prompt_version": PROMPT_VERSION,
        "personality_generated_at": generated_at or utcnow(),
    }
    result["personality_locked"] = True

    if _authoritative_view(result) != before:
        raise PersonalityError("La integración alteró campos autoritativos del NPC.")
    return result
