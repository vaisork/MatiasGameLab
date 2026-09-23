"""Pruebas de VT-NAR-003 'El lindero roto': combate v1 (GAMEPLAY.md 20),
XP/descubrimientos/antifarmeo (22), mapa progresivo (23) y el contenido de
la microaventura piloto (NARRATIVE.md)."""
import os
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, creatures, store, world


class FixedRoll:
    """RNG de prueba: rng.uniform(a, b) siempre devuelve el mismo valor, para
    forzar aciertos (0) o fallos (100) de forma determinista."""
    def __init__(self, value):
        self.value = value

    def uniform(self, a, b):
        return self.value


# --- combat.py: formulas puras, sin Flask ni base de datos -----------------

class CombatMathTests(unittest.TestCase):
    def test_xp_curve_matches_gameplay_reference_table(self):
        # GAMEPLAY.md 22.1, tabla de referencia.
        self.assertEqual(combat.xp_for_next_level(1), 100)
        self.assertEqual(combat.xp_for_next_level(5), 176)
        self.assertEqual(combat.xp_for_next_level(10), 282)
        self.assertEqual(combat.xp_for_next_level(25), 676)
        self.assertEqual(combat.xp_for_next_level(50), 1582)
        self.assertEqual(combat.xp_for_next_level(75), 2801)
        self.assertEqual(combat.xp_for_next_level(99), 4265)

    def test_hp_max_formula(self):
        # GAMEPLAY.md 20.3.
        self.assertEqual(combat.hp_max(level=1, resistencia=10, voluntad=10), 100)
        self.assertEqual(combat.hp_max(level=1, resistencia=14, voluntad=10), 110)

    def test_accuracy_is_clamped_between_25_and_90(self):
        self.assertEqual(combat.accuracy(10, 10, 0, 0), 55)
        self.assertEqual(combat.accuracy(-1000, -1000, 0, 0), 25)
        self.assertEqual(combat.accuracy(1000, 1000, 0, 0), 90)

    def test_apply_xp_levels_up_and_keeps_remainder(self):
        # 100 XP en nivel 1 (necesita 100) sube exactamente a nivel 2 con 0 sobrante.
        level, xp, gained = combat.apply_xp(1, 0, 100)
        self.assertEqual((level, xp, gained), (2, 0, 1))
        # El exceso de XP se conserva al cruzar de nivel (22.1).
        level, xp, gained = combat.apply_xp(1, 90, 30)
        self.assertEqual(level, 2)
        self.assertEqual(xp, 20)
        self.assertEqual(gained, 1)

    def test_apply_xp_can_cascade_multiple_levels(self):
        level, xp, gained = combat.apply_xp(1, 0, 100 + 118 + 50)
        self.assertEqual(level, 3)
        self.assertEqual(gained, 2)
        self.assertEqual(xp, 50)

    def test_combat_xp_caps_at_25_percent_of_player_next_level(self):
        # Un enemigo de referencia muy alta contra un jugador nivel 1 no
        # puede regalar mas del 25% del siguiente nivel (22.4).
        xp = combat.combat_xp(enemy_ref_level=99, category="abrumador", player_level=1,
                               is_first_family_victory=False, repeats_in_last_10=1)
        self.assertLessEqual(xp, round(0.25 * combat.xp_for_next_level(1)))

    def test_antifarm_reduces_repeated_family_kills(self):
        # GAMEPLAY.md 22.6: 1-3 repeticiones 100%, 4-5 60%, 6+ 25%.
        full = combat.combat_xp(1, "comparable", 1, False, repeats_in_last_10=1)
        reduced = combat.combat_xp(1, "comparable", 1, False, repeats_in_last_10=4)
        floor = combat.combat_xp(1, "comparable", 1, False, repeats_in_last_10=6)
        self.assertGreater(full, reduced)
        self.assertGreater(reduced, floor)

    def test_first_family_victory_adds_bonus(self):
        without_bonus = combat.combat_xp(1, "comparable", 1, False, repeats_in_last_10=1)
        with_bonus = combat.combat_xp(1, "comparable", 1, True, repeats_in_last_10=1)
        self.assertGreater(with_bonus, without_bonus)

    def test_discovery_xp_fractions(self):
        # GAMEPLAY.md 22.7, sobre un contenido de referencia nivel 1 (100 XP).
        self.assertEqual(combat.discovery_xp(1, "descubrimiento_significativo"), 5)
        self.assertEqual(combat.discovery_xp(1, "descubrimiento_mayor"), 10)
        self.assertEqual(combat.discovery_xp(1, "hito_narrativo_menor"), 10)

    def test_respawn_wound_downgrades_one_step_and_never_persists_more_than_one(self):
        # GAMEPLAY.md 20.9.
        self.assertEqual(combat.respawn_wound("grave"), "moderada")
        self.assertEqual(combat.respawn_wound("moderada"), "leve")
        self.assertEqual(combat.respawn_wound("leve"), "ninguna")
        self.assertEqual(combat.respawn_wound("ninguna"), "ninguna")

    def test_respawn_state_is_60_percent_hp_and_40_fatigue(self):
        state = combat.respawn_state(100)
        self.assertEqual(state, {"hp_current": 60, "fatigue": 40})

    def test_flee_chance_clamped_between_20_and_95(self):
        self.assertGreaterEqual(combat.flee_chance(10, 10, 10, 10, 0, 0, 0), 20)
        self.assertLessEqual(combat.flee_chance(10, 10, 10, 10, 0, 0, 0), 95)
        # Fallos previos consecutivos ayudan al siguiente intento (20.10).
        base = combat.flee_chance(10, 10, 10, 10, 0, 0, 0)
        after_failures = combat.flee_chance(10, 10, 10, 10, 0, 3, 0)
        self.assertGreater(after_failures, base)


