"""Regression de la expansion del recorrido inicial de Valdren."""

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

    def test_expanded_route_is_bidirectional_and_reaches_zanja(self):
        chain = [
            "valdren_camino_lindero",
            "valdren_lindero_tres_piedras",
            "valdren_camino_hundido",
            "valdren_cobertizos_viejos",
            "valdren_cruce_cercas",
            "valdren_campo_rastrojo",
            "valdren_zanja_vieja",
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


if __name__ == "__main__":
    unittest.main()
