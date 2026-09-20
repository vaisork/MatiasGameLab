from datetime import timedelta
import hmac
import os
from pathlib import Path
import re
import secrets
import sqlite3

from flask import Flask, abort, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from . import store


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

    @app.before_request
    def prepare_request():
        # Even the anonymous form has a signed, random anti-CSRF token.
        if request.method == "POST":
            expected = session.get("csrf", "")
            supplied = request.form.get("csrf", "")
            if not expected or not hmac.compare_digest(expected.encode(), supplied.encode()):
                abort(400, "Formulario vencido. Recarga la página.")
        if request.endpoint == "health":
            return
        session.setdefault("csrf", secrets.token_urlsafe(32))
        g.player = store.player_for_token(path, session.get("token"))

    @app.after_request
    def headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; "
            "frame-ancestors 'none'; base-uri 'none'")
        return response

    def establish_session(token):
        session.clear()
        session.permanent = True
        session["csrf"] = secrets.token_urlsafe(32)
        session["token"] = token
        return redirect(url_for("index"), code=303)

    @app.get("/")
    def index():
        return render_template("entry.html", player=g.player)

    @app.post("/register")
    def register():
        if not store.allow_attempt(path, request.remote_addr or "unknown"):
            return render_template("entry.html", error="Demasiados intentos. Espera un minuto."), 429
        username = request.form.get("username", "").strip().lower()
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        if (not re.fullmatch(r"[a-z0-9_]{3,32}", username)
                or not 1 <= len(name) <= 60 or any(ord(c) < 32 for c in name)
                or not 12 <= len(password) <= 128):
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

    @app.get("/api/me")
    def me():
        if g.player is None:
            abort(401)
        return jsonify(player=dict(g.player), world_status="under_construction")

    @app.get("/healthz")
    def health():
        with store.connect(path) as db:
            db.execute("SELECT id FROM players LIMIT 1").fetchone()
            version = db.execute("PRAGMA user_version").fetchone()[0]
        return jsonify(status="ok", schema_version=version)

    return app
