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

from . import combat, creatures, dm_auth, store, world

# NECESIDAD NARRATIVA pendiente (Issue #46): el Narrador todavia no confirmo
# el punto concreto de Valdren que funciona como reaparicion tras morir
# (GAMEPLAY.md 20.9) ni como recuperacion segura (24.9) para VT-NAR-003. Se
# usa el centro del pueblo -- ya existente como punto de entrada de especie,
# no inventado para esta tarea -- como marcador tecnico operativo mientras
# tanto. Esto NO es una decision narrativa de Desarrollo: en cuanto Issue
# #46 entregue el ID, solo hay que cambiar esta constante.
PENDING_SAFE_ROOM_ID = "valdren_centro"

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

# Biblioteca de arte HTML (vintage-telnet/assets/html-ui/), servida explícitamente en vez de
# habilitar una carpeta estática general -- mantiene el resto del árbol del repo fuera de HTTP.
HTML_UI_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "html-ui"


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
        if request.endpoint in ("health", "html_ui_assets"):
            return
        session.setdefault("csrf", secrets.token_urlsafe(32))
        g.player = store.player_for_token(path, session.get("token"))
        g.dm = bool(session.get("dm"))

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
            f"script-src 'nonce-{nonce}'; form-action 'self'; "
            "frame-ancestors 'none'; base-uri 'none'")
        return response

    def establish_session(token):
        session.clear()
        session.permanent = True
        session["csrf"] = secrets.token_urlsafe(32)
        session["token"] = token
        return redirect(url_for("index"), code=303)

    def require_approved_player():
        if g.player is None:
            abort(401)
        if g.player["status"] != "approved":
            abort(403)

    def require_dm():
        if not g.dm:
            abort(403)

    def room_view(room_id, player_id):
        others = store.players_in_room(path, room_id, exclude_id=player_id)
        view = world.describe_room(room_id, [p["name"] for p in others])
        view["messages"] = store.recent_messages(path, room_id)
        encounter = store.get_encounter(path, player_id, room_id)
        if encounter:
            creature = creatures.get_creature(encounter["creature_id"])
            view["encounter"] = {
                "creature_id": encounter["creature_id"],
                "name": creature["name"],
                "hp_current": max(0, round(encounter["hp_current"])),
                "hp_max": creature["hp"],
            }
        else:
            view["encounter"] = None
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
        store.move_player(path, player["id"], destination)
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

    def resolve_inspect(player, target):
        """Devuelve (texto, mensaje_de_descubrimiento_o_None) si hay un
        texto canonico de NARRATIVE.md para ese objetivo en esta sala, o
        None si no hay nada especifico definido (el llamador decide el
        mensaje generico de respaldo)."""
        normalized = _normalize(target)
        if not normalized:
            return None
        text = world.get_examine_text(player["room"], normalized)
        if text is None:
            return None
        discovery_key = None
        if player["room"] == "valdren_camino_parcela" and normalized in ("tallos", "monticulos"):
            discovery_key = "senales_mordelinde"
        elif player["room"] == "valdren_camino_lindero" and normalized in ("cerca", "huellas"):
            discovery_key = "lindero_roto"
        awarded_message = None
        if discovery_key:
            discovery = world.get_discovery(discovery_key)
            is_new, xp_amount = store.award_discovery(
                path, player["id"], discovery_key, discovery["category"], discovery["reference_level"])
            if is_new:
                awarded_message = f"{discovery['message']} (+{xp_amount} XP)"
        return text, awarded_message

    def attempt_evaluate(player):
        """GAMEPLAY.md 22.11: solo funciona sobre un objetivo visible (la
        criatura activa de la sala) y nunca revela numeros."""
        encounter = store.get_encounter(path, player["id"], player["room"])
        if not encounter:
            return None, "No hay ninguna criatura visible para evaluar."
        creature = creatures.get_creature(encounter["creature_id"])
        attrs = _attributes(player)
        cg_player = combat.competencia_general(player["level"])
        cg_enemy = combat.competencia_general(creature["reference_level"])
        player_dps = combat.expected_dps(attrs["destreza"], attrs["percepcion"], attrs["fuerza"],
                                          cg_player, cg_enemy)
        enemy_dps = combat.expected_dps(creature["destreza"], creature["percepcion"], creature["fuerza"],
                                         cg_enemy, cg_player, base_arma=creature["base_ataque"])
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
        cg_player = combat.competencia_general(player["level"])
        cg_enemy = combat.competencia_general(creature["reference_level"])

        wound = player["wound"]
        fatigue = min(100, player["fatigue"]
                      + combat.fatigue_gained("ataque_basico", attrs["resistencia"], wound))
        accuracy_penalty = combat.combined_accuracy_penalty(player["fatigue"], wound)
        damage_multiplier = combat.combined_damage_multiplier(player["fatigue"], wound)

        player_hits, player_damage = combat.resolve_attack_roll(
            attrs["destreza"], attrs["percepcion"], attrs["fuerza"], cg_player, cg_enemy, rng=rng,
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
                                              cg_player, cg_enemy)
            enemy_dps = combat.expected_dps(creature["destreza"], creature["percepcion"], creature["fuerza"],
                                             cg_enemy, cg_player, base_arma=creature["base_ataque"])
            category = combat.encounter_category(player_dps, player["hp_current"], enemy_dps, creature["hp"])
            xp_amount = combat.combat_xp(creature["reference_level"], category, player["level"],
                                          is_first, repeats)
            xp_state = store.award_xp(path, player["id"], xp_amount)
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            messages.append(f"¡{creature['name']} cae derrotado! Ganas {xp_amount} XP.")
            if is_first:
                messages.append(f"Primera vez que superas a un {creature['name']}: bono de familia incluido.")
            if xp_state["levels_gained"]:
                messages.append(f"¡Subes a nivel {xp_state['level']}!")
            return {"outcome": "victory", "messages": messages}

        store.update_encounter(path, player["id"], player["room"], hp_current=creature_hp)

        enemy_hits, enemy_damage = combat.resolve_attack_roll(
            creature["destreza"], creature["percepcion"], creature["fuerza"],
            cg_enemy, cg_player, base_arma=creature["base_ataque"], rng=rng)
        new_wound = wound
        if enemy_hits:
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
                                       room=PENDING_SAFE_ROOM_ID)
            messages.append(f"{creature['name']} te derrota. Despiertas de vuelta en Valdren.")
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
        fatigue = min(100, player["fatigue"] + combat.fatigue_gained("huir", player["attr_resistencia"], wound))
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
        enemy_hits, enemy_damage = combat.resolve_attack_roll(
            creature["destreza"], creature["percepcion"], creature["fuerza"],
            combat.competencia_general(creature["reference_level"]), combat.competencia_general(player["level"]),
            base_arma=creature["base_ataque"], rng=rng)
        messages = [f"No logras huir de {creature['name']}."]
        if not enemy_hits:
            store.update_combat_state(path, player["id"], fatigue=round(fatigue))
            return {"outcome": "failed", "messages": messages}
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
                                       room=PENDING_SAFE_ROOM_ID)
            messages.append(f"{creature['name']} te derrota. Despiertas de vuelta en Valdren.")
            return {"outcome": "defeat", "messages": messages}
        store.update_combat_state(path, player["id"], hp_current=player_hp,
                                   fatigue=round(fatigue), wound=new_wound)
        return {"outcome": "failed", "messages": messages}

    def attempt_rest(player):
        """GAMEPLAY.md 24.8: accion explicita `descansar`, solo fuera de
        combate. Si la sala esta marcada como recuperacion segura (24.9),
        usa esa version superior en vez del descanso de campo basico --
        hoy ninguna sala lo esta todavia (NECESIDAD NARRATIVA pendiente,
        Issue #46), asi que siempre cae en el descanso de campo v1."""
        if store.get_encounter(path, player["id"], player["room"]):
            return {"outcome": "blocked", "messages": ["No puedes descansar con una criatura cerca."]}
        if player["hp_current"] >= player["hp_max"] and player["fatigue"] <= 0:
            return {"outcome": "no_op", "messages": ["Ya estás descansado."]}
        result = combat.rest_result(player["hp_current"], player["hp_max"], player["fatigue"],
                                     player["attr_resistencia"], player["wound"])
        store.update_combat_state(path, player["id"], hp_current=result["hp_current"], fatigue=result["fatigue"])
        return {"outcome": "rested", "messages": [
            f"Descansas un momento y recuperas fuerzas (HP {result['hp_current']}/{round(player['hp_max'])}, "
            f"fatiga {result['fatigue']})."]}

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

    @app.post("/move")
    def move():
        require_approved_player()
        if g.player["species"] is None:
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
        if g.player["species"] is None:
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
        if g.player["species"] is None:
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

    @app.post("/api/intent")
    def api_intent():
        """Contrato estructurado para intención de terminal."""
        error = api_player_state(g.player)
        if error:
            return error
        if g.player["species"] is None:
            return jsonify(error="species_required"), 409
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
            level=g.player["level"], xp=g.player["xp"],
            xp_to_next=combat.xp_for_next_level(g.player["level"]),
            pa_unspent=g.player["pa_unspent"],
            hp_current=g.player["hp_current"], hp_max=g.player["hp_max"],
            fatigue=g.player["fatigue"], wound=g.player["wound"],
            attributes=_attributes(g.player),
            discoveries=store.list_discoveries(path, g.player["id"]),
        )

    @app.get("/api/map")
    def api_map():
        """Mapa progresivo (GAMEPLAY.md 23): solo lo que este personaje
        visito/recorrio de verdad, nunca el mundo completo de produccion."""
        error = api_player_state(g.player)
        if error:
            return error
        return jsonify(**store.get_map_state(path, g.player["id"]))

    @app.post("/attack")
    def attack():
        require_approved_player()
        if g.player["species"] is None:
            abort(403)
        result = attempt_attack(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), 200

    @app.post("/flee")
    def flee():
        require_approved_player()
        if g.player["species"] is None:
            abort(403)
        result = attempt_flee(g.player)
        player_now = store.player_for_token(path, session.get("token"))
        room_data = room_view(player_now["room"], player_now["id"])
        return render_template("entry.html", player=player_now, species_list=world.SPECIES,
                               room=room_data, error=" ".join(result["messages"])), 200

    @app.post("/evaluate")
    def evaluate():
        require_approved_player()
        if g.player["species"] is None:
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

    @app.get("/assets/html-ui/<path:filename>")
    def html_ui_assets(filename):
        return send_from_directory(HTML_UI_ASSETS_DIR, filename)

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
