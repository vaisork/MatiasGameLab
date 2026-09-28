"""Pruebas exhaustivas para compra autoritativa de armas con Daro (MERCHANT-01, Issue #385).

Verifica todos los criterios y reglas del Issue #385:
1. Acciones estructuradas de tienda: list_shop_inventory, quote_item, purchase_item.
2. Gate autoritativo: valida rol, presencia, combate, catálogo, fondos e inventario.
3. El modelo jamás suministra el precio autoritativo (se rechaza o ignora manipulación).
4. Compra atómica: debita moneda, crea instancia única no equipada y sin forja, registra en ledger.
5. Antifarming y seguridad: fondos insuficientes rechazan limpiamente; armas culturales rechazadas.
6. Cero duplicación ante reintento / doble submit con client_tx_id.
7. Persistencia completa y auditoría en npc_action_logs y economy_ledger.
8. Integración con el proveedor conversacional y endpoint /api/talk.
9. Lógica compartida entre comandos directos y diálogo estructurado.
"""
from copy import deepcopy
import json
import os
import sqlite3
import tempfile
import time
import unittest
from unittest.mock import patch

from server.app import create_app
from server import economy, items, npc_dialogue, store, world
from server.npc_dialogue import (
    ALLOWLISTED_NPC_ACTIONS,
    ActionGateResult,
    DialoguePrompt,
    DialogueResult,
    FixedDialogueProvider,
    NPCRegistry,
    ProposedAction,
    evaluate_action_gate,
    extract_proposed_action,
    converse,
)


class MockActionDialogueProvider(npc_dialogue.DialogueProvider):
    """Proveedor mock que inyecta una acción estructurada preconfigurada en formato de tag."""

    def __init__(self, reply_text: str, action_type: str | None = None, payload: dict | None = None):
        self.reply_text = reply_text
        self.action_type = action_type
        self.payload = payload or {}
        self.prompts: list[DialoguePrompt] = []

    def generate_reply(self, prompt: DialoguePrompt) -> str:
        self.prompts.append(prompt)
        if not self.action_type:
            return self.reply_text
        tag = f'<!--ACTION: {json.dumps({"type": self.action_type, "payload": self.payload})}-->'
        return f"{self.reply_text}\n{tag}"


