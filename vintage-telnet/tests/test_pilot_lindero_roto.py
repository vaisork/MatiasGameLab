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

    # --- GAMEPLAY.md 24: fatiga, heridas y recuperacion --------------------

    def test_fatigue_state_thresholds(self):
        # GAMEPLAY.md 20.7/24.4: 0-69 operativo, 70-89 cansado, 90-100 agotado.
        self.assertEqual(combat.fatigue_state(0), "operativo")
        self.assertEqual(combat.fatigue_state(69), "operativo")
        self.assertEqual(combat.fatigue_state(70), "cansado")
        self.assertEqual(combat.fatigue_state(89), "cansado")
        self.assertEqual(combat.fatigue_state(90), "agotado")
        self.assertEqual(combat.fatigue_state(100), "agotado")

    def test_fatigue_gained_applies_resistencia_modifier_and_wound_multiplier(self):
        # GAMEPLAY.md 20.7 ModFatiga=1 con Resistencia 10; 24.3 coste base 4
        # para ataque basico; 24.6 x1.20 con herida moderada.
        self.assertEqual(combat.fatigue_gained("ataque_basico", 10, "ninguna"), 4)
        self.assertAlmostEqual(combat.fatigue_gained("ataque_basico", 10, "moderada"), 4.8)
        # Mas Resistencia reduce la fatiga generada (piso 0.55).
        self.assertLess(combat.fatigue_gained("ataque_basico", 100, "ninguna"), 4)

    def test_combined_penalties_stack_fatigue_and_wound(self):
        # Cansado (-5) + herida moderada (-5) = -10 de precision;
        # 0.90 (cansado) x 1.0 (moderada no reduce dano) = 0.90 de dano.
        self.assertEqual(combat.combined_accuracy_penalty(75, "moderada"), 10)
        self.assertAlmostEqual(combat.combined_damage_multiplier(75, "moderada"), 0.90)
        self.assertEqual(combat.combined_accuracy_penalty(0, "ninguna"), 0)
        self.assertEqual(combat.combined_damage_multiplier(0, "ninguna"), 1.0)

    def test_wound_from_hit_matches_gameplay_reference_table(self):
        # GAMEPLAY.md 24.5, HP maximo de referencia 100.
        self.assertEqual(combat.wound_from_hit(19, 100), "ninguna")
        self.assertEqual(combat.wound_from_hit(20, 100), "leve")
        self.assertEqual(combat.wound_from_hit(34, 100), "leve")
        self.assertEqual(combat.wound_from_hit(35, 100), "moderada")
        self.assertEqual(combat.wound_from_hit(49, 100), "moderada")
        self.assertEqual(combat.wound_from_hit(50, 100), "grave")

    def test_worse_wound_never_downgrades(self):
        # GAMEPLAY.md 24.5: una herida mayor reemplaza a una menor; nunca se
        # acumulan dos heridas ni una nueva mas leve reemplaza a la actual.
        self.assertEqual(combat.worse_wound("leve", "grave"), "grave")
        self.assertEqual(combat.worse_wound("grave", "leve"), "grave")
        self.assertEqual(combat.worse_wound("ninguna", "moderada"), "moderada")

    def test_rest_result_heals_10_percent_and_reduces_fatigue(self):
        # GAMEPLAY.md 24.8, sin herida: sin tope de HP, -25 de fatiga con
        # Resistencia 10.
        result = combat.rest_result(hp_current=50, hp_max_value=100, fatigue=80,
                                     resistencia=10, wound="ninguna")
        self.assertEqual(result, {"hp_current": 60, "fatigue": 55})

    def test_rest_result_respects_wound_hp_cap(self):
        # GAMEPLAY.md 24.6: herida grave no deja curar el descanso de campo
        # por encima del 65% del HP maximo.
        result = combat.rest_result(hp_current=64, hp_max_value=100, fatigue=0,
                                     resistencia=10, wound="grave")
        self.assertEqual(result["hp_current"], 65)

    def test_safe_recovery_result_fully_heals_and_upgrades_wound_one_grade(self):
        # GAMEPLAY.md 24.9.
        result = combat.safe_recovery_result(100, "grave")
        self.assertEqual(result, {"hp_current": 100, "fatigue": 0, "wound": "moderada"})


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
        enemy_dps = combat.fixed_expected_dps(creature["precision"], creature["damage"])
        return combat.encounter_category(player_dps, 100, enemy_dps, creature["hp"])

    def test_mordelinde_matches_approved_starter_balance_profile(self):
        # STARTER_CREATURE_BALANCE.md fija el perfil visible tal cual, sin
        # derivarlo de un modelo interno de atributos (revision de
        # Arquitectura de PR #49).
        mordelinde = creatures.get_creature("mordelinde")
        self.assertEqual(mordelinde["hp"], 28)
        self.assertEqual(mordelinde["precision"], 45)
        self.assertEqual(mordelinde["damage"], 5)

    def test_espinajo_matches_approved_starter_balance_profile(self):
        espinajo = creatures.get_creature("espinajo_rastrojo")
        self.assertEqual(espinajo["hp"], 40)
        self.assertEqual(espinajo["precision"], 50)
        self.assertEqual(espinajo["damage"], 8)

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

    def choose_class_without_starter_weapon(self):
        """Clase elegida sin arma inicial (Issue #112): estas pruebas miden el
        perfil tecnico sin arma de GAMEPLAY.md 24.10 y equipan a mano lo que
        necesitan. El flujo real /class con arma inicial se prueba aparte."""
        player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.app.config["DATABASE"], player_id, "juramentado")

    def register_and_enter_world(self, username="matias", name="Matías"):
        self.post("/register", dict(username=username, name=name, password="una clave de prueba"))
        dm = self.app.test_client()
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))  # arranca en valdren_centro
        self.choose_class_without_starter_weapon()

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

    def test_a_single_ambiguous_sign_does_not_name_mordelinde_yet(self):
        # VT-PSY-004: "tallos" por si solo solo describe "algo pequeno" --
        # no basta para que el sistema concluya la especie ni pague XP
        # (aunque el nombre "Mordelinde" ya pueda verse en la caja de
        # encuentro porque la criatura esta visible en la sala).
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela
        page = self.post("/command", dict(text="examinar tallos")).get_data(as_text=True)
        self.assertNotIn("Reconoces las señales de un Mordelinde", page)
        self.assertEqual(self.character()["xp"], 0)
        self.assertEqual(self.character()["discoveries"], [])

    def test_examining_both_signs_grants_discovery_xp_exactly_once(self):
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela
        self.post("/command", dict(text="examinar tallos"))
        self.assertEqual(self.character()["xp"], 0)
        # Solo al examinar la segunda senal hay evidencia suficiente.
        self.post("/command", dict(text="examinar monticulos"))
        self.assertEqual(self.character()["xp"], 5)
        # Repetir cualquiera de los dos examenes no debe volver a pagar
        # (22.7: una sola vez).
        self.post("/command", dict(text="examinar tallos"))
        self.post("/command", dict(text="examinar monticulos"))
        self.assertEqual(self.character()["xp"], 5)

    def test_examining_cerca_alone_does_not_conclude_a_much_bigger_creature(self):
        # VT-PSY-004: "examinar cerca" solo demuestra violencia, no tamano --
        # no basta por si sola para el descubrimiento mayor del lindero.
        self.register_and_enter_world()
        self.walk_to_lindero()
        page = self.post("/command", dict(text="examinar cerca")).get_data(as_text=True)
        self.assertNotIn("Comprendes que una criatura mucho mayor", page)
        self.assertEqual(self.character()["xp"], 0)

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

    # --- GAMEPLAY.md 31: informacion visible de enemigos / VT-PSY-004 ------

    def test_room_view_never_exposes_enemy_numeric_hp(self):
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela: aparece Mordelinde
        encounter = self.client.get("/api/room").json["room"]["encounter"]
        self.assertNotIn("hp_current", encounter)
        self.assertNotIn("hp_max", encounter)
        self.assertEqual(encounter["condition"], "entero / apenas afectado")

    @patch("server.combat.random.Random")
    def test_enemy_condition_band_drops_as_it_takes_damage(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # el jugador siempre acierta
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde (28 HP, ~10 de daño/golpe)
        self.post("/command", dict(text="atacar"))
        self.post("/command", dict(text="atacar"))
        encounter = self.client.get("/api/room").json["room"]["encounter"]
        self.assertIn(encounter["condition"], ("herido", "malherido", "al borde de caer"))

    def test_mordelinde_and_espinajo_show_different_behavior_before_deciding(self):
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde
        mordelinde_behavior = self.client.get("/api/room").json["room"]["encounter"]["behavior"]
        self.post("/move", dict(direction="west"))  # cerca: Espinajo de rastrojo
        espinajo_behavior = self.client.get("/api/room").json["room"]["encounter"]["behavior"]
        self.assertNotEqual(mordelinde_behavior, espinajo_behavior)
        self.assertIn("zigzag", mordelinde_behavior)
        self.assertIn("puas", espinajo_behavior)

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

    # --- GAMEPLAY.md 24: fatiga, heridas, descanso y respawn de monstruos --

    @patch("server.combat.random.Random")
    def test_attacking_costs_fatigue(self, mock_random):
        mock_random.return_value = FixedRoll(100)  # nunca acierta: solo interesa el coste de intentar
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde
        self.assertEqual(self.character()["fatigue"], 0)
        self.post("/command", dict(text="atacar"))
        self.assertEqual(self.character()["fatigue"], 4)  # 24.3: ataque básico = 4, Resistencia 10.

    @patch("server.combat.random.Random")
    def test_a_heavy_hit_inflicts_a_wound(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # ambos golpes aciertan siempre
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde
        player_id = self.client.get("/api/me").json["player"]["id"]
        # Bajamos el HP maximo del personaje para que el golpe de Mordelinde
        # (~6-7 de daño bruto) cruce el 20% de 24.5 y dispare una herida leve
        # sin inventar estadisticas de la criatura.
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET hp_max = 20, hp_current = 20 WHERE id = ?", (player_id,))
        self.post("/command", dict(text="atacar"))
        self.assertIn(self.character()["wound"], ("leve", "moderada", "grave"))

    def test_resting_outside_combat_heals_and_reduces_fatigue(self):
        # Fuera de la sala segura (24.8: descanso de campo v1).
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))  # valdren_sendero: no es SAFE_ROOM_ID
        player_id = self.client.get("/api/me").json["player"]["id"]
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET hp_current = 50, fatigue = 80 WHERE id = ?", (player_id,))
        page = self.post("/command", dict(text="descansar")).get_data(as_text=True)
        self.assertIn("Descansas un momento", page)
        character = self.character()
        self.assertEqual(character["hp_current"], 60)  # +10% de 100 de HP máximo.
        self.assertEqual(character["fatigue"], 55)  # 80 - (25 + 0.2*(10-10)).

    def test_resting_in_valdren_centro_uses_full_safe_recovery(self):
        # Issue #46: valdren_centro es el punto de recuperación segura
        # (GAMEPLAY.md 24.9) — descansar ahí cura HP al 100%, fatiga a 0 y
        # mejora la herida un grado, en vez del descanso de campo v1.
        self.register_and_enter_world()  # humano arranca en valdren_centro
        player_id = self.client.get("/api/me").json["player"]["id"]
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET hp_current = 50, fatigue = 80, wound = 'moderada' WHERE id = ?",
                       (player_id,))
        page = self.post("/command", dict(text="descansar")).get_data(as_text=True)
        self.assertIn("plaza de Valdren", page)
        character = self.character()
        self.assertEqual(character["hp_current"], round(character["hp_max"]))
        self.assertEqual(character["fatigue"], 0)
        self.assertEqual(character["wound"], "leve")

    def test_resting_is_blocked_while_a_creature_is_present(self):
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde
        page = self.post("/command", dict(text="descansar")).get_data(as_text=True)
        self.assertIn("No puedes descansar", page)

    @patch("server.combat.random.Random")
    def test_defeated_creature_does_not_respawn_immediately_but_does_after_cooldown(self, mock_random):
        mock_random.return_value = FixedRoll(0)
        self.register_and_enter_world()
        self.post("/move", dict(direction="west"))
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde (45 HP)
        for _ in range(10):
            room = self.client.get("/api/room").json["room"]
            if room["encounter"] is None:
                break
            self.post("/command", dict(text="atacar"))
        # Salir y volver a entrar de inmediato no debe regenerar la criatura
        # (GAMEPLAY.md 20.14: ~5 minutos de referencia, no reaparición llena
        # instantánea).
        self.post("/move", dict(direction="east"))
        self.post("/move", dict(direction="west"))
        room = self.client.get("/api/room").json["room"]
        self.assertIsNone(room["encounter"])
        # Una vez cumplido el cooldown, la criatura vuelve a aparecer.
        player_id = self.client.get("/api/me").json["player"]["id"]
        with store.connect(self.path) as db:
            db.execute("UPDATE creature_cooldowns SET available_at = '2000-01-01T00:00:00.000000+00:00' "
                       "WHERE player_id = ?", (player_id,))
        self.post("/move", dict(direction="east"))
        self.post("/move", dict(direction="west"))
        room = self.client.get("/api/room").json["room"]
        self.assertIsNotNone(room["encounter"])


if __name__ == "__main__":
    unittest.main()
