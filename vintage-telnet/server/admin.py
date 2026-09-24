"""Local operator commands; never exposes hashes or sessions."""
import argparse
import json
from pathlib import Path
import sqlite3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("players")
    sub.add_parser("accesses")
    sub.add_parser("check")
    backup = sub.add_parser("backup")
    backup.add_argument("destination", type=Path)
    grant_item = sub.add_parser(
        "grant-item",
        help="Entrega autoritativa de un objeto del catálogo a un jugador (GAMEPLAY.md 32.5).")
    grant_item.add_argument("username")
    grant_item.add_argument("item_key")
    grant_item.add_argument("--forge-validated", action="store_true",
                             help="Marca la validación de Forja como completa (GAMEPLAY.md 32.4).")
    args = parser.parse_args()
    source = args.data_dir / "vintage.sqlite3"

    if args.command == "grant-item":
        # Import diferido: solo esta rama necesita escritura real, el resto
        # de comandos de este archivo son deliberadamente de solo lectura.
        from . import items, store
        if items.get_item(args.item_key) is None:
            raise SystemExit(f"Objeto desconocido en el catálogo: {args.item_key}")
        with store.connect(str(source)) as db_write:
            player = store.player_by_username(db_write, args.username)
            if player is None:
                raise SystemExit(f"Jugador desconocido: {args.username}")
            player_id = player["id"]
        item_id = store.grant_item(str(source), player_id, args.item_key,
                                    forge_validated=args.forge_validated)
        print(json.dumps({"granted": args.item_key, "item_id": item_id, "player": args.username}))
        return

    # Read-only URI prevents accidental creation of an empty database on a typo.
    db = sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    try:
        if args.command == "backup":
            # Never overwrite another backup or the live database.
            with args.destination.open("xb"):
                pass
            target = sqlite3.connect(args.destination)
            try:
                db.backup(target)
                result = target.execute("PRAGMA integrity_check").fetchone()[0]
                if result != "ok":
                    raise RuntimeError("La copia no pasó integrity_check")
            finally:
                target.close()
            print("Backup verificado:", args.destination)
        elif args.command == "check":
            result = [row[0] for row in db.execute("PRAGMA integrity_check")]
            foreign = list(db.execute("PRAGMA foreign_key_check"))
            print(json.dumps({"integrity": result, "foreign_key_errors": len(foreign),
                              "schema_version": db.execute("PRAGMA user_version").fetchone()[0]}))
            if result != ["ok"] or foreign:
                raise SystemExit(1)
        else:
            query = ("SELECT id, player_number, username, name, status, species, room, "
                     "created_at, last_access_at FROM players ORDER BY player_number"
                     if args.command == "players" else
                     "SELECT a.id, p.player_number, a.kind, a.occurred_at FROM access_events a "
                     "JOIN players p ON p.id = a.player_id ORDER BY a.id DESC LIMIT 100")
            print(json.dumps([dict(row) for row in db.execute(query)], ensure_ascii=False, indent=2))
    finally:
        db.close()


if __name__ == "__main__":
    main()
