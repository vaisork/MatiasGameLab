"""Pruebas exhaustivas para Clima Regional Compartido v1 (GAMEPLAY.md §37,
REGIONAL_WEATHER_CANON.md, Issue #138 / PR #293).
"""

import tempfile
import time
import unittest
from unittest.mock import patch

from server import weather, world, store
from server.app import create_app


class TestWeatherEpochAndDeterminism(unittest.TestCase):
    """GAMEPLAY §37.1 - §37.3: Fase climática global, cadencia de 2 horas reales
    y determinismo estricto como función pura del tiempo real."""

    def test_weather_epoch_cadence_two_hours(self):
        # 1 ciclo = 7200 segundos (2 horas)
        two_hours = 7200
        self.assertEqual(weather.weather_epoch(0), 0)
        self.assertEqual(weather.weather_epoch(two_hours - 1), 0)
        self.assertEqual(weather.weather_epoch(two_hours), 1)
        self.assertEqual(weather.weather_epoch(2 * two_hours - 1), 1)
        self.assertEqual(weather.weather_epoch(2 * two_hours), 2)
        self.assertEqual(weather.weather_epoch(10 * two_hours + 3500), 10)

    def test_pure_function_deterministic_restart_simulation(self):
        # Mismo timestamp siempre produce idéntico clima sin depender de SQLite o cron
        ts = 1774880000
        for region in weather.REGIONS:
            w1 = weather.get_region_weather(region, now=ts)
            w2 = weather.get_region_weather(region, now=ts)
            self.assertEqual(w1, w2)
            self.assertEqual(w1["label"], w2["label"])
            self.assertEqual(w1["icon"], w2["icon"])

    def test_offsets_are_stable_and_differentiated(self):
        # Cada región tiene un offset fijo
        self.assertEqual(len(weather.REGIONAL_OFFSETS), 6)
        for r in weather.REGIONS:
            self.assertIn(r, weather.REGIONAL_OFFSETS)
            self.assertIsInstance(weather.REGIONAL_OFFSETS[r], int)

        # En epoch 0, las regiones muestran estados diferenciados definidos por sus offsets
        e0_weathers = {r: weather.get_region_weather(r, now=0)["key"] for r in weather.REGIONS}
        # Al menos 4 estados climáticos distintos manifestándose simultáneamente en el mundo
        self.assertGreaterEqual(len(set(e0_weathers.values())), 4)


class TestRegionalCanonicalRestrictions(unittest.TestCase):
    """GAMEPLAY §37.4 y REGIONAL_WEATHER_CANON.md: Restricciones canónicas
    por región (Nieve exclusiva de Hoshai, Korven sin Niebla ni Nieve, etc.)."""

    def test_canonical_exclusion_rules_across_full_cycle(self):
        # El ciclo combinado de periodos 5, 6 y 7 es lcm(5, 6, 7) = 210 épocas
        full_cycle_epochs = 210
        two_hours = 7200

        observed_by_region = {r: set() for r in weather.REGIONS}

        for epoch in range(full_cycle_epochs):
            now = epoch * two_hours + 100
            for r in weather.REGIONS:
                w = weather.get_region_weather(r, now=now)
                key = w["key"]
                observed_by_region[r].add(key)
                # Garantizar que el clima observado pertenece estrictamente a los permitidos de esa región
                self.assertIn(
                    key,
                    weather.REGIONAL_ALLOWED_WEATHER[r],
                    f"Clima {key} no permitido en región {r}",
                )

        # 1. NIEVE: Solo Hoshai en v1
        self.assertIn("nieve", observed_by_region["hoshai"])
        self.assertNotIn("nieve", observed_by_region["veyra"])
        self.assertNotIn("nieve", observed_by_region["edran"])
        self.assertNotIn("nieve", observed_by_region["korven"])
        self.assertNotIn("nieve", observed_by_region["lethra"])
        self.assertNotIn("nieve", observed_by_region["nhal"])

        # 2. KORVEN: Sin Niebla ni Nieve
        self.assertNotIn("niebla", observed_by_region["korven"])
        self.assertNotIn("nieve", observed_by_region["korven"])

        # 3. LETHRA y NHAL: Niebla permitida, Nieve prohibida
        self.assertIn("niebla", observed_by_region["lethra"])
        self.assertIn("niebla", observed_by_region["nhal"])
        self.assertNotIn("nieve", observed_by_region["lethra"])
        self.assertNotIn("nieve", observed_by_region["nhal"])

        # 4. VEYRA y EDRAN: Sin Nieve
        self.assertNotIn("nieve", observed_by_region["veyra"])
        self.assertNotIn("nieve", observed_by_region["edran"])

    def test_all_weather_states_use_approved_ambient_icons(self):
        for state_key, state_data in weather.WEATHER_STATES.items():
            self.assertIn(
                state_data["icon"],
                world.AMBIENT_ICONS,
                f"Icono {state_data['icon']} para {state_key} no está en AMBIENT_ICONS",
            )
            self.assertIn(
                state_data["label"],
                ("Despejado", "Nublado", "Lluvia", "Niebla", "Nieve", "Tormenta", "Viento"),
            )


