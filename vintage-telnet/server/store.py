"""SQLite storage. Every operation owns its connection; writes are transactional."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import secrets
import sqlite3
import time
import uuid

STATUSES = ("pending", "approved", "rejected", "removed")

PLAYER_COLUMNS = (
    "id, player_number, username, name, status, species, room, created_at, last_access_at"
)


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


@contextmanager
def connect(path):
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        with db:
            yield db
    finally:
        db.close()


def initialize(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.execute("PRAGMA journal_mode = WAL")
        db.execute("BEGIN IMMEDIATE")
        version = db.execute("PRAGMA user_version").fetchone()[0]
        if version not in (0, 1, 2):
            raise RuntimeError("Versión de base de datos no soportada; no iniciar ni degradar.")
        if version == 2:
            return
        if version == 0:
            statements = [
                """CREATE TABLE players (
                    player_number INTEGER PRIMARY KEY AUTOINCREMENT,
                    id TEXT NOT NULL UNIQUE,
                    username TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending'
                        CHECK(status IN ('pending', 'approved', 'rejected', 'removed')),
                    species TEXT,
                    room TEXT,
                    created_at TEXT NOT NULL,
                    last_access_at TEXT NOT NULL)""",
                """CREATE TABLE access_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id TEXT NOT NULL REFERENCES players(id),
                    kind TEXT NOT NULL CHECK(kind IN ('register', 'login')),
                    occurred_at TEXT NOT NULL)""",
                "CREATE INDEX access_player_time ON access_events(player_id, occurred_at)",
                """CREATE TABLE sessions (
                    token_hash TEXT PRIMARY KEY,
                    player_id TEXT NOT NULL REFERENCES players(id),
                    expires_at INTEGER NOT NULL)""",
                """CREATE TABLE auth_limits (
                    key TEXT PRIMARY KEY, window_start INTEGER NOT NULL,
                    attempts INTEGER NOT NULL)""",
                """CREATE TABLE room_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room TEXT NOT NULL,
                    player_id TEXT NOT NULL REFERENCES players(id),
                    body TEXT NOT NULL,
                    created_at TEXT NOT NULL)""",
                "CREATE INDEX room_messages_room_time ON room_messages(room, created_at)",
            ]
            for statement in statements:
                db.execute(statement)
        else:  # version == 1: upgrade an existing deployment in place
            db.execute("""ALTER TABLE players ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'
                          CHECK(status IN ('pending', 'approved', 'rejected', 'removed'))""")
            db.execute("ALTER TABLE players ADD COLUMN species TEXT")
            db.execute("ALTER TABLE players ADD COLUMN room TEXT")
            db.execute("""CREATE TABLE room_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room TEXT NOT NULL,
                    player_id TEXT NOT NULL REFERENCES players(id),
                    body TEXT NOT NULL,
                    created_at TEXT NOT NULL)""")
            db.execute("CREATE INDEX room_messages_room_time ON room_messages(room, created_at)")
        db.execute("PRAGMA user_version = 2")


def allow_attempt(path, address):
    """Shared durable fixed window: 20 auth submissions per source IP per minute."""
    now = int(time.time())
    key = digest(address)
    with connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        db.execute("DELETE FROM auth_limits WHERE window_start <= ?", (now - 60,))
        db.execute("INSERT OR IGNORE INTO auth_limits VALUES (?, ?, 0)", (key, now))
        count = db.execute("SELECT attempts FROM auth_limits WHERE key = ?", (key,)).fetchone()[0]
        if count >= 20:
            return False
        db.execute("UPDATE auth_limits SET attempts = attempts + 1 WHERE key = ?", (key,))
    return True


def record_access(db, player_id, kind, old_token=None):
    now = utcnow()
    token = secrets.token_urlsafe(32)
    db.execute("DELETE FROM sessions WHERE expires_at <= ?", (int(time.time()),))
    if old_token:
        db.execute("DELETE FROM sessions WHERE token_hash = ?", (digest(old_token),))
    db.execute("INSERT INTO sessions VALUES (?, ?, ?)",
               (digest(token), player_id, int(time.time()) + 12 * 3600))
    db.execute("UPDATE players SET last_access_at = ? WHERE id = ?", (now, player_id))
    db.execute("INSERT INTO access_events(player_id, kind, occurred_at) VALUES (?, ?, ?)",
               (player_id, kind, now))
    return token


def register(path, username, name, password_hash, old_token=None):
    with connect(path) as db:
        player_id = str(uuid.uuid4())
        now = utcnow()
        db.execute("""INSERT INTO players(id, username, name, password_hash, created_at, last_access_at)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   (player_id, username, name, password_hash, now, now))
        return record_access(db, player_id, "register", old_token)


