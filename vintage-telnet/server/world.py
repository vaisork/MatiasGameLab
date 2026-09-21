"""Static world data: rooms and species. No persistent state lives here.

PLACEHOLDER DE GEOGRAFIA -- NO ES CANON.

Esta conectividad (quien esta al norte/sur/este/oeste de quien, y la
microzona interna de cada pueblo) es un andamiaje minimo para poder probar
movimiento y persistencia, siguiendo el alcance minimo de
`vintage-telnet/FIRST_PLAYABLE_SLICE.md` (punto central, forja/taller,
mercado/alimentos, y caminos suficientes para N/S/E/O). Los nombres de
lugares y la asignacion especie -> pueblo de inicio SI son canon confirmado
(vintage-telnet/CONFIRMED_IDEAS.md), pero la geometria exacta y los textos
definitivos corresponden al Historiador y deben reemplazar este
placeholder cuando existan. La interfaz marca cada descripcion como
[PLACEHOLDER] para no presentar esta geografia provisional como canon.
"""

OPPOSITE_DIRECTION = {"north": "south", "south": "north", "east": "west", "west": "east"}
ALL_DIRECTIONS = ("north", "south", "east", "west")


def _build_town(prefix, display_name, outward_exits):
    """Genera la microzona minima de un pueblo: sala central (con las
    conexiones externas ya definidas) mas forja/mercado/sendero en las
    direcciones que queden libres, hasta un maximo de 3 salas internas
    (algunos pueblos ya usan 2 direcciones para caminos externos, como
    Narevia, y no les queda lugar para las tres)."""
    centro_id = f"{prefix}_centro"
    centro_exits = dict(outward_exits)
    free_directions = [d for d in ALL_DIRECTIONS if d not in outward_exits]

    internal_kinds = ["forja", "mercado", "sendero"]
    rooms = {}
    for direction, kind in zip(free_directions, internal_kinds):
        room_id = f"{prefix}_{kind}"
        centro_exits[direction] = room_id
        if kind == "forja":
            name = f"Forja de {display_name}"
            description = (
                f"[PLACEHOLDER] La forja o taller de {display_name}. "
                "(Descripcion pendiente del Historiador.)"
            )
        elif kind == "mercado":
            name = f"Mercado de {display_name}"
            description = (
                f"[PLACEHOLDER] El mercado o zona de alimentos de {display_name}. "
                "(Descripcion pendiente del Historiador.)"
            )
        else:
            name = f"Sendero de {display_name}"
            description = (
                f"[PLACEHOLDER] Un sendero interno de {display_name}, usado para probar "
                "el movimiento. (Descripcion pendiente del Historiador.)"
            )
        rooms[room_id] = {
            "name": name,
            "description": description,
            "exits": {OPPOSITE_DIRECTION[direction]: centro_id},
        }

    rooms[centro_id] = {
        "name": display_name,
        "description": (
            f"[PLACEHOLDER] El punto central y comunitario de {display_name}. "
            "(Descripcion pendiente del Historiador.)"
        ),
        "exits": centro_exits,
    }
    return rooms


ROOMS = {
    "vaisgard": {
        "name": "Vaisgard",
        "description": (
            "[PLACEHOLDER] La ciudad principal de Vintage Telnet. Aqui confluyen los "
            "caminos hacia los cinco pueblos de inicio. (Descripcion pendiente del Historiador.)"
        ),
        "exits": {
            "north": "road_north",
            "east": "khariel_centro",
            "south": "brumak_centro",
            "west": "narevia_centro",
        },
    },
    "road_north": {
        "name": "Camino del Norte",
        "description": (
            "[PLACEHOLDER] Un camino que conecta Vaisgard con Valdren. "
            "(Descripcion pendiente del Historiador.)"
        ),
        "exits": {"south": "vaisgard", "north": "valdren_centro"},
    },
    "road_west": {
        "name": "Camino del Oeste",
        "description": (
            "[PLACEHOLDER] Un camino que conecta Narevia con Velmora. "
            "(Descripcion pendiente del Historiador.)"
        ),
        "exits": {"east": "narevia_centro", "west": "velmora_centro"},
    },
}

# Cada pueblo de inicio confirmado recibe la misma microzona minima:
# punto central + forja + mercado (+ sendero cuando queda una cuarta
# direccion libre), suficiente para probar N/S/E/O dentro del pueblo.
ROOMS.update(_build_town("valdren", "Valdren", {"south": "road_north"}))
ROOMS.update(_build_town("khariel", "Khariel", {"west": "vaisgard"}))
ROOMS.update(_build_town("brumak", "Brumak", {"north": "vaisgard"}))
ROOMS.update(_build_town("narevia", "Narevia", {"east": "vaisgard", "west": "road_west"}))
ROOMS.update(_build_town("velmora", "Velmora", {"east": "road_west"}))

DIRECTION_LABEL_ES = {"north": "norte", "south": "sur", "east": "este", "west": "oeste"}

# Especie -> sala central del pueblo de inicio. Confirmado en
# vintage-telnet/CONFIRMED_IDEAS.md (la especie -> pueblo; la sala exacta
# dentro del pueblo es el punto central provisional de esta microzona).
STARTING_ROOM_BY_SPECIES = {
    "humano": "valdren_centro",
    "felaryn": "khariel_centro",
    "dravak": "brumak_centro",
    "marevyn": "narevia_centro",
    "vesperi": "velmora_centro",
}

# Lista de especies jugables confirmada. Los rasgos mostrados aqui son
# unicamente los que CONFIRMED_IDEAS.md autoriza a revelar al jugador (no se
# exponen las inspiraciones internas de diseno).
SPECIES = [
    {"id": "humano", "name": "Humano", "blurb": "Humano de este mundo de fantasia."},
    {
        "id": "felaryn",
        "name": "Felaryn",
        "blurb": (
            "Originarios de un pueblo entre las montanas. Saltan grandes distancias y "
            "ven con gran nitidez a la distancia."
        ),
    },
    {
        "id": "dravak",
        "name": "Dravak",
        "blurb": "Muy pequenos en comparacion con los humanos. (Cultura y capacidades pendientes.)",
    },
    {
        "id": "marevyn",
        "name": "Marevyn",
        "blurb": (
            "Altos, estilizados y muy integrados con la naturaleza; afines a lagos, rios "
            "y humedales. (Detalles pendientes.)"
        ),
    },
    {
        "id": "vesperi",
        "name": "Vesperi",
        "blurb": "Asociados a zonas nocturnas, bosques profundos y cavernas. (Apariencia pendiente.)",
    },
]

SPECIES_IDS = tuple(s["id"] for s in SPECIES)


def get_room(room_id):
    return ROOMS.get(room_id)


def get_starting_room_for_species(species_id):
    return STARTING_ROOM_BY_SPECIES.get(species_id, "vaisgard")


def describe_room(room_id, others_present):
    room = get_room(room_id)
    if room is None:
        return {
            "id": room_id,
            "name": "Sala desconocida",
            "description": "Estas en un lugar sin definir. (Error de mundo: sala desconocida.)",
            "exits": [],
            "others_present": [],
        }
    return {
        "id": room_id,
        "name": room["name"],
        "description": room["description"],
        "exits": [
            {"direction": direction, "label": DIRECTION_LABEL_ES.get(direction, direction)}
            for direction in room["exits"]
        ],
        "others_present": others_present,
    }