class TestRoomToRegionMapping(unittest.TestCase):
    """Mapeo geográfico de salas a regiones canónicas."""

    def test_all_world_rooms_map_to_valid_canonical_region(self):
        self.assertGreaterEqual(len(world.ROOMS), 112)
        for room_id in world.ROOMS:
            region = world.get_room_region(room_id)
            self.assertIn(
                region,
                weather.REGIONS,
                f"Sala {room_id} mapeada a región no canónica: {region}",
            )

    def test_hub_and_town_centers_mapping(self):
        self.assertEqual(world.get_room_region("vaisgard"), "veyra")
        self.assertEqual(world.get_room_region("cuenca_aproximacion_sur"), "veyra")
        self.assertEqual(world.get_room_region("valdren_centro"), "edran")
        self.assertEqual(world.get_room_region("khariel_centro"), "hoshai")
        self.assertEqual(world.get_room_region("brumak_centro"), "korven")
        self.assertEqual(world.get_room_region("narevia_centro"), "lethra")
        self.assertEqual(world.get_room_region("velmora_centro"), "nhal")

    def test_approach_and_transition_rooms_to_veyra(self):
        # Las salas de aproximación final a la Cuenca de Veyra pertenecen a veyra
        veyra_approaches = (
            "campos_colinas", "campos_almacen", "campos_vista_vaisgard",
            "campos_camino_exterior", "campos_acceso",
            "alto_cuenca_norte", "alto_vista_vaisgard", "alto_aproximacion",
            "piedra_entrada_veyra", "piedra_vista_vaisgard", "piedra_aproximacion",
            "juncos_entrada_veyra", "juncos_vista_vaisgard", "juncos_aproximacion",
            "sombra_entrada_veyra", "sombra_cruce_viajeros", "sombra_vista_vaisgard",
            "sombra_aproximacion",
        )
        for room_id in veyra_approaches:
            self.assertEqual(world.get_room_region(room_id), "veyra", f"{room_id} debe ser veyra")

    def test_explicit_room_region_attribute_takes_precedence(self):
        with patch.dict(world.ROOMS, {"test_custom_room": {"name": "Test", "region": "hoshai", "exits": {}}}):
            self.assertEqual(world.get_room_region("test_custom_room"), "hoshai")

    def test_unknown_room_falls_back_to_veyra(self):
        self.assertEqual(world.get_room_region("sala_inexistente_xyz"), "veyra")
        self.assertEqual(world.get_room_region(None), "veyra")


class TestImmediateRecalculationOnRegionChange(unittest.TestCase):
    """GAMEPLAY §37.5: Al entrar a otra región, la interfaz recalcula inmediatamente
    la manifestación climática con la misma epoch global y la lista de la nueva región."""

    def test_moving_between_regions_updates_weather_immediately(self):
        # A un instante fijo now=0
        fixed_now = 0  # epoch 0
        w_edran = weather.get_weather_for_room("valdren_centro", now=fixed_now)
        w_veyra = weather.get_weather_for_room("vaisgard", now=fixed_now)

        # En epoch 0:
        # veyra (offset 0) -> allowed[0] = Despejado
        # edran (offset 1) -> allowed[1] = Nublado
        self.assertEqual(w_veyra["key"], "despejado")
        self.assertEqual(w_edran["key"], "nublado")
        self.assertNotEqual(w_edran["key"], w_veyra["key"])

        # En el borde de Hoshai / Veyra:
        # alto_piedra_cinco_marcas (Hoshai) -> alto_cuenca_norte (Veyra)
        w_hoshai = weather.get_weather_for_room("alto_piedra_cinco_marcas", now=fixed_now)
        w_cuenca = weather.get_weather_for_room("alto_cuenca_norte", now=fixed_now)
        self.assertEqual(w_hoshai["key"], "lluvia")       # Hoshai offset 2 -> index 2: lluvia
        self.assertEqual(w_cuenca["key"], "despejado")    # Veyra offset 0 -> index 0: despejado


