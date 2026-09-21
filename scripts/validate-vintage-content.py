#!/usr/bin/env python3
"""Deterministic validator for public Vintage Telnet content.

No Flask/server import is required. The validator is stdlib-only so it can run
without starting the game server.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 1
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
PRIVATE_MARKERS = (
    "private-content/",
    "private-content\\",
    "/var/lib/vintage-telnet/private-content",
)


class ValidationErrorCollector:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def add(self, path: Path | str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def require_nonempty_string(
        self, obj: dict[str, Any], key: str, path: str
    ) -> str | None:
        value = obj.get(key)
        if not isinstance(value, str) or not value.strip():
            self.add(path, f"required field '{key}' must be a non-empty string")
            return None
        return value.strip()


def parse_json(path: Path, errors: ValidationErrorCollector) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.add(path, "file does not exist")
    except UnicodeDecodeError as exc:
        errors.add(path, f"not valid UTF-8: {exc}")
    except json.JSONDecodeError as exc:
        errors.add(
            path,
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
        )
    except OSError as exc:
        errors.add(path, f"cannot read file: {exc}")
    return None


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def contains_private_reference(value: Any) -> bool:
    for text in iter_strings(value):
        lowered = text.lower()
        if any(marker in lowered for marker in PRIVATE_MARKERS):
            return True
    return False


def safe_manifest_path(raw: Any) -> bool:
    if not isinstance(raw, str) or not raw.strip():
        return False
    path = Path(raw)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and path.suffix.lower() == ".json"
    )


def normalize_list_container(
    data: Any,
    key: str,
    path: str,
    errors: ValidationErrorCollector,
) -> list[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get(key), list):
        return data[key]
    errors.add(
        path,
        f"expected a JSON array or object containing array field '{key}'",
    )
    return []


def validate_content(content_dir: Path) -> list[str]:
    errors = ValidationErrorCollector()
    content_dir = content_dir.resolve()
    manifest_path = content_dir / "manifest.json"

    if not content_dir.is_dir():
        errors.add(content_dir, "content directory does not exist")
        return errors.errors

    manifest = parse_json(manifest_path, errors)
    if not isinstance(manifest, dict):
        if manifest is not None:
            errors.add(manifest_path, "manifest must be a JSON object")
        return errors.errors

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.add(
            manifest_path,
            f"schema_version must be {SCHEMA_VERSION}",
        )

    version = manifest.get("content_version")
    if (
        not isinstance(version, str)
        or not VERSION_RE.fullmatch(version.strip())
    ):
        errors.add(
            manifest_path,
            "content_version must be a non-empty MAJOR.MINOR.PATCH string",
        )

    raw_files = manifest.get("files")
    if not isinstance(raw_files, list):
        errors.add(
            manifest_path,
            "files must be an array of relative JSON paths",
        )
        raw_files = []

    manifest_files: list[str] = []
    seen_manifest_paths: set[str] = set()
    for idx, raw in enumerate(raw_files):
        label = f"manifest.files[{idx}]"
        if not safe_manifest_path(raw):
            errors.add(
                manifest_path,
                f"{label} must be a safe relative .json path",
            )
            continue

        normalized = Path(raw).as_posix()
        if normalized == "manifest.json" or normalized.startswith("schema/"):
            errors.add(
                manifest_path,
                f"{label} must reference public content, not manifest/schema metadata",
            )
            continue

        if normalized in seen_manifest_paths:
            errors.add(
                manifest_path,
                f"duplicate file entry '{normalized}'",
            )
            continue

        seen_manifest_paths.add(normalized)
        manifest_files.append(normalized)

    actual_files = sorted(
        path.relative_to(content_dir).as_posix()
        for path in content_dir.rglob("*.json")
        if path != manifest_path
        and "schema" not in path.relative_to(content_dir).parts[:1]
    )
    expected_files = sorted(manifest_files)

    if actual_files != expected_files:
        missing = sorted(set(expected_files) - set(actual_files))
        unlisted = sorted(set(actual_files) - set(expected_files))

        if missing:
            errors.add(
                manifest_path,
                f"listed files do not exist: {', '.join(missing)}",
            )
        if unlisted:
            errors.add(
                manifest_path,
                f"JSON files are not listed in manifest: {', '.join(unlisted)}",
            )

    documents: dict[str, Any] = {}
    for rel in manifest_files:
        path = content_dir / rel
        data = parse_json(path, errors)
        if data is not None:
            documents[rel] = data
            if contains_private_reference(data):
                errors.add(
                    rel,
                    "public content must not reference private-content paths",
                )

    ids: dict[str, str] = {}
    rooms: dict[str, dict[str, Any]] = {}
    room_settlements: dict[str, str] = {}
    settlements: dict[str, dict[str, Any]] = {}
    species: dict[str, dict[str, Any]] = {}
    narrative: dict[str, dict[str, Any]] = {}

    def register_id(entity_id: str | None, entity_path: str) -> None:
        if not entity_id:
            return
        if entity_id in ids:
            errors.add(
                entity_path,
                f"duplicate id '{entity_id}' (already used at {ids[entity_id]})",
            )
        else:
            ids[entity_id] = entity_path

    for rel, data in documents.items():
        path = rel

        if rel == "species.json":
            items = normalize_list_container(
                data,
                "species",
                path,
                errors,
            )
            for idx, item in enumerate(items):
                entity_path = f"{path}:species[{idx}]"
                if not isinstance(item, dict):
                    errors.add(
                        entity_path,
                        "species entry must be an object",
                    )
                    continue

                entity_id = errors.require_nonempty_string(
                    item, "id", entity_path
                )
                errors.require_nonempty_string(item, "name", entity_path)
                errors.require_nonempty_string(
                    item, "starting_settlement", entity_path
                )
                errors.require_nonempty_string(
                    item, "starting_room", entity_path
                )
                register_id(entity_id, entity_path)

                if entity_id:
                    species[entity_id] = item

        elif rel.startswith("settlements/"):
            if not isinstance(data, dict):
                errors.add(path, "settlement file must be an object")
                continue

            settlement_id = errors.require_nonempty_string(
                data, "id", path
            )
            errors.require_nonempty_string(data, "name", path)
            errors.require_nonempty_string(data, "starting_room", path)

            room_items = data.get("rooms")
            if not isinstance(room_items, list) or not room_items:
                errors.add(
                    path,
                    "required field 'rooms' must be a non-empty array",
                )
                room_items = []

            register_id(settlement_id, path)
            if settlement_id:
                settlements[settlement_id] = data

            for idx, room in enumerate(room_items):
                room_path = f"{path}:rooms[{idx}]"
                if not isinstance(room, dict):
                    errors.add(
                        room_path,
                        "room entry must be an object",
                    )
                    continue

                room_id = errors.require_nonempty_string(
                    room, "id", room_path
                )
                room_settlement = errors.require_nonempty_string(
                    room, "settlement", room_path
                )
                errors.require_nonempty_string(
                    room, "name", room_path
                )
                errors.require_nonempty_string(
                    room, "description_id", room_path
                )

                exits = room.get("exits")
                if not isinstance(exits, dict):
                    errors.add(
                        room_path,
                        "required field 'exits' must be an object",
                    )
                else:
                    for direction, target in exits.items():
                        if (
                            not isinstance(direction, str)
                            or not direction.strip()
                        ):
                            errors.add(
                                room_path,
                                "exit direction must be a non-empty string",
                            )
                        if (
                            not isinstance(target, str)
                            or not target.strip()
                        ):
                            errors.add(
                                room_path,
                                f"exit '{direction}' target must be a non-empty room id",
                            )

                tags = room.get("tags", [])
                if not isinstance(tags, list):
                    errors.add(
                        room_path,
                        "field 'tags' must be an array when present",
                    )

                if (
                    settlement_id
                    and room_settlement
                    and room_settlement != settlement_id
                ):
                    errors.add(
                        room_path,
                        f"room settlement '{room_settlement}' does not match file settlement '{settlement_id}'",
                    )

                register_id(room_id, room_path)

                if room_id:
                    rooms[room_id] = room
                    if room_settlement:
                        room_settlements[room_id] = room_settlement

        elif rel.startswith("narrative/"):
            items = normalize_list_container(
                data,
                "narrative",
                path,
                errors,
            )
            for idx, item in enumerate(items):
                narrative_path = f"{path}:narrative[{idx}]"
                if not isinstance(item, dict):
                    errors.add(
                        narrative_path,
                        "narrative entry must be an object",
                    )
                    continue

                narrative_id = errors.require_nonempty_string(
                    item, "id", narrative_path
                )
                errors.require_nonempty_string(
                    item, "room", narrative_path
                )
                errors.require_nonempty_string(
                    item, "trigger", narrative_path
                )
                errors.require_nonempty_string(
                    item, "text", narrative_path
                )

                if (
                    "once_per_player" in item
                    and not isinstance(item["once_per_player"], bool)
                ):
                    errors.add(
                        narrative_path,
                        "field 'once_per_player' must be boolean when present",
                    )

                for list_field in ("requires", "sets"):
                    if (
                        list_field in item
                        and not isinstance(item[list_field], list)
                    ):
                        errors.add(
                            narrative_path,
                            f"field '{list_field}' must be an array when present",
                        )

                register_id(narrative_id, narrative_path)

                if narrative_id:
                    narrative[narrative_id] = item

        else:
            errors.add(
                path,
                "unsupported content path; expected species.json, settlements/*.json or narrative/*.json",
            )

    for settlement_id, settlement in settlements.items():
        starting_room = settlement.get("starting_room")
        if isinstance(starting_room, str) and starting_room.strip():
            if starting_room not in rooms:
                errors.add(
                    f"settlement:{settlement_id}",
                    f"starting_room '{starting_room}' does not exist",
                )
            elif room_settlements.get(starting_room) != settlement_id:
                errors.add(
                    f"settlement:{settlement_id}",
                    f"starting_room '{starting_room}' does not belong to settlement '{settlement_id}'",
                )

    for room_id, room in rooms.items():
        exits = room.get("exits")
        if isinstance(exits, dict):
            for direction, target in exits.items():
                if (
                    isinstance(target, str)
                    and target.strip()
                    and target not in rooms
                ):
                    errors.add(
                        f"room:{room_id}",
                        f"exit '{direction}' points to missing room '{target}'",
                    )

    for narrative_id, item in narrative.items():
        room_id = item.get("room")
        if (
            isinstance(room_id, str)
            and room_id.strip()
            and room_id not in rooms
        ):
            errors.add(
                f"narrative:{narrative_id}",
                f"room '{room_id}' does not exist",
            )

    for species_id, item in species.items():
        settlement_id = item.get("starting_settlement")
        room_id = item.get("starting_room")

        if (
            isinstance(settlement_id, str)
            and settlement_id.strip()
            and settlement_id not in settlements
        ):
            errors.add(
                f"species:{species_id}",
                f"starting_settlement '{settlement_id}' does not exist",
            )

        if isinstance(room_id, str) and room_id.strip():
            if room_id not in rooms:
                errors.add(
                    f"species:{species_id}",
                    f"starting_room '{room_id}' does not exist",
                )
            elif (
                isinstance(settlement_id, str)
                and settlement_id.strip()
                and room_settlements.get(room_id) != settlement_id
            ):
                errors.add(
                    f"species:{species_id}",
                    f"starting_room '{room_id}' does not belong to starting_settlement '{settlement_id}'",
                )

    return errors.errors


def default_content_dir() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "vintage-telnet"
        / "content"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate public Vintage Telnet content "
            "without starting the server."
        )
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=default_content_dir(),
        help="content directory to validate",
    )
    args = parser.parse_args(argv)

    errors = validate_content(args.content_dir)
    if errors:
        print(
            f"Vintage Telnet content validation FAILED "
            f"({len(errors)} error(s)):",
            file=sys.stderr,
        )
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Vintage Telnet content validation OK: "
        f"{args.content_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
