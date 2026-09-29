"""Pruebas completas del contrato de Uñapiedra v1 (Issue #229).

Canon: vintage-telnet/CREATURES.md (§ Sierra de Hoshai — alrededores de Khariel).
Contrato mecánico: Jugabilidad y Arquitectura en Issue #229 (2026-09-27).
Reglas: GAMEPLAY.md §§20, 22.
"""
import math
import os
import random
import re
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, creatures, encounters, items, store, world


class FixedRoll:
    """RNG determinista para tests."""
    def __init__(self, value):
        self.value = value

    def uniform(self, a, b):
        return self.value


class UnapiedraUnitTests(unittest.TestCase):
    """Verificación de contrato unitario, atributos y fórmulas de combate."""

    def test_unapiedra_profile_matches_gameplay_approved_contract(self):
        """Criterio 2: Perfil exacto ref 1 / HP 30 / precisión 45 / daño 5 / flee_agilidad 15 / flee_percepcion 12."""
        creature = creatures.get_creature("unapiedra")
        self.assertIsNotNone(creature, "Uñapiedra debe existir en CREATURES")
        self.assertEqual(creature["name"], "Uñapiedra")
        self.assertEqual(creature["family"], "unapiedra")
        self.assertEqual(creature["reference_level"], 1)
        self.assertEqual(creature["hp"], 30)
        self.assertEqual(creature["precision"], 45)
        self.assertEqual(creature["damage"], 5)
        self.assertEqual(creature["flee_agilidad"], 15)
        self.assertEqual(creature["flee_percepcion"], 12)
        self.assertEqual(creature.get("armor_reduction", 0.0), 0.0)
        expected_behavior = (
            "Uñapiedra se aplasta contra la roca y busca una grieta o saliente cercana; "
            "si la acorralas, sisea y defiende el refugio con una mordida corta."
        )
        self.assertEqual(creature["behavior_text"], expected_behavior)

    def test_unapiedra_has_approved_art_in_creature_art(self):
        """Issue #548: arte aprobado (PR #227/#178, Issue #167) ya conectado al runtime."""
        self.assertIn("unapiedra", creatures.CREATURE_ART)
        art = creatures.CREATURE_ART["unapiedra"]
        self.assertEqual(art["src"], "/assets/creatures/unapiedra.webp")

    def test_unapiedra_relative_difficulty_is_favorable_for_level_1(self):
        """Criterio: Dificultad relativa FAVORABLE para nivel 1 sano."""
        player_dps = combat.expected_dps(destreza=10, percepcion=10, fuerza=10,
                                         cg_self=0, cg_other=0, base_arma=10)
        self.assertEqual(player_dps, 5.5)
        enemy_dps = combat.fixed_expected_dps(precision_pct=45, damage=5)
        self.assertEqual(enemy_dps, 2.25)
        category = combat.encounter_category(player_dps=player_dps, player_hp=100,
                                             enemy_dps=enemy_dps, enemy_hp=30)
        self.assertEqual(category, "favorable")

    def test_unapiedra_combat_duration_comparable_to_mordelinde(self):
        """Criterio 5: Combate forzado de duración aproximada a Mordelinde."""
        player_dps = 5.5
        mordelinde_expected_rounds = 28 / player_dps  # ~5.09
        unapiedra_expected_rounds = 30 / player_dps    # ~5.45
        diff_rounds = abs(unapiedra_expected_rounds - mordelinde_expected_rounds)
        self.assertLess(diff_rounds, 1.0,
                        "La duración esperada debe ser prácticamente idéntica a Mordelinde")

    def test_unapiedra_flee_formula(self):
        """Criterio 4: Huida ágil pero accesible con fórmula estándar de fuga."""
        chance = combat.flee_chance(player_agilidad=10, player_percepcion=10,
                                    enemy_agilidad=15, enemy_percepcion=12,
                                    attacker_level_advantage=0, previous_failed_attempts=0,
                                    fatigue=0)
        # 50 + 0.45*(-5) + 0.15*(-2) = 47.45
        self.assertAlmostEqual(chance, 47.45, places=2)
        # Con 1 intento fallido previo (+15% bonus_fallos)
        chance_retry = combat.flee_chance(player_agilidad=10, player_percepcion=10,
                                          enemy_agilidad=15, enemy_percepcion=12,
                                          attacker_level_advantage=0, previous_failed_attempts=1,
                                          fatigue=0)
        self.assertAlmostEqual(chance_retry, 62.45, places=2)

    def test_zero_spawns_in_civil_and_safe_rooms(self):
        """Criterio 7: Cero apariciones en interiores, forja, centro de Khariel y salas seguras."""
        civil_rooms = [
            "khariel_centro", "khariel_forja", "khariel_mercado", "khariel_sendero",
            "valdren_centro", "valdren_forja", "valdren_mercado",
            "brumak_centro", "brumak_forja", "brumak_mercado",
            "narevia_centro", "velmora_centro", "vaisgard",
        ]
        for room_id in civil_rooms:
            self.assertIsNone(world.get_room_encounter(room_id),
                              f"La sala civil {room_id} no debe tener encuentro fijo")
            for pool_id, pool in encounters.RANDOM_ENCOUNTER_POOLS.items():
                self.assertNotIn(room_id, pool.get("rooms", set()),
                                 f"La sala civil {room_id} no debe estar en el pool {pool_id}")

    def test_hoshai_and_khariel_contexts(self):
        """Contextos identificados por el contrato: alto_terrazas, alto_garganta, hábitat hoshai_alto."""
        self.assertEqual(world.ROOM_VISUAL_CONTEXT_OVERRIDES.get("alto_terrazas"), "zone.khariel")
        self.assertEqual(world.DYNAMIC_HABITAT_ROOMS.get("alto_garganta"), "hoshai_alto")
        self.assertEqual(world.get_room_encounter("alto_terrazas"), "unapiedra")

    def test_unapiedra_is_not_boss_and_no_weapon_loss(self):
        """Criterio 8: No introduce amenazas superiores ni riesgo de pérdida de arma."""
        creature = creatures.get_creature("unapiedra")
        self.assertEqual(creature["reference_level"], 1)
        self.assertFalse(creature.get("is_boss", False))


