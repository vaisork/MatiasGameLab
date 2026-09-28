"""REGIONAL-FAUNA-BUNDLE #406: perfiles y pools Korven/Lethra/Nhal."""
import random
import unittest
from unittest.mock import Mock, patch

from server import combat, creatures, encounters, items, world


PROFILES = {
    "cascapedernal": ("Cascapedernal", 1, 34, 42, 5, 0.10, 8, 9),
    "colagrieta": ("Colagrieta", 2, 33, 52, 7, 0.00, 14, 13),
    "pinzajunco": ("Pinzajunco", 1, 32, 47, 6, 0.05, 8, 10),
    "saltalodo": ("Saltalodo", 2, 38, 50, 7, 0.00, 14, 12),
    "rondamusgo": ("Rondamusgo", 1, 29, 44, 5, 0.00, 14, 12),
    "hilaria_niebla": ("Hilaria de niebla", 2, 34, 52, 7, 0.00, 10, 14),
}

# room_id -> (chance, creature weights). Zeros from the approved tables are
# asserted separately so reserved/transitional rooms cannot enter by accident.
HOSHAI = {
    "alto_anclajes": (0.10, (("unapiedra", 100),)),
    "alto_escalones": (0.20, (("unapiedra", 50), ("saltacresta", 50))),
    "alto_terraza_abandonada": (0.30, (("unapiedra", 50), ("saltacresta", 50))),
    "alto_garganta": (0.30, (("unapiedra", 100),)),
    "alto_cruce_alturas": (0.20, (("unapiedra", 50), ("saltacresta", 50))),
    "alto_pinar": (0.20, (("saltacresta", 100),)),
    "alto_descenso": (0.30, (("unapiedra", 50), ("saltacresta", 50))),
    "alto_ultimo_risco": (0.30, (("unapiedra", 75), ("saltacresta", 25))),
    "alto_camino_falda": (0.10, (("unapiedra", 50), ("saltacresta", 50))),
}

KORVEN = {
    "piedra_pared_anclajes": (0.10, (("cascapedernal", 100),)),
    "piedra_paso_corto": (0.20, (("cascapedernal", 60), ("colagrieta", 40))),
    "piedra_patio_abierto": (0.10, (("cascapedernal", 100),)),
    "piedra_hendiduras": (0.30, (("cascapedernal", 40), ("colagrieta", 60))),
    "piedra_pared_partida": (0.20, (("cascapedernal", 50), ("colagrieta", 50))),
    "piedra_meseta_baja": (0.20, (("cascapedernal", 100),)),
    "piedra_cruce_montones": (0.20, (("cascapedernal", 100),)),
    "piedra_cavidades": (0.30, (("cascapedernal", 35), ("colagrieta", 65))),
    "piedra_ultimo_corredor": (0.30, (("cascapedernal", 40), ("colagrieta", 60))),
    "piedra_suelo_quebrado": (0.10, (("cascapedernal", 100),)),
}
LETHRA = {
    "juncos_postes": (0.10, (("pinzajunco", 100),)),
    "juncos_juncal": (0.20, (("pinzajunco", 55), ("saltalodo", 45))),
    "juncos_paso_raices": (0.30, (("pinzajunco", 50), ("saltalodo", 50))),
    "juncos_agua_entre_caminos": (0.30, (("pinzajunco", 55), ("saltalodo", 45))),
    "juncos_pasarela_larga": (0.20, (("saltalodo", 100),)),
    "juncos_islas_bajas": (0.20, (("pinzajunco", 50), ("saltalodo", 50))),
    "juncos_canal_ancho": (0.30, (("pinzajunco", 55), ("saltalodo", 45))),
    "juncos_ultimos": (0.30, (("pinzajunco", 40), ("saltalodo", 60))),
    "juncos_corrientes": (0.10, (("pinzajunco", 100),)),
}
NHAL = {
    "sombra_raices_cruzadas": (0.20, (("rondamusgo", 50), ("hilaria_niebla", 50))),
    "sombra_claro_pequeno": (0.10, (("rondamusgo", 100),)),
    "sombra_sendero_doble": (0.20, (("rondamusgo", 55), ("hilaria_niebla", 45))),
    "sombra_niebla_baja": (0.30, (("rondamusgo", 40), ("hilaria_niebla", 60))),
    "sombra_arbol_caido": (0.30, (("rondamusgo", 40), ("hilaria_niebla", 60))),
    "sombra_raiz_alta": (0.30, (("rondamusgo", 50), ("hilaria_niebla", 50))),
    "sombra_bosque_abierto": (0.10, (("rondamusgo", 100),)),
}
REGIONS = {"HOSHAI-01": HOSHAI, "KORVEN-01": KORVEN, "LETHRA-01": LETHRA, "NHAL-01": NHAL}

