#!/usr/bin/env python3
"""Safe migration probe for the live Vintage Telnet SQLite database.

The source database is opened read-only and copied with SQLite backup().
Only the temporary copy is passed to server.store.initialize().
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server import store  # noqa: E402


def snapshot_players(db: sqlite3.Connection) -> list[tuple[str, int, str]]:
    rows = db.execute(
        "SELECT id, player_number, username FROM players ORDER BY player_number"
    ).fetchall()
    return [(str(row[0]), int(row[1]), str(row[2])) for row in rows]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("db", help="Ruta a la SQLite viva; se abre read-only.")
    args = parser.parse_args()

    source_path = Path(args.db).resolve()
    if not source_path.is_file():
        print(f"FAIL: no existe {source_path}")
        return 2

    source_uri = f"file:{source_path}?mode=ro"
    with sqlite3.connect(source_uri, uri=True, timeout=10) as src:
        before_version = src.execute("PRAGMA user_version").fetchone()[0]
        before_players = snapshot_players(src)
        integrity = src.execute("PRAGMA quick_check").fetchone()[0]
        if integrity != "ok":
            print(f"FAIL: quick_check de origen: {integrity}")
            return 3

        with tempfile.TemporaryDirectory(prefix="vt-migration-probe-") as tmp:
            copy_path = Path(tmp) / "probe.sqlite3"
            with sqlite3.connect(copy_path) as dst:
                src.backup(dst)

            # Migration happens ONLY on the temporary backup.
            store.initialize(copy_path)

            with sqlite3.connect(copy_path) as migrated:
                after_version = migrated.execute("PRAGMA user_version").fetchone()[0]
                after_players = snapshot_players(migrated)
                tables = {
                    row[0]
                    for row in migrated.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    ).fetchall()
                }
                columns = {
                    row[1]
                    for row in migrated.execute("PRAGMA table_info(players)").fetchall()
                }
                fk_errors = migrated.execute("PRAGMA foreign_key_check").fetchall()
                quick = migrated.execute("PRAGMA quick_check").fetchone()[0]

    checks = {
        "source_version_supported": before_version in (0, 1, 2, 3, 4, 5, 6),
        "migrated_to_v6": after_version == 6,
        "players_preserved": before_players == after_players,
        "inventory_table": "inventory_items" in tables,
        "equipped_weapon_column": "equipped_weapon_id" in columns,
        "equipped_armor_column": "equipped_armor_id" in columns,
        "foreign_keys": not fk_errors,
        "quick_check": quick == "ok",
    }

    print(f"Source: {source_path}")
    print(f"Version: {before_version} -> {after_version}")
    print(f"Players preserved: {len(before_players)}")
    for name, ok in checks.items():
        print(f"[{'OK' if ok else 'FAIL'}] {name}")

    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
