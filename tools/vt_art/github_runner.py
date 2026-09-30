"""Generate the one approved art pilot and keep its outputs in the repo workspace."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import sys

from .critique import OpenAIVisionCritic
from .pipeline import ArtPipeline, ArtRequest, OpenAIImageClient, ROOT


REQUEST_ROOT = ROOT / "vintage-telnet" / "art_requests"
DEFAULT_CRITIC_MODEL = "gpt-5-mini"


def resolve_request_path(relative_request: str) -> Path:
    request_path = (ROOT / relative_request).resolve()
    if request_path.parent != REQUEST_ROOT.resolve() or request_path.suffix.lower() != ".json" or request_path.name == "template.json":
        raise ValueError("Elige una ficha JSON directa dentro de vintage-telnet/art_requests/.")
    if not request_path.is_file():
        raise FileNotFoundError("No existe la ficha solicitada en la rama main.")
    return request_path


def copy_request_to_version(request_path: Path, version_dir: Path) -> Path:
    """Keep the exact approved brief beside its generated draft."""
    destination = version_dir / "request.json"
    if destination.exists():
        raise FileExistsError("La ficha de esta versión ya existe.")
    shutil.copyfile(request_path, destination)
    return destination


def run_v2() -> int:
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        raise RuntimeError("Falta el secreto OPENAI_API_KEY.")
    relative_request = os.environ.get("VT_ART_REQUEST_FILE", "").strip()
    request_path = resolve_request_path(relative_request)
    request = ArtRequest.load(request_path)
    model = os.environ.get("VT_ART_MODEL", "gpt-image-2.5-flare")
    version_hint = None
    if os.environ.get("GITHUB_RUN_NUMBER"):
        try:
            version_hint = f"v{int(os.environ['GITHUB_RUN_NUMBER']):03d}"
        except ValueError as exc:
            raise RuntimeError("GITHUB_RUN_NUMBER no es numérico.") from exc
    api_key = os.environ["OPENAI_API_KEY"]
    pipeline = ArtPipeline(OpenAIImageClient(api_key), model)
    # La autocrítica es el camino por defecto. Reintenta hasta 3 veces si falla,
    # así que reclama sus propias versiones por auto-incremento (v001, v002...);
    # version_hint (de GITHUB_RUN_NUMBER) solo se usa si se apaga la crítica
    # explícitamente con VT_ART_CRITIC_MODEL="".
    critic_model = os.environ.get("VT_ART_CRITIC_MODEL", DEFAULT_CRITIC_MODEL).strip()
    if critic_model:
        result = pipeline.generate_with_critique(request, OpenAIVisionCritic(api_key), critic_model, max_attempts=4)
    else:
        result = pipeline.generate(request, version_hint)
        result["critique"] = None
    image_path = ROOT / result["image"]
    version_dir = image_path.parent
    copy_request_to_version(request_path, version_dir)
    output_file = os.environ.get("GITHUB_OUTPUT")
    critique = result.get("critique")
    verdict = "sin autocrítica" if critique is None else ("aprobado" if critique["passes"] else "NECESITA REVISIÓN")

    # Si la autocrítica aprobó, generar formatos adicionales:
    # - WebP para assets/ (quality:low, compression:85)
    # - PNG high para archivo maestro (quality:high)
    print(f"DEBUG: critique exists = {critique is not None}, passes = {critique.get('passes') if critique else 'N/A'}")
    if critique and critique.get("passes"):
        print("DEBUG: Entrando a bloque de generación de formatos adicionales")
        try:
            print("DEBUG: Intentando generar WebP...")
            # WebP para assets/
            webp_result = pipeline.generate_with_params(
                request,
                quality="low",
                output_format="webp",
                output_compression=85,
            )
            webp_path = ROOT / webp_result["image"]
            print(f"✅ Generado WebP: {webp_path.relative_to(ROOT)}")

            print("DEBUG: Intentando generar PNG high-quality...")
            # PNG high para archive (driver later)
            hq_result = pipeline.generate_with_params(
                request,
                quality="high",
                output_format="png",
                output_compression=None,
            )
            hq_path = ROOT / hq_result["image"]
            print(f"✅ Generado PNG high-quality: {hq_path.relative_to(ROOT)}")
        except Exception as exc:
            print(f"❌ ERROR generando formatos adicionales: {type(exc).__name__}: {exc}")
            import traceback
            traceback.print_exc()
    else:
        print("DEBUG: No entrando a bloque (critique no aprobó o no existe)")

    if output_file:
        with Path(output_file).open("a", encoding="utf-8") as stream:
            stream.write(
                f"asset_id={request.asset_id}\nversion={result['version']}\nverdict={verdict}\n"
            )
    print(f"Generación terminada: {request.asset_id} {result['version']} (draft, autocrítica: {verdict}).")
    print(f"Imagen y metadata: {version_dir.relative_to(ROOT)}")
    print("El workflow propondrá una PR de borrador; no aprobará ni integrará el arte al juego.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(run_v2())
    except Exception as exc:
        # Never echo exception payloads: provider errors can carry request content.
        print(f"Fallo del piloto: {type(exc).__name__}.", file=sys.stderr)
        raise SystemExit(1)
