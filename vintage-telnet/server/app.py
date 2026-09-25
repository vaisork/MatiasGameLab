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

from . import combat, creatures, dm_auth, items, store, world

# Issue #46 resuelto: el Narrador fijo la plaza central de Valdren como
# punto de reaparicion tras morir (GAMEPLAY.md 20.9) y de recuperacion
# segura (24.9) para VT-NAR-003 (comentario del 2026-09-23), confirmado
# compatible con el canon por el Historiador y con conformidad de
# Jugabilidad. Es una decision narrativa ya tomada, no un marcador
# provisional de Desarrollo.
SAFE_ROOM_ID = "valdren_centro"

# Texto propuesto por el Narrador en Issue #46 para respawn y recuperacion
# segura en `SAFE_ROOM_ID` -- no es redaccion inventada por Desarrollo.
RESPAWN_MESSAGE = ("Vuelves en ti en la plaza central de Valdren. A tu alrededor regresan los "
                    "sonidos conocidos del pueblo: voces, pasos y trabajo cotidiano. El camino "
                    "hacia los campos sigue ahí, pero aquí estás fuera del peligro inmediato.")
SAFE_RECOVERY_MESSAGE = ("En la plaza de Valdren puedes detenerte sin vigilar cada ruido del "
                          "campo. Entre el movimiento cotidiano del pueblo recuperas fuerzas "
                          "antes de volver al camino.")

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

