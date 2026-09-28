"""REMAINING-FAUNA-BUNDLE #412: segunda oleada de fauna menor (#340, #342–#345).

Contratos mecánicos aprobados por Jugabilidad:
- Remojunco (#340): ref1, HP 24, prec 42, dmg 4, arm 0.00, flee_agi 16, flee_per 12
- Garralaja (#342): ref1, HP 22, prec 46, dmg 4, arm 0.00, flee_agi 17, flee_per 14
- Cavapolvo (#343): ref2, HP 35, prec 48, dmg 7, arm 0.05, flee_agi 9, flee_per 10
- Velacauce (#344): ref2, HP 27, prec 53, dmg 6, arm 0.00, flee_agi 15, flee_per 14
- Silbarisco (#345): ref1, HP 26, prec 43, dmg 4, arm 0.00, flee_agi 17, flee_per 13
"""
import random
import unittest

from server import combat, creatures, encounters, items, world


SECOND_WAVE_PROFILES = {
    # id: (name, level, hp, precision, damage, armor, agi, perception)
    "remojunco": ("Remojunco", 1, 24, 42, 4, 0.00, 16, 12),
    "garralaja": ("Garralaja", 1, 22, 46, 4, 0.00, 17, 14),
    "cavapolvo": ("Cavapolvo", 2, 35, 48, 7, 0.05, 9, 10),
    "velacauce": ("Velacauce", 2, 27, 53, 6, 0.00, 15, 14),
    "silbarisco": ("Silbarisco", 1, 26, 43, 4, 0.00, 17, 13),
}


class SecondWaveCreatureContractTests(unittest.TestCase):
    def test_five_profiles_match_approved_gameplay_contracts(self):
        """Los 5 perfiles de segunda oleada coinciden exactamente con los números de #340 y #342–#345."""
        for creature_id, (name, level, hp, precision, damage, armor, agi, perception) in SECOND_WAVE_PROFILES.items():
            with self.subTest(creature=creature_id):
                creature = creatures.get_creature(creature_id)
                self.assertIsNotNone(creature, f"Criatura '{creature_id}' no encontrada en catálogo.")
                self.assertEqual(creature["name"], name)
                self.assertEqual(creature["family"], creature_id)
                self.assertEqual(creature["reference_level"], level)
                self.assertEqual(creature["hp"], hp)
                self.assertEqual(creature["precision"], precision)
                self.assertEqual(creature["damage"], damage)
                self.assertEqual(creature.get("armor_reduction", 0.0), armor)
                self.assertEqual(creature["flee_agilidad"], agi)
                self.assertEqual(creature["flee_percepcion"], perception)
                self.assertTrue(creature["behavior_text"], "behavior_text no debe estar vacío")
                # Sin assets de arte aprobados: deben permanecer fuera de CREATURE_ART para marco neutral
                self.assertNotIn(creature_id, creatures.CREATURE_ART)

    def test_second_wave_creatures_have_no_unapproved_special_mechanics_or_c3_status(self):
        """No deben ser tratadas como jefes, ni amenazas C3, ni tener ataques preparados o multi-enemigo."""
        for creature_id in SECOND_WAVE_PROFILES:
            with self.subTest(creature=creature_id):
                creature = creatures.get_creature(creature_id)
                self.assertFalse(creature.get("is_boss", False))
                self.assertNotIn(creature_id, encounters.C3_THREAT_IDS)
                self.assertNotIn("special_attack", creature)
                self.assertNotIn("prepared_action", creature)
                self.assertNotIn("multi_enemy", creature)

    def test_creatures_appear_only_in_authorized_surface_branch_pools(self):
        """La segunda oleada sólo entra en pools de los ramales ya integrados (#458)."""
        authorized_rooms = {
            "remojunco": {"mh_02_bordes_vencidos", "mh_03_juncos_partidos", "mh_05_terreno_dos_aguas",
                           "mh_06_restos_cauce", "mh_08_rodeo_base", "mh_09_plataforma_caida"},
            "garralaja": {"ge_02_terrazas_rotas", "ge_03_repisa_viento", "ge_04_quiebre_lajas",
                          "ge_06_fisuras_paralelas", "ge_07_grava_fondo", "ge_08_ultima_luz_directa"},
            "cavapolvo": {"ca_04_montones_descarte", "ca_07_frente_quebrado"},
            "velacauce": {"cq_04_raices_ribera", "cq_06_paso_raices", "cq_07_orilla_blanda", "cq_08_recodo_sin_vista"},
            "silbarisco": {"bm_02_raices_sobre_roca", "bm_04_ladera_grava", "bm_05_saliente_raices",
                           "bm_06_terraza_exterior"},
        }
        for creature_id, expected_rooms in authorized_rooms.items():
            with self.subTest(creature=creature_id):
                actual_rooms = {
                    room
                    for pool in encounters.RANDOM_ENCOUNTER_POOLS.values()
                    if any(cid == creature_id for cid, _weight in pool["creatures"])
                    for room in pool["rooms"]
                }
                self.assertEqual(actual_rooms, expected_rooms)
                self.assertNotIn(creature_id, world.ROOM_ENCOUNTER.values(),
                                 f"{creature_id} no debe tener encuentro fijo sin contrato de sala.")

    def test_family_xp_and_progression_scale(self):
        """Verifica que la XP otorgada sea coherente con la escala de combate."""
        for creature_id, (_name, ref_level, _hp, _p, _d, _a, _fa, _fp) in SECOND_WAVE_PROFILES.items():
            for category in ("trivial", "favorable", "comparable"):
                xp_first = combat.combat_xp(
                    enemy_ref_level=ref_level,
                    category=category,
                    player_level=1,
                    is_first_family_victory=True,
                    repeats_in_last_10=1,
                )
                xp_repeated = combat.combat_xp(
                    enemy_ref_level=ref_level,
                    category=category,
                    player_level=1,
                    is_first_family_victory=False,
                    repeats_in_last_10=1,
                )
                self.assertGreater(xp_first, 0, f"Primera victoria contra {creature_id} debe dar XP > 0")
                self.assertGreater(xp_first, xp_repeated, f"Primera victoria debe incluir bono de familia para {creature_id}")

                # Antifarmeo reduce XP al repetirse
                xp_farmed = combat.combat_xp(
                    enemy_ref_level=ref_level,
                    category=category,
                    player_level=1,
                    is_first_family_victory=False,
                    repeats_in_last_10=6,
                )
                self.assertLessEqual(xp_farmed, xp_repeated)


