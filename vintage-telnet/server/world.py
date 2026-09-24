"""Static world data: rooms and species. No persistent state lives here.

La topologia cardinal v1 sigue siendo un contrato tecnico del primer slice y
no debe interpretarse como mapa canonico completo. Los textos visibles usan
solo hechos ya establecidos en SETTLEMENTS.md, SPECIES.md y NARRATIVE.md.
"""

OPPOSITE_DIRECTION = {"north": "south", "south": "north", "east": "west", "west": "east"}
ALL_DIRECTIONS = ("north", "south", "east", "west")

TOWN_DESCRIPTIONS = {
    "valdren": (
        "Valdren es un pueblo abierto de caminos de tierra, construcciones de madera y piedra "
        "y pequeñas parcelas de cultivo en los Llanos de Edran."
    ),
    "khariel": (
        "Khariel está construido entre las montañas, aprovechando terrazas naturales, "
        "salientes de roca y distintos niveles de altura."
    ),
    "brumak": (
        "Brumak es un asentamiento compacto en una región rocosa protegida del viento, "
        "con espacios y pasajes adaptados a la escala de los Dravak."
    ),
    "narevia": (
        "Narevia se levanta alrededor de un gran cuerpo de agua dulce, con canales, "
        "vegetación abundante y pequeñas islas integradas en el pueblo."
    ),
    "velmora": (
        "Velmora se encuentra en un bosque muy denso donde la luz se reduce incluso durante "
        "el día, unido por senderos y señales discretas."
    ),
}

# Arte por visual_context_id, no por room_id: varias salas de un mismo
# pueblo/zona comparten la misma ilustracion mientras el jugador no cambie
# de contexto (VISUAL_CONTEXT_CANON.md). Los contextos sin fila aqui todavia
# no tienen asset aprobado y describe_room() debe devolver "art": None
# (fallback sobrio) para ellos.
VISUAL_CONTEXT_ART = {
    "zone.valdren": {
        "src": "/assets/locations/valdren.webp",
        "alt": "Vista contextual de Valdren",
        "width": 1536,
        "height": 1024,
    },
    "zone.vaisgard": {
        "src": "/assets/locations/vaisgard.webp",
        "alt": "Vista contextual de Vaisgard",
        "width": 1536,
        "height": 1024,
    },
}

# Excepciones explicitas de VISUAL_CONTEXT_CANON.md ("Mapeo de las salas
# actuales"): salas que NO comparten el contexto de su propio prefijo de
# pueblo, o que no pertenecen a ningun pueblo. Cualquier sala de pueblo que
# no aparezca aqui hereda "zone.<pueblo>" (ver get_visual_context_id), tal
# como el canon autoriza para micro-salas internas futuras.
ROOM_VISUAL_CONTEXT_OVERRIDES = {
    "vaisgard": "zone.vaisgard",
    "road_north": "zone.veyra.road",
    "road_west": "zone.veyra.road",
    "valdren_sendero": "zone.edran.valdren_outskirts",
    "valdren_camino_parcela": "zone.edran.valdren_outskirts",
    "valdren_camino_cerca": "zone.edran.valdren_outskirts",
    "valdren_camino_lindero": "zone.edran.valdren_outskirts",
}

_TOWN_VISUAL_CONTEXT_PREFIXES = ("valdren", "khariel", "brumak", "narevia", "velmora")


def get_visual_context_id(room_id):
    """Resuelve el visual_context_id autoritativo de una sala segun
    VISUAL_CONTEXT_CANON.md. No infiere nada a partir de nombres o
    descripcion; solo usa room_id como clave estructurada, igual que el
    resto de los datos de mundo en este archivo."""
    override = ROOM_VISUAL_CONTEXT_OVERRIDES.get(room_id)
    if override:
        return override
    for prefix in _TOWN_VISUAL_CONTEXT_PREFIXES:
        if room_id == prefix or room_id.startswith(f"{prefix}_"):
            return f"zone.{prefix}"
    return None


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
                f"La forja o taller de {display_name} es un espacio de trabajo dedicado "
                "a fabricar y reparar armas y herramientas."
            )
        elif kind == "mercado":
            name = f"Mercado de {display_name}"
            description = (
                f"La zona de alimentos y comercio de {display_name} sirve al abastecimiento "
                "cotidiano del pueblo."
            )
        else:
            name = f"Sendero de {display_name}"
            description = (
                f"Un sendero de {display_name} conecta el punto central con los caminos "
                "del asentamiento."
            )
        rooms[room_id] = {
            "name": name,
            "description": description,
            "exits": {OPPOSITE_DIRECTION[direction]: centro_id},
        }

    rooms[centro_id] = {
        "name": display_name,
        "description": TOWN_DESCRIPTIONS[prefix],
        "exits": centro_exits,
    }
    return rooms


