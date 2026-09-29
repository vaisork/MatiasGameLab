"""Materiales C1 y acopio de Valdren, según GAMEPLAY §42 y #500."""
import random
import time
import uuid

from . import store

MARKET = "valdren_mercado"
MARKETS = {f"{town}_mercado" for town in ("valdren", "khariel", "brumak", "narevia", "velmora")}
# family: (item_key, label, valor). Exactamente una opción por familia.
MATERIALS = {
    "mordelinde": ("salvage_mordelinde_piel", "Retazo de piel de Mordelinde", 3),
    "espinajo_rastrojo": ("salvage_espinajo_pua", "Púa rígida de Espinajo", 4),
    "unapiedra": ("salvage_unapiedra_escama", "Escama gruesa de Uñapiedra", 3),
    "saltacresta": ("salvage_saltacresta_fibra", "Fibra resistente de Saltacresta", 4),
    "cascapedernal": ("salvage_cascapedernal_caparazon", "Fragmento de caparazón de Cascapedernal", 3),
    "colagrieta": ("salvage_colagrieta_piel", "Retazo de piel de Colagrieta", 4),
    "pinzajunco": ("salvage_pinzajunco_caparazon", "Segmento de caparazón de Pinzajunco", 3),
    "saltalodo": ("salvage_saltalodo_membrana", "Membrana resistente de Saltalodo", 4),
    "rondamusgo": ("salvage_rondamusgo_fibra", "Fibra áspera de Rondamusgo", 3),
    "hilaria_niebla": ("salvage_hilaria_seda", "Seda de Hilaria de niebla", 4),
    "garralaja": ("salvage_garralaja_piel", "Tira de piel escamada de Garralaja", 3),
    "cavapolvo": ("salvage_cavapolvo_placa", "Placa dérmica de Cavapolvo", 4),
    "remojunco": ("salvage_remojunco_placa", "Placa córnea de Remojunco", 3),
    "velacauce": ("salvage_velacauce_membrana", "Membrana flexible de Velacauce", 4),
    "silbarisco": ("salvage_silbarisco_fibra", "Fibra superficial de Silbarisco", 3),
}
BY_KEY = {item[0]: item for item in MATERIALS.values()}


def roll_in_transaction(db, player_id, family, repeats, victory_id, *, rng=None):
    """Una tirada por victoria persistida; el caller posee la transacción."""
    item = MATERIALS.get(family)
    if not item:
        return None
    multiplier = 1 if repeats <= 3 else .6 if repeats <= 5 else .25
    draw = random.random() if rng is None else rng.random()
    if draw >= .7 * multiplier:
        return None
    material_id = str(uuid.uuid4())
    db.execute("""INSERT INTO salvage_items(id, player_id, victory_id, item_key, acquired_at)
                  VALUES (?, ?, ?, ?, ?)""", (material_id, player_id, victory_id, item[0], store.utcnow()))
    return item[1]


def list_materials(path, player_id):
    with store.connect(path) as db:
        rows = db.execute("SELECT id, item_key, acquired_at FROM salvage_items WHERE player_id = ? ORDER BY acquired_at",
                          (player_id,)).fetchall()
    return [{"id": row["id"], "item_key": row["item_key"], "name": BY_KEY[row["item_key"]][1],
             "price": BY_KEY[row["item_key"]][2], "category": "material", "acquired_at": row["acquired_at"]}
            for row in rows if row["item_key"] in BY_KEY]


def victory_message(path, player_id, family):
    if family not in MATERIALS:
        return None
    with store.connect(path) as db:
        row = db.execute("""SELECT s.item_key FROM pve_victories v
                            LEFT JOIN salvage_items s ON s.victory_id = v.id
                            WHERE v.player_id = ? ORDER BY v.id DESC LIMIT 1""", (player_id,)).fetchone()
    return (f"Recoges {BY_KEY[row['item_key']][1]}." if row and row["item_key"] in BY_KEY
            else "No quedó material aprovechable.")


def sell(path, player_id, room_id, material_id, *, now=None):
    if room_id not in MARKETS:
        return False, "El acopio compra materiales en los mercados de los pueblos.", None
    if not material_id:
        return False, "Elige un material de tu inventario.", None
    now = time.time() if now is None else now
    with store.connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        if db.execute("SELECT 1 FROM room_encounters WHERE player_id = ? AND room_id = ?", (player_id, room_id)).fetchone():
            return False, "No puedes comerciar durante un encuentro.", None
        source = f"salvage:sale:{material_id}"
        previous = db.execute("SELECT balance_after FROM economy_ledger WHERE player_id = ? AND source_key = ?",
                              (player_id, source)).fetchone()
        if previous:
            return True, "Este material ya fue vendido.", {"balance": previous["balance_after"], "idempotent_replay": True}
        row = db.execute("SELECT item_key FROM salvage_items WHERE id = ? AND player_id = ?", (material_id, player_id)).fetchone()
        if not row or row["item_key"] not in BY_KEY:
            return False, "No posees ese material.", None
        item = BY_KEY[row["item_key"]]
        balance = db.execute("SELECT sellos FROM players WHERE id = ?", (player_id,)).fetchone()["sellos"] + item[2]
        db.execute("DELETE FROM salvage_items WHERE id = ? AND player_id = ?", (material_id, player_id))
        db.execute("UPDATE players SET sellos = ? WHERE id = ?", (balance, player_id))
        db.execute("""INSERT INTO economy_ledger(player_id, delta, balance_after, reason_code, source_key, created_at)
                      VALUES (?, ?, ?, 'salvage_sale', ?, ?)""", (player_id, item[2], balance, source, now))
        return True, f"El acopio paga {item[2]} sellos por {item[1]}.", {"balance": balance, "price": item[2]}
