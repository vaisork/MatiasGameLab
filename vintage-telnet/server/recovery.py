"""Recuperación comprable temprana — #410/#499.

Contrato cerrado:
- Ración de camino de Valdren: 8 sellos, +18% HPmax, -20 fatiga,
  no herida, no reset REST-01, consumible one-shot.
- Comida caliente del mercado: 18 sellos, HP hasta 90%, fatiga 0,
  herida mejora 1 grado y reset REST-01.
- Ambos contenidos viven en valdren_mercado y no producen efecto/coste
  cuando el personaje no obtiene beneficio.
"""
import time
import uuid

from . import combat, items, store


RATION_ITEM_ID = "racion_camino_valdren"
RATION_NAME = "Ración de camino de Valdren"
RATION_PRICE = 8
RATION_HP_FRACTION = 0.18
RATION_FATIGUE_REDUCTION = 20

SERVICE_ID = "comida_caliente_valdren_mercado"
SERVICE_NAME = "Comida caliente del mercado"
SERVICE_PRICE = 18
SERVICE_HP_FRACTION = 0.90

RECOVERY_ROOM = "valdren_mercado"


def _fold(text):
    return items._fold(text)


def resolve_recovery_target(text):
    normalized = _fold(text)
    aliases = {
        _fold(RATION_ITEM_ID): RATION_ITEM_ID,
        _fold(RATION_NAME): RATION_ITEM_ID,
        "racion": RATION_ITEM_ID,
        "racion de camino": RATION_ITEM_ID,
        _fold(SERVICE_ID): SERVICE_ID,
        _fold(SERVICE_NAME): SERVICE_ID,
        "comida caliente": SERVICE_ID,
    }
    return aliases.get(normalized)


def catalog():
    return {
        "room_id": RECOVERY_ROOM,
        "ration": {
            "item_id": RATION_ITEM_ID,
            "name": RATION_NAME,
            "price": RATION_PRICE,
        },
        "service": {
            "service_id": SERVICE_ID,
            "name": SERVICE_NAME,
            "price": SERVICE_PRICE,
        },
    }


def _combat_active(db, player_id, room_id):
    return db.execute(
        "SELECT 1 FROM room_encounters WHERE player_id = ? AND room_id = ? LIMIT 1",
        (player_id, room_id),
    ).fetchone() is not None


def buy_ration(path, player_id, room_id, *, now=None, client_tx_id=None):
    """Compra una instancia persistente de la ración, atómicamente."""
    if room_id != RECOVERY_ROOM:
        return False, "La Ración de camino se vende en el mercado de Valdren.", None
    now = time.time() if now is None else now
    clean_tx_id = str(client_tx_id).strip() if client_tx_id else None

    with store.connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        if _combat_active(db, player_id, room_id):
            return False, "No puedes comprar provisiones durante un encuentro.", None

        if clean_tx_id:
            source = f"recovery:buy:{RATION_ITEM_ID}:{clean_tx_id}"
            existing = db.execute(
                """SELECT balance_after FROM economy_ledger
                   WHERE player_id = ? AND source_key = ?""",
                (player_id, source),
            ).fetchone()
            if existing:
                return True, f"Compras {RATION_NAME} por {RATION_PRICE} sellos.", {
                    "balance": existing["balance_after"],
                    "item_id": RATION_ITEM_ID,
                    "idempotent_replay": True,
                }

        player = db.execute(
            "SELECT sellos FROM players WHERE id = ?", (player_id,)
        ).fetchone()
        if player is None:
            return False, "Personaje no encontrado.", None
        if player["sellos"] < RATION_PRICE:
            return False, (
                f"No tienes suficientes sellos. Necesitas {RATION_PRICE} "
                f"y tienes {player['sellos']}."
            ), {"balance": player["sellos"]}

        balance = player["sellos"] - RATION_PRICE
        db.execute(
            "UPDATE players SET sellos = ? WHERE id = ?",
            (balance, player_id),
        )
        instance_id = store.grant_item(
            path, player_id, RATION_ITEM_ID, connection=db
        )
        source = (
            f"recovery:buy:{RATION_ITEM_ID}:{clean_tx_id}"
            if clean_tx_id
            else f"recovery:buy:{RATION_ITEM_ID}:{instance_id}"
        )
        db.execute(
            """INSERT INTO economy_ledger
               (player_id, delta, balance_after, reason_code, source_key, created_at)
               VALUES (?, ?, ?, 'recovery_purchase', ?, ?)""",
            (player_id, -RATION_PRICE, balance, source, now),
        )
        return True, f"Compras {RATION_NAME} por {RATION_PRICE} sellos.", {
            "balance": balance,
            "item_id": RATION_ITEM_ID,
            "instance_id": instance_id,
            "idempotent_replay": False,
        }


