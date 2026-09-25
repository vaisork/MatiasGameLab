"""Camino de los Campos, bloque 1 (A1-A10 de NARRATIVE_ROUTES.md): regresión
de la expansión del recorrido inicial de Valdren (PR #171 del Junior + A8-A10)."""

import unittest

from server import world


class ValdrenRouteExpansionTests(unittest.TestCase):
    def test_lindero_roto_keeps_scripted_microadventure_and_opens_route(self):
        self.assertEqual(
            world.ROOMS["valdren_camino_lindero"]["exits"],
            {"east": "valdren_camino_cerca", "west": "valdren_lindero_tres_piedras"},
        )
        self.assertEqual(world.ROOM_ENCOUNTER["valdren_camino_parcela"], "mordelinde")
        self.assertEqual(world.ROOM_ENCOUNTER["valdren_camino_cerca"], "espinajo_rastrojo")

    def test_expanded_route_is_bidirectional_and_reaches_vado(self):
        chain = [
            "valdren_camino_lindero",
            "valdren_lindero_tres_piedras",
            "valdren_camino_hundido",
            "valdren_cobertizos_viejos",
            "valdren_cruce_cercas",
            "valdren_campo_rastrojo",
            "valdren_zanja_vieja",
            "valdren_arbol_descanso",
            "valdren_campos_sin_cerca",
            "valdren_vado_menor",
        ]
        for current, following in zip(chain, chain[1:]):
            self.assertEqual(world.ROOMS[current]["exits"]["west"], following)
            self.assertEqual(world.ROOMS[following]["exits"]["east"], current)

    def test_new_rooms_do_not_add_scripted_encounters(self):
        new_rooms = {
            "valdren_lindero_tres_piedras",
            "valdren_camino_hundido",
            "valdren_cobertizos_viejos",
            "valdren_cruce_cercas",
            "valdren_campo_rastrojo",
            "valdren_zanja_vieja",
            "valdren_parcelas_exteriores",
            "valdren_arbol_descanso",
            "valdren_campos_sin_cerca",
            "valdren_vado_menor",
        }
        self.assertTrue(new_rooms.isdisjoint(world.ROOM_ENCOUNTER))
        for room_id in new_rooms:
            self.assertEqual(
                world.get_visual_context_id(room_id),
                "zone.edran.valdren_outskirts",
            )

    def test_world_map_still_covers_expanded_route_without_collisions(self):
        # map_layout caches globally, but this branch imports the complete world
        # before the first call in a normal test process.
        layout = world.map_layout()
        self.assertTrue({
            "valdren_lindero_tres_piedras",
            "valdren_zanja_vieja",
        }.issubset(layout))
        self.assertEqual(len(layout), len(set(layout.values())))

    def test_side_branch_at_cruce_de_las_cercas_returns_to_route(self):
        self.assertEqual(world.ROOMS["valdren_cruce_cercas"]["exits"]["north"], "valdren_parcelas_exteriores")
        self.assertEqual(world.ROOMS["valdren_parcelas_exteriores"]["exits"], {"south": "valdren_cruce_cercas"})

    def test_dynamic_habitat_rooms_exist_and_have_no_fixed_encounter(self):
        rooms = world.habitat_rooms("edran_campos")
        self.assertEqual(rooms, {"valdren_camino_hundido", "valdren_parcelas_exteriores",
                                 "valdren_campo_rastrojo", "valdren_campos_sin_cerca"})
        for room_id in rooms:
            self.assertIn(room_id, world.ROOMS)
            self.assertNotIn(room_id, world.ROOM_ENCOUNTER)

    def test_historical_traces_can_be_examined(self):
        self.assertIn("surco por surco", world.get_examine_text("valdren_lindero_tres_piedras", "piedras"))
        self.assertIn("épocas distintas", world.get_examine_text("valdren_zanja_vieja", "zanja"))

    def test_route_text_uses_proper_spanish_accents(self):
        # Texto para niños que están aprendiendo a leer: sin palabras sin acento.
        for room_id in ("valdren_lindero_tres_piedras", "valdren_arbol_descanso", "valdren_camino_parcela"):
            text = world.ROOMS[room_id]["description"]
            for bare in ("division", " mas ", "debiles", "Pequenos", "arbol"):
                self.assertNotIn(bare, text)


if __name__ == "__main__":
    unittest.main()