# --- Calibracion de criaturas (Issue #45: bandas exigidas por Jugabilidad) --

class CreatureCalibrationTests(unittest.TestCase):
    """Un personaje nivel 1 recien creado tiene los 8 atributos en 10 y
    HP=100 (GAMEPLAY.md 20.1/20.3). Issue #45 exige que, contra ese
    personaje, Mordelinde caiga en Favorable/Comparable y Espinajo de
    rastrojo en Comparable/Peligroso."""

    def _category_for(self, creature_id):
        creature = creatures.get_creature(creature_id)
        cg_player = combat.competencia_general(1)
        cg_enemy = combat.competencia_general(creature["reference_level"])
        player_dps = combat.expected_dps(10, 10, 10, cg_player, cg_enemy)
        enemy_dps = combat.expected_dps(creature["destreza"], creature["percepcion"], creature["fuerza"],
                                         cg_enemy, cg_player, base_arma=creature["base_ataque"])
        return combat.encounter_category(player_dps, 100, enemy_dps, creature["hp"])

    def test_mordelinde_is_favorable_or_comparable_for_a_new_character(self):
        self.assertIn(self._category_for("mordelinde"), ("favorable", "comparable"))

    def test_espinajo_is_comparable_or_dangerous_for_a_new_character(self):
        self.assertIn(self._category_for("espinajo_rastrojo"), ("comparable", "peligroso"))

    def test_cornalomo_has_no_playable_stats_yet(self):
        # NARRATIVE.md: Desarrollo debe pedir la tabla de Cornalomo a
        # Jugabilidad antes de montar combate real; no se inventa aqui.
        self.assertIsNone(creatures.get_creature("cornalomo"))


# --- world.py: contenido y conectividad de la microaventura -----------------