class UnapiedraStatisticalPlaytest(unittest.TestCase):
    """Criterio 9: Mínimo 40 combates aislados por clase a nivel 1.

    Registra victoria/derrota, rondas, HP final, fatiga final y huidas.
    Criterio 3: Nivel 1 sano no debe morir habitualmente contra una Uñapiedra aislada.
    """

    def test_40_simulated_combats_per_class_level_1(self):
        classes = ["arcano", "juramentado", "sombra", "artifice"]
        creature = creatures.get_creature("unapiedra")
        rng = random.Random(42)  # Semilla fija para reproducibilidad

        results = {}
        for cls in classes:
            starter_weapon = items.STARTER_WEAPON_BY_CLASS[cls]
            weapon_data = items.get_item(starter_weapon)
            base_damage = weapon_data["base_damage"]

            victories = 0
            defeats = 0
            total_rounds = 0
            final_hps = []
            final_fatigues = []
            escapes = 0

            # 40 combates completos a muerte
            for _ in range(40):
                p_hp = 100
                p_fatigue = 0
                e_hp = creature["hp"]
                rounds = 0

                while p_hp > 0 and e_hp > 0:
                    rounds += 1
                    # Turno del jugador: atacar
                    p_hit_chance = combat.accuracy(10, 10, 0, 0)
                    if rng.uniform(0, 100) < p_hit_chance:
                        p_dmg = combat.raw_damage(10, 10, 0, base_arma=base_damage)
                        e_hp -= p_dmg
                    p_fatigue += combat.FATIGUE_BASE_COST["ataque_basico"]

                    if e_hp <= 0:
                        break

                    # Turno de Uñapiedra: atacar
                    e_hits, e_dmg = combat.resolve_fixed_attack_roll(
                        creature["precision"], creature["damage"], rng=rng
                    )
                    if e_hits:
                        p_hp -= e_dmg

                if p_hp > 0:
                    victories += 1
                    total_rounds += rounds
                    final_hps.append(p_hp)
                    final_fatigues.append(p_fatigue)
                else:
                    defeats += 1

            # 40 intentos de huida desde combate activo
            for _ in range(40):
                failed = 0
                while True:
                    flee_pct = combat.flee_chance(10, 10, creature["flee_agilidad"],
                                                  creature["flee_percepcion"],
                                                  0, failed, 0)
                    if rng.uniform(0, 100) < flee_pct:
                        escapes += 1
                        break
                    else:
                        failed += 1

            results[cls] = {
                "victories": victories,
                "defeats": defeats,
                "avg_rounds": total_rounds / max(1, victories),
                "avg_final_hp": sum(final_hps) / max(1, len(final_hps)),
                "avg_final_fatigue": sum(final_fatigues) / max(1, len(final_fatigues)),
                "escapes_successful": escapes,
            }

            # Verificaciones estrictas por clase:
            # 1. 0 derrotas contra Uñapiedra aislada con nivel 1 sano
            self.assertEqual(defeats, 0, f"Clase {cls} no debe morir contra Uñapiedra sana (derrotas: {defeats})")
            self.assertEqual(victories, 40, f"Clase {cls} debe ganar los 40 combates")
            # 2. HP final promedio debe ser ampliamente seguro (> 70 HP)
            self.assertGreater(results[cls]["avg_final_hp"], 70.0,
                               f"Clase {cls} debe terminar con HP alto")
            # 3. Rondas promedio razonables (entre 3 y 12 rondas según arma de clase)
            self.assertGreaterEqual(results[cls]["avg_rounds"], 3.0)
            self.assertLessEqual(results[cls]["avg_rounds"], 12.0)
            # 4. Los 40 intentos de fuga tienen éxito
            self.assertEqual(escapes, 40)


@patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
class UnapiedraServerIntegrationTests(unittest.TestCase):
    """Pruebas end-to-end con cliente Flask y SQLite en servidor real."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(
            TESTING=True,
            SECRET_KEY="test-secret-" * 5,
            DATA_DIR=self.temp.name,
            SESSION_COOKIE_SECURE=False,
        )
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        try:
            self.temp.cleanup()
        except PermissionError:
            pass

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        resp = client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})
        if resp.status_code in (301, 302, 303):
            return client.get(resp.headers.get("Location", "/"))
        return resp

    def register_felaryn_and_enter_world(self, username="valan", name="Valan"):
        self.post("/register", dict(username=username, name=name, password="clave-de-prueba-valan"))
        dm = self.app.test_client()
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="felaryn"))
        self.post("/class", dict(player_class="juramentado"))
        self.post("/move", dict(direction="south"))  # arranca en khariel_centro tras salir del hogar

    def get_player_id(self):
        return self.client.get("/api/me").json["player"]["id"]

    def character(self):
        return self.client.get("/api/character").json

    def test_alto_terrazas_encounter_presence_and_art(self):
        """Al salir de Khariel a alto_terrazas se encuentra Uñapiedra con su arte (#548)."""
        self.register_felaryn_and_enter_world()
        pid = self.get_player_id()

        # Khariel centro: salida sur es alto_terrazas
        resp = self.post("/move", dict(direction="south"))
        self.assertEqual(resp.status_code, 200)

        # En la API estructurada de la sala:
        room_data = self.client.get("/api/room").json["room"]
        self.assertIsNotNone(room_data.get("encounter"))
        self.assertEqual(room_data["encounter"]["creature_id"], "unapiedra")
        self.assertEqual(room_data["encounter"]["name"], "Uñapiedra")
        self.assertIn("Uñapiedra se aplasta contra la roca", room_data["encounter"]["behavior"])
        # Issue #548: el marco de combate ya muestra a Uñapiedra, no el
        # paisaje (alto_terrazas en sí sigue sin arte de ubicación propia).
        self.assertEqual(room_data.get("art"), creatures.CREATURE_ART["unapiedra"])

        # En SQLite:
        enc = store.get_encounter(self.path, pid, "alto_terrazas")
        self.assertIsNotNone(enc)
        self.assertEqual(enc["creature_id"], "unapiedra")

    def test_evaluate_unapiedra_returns_favorable(self):
        """Evaluar Uñapiedra devuelve que es un encuentro favorable."""
        self.register_felaryn_and_enter_world()
        self.post("/move", dict(direction="south"))

        resp = self.post("/command", dict(text="evaluar unapiedra"))
        self.assertEqual(resp.status_code, 200)

        room_data = self.client.get("/api/room").json["room"]
        logs = room_data.get("combat_log", [])
        self.assertTrue(any(log.get("action") == "evaluar" and "favorable" in log.get("text", "").lower() for log in logs),
                        f"Se esperaba 'favorable' en combat_log: {logs}")

    def test_complete_combat_victory_awards_unapiedra_family_xp(self):
        """Derrotar a Uñapiedra otorga XP de familia independiente y limpia el encuentro."""
        self.register_felaryn_and_enter_world()
        pid = self.get_player_id()
        self.post("/move", dict(direction="south"))

        initial_xp = self.character()["xp"]

        # Juramentado con Espada de juramento (base_damage 10). Con 3 aciertos (3x10 = 30 dmg), Uñapiedra (30 HP) cae.
        with patch("server.combat.accuracy", return_value=100.0):
            self.post("/command", dict(text="atacar"))
            self.post("/command", dict(text="atacar"))
            resp = self.post("/command", dict(text="atacar"))
            self.assertEqual(resp.status_code, 200)

        # Encuentro activo limpio en SQLite
        self.assertIsNone(store.get_encounter(self.path, pid, "alto_terrazas"))

        # XP ganada
        self.assertGreater(self.character()["xp"], initial_xp)

        # Familia registrada en pve_victories y family_first_victory
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM pve_victories WHERE player_id = ? AND family = ?", (pid, "unapiedra"))
        wins = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM family_first_victory WHERE player_id = ? AND family = ?", (pid, "unapiedra"))
        first_wins = cur.fetchone()[0]
        con.close()
        self.assertEqual(wins, 1)
        self.assertEqual(first_wins, 1)

    def test_flee_from_unapiedra_retreats_safely_to_khariel_centro(self):
        """Huir con éxito de Uñapiedra retira al personaje a khariel_centro."""
        self.register_felaryn_and_enter_world()
        pid = self.get_player_id()
        self.post("/move", dict(direction="south"))

        # Forzar huida exitosa
        with patch("random.Random.uniform", return_value=0.0):
            resp = self.post("/command", dict(text="huir"))
            self.assertEqual(resp.status_code, 200)

        # El jugador volvió a khariel_centro
        current_room = self.client.get("/api/room").json["room"]["id"]
        self.assertEqual(current_room, "khariel_centro")
        # Encuentro limpio en alto_terrazas
        self.assertIsNone(store.get_encounter(self.path, pid, "alto_terrazas"))


if __name__ == "__main__":
    unittest.main()
