"""CLI bridge: generator JSON -> Ollama personality -> locked NPC JSON.

Examples:
  python -m server.npc_personality_cli npc.json
  python -m server.npc_personality_cli npc.json --in-place
  python -m server.npc_personality_cli npc.json --output npc-ready.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile

from .npc_personality import (
    OllamaPersonalityClient,
    PersonalityError,
    enrich_personality_once,
)


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=path.name + ".",
        suffix=".tmp",
        delete=False,
    ) as temp:
        temp.write(content)
        temp_path = Path(temp.name)
    temp_path.replace(path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Añade personalidad Ollama una sola vez a un NPC autoritativo."
    )
    parser.add_argument("input", type=Path, help="Ficha JSON producida por el generador de NPCs.")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--in-place", action="store_true", help="Reemplaza el archivo de entrada atómicamente.")
    destination.add_argument("--output", type=Path, help="Escribe el NPC enriquecido en otro archivo.")
    parser.add_argument("--ollama-url", default=None, help="Por defecto VT_OLLAMA_URL o http://127.0.0.1:11434.")
    parser.add_argument("--model", default=None, help="Por defecto VT_OLLAMA_NPC_MODEL; si hay un solo modelo instalado se autodetecta.")
    parser.add_argument("--timeout", type=float, default=180.0)
    args = parser.parse_args(argv)

    try:
        npc = json.loads(args.input.read_text(encoding="utf-8"))
        client = OllamaPersonalityClient(
            base_url=args.ollama_url,
            model=args.model,
            timeout=args.timeout,
        )
        enriched = enrich_personality_once(npc, client)
        rendered = json.dumps(enriched, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

        if args.in_place:
            _write_atomic(args.input, rendered)
        elif args.output:
            _write_atomic(args.output, rendered)
        else:
            sys.stdout.write(rendered)
        return 0
    except (OSError, json.JSONDecodeError, PersonalityError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
