"""Pruebas de topología autoritativa para los 5 ramales superficiales (#430).

Materialización de 46 salas hacia umbrales de futuras mazmorras:
- Molino Hundido (MH-01 a MH-10, 10 salas)
- Grieta del Eco Seco (GE-01 a GE-09, 9 salas)
- Cantera Abandonada (CA-01 a CA-09, 9 salas)
- Canal Quieto (CQ-01 a CQ-09, 9 salas)
- Boca de la Montaña (BM-01 a BM-09, 9 salas)
"""
import unittest

from server import world


class SurfaceBranchesTopologyTests(unittest.TestCase):
    def test_surface_branches_room_count(self):
        """Verifica que existen exactamente 46 salas con mapping unívoco."""
        self.assertEqual(len(world.SURFACE_BRANCH_MAPPING), 46)
        for code, room_id in world.SURFACE_BRANCH_MAPPING.items():
            with self.subTest(code=code, room_id=room_id):
                self.assertIn(room_id, world.ROOMS)
                self.assertEqual(world.get_surface_branch_room_id(code), room_id)
                self.assertEqual(world.get_surface_branch_code(room_id), code)

    def test_canonical_codes_distribution(self):
        """Comprueba que cada ramal tiene la cantidad exacta aprobada por Narrativa e Historia."""
        mh_codes = [c for c in world.SURFACE_BRANCH_MAPPING if c.startswith("MH-")]
        ge_codes = [c for c in world.SURFACE_BRANCH_MAPPING if c.startswith("GE-")]
        ca_codes = [c for c in world.SURFACE_BRANCH_MAPPING if c.startswith("CA-")]
        cq_codes = [c for c in world.SURFACE_BRANCH_MAPPING if c.startswith("CQ-")]
        bm_codes = [c for c in world.SURFACE_BRANCH_MAPPING if c.startswith("BM-")]

        self.assertEqual(len(mh_codes), 10, "Molino Hundido debe tener 10 salas (MH-01 a MH-10)")
        self.assertEqual(len(ge_codes), 9, "Grieta del Eco Seco debe tener 9 salas (GE-01 a GE-09)")
        self.assertEqual(len(ca_codes), 9, "Cantera Abandonada debe tener 9 salas (CA-01 a CA-09)")
        self.assertEqual(len(cq_codes), 9, "Canal Quieto debe tener 9 salas (CQ-01 a CQ-09)")
        self.assertEqual(len(bm_codes), 9, "Boca de la Montaña debe tener 9 salas (BM-01 a BM-09)")

    def test_five_anchors_resolved_and_bidirectional(self):
        """Comprueba que los 5 anclajes a las rutas o salas canónicas están conectados en ambos sentidos."""
        self.assertEqual(set(world.SURFACE_BRANCH_ANCHORS.keys()), {"MH", "GE", "CA", "CQ", "BM"})

        for branch_key, anchor_info in world.SURFACE_BRANCH_ANCHORS.items():
            anchor_room = anchor_info["anchor_room"]
            branch_entry = anchor_info["branch_entry"]
            dir_from_anchor = anchor_info["direction_from_anchor"]
            opposite_dir = world.OPPOSITE_DIRECTION[dir_from_anchor]

            with self.subTest(branch=branch_key):
                self.assertIn(anchor_room, world.ROOMS)
                self.assertIn(branch_entry, world.ROOMS)
                self.assertEqual(world.ROOMS[anchor_room]["exits"].get(dir_from_anchor), branch_entry)
                self.assertEqual(world.ROOMS[branch_entry]["exits"].get(opposite_dir), anchor_room)

    def test_terminal_thresholds_have_no_functional_interior(self):
        """Los 5 umbrales finales sólo permiten retornar: no tienen salida a interior funcional."""
        for threshold_id in world.SURFACE_BRANCH_THRESHOLDS:
            with self.subTest(threshold=threshold_id):
                room = world.ROOMS[threshold_id]
                self.assertEqual(len(room["exits"]), 1, f"{threshold_id} no debe tener más de 1 salida (solo retorno)")

    def test_full_bidirectional_traversal_molino_hundido(self):
        """Recorrido de ida y vuelta completo para Molino Hundido (MH-01 .. MH-10)."""
        chain = [world.SURFACE_BRANCH_MAPPING[f"MH-{i:02d}"] for i in range(1, 11)]
        # Salida desde anclaje hacia MH-01
        anchor = world.SURFACE_BRANCH_ANCHORS["MH"]["anchor_room"]
        self.assertEqual(world.ROOMS[anchor]["exits"]["south"], chain[0])
        self.assertEqual(world.ROOMS[chain[0]]["exits"]["north"], anchor)

        # De MH-01 a MH-10
        for current, nxt in zip(chain[:-1], chain[1:]):
            self.assertEqual(world.ROOMS[current]["exits"]["south"], nxt)
            self.assertEqual(world.ROOMS[nxt]["exits"]["north"], current)

    def test_full_bidirectional_traversal_grieta_eco_seco(self):
        """Recorrido de ida y vuelta completo para Grieta del Eco Seco (GE-01 .. GE-09)."""
        chain = [world.SURFACE_BRANCH_MAPPING[f"GE-{i:02d}"] for i in range(1, 10)]
        anchor = world.SURFACE_BRANCH_ANCHORS["GE"]["anchor_room"]
        self.assertEqual(world.ROOMS[anchor]["exits"]["west"], chain[0])
        self.assertEqual(world.ROOMS[chain[0]]["exits"]["east"], anchor)

        for current, nxt in zip(chain[:-1], chain[1:]):
            self.assertEqual(world.ROOMS[current]["exits"]["west"], nxt)
            self.assertEqual(world.ROOMS[nxt]["exits"]["east"], current)

    def test_full_bidirectional_traversal_cantera_abandonada(self):
        """Recorrido de ida y vuelta completo para Cantera Abandonada (CA-01 .. CA-09)."""
        chain = [world.SURFACE_BRANCH_MAPPING[f"CA-{i:02d}"] for i in range(1, 10)]
        anchor = world.SURFACE_BRANCH_ANCHORS["CA"]["anchor_room"]
        self.assertEqual(world.ROOMS[anchor]["exits"]["south"], chain[0])
        self.assertEqual(world.ROOMS[chain[0]]["exits"]["north"], anchor)

        for current, nxt in zip(chain[:-1], chain[1:]):
            self.assertEqual(world.ROOMS[current]["exits"]["south"], nxt)
            self.assertEqual(world.ROOMS[nxt]["exits"]["north"], current)

    def test_full_bidirectional_traversal_canal_quieto(self):
        """Recorrido de ida y vuelta completo para Canal Quieto (CQ-01 .. CQ-09)."""
        chain = [world.SURFACE_BRANCH_MAPPING[f"CQ-{i:02d}"] for i in range(1, 10)]
        anchor = world.SURFACE_BRANCH_ANCHORS["CQ"]["anchor_room"]
        self.assertEqual(world.ROOMS[anchor]["exits"]["east"], chain[0])
        self.assertEqual(world.ROOMS[chain[0]]["exits"]["west"], anchor)

        for current, nxt in zip(chain[:-1], chain[1:]):
            self.assertEqual(world.ROOMS[current]["exits"]["east"], nxt)
            self.assertEqual(world.ROOMS[nxt]["exits"]["west"], current)

    def test_full_bidirectional_traversal_boca_montana(self):
        """Recorrido de ida y vuelta completo para Boca de la Montaña (BM-01 .. BM-09)."""
        chain = [world.SURFACE_BRANCH_MAPPING[f"BM-{i:02d}"] for i in range(1, 10)]
        anchor = world.SURFACE_BRANCH_ANCHORS["BM"]["anchor_room"]
        self.assertEqual(world.ROOMS[anchor]["exits"]["north"], chain[0])
        self.assertEqual(world.ROOMS[chain[0]]["exits"]["south"], anchor)

        for current, nxt in zip(chain[:-1], chain[1:]):
            self.assertEqual(world.ROOMS[current]["exits"]["north"], nxt)
            self.assertEqual(world.ROOMS[nxt]["exits"]["south"], current)

    def test_approved_names_and_narrative_descriptions(self):
        """Verifica que los nombres y descripciones aprobados están completos y legibles."""
        expected_names = {
            "MH-01": "Desvío de la acequia",
            "MH-02": "Bordes vencidos",
            "MH-03": "Juncos partidos",
            "MH-04": "Piedra del canal",
            "MH-05": "Terreno de dos aguas",
            "MH-06": "Restos del cauce",
            "MH-07": "Vista del Molino",
            "MH-08": "Rodeo de la base",
            "MH-09": "Plataforma caída",
            "MH-10": "Umbral inferior",
            "GE-01": "Desvío de la grieta",
            "GE-02": "Terrazas rotas",
            "GE-03": "Repisa del viento",
            "GE-04": "Quiebre de las lajas",
            "GE-05": "Bolsillo seco",
            "GE-06": "Fisuras paralelas",
            "GE-07": "Grava de fondo",
            "GE-08": "Última luz directa",
            "GE-09": "Boca inferior",
            "CA-01": "Desvío de piedra descartada",
            "CA-02": "Patio de grava",
            "CA-03": "Plataforma baja",
            "CA-04": "Montones de descarte",
            "CA-05": "Zanja seca",
            "CA-06": "Plataforma alta",
            "CA-07": "Frente quebrado",
            "CA-08": "Paso entre bloques",
            "CA-09": "Cavidad tras el frente",
            "CQ-01": "Desvío de agua lenta",
            "CQ-02": "Orilla de juncos bajos",
            "CQ-03": "Ensanchamiento claro",
            "CQ-04": "Raíces de ribera",
            "CQ-05": "Recodo del tronco",
            "CQ-06": "Paso entre raíces",
            "CQ-07": "Orilla blanda",
            "CQ-08": "Recodo sin vista",
            "CQ-09": "Estrechamiento bajo raíces y roca",
            "BM-01": "Desvío bajo el dosel",
            "BM-02": "Raíces sobre roca",
            "BM-03": "Piedra del sotobosque",
            "BM-04": "Ladera de grava",
            "BM-05": "Saliente de raíces",
            "BM-06": "Terraza exterior",
            "BM-07": "Risco sombreado",
            "BM-08": "Antesala de la boca",
            "BM-09": "Boca rocosa",
        }

        for code, expected_name in expected_names.items():
            room_id = world.get_surface_branch_room_id(code)
            room = world.ROOMS[room_id]
            with self.subTest(code=code, room_id=room_id):
                self.assertEqual(room["name"], expected_name)
                self.assertTrue(len(room["description"]) > 30, "Descripción insuficiente")
                self.assertTrue(room["description"][0].isupper(), "Debe comenzar con mayúscula")
                self.assertTrue(room["description"].endswith("."), "Debe terminar con punto")

    def test_map_layout_and_describe_room_contract(self):
        """Garantiza que todas las salas están integradas en map_layout y describe_room ofrece fallback sobrio."""
        layout = world.map_layout()
        self.assertEqual(set(layout), set(world.ROOMS))

        for room_id in world.SURFACE_BRANCH_MAPPING.values():
            with self.subTest(room=room_id):
                desc = world.describe_room(room_id, others_present=[])
                self.assertIsNotNone(desc)
                self.assertEqual(desc["id"], room_id)
                self.assertIsNone(desc["art"], "Ramal superficial v1 sin asset aprobado debe dar art: None")
                self.assertTrue(len(desc["exits"]) >= 1)

    def test_no_unapproved_fixed_encounters(self):
        """Verifica que no se agregaron encuentros fijos no aprobados en los ramales."""
        for room_id in world.SURFACE_BRANCH_MAPPING.values():
            self.assertNotIn(room_id, world.ROOM_ENCOUNTER)


if __name__ == "__main__":
    unittest.main()
