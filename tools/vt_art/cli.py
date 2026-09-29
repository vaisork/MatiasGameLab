from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .pipeline import (
    ArtPipeline,
    ArtPipelineError,
    ArtRequest,
    DEFAULT_GENERATIONS,
    OpenAIImageClient,
    ROOT,
    VALID_STATES,
    _write_new_file,
)


DEFAULT_MODEL = "gpt-image-2.5-flare"
ENV_FILE = ROOT / "vintage-telnet" / ".env"


def load_local_config() -> None:
    """Load only the art-tool settings; shell environment takes precedence."""
    try:
        lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return
    except OSError as exc:
        raise ArtPipelineError(f"No se pudo leer la configuración local: {ENV_FILE}") from exc
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, sep, value = line.partition("=")
        if not sep or key.strip() not in {"OPENAI_API_KEY", "VT_ART_MODEL"}:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.vt_art",
        description="Genera y versiona borradores de arte de Vintage Telnet con OpenAI Image API.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("generate", "Generar una imagen desde una ficha."),
        ("variants", "Generar varias versiones independientes desde una ficha."),
    ):
        command = sub.add_parser(name, help=help_text)
        command.add_argument("request", type=Path, help="Ruta de la ficha JSON.")
        if name == "variants":
            command.add_argument("--count", type=int, default=3, help="Cantidad de generaciones (1–10).")
        command.add_argument("--model", help="Sobrescribe VT_ART_MODEL para esta ejecución.")
    batch = sub.add_parser("batch", help="Procesar todas las fichas JSON de una carpeta.")
    batch.add_argument("requests_dir", type=Path)
    batch.add_argument("--model", help="Sobrescribe VT_ART_MODEL para esta ejecución.")
    status = sub.add_parser("status", help="Consultar o actualizar el estado de las versiones de un asset.")
    status.add_argument("asset_id")
    status.add_argument("--set", choices=sorted(VALID_STATES), dest="state")
    status.add_argument("--version", help="Versión exacta, por ejemplo v002; sin esto se actualiza la más reciente.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        load_local_config()
        if args.command == "status":
            results = ArtPipeline(client=None, model="").status(  # type: ignore[arg-type]
                DEFAULT_GENERATIONS, args.asset_id, args.state, args.version
            )
            for item in results:
                print(f"{item['asset_id']} {item['version']}: {item['status']} · {item['image']}")
            return 0

        model = args.model or os.environ.get("VT_ART_MODEL") or DEFAULT_MODEL
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ArtPipelineError(
                f"Falta OPENAI_API_KEY. Añádela a {ENV_FILE} o expórtala en el entorno; no la pegues en la ficha."
            )
        pipeline = ArtPipeline(OpenAIImageClient(api_key), model)

        if args.command in {"generate", "variants"}:
            request = ArtRequest.load(args.request)
            count = 1 if args.command == "generate" else args.count
            if not 1 <= count <= 10:
                raise ArtPipelineError("count debe estar entre 1 y 10.")
            result = _run_variants(pipeline, request, count)
            _print_summary(result)
            return 0 if not result["failures"] else 1

        if args.command == "batch":
            results = _run_batch(pipeline, args.requests_dir)
            _print_summary(results)
            return 0 if not results["failures"] else 1
        parser.error("Comando desconocido")
    except ArtPipelineError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 2


def _run_variants(pipeline: ArtPipeline, request: ArtRequest, count: int) -> dict[str, Any]:
    batch_id = str(uuid.uuid4())
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    attempted = 0
    for index in range(count):
        attempted += 1
        try:
            metadata = pipeline.generate(request)
            results.append({"version": metadata["version"], "image": metadata["image"], "usage": metadata["usage"]})
        except Exception as exc:  # preserve earlier drafts even if a later request fails
            failures.append(_safe_failure(index + 1, exc))
            break
    summary = _summary_document(batch_id, [request.asset_id], attempted, results, failures, pipeline.model)
    _save_batch_summary(request.output_destination, summary)
    return summary


def _run_batch(
    pipeline: ArtPipeline,
    requests_dir: Path,
    generation_root: Path = DEFAULT_GENERATIONS,
) -> dict[str, Any]:
    requests_dir = requests_dir.resolve()
    if not requests_dir.is_dir():
        raise ArtPipelineError(f"No existe la carpeta de fichas: {requests_dir}")
    files = sorted(p for p in requests_dir.glob("*.json") if p.is_file() and p.name != "template.json")
    if not files:
        raise ArtPipelineError(f"No hay fichas JSON en {requests_dir}.")
    batch_id = str(uuid.uuid4())
    completed: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    attempted = 0
    for file_index, path in enumerate(files):
        try:
            request = ArtRequest.load(path, ROOT, generation_root)
        except ArtPipelineError as exc:
            failures.append({"request_file": str(path), "error": str(exc)})
            continue
        attempted += 1
        try:
            metadata = pipeline.generate(request)
            completed.append({"asset_id": request.asset_id, "version": metadata["version"], "image": metadata["image"], "usage": metadata["usage"]})
        except Exception as exc:
            failures.append(_safe_failure(attempted, exc, str(path)))
            failures.extend(
                {"request_file": str(skipped), "status": "not_attempted_after_error"}
                for skipped in files[file_index + 1 :]
            )
            break
    summary = _summary_document(batch_id, [x.get("asset_id", "") for x in completed], attempted, completed, failures, pipeline.model)
    _save_batch_summary(generation_root, summary)
    return summary


def _summary_document(batch_id: str, asset_ids: list[str], attempted: int, completed: list[dict[str, Any]], failures: list[dict[str, Any]], model: str) -> dict[str, Any]:
    usage_items = [item.get("usage") for item in completed if item.get("usage")]
    return {
        "batch_id": batch_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "asset_ids": asset_ids,
        "model_id": model,
        "request_count": attempted,
        "generation_count": len(completed),
        "completed": completed,
        "failures": failures,
        "usage": usage_items,
        "usage_totals": _sum_usage(usage_items),
        "cost_estimate": None,
    }


def _save_batch_summary(destination: Path, summary: dict[str, Any]) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / f"batch-{summary['batch_id']}.json"
    _write_new_file(path, (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode())
    summary["summary_file"] = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def _safe_failure(index: int, exc: Exception, request_file: str | None = None) -> dict[str, Any]:
    # Never print exception text: HTTP errors can include request details. Keep only non-secret diagnostics.
    code = getattr(exc, "code", None)
    request_id = getattr(exc, "request_id", None) or getattr(exc, "requestID", None)
    status = getattr(exc, "status_code", None)
    result: dict[str, Any] = {"item": index, "error_type": type(exc).__name__}
    if isinstance(code, str):
        result["error_code"] = code
    if isinstance(status, int):
        result["http_status"] = status
    if isinstance(request_id, str):
        result["request_id"] = request_id
    if request_file:
        result["request_file"] = request_file
    kind = type(exc).__name__
    hints = {
        "AuthenticationError": "Revisa OPENAI_API_KEY y el acceso de la cuenta a Image API.",
        "PermissionDeniedError": "La cuenta no tiene acceso a ese modelo o endpoint.",
        "RateLimitError": "Se alcanzó un límite. Espera antes de volver a intentarlo.",
        "APITimeoutError": "La solicitud agotó el tiempo. No hubo reintento automático; verifica el lote y reintenta manualmente.",
        "APIConnectionError": "No se pudo conectar con OpenAI. No hubo reintento automático.",
        "BadRequestError": "OpenAI rechazó la ficha o sus referencias; revisa el error y corrige la ficha antes de reintentar.",
        "OSError": "Falló la escritura local después de la solicitud. Revisa permisos y espacio disponible.",
    }
    if kind in hints:
        result["hint"] = hints[kind]
    return result


def _print_summary(summary: dict[str, Any]) -> None:
    print(f"Lote {summary['batch_id']}: {summary['request_count']} requests, {summary['generation_count']} drafts.")
    for item in summary["completed"]:
        print(f"  OK {item.get('asset_id', '')} {item['version']}: {item['image']}")
    for item in summary["failures"]:
        print(f"  ERROR request {item.get('item', '?')}: {item.get('error_type', item.get('error', 'Error'))} ({item.get('error_code', 'sin código')})")
        if item.get("hint"):
            print(f"    {item['hint']}")
    if summary.get("summary_file"):
        print(f"Resumen: {summary['summary_file']}")
    if not summary.get("usage"):
        print("Uso/costo exacto: la API no entregó datos de uso para este lote.")


def _sum_usage(items: list[dict[str, Any]]) -> dict[str, Any]:
    totals: dict[str, Any] = {}
    for item in items:
        _merge_numeric_usage(totals, item)
    return totals


def _merge_numeric_usage(target: dict[str, Any], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            target[key] = target.get(key, 0) + value
        elif isinstance(value, dict):
            child = target.setdefault(key, {})
            if isinstance(child, dict):
                _merge_numeric_usage(child, value)


if __name__ == "__main__":
    raise SystemExit(main())
