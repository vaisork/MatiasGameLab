"""Pruebas de HOME-CORE (Issue #280 / Issue #114 / GAMEPLAY.md §34).

Cubre:
1. dos personajes de una misma cuenta obtienen hogares distintos;
2. dos cuentas no comparten hogar;
3. personaje nuevo inicia en su hogar después de completar onboarding;
4. salir conduce al pueblo correcto por especie;
5. reconectar dentro del hogar conserva ubicación;
6. salir y reconectar fuera no devuelve automáticamente a casa;
7. no hay encuentro random/fijo;
8. PvP no puede iniciarse dentro;
9. inventario/equipamiento permanece sin nuevo sistema de almacenamiento;
10. personajes existentes con posición válida no son teletransportados;
11. cambio/migración de esquema y reinicio de servidor no destruyen estado vivo.
"""

import os
import re
import tempfile
import unittest
from unittest.mock import patch

from server import combat, encounters, items, store, world
from server.app import create_app


class HomeCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = {
            "TESTING": True,
            "SECRET_KEY": "test-secret-" * 5,
            "DATA_DIR": self.temp.name,
            "SESSION_COOKIE_SECURE": False,
        }
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        try:
            self.temp.cleanup()
        except PermissionError:
            pass

    def csrf(self, client=None):
        cl = client or self.client
        page = cl.get("/").get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', page)
        if match:
            return match[1]
        token_match = re.search(r'name="csrf_token" content="([^"]+)"', page)
        return token_match[1] if token_match else ""

    def post(self, route, data=None, client=None, csrf_path="/"):
        cl = client or self.client
        csrf_val = self.csrf(cl)
        payload = {**(data or {})}
        if "csrf" not in payload:
            payload["csrf"] = csrf_val
        return cl.post(route, data=payload)

    def register_and_approve(self, username="matias", name="Matías", password="una clave de prueba", client=None):
        cl = client or self.client
        self.post("/register", dict(username=username, name=name, password=password), cl)
        store.set_status(self.path, username, "approved")

    def complete_onboarding(self, species="humano", player_class="sombra", client=None):
        cl = client or self.client
        self.post("/species", dict(species=species), cl)
        self.post("/class", dict(player_class=player_class), cl)

    # 1. dos personajes de una misma cuenta obtienen hogares distintos
    def test_two_characters_of_same_account_get_distinct_homes(self):
        self.register_and_approve("cuenta1", name="Personaje Uno")
        self.complete_onboarding("humano", "sombra")
        p1 = self.client.get("/api/me").json["player"]
        self.assertTrue(world.is_home_room(p1["room"]))
        self.assertEqual(p1["room"], world.get_home_room_id(p1["id"]))

        # Crear segundo personaje en la misma cuenta
        self.post("/characters/new", dict(name="Personaje Dos"))
        # Aprobar segundo personaje por su nombre
        with store.connect(self.path) as db:
            p2_row = db.execute("SELECT id, username FROM players WHERE name = 'Personaje Dos'").fetchone()
            p2_id = p2_row["id"]
        store.set_status(self.path, p2_row["username"], "approved")

        # Seleccionar segundo personaje
        self.post("/characters/select", dict(player_id=p2_id))
        self.complete_onboarding("felaryn", "artifice")
        p2 = self.client.get("/api/me").json["player"]
        self.assertTrue(world.is_home_room(p2["room"]))
        self.assertEqual(p2["room"], world.get_home_room_id(p2_id))

        # Hogares distintos
        self.assertNotEqual(p1["room"], p2["room"])
        self.assertNotEqual(p1["id"], p2["id"])

    # 2. dos cuentas no comparten hogar
    def test_two_accounts_do_not_share_homes(self):
        # Cuenta 1
        self.register_and_approve("cuenta_a", name="Jugador A")
        self.complete_onboarding("humano", "sombra")
        p1 = self.client.get("/api/me").json["player"]

        # Cuenta 2
        client2 = self.app.test_client()
        self.register_and_approve("cuenta_b", name="Jugador B", client=client2)
        self.complete_onboarding("humano", "sombra", client=client2)
        p2 = client2.get("/api/me").json["player"]

        self.assertNotEqual(p1["room"], p2["room"])
        # Jugador B no aparece en el hogar de Jugador A
        others_a = self.client.get("/api/room").json["room"]["others_present"]
        self.assertNotIn("Jugador B", others_a)

        # Mensaje en hogar A no se filtra a hogar B
        self.post("/room/say", dict(body="Mensaje privado en casa A"))
        room_b = client2.get("/api/room").json["room"]
        messages_b = [m["body"] for m in room_b["messages"]]
        self.assertNotIn("Mensaje privado en casa A", messages_b)

    # 3. personaje nuevo inicia en su hogar después de completar onboarding
    def test_new_character_starts_in_home_after_onboarding(self):
        self.register_and_approve("nuevo", name="Aventurero")
        self.complete_onboarding("humano", "arcano")

        player = self.client.get("/api/me").json["player"]
        expected_home_id = world.get_home_room_id(player["id"])
        self.assertEqual(player["room"], expected_home_id)

        room_data = self.client.get("/api/room").json["room"]
        self.assertEqual(room_data["id"], expected_home_id)
        self.assertEqual(room_data["name"], "Tu hogar")
        self.assertEqual(
            room_data["description"],
            "Este es tu hogar. Aquí comienza tu viaje y aquí conservas un lugar propio "
            "dentro del mundo. La salida conduce hacia tu comunidad.",
        )
        self.assertEqual(len(room_data["exits"]), 1)
        self.assertEqual(room_data["exits"][0]["direction"], world.HOME_EXIT_DIRECTION)

        # Verificación en HTML
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn("TU HOGAR", page)
        self.assertIn("Este es tu hogar.", page)
        self.assertNotIn(">Atacar</button>", page)

    # 4. salir conduce al pueblo correcto por especie
    def test_exit_leads_to_correct_town_by_species(self):
        species_town_map = {
            "humano": "valdren_centro",
            "felaryn": "khariel_centro",
            "dravak": "brumak_centro",
            "marevyn": "narevia_centro",
            "vesperi": "velmora_centro",
        }

        for idx, (species, expected_town) in enumerate(species_town_map.items()):
            with self.subTest(species=species):
                client = self.app.test_client()
                uname = f"user_{species}_{idx}"
                self.register_and_approve(uname, name=f"Héroe {species}", client=client)
                self.complete_onboarding(species=species, player_class="sombra", client=client)

                # Verificar inicio en hogar
                player = client.get("/api/me").json["player"]
                self.assertTrue(world.is_home_room(player["room"]))

                # Movimiento hacia el asentamiento (usando botón de salida / dirección sur)
                resp = self.post("/move", dict(direction=world.HOME_EXIT_DIRECTION), client=client)
                self.assertEqual(resp.status_code, 303)

                player_after = client.get("/api/me").json["player"]
                self.assertEqual(player_after["room"], expected_town)

                # También probar con comando literal "salir"
                client_cmd = self.app.test_client()
                uname_cmd = f"user_cmd_{species}_{idx}"
                self.register_and_approve(uname_cmd, name=f"Héroe Cmd {species}", client=client_cmd)
                self.complete_onboarding(species=species, player_class="artifice", client=client_cmd)
                resp_cmd = self.post("/command", dict(text="salir"), client=client_cmd)
                self.assertEqual(resp_cmd.status_code, 303)
                self.assertEqual(client_cmd.get("/api/me").json["player"]["room"], expected_town)

    # 5. reconectar dentro del hogar conserva ubicación
    def test_reconnect_inside_home_preserves_location(self):
        self.register_and_approve("reconectador", name="Dormilón")
        self.complete_onboarding("humano", "sombra")
        p1 = self.client.get("/api/me").json["player"]
        home_id = p1["room"]
        self.assertTrue(world.is_home_room(home_id))

        # Cerrar sesión
        self.post("/logout")
        # Iniciar sesión de nuevo
        self.post("/login", dict(username="reconectador", password="una clave de prueba"))
        p2 = self.client.get("/api/me").json["player"]
        self.assertEqual(p2["room"], home_id)

    # 6. salir y reconectar fuera no devuelve automáticamente a casa
    def test_exit_and_reconnect_outside_does_not_return_home(self):
        self.register_and_approve("caminante", name="Caminante")
        self.complete_onboarding("humano", "juramentado")
        # Salir al pueblo
        self.post("/move", dict(direction=world.HOME_EXIT_DIRECTION))
        self.assertEqual(self.client.get("/api/me").json["player"]["room"], "valdren_centro")

        # Cerrar sesión
        self.post("/logout")
        # Reconectar
        self.post("/login", dict(username="caminante", password="una clave de prueba"))
        p = self.client.get("/api/me").json["player"]
        self.assertEqual(p["room"], "valdren_centro")
        self.assertFalse(world.is_home_room(p["room"]))

    # 7. no hay encuentro random/fijo
    def test_no_random_or_fixed_encounters_in_home(self):
        self.register_and_approve("seguro", name="Tranquilo")
        self.complete_onboarding("humano", "arcano")
        player = self.client.get("/api/me").json["player"]
        home_id = player["room"]

        self.assertIsNone(world.get_room_encounter(home_id))
        self.assertIsNone(encounters.get_encounter_for_room(home_id))
        self.assertIsNone(store.get_encounter(self.path, player["id"], home_id))

        # Intentar atacar en el hogar no encuentra objetivo
        res = self.post("/command", dict(text="atacar"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("No hay ninguna criatura para atacar aquí.", res.get_data(as_text=True))

        # Descanso normal permitido en el hogar
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET fatigue = 30 WHERE id = ?", (player["id"],))
        res_rest = self.post("/command", dict(text="descansar"))
        self.assertEqual(res_rest.status_code, 200)
        char = self.client.get("/api/character").json
        self.assertLess(char["fatigue"], 30)

    # 8. PvP no puede iniciarse dentro
    def test_pvp_cannot_be_initiated_inside_home(self):
        self.register_and_approve("pacifico", name="Pacífico")
        self.complete_onboarding("humano", "sombra")
        # El comando atacar no acepta jugadores como objetivo y no hay PvP
        res = self.post("/command", dict(text="atacar pacífico"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("No hay ninguna criatura para atacar aquí.", res.get_data(as_text=True))

    # 9. inventario/equipamiento permanece sin nuevo sistema de almacenamiento
    def test_inventory_equipment_remains_without_domestic_storage(self):
        self.register_and_approve("minimalista", name="Minimalista")
        self.complete_onboarding("humano", "arcano")
        inv = self.client.get("/api/inventory").json
        # Solo existe el inventario estándar del personaje con su arma inicial
        self.assertEqual(len(inv["items"]), 1)
        self.assertEqual(inv["items"][0]["item_key"], "varita_aprendiz")
        self.assertTrue(inv["items"][0]["equipped"])

        # No hay cofres, bancos, ni endpoints de almacenamiento doméstico
        res = self.client.get("/api/chest")
        self.assertEqual(res.status_code, 404)
        res_bank = self.client.get("/api/bank")
        self.assertEqual(res_bank.status_code, 404)

    # 10. personajes existentes con posición válida no son teletransportados
    def test_existing_characters_with_valid_positions_not_teleported(self):
        # Crear personaje existente simulado con progreso en el mundo
        self.register_and_approve("veterano", name="Veterano")
        self.complete_onboarding("humano", "sombra")
        # Simular que el personaje ya exploró y quedó ubicado en valdren_sendero
        with store.connect(self.path) as db:
            p_id = db.execute("SELECT id FROM players WHERE username = 'veterano'").fetchone()["id"]
            db.execute("UPDATE players SET room = 'valdren_sendero' WHERE id = ?", (p_id,))
        store.mark_visited(self.path, p_id, "valdren_sendero")

        p = self.client.get("/api/me").json["player"]
        self.assertEqual(p["room"], "valdren_sendero")

        # Reiniciar servidor (create_app)
        app2 = create_app(self.config)
        client2 = app2.test_client()
        client2.post("/login", data=dict(csrf=self.csrf(client2), username="veterano", password="una clave de prueba"))
        p2 = client2.get("/api/me").json["player"]
        self.assertEqual(p2["room"], "valdren_sendero")

    # 11. cambio/migración de esquema y reinicio no destruyen estado vivo ni expulsan del hogar
    def test_schema_stability_and_restart_preserves_home_and_live_state(self):
        self.register_and_approve("residente", name="Residente")
        self.complete_onboarding("dravak", "juramentado")
        player = self.client.get("/api/me").json["player"]
        home_id = player["room"]
        self.assertTrue(world.is_home_room(home_id))

        # Reinicio del servidor (re-crea la app con la misma base)
        app_restarted = create_app(self.config)
        client_restarted = app_restarted.test_client()
        csrf_val = self.csrf(client_restarted)
        client_restarted.post("/login", data=dict(csrf=csrf_val, username="residente", password="una clave de prueba"))
        player_restarted = client_restarted.get("/api/me").json["player"]
        self.assertEqual(player_restarted["room"], home_id)

        # Salida funciona perfectamente tras el reinicio
        csrf_val2 = self.csrf(client_restarted)
        client_restarted.post("/move", data=dict(csrf=csrf_val2, direction=world.HOME_EXIT_DIRECTION))
        player_in_town = client_restarted.get("/api/me").json["player"]
        self.assertEqual(player_in_town["room"], "brumak_centro")


if __name__ == "__main__":
    unittest.main()
