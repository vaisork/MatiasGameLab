from __future__ import annotations

import base64
import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GENERATIONS = ROOT / "vintage-telnet" / "art_generations"
ASSET_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$")
VALID_STATES = {"draft", "review", "approved", "published"}


class ArtPipelineError(Exception):
    """A user-correctable pipeline error with no secret-bearing detail."""


@dataclass(frozen=True)
class ArtRequest:
    asset_id: str
    asset_type: str
    target: str
    canonical_name: str
    art_direction: str
    prompt: str
    references: tuple[Path, ...]
    negative_constraints: tuple[str, ...]
    aspect_ratio: str
    output_destination: Path
    requested_status: str
    source_request: Path
    canon_sources: tuple[str, ...] = ()
    room_id: str | None = None
    creature_id: str | None = None
    species_id: str | None = None
    prior_asset: Path | None = None
    edit_source: Path | None = None
    variation_of: str | None = None
    notes: str | None = None
    quality: str = "low"
    output_format: str = "png"
    output_compression: int | None = None
    background: str = "auto"

    @classmethod
    def load(
        cls,
        path: Path,
        project_root: Path = ROOT,
        generation_root: Path = DEFAULT_GENERATIONS,
    ) -> "ArtRequest":
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ArtPipelineError(f"No existe la ficha: {path}") from exc
        except (OSError, json.JSONDecodeError) as exc:
            raise ArtPipelineError(f"No se pudo leer la ficha JSON: {path}") from exc
        if not isinstance(raw, dict):
            raise ArtPipelineError("La ficha debe contener un objeto JSON.")

        required = (
            "asset_id", "asset_type", "target", "canonical_name",
            "art_direction", "prompt", "aspect_ratio", "output_destination",
        )
        missing = [key for key in required if not isinstance(raw.get(key), str) or not raw[key].strip()]
        if missing:
            raise ArtPipelineError("Faltan campos obligatorios: " + ", ".join(missing))

        asset_id = raw["asset_id"].strip()
        if not ASSET_ID_RE.fullmatch(asset_id):
            raise ArtPipelineError("asset_id debe usar solo letras, números, guion y guion bajo.")

        references = _resolve_image_list(raw.get("references", []), path.parent)
        prior_asset = _resolve_optional_image(raw.get("prior_asset"), path.parent)
        edit_source = _resolve_optional_image(raw.get("edit_source"), path.parent)
        if prior_asset:
            references += (prior_asset,)
        if edit_source:
            references += (edit_source,)
        if len(set(references)) != len(references):
            references = tuple(dict.fromkeys(references))

        negative = _string_tuple(raw.get("negative_constraints", []), "negative_constraints")
        canon_sources = _string_tuple(raw.get("canon_sources", []), "canon_sources")
        requested_status = raw.get("status", "draft")
        if not isinstance(requested_status, str) or requested_status not in VALID_STATES:
            raise ArtPipelineError("status debe ser draft, review, approved o published.")
        if requested_status != "draft":
            raise ArtPipelineError("Toda generación nueva comienza en draft; el estado se cambia después de revisar.")

        quality = raw.get("quality", "low")
        if quality not in {"low", "medium", "high", "xhigh", "max", "auto"}:
            raise ArtPipelineError("quality no está soportada.")
        output_format = raw.get("output_format", "png")
        if output_format not in {"png", "jpeg", "webp"}:
            raise ArtPipelineError("output_format debe ser png, jpeg o webp.")
        background = raw.get("background", "auto")
        if background not in {"auto", "opaque", "transparent"}:
            raise ArtPipelineError("background debe ser auto, opaque o transparent.")
        compression = raw.get("output_compression")
        if compression is not None and (not isinstance(compression, int) or not 0 <= compression <= 100):
            raise ArtPipelineError("output_compression debe ser un entero de 0 a 100.")
        if compression is not None and output_format not in {"jpeg", "webp"}:
            raise ArtPipelineError("output_compression sólo se usa con JPEG o WebP.")
        if background == "transparent" and output_format not in {"png", "webp"}:
            raise ArtPipelineError("Un fondo transparente requiere PNG o WebP.")

        destination = (project_root / raw["output_destination"]).resolve()
        safe_root = generation_root.resolve()
        if destination != safe_root and safe_root not in destination.parents:
            raise ArtPipelineError("output_destination debe permanecer dentro de vintage-telnet/art_generations/.")

        optional_text = ("room_id", "creature_id", "species_id", "variation_of", "notes")
        optional = {key: _optional_text(raw.get(key), key) for key in optional_text}
        return cls(
            asset_id=asset_id,
            asset_type=raw["asset_type"].strip(),
            target=raw["target"].strip(),
            canonical_name=raw["canonical_name"].strip(),
            art_direction=raw["art_direction"].strip(),
            prompt=raw["prompt"].strip(),
            references=references,
            negative_constraints=negative,
            aspect_ratio=raw["aspect_ratio"].strip(),
            output_destination=destination,
            requested_status=requested_status,
            source_request=path.resolve(),
            canon_sources=canon_sources,
            quality=quality,
            output_format=output_format,
            output_compression=compression,
            background=background,
            **optional,
        )


