"""Pruebas de Issue #73 (VT-DEV): Esquivar, Bloquear y Resistir como
intervenciones que sustituyen el ataque básico (GAMEPLAY.md 20.5, 24.2,
24.3), y el campo estructurado `available_actions` que expone
`server/app.py.room_view()` conforme a `UI_ACTIONS_CONTRACT.md`.

`atacar`, `huir`, `evaluar` y `descansar` ya tenían su propia cobertura en
test_pilot_lindero_roto.py; este archivo no la repite."""
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, store


class FixedRoll:
    """RNG de prueba: rng.uniform(a, b) siempre devuelve el mismo valor, para
    forzar aciertos (0) o fallos (100) de forma determinista. Mismo patrón
    que test_pilot_lindero_roto.py."""
    def __init__(self, value):
        self.value = value

    def uniform(self, a, b):
        return self.value


# --- combat.py: fórmulas puras de defensa contextual (20.5), sin Flask/DB --

class DefenseMathTests(unittest.TestCase):
    def test_fatigue_base_costs_match_gameplay_24_3_table(self):
        self.assertEqual(combat.FATIGUE_BASE_COST["resistir"], 3)
        self.assertEqual(combat.FATIGUE_BASE_COST["bloquear"], 5)
        self.assertEqual(combat.FATIGUE_BASE_COST["esquivar"], 6)
        self.assertEqual(combat.FATIGUE_BASE_COST["huir"], 8)

    def test_dodge_with_default_attributes_leaves_precision_unchanged(self):
        # Agilidad/Percepción en 10 (valor base): sin reducción.
        hits, damage = combat.resolve_dodged_attack_roll(
            45, 5, agilidad=10, percepcion=10, rng=FixedRoll(40))
        self.assertTrue(hits)
        self.assertEqual(damage, 5.0)

    def test_dodge_with_high_agility_reduces_effective_hit_chance(self):
        # Agilidad muy alta empuja el % de impacto al piso del clamp (20),
        # así que un tiro que normalmente acertaría (40 < 45) ahora falla.
        hits, damage = combat.resolve_dodged_attack_roll(
            45, 5, agilidad=200, percepcion=10, rng=FixedRoll(40))
        self.assertFalse(hits)
        self.assertEqual(damage, 0.0)

    def test_dodge_never_reduces_damage_of_a_hit_that_lands(self):
        # GAMEPLAY.md 20.5: "Evita contacto; no reduce daño si el golpe
        # finalmente conecta." -- con reducción insuficiente el golpe sigue
        # haciendo el daño completo de la criatura.
        hits, damage = combat.resolve_dodged_attack_roll(
            45, 5, agilidad=10, percepcion=10, rng=FixedRoll(0))
        self.assertTrue(hits)
        self.assertEqual(damage, 5.0)

    def test_dodge_accuracy_penalty_makes_dodging_harder(self):
        # 24.4/24.6: la fatiga/herida del propio defensor también penaliza
        # su intento de esquivar (combined_accuracy_penalty ya lo documenta
        # como aplicable a "esquiva"). Con Agilidad 58 el % de impacto sin
        # penalizar queda en 21.96 (justo sobre el piso del clamp, 20); una
        # tirada de 30 falla contra eso (esquiva exitosa) pero acierta en
        # cuanto se suma una penalización de 24.4/24.6 de 15.
        hits, _ = combat.resolve_dodged_attack_roll(45, 5, agilidad=58, percepcion=10, rng=FixedRoll(30))
        self.assertFalse(hits)
        hits, _ = combat.resolve_dodged_attack_roll(
            45, 5, agilidad=58, percepcion=10, accuracy_penalty=15, rng=FixedRoll(30))
        self.assertTrue(hits)

    def test_resist_does_not_change_hit_chance(self):
        # 20.5: "no reduce la probabilidad de ser golpeado" -- el % de
        # impacto usado es el precision_pct puro de la criatura, sea cual
        # sea la Resistencia del defensor.
        hits, _ = combat.resolve_resisted_attack_roll(45, 5, resistencia=200, rng=FixedRoll(50))
        self.assertFalse(hits)  # 50 no < 45: falla igual que sin resistir.
        hits, _ = combat.resolve_resisted_attack_roll(45, 5, resistencia=200, rng=FixedRoll(30))
        self.assertTrue(hits)  # 30 < 45: acierta igual que sin resistir.

    def test_resist_reduces_damage_and_caps_at_38_percent(self):
        _, damage_baseline = combat.resolve_resisted_attack_roll(45, 5, resistencia=10, rng=FixedRoll(0))
        self.assertEqual(damage_baseline, 5.0)  # Resistencia 10: sin reducción.
        _, damage_reduced = combat.resolve_resisted_attack_roll(45, 5, resistencia=100, rng=FixedRoll(0))
        self.assertAlmostEqual(damage_reduced, 5.0 * (1 - 0.38))  # tope de 38%.

    def test_block_does_not_change_hit_chance(self):
        hits, _ = combat.resolve_blocked_attack_roll(45, 5, destreza=200, rng=FixedRoll(50))
        self.assertFalse(hits)
        hits, _ = combat.resolve_blocked_attack_roll(45, 5, destreza=200, rng=FixedRoll(30))
        self.assertTrue(hits)

    def test_block_reduces_damage_and_caps_at_32_percent(self):
        _, damage_baseline = combat.resolve_blocked_attack_roll(45, 5, destreza=10, rng=FixedRoll(0))
        self.assertAlmostEqual(damage_baseline, 5.0 * (1 - 0.10))  # 10% ya con Destreza 10.
        _, damage_reduced = combat.resolve_blocked_attack_roll(45, 5, destreza=200, rng=FixedRoll(0))
        self.assertAlmostEqual(damage_reduced, 5.0 * (1 - 0.32))  # tope de 32%.