RESERVED = {
    "HOSHAI-01": {"alto_terrazas", "alto_mirador", "alto_puente_viento", "alto_agua_fria"},
    "KORVEN-01": {"piedra_patio_exterior", "piedra_primer_monton", "piedra_abrigo_viento", "piedra_clara"},
    "LETHRA-01": {"juncos_plataformas", "juncos_pasarela_antigua", "juncos_isla_refugio",
                  "juncos_embarcadero", "juncos_suelo_firme", "juncos_entrada_veyra"},
    "NHAL-01": {"sombra_borde", "sombra_tronco", "sombra_tres_marcas", "sombra_claro_escucha",
                "sombra_hojas_claras", "sombra_ultimas_senales", "sombra_entrada_veyra"},
}


class RegionalCreatureContractTests(unittest.TestCase):
    def test_six_profiles_match_approved_gameplay_contracts(self):
        for creature_id, (name, level, hp, precision, damage, armor, agi, perception) in PROFILES.items():
            with self.subTest(creature=creature_id):
                creature = creatures.get_creature(creature_id)
                self.assertIsNotNone(creature)
                self.assertEqual(creature["name"], name)
                self.assertEqual(creature["family"], creature_id)
                self.assertEqual(creature["reference_level"], level)
                self.assertEqual(creature["hp"], hp)
                self.assertEqual(creature["precision"], precision)
                self.assertEqual(creature["damage"], damage)
                self.assertEqual(creature.get("armor_reduction", 0.0), armor)
                self.assertEqual(creature["flee_agilidad"], agi)
                self.assertEqual(creature["flee_percepcion"], perception)
                self.assertTrue(creature["behavior_text"])
                self.assertNotIn(creature_id, creatures.CREATURE_ART)

    def test_new_creatures_have_no_unapproved_special_mechanics_or_c3_status(self):
        for creature_id in PROFILES:
            creature = creatures.get_creature(creature_id)
            self.assertFalse(creature.get("is_boss", False))
            self.assertNotIn(creature_id, encounters.C3_THREAT_IDS)
            self.assertNotIn("special_attack", creature)


