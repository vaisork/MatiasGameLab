from datetime import timedelta
import hmac
import os
from pathlib import Path
import random
import re
import secrets
import sqlite3
import unicodedata

from flask import (Flask, abort, g, jsonify, redirect, render_template, request, send_from_directory,
                    session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from . import bosses, combat, content_parser, creatures, dm_auth, economy, encounters, errands, items, major_fauna, npc_dialogue, population, recovery, respawn as respawn_logic, store, threats, travelers, world

SAFE_RECOVERY_MESSAGE = ("En la plaza de Valdren puedes detenerte sin vigilar cada ruido del "
                          "campo. Entre el movimiento cotidiano del pueblo recuperas fuerzas "
                          "antes de volver al camino.")

# DEATH-PRESENTATION-01 (#366 / Narrador PR #368). Texto reusable; no cambia
# ninguna consecuencia mecánica de muerte o respawn.
DEATH_HEADING = "HAS MUERTO"
DEATH_FALL_MESSAGE = ("Las fuerzas te abandonan. El combate desaparece a tu alrededor y "
                      "pierdes la conciencia.")

# Categorias cualitativas de "evaluar" (GAMEPLAY.md 22.11) -- nunca exponen
# numeros, solo la frase equivalente.
EVALUATE_TEXT = {
    "trivial": "parece muy inferior a ti",
    "favorable": "parece favorable",
    "comparable": "parece comparable a ti",
    "peligroso": "parece peligroso",
    "abrumador": "te supera claramente",
}


def _normalize(text):
    """minusculas y sin acentos, para comparar objetivos de examinar/atacar
    sin depender de que el jugador escriba tildes."""
    folded = unicodedata.normalize("NFKD", (text or "").strip().lower())
    return "".join(c for c in folded if not unicodedata.combining(c))


def _can_block(path, player_id):
    """GAMEPLAY.md 20.5 + WEAPON_CATALOG.md: Bloquear/desviar depende de si
    el arma actualmente equipada lo permite (Issue #57 conecta equipo real
    a la ranura de arma; ver `items.WEAPONS` para qué armas lo permiten).
    Sin arma equipada, o con una que no lo permite, devuelve False -- por
    eso 'bloquear' sigue sin aparecer en `available_actions` para un
    personaje desarmado, en vez de simular equipo que no existe."""
    character = store.character_by_player_id(path, player_id)
    if not character or not character["equipped_weapon_id"]:
        return False
    weapon_key, _armor_key = store.equipped_item_keys(path, character["equipped_weapon_id"], None)
    weapon = items.get_item(weapon_key) if weapon_key else None
    return bool(weapon and weapon["can_block"])


def _equipped_weapon(path, player_id):
    """Objeto del catalogo para el arma equipada real, o None si va desarmado."""
    character = store.character_by_player_id(path, player_id)
    if not character or not character["equipped_weapon_id"]:
        return None
    weapon_key, _ = store.equipped_item_keys(path, character["equipped_weapon_id"], None)
    return items.get_item(weapon_key) if weapon_key else None


def _can_use_signature_ability(path, player, encounter=None):
    """GAMEPLAY.md 36: valida requisitos fisicos/contextuales de la capacidad firma.
    Devuelve (authorized: bool, reason_if_not: str or None, ability_dict)."""
    if player is None:
        return False, "Personaje no encontrado.", None
    player_dict = dict(player) if hasattr(player, "keys") else player
    player_class = player_dict.get("player_class")
    ability = combat.SIGNATURE_ABILITIES.get(player_class)
    if not ability:
        return False, "Tu clase no dispone de una capacidad firma.", None
    if encounter:
        enc_dict = dict(encounter) if hasattr(encounter, "keys") else encounter
        if enc_dict.get("signature_cooldown", 0) > 0:
            cd = enc_dict["signature_cooldown"]
            return False, f"{ability['name']} está en recarga (faltan {cd} rondas).", ability
    if player_class == "juramentado":
        if not _can_block(path, player["id"]):
            return False, "Requiere un arma u objeto equipado que permita bloquear.", ability
    elif player_class == "arcano":
        w = _equipped_weapon(path, player["id"])
        if not (w and w.get("is_arcane_focus")):
            return False, "Requiere un foco arcano equipado.", ability
    elif player_class == "artifice":
        w = _equipped_weapon(path, player["id"])
        if not (w and w.get("is_ranged")):
            return False, "Requiere un arma a distancia equipada.", ability
    elif player_class == "sombra":
        if encounter:
            creature = creatures.get_creature(encounter["creature_id"])
            if creature and not creature.get("focus_break_possible", True):
                return False, "El objetivo no puede perder el foco por este medio.", ability
    return True, None, ability


# Biblioteca de arte HTML (vintage-telnet/assets/html-ui/), servida explícitamente en vez de
# habilitar una carpeta estática general -- mantiene el resto del árbol del repo fuera de HTTP.
HTML_UI_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "html-ui"
LOCATION_ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "vintage-telnet" / "locations"
# Mapa regional aprobado (Issue #120 / PR #99): carpeta propia y acotada, nunca
# el arbol completo de assets/.
MAPS_ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "vintage-telnet" / "maps"
CREATURE_ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "vintage-telnet" / "creatures"
SPECIES_ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "vintage-telnet" / "species"
APP_ICON_PATH = Path(__file__).resolve().parent.parent.parent / "assets" / "icon" / "vintage-telnet-portal.webp"


def create_app(config=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("VT_SECRET_KEY"),
        DATA_DIR=os.environ.get("VT_DATA_DIR"),
        SESSION_COOKIE_NAME="vt_session",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_REFRESH_EACH_REQUEST=False,
        SESSION_COOKIE_SECURE=os.environ.get("VT_ALLOW_HTTP", "0") != "1",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
        MAX_CONTENT_LENGTH=8192,
        TRUSTED_HOSTS=os.environ.get("VT_TRUSTED_HOSTS", "localhost,127.0.0.1").split(","),
    )
    if config:
        app.config.update(config)
    if (not app.config["SECRET_KEY"] or len(app.config["SECRET_KEY"]) < 32
            or app.config["SECRET_KEY"].startswith("REPLACE_")):
        raise RuntimeError("VT_SECRET_KEY debe contener al menos 32 caracteres aleatorios.")
    if not app.config["DATA_DIR"] or not Path(app.config["DATA_DIR"]).is_absolute():
        raise RuntimeError("VT_DATA_DIR debe ser una ruta absoluta persistente.")
    path = str(Path(app.config["DATA_DIR"]) / "vintage.sqlite3")
    store.initialize(path)
    threats.load_canonical_threat_zones()
    world.set_home_species_resolver(lambda pid: store.get_player_species(path, pid))
    store.relocate_players_outside_world(path, set(world.ROOMS), world.get_starting_room_for_species)
    app.config["DATABASE"] = path
    dummy_hash = generate_password_hash(secrets.token_urlsafe(32))
    app.jinja_env.globals["xp_for_next_level"] = combat.xp_for_next_level
    app.jinja_env.globals["class_list"] = world.CLASSES
    app.jinja_env.globals["class_names"] = {c["id"]: c["name"] for c in world.CLASSES}
    app.jinja_env.globals["ambient_icons"] = world.AMBIENT_ICONS

    def from_public_internet():
        """Tailscale Funnel marca cada petición que llega desde internet con
        `Tailscale-Funnel-Request`; las de la red Tailscale privada o de la
        propia Raspberry no la traen. Un visitante no puede quitarla: la
        agrega el proxy de Funnel."""
        return bool(request.headers.get("Tailscale-Funnel-Request"))

    @app.before_request
    def dm_panel_is_private():
        """Petición de Javier (2026-09-25): el panel del Dungeon Master solo
        existe desde la red privada (Tailscale) o la propia Raspberry, nunca
        desde internet. Para Funnel responde 404, como si no existiera, y
        corre antes de cualquier otra lógica (incluido CSRF y login)."""
        if (request.path == "/dm" or request.path.startswith("/dm/")) and from_public_internet():
            abort(404)

    @app.before_request
    def prepare_request():
        # Even the anonymous form has a signed, random anti-CSRF token.
        if request.method == "POST":
            expected = session.get("csrf", "")
            supplied = request.form.get("csrf", "")
            if not supplied and request.is_json:
                supplied = (request.get_json(silent=True) or {}).get("csrf", "")
            if not expected or not hmac.compare_digest(expected.encode(), str(supplied).encode()):
                abort(400, "Formulario vencido. Recarga la página.")
        g.csp_nonce = secrets.token_urlsafe(16)
        if request.endpoint in ("health", "html_ui_assets", "location_assets", "map_assets"):
            return
        session.setdefault("csrf", secrets.token_urlsafe(32))
        g.account = store.account_for_token(path, session.get("token"))
        g.player = store.player_for_token(path, session.get("token")) if g.account else None
        # Aunque haya una sesión de DM abierta desde la red privada, esa
        # sesión no da poderes de DM si la petición llega por internet.
        g.dm = bool(session.get("dm")) and not from_public_internet()

    @app.context_processor
    def inject_csp_nonce():
        return {"csp_nonce": getattr(g, "csp_nonce", ""), "account": getattr(g, "account", None)}

    # Imágenes/iconos públicos del juego: el celular los guarda un día para
    # que la ilustración no se vuelva a descargar (y parpadee) en cada acción.
    # Las páginas y la API siguen sin guardarse (no-store): llevan datos del
    # jugador.
    CACHEABLE_ENDPOINTS = {"app_icon", "html_ui_assets", "location_assets", "map_assets", "creature_assets", "species_assets"}

    @app.after_request
    def headers(response):
        if request.endpoint in CACHEABLE_ENDPOINTS and response.status_code in (200, 304):
            response.headers["Cache-Control"] = "public, max-age=86400"
        else:
            response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        nonce = getattr(g, "csp_nonce", "")
        response.headers["Content-Security-Policy"] = (
            f"default-src 'none'; style-src 'unsafe-inline'; img-src 'self'; "
            f"script-src 'nonce-{nonce}'; connect-src 'self'; form-action 'self'; "
            "frame-ancestors 'none'; base-uri 'none'")
        return response

    def establish_session(token):
        session.clear()
        session.permanent = True
        session["csrf"] = secrets.token_urlsafe(32)
        session["token"] = token
        return redirect(url_for("index"), code=303)

    def character_ready(player):
        """Especie y clase inicial elegidas (GAMEPLAY.md 2, Issue #112): hasta
        entonces el personaje no entra al mundo."""
        return player["species"] is not None and player["player_class"] is not None

    def require_approved_player():
        if g.player is None:
            abort(401)
        if g.player["status"] != "approved":
            abort(403)

    def require_dm():
        if not g.dm:
            abort(403)

    def _minimap(state, current_room):
        """Datos del minimapa (navegación, Issue #135), solo de lo conocido:
        salas visitadas con nombre y coordenadas de rejilla (world.map_layout),
        rutas recorridas y, por cada sala visitada, las direcciones de salida
        que llevan a una sala todavía no visitada (sin nombre ni destino)."""
        layout = world.map_layout()
        visited = [room_id for room_id in state["visited_rooms"] if room_id in layout]
        visited_set = set(visited)
        places = []
        unexplored = []
        for room_id in visited:
            room = world.get_room(room_id)
            x, y = layout[room_id]
            places.append({"id": room_id, "name": room["name"], "x": x, "y": y,
                           "current": room_id == current_room})
            for direction, destination in room["exits"].items():
                if destination not in visited_set:
                    unexplored.append({"from": room_id, "direction": direction})
        current_room_data = world.get_room(current_room)
        current_room_name = current_room_data["name"] if current_room_data else current_room
        room_names = {}
        for r_id in state.get("visited_rooms", []):
            r = world.get_room(r_id)
            if r and "name" in r:
                room_names[r_id] = r["name"]
            elif world.is_home_room(r_id):
                room_names[r_id] = world.HOME_ROOM_NAME
        return {
            "current_room": current_room,
            "current_room_name": current_room_name,
            "places": places,
            "unexplored_exits": unexplored,
            "room_names": room_names,
        }

    def room_view(room_id, player_id):
        others = store.players_in_room(path, room_id, exclude_id=player_id)
        view = world.describe_room(room_id, [p["name"] for p in others])
        view["messages"] = store.recent_messages(path, room_id)
        # Navegación: el nombre del destino de cada salida solo se muestra si
        # el personaje ya estuvo ahí (GAMEPLAY.md 23: el mapa es progresivo);
        # una salida nueva se ve como dirección sin nombre.
        room_data = world.get_room(room_id)
        if room_data and view.get("exits"):
            visited = set(store.get_map_state(path, player_id)["visited_rooms"])
            for exit_info in view["exits"]:
                destination = room_data["exits"].get(exit_info["direction"])
                target = world.get_room(destination) if destination in visited else None
                exit_info["known_name"] = target["name"] if target else None
        encounter = store.get_encounter(path, player_id, room_id)
        view["in_combat"] = bool(encounter and encounter.get("engaged", 1))
        boss_eval = bosses.get_room_boss_view(path, player_id, room_id)
        if boss_eval and boss_eval.message:
            view["threat_signal"] = boss_eval.message
        threat_eval = threats.get_room_threat_view(path, player_id, room_id)
        if not (boss_eval and boss_eval.message) and threat_eval and threat_eval.message:
            view["threat_signal"] = threat_eval.message
        if encounter:
            creature = creatures.get_creature(encounter["creature_id"])
            prep = encounter.get("prepared_action")
            view["encounter"] = {
                "creature_id": encounter["creature_id"],
                "name": creature["name"],
                # GAMEPLAY.md 31: nunca HP numerico de un enemigo, solo
                # condicion cualitativa; el comportamiento ayuda a distinguir
                # Mordelinde de Espinajo antes de decidir (VT-PSY-004).
                "condition": combat.enemy_condition(encounter["hp_current"], creature["hp"]),
                "behavior": creature["behavior_text"],
            }
            if prep:
                view["encounter"]["prepared_action"] = {
                    "id": prep["id"],
                    "name": prep["name"],
                    "interruptible": prep.get("interruptible", False),
                    "frontal": prep.get("frontal", False),
                    "telegraph": prep.get("telegraph", ""),
                }
                view["encounter"]["telegraph"] = prep.get("telegraph", "")
            # En combate el marco muestra a la criatura, o nada si todavía no
            # hay arte aprobado de ella (nunca el paisaje de fondo).
            view["art"] = creatures.CREATURE_ART.get(encounter["creature_id"])
            view["combat_log"] = store.get_combat_log(path, player_id, room_id) if view["in_combat"] else []
            # Issue #73 / UI_ACTIONS_CONTRACT.md: fuente estructurada de
            # acciones de combate/descanso inmediatas -- el cliente no debe
            # deducir botones por su cuenta. Alcance de esta entrega: solo
            # combate/descanso (lo que pide el Issue); movimiento, mirar,
            # observar/examinar y hablar ya tienen su propia autorizacion
            # (salidas de sala, texto de examinar, NPC activo) y quedan
            # fuera de esta lista por ahora.
            view["available_actions"] = [
                {"action": "atacar", "targets": [encounter["creature_id"]]},
                {"action": "evaluar", "targets": [encounter["creature_id"]]},
                {"action": "huir"},
            ]
            if view["in_combat"]:
                view["available_actions"].extend([
                    {"action": "esquivar"},
                    {"action": "resistir"},
                ])
            if view["in_combat"] and _can_block(path, player_id):
                view["available_actions"].append({"action": "bloquear"})
            view["n0_presence"] = None
            character = store.character_by_player_id(path, player_id)
            if character and character["player_class"]:
                ready, disabled_reason, ability_def = _can_use_signature_ability(path, character, encounter)
                cd = encounter.get("signature_cooldown", 0) if encounter else 0
                view["signature_ability"] = {"id": ability_def["id"], "name": ability_def["name"],
                                              "cooldown_remaining": cd, "ready": ready,
                                              "disabled_reason": disabled_reason}
                if ready:
                    view["available_actions"].append({"action": "capacidad", "name": ability_def["name"]})
        elif boss_eval and boss_eval.close_encounter:
            view["encounter"] = None
            view["boss_c5"] = {
                "boss_id": boss_eval.boss_id, "name": boss_eval.name,
                "current_hp": boss_eval.current_hp, "max_hp": boss_eval.max_hp,
                "phase": boss_eval.current_phase,
            }
            view["available_actions"] = list(boss_eval.available_actions)
            view["npcs"] = []
            view["n0_presence"] = None
        else:
            view["encounter"] = None
            if threat_eval and threat_eval.close_encounter:
                creature = creatures.get_creature(threat_eval.creature_id)
                view["threat_c3"] = {
                    "threat_zone_id": threat_eval.zone_id,
                    "creature_id": threat_eval.creature_id,
                    "name": creature["name"],
                    "condition": combat.enemy_condition(creature["hp"], creature["hp"]),
                    "behavior": creature["behavior_text"],
                }
                view["art"] = creatures.CREATURE_ART.get(threat_eval.creature_id)
                view["available_actions"] = list(threat_eval.available_actions)
                view["npcs"] = []
                view["n0_presence"] = None
            else:
                rest_recovery = store.field_rest_status(path, player_id)
                view["rest_recovery"] = rest_recovery
                view["available_actions"] = []
                if rest_recovery and rest_recovery["available"]:
                    view["available_actions"].append({"action": "descansar"})
                npcs_present = list(npc_dialogue.get_registry().get_in_room(room_id))
                for traveler in travelers.get_travelers_in_room(room_id, db_path=path):
                    if not any(npc["id"] == traveler["id"] for npc in npcs_present):
                        npcs_present.append(traveler)
                npcs_list = []
                if npcs_present:
                    npcs_list = [{"id": n["id"], "name": n["name"], "role": n.get("role", "habitante"), "is_n0": False} for n in npcs_present]
                    for n in npcs_present:
                        view["available_actions"].append({"action": "hablar", "targets": [n["name"].lower(), n["id"]]})
                if room_id == "khariel_forja" and not store.get_story_flag(path, player_id, "hoshai_paso_ayudado"):
                    view["available_actions"].append({"action": "ayudar", "targets": ["aren", "paso"]})
                elif room_id == "brumak_forja" and not store.reconcile_story_flag_alias(path, player_id, "korven_carga_asentada", "korven_trabajo_ayudado"):
                    view["available_actions"].append({"action": "ayudar", "targets": ["karn", "apoyo"]})
                n0 = population.get_room_n0_presence(room_id, room_data=room_data)
                view["n0_presence"] = n0
                if n0:
                    npcs_list.append({"id": n0["id"], "name": n0["name"], "role": n0["role_id"],
                                      "is_n0": True, "bark": n0.get("bark", "")})
                    view["available_actions"].append({"action": "hablar", "targets": [n0["name"].lower(), n0["id"], n0["role_id"].lower()]})
                if npcs_list:
                    view["npcs"] = npcs_list
        major_data = major_fauna.get_zone_view_data(room_id, db_path=path)
        if major_data:
            view["major_fauna"] = major_data
            if major_data["ring"] == 3 and major_data["present"] and not view.get("in_combat"):
                if not any(action.get("action") == "atacar" for action in view["available_actions"]):
                    view["available_actions"].append({"action": "atacar", "targets": [major_data["species_id"], major_data["species_name"].lower()]})
                if not any(action.get("action") == "observar" for action in view["available_actions"]):
                    view["available_actions"].append({"action": "observar", "targets": [major_data["species_id"], major_data["species_name"].lower()]})
        return view

    # Intenciones canonicas: boton y comando escrito deben terminar en la misma
    # accion autoritativa del servidor (ver FIRST_PLAYABLE_SLICE.md).
    DIRECTION_ALIASES = {
        "norte": "north", "n": "north", "north": "north",
        "sur": "south", "s": "south", "south": "south",
        "este": "east", "e": "east", "east": "east",
        "oeste": "west", "o": "west", "west": "west",
        "salir": "salir", "salida": "salir", "out": "salir", "leave": "salir",
    }
    LOOK_ALIASES = {"mirar", "ver", "look"}
    INSPECT_ALIASES = {"observar", "examinar"}
    SAY_PREFIXES = ("decir ", "say ")
    TALK_PREFIXES = ("hablar con ", "hablar ")
    FLEE_ALIASES = {"huir"}
    AVOID_ALIASES = {"evitar", "retroceder", "avoid"}
    ATTACK_ALIASES = {"atacar"}
    EVALUATE_ALIASES = {"evaluar", "considerar"}
    REST_ALIASES = {"descansar"}
    DODGE_ALIASES = {"esquivar"}
    BLOCK_ALIASES = {"bloquear"}
    RESIST_ALIASES = {"resistir"}
    HELP_ALIASES = {"ayudar", "sujetar", "asegurar", "socorrer", "sostener"}
    SIGNATURE_ABILITY_ALIASES = {
        "capacidad", "firma", "habilidad", "guardia comprometida", "guardia", "guardia_comprometida",
        "impulso arcano", "impulso", "impulso_arcano", "borrar el foco", "borrar foco", "foco", "borrar_el_foco",
        "tiro de interrupcion", "tiro de interrupción", "interrupcion", "interrupción", "tiro", "tiro_de_interrupcion",
    }
    # GAMEPLAY.md 32.8: comandos canónicos de inventario/equipo (Issue #57).
    EQUIP_PREFIXES = ("equipar ",)
    UNEQUIP_PREFIXES = ("desequipar ",)
    # ECONOMY.md §§7-9: comandos de comercio con Daro (Issue #408).
    BUY_PREFIXES = ("comprar ",)
    SELL_PREFIXES = ("vender ",)
    USE_PREFIXES = ("usar ", "consumir ")

    def parse_intent(raw):
        """Clasifica texto del terminal sin convertir comandos desconocidos en chat."""
        text = (raw or "").strip()
        lowered = text.lower()
        if lowered in DIRECTION_ALIASES:
            return {"type": "move", "direction": DIRECTION_ALIASES[lowered]}
        if lowered in LOOK_ALIASES:
            return {"type": "look"}
        if lowered in FLEE_ALIASES:
            return {"type": "flee"}
        if lowered in AVOID_ALIASES:
            return {"type": "avoid"}
        if lowered in REST_ALIASES:
            return {"type": "rest"}
        if lowered in DODGE_ALIASES:
            return {"type": "dodge"}
        if lowered in BLOCK_ALIASES:
            return {"type": "block"}
        if lowered in RESIST_ALIASES:
            return {"type": "resist"}
        if lowered in SIGNATURE_ABILITY_ALIASES or lowered.startswith("capacidad "):
            return {"type": "signature_ability"}
        for verb in INSPECT_ALIASES:
            if lowered == verb:
                return {"type": "inspect", "verb": verb, "target": ""}
            prefix = verb + " "
            if lowered.startswith(prefix):
                return {"type": "inspect", "verb": verb, "target": text[len(prefix):].strip()}
        for verb in ATTACK_ALIASES:
            if lowered == verb:
                return {"type": "attack", "target": ""}
            prefix = verb + " "
            if lowered.startswith(prefix):
                return {"type": "attack", "target": text[len(prefix):].strip()}
        for verb in EVALUATE_ALIASES:
            if lowered == verb:
                return {"type": "evaluate", "target": ""}
            prefix = verb + " "
            if lowered.startswith(prefix):
                return {"type": "evaluate", "target": text[len(prefix):].strip()}
        for verb in HELP_ALIASES:
            if lowered == verb:
                return {"type": "help_scene", "target": ""}
            prefix = verb + " "
            if lowered.startswith(prefix):
                return {"type": "help_scene", "target": text[len(prefix):].strip()}
        for prefix in TALK_PREFIXES:
            if lowered.startswith(prefix):
                target_raw = text[len(prefix):].strip()
                if not target_raw:
                    return {"type": "invalid"}
                parts = target_raw.split(None, 1)
                candidate = parts[0]
                if len(parts) > 1 and npc_dialogue.get_registry().get(candidate) is not None:
                    return {"type": "talk_npc", "target": candidate, "message": parts[1].strip()}
                return {"type": "talk_npc", "target": target_raw, "message": ""}
        for prefix in EQUIP_PREFIXES:
            if lowered.startswith(prefix):
                target = text[len(prefix):].strip()
                return {"type": "equip", "target": target} if target else {"type": "invalid"}
        for prefix in UNEQUIP_PREFIXES:
            if lowered.startswith(prefix):
                target = text[len(prefix):].strip()
                return {"type": "unequip", "target": target} if target else {"type": "invalid"}
        if lowered == "comprar":
            return {"type": "buy", "target": ""}
        for prefix in BUY_PREFIXES:
            if lowered.startswith(prefix):
                target = text[len(prefix):].strip()
                return {"type": "buy", "target": target} if target else {"type": "invalid"}
        if lowered == "vender":
            return {"type": "sell", "target": ""}
        if lowered == "encargos":
            return {"type": "errands_list"}
        for verb, action in (("aceptar encargo ", "accept"), ("registrar encargo ", "record"),
                             ("cobrar encargo ", "claim")):
            if lowered.startswith(verb):
                return {"type": "errand", "action": action, "contract_id": text[len(verb):].strip()}
        for prefix in SELL_PREFIXES:
            if lowered.startswith(prefix):
                target = text[len(prefix):].strip()
                return {"type": "sell", "target": target} if target else {"type": "invalid"}
        for prefix in USE_PREFIXES:
            if lowered.startswith(prefix):
                target = text[len(prefix):].strip()
                return {"type": "use_recovery", "target": target} if target else {"type": "invalid"}
        for prefix in SAY_PREFIXES:
            if lowered.startswith(prefix):
                body = text[len(prefix):].strip()
                return {"type": "say", "body": body} if body else {"type": "invalid"}
        return {"type": "unknown"}


    def attempt_move(player, direction):
        """Unica logica autoritativa de movimiento. Devuelve
        (accepted, previous_room_id, new_room_id_or_None, reason_or_None, level_up_event_or_None).

        De paso actualiza el mapa progresivo (GAMEPLAY.md 23: la sala de
        destino queda visitada y la ruta recorrida), coloca una criatura si
        la sala de destino puede tenerla y todavia no hay ninguna activa
        (VT-NAR-003), y otorga el hito de regreso si corresponde."""
        previous_room = player["room"]
        room = world.get_room(previous_room)
        if direction in ("salir", "salida", "out", "leave"):
            if world.is_home_room(previous_room):
                direction = world.HOME_EXIT_DIRECTION
            else:
                return False, previous_room, None, "No puedes ir en esa dirección.", None
        destination = room["exits"].get(direction) if room else None
        if not destination:
            return False, previous_room, None, "No puedes ir en esa dirección.", None
        # GAMEPLAY §40.6: Abandono explícito de zona C3 tras activación en close
        for p_zone in threats.get_threat_zones_for_room(previous_room):
            if previous_room in p_zone.encounter_rooms:
                rec = store.get_threat_state(path, player["id"], p_zone.threat_zone_id)
                if rec and rec["state"] == "close":
                    threats.resolve_threat_avoid(path, player["id"], p_zone.threat_zone_id)
        store.move_player(path, player["id"], destination, direction)
        store.mark_visited(path, player["id"], destination)
        if not world.is_home_room(previous_room) and not world.is_home_room(destination):
            store.mark_route_traversed(path, player["id"], previous_room, destination)

        # GAMEPLAY §40.10: Evaluación de amenaza C3 en sala de destino
        threat_eval = threats.evaluate_room_threat(path, player["id"], destination)
        is_close_threat = bool(threat_eval and threat_eval.close_encounter)

        # Primero el encuentro fijo de la sala y, si no hay, la fauna
        # aleatoria de su pool (Issue #160). Solo se tira el dado si no hay
        # ya una pelea activa ni enfriamiento en esa sala Y no hay C3 en close (§40.10).
        boss_in_destination = bosses.get_boss_by_arena(destination)
        boss_active = bool(boss_in_destination and not bosses.is_boss_defeated(path, boss_in_destination.boss_id))
        if (not is_close_threat and not boss_active
                and not store.get_encounter(path, player["id"], destination)
                and store.creature_available(path, player["id"], destination)):
            encounter_creature = encounters.get_encounter_for_room(destination)
            if encounter_creature:
                creature = creatures.get_creature(encounter_creature)
                store.start_encounter(path, player["id"], destination, encounter_creature,
                                      creature["hp"], engaged=bool(world.get_room_encounter(destination)))
        level_up_event = None
        previous_boss = bosses.get_boss_by_arena(previous_room)
        if previous_boss and not bosses.is_boss_defeated(path, previous_boss.boss_id):
            bosses.check_and_clear_attempt_if_wiped(path, previous_boss.boss_id)
        if (destination == "valdren_centro"
                and store.has_discovery(path, player["id"], "lindero_roto")
                and not store.has_discovery(path, player["id"], "regreso_valdren_lindero")):
            discovery = world.get_discovery("regreso_valdren_lindero")
            is_new, xp_amount, xp_state = store.award_discovery(
                path, player["id"], "regreso_valdren_lindero",
                discovery["category"], discovery["reference_level"],
                reward_item=discovery["reward_item"])
            if is_new:
                g.reward_message = f"{discovery['reward_text']} (+{xp_amount} XP)"
                level_message = _level_up_message(xp_state)
                if level_message:
                    g.reward_message += f" {level_message}"
            level_up_event = _level_up_event(xp_state)
        # Umbrales de los 5 ramales superficiales (#419, #422, #423, #424, #341)
        SURFACE_THRESHOLDS_INFO = {
            "bm_09_boca_rocosa": ("boca_montana_umbral_descubierto", "boca_montana_umbral", "Boca de la Montaña"),
            "cq_09_estrechamiento_raices_roca": ("canal_quieto_umbral_descubierto", "canal_quieto_umbral", "Canal Quieto"),
            "ca_09_cavidad_tras_frente": ("cantera_abandonada_umbral_descubierto", "cantera_abandonada_umbral", "Cantera Abandonada"),
            "ge_09_boca_inferior": ("grieta_eco_seco_umbral_descubierto", "grieta_eco_seco_umbral", "Grieta del Eco Seco"),
            "mh_10_umbral_inferior": ("molino_hundido_umbral_descubierto", "molino_hundido_umbral", "Molino Hundido"),
        }
        if destination in SURFACE_THRESHOLDS_INFO:
            flag_name, disc_key, name = SURFACE_THRESHOLDS_INFO[destination]
            if not store.get_story_flag(path, player["id"], flag_name):
                store.set_story_flag(path, player["id"], flag_name, True)
                is_new, xp_amount, xp_state = store.award_discovery(
                    path, player["id"], disc_key, "descubrimiento_mayor", 1)
                if is_new:
                    g.reward_message = f"Has alcanzado el umbral de {name}. (+{xp_amount} XP)"
                    level_message = _level_up_message(xp_state)
                    if level_message:
                        g.reward_message += f" {level_message}"
                    level_up_event = _level_up_event(xp_state)
        return True, previous_room, destination, None, level_up_event

    def _attributes(player):
        return {name: player[f"attr_{name}"] for name in combat.ATTRIBUTES}

    def _level_up_message(xp_state):
        """GAMEPLAY.md 25.9: aviso breve de nuevo nivel, PA y PP obtenidos.
        No abre ninguna distribucion obligatoria; el jugador decide cuando
        gastar sus PA desde Personaje."""
        if not xp_state or not xp_state["levels_gained"]:
            return None
        message = f"¡Subes a nivel {xp_state['level']}! +{xp_state['pa_gained']} PA"
        if xp_state["pp_gained"]:
            message += f", +{xp_state['pp_gained']} PP"
        return message + "."

    def _level_up_event(xp_state):
        """#381 / GAMEPLAY §25.9: evento efímero para el frontend.

        Consume exclusivamente el resultado autoritativo de store.award_xp()
        y la función vigente de XP siguiente; no persiste nada, así que un
        GET/reconnect posterior no puede reemitir una subida antigua.
        """
        if not xp_state:
            return None
        if not xp_state["levels_gained"]:
            return {"level_up": False}
        new_level = xp_state["level"]
        return {
            "level_up": True,
            "new_level": new_level,
            "levels_gained": xp_state["levels_gained"],
            "pa_gained": xp_state["pa_gained"],
            "pp_gained": xp_state["pp_gained"],
            "xp_current": xp_state["xp"],
            "xp_next": None if new_level >= 100 else combat.xp_for_next_level(new_level),
        }

    def _equipment(player):
        """GAMEPLAY.md 32: arma/armadura activas resueltas a sus valores de
        catálogo (Issue #57). Sin arma equipada usa `combat.BASE_ARMA` (10),
        el mismo valor que ya usaban las fórmulas antes de que el equipo
        real existiera -- un personaje desarmado no cambia de golpe."""
        weapon_key, armor_key = store.equipped_item_keys(
            path, player["equipped_weapon_id"], player["equipped_armor_id"])
        weapon = items.get_item(weapon_key) if weapon_key else None
        armor = items.get_item(armor_key) if armor_key else None
        return {
            "weapon_base_damage": weapon["base_damage"] if weapon else combat.BASE_ARMA,
            "can_block": bool(weapon and weapon["can_block"]),
            "armor_reduction": armor["armor_reduction"] if armor else 0.0,
        }

    def resolve_inspect(player, target):
        """Devuelve (texto, mensaje_de_descubrimiento_o_None) si hay un
        texto canonico de NARRATIVE.md para ese objetivo en esta sala, o
        None si no hay nada especifico definido (el llamador decide el
        mensaje generico de respaldo).

        VT-PSY-004 (revision de Psicopedagogia en PR #49): ninguna senal
        aislada y ambigua debe bastar para que el sistema concluya mas de
        lo que esa senal realmente demuestra.
        - `tallos` y `monticulos` por separado solo describen "algo
          pequeno" comiendo/excavando -- ninguno nombra una especie. Solo
          al examinar AMBAS senales hay evidencia suficiente para que el
          personaje reconozca que son senales de Mordelinde.
        - `examinar cerca` por si sola solo demuestra violencia, no tamano;
          `examinar huellas` si compara tamano explicitamente contra las
          criaturas pequenas ya vistas cerca de Valdren, asi que basta por
          si misma para el descubrimiento mayor del lindero."""
        normalized = _normalize(target)
        if not normalized:
            return None
        text = world.get_examine_text(player["room"], normalized)
        if text is None:
            return None
        store.mark_examined_signal(path, player["id"], player["room"], normalized)
        discovery_key = None
        if player["room"] == "valdren_camino_parcela" and normalized in ("tallos", "monticulos"):
            if (store.has_examined_signal(path, player["id"], player["room"], "tallos")
                    and store.has_examined_signal(path, player["id"], player["room"], "monticulos")):
                discovery_key = "senales_mordelinde"
        elif player["room"] == "valdren_camino_lindero" and normalized == "huellas":
            discovery_key = "lindero_roto"
        awarded_message = None
        level_up_event = None
        if discovery_key:
            discovery = world.get_discovery(discovery_key)
            is_new, xp_amount, xp_state = store.award_discovery(
                path, player["id"], discovery_key, discovery["category"], discovery["reference_level"])
            if is_new:
                awarded_message = f"{discovery['message']} (+{xp_amount} XP)"
                level_message = _level_up_message(xp_state)
                if level_message:
                    awarded_message = f"{awarded_message} {level_message}"
                level_up_event = _level_up_event(xp_state)
        return text, awarded_message, level_up_event

    def attempt_evaluate(player):
        """GAMEPLAY.md 22.11 / §40.4: solo funciona sobre un objetivo visible (la
        criatura activa de la sala o una amenaza regional C3 en proximidad crítica)
        y nunca revela números."""
        boss = bosses.get_boss_by_arena(player["room"])
        if boss and not bosses.is_boss_defeated(path, boss.boss_id):
            attempt = store.get_boss_attempt(path, boss.boss_id)
            current_hp = attempt["current_hp"] if attempt else float(boss.max_hp)
            phase = bosses.determine_current_phase(boss, current_hp)
            attrs = _attributes(player)
            equipment = _equipment(player)
            player_dps = combat.expected_dps(attrs["destreza"], attrs["percepcion"], attrs["fuerza"],
                combat.competencia_general(player["level"]), combat.competencia_general(10),
                base_arma=equipment["weapon_base_damage"])
            enemy_dps = combat.fixed_expected_dps(phase.precision, phase.damage)
            category = combat.encounter_category(player_dps, player["hp_current"], enemy_dps, current_hp)
            return boss.name, f"{boss.name} {EVALUATE_TEXT[category]}."
        encounter = store.get_encounter(path, player["id"], player["room"])
        creature_id = None
        if encounter:
            creature_id = encounter["creature_id"]
        else:
            threat_eval = threats.get_room_threat_view(path, player["id"], player["room"])
            if threat_eval and threat_eval.close_encounter:
                creature_id = threat_eval.creature_id
        if not creature_id:
            return None, "No hay ninguna criatura visible para evaluar."
        creature = creatures.get_creature(creature_id)
        attrs = _attributes(player)
        equipment = _equipment(player)
        cg_player = combat.competencia_general(player["level"])
        cg_enemy = combat.competencia_general(creature["reference_level"])
        player_dps = combat.expected_dps(attrs["destreza"], attrs["percepcion"], attrs["fuerza"],
                                          cg_player, cg_enemy, base_arma=equipment["weapon_base_damage"])
        enemy_dps = combat.fixed_expected_dps(creature["precision"], creature["damage"])
        category = combat.encounter_category(player_dps, player["hp_current"], enemy_dps, creature["hp"])
        return creature["name"], f"{creature['name']} {EVALUATE_TEXT[category]}."

    def _defeat_result(creature, combat_messages, player, respawn_result):
        """Añade presentación estructurada a una derrota ya resuelta."""
        creature_family = creature.get("family", "")
        if creature_family in encounters.C3_THREAT_IDS:
            for tz in threats.get_all_threat_zones():
                if tz.creature_id == creature_family:
                    threats.resolve_threat_combat_end(path, player["id"], tz.threat_zone_id, "defeat")
        death_event = {
            "heading": DEATH_HEADING,
            "combat_messages": list(combat_messages),
            "defeat_message": f"{creature['name']} te derrota.",
            "fall_message": DEATH_FALL_MESSAGE,
            "respawn_message": f"Vuelves en ti en {respawn_result['room_name']}.",
            "post_respawn_state": {
                "hp_current": respawn_result["hp_current"],
                "hp_max": round(player["hp_max"]),
                "fatigue": respawn_result["fatigue"],
                "wound": respawn_result["wound"],
                "equipment": "Conservado",
                "inventory": "Conservado",
            },
            "preservation_message": "Conservas tu equipo e inventario.",
        }
        legacy_messages = list(combat_messages)
        legacy_messages.append(
            f"{creature['name']} te derrota. Vuelves en ti en {respawn_result['room_name']}."
        )
        return {"outcome": "defeat", "messages": legacy_messages, "death_event": death_event}

    def _resolve_standard_defeat(creature, combat_messages, player, current_wound):
        """Única ruta de muerte para combate C1/C2/C3 y capacidades firma."""
        store.clear_encounter(path, player["id"], player["room"])
        respawn_result = respawn_logic.apply_player_respawn(
            path,
            player,
            current_wound=current_wound,
            death_room_id=player["room"],
        )
        return _defeat_result(creature, combat_messages, player, respawn_result)

    def attempt_attack(player, rng=None):
        """Una ronda de combate real (golpe del jugador y, si la criatura
        sobrevive, contragolpe). Aplica fatiga/heridas segun GAMEPLAY.md 24
        (coste de fatiga del ataque, penalizaciones de fatiga/herida sobre
        el propio golpe, disparador de herida por el golpe recibido).
        Devuelve un dict con 'outcome'
        ('no_target'|'victory'|'ongoing'|'defeat') y 'messages'."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
            boss = bosses.get_boss_by_arena(player["room"])
            if boss and not bosses.is_boss_defeated(path, boss.boss_id):
                return bosses.resolve_boss_attack_round(path, player, boss, rng=rng)
            threat_eval = threats.get_room_threat_view(path, player["id"], player["room"])
            if threat_eval and threat_eval.close_encounter:
                creature_data = creatures.get_creature(threat_eval.creature_id)
                store.start_encounter(path, player["id"], player["room"], threat_eval.creature_id, creature_data["hp"])
                encounter = store.get_encounter(path, player["id"], player["room"])
            else:
                return {"outcome": "no_target", "messages": ["No hay ninguna criatura para atacar aquí."]}
        if not encounter.get("engaged", 1):
            store.update_encounter(path, player["id"], player["room"], engaged=True)
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        equipment = _equipment(player)
        cg_player = combat.competencia_general(player["level"])
        cg_enemy = combat.competencia_general(creature["reference_level"])

        wound = player["wound"]
        fatigue = min(100, player["fatigue"]
                      + combat.fatigue_gained("ataque_basico", attrs["resistencia"], wound,
                                               armor_reduction=equipment["armor_reduction"]))
        accuracy_penalty = combat.combined_accuracy_penalty(player["fatigue"], wound)
        damage_multiplier = combat.combined_damage_multiplier(player["fatigue"], wound)

        # GAMEPLAY.md 36.6: bono de Apertura (+15% precision en siguiente basico)
        apertura = encounter.get("apertura", 0)
        apertura_bonus = 15 if apertura > 0 else 0

        player_hits, player_damage = combat.resolve_attack_roll(
            attrs["destreza"], attrs["percepcion"], attrs["fuerza"], cg_player, cg_enemy, rng=rng,
            base_arma=equipment["weapon_base_damage"],
            accuracy_penalty=accuracy_penalty - apertura_bonus, damage_multiplier=damage_multiplier)
        messages = []
        if apertura_bonus > 0:
            messages.append("Aprovechas la apertura creada (+15% precisión).")
        if player_hits:
            player_damage = combat.apply_armor_reduction(player_damage, creature.get("armor_reduction", 0.0))
            messages.append(f"Golpeas a {creature['name']} por {round(player_damage)} de daño.")
        else:
            player_damage = 0.0
            messages.append(f"Fallas tu ataque contra {creature['name']}.")
        creature_hp = encounter["hp_current"] - player_damage

        if creature_hp <= 0:
            store.clear_encounter(path, player["id"], player["room"])
            store.start_creature_cooldown(path, player["id"], player["room"], encounter["creature_id"])
            if encounter["creature_id"] in encounters.C3_THREAT_IDS:
                for tz in threats.get_all_threat_zones():
                    if tz.creature_id == encounter["creature_id"]:
                        threats.resolve_threat_combat_end(path, player["id"], tz.threat_zone_id, "victory")
            is_first, repeats = store.record_pve_victory(path, player["id"], creature["family"])
            player_dps = combat.expected_dps(attrs["destreza"], attrs["percepcion"], attrs["fuerza"],
                                              cg_player, cg_enemy, base_arma=equipment["weapon_base_damage"])
            enemy_dps = combat.fixed_expected_dps(creature["precision"], creature["damage"])
            category = combat.encounter_category(player_dps, player["hp_current"], enemy_dps, creature["hp"])
            xp_amount = combat.combat_xp(creature["reference_level"], category, player["level"],
                                          is_first, repeats)
            xp_state = store.award_xp(path, player["id"], xp_amount)
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            messages.append(f"¡{creature['name']} cae derrotado! Ganas {xp_amount} XP.")
            if is_first:
                messages.append(f"Primera vez que superas a un {creature['name']}: bono de familia incluido.")
            level_message = _level_up_message(xp_state)
            if level_message:
                messages.append(level_message)
            return {"outcome": "victory", "messages": messages,
                    "level_up_event": _level_up_event(xp_state)}

        # Decremento de recarga de capacidad firma tras intervencion (36.2)
        cd = encounter.get("signature_cooldown", 0)
        new_cd = max(0, cd - 1) if cd > 0 else 0

        # Accion de respuesta enemiga: preparada o basica (36.3)
        prepared_action = encounter.get("prepared_action")
        if prepared_action:
            enemy_prec = prepared_action.get("precision", creature["precision"])
            enemy_dmg = prepared_action.get("damage", creature["damage"])
            prep_name = prepared_action.get("name")
        else:
            enemy_prec = creature["precision"]
            enemy_dmg = creature["damage"]
            prep_name = None

        store.update_encounter(path, player["id"], player["room"], hp_current=creature_hp,
                               signature_cooldown=new_cd, apertura=0, prepared_action=None)

        enemy_hits, enemy_damage = combat.resolve_fixed_attack_roll(
            enemy_prec, enemy_dmg, rng=rng)
        new_wound = wound
        if enemy_hits:
            enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
            if prep_name:
                messages.append(f"{creature['name']} ejecuta su {prep_name} y te golpea por {round(enemy_damage)} de daño.")
            else:
                messages.append(f"{creature['name']} te golpea por {round(enemy_damage)} de daño.")
            new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
            if new_wound != wound:
                messages.append(f"Sufres una herida {new_wound}.")
        else:
            if prep_name:
                messages.append(f"{creature['name']} falla su {prep_name}.")
            else:
                messages.append(f"{creature['name']} falla su ataque.")
        player_hp = player["hp_current"] - (enemy_damage if enemy_hits else 0)

        if player_hp <= 0:
            return _resolve_standard_defeat(creature, messages, player, new_wound)

        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "ongoing", "messages": messages}

    def attempt_flee(player, rng=None):
        """GAMEPLAY.md 20.10 y 24.3 (coste de fatiga del intento). Si tiene
        exito, retrocede por la salida que lleva de vuelta hacia Valdren; si
        falla, la criatura tiene una oportunidad de golpear."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
            boss = bosses.get_boss_by_arena(player["room"])
            if boss and not bosses.is_boss_defeated(path, boss.boss_id):
                return bosses.resolve_boss_player_flee(path, player, boss, rng=rng)
            return {"outcome": "no_target", "messages": ["No hay ninguna criatura de la que huir."]}
        creature = creatures.get_creature(encounter["creature_id"])
        room = world.get_room(player["room"])
        retreat_direction = "east" if "east" in room["exits"] else next(iter(room["exits"]), None)
        wound = player["wound"]
        equipment = _equipment(player)
        fatigue = min(100, player["fatigue"] + combat.fatigue_gained(
            "huir", player["attr_resistencia"], wound, armor_reduction=equipment["armor_reduction"]))
        chance = combat.flee_chance(
            player["attr_agilidad"], player["attr_percepcion"],
            creature["flee_agilidad"], creature["flee_percepcion"],
            attacker_level_advantage=creature["reference_level"] - player["level"],
            previous_failed_attempts=encounter["failed_flee_attempts"],
            fatigue=player["fatigue"],
        )
        rng = rng or random.Random()
        if rng.uniform(0, 100) < chance:
            store.clear_encounter(path, player["id"], player["room"])
            if encounter["creature_id"] in encounters.C3_THREAT_IDS:
                for tz in threats.get_all_threat_zones():
                    if tz.creature_id == encounter["creature_id"]:
                        threats.resolve_threat_combat_end(path, player["id"], tz.threat_zone_id, "flee")
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            messages = [f"Consigues alejarte de {creature['name']}."]
            if retreat_direction:
                attempt_move(player, retreat_direction)
            return {"outcome": "success", "messages": messages}

        cd = encounter.get("signature_cooldown", 0)
        new_cd = max(0, cd - 1) if cd > 0 else 0
        prepared_action = encounter.get("prepared_action")
        if prepared_action:
            enemy_prec = prepared_action.get("precision", creature["precision"])
            enemy_dmg = prepared_action.get("damage", creature["damage"])
            prep_name = prepared_action.get("name")
        else:
            enemy_prec = creature["precision"]
            enemy_dmg = creature["damage"]
            prep_name = None

        store.update_encounter(path, player["id"], player["room"],
                                failed_flee_attempts=encounter["failed_flee_attempts"] + 1,
                                engaged=True, signature_cooldown=new_cd, prepared_action=None)
        enemy_hits, enemy_damage = combat.resolve_fixed_attack_roll(
            enemy_prec, enemy_dmg, rng=rng)
        messages = [f"No logras huir de {creature['name']}."]
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            return {"outcome": "failed", "messages": messages}
        enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
        if prep_name:
            messages.append(f"{creature['name']} te alcanza con su {prep_name} por {round(enemy_damage)} de daño mientras intentas escapar.")
        else:
            messages.append(f"{creature['name']} te golpea por {round(enemy_damage)} de daño mientras intentas escapar.")
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
        player_hp = player["hp_current"] - enemy_damage
        if player_hp <= 0:
            return _resolve_standard_defeat(creature, messages, player, new_wound)
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_avoid(player):
        """GAMEPLAY.md §40.4/§40.6: decisión explícita de evitar/retroceder ante una
        amenaza regional en proximidad crítica ('close'). Resuelve el encuentro sin
        combate y activa enfriamiento de 30 minutos reales."""
        active_zone = None
        for z in threats.get_threat_zones_for_room(player["room"]):
            if player["room"] in z.encounter_rooms:
                rec = store.get_threat_state(path, player["id"], z.threat_zone_id)
                if rec and rec["state"] == "close":
                    active_zone = z
                    break
        if not active_zone:
            return {"outcome": "no_target", "messages": ["No hay ninguna amenaza que evitar aquí."]}
        threats.resolve_threat_avoid(path, player["id"], active_zone.threat_zone_id)
        creature = creatures.get_creature(active_zone.creature_id)
        room = world.get_room(player["room"])
        retreat_direction = None
        for dir_cand, dest_cand in room.get("exits", {}).items():
            if dest_cand in active_zone.warning_rooms:
                retreat_direction = dir_cand
                break
        if not retreat_direction:
            retreat_direction = "south" if "south" in room.get("exits", {}) else next(iter(room.get("exits", {})), None)
        messages = [f"Decides retroceder con cautela. Te alejas sin provocar a {creature['name']}."]
        if retreat_direction:
            attempt_move(player, retreat_direction)
        return {"outcome": "avoided", "messages": messages}

    def attempt_dodge(player, rng=None):
        """GAMEPLAY.md 20.5/24.2/24.3: sustituye el ataque básico del
        jugador por un intento de esquivar el golpe entrante de la
        criatura. Reduce la probabilidad de que ese golpe conecte; si
        conecta igual, el daño es el normal (esquivar no reduce daño)."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter or not encounter.get("engaged", 1):
            boss = bosses.get_boss_by_arena(player["room"])
            if boss and not bosses.is_boss_defeated(path, boss.boss_id):
                return bosses.resolve_boss_dodge_round(path, player, boss, rng=rng)
            return {"outcome": "no_target", "messages": ["No hay ningún ataque que esquivar aquí."]}
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        equipment = _equipment(player)
        wound = player["wound"]
        fatigue = min(100, player["fatigue"] + combat.fatigue_gained(
            "esquivar", attrs["resistencia"], wound, armor_reduction=equipment["armor_reduction"]))
        accuracy_penalty = combat.combined_accuracy_penalty(player["fatigue"], wound)
        rng = rng or random.Random()

        cd = encounter.get("signature_cooldown", 0)
        new_cd = max(0, cd - 1) if cd > 0 else 0
        prepared_action = encounter.get("prepared_action")
        prep_name = prepared_action.get("name") if prepared_action else None
        enemy_prec = prepared_action.get("precision", creature["precision"]) if prepared_action else creature["precision"]
        enemy_dmg = prepared_action.get("damage", creature["damage"]) if prepared_action else creature["damage"]

        store.update_encounter(path, player["id"], player["room"],
                               signature_cooldown=new_cd, prepared_action=None)

        enemy_hits, enemy_damage = combat.resolve_dodged_attack_roll(
            enemy_prec, enemy_dmg, attrs["agilidad"], attrs["percepcion"],
            accuracy_penalty=accuracy_penalty, rng=rng)
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            if prep_name:
                return {"outcome": "success", "messages": [f"Esquivas la {prep_name} de {creature['name']}."]}
            return {"outcome": "success", "messages": [f"Esquivas el ataque de {creature['name']}."]}
        enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
        if prep_name:
            messages = [f"No logras esquivar y {creature['name']} te golpea con su {prep_name} por {round(enemy_damage)} de daño."]
        else:
            messages = [f"No logras esquivar y {creature['name']} te golpea por {round(enemy_damage)} de daño."]
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
        player_hp = player["hp_current"] - enemy_damage
        if player_hp <= 0:
            return _resolve_standard_defeat(creature, messages, player, new_wound)
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_resist(player, rng=None):
        """GAMEPLAY.md 20.5/24.2/24.3: sustituye el ataque básico por
        resistir el golpe entrante. No cambia la probabilidad de ser
        golpeado; si el golpe conecta, reduce su daño según Resistencia."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter or not encounter.get("engaged", 1):
            boss = bosses.get_boss_by_arena(player["room"])
            if boss and not bosses.is_boss_defeated(path, boss.boss_id):
                return bosses.resolve_boss_resist_round(path, player, boss, rng=rng)
            return {"outcome": "no_target", "messages": ["No hay ningún golpe que resistir aquí."]}
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        equipment = _equipment(player)
        wound = player["wound"]
        fatigue = min(100, player["fatigue"] + combat.fatigue_gained(
            "resistir", attrs["resistencia"], wound, armor_reduction=equipment["armor_reduction"]))
        rng = rng or random.Random()

        cd = encounter.get("signature_cooldown", 0)
        new_cd = max(0, cd - 1) if cd > 0 else 0
        prepared_action = encounter.get("prepared_action")
        prep_name = prepared_action.get("name") if prepared_action else None
        enemy_prec = prepared_action.get("precision", creature["precision"]) if prepared_action else creature["precision"]
        enemy_dmg = prepared_action.get("damage", creature["damage"]) if prepared_action else creature["damage"]

        store.update_encounter(path, player["id"], player["room"],
                               signature_cooldown=new_cd, prepared_action=None)

        enemy_hits, enemy_damage = combat.resolve_resisted_attack_roll(
            enemy_prec, enemy_dmg, attrs["resistencia"], rng=rng)
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            if prep_name:
                return {"outcome": "success", "messages": [f"Te preparas y {creature['name']} falla su {prep_name}."]}
            return {"outcome": "success", "messages": [f"Te preparas y {creature['name']} falla su ataque."]}
        enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
        if prep_name:
            messages = [f"Resistes la {prep_name} de {creature['name']}, que aun así te hace "
                        f"{round(enemy_damage)} de daño."]
        else:
            messages = [f"Resistes el golpe de {creature['name']}, que aun así te hace "
                        f"{round(enemy_damage)} de daño."]
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
        player_hp = player["hp_current"] - enemy_damage
        if player_hp <= 0:
            return _resolve_standard_defeat(creature, messages, player, new_wound)
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_block(player, rng=None):
        """GAMEPLAY.md 20.5: requiere arma/escudo/objeto adecuado -- ver
        `_can_block`, que desde el Issue #57 consulta el arma equipada
        real."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter or not encounter.get("engaged", 1):
            boss = bosses.get_boss_by_arena(player["room"])
            if boss and not bosses.is_boss_defeated(path, boss.boss_id):
                return bosses.resolve_boss_block_round(path, player, boss, rng=rng)
            return {"outcome": "no_target", "messages": ["No hay ningún golpe que bloquear aquí."]}
        if not _can_block(path, player["id"]):
            return {"outcome": "unavailable",
                    "messages": ["Todavía no tienes equipo adecuado para bloquear."]}
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        equipment = _equipment(player)
        wound = player["wound"]
        fatigue = min(100, player["fatigue"] + combat.fatigue_gained(
            "bloquear", attrs["resistencia"], wound, armor_reduction=equipment["armor_reduction"]))
        rng = rng or random.Random()

        cd = encounter.get("signature_cooldown", 0)
        new_cd = max(0, cd - 1) if cd > 0 else 0
        prepared_action = encounter.get("prepared_action")
        prep_name = prepared_action.get("name") if prepared_action else None
        enemy_prec = prepared_action.get("precision", creature["precision"]) if prepared_action else creature["precision"]
        enemy_dmg = prepared_action.get("damage", creature["damage"]) if prepared_action else creature["damage"]

        store.update_encounter(path, player["id"], player["room"],
                               signature_cooldown=new_cd, prepared_action=None)

        enemy_hits, enemy_damage = combat.resolve_blocked_attack_roll(
            enemy_prec, enemy_dmg, attrs["destreza"], rng=rng)
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            if prep_name:
                return {"outcome": "success", "messages": [f"Bloqueas la {prep_name} de {creature['name']}."]}
            return {"outcome": "success", "messages": [f"Bloqueas el ataque de {creature['name']}."]}
        enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
        if prep_name:
            messages = [f"Bloqueas parcialmente la {prep_name} de {creature['name']}, que aun así te hace "
                        f"{round(enemy_damage)} de daño."]
        else:
            messages = [f"Bloqueas parcialmente a {creature['name']}, que aun así te hace "
                        f"{round(enemy_damage)} de daño."]
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
        player_hp = player["hp_current"] - enemy_damage
        if player_hp <= 0:
            return _resolve_standard_defeat(creature, messages, player, new_wound)
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_signature_ability(player, rng=None):
        """GAMEPLAY.md 36: Uso de la capacidad firma de la clase del personaje.
        Sustituye el ataque básico, genera 5 de fatiga base, entra en recarga
        y resuelve la interacción táctica."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
            return {"outcome": "no_target", "messages": ["No hay ninguna criatura contra la que usar tu capacidad aquí."]}
        authorized, reason, ability = _can_use_signature_ability(path, player, encounter)
        if not authorized:
            return {"outcome": "unavailable", "messages": [reason]}

        player_class = player["player_class"]
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        equipment = _equipment(player)
        wound = player["wound"]

        # 36.2: genera 5 puntos base de fatiga
        fatigue = min(100, player["fatigue"] + combat.fatigue_gained(
            "capacidad_firma", attrs["resistencia"], wound, armor_reduction=equipment["armor_reduction"]))

        messages = []
        prepared_action = encounter.get("prepared_action")
        cooldown_rounds = ability["cooldown"]

        if player_class == "juramentado":
            # 36.4: Guardia Comprometida
            is_frontal = bool(prepared_action and prepared_action.get("frontal"))
            creature_base_prec = creature["precision"]
            enemy_prec = prepared_action.get("precision", creature["precision"]) if prepared_action else creature["precision"]
            enemy_dmg = prepared_action.get("damage", creature["damage"]) if prepared_action else creature["damage"]
            prep_name = prepared_action.get("name") if prepared_action else None

            enemy_hits, enemy_damage = combat.resolve_guardia_comprometida_attack_roll(
                enemy_prec, enemy_dmg, attrs["destreza"], attrs["resistencia"],
                is_frontal_charge=is_frontal, creature_base_precision=creature_base_prec, rng=rng)

            store.update_encounter(path, player["id"], player["room"],
                                   signature_cooldown=cooldown_rounds, prepared_action=None)

            if not enemy_hits:
                store.update_combat_state(path, player["id"], fatigue=round(fatigue))
                if prep_name:
                    messages.append(f"Mantienes una Guardia Comprometida firme: {creature['name']} se estrella contra tu defensa con su {prep_name} sin lograr dañarte.")
                else:
                    messages.append(f"Mantienes una Guardia Comprometida y {creature['name']} no logra conectar su ataque.")
                return {"outcome": "success", "messages": messages}

            enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
            red_pct = round(combat.guardia_reduction(attrs["destreza"], attrs["resistencia"]) * 100)
            if prep_name:
                messages.append(f"Sostienes tu Guardia Comprometida ante la {prep_name} de {creature['name']}: reduces el impacto (-{red_pct}%) y recibes {round(enemy_damage)} de daño.")
            else:
                messages.append(f"Sostienes tu Guardia Comprometida: mitigas el ataque de {creature['name']} (-{red_pct}%) y recibes {round(enemy_damage)} de daño.")

            new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
            if new_wound != wound:
                messages.append(f"Sufres una herida {new_wound}.")
            player_hp = player["hp_current"] - enemy_damage
            if player_hp <= 0:
                return _resolve_standard_defeat(creature, messages, player, new_wound)
            store.update_combat_state(path, player["id"], hp_current=player_hp,
                                       fatigue=round(fatigue), wound=new_wound)
            return {"outcome": "ongoing", "messages": messages}

        elif player_class == "arcano":
            # 36.5: Impulso Arcano
            imp_result = combat.resolve_impulso_arcano_effect(prepared_action)
            prep_name = prepared_action.get("name") if prepared_action else None
            if imp_result["interrupted"]:
                messages.append(f"Liberas un Impulso Arcano que desbarata la {prep_name} de {creature['name']}.")
            else:
                messages.append(f"Canalizas un Impulso Arcano que desestabiliza a {creature['name']} (-20% precisión).")

            store.update_encounter(path, player["id"], player["room"],
                                   signature_cooldown=cooldown_rounds, prepared_action=None)

            effective_precision = max(20, creature["precision"] - imp_result["enemy_accuracy_penalty"])
            enemy_hits, enemy_damage = combat.resolve_fixed_attack_roll(
                effective_precision, creature["damage"], rng=rng)

            if not enemy_hits:
                store.update_combat_state(path, player["id"], fatigue=round(fatigue))
                messages.append(f"{creature['name']} falla su ataque desestabilizado.")
                return {"outcome": "success", "messages": messages}

            enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
            messages.append(f"{creature['name']} ataca de forma descompuesta pero te alcanza por {round(enemy_damage)} de daño.")
            new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
            if new_wound != wound:
                messages.append(f"Sufres una herida {new_wound}.")
            player_hp = player["hp_current"] - enemy_damage
            if player_hp <= 0:
                return _resolve_standard_defeat(creature, messages, player, new_wound)
            store.update_combat_state(path, player["id"], hp_current=player_hp,
                                       fatigue=round(fatigue), wound=new_wound)
            return {"outcome": "ongoing", "messages": messages}

        elif player_class == "sombra":
            # 36.6: Borrar el Foco
            foco_result = combat.resolve_borrar_el_foco_effect()
            penalty = foco_result["enemy_accuracy_penalty"]
            prep_name = prepared_action.get("name") if prepared_action else None
            if prepared_action:
                base_prec = prepared_action.get("precision", creature["precision"])
                base_dmg = prepared_action.get("damage", creature["damage"])
            else:
                base_prec = creature["precision"]
                base_dmg = creature["damage"]

            effective_precision = max(20, base_prec - penalty)
            enemy_hits, enemy_damage = combat.resolve_fixed_attack_roll(
                effective_precision, base_dmg, rng=rng)

            if not enemy_hits:
                store.update_encounter(path, player["id"], player["room"],
                                       signature_cooldown=cooldown_rounds, apertura=1, prepared_action=None)
                store.update_combat_state(path, player["id"], fatigue=round(fatigue))
                if prep_name:
                    messages.append(f"Borras el foco: {creature['name']} pierde tu posición y su {prep_name} golpea el aire. ¡Ganas Apertura (+15% precisión en tu próximo ataque)!")
                else:
                    messages.append(f"Borras el foco: {creature['name']} pierde tu posición y ataca al vacío. ¡Ganas Apertura (+15% precisión en tu próximo ataque)!")
                return {"outcome": "success", "messages": messages}

            store.update_encounter(path, player["id"], player["room"],
                                   signature_cooldown=cooldown_rounds, apertura=0, prepared_action=None)
            enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
            messages.append(f"Rompes la línea de atención, pero {creature['name']} logra alcanzarte por {round(enemy_damage)} de daño.")
            new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
            if new_wound != wound:
                messages.append(f"Sufres una herida {new_wound}.")
            player_hp = player["hp_current"] - enemy_damage
            if player_hp <= 0:
                return _resolve_standard_defeat(creature, messages, player, new_wound)
            store.update_combat_state(path, player["id"], hp_current=player_hp,
                                       fatigue=round(fatigue), wound=new_wound)
            return {"outcome": "ongoing", "messages": messages}

        elif player_class == "artifice":
            # 36.7: Tiro de Interrupción
            cg_player = combat.competencia_general(player["level"])
            cg_enemy = combat.competencia_general(creature["reference_level"])
            accuracy_penalty = combat.combined_accuracy_penalty(player["fatigue"], wound)
            damage_multiplier = combat.combined_damage_multiplier(player["fatigue"], wound)
            apertura = encounter.get("apertura", 0)
            apertura_bonus = 15 if apertura > 0 else 0

            player_hits, player_damage, shot_effect = combat.resolve_tiro_de_interrupcion_attack_roll(
                attrs["destreza"], attrs["percepcion"], attrs["fuerza"],
                cg_player, cg_enemy, base_arma=equipment["weapon_base_damage"],
                accuracy_penalty=accuracy_penalty, damage_multiplier=damage_multiplier,
                apertura_bonus=apertura_bonus, prepared_action=prepared_action, rng=rng)

            if apertura > 0:
                store.update_encounter(path, player["id"], player["room"], apertura=0)

            if player_hits:
                player_damage = combat.apply_armor_reduction(player_damage, creature.get("armor_reduction", 0.0))
                messages.append(f"Disparas un Tiro de Interrupción certero e impactas a {creature['name']} por {round(player_damage)} de daño.")
                creature_hp = encounter["hp_current"] - player_damage
                if creature_hp <= 0:
                    store.clear_encounter(path, player["id"], player["room"])
                    store.start_creature_cooldown(path, player["id"], player["room"], encounter["creature_id"])
                    is_first, repeats = store.record_pve_victory(path, player["id"], creature["family"])
                    player_dps = combat.expected_dps(attrs["destreza"], attrs["percepcion"], attrs["fuerza"],
                                                      cg_player, cg_enemy, base_arma=equipment["weapon_base_damage"])
                    enemy_dps = combat.fixed_expected_dps(creature["precision"], creature["damage"])
                    category = combat.encounter_category(player_dps, player["hp_current"], enemy_dps, creature["hp"])
                    xp_amount = combat.combat_xp(creature["reference_level"], category, player["level"],
                                                  is_first, repeats)
                    xp_state = store.award_xp(path, player["id"], xp_amount)
                    store.update_combat_state(path, player["id"], fatigue=round(fatigue))
                    messages.append(f"¡{creature['name']} cae derrotado! Ganas {xp_amount} XP.")
                    if is_first:
                        messages.append(f"Primera vez que superas a un {creature['name']}: bono de familia incluido.")
                    level_message = _level_up_message(xp_state)
                    if level_message:
                        messages.append(level_message)
                    return {"outcome": "victory", "messages": messages}

                store.update_encounter(path, player["id"], player["room"],
                                       hp_current=creature_hp, signature_cooldown=cooldown_rounds,
                                       prepared_action=None)

                if shot_effect["interrupted"]:
                    prep_name = prepared_action.get("name", "acción especial")
                    messages.append(f"El impacto desbarata la {prep_name} de {creature['name']}, forzando un ataque básico ordinario.")
                    enemy_prec = creature["precision"]
                    enemy_dmg = creature["damage"]
                else:
                    messages.append(f"El impacto descompone el avance de {creature['name']} (-15% precisión).")
                    enemy_prec = max(20, creature["precision"] - shot_effect["enemy_accuracy_penalty"])
                    enemy_dmg = creature["damage"]
            else:
                messages.append(f"Tu Tiro de Interrupción falla contra {creature['name']}.")
                store.update_encounter(path, player["id"], player["room"],
                                       signature_cooldown=cooldown_rounds, prepared_action=None)
                if prepared_action:
                    enemy_prec = prepared_action.get("precision", creature["precision"])
                    enemy_dmg = prepared_action.get("damage", creature["damage"])
                else:
                    enemy_prec = creature["precision"]
                    enemy_dmg = creature["damage"]

            # Enemy counter-attack
            enemy_hits, enemy_damage = combat.resolve_fixed_attack_roll(
                enemy_prec, enemy_dmg, rng=rng)
            if not enemy_hits:
                store.update_combat_state(path, player["id"], fatigue=round(fatigue))
                messages.append(f"{creature['name']} falla su ataque.")
                return {"outcome": "ongoing", "messages": messages}

            enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
            messages.append(f"{creature['name']} te golpea por {round(enemy_damage)} de daño.")
            new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
            if new_wound != wound:
                messages.append(f"Sufres una herida {new_wound}.")
            player_hp = player["hp_current"] - enemy_damage
            if player_hp <= 0:
                return _resolve_standard_defeat(creature, messages, player, new_wound)
            store.update_combat_state(path, player["id"], hp_current=player_hp,
                                       fatigue=round(fatigue), wound=new_wound)
            return {"outcome": "ongoing", "messages": messages}

        return {"outcome": "unavailable", "messages": ["Capacidad no implementada."]}

    # Relato de la pelea (petición de Javier, 2026-09-25): cada acción de
    # combate que ocurre con una criatura presente deja su línea en el
    # historial del encuentro, sin importar si llegó por botón, comando o API.
    # Si la acción terminó el encuentro, store.clear_encounter ya borró el
    # historial y no se agrega nada.
    def _record_combat(action, fn):
        def wrapper(player, *args, **kwargs):
            room_id = player["room"]
            result = fn(player, *args, **kwargs)
            if (room_id and result.get("outcome") not in ("no_target", "unavailable")
                    and store.get_encounter(path, player["id"], room_id)):
                store.append_combat_log(path, player["id"], room_id, action, " ".join(result["messages"]))
            return result
        return wrapper

    attempt_attack = _record_combat("atacar", attempt_attack)
    attempt_flee = _record_combat("huir", attempt_flee)
    attempt_dodge = _record_combat("esquivar", attempt_dodge)
    attempt_resist = _record_combat("resistir", attempt_resist)
    attempt_block = _record_combat("bloquear", attempt_block)
    attempt_signature_ability = _record_combat("capacidad", attempt_signature_ability)

    _attempt_evaluate_raw = attempt_evaluate

    def attempt_evaluate(player):
        name, message = _attempt_evaluate_raw(player)
        if player["room"] and store.get_encounter(path, player["id"], player["room"]):
            store.append_combat_log(path, player["id"], player["room"], "evaluar", message)
        return name, message

    def attempt_rest(player):
        """GAMEPLAY.md 24.8-24.9 / REST-01: descanso gratuito limitado.

        Un lugar seguro permite descansar sin peligro, pero no concede por sí
        solo una recuperación completa gratuita. El presupuesto autoritativo
        vive en SQLite y se consume atómicamente en store.apply_field_rest().
        """
        boss = bosses.get_boss_by_arena(player["room"])
        if boss and not bosses.is_boss_defeated(path, boss.boss_id):
            return {"outcome": "blocked", "messages": ["No puedes descansar ante la presencia de un jefe."]}
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes descansar con una criatura cerca."]}
        threat_eval = threats.get_room_threat_view(path, player["id"], player["room"])
        if threat_eval and threat_eval.close_encounter:
            return {"outcome": "blocked", "messages": ["No puedes descansar frente a una amenaza regional."]}
        result = store.apply_field_rest(path, player["id"])
        if result is None:
            return {"outcome": "blocked", "messages": ["No se pudo recuperar el estado del personaje."]}
        if result.get("blocked") == "budget_exhausted":
            return {
                "outcome": "blocked",
                "messages": [
                    "No puedes descansar: agotaste la recuperación de campo disponible. "
                    "Necesitas provisiones o una recuperación completa legítima."
                ],
            }

        healed = result["healed"]
        remaining = result["budget_remaining"]
        hp_now = result["hp_current"]
        fatigue_now = result["fatigue"]
        if healed > 0:
            message = (f"Descansas y recuperas {round(healed)} HP. "
                       f"Recuperación de campo restante: {round(remaining)} HP.")
        elif hp_now >= player["hp_max"]:
            message = "Tu vida ya está al máximo. El descanso todavía puede reducir fatiga."
        elif remaining <= 0:
            message = ("Descansas y recuperas fuerzas, pero el descanso de campo ya no puede "
                       "restaurar más vida. Necesitas provisiones o una recuperación completa legítima.")
        else:
            message = "Descansas y recuperas fuerzas. Tu herida limita la recuperación de vida."

        unchanged = (healed <= 0 and round(fatigue_now) == round(player["fatigue"]))
        return {"outcome": "no_op" if unchanged else "rested", "messages": [message]}

    def attempt_equip(player, target_text):
        """GAMEPLAY.md 32.3: `equipar <objeto>`. Solo fuera de combate,
        requiere poseer el objeto y, si el catálogo lo exige, tener la
        validación de Forja completa (32.4)."""
        boss = bosses.get_boss_by_arena(player["room"])
        if boss and not bosses.is_boss_defeated(path, boss.boss_id):
            return {"outcome": "blocked", "messages": ["No puedes equipar nada ante la presencia de un jefe."]}
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes equipar nada con una criatura cerca."]}
        threat_eval = threats.get_room_threat_view(path, player["id"], player["room"])
        if threat_eval and threat_eval.close_encounter:
            return {"outcome": "blocked", "messages": ["No puedes equipar nada frente a una amenaza regional."]}
        item_key = items.find_key_by_name(target_text)
        if item_key is None:
            return {"outcome": "not_found", "messages": ["No reconoces ese objeto."]}
        owned = next((row for row in store.list_inventory(path, player["id"]) if row["item_key"] == item_key), None)
        if owned is None:
            return {"outcome": "not_owned", "messages": ["No posees ese objeto."]}
        ok, _category, reason = store.equip_item(path, player["id"], owned["id"])
        if not ok:
            return {"outcome": "rejected", "messages": [reason]}
        return {"outcome": "equipped", "messages": [f"Equipas {items.get_item(item_key)['name']}."]}

    def attempt_unequip(player, target_text):
        """GAMEPLAY.md 32.3: desequipar solo fuera de combate; el objeto
        sigue en el inventario pero deja de aportar sus efectos."""
        boss = bosses.get_boss_by_arena(player["room"])
        if boss and not bosses.is_boss_defeated(path, boss.boss_id):
            return {"outcome": "blocked", "messages": ["No puedes desequipar nada ante la presencia de un jefe."]}
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes desequipar nada con una criatura cerca."]}
        threat_eval = threats.get_room_threat_view(path, player["id"], player["room"])
        if threat_eval and threat_eval.close_encounter:
            return {"outcome": "blocked", "messages": ["No puedes desequipar nada frente a una amenaza regional."]}
        item_key = items.find_key_by_name(target_text)
        if item_key is None:
            return {"outcome": "not_found", "messages": ["No reconoces ese objeto."]}
        category = items.category_of(item_key)
        weapon_key, armor_key = store.equipped_item_keys(
            path, player["equipped_weapon_id"], player["equipped_armor_id"])
        equipped_key = weapon_key if category == "weapon" else armor_key
        if equipped_key != item_key:
            return {"outcome": "not_equipped", "messages": ["No tienes eso equipado."]}
        store.unequip_item(path, player["id"], category)
        return {"outcome": "unequipped", "messages": [f"Guardas {items.get_item(item_key)['name']}."]}

    def attempt_buy(player, target_text):
        """Compra autoritativa en el comercio disponible de la sala actual."""
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes comerciar durante un encuentro."]}

        recovery_target = recovery.resolve_recovery_target(target_text)
        if player["room"] == recovery.RECOVERY_ROOM and recovery_target == recovery.RATION_ITEM_ID:
            ok, message, extra = recovery.buy_ration(
                path, player["id"], player["room"]
            )
            return {
                "outcome": "bought" if ok else "rejected",
                "messages": [message],
                "item_key": recovery.RATION_ITEM_ID if ok else None,
                "balance": extra.get("balance") if extra else None,
            }
        if player["room"] == recovery.RECOVERY_ROOM and recovery_target == recovery.SERVICE_ID:
            return {
                "outcome": "rejected",
                "messages": ["La comida caliente se consume en el mercado; usa «usar Comida caliente del mercado»."],
            }

        if player["room"] != economy.DARO_SHOP_ROOM:
            return {"outcome": "blocked", "messages": ["Aquí no puedes comprar ese objeto."]}
        if not target_text:
            return {
                "outcome": "rejected",
                "messages": [
                    "¿Qué deseas comprar? Daro vende: Varita de aprendiz (40 sellos), "
                    "Puñal de camino (50 sellos), Arco de ruta (65 sellos), "
                    "Espada de juramento (85 sellos)."
                ],
            }
        item_key = economy.resolve_daro_item(target_text)
        if not item_key:
            return {"outcome": "not_found", "messages": ["Daro no vende ese objeto en su taller."]}

        ok, message, extra = economy.buy_item_from_daro(path, player["id"], item_key)
        if not ok:
            return {"outcome": "rejected", "messages": [message], "balance": extra.get("balance") if extra else None}
        return {"outcome": "bought", "messages": [message], "item_key": item_key, "balance": extra["balance"]}

    def attempt_use_recovery(player, target_text):
        """Usa consumible/servicio de recuperación sin inferir efectos en cliente."""
        target = recovery.resolve_recovery_target(target_text)
        if target == recovery.RATION_ITEM_ID:
            owned = next(
                (row for row in store.list_inventory(path, player["id"])
                 if row["item_key"] == recovery.RATION_ITEM_ID),
                None,
            )
            if owned is None:
                return {"outcome": "not_owned", "messages": ["No posees una Ración de camino de Valdren."]}
            ok, message, extra = recovery.use_ration(path, player["id"], owned["id"])
            return {"outcome": "used" if ok else "rejected", "messages": [message], "effect": extra}
        if target == recovery.SERVICE_ID:
            ok, message, extra = recovery.use_market_service(
                path, player["id"], player["room"]
            )
            return {
                "outcome": "used" if ok else "rejected",
                "messages": [message],
                "effect": extra,
                "balance": extra.get("balance") if extra else None,
            }
        return {"outcome": "not_found", "messages": ["No reconoces esa recuperación."]}

    def attempt_sell(player, target_text):
        """ECONOMY-CORE-01 (#408 / ECONOMY.md §§8, 9, 20): reventa atómica al 35% a Daro.
        Solo fuera de combate y físicamente en el taller de Daro (valdren_forja).
        Rechaza vender objetos equipados o la última arma utilizable."""
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes comerciar durante un encuentro."]}
        if player["room"] != economy.DARO_SHOP_ROOM:
            return {"outcome": "blocked", "messages": ["Solo puedes comerciar con Daro en su taller de Valdren (valdren_forja)."]}
        if not target_text:
            return {
                "outcome": "rejected",
                "messages": [
                    "¿Qué deseas vender? Daro compra armas comunes de su catálogo al 35% de su valor: "
                    "Varita (14 sellos), Puñal (17 sellos), Arco (22 sellos), Espada (29 sellos)."
                ],
            }

        item_key = economy.resolve_daro_item(target_text) or items.find_key_by_name(target_text)
        if not item_key:
            return {"outcome": "not_found", "messages": ["No reconoces ese objeto."]}

        if item_key not in economy.DARO_BUYBACK:
            return {"outcome": "rejected", "messages": ["Daro no compra este tipo de objeto."]}

        inv = store.list_inventory(path, player["id"])
        matches = [it for it in inv if it["item_key"] == item_key]
        if not matches:
            return {"outcome": "not_owned", "messages": ["No posees ese objeto en tu inventario."]}

        unequipped = [it for it in matches if it["id"] not in (player["equipped_weapon_id"], player["equipped_armor_id"])]
        if not unequipped:
            return {"outcome": "equipped", "messages": ["No puedes vender un objeto que tienes equipado. Desequípalo primero."]}

        instance_to_sell = unequipped[0]
        ok, message, extra = economy.sell_item_to_daro(path, player["id"], instance_to_sell["id"])
        if not ok:
            return {"outcome": "rejected", "messages": [message], "balance": extra.get("balance") if extra else None}
        return {"outcome": "sold", "messages": [message], "item_key": item_key, "balance": extra["balance"]}

    def attempt_choose_species(player, species_id):
        """Devuelve (accepted, species_or_None, room_or_None, reason_or_None).
        La atomicidad real la garantiza store.set_species (rowcount), no una
        lectura previa de player["species"]: asi dos POST casi simultaneos no
        pueden terminar ambos con accepted=True."""
        if species_id not in world.SPECIES_IDS:
            return False, None, None, "Elige una especie de la lista."
        # VT-SERVER: HOME-CORE (Issue #280 / GAMEPLAY.md §34)
        # El personaje nuevo comienza en su hogar personal persistente.
        room_id = world.get_home_room_id(player["id"])
        updated = store.set_species(path, player["id"], species_id, room_id)
        if not updated:
            return False, None, None, "Ya elegiste tu especie."
        # El mapa progresivo debe reflejar lo que el personaje realmente ha
        # pisado. Al completar especie ya está físicamente en su hogar; el
        # pueblo se marca después, cuando attempt_move() acepta hogar→pueblo.
        store.mark_visited(path, player["id"], room_id)
        return True, species_id, room_id, None

    def attempt_choose_class(player, class_id):
        """Devuelve (accepted, class_or_None, reason_or_None). Mismo patron
        que attempt_choose_species: la atomicidad la da store.set_player_class."""
        if player["species"] is None:
            return False, None, "Primero elige tu especie."
        if class_id not in world.CLASS_IDS:
            return False, None, "Elige una clase de la lista."
        updated = store.set_player_class(path, player["id"], class_id,
                                         items.STARTER_WEAPON_BY_CLASS.get(class_id))
        if not updated:
            return False, None, "Ya elegiste tu clase."
        return True, class_id, None

    def api_player_state(player):
        """Errores JSON estables para rutas /api/*: unauthenticated /
        not_approved. Devuelve None si puede continuar."""
        if player is None:
            return jsonify(error="unauthenticated"), 401
        if player["status"] != "approved":
            return jsonify(error="not_approved", status=player["status"]), 403
        return None

    def valid_character_name(name):
        return (1 <= len(name) <= 60 and not any(ord(c) < 32 for c in name)
                and store.name_key(name) != "")

    def character_list_page(error=None, status=200, new_name=""):
        characters = store.list_characters(path, g.account["id"])
        return render_template("entry.html", player=None, characters=characters,
                               max_characters=store.MAX_CHARACTERS_PER_ACCOUNT,
                               new_name=new_name, error=error), status

    def guest_page(error, status, view, values=None):
        """Formulario de entrada con el error y los datos que el jugador ya
        escribió (nunca la contraseña), en la misma vista donde estaba."""
        return render_template("entry.html", error=error, onboarding_view=view, account=None,
                               form_values=values or {}), status

    @app.get("/")
    def index():
        if g.account is not None and g.player is None:
            return character_list_page()
        room = None
        if g.player is not None and g.player["status"] == "approved" and g.player["room"]:
            room = room_view(g.player["room"], g.player["id"])
        onboarding_view = request.args.get("view", "welcome").strip().lower()
        if onboarding_view not in ("welcome", "login", "register"):
            onboarding_view = "welcome"
        return render_template("entry.html", player=g.player, species_list=world.SPECIES, room=room,
                               onboarding_view=onboarding_view, notice=session.pop("reward_notice", None))

    @app.get("/mundo")
    def world_reader():
        capitulo = request.args.get("capitulo", "1").strip().lower()
        if capitulo not in ("1", "2", "3", "4", "5", "todo"):
            capitulo = "1"
        content = content_parser.get_world_content()
        return render_template(
            "world.html",
            world=content,
            active_chapter=capitulo,
            account=g.account,
            player=g.player,
        )

    @app.get("/guia")
    def guide_reader():
        content = content_parser.get_guide_content()
        return render_template(
            "guide.html",
            guide=content,
            account=g.account,
            player=g.player,
        )

    @app.post("/register")
    def register():
        if not store.allow_attempt(path, request.remote_addr or "unknown"):
            return guest_page("Demasiados intentos. Espera un minuto.", 429, "register")
        username = request.form.get("username", "").strip().lower()
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        values = {"username": username[:32], "name": name[:60]}
        if not re.fullmatch(r"[a-z0-9_]{3,32}", username):
            return guest_page("El usuario debe tener de 3 a 32 letras o números, sin acentos ni espacios "
                              "(puedes usar guion bajo _).", 400, "register", values)
        if not valid_character_name(name):
            return guest_page("Escribe el nombre de tu personaje (hasta 60 letras).", 400, "register", values)
        if not 8 <= len(password) <= 128:
            return guest_page("La contraseña debe tener al menos 8 caracteres.", 400, "register", values)
        try:
            token = store.register(path, username, name, generate_password_hash(password), session.get("token"))
        except store.UsernameTaken:
            return guest_page(f"El usuario «{username}» ya existe. Si es tuyo, usa Entrar; "
                              "si no, elige otro usuario.", 409, "register", values)
        except (store.NameTaken, sqlite3.IntegrityError):
            return guest_page(f"Ya hay un personaje llamado «{name}» en el mundo. "
                              "Elige otro nombre para tu personaje.", 409, "register", values)
        return establish_session(token)

    @app.post("/login")
    def login():
        if not store.allow_attempt(path, request.remote_addr or "unknown"):
            return guest_page("Demasiados intentos. Espera un minuto.", 429, "login")
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        if len(password) > 128 or len(username) > 32:
            abort(400)
        with store.connect(path) as db:
            account = store.account_by_username(db, username)
            valid = check_password_hash(account["password_hash"] if account else dummy_hash, password)
            if not valid or account is None:
                return guest_page("Usuario o contraseña incorrectos.", 401, "login", {"username": username})
            # Con un solo personaje se entra directo, como siempre; con varios
            # (o ninguno) se muestra la lista para elegir.
            player_id = store.only_character_id(db, account["id"])
            token = store.record_access(db, account["id"], player_id, "login", session.get("token"))
        return establish_session(token)

    def require_account():
        if g.account is None:
            abort(401)

    @app.post("/characters/select")
    def select_character():
        require_account()
        if not store.select_character(path, session.get("token"), g.account["id"],
                                      request.form.get("player_id", "")):
            return character_list_page("Ese personaje no está en tu cuenta.", 404)
        return redirect(url_for("index"), code=303)

    @app.post("/characters/new")
    def new_character():
        require_account()
        name = request.form.get("name", "").strip()
        if not valid_character_name(name):
            return character_list_page("Escribe el nombre de tu personaje (hasta 60 letras).", 400, name[:60])
        try:
            store.create_character(path, g.account["id"], name)
        except store.TooManyCharacters:
            return character_list_page(
                f"Ya tienes {store.MAX_CHARACTERS_PER_ACCOUNT} personajes, el máximo por cuenta.", 409)
        except (store.NameTaken, sqlite3.IntegrityError):
            return character_list_page(f"Ya hay un personaje llamado «{name}» en el mundo. "
                                       "Elige otro nombre.", 409, name[:60])
        return redirect(url_for("index"), code=303)

    @app.post("/characters/switch")
    def switch_character():
        require_account()
        store.release_character(path, session.get("token"))
        return redirect(url_for("index"), code=303)

    @app.post("/logout")
    def logout():
        token = session.get("token", "")
        with store.connect(path) as db:
            row = db.execute(
                "SELECT player_id FROM sessions WHERE token_hash = ?",
                (store.digest(token),),
            ).fetchone()
            if row and row["player_id"]:
                store._clear_presence(db, row["player_id"])
            db.execute("DELETE FROM sessions WHERE token_hash = ?", (store.digest(token),))
        session.clear()
        return redirect(url_for("index"), code=303)

    @app.post("/species")
    def choose_species():
        require_approved_player()
        if g.player["species"] is not None:
            # Ya eligio: no es un error de validacion, solo no hay nada que hacer.
            return redirect(url_for("index"), code=303)
        accepted, _species, _room, reason = attempt_choose_species(g.player, request.form.get("species", ""))
        if not accepted:
            return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                                   error=reason), 400
        return redirect(url_for("index"), code=303)

    @app.post("/class")
    def choose_class():
        require_approved_player()
        if g.player["species"] is None:
            return redirect(url_for("index"), code=303)
        if g.player["player_class"] is not None:
            return redirect(url_for("index"), code=303)
        accepted, _class, reason = attempt_choose_class(g.player, request.form.get("player_class", ""))
        if not accepted:
            return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                                   error=reason), 400
        return redirect(url_for("index"), code=303)

    def _combat_result_page(result):
        """Renderiza una resolución de combate sin inferir derrota desde texto."""
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        death_event = result.get("death_event")
        return render_template(
            "entry.html",
            player=player_now,
            species_list=world.SPECIES,
            room=room_data,
            error=None if death_event else " ".join(result["messages"]),
            death_event=death_event,
            level_up_event=result.get("level_up_event"),
        ), 200

    @app.post("/move")
    def move():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        accepted, _previous, _new, reason, level_up_event = attempt_move(g.player, request.form.get("direction", ""))
        if not accepted:
            room_data = room_view(g.player["room"], g.player["id"])
            return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                                   room=room_data, error=reason), 400
        if level_up_event and level_up_event.get("level_up"):
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template(
                "entry.html", player=player_now, species_list=world.SPECIES, room=room_data,
                notice=getattr(g, "reward_message", None), level_up_event=level_up_event,
            ), 200
        if getattr(g, "reward_message", None):
            session["reward_notice"] = g.reward_message
        return redirect(url_for("index"), code=303)

    @app.post("/room/say")
    def say():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        body = request.form.get("body", "").strip()
        if not body or len(body) > 500:
            abort(400)
        store.add_message(path, g.player["room"], g.player["id"], body)
        return redirect(url_for("index"), code=303)

    @app.post("/command")
    def command():
        """Cuadro de texto del terminal: cada texto se clasifica por intención.
        El chat requiere 'decir <texto>'; un comando desconocido nunca se publica."""
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        raw = request.form.get("text", "")
        if len(raw) > 500:
            abort(400)
        intent = parse_intent(raw)
        if intent["type"] == "move":
            accepted, _previous, _new, reason, level_up_event = attempt_move(g.player, intent["direction"])
            if not accepted:
                room_data = room_view(g.player["room"], g.player["id"])
                return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                                       room=room_data, error=reason), 400
            if level_up_event and level_up_event.get("level_up"):
                player_now = store.player_for_token(path, session.get("token"))
                room_data = room_view(player_now["room"], player_now["id"])
                return render_template(
                    "entry.html", player=player_now, species_list=world.SPECIES, room=room_data,
                    notice=getattr(g, "reward_message", None), level_up_event=level_up_event,
                ), 200
            if getattr(g, "reward_message", None):
                session["reward_notice"] = g.reward_message
            return redirect(url_for("index"), code=303)
        if intent["type"] == "look":
            return redirect(url_for("index"), code=303)
        if intent["type"] in ("errands_list", "errand"):
            if intent["type"] == "errands_list":
                message = "; ".join(f"{e['contract_id']}: {e['state']} ({e['base_payout']} sellos base)"
                                    for e in errands.list_contracts(path, g.player["id"]))
                ok = True
            else:
                ok, message, _extra = errands.act(path, g.player["id"], g.player["room"],
                                                  intent["contract_id"], intent["action"])
            player_now = store.player_for_token(path, session.get("token"))
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_view(player_now["room"], player_now["id"]), error=message), (200 if ok else 400)
        if intent["type"] == "say":
            store.add_message(path, g.player["room"], g.player["id"], intent["body"])
            return redirect(url_for("index"), code=303)

        if intent["type"] == "inspect":
            target = intent["target"] or "el lugar"
            result = resolve_inspect(g.player, intent["target"])
            level_up_event = None
            if result:
                text, awarded, level_up_event = result
                message = f"{text} {awarded}" if awarded else text
            else:
                message = f"Inspección registrada para {target}. No hay detalle adicional autorizado todavía."
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(g.player["room"], g.player["id"])
            return render_template(
                "entry.html", player=player_now, species_list=world.SPECIES,
                room=room_data, error=message, level_up_event=level_up_event,
            ), 200
        if intent["type"] == "evaluate":
            _name, message = attempt_evaluate(g.player)
            room_data = room_view(g.player["room"], g.player["id"])
            return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                                   room=room_data, error=message), 200
        if intent["type"] == "attack":
            return _combat_result_page(attempt_attack(g.player))
        if intent["type"] == "flee":
            return _combat_result_page(attempt_flee(g.player))
        if intent["type"] == "avoid":
            result = attempt_avoid(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), (200 if result["outcome"] != "no_target" else 400)
        if intent["type"] == "rest":
            result = attempt_rest(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "dodge":
            return _combat_result_page(attempt_dodge(g.player))
        if intent["type"] == "resist":
            return _combat_result_page(attempt_resist(g.player))
        if intent["type"] == "block":
            return _combat_result_page(attempt_block(g.player))
        if intent["type"] == "signature_ability":
            return _combat_result_page(attempt_signature_ability(g.player))
        if intent["type"] == "equip":
            result = attempt_equip(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "unequip":
            result = attempt_unequip(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "buy":
            result = attempt_buy(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "sell":
            result = attempt_sell(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "use_recovery":
            result = attempt_use_recovery(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "talk_npc":
            target = intent.get("target", "")
            target_norm = target.strip().lower()
            room_data_current = world.get_room(g.player["room"])
            encounter_active = store.get_encounter(path, g.player["id"], g.player["room"])
            n0 = None if encounter_active else population.get_room_n0_presence(g.player["room"], room_data=room_data_current)
            if n0 and target_norm in (n0["id"].lower(), n0["name"].lower(), n0["role_id"].lower()):
                player_now = store.player_for_token(path, session.get("token"))
                room_data = room_view(g.player["room"], g.player["id"])
                dialogue_text = f"{n0['name']}: «{n0['reply']}»"
                return render_template(
                    "entry.html", player=player_now, species_list=world.SPECIES, room=room_data,
                    error=dialogue_text,
                ), 200

            result = npc_dialogue.converse(
                g.player,
                intent["target"],
                message=intent.get("message", ""),
                room_id=g.player["room"],
                db_path=path,
            )
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(g.player["room"], g.player["id"])
            if not result.success:
                return render_template(
                    "entry.html", player=player_now, species_list=world.SPECIES, room=room_data,
                    error=result.reason,
                ), 200
            dialogue_text = f"{result.npc_name}: «{result.text}»"
            if result.gate_result and result.gate_result.accepted and result.gate_result.action_type == "purchase_item":
                eff = result.gate_result.effect or {}
                dialogue_text += f" [Comprado: {eff.get('name', 'arma')} por {eff.get('price', '')} sellos. Saldo restante: {eff.get('balance')} sellos]"
            return render_template(
                "entry.html", player=player_now, species_list=world.SPECIES, room=room_data,
                error=dialogue_text,
            ), 200
        if intent["type"] == "help_scene":
            room_id = g.player["room"]
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(room_id, g.player["id"])
            if room_id == "khariel_forja":
                result = npc_dialogue.converse(
                    g.player,
                    "khariel_taller_hoshai_01",
                    message="ayudo a sujetar el amarre",
                    room_id=room_id,
                    db_path=path,
                )
                dialogue_text = f"{result.npc_name}: «{result.text}»"
                return render_template(
                    "entry.html", player=player_now, species_list=world.SPECIES, room=room_data,
                    error=dialogue_text,
                ), 200
            elif room_id == "brumak_forja":
                result = npc_dialogue.converse(
                    g.player,
                    "brumak_taller_korven_01",
                    message="ayudo a sostener el apoyo",
                    room_id=room_id,
                    db_path=path,
                )
                dialogue_text = f"{result.npc_name}: «{result.text}»"
                return render_template(
                    "entry.html", player=player_now, species_list=world.SPECIES, room=room_data,
                    error=dialogue_text,
                ), 200
            return render_template(
                "entry.html", player=player_now, species_list=world.SPECIES, room=room_data,
                error="No hay ninguna tarea o paso que asegurar aquí.",
            ), 200
        room_data = room_view(g.player["room"], g.player["id"])
        return render_template(
            "entry.html", player=g.player, species_list=world.SPECIES, room=room_data,
            error="Comando no reconocido. Para chat usa: decir <texto>."
        ), 400

    @app.get("/api/me")
    def me():
        # csrf va incluido para que un cliente JSON (fetch) pueda reusarlo en
        # los POST estructurados (/api/species, /api/move) sin parsear HTML.
        if g.account is not None and g.player is None:
            # Cuenta abierta sin personaje activo: toca elegir uno en "/".
            return jsonify(player=None, error="character_required", csrf=session.get("csrf")), 409
        if g.player is None:
            return jsonify(player=None, csrf=session.get("csrf")), 401
        return jsonify(player=dict(g.player), world_status="under_construction", csrf=session.get("csrf"))

    @app.get("/api/room")
    def api_room():
        error = api_player_state(g.player)
        if error:
            return error
        if g.player["species"] is None:
            return jsonify(error="species_required"), 409
        if g.player["player_class"] is None:
            return jsonify(error="class_required"), 409
        return jsonify(room=room_view(g.player["room"], g.player["id"]))

    @app.post("/api/species")
    def api_choose_species():
        """Contrato estructurado (FIRST_PLAYABLE_SLICE.md): responde con la
        especie confirmada, el pueblo inicial, la sala inicial y el estado
        actualizado del jugador."""
        error = api_player_state(g.player)
        if error:
            return error
        payload = request.get_json(silent=True) or {}
        accepted, species_id, room_id, reason = attempt_choose_species(g.player, payload.get("species", ""))
        if not accepted:
            return jsonify(accepted=False, reason=reason), 400
        updated_player = store.player_for_token(path, session.get("token"))
        starting_town_room = world.get_starting_room_for_species(species_id)
        town = world.get_room(starting_town_room)
        return jsonify(
            accepted=True,
            species=species_id,
            town=town["name"] if town else None,
            room=room_view(room_id, g.player["id"]),
            player=dict(updated_player) if updated_player else None,
        )

    @app.post("/api/class")
    def api_choose_class():
        """Contrato estructurado de la clase inicial (Issue #112): clase
        confirmada, arma inicial entregada y estado actualizado del jugador."""
        error = api_player_state(g.player)
        if error:
            return error
        payload = request.get_json(silent=True) or {}
        accepted, class_id, reason = attempt_choose_class(g.player, str(payload.get("player_class", "")))
        if not accepted:
            return jsonify(accepted=False, reason=reason), 400
        updated_player = store.player_for_token(path, session.get("token"))
        weapon_key = items.STARTER_WEAPON_BY_CLASS.get(class_id)
        return jsonify(
            accepted=True,
            player_class=class_id,
            starter_weapon=({"item_key": weapon_key, "name": items.get_item(weapon_key)["name"]}
                            if weapon_key else None),
            player=dict(updated_player) if updated_player else None,
        )

    @app.post("/api/intent")
    def api_intent():
        """Contrato estructurado para intención de terminal."""
        error = api_player_state(g.player)
        if error:
            return error
        if g.player["species"] is None:
            return jsonify(error="species_required"), 409
        if g.player["player_class"] is None:
            return jsonify(error="class_required"), 409
        payload = request.get_json(silent=True) or {}
        raw = str(payload.get("text", ""))
        if len(raw) > 500:
            return jsonify(accepted=False, intent="invalid", reason="Texto demasiado largo."), 400
        intent = parse_intent(raw)
        kind = intent["type"]

        if kind == "move":
            accepted, previous_room, new_room, reason, level_up_event = attempt_move(g.player, intent["direction"])
            current_room_id = new_room if accepted else previous_room
            return jsonify(
                accepted=accepted,
                intent="move",
                reward_message=getattr(g, "reward_message", None),
                previous_room=previous_room,
                current_room=room_view(current_room_id, g.player["id"]),
                reason=reason,
                level_up_event=level_up_event,
            ), (200 if accepted else 400)
        if kind == "look":
            return jsonify(
                accepted=True,
                intent="look",
                current_room=room_view(g.player["room"], g.player["id"]),
            )
        if kind in ("errands_list", "errand"):
            if kind == "errands_list":
                return jsonify(accepted=True, intent=kind, contracts=errands.list_contracts(path, g.player["id"]))
            ok, message, extra = errands.act(path, g.player["id"], g.player["room"],
                                             intent["contract_id"], intent["action"])
            return jsonify(accepted=ok, intent=kind, message=message, result=extra,
                           contracts=errands.list_contracts(path, g.player["id"])), (200 if ok else 400)
        if kind == "say":
            store.add_message(path, g.player["room"], g.player["id"], intent["body"])
            return jsonify(accepted=True, intent="say")
        if kind == "inspect":
            result = resolve_inspect(g.player, intent["target"])
            text, awarded, level_up_event = result if result else (None, None, None)
            return jsonify(
                accepted=True,
                intent="inspect",
                verb=intent["verb"],
                target=intent["target"],
                detail=text,
                message=(text or "No hay detalle adicional autorizado todavía."),
                discovery=awarded,
                level_up_event=level_up_event,
                current_room=room_view(g.player["room"], g.player["id"]),
            )
        if kind == "evaluate":
            name, message = attempt_evaluate(g.player)
            return jsonify(accepted=name is not None, intent="evaluate", target=name, message=message)
        if kind == "attack":
            result = attempt_attack(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] != "no_target",
                intent="attack",
                outcome=result["outcome"],
                messages=result["messages"],
                death_event=result.get("death_event"),
                level_up_event=result.get("level_up_event"),
                player=dict(player_now) if player_now else None,
                current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
            )
        if kind == "flee":
            result = attempt_flee(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] != "no_target",
                intent="flee",
                outcome=result["outcome"],
                messages=result["messages"],
                death_event=result.get("death_event"),
                player=dict(player_now) if player_now else None,
                current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
            )
        if kind == "avoid":
            result = attempt_avoid(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] != "no_target",
                intent="avoid",
                outcome=result["outcome"],
                messages=result["messages"],
                player=dict(player_now) if player_now else None,
                current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
            ), (200 if result["outcome"] != "no_target" else 400)
        if kind == "rest":
            result = attempt_rest(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] != "blocked",
                intent="rest",
                outcome=result["outcome"],
                messages=result["messages"],
                player=dict(player_now) if player_now else None,
            )
        if kind == "dodge":
            result = attempt_dodge(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] != "no_target",
                intent="dodge",
                outcome=result["outcome"],
                messages=result["messages"],
                death_event=result.get("death_event"),
                player=dict(player_now) if player_now else None,
                current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
            )
        if kind == "resist":
            result = attempt_resist(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] != "no_target",
                intent="resist",
                outcome=result["outcome"],
                messages=result["messages"],
                death_event=result.get("death_event"),
                player=dict(player_now) if player_now else None,
                current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
            )
        if kind == "block":
            result = attempt_block(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] not in ("no_target", "unavailable"),
                intent="block",
                outcome=result["outcome"],
                messages=result["messages"],
                death_event=result.get("death_event"),
                player=dict(player_now) if player_now else None,
                current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
            )
        if kind == "signature_ability":
            result = attempt_signature_ability(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] not in ("no_target", "unavailable"),
                intent="signature_ability",
                outcome=result["outcome"],
                messages=result["messages"],
                player=dict(player_now) if player_now else None,
                current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
            )
        if kind == "equip":
            result = attempt_equip(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] == "equipped",
                intent="equip",
                outcome=result["outcome"],
                messages=result["messages"],
                player=dict(player_now) if player_now else None,
            )
        if kind == "unequip":
            result = attempt_unequip(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] == "unequipped",
                intent="unequip",
                outcome=result["outcome"],
                messages=result["messages"],
                player=dict(player_now) if player_now else None,
            )
        if kind == "buy":
            result = attempt_buy(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] == "bought",
                intent="buy",
                outcome=result["outcome"],
                messages=result["messages"],
                player=dict(player_now) if player_now else None,
            )
        if kind == "sell":
            result = attempt_sell(g.player, intent["target"])
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=result["outcome"] == "sold",
                intent="sell",
                outcome=result["outcome"],
                messages=result["messages"],
                player=dict(player_now) if player_now else None,
            )
        if kind == "talk_npc":
            target = intent.get("target", "")
            target_norm = target.strip().lower()
            room_data_current = world.get_room(g.player["room"])
            encounter_active = store.get_encounter(path, g.player["id"], g.player["room"])
            n0 = None if encounter_active else population.get_room_n0_presence(g.player["room"], room_data=room_data_current)
            if n0 and target_norm in (n0["id"].lower(), n0["name"].lower(), n0["role_id"].lower()):
                return jsonify(
                    accepted=True,
                    intent="talk_npc",
                    npc=n0["id"],
                    npc_name=n0["name"],
                    reply=n0["reply"],
                    is_fallback=False,
                    is_n0=True,
                    proposed_action=None,
                    gate_result=None,
                ), 200

            result = npc_dialogue.converse(
                g.player,
                intent["target"],
                message=intent.get("message", ""),
                room_id=g.player["room"],
                db_path=path,
            )
            if not result.success:
                return jsonify(
                    accepted=False,
                    intent="talk_npc",
                    npc=intent["target"],
                    target=intent["target"],
                    error=result.error,
                    reason=result.reason,
                ), 409
            action_payload = (
                {"action_type": result.proposed_action.action_type, "payload": result.proposed_action.payload}
                if result.proposed_action else None
            )
            gate_payload = (
                {
                    "accepted": result.gate_result.accepted,
                    "action_type": result.gate_result.action_type,
                    "reason": result.gate_result.reason,
                    "effect": result.gate_result.effect,
                }
                if result.gate_result else None
            )
            return jsonify(
                accepted=True,
                intent="talk_npc",
                npc=result.npc_id,
                npc_name=result.npc_name,
                reply=result.text,
                is_fallback=result.is_fallback,
                proposed_action=action_payload,
                gate_result=gate_payload,
            ), 200
        if kind == "help_scene":
            room_id = g.player["room"]
            if room_id == "khariel_forja":
                result = npc_dialogue.converse(
                    g.player,
                    "khariel_taller_hoshai_01",
                    message="ayudo a sujetar el amarre",
                    room_id=room_id,
                    db_path=path,
                )
                player_now = store.player_for_token(path, session.get("token"))
                return jsonify(
                    accepted=True,
                    intent="help_scene",
                    npc=result.npc_id,
                    npc_name=result.npc_name,
                    reply=result.text,
                    player=dict(player_now) if player_now else None,
                    current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
                ), 200
            elif room_id == "brumak_forja":
                result = npc_dialogue.converse(
                    g.player,
                    "brumak_taller_korven_01",
                    message="ayudo a sostener el apoyo",
                    room_id=room_id,
                    db_path=path,
                )
                player_now = store.player_for_token(path, session.get("token"))
                return jsonify(
                    accepted=True,
                    intent="help_scene",
                    npc=result.npc_id,
                    npc_name=result.npc_name,
                    reply=result.text,
                    player=dict(player_now) if player_now else None,
                    current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
                ), 200
            return jsonify(
                accepted=False,
                intent="help_scene",
                reason="No hay ninguna tarea o paso que asegurar aquí.",
            ), 400
        return jsonify(
            accepted=False,
            intent=kind,
            reason="Comando no reconocido. Para chat usa: decir <texto>.",
        ), 400

    @app.post("/api/talk")
    def api_talk():
        """Contrato estructurado para conversación con NPC (Issue #245)."""
        error = api_player_state(g.player)
        if error:
            return error
        data = request.get_json(silent=True) or request.form
        target = (data.get("target") or data.get("npc") or "").strip()
        message = (data.get("message") or data.get("text") or "").strip()
        if not target:
            return jsonify(accepted=False, error="target_required", reason="Debes indicar con quién deseas hablar."), 400

        target_norm = target.strip().lower()
        room_data_current = world.get_room(g.player["room"])
        encounter_active = store.get_encounter(path, g.player["id"], g.player["room"])
        n0 = None if encounter_active else population.get_room_n0_presence(g.player["room"], room_data=room_data_current)
        if n0 and target_norm in (n0["id"].lower(), n0["name"].lower(), n0["role_id"].lower()):
            return jsonify(
                accepted=True,
                intent="talk_npc",
                npc=n0["id"],
                npc_name=n0["name"],
                reply=n0["reply"],
                is_fallback=False,
                is_n0=True,
                proposed_action=None,
                gate_result=None,
            ), 200

        result = npc_dialogue.converse(g.player, target, message=message, room_id=g.player["room"], db_path=path)
        if not result.success:
            status_code = 404 if result.error in ("npc_not_found", "npc_not_present") else 400
            return jsonify(
                accepted=False,
                intent="talk_npc",
                target=target,
                error=result.error,
                reason=result.reason,
            ), status_code
        action_payload = (
            {"action_type": result.proposed_action.action_type, "payload": result.proposed_action.payload}
            if result.proposed_action else None
        )
        gate_payload = (
            {
                "accepted": result.gate_result.accepted,
                "action_type": result.gate_result.action_type,
                "reason": result.gate_result.reason,
                "effect": result.gate_result.effect,
            }
            if result.gate_result else None
        )
        return jsonify(
            accepted=True,
            intent="talk_npc",
            npc=result.npc_id,
            npc_name=result.npc_name,
            reply=result.text,
            is_fallback=result.is_fallback,
            proposed_action=action_payload,
            gate_result=gate_payload,
        ), 200

    @app.post("/api/move")
    def api_move():
        """Contrato estructurado (FIRST_PLAYABLE_SLICE.md): responde con
        aceptada/rechazada, sala anterior, sala actual y salidas -- el cliente
        no debe deducir la ubicacion interpretando texto narrativo."""
        error = api_player_state(g.player)
        if error:
            return error
        if g.player["species"] is None:
            return jsonify(error="species_required"), 409
        if g.player["player_class"] is None:
            return jsonify(error="class_required"), 409
        payload = request.get_json(silent=True) or {}
        direction = DIRECTION_ALIASES.get(str(payload.get("direction", "")).strip().lower())
        if direction is None:
            return jsonify(accepted=False, reason="Dirección desconocida."), 400
        accepted, previous_room, new_room, reason, level_up_event = attempt_move(g.player, direction)
        current_room_id = new_room if accepted else previous_room
        return jsonify(
            accepted=accepted,
            previous_room=previous_room,
            reason=reason,
            reward_message=getattr(g, "reward_message", None),
            current_room=room_view(current_room_id, g.player["id"]),
            level_up_event=level_up_event,
        ), (200 if accepted else 400)

    @app.get("/api/character")
    def api_character():
        """Estado de personaje jugable (GAMEPLAY.md 20-22): nivel, XP, PA sin
        gastar, HP, fatiga, herida, atributos y descubrimientos -- para el
        panel Personaje que pide Issue #43 (P1)."""
        error = api_player_state(g.player)
        if error:
            return error
        encounter = (store.get_encounter(path, g.player["id"], g.player["room"])
                     if g.player["room"] else None)
        player_class = g.player["player_class"]
        ability_info = combat.SIGNATURE_ABILITIES.get(player_class) if player_class else None
        return jsonify(
            species=g.player["species"], player_class=g.player["player_class"],
            signature_ability=({"id": ability_info["id"], "name": ability_info["name"], "cooldown": ability_info["cooldown"]}
                               if ability_info else None),
            level=g.player["level"], xp=g.player["xp"],
            xp_to_next=combat.xp_for_next_level(g.player["level"]),
            pa_unspent=g.player["pa_unspent"], pp_unspent=g.player["pp_unspent"],
            hp_current=g.player["hp_current"], hp_max=g.player["hp_max"],
            fatigue=g.player["fatigue"], wound=g.player["wound"],
            attributes=_attributes(g.player),
            # GAMEPLAY.md 19/25.4: coste visible del siguiente +1 de cada
            # atributo, para que el panel muestre valor actual, nuevo valor y
            # coste antes de confirmar. El cliente no calcula costes.
            attribute_costs={name: combat.attribute_cost(value)
                             for name, value in _attributes(g.player).items()},
            in_combat=bool(encounter and encounter.get("engaged", 1)),
            discoveries=store.list_discoveries(path, g.player["id"]),
            sellos=g.player["sellos"],
        )

    @app.post("/api/character/attributes")
    def api_spend_attribute_point():
        """GAMEPLAY.md 25.4/25.5: gastar PA en +1 de un atributo. El cliente
        envía el atributo y el valor que el jugador vio al confirmar
        (`current_value`); si ya cambió, se rechaza como confirmación vieja
        en vez de gastar sobre un estado distinto. Solo fuera de combate, sin
        PA negativos y atómico frente a solicitudes concurrentes. Sin
        deshacer en v1."""
        error = api_player_state(g.player)
        if error:
            return error
        if g.player["species"] is None:
            return jsonify(error="species_required"), 409
        if g.player["player_class"] is None:
            return jsonify(error="class_required"), 409
        payload = request.get_json(silent=True) or {}
        attribute = str(payload.get("attribute", ""))
        expected = payload.get("current_value")
        if not isinstance(expected, int) or isinstance(expected, bool):
            return jsonify(accepted=False, reason="confirmation_required",
                           message="Confirma el valor actual del atributo antes de gastar PA."), 400
        ok, reason, result = store.spend_attribute_point(path, g.player["id"], attribute, expected)
        if not ok:
            messages = {
                "unknown_attribute": "Ese atributo no existe.",
                "no_character": "Tu personaje todavía no está listo.",
                "in_combat": "No puedes mejorar atributos con una criatura cerca.",
                "stale_confirmation": "Tu personaje cambió; revisa los valores y vuelve a confirmar.",
                "not_enough_pa": "No tienes PA suficientes para esa mejora.",
            }
            status = 400 if reason == "unknown_attribute" else 409
            return jsonify(accepted=False, reason=reason, message=messages[reason]), status
        return jsonify(
            accepted=True, **result,
            next_cost=combat.attribute_cost(result["value"]),
            message=f"{result['attribute'].capitalize()} sube a {result['value']} (−{result['cost']} PA).",
        )

    @app.get("/api/inventory")
    def api_inventory():
        """GAMEPLAY.md 32.8: estado estructurado de inventario/equipo para
        el panel Inventario/Equipo -- objetos poseídos, cuál está activo,
        protección/carga conocida y estado de validación de Forja. El
        servidor entrega el estado ya resuelto; el cliente no calcula nada
        autoritativo (Issue #57)."""
        error = api_player_state(g.player)
        if error:
            return error
        weapon_id, armor_id = g.player["equipped_weapon_id"], g.player["equipped_armor_id"]

        def decorate(row):
            catalog = items.get_item(row["item_key"])
            return {
                "id": row["id"],
                "item_key": row["item_key"],
                "name": catalog["name"],
                "category": row["category"],
                "forge_required": catalog["forge_required"],
                "forge_validated": bool(row["forge_validated"]),
                "equipped": row["id"] in (weapon_id, armor_id),
                "base_damage": catalog.get("base_damage"),
                "can_block": catalog.get("can_block"),
                "armor_reduction": catalog.get("armor_reduction"),
            }

        inventory = [decorate(row) for row in store.list_inventory(path, g.player["id"])]
        equipment = _equipment(g.player)
        return jsonify(
            items=inventory,
            equipped={
                "weapon": next((row for row in inventory if row["id"] == weapon_id), None),
                "armor": next((row for row in inventory if row["id"] == armor_id), None),
            },
            sellos=g.player["sellos"],
            armor_reduction_total=equipment["armor_reduction"],
            carga_multiplier=combat.armor_load_multiplier(equipment["armor_reduction"]),
        )

    @app.get("/api/recovery/valdren")
    def api_recovery_valdren():
        error = api_player_state(g.player)
        if error:
            return error
        data = recovery.catalog()
        return jsonify(**data, in_market=(g.player["room"] == recovery.RECOVERY_ROOM),
                       sellos=g.player["sellos"])

    @app.post("/api/recovery/buy")
    def api_recovery_buy():
        error = api_player_state(g.player)
        if error:
            return error
        data = request.get_json(silent=True) or request.form
        item_id = (data.get("item_id") or "").strip()
        if item_id != recovery.RATION_ITEM_ID:
            return jsonify(accepted=False, outcome="not_found",
                           messages=["Ese item_id no es una provisión de recuperación."]), 400
        ok, message, extra = recovery.buy_ration(
            path, g.player["id"], g.player["room"],
            client_tx_id=data.get("client_tx_id"),
        )
        return jsonify(accepted=ok, outcome="bought" if ok else "rejected",
                       messages=[message], **(extra or {})), (200 if ok else 400)

    @app.post("/api/recovery/use")
    def api_recovery_use():
        error = api_player_state(g.player)
        if error:
            return error
        data = request.get_json(silent=True) or request.form
        instance_id = (data.get("inventory_item_id") or "").strip()
        if not instance_id:
            return jsonify(accepted=False, outcome="invalid",
                           messages=["Falta inventory_item_id."]), 400
        ok, message, extra = recovery.use_ration(path, g.player["id"], instance_id)
        return jsonify(accepted=ok, outcome="used" if ok else "rejected",
                       messages=[message], **(extra or {})), (200 if ok else 400)

    @app.post("/api/recovery/service")
    def api_recovery_service():
        error = api_player_state(g.player)
        if error:
            return error
        data = request.get_json(silent=True) or request.form
        service_id = (data.get("service_id") or "").strip()
        if service_id != recovery.SERVICE_ID:
            return jsonify(accepted=False, outcome="not_found",
                           messages=["Ese service_id no existe."]), 400
        ok, message, extra = recovery.use_market_service(
            path, g.player["id"], g.player["room"],
            client_tx_id=data.get("client_tx_id"),
        )
        return jsonify(accepted=ok, outcome="used" if ok else "rejected",
                       messages=[message], **(extra or {})), (200 if ok else 400)

    @app.get("/api/shop/daro")
    def api_shop_daro():
        """ECONOMY-CORE-01: catálogo de compra y recompra de Daro en Valdren."""
        error = api_player_state(g.player)
        if error:
            return error
        in_shop = (g.player["room"] == economy.DARO_SHOP_ROOM)
        return jsonify(
            shop_id=economy.DARO_NPC_ID,
            shop_name="Taller de Daro",
            room=economy.DARO_SHOP_ROOM,
            in_shop=in_shop,
            sellos=g.player["sellos"],
            catalog=economy.daro_catalog_entries(),
        )

    @app.post("/api/shop/daro/buy")
    def api_shop_daro_buy():
        """ECONOMY-CORE-01: compra estructurada en el taller de Daro."""
        error = api_player_state(g.player)
        if error:
            return error
        data = request.get_json(silent=True) or request.form
        item_target = (data.get("item_key") or data.get("item") or "").strip()
        result = attempt_buy(g.player, item_target)
        player_now = store.player_for_token(path, session.get("token"))
        status_code = 200 if result["outcome"] == "bought" else 400
        return jsonify(
            accepted=result["outcome"] == "bought",
            outcome=result["outcome"],
            messages=result["messages"],
            sellos=player_now["sellos"] if player_now else None,
            item_key=result.get("item_key"),
        ), status_code

    @app.post("/api/shop/daro/sell")
    def api_shop_daro_sell():
        """ECONOMY-CORE-01: venta estructurada en el taller de Daro."""
        error = api_player_state(g.player)
        if error:
            return error
        data = request.get_json(silent=True) or request.form
        item_id = data.get("item_id")
        item_target = (data.get("item_key") or data.get("item") or "").strip()
        if item_id:
            if store.get_encounter(path, g.player["id"], g.player["room"]):
                return jsonify(accepted=False, outcome="blocked", messages=["No puedes comerciar durante un encuentro."]), 400
            if g.player["room"] != economy.DARO_SHOP_ROOM:
                return jsonify(accepted=False, outcome="blocked", messages=["Solo puedes comerciar con Daro en su taller de Valdren (valdren_forja)."]), 400
            ok, message, extra = economy.sell_item_to_daro(path, g.player["id"], item_id)
            player_now = store.player_for_token(path, session.get("token"))
            return jsonify(
                accepted=ok,
                outcome="sold" if ok else "rejected",
                messages=[message],
                sellos=player_now["sellos"] if player_now else None,
            ), (200 if ok else 400)
        else:
            result = attempt_sell(g.player, item_target)
            player_now = store.player_for_token(path, session.get("token"))
            status_code = 200 if result["outcome"] == "sold" else 400
            return jsonify(
                accepted=result["outcome"] == "sold",
                outcome=result["outcome"],
                messages=result["messages"],
                sellos=player_now["sellos"] if player_now else None,
                item_key=result.get("item_key"),
            ), status_code

    @app.get("/api/economy/ledger")
    def api_economy_ledger():
        """ECONOMY-CORE-01: consulta autoritativa del ledger del personaje."""
        error = api_player_state(g.player)
        if error:
            return error
        entries = economy.list_player_ledger(path, g.player["id"])
        return jsonify(sellos=g.player["sellos"], entries=entries)

    @app.get("/api/map")
    def api_map():
        """Mapa progresivo (GAMEPLAY.md 23): solo lo que este personaje
        visito/recorrio de verdad, nunca el mundo completo de produccion."""
        error = api_player_state(g.player)
        if error:
            return error
        # current_heading (Issue #120): rumbo del ultimo movimiento aceptado
        # por el servidor, o null si el personaje todavia no se movio. El
        # frontend no debe inferirlo de narrativa, nombre de sala ni imagen.
        state = store.get_map_state(path, g.player["id"])
        return jsonify(current_heading=g.player["heading"], **state,
                       **_minimap(state, g.player["room"]))

    @app.post("/attack")
    def attack():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        return _combat_result_page(attempt_attack(g.player))

    @app.post("/flee")
    def flee():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        return _combat_result_page(attempt_flee(g.player))

    @app.post("/dodge")
    def dodge():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        return _combat_result_page(attempt_dodge(g.player))

    @app.post("/resist")
    def resist():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        return _combat_result_page(attempt_resist(g.player))

    @app.post("/block")
    def block():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        return _combat_result_page(attempt_block(g.player))

    @app.post("/evaluate")
    def evaluate():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        _name, message = attempt_evaluate(g.player)
        room_data = room_view(g.player["room"], g.player["id"])
        return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                               room=room_data, error=message), 200

    @app.post("/avoid")
    def avoid():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        result = attempt_avoid(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), (200 if result["outcome"] != "no_target" else 400)

    @app.post("/ability")
    def ability():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        result = attempt_signature_ability(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), 200

    @app.get("/healthz")
    def health():
        with store.connect(path) as db:
            db.execute("SELECT id FROM players LIMIT 1").fetchone()
            version = db.execute("PRAGMA user_version").fetchone()[0]
        return jsonify(status="ok", schema_version=version)

    @app.get("/vintage-telnet.webmanifest")
    def webmanifest():
        response = jsonify(
            name="Vintage Telnet",
            short_name="Vintage Telnet",
            start_url="/",
            scope="/",
            display="standalone",
            background_color="#0a0e15",
            theme_color="#141c28",
            icons=[{
                "src": "/assets/app-icon/vintage-telnet.webp",
                "sizes": "192x192",
                "type": "image/webp",
                "purpose": "any",
            }],
        )
        response.mimetype = "application/manifest+json"
        return response

    @app.get("/assets/app-icon/vintage-telnet.webp")
    def app_icon():
        return send_from_directory(
            APP_ICON_PATH.parent,
            APP_ICON_PATH.name,
            mimetype="image/webp",
        )

    @app.get("/assets/html-ui/<path:filename>")
    def html_ui_assets(filename):
        return send_from_directory(HTML_UI_ASSETS_DIR, filename)

    @app.get("/assets/locations/<path:filename>")
    def location_assets(filename):
        # mimetype explicito: el pipeline de Arte (#42) solo publica WebP aqui,
        # y el modulo mimetypes del sistema no siempre lo conoce (falla en
        # Windows y en algunas imagenes minimas de Linux/Raspberry Pi OS),
        # lo que hacia que el navegador recibiera application/octet-stream y
        # nunca renderizara la imagen -- se veia como "ilustracion no
        # disponible" aunque el archivo si existiera y se sirviera con 200.
        return send_from_directory(LOCATION_ASSETS_DIR, filename, mimetype="image/webp")

    @app.get("/assets/maps/<path:filename>")
    def map_assets(filename):
        # Mismo motivo que location_assets: MIME explicito porque el pipeline
        # de Arte solo publica WebP aqui y algunos entornos (Windows,
        # Raspberry Pi OS minimo) no lo reconocen por extension.
        # send_from_directory ya rechaza cualquier `filename` que intente
        # escapar de MAPS_ASSETS_DIR (traversal) con 404.
        return send_from_directory(MAPS_ASSETS_DIR, filename, mimetype="image/webp")

    @app.get("/assets/species/<path:filename>")
    def species_assets(filename):
        # Fichas aprobadas de las cinco especies (pantalla de elección).
        return send_from_directory(SPECIES_ASSETS_DIR, filename, mimetype="image/webp")

    @app.get("/assets/creatures/<path:filename>")
    def creature_assets(filename):
        # Ilustraciones aprobadas de criaturas (combate). Mismas garantías que
        # map_assets: WebP explícito y send_from_directory rechaza traversal.
        return send_from_directory(CREATURE_ASSETS_DIR, filename, mimetype="image/webp")

    # --- Dungeon Master ---------------------------------------------------

    @app.get("/dm")
    def dm_panel():
        if not g.dm:
            return render_template("dm.html", authenticated=False, configured=dm_auth.is_configured())
        pending = store.list_by_status(path, "pending")
        approved = store.list_by_status(path, "approved")
        return render_template("dm.html", authenticated=True, pending=pending, approved=approved)

    @app.post("/dm/login")
    def dm_login():
        if not store.allow_attempt(path, "dm:" + (request.remote_addr or "unknown")):
            return render_template("dm.html", authenticated=False, configured=dm_auth.is_configured(),
                                   error="Demasiados intentos. Espera un minuto."), 429
        if not dm_auth.is_configured():
            return render_template("dm.html", authenticated=False, configured=False,
                                   error="El panel del Dungeon Master no está configurado en este servidor."), 503
        if not dm_auth.check_secret(request.form.get("dm_password", "")):
            return render_template("dm.html", authenticated=False, configured=True,
                                   error="Contraseña de Dungeon Master incorrecta."), 401
        session["dm"] = True
        return redirect(url_for("dm_panel"), code=303)

    @app.post("/dm/logout")
    def dm_logout():
        session.pop("dm", None)
        return redirect(url_for("dm_panel"), code=303)

    @app.post("/dm/approve")
    def dm_approve():
        require_dm()
        store.set_status(path, request.form.get("username", ""), "approved")
        return redirect(url_for("dm_panel"), code=303)

    @app.post("/dm/reject")
    def dm_reject():
        require_dm()
        store.set_status(path, request.form.get("username", ""), "rejected")
        return redirect(url_for("dm_panel"), code=303)

    @app.post("/dm/remove")
    def dm_remove():
        require_dm()
        store.set_status(path, request.form.get("username", ""), "removed", revoke_sessions=True)
        return redirect(url_for("dm_panel"), code=303)

    return app