def player_for_token(path, token):
    if not token:
        return None
    with connect(path) as db:
        return db.execute(
            """SELECT p.id, p.player_number, p.username, p.name, p.status, p.species, p.room,
                      p.created_at, p.last_access_at
               FROM players p
               JOIN sessions s ON s.player_id = p.id
               WHERE s.token_hash = ? AND s.expires_at > ?""",
            (digest(token), int(time.time())),
        ).fetchone()


def player_by_username(db, username):
    return db.execute(f"SELECT {PLAYER_COLUMNS} FROM players WHERE username = ?", (username,)).fetchone()


def list_by_status(path, status):
    with connect(path) as db:
        return db.execute(
            f"SELECT {PLAYER_COLUMNS} FROM players WHERE status = ? ORDER BY player_number", (status,)
        ).fetchall()


def set_status(path, username, status, revoke_sessions=False):
    """Returns the updated player row, or None if the username doesn't exist."""
    if status not in STATUSES:
        raise ValueError(f"Estado desconocido: {status}")
    with connect(path) as db:
        player = player_by_username(db, username)
        if player is None:
            return None
        db.execute("UPDATE players SET status = ? WHERE id = ?", (status, player["id"]))
        if revoke_sessions:
            db.execute("DELETE FROM sessions WHERE player_id = ?", (player["id"],))
        return player_by_username(db, username)


def set_species(path, player_id, species, room):
    """Solo toma efecto la primera vez (species debe ser NULL todavia).

    Atomico de verdad: usa rowcount para saber si ESTA llamada fue la que
    escribio, en vez de asumirlo por el estado leido antes del UPDATE. Dos
    POST concurrentes solo pueden hacer que una de las dos devuelva True."""
    with connect(path) as db:
        cursor = db.execute(
            "UPDATE players SET species = ?, room = ? WHERE id = ? AND species IS NULL",
            (species, room, player_id),
        )
        return cursor.rowcount > 0


def move_player(path, player_id, room):
    with connect(path) as db:
        db.execute("UPDATE players SET room = ? WHERE id = ?", (room, player_id))


def players_in_room(path, room, exclude_id=None):
    with connect(path) as db:
        rows = db.execute(
            "SELECT name, username FROM players WHERE room = ? AND status = 'approved' AND id != ?",
            (room, exclude_id or ""),
        ).fetchall()
        return [dict(row) for row in rows]


def add_message(path, room, player_id, body):
    with connect(path) as db:
        db.execute(
            "INSERT INTO room_messages(room, player_id, body, created_at) VALUES (?, ?, ?, ?)",
            (room, player_id, body, utcnow()),
        )


def recent_messages(path, room, limit=30):
    # Solo identidad publica (name): el username es la credencial de login de
    # otro jugador y no debe salir en el chat.
    with connect(path) as db:
        rows = db.execute(
            """SELECT m.body, m.created_at, p.name FROM room_messages m
               JOIN players p ON p.id = m.player_id
               WHERE m.room = ? ORDER BY m.id DESC LIMIT ?""",
            (room, limit),
        ).fetchall()
        return [dict(row) for row in reversed(rows)]