ROOMS = {
    "vaisgard": {
        "name": "Vaisgard",
        "description": (
            "Vaisgard es la ciudad principal del mundo conocido y no pertenece "
            "exclusivamente a ninguna de las cinco especies."
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
        "description": "Un camino transitado entre asentamientos del mundo conocido.",
        "exits": {"south": "vaisgard", "north": "valdren_centro"},
    },
    "road_west": {
        "name": "Camino del Oeste",
        "description": "Un camino transitado entre asentamientos del mundo conocido.",
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

# --- VT-NAR-003 "El lindero roto" -- microaventura piloto (NARRATIVE.md) ---
# El sendero tecnico de Valdren representa el camino de salida
# del pueblo; se reemplaza su descripcion generica por el texto real de
# apertura de la microaventura y se extiende hacia el oeste con las tres
# ubicaciones nuevas que pide NARRATIVE.md. Ningun otro pueblo/sala cambia.
ROOMS["valdren_sendero"] = {
    "name": "Sendero de Valdren",
    "description": (
        "Las ultimas casas de Valdren quedan a tu espalda. Delante, el camino de "
        "tierra pasa entre parcelas y cercas bajas. El aire trae olor a tierra "
        "removida y vegetacion cortada. Todavia se oyen voces y trabajo desde el "
        "pueblo."
    ),
    "exits": {"east": "valdren_centro", "west": "valdren_camino_parcela"},
}
ROOMS["valdren_camino_parcela"] = {
    "name": "Parcela removida",
    "description": (
        "Junto al sendero hay varios tallos mordidos casi a ras del suelo. "
        "Pequenos monticulos de tierra rompen la linea de una parcela. Algo se "
        "mueve un instante entre las plantas y vuelve a desaparecer."
    ),
    "exits": {"east": "valdren_sendero", "west": "valdren_camino_cerca"},
}
ROOMS["valdren_camino_cerca"] = {
    "name": "Cerca del rastrojo",
    "description": (
        "El camino se estrecha junto a una cerca. Entre restos secos de cultivo "
        "ves un surco corto y varias raices expuestas. Una pua rigida yace en la "
        "tierra."
    ),
    "exits": {"east": "valdren_camino_parcela", "west": "valdren_camino_lindero"},
}
ROOMS["valdren_camino_lindero"] = {
    "name": "El lindero roto",
    "description": (
        "Mas adelante, dos postes de una cerca estan quebrados hacia afuera. El "
        "barro conserva depresiones profundas. En este tramo no ves los pequenos "
        "movimientos entre cultivos que acompanaban el camino hasta ahora."
    ),
    "exits": {"east": "valdren_camino_cerca"},
}

# examinar <objetivo> por sala -- las claves se comparan normalizadas
# (minusculas, sin acentos; ver app.py _normalize).
ROOM_EXAMINE_TARGETS = {}
ROOM_EXAMINE_TARGETS["valdren_camino_parcela"] = {
    "tallos": (
        "Los tallos estan mordidos casi a ras del suelo, en un angulo limpio. No "
        "es viento ni una herramienta: algo pequeno ha estado comiendo aqui."
    ),
    "monticulos": (
        "Los monticulos de tierra son recientes y estan huecos por dentro: la "
        "entrada de una madriguera poco profunda."
    ),
}
ROOM_EXAMINE_TARGETS["valdren_camino_cerca"] = {
    "pua": (
        "Es dura y termina en una punta gastada. No parece una herramienta ni "
        "una astilla de la cerca."
    ),
}
ROOM_EXAMINE_TARGETS["valdren_camino_lindero"] = {
    "cerca": (
        "La madera no esta podrida. Algo la forzo con suficiente violencia para "
        "partirla y seguir adelante."
    ),
    "huellas": (
        "Las marcas son mucho mas profundas y anchas que las de las criaturas "
        "pequenas que has visto cerca de Valdren."
    ),
}

# Encuentro posible por sala (id de vintage-telnet/server/creatures.py). El
# jugador decide si combate, evalua o sigue de largo -- la criatura nunca
# ataca primero (ver creatures.py, docstring).
ROOM_ENCOUNTER = {
    "valdren_camino_parcela": "mordelinde",
    "valdren_camino_cerca": "espinajo_rastrojo",
}

# Descubrimientos de la microaventura (GAMEPLAY.md 22.7). nivel_referencia
# se usa solo para calcular la XP, no se muestra al jugador.
DISCOVERIES = {
    "senales_mordelinde": {
        "category": "descubrimiento_significativo",
        "reference_level": 1,
        "message": "Reconoces las senales de un Mordelinde en los alrededores de Valdren.",
    },
    "lindero_roto": {
        "category": "descubrimiento_mayor",
        "reference_level": 1,
        "message": "Comprendes que una criatura mucho mayor que las que conoces atraveso este lindero.",
    },
    "regreso_valdren_lindero": {
        "category": "hito_narrativo_menor",
        "reference_level": 1,
        "message": "Vuelves a Valdren sabiendo leer las senales del camino que dejaste atras.",
    },
}

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
        "blurb": (
            "Más pequeños y compactos que un Humano adulto, con zonas de piel endurecida de "
            "aspecto mineral; se desenvuelven especialmente bien en espacios compactos."
        ),
    },
    {
        "id": "marevyn",
        "name": "Marevyn",
        "blurb": (
            "Altos y estilizados, con escamas parciales y adaptación natural al agua dulce "
            "y los humedales; nadan y controlan la respiración mejor que un Humano."
        ),
    },
    {
        "id": "vesperi",
        "name": "Vesperi",
        "blurb": (
            "Adaptados a la baja luz, con ojos muy grandes, postura ligeramente recogida, "
            "oído sensible y orientación mediante señales sutiles."
        ),
    },
]

SPECIES_IDS = tuple(s["id"] for s in SPECIES)

# Clases base confirmadas (Issue #112). Nombres y orientacion copiados de
# vintage-telnet/CONFIRMED_IDEAS.md; GAMEPLAY.md 2: la clase inicial orienta
# el desarrollo pero no encierra permanentemente al personaje. No se listan
# poderes ni ventajas numericas: todavia no estan definidos.
CLASSES = [
    {"id": "arcano", "name": "Arcano",
     "blurb": "Camino de la magia. Comienza con una varita que más adelante podrá dar paso a instrumentos mayores."},
    {"id": "juramentado", "name": "Juramentado",
     "blurb": "Combate directo con espadas medianas o pesadas."},
    {"id": "sombra", "name": "Sombra",
     "blurb": "Sigilo, movimiento discreto, ataques sorpresivos y armas ligeras como cuchillos o puñales."},
    {"id": "artifice", "name": "Artífice",
     "blurb": "Arco, herramientas, construcción, reparación y fabricación."},
]

CLASS_IDS = tuple(c["id"] for c in CLASSES)


def get_room(room_id):
    return ROOMS.get(room_id)


def get_starting_room_for_species(species_id):
    return STARTING_ROOM_BY_SPECIES.get(species_id, "vaisgard")


def get_examine_text(room_id, normalized_target):
    return ROOM_EXAMINE_TARGETS.get(room_id, {}).get(normalized_target)


def get_room_encounter(room_id):
    return ROOM_ENCOUNTER.get(room_id)


def get_discovery(key):
    return DISCOVERIES.get(key)


# Hora del día y clima (Issue #138, petición directa de Javier). La pantalla
# ya tiene su espacio en la barra de lugar; QUÉ horas y climas existen, cómo
# cambian (reloj real, reloj de juego, por zona, al azar...) y si afectan al
# juego lo deciden Jugabilidad y Narrador. Mientras no lo definan, no hay
# ambiente y la barra no muestra nada: no se inventa ningún estado.
#
# Contrato: cada campo es None o {"label": texto visible, "icon": clave}. Las
# claves de icono disponibles en la interfaz son AMBIENT_ICONS; un icono
# desconocido se muestra solo como texto.
AMBIENT_ICONS = ("sol", "luna", "amanecer", "atardecer", "nube", "lluvia", "niebla", "nieve", "tormenta", "viento")


def get_ambient(room_id):
    """Ambiente visible de una sala: {"time_of_day": ..., "weather": ...}.
    Punto único que Jugabilidad/Narrador llenarán; hoy siempre vacío."""
    return {"time_of_day": None, "weather": None}


# Minimapa (navegación, Issue #135): coordenadas de rejilla para cada sala,
# derivadas solo de las salidas reales (norte = y-1, este = x+1...). Se calculan
# una vez sobre el mundo completo para que la posición de una sala no cambie
# según lo que el jugador haya descubierto; la API solo entrega las visitadas.
_GRID_STEP = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
_MAP_LAYOUT = None


def map_layout():
    """{room_id: (x, y)} por recorrido en anchura desde Vaisgard. Si dos salas
    caen en la misma celda (mundo no perfectamente cuadriculado) la segunda
    se desplaza a la celda libre más cercana en esa misma dirección."""
    global _MAP_LAYOUT
    if _MAP_LAYOUT is not None:
        return _MAP_LAYOUT
    start = "vaisgard" if "vaisgard" in ROOMS else next(iter(ROOMS))
    layout = {start: (0, 0)}
    taken = {(0, 0)}
    queue = [start]
    while queue:
        room_id = queue.pop(0)
        x, y = layout[room_id]
        for direction, destination in ROOMS[room_id]["exits"].items():
            if destination in layout or destination not in ROOMS or direction not in _GRID_STEP:
                continue
            dx, dy = _GRID_STEP[direction]
            cell = (x + dx, y + dy)
            while cell in taken:
                cell = (cell[0] + dx, cell[1] + dy)
            layout[destination] = cell
            taken.add(cell)
            queue.append(destination)
    _MAP_LAYOUT = layout
    return layout


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
    visual_context_id = get_visual_context_id(room_id)
    return {
        "id": room_id,
        "name": room["name"],
        "description": room["description"],
        "exits": [
            {"direction": direction, "label": DIRECTION_LABEL_ES.get(direction, direction)}
            for direction in room["exits"]
        ],
        "others_present": others_present,
        "visual_context_id": visual_context_id,
        "art": VISUAL_CONTEXT_ART.get(visual_context_id),
        "ambient": get_ambient(room_id),
    }
