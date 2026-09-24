"""SQLite storage. Every operation owns its connection; writes are transactional."""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import hashlib
from pathlib import Path
import secrets
import sqlite3
import time
import uuid

from . import combat, items

STATUSES = ("pending", "approved", "rejected", "removed")

PLAYER_COLUMNS = (
    "id, player_number, username, name, status, species, player_class, room, heading, created_at, last_access_at"
)

ATTRIBUTE_COLUMNS = ", ".join(f"attr_{name}" for name in combat.ATTRIBUTES)

# Estado de personaje (VT-NAR-003 / GAMEPLAY.md 20-22): se agrega a la
# consulta del jugador autenticado para que g.player siempre traiga nivel,
# XP, HP, fatiga, herida y los ocho atributos sin una segunda consulta.
# equipped_weapon_id/equipped_armor_id (Issue #57, GAMEPLAY.md 32.2) viajan
# igual: el arma/armadura activa del personaje es parte de su estado.
CHARACTER_COLUMNS = (f"{PLAYER_COLUMNS}, level, xp, pa_unspent, hp_current, hp_max, fatigue, wound, "
                     f"{ATTRIBUTE_COLUMNS}, equipped_weapon_id, equipped_armor_id")


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


CHARACTER_TABLES = [
    """CREATE TABLE discoveries (
            player_id TEXT NOT NULL REFERENCES players(id),
            key TEXT NOT NULL,
            xp_awarded INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(player_id, key))""",
    """CREATE TABLE visited_rooms (
            player_id TEXT NOT NULL REFERENCES players(id),
            room_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(player_id, room_id))""",
    """CREATE TABLE traversed_routes (
            player_id TEXT NOT NULL REFERENCES players(id),
            room_a TEXT NOT NULL,
            room_b TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(player_id, room_a, room_b))""",
    """CREATE TABLE pve_victories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT NOT NULL REFERENCES players(id),
            family TEXT NOT NULL,
            created_at TEXT NOT NULL)""",
    "CREATE INDEX pve_victories_player_time ON pve_victories(player_id, id)",
    """CREATE TABLE family_first_victory (
            player_id TEXT NOT NULL REFERENCES players(id),
            family TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(player_id, family))""",
    """CREATE TABLE room_encounters (
            player_id TEXT NOT NULL REFERENCES players(id),
            room_id TEXT NOT NULL,
            creature_id TEXT NOT NULL,
            hp_current REAL NOT NULL,
            failed_flee_attempts INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            UNIQUE(player_id, room_id))""",
]

# v4: GAMEPLAY.md 20.14 -- respawn de monstruos comunes con temporizador en
# vez de reaparicion llena instantanea. Por jugador/sala: mientras
# available_at no haya pasado, esa sala no vuelve a generar un encuentro
# nuevo para ese jugador.
CREATURE_COOLDOWN_TABLE = """CREATE TABLE creature_cooldowns (
        player_id TEXT NOT NULL REFERENCES players(id),
        room_id TEXT NOT NULL,
        creature_id TEXT NOT NULL,
        available_at TEXT NOT NULL,
        UNIQUE(player_id, room_id))"""

# v5: VT-PSY-004 (revision de Psicopedagogia en PR #49) -- registrar que
# senal(es) examino legitimamente un jugador en una sala, para poder exigir
# mas de una senal antes de conceder una identificacion/descubrimiento que
# ninguna senal aislada justifica por si sola (ver resolve_inspect).
EXAMINED_SIGNALS_TABLE = """CREATE TABLE examined_signals (
        player_id TEXT NOT NULL REFERENCES players(id),
        room_id TEXT NOT NULL,
        target TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(player_id, room_id, target))"""

