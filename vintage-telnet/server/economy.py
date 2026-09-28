"""Núcleo económico v1 — ECONOMY-CORE-01 (#408 / ECONOMY.md / DARO_ECONOMY_CANON.md).

Reglas autoritativas:
- Moneda: sellos (entero no negativo por personaje).
- Saldo inicial: 20 sellos por personaje.
- Catálogo de Daro en Valdren:
    * Varita de aprendiz: 40 sellos (compra), 14 sellos (reventa 35% floor).
    * Puñal de camino: 50 sellos (compra), 17 sellos (reventa 35% floor).
    * Arco de ruta: 65 sellos (compra), 22 sellos (reventa 35% floor).
    * Espada de juramento: 85 sellos (compra), 29 sellos (reventa 35% floor).
- Reventa a Daro: solo las 4 armas comunes a 35% floor.
- Exclusiones de reventa:
    * Objetos equipados (debe desequipar primero).
    * Última arma utilizable del personaje (no dejar al jugador desarmado).
    * Armas regionales (Hoja de Hoshai, Martillo de Korven).
    * Objetos con forge_required = True.
    * Recompensas únicas / hito / misión.
- Transacciones atómicas con registro en ledger.
- El cliente nunca envía el precio autoritativo.
"""
import math
import time
import uuid

from . import items, store


STARTING_SELLOS = 20

# Catálogo de venta de Daro en Valdren (precios en sellos)
DARO_CATALOG = {
    "varita_aprendiz": 40,
    "punal_camino": 50,
    "arco_ruta": 65,
    "espada_juramento": 85,
}

# Porcentaje de reventa a Daro (35% redondeado hacia abajo)
RESALE_FRACTION = 0.35

DARO_BUYBACK = {
    key: int(math.floor(price * RESALE_FRACTION))
    for key, price in DARO_CATALOG.items()
}

DARO_SHOP_ROOM = "valdren_forja"
DARO_NPC_ID = "daro_herrero"

DARO_ITEM_ALIASES = {
    "varita": "varita_aprendiz",
    "varita de aprendiz": "varita_aprendiz",
    "punal": "punal_camino",
    "puñal": "punal_camino",
    "punal de camino": "punal_camino",
    "puñal de camino": "punal_camino",
    "arco": "arco_ruta",
    "arco de ruta": "arco_ruta",
    "espada": "espada_juramento",
    "espada de juramento": "espada_juramento",
}


def resolve_daro_item(text: str) -> str | None:
    """Resuelve texto de comando o clave a una clave canónica de Daro."""
    if not text:
        return None
    normalized = items._fold(text)
    if normalized in DARO_ITEM_ALIASES:
        return DARO_ITEM_ALIASES[normalized]
    if normalized in DARO_CATALOG:
        return normalized
    for key in DARO_CATALOG:
        data = items.get_item(key)
        if data and data.get("normalized_name") == normalized:
            return key
    return None


def get_buy_price(item_key: str) -> int | None:
    """Devuelve el precio en sellos de venta de Daro o None si no está en catálogo."""
    return DARO_CATALOG.get(item_key)


def get_resale_price(item_key: str) -> int | None:
    """Devuelve el precio de recompra de Daro (35% floor) o None si no lo compra."""
    return DARO_BUYBACK.get(item_key)


def daro_catalog_entries() -> list[dict]:
    """Lista estructurada de artículos que Daro vende."""
    entries = []
    for item_key, price in DARO_CATALOG.items():
        data = items.get_item(item_key)
        if data:
            entries.append({
                "item_key": item_key,
                "name": data["name"],
                "price": price,
                "resale_price": DARO_BUYBACK.get(item_key, 0),
                "category": data["category"],
                "base_damage": data.get("base_damage"),
                "can_block": data.get("can_block", False),
            })
    return entries


get_daro_catalog_items = daro_catalog_entries


