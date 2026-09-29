"""Selector y aplicación autoritativa de respawn (Issues #478/#479).

Fase A:
- Edran usa la plaza central de Valdren, ya autorizada por #46.
- Regiones sin ancla regional publicada usan el hogar personal.
- Toda muerte reutiliza combat.respawn_state()/respawn_wound() y reinicia
  el recovery budget de REST-01.
"""

from . import combat, store, world


REGIONAL_RESPAWN_ANCHORS = {
    "edran": "valdren_centro",
}


def select_respawn_room(player_id, death_room_id, species=None):
    """Devuelve un destino seguro sin usar Valdren como fallback global."""
    if not player_id:
        raise ValueError("player_id es obligatorio para seleccionar respawn.")

    region = world.get_room_region(death_room_id)
    if species == "humano":
        human_anchor = "valdren_centro"
        if world.get_room(human_anchor) is not None:
            return human_anchor
    anchor = REGIONAL_RESPAWN_ANCHORS.get(region)
    if anchor and world.get_room(anchor) is not None:
        return anchor
    return world.get_home_room_id(player_id)


def apply_player_respawn(db_path, player, current_wound=None, death_room_id=None):
    """Aplica el estado canónico de muerte y devuelve el resultado persistido.

    No toca XP, nivel, PA/PP, inventario ni equipo. Las excepciones específicas
    de C5 (pérdida de arma opt-in) se resuelven antes de llamar a este helper.
    """
    player = dict(player)
    player_id = player["id"]
    death_room_id = death_room_id or player.get("room")
    species = store.get_player_species(db_path, player_id)
    destination = select_respawn_room(player_id, death_room_id, species)

    state = combat.respawn_state(player["hp_max"])
    wound_after = combat.respawn_wound(
        current_wound if current_wound is not None else player.get("wound", "ninguna")
    )
    store.update_combat_state(
        db_path,
        player_id,
        hp_current=state["hp_current"],
        fatigue=state["fatigue"],
        wound=wound_after,
        room=destination,
        reset_rest_budget=True,
    )

    room = world.get_room(destination)
    return {
        "room_id": destination,
        "room_name": room["name"] if room else "un lugar seguro",
        "hp_current": state["hp_current"],
        "fatigue": state["fatigue"],
        "wound": wound_after,
    }
