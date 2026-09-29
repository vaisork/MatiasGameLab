"""Pruebas exhaustivas del núcleo económico v1 — ECONOMY-CORE-01 (#408 / ECONOMY.md).

Cubre:
1. Migración segura v14 -> v15 (columna sellos DEFAULT 20, tabla economy_ledger, seeding de starting_purse).
2. Saldo inicial de 20 sellos por personaje al crearse y registro en el ledger.
3. Catálogo autoritativo de compra de Daro en Valdren (Varita 40, Puñal 50, Arco 65, Espada 85).
4. Recompra autoritativa al 35% floor (Varita 14, Puñal 17, Arco 22, Espada 29).
5. Compra atómica: débito de sellos, creación de instancia única no autoequipada, registro en ledger.
6. Rechazo atómico de compra por fondos insuficientes o artículo fuera de catálogo.
7. Restricciones espaciales y de combate (solo fuera de combate y en valdren_forja).
8. Venta atómica: acreditación de sellos, eliminación de instancia, registro en ledger.
9. Protección de venta: bloqueo si está equipado o si es la última arma utilizable del personaje.
10. Exclusiones de venta: objetos de armadura, forja o armas regionales (Hoja de Hoshai, Martillo de Korven).
11. Concurrencia y protección contra doble gasto.
12. Invarianza ante muerte y respawn seguro (sellos y ledger preservados).
13. Endpoints REST (/api/shop/daro, /api/shop/daro/buy, /api/shop/daro/sell, /api/economy/ledger) y /api/intent.
14. Invariante de seguridad: cliente nunca propone el precio.
"""
import concurrent.futures
import math
import os
from pathlib import Path
import re
import tempfile
import time
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, economy, items, store


class EconomyCoreCatalogAndMathTests(unittest.TestCase):
    """Pruebas unitarias puras del catálogo y matemáticas de reventa."""

    def test_canonical_starting_sellos_is_20(self):
        self.assertEqual(economy.STARTING_SELLOS, 20)

    def test_daro_catalog_prices_match_canon(self):
        expected = {
            "varita_aprendiz": 40,
            "punal_camino": 50,
            "arco_ruta": 65,
            "espada_juramento": 85,
        }
        self.assertEqual(economy.DARO_CATALOG, expected)

    def test_daro_buyback_is_exact_35_percent_floor(self):
        expected_buyback = {
            "varita_aprendiz": 14,  # floor(40 * 0.35) = 14
            "punal_camino": 17,     # floor(50 * 0.35) = 17
            "arco_ruta": 22,        # floor(65 * 0.35) = 22
            "espada_juramento": 29, # floor(85 * 0.35) = 29
        }
        self.assertEqual(economy.DARO_BUYBACK, expected_buyback)
        for key, price in economy.DARO_CATALOG.items():
            self.assertEqual(economy.get_resale_price(key), int(math.floor(price * 0.35)))

    def test_resolve_daro_item_aliases(self):
        self.assertEqual(economy.resolve_daro_item("espada"), "espada_juramento")
        self.assertEqual(economy.resolve_daro_item("espada de juramento"), "espada_juramento")
        self.assertEqual(economy.resolve_daro_item("varita"), "varita_aprendiz")
        self.assertEqual(economy.resolve_daro_item("puñal"), "punal_camino")
        self.assertEqual(economy.resolve_daro_item("punal"), "punal_camino")
        self.assertEqual(economy.resolve_daro_item("arco"), "arco_ruta")
        self.assertEqual(economy.resolve_daro_item("espada_juramento"), "espada_juramento")
        self.assertIsNone(economy.resolve_daro_item("hoja_hoshai"))
        self.assertIsNone(economy.resolve_daro_item("martillo_korven"))
        self.assertIsNone(economy.resolve_daro_item("pocion"))