class SecondWaveCreaturePlaytest(unittest.TestCase):
    """40 combates de referencia por clase y criatura; RNG reproducible según criterio de issues."""
    CLASSES = ("arcano", "juramentado", "sombra", "artifice")

    def test_40_simulated_combats_per_class_and_creature(self):
        rng = random.Random(412)
        for creature_id in SECOND_WAVE_PROFILES:
            creature = creatures.get_creature(creature_id)
            for player_class in self.CLASSES:
                with self.subTest(creature=creature_id, player_class=player_class):
                    weapon = items.get_item(items.STARTER_WEAPON_BY_CLASS[player_class])
                    victories = defeats = rounds_total = hp_total = fatigue_total = 0
                    for _ in range(40):
                        player_hp, enemy_hp, fatigue, rounds = 100.0, creature["hp"], 0, 0
                        while player_hp > 0 and enemy_hp > 0:
                            rounds += 1
                            if rng.uniform(0, 100) < combat.accuracy(10, 10, 0, 0):
                                damage = combat.raw_damage(10, 10, 0, base_arma=weapon["base_damage"])
                                enemy_hp -= combat.apply_armor_reduction(
                                    damage, creature.get("armor_reduction", 0.0))
                            fatigue += combat.FATIGUE_BASE_COST["ataque_basico"]
                            if enemy_hp <= 0:
                                break
                            hits, damage = combat.resolve_fixed_attack_roll(
                                creature["precision"], creature["damage"], rng=rng)
                            if hits:
                                player_hp -= damage
                        if player_hp > 0:
                            victories += 1
                            rounds_total += rounds
                            hp_total += player_hp
                            fatigue_total += fatigue
                        else:
                            defeats += 1

                    # Nivel 1 sano domina la fauna menor (casi 0 derrotas)
                    self.assertEqual(defeats, 0,
                                     f"{player_class} sufrió derrotas ({defeats}/40) contra {creature_id}")
                    self.assertEqual(victories, 40)
                    self.assertGreater(hp_total / victories, 50)
                    self.assertGreaterEqual(rounds_total / victories, 2)
                    self.assertLessEqual(rounds_total / victories, 12)
                    self.assertGreater(fatigue_total, 0)

    def test_flee_is_available_and_eventually_succeeds_for_every_creature(self):
        """Verifica que la huida sea viable y tenga éxito en pocos intentos contra toda criatura."""
        rng = random.Random(412)
        for creature_id in SECOND_WAVE_PROFILES:
            creature = creatures.get_creature(creature_id)
            for _ in range(40):
                failed = 0
                while failed < 10:
                    chance = combat.flee_chance(10, 10, creature["flee_agilidad"],
                                                creature["flee_percepcion"], 0, failed, 0)
                    if rng.uniform(0, 100) < chance:
                        break
                    failed += 1
                self.assertLess(failed, 10, f"{creature_id}: huida no consiguió salir tras {failed} intentos")


if __name__ == "__main__":
    unittest.main()