class RegionalPoolContractTests(unittest.TestCase):
    def test_every_pool_room_chance_and_weight_matches_approved_tables(self):
        encounters.validate_pools(encounters.RANDOM_ENCOUNTER_POOLS)
        expected = {**KORVEN, **LETHRA, **NHAL}
        edran_rooms = {
            "valdren_sendero", "valdren_camino_hundido", "valdren_parcelas_exteriores",
            "valdren_campo_rastrojo", "valdren_campos_sin_cerca",
        }
        surface_branch_rooms = {
            "bm_02_raices_sobre_roca", "bm_04_ladera_grava", "bm_05_saliente_raices",
            "bm_06_terraza_exterior", "bm_07_risco_sombreado", "bm_08_antesala_boca",
            "cq_02_orilla_juncos_bajos", "cq_04_raices_ribera", "cq_05_recodo_tronco",
            "cq_06_paso_raices", "cq_07_orilla_blanda", "cq_08_recodo_sin_vista",
            "ca_02_patio_grava", "ca_03_plataforma_baja", "ca_04_montones_descarte",
            "ca_06_plataforma_alta", "ca_07_frente_quebrado", "ca_08_paso_bloques",
            "ge_02_terrazas_rotas", "ge_03_repisa_viento", "ge_04_quiebre_lajas",
            "ge_06_fisuras_paralelas", "ge_07_grava_fondo", "ge_08_ultima_luz_directa",
            "mh_02_bordes_vencidos", "mh_03_juncos_partidos", "mh_05_terreno_dos_aguas",
            "mh_06_restos_cauce", "mh_08_rodeo_base", "mh_09_plataforma_caida",
        }
        all_pool_rooms = {room for pool in encounters.RANDOM_ENCOUNTER_POOLS.values() for room in pool["rooms"]}
        self.assertTrue(surface_branch_rooms <= all_pool_rooms)
        self.assertEqual(all_pool_rooms - edran_rooms - surface_branch_rooms, set(expected))
        for room_id, (chance, weighted) in expected.items():
            with self.subTest(room=room_id):
                pool = encounters.pool_for_room(room_id)
                self.assertIsNotNone(world.get_room(room_id))
                self.assertIsNone(world.get_room_encounter(room_id))
                self.assertEqual(pool["chance"], chance)
                self.assertEqual(pool["creatures"], list(weighted))

    def test_reserved_and_zero_chance_rooms_are_excluded(self):
        all_reserved = set().union(*RESERVED.values())
        all_active = {room for config in REGIONS.values() for room in config}
        self.assertTrue(all_reserved.isdisjoint(all_active))
        for room_id in all_reserved:
            with self.subTest(room=room_id):
                self.assertIsNone(encounters.pool_for_room(room_id))

    def test_regions_do_not_mix_families_or_admit_threats(self):
        allowed = {
            "HOSHAI-01": {"unapiedra", "saltacresta"},
            "KORVEN-01": {"cascapedernal", "colagrieta"},
            "LETHRA-01": {"pinzajunco", "saltalodo"},
            "NHAL-01": {"rondamusgo", "hilaria_niebla"},
        }
        for region, config in REGIONS.items():
            ids = {cid for _chance, entries in config.values() for cid, _weight in entries}
            self.assertEqual(ids, allowed[region])
            self.assertTrue(encounters.C3_THREAT_IDS.isdisjoint(ids))
        self.assertFalse(encounters.C3_THREAT_IDS.intersection(
            cid for pool in encounters.RANDOM_ENCOUNTER_POOLS.values()
            for cid, _weight in pool["creatures"]))

    def test_scripted_encounter_preempts_regional_pool_without_rng(self):
        for room_id in ("alto_escalones", "piedra_hendiduras"):
            with self.subTest(room=room_id):
                rng = Mock()
                with patch.dict(world.ROOM_ENCOUNTER, {room_id: "espinajo_rastrojo"}):
                    self.assertEqual(
                        encounters.get_encounter_for_room(room_id, rng),
                        "espinajo_rastrojo",
                    )
                self.assertEqual(rng.mock_calls, [])

    def test_hoshai_exact_mapping_and_zero_percent_pauses(self):
        for room_id, (chance, weighted) in HOSHAI.items():
            with self.subTest(room=room_id):
                pool = encounters.pool_for_room(room_id)
                self.assertIsNotNone(pool)
                self.assertEqual(pool["chance"], chance)
                self.assertEqual(pool["creatures"], list(weighted))
                self.assertEqual(world.get_room_region(room_id), "hoshai")
        for room_id in RESERVED["HOSHAI-01"]:
            with self.subTest(pause=room_id):
                self.assertIsNone(encounters.pool_for_room(room_id))

    def test_hoshai_ecological_exclusions_and_c3_boundary(self):
        active_ids = {
            creature_id
            for room_id in HOSHAI
            for creature_id, _weight in encounters.pool_for_room(room_id)["creatures"]
        }
        self.assertEqual(active_ids, {"unapiedra", "saltacresta"})
        self.assertNotIn("rasgacumbres", active_ids)
        self.assertTrue(encounters.C3_THREAT_IDS.isdisjoint(active_ids))

        only_unapiedra = {"alto_anclajes", "alto_garganta"}
        only_saltacresta = {"alto_pinar"}
        for room_id in only_unapiedra:
            self.assertEqual(encounters.pool_for_room(room_id)["creatures"], [("unapiedra", 100)])
        for room_id in only_saltacresta:
            self.assertEqual(encounters.pool_for_room(room_id)["creatures"], [("saltacresta", 100)])

    def test_pool_selection_is_deterministic_and_respects_chance_and_weights(self):
        for region, config in REGIONS.items():
            for room_id, (chance, weighted) in config.items():
                with self.subTest(region=region, room=room_id):
                    def sample():
                        rng = random.Random(406)
                        return [encounters.get_encounter_for_room(room_id, rng) for _ in range(5000)]
                    results = sample()
                    self.assertEqual(results, sample())
                    hits = [result for result in results if result is not None]
                    self.assertAlmostEqual(len(hits) / len(results), chance, delta=0.025)
                    for creature_id, weight in weighted:
                        share = hits.count(creature_id) / len(hits)
                        self.assertAlmostEqual(share, weight / sum(w for _, w in weighted), delta=0.06)

    def test_twenty_complete_route_walks_per_region_keep_pauses_and_pacing(self):
        route_for_region = {"HOSHAI-01": "B", "KORVEN-01": "C", "LETHRA-01": "D", "NHAL-01": "E"}
        for region, route_key in route_for_region.items():
            route = world.ROUTE_CHAINS[route_key][0]
            counts = []
            for walk in range(20):
                rng = random.Random(40600 + walk)
                count = sum(encounters.get_encounter_for_room(room_id, rng) is not None
                            for room_id in route[1:])
                counts.append(count)
            with self.subTest(region=region):
                self.assertTrue(any(count == 0 for count in counts), counts)
                transitions = (len(route) - 1) * len(counts)
                encounter_rate_per_ten_moves = sum(counts) / transitions * 10
                self.assertLessEqual(encounter_rate_per_ten_moves, 4.0)


