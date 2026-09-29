"""RECOVERY-CONTENT-IDS-01 (#499 / #410)."""
import re
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import economy, items, recovery, store


class RecoveryEconomyIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = {
            "TESTING": True,
            "SECRET_KEY": "test-recovery-secret-" * 4,
            "DATA_DIR": self.temp.name,
            "SESSION_COOKIE_SECURE": False,
        }
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]
        self._register()
        store.move_player(self.path, self.player_id, recovery.RECOVERY_ROOM)

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, client=None):
        client = client or self.client
        page = client.get("/").get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', page)
        return match[1] if match else ""

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        page = client.get(csrf_path).get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', page)
        csrf = match[1] if match else ""
        return client.post(route, data={**(data or {}), "csrf": csrf})

    def post_json(self, route, data=None):
        payload = dict(data or {})
        payload.setdefault("csrf", self.csrf())
        return self.client.post(route, json=payload)

    def _register(self):
        self.post("/register", {
            "username": "recoverytester",
            "name": "Recovery Tester",
            "password": "password123",
        })
        dm = self.app.test_client()
        with patch.dict("os.environ", {"VT_DM_PASSWORD": "dm-secret-value"}):
            self.post("/dm/login", {"dm_password": "dm-secret-value"}, dm, "/dm")
            self.post("/dm/approve", {"username": "recoverytester"}, dm, "/dm")
        self.post("/species", {"species": "humano"})
        self.player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(
            self.path, self.player_id, "juramentado", "espada_juramento"
        )

    def set_state(self, **values):
        assignments = ", ".join(f"{key} = ?" for key in values)
        with store.connect(self.path) as db:
            db.execute(
                f"UPDATE players SET {assignments} WHERE id = ?",
                (*values.values(), self.player_id),
            )

    def player(self):
        return dict(store.character_by_player_id(self.path, self.player_id))

    def rations(self):
        return [
            row for row in store.list_inventory(self.path, self.player_id)
            if row["item_key"] == recovery.RATION_ITEM_ID
        ]

    def test_valdren_plaza_exposes_market_and_forge_then_buy_ration(self):
        store.move_player(self.path, self.player_id, "valdren_centro")
        plaza = self.client.get("/").get_data(as_text=True)
        self.assertIn("Ir al Mercado de Valdren", plaza)
        self.assertIn("Ir a la Forja de Daro", plaza)
        self.assertEqual(self.post("/move", {"direction": "east"}).status_code, 303)
        market = self.client.get("/").get_data(as_text=True)
        self.assertIn("Provisiones y comida del mercado", market)
        self.assertIn("Comprar ración · 8 sellos", market)
        self.assertIn("Comida caliente · 18 sellos", market)
        bought = self.post("/command", {"text": "comprar Ración de camino de Valdren"})
        self.assertEqual(bought.status_code, 200)
        self.assertIn("Compras", bought.get_data(as_text=True))
        self.assertEqual(len(self.rations()), 1)
        inventory_page = self.client.get("/").get_data(as_text=True)
        self.assertIn('item.category === "consumable" ? "Usar"', inventory_page)
        self.assertEqual(self.post("/move", {"direction": "west"}).status_code, 303)
        self.assertEqual(self.post("/move", {"direction": "west"}).status_code, 303)
        forge = self.client.get("/").get_data(as_text=True)
        self.assertIn("Taller de Daro", forge)

    def test_stable_ids_and_catalog_contract(self):
        self.assertEqual(recovery.RATION_ITEM_ID, "racion_camino_valdren")
        self.assertEqual(recovery.SERVICE_ID, "comida_caliente_valdren_mercado")
        self.assertEqual(recovery.RATION_PRICE, 8)
        self.assertEqual(recovery.SERVICE_PRICE, 18)
        self.assertEqual(items.category_of(recovery.RATION_ITEM_ID), "consumable")
        data = self.client.get("/api/recovery/valdren").json
        self.assertTrue(data["in_market"])
        self.assertEqual(data["ration"]["item_id"], recovery.RATION_ITEM_ID)
        self.assertEqual(data["service"]["service_id"], recovery.SERVICE_ID)

    def test_buy_ration_is_atomic_and_idempotent(self):
        self.set_state(sellos=20)
        payload = {
            "item_id": recovery.RATION_ITEM_ID,
            "client_tx_id": "buy-ration-001",
        }
        first = self.post_json("/api/recovery/buy", payload)
        second = self.post_json("/api/recovery/buy", payload)

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(economy.get_player_balance(self.path, self.player_id), 12)
        self.assertEqual(len(self.rations()), 1)
        self.assertTrue(second.json["idempotent_replay"])

        entries = [
            row for row in economy.list_player_ledger(self.path, self.player_id)
            if row["reason_code"] == "recovery_purchase"
        ]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["delta"], -8)

    def test_ration_restores_exact_contract_without_resetting_rest_budget(self):
        self.set_state(
            sellos=20, hp_max=100, hp_current=50, fatigue=50, wound="grave",
            field_rest_budget_max=12, field_rest_healed=7,
        )
        self.post_json("/api/recovery/buy", {"item_id": recovery.RATION_ITEM_ID})
        ration = self.rations()[0]

        response = self.post_json(
            "/api/recovery/use", {"inventory_item_id": ration["id"]}
        )
        self.assertEqual(response.status_code, 200)
        state = self.player()
        self.assertEqual(state["hp_current"], 68)
        self.assertEqual(state["fatigue"], 30)
        self.assertEqual(state["wound"], "grave")
        self.assertEqual(state["field_rest_budget_max"], 12)
        self.assertEqual(state["field_rest_healed"], 7)
        self.assertEqual(len(self.rations()), 0)
        self.assertEqual(state["sellos"], 12)

    def test_ration_is_not_consumed_when_it_produces_no_benefit(self):
        self.set_state(sellos=20, hp_max=100, hp_current=100, fatigue=0)
        self.post_json("/api/recovery/buy", {"item_id": recovery.RATION_ITEM_ID})
        ration = self.rations()[0]
        before = self.player()

        response = self.post_json(
            "/api/recovery/use", {"inventory_item_id": ration["id"]}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(self.rations()), 1)
        after = self.player()
        self.assertEqual(after["hp_current"], before["hp_current"])
        self.assertEqual(after["fatigue"], before["fatigue"])
        self.assertEqual(after["sellos"], before["sellos"])

    def test_market_service_applies_full_contract_and_resets_rest_budget(self):
        self.set_state(
            sellos=40, hp_max=100, hp_current=40, fatigue=60, wound="grave",
            field_rest_budget_max=12, field_rest_healed=12,
        )
        response = self.post_json("/api/recovery/service", {
            "service_id": recovery.SERVICE_ID,
            "client_tx_id": "hot-meal-001",
        })
        self.assertEqual(response.status_code, 200)

        state = self.player()
        self.assertEqual(state["sellos"], 22)
        self.assertEqual(state["hp_current"], 90)
        self.assertEqual(state["fatigue"], 0)
        self.assertEqual(state["wound"], "moderada")
        self.assertIsNone(state["field_rest_budget_max"])
        self.assertEqual(state["field_rest_healed"], 0)
        self.assertEqual(len([
            row for row in store.list_inventory(self.path, self.player_id)
            if row["item_key"] == recovery.SERVICE_ID
        ]), 0)

    def test_market_service_does_not_charge_without_benefit(self):
        self.set_state(
            sellos=40, hp_max=100, hp_current=100, fatigue=0, wound="ninguna",
            field_rest_budget_max=None, field_rest_healed=0,
        )
        response = self.post_json("/api/recovery/service", {
            "service_id": recovery.SERVICE_ID,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(economy.get_player_balance(self.path, self.player_id), 40)
        self.assertEqual(len([
            row for row in economy.list_player_ledger(self.path, self.player_id)
            if row["reason_code"] == "recovery_service"
        ]), 0)

    def test_market_service_retry_is_idempotent(self):
        self.set_state(
            sellos=40, hp_max=100, hp_current=50, fatigue=20, wound="leve",
            field_rest_budget_max=5, field_rest_healed=5,
        )
        payload = {
            "service_id": recovery.SERVICE_ID,
            "client_tx_id": "service-retry-001",
        }
        first = self.post_json("/api/recovery/service", payload)
        second = self.post_json("/api/recovery/service", payload)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(economy.get_player_balance(self.path, self.player_id), 22)
        self.assertTrue(second.json["idempotent_replay"])
        entries = [
            row for row in economy.list_player_ledger(self.path, self.player_id)
            if row["reason_code"] == "recovery_service"
        ]
        self.assertEqual(len(entries), 1)

    def test_recovery_is_rejected_outside_market_or_during_encounter(self):
        self.set_state(sellos=40)
        store.move_player(self.path, self.player_id, "valdren_centro")
        outside = self.post_json(
            "/api/recovery/buy", {"item_id": recovery.RATION_ITEM_ID}
        )
        self.assertEqual(outside.status_code, 400)
        self.assertEqual(economy.get_player_balance(self.path, self.player_id), 40)

        store.move_player(self.path, self.player_id, recovery.RECOVERY_ROOM)
        with store.connect(self.path) as db:
            db.execute(
                """INSERT INTO room_encounters
                   (player_id, room_id, creature_id, hp_current, engaged, created_at)
                   VALUES (?, ?, 'mordelinde', 10, 1, '2026-09-28')""",
                (self.player_id, recovery.RECOVERY_ROOM),
            )
        blocked = self.post_json(
            "/api/recovery/buy", {"item_id": recovery.RATION_ITEM_ID}
        )
        self.assertEqual(blocked.status_code, 400)
        self.assertEqual(economy.get_player_balance(self.path, self.player_id), 40)
        self.assertEqual(len(self.rations()), 0)

    def test_v22_inventory_migration_preserves_equipped_weapon(self):
        with tempfile.TemporaryDirectory() as temp:
            path = f"{temp}/migration.sqlite3"
            store.initialize(path)
            token = store.register(path, "legacy499", "Legacy 499", "password123")
            player = store.player_for_token(path, token)
            with store.connect(path) as db:
                db.execute(
                    "UPDATE players SET status = 'approved', species = 'humano' WHERE id = ?",
                    (player["id"],),
                )
            store.set_player_class(path, player["id"], "juramentado", "espada_juramento")
            before = dict(store.character_by_player_id(path, player["id"]))
            equipped_id = before["equipped_weapon_id"]
            self.assertIsNotNone(equipped_id)

            raw = sqlite3.connect(path)
            try:
                raw.execute("PRAGMA foreign_keys = OFF")
                raw.execute("BEGIN IMMEDIATE")
                raw.execute("""CREATE TABLE inventory_items_v22 (
                    id TEXT PRIMARY KEY,
                    player_id TEXT NOT NULL REFERENCES players(id),
                    item_key TEXT NOT NULL,
                    category TEXT NOT NULL CHECK(category IN ('weapon', 'armor')),
                    forge_validated INTEGER NOT NULL DEFAULT 0,
                    acquired_at TEXT NOT NULL)""")
                raw.execute(
                    """INSERT INTO inventory_items_v22
                       SELECT id, player_id, item_key, category, forge_validated, acquired_at
                       FROM inventory_items"""
                )
                raw.execute("DROP TABLE inventory_items")
                raw.execute("ALTER TABLE inventory_items_v22 RENAME TO inventory_items")
                raw.execute("CREATE INDEX inventory_items_player ON inventory_items(player_id)")
                raw.execute("PRAGMA user_version = 22")
                raw.commit()
            finally:
                raw.close()

            store.initialize(path)
            after = dict(store.character_by_player_id(path, player["id"]))
            self.assertEqual(after["equipped_weapon_id"], equipped_id)
            with store.connect(path) as db:
                self.assertEqual(
                    db.execute("PRAGMA user_version").fetchone()[0],
                    store.SCHEMA_VERSION,
                )
                self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])

            ration_id = store.grant_item(path, player["id"], recovery.RATION_ITEM_ID)
            inventory = store.list_inventory(path, player["id"])
            ration = next(row for row in inventory if row["id"] == ration_id)
            self.assertEqual(ration["category"], "consumable")

    def test_consumable_cannot_be_equipped(self):
        item_id = store.grant_item(
            self.path, self.player_id, recovery.RATION_ITEM_ID
        )
        ok, category, reason = store.equip_item(
            self.path, self.player_id, item_id
        )
        self.assertFalse(ok)
        self.assertEqual(category, "consumable")
        self.assertIn("no se equipa", reason)


if __name__ == "__main__":
    unittest.main()