# --- Integración end-to-end contra el servidor real -------------------------

class CombatActionsIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

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
        with patch.dict("os.environ", {"VT_DM_PASSWORD": "dm-secret-value"}):
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))  # arranca en valdren_centro

    def enter_combat_with_mordelinde(self):
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela: aparece Mordelinde

    def player_id(self):
        return self.client.get("/api/me").json["player"]["id"]

    def character(self):
        return self.client.get("/api/character").json

    def room(self):
        return self.client.get("/api/room").json["room"]

    # --- Sin criatura presente: no-op honesto, no una defensa fingida ------

    def test_dodge_without_a_creature_is_a_no_op(self):
        self.register_and_enter_world()
        page = self.post("/command", dict(text="esquivar")).get_data(as_text=True)
        self.assertIn("No hay ningún ataque que esquivar aquí", page)

    def test_resist_without_a_creature_is_a_no_op(self):
        self.register_and_enter_world()
        page = self.post("/command", dict(text="resistir")).get_data(as_text=True)
        self.assertIn("No hay ningún golpe que resistir aquí", page)

    def test_block_without_a_creature_is_a_no_op(self):
        self.register_and_enter_world()
        page = self.post("/command", dict(text="bloquear")).get_data(as_text=True)
        self.assertIn("No hay ningún golpe que bloquear aquí", page)

    # --- Esquivar ------------------------------------------------------------

    @patch("server.combat.random.Random")
    def test_dodging_with_high_agility_avoids_a_hit_that_would_otherwise_land(self, mock_random):
        mock_random.return_value = FixedRoll(40)  # 40 < 45 (precisión de Mordelinde): acertaría sin esquivar.
        self.register_and_enter_world()
        self.enter_combat_with_mordelinde()
        player_id = self.player_id()
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET attr_agilidad = 200 WHERE id = ?", (player_id,))
        hp_before = self.character()["hp_current"]
        page = self.post("/command", dict(text="esquivar")).get_data(as_text=True)
        self.assertIn("Esquivas el ataque", page)
        self.assertEqual(self.character()["hp_current"], hp_before)

    @patch("server.combat.random.Random")
    def test_dodge_costs_fatigue(self, mock_random):
        mock_random.return_value = FixedRoll(100)  # nunca acierta: solo interesa el coste de intentar.
        self.register_and_enter_world()
        self.enter_combat_with_mordelinde()
        self.assertEqual(self.character()["fatigue"], 0)
        self.post("/command", dict(text="esquivar"))
        self.assertEqual(self.character()["fatigue"], 6)  # 24.3: esquivar = 6, Resistencia 10.

    # --- Resistir --------------------------------------------------------------

    @patch("server.combat.random.Random")
    def test_resisting_reduces_damage_taken_compared_to_a_plain_hit(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # siempre acierta.
        self.register_and_enter_world()
        self.enter_combat_with_mordelinde()
        player_id = self.player_id()
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET attr_resistencia = 100 WHERE id = ?", (player_id,))
        hp_before = self.character()["hp_current"]
        page = self.post("/command", dict(text="resistir")).get_data(as_text=True)
        self.assertIn("Resistes el golpe", page)
        hp_after = self.character()["hp_current"]
        # Mordelinde hace 5 de daño fijo; con Resistencia 100 el tope de
        # reducción (38%) deja el golpe en 5*0.62 = 3.1 -> redondeado a 3.
        self.assertEqual(round(hp_before - hp_after), 3)

    @patch("server.combat.random.Random")
    def test_resist_costs_fatigue(self, mock_random):
        mock_random.return_value = FixedRoll(100)
        self.register_and_enter_world()
        self.enter_combat_with_mordelinde()
        self.post("/command", dict(text="resistir"))
        self.assertEqual(self.character()["fatigue"], 3)  # 24.3: resistir = 3, Resistencia 10.

    # --- Bloquear (sin equipo real todavía: Issue #57) --------------------

    def test_block_is_rejected_without_equipment(self):
        self.register_and_enter_world()
        self.enter_combat_with_mordelinde()
        page = self.post("/command", dict(text="bloquear")).get_data(as_text=True)
        self.assertIn("Todavía no tienes equipo adecuado para bloquear", page)
        # No se resolvió ningún golpe ni se gastó fatiga por una acción rechazada.
        self.assertEqual(self.character()["fatigue"], 0)

    @patch("server.app._can_block", return_value=True)
    @patch("server.combat.random.Random")
    def test_block_resolves_once_equipment_is_authorized(self, mock_random, _mock_can_block):
        # Simula que #57 ya autorizó equipo de bloqueo, sin implementarlo:
        # confirma que la resolución de golpe/daño/fatiga queda lista.
        mock_random.return_value = FixedRoll(0)
        self.register_and_enter_world()
        self.enter_combat_with_mordelinde()
        page = self.post("/command", dict(text="bloquear")).get_data(as_text=True)
        self.assertIn("Bloqueas", page)
        self.assertEqual(self.character()["fatigue"], 5)  # 24.3: bloquear = 5, Resistencia 10.

    # --- Paridad botón/comando ------------------------------------------------

    def test_dodge_button_and_command_reach_the_same_intention(self):
        self.register_and_enter_world()
        page_button = self.post("/dodge").get_data(as_text=True)
        page_command = self.post("/command", dict(text="esquivar")).get_data(as_text=True)
        self.assertIn("No hay ningún ataque que esquivar aquí", page_button)
        self.assertIn("No hay ningún ataque que esquivar aquí", page_command)

    def test_resist_button_and_command_reach_the_same_intention(self):
        self.register_and_enter_world()
        page_button = self.post("/resist").get_data(as_text=True)
        page_command = self.post("/command", dict(text="resistir")).get_data(as_text=True)
        self.assertIn("No hay ningún golpe que resistir aquí", page_button)
        self.assertIn("No hay ningún golpe que resistir aquí", page_command)

    def test_block_button_and_command_reach_the_same_intention(self):
        self.register_and_enter_world()
        page_button = self.post("/block").get_data(as_text=True)
        page_command = self.post("/command", dict(text="bloquear")).get_data(as_text=True)
        self.assertIn("No hay ningún golpe que bloquear aquí", page_button)
        self.assertIn("No hay ningún golpe que bloquear aquí", page_command)

    # --- available_actions -----------------------------------------------------

    def test_available_actions_offers_only_rest_outside_combat(self):
        self.register_and_enter_world()
        room = self.room()
        self.assertEqual(room["available_actions"], [{"action": "descansar"}])

    def test_available_actions_lists_combat_options_with_a_creature_present(self):
        self.register_and_enter_world()
        self.enter_combat_with_mordelinde()
        room = self.room()
        actions = {entry["action"] for entry in room["available_actions"]}
        self.assertEqual(actions, {"atacar", "evaluar", "huir", "esquivar", "resistir"})
        self.assertNotIn("bloquear", actions)  # sin equipo real todavía (Issue #57).
        self.assertNotIn("descansar", actions)  # no se ofrece descanso en combate.
        attack_entry = next(e for e in room["available_actions"] if e["action"] == "atacar")
        self.assertEqual(attack_entry["targets"], ["mordelinde"])

    @patch("server.app._can_block", return_value=True)
    def test_available_actions_includes_block_once_equipment_is_authorized(self, _mock_can_block):
        self.register_and_enter_world()
        self.enter_combat_with_mordelinde()
        actions = {entry["action"] for entry in self.room()["available_actions"]}
        self.assertIn("bloquear", actions)


if __name__ == "__main__":
    unittest.main()