class WorldContentTests(unittest.TestCase):
    def test_camino_chain_is_reachable_from_valdren_centro(self):
        room = world.get_room("valdren_centro")
        self.assertEqual(room["exits"]["west"], "valdren_sendero")
        chain = ["valdren_sendero", "valdren_camino_parcela", "valdren_camino_cerca", "valdren_camino_lindero"]
        for previous, current in zip(chain, chain[1:]):
            self.assertEqual(world.get_room(previous)["exits"]["west"], current)
            self.assertEqual(world.get_room(current)["exits"]["east"], previous)

    def test_other_towns_keep_their_original_dead_end_sendero(self):
        # Solo el sendero de Valdren se extiende hacia la microaventura; los
        # demas pueblos conservan su sendero original de una sola salida
        # (de vuelta al centro).
        khariel_sendero = world.get_room("khariel_sendero")
        self.assertEqual(khariel_sendero["exits"], {"west": "khariel_centro"})

    def test_examine_targets_exist_for_the_three_narrative_beats(self):
        self.assertIsNotNone(world.get_examine_text("valdren_camino_parcela", "tallos"))
        self.assertIsNotNone(world.get_examine_text("valdren_camino_parcela", "monticulos"))
        self.assertIsNotNone(world.get_examine_text("valdren_camino_cerca", "pua"))
        self.assertIsNotNone(world.get_examine_text("valdren_camino_lindero", "cerca"))
        self.assertIsNotNone(world.get_examine_text("valdren_camino_lindero", "huellas"))
        self.assertIsNone(world.get_examine_text("valdren_camino_lindero", "algo_inventado"))

    def test_encounters_are_defined_only_for_parcela_and_cerca(self):
        self.assertEqual(world.get_room_encounter("valdren_camino_parcela"), "mordelinde")
        self.assertEqual(world.get_room_encounter("valdren_camino_cerca"), "espinajo_rastrojo")
        self.assertIsNone(world.get_room_encounter("valdren_camino_lindero"))

    def test_discoveries_are_defined(self):
        for key in ("senales_mordelinde", "lindero_roto", "regreso_valdren_lindero"):
            self.assertIsNotNone(world.get_discovery(key))


# --- Integracion end-to-end contra el servidor real -------------------------

@patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
class PilotIntegrationTests(unittest.TestCase):
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
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))  # arranca en valdren_centro

    def walk_to_lindero(self):
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela (Mordelinde)
        self.post("/move", dict(direction="west"))  # cerca (Espinajo)
        self.post("/move", dict(direction="west"))  # lindero roto

    def character(self):
        return self.client.get("/api/character").json

    # --- Mapa progresivo ---------------------------------------------------

    def test_new_character_starts_with_only_the_starting_town_visited(self):
        self.register_and_enter_world()
        state = self.client.get("/api/map").json
        self.assertEqual(state["visited_rooms"], ["valdren_centro"])
        self.assertEqual(state["traversed_routes"], [])

    def test_walking_the_path_marks_rooms_visited_and_routes_traversed(self):
        self.register_and_enter_world()
        self.walk_to_lindero()
        state = self.client.get("/api/map").json
        for room_id in ("valdren_centro", "valdren_sendero", "valdren_camino_parcela",
                         "valdren_camino_cerca", "valdren_camino_lindero"):
            self.assertIn(room_id, state["visited_rooms"])
        self.assertIn(["valdren_camino_cerca", "valdren_camino_lindero"], state["traversed_routes"])

    def test_map_persists_after_app_restart(self):
        self.register_and_enter_world()
        self.walk_to_lindero()
        cookie = self.client.get_cookie("vt_session").value
        app2 = create_app(self.config)
        resumed = app2.test_client()
        resumed.set_cookie("vt_session", cookie)
        state = resumed.get("/api/map").json
        self.assertIn("valdren_camino_lindero", state["visited_rooms"])

    # --- Descubrimientos y XP -----------------------------------------------

    def test_examining_signs_grants_discovery_xp_exactly_once(self):
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela
        self.post("/command", dict(text="examinar tallos"))
        self.assertEqual(self.character()["xp"], 5)
        # Repetir el mismo examen no debe volver a pagar (22.7: una sola vez).
        self.post("/command", dict(text="examinar monticulos"))
        self.assertEqual(self.character()["xp"], 5)

    def test_lindero_discovery_and_return_milestone_award_xp_once_each(self):
        self.register_and_enter_world()
        self.walk_to_lindero()
        self.post("/command", dict(text="examinar huellas"))
        self.assertEqual(self.character()["xp"], 10)
        # Volver a Valdren con el descubrimiento otorga el hito de regreso.
        self.post("/move", dict(direction="east"))
        self.post("/move", dict(direction="east"))
        self.post("/move", dict(direction="east"))
        self.post("/move", dict(direction="east"))  # entra a valdren_centro
        self.assertEqual(self.character()["xp"], 20)
        discovery_keys = {d["key"] for d in self.character()["discoveries"]}
        self.assertEqual(discovery_keys, {"lindero_roto", "regreso_valdren_lindero"})
        # Salir y volver a entrar a Valdren de nuevo no debe repetir el hito.
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="east"))
        self.assertEqual(self.character()["xp"], 20)

    def test_examining_unknown_target_falls_back_to_generic_message(self):
        self.register_and_enter_world()
        page = self.post("/command", dict(text="examinar nube")).get_data(as_text=True)
        self.assertIn("No hay detalle adicional autorizado todavía", page)

    # --- Evaluar -------------------------------------------------------------

    def test_evaluate_without_visible_creature_says_so(self):
        self.register_and_enter_world()
        page = self.post("/command", dict(text="evaluar mordelinde")).get_data(as_text=True)
        self.assertIn("No hay ninguna criatura visible", page)

    def test_evaluate_a_visible_mordelinde_never_reveals_numbers(self):
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela: aparece Mordelinde
        page = self.post("/command", dict(text="evaluar mordelinde")).get_data(as_text=True)
        self.assertIn("Mordelinde", page)
        self.assertTrue(any(phrase in page for phrase in
                             ("favorable", "comparable a ti", "peligroso", "inferior a ti", "supera claramente")))
        self.assertNotRegex(page, r"\b\d+\s*(HP|hp|%|de daño)\b")

    # --- Combate ---------------------------------------------------------------

    @patch("server.combat.random.Random")
    def test_attacking_until_victory_awards_xp_and_clears_the_encounter(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # 0 < cualquier % de impacto real: siempre acierta
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde (45 HP)
        for _ in range(10):  # de sobra para derrotarlo con golpes garantizados
            room = self.client.get("/api/room").json["room"]
            if room["encounter"] is None:
                break
            self.post("/command", dict(text="atacar"))
        room = self.client.get("/api/room").json["room"]
        self.assertIsNone(room["encounter"])
        character = self.character()
        self.assertGreater(character["xp"], 0)

    @patch("server.combat.random.Random")
    def test_defeat_respawns_in_valdren_with_60_percent_hp(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # el jugador tambien acierta, pero bajamos su HP a 1 antes
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde
        store.update_combat_state(self.path, self.client.get("/api/me").json["player"]["id"], hp_current=1)
        self.post("/command", dict(text="atacar"))
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")
        character = self.character()
        self.assertEqual(character["hp_current"], round(character["hp_max"] * 0.6))

    @patch("server.app.random.Random")
    def test_fleeing_successfully_returns_toward_valdren_and_clears_encounter(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # 0 < cualquier probabilidad de huida real: siempre escapa
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde
        self.post("/command", dict(text="huir"))
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_sendero")
        room = self.client.get("/api/room").json["room"]
        self.assertIsNone(room["encounter"])

    def test_attack_without_a_creature_present_is_a_no_op(self):
        self.register_and_enter_world()
        page = self.post("/command", dict(text="atacar")).get_data(as_text=True)
        self.assertIn("No hay ninguna criatura para atacar aquí", page)


if __name__ == "__main__":
    unittest.main()
