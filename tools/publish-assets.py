#!/usr/bin/env python3
"""Deterministic Vintage Telnet asset batch publisher.

Local publisher:
  python tools/publish-assets.py ./incoming --target assets/vintage-telnet/locations/ --dry-run
  python tools/publish-assets.py ./incoming --target assets/vintage-telnet/locations/

Manifest publisher:
  python tools/publish-assets.py batch.json --dry-run

PR validation:
  python tools/publish-assets.py --validate-pr origin/main

The publisher never pushes, merges, deploys, or touches Raspberry. In publish mode it
copies a fully validated batch into the current non-main Git branch and creates one
local commit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import Iterable

ALLOWLIST = (
    "assets/vintage-telnet/locations/",
    "assets/vintage-telnet/species/",
    "assets/vintage-telnet/maps/",
)
ALLOWED_EXTENSIONS = {".png", ".webp", ".jpg", ".jpeg"}
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_DIMENSION = 8192
SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]{0,118}[a-z0-9]$|^[a-z0-9]$")
FORBIDDEN_FINAL_EXTENSIONS = {".zip", ".b64", ".base64"}


class AssetBatchError(RuntimeError):
    pass


@dataclass(frozen=True)
class Asset:
    source: Path
    destination: str
    width: int
    height: int
    format: str
    bytes: int
    sha256: str


def _run_git(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode:
        raise AssetBatchError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def git_root(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise AssetBatchError("Run inside a Git checkout.")
    return Path(proc.stdout.strip()).resolve()


def normalize_target(target: str) -> str:
    if not isinstance(target, str) or not target.strip():
        raise AssetBatchError("target is required")
    raw = target.replace("\\", "/").strip()
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts:
        raise AssetBatchError(f"unsafe target path: {target}")
    normalized = path.as_posix().rstrip("/") + "/"
    if not any(normalized.startswith(prefix) for prefix in ALLOWLIST):
        raise AssetBatchError(f"target outside allowlist: {normalized}")
    return normalized


def safe_name(name: str) -> str:
    if not isinstance(name, str) or "/" in name or "\\" in name:
        raise AssetBatchError(f"unsafe asset name: {name!r}")
    if name != name.lower() or not SAFE_NAME.fullmatch(name):
        raise AssetBatchError(
            f"unsafe asset name: {name!r}; use lowercase letters, digits, dot, dash, underscore"
        )
    ext = Path(name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise AssetBatchError(f"unsupported asset extension: {ext or '<none>'}")
    return name


def _png_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise AssetBatchError("invalid PNG")
    return struct.unpack(">II", data[16:24])


def _jpeg_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise AssetBatchError("invalid JPEG")
    i = 2
    sof = {
        0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    }
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in {0xD8, 0xD9}:
            continue
        if i + 2 > len(data):
            break
        length = int.from_bytes(data[i:i + 2], "big")
        if length < 2 or i + length > len(data):
            break
        if marker in sof:
            if length < 7:
                break
            height = int.from_bytes(data[i + 3:i + 5], "big")
            width = int.from_bytes(data[i + 5:i + 7], "big")
            return width, height
        i += length
    raise AssetBatchError("invalid JPEG dimensions")


def _webp_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise AssetBatchError("invalid WebP")
    kind = data[12:16]
    if kind == b"VP8X":
        if len(data) < 30:
            raise AssetBatchError("invalid WebP VP8X")
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    if kind == b"VP8 ":
        marker = data.find(b"\x9d\x01\x2a", 20)
        if marker < 0 or marker + 7 > len(data):
            raise AssetBatchError("invalid WebP VP8")
        width = int.from_bytes(data[marker + 3:marker + 5], "little") & 0x3FFF
        height = int.from_bytes(data[marker + 5:marker + 7], "little") & 0x3FFF
        return width, height
    if kind == b"VP8L":
        if len(data) < 25 or data[20] != 0x2F:
            raise AssetBatchError("invalid WebP VP8L")
        bits = int.from_bytes(data[21:25], "little")
        width = (bits & 0x3FFF) + 1
        height = ((bits >> 14) & 0x3FFF) + 1
        return width, height
    raise AssetBatchError(f"unsupported WebP chunk: {kind!r}")


def inspect_image(path: Path) -> tuple[str, int, int, int, str]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise AssetBatchError(f"cannot read {path}: {exc}") from exc
    size = len(data)
    if size == 0:
        raise AssetBatchError(f"empty asset: {path}")
    if size > MAX_FILE_BYTES:
        raise AssetBatchError(f"asset exceeds {MAX_FILE_BYTES} bytes: {path}")
    ext = path.suffix.lower()
    if ext == ".png":
        width, height = _png_dimensions(data)
        fmt = "PNG"
    elif ext in {".jpg", ".jpeg"}:
        width, height = _jpeg_dimensions(data)
        fmt = "JPEG"
    elif ext == ".webp":
        width, height = _webp_dimensions(data)
        fmt = "WEBP"
    else:
        raise AssetBatchError(f"unsupported asset extension: {ext}")
    if width < 1 or height < 1 or width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise AssetBatchError(f"invalid dimensions {width}x{height}: {path}")
    return fmt, width, height, size, hashlib.sha256(data).hexdigest()


def _manifest_entries(manifest: Path) -> tuple[str, bool, list[tuple[Path, str]]]:
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssetBatchError(f"invalid manifest: {exc}") from exc
    if not isinstance(payload, dict):
        raise AssetBatchError("manifest root must be an object")
    target = normalize_target(payload.get("target", ""))
    replace = payload.get("replace", False)
    if not isinstance(replace, bool):
        raise AssetBatchError("manifest replace must be boolean")
    files = payload.get("files")
    if not isinstance(files, list) or not files:
        raise AssetBatchError("manifest files must be a non-empty list")
    entries: list[tuple[Path, str]] = []
    base = manifest.parent
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            raise AssetBatchError(f"manifest files[{index}] must be an object")
        source = item.get("source")
        name = item.get("name")
        if not isinstance(source, str) or not source:
            raise AssetBatchError(f"manifest files[{index}].source is required")
        source_path = Path(source)
        if source_path.is_absolute() or ".." in source_path.parts:
            raise AssetBatchError(f"unsafe manifest source: {source}")
        entries.append(((base / source_path).resolve(), safe_name(name)))
    return target, replace, entries


def _folder_entries(folder: Path, target: str) -> tuple[str, bool, list[tuple[Path, str]]]:
    if not folder.is_dir():
        raise AssetBatchError(f"input folder not found: {folder}")
    entries = []
    for path in sorted(folder.iterdir()):
        if path.is_file():
            if path.suffix.lower() in FORBIDDEN_FINAL_EXTENSIONS:
                raise AssetBatchError(f"forbidden final asset type: {path.name}")
            entries.append((path.resolve(), safe_name(path.name)))
    if not entries:
        raise AssetBatchError("input folder contains no supported assets")
    return normalize_target(target), False, entries


def load_batch(source: Path, target: str | None) -> tuple[str, bool, list[tuple[Path, str]]]:
    if source.is_file() and source.suffix.lower() == ".json":
        if target:
            raise AssetBatchError("--target is not used with a manifest")
        return _manifest_entries(source)
    if target is None:
        raise AssetBatchError("--target is required when input is a folder")
    return _folder_entries(source, target)


def validate_batch(
    repo: Path,
    target: str,
    entries: Iterable[tuple[Path, str]],
    *,
    replace: bool,
) -> list[Asset]:
    names: set[str] = set()
    destinations: set[str] = set()
    assets: list[Asset] = []
    for source, name in entries:
        key = name.casefold()
        if key in names:
            raise AssetBatchError(f"duplicate asset name in batch: {name}")
        names.add(key)
        destination = (PurePosixPath(target) / name).as_posix()
        if destination.casefold() in destinations:
            raise AssetBatchError(f"duplicate destination in batch: {destination}")
        destinations.add(destination.casefold())
        dest_path = repo / destination
        if dest_path.exists() and not replace:
            raise AssetBatchError(f"destination exists; replacement not authorized: {destination}")
        fmt, width, height, size, sha256 = inspect_image(source)
        if source.suffix.lower() != Path(name).suffix.lower():
            raise AssetBatchError(f"source/name extension mismatch: {source.name} -> {name}")
        assets.append(Asset(source, destination, width, height, fmt, size, sha256))
    return assets


def batch_digest(assets: Iterable[Asset]) -> str:
    digest = hashlib.sha256()
    for asset in sorted(assets, key=lambda item: item.destination):
        digest.update(asset.destination.encode("utf-8"))
        digest.update(b"\0")
        digest.update(asset.sha256.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def print_summary(assets: list[Asset], target: str, *, dry_run: bool, commit: str | None) -> None:
    print("ASSET BATCH: OK")
    print(f"mode: {'dry-run' if dry_run else 'published'}")
    print(f"files: {len(assets)}")
    print(f"target: {target}")
    print(f"bytes: {sum(a.bytes for a in assets)}")
    print(f"batch_sha256: {batch_digest(assets)}")
    print(f"commit: {commit or 'none'}")
    for asset in assets:
        print(
            f"{asset.destination} — {asset.width}x{asset.height} — "
            f"{asset.format} — {asset.bytes} bytes — sha256:{asset.sha256}"
        )


def publish(repo: Path, assets: list[Asset], message: str, *, replace: bool) -> str:
    branch = _run_git(repo, "branch", "--show-current")
    if not branch or branch in {"main", "master"}:
        raise AssetBatchError("publishing directly to main/master is forbidden")
    tracked_dirty = _run_git(repo, "status", "--porcelain", "--untracked-files=no")
    if tracked_dirty:
        raise AssetBatchError("tracked working tree must be clean before publishing")

    backups: dict[Path, bytes | None] = {}
    tempdir = Path(tempfile.mkdtemp(prefix="asset-batch-", dir=repo))
    written: list[Path] = []
    try:
        staged: list[tuple[Path, Path]] = []
        for index, asset in enumerate(assets):
            tmp = tempdir / str(index)
            tmp.write_bytes(asset.source.read_bytes())
            dest = repo / asset.destination
            backups[dest] = dest.read_bytes() if dest.exists() else None
            staged.append((tmp, dest))

        for tmp, dest in staged:
            dest.parent.mkdir(parents=True, exist_ok=True)
            os.replace(tmp, dest)
            written.append(dest)

        rel_paths = [asset.destination for asset in assets]
        _run_git(repo, "add", "--", *rel_paths)
        _run_git(repo, "commit", "-m", message)
        return _run_git(repo, "rev-parse", "HEAD")
    except Exception:
        _run_git(repo, "reset", "--", *[asset.destination for asset in assets], check=False)
        for dest in written:
            previous = backups.get(dest)
            if previous is None:
                try:
                    dest.unlink()
                except FileNotFoundError:
                    pass
            else:
                dest.write_bytes(previous)
        raise
    finally:
        shutil.rmtree(tempdir, ignore_errors=True)


def _changed_paths(repo: Path, base_ref: str) -> list[tuple[str, str]]:
    raw = _run_git(repo, "diff", "--name-status", f"{base_ref}...HEAD")
    rows = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1].replace("\\", "/")
        rows.append((status, path))
    return rows


def validate_pr(repo: Path, base_ref: str) -> int:
    changes = _changed_paths(repo, base_ref)
    asset_changes = [(s, p) for s, p in changes if p.startswith("assets/")]
    if not asset_changes:
        print("ASSET PR VALIDATION: OK (no asset changes)")
        return 0

    violations: list[str] = []
    for status, path in asset_changes:
        if not any(path.startswith(prefix) for prefix in ALLOWLIST):
            violations.append(f"asset path outside allowlist: {path}")
            continue
        ext = Path(path).suffix.lower()
        if ext in FORBIDDEN_FINAL_EXTENSIONS:
            violations.append(f"forbidden final asset type: {path}")
            continue
        if status != "A":
            violations.append(
                f"v1 asset PRs may only add new files; replacement/deletion needs explicit future flow: {status} {path}"
            )
            continue
        try:
            safe_name(Path(path).name)
            inspect_image(repo / path)
        except AssetBatchError as exc:
            violations.append(f"{path}: {exc}")

    non_asset_changes = [
        p for _s, p in changes
        if not p.startswith("assets/")
        and p not in {"tools/publish-assets.py", ".github/workflows/asset-validation.yml"}
        and not p.startswith("tests/asset_publisher/")
        and p != "docs/ASSET_BATCH_PUBLISHER.md"
    ]
    if asset_changes and non_asset_changes:
        violations.append(
            "asset delivery PR also changes files outside the approved asset-publisher surface: "
            + ", ".join(non_asset_changes)
        )

    if violations:
        print("ASSET PR VALIDATION: FAILED", file=sys.stderr)
        for violation in violations:
            print(f"- {violation}", file=sys.stderr)
        return 2

    print(f"ASSET PR VALIDATION: OK ({len(asset_changes)} asset files)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate and publish Vintage Telnet asset batches.")
    parser.add_argument("source", nargs="?", type=Path, help="Folder or JSON manifest.")
    parser.add_argument("--target", help="Destination folder for directory input.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and summarize without modifying the repo.")
    parser.add_argument("--replace", action="store_true", help="Explicitly authorize local replacement.")
    parser.add_argument("--commit-message", default="Publish Vintage Telnet asset batch")
    parser.add_argument("--validate-pr", metavar="BASE_REF", help="Validate asset changes against a PR base ref.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        repo = git_root()
        if args.validate_pr:
            if args.source or args.target or args.dry_run or args.replace:
                raise AssetBatchError("--validate-pr cannot be combined with publishing arguments")
            return validate_pr(repo, args.validate_pr)

        if args.source is None:
            raise AssetBatchError("source folder or manifest is required")
        source = args.source.resolve()
        target, manifest_replace, entries = load_batch(source, args.target)
        replace = args.replace or manifest_replace
        assets = validate_batch(repo, target, entries, replace=replace)
        if args.dry_run:
            print_summary(assets, target, dry_run=True, commit=None)
            return 0
        commit = publish(repo, assets, args.commit_message, replace=replace)
        print_summary(assets, target, dry_run=False, commit=commit)
        return 0
    except AssetBatchError as exc:
        print(f"ASSET BATCH: FAILED\n{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