class RegionalCreaturePlaytest(unittest.TestCase):
    """40 combates de referencia por clase y criatura; RNG reproducible."""
    CLASSES = ("arcano", "juramentado", "sombra", "artifice")

    def test_40_simulated_combats_per_class_and_creature(self):
        rng = random.Random(406)
        for creature_id in PROFILES:
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
                    # Los seis contratos tienen banda favorable/comparable bajo
                    # para un nivel 1 sano; nunca deben producir derrotas aquí.
                    self.assertEqual(defeats, 0)
                    self.assertEqual(victories, 40)
                    self.assertGreater(hp_total / victories, 50)
                    self.assertGreaterEqual(rounds_total / victories, 3)
                    self.assertLessEqual(rounds_total / victories, 12)
                    self.assertGreater(fatigue_total, 0)

    def test_flee_is_available_and_eventually_succeeds_for_every_creature(self):
        rng = random.Random(406)
        for creature_id in PROFILES:
            creature = creatures.get_creature(creature_id)
            for _ in range(40):
                failed = 0
                while failed < 10:
                    chance = combat.flee_chance(10, 10, creature["flee_agilidad"],
                                                creature["flee_percepcion"], 0, failed, 0)
                    if rng.uniform(0, 100) < chance:
                        break
                    failed += 1
                self.assertLess(failed, 10, f"{creature_id}: huida no consiguió salir")


if __name__ == "__main__":
    unittest.main()
