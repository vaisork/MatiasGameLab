"""Static world data: rooms and species. No persistent state lives here.

PLACEHOLDER DE GEOGRAFIA -- NO ES CANON.

Esta conectividad (quien esta al norte/sur/este/oeste de quien) es un
andamiaje minimo para poder probar movimiento y persistencia. Los nombres
de lugares y la asignacion especie -> pueblo de inicio SI son canon
confirmado (vintage-telnet/CONFIRMED_IDEAS.md), pero la forma exacta del
mapa y las descripciones corresponden al Historiador y deben reemplazar
este placeholder cuando existan.
"""

ROOMS = {
    "vaisgard": {
        "name": "Vaisgard",
        "description": (
            "[PLACEHOLDER] La ciudad principal de Vintage Telnet. Aqui confluyen los "
            "caminos hacia los cinco pueblos de inicio. (Descripcion pendiente del Historiador.)"
        ),
        "exits": {"north": "road_north", "east": "khariel", "south": "brumak", "west": "narevia"},
    },
    "road_north": {
        "name": "Camino del Norte",
        "description": (
            "[PLACEHOLDER] Un camino que conecta Vaisgard con Valdren. "
            "(Descripcion pendiente del Historiador.)"
        ),
        "exits": {"south": "vaisgard", "north": "valdren"},
    },
    "valdren": {
        "name": "Valdren",
        "description": (
            "[PLACEHOLDER] Pueblo de inicio de los Humanos. (Descripcion pendiente del Historiador.)"
        ),
        "exits": {"south": "road_north"},
    },
    "khariel": {
        "name": "Khariel",
        "description": (
            "[PLACEHOLDER] Pueblo de inicio de los Felaryn, situado entre montanas. "
            "(Descripcion pendiente del Historiador.)"
        ),
        "exits": {"west": "vaisgard"},
    },
    "brumak": {
        "name": "Brumak",
        "description": (
            "[PLACEHOLDER] Pueblo de inicio de los Dravak. (Descripcion pendiente del Historiador.)"
        ),
        "exits": {"north": "vaisgard"},
    },
    "narevia": {
        "name": "Narevia",
        "description": (
            "[PLACEHOLDER] Pueblo de inicio de los Marevyn. (Descripcion pendiente del Historiador.)"
        ),
        "exits": {"east": "vaisgard", "west": "road_west"},
    },
    "road_west": {
        "name": "Camino del Oeste",
        "description": (
            "[PLACEHOLDER] Un camino que conecta Narevia con Velmora. "
            "(Descripcion pendiente del Historiador.)"
        ),
        "exits": {"east": "narevia", "west": "velmora"},
    },
    "velmora": {
        "name": "Velmora",
        "description": (
            "[PLACEHOLDER] Pueblo de inicio de los Vesperi. (Descripcion pendiente del Historiador.)"
        ),
        "exits": {"east": "road_west"},
    },
}

DIRECTION_LABEL_ES = {"north": "norte", "south": "sur", "east": "este", "west": "oeste"}

# Especie -> pueblo de inicio. Confirmado en vintage-telnet/CONFIRMED_IDEAS.md.
STARTING_ROOM_BY_SPECIES = {
    "humano": "valdren",
    "felaryn": "khariel",
    "dravak": "brumak",
    "marevyn": "narevia",
    "vesperi": "velmora",
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
