"""Ayuda para simular bases de datos anteriores a la v11 (cuentas con varios
personajes) en pruebas de migración. Recibe una conexión sqlite3 cruda."""


def undo_v11(raw):
    """Devuelve una base v11 a la forma v10: usuario y contraseña en
    `players`, sesiones ligadas solo al personaje y sin tabla `accounts`."""
    raw.execute("""UPDATE players SET password_hash =
                   (SELECT a.password_hash FROM accounts a WHERE a.id = players.account_id)
                   WHERE account_id IS NOT NULL""")
    raw.execute("""CREATE TABLE sessions_v10 (
        token_hash TEXT PRIMARY KEY,
        player_id TEXT NOT NULL REFERENCES players(id),
        expires_at INTEGER NOT NULL)""")
    raw.execute("""INSERT INTO sessions_v10 SELECT token_hash, player_id, expires_at
                   FROM sessions WHERE player_id IS NOT NULL""")
    raw.execute("DROP TABLE sessions")
    raw.execute("ALTER TABLE sessions_v10 RENAME TO sessions")
    raw.execute("DROP INDEX players_name_key")
    raw.execute("DROP INDEX players_account")
    raw.execute("ALTER TABLE players DROP COLUMN name_key")
    raw.execute("ALTER TABLE players DROP COLUMN account_id")
    raw.execute("DROP TABLE accounts")