class MerchantDaroUnitTests(unittest.TestCase):
    """Pruebas unitarias de aislamiento para las acciones estructuradas de comerciante y el Gate."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp.name, "test_merchant.db")
        store.initialize(self.db_path)

        token = store.register(self.db_path, "user_merchant", "Aran", "pass123")
        self.token = token
        self.player = dict(store.player_for_token(self.db_path, token))
        self.player["token"] = token
        self.player["room"] = "valdren_forja"

        # Otorgar 100 sellos para pruebas de compra
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET sellos = 100 WHERE id = ?", (self.player["id"],))
        self.player["sellos"] = 100

        self.registry = NPCRegistry()
        self.npc_daro = deepcopy(npc_dialogue.CANONICAL_NPCS[0])
        self.registry.register(self.npc_daro)

    def tearDown(self):
        try:
            self.temp.cleanup()
        except (PermissionError, OSError):
            pass

    # --- 1. Allowlist ---------------------------------------------------------

    def test_merchant_actions_are_allowlisted(self):
        """Las acciones list_shop_inventory, quote_item y purchase_item pertenecen al allowlist."""
        self.assertIn("list_shop_inventory", ALLOWLISTED_NPC_ACTIONS)
        self.assertIn("quote_item", ALLOWLISTED_NPC_ACTIONS)
        self.assertIn("purchase_item", ALLOWLISTED_NPC_ACTIONS)

    # --- 2. list_shop_inventory -----------------------------------------------

    def test_list_shop_inventory_success(self):
        """En valdren_forja con Daro, el Gate acepta y lista el catálogo completo con precios canónicos."""
        proposed = ProposedAction(action_type="list_shop_inventory", payload={})
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_res.accepted)
        self.assertEqual(gate_res.action_type, "list_shop_inventory")
        self.assertEqual(gate_res.reason, "shop_inventory_listed")
        self.assertIsNotNone(gate_res.effect)

        catalog = gate_res.effect["catalog"]
        keys = [item["item_key"] for item in catalog]
        self.assertIn("varita_aprendiz", keys)
        self.assertIn("punal_camino", keys)
        self.assertIn("arco_ruta", keys)
        self.assertIn("espada_juramento", keys)

        # Precios exactos
        price_map = {item["item_key"]: item["price"] for item in catalog}
        self.assertEqual(price_map["varita_aprendiz"], 40)
        self.assertEqual(price_map["punal_camino"], 50)
        self.assertEqual(price_map["arco_ruta"], 65)
        self.assertEqual(price_map["espada_juramento"], 85)

    def test_list_shop_inventory_wrong_room_rejected(self):
        """Fuera de la forja, el Gate rechaza listar el inventario del taller."""
        player_outside = dict(self.player)
        player_outside["room"] = "valdren_centro"
        proposed = ProposedAction(action_type="list_shop_inventory", payload={})
        gate_res = evaluate_action_gate(
            self.npc_daro,
            player_outside,
            proposed,
            room_id="valdren_centro",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.reason, "presence_mismatch")

    def test_list_shop_inventory_during_combat_rejected(self):
        """Durante combate activo, el Gate rechaza listar el inventario."""
        player_combat = dict(self.player)
        player_combat["in_combat"] = True
        proposed = ProposedAction(action_type="list_shop_inventory", payload={})
        gate_res = evaluate_action_gate(
            self.npc_daro,
            player_combat,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.reason, "cannot_trade_during_combat")

    # --- 3. quote_item -------------------------------------------------------

    def test_quote_item_canonical_prices(self):
        """Cotizar armas retorna exactamente los precios canónicos del catálogo."""
        for item_key, expected_price in economy.DARO_CATALOG.items():
            proposed = ProposedAction(action_type="quote_item", payload={"item_key": item_key})
            gate_res = evaluate_action_gate(
                self.npc_daro,
                self.player,
                proposed,
                room_id="valdren_forja",
                db_path=self.db_path,
            )
            self.assertTrue(gate_res.accepted, f"Fallo al cotizar {item_key}")
            self.assertEqual(gate_res.effect["price_sellos"], expected_price)
            self.assertEqual(gate_res.effect["item_key"], item_key)
            self.assertTrue(gate_res.effect["can_afford"])  # Con 100 sellos puede costear todas

    def test_quote_item_can_afford_false_when_balance_too_low(self):
        """Cotizar espada (85 sellos) con saldo 20 indica can_afford = False."""
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET sellos = 20 WHERE id = ?", (self.player["id"],))

        proposed = ProposedAction(action_type="quote_item", payload={"item_key": "espada_juramento"})
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_res.accepted)
        self.assertEqual(gate_res.effect["price_sellos"], 85)
        self.assertEqual(gate_res.effect["player_balance"], 20)
        self.assertFalse(gate_res.effect["can_afford"])

    def test_quote_item_ignores_manipulated_price_payload(self):
        """Un payload malicioso con price=0 es completamente ignorado; el Gate fija el precio canónico."""
        proposed = ProposedAction(
            action_type="quote_item",
            payload={"item_key": "espada_juramento", "price": 0, "sellos": 1},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_res.accepted)
        # El precio reportado es 85, no 0 ni 1
        self.assertEqual(gate_res.effect["price_sellos"], 85)

    def test_quote_item_non_catalog_rejected(self):
        """Objetos no vendidos por Daro (Hoja de Hoshai, armaduras, desconocidos) son rechazados."""
        for invalid_key in ["hoja_hoshai", "martillo_korven", "armadura_cuero", "pocion_rara"]:
            proposed = ProposedAction(action_type="quote_item", payload={"item_key": invalid_key})
            gate_res = evaluate_action_gate(
                self.npc_daro,
                self.player,
                proposed,
                room_id="valdren_forja",
                db_path=self.db_path,
            )
            self.assertFalse(gate_res.accepted, f"No debió aceptar cotizar {invalid_key}")
            self.assertEqual(gate_res.reason, "item_not_in_catalog")

    # --- 4. purchase_item ----------------------------------------------------

    def test_purchase_item_success_atomic(self):
        """Compra exitosa: descuenta sellos, entrega instancia no equipada y audita en ledger y logs."""
        proposed = ProposedAction(
            action_type="purchase_item",
            payload={"item_key": "espada_juramento"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_res.accepted)
        self.assertEqual(gate_res.reason, "item_purchased_safely")
        self.assertEqual(gate_res.effect["balance"], 15)  # 100 - 85 = 15
        self.assertEqual(gate_res.effect["item_key"], "espada_juramento")
        self.assertFalse(gate_res.effect["is_equipped"])
        self.assertFalse(gate_res.effect["forge_validated"])

        # Verificar saldo en SQLite
        balance = economy.get_player_balance(self.db_path, self.player["id"])
        self.assertEqual(balance, 15)

        # Verificar que el inventario contiene la espada
        items_list = store.list_inventory(self.db_path, self.player["id"])
        swords = [i for i in items_list if i["item_key"] == "espada_juramento"]
        self.assertEqual(len(swords), 1)
        self.assertEqual(swords[0]["forge_validated"], 0)

        # Verificar ledger
        ledger = economy.list_player_ledger(self.db_path, self.player["id"])
        self.assertEqual(ledger[0]["delta"], -85)
        self.assertEqual(ledger[0]["balance_after"], 15)
        self.assertEqual(ledger[0]["reason_code"], "shop_purchase")

        # Verificar auditoría de Gate en npc_action_logs
        logs = store.list_npc_action_logs(self.db_path, player_id=self.player["id"])
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["action_type"], "purchase_item")
        self.assertEqual(logs[0]["accepted"], 1)

    def test_purchase_item_insufficient_funds_rejected(self):
        """Fondos insuficientes: el Gate rechaza tajantemente; 0 sellos descontados, 0 items entregados."""
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET sellos = 30 WHERE id = ?", (self.player["id"],))

        proposed = ProposedAction(
            action_type="purchase_item",
            payload={"item_key": "espada_juramento"},  # Cuesta 85 sellos
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.reason, "insufficient_funds")

        # Saldo sin cambios
        balance = economy.get_player_balance(self.db_path, self.player["id"])
        self.assertEqual(balance, 30)

        # Sin items nuevos
        items_list = store.list_inventory(self.db_path, self.player["id"])
        swords = [i for i in items_list if i["item_key"] == "espada_juramento"]
        self.assertEqual(len(swords), 0)

        # Auditoría registrada con accepted=0
        logs = store.list_npc_action_logs(self.db_path, player_id=self.player["id"])
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["action_type"], "purchase_item")
        self.assertEqual(logs[0]["accepted"], 0)
        self.assertEqual(logs[0]["reason"], "insufficient_funds")

    def test_purchase_item_non_catalog_rejected(self):
        """Comprar armas no autorizadas (Hoja de Hoshai) es rechazado por el Gate sin tocar moneda."""
        proposed = ProposedAction(
            action_type="purchase_item",
            payload={"item_key": "hoja_hoshai"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.reason, "item_not_in_catalog")

        # Saldo intacto
        self.assertEqual(economy.get_player_balance(self.db_path, self.player["id"]), 100)

    def test_purchase_item_during_combat_rejected(self):
        """Comprar durante combate activo es rechazado de inmediato."""
        player_combat = dict(self.player)
        player_combat["in_combat"] = True
        proposed = ProposedAction(
            action_type="purchase_item",
            payload={"item_key": "varita_aprendiz"},
        )
        gate_res = evaluate_action_gate(
            self.npc_daro,
            player_combat,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertFalse(gate_res.accepted)
        self.assertEqual(gate_res.reason, "cannot_buy_during_combat")
        self.assertEqual(economy.get_player_balance(self.db_path, self.player["id"]), 100)

    def test_purchase_item_idempotent_double_submit(self):
        """Doble submit con el mismo client_tx_id no duplica cobro ni crea un segundo objeto."""
        tx_id = "tx-unique-nonce-12345"
        proposed = ProposedAction(
            action_type="purchase_item",
            payload={"item_key": "varita_aprendiz", "client_tx_id": tx_id},  # 40 sellos
        )

        # Primer submit
        gate_1 = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_1.accepted)
        self.assertEqual(gate_1.effect["balance"], 60)  # 100 - 40 = 60

        # Segundo submit idéntico (reintento de red o doble click)
        gate_2 = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_2.accepted)
        self.assertTrue(gate_2.effect.get("idempotent_replay"))
        self.assertEqual(gate_2.effect["balance"], 60)

        # Verificar saldo final en DB: sigue siendo 60, no 20
        self.assertEqual(economy.get_player_balance(self.db_path, self.player["id"]), 60)

        # Solo existe 1 varita creada, no 2
        items_list = store.list_inventory(self.db_path, self.player["id"])
        varitas = [i for i in items_list if i["item_key"] == "varita_aprendiz"]
        self.assertEqual(len(varitas), 1)

    def test_purchase_item_never_auto_equips(self):
        """La compra nunca autoequipa el arma; el arma original sigue equipada."""
        # Otorgar puñal inicial y equiparlo
        dagger_id = store.grant_item(self.db_path, self.player["id"], "punal_camino")
        store.equip_item(self.db_path, self.player["id"], dagger_id)

        p_before = store.player_for_token(self.db_path, self.player["token"])
        self.assertEqual(p_before["equipped_weapon_id"], dagger_id)

        # Compra una espada
        proposed = ProposedAction(action_type="purchase_item", payload={"item_key": "espada_juramento"})
        gate_res = evaluate_action_gate(
            self.npc_daro,
            self.player,
            proposed,
            room_id="valdren_forja",
            db_path=self.db_path,
        )
        self.assertTrue(gate_res.accepted)
        self.assertFalse(gate_res.effect["is_equipped"])

        # Verificar qué arma está equipada: sigue siendo el puñal inicial
        p_after = store.player_for_token(self.db_path, self.player["token"])
        self.assertEqual(p_after["equipped_weapon_id"], dagger_id)

        # La espada está en inventario pero su id no es equipped_weapon_id
        items_after = store.list_inventory(self.db_path, self.player["id"])
        sword = [i for i in items_after if i["item_key"] == "espada_juramento"][0]
        self.assertNotEqual(sword["id"], dagger_id)
        self.assertNotEqual(p_after["equipped_weapon_id"], sword["id"])


class MerchantDaroDialogueIntegrationTests(unittest.TestCase):
    """Pruebas de integración de conversación con Daro y compras mediante API HTTP."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({
            "DATA_DIR": self.temp.name,
            "TESTING": True,
            "SECRET_KEY": "a" * 32,
        })
        self.client = self.app.test_client()
        self.db_path = self.app.config["DATABASE"]
        self._register_and_setup()

    def tearDown(self):
        npc_dialogue.set_default_provider(FixedDialogueProvider())
        try:
            self.temp.cleanup()
        except (PermissionError, OSError):
            pass

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        import re
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
        self.post("/register", dict(username="buyer1", name="El Comprador", password="password123"))
        dm = self.app.test_client()
        with patch.dict("os.environ", {"VT_DM_PASSWORD": "dm-secret-value"}):
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username="buyer1"), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        self.player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.db_path, self.player_id, "juramentado", "espada_juramento")
        store.move_player(self.db_path, self.player_id, "valdren_forja")
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET sellos = 100 WHERE id = ?", (self.player_id,))

    def test_api_talk_with_action_tag_executes_purchase(self):
        """Conversar con Daro y recibir una propuesta estructurada purchase_item ejecuta la compra en /api/talk."""
        provider = MockActionDialogueProvider(
            reply_text="Aquí tienes un buen arco de ruta bien templado.",
            action_type="purchase_item",
            payload={"item_key": "arco_ruta"},  # 65 sellos
        )

        npc_dialogue.set_default_provider(provider)
        resp = self.post_json(
            "/api/talk",
            {"target": "daro", "message": "Quiero comprar un arco de ruta"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["accepted"])
        self.assertEqual(data["npc"], "daro_herrero")
        self.assertIn("Aquí tienes un buen arco", data["reply"])

        # Comprobar gate_result en el payload
        gate_res = data["gate_result"]
        self.assertIsNotNone(gate_res)
        self.assertTrue(gate_res["accepted"])
        self.assertEqual(gate_res["action_type"], "purchase_item")
        self.assertEqual(gate_res["effect"]["balance"], 35)  # 100 - 65 = 35

        # Verificar persistencia en base de datos
        balance = economy.get_player_balance(self.db_path, self.player_id)
        self.assertEqual(balance, 35)

        items_list = store.list_inventory(self.db_path, self.player_id)
        bows = [i for i in items_list if i["item_key"] == "arco_ruta"]
        self.assertEqual(len(bows), 1)

    def test_api_talk_quote_item_dialogue(self):
        """Cotizar un arma vía /api/talk devuelve el precio canónico y no altera el saldo."""
        provider = MockActionDialogueProvider(
            reply_text="La espada de juramento son ochenta y cinco sellos de bronce.",
            action_type="quote_item",
            payload={"item_key": "espada_juramento"},
        )

        npc_dialogue.set_default_provider(provider)
        resp = self.post_json(
            "/api/talk",
            {"target": "daro", "message": "¿Cuánto cuesta la espada?"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        gate_res = data["gate_result"]
        self.assertTrue(gate_res["accepted"])
        self.assertEqual(gate_res["effect"]["price_sellos"], 85)
        self.assertTrue(gate_res["effect"]["can_afford"])

        # Saldo permanece intacto en 100 sellos
        self.assertEqual(economy.get_player_balance(self.db_path, self.player_id), 100)

    def test_api_talk_rejected_purchase_leaves_state_clean(self):
        """Si la compra es rechazada por fondos insuficientes, /api/talk reporta el fallo sin debitar."""
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET sellos = 10 WHERE id = ?", (self.player_id,))

        provider = MockActionDialogueProvider(
            reply_text="No tienes suficientes sellos para esa pieza.",
            action_type="purchase_item",
            payload={"item_key": "espada_juramento"},
        )

        npc_dialogue.set_default_provider(provider)
        resp = self.post_json(
            "/api/talk",
            {"target": "daro", "message": "Compro la espada"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        gate_res = data["gate_result"]
        self.assertFalse(gate_res["accepted"])
        self.assertEqual(gate_res["reason"], "insufficient_funds")

        # Saldo sigue en 10
        self.assertEqual(economy.get_player_balance(self.db_path, self.player_id), 10)


if __name__ == "__main__":
    unittest.main()