# v6: Issue #57 (GAMEPLAY.md 32) -- inventario/equipamiento mínimo v1. Cada
# fila es una instancia propia del objeto (32.5: "identidad de
# objeto/instancia suficiente para impedir duplicación accidental"), nunca
# un contador; dos espadas de juramento del mismo jugador son dos filas.
INVENTORY_ITEMS_TABLE = """CREATE TABLE inventory_items (
        id TEXT PRIMARY KEY,
        player_id TEXT NOT NULL REFERENCES players(id),
        item_key TEXT NOT NULL,
        category TEXT NOT NULL CHECK(category IN ('weapon', 'armor')),
        forge_validated INTEGER NOT NULL DEFAULT 0,
        acquired_at TEXT NOT NULL)"""

CHARACTER_PLAYER_COLUMNS = [
    "level INTEGER NOT NULL DEFAULT 1",
    "xp INTEGER NOT NULL DEFAULT 0",
    "pa_unspent INTEGER NOT NULL DEFAULT 0",
    "hp_current REAL",
    "hp_max REAL",
    "fatigue INTEGER NOT NULL DEFAULT 0",
    "wound TEXT NOT NULL DEFAULT 'ninguna' CHECK(wound IN ('ninguna', 'leve', 'moderada', 'grave'))",
] + [f"attr_{name} INTEGER NOT NULL DEFAULT 10" for name in combat.ATTRIBUTES]


def initialize(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.execute("PRAGMA journal_mode = WAL")
        db.execute("BEGIN IMMEDIATE")
        version = db.execute("PRAGMA user_version").fetchone()[0]
        if version not in (0, 1, 2, 3, 4, 5, 6, 7, 8):
            raise RuntimeError("Versión de base de datos no soportada; no iniciar ni degradar.")
        if version == 8:
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
        elif version == 1:  # upgrade an existing deployment in place
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
        if version <= 2:
            # v3: estado de personaje jugable (VT-NAR-003) -- atributos, nivel,
            # XP, HP, fatiga, herida, descubrimientos, mapa progresivo y
            # combate. Ver GAMEPLAY.md 20-23 y server/combat.py.
            for column in CHARACTER_PLAYER_COLUMNS:
                db.execute(f"ALTER TABLE players ADD COLUMN {column}")
            for statement in CHARACTER_TABLES:
                db.execute(statement)
        if version <= 3:
            db.execute(CREATURE_COOLDOWN_TABLE)
        if version <= 4:
            db.execute(EXAMINED_SIGNALS_TABLE)
        if version <= 5:
            db.execute(INVENTORY_ITEMS_TABLE)
            db.execute("CREATE INDEX inventory_items_player ON inventory_items(player_id)")
            db.execute("ALTER TABLE players ADD COLUMN equipped_weapon_id TEXT REFERENCES inventory_items(id)")
            db.execute("ALTER TABLE players ADD COLUMN equipped_armor_id TEXT REFERENCES inventory_items(id)")
        if version <= 6:
            # v7: rumbo autoritativo (Issue #120) -- direccion cardinal del ultimo
            # movimiento aceptado, para que /api/map deje de depender de que el
            # cliente infiera "hacia donde mira" desde narrativa o imagen.
            db.execute("ALTER TABLE players ADD COLUMN heading TEXT "
                       "CHECK(heading IN ('north', 'south', 'east', 'west'))")
        if version <= 7:
            # v8: clase inicial (Issue #112, GAMEPLAY.md 2). NULL hasta que el
            # jugador la elige; personajes existentes la eligen al volver.
            db.execute("ALTER TABLE players ADD COLUMN player_class TEXT "
                       "CHECK(player_class IN ('arcano', 'juramentado', 'sombra', 'artifice'))")
        db.execute("PRAGMA user_version = 8")


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
            f"""SELECT {CHARACTER_COLUMNS}
               FROM players p
               JOIN sessions s ON s.player_id = p.id
               WHERE s.token_hash = ? AND s.expires_at > ?""",
            (digest(token), int(time.time())),
        ).fetchone()


def player_by_username(db, username):
    return db.execute(f"SELECT {PLAYER_COLUMNS} FROM players WHERE username = ?", (username,)).fetchone()