class ImageClient(Protocol):
    def generate(self, *, prompt: str, model: str, request: ArtRequest) -> tuple[bytes, dict[str, Any], str | None]: ...


class OpenAIImageClient:
    def __init__(self, api_key: str, timeout: float = 180.0, sdk_client: Any | None = None):
        if sdk_client is not None:
            self.client = sdk_client
            return
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ArtPipelineError("Falta el SDK. Instala vintage-telnet/tools/vt_art/requirements.txt.") from exc
        self.client = OpenAI(api_key=api_key, timeout=timeout, max_retries=0)

    def generate(self, *, prompt: str, model: str, request: ArtRequest) -> tuple[bytes, dict[str, Any], str | None]:
        params: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "size": size_for_aspect(request.aspect_ratio),
            "quality": request.quality,
            "output_format": request.output_format,
            "background": request.background,
            "n": 1,
        }
        if request.output_compression is not None and request.output_format in {"jpeg", "webp"}:
            params["output_compression"] = request.output_compression

        if request.references:
            handles = []
            try:
                for path in request.references:
                    handles.append(path.open("rb"))
                response = self.client.images.edit(image=handles, **params)
            finally:
                for handle in handles:
                    handle.close()
        else:
            response = self.client.images.generate(**params)

        data = getattr(response, "data", None) or []
        if not data or not getattr(data[0], "b64_json", None):
            raise ArtPipelineError("La API respondió sin una imagen codificada.")
        usage = _to_jsonable(getattr(response, "usage", None))
        request_id = getattr(response, "_request_id", None) or getattr(response, "request_id", None)
        return base64.b64decode(data[0].b64_json, validate=True), usage or {}, request_id


