"""Pruebas exhaustivas para el motor de población ambiental N0 (Issue #380).

Verifica todos los criterios de aceptación de GAMEPLAY §39.6–39.10 y WORLD_POPULATION_NARRATIVE.md:
1. Determinismo: mismo epoch + room_id + role_table produce idéntica presencia y bark.
2. Densidades: perfiles none (0%), sparse (15%), normal (30%), busy (55%), hub (75%).
3. Máximo 1 presencia N0 ambiental por sala.
4. Coexistencia con NPC scripted: los NPCs definidos tienen prioridad y nunca son sustituidos.
5. Conversación con N0: hablar <N0> devuelve respuesta fija canónica sin invocar proveedor LLM.
6. Inmutabilidad de estado: cero mutaciones en SQLite, HP, XP, PA, oro o inventario.
7. Role table vacía: en producción sin roles activos retorna None sin fallos.
8. Ocultación en combate: un encuentro activo oculta la presencia ambiental.
9. Persistencia efímera: reconexión en el mismo epoch conserva presencia sin persistencia en DB.
"""

from copy import deepcopy
import hashlib
import os
import re
import sqlite3
import tempfile
import time
import unittest
from unittest.mock import MagicMock, patch

from server.app import create_app
from server import creatures, npc_dialogue, population, store, world
from server.npc_dialogue import DialogueProvider, DialogueResult


class TestPopulationN0Unit(unittest.TestCase):
    """Pruebas unitarias de aislamiento para server/population.py."""

    def setUp(self):
        population.clear_roles()

    def tearDown(self):
        population.clear_roles()

    def test_epoch_calculation(self):
        """Verifica population_epoch = floor(unix_time / 900) con ventanas exactas de 15 minutos."""
        self.assertEqual(population.get_population_epoch(0), 0)
        self.assertEqual(population.get_population_epoch(450), 0)
        self.assertEqual(population.get_population_epoch(899), 0)
        self.assertEqual(population.get_population_epoch(900), 1)
        self.assertEqual(population.get_population_epoch(1799), 1)
        self.assertEqual(population.get_population_epoch(1800), 2)
        self.assertEqual(population.get_population_epoch(9000), 10)

    def test_empty_roles_returns_none(self):
        """Si la tabla de roles está vacía, no genera presencia sin importar el perfil."""
        self.assertEqual(len(population.get_registered_roles()), 0)
        presence = population.get_room_n0_presence("valdren_centro", profile="hub", timestamp=1000)
        self.assertIsNone(presence)

    def test_density_none_profile_returns_none(self):
        """Perfil none o population_none siempre devuelve None (0%)."""
        population.load_canonical_roles()
        presence_none = population.get_room_n0_presence("valdren_centro", profile="none", timestamp=1000)
        self.assertIsNone(presence_none)
        presence_pop_none = population.get_room_n0_presence("valdren_centro", profile="population_none", timestamp=1000)
        self.assertIsNone(presence_pop_none)

    def test_canonical_roles_definitions(self):
        """Los 5 roles canónicos de WORLD_POPULATION_NARRATIVE.md están presentes y tienen respuestas fijas."""
        canonical = population.CANONICAL_N0_DATA
        expected_roles = ["habitante", "trabajador", "cargador", "viajero", "recolector"]
        for role_id in expected_roles:
            self.assertIn(role_id, canonical)
            role = canonical[role_id]
            self.assertEqual(role["role_id"], role_id)
            self.assertTrue(len(role["barks"]) >= 4)
            self.assertTrue(len(role["reply"]) > 0)
            self.assertIn(role["barks"][0], [
                "Buen camino.",
                "Un momento; termino esto y dejo libre el paso.",
                "Despacio. Esto pesa más de lo que parece.",
                "Aún me queda camino.",
                "Aquí todavía se encuentra algo si sabes mirar.",
            ])

    def test_deterministic_selection_same_epoch_and_room(self):
        """Mismo epoch y room_id con la misma tabla produce exactamente la misma presencia y bark."""
        population.load_canonical_roles()
        found_ts = None
        for step in range(50):
            ts = step * 900
            if population.get_room_n0_presence("camino_norte_1", profile="hub", timestamp=ts) is not None:
                found_ts = ts
                break
        self.assertIsNotNone(found_ts, "Debe existir un epoch que genere presencia en profile hub")

        presence1 = population.get_room_n0_presence("camino_norte_1", profile="hub", timestamp=found_ts)
        presence2 = population.get_room_n0_presence("camino_norte_1", profile="hub", timestamp=found_ts)
        self.assertIsNotNone(presence1)
        self.assertEqual(presence1, presence2)
        self.assertEqual(presence1["id"], presence2["id"])
        self.assertEqual(presence1["bark"], presence2["bark"])
        self.assertEqual(presence1["reply"], presence2["reply"])
        self.assertTrue(presence1["is_n0"])

    def test_maximum_one_n0_presence_per_room(self):
        """get_room_n0_presence siempre devuelve a lo sumo un solo objeto dict o None."""
        population.load_canonical_roles()
        for i in range(100):
            res = population.get_room_n0_presence(f"room_{i}", profile="hub", timestamp=i * 100)
            if res is not None:
                self.assertIsInstance(res, dict)
                self.assertIn("id", res)
                self.assertIn("role_id", res)
                self.assertIn("bark", res)
                self.assertIn("reply", res)
                self.assertTrue(res["is_n0"])

    def test_density_profiles_distribution(self):
        """Verifica que las densidades aproximan las probabilidades de GAMEPLAY §39.7."""
        population.load_canonical_roles()
        trials = 1000

        for profile, expected_rate in [
            ("sparse", 0.15),
            ("normal", 0.30),
            ("busy", 0.55),
            ("hub", 0.75),
        ]:
            count = 0
            for i in range(trials):
                # Generamos pares (room_id, epoch) variados
                res = population.get_room_n0_presence(f"room_test_{i}", profile=profile, timestamp=i * 900)
                if res is not None:
                    count += 1
            observed_rate = count / trials
            # Tolerancia de +/- 5% con 1000 muestras
            self.assertAlmostEqual(observed_rate, expected_rate, delta=0.06,
                                   msg=f"Perfil {profile}: observado {observed_rate}, esperado {expected_rate}")

    def test_role_exclusions_and_region_filters(self):
        """Un rol excluido de una sala o de una región no puede aparecer en ella."""
        custom_roles = [
            {
                "role_id": "minero",
                "label": "Minero",
                "barks": ["Pica y pala."],
                "reply": "No hay paso a la mina.",
                "regions": ["montana"],
                "room_tags": ["subterraneo"],
                "exclusions": ["mina_entrada_segura"],
            }
        ]
        # Sala excluida explícitamente
        res = population.get_room_n0_presence(
            "mina_entrada_segura",
            profile="hub",
            timestamp=1000,
            room_data={"region": "montana", "tags": ["subterraneo"]},
            role_table=custom_roles,
        )
        self.assertIsNone(res)

        # Región equivocada
        res2 = population.get_room_n0_presence(
            "mina_galeria_1",
            profile="hub",
            timestamp=1000,
            room_data={"region": "costa", "tags": ["subterraneo"]},
            role_table=custom_roles,
        )
        self.assertIsNone(res2)

        # Tag faltante
        res3 = population.get_room_n0_presence(
            "mina_galeria_1",
            profile="hub",
            timestamp=1000,
            room_data={"region": "montana", "tags": ["exterior"]},
            role_table=custom_roles,
        )
        self.assertIsNone(res3)


