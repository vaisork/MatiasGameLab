"""Adapter between the authoritative NPC generator and one-shot personality enrichment.

This module does not call Ollama directly. It validates and normalizes generator output,
then hands the authoritative record to PR #20's enrich_personality_once(). For local
tests, an enrichment function may be injected.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Iterable

REQUIRED_FIELDS = {
    "id",
    "name",
    "species",
    "settlement",
    "location",
    "role",
    "relationships",
    "knowledge_allowed",
    "knowledge_forbidden",
    "beliefs_uncertain",
    "initial_talk",
    "conditional_knowledge",
    "narrative_function",
    "gameplay_function",
    "memory_hooks",
}

_RESERVED_PERSONALITY_FIELDS = {
    "personality",
    "personality_locked",
    "personality_provenance",
}


class NpcGeneratorContractError(ValueError):
    """Raised when generator output does not satisfy the authoritative NPC contract."""


def _require_text(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise NpcGeneratorContractError(f"{key} must be a non-empty string")
    return value.strip()


def _require_string_list(record: dict[str, Any], key: str) -> list[str]:
    value = record.get(key)
    if not isinstance(value, list):
        raise NpcGeneratorContractError(f"{key} must be a list")
    result: list[str] = []
    for idx, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise NpcGeneratorContractError(
                f"{key}[{idx}] must be a non-empty string"
            )
        result.append(item.strip())
    return result


def _require_dict_list(record: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = record.get(key)
    if not isinstance(value, list):
        raise NpcGeneratorContractError(f"{key} must be a list")
    result: list[dict[str, Any]] = []
    for idx, item in enumerate(value):
        if not isinstance(item, dict):
            raise NpcGeneratorContractError(f"{key}[{idx}] must be an object")
        result.append(deepcopy(item))
    return result


def normalize_authoritative_npc(record: Any) -> dict[str, Any]:
    """Return the stable authoritative JSON record expected by the personality bridge."""
    if not isinstance(record, dict):
        raise NpcGeneratorContractError("NPC generator output must be a JSON object")

    forbidden = _RESERVED_PERSONALITY_FIELDS.intersection(record)
    if forbidden:
        raise NpcGeneratorContractError(
            "generator output must not pre-populate personality fields: "
            + ", ".join(sorted(forbidden))
        )

    missing = REQUIRED_FIELDS - set(record)
    if missing:
        raise NpcGeneratorContractError(
            "missing authoritative fields: " + ", ".join(sorted(missing))
        )

    normalized = deepcopy(record)
    for key in (
        "id",
        "name",
        "species",
        "settlement",
        "location",
        "role",
        "narrative_function",
        "gameplay_function",
    ):
        normalized[key] = _require_text(record, key)

    normalized["relationships"] = _require_dict_list(record, "relationships")
    normalized["knowledge_allowed"] = _require_string_list(record, "knowledge_allowed")
    normalized["knowledge_forbidden"] = _require_string_list(record, "knowledge_forbidden")
    normalized["beliefs_uncertain"] = _require_string_list(record, "beliefs_uncertain")
    normalized["initial_talk"] = _require_string_list(record, "initial_talk")
    normalized["conditional_knowledge"] = _require_dict_list(
        record, "conditional_knowledge"
    )
    normalized["memory_hooks"] = _require_string_list(record, "memory_hooks")

    if not normalized["knowledge_forbidden"]:
        raise NpcGeneratorContractError(
            "knowledge_forbidden must explicitly describe at least one knowledge boundary"
        )

    return normalized


def _default_enrich_fn():
    try:
        from server.npc_personality import enrich_personality_once
    except ImportError as exc:
        raise RuntimeError(
            "PR #20 personality bridge is not available on this branch; "
            "inject enrich_fn for local development or integrate after PR #20."
        ) from exc
    return enrich_personality_once


def enrich_generated_npc(
    record: Any,
    personality_client: Any,
    *,
    enrich_fn: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise NpcGeneratorContractError("NPC generator output must be a JSON object")

    already_locked = record.get("personality_locked") is True
    if already_locked:
        authoritative_source = {
            key: deepcopy(value)
            for key, value in record.items()
            if key not in _RESERVED_PERSONALITY_FIELDS
        }
        authoritative = normalize_authoritative_npc(authoritative_source)
        bridge_input = deepcopy(record)
    else:
        authoritative = normalize_authoritative_npc(record)
        bridge_input = authoritative

    before = deepcopy(authoritative)
    fn = enrich_fn or _default_enrich_fn()
    enriched = fn(bridge_input, personality_client)

    if not isinstance(enriched, dict):
        raise NpcGeneratorContractError("personality bridge must return an NPC object")

    for key, value in before.items():
        if enriched.get(key) != value:
            raise NpcGeneratorContractError(
                f"authoritative field changed after enrichment: {key}"
            )

    if enriched.get("personality_locked") is not True:
        raise NpcGeneratorContractError(
            "personality bridge did not set personality_locked=true"
        )
    if not isinstance(enriched.get("personality"), dict):
        raise NpcGeneratorContractError("personality bridge did not return personality")
    if not isinstance(enriched.get("personality_provenance"), dict):
        raise NpcGeneratorContractError(
            "personality bridge did not return personality_provenance"
        )
    return enriched


def enrich_generated_batch(
    records: Iterable[Any],
    personality_client: Any,
    *,
    enrich_fn: Callable[..., dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Enrich several already-authored NPC records without inventing any new NPCs."""
    result: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, record in enumerate(records):
        normalized = normalize_authoritative_npc(record)
        npc_id = normalized["id"]
        if npc_id in seen_ids:
            raise NpcGeneratorContractError(
                f"duplicate NPC id in batch at index {index}: {npc_id}"
            )
        seen_ids.add(npc_id)
        result.append(
            enrich_generated_npc(
                normalized,
                personality_client,
                enrich_fn=enrich_fn,
            )
        )
    return result