def character_by_id(db, player_id):
    return db.execute(
        f"SELECT {CHARACTER_COLUMNS} FROM players WHERE id = ?", (player_id,)
    ).fetchone()


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
    POST concurrentes solo pueden hacer que una de las dos devuelva True.

    De paso inicializa el estado de personaje jugable (GAMEPLAY.md 20.1/20.3):
    ocho atributos en 10, nivel 1, HP al maximo de nivel 1 con atributos
    base."""
    hp = combat.hp_max(level=1, resistencia=10, voluntad=10)
    with connect(path) as db:
        cursor = db.execute(
            """UPDATE players SET species = ?, room = ?, hp_current = ?, hp_max = ?
               WHERE id = ? AND species IS NULL""",
            (species, room, hp, hp, player_id),
        )
        return cursor.rowcount > 0


def set_player_class(path, player_id, class_id, starter_weapon_key=None):
    """Clase inicial (Issue #112). Igual que `set_species`: solo toma efecto
    la primera vez y exige que la especie ya este elegida; rowcount decide
    que llamada gano frente a dos POST concurrentes.

    En la misma transaccion entrega el arma inicial de la clase (entrega
    autoritativa, GAMEPLAY.md 32.5) y la deja activa si el personaje no tenia
    ya un arma equipada, para que nunca quede clase sin arma ni arma sin
    clase."""
    if starter_weapon_key is not None and items.category_of(starter_weapon_key) != "weapon":
        raise ValueError(f"Arma inicial desconocida: {starter_weapon_key}")
    with connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        cursor = db.execute(
            """UPDATE players SET player_class = ?
               WHERE id = ? AND player_class IS NULL AND species IS NOT NULL""",
            (class_id, player_id),
        )
        if cursor.rowcount == 0:
            return False
        if starter_weapon_key is not None:
            item_id = str(uuid.uuid4())
            db.execute(
                """INSERT INTO inventory_items(id, player_id, item_key, category, forge_validated, acquired_at)
                   VALUES (?, ?, ?, 'weapon', 0, ?)""",
                (item_id, player_id, starter_weapon_key, utcnow()),
            )
            db.execute("UPDATE players SET equipped_weapon_id = ? WHERE id = ? AND equipped_weapon_id IS NULL",
                       (item_id, player_id))
        return True


def move_player(path, player_id, room, heading=None):
    """`heading` es la direccion cardinal del movimiento que produjo este
    cambio de sala (Issue #120): el servidor la decide al aceptar el
    movimiento, nunca se infiere despues desde narrativa o nombre de sala."""
    with connect(path) as db:
        if heading is None:
            db.execute("UPDATE players SET room = ? WHERE id = ?", (room, player_id))
        else:
            db.execute("UPDATE players SET room = ?, heading = ? WHERE id = ?", (room, heading, player_id))


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


# --- Progresion de personaje (VT-NAR-003 / GAMEPLAY.md 20-22) -------------

def award_xp(path, player_id, amount):
    """Aplica XP y sube de nivel (GAMEPLAY.md 22.1), recalculando HP maximo
    (20.3) y curando al nuevo maximo en cada nivel ganado, mas 2 PA por
    nivel (19). Devuelve el estado resultante."""
    with connect(path) as db:
        row = character_by_id(db, player_id)
        new_level, new_xp, levels_gained = combat.apply_xp(row["level"], row["xp"], amount)
        hp_max_value, hp_current, pa_unspent = row["hp_max"], row["hp_current"], row["pa_unspent"]
        if levels_gained:
            hp_max_value = combat.hp_max(new_level, row["attr_resistencia"], row["attr_voluntad"])
            hp_current = hp_max_value
            pa_unspent += 2 * levels_gained
        db.execute(
            "UPDATE players SET level=?, xp=?, hp_max=?, hp_current=?, pa_unspent=? WHERE id=?",
            (new_level, new_xp, hp_max_value, hp_current, pa_unspent, player_id),
        )
        return {"level": new_level, "xp": new_xp, "levels_gained": levels_gained,
                "hp_current": hp_current, "hp_max": hp_max_value}


def award_discovery(path, player_id, key, category, reference_level):
    """Otorga un descubrimiento/hito una sola vez por personaje (22.7).
    Devuelve (is_new, xp_awarded)."""
    xp_amount = combat.discovery_xp(reference_level, category)
    with connect(path) as db:
        cursor = db.execute(
            "INSERT OR IGNORE INTO discoveries(player_id, key, xp_awarded, created_at) VALUES (?, ?, ?, ?)",
            (player_id, key, xp_amount, utcnow()),
        )
        is_new = cursor.rowcount > 0
    if is_new:
        award_xp(path, player_id, xp_amount)
    return is_new, xp_amount


def list_discoveries(path, player_id):
    with connect(path) as db:
        rows = db.execute(
            "SELECT key, xp_awarded, created_at FROM discoveries WHERE player_id = ? ORDER BY created_at",
            (player_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def has_discovery(path, player_id, key):
    with connect(path) as db:
        row = db.execute(
            "SELECT 1 FROM discoveries WHERE player_id = ? AND key = ?", (player_id, key)
        ).fetchone()
        return row is not None


# --- Senales examinadas (VT-PSY-004) ---------------------------------------

def mark_examined_signal(path, player_id, room_id, target):
    """Registra que el jugador examino legitimamente `target` en `room_id`.
    Devuelve True la primera vez; una repeticion es un no-op silencioso."""
    with connect(path) as db:
        cursor = db.execute(
            """INSERT OR IGNORE INTO examined_signals(player_id, room_id, target, created_at)
               VALUES (?, ?, ?, ?)""",
            (player_id, room_id, target, utcnow()),
        )
        return cursor.rowcount > 0


def has_examined_signal(path, player_id, room_id, target):
    with connect(path) as db:
        row = db.execute(
            "SELECT 1 FROM examined_signals WHERE player_id = ? AND room_id = ? AND target = ?",
            (player_id, room_id, target),
        ).fetchone()
        return row is not None


# --- Mapa progresivo (GAMEPLAY.md 23) -------------------------------------

def mark_visited(path, player_id, room_id):
    with connect(path) as db:
        cursor = db.execute(
            "INSERT OR IGNORE INTO visited_rooms(player_id, room_id, created_at) VALUES (?, ?, ?)",
            (player_id, room_id, utcnow()),
        )
        return cursor.rowcount > 0


def mark_route_traversed(path, player_id, room_a, room_b):
    # Ruta no dirigida (23.2): el par se guarda ordenado para no duplicar
    # ida/vuelta como dos rutas distintas.
    ordered = tuple(sorted((room_a, room_b)))
    with connect(path) as db:
        db.execute(
            """INSERT OR IGNORE INTO traversed_routes(player_id, room_a, room_b, created_at)
               VALUES (?, ?, ?, ?)""",
            (player_id, ordered[0], ordered[1], utcnow()),
        )


def get_map_state(path, player_id):
    with connect(path) as db:
        visited = [r["room_id"] for r in db.execute(
            "SELECT room_id FROM visited_rooms WHERE player_id = ? ORDER BY created_at", (player_id,)
        ).fetchall()]
        routes = [[r["room_a"], r["room_b"]] for r in db.execute(
            "SELECT room_a, room_b FROM traversed_routes WHERE player_id = ? ORDER BY created_at", (player_id,)
        ).fetchall()]
        return {"visited_rooms": visited, "traversed_routes": routes}


# --- Combate y encuentros --------------------------------------------------

def get_encounter(path, player_id, room_id):
    with connect(path) as db:
        row = db.execute(
            "SELECT * FROM room_encounters WHERE player_id = ? AND room_id = ?", (player_id, room_id)
        ).fetchone()
        return dict(row) if row else None


def start_encounter(path, player_id, room_id, creature_id, hp):
    """No-op si ya hay un encuentro activo en esa sala para ese jugador
    (persistente: si se aleja y vuelve sin resolverlo, sigue con la misma
    vida que tenia)."""
    with connect(path) as db:
        db.execute(
            """INSERT OR IGNORE INTO room_encounters
               (player_id, room_id, creature_id, hp_current, failed_flee_attempts, created_at)
               VALUES (?, ?, ?, ?, 0, ?)""",
            (player_id, room_id, creature_id, hp, utcnow()),
        )


def update_encounter(path, player_id, room_id, hp_current=None, failed_flee_attempts=None):
    fields, params = [], []
    if hp_current is not None:
        fields.append("hp_current = ?")
        params.append(hp_current)
    if failed_flee_attempts is not None:
        fields.append("failed_flee_attempts = ?")
        params.append(failed_flee_attempts)
    if not fields:
        return
    params += [player_id, room_id]
    with connect(path) as db:
        db.execute(
            f"UPDATE room_encounters SET {', '.join(fields)} WHERE player_id = ? AND room_id = ?", params
        )


def clear_encounter(path, player_id, room_id):
    with connect(path) as db:
        db.execute("DELETE FROM room_encounters WHERE player_id = ? AND room_id = ?", (player_id, room_id))


def record_pve_victory(path, player_id, family):
    """Registra la victoria, calcula si es la primera de esta familia
    (22.5) y cuenta repeticiones de la misma familia en las ultimas 10
    victorias para el antifarmeo (22.6, incluyendo esta victoria). Devuelve
    (is_first_family_victory, repeats_in_last_10)."""
    with connect(path) as db:
        db.execute(
            "INSERT INTO pve_victories(player_id, family, created_at) VALUES (?, ?, ?)",
            (player_id, family, utcnow()),
        )
        first_cursor = db.execute(
            "INSERT OR IGNORE INTO family_first_victory(player_id, family, created_at) VALUES (?, ?, ?)",
            (player_id, family, utcnow()),
        )
        is_first = first_cursor.rowcount > 0
        last_ten = db.execute(
            "SELECT family FROM pve_victories WHERE player_id = ? ORDER BY id DESC LIMIT 10",
            (player_id,),
        ).fetchall()
        repeats = sum(1 for row in last_ten if row["family"] == family)
        return is_first, repeats


def update_combat_state(path, player_id, hp_current=None, wound=None, room=None, fatigue=None):
    fields, params = [], []
    if hp_current is not None:
        fields.append("hp_current = ?")
        params.append(hp_current)
    if wound is not None:
        fields.append("wound = ?")
        params.append(wound)
    if room is not None:
        fields.append("room = ?")
        params.append(room)
    if fatigue is not None:
        fields.append("fatigue = ?")
        params.append(fatigue)
    if not fields:
        return
    params.append(player_id)
    with connect(path) as db:
        db.execute(f"UPDATE players SET {', '.join(fields)} WHERE id = ?", params)


# --- GAMEPLAY.md 20.14: respawn de monstruos comunes con temporizador -----

CREATURE_RESPAWN_COOLDOWN_SECONDS = 5 * 60  # referencia v1: "alrededor de 5 minutos".


def creature_available(path, player_id, room_id):
    """False si ese jugador derroto a la criatura de esa sala hace menos de
    CREATURE_RESPAWN_COOLDOWN_SECONDS: evita reaparicion llena instantanea
    y farmeo por entrar/salir de la sala."""
    with connect(path) as db:
        row = db.execute(
            "SELECT available_at FROM creature_cooldowns WHERE player_id = ? AND room_id = ?",
            (player_id, room_id),
        ).fetchone()
        if row is None:
            return True
        return utcnow() >= row["available_at"]


def start_creature_cooldown(path, player_id, room_id, creature_id,
                             seconds=CREATURE_RESPAWN_COOLDOWN_SECONDS):
    available_at = (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat(timespec="microseconds")
    with connect(path) as db:
        db.execute(
            """INSERT INTO creature_cooldowns(player_id, room_id, creature_id, available_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(player_id, room_id) DO UPDATE SET
                   creature_id = excluded.creature_id, available_at = excluded.available_at""",
            (player_id, room_id, creature_id, available_at),
        )


# --- Inventario y equipamiento v1 (Issue #57, GAMEPLAY.md 32) -------------

def character_by_player_id(path, player_id):
    with connect(path) as db:
        return character_by_id(db, player_id)


def grant_item(path, player_id, item_key, forge_validated=False):
    """Entrega autoritativa de un objeto del catálogo (32.5): recompensa,
    encargo válido, Forja o acción administrativa -- nunca compra directa
    del jugador en v1. Cada llamada crea una instancia propia (id nueva),
    aunque el jugador ya tenga otra copia del mismo `item_key`."""
    category = items.category_of(item_key)
    if category is None:
        raise ValueError(f"Objeto desconocido en el catálogo: {item_key}")
    item_id = str(uuid.uuid4())
    with connect(path) as db:
        db.execute(
            """INSERT INTO inventory_items(id, player_id, item_key, category, forge_validated, acquired_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (item_id, player_id, item_key, category, int(bool(forge_validated)), utcnow()),
        )
    return item_id


def list_inventory(path, player_id):
    """Objetos que el personaje posee legítimamente (32.1), sin importar si
    están activos."""
    with connect(path) as db:
        rows = db.execute(
            """SELECT id, item_key, category, forge_validated, acquired_at FROM inventory_items
               WHERE player_id = ? ORDER BY acquired_at""",
            (player_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def equipped_item_keys(path, weapon_item_id, armor_item_id):
    """Resuelve en una sola consulta las claves de catálogo de lo
    actualmente equipado, a partir de los ids guardados en `players`.
    Devuelve (weapon_item_key_or_None, armor_item_key_or_None)."""
    ids = [item_id for item_id in (weapon_item_id, armor_item_id) if item_id]
    if not ids:
        return None, None
    with connect(path) as db:
        placeholders = ",".join("?" * len(ids))
        rows = db.execute(
            f"SELECT id, item_key FROM inventory_items WHERE id IN ({placeholders})", ids
        ).fetchall()
    by_id = {row["id"]: row["item_key"] for row in rows}
    return by_id.get(weapon_item_id), by_id.get(armor_item_id)


def equip_item(path, player_id, item_id):
    """GAMEPLAY.md 32.3: equipar reemplaza atómicamente el objeto activo de
    la misma categoría; requiere poseer el objeto y, si el catálogo lo
    exige, tener la validación de Forja completa (32.4). `BEGIN IMMEDIATE`
    hace la operación atómica de verdad frente a dos solicitudes
    concurrentes, igual que `set_species`. Devuelve (ok, category_or_None,
    reason_or_None); el llamador decide si "fuera de combate" se cumple."""
    with connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        item = db.execute(
            "SELECT id, item_key, category, forge_validated FROM inventory_items WHERE id = ? AND player_id = ?",
            (item_id, player_id),
        ).fetchone()
        if item is None:
            return False, None, "No posees ese objeto."
        catalog = items.get_item(item["item_key"])
        if catalog["forge_required"] and not item["forge_validated"]:
            return False, None, "Ese objeto todavía no tiene su validación de Forja completa."
        column = "equipped_weapon_id" if item["category"] == "weapon" else "equipped_armor_id"
        db.execute(f"UPDATE players SET {column} = ? WHERE id = ?", (item_id, player_id))
        return True, item["category"], None


def unequip_item(path, player_id, category):
    """GAMEPLAY.md 32.3: desequipar devuelve el objeto a poseído/no activo;
    no destruye nada ni tiene coste."""
    if category not in ("weapon", "armor"):
        raise ValueError(f"Categoría desconocida: {category}")
    column = "equipped_weapon_id" if category == "weapon" else "equipped_armor_id"
    with connect(path) as db:
        db.execute(f"UPDATE players SET {column} = NULL WHERE id = ?", (player_id,))
