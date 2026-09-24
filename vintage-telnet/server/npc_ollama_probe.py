"""Probe read-only de compatibilidad Ollama para personalidad NPC.

No persiste NPCs, no toca SQLite y no modifica configuración de Ollama.
Prueba el contrato de personalidad contra uno o todos los modelos instalados.
"""
from __future__ import annotations

import argparse
import json
import time

try:
    from .npc_personality import OllamaPersonalityClient, PersonalityError
except ImportError:
    from npc_personality import OllamaPersonalityClient, PersonalityError


SYNTHETIC_NPC = {
    "id": "synthetic_probe_01",
    "name": "Daro",
    "species": "humano",
    "town": "Valdren",
    "role": "herrero",
    "knowledge_allowed": ["forja local", "caminos cercanos"],
    "knowledge_forbidden": ["secreto_sintetico"],
    "relationships": [],
}


def installed_models(base_url: str, timeout: float) -> list[str]:
    client = OllamaPersonalityClient(base_url=base_url, model="probe", timeout=timeout)
    payload = client._json_request("/api/tags")
    return [
        item["name"]
        for item in payload.get("models", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--model", action="append", help="Modelo concreto; puede repetirse.")
    parser.add_argument("--timeout", type=float, default=180.0)
    args = parser.parse_args()

    models = args.model or installed_models(args.base_url, args.timeout)
    if not models:
        print("No se detectaron modelos Ollama.")
        return 2

    failures = 0
    print("Modelos a probar:", ", ".join(models))
    for model in models:
        started = time.monotonic()
        client = OllamaPersonalityClient(
            base_url=args.base_url,
            model=model,
            timeout=args.timeout,
        )
        try:
            personality = client.generate_personality(SYNTHETIC_NPC)
        except PersonalityError as exc:
            failures += 1
            elapsed = time.monotonic() - started
            print(f"[FAIL] {model} ({elapsed:.1f}s): {exc}")
            continue

        elapsed = time.monotonic() - started
        print(f"[OK] {model} ({elapsed:.1f}s)")
        print(json.dumps(personality, ensure_ascii=False, sort_keys=True))

    print(f"Resultado: {len(models) - failures}/{len(models)} modelos compatibles.")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