class ArtPipeline:
    def __init__(self, client: ImageClient, model: str):
        self.client = client
        self.model = model

    def generate(self, request: ArtRequest) -> dict[str, Any]:
        prompt = build_prompt(request)
        image_bytes, usage, request_id = self.client.generate(
            prompt=prompt, model=self.model, request=request
        )
        version_dir, version = _claim_version(request.output_destination, request.asset_id)
        ext = "jpg" if request.output_format == "jpeg" else request.output_format
        image_path = version_dir / f"{request.asset_id}_{version}.{ext}"
        _write_new_file(image_path, image_bytes)
        generation_id = str(uuid.uuid4())
        metadata = {
            "asset_id": request.asset_id,
            "generation_id": generation_id,
            "version": version,
            "prompt": prompt,
            "model_id": self.model,
            "parameters": {
                "quality": request.quality,
                "size": size_for_aspect(request.aspect_ratio),
                "output_format": request.output_format,
                "output_compression": request.output_compression,
                "background": request.background,
                "reference_files": [str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else p.name for p in request.references],
            },
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "status": "draft",
            "image": _display_path(image_path),
            "request_file": str(request.source_request.relative_to(ROOT)) if request.source_request.is_relative_to(ROOT) else request.source_request.name,
            "request_id": request_id,
            "usage": usage,
            "cost_estimate": None,
        }
        _write_new_file(version_dir / "metadata.json", (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode())
        return metadata

    def status(self, output_destination: Path, asset_id: str, state: str | None = None, version: str | None = None) -> list[dict[str, Any]]:
        if not ASSET_ID_RE.fullmatch(asset_id):
            raise ArtPipelineError("asset_id contiene caracteres no permitidos.")
        asset_dir = output_destination / asset_id
        metadata_files = sorted(
            asset_dir.glob("v*/metadata.json"),
            key=lambda path: int(path.parent.name[1:]) if path.parent.name[1:].isdigit() else -1,
        )
        if version:
            metadata_files = [p for p in metadata_files if p.parent.name == version]
        if not metadata_files:
            raise ArtPipelineError(f"No hay generaciones registradas para {asset_id}.")
        if state:
            if state not in VALID_STATES:
                raise ArtPipelineError("El estado debe ser draft, review, approved o published.")
            target = metadata_files[-1]
            try:
                data = json.loads(target.read_text(encoding="utf-8"))
                data["status"] = state
                data["status_updated_at_utc"] = datetime.now(timezone.utc).isoformat()
                _atomic_replace(target, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())
            except (OSError, json.JSONDecodeError) as exc:
                raise ArtPipelineError("No se pudo actualizar el metadata de estado.") from exc
            metadata_files = [target]
        output = []
        for path in metadata_files:
            try:
                output.append(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError) as exc:
                raise ArtPipelineError(f"Metadata inválido: {path}") from exc
        return output


def build_prompt(request: ArtRequest) -> str:
    sections = [
        "Create a draft visual asset for Vintage Telnet using the supplied art direction.",
        f"Asset type: {request.asset_type}",
        f"Target: {request.target}",
        f"Canonical name: {request.canonical_name}",
        f"Art direction: {request.art_direction}",
        f"Aspect ratio: {request.aspect_ratio}",
        f"Prompt: {request.prompt}",
    ]
    if request.canon_sources:
        sections.append("Canon sources supplied by the Art Director: " + "; ".join(request.canon_sources))
    if request.negative_constraints:
        sections.append("Do not include: " + "; ".join(request.negative_constraints))
    if request.room_id or request.creature_id or request.species_id:
        sections.append(
            "IDs (reference only): "
            + ", ".join(v for v in (request.room_id, request.creature_id, request.species_id) if v)
        )
    if request.variation_of:
        sections.append(f"Variation requested from prior asset/version: {request.variation_of}")
    if request.notes:
        sections.append("Notes: " + request.notes)
    if request.references:
        sections.append("Use the attached reference images according to the art direction and constraints above.")
    return "\n\n".join(sections)


def size_for_aspect(aspect: str) -> str:
    normalized = aspect.strip().lower().replace(" ", "")
    if normalized in {"square", "1:1", "1x1"}:
        return "1024x1024"
    if normalized in {"landscape", "3:2", "16:9", "1536:1024"}:
        return "1536x1024" if normalized != "16:9" else "1536x864"
    if normalized in {"portrait", "2:3", "3:4", "1024:1536"}:
        return "1024x1536"
    match = re.fullmatch(r"(\d{3,4})\s*[:x]\s*(\d{3,4})", normalized)
    if match:
        width, height = map(int, match.groups())
        if width % 16 or height % 16 or not (655360 <= width * height <= 8294400):
            raise ArtPipelineError("aspect_ratio como dimensiones debe cumplir los límites de GPT Image.")
        if max(width, height) > 3840 or max(width, height) / min(width, height) > 3:
            raise ArtPipelineError("aspect_ratio supera los límites de dimensiones de GPT Image.")
        return f"{width}x{height}"
    raise ArtPipelineError("aspect_ratio debe ser square/landscape/portrait o dimensiones válidas como 1536x864.")


def _claim_version(root: Path, asset_id: str) -> tuple[Path, str]:
    asset_dir = root / asset_id
    asset_dir.mkdir(parents=True, exist_ok=True)
    number = 1
    while True:
        version = f"v{number:03d}"
        candidate = asset_dir / version
        try:
            candidate.mkdir()
            return candidate, version
        except FileExistsError:
            number += 1


def _write_new_file(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temp.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temp, path)
    except FileExistsError as exc:
        raise ArtPipelineError(f"Se rehúsa sobrescribir: {path}") from exc
    except OSError as exc:
        raise ArtPipelineError(f"No se pudo escribir el resultado en {path}.") from exc
    finally:
        temp.unlink(missing_ok=True)


def _atomic_replace(path: Path, data: bytes) -> None:
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temp.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def _resolve_image_list(value: Any, base: Path) -> tuple[Path, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ArtPipelineError("references debe ser una lista de rutas locales.")
    return tuple(_resolve_optional_image(item, base) for item in value if item)


def _resolve_optional_image(value: Any, base: Path) -> Path | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ArtPipelineError("Las rutas de referencia deben ser texto.")
    path = Path(value.strip())
    if not path.is_absolute():
        path = (base / path).resolve()
    if not path.is_file():
        raise ArtPipelineError(f"No existe la imagen de referencia: {value}")
    if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ArtPipelineError(f"Formato de referencia no soportado: {path.suffix}")
    return path


def _string_tuple(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
        raise ArtPipelineError(f"{field} debe ser una lista de textos.")
    return tuple(v.strip() for v in value if v.strip())


def _optional_text(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ArtPipelineError(f"{field} debe ser texto.")
    return value.strip() or None


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


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)