class EconomyMigrationAndPersistenceTests(unittest.TestCase):
    """Pruebas de migración de esquema v14 a v18 y persistencia del ledger."""

    def test_migration_v14_to_current_adds_all_tables_and_preserves_player_data(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = str(Path(td) / "test.db")
            # 1. Crear base en v14 con un jugador existente
            store.initialize(db_path)
            with store.connect(db_path) as db:
                db.execute("ALTER TABLE players DROP COLUMN sellos")
                db.execute("DROP TABLE economy_ledger")
                # Insertar un jugador simulado en v14
                p_id = "test-player-v14"
                db.execute(
                    """INSERT INTO players (id, username, name, name_key, password_hash, status, created_at, last_access_at)
                       VALUES (?, 'v14user', 'V14 User', 'v14 user', 'hash', 'approved', '2026-09-28', '2026-09-28')""",
                    (p_id,),
                )
                db.execute("PRAGMA user_version = 14")

            # 2. Ejecutar initialize() debe aplicar v15-v17 desde un esquema legado.
            store.initialize(db_path)

            # 3. Validar tablas, columnas y datos preservados.
            with store.connect(db_path) as db:
                self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], store.SCHEMA_VERSION)
                encounter_cols = {row["name"] for row in db.execute("PRAGMA table_info(room_encounters)")}
                self.assertTrue({"engaged", "signature_cooldown", "apertura", "prepared_action"} <= encounter_cols)
                self.assertTrue(db.execute("SELECT 1 FROM player_story_flags LIMIT 1").fetchone() is None)
                self.assertIsNotNone(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player_threat_states'").fetchone())
                cols = {row["name"] for row in db.execute("PRAGMA table_info(players)").fetchall()}
                self.assertIn("sellos", cols)
                player_row = db.execute("SELECT sellos FROM players WHERE id = ?", (p_id,)).fetchone()
                self.assertEqual(player_row["sellos"], 20)

                ledger_rows = db.execute("SELECT * FROM economy_ledger WHERE player_id = ?", (p_id,)).fetchall()
                self.assertEqual(len(ledger_rows), 1)
                entry = dict(ledger_rows[0])
                self.assertEqual(entry["delta"], 20)
                self.assertEqual(entry["balance_after"], 20)
                self.assertEqual(entry["reason_code"], "starting_purse")
                self.assertEqual(entry["source_key"], "migration:v17")

    def test_new_character_receives_20_sellos_and_character_creation_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = str(Path(td) / "test.db")
            store.initialize(db_path)
            token = store.register(db_path, "newcomer", "Nuevo Viajero", "hashed_pwd")
            player = store.player_for_token(db_path, token)
            self.assertIsNotNone(player)
            self.assertEqual(player["sellos"], 20)

            ledger = economy.list_player_ledger(db_path, player["id"])
            self.assertEqual(len(ledger), 1)
            self.assertEqual(ledger[0]["delta"], 20)
            self.assertEqual(ledger[0]["balance_after"], 20)
            self.assertEqual(ledger[0]["reason_code"], "starting_purse")
            self.assertEqual(ledger[0]["source_key"], "character_creation")


class EconomyAppIntegrationTests(unittest.TestCase):
    """Pruebas integradas de endpoints Flask, compra, venta y casos límite."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = {
            "TESTING": True,
            "SECRET_KEY": "test-economy-secret-key-" * 4,
            "DATA_DIR": self.temp.name,
            "SESSION_COOKIE_SECURE": False,
        }
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self._register_and_setup()

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', page)
        return match[1] if match else ""

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def post_json(self, route, data=None, client=None):
        client = client or self.client
        payload = dict(data or {})
        if "csrf" not in payload:
            payload["csrf"] = self.csrf(client=client)
        return client.post(route, json=payload)

    def _register_and_setup(self):
        self.post("/register", dict(username="artesano", name="El Artesano", password="password123"))
        dm = self.app.test_client()
        with patch.dict("os.environ", {"VT_DM_PASSWORD": "dm-secret-value"}):
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username="artesano"), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        self.player_id = self.client.get("/api/me").json["player"]["id"]
        # Inicia como Juramentado (recibe espada_juramento inicial)
        store.set_player_class(self.path, self.player_id, "juramentado", "espada_juramento")
        # Mover a valdren_forja
        store.move_player(self.path, self.player_id, "valdren_forja")

    def set_sellos(self, amount):
        with store.connect(self.path) as db:
            db.execute("UPDATE players SET sellos = ? WHERE id = ?", (amount, self.player_id))

    def get_sellos(self):
        return economy.get_player_balance(self.path, self.player_id)

    # --- Pruebas de Compra ---

    def test_buy_item_with_sufficient_funds_succeeds(self):
        self.set_sellos(50)
        resp = self.post_json("/api/shop/daro/buy", {"item_key": "punal_camino"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["accepted"])
        self.assertEqual(resp.json["sellos"], 0)
        self.assertEqual(self.get_sellos(), 0)

        # Verificar inventario tiene el nuevo puñal
        inv = self.client.get("/api/inventory").json["items"]
        weapons = [it for it in inv if it["item_key"] == "punal_camino"]
        self.assertEqual(len(weapons), 1)
        self.assertFalse(weapons[0]["equipped"])

        # Verificar ledger
        ledger = economy.list_player_ledger(self.path, self.player_id)
        self.assertEqual(ledger[0]["delta"], -50)
        self.assertEqual(ledger[0]["balance_after"], 0)
        self.assertEqual(ledger[0]["reason_code"], "shop_purchase")

    def test_buy_item_insufficient_funds_rejected_atomically(self):
        self.set_sellos(20)
        resp = self.post_json("/api/shop/daro/buy", {"item_key": "varita_aprendiz"})
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.json["accepted"])
        self.assertEqual(self.get_sellos(), 20)

        inv = self.client.get("/api/inventory").json["items"]
        self.assertEqual(len([it for it in inv if it["item_key"] == "varita_aprendiz"]), 0)

    def test_repeat_purchases_deliver_separate_instances_without_autoequip(self):
        self.set_sellos(100)
        # Comprar dos puñales (50 cada uno)
        resp1 = self.post_json("/api/shop/daro/buy", {"item_key": "punal_camino"})
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.post_json("/api/shop/daro/buy", {"item_key": "punal_camino"})
        self.assertEqual(resp2.status_code, 200)

        self.assertEqual(self.get_sellos(), 0)
        inv = self.client.get("/api/inventory").json["items"]
        daggers = [it for it in inv if it["item_key"] == "punal_camino"]
        self.assertEqual(len(daggers), 2)
        self.assertNotEqual(daggers[0]["id"], daggers[1]["id"])
        self.assertFalse(daggers[0]["equipped"])
        self.assertFalse(daggers[1]["equipped"])

    def test_cannot_buy_outside_daro_shop(self):
        self.set_sellos(100)
        store.move_player(self.path, self.player_id, "valdren_centro")
        resp = self.post_json("/api/shop/daro/buy", {"item_key": "punal_camino"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json["outcome"], "blocked")
        self.assertEqual(self.get_sellos(), 100)

    def test_cannot_buy_while_in_combat(self):
        self.set_sellos(100)
        # Simular encuentro en valdren_forja
        with store.connect(self.path) as db:
            db.execute(
                """INSERT INTO room_encounters (player_id, room_id, creature_id, hp_current, engaged, created_at)
                   VALUES (?, 'valdren_forja', 'mordelinde', 10, 1, '2026-09-28')""",
                (self.player_id,),
            )
        resp = self.post_json("/api/shop/daro/buy", {"item_key": "punal_camino"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json["outcome"], "blocked")
        self.assertEqual(self.get_sellos(), 100)

    # --- Pruebas de Venta ---

    def test_sell_item_success_atomically_credits_resale_price(self):
        # El jugador empieza con 1 espada equipada. Compramos un puñal (50 sellos)
        self.set_sellos(50)
        self.post_json("/api/shop/daro/buy", {"item_key": "punal_camino"})
        self.assertEqual(self.get_sellos(), 0)

        # Ahora tiene 2 armas: espada (equipada) y puñal (no equipado)
        inv = self.client.get("/api/inventory").json["items"]
        dagger = next(it for it in inv if it["item_key"] == "punal_camino")

        # Vender el puñal por su ID
        resp = self.post_json("/api/shop/daro/sell", {"item_id": dagger["id"]})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["accepted"])
        # Recompra del puñal: 17 sellos
        self.assertEqual(resp.json["sellos"], 17)
        self.assertEqual(self.get_sellos(), 17)

        # Verificar que el puñal fue eliminado del inventario
        inv_after = self.client.get("/api/inventory").json["items"]
        self.assertEqual(len([it for it in inv_after if it["id"] == dagger["id"]]), 0)

        # Verificar ledger
        ledger = economy.list_player_ledger(self.path, self.player_id)
        self.assertEqual(ledger[0]["delta"], 17)
        self.assertEqual(ledger[0]["balance_after"], 17)
        self.assertEqual(ledger[0]["reason_code"], "shop_sale")

    def test_cannot_sell_equipped_item(self):
        # Comprar un puñal adicional para no violar la regla de última arma
        self.set_sellos(50)
        self.post_json("/api/shop/daro/buy", {"item_key": "punal_camino"})

        # La espada de juramento inicial está equipada
        inv = self.client.get("/api/inventory").json["items"]
        sword = next(it for it in inv if it["item_key"] == "espada_juramento")
        self.assertTrue(sword["equipped"])

        resp = self.post_json("/api/shop/daro/sell", {"item_id": sword["id"]})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("equipado", resp.json["messages"][0])

    def test_cannot_sell_last_usable_weapon(self):
        # El jugador solo tiene 1 arma (espada_juramento). La desequipamos:
        self.post_json("/api/intent", {"text": "desequipar espada de juramento"})
        inv = self.client.get("/api/inventory").json["items"]
        sword = next(it for it in inv if it["item_key"] == "espada_juramento")
        self.assertFalse(sword["equipped"])

        # Intentar vender su única arma
        resp = self.post_json("/api/shop/daro/sell", {"item_id": sword["id"]})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("última arma", resp.json["messages"][0])
        # Fondos no cambiaron
        self.assertEqual(self.get_sellos(), 20)

    def test_cannot_sell_non_catalog_or_regional_or_armor_items(self):
        # Añadir al inventario un Acolchado de Camino (armadura) y una Hoja de Hoshai
        with store.connect(self.path) as db:
            db.execute(
                """INSERT INTO inventory_items (id, player_id, item_key, category, forge_validated, acquired_at)
                   VALUES ('armor-1', ?, 'acolchado_camino', 'armor', 0, '2026-09-28'),
                          ('hoshai-1', ?, 'hoja_hoshai', 'weapon', 1, '2026-09-28')""",
                (self.player_id, self.player_id),
            )
        resp1 = self.post_json("/api/shop/daro/sell", {"item_id": "armor-1"})
        self.assertEqual(resp1.status_code, 400)
        self.assertIn("no compra", resp1.json["messages"][0])

        resp2 = self.post_json("/api/shop/daro/sell", {"item_id": "hoshai-1"})
        self.assertEqual(resp2.status_code, 400)
        self.assertIn("no compra", resp2.json["messages"][0])

    # --- Pruebas de Terminal / Command / Intent ---

    def test_terminal_command_comprar_and_vender(self):
        self.set_sellos(100)
        # Comprar mediante terminal
        resp_buy = self.post("/command", {"text": "comprar arco de ruta"})
        self.assertEqual(resp_buy.status_code, 200)
        # 100 - 65 = 35 sellos
        self.assertEqual(self.get_sellos(), 35)

        # Vender mediante terminal: "vender arco"
        resp_sell = self.post("/command", {"text": "vender arco"})
        self.assertEqual(resp_sell.status_code, 200)
        # Recompra del arco: 22 sellos -> 35 + 22 = 57 sellos
        self.assertEqual(self.get_sellos(), 57)

    def test_api_intent_comprar_and_vender(self):
        self.set_sellos(100)
        resp_intent = self.post_json("/api/intent", {"text": "comprar varita"})
        self.assertEqual(resp_intent.status_code, 200)
        self.assertTrue(resp_intent.json["accepted"])
        self.assertEqual(resp_intent.json["intent"], "buy")
        self.assertEqual(self.get_sellos(), 60)

        resp_intent_sell = self.post_json("/api/intent", {"text": "vender varita"})
        self.assertEqual(resp_intent_sell.status_code, 200)
        self.assertTrue(resp_intent_sell.json["accepted"])
        self.assertEqual(resp_intent_sell.json["intent"], "sell")
        # 60 + 14 = 74 sellos
        self.assertEqual(self.get_sellos(), 74)

    def test_client_cannot_tamper_with_prices(self):
        self.set_sellos(50)
        # Intentar enviar un precio propuesto fraudulento por el cliente
        resp = self.post_json("/api/shop/daro/buy", {"item_key": "punal_camino", "price": 1})
        self.assertEqual(resp.status_code, 200)
        # Debe debitar los 50 autoritativos, no 1
        self.assertEqual(self.get_sellos(), 0)

    # --- Pruebas de Endpoints Estructurados ---

    def test_api_shop_daro_endpoint(self):
        resp = self.client.get("/api/shop/daro")
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertEqual(data["shop_name"], "Taller de Daro")
        self.assertEqual(data["room"], "valdren_forja")
        self.assertTrue(data["in_shop"])
        self.assertEqual(data["sellos"], 20)
        catalog = {entry["item_key"]: entry["price"] for entry in data["catalog"]}
        self.assertEqual(catalog["varita_aprendiz"], 40)
        self.assertEqual(catalog["punal_camino"], 50)
        self.assertEqual(catalog["arco_ruta"], 65)
        self.assertEqual(catalog["espada_juramento"], 85)

    def test_api_economy_ledger_endpoint(self):
        resp = self.client.get("/api/economy/ledger")
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertEqual(data["sellos"], 20)
        self.assertGreaterEqual(len(data["entries"]), 1)
        self.assertEqual(data["entries"][0]["reason_code"], "starting_purse")

    # --- Pruebas de Concurrencia / Doble Gasto ---

    def test_concurrent_double_spend_prevented(self):
        # Saldo exacto para una sola compra de espada (85 sellos)
        self.set_sellos(85)

        def buy_attempt(_):
            return economy.buy_item_from_daro(self.path, self.player_id, "espada_juramento")[0]

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(buy_attempt, range(4)))

        # Exactamente UNA compra debe haber tenido éxito
        self.assertEqual(results.count(True), 1)
        self.assertEqual(results.count(False), 3)
        self.assertEqual(self.get_sellos(), 0)

    # --- Pruebas de Invarianza: Muerte y Respawn ---

    def test_sellos_and_ledger_survive_defeat_and_respawn(self):
        self.set_sellos(77)
        respawn_state = combat.respawn_state(100)
        wound = combat.respawn_wound("ninguna")
        store.update_combat_state(
            self.path,
            self.player_id,
            hp_current=respawn_state["hp_current"],
            fatigue=respawn_state["fatigue"],
            wound=wound,
            room="valdren_centro",
        )

        # Saldo debe permanecer intacto tras respawn
        self.assertEqual(self.get_sellos(), 77)
        # Consultar /api/inventory y /api/character
        inv = self.client.get("/api/inventory").json
        self.assertEqual(inv["sellos"], 77)
        char = self.client.get("/api/character").json
        self.assertEqual(char["sellos"], 77)


if __name__ == "__main__":
    unittest.main()
