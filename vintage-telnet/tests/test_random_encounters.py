"""Motor de encuentros aleatorios (Issue #160): los encuentros fijos de El
lindero roto mandan, las salas elegibles tiran el dado de su pool, las no
elegibles nunca generan criatura y la configuración rota no pasa en silencio."""
import random
import re
import tempfile
import unittest
from unittest.mock import Mock, patch

from server.app import create_app
from server import encounters, store, world

ROAD_POOL = {
    "prueba_camino": {
        "rooms": {"valdren_sendero", "valdren_camino_parcela"},
        "chance": 0.5,
        "gameplay_override": True,  # solo pruebas: fuera de la banda 10–35 %
        "creatures": [("mordelinde", 3), ("espinajo_rastrojo", 1)],
    },
}


class AlwaysRoll:
    """rng de prueba: random() fijo y choices() elige por índice."""
    def __init__(self, value, pick=0):
        self.value, self.pick = value, pick

    def random(self):
        return self.value

    def choices(self, population, weights=None, k=1):
        return [population[self.pick]]


class EngineTests(unittest.TestCase):
    # Contrato EDRAN-01 (#207), independiente de los perfiles del motor.
    EDRAN_ROOMS = {
        "valdren_sendero": (0.10, 85, 15),
        "valdren_camino_hundido": (0.20, 75, 25),
        "valdren_parcelas_exteriores": (0.20, 75, 25),
        "valdren_campo_rastrojo": (0.30, 65, 35),
        "valdren_campos_sin_cerca": (0.30, 65, 35),
    }

    def test_production_config_matches_edran_01(self):
        encounters.validate_pools(encounters.RANDOM_ENCOUNTER_POOLS)
        self.assertEqual(len(encounters.RANDOM_ENCOUNTER_POOLS), 3)
        rooms = set().union(*(p["rooms"] for p in encounters.RANDOM_ENCOUNTER_POOLS.values()))
        self.assertEqual(rooms, set(self.EDRAN_ROOMS))
        for room, (chance, mordelinde, espinajo) in self.EDRAN_ROOMS.items():
            with self.subTest(room=room):
                pool = encounters.pool_for_room(room)
                self.assertEqual(pool["chance"], chance)
                self.assertEqual(pool["creatures"],
                                 [("mordelinde", mordelinde), ("espinajo_rastrojo", espinajo)])
                self.assertIsNone(world.get_room_encounter(room))

    def test_edran_excludes_every_other_room_and_cornalomo(self):
        for room in set(world.ROOMS) - self.EDRAN_ROOMS.keys():
            with self.subTest(room=room):
                self.assertIsNone(encounters.pool_for_room(room))
                rng = Mock()
                self.assertEqual(encounters.get_encounter_for_room(room, rng),
                                 world.get_room_encounter(room))
                self.assertEqual(rng.mock_calls, [])
        for pool in encounters.RANDOM_ENCOUNTER_POOLS.values():
            self.assertNotIn("cornalomo", [cid for cid, _ in pool["creatures"]])

    def test_edran_chance_boundaries_and_exact_weights_reach_rng(self):
        for room, (chance, mordelinde, espinajo) in self.EDRAN_ROOMS.items():
            with self.subTest(room=room):
                rng = Mock()
                rng.random.return_value = chance - 0.000001
                rng.choices.return_value = ["espinajo_rastrojo"]
                self.assertEqual(encounters.get_encounter_for_room(room, rng), "espinajo_rastrojo")
                rng.choices.assert_called_once_with(
                    ["mordelinde", "espinajo_rastrojo"], weights=[mordelinde, espinajo], k=1)
                rng.reset_mock()
                rng.random.return_value = chance
                self.assertIsNone(encounters.get_encounter_for_room(room, rng))
                rng.choices.assert_not_called()

    def test_scripted_encounter_preempts_an_active_edran_pool_without_rng(self):
        rng = Mock()
        with patch.dict(world.ROOM_ENCOUNTER, {"valdren_sendero": "espinajo_rastrojo"}):
            self.assertEqual(encounters.get_encounter_for_room("valdren_sendero", rng),
                             "espinajo_rastrojo")
        self.assertEqual(rng.mock_calls, [])

    def test_edran_distribution_is_reproducible_with_injected_rng(self):
        for room, (chance, mordelinde, _) in self.EDRAN_ROOMS.items():
            with self.subTest(room=room):
                def sample():
                    rng = random.Random(207)
                    return [encounters.get_encounter_for_room(room, rng) for _ in range(10000)]
                results = sample()
                self.assertEqual(results, sample())
                hits = [creature for creature in results if creature is not None]
                self.assertEqual(set(hits), {"mordelinde", "espinajo_rastrojo"})
                self.assertAlmostEqual(len(hits) / len(results), chance, delta=0.015)
                self.assertAlmostEqual(hits.count("mordelinde") / len(hits),
                                       mordelinde / 100, delta=0.04)

    def test_fixed_encounter_wins_over_random_pool(self):
        for value in (0.0, 0.99):
            rng = AlwaysRoll(value, pick=1)
            self.assertEqual(encounters.get_encounter_for_room("valdren_camino_parcela", rng, ROAD_POOL),
                             "mordelinde")
        self.assertEqual(encounters.get_encounter_for_room("valdren_camino_cerca", AlwaysRoll(0.0), ROAD_POOL),
                         "espinajo_rastrojo")

    def test_eligible_room_can_return_different_creatures(self):
        self.assertEqual(encounters.get_encounter_for_room("valdren_sendero", AlwaysRoll(0.1, 0), ROAD_POOL),
                         "mordelinde")
        self.assertEqual(encounters.get_encounter_for_room("valdren_sendero", AlwaysRoll(0.1, 1), ROAD_POOL),
                         "espinajo_rastrojo")
        # Por encima de chance no aparece nada.
        self.assertIsNone(encounters.get_encounter_for_room("valdren_sendero", AlwaysRoll(0.5), ROAD_POOL))
        seen = {encounters.get_encounter_for_room("valdren_sendero", random.Random(seed), ROAD_POOL)
                for seed in range(200)}
        self.assertEqual(seen, {None, "mordelinde", "espinajo_rastrojo"})

    def test_ineligible_room_never_spawns(self):
        for room_id in ("valdren_centro", "valdren_forja", "valdren_camino_lindero"):
            for seed in range(50):
                self.assertIsNone(encounters.get_encounter_for_room(room_id, random.Random(seed), ROAD_POOL))

    def test_same_seed_gives_same_sequence(self):
        def run(seed):
            rng = random.Random(seed)
            return [encounters.get_encounter_for_room("valdren_sendero", rng, ROAD_POOL) for _ in range(30)]
        self.assertEqual(run(7), run(7))

    def test_weights_are_respected(self):
        rng = random.Random(1)
        pools = {"p": {**ROAD_POOL["prueba_camino"], "chance": 1.0}}
        results = [encounters.get_encounter_for_room("valdren_sendero", rng, pools) for _ in range(2000)]
        share = results.count("mordelinde") / len(results)
        self.assertAlmostEqual(share, 0.75, delta=0.05)

    def test_invalid_configurations_are_rejected(self):
        base = ROAD_POOL["prueba_camino"]
        broken = [
            {**base, "creatures": [("no_existe", 1)]},
            {**base, "creatures": []},
            {**base, "rooms": set()},
            {**base, "rooms": {"sala_fantasma"}},
            {**base, "chance": 0},
            {**base, "chance": 1.5},
            {**base, "chance": True},
            {**base, "creatures": [("mordelinde", 0)]},
            {**base, "creatures": [("mordelinde", -2)]},
            {**base, "creatures": [("mordelinde",)]},
        ]
        for pool in broken:
            with self.subTest(pool=pool), self.assertRaises(encounters.InvalidPoolConfig):
                encounters.validate_pools({"roto": pool})
        with self.assertRaises(encounters.InvalidPoolConfig):
            encounters.validate_pools({"a": base, "b": {**base, "rooms": {"valdren_sendero"}}})

    def test_density_profiles_follow_gameplay_band(self):
        # RANDOM_ENCOUNTER_GAMEPLAY.md §2 y GAMEPLAY.md §33.3.
        self.assertEqual(encounters.DENSITY["camino"], 0.20)
        plain = {"rooms": {"valdren_sendero"}, "creatures": [("mordelinde", 70), ("espinajo_rastrojo", 30)]}
        for profile, chance in encounters.DENSITY.items():
            with self.subTest(profile=profile):
                encounters.validate_pools({"p": {**plain, "chance": chance}})
        for chance in (0.05, 0.5):
            with self.subTest(chance=chance), self.assertRaises(encounters.InvalidPoolConfig):
                encounters.validate_pools({"p": {**plain, "chance": chance}})
        encounters.validate_pools({"p": {**plain, "chance": 0.5, "gameplay_override": True}})


class MoveIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self.post("/register", dict(username="matias", name="Matías", password="una clave de prueba"))
        store.set_status(self.path, "matias", "approved")
        self.post("/species", dict(species="humano"))
        self.player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.path, self.player_id, "juramentado")
        self.post("/move", dict(direction="south"))  # salir del hogar al centro de Valdren

    def tearDown(self):
        self.temp.cleanup()

    def post(self, route, data=None):
        page = self.client.get("/").get_data(as_text=True)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
        return self.client.post(route, data={**(data or {}), "csrf": csrf})

    def encounter(self, room_id):
        return store.get_encounter(self.path, self.player_id, room_id)

    def test_entering_eligible_room_starts_random_encounter(self):
        with patch.object(encounters, "_rng", AlwaysRoll(0.0, pick=1)):
            self.post("/move", dict(direction="north"))
        self.assertEqual(self.client.get("/api/me").json["player"]["room"], "valdren_sendero")
        self.assertEqual(self.encounter("valdren_sendero")["creature_id"], "espinajo_rastrojo")
        self.assertIn("Espinajo de rastrojo", self.client.get("/").get_data(as_text=True))

    def test_failed_roll_leaves_room_empty(self):
        with patch.object(encounters, "_rng", AlwaysRoll(0.10)):
            self.post("/move", dict(direction="north"))
        self.assertIsNone(self.encounter("valdren_sendero"))

    def test_no_pools_means_behavior_unchanged(self):
        with patch.object(encounters, "RANDOM_ENCOUNTER_POOLS", {}):
            self.post("/move", dict(direction="north"))  # sendero
        self.assertIsNone(self.encounter("valdren_sendero"))
        self.post("/move", dict(direction="north"))  # parcela: Mordelinde fija
        self.assertEqual(self.encounter("valdren_camino_parcela")["creature_id"], "mordelinde")

    def test_cooldown_blocks_random_respawn_without_rolling(self):
        store.start_creature_cooldown(self.path, self.player_id, "valdren_sendero", "mordelinde")

        class Boom:
            def random(self):
                raise AssertionError("no debe tirar el dado con enfriamiento activo")
        with patch.object(encounters, "RANDOM_ENCOUNTER_POOLS", ROAD_POOL), \
                patch.object(encounters, "_rng", Boom()):
            self.post("/move", dict(direction="north"))
        self.assertIsNone(self.encounter("valdren_sendero"))


if __name__ == "__main__":
    unittest.main()
