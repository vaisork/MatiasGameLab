"""SQLite storage. Every operation owns its connection; writes are transactional."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import secrets
import sqlite3
import time
import uuid


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
        if version not in (0, 1):
            raise RuntimeError("Versión de base de datos no soportada; no iniciar ni degradar.")
        if version == 1:
            return
        statements = [
            """CREATE TABLE players (
                player_number INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
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
        ]
        for statement in statements:
            db.execute(statement)
        db.execute("PRAGMA user_version = 1")


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
        return db.execute("""SELECT p.id, p.player_number, p.username, p.name,
                             p.created_at, p.last_access_at FROM players p
                             JOIN sessions s ON s.player_id = p.id
                             WHERE s.token_hash = ? AND s.expires_at > ?""",
                          (digest(token), int(time.time()))).fetchone()