# Biblioteca de arte HTML (vintage-telnet/assets/html-ui/), servida explícitamente en vez de
# habilitar una carpeta estática general -- mantiene el resto del árbol del repo fuera de HTTP.
HTML_UI_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "html-ui"
LOCATION_ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "vintage-telnet" / "locations"
# Mapa regional aprobado (Issue #120 / PR #99): carpeta propia y acotada, nunca
# el arbol completo de assets/.
MAPS_ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "vintage-telnet" / "maps"
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
        g.player = store.player_for_token(path, session.get("token"))
        # Aunque haya una sesión de DM abierta desde la red privada, esa
        # sesión no da poderes de DM si la petición llega por internet.
        g.dm = bool(session.get("dm")) and not from_public_internet()

    @app.context_processor
    def inject_csp_nonce():
        return {"csp_nonce": getattr(g, "csp_nonce", "")}

    @app.after_request
    def headers(response):
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
        return {"current_room": current_room, "places": places, "unexplored_exits": unexplored}

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
        if encounter:
            creature = creatures.get_creature(encounter["creature_id"])
            view["encounter"] = {
                "creature_id": encounter["creature_id"],
                "name": creature["name"],
                # GAMEPLAY.md 31: nunca HP numerico de un enemigo, solo
                # condicion cualitativa; el comportamiento ayuda a distinguir
                # Mordelinde de Espinajo antes de decidir (VT-PSY-004).
                "condition": combat.enemy_condition(encounter["hp_current"], creature["hp"]),
                "behavior": creature["behavior_text"],
            }
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
                {"action": "esquivar"},
                {"action": "resistir"},
            ]
            if _can_block(path, player_id):
                view["available_actions"].append({"action": "bloquear"})
        else:
            view["encounter"] = None
            view["available_actions"] = [{"action": "descansar"}]
        return view

    # Intenciones canonicas: boton y comando escrito deben terminar en la misma
    # accion autoritativa del servidor (ver FIRST_PLAYABLE_SLICE.md).
    DIRECTION_ALIASES = {
        "norte": "north", "n": "north", "north": "north",
        "sur": "south", "s": "south", "south": "south",
        "este": "east", "e": "east", "east": "east",
        "oeste": "west", "o": "west", "west": "west",
    }
    LOOK_ALIASES = {"mirar", "ver", "look"}
    INSPECT_ALIASES = {"observar", "examinar"}
    SAY_PREFIXES = ("decir ", "say ")
    TALK_PREFIXES = ("hablar con ", "hablar ")
    FLEE_ALIASES = {"huir"}
    ATTACK_ALIASES = {"atacar"}
    EVALUATE_ALIASES = {"evaluar", "considerar"}
    REST_ALIASES = {"descansar"}
    DODGE_ALIASES = {"esquivar"}
    BLOCK_ALIASES = {"bloquear"}
    RESIST_ALIASES = {"resistir"}
    # GAMEPLAY.md 32.8: comandos canónicos de inventario/equipo (Issue #57).
    EQUIP_PREFIXES = ("equipar ",)
    UNEQUIP_PREFIXES = ("desequipar ",)

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
        if lowered in REST_ALIASES:
            return {"type": "rest"}
        if lowered in DODGE_ALIASES:
            return {"type": "dodge"}
        if lowered in BLOCK_ALIASES:
            return {"type": "block"}
        if lowered in RESIST_ALIASES:
            return {"type": "resist"}
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
        for prefix in TALK_PREFIXES:
            if lowered.startswith(prefix):
                target = text[len(prefix):].strip()
                return {"type": "talk_npc", "target": target} if target else {"type": "invalid"}
        for prefix in EQUIP_PREFIXES:
            if lowered.startswith(prefix):
                target = text[len(prefix):].strip()
                return {"type": "equip", "target": target} if target else {"type": "invalid"}
        for prefix in UNEQUIP_PREFIXES:
            if lowered.startswith(prefix):
                target = text[len(prefix):].strip()
                return {"type": "unequip", "target": target} if target else {"type": "invalid"}
        for prefix in SAY_PREFIXES:
            if lowered.startswith(prefix):
                body = text[len(prefix):].strip()
                return {"type": "say", "body": body} if body else {"type": "invalid"}
        return {"type": "unknown"}


    def attempt_move(player, direction):
        """Unica logica autoritativa de movimiento. Devuelve
        (accepted, previous_room_id, new_room_id_or_None, reason_or_None).

        De paso actualiza el mapa progresivo (GAMEPLAY.md 23: la sala de
        destino queda visitada y la ruta recorrida), coloca una criatura si
        la sala de destino puede tenerla y todavia no hay ninguna activa
        (VT-NAR-003), y otorga el hito de regreso si corresponde."""
        previous_room = player["room"]
        room = world.get_room(previous_room)
        destination = room["exits"].get(direction) if room else None
        if not destination:
            return False, previous_room, None, "No puedes ir en esa dirección."
        store.move_player(path, player["id"], destination, direction)
        store.mark_visited(path, player["id"], destination)
        store.mark_route_traversed(path, player["id"], previous_room, destination)
        encounter_creature = world.get_room_encounter(destination)
        if (encounter_creature and not store.get_encounter(path, player["id"], destination)
                and store.creature_available(path, player["id"], destination)):
            creature = creatures.get_creature(encounter_creature)
            store.start_encounter(path, player["id"], destination, encounter_creature, creature["hp"])
        if (destination == "valdren_centro"
                and store.has_discovery(path, player["id"], "lindero_roto")
                and not store.has_discovery(path, player["id"], "regreso_valdren_lindero")):
            discovery = world.get_discovery("regreso_valdren_lindero")
            store.award_discovery(path, player["id"], "regreso_valdren_lindero",
                                   discovery["category"], discovery["reference_level"])
        return True, previous_room, destination, None

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
        if discovery_key:
            discovery = world.get_discovery(discovery_key)
            is_new, xp_amount, xp_state = store.award_discovery(
                path, player["id"], discovery_key, discovery["category"], discovery["reference_level"])
            if is_new:
                awarded_message = f"{discovery['message']} (+{xp_amount} XP)"
                level_message = _level_up_message(xp_state)
                if level_message:
                    awarded_message = f"{awarded_message} {level_message}"
        return text, awarded_message

    def attempt_evaluate(player):
        """GAMEPLAY.md 22.11: solo funciona sobre un objetivo visible (la
        criatura activa de la sala) y nunca revela numeros."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
            return None, "No hay ninguna criatura visible para evaluar."
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        equipment = _equipment(player)
        cg_player = combat.competencia_general(player["level"])
        cg_enemy = combat.competencia_general(creature["reference_level"])
        player_dps = combat.expected_dps(attrs["destreza"], attrs["percepcion"], attrs["fuerza"],
                                          cg_player, cg_enemy, base_arma=equipment["weapon_base_damage"])
        enemy_dps = combat.fixed_expected_dps(creature["precision"], creature["damage"])
        category = combat.encounter_category(player_dps, player["hp_current"], enemy_dps, creature["hp"])
        return creature["name"], f"{creature['name']} {EVALUATE_TEXT[category]}."

    def attempt_attack(player, rng=None):
        """Una ronda de combate real (golpe del jugador y, si la criatura
        sobrevive, contragolpe). Aplica fatiga/heridas segun GAMEPLAY.md 24
        (coste de fatiga del ataque, penalizaciones de fatiga/herida sobre
        el propio golpe, disparador de herida por el golpe recibido).
        Devuelve un dict con 'outcome'
        ('no_target'|'victory'|'ongoing'|'defeat') y 'messages'."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
            return {"outcome": "no_target", "messages": ["No hay ninguna criatura para atacar aquí."]}
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

        player_hits, player_damage = combat.resolve_attack_roll(
            attrs["destreza"], attrs["percepcion"], attrs["fuerza"], cg_player, cg_enemy, rng=rng,
            base_arma=equipment["weapon_base_damage"],
            accuracy_penalty=accuracy_penalty, damage_multiplier=damage_multiplier)
        messages = []
        if player_hits:
            messages.append(f"Golpeas a {creature['name']} por {round(player_damage)} de daño.")
        else:
            messages.append(f"Fallas tu ataque contra {creature['name']}.")
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

        store.update_encounter(path, player["id"], player["room"], hp_current=creature_hp)

        enemy_hits, enemy_damage = combat.resolve_fixed_attack_roll(
            creature["precision"], creature["damage"], rng=rng)
        new_wound = wound
        if enemy_hits:
            enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
            messages.append(f"{creature['name']} te golpea por {round(enemy_damage)} de daño.")
            new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
            if new_wound != wound:
                messages.append(f"Sufres una herida {new_wound}.")
        else:
            messages.append(f"{creature['name']} falla su ataque.")
        player_hp = player["hp_current"] - (enemy_damage if enemy_hits else 0)

        if player_hp <= 0:
            store.clear_encounter(path, player["id"], player["room"])
            respawn = combat.respawn_state(player["hp_max"])
            respawn_wound_value = combat.respawn_wound(new_wound)
            store.update_combat_state(path, player["id"], hp_current=respawn["hp_current"],
                                       fatigue=respawn["fatigue"], wound=respawn_wound_value,
                                       room=SAFE_ROOM_ID)
            messages.append(f"{creature['name']} te derrota. {RESPAWN_MESSAGE}")
            return {"outcome": "defeat", "messages": messages}

        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "ongoing", "messages": messages}

    def attempt_flee(player, rng=None):
        """GAMEPLAY.md 20.10 y 24.3 (coste de fatiga del intento). Si tiene
        exito, retrocede por la salida que lleva de vuelta hacia Valdren; si
        falla, la criatura tiene una oportunidad de golpear."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
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
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            messages = [f"Consigues alejarte de {creature['name']}."]
            if retreat_direction:
                attempt_move(player, retreat_direction)
            return {"outcome": "success", "messages": messages}

        store.update_encounter(path, player["id"], player["room"],
                                failed_flee_attempts=encounter["failed_flee_attempts"] + 1)
        enemy_hits, enemy_damage = combat.resolve_fixed_attack_roll(
            creature["precision"], creature["damage"], rng=rng)
        messages = [f"No logras huir de {creature['name']}."]
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            return {"outcome": "failed", "messages": messages}
        enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
        messages.append(f"{creature['name']} te golpea por {round(enemy_damage)} de daño mientras intentas escapar.")
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
        player_hp = player["hp_current"] - enemy_damage
        if player_hp <= 0:
            store.clear_encounter(path, player["id"], player["room"])
            respawn = combat.respawn_state(player["hp_max"])
            respawn_wound_value = combat.respawn_wound(new_wound)
            store.update_combat_state(path, player["id"], hp_current=respawn["hp_current"],
                                       fatigue=respawn["fatigue"], wound=respawn_wound_value,
                                       room=SAFE_ROOM_ID)
            messages.append(f"{creature['name']} te derrota. {RESPAWN_MESSAGE}")
            return {"outcome": "defeat", "messages": messages}
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_dodge(player, rng=None):
        """GAMEPLAY.md 20.5/24.2/24.3: sustituye el ataque básico del
        jugador por un intento de esquivar el golpe entrante de la
        criatura. Reduce la probabilidad de que ese golpe conecte; si
        conecta igual, el daño es el normal (esquivar no reduce daño)."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
            return {"outcome": "no_target", "messages": ["No hay ningún ataque que esquivar aquí."]}
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        equipment = _equipment(player)
        wound = player["wound"]
        fatigue = min(100, player["fatigue"] + combat.fatigue_gained(
            "esquivar", attrs["resistencia"], wound, armor_reduction=equipment["armor_reduction"]))
        accuracy_penalty = combat.combined_accuracy_penalty(player["fatigue"], wound)
        rng = rng or random.Random()
        enemy_hits, enemy_damage = combat.resolve_dodged_attack_roll(
            creature["precision"], creature["damage"], attrs["agilidad"], attrs["percepcion"],
            accuracy_penalty=accuracy_penalty, rng=rng)
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            return {"outcome": "success", "messages": [f"Esquivas el ataque de {creature['name']}."]}
        enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
        messages = [f"No logras esquivar y {creature['name']} te golpea por {round(enemy_damage)} de daño."]
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
        player_hp = player["hp_current"] - enemy_damage
        if player_hp <= 0:
            store.clear_encounter(path, player["id"], player["room"])
            respawn = combat.respawn_state(player["hp_max"])
            respawn_wound_value = combat.respawn_wound(new_wound)
            store.update_combat_state(path, player["id"], hp_current=respawn["hp_current"],
                                       fatigue=respawn["fatigue"], wound=respawn_wound_value,
                                       room=SAFE_ROOM_ID)
            messages.append(f"{creature['name']} te derrota. {RESPAWN_MESSAGE}")
            return {"outcome": "defeat", "messages": messages}
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_resist(player, rng=None):
        """GAMEPLAY.md 20.5/24.2/24.3: sustituye el ataque básico por
        resistir el golpe entrante. No cambia la probabilidad de ser
        golpeado; si el golpe conecta, reduce su daño según Resistencia."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
            return {"outcome": "no_target", "messages": ["No hay ningún golpe que resistir aquí."]}
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        equipment = _equipment(player)
        wound = player["wound"]
        fatigue = min(100, player["fatigue"] + combat.fatigue_gained(
            "resistir", attrs["resistencia"], wound, armor_reduction=equipment["armor_reduction"]))
        rng = rng or random.Random()
        enemy_hits, enemy_damage = combat.resolve_resisted_attack_roll(
            creature["precision"], creature["damage"], attrs["resistencia"], rng=rng)
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            return {"outcome": "success", "messages": [f"Te preparas y {creature['name']} falla su ataque."]}
        enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
        messages = [f"Resistes el golpe de {creature['name']}, que aun así te hace "
                    f"{round(enemy_damage)} de daño."]
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
        player_hp = player["hp_current"] - enemy_damage
        if player_hp <= 0:
            store.clear_encounter(path, player["id"], player["room"])
            respawn = combat.respawn_state(player["hp_max"])
            respawn_wound_value = combat.respawn_wound(new_wound)
            store.update_combat_state(path, player["id"], hp_current=respawn["hp_current"],
                                       fatigue=respawn["fatigue"], wound=respawn_wound_value,
                                       room=SAFE_ROOM_ID)
            messages.append(f"{creature['name']} te derrota. {RESPAWN_MESSAGE}")
            return {"outcome": "defeat", "messages": messages}
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_block(player, rng=None):
        """GAMEPLAY.md 20.5: requiere arma/escudo/objeto adecuado -- ver
        `_can_block`, que desde el Issue #57 consulta el arma equipada
        real."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
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
        enemy_hits, enemy_damage = combat.resolve_blocked_attack_roll(
            creature["precision"], creature["damage"], attrs["destreza"], rng=rng)
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            return {"outcome": "success", "messages": [f"Bloqueas el ataque de {creature['name']}."]}
        enemy_damage = combat.apply_armor_reduction(enemy_damage, equipment["armor_reduction"])
        messages = [f"Bloqueas parcialmente a {creature['name']}, que aun así te hace "
                    f"{round(enemy_damage)} de daño."]
        new_wound = combat.worse_wound(wound, combat.wound_from_hit(enemy_damage, player["hp_max"]))
        if new_wound != wound:
            messages.append(f"Sufres una herida {new_wound}.")
        player_hp = player["hp_current"] - enemy_damage
        if player_hp <= 0:
            store.clear_encounter(path, player["id"], player["room"])
            respawn = combat.respawn_state(player["hp_max"])
            respawn_wound_value = combat.respawn_wound(new_wound)
            store.update_combat_state(path, player["id"], hp_current=respawn["hp_current"],
                                       fatigue=respawn["fatigue"], wound=respawn_wound_value,
                                       room=SAFE_ROOM_ID)
            messages.append(f"{creature['name']} te derrota. {RESPAWN_MESSAGE}")
            return {"outcome": "defeat", "messages": messages}
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_rest(player):
        """GAMEPLAY.md 24.8: accion explicita `descansar`, solo fuera de
        combate. En `SAFE_ROOM_ID` (Issue #46) usa la recuperacion segura
        completa de 24.9 en vez del descanso de campo basico."""
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes descansar con una criatura cerca."]}
        in_safe_room = player["room"] == SAFE_ROOM_ID
        already_recovered = (player["hp_current"] >= player["hp_max"] and player["fatigue"] <= 0
                              and (not in_safe_room or player["wound"] == "ninguna"))
        if already_recovered:
            return {"outcome": "no_op", "messages": ["Ya estás descansado."]}
        if in_safe_room:
            result = combat.safe_recovery_result(player["hp_max"], player["wound"])
            store.update_combat_state(path, player["id"], hp_current=result["hp_current"],
                                       fatigue=result["fatigue"], wound=result["wound"])
            return {"outcome": "rested", "messages": [
                f"{SAFE_RECOVERY_MESSAGE} (HP {result['hp_current']}/{round(player['hp_max'])}, "
                f"fatiga {result['fatigue']})."]}
        result = combat.rest_result(player["hp_current"], player["hp_max"], player["fatigue"],
                                     player["attr_resistencia"], player["wound"])
        store.update_combat_state(path, player["id"], hp_current=result["hp_current"], fatigue=result["fatigue"])
        return {"outcome": "rested", "messages": [
            f"Descansas un momento y recuperas fuerzas (HP {result['hp_current']}/{round(player['hp_max'])}, "
            f"fatiga {result['fatigue']})."]}

    def attempt_equip(player, target_text):
        """GAMEPLAY.md 32.3: `equipar <objeto>`. Solo fuera de combate,
        requiere poseer el objeto y, si el catálogo lo exige, tener la
        validación de Forja completa (32.4)."""
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes equipar nada con una criatura cerca."]}
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
        """GAMEPLAY.md 32.3: `desequipar <objeto>`. Solo fuera de combate;
        devuelve el objeto a poseído/no activo, sin coste."""
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes desequipar nada con una criatura cerca."]}
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

    def attempt_choose_species(player, species_id):
        """Devuelve (accepted, species_or_None, room_or_None, reason_or_None).
        La atomicidad real la garantiza store.set_species (rowcount), no una
        lectura previa de player["species"]: asi dos POST casi simultaneos no
        pueden terminar ambos con accepted=True."""
        if species_id not in world.SPECIES_IDS:
            return False, None, None, "Elige una especie de la lista."
        room_id = world.get_starting_room_for_species(species_id)
        updated = store.set_species(path, player["id"], species_id, room_id)
        if not updated:
            return False, None, None, "Ya elegiste tu especie."
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

    @app.get("/")
    def index():
        room = None
        if g.player is not None and g.player["status"] == "approved" and g.player["room"]:
            room = room_view(g.player["room"], g.player["id"])
        return render_template("entry.html", player=g.player, species_list=world.SPECIES, room=room)

    @app.post("/register")
    def register():
        if not store.allow_attempt(path, request.remote_addr or "unknown"):
            return render_template("entry.html", error="Demasiados intentos. Espera un minuto."), 429
        username = request.form.get("username", "").strip().lower()
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        if (not re.fullmatch(r"[a-z0-9_]{3,32}", username)
                or not 1 <= len(name) <= 60 or any(ord(c) < 32 for c in name)
                or not 8 <= len(password) <= 128):
            return render_template("entry.html", error="Revisa el nombre, usuario y contraseña según las indicaciones."), 400
        try:
            token = store.register(path, username, name, generate_password_hash(password), session.get("token"))
        except sqlite3.IntegrityError:
            return render_template("entry.html", error="Ese usuario no está disponible."), 409
        return establish_session(token)

    @app.post("/login")
    def login():
        if not store.allow_attempt(path, request.remote_addr or "unknown"):
            return render_template("entry.html", error="Demasiados intentos. Espera un minuto."), 429
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        if len(password) > 128 or len(username) > 32:
            abort(400)
        with store.connect(path) as db:
            player = db.execute("SELECT id, password_hash FROM players WHERE username = ?", (username,)).fetchone()
            valid = check_password_hash(player["password_hash"] if player else dummy_hash, password)
            if not valid or player is None:
                return render_template("entry.html", error="Usuario o contraseña incorrectos."), 401
            token = store.record_access(db, player["id"], "login", session.get("token"))
        return establish_session(token)

    @app.post("/logout")
    def logout():
        with store.connect(path) as db:
            db.execute("DELETE FROM sessions WHERE token_hash = ?", (store.digest(session.get("token", "")),))
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

    @app.post("/move")
    def move():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        accepted, _previous, _new, reason = attempt_move(g.player, request.form.get("direction", ""))
        if not accepted:
            room_data = room_view(g.player["room"], g.player["id"])
            return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                                   room=room_data, error=reason), 400
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
            accepted, _previous, _new, reason = attempt_move(g.player, intent["direction"])
            if not accepted:
                room_data = room_view(g.player["room"], g.player["id"])
                return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                                       room=room_data, error=reason), 400
            return redirect(url_for("index"), code=303)
        if intent["type"] == "look":
            return redirect(url_for("index"), code=303)
        if intent["type"] == "say":
            store.add_message(path, g.player["room"], g.player["id"], intent["body"])
            return redirect(url_for("index"), code=303)

        if intent["type"] == "inspect":
            target = intent["target"] or "el lugar"
            result = resolve_inspect(g.player, intent["target"])
            if result:
                text, awarded = result
                message = f"{text} {awarded}" if awarded else text
            else:
                message = f"Inspección registrada para {target}. No hay detalle adicional autorizado todavía."
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(g.player["room"], g.player["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=message), 200
        if intent["type"] == "evaluate":
            _name, message = attempt_evaluate(g.player)
            room_data = room_view(g.player["room"], g.player["id"])
            return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                                   room=room_data, error=message), 200
        if intent["type"] == "attack":
            result = attempt_attack(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "flee":
            result = attempt_flee(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "rest":
            result = attempt_rest(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "dodge":
            result = attempt_dodge(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "resist":
            result = attempt_resist(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
        if intent["type"] == "block":
            result = attempt_block(g.player)
            player_now = store.player_for_token(path, session.get("token"))
            room_data = room_view(player_now["room"], player_now["id"])
            return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                                   room=room_data, error=" ".join(result["messages"])), 200
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
        if intent["type"] == "talk_npc":
            room_data = room_view(g.player["room"], g.player["id"])
            return render_template(
                "entry.html", player=g.player, species_list=world.SPECIES, room=room_data,
                error="La conversación con NPC tiene contrato separado, pero todavía no hay NPC activo."
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
        town = world.get_room(room_id)
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
            accepted, previous_room, new_room, reason = attempt_move(g.player, intent["direction"])
            current_room_id = new_room if accepted else previous_room
            return jsonify(
                accepted=accepted,
                intent="move",
                previous_room=previous_room,
                current_room=room_view(current_room_id, g.player["id"]),
                reason=reason,
            ), (200 if accepted else 400)
        if kind == "look":
            return jsonify(
                accepted=True,
                intent="look",
                current_room=room_view(g.player["room"], g.player["id"]),
            )
        if kind == "say":
            store.add_message(path, g.player["room"], g.player["id"], intent["body"])
            return jsonify(accepted=True, intent="say")
        if kind == "inspect":
            result = resolve_inspect(g.player, intent["target"])
            text, awarded = result if result else (None, None)
            return jsonify(
                accepted=True,
                intent="inspect",
                verb=intent["verb"],
                target=intent["target"],
                detail=text,
                message=(text or "No hay detalle adicional autorizado todavía."),
                discovery=awarded,
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
                player=dict(player_now) if player_now else None,
                current_room=room_view(player_now["room"], player_now["id"]) if player_now else None,
            )
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
        if kind == "talk_npc":
            return jsonify(
                accepted=False,
                intent="talk_npc",
                npc=intent["target"],
                reason="No hay NPC activo para conversación todavía.",
            ), 409
        return jsonify(
            accepted=False,
            intent=kind,
            reason="Comando no reconocido. Para chat usa: decir <texto>.",
        ), 400

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
        accepted, previous_room, new_room, reason = attempt_move(g.player, direction)
        current_room_id = new_room if accepted else previous_room
        return jsonify(
            accepted=accepted,
            previous_room=previous_room,
            reason=reason,
            current_room=room_view(current_room_id, g.player["id"]),
        ), (200 if accepted else 400)

    @app.get("/api/character")
    def api_character():
        """Estado de personaje jugable (GAMEPLAY.md 20-22): nivel, XP, PA sin
        gastar, HP, fatiga, herida, atributos y descubrimientos -- para el
        panel Personaje que pide Issue #43 (P1)."""
        error = api_player_state(g.player)
        if error:
            return error
        return jsonify(
            species=g.player["species"], player_class=g.player["player_class"],
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
            in_combat=bool(g.player["room"] and store.get_encounter(path, g.player["id"], g.player["room"])),
            discoveries=store.list_discoveries(path, g.player["id"]),
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
            armor_reduction_total=equipment["armor_reduction"],
            carga_multiplier=combat.armor_load_multiplier(equipment["armor_reduction"]),
        )

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
        result = attempt_attack(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), 200

    @app.post("/flee")
    def flee():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        result = attempt_flee(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), 200

    @app.post("/dodge")
    def dodge():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        result = attempt_dodge(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), 200

    @app.post("/resist")
    def resist():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        result = attempt_resist(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), 200

    @app.post("/block")
    def block():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        result = attempt_block(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), 200

    @app.post("/evaluate")
    def evaluate():
        require_approved_player()
        if not character_ready(g.player):
            abort(403)
        _name, message = attempt_evaluate(g.player)
        room_data = room_view(g.player["room"], g.player["id"])
        return render_template("entry.html", player=g.player, species_list=world.SPECIES,
                               room=room_data, error=message), 200

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