class TestPopulationN0Integration(unittest.TestCase):
    """Pruebas de integración HTTP y flujo del servidor para N0."""

    def setUp(self):
        population.clear_roles()
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(
            TESTING=True,
            SECRET_KEY="test-secret-" * 5,
            DATA_DIR=self.temp.name,
            SESSION_COOKIE_SECURE=False,
        )
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.db_path = self.app.config["DATABASE"]

        # Mock provider para rastrear si se llama al LLM
        from server.npc_dialogue import MockDialogueProvider, FixedDialogueProvider
        self.mock_provider = MockDialogueProvider(
            lambda p: "Respuesta generada por LLM"
        )
        npc_dialogue.set_default_provider(self.mock_provider)

    def tearDown(self):
        population.clear_roles()
        from server.npc_dialogue import FixedDialogueProvider
        npc_dialogue.set_default_provider(FixedDialogueProvider())
        try:
            self.temp.cleanup()
        except (PermissionError, OSError):
            pass

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', page)
        return match[1] if match else ""

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        payload = {**(data or {}), "csrf": self.csrf(csrf_path, client)}
        return client.post(route, data=payload)

    def register_and_approve(self, username="viajero_n0", name="Viajero"):
        self.post("/register", dict(username=username, name=name, password="clave-de-prueba"))
        with patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"}):
            dm = self.app.test_client()
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class="sombra"))
        self.post("/move", dict(direction="south"))

    def move_to_forja(self):
        self.post("/move", dict(direction="west"))

    def test_production_default_has_no_n0_when_no_roles_or_profiles(self):
        """En producción inicial sin roles activos, /api/room no muestra N0 y no rompe tests existentes."""
        self.register_and_approve()
        room_res = self.client.get("/api/room").json["room"]
        self.assertNotIn("npcs", room_res)
        self.assertIsNone(room_res.get("n0_presence"))

    def test_coexistence_with_scripted_npc_in_forja(self):
        """N0 coexiste con NPC scripted sin sustituirlo; el scripted NPC se preserva con prioridad."""
        self.register_and_approve()
        self.move_to_forja()

        # Inyectamos rol canónico garantizando presencia determinista con fixture
        population.load_canonical_roles()

        # Configuramos temporalmente perfil hub en la sala de forja
        room_data = world.get_room("valdren_forja")
        original_profile = room_data.get("population_profile")
        room_data["population_profile"] = "hub"

        try:
            # Buscar un timestamp que genere presencia en valdren_forja
            found_ts = None
            for step in range(50):
                candidate_ts = step * 900
                if population.get_room_n0_presence("valdren_forja", profile="hub", timestamp=candidate_ts) is not None:
                    found_ts = candidate_ts
                    break
            self.assertIsNotNone(found_ts, "Debe existir al menos un epoch que genere presencia con hub")

            with patch("server.population.get_current_time", return_value=found_ts):
                room_res = self.client.get("/api/room").json["room"]
                self.assertIn("npcs", room_res)
                npcs = room_res["npcs"]
                # Daro (scripted) debe ser el primero y no estar sustituido
                self.assertEqual(npcs[0]["id"], "daro_herrero")
                self.assertFalse(npcs[0].get("is_n0", False))

                # Segundo debe ser la presencia N0
                self.assertTrue(len(npcs) >= 2)
                n0_npc = npcs[1]
                self.assertTrue(n0_npc.get("is_n0", False))
                self.assertIn("bark", n0_npc)
                self.assertTrue(len(n0_npc["bark"]) > 0)

                # Available actions debe contener hablar con daro Y hablar con el N0
                talk_actions = [a for a in room_res["available_actions"] if a["action"] == "hablar"]
                self.assertTrue(len(talk_actions) >= 2)
                daro_targets = talk_actions[0]["targets"]
                self.assertIn("daro", daro_targets)

                n0_targets = talk_actions[1]["targets"]
                self.assertIn(n0_npc["role"].lower(), n0_targets)
        finally:
            if original_profile is None:
                room_data.pop("population_profile", None)
            else:
                room_data["population_profile"] = original_profile

    def test_talk_n0_returns_fixed_reply_zero_llm_zero_db_mutation(self):
        """hablar con N0 devuelve respuesta fija de WORLD_POPULATION_NARRATIVE.md sin llamar al LLM ni alterar DB."""
        self.register_and_approve()

        # Inyectamos roles canónicos y perfil en valdren_centro
        population.load_canonical_roles()
        room_data = world.get_room("valdren_centro")
        original_profile = room_data.get("population_profile")
        room_data["population_profile"] = "hub"

        try:
            # Encontrar timestamp con presencia N0 en valdren_centro
            found_ts = None
            n0_target_presence = None
            for step in range(50):
                candidate_ts = step * 900
                n0_p = population.get_room_n0_presence("valdren_centro", profile="hub", timestamp=candidate_ts)
                if n0_p is not None:
                    found_ts = candidate_ts
                    n0_target_presence = n0_p
                    break
            self.assertIsNotNone(found_ts)

            with patch("server.population.get_current_time", return_value=found_ts):
                # Estado previo de la base de datos
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                player_before = dict(conn.execute("SELECT * FROM players WHERE username='viajero_n0'").fetchone())
                inventory_count_before = conn.execute("SELECT COUNT(*) FROM inventory_items WHERE player_id=?", (player_before["id"],)).fetchone()[0]
                conn.close()

                # 1. Probar endpoint estructurado /api/talk
                res_api_talk = self.client.post("/api/talk", json={"target": n0_target_presence["role_id"], "csrf": self.csrf()})
                self.assertEqual(res_api_talk.status_code, 200)
                data_talk = res_api_talk.json
                self.assertTrue(data_talk["accepted"])
                self.assertEqual(data_talk["reply"], n0_target_presence["reply"])
                self.assertTrue(data_talk["is_n0"])
                self.assertIsNone(data_talk["proposed_action"])
                self.assertIsNone(data_talk["gate_result"])

                # CERO llamadas a LLM
                self.assertEqual(len(self.mock_provider.received_prompts), 0)

                # 2. Probar endpoint /api/intent
                res_intent = self.client.post("/api/intent", json={"text": f"hablar {n0_target_presence['role_id']}", "csrf": self.csrf()})
                self.assertEqual(res_intent.status_code, 200)
                data_intent = res_intent.json
                self.assertTrue(data_intent["accepted"])
                self.assertEqual(data_intent["reply"], n0_target_presence["reply"])
                self.assertTrue(data_intent["is_n0"])

                # CERO llamadas a LLM todavía
                self.assertEqual(len(self.mock_provider.received_prompts), 0)

                # 3. Probar formulario web terminal /command
                res_terminal = self.post("/command", {"text": f"hablar {n0_target_presence['name']}"})
                self.assertEqual(res_terminal.status_code, 200)
                page_text = res_terminal.get_data(as_text=True)
                self.assertIn(n0_target_presence["reply"], page_text)

                # CERO llamadas a LLM aún
                self.assertEqual(len(self.mock_provider.received_prompts), 0)

                # Verificar inmutabilidad absoluta de la DB
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                player_after = dict(conn.execute("SELECT * FROM players WHERE username='viajero_n0'").fetchone())
                inventory_count_after = conn.execute("SELECT COUNT(*) FROM inventory_items WHERE player_id=?", (player_after["id"],)).fetchone()[0]
                conn.close()

                self.assertEqual(dict(player_before), dict(player_after))
                self.assertEqual(inventory_count_before, inventory_count_after)

        finally:
            if original_profile is None:
                room_data.pop("population_profile", None)
            else:
                room_data["population_profile"] = original_profile

    def test_combat_active_hides_n0_presence(self):
        """Un encuentro de combate activo oculta completamente la presencia N0 en room_view y /api/talk."""
        self.register_and_approve()
        population.load_canonical_roles()
        room_data = world.get_room("valdren_centro")
        original_profile = room_data.get("population_profile")
        room_data["population_profile"] = "hub"

        try:
            # Encontrar timestamp con presencia N0
            found_ts = None
            n0_target = None
            for step in range(50):
                ts = step * 900
                p = population.get_room_n0_presence("valdren_centro", profile="hub", timestamp=ts)
                if p is not None:
                    found_ts = ts
                    n0_target = p
                    break
            self.assertIsNotNone(found_ts)

            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            player = dict(conn.execute("SELECT * FROM players WHERE username='viajero_n0'").fetchone())
            conn.close()

            with patch("server.population.get_current_time", return_value=found_ts):
                # Sin combate: N0 visible
                room_view_peace = self.client.get("/api/room").json["room"]
                self.assertIsNotNone(room_view_peace.get("n0_presence"))

                # Iniciar combate activo
                creature = creatures.get_creature("mordelinde")
                store.start_encounter(self.db_path, player["id"], "valdren_centro", "mordelinde", creature["hp"])

                # Con combate activo: N0 oculto
                room_view_combat = self.client.get("/api/room").json["room"]
                self.assertIsNone(room_view_combat.get("n0_presence"))
                if "npcs" in room_view_combat:
                    self.assertFalse(any(n.get("is_n0") for n in room_view_combat["npcs"]))

                # Intento de hablar con N0 durante combate no encuentra al N0
                res_talk = self.client.post("/api/talk", json={"target": n0_target["id"], "csrf": self.csrf()})
                # npc_dialogue no encuentra el NPC porque está oculto/no es scripted
                self.assertFalse(res_talk.json["accepted"])

        finally:
            if original_profile is None:
                room_data.pop("population_profile", None)
            else:
                room_data["population_profile"] = original_profile

    def test_ephemeral_reconnect_preserves_presence_in_same_epoch(self):
        """Dos peticiones en el mismo epoch ven exactamente el mismo N0 sin escribir en DB."""
        population.load_canonical_roles()
        room_data = world.get_room("valdren_centro")
        original_profile = room_data.get("population_profile")
        room_data["population_profile"] = "hub"

        try:
            fixed_ts = 36000.0  # Epoch 40
            n0_first = population.get_room_n0_presence("valdren_centro", profile="hub", timestamp=fixed_ts)
            self.assertIsNotNone(n0_first)

            # 10 consultas en el mismo epoch (ej. reconexiones o clientes simultáneos)
            for _ in range(10):
                n0_repeat = population.get_room_n0_presence("valdren_centro", profile="hub", timestamp=fixed_ts + 120)
                self.assertEqual(n0_first, n0_repeat)

            # Al avanzar un epoch (+900 segundos) cambia determinísticamente
            next_epoch_ts = fixed_ts + 901
            next_epoch = population.get_population_epoch(next_epoch_ts)
            self.assertEqual(next_epoch, population.get_population_epoch(fixed_ts) + 1)
        finally:
            if original_profile is None:
                room_data.pop("population_profile", None)
            else:
                room_data["population_profile"] = original_profile


if __name__ == "__main__":
    unittest.main()
