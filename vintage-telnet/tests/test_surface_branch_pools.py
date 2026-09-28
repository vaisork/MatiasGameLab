"""Tests para los pools y descubrimientos de los 5 ramales superficiales:
- BM: Boca de la Montaña (#424)
- CQ: Canal Quieto (#423)
- CA: Cantera Abandonada (#422)
- GE: Grieta del Eco Seco (#419)
- MH: Molino Hundido (#341)
"""
import re
import tempfile
import unittest

from server import encounters, store, world
from server.app import create_app


class SurfaceBranchPoolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self):
        page = self.client.get("/").get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def register_and_approve(self, username="explorador"):
        self.client.post("/register", data=dict(username=username, name="Explorador", password="una clave de prueba", csrf=self.csrf()))
        store.set_status(self.path, username, "approved")
        self.client.post("/species", data=dict(species="humano", csrf=self.csrf()))
        self.client.post("/class", data=dict(player_class="sombra", csrf=self.csrf()))

    def test_all_surface_branch_pools_are_registered_and_valid(self):
        # 30 salas con encuentro aleatorio en los 5 ramales:
        # BM: 6 salas (02, 04, 05, 06, 07, 08)
        # CQ: 6 salas (02, 04, 05, 06, 07, 08)
        # CA: 6 salas (02, 03, 04, 06, 07, 08)
        # GE: 6 salas (02, 03, 04, 06, 07, 08)
        # MH: 6 salas (02, 03, 05, 06, 08, 09)
        branch_pools = [
            # BM
            "bm_02_raices_sobre_roca", "bm_04_ladera_grava", "bm_05_saliente_raices",
            "bm_06_terraza_exterior", "bm_07_risco_sombreado", "bm_08_antesala_boca",
            # CQ
            "cq_02_orilla_juncos_bajos", "cq_04_raices_ribera", "cq_05_recodo_tronco",
            "cq_06_paso_raices", "cq_07_orilla_blanda", "cq_08_recodo_sin_vista",
            # CA
            "ca_02_patio_grava", "ca_03_plataforma_baja", "ca_04_montones_descarte",
            "ca_06_plataforma_alta", "ca_07_frente_quebrado", "ca_08_paso_bloques",
            # GE
            "ge_02_terrazas_rotas", "ge_03_repisa_viento", "ge_04_quiebre_lajas",
            "ge_06_fisuras_paralelas", "ge_07_grava_fondo", "ge_08_ultima_luz_directa",
            # MH
            "mh_02_bordes_vencidos", "mh_03_juncos_partidos", "mh_05_terreno_dos_aguas",
            "mh_06_restos_cauce", "mh_08_rodeo_base", "mh_09_plataforma_caida",
        ]
        for pool_id in branch_pools:
            self.assertIn(pool_id, encounters.RANDOM_ENCOUNTER_POOLS)
            pool = encounters.RANDOM_ENCOUNTER_POOLS[pool_id]
            self.assertEqual(pool["rooms"], {pool_id})
            self.assertIn(pool["chance"], (0.10, 0.20, 0.30, 0.35))
            total_weight = sum(w for _, w in pool["creatures"])
            self.assertEqual(total_weight, 100, f"Pool {pool_id} pesos no suman 100")

    def test_zero_chance_rooms_have_no_pool(self):
        zero_rooms = [
            # BM 01, 03, 09
            "bm_01_desvio_dosel", "bm_03_piedra_sotobosque", "bm_09_boca_rocosa",
            # CQ 01, 03, 09
            "cq_01_desvio_agua_lenta", "cq_03_ensanchamiento_claro", "cq_09_estrechamiento_raices_roca",
            # CA 01, 05, 09
            "ca_01_desvio_descarte", "ca_05_zanja_seca", "ca_09_cavidad_tras_frente",
            # GE 01, 05, 09
            "ge_01_desvio_grieta", "ge_05_bolsillo_seco", "ge_09_boca_inferior",
            # MH 01, 04, 07, 10
            "mh_01_desvio_acequia", "mh_04_piedra_canal", "mh_07_vista_molino", "mh_10_umbral_inferior",
        ]
        for room_id in zero_rooms:
            self.assertIsNone(encounters.pool_for_room(room_id))
            self.assertIsNone(encounters.get_encounter_for_room(room_id))

    def test_bm_rules_and_creature_restrictions(self):
        # Hilaria solo BM-02 y BM-05 en Boca de la Montaña
        bm_rooms_with_hilaria = {
            r for r, p in encounters.RANDOM_ENCOUNTER_POOLS.items()
            if r.startswith("bm_") and any(c == "hilaria_niebla" for c, _ in p["creatures"])
        }
        self.assertEqual(bm_rooms_with_hilaria, {"bm_02_raices_sobre_roca", "bm_05_saliente_raices"})

        # Saltacresta solo BM-06 y BM-07
        bm_rooms_with_saltacresta = {
            r for r, p in encounters.RANDOM_ENCOUNTER_POOLS.items()
            if r.startswith("bm_") and any(c == "saltacresta" for c, _ in p["creatures"])
        }
        self.assertEqual(bm_rooms_with_saltacresta, {"bm_06_terraza_exterior", "bm_07_risco_sombreado"})

        # Rasgacorteza, Rasgacumbres, C4 nunca en BM
        bm_creatures = {
            c for r, p in encounters.RANDOM_ENCOUNTER_POOLS.items()
            if r.startswith("bm_") for c, _ in p["creatures"]
        }
        self.assertNotIn("rasgacorteza", bm_creatures)
        self.assertNotIn("rasgacumbres", bm_creatures)
        self.assertNotIn("cargallanura", bm_creatures)

    def test_cq_rules_and_creature_restrictions(self):
        # Hilaria solo CQ-06 en Canal Quieto
        cq_rooms_with_hilaria = {
            r for r, p in encounters.RANDOM_ENCOUNTER_POOLS.items()
            if r.startswith("cq_") and any(c == "hilaria_niebla" for c, _ in p["creatures"])
        }
        self.assertEqual(cq_rooms_with_hilaria, {"cq_06_paso_raices"})

        # Dorsalodo, Rasgacorteza, C4 nunca en CQ
        cq_creatures = {
            c for r, p in encounters.RANDOM_ENCOUNTER_POOLS.items()
            if r.startswith("cq_") for c, _ in p["creatures"]
        }
        self.assertNotIn("dorsalodo", cq_creatures)
        self.assertNotIn("rasgacorteza", cq_creatures)

    def test_ge_rules_and_creature_restrictions(self):
        # Saltacresta solo GE-02
        ge_rooms_with_saltacresta = {
            r for r, p in encounters.RANDOM_ENCOUNTER_POOLS.items()
            if r.startswith("ge_") and any(c == "saltacresta" for c, _ in p["creatures"])
        }
        self.assertEqual(ge_rooms_with_saltacresta, {"ge_02_terrazas_rotas"})

        # Rasgacumbres, Quebrarrocas nunca en GE
        ge_creatures = {
            c for r, p in encounters.RANDOM_ENCOUNTER_POOLS.items()
            if r.startswith("ge_") for c, _ in p["creatures"]
        }
        self.assertNotIn("rasgacumbres", ge_creatures)
        self.assertNotIn("quebrarrocas", ge_creatures)

    def test_mh_rules_and_creature_restrictions(self):
        # Dorsalodo, Cornalomo nunca en MH
        mh_creatures = {
            c for r, p in encounters.RANDOM_ENCOUNTER_POOLS.items()
            if r.startswith("mh_") for c, _ in p["creatures"]
        }
        self.assertNotIn("dorsalodo", mh_creatures)
        self.assertNotIn("cornalomo", mh_creatures)

    def test_threshold_discovery_persistence_and_idempotence(self):
        self.register_and_approve("viajero")
        player = self.client.get("/api/me").json["player"]
        player_id = player["id"]

        thresholds = [
            ("bm_09_boca_rocosa", "boca_montana_umbral_descubierto", "boca_montana_umbral"),
            ("cq_09_estrechamiento_raices_roca", "canal_quieto_umbral_descubierto", "canal_quieto_umbral"),
            ("ca_09_cavidad_tras_frente", "cantera_abandonada_umbral_descubierto", "cantera_abandonada_umbral"),
            ("ge_09_boca_inferior", "grieta_eco_seco_umbral_descubierto", "grieta_eco_seco_umbral"),
            ("mh_10_umbral_inferior", "molino_hundido_umbral_descubierto", "molino_hundido_umbral"),
        ]

        for room_id, flag, disc_key in thresholds:
            with self.subTest(threshold=room_id):
                self.assertFalse(store.get_story_flag(self.path, player_id, flag))
                self.assertFalse(store.has_discovery(self.path, player_id, disc_key))

                # Colocar al personaje en la sala previa y entrar al umbral
                # Mover al umbral via move_player directo para testear app.attempt_move
                prev_room = list(world.get_room(room_id)["exits"].values())[0]
                store.move_player(self.path, player_id, prev_room)

                # Buscar la dirección hacia el umbral
                direction = [d for d, target in world.get_room(prev_room)["exits"].items() if target == room_id][0]
                resp = self.client.post("/move", data=dict(direction=direction, csrf=self.csrf()))
                self.assertEqual(resp.status_code, 303)

                # Verificar flag y descubrimiento otorgados
                self.assertTrue(store.get_story_flag(self.path, player_id, flag))
                self.assertTrue(store.has_discovery(self.path, player_id, disc_key))

                # XP inicial de descubrimiento
                initial_xp = self.client.get("/api/character").json["xp"]
                self.assertGreater(initial_xp, 0)

                # Salir y volver a entrar: idempotente, no duplica XP
                exit_dir = [d for d, target in world.get_room(room_id)["exits"].items() if target == prev_room][0]
                self.client.post("/move", data=dict(direction=exit_dir, csrf=self.csrf()))
                self.client.post("/move", data=dict(direction=direction, csrf=self.csrf()))

                xp_after_revisit = self.client.get("/api/character").json["xp"]
                self.assertEqual(initial_xp, xp_after_revisit)


if __name__ == "__main__":
    unittest.main()
