"""Vision-based self-critique of a generated draft against its own approved
brief. Runs right after generation, before a PR is opened, so nobody has to
eyeball every image by hand -- and so it works even though GPT Actions-based
chats (like the Art Director's) cannot receive images at all (documented
platform limit, not a bug: platform.openai.com/docs/actions/sending-files).

Uses a cheap text+vision chat model -- never the image-generation model --
called directly by API, so there is no chat/Action in the loop to fail.
"""
from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any, Protocol

from .pipeline import ArtPipelineError, ArtRequest


# USD por millon de tokens. Confirmado contra developers.openai.com/api/docs
# (2026-09-30). Un modelo ausente de esta tabla no hace fallar la critica:
# cost_estimate simplemente queda en None.
CRITIQUE_TOKEN_PRICING_USD_PER_MILLION: dict[str, dict[str, float]] = {
    "gpt-5-mini": {"input": 0.25, "output": 2.00},
}


@dataclass(frozen=True)
class CritiqueResult:
    passes: bool
    issues: tuple[str, ...]
    reasoning: str
    model: str
    usage: dict[str, Any]
    cost_estimate: float | None


class VisionCriticClient(Protocol):
    def critique(
        self, *, image_bytes: bytes, image_format: str, brief: str, model: str
    ) -> tuple[dict[str, Any], dict[str, Any]]: ...


class OpenAIVisionCritic:
    def __init__(self, api_key: str, timeout: float = 120.0, sdk_client: Any | None = None):
        if sdk_client is not None:
            self.client = sdk_client
            return
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ArtPipelineError("Falta el SDK. Instala vintage-telnet/tools/vt_art/requirements.txt.") from exc
        self.client = OpenAI(api_key=api_key, timeout=timeout, max_retries=0)

    def critique(
        self, *, image_bytes: bytes, image_format: str, brief: str, model: str
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        encoded = base64.b64encode(image_bytes).decode("ascii")
        response = self.client.responses.create(
            model=model,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": brief},
                    {"type": "input_image", "image_url": f"data:image/{image_format};base64,{encoded}"},
                ],
            }],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "art_critique",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "passes": {"type": "boolean"},
                            "issues": {"type": "array", "items": {"type": "string"}},
                            "reasoning": {"type": "string"},
                        },
                        "required": ["passes", "issues", "reasoning"],
                        "additionalProperties": False,
                    },
                },
            },
        )
        output_text = getattr(response, "output_text", None)
        if not output_text:
            raise ArtPipelineError("La crítica no devolvió texto estructurado.")
        try:
            verdict = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise ArtPipelineError("La crítica devolvió JSON inválido.") from exc
        usage = _to_jsonable(getattr(response, "usage", None)) or {}
        return verdict, usage


def build_critique_brief(request: ArtRequest) -> str:
    sections = [
        "You are reviewing ONE generated draft image against its approved art "
        "brief for the game Vintage Telnet. Judge strictly what is visible in "
        "the image; never judge artistic style or taste.",
        f"Canonical name: {request.canonical_name}",
        f"Art direction: {request.art_direction}",
    ]
    if request.canon_sources:
        sections.append("Canon sources supplied by the Art Director: " + "; ".join(request.canon_sources))
    if request.negative_constraints:
        sections.append("The image MUST NOT show any of: " + "; ".join(request.negative_constraints))
    sections.append(
        "Set passes=true only if the image clearly satisfies the art "
        "direction above and violates none of the negative constraints. "
        "Otherwise set passes=false and list every violated constraint or "
        "missing required element in issues, one short plain-language item "
        "each, specific enough that someone could fix the prompt from it."
    )
    return "\n\n".join(sections)


def critique_generation(
    client: VisionCriticClient,
    model: str,
    request: ArtRequest,
    image_bytes: bytes,
    image_format: str,
) -> CritiqueResult:
    brief = build_critique_brief(request)
    verdict, usage = client.critique(
        image_bytes=image_bytes, image_format=image_format, brief=brief, model=model
    )
    if not isinstance(verdict, dict) or "passes" not in verdict:
        raise ArtPipelineError("La crítica no devolvió un veredicto reconocible.")
    return CritiqueResult(
        passes=bool(verdict.get("passes")),
        issues=tuple(str(item) for item in verdict.get("issues") or ()),
        reasoning=str(verdict.get("reasoning", "")),
        model=model,
        usage=usage,
        cost_estimate=estimate_critique_cost_usd(model, usage),
    )


def estimate_critique_cost_usd(model: str, usage: dict[str, Any] | None) -> float | None:
    pricing = CRITIQUE_TOKEN_PRICING_USD_PER_MILLION.get(model)
    if not pricing or not usage:
        return None
    try:
        input_tokens = float(usage.get("input_tokens", 0) or 0)
        output_tokens = float(usage.get("output_tokens", 0) or 0)
    except (TypeError, ValueError):
        return None
    cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000
    return round(cost, 6)


def _to_jsonable(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        dumped = value.model_dump(mode="json")
        return dumped if isinstance(dumped, dict) else None
    if isinstance(value, dict):
        return value
    try:
        return json.loads(json.dumps(value))
    except (TypeError, ValueError):
        return None