def get_player_balance(path: str, player_id: str) -> int:
    """Obtiene el saldo autoritativo de sellos de un personaje."""
    with store.connect(path) as db:
        row = db.execute("SELECT sellos FROM players WHERE id = ?", (player_id,)).fetchone()
        if row is None:
            raise LookupError(f"Personaje {player_id} no encontrado.")
        return row["sellos"]


def list_player_ledger(path: str, player_id: str, limit: int = 50) -> list[dict]:
    """Lista las entradas recientes del ledger económico de un personaje."""
    with store.connect(path) as db:
        rows = db.execute(
            """SELECT id, player_id, delta, balance_after, reason_code, source_key, created_at
               FROM economy_ledger
               WHERE player_id = ?
               ORDER BY id DESC
               LIMIT ?""",
            (player_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]


def buy_item_from_daro(
    path: str,
    player_id: str,
    item_key: str,
    now: float | None = None,
    client_tx_id: str | None = None,
) -> tuple[bool, str, dict | None]:
    """Compra atómicamente un objeto a Daro.

    Validaciones:
    - El objeto debe pertenecer al catálogo de Daro.
    - El personaje debe tener fondos suficientes (sellos >= precio).

    Efectos atómicos:
    - Debita el precio en sellos.
    - Crea una nueva instancia del objeto en inventory_items.
    - Registra la transacción en economy_ledger.
    - Soporta client_tx_id opcional para deduplicación idempotente ante reintentos/doble submit.

    Retorna: (éxito, mensaje, datos_extra)
    """
    if now is None:
        now = time.time()

    price = DARO_CATALOG.get(item_key)
    if price is None:
        return False, "Daro no vende ese objeto en su taller.", None

    catalog_item = items.get_item(item_key)
    if not catalog_item:
        return False, "Objeto desconocido en el catálogo.", None

    clean_tx_id = str(client_tx_id).strip() if client_tx_id else None

    with store.connect(path) as db:
        db.execute("BEGIN IMMEDIATE")

        # Comprobación de idempotencia si se proporciona client_tx_id
        if clean_tx_id:
            expected_key = f"daro:buy:{item_key}:{clean_tx_id}"
            existing = db.execute(
                "SELECT balance_after FROM economy_ledger WHERE player_id = ? AND source_key = ?",
                (player_id, expected_key),
            ).fetchone()
            if existing:
                return True, f"Compras {catalog_item['name']} a Daro por {price} sellos.", {
                    "balance": existing["balance_after"],
                    "item_key": item_key,
                    "name": catalog_item["name"],
                    "idempotent_replay": True,
                    "forge_validated": False,
                    "is_equipped": False,
                }

        player_row = db.execute("SELECT sellos FROM players WHERE id = ?", (player_id,)).fetchone()
        if not player_row:
            return False, "Personaje no encontrado.", None

        current_balance = player_row["sellos"]
        if current_balance < price:
            return False, f"No tienes suficientes sellos. Necesitas {price} sellos y tienes {current_balance}.", {"balance": current_balance}

        new_balance = current_balance - price
        cursor = db.execute(
            "UPDATE players SET sellos = ? WHERE id = ? AND sellos >= ?",
            (new_balance, player_id, price),
        )
        if cursor.rowcount == 0:
            return False, "No se pudo debitar el saldo. Inténtalo de nuevo.", {"balance": current_balance}

        instance_id = str(uuid.uuid4())
        db.execute(
            """INSERT INTO inventory_items (id, player_id, item_key, category, forge_validated, acquired_at)
               VALUES (?, ?, ?, ?, 0, ?)""",
            (instance_id, player_id, item_key, catalog_item["category"], store.utcnow()),
        )

        ledger_source = f"daro:buy:{item_key}:{clean_tx_id}" if clean_tx_id else f"daro:buy:{item_key}:{instance_id}"
        db.execute(
            """INSERT INTO economy_ledger (player_id, delta, balance_after, reason_code, source_key, created_at)
               VALUES (?, ?, ?, 'shop_purchase', ?, ?)""",
            (player_id, -price, new_balance, ledger_source, now),
        )

        return True, f"Compras {catalog_item['name']} a Daro por {price} sellos.", {
            "balance": new_balance,
            "instance_id": instance_id,
            "item_key": item_key,
            "name": catalog_item["name"],
            "forge_validated": False,
            "is_equipped": False,
        }


def sell_item_to_daro(path: str, player_id: str, inventory_item_id: str, now: float | None = None) -> tuple[bool, str, dict | None]:
    """Vende atómicamente un objeto de inventario a Daro.

    Validaciones:
    - El objeto debe existir en el inventario del personaje.
    - No debe estar equipado (debe desequipar primero).
    - Debe ser un objeto recomprable por Daro (DARO_BUYBACK: armas comunes).
    - No debe ser la última arma utilizable en el inventario del personaje.

    Efectos atómicos:
    - Retira la instancia de inventory_items.
    - Acredita el precio de reventa (35% floor) en sellos.
    - Registra la transacción en economy_ledger.

    Retorna: (éxito, mensaje, datos_extra)
    """
    if now is None:
        now = time.time()

    with store.connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        player_row = db.execute(
            "SELECT sellos, equipped_weapon_id, equipped_armor_id FROM players WHERE id = ?",
            (player_id,),
        ).fetchone()
        if not player_row:
            return False, "Personaje no encontrado.", None

        current_balance = player_row["sellos"]

        item_row = db.execute(
            "SELECT id, item_key, category FROM inventory_items WHERE id = ? AND player_id = ?",
            (inventory_item_id, player_id),
        ).fetchone()
        if not item_row:
            return False, "No posees ese objeto en tu inventario.", {"balance": current_balance}

        item_key = item_row["item_key"]
        category = item_row["category"]

        # No vender si está equipado
        if inventory_item_id in (player_row["equipped_weapon_id"], player_row["equipped_armor_id"]):
            return False, "No puedes vender un objeto que tienes equipado. Desequípalo primero.", {"balance": current_balance}

        # Daro solo compra las 4 armas comunes autorizadas
        resale_price = DARO_BUYBACK.get(item_key)
        if resale_price is None:
            return False, "Daro no compra este tipo de objeto.", {"balance": current_balance}

        # Regla de seguridad: no dejar al personaje sin armas utilizables
        if category == "weapon":
            weapon_count = db.execute(
                "SELECT COUNT(*) FROM inventory_items WHERE player_id = ? AND category = 'weapon'",
                (player_id,),
            ).fetchone()[0]
            if weapon_count <= 1:
                return False, "No puedes vender tu última arma utilizable. Consigue otra antes de venderla.", {"balance": current_balance}

        # Eliminar la instancia del inventario
        cursor = db.execute(
            "DELETE FROM inventory_items WHERE id = ? AND player_id = ?",
            (inventory_item_id, player_id),
        )
        if cursor.rowcount == 0:
            return False, "No se pudo retirar el objeto del inventario.", {"balance": current_balance}

        new_balance = current_balance + resale_price
        db.execute(
            "UPDATE players SET sellos = ? WHERE id = ?",
            (new_balance, player_id),
        )

        db.execute(
            """INSERT INTO economy_ledger (player_id, delta, balance_after, reason_code, source_key, created_at)
               VALUES (?, ?, ?, 'shop_sale', ?, ?)""",
            (player_id, resale_price, new_balance, f"daro:sale:{item_key}:{inventory_item_id}", now),
        )

        item_data = items.get_item(item_key)
        name = item_data["name"] if item_data else item_key

        return True, f"Vendes {name} a Daro por {resale_price} sellos.", {
            "balance": new_balance,
            "item_key": item_key,
            "name": name,
            "resale_price": resale_price,
        }
