"""Pruebas de Issue #57 (VT-DEV): inventario y equipamiento mínimo v1
(GAMEPLAY.md §32), incluyendo la conexión de armadura/arma real a la
matemática de combate de §30 (armor_reduction, MultiplicadorCarga) y a
`_can_block` (Bloquear/desviar, dejado pendiente por el Issue #73).

`atacar`, `huir`, `esquivar`, `resistir`, `bloquear` y `available_actions`
ya tienen su propia cobertura en test_pilot_lindero_roto.py y
test_combat_actions.py; este archivo cubre lo que cambia con equipo real."""
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, items, store


class FixedRoll:
    """RNG de prueba: rng.uniform(a, b) siempre devuelve el mismo valor.
    Mismo patrón que test_combat_actions.py/test_pilot_lindero_roto.py."""
    def __init__(self, value):
        self.value = value

    def uniform(self, a, b):
        return self.value


# --- items.py: catálogo puro, sin Flask/DB ----------------------------------

class ItemsCatalogTests(unittest.TestCase):
    def test_find_key_by_name_ignores_case_and_accents(self):
        self.assertEqual(items.find_key_by_name("ESPADA DE JURAMENTO"), "espada_juramento")
        self.assertEqual(items.find_key_by_name("espada de juramento"), "espada_juramento")

    def test_find_key_by_name_returns_none_for_unknown_object(self):
        self.assertIsNone(items.find_key_by_name("excalibur"))

    def test_category_of_weapons_and_armors(self):
        self.assertEqual(items.category_of("espada_juramento"), "weapon")
        self.assertEqual(items.category_of("acolchado_camino"), "armor")
        self.assertIsNone(items.category_of("no_existe"))


# --- combat.py: fórmulas puras de armadura (30.1-30.3) ----------------------

class ArmorCombatMathTests(unittest.TestCase):
    def test_armor_load_multiplier_matches_gameplay_30_3_table(self):
        self.assertAlmostEqual(combat.armor_load_multiplier(0.10), 1.10)
        self.assertAlmostEqual(combat.armor_load_multiplier(0.20), 1.20)
        self.assertAlmostEqual(combat.armor_load_multiplier(0.35), 1.35)
        self.assertEqual(combat.armor_load_multiplier(0.0), 1.0)

    def test_apply_armor_reduction(self):
        self.assertAlmostEqual(combat.apply_armor_reduction(10.0, 0.30), 7.0)
        self.assertEqual(combat.apply_armor_reduction(10.0, 0.0), 10.0)

    def test_fatigue_gained_applies_armor_load_on_top_of_existing_multipliers(self):
        base = combat.fatigue_gained("ataque_basico", 10, "ninguna")
        with_armor = combat.fatigue_gained("ataque_basico", 10, "ninguna", armor_reduction=0.20)
        self.assertAlmostEqual(with_armor, base * 1.20)
        # Sin armadura, el comportamiento previo a Issue #57 no cambia.
        self.assertAlmostEqual(combat.fatigue_gained("ataque_basico", 10, "ninguna", armor_reduction=0.0), base)


# --- Integración end-to-end contra el servidor real -------------------------

class InventoryIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def choose_class_without_starter_weapon(self):
        """Clase elegida sin arma inicial (Issue #112): estas pruebas miden el
        perfil tecnico sin arma de GAMEPLAY.md 24.10 y equipan a mano lo que
        necesitan. El flujo real /class con arma inicial se prueba aparte."""
        player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.app.config["DATABASE"], player_id, "juramentado")

    def register_and_enter_world(self, username="matias", name="Matías"):
        self.post("/register", dict(username=username, name=name, password="una clave de prueba"))
        dm = self.app.test_client()
        with patch.dict("os.environ", {"VT_DM_PASSWORD": "dm-secret-value"}):
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))  # arranca en valdren_centro
        self.choose_class_without_starter_weapon()

    def enter_combat_with_mordelinde(self):
        self.post("/move", dict(direction="west"))  # sendero
        self.post("/move", dict(direction="west"))  # parcela: aparece Mordelinde

    def player_id(self):
        return self.client.get("/api/me").json["player"]["id"]

    def character(self):
        return self.client.get("/api/character").json

    def inventory(self):
        return self.client.get("/api/inventory").json

    def room(self):
        return self.client.get("/api/room").json["room"]

    # --- Esquema (Issue #57) ------------------------------------------------

    def test_schema_creates_inventory_table_and_equip_columns(self):
        self.register_and_enter_world()
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 8)
            db.execute("SELECT equipped_weapon_id, equipped_armor_id FROM players LIMIT 1")
            db.execute("SELECT id, player_id, item_key, category, forge_validated, acquired_at "
                       "FROM inventory_items")

    # --- 32.5: adquisición autoritativa -------------------------------------

    def test_grant_item_rejects_unknown_catalog_key(self):
        self.register_and_enter_world()
        with self.assertRaises(ValueError):
            store.grant_item(self.path, self.player_id(), "excalibur")

    # --- Aceptación #1-2: entrega autoritativa + verla en inventario -------

    def test_granted_item_appears_in_inventory_unequipped(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "acolchado_camino")
        data = self.inventory()
        self.assertEqual(len(data["items"]), 1)
        entry = data["items"][0]
        self.assertEqual(entry["item_key"], "acolchado_camino")
        self.assertEqual(entry["name"], "Acolchado de Camino")
        self.assertEqual(entry["category"], "armor")
        self.assertFalse(entry["equipped"])
        self.assertFalse(entry["forge_required"])
        self.assertIsNone(data["equipped"]["armor"])
        self.assertEqual(data["armor_reduction_total"], 0.0)

    # --- Aceptación #3: equipar fuera de combate ----------------------------

    def test_equip_armor_by_name_activates_it(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "acolchado_camino")
        page = self.post("/command", dict(text="equipar Acolchado de Camino")).get_data(as_text=True)
        self.assertIn("Equipas Acolchado de Camino", page)
        data = self.inventory()
        self.assertTrue(data["items"][0]["equipped"])
        self.assertEqual(data["equipped"]["armor"]["item_key"], "acolchado_camino")

    def test_equip_is_case_and_accent_insensitive(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "espada_juramento")
        page = self.post("/command", dict(text="equipar ESPADA DE JURAMENTO")).get_data(as_text=True)
        self.assertIn("Equipas Espada de juramento", page)

    def test_equipping_unowned_item_is_rejected(self):
        self.register_and_enter_world()
        page = self.post("/command", dict(text="equipar Espada de juramento")).get_data(as_text=True)
        self.assertIn("No posees ese objeto", page)
        self.assertIsNone(self.inventory()["equipped"]["weapon"])

    def test_equipping_unknown_object_name_is_honest(self):
        self.register_and_enter_world()
        page = self.post("/command", dict(text="equipar excalibur")).get_data(as_text=True)
        self.assertIn("No reconoces ese objeto", page)

    def test_equipping_a_new_weapon_replaces_the_previous_one_without_destroying_it(self):
        # 32.3: "reemplaza el objeto activo de la misma categoría; no
        # destruye ni consume el objeto reemplazado."
        self.register_and_enter_world()
        pid = self.player_id()
        store.grant_item(self.path, pid, "punal_camino")
        store.grant_item(self.path, pid, "arco_ruta")
        self.post("/command", dict(text="equipar Puñal de camino"))
        self.post("/command", dict(text="equipar Arco de ruta"))
        data = self.inventory()
        self.assertEqual(data["equipped"]["weapon"]["item_key"], "arco_ruta")
        keys = {row["item_key"] for row in data["items"]}
        self.assertEqual(keys, {"punal_camino", "arco_ruta"})
        punal = next(row for row in data["items"] if row["item_key"] == "punal_camino")
        self.assertFalse(punal["equipped"])

    # --- Aceptación #4: cambia armor_reduction y fatiga según §30 ----------

    def test_equipping_armor_changes_reported_reduction_and_carga(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "cota_cinco_rutas")  # 20%
        self.post("/command", dict(text="equipar Cota de las Cinco Rutas"))
        data = self.inventory()
        self.assertEqual(data["armor_reduction_total"], 0.20)
        self.assertAlmostEqual(data["carga_multiplier"], 1.20)

    @patch("server.combat.random.Random")
    def test_equipped_armor_increases_fatigue_cost_of_fleeing(self, mock_random):
        mock_random.return_value = FixedRoll(100)  # nunca acierta: solo interesa la fatiga.
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "cota_cinco_rutas")  # 20%
        self.post("/command", dict(text="equipar Cota de las Cinco Rutas"))
        self.enter_combat_with_mordelinde()
        self.post("/command", dict(text="huir"))
        # 24.3: huir = 8, Resistencia 10 -> ModFatiga 1.0; 30.3: x1.20 de carga.
        self.assertAlmostEqual(self.character()["fatigue"], round(8 * 1.20))

    @patch("server.combat.random.Random")
    def test_equipped_armor_reduces_damage_taken_in_combat(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # siempre acierta.
        self.register_and_enter_world()
        pid = self.player_id()
        store.grant_item(self.path, pid, "arnes_mayor_cinco_rutas", forge_validated=True)  # 35%
        self.post("/command", dict(text="equipar Arnés Mayor de las Cinco Rutas"))
        self.enter_combat_with_mordelinde()
        hp_before = self.character()["hp_current"]
        self.post("/command", dict(text="atacar"))
        hp_after = self.character()["hp_current"]
        # Mordelinde hace 5 de daño fijo; con 35% de reducción quedan 3.25 -> redondeado a 3.
        self.assertEqual(round(hp_before - hp_after), 3)

    @patch("server.combat.random.Random")
    def test_equipping_a_weapon_changes_the_players_attack_damage(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # siempre acierta.
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "arco_ruta")  # base_damage 9
        self.post("/command", dict(text="equipar Arco de ruta"))
        self.enter_combat_with_mordelinde()
        page = self.post("/command", dict(text="atacar")).get_data(as_text=True)
        # Atributos base (10) y CG 0: el daño bruto coincide con base_damage.
        self.assertIn("Golpeas a Mordelinde por 9 de daño", page)

    # --- Aceptación #5: impedir equipar/desequipar durante combate ---------

    def test_cannot_equip_during_combat(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "acolchado_camino")
        self.enter_combat_with_mordelinde()
        page = self.post("/command", dict(text="equipar Acolchado de Camino")).get_data(as_text=True)
        self.assertIn("No puedes equipar nada con una criatura cerca", page)
        self.assertIsNone(self.inventory()["equipped"]["armor"])

    def test_cannot_unequip_during_combat(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "acolchado_camino")
        self.post("/command", dict(text="equipar Acolchado de Camino"))
        self.enter_combat_with_mordelinde()
        page = self.post("/command", dict(text="desequipar Acolchado de Camino")).get_data(as_text=True)
        self.assertIn("No puedes desequipar nada con una criatura cerca", page)
        self.assertIsNotNone(self.inventory()["equipped"]["armor"])

    # --- Aceptación #6: desequipar y volver a estadísticas base -------------

    def test_unequip_returns_to_base_reduction(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "cota_cinco_rutas")
        self.post("/command", dict(text="equipar Cota de las Cinco Rutas"))
        self.assertEqual(self.inventory()["armor_reduction_total"], 0.20)
        page = self.post("/command", dict(text="desequipar Cota de las Cinco Rutas")).get_data(as_text=True)
        self.assertIn("Guardas Cota de las Cinco Rutas", page)
        data = self.inventory()
        self.assertEqual(data["armor_reduction_total"], 0.0)
        self.assertIsNone(data["equipped"]["armor"])
        self.assertFalse(data["items"][0]["equipped"])

    def test_unequip_something_not_equipped_is_honest(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "acolchado_camino")  # posee, no equipa
        page = self.post("/command", dict(text="desequipar Acolchado de Camino")).get_data(as_text=True)
        self.assertIn("No tienes eso equipado", page)

    # --- Aceptación #7: persistir tras recarga/reinicio de sesión ----------

    def test_equipment_persists_across_login_sessions(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "espada_juramento")
        self.post("/command", dict(text="equipar Espada de juramento"))
        self.post("/logout")
        self.post("/login", dict(username="matias", password="una clave de prueba"))
        data = self.inventory()
        self.assertEqual(data["equipped"]["weapon"]["item_key"], "espada_juramento")

    # --- Aceptación #8: impedir equipar una pieza de Forja no validada -----

    def test_forge_required_armor_cannot_be_equipped_without_validation(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "arnes_korven", forge_validated=False)
        page = self.post("/command", dict(text="equipar Arnés de Korven")).get_data(as_text=True)
        self.assertIn("todavía no tiene su validación de Forja completa", page)
        self.assertIsNone(self.inventory()["equipped"]["armor"])

    def test_forge_validated_armor_can_be_equipped(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "arnes_korven", forge_validated=True)
        page = self.post("/command", dict(text="equipar Arnés de Korven")).get_data(as_text=True)
        self.assertIn("Equipas Arnés de Korven", page)

    def test_forge_required_weapon_cannot_be_equipped_without_validation(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "hoja_hoshai", forge_validated=False)
        page = self.post("/command", dict(text="equipar Hoja de Hoshai")).get_data(as_text=True)
        self.assertIn("todavía no tiene su validación de Forja completa", page)

    # --- Muerte conserva armadura/objetos (32.7) ----------------------------

    @patch("server.combat.random.Random")
    def test_equipped_items_survive_defeat_and_respawn(self, mock_random):
        mock_random.return_value = FixedRoll(0)  # el jugador y Mordelinde aciertan siempre.
        self.register_and_enter_world()
        pid = self.player_id()
        store.grant_item(self.path, pid, "espada_juramento")
        self.post("/command", dict(text="equipar Espada de juramento"))
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET hp_current = 1 WHERE id = ?", (pid,))
        self.enter_combat_with_mordelinde()
        page = self.post("/command", dict(text="atacar")).get_data(as_text=True)
        self.assertIn("te derrota", page)
        data = self.inventory()
        self.assertEqual(data["equipped"]["weapon"]["item_key"], "espada_juramento")

    # --- Bloquear depende del arma real equipada (conecta el Issue #73) ----

    def test_block_becomes_available_once_a_blocking_weapon_is_equipped(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "espada_juramento")  # can_block: Sí
        self.post("/command", dict(text="equipar Espada de juramento"))
        self.enter_combat_with_mordelinde()
        actions = {entry["action"] for entry in self.room()["available_actions"]}
        self.assertIn("bloquear", actions)

    def test_block_stays_unavailable_with_a_non_blocking_weapon_equipped(self):
        self.register_and_enter_world()
        store.grant_item(self.path, self.player_id(), "punal_camino")  # can_block: No
        self.post("/command", dict(text="equipar Puñal de camino"))
        self.enter_combat_with_mordelinde()
        actions = {entry["action"] for entry in self.room()["available_actions"]}
        self.assertNotIn("bloquear", actions)

    # --- CLI de operador: entrega administrativa (32.5) ---------------------

    def test_admin_grant_item_cli(self):
        self.register_and_enter_world()
        command = [sys.executable, "-m", "server.admin", "--data-dir", self.temp.name]
        result = subprocess.run(command + ["grant-item", "matias", "punal_camino"],
                                check=True, capture_output=True, text=True)
        self.assertIn("punal_camino", result.stdout)
        data = self.inventory()
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["item_key"], "punal_camino")

    def test_admin_grant_item_rejects_unknown_catalog_key(self):
        self.register_and_enter_world()
        command = [sys.executable, "-m", "server.admin", "--data-dir", self.temp.name]
        result = subprocess.run(command + ["grant-item", "matias", "excalibur"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def test_admin_grant_item_rejects_unknown_player(self):
        self.register_and_enter_world()
        command = [sys.executable, "-m", "server.admin", "--data-dir", self.temp.name]
        result = subprocess.run(command + ["grant-item", "nadie", "punal_camino"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
