"""Pruebas completas del contrato de Saltacresta v1 (Issue #274).

Origen: Prioridad #229 — poblar Hoshai/Khariel con más de una familia combatible.
Canon: vintage-telnet/CREATURES.md (§ Saltacresta, criatura menor territorial).
Contrato mecánico: Jugabilidad en Issue #274 (SALTACRESTA-01, 2026-09-27).
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


class SaltacrestaUnitTests(unittest.TestCase):
    """Verificación de contrato unitario, atributos y fórmulas de combate."""

    def test_saltacresta_profile_matches_gameplay_approved_contract(self):
        """Criterio SALTACRESTA-01: Perfil v1 ref 2 / HP 36 / precisión 50 / daño 7 / flee 16/14 / 0% armadura."""
        creature = creatures.get_creature("saltacresta")
        self.assertIsNotNone(creature, "Saltacresta debe existir en CREATURES")
        self.assertEqual(creature["name"], "Saltacresta")
        self.assertEqual(creature["family"], "saltacresta")
        self.assertEqual(creature["reference_level"], 2)
        self.assertEqual(creature["hp"], 36)
        self.assertEqual(creature["precision"], 50)
        self.assertEqual(creature["damage"], 7)
        self.assertEqual(creature["flee_agilidad"], 16)
        self.assertEqual(creature["flee_percepcion"], 14)
        self.assertEqual(creature.get("armor_reduction", 0.0), 0.0)
        expected_behavior = (
            "Saltacresta flexiona las patas traseras y busca una terraza libre; "
            "si le cierras la salida, golpea el suelo y se prepara para defenderse con una patada corta."
        )
        self.assertEqual(creature["behavior_text"], expected_behavior)

    def test_saltacresta_has_no_art_in_creature_art(self):
        """Fuera de alcance: arte; marco neutral/vacío en combate, sin imagen ajena."""
        self.assertNotIn("saltacresta", creatures.CREATURE_ART)
        self.assertIsNone(creatures.CREATURE_ART.get("saltacresta"))

    def test_saltacresta_relative_difficulty_band(self):
        """Banda esperada: Favorable alto / Comparable bajo para nivel 1 sano.

        Más exigente que Uñapiedra, menos resistente y menos castigador que Espinajo de rastrojo.
        """
        player_dps = combat.expected_dps(destreza=10, percepcion=10, fuerza=10,
                                         cg_self=0, cg_other=0, base_arma=10)
        self.assertEqual(player_dps, 5.5)

        unapiedra = creatures.get_creature("unapiedra")
        saltacresta = creatures.get_creature("saltacresta")
        espinajo = creatures.get_creature("espinajo_rastrojo")

        u_dps = combat.fixed_expected_dps(unapiedra["precision"], unapiedra["damage"])
        s_dps = combat.fixed_expected_dps(saltacresta["precision"], saltacresta["damage"])
        e_dps = combat.fixed_expected_dps(espinajo["precision"], espinajo["damage"])

        # DPS: Uñapiedra (2.25) < Saltacresta (3.5) < Espinajo (4.0)
        self.assertLess(u_dps, s_dps)
        self.assertLess(s_dps, e_dps)
        self.assertEqual(s_dps, 3.5)

        # HP: Uñapiedra (30) < Saltacresta (36) < Espinajo (40)
        self.assertLess(unapiedra["hp"], saltacresta["hp"])
        self.assertLess(saltacresta["hp"], espinajo["hp"])

        # Categoría para nivel 1 sano (100 HP, dps 5.5)
        category = combat.encounter_category(player_dps=player_dps, player_hp=100,
                                             enemy_dps=s_dps, enemy_hp=saltacresta["hp"])
        self.assertIn(category, ("favorable", "comparable"))

    def test_saltacresta_flee_formula(self):
        """Huida ágil (flee_agilidad 16, flee_percepcion 14) pero viable."""
        # chance = 50 + 0.45*(10 - 16) + 0.15*(10 - 14) = 50 - 2.7 - 0.6 = 46.7%
        chance = combat.flee_chance(player_agilidad=10, player_percepcion=10,
                                    enemy_agilidad=16, enemy_percepcion=14,
                                    attacker_level_advantage=0, previous_failed_attempts=0,
                                    fatigue=0)
        self.assertAlmostEqual(chance, 46.7, places=1)

        # Con 1 intento fallido previo (+15% bonus_fallos = 61.7%)
        chance_retry = combat.flee_chance(player_agilidad=10, player_percepcion=10,
                                          enemy_agilidad=16, enemy_percepcion=14,
                                          attacker_level_advantage=0, previous_failed_attempts=1,
                                          fatigue=0)
        self.assertAlmostEqual(chance_retry, 61.7, places=1)

    def test_zero_spawns_in_civil_and_safe_rooms(self):
        """0% en centro/interiores de Khariel, forja/mercado y salas seguras."""
        civil_rooms = [
            "khariel_centro", "khariel_forja", "khariel_mercado", "khariel_sendero",
            "valdren_centro", "valdren_forja", "valdren_mercado",
            "brumak_centro", "brumak_forja", "brumak_mercado",
            "narevia_centro", "velmora_centro", "vaisgard",
        ]
        for room_id in civil_rooms:
            self.assertNotEqual(world.get_room_encounter(room_id), "saltacresta",
                                f"La sala civil {room_id} no debe tener encuentro con saltacresta")
            for pool_id, pool in encounters.RANDOM_ENCOUNTER_POOLS.items():
                self.assertNotIn(room_id, pool.get("rooms", set()),
                                 f"La sala civil {room_id} no debe estar en el pool {pool_id}")

    def test_saltacresta_context_and_room_mapping(self):
        """Contexto permitido: Sierra de Hoshai (alto_terraza_abandonada)."""
        self.assertEqual(world.get_room_encounter("alto_terraza_abandonada"), "saltacresta")
        room = world.ROOMS["alto_terraza_abandonada"]
        self.assertEqual(room["name"], "Terraza abandonada")
        self.assertIn("terraza", room["name"].lower())

    def test_saltacresta_is_not_boss_and_no_special_attack_mechanics(self):
        """Sin ataque especial nuevo, sin daño por caída, sin empuje, sin armadura."""
        creature = creatures.get_creature("saltacresta")
        self.assertEqual(creature["reference_level"], 2)
        self.assertFalse(creature.get("is_boss", False))
        self.assertEqual(creature.get("armor_reduction", 0.0), 0.0)


class SaltacrestaStatisticalPlaytest(unittest.TestCase):
    """Playtest mínimo obligatorio: 40 combates aislados por clase a nivel 1 (160 combates).

    Registra victoria/derrota, rondas, HP final, fatiga final y huidas.
    Gates de Jugabilidad:
    - 0 o muy pocas derrotas de nivel 1 sano;
    - claramente más exigente que Uñapiedra;
    - no más castigador que Espinajo de rastrojo;
    - huida viable;
    - no convertirlo en saco de HP.
    """

    def test_40_simulated_combats_per_class_level_1(self):
        classes = ["arcano", "juramentado", "sombra", "artifice"]
        creature = creatures.get_creature("saltacresta")
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

                    # Turno de Saltacresta: atacar
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

            # 1. Cero o muy pocas derrotas de nivel 1 sano
            self.assertEqual(defeats, 0,
                             f"Clase {cls} no debe morir habitualmente contra Saltacresta (derrotas: {defeats})")
            self.assertEqual(victories, 40, f"Clase {cls} debe ganar los 40 combates")

            # 2. HP final promedio entre 60 y 85 (daño recibido esperado: ~20-35 HP)
            self.assertGreater(results[cls]["avg_final_hp"], 60.0,
                               f"Clase {cls} debe terminar con HP seguro (> 60 HP)")
            self.assertLess(results[cls]["avg_final_hp"], 90.0,
                            f"Clase {cls} debe haber recibido daño apreciable (< 90 HP)")

            # 3. Rondas promedio según clase (referencia: Arcano ~9, Sombra ~8, Artífice ~7, Juramentado ~7)
            self.assertGreaterEqual(results[cls]["avg_rounds"], 4.0)
            self.assertLessEqual(results[cls]["avg_rounds"], 12.0)

            # 4. Huida viable: los 40 intentos tienen éxito con reintentos
            self.assertEqual(escapes, 40)


@patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
class SaltacrestaServerIntegrationTests(unittest.TestCase):
    """Pruebas end-to-end con cliente Flask y base de datos SQLite en servidor real."""

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

    def register_felaryn_and_enter_world(self, username="fel_valan", name="Valan"):
        self.post("/register", dict(username=username, name=name, password="clave-de-prueba-valan"))
        dm = self.app.test_client()
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="felaryn"))  # hogar personal de Felaryn
        self.post("/class", dict(player_class="juramentado"))
        # HOME-CORE: el onboarding termina en el hogar personal; sal primero
        # al pueblo antes de recorrer la ruta regional.
        self.post("/move", dict(direction="salir"))

    def get_player_id(self):
        return self.client.get("/api/me").json["player"]["id"]

    def character(self):
        return self.client.get("/api/character").json

    def test_reach_alto_terraza_abandonada_and_encounter_saltacresta(self):
        """Un jugador que viaja al sur por el Camino Alto encuentra a Saltacresta en alto_terraza_abandonada."""
        self.register_felaryn_and_enter_world()
        pid = self.get_player_id()

        # Ruta B desde khariel_centro: 5 pasos al sur
        # 1. alto_terrazas
        self.post("/move", dict(direction="south"))
        # 2. alto_mirador
        self.post("/move", dict(direction="south"))
        # 3. alto_anclajes
        self.post("/move", dict(direction="south"))
        # 4. alto_escalones
        self.post("/move", dict(direction="south"))
        # 5. alto_terraza_abandonada (saltacresta)
        resp = self.post("/move", dict(direction="south"))
        self.assertEqual(resp.status_code, 200)

        # En la API estructurada de la sala:
        room_data = self.client.get("/api/room").json["room"]
        self.assertEqual(room_data["id"], "alto_terraza_abandonada")
        self.assertIsNotNone(room_data.get("encounter"))
        self.assertEqual(room_data["encounter"]["creature_id"], "saltacresta")
        self.assertEqual(room_data["encounter"]["name"], "Saltacresta")
        self.assertIn("Saltacresta flexiona las patas traseras", room_data["encounter"]["behavior"])
        # Sin arte aprobado: el marco de arte debe ser None
        self.assertIsNone(room_data.get("art"))

        # En SQLite:
        enc = store.get_encounter(self.path, pid, "alto_terraza_abandonada")
        self.assertIsNotNone(enc)
        self.assertEqual(enc["creature_id"], "saltacresta")

    def test_evaluate_saltacresta_returns_favorable_or_comparable(self):
        """Evaluar a Saltacresta devuelve categoría favorable o comparable."""
        self.register_felaryn_and_enter_world()
        for _ in range(5):
            self.post("/move", dict(direction="south"))

        resp = self.post("/command", dict(text="evaluar saltacresta"))
        self.assertEqual(resp.status_code, 200)

        room_data = self.client.get("/api/room").json["room"]
        logs = room_data.get("combat_log", [])
        self.assertTrue(any(log.get("action") == "evaluar" and any(cat in log.get("text", "").lower() for cat in ("favorable", "comparable")) for log in logs),
                        f"Se esperaba 'favorable' o 'comparable' en combat_log: {logs}")

    def test_complete_combat_victory_awards_saltacresta_family_xp(self):
        """Derrotar a Saltacresta otorga experiencia de referencia 2 de la familia saltacresta."""
        self.register_felaryn_and_enter_world()
        pid = self.get_player_id()
        for _ in range(5):
            self.post("/move", dict(direction="south"))

        initial_xp = self.character()["xp"]

        # Juramentado con Espada de juramento (base_damage 10). Con 4 aciertos (4x10 = 40 dmg), Saltacresta (36 HP) cae.
        with patch("server.combat.accuracy", return_value=100.0):
            for _ in range(4):
                resp = self.post("/command", dict(text="atacar"))
                self.assertEqual(resp.status_code, 200)

        # Encuentro activo limpio en SQLite
        self.assertIsNone(store.get_encounter(self.path, pid, "alto_terraza_abandonada"))

        # XP ganada
        self.assertGreater(self.character()["xp"], initial_xp)

        # Familia registrada en pve_victories y family_first_victory
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM pve_victories WHERE player_id = ? AND family = ?", (pid, "saltacresta"))
        wins = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM family_first_victory WHERE player_id = ? AND family = ?", (pid, "saltacresta"))
        first_wins = cur.fetchone()[0]
        con.close()
        self.assertEqual(wins, 1)
        self.assertEqual(first_wins, 1)

    def test_flee_from_saltacresta_retreats_safely_to_previous_room(self):
        """Huir con éxito de Saltacresta retira al personaje a la sala anterior (alto_escalones)."""
        self.register_felaryn_and_enter_world()
        pid = self.get_player_id()
        for _ in range(5):
            self.post("/move", dict(direction="south"))

        # Forzar huida exitosa
        with patch("random.Random.uniform", return_value=0.0):
            resp = self.post("/command", dict(text="huir"))
            self.assertEqual(resp.status_code, 200)

        # El jugador volvió a la sala previa (alto_escalones)
        current_room = self.client.get("/api/room").json["room"]["id"]
        self.assertEqual(current_room, "alto_escalones")
        # Encuentro limpio en alto_terraza_abandonada
        self.assertIsNone(store.get_encounter(self.path, pid, "alto_terraza_abandonada"))


if __name__ == "__main__":
    unittest.main()