def use_ration(path, player_id, inventory_item_id):
    """Consume una ración sólo si restaura HP y/o reduce fatiga."""
    with store.connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        player = db.execute(
            """SELECT room, hp_current, hp_max, fatigue, wound,
                      field_rest_budget_max, field_rest_healed
               FROM players WHERE id = ?""",
            (player_id,),
        ).fetchone()
        if player is None:
            return False, "Personaje no encontrado.", None
        if _combat_active(db, player_id, player["room"]):
            return False, "No puedes usar la ración durante un encuentro.", None

        owned = db.execute(
            """SELECT id FROM inventory_items
               WHERE id = ? AND player_id = ? AND item_key = ?""",
            (inventory_item_id, player_id, RATION_ITEM_ID),
        ).fetchone()
        if owned is None:
            return False, "No posees esa Ración de camino.", None

        hp_gain = min(
            max(0.0, float(player["hp_max"]) - float(player["hp_current"])),
            float(player["hp_max"]) * RATION_HP_FRACTION,
        )
        fatigue_gain = min(
            max(0.0, float(player["fatigue"])),
            float(RATION_FATIGUE_REDUCTION),
        )
        if hp_gain <= 0 and fatigue_gain <= 0:
            return False, "La ración no te aportaría ningún beneficio ahora.", {
                "consumed": False
            }

        hp_after = float(player["hp_current"]) + hp_gain
        fatigue_after = max(0.0, float(player["fatigue"]) - fatigue_gain)
        db.execute(
            """UPDATE players
               SET hp_current = ?, fatigue = ?, fatigue_updated_at = ?
               WHERE id = ?""",
            (hp_after, fatigue_after, time.time(), player_id),
        )
        db.execute(
            "DELETE FROM inventory_items WHERE id = ? AND player_id = ?",
            (inventory_item_id, player_id),
        )
        return True, f"Consumes {RATION_NAME}.", {
            "consumed": True,
            "hp_current": hp_after,
            "fatigue": fatigue_after,
            "wound": player["wound"],
            "field_rest_budget_max": player["field_rest_budget_max"],
            "field_rest_healed": player["field_rest_healed"],
        }


def use_market_service(path, player_id, room_id, *, now=None, client_tx_id=None):
    """Consume el servicio seguro del mercado sin crear objeto de inventario."""
    if room_id != RECOVERY_ROOM:
        return False, "La comida caliente sólo está disponible en el mercado de Valdren.", None
    now = time.time() if now is None else now
    clean_tx_id = str(client_tx_id).strip() if client_tx_id else None

    with store.connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        if _combat_active(db, player_id, room_id):
            return False, "No puedes usar el servicio durante un encuentro.", None

        if clean_tx_id:
            source = f"recovery:service:{SERVICE_ID}:{clean_tx_id}"
            existing = db.execute(
                """SELECT balance_after FROM economy_ledger
                   WHERE player_id = ? AND source_key = ?""",
                (player_id, source),
            ).fetchone()
            if existing:
                player = db.execute(
                    """SELECT hp_current, fatigue, wound FROM players WHERE id = ?""",
                    (player_id,),
                ).fetchone()
                return True, f"Recibes {SERVICE_NAME}.", {
                    "balance": existing["balance_after"],
                    "hp_current": player["hp_current"],
                    "fatigue": player["fatigue"],
                    "wound": player["wound"],
                    "idempotent_replay": True,
                }

        player = db.execute(
            """SELECT sellos, hp_current, hp_max, fatigue, wound,
                      field_rest_budget_max, field_rest_healed
               FROM players WHERE id = ?""",
            (player_id,),
        ).fetchone()
        if player is None:
            return False, "Personaje no encontrado.", None

        hp_target = float(player["hp_max"]) * SERVICE_HP_FRACTION
        hp_after = max(float(player["hp_current"]), hp_target)
        fatigue_after = 0.0
        wound_after = combat.respawn_wound(player["wound"])
        rest_needs_reset = (
            player["field_rest_budget_max"] is not None
            or float(player["field_rest_healed"] or 0.0) > 0
        )
        benefits = (
            hp_after > float(player["hp_current"])
            or float(player["fatigue"]) > 0
            or wound_after != player["wound"]
            or rest_needs_reset
        )
        if not benefits:
            return False, "La comida caliente no te aportaría ningún beneficio ahora.", {
                "charged": False,
                "balance": player["sellos"],
            }
        if player["sellos"] < SERVICE_PRICE:
            return False, (
                f"No tienes suficientes sellos. Necesitas {SERVICE_PRICE} "
                f"y tienes {player['sellos']}."
            ), {"charged": False, "balance": player["sellos"]}

        balance = player["sellos"] - SERVICE_PRICE
        db.execute(
            """UPDATE players
               SET sellos = ?, hp_current = ?, fatigue = ?, fatigue_updated_at = ?,
                   wound = ?, field_rest_budget_max = NULL, field_rest_healed = 0
               WHERE id = ?""",
            (balance, hp_after, fatigue_after, time.time(), wound_after, player_id),
        )
        source = (
            f"recovery:service:{SERVICE_ID}:{clean_tx_id}"
            if clean_tx_id
            else f"recovery:service:{SERVICE_ID}:{uuid.uuid4()}"
        )
        db.execute(
            """INSERT INTO economy_ledger
               (player_id, delta, balance_after, reason_code, source_key, created_at)
               VALUES (?, ?, ?, 'recovery_service', ?, ?)""",
            (player_id, -SERVICE_PRICE, balance, source, now),
        )
        return True, f"Recibes {SERVICE_NAME}.", {
            "balance": balance,
            "hp_current": hp_after,
            "fatigue": fatigue_after,
            "wound": wound_after,
            "charged": True,
            "idempotent_replay": False,
        }
