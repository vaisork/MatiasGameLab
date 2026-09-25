"""Motor de encuentros aleatorios (Issue #160): los encuentros fijos de El
lindero roto mandan, las salas elegibles tiran el dado de su pool, las no
elegibles nunca generan criatura y la configuración rota no pasa en silencio."""
import random
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import encounters, store, world

ROAD_POOL = {
    "prueba_camino": {
        "rooms": {"road_north", "valdren_camino_parcela"},
        "chance": 0.5,
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
    def test_production_config_is_valid_and_starts_empty(self):
        # Hasta que Jugabilidad/Historiador definan pools, el juego no cambia.
        encounters.validate_pools(encounters.RANDOM_ENCOUNTER_POOLS)
        self.assertEqual(encounters.RANDOM_ENCOUNTER_POOLS, {})

    def test_fixed_encounter_wins_over_random_pool(self):
        for value in (0.0, 0.99):
            rng = AlwaysRoll(value, pick=1)
            self.assertEqual(encounters.get_encounter_for_room("valdren_camino_parcela", rng, ROAD_POOL),
                             "mordelinde")
        self.assertEqual(encounters.get_encounter_for_room("valdren_camino_cerca", AlwaysRoll(0.0), ROAD_POOL),
                         "espinajo_rastrojo")

    def test_eligible_room_can_return_different_creatures(self):
        self.assertEqual(encounters.get_encounter_for_room("road_north", AlwaysRoll(0.1, 0), ROAD_POOL),
                         "mordelinde")
        self.assertEqual(encounters.get_encounter_for_room("road_north", AlwaysRoll(0.1, 1), ROAD_POOL),
                         "espinajo_rastrojo")
        # Por encima de chance no aparece nada.
        self.assertIsNone(encounters.get_encounter_for_room("road_north", AlwaysRoll(0.5), ROAD_POOL))
        seen = {encounters.get_encounter_for_room("road_north", random.Random(seed), ROAD_POOL)
                for seed in range(200)}
        self.assertEqual(seen, {None, "mordelinde", "espinajo_rastrojo"})

    def test_ineligible_room_never_spawns(self):
        for room_id in ("valdren_centro", "road_west", "valdren_camino_lindero"):
            for seed in range(50):
                self.assertIsNone(encounters.get_encounter_for_room(room_id, random.Random(seed), ROAD_POOL))

    def test_same_seed_gives_same_sequence(self):
        def run(seed):
            rng = random.Random(seed)
            return [encounters.get_encounter_for_room("road_north", rng, ROAD_POOL) for _ in range(30)]
        self.assertEqual(run(7), run(7))

    def test_weights_are_respected(self):
        rng = random.Random(1)
        pools = {"p": {**ROAD_POOL["prueba_camino"], "chance": 1}}
        results = [encounters.get_encounter_for_room("road_north", rng, pools) for _ in range(2000)]
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
            encounters.validate_pools({"a": base, "b": {**base, "rooms": {"road_north"}}})


class MoveIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self.post("/register", dict(username="matias", name="Matías", password="una clave de prueba"))
        store.set_status(self.path, "matias", "approved")
        self.post("/species", dict(species="humano"))  # valdren_centro
        self.player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.path, self.player_id, "juramentado")

    def tearDown(self):
        self.temp.cleanup()

    def post(self, route, data=None):
        page = self.client.get("/").get_data(as_text=True)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
        return self.client.post(route, data={**(data or {}), "csrf": csrf})

    def encounter(self, room_id):
        return store.get_encounter(self.path, self.player_id, room_id)

    def test_entering_eligible_room_starts_random_encounter(self):
        pools = {"p": {**ROAD_POOL["prueba_camino"], "chance": 1}}
        with patch.object(encounters, "RANDOM_ENCOUNTER_POOLS", pools), \
                patch.object(encounters, "_rng", AlwaysRoll(0.0, pick=1)):
            self.post("/move", dict(direction="south"))
        self.assertEqual(self.client.get("/api/me").json["player"]["room"], "road_north")
        self.assertEqual(self.encounter("road_north")["creature_id"], "espinajo_rastrojo")
        self.assertIn("Espinajo de rastrojo", self.client.get("/").get_data(as_text=True))

    def test_failed_roll_leaves_room_empty(self):
        with patch.object(encounters, "RANDOM_ENCOUNTER_POOLS", ROAD_POOL), \
                patch.object(encounters, "_rng", AlwaysRoll(0.9)):
            self.post("/move", dict(direction="south"))
        self.assertIsNone(self.encounter("road_north"))

    def test_no_pools_means_behavior_unchanged(self):
        self.post("/move", dict(direction="south"))
        self.assertIsNone(self.encounter("road_north"))
        self.post("/move", dict(direction="north"))
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela: Mordelinde fija
        self.assertEqual(self.encounter("valdren_camino_parcela")["creature_id"], "mordelinde")

    def test_cooldown_blocks_random_respawn_without_rolling(self):
        store.start_creature_cooldown(self.path, self.player_id, "road_north", "mordelinde")

        class Boom:
            def random(self):
                raise AssertionError("no debe tirar el dado con enfriamiento activo")
        with patch.object(encounters, "RANDOM_ENCOUNTER_POOLS", ROAD_POOL), \
                patch.object(encounters, "_rng", Boom()):
            self.post("/move", dict(direction="south"))
        self.assertIsNone(self.encounter("road_north"))


if __name__ == "__main__":
    unittest.main()
