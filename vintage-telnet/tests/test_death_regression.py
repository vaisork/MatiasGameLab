"""Pruebas de regresión del motor de muerte y respawn existente (Issue #213 / DEATH-01).

Valida el contrato de DEATH_PLAYTEST.md §7:
HP 0 -> termina combate -> respawn seguro -> estado persistente -> reconexión.
"""
import os
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, encounters, store


class SequenceRng:
    """RNG determinista secuencial para simular tiradas de combate y huida."""
    def __init__(self, *values):
        self.values = list(values)
        self.idx = 0

    def uniform(self, a, b):
        if self.idx < len(self.values):
            val = self.values[self.idx]
            self.idx += 1
            return val
        return self.values[-1]


@patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
class DeathRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

        # Controlar _rng de encuentros aleatorios (#207) para que las salas de paso
        # como valdren_sendero no generen encuentros espurios durante la prueba.
        self.enc_patch = patch.object(encounters, "_rng")
        self.mock_enc_rng = self.enc_patch.start()
        self.mock_enc_rng.random.return_value = 0.50  # 0.50 >= 0.10: sendero queda libre de encuentro aleatorio
        self.addCleanup(self.enc_patch.stop)

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def register_and_enter_world(self, username="matias", name="Matías"):
        self.post("/register", dict(username=username, name=name, password="una clave de prueba"))
        dm = self.app.test_client()
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.path, player_id, "juramentado")
        self.post("/move", dict(direction="south"))  # salir del hogar al centro de Valdren
        return player_id

    def enter_combat_with_mordelinde(self):
        self.post("/move", dict(direction="north"))  # valdren_sendero (rng controlado a 0.50)
        self.post("/move", dict(direction="north"))  # valdren_camino_parcela (Mordelinde fija)

    def character(self, client=None):
        client = client or self.client
        return client.get("/api/character").json

    def inventory(self, client=None):
        client = client or self.client
        return client.get("/api/inventory").json

    @patch("server.combat.random.Random")
    def test_defeat_attacking_terminates_encounter_and_persists_respawn_state_on_reconnect(self, mock_random):
        """Alcance 1 a 8:
        1. Llegar a 0 HP termina el encuentro.
        2. No queda room_encounter fantasma en DB ni en el store.
        3. El jugador reaparece en valdren_centro.
        4. Reaparece con 60% HP, 40 fatiga y herida degradada 1 grado.
        5. XP, nivel, PA y PP permanecen intactos.
        6. Inventario completo y equipo (arma y armadura) permanecen intactos.
        7. Reconexión en nueva sesión recupera exactamente el estado persistido.
        8. /api/me, /api/character y /api/inventory reflejan el estado autoritativo sin combate activo.
        """
        mock_random.return_value = SequenceRng(0.0)  # ambos impactan
        pid = self.register_and_enter_world()

        # Configurar progresión, equipo completo (arma + armadura + item en bolsa) y herida previa
        store.grant_item(self.path, pid, "espada_juramento")
        store.grant_item(self.path, pid, "acolchado_camino")
        store.grant_item(self.path, pid, "punal_camino")
        self.post("/command", dict(text="equipar Espada de juramento"))
        self.post("/command", dict(text="equipar Acolchado de Camino"))

        with store.connect(self.path) as db:
            db.execute("UPDATE players SET xp = 45, pa_unspent = 3, pp_unspent = 1, wound = 'moderada' WHERE id = ?",
                       (pid,))

        char_before = self.character()
        inv_before = self.inventory()
        hp_max = char_before["hp_max"]

        self.assertEqual(char_before["level"], 1)
        self.assertEqual(char_before["xp"], 45)
        self.assertEqual(char_before["pa_unspent"], 3)
        self.assertEqual(char_before["pp_unspent"], 1)
        self.assertEqual(char_before["wound"], "moderada")
        self.assertEqual(inv_before["equipped"]["weapon"]["item_key"], "espada_juramento")
        self.assertEqual(inv_before["equipped"]["armor"]["item_key"], "acolchado_camino")
        self.assertEqual(len(inv_before["items"]), 3)

        self.enter_combat_with_mordelinde()
        self.assertIsNotNone(store.get_encounter(self.path, pid, "valdren_camino_parcela"))

        # Bajar HP a 1 para que el contragolpe de la criatura cause derrota
        store.update_combat_state(self.path, pid, hp_current=1)

        response = self.post("/command", dict(text="atacar"))
        html = response.get_data(as_text=True)
        self.assertIn("te derrota", html)

        # 1 y 2: Encuentro terminado y sin encuentro fantasma en store/SQLite
        self.assertIsNone(store.get_encounter(self.path, pid, "valdren_camino_parcela"))
        with store.connect(self.path) as db:
            active_encounters = db.execute("SELECT count(*) FROM room_encounters WHERE player_id = ?", (pid,)).fetchone()[0]
            self.assertEqual(active_encounters, 0)

        # 3, 4, 8: /api/me y /api/character autoritativos
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")

        char_after = self.character()
        expected_hp = round(hp_max * 0.60)
        self.assertEqual(char_after["hp_current"], expected_hp)
        self.assertEqual(char_after["fatigue"], 40)
        self.assertEqual(char_after["wound"], "leve")  # degradada de moderada a leve
        self.assertFalse(char_after["in_combat"])

        # 5: XP, nivel, PA y PP intactos antes de reconectar
        self.assertEqual(char_after["level"], char_before["level"])
        self.assertEqual(char_after["xp"], char_before["xp"])
        self.assertEqual(char_after["pa_unspent"], char_before["pa_unspent"])
        self.assertEqual(char_after["pp_unspent"], char_before["pp_unspent"])

        # 6: Comparar inventario y equipo completos antes y después de morir
        inv_after = self.inventory()
        self.assertEqual(inv_after["items"], inv_before["items"])
        self.assertEqual(inv_after["equipped"], inv_before["equipped"])
        self.assertEqual(inv_after["armor_reduction_total"], inv_before["armor_reduction_total"])
        self.assertEqual(inv_after["carga_multiplier"], inv_before["carga_multiplier"])

        # 7: Reconexión / recreación de cliente recupera exactamente el estado persistido
        session_cookie = self.client.get_cookie("vt_session").value
        new_client = self.app.test_client()
        new_client.set_cookie("vt_session", session_cookie)

        reconnected_me = new_client.get("/api/me").json["player"]
        self.assertEqual(reconnected_me["room"], "valdren_centro")

        reconnected_char = self.character(new_client)
        # Verificar también nivel, XP, PA y PP tras reconectar
        self.assertEqual(reconnected_char["level"], char_before["level"])
        self.assertEqual(reconnected_char["xp"], char_before["xp"])
        self.assertEqual(reconnected_char["pa_unspent"], char_before["pa_unspent"])
        self.assertEqual(reconnected_char["pp_unspent"], char_before["pp_unspent"])
        self.assertEqual(reconnected_char["hp_current"], expected_hp)
        self.assertEqual(reconnected_char["fatigue"], 40)
        self.assertEqual(reconnected_char["wound"], "leve")
        self.assertFalse(reconnected_char["in_combat"])

        # Volver a comprobar inventario y equipo completos tras reconectar
        inv_reconnected = self.inventory(new_client)
        self.assertEqual(inv_reconnected["items"], inv_before["items"])
        self.assertEqual(inv_reconnected["equipped"], inv_before["equipped"])
        self.assertEqual(inv_reconnected["armor_reduction_total"], inv_before["armor_reduction_total"])
        self.assertEqual(inv_reconnected["carga_multiplier"], inv_before["carga_multiplier"])

        reconnected_room = new_client.get("/api/room").json["room"]
        self.assertEqual(reconnected_room["id"], "valdren_centro")
        self.assertIsNone(reconnected_room["encounter"])

    @patch("server.app.random.Random")
    def test_defeat_while_fleeing_terminates_encounter_and_triggers_safe_respawn(self, mock_random):
        """DEATH_PLAYTEST.md §7.B: Muerte intentando huir."""
        # Tirada 1: 99.0 para fallar huida (99 > flee_chance)
        # Tirada 2: 0.0 para que el contragolpe enemigo conecte
        mock_random.return_value = SequenceRng(99.0, 0.0)
        pid = self.register_and_enter_world()
        self.enter_combat_with_mordelinde()

        store.update_combat_state(self.path, pid, hp_current=1)

        response = self.post("/command", dict(text="huir"))
        html = response.get_data(as_text=True)
        self.assertIn("te derrota", html)

        self.assertIsNone(store.get_encounter(self.path, pid, "valdren_camino_parcela"))
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")

        char = self.character()
        self.assertEqual(char["hp_current"], round(char["hp_max"] * 0.60))
        self.assertEqual(char["fatigue"], 40)
        self.assertFalse(char["in_combat"])

    @patch("server.app.random.Random")
    def test_defeat_while_defending_terminates_encounter_and_triggers_safe_respawn(self, mock_random):
        """DEATH_PLAYTEST.md §7.C: Muerte defendiendo (esquivar)."""
        # Tirada 0.0: el ataque de la criatura impacta a pesar de esquivar
        mock_random.return_value = SequenceRng(0.0)
        pid = self.register_and_enter_world()
        self.enter_combat_with_mordelinde()

        store.update_combat_state(self.path, pid, hp_current=1)

        response = self.post("/command", dict(text="esquivar"))
        html = response.get_data(as_text=True)
        self.assertIn("te derrota", html)

        self.assertIsNone(store.get_encounter(self.path, pid, "valdren_camino_parcela"))
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")

        char = self.character()
        self.assertEqual(char["hp_current"], round(char["hp_max"] * 0.60))
        self.assertEqual(char["fatigue"], 40)
        self.assertFalse(char["in_combat"])

    def test_player_can_continue_exploring_world_after_respawn(self):
        """DEATH_PLAYTEST.md §7.E: El personaje no queda atascado en estado muerto y puede seguir jugando."""
        with patch("server.combat.random.Random", return_value=SequenceRng(0.0)):
            pid = self.register_and_enter_world()
            self.enter_combat_with_mordelinde()
            store.update_combat_state(self.path, pid, hp_current=1)
            self.post("/command", dict(text="atacar"))

        # El jugador reapareció en valdren_centro y puede volver a caminar
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")

        move_res = self.post("/move", dict(direction="north"))
        self.assertEqual(move_res.status_code, 303)
        current_room = self.client.get("/api/room").json["room"]
        self.assertEqual(current_room["id"], "valdren_sendero")


if __name__ == "__main__":
    unittest.main()