class TestGameplayIndependence(unittest.TestCase):
    """GAMEPLAY §37: El clima es ambiental/presentacional y no altera reglas mecánicas."""

    def test_weather_does_not_modify_combat_parameters(self):
        # Las funciones de clima son puras y desacopladas de combat y store
        for reg in weather.REGIONS:
            w = weather.get_region_weather(reg, now=123456)
            self.assertIn("label", w)
            self.assertIn("icon", w)
            self.assertIn("key", w)
            # Cero campos de combate o atributos en el contrato de clima
            self.assertNotIn("damage_modifier", w)
            self.assertNotIn("defense_modifier", w)
            self.assertNotIn("perception_modifier", w)
            self.assertNotIn("speed_modifier", w)


class TestWebAndApiPresentation(unittest.TestCase):
    """Presentación de clima y hora del día en API y HTML."""

    def setUp(self):
        import re
        self._re = re
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config = dict(
            TESTING=True,
            SECRET_KEY="test-secret-" * 5,
            DATA_DIR=self.temp_dir.name,
            SESSION_COOKIE_SECURE=False,
        )
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp_dir.cleanup()

    def post(self, route, data=None):
        page = self.client.get("/").get_data(as_text=True)
        csrf = self._re.search(r'name="csrf" value="([^"]+)"', page)[1]
        return self.client.post(route, data={**(data or {}), "csrf": csrf})

    def _register_and_enter(self, username="viajero_clima"):
        self.post("/register", dict(username=username, name="Viajero", password="una clave de prueba"))
        store.set_status(self.path, username, "approved")
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class="sombra"))

    def test_api_room_exposes_both_time_of_day_and_weather(self):
        self._register_and_enter()
        res = self.client.get("/api/room")
        self.assertEqual(res.status_code, 200)
        data = res.json["room"]
        ambient = data["ambient"]
        self.assertIsNotNone(ambient)
        self.assertIn("time_of_day", ambient)
        self.assertIn("weather", ambient)
        self.assertIn(ambient["time_of_day"]["label"], ("Amanecer", "Día", "Atardecer", "Noche"))
        self.assertIn(ambient["weather"]["label"], ("Despejado", "Nublado", "Lluvia", "Niebla", "Tormenta", "Viento"))
        self.assertIn(ambient["weather"]["icon"], world.AMBIENT_ICONS)

    def test_html_renders_weather_chip_with_svg_icon(self):
        self._register_and_enter()
        # 1. Comprobar renderizado en vivo real con el ambient autoritativo de la sala
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn('class="ambient-chip"', html)

        live_ambient = world.get_ambient("valdren_centro")
        self.assertIn(live_ambient["time_of_day"]["label"], html)
        self.assertIn(live_ambient["weather"]["label"], html)
        self.assertIn(f'href="#icon-amb-{live_ambient["time_of_day"]["icon"]}"', html)
        self.assertIn(f'href="#icon-amb-{live_ambient["weather"]["icon"]}"', html)

        # 2. Comprobar renderizado determinista simulado con patch.object(world, "get_ambient")
        mocked_ambient = {
            "time_of_day": {"label": "Amanecer", "icon": "amanecer"},
            "weather": {"label": "Nublado", "icon": "nube", "key": "nublado"},
        }
        with patch.object(world, "get_ambient", return_value=mocked_ambient):
            res_mocked = self.client.get("/")
            self.assertEqual(res_mocked.status_code, 200)
            html_mocked = res_mocked.get_data(as_text=True)
            self.assertIn('href="#icon-amb-amanecer"', html_mocked)
            self.assertIn("Amanecer", html_mocked)
            self.assertIn('href="#icon-amb-nube"', html_mocked)
            self.assertIn("Nublado", html_mocked)


if __name__ == "__main__":
    unittest.main()
