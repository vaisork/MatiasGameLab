"""Pruebas autoritativas para PRESENCE-CHAT-01 (#376 / GAMEPLAY.md 26.8).

Valida:
1. Co-presencia en la misma sala sin auto-inclusión.
2. Salida explícita por movimiento: desaparición inmediata en el siguiente refresh.
3. Desconexión abrupta / abandono de pestaña: expiración tras 30 s de inactividad.
4. Reconexión / actividad posterior: reaparición inmediata sin duplicados.
5. Logout explícito: desaparición inmediata.
6. Cambio de personaje: desaparición inmediata.
7. Revocación de sesiones: desaparición inmediata.
8. Chat activo: sólo mensajes de los últimos 10 minutos (600 s) por defecto.
9. Mensajes anteriores (>10 min): archivados en almacenamiento / consulta histórica.
10. Aislamiento de sala: cambiar de sala no contamina la nueva con mensajes anteriores.
11. Regreso a sala: no resucita mensajes antiguos fuera de la ventana de 10 min.
"""

from datetime import datetime, timedelta, timezone
import os
import shutil
import re
import tempfile
import time
import unittest
from unittest.mock import patch

from server.app import create_app
from server import store, world


class PresenceChatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.path = self.app.config["DATABASE"]
        self.client_a = self.app.test_client()
        self.client_b = self.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def post(self, client, route, data=None):
        page = client.get("/").get_data(as_text=True)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
        return client.post(route, data={**(data or {}), "csrf": csrf})

    def _setup_character(self, client, username, name, species="humano", player_class="sombra"):
        res = self.post(client, "/register", {"username": username, "name": name, "password": "password123"})
        self.assertEqual(res.status_code, 303)
        store.set_status(self.path, username, "approved")
        # Elegir especie y clase
        res_sp = self.post(client, "/species", {"species": species})
        self.assertEqual(res_sp.status_code, 303)
        res_cl = self.post(client, "/class", {"player_class": player_class})
        self.assertEqual(res_cl.status_code, 303)
        # Salir al centro comunal (valdren_centro)
        res_mv = self.post(client, "/move", {"direction": "south"})
        self.assertIn(res_mv.status_code, (200, 303))

    def test_presence_same_room_mutual_visibility_and_no_self(self):
        """1. A y B en la misma sala se ven mutuamente y ninguno se ve a sí mismo."""
        self._setup_character(self.client_a, "alice", "Alice")
        self._setup_character(self.client_b, "bob", "Bob")

        room_a = self.client_a.get("/api/room").json["room"]
        self.assertEqual(room_a["id"], "valdren_centro")
        self.assertIn("Bob", room_a["others_present"])
        self.assertNotIn("Alice", room_a["others_present"])

        room_b = self.client_b.get("/api/room").json["room"]
        self.assertEqual(room_b["id"], "valdren_centro")
        self.assertIn("Alice", room_b["others_present"])
        self.assertNotIn("Bob", room_b["others_present"])

    def test_presence_explicit_room_move_immediate_departure(self):
        """2. Salida explícita por movimiento: B sale y A deja de verlo inmediatamente."""
        self._setup_character(self.client_a, "alice", "Alice")
        self._setup_character(self.client_b, "bob", "Bob")

        # Bob se mueve al oeste
        res = self.post(self.client_b, "/move", {"direction": "west"})
        self.assertIn(res.status_code, (200, 303))

        # En la siguiente lectura de Alice, Bob ya no está
        room_a = self.client_a.get("/api/room").json["room"]
        self.assertNotIn("Bob", room_a["others_present"])

    def test_presence_abrupt_disconnect_timeout_30s(self):
        """3. Desconexión abrupta / abandono de pestaña: expira tras 30 s sin actividad."""
        self._setup_character(self.client_a, "alice", "Alice")
        self._setup_character(self.client_b, "bob", "Bob")

        with store.connect(self.path) as db:
            player_b = store.player_by_username(db, "bob")
        self.assertIsNotNone(player_b)

        now = time.time()
        # Bob fue visto hace 10 s (dentro del margen de 30 s)
        store.touch_presence(self.path, player_b["id"], timestamp=now - 10)
        present = [p["name"] for p in store.players_in_room(self.path, "valdren_centro", now=now)]
        self.assertIn("Bob", present)

        # Bob no envía señales durante 31 s (> 30 s)
        store.touch_presence(self.path, player_b["id"], timestamp=now - 31)
        present_after = [p["name"] for p in store.players_in_room(self.path, "valdren_centro", now=now)]
        self.assertNotIn("Bob", present_after)

        # La vista de Alice refleja que Bob ya no figura
        with patch("time.time", return_value=now):
            room_a = self.client_a.get("/api/room").json["room"]
            self.assertNotIn("Bob", room_a["others_present"])

    def test_presence_reconnect_resumes_without_duplicates(self):
        """4. Tras expirar, una nueva petición de Bob lo reactiva sin duplicados."""
        self._setup_character(self.client_a, "alice", "Alice")
        self._setup_character(self.client_b, "bob", "Bob")

        with store.connect(self.path) as db:
            player_b = store.player_by_username(db, "bob")
        now = time.time()
        # Expirar a Bob
        store.touch_presence(self.path, player_b["id"], timestamp=now - 45)
        present = [p["name"] for p in store.players_in_room(self.path, "valdren_centro", now=now)]
        self.assertNotIn("Bob", present)

        # Bob vuelve a tener foco / realiza polling en t = now
        with patch("time.time", return_value=now):
            self.client_b.get("/api/room")

        # Alice lo vuelve a ver inmediatamente, exactamente una vez
        with patch("time.time", return_value=now):
            room_a = self.client_a.get("/api/room").json["room"]
            self.assertIn("Bob", room_a["others_present"])
            self.assertEqual(room_a["others_present"].count("Bob"), 1)

    def test_presence_explicit_logout_immediate_departure(self):
        """5. Logout explícito de Bob limpia la presencia inmediatamente."""
        self._setup_character(self.client_a, "alice", "Alice")
        self._setup_character(self.client_b, "bob", "Bob")

        # Bob cierra sesión
        res = self.post(self.client_b, "/logout")
        self.assertEqual(res.status_code, 303)

        # Alice consulta y Bob ya no está
        room_a = self.client_a.get("/api/room").json["room"]
        self.assertNotIn("Bob", room_a["others_present"])

    def test_presence_switch_character_immediate_departure(self):
        """6. Cambiar de personaje desvincula la presencia inmediatamente."""
        self._setup_character(self.client_a, "alice", "Alice")
        self._setup_character(self.client_b, "bob", "Bob")

        # Bob cambia de personaje
        res = self.post(self.client_b, "/characters/switch")
        self.assertEqual(res.status_code, 303)

        # Alice consulta y Bob ya no está
        room_a = self.client_a.get("/api/room").json["room"]
        self.assertNotIn("Bob", room_a["others_present"])

    def test_presence_revocation_by_status_immediate(self):
        """7. Revocar sesión por DM/admin limpia la presencia inmediatamente."""
        self._setup_character(self.client_a, "alice", "Alice")
        self._setup_character(self.client_b, "bob", "Bob")

        store.set_status(self.path, "bob", "rejected", revoke_sessions=True)

        room_a = self.client_a.get("/api/room").json["room"]
        self.assertNotIn("Bob", room_a["others_present"])

    def test_active_chat_10_minute_window_and_historical_archive(self):
        """8 & 9. Chat activo solo muestra últimos 10 min; anteriores van a histórico."""
        self._setup_character(self.client_a, "alice", "Alice")
        with store.connect(self.path) as db:
            player_a = store.player_by_username(db, "alice")

        base_time = datetime(2026, 9, 28, 12, 0, 0, tzinfo=timezone.utc)

        # Insertar mensaje viejo (hace 15 minutos)
        with store.connect(self.path) as db:
            db.execute(
                "INSERT INTO room_messages(room, player_id, body, created_at) VALUES (?, ?, ?, ?)",
                ("valdren_centro", player_a["id"], "Mensaje de hace 15 minutos",
                 (base_time - timedelta(minutes=15)).isoformat(timespec="microseconds")),
            )
            # Insertar mensaje reciente (hace 3 minutos)
            db.execute(
                "INSERT INTO room_messages(room, player_id, body, created_at) VALUES (?, ?, ?, ?)",
                ("valdren_centro", player_a["id"], "Mensaje de hace 3 minutos",
                 (base_time - timedelta(minutes=3)).isoformat(timespec="microseconds")),
            )

        # recent_messages a las 12:00
        active_msgs = store.recent_messages(self.path, "valdren_centro", now=base_time)
        bodies = [m["body"] for m in active_msgs]
        self.assertIn("Mensaje de hace 3 minutos", bodies)
        self.assertNotIn("Mensaje de hace 15 minutos", bodies)

        # historical_messages sí incluye el mensaje viejo
        history = store.historical_messages(self.path, "valdren_centro")
        history_bodies = [m["body"] for m in history]
        self.assertIn("Mensaje de hace 15 minutos", history_bodies)
        self.assertIn("Mensaje de hace 3 minutos", history_bodies)

    def test_chat_room_isolation_on_change(self):
        """10. Cambiar de sala no arrastra mensajes activos de la sala anterior."""
        self._setup_character(self.client_a, "alice", "Alice")

        # Alice dice algo en valdren_centro
        res = self.post(self.client_a, "/room/say", {"body": "Hola en centro"})
        self.assertEqual(res.status_code, 303)

        room_view_centro = self.client_a.get("/api/room").json["room"]
        self.assertEqual(room_view_centro["id"], "valdren_centro")
        self.assertIn("Hola en centro", [m["body"] for m in room_view_centro["messages"]])

        # Alice se mueve al oeste (valdren_barrio_artesanos)
        res_mv = self.post(self.client_a, "/move", {"direction": "west"})
        self.assertIn(res_mv.status_code, (200, 303))

        room_view_oeste = self.client_a.get("/api/room").json["room"]
        self.assertNotEqual(room_view_oeste["id"], "valdren_centro")
        self.assertNotIn("Hola en centro", [m["body"] for m in room_view_oeste["messages"]])

    def test_chat_room_return_does_not_resurrect_old_messages(self):
        """11. Volver a una sala no resucita mensajes de horas anteriores como activos."""
        self._setup_character(self.client_a, "alice", "Alice")
        with store.connect(self.path) as db:
            player_a = store.player_by_username(db, "alice")

        t0 = datetime(2026, 9, 28, 8, 0, 0, tzinfo=timezone.utc)
        # Mensaje de hace 2 horas
        with store.connect(self.path) as db:
            db.execute(
                "INSERT INTO room_messages(room, player_id, body, created_at) VALUES (?, ?, ?, ?)",
                ("valdren_centro", player_a["id"], "Mensaje de hace dos horas",
                 t0.isoformat(timespec="microseconds")),
            )

        # 2 horas después (10:00:00)
        t_now = datetime(2026, 9, 28, 10, 0, 0, tzinfo=timezone.utc)
        msgs = store.recent_messages(self.path, "valdren_centro", now=t_now)
        self.assertEqual(len(msgs), 0)


if __name__ == "__main__":
    unittest.main()
