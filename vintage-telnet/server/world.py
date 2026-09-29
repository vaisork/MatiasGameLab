"""Static world data: rooms and species. No persistent state lives here.

La topologia cardinal v1 sigue siendo un contrato tecnico del primer slice y
no debe interpretarse como mapa canonico completo. Los textos visibles usan
solo hechos ya establecidos en SETTLEMENTS.md, SPECIES.md y NARRATIVE.md.
"""

import time

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
    # Publicados como "approved runtime asset" el 2026-09-23 (commits 6de5885,
    # 0f07a28, 81ed307, c5af42b) en assets/vintage-telnet/locations/.
    "zone.khariel": {
        "src": "/assets/locations/khariel.webp",
        "alt": "Vista contextual de Khariel",
        "width": 1536,
        "height": 1024,
    },
    "zone.brumak": {
        "src": "/assets/locations/brumak.webp",
        "alt": "Vista contextual de Brumak",
        "width": 1536,
        "height": 1024,
    },
    "zone.narevia": {
        "src": "/assets/locations/narevia.webp",
        "alt": "Vista contextual de Narevia",
        "width": 1536,
        "height": 1024,
    },
    "zone.velmora": {
        "src": "/assets/locations/velmora.webp",
        "alt": "Vista contextual de Velmora",
        "width": 1536,
        "height": 1024,
    },
    # Caminos de la Cuenca de Veyra (Issue #151, aprobado por Dirección de
    # Arte; publicado en la PR #169, SHA-256 dd086367...).
    "zone.veyra.road": {
        "src": "/assets/locations/road-veyra.webp",
        "alt": "Camino de la Cuenca de Veyra",
        "width": 1536,
        "height": 1024,
    },
    # Issue #151, arte aprobado por Dirección y publicado en PR #174.
    "zone.edran.valdren_outskirts": {
        "src": "/assets/locations/valdren-outskirts.webp",
        "alt": "Alrededores de Valdren: parcelas, cercas bajas y caminos de tierra",
        "width": 1672,
        "height": 941,
    },
    # Issue #548 (APPROVED-BINDINGS-01), mapping validado en
    # REGIONAL_VISUAL_MAPPING_CANON.md (#203/#215/#487). Publicado en PR #255.
    "zone.hoshai.paso_alto": {
        "src": "/assets/locations/hoshai-paso-alto.webp",
        "alt": "Paso alto interior de Hoshai: escalones y roca próxima",
        "width": 1672,
        "height": 941,
    },
    # Issue #548 (APPROVED-BINDINGS-01), mapping validado en
    # REGIONAL_VISUAL_MAPPING_CANON.md (#203/#215/#487). Publicado en PR #259.
    "zone.lethra.canal_bajo_islas": {
        "src": "/assets/locations/lethra-canal-bajo-islas.webp",
        "alt": "Canal bajo entre islas de Lethra",
        "width": 1670,
        "height": 942,
    },
}

# Excepciones explicitas de VISUAL_CONTEXT_CANON.md ("Mapeo de las salas
# actuales"): salas que NO comparten el contexto de su propio prefijo de
# pueblo, o que no pertenecen a ningun pueblo. Cualquier sala de pueblo que
# no aparezca aqui hereda "zone.<pueblo>" (ver get_visual_context_id), tal
# como el canon autoriza para micro-salas internas futuras.
ROOM_VISUAL_CONTEXT_OVERRIDES = {
    "vaisgard": "zone.vaisgard",
    "valdren_sendero": "zone.edran.valdren_outskirts",
    "valdren_camino_parcela": "zone.edran.valdren_outskirts",
    "valdren_camino_cerca": "zone.edran.valdren_outskirts",
    "valdren_camino_lindero": "zone.edran.valdren_outskirts",
    "valdren_lindero_tres_piedras": "zone.edran.valdren_outskirts",
    "valdren_camino_hundido": "zone.edran.valdren_outskirts",
    "valdren_cobertizos_viejos": "zone.edran.valdren_outskirts",
    "valdren_cruce_cercas": "zone.edran.valdren_outskirts",
    "valdren_campo_rastrojo": "zone.edran.valdren_outskirts",
    "valdren_zanja_vieja": "zone.edran.valdren_outskirts",
    "valdren_parcelas_exteriores": "zone.edran.valdren_outskirts",
    "valdren_pastos_altos": "zone.edran.valdren_outskirts",
    "valdren_arbol_descanso": "zone.edran.valdren_outskirts",
    "valdren_campos_sin_cerca": "zone.edran.valdren_outskirts",
    "valdren_vado_menor": "zone.edran.valdren_outskirts",
    # Issue #548: mapping recomendado en REGIONAL_VISUAL_MAPPING_CANON.md.
    "alto_escalones": "zone.hoshai.paso_alto",
    "alto_garganta": "zone.hoshai.paso_alto",
    "alto_cruce_alturas": "zone.hoshai.paso_alto",
    "juncos_agua_entre_caminos": "zone.lethra.canal_bajo_islas",
    "juncos_islas_bajas": "zone.lethra.canal_bajo_islas",
    "juncos_canal_ancho": "zone.lethra.canal_bajo_islas",
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


def _build_town(prefix, display_name, outward_exits, internal=None):
    """Genera la microzona minima de un pueblo: sala central (con las
    conexiones externas ya definidas) mas forja/mercado/sendero en las
    direcciones que queden libres, hasta un maximo de 3 salas internas
    (algunos pueblos ya usan 2 direcciones para caminos externos, como
    Narevia, y no les queda lugar para las tres)."""
    centro_id = f"{prefix}_centro"
    centro_exits = dict(outward_exits)
    free_directions = [d for d in ALL_DIRECTIONS if d not in outward_exits]

    internal_kinds = ["forja", "mercado", "sendero"]
    # `internal` fija a mano [(direccion, tipo), ...] cuando el reparto
    # automatico chocaria con una ruta (Valdren: su sendero ES la ruta).
    placements = internal if internal is not None else list(zip(free_directions, internal_kinds))
    rooms = {}
    for direction, kind in placements:
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
        # Las cinco rutas se enlazan mas abajo (link_route).
        "exits": {},
    },
}

# Cada pueblo de inicio confirmado recibe la misma microzona minima:
# punto central + forja + mercado (+ sendero cuando queda una cuarta
# direccion libre), suficiente para probar N/S/E/O dentro del pueblo.
# Orientacion segun REGIONS.md y el mapa regional aprobado (Issue #120): cada
# pueblo sale por el lado que mira hacia Vaisgard. Khariel al norte, Brumak
# al oeste, Velmora al este, Valdren al suroeste y Narevia al sureste.
ROOMS.update(_build_town("valdren", "Valdren", {"north": "valdren_sendero"},
                         internal=[("west", "forja"), ("east", "mercado")]))
ROOMS.update(_build_town("khariel", "Khariel", {"south": "alto_terrazas"}))
ROOMS.update(_build_town("brumak", "Brumak", {"east": "piedra_patio_exterior"}))
ROOMS.update(_build_town("narevia", "Narevia", {"north": "juncos_plataformas"}))
ROOMS.update(_build_town("velmora", "Velmora", {"west": "sombra_borde"}))

# --- VT-NAR-003 "El lindero roto" -- microaventura piloto (NARRATIVE.md) ---
# El sendero tecnico de Valdren representa el camino de salida
# del pueblo; se reemplaza su descripcion generica por el texto real de
# apertura de la microaventura y se extiende hacia el oeste con las tres
# ubicaciones nuevas que pide NARRATIVE.md. Ningun otro pueblo/sala cambia.
ROOMS["valdren_sendero"] = {
    "name": "Sendero de Valdren",
    "description": (
        "Las últimas casas de Valdren quedan a tu espalda. Delante, el camino de "
        "tierra pasa entre parcelas y cercas bajas. El aire trae olor a tierra "
        "removida y vegetación cortada. Todavía se oyen voces y trabajo desde el "
        "pueblo."
    ),
    "exits": {"east": "valdren_centro", "west": "valdren_camino_parcela"},
}
ROOMS["valdren_camino_parcela"] = {
    "name": "Parcela removida",
    "description": (
        "Junto al sendero hay varios tallos mordidos casi a ras del suelo. "
        "Pequeños montículos de tierra rompen la línea de una parcela. Algo se "
        "mueve un instante entre las plantas y vuelve a desaparecer."
    ),
    "exits": {"east": "valdren_sendero", "west": "valdren_camino_cerca"},
}
ROOMS["valdren_camino_cerca"] = {
    "name": "Cerca del rastrojo",
    "description": (
        "El camino se estrecha junto a una cerca. Entre restos secos de cultivo "
        "ves un surco corto y varias raíces expuestas. Una púa rígida yace en la "
        "tierra."
    ),
    "exits": {"east": "valdren_camino_parcela", "west": "valdren_camino_lindero"},
}
ROOMS["valdren_camino_lindero"] = {
    "name": "El lindero roto",
    "description": (
        "Más adelante, dos postes de una cerca están quebrados hacia afuera. El "
        "barro conserva depresiones profundas. En este tramo no ves los pequeños "
        "movimientos entre cultivos que acompanaban el camino hasta ahora."
    ),
    "exits": {"east": "valdren_camino_cerca", "west": "valdren_lindero_tres_piedras"},
}

# Camino de los Campos -- bloque 1 (A1-A10) de vintage-telnet/NARRATIVE_ROUTES.md
# (Narrador, #163/#164). El lindero roto funciona como A1 "Parcelas interiores"
# y queda intacto con sus dos encuentros fijos. Las descripciones siguen solo
# lo que dice el documento para cada estación; son salas de tránsito: no
# agregan encuentros fijos, recompensas, balance ni reglas. Iniciado por el
# Junior en la PR #171 y completado aquí. A11-A18 (hasta Vaisgard) es el
# bloque 2 del handoff.
ROUTE_A_BLOCK_1 = {
    "valdren_lindero_tres_piedras": {
        "name": "Lindero de las tres piedras",
        "description": (
            "Tres piedras grandes, gastadas y reutilizadas, marcan una división más "
            "antigua que las cercas de alrededor. El camino sigue entre parcelas menos "
            "juntas y las voces de Valdren ya llegan débiles a tu espalda."
        ),
        "exits": {"east": "valdren_camino_lindero", "west": "valdren_camino_hundido"},
    },
    "valdren_camino_hundido": {
        "name": "Camino hundido",
        "description": (
            "Generaciones de paso han dejado esta franja de tierra endurecida un poco "
            "más baja que los campos de ambos lados. Hay hierba, surcos viejos y "
            "reparaciones hechas en épocas distintas."
        ),
        "exits": {"east": "valdren_lindero_tres_piedras", "west": "valdren_cobertizos_viejos"},
    },
    "valdren_cobertizos_viejos": {
        "name": "Cobertizos viejos",
        "description": (
            "Varios cobertizos bajos se levantan junto al camino. Algunos siguen en "
            "uso; otros conservan tablas y apoyos reemplazados muchas veces. Es un "
            "buen lugar para detenerse un momento antes del campo abierto."
        ),
        "exits": {"east": "valdren_camino_hundido", "west": "valdren_cruce_cercas"},
    },
    "valdren_cruce_cercas": {
        "name": "Cruce de las cercas",
        "description": (
            "Dos cercas se separan y dejan un cruce ancho de tierra. Un sendero menor "
            "se desvía hacia las parcelas exteriores; el camino principal conserva su "
            "dirección hacia Vaisgard."
        ),
        "exits": {"east": "valdren_cobertizos_viejos", "west": "valdren_campo_rastrojo",
                  "north": "valdren_parcelas_exteriores"},
    },
    "valdren_parcelas_exteriores": {
        "name": "Parcelas exteriores",
        "description": (
            "El sendero menor termina entre parcelas alejadas del pueblo. No lleva a "
            "ningún otro lugar: sirve a quienes trabajan estas tierras. Para seguir "
            "viaje hay que volver al cruce."
        ),
        "exits": {"south": "valdren_cruce_cercas"},
    },
    "valdren_campo_rastrojo": {
        "name": "Campo de rastrojo",
        "description": (
            "Los cultivos continuos quedan atrás. Rastrojo, hierba y tierras en "
            "descanso se alternan junto a un camino todavía claro. Ya casi no hay "
            "construcciones y el horizonte sigue abierto."
        ),
        "exits": {"east": "valdren_cruce_cercas", "west": "valdren_zanja_vieja"},
    },
    "valdren_zanja_vieja": {
        "name": "La zanja vieja",
        "description": (
            "Una zanja de drenaje acompaña el camino durante un tramo. No es una "
            "defensa: sus bordes muestran arreglos de piedra, tierra y madera hechos "
            "en momentos distintos."
        ),
        "exits": {"east": "valdren_campo_rastrojo", "west": "valdren_arbol_descanso"},
    },
    "valdren_arbol_descanso": {
        "name": "Árbol del descanso",
        "description": (
            "Un árbol solitario da sombra a un ensanche de tierra apisonada donde los "
            "viajeros suelen detenerse. No es un santuario, solo un lugar práctico que "
            "todos conocen. Valdren ya quedó atrás."
        ),
        "exits": {"east": "valdren_zanja_vieja", "west": "valdren_campos_sin_cerca"},
    },
    "valdren_campos_sin_cerca": {
        "name": "Campos sin cerca",
        "description": (
            "Siguen los Llanos de Edran, pero ya no hay cercas continuas. Hierba alta, "
            "parcelas abandonadas o en descanso y huellas de tránsito cruzan el campo."
        ),
        "exits": {"east": "valdren_arbol_descanso", "west": "valdren_vado_menor"},
    },
    "valdren_vado_menor": {
        "name": "Vado menor",
        "description": (
            "Un arroyo pequeño obliga al camino a estrecharse. Piedras colocadas a mano "
            "y reparaciones sencillas muestran que esta ruta importa a quienes la usan."
        ),
        "exits": {"east": "valdren_campos_sin_cerca"},
    },
}
ROOMS.update(ROUTE_A_BLOCK_1)

# Ramal opcional de Edran para la prueba de amenaza regional superior (Cornalomo,
# Issue #213 / DEATH-01). Claramente fuera del recorrido obligatorio a Vaisgard;
# sale al este desde el Cruce de las cercas hacia campos altos.
ROOMS["valdren_pastos_altos"] = {
    "name": "Pastos altos",
    "description": (
        "El terreno asciende hacia una zona de pasto áspero y matorral fuera de las "
        "parcelas de labor. Cercas partidas a gran altura, árboles jóvenes con la "
        "corteza raspada y huellas hondas en la tierra húmeda marcan el paso de "
        "una bestia pesada. No se oye fauna menor."
    ),
    "exits": {"west": "valdren_cruce_cercas"},
}

# Salas marcadas como "hábitat dinámico" en NARRATIVE_ROUTES.md. Solo dicen
# DÓNDE puede aparecer fauna aleatoria (encounters.py, Issue #160); QUÉ
# criatura vive en cada hábitat lo define Historia/Narrativa en #166. Nada
# aparece hasta que exista un pool aprobado.
DYNAMIC_HABITAT_ROOMS = {
    "valdren_camino_hundido": "edran_campos",       # A3
    "valdren_parcelas_exteriores": "edran_campos",  # A5, ramal exterior
    "valdren_campo_rastrojo": "edran_campos",       # A6
    "valdren_campos_sin_cerca": "edran_campos",     # A9
}


def habitat_rooms(habitat):
    """Salas de un hábitat dinámico, para armar pools de encounters.py."""
    return {room_id for room_id, value in DYNAMIC_HABITAT_ROOMS.items() if value == habitat}

# --- Las Cinco Rutas (NARRATIVE_ROUTES.md, Narrador #163/#164) ------------------
# Cada pueblo llega a Vaisgard por un camino con estaciones narrativas en vez de
# un salto. Los textos siguen solo lo que el documento dice de cada estación;
# el Narrador puede reescribirlos sin tocar la estructura. Cada lista va del
# pueblo hacia Vaisgard. Pendiente del documento: ramales laterales (salvo el
# de A5) y los dos trazados de B7/C6/E5, que aquí son un solo camino.
def _route_rooms(specs):
    return {room_id: {"name": name, "description": description, "exits": {}}
            for room_id, name, description in specs}


# Camino de los Campos, A11-A18 (A1-A10 están arriba).
ROUTE_A_BLOCK_2 = [
    ("campos_loma", "Loma de regreso",
     "Desde esta loma suave se ve hacia atrás todo lo recorrido. Valdren ya no domina el paisaje."),
    ("campos_mojon", "Mojón de Veyra",
     "Un mojón de piedra acompaña el camino. No es una frontera: el terreno empieza a ondular y "
     "aparecen obras de mantenimiento para el tránsito hacia la Cuenca."),
    ("campos_camino_compartido", "Camino compartido",
     "Hay más huellas de carros y caminantes, y materiales que no vienen solo de Edran. Por aquí "
     "pasa gente de otros lugares."),
    ("campos_colinas", "Primeras colinas de Veyra",
     "El horizonte llano se pierde entre colinas. Estás dejando atrás los Llanos de Edran."),
    ("campos_almacen", "Almacén de ruta",
     "Un antiguo almacén de alimentos para viajeros fue reparado y se usa otra vez."),
    ("campos_vista_vaisgard", "Vista lejana de Vaisgard",
     "A lo lejos aparece Vaisgard por primera vez, levantada en capas. Todavía falta camino."),
    ("campos_camino_exterior", "Camino exterior de la Cuenca",
     "Más viajeros, reparaciones recientes y cruces pequeños. La ciudad ya se nota en el paisaje."),
    ("campos_acceso", "Acceso de los Campos",
     "El Camino de los Campos entra en los alrededores de Vaisgard."),
]

ROUTE_B = [  # Camino Alto: Khariel -> Vaisgard
    ("alto_terrazas", "Terrazas habitadas",
     "Los últimos espacios cotidianos de Khariel se escalonan sobre la roca. Los muros de apoyo "
     "muestran reparaciones de generaciones distintas."),
    ("alto_mirador", "Mirador antiguo",
     "Un punto de observación más antiguo que parte del camino actual. Desde aquí se ve el trazado "
     "antes de recorrerlo."),
    ("alto_anclajes", "Anclajes del puente viejo",
     "Unos huecos en la piedra recuerdan un paso que ya fue sustituido. El camino de ahora es "
     "seguro y va por otro lado."),
    ("alto_escalones", "Escalones del viento",
     "El sendero cambia de nivel entre escalones de roca. El viento domina el sonido y Khariel "
     "queda atrás."),
    ("alto_terraza_abandonada", "Terraza abandonada",
     "Una plataforma antigua ya no tiene uso cotidiano. Sus bordes gastados cuentan que alguien la "
     "trabajó hace mucho."),
    ("alto_garganta", "Garganta clara",
     "Un paso estrecho entre paredes de roca. Hacia adelante se ve lejos; a los lados casi no hay "
     "espacio."),
    ("alto_cruce_alturas", "Cruce de alturas",
     "El camino rodea un desnivel. Hay huellas de más de un trazado y todos vuelven a encontrarse "
     "más adelante."),
    ("alto_puente_viento", "Puente de viento",
     "El puente cruza un tramo expuesto. El viento lo hace sonar y la vista se abre en todas "
     "direcciones. Es difícil olvidar este lugar."),
    ("alto_pinar", "Pinar disperso",
     "La roca se alterna con árboles de montaña. El aire huele distinto y el suelo se vuelve más "
     "blando."),
    ("alto_descenso", "Descenso largo",
     "Los senderos bajan uno tras otro. Khariel ya no se ve desde aquí."),
    ("alto_agua_fria", "Agua fría",
     "Una corriente estrecha baja de la sierra. Es un buen lugar para detenerse un momento."),
    ("alto_ultimo_risco", "Último risco",
     "Las rocas empiezan a abrirse y, más abajo, se adivina la Cuenca."),
    ("alto_camino_falda", "Camino de falda",
     "El camino corre por la falda de la sierra. Sus reparaciones sirven a viajeros de todos los "
     "tamaños, no solo a los Felaryn."),
    ("alto_piedra_cinco_marcas", "Piedra de las cinco marcas",
     "Una piedra de mantenimiento del camino lleva cinco marcas. Señala que por aquí pasan viajeros "
     "de todas las rutas."),
    ("alto_cuenca_norte", "Cuenca norte",
     "El terreno baja con suavidad. Estás entrando en la Cuenca de Veyra."),
    ("alto_vista_vaisgard", "Vista norte de Vaisgard",
     "Abajo, a lo lejos, se ven las capas de Vaisgard. Todavía falta camino para llegar."),
    ("alto_aproximacion", "Aproximación del Camino Alto",
     "Cada vez hay más viajeros y el camino se ensancha hacia los accesos de la ciudad."),
]

ROUTE_C = [  # Camino de Piedra: Brumak -> Vaisgard
    ("piedra_patio_exterior", "Patio exterior de Brumak",
     "Un patio amplio, preparado para visitantes más grandes que los Dravak. Aquí termina el pueblo "
     "y empieza el camino."),
    ("piedra_pared_anclajes", "Pared de los anclajes",
     "La roca conserva huellas de estructuras de trabajo muy antiguas."),
    ("piedra_paso_corto", "Paso corto",
     "El camino se aprieta entre dos paredes de piedra durante un tramo breve."),
    ("piedra_patio_abierto", "Patio de piedra abierto",
     "Brumak queda atrás. El espacio se abre y el viento gana fuerza."),
    ("piedra_primer_monton", "Primer montón de ruta",
     "Piedras apiladas por viajeros marcan el camino. Sirven para orientarse cuando se ve poco."),
    ("piedra_hendiduras", "Hendiduras paralelas",
     "Dos corredores de roca corren uno junto al otro, en la misma dirección."),
    ("piedra_pared_partida", "Pared partida",
     "Una enorme pared de roca partida se levanta junto al camino. Se ve desde muchos puntos de los "
     "Pedrales."),
    ("piedra_abrigo_viento", "Abrigo del viento",
     "Una hondonada protegida del viento sirve de pausa a los viajeros. Hay rastros de otros que "
     "descansaron aquí."),
    ("piedra_meseta_baja", "Meseta baja",
     "El horizonte se abre sobre una meseta rocosa y el viento pega de frente."),
    ("piedra_cruce_montones", "Cruce de montones",
     "Varios montones de piedra marcan caminos distintos. Hay que fijarse cuál sigue la ruta "
     "principal."),
    ("piedra_cavidades", "Cavidades superficiales",
     "Unas cavidades poco profundas se abren en la roca. Recuerdan cómo los primeros Dravak "
     "aprovecharon el terreno."),
    ("piedra_clara", "Piedra clara",
     "La roca cambia a un tono más claro. Es una buena señal de cuánto has avanzado."),
    ("piedra_ultimo_corredor", "Último corredor",
     "Las paredes de piedra bajan y el viento cambia."),
    ("piedra_suelo_quebrado", "Suelo quebrado",
     "Los Pedrales de Korven empiezan a quedar atrás y el terreno se vuelve más abierto."),
    ("piedra_entrada_veyra", "Entrada oeste de Veyra",
     "Aparecen caminos de viajeros y reparaciones hechas con materiales de distintos lugares."),
    ("piedra_vista_vaisgard", "Vista occidental de Vaisgard",
     "Por primera vez se ve la ciudad a lo lejos."),
    ("piedra_aproximacion", "Aproximación de Piedra",
     "Último tramo del camino antes de entrar a Vaisgard."),
]

ROUTE_D = [  # Camino de los Juncos: Narevia -> Vaisgard
    ("juncos_plataformas", "Plataformas de Narevia",
     "Las últimas plataformas del pueblo se asoman al agua. Más allá empieza el Camino de los Juncos."),
    ("juncos_postes", "Postes de las aguas",
     "Unos postes llevan marcas de hasta dónde llegó el agua en distintas generaciones."),
    ("juncos_pasarela_antigua", "Pasarela antigua",
     "Junto a una pasarela nueva quedan las bases de otra más vieja. El pueblo cambia con el agua."),
    ("juncos_isla_refugio", "Isla de refugio",
     "Una isla pequeña conserva restos de un uso antiguo, de temporada."),
    ("juncos_juncal", "Juncal abierto",
     "Los juncos crecen altos a los lados. Narevia ya no domina el paisaje."),
    ("juncos_paso_raices", "Paso de raíces",
     "El sendero va elevado sobre raíces, entre vegetación y barro."),
    ("juncos_embarcadero", "Embarcadero viejo",
     "Un embarcadero antiguo recuerda una ruta por agua que todavía se conoce, aunque ha cambiado."),
    ("juncos_agua_entre_caminos", "Agua entre caminos",
     "El camino de tierra se interrumpe entre el agua. Hay que buscar por dónde seguir."),
    ("juncos_pasarela_larga", "Pasarela larga",
     "Una pasarela larga cruza el agua. A los lados solo hay agua y casi ninguna señal del pueblo."),
    ("juncos_islas_bajas", "Islas bajas",
     "Varias islas pequeñas dibujan caminos distintos con la vista."),
    ("juncos_canal_ancho", "Canal ancho",
     "Un canal ancho obliga a bordear el agua antes de recuperar la dirección."),
    ("juncos_ultimos", "Últimos juncos densos",
     "Los juncos más espesos quedan atrás. Estás saliendo del corazón de Lethra."),
    ("juncos_suelo_firme", "Suelo firme",
     "Por primera vez en mucho rato, el camino es de tierra firme."),
    ("juncos_corrientes", "Corrientes hacia Veyra",
     "Pequeños canales acompañan el camino hacia la Cuenca."),
    ("juncos_entrada_veyra", "Entrada sureste de Veyra",
     "Cada vez hay más huellas de viajeros de distintos lugares."),
    ("juncos_vista_vaisgard", "Vista de Vaisgard entre aguas",
     "Entre aguas menores se ve la ciudad a lo lejos. Todavía hay que llegar."),
    ("juncos_aproximacion", "Aproximación de los Juncos",
     "Último tramo del camino hacia los accesos de la ciudad."),
]

ROUTE_E = [  # Camino de la Sombra Verde: Velmora -> Vaisgard
    ("sombra_borde", "Borde habitado de Velmora",
     "Las casas de Velmora se funden con raíces y troncos que sirven de referencia. Aquí empieza el "
     "Camino de la Sombra Verde."),
    ("sombra_tronco", "Tronco de las reparaciones",
     "Un tronco lleva marcas de distintas épocas. Es una señal útil que se ha cuidado mucho tiempo."),
    ("sombra_raices_cruzadas", "Raíces cruzadas",
     "Las raíces se cruzan sobre el sendero. El camino ya no parece construido."),
    ("sombra_claro_pequeno", "Claro pequeño",
     "Un claro pequeño deja mirar atrás. Las copas ya ocultan casi todo."),
    ("sombra_sendero_doble", "Sendero doble",
     "Dos huellas rodean vegetación espesa y vuelven a unirse más adelante."),
    ("sombra_niebla_baja", "Niebla baja",
     "La humedad se queda cerca del suelo y a veces forma una niebla baja. Es un tramo fácil de "
     "reconocer."),
    ("sombra_arbol_caido", "Árbol caído antiguo",
     "Un árbol enorme cayó hace mucho tiempo y el camino lo rodea. En Nhal, la ruta se adapta al "
     "bosque."),
    ("sombra_tres_marcas", "Tres marcas discretas",
     "Tres marcas pequeñas señalan el rumbo. Hay que observar con calma para verlas."),
    ("sombra_claro_escucha", "Claro de escucha",
     "Se sigue viendo poco, pero los sonidos cambian. Es un buen lugar para detenerse."),
    ("sombra_raiz_alta", "Raíz alta",
     "Una raíz enorme se levanta sobre el sendero. Es el punto más reconocible del bosque profundo."),
    ("sombra_bosque_abierto", "Bosque menos cerrado",
     "La luz entra poco a poco entre las copas."),
    ("sombra_hojas_claras", "Sendero de hojas claras",
     "El suelo se cubre de hojas más claras. La salida del bosque está cerca."),
    ("sombra_ultimas_senales", "Últimas señales de Nhal",
     "Las señales en los árboles dejan paso a marcas de camino que usan viajeros de todas partes."),
    ("sombra_entrada_veyra", "Entrada este de Veyra",
     "El terreno se abre al salir del bosque."),
    ("sombra_cruce_viajeros", "Cruce de viajeros",
     "Aquí se juntan muchas huellas de gente que viene de fuera del bosque."),
    ("sombra_vista_vaisgard", "Vista oriental de Vaisgard",
     "Por primera vez aparece la ciudad a lo lejos."),
    ("sombra_aproximacion", "Aproximación de Sombra Verde",
     "Último tramo del camino antes de los accesos de la ciudad."),
]

# Anillo de aproximación (NARRATIVE_ROUTES.md): los caminos del sur se juntan
# antes de la ciudad; ninguna ruta desemboca de golpe en Vaisgard.
APPROACH_SOUTH = [
    ("cuenca_aproximacion_sur", "Aproximación sur de Vaisgard",
     "Aquí se juntan el Camino de los Campos y el Camino de los Juncos antes de entrar a la ciudad. "
     "Viajeros de distintas regiones comparten el paso."),
]

for _specs in (ROUTE_A_BLOCK_2, ROUTE_B, ROUTE_C, ROUTE_D, ROUTE_E, APPROACH_SOUTH):
    ROOMS.update(_route_rooms(_specs))


def _ids(specs):
    return [room_id for room_id, _name, _description in specs]


# Cada cadena va del centro del pueblo a su entrada de Vaisgard. Las
# direcciones son las de cada paso hacia Vaisgard (la vuelta es la opuesta):
# N = norte, S = sur, E = este, O = oeste.
ROUTE_A_CHAIN = (["valdren_centro", "valdren_sendero", "valdren_camino_parcela",
                  "valdren_camino_cerca", "valdren_camino_lindero"]
                 + [room_id for room_id in ROUTE_A_BLOCK_1 if room_id != "valdren_parcelas_exteriores"]
                 + _ids(ROUTE_A_BLOCK_2) + ["cuenca_aproximacion_sur"])
ROUTE_CHAINS = {
    # Valdren (suroeste): sale al norte por El lindero roto y luego serpentea
    # hacia el noreste.
    "A": (ROUTE_A_CHAIN, "NNNN" + "ENEENEENENEENEENEE"),
    "B": (["khariel_centro"] + _ids(ROUTE_B) + ["vaisgard"], "S" * 18),      # Khariel (norte)
    "C": (["brumak_centro"] + _ids(ROUTE_C) + ["vaisgard"], "E" * 18),       # Brumak (oeste)
    # Narevia (sureste): serpentea hacia el noroeste.
    "D": (["narevia_centro"] + _ids(ROUTE_D) + ["cuenca_aproximacion_sur"], "NONONONONONONONONO"),
    "E": (["velmora_centro"] + _ids(ROUTE_E) + ["vaisgard"], "O" * 18),      # Velmora (este)
}
_LETTER_TO_DIRECTION = {"N": "north", "S": "south", "E": "east", "O": "west"}


def link(room_a, direction, room_b):
    ROOMS[room_a]["exits"][direction] = room_b
    ROOMS[room_b]["exits"][OPPOSITE_DIRECTION[direction]] = room_a


def _link_chain(chain, letters):
    assert len(letters) == len(chain) - 1, chain[0]
    for room_id in chain[1:-1]:
        ROOMS[room_id]["exits"] = {}  # las salas de ruta solo tienen las salidas del camino
    for (room_a, room_b), letter in zip(zip(chain, chain[1:]), letters):
        link(room_a, _LETTER_TO_DIRECTION[letter], room_b)


for _chain, _letters in ROUTE_CHAINS.values():
    _link_chain(_chain, _letters)
link("vaisgard", "south", "cuenca_aproximacion_sur")
# Ramal de A5: el sendero menor sale del cruce por un lado libre, de
# preferencia el contrario a Vaisgard (sur u oeste).
ROOMS["valdren_parcelas_exteriores"]["exits"] = {}
link("valdren_cruce_cercas",
     next(d for d in ("south", "west", "north", "east") if d not in ROOMS["valdren_cruce_cercas"]["exits"]),
     "valdren_parcelas_exteriores")
# Ramal opcional a Pastos altos (Cornalomo, #213 / DEATH-01).
ROOMS["valdren_pastos_altos"]["exits"] = {}
link("valdren_cruce_cercas", "east", "valdren_pastos_altos")

# --- Ramales superficiales hacia mazmorras (Issue #430 / PR #429 / #341 #419 #422 #423 #424) ---
# 46 ubicaciones superficiales aprobadas, distribuidas en 5 ramales periféricos.
SURFACE_BRANCH_MAPPING = {
    "MH-01": "mh_01_desvio_acequia",
    "MH-02": "mh_02_bordes_vencidos",
    "MH-03": "mh_03_juncos_partidos",
    "MH-04": "mh_04_piedra_canal",
    "MH-05": "mh_05_terreno_dos_aguas",
    "MH-06": "mh_06_restos_cauce",
    "MH-07": "mh_07_vista_molino",
    "MH-08": "mh_08_rodeo_base",
    "MH-09": "mh_09_plataforma_caida",
    "MH-10": "mh_10_umbral_inferior",
    "GE-01": "ge_01_desvio_grieta",
    "GE-02": "ge_02_terrazas_rotas",
    "GE-03": "ge_03_repisa_viento",
    "GE-04": "ge_04_quiebre_lajas",
    "GE-05": "ge_05_bolsillo_seco",
    "GE-06": "ge_06_fisuras_paralelas",
    "GE-07": "ge_07_grava_fondo",
    "GE-08": "ge_08_ultima_luz_directa",
    "GE-09": "ge_09_boca_inferior",
    "CA-01": "ca_01_desvio_descarte",
    "CA-02": "ca_02_patio_grava",
    "CA-03": "ca_03_plataforma_baja",
    "CA-04": "ca_04_montones_descarte",
    "CA-05": "ca_05_zanja_seca",
    "CA-06": "ca_06_plataforma_alta",
    "CA-07": "ca_07_frente_quebrado",
    "CA-08": "ca_08_paso_bloques",
    "CA-09": "ca_09_cavidad_tras_frente",
    "CQ-01": "cq_01_desvio_agua_lenta",
    "CQ-02": "cq_02_orilla_juncos_bajos",
    "CQ-03": "cq_03_ensanchamiento_claro",
    "CQ-04": "cq_04_raices_ribera",
    "CQ-05": "cq_05_recodo_tronco",
    "CQ-06": "cq_06_paso_raices",
    "CQ-07": "cq_07_orilla_blanda",
    "CQ-08": "cq_08_recodo_sin_vista",
    "CQ-09": "cq_09_estrechamiento_raices_roca",
    "BM-01": "bm_01_desvio_dosel",
    "BM-02": "bm_02_raices_sobre_roca",
    "BM-03": "bm_03_piedra_sotobosque",
    "BM-04": "bm_04_ladera_grava",
    "BM-05": "bm_05_saliente_raices",
    "BM-06": "bm_06_terraza_exterior",
    "BM-07": "bm_07_risco_sombreado",
    "BM-08": "bm_08_antesala_boca",
    "BM-09": "bm_09_boca_rocosa",
}

SURFACE_BRANCH_ANCHORS = {
    "MH": {
        "branch_entry": "mh_01_desvio_acequia",
        "anchor_room": "valdren_vado_menor",
        "direction_from_anchor": "south",
        "corridor": "Camino de la Tierra Húmeda",
    },
    "GE": {
        "branch_entry": "ge_01_desvio_grieta",
        "anchor_room": "alto_terrazas",
        "direction_from_anchor": "west",
        "corridor": "Paso de las Lajas",
    },
    "CA": {
        "branch_entry": "ca_01_desvio_descarte",
        "anchor_room": "piedra_patio_exterior",
        "direction_from_anchor": "south",
        "corridor": "Senda del Viento Bajo",
    },
    "CQ": {
        "branch_entry": "cq_01_desvio_agua_lenta",
        "anchor_room": "juncos_plataformas",
        "direction_from_anchor": "east",
        "corridor": "Ribera Sombría",
    },
    "BM": {
        "branch_entry": "bm_01_desvio_dosel",
        "anchor_room": "sombra_borde",
        "direction_from_anchor": "north",
        "corridor": "Paso del Dosel Alto",
    },
}

SURFACE_BRANCH_THRESHOLDS = (
    "mh_10_umbral_inferior",
    "ge_09_boca_inferior",
    "ca_09_cavidad_tras_frente",
    "cq_09_estrechamiento_raices_roca",
    "bm_09_boca_rocosa",
)

def get_surface_branch_room_id(code: str) -> str | None:
    """Devuelve el room_id técnico para un ID narrativo (ej. 'MH-01')."""
    return SURFACE_BRANCH_MAPPING.get(code)

def get_surface_branch_code(room_id: str) -> str | None:
    """Devuelve el ID narrativo (ej. 'MH-01') a partir del room_id técnico."""
    for code, r_id in SURFACE_BRANCH_MAPPING.items():
        if r_id == room_id:
            return code
    return None

# Definición de salas de los cinco ramales superficiales
BRANCH_MOLINO_HUNDIDO = [
    ("mh_01_desvio_acequia", "Desvío de la acequia",
     "Desde el Camino de la Tierra Húmeda, una acequia antigua se aparta hacia terreno más bajo. "
     "El agua corre lenta entre tierra pisada y vegetación húmeda. El paso principal sigue siendo legible "
     "como referencia a tu espalda."),
    ("mh_02_bordes_vencidos", "Bordes vencidos",
     "La acequia pierde su forma regular. Algunos bordes han cedido y el agua invade depresiones laterales "
     "con barro reciente y tallos doblados, aunque todavía queda suelo firme para avanzar."),
    ("mh_03_juncos_partidos", "Juncos partidos",
     "La vegetación alta empieza a ocultar el recorrido recto. Pasos estrechos se abren entre juncos "
     "y entradas pequeñas al agua, dejando atrás la vista clara de la bifurcación inicial."),
    ("mh_04_piedra_canal", "Piedra del canal",
     "Un bloque de piedra resistente se levanta junto al antiguo canal, parcialmente cubierto por humedad "
     "y vegetación. Es un punto firme y reconocible antes de continuar hacia terreno más bajo."),
    ("mh_05_terreno_dos_aguas", "Terreno de dos aguas",
     "El suelo húmedo se divide brevemente entre una franja más firme y expuesta y otra más corta y cubierta. "
     "Ambos pasos vuelven a reunirse poco después sobre el cauce."),
    ("mh_06_restos_cauce", "Restos del cauce",
     "Aparecen piedras desplazadas, maderas viejas y el borde definido de una infraestructura que alteró el flujo "
     "del agua. La presencia de una construcción mayor se intuye en el terreno."),
    ("mh_07_vista_molino", "Vista del Molino",
     "El terreno se abre lo suficiente para mostrar el conjunto exterior del Molino Hundido: una parte superior "
     "sobre suelo firme y una base tomada por el agua, el barro y la vegetación."),
    ("mh_08_rodeo_base", "Rodeo de la base",
     "El paso bordea la estructura por una franja transitable entre raíces y restos de madera. El agua y los muros "
     "reducen el espacio lateral y cortan las líneas de visión."),
    ("mh_09_plataforma_caida", "Plataforma caída",
     "Un borde elevado de piedra permite observar el sector inferior del molino antes de descender. Hacia atrás queda "
     "el exterior recorrido; delante, la estructura desciende donde el agua y la sombra ganan espacio."),
    ("mh_10_umbral_inferior", "Umbral inferior",
     "Llegas al acceso del nivel inferior del Molino Hundido. El agua lame los peldaños y la entrada se interna en la "
     "oscuridad de la base. Aquí termina el exterior conocido."),
]

BRANCH_GRIETA_ECO_SECO = [
    ("ge_01_desvio_grieta", "Desvío de la grieta",
     "Una fractura natural descendente se abre en la roca expuesta, apartándose del Paso de las Lajas. "
     "La boca superior conserva luz amplia y la conexión con la ruta es inmediata a tu espalda."),
    ("ge_02_terrazas_rotas", "Terrazas rotas",
     "Lajas escalonadas y grava fina forman peldaños irregulares hacia abajo. El viento de la sierra "
     "todavía entra franco entre las paredes de piedra."),
    ("ge_03_repisa_viento", "Repisa del viento",
     "Una repisa lateral amplia ofrece suelo estable junto a fisuras secas. Una última corriente constante "
     "de aire acompaña este tramo antes de que las paredes se estrechen."),
    ("ge_04_quiebre_lajas", "Quiebre de las lajas",
     "Placas de roca inclinadas y huecos laterales rompen la uniformidad del suelo. El paso se vuelve más encajonado "
     "y el crujido de la grava resuena contra la piedra cercana."),
    ("ge_05_bolsillo_seco", "Bolsillo seco",
     "Un ensanchamiento protegido entre paredes altas corta el viento por completo. La luz directa disminuye, "
     "pero la salida superior sigue siendo una referencia legible de regreso."),
    ("ge_06_fisuras_paralelas", "Fisuras paralelas",
     "El corredor se estrecha entre grietas laterales y paredes próximas. La roca conserva hendiduras profundas "
     "y el suelo desciende en un desnivel suave y protegido."),
    ("ge_07_grava_fondo", "Grava de fondo",
     "Una bajada corta de grava suelta se extiende entre repisas bajas. Las paredes de roca encierran el sonido "
     "y la luz exterior llega tamizada desde lo alto."),
    ("ge_08_ultima_luz_directa", "Última luz directa",
     "Un recodo de la grieta donde la abertura superior ilumina una última franja de roca. Mirando hacia atrás "
     "permanece visible la línea de luz que orienta el regreso."),
    ("ge_09_boca_inferior", "Boca inferior",
     "El corte abierto de la grieta se comprime en un estrechamiento pétreo. El aire se vuelve inmóvil, el eco se acorta "
     "y la abertura insinúa una profundidad que continúa bajo la roca."),
]

BRANCH_CANTERA_ABANDONADA = [
    ("ca_01_desvio_descarte", "Desvío de piedra descartada",
     "Montones de piedra acumulada y grava anuncian una excavación antigua que se aparta de la Senda del Viento Bajo. "
     "El borde abierto conserva vegetación residual y la ruta principal a la vista."),
    ("ca_02_patio_grava", "Patio de grava",
     "Una explanada irregular cubierta de polvo y piedra partida se extiende ante las primeras paredes de corte. "
     "El espacio sigue siendo amplio y despejado."),
    ("ca_03_plataforma_baja", "Plataforma baja",
     "Una superficie de trabajo antigua y rebajada ofrece buena visibilidad del terreno. Desde aquí se distingue "
     "con total claridad el desvío de salida hacia la senda."),
    ("ca_04_montones_descarte", "Montones de descarte",
     "Pasajes cortos discurren entre montículos de piedra desechada y polvo seco. Los bloques apilados forman refugios "
     "bajos al pie de la pared."),
    ("ca_05_zanja_seca", "Zanja seca",
     "Un canal de drenaje superficial, seco desde hace tiempo, marca el desnivel entre dos plataformas. El lugar ofrece "
     "una pausa limpia entre las acumulaciones de piedra."),
    ("ca_06_plataforma_alta", "Plataforma alta",
     "Una repisa de trabajo elevada se asoma a un frente de roca más fracturado. El polvo en suspensión y las fisuras "
     "visibles muestran un terreno menos uniforme."),
    ("ca_07_frente_quebrado", "Frente quebrado",
     "El frente bajo de extracción presenta fracturas hondas, bloques caídos y cavidades superficiales al pie del corte mineral."),
    ("ca_08_paso_bloques", "Paso entre bloques",
     "Un corredor irregular serpentea entre bloques desprendidos. Aunque el paso se encajona, el cielo sigue visible "
     "y la plataforma alta sirve de referencia detrás."),
    ("ca_09_cavidad_tras_frente", "Cavidad tras el frente",
     "Una abertura entre grandes bloques marca la transición entre la excavación exterior y una cavidad no explorada. "
     "El aire y la sombra cambian al pie de la piedra."),
]

BRANCH_CANAL_QUIETO = [
    ("cq_01_desvio_agua_lenta", "Desvío de agua lenta",
     "Un brazo del cauce se separa de la Ribera Sombría. La corriente se vuelve notablemente más lenta junto a una orilla "
     "firme que permite seguir el agua hacia la sombra."),
    ("cq_02_orilla_juncos_bajos", "Orilla de juncos bajos",
     "El sendero bordea juncos de ribera y tramos de barro blando. El agua apenas se mueve y el paso permanece transitable "
     "sobre suelo firme."),
    ("cq_03_ensanchamiento_claro", "Ensanchamiento claro",
     "Una bolsa de agua abierta deja espacio a una orilla limpia con buena visibilidad. Hacia atrás aún se reconoce "
     "el punto de bifurcación con la ribera principal."),
    ("cq_04_raices_ribera", "Raíces de ribera",
     "Raíces gruesas se extienden sobre el barro húmedo y se hunden en el canal. La vegetación se cierra sobre la orilla "
     "y abundan los huecos junto al agua."),
    ("cq_05_recodo_tronco", "Recodo del tronco",
     "Un gran tronco caído altera el margen del canal sin cortar el paso. Su madera musgosa sirve como hito reconocible "
     "bajo una sombra cada vez más densa."),
    ("cq_06_paso_raices", "Paso entre raíces",
     "El sendero se estrecha entre contrafuertes leñosos y anclajes vegetales. Las ramas bajas tamizan la luz sobre un "
     "suelo húmedo pero transitable."),
    ("cq_07_orilla_blanda", "Orilla blanda",
     "El barro se vuelve más continuo junto al agua estancada. La cobertura del follaje se espesa y el recorrido exige "
     "pisar con atención sobre las franjas firmes."),
    ("cq_08_recodo_sin_vista", "Recodo sin vista",
     "Una curva cerrada del canal oculta por completo la entrada lejana. No obstante, las raíces y el tronco previo forman "
     "una cadena clara para orientar el regreso."),
    ("cq_09_estrechamiento_raices_roca", "Estrechamiento bajo raíces y roca",
     "El canal y la orilla se comprimen bajo un arco macizo de raíces y piedra. La corriente se desliza hacia una penumbra "
     "cerrada donde termina el exterior."),
]

BRANCH_BOCA_MONTANA = [
    ("bm_01_desvio_dosel", "Desvío bajo el dosel",
     "Un sendero se aparta del Paso del Dosel Alto entre raíces y piedra emergente. El bosque cerrado de hojas y humedad "
     "mantiene a la espalda la referencia del camino principal."),
    ("bm_02_raices_sobre_roca", "Raíces sobre roca",
     "Raíces gruesas cruzan placas inclinadas de piedra bajo una cobertura vegetal tupida. El suelo empieza a ganar inclinación "
     "de forma constante."),
    ("bm_03_piedra_sotobosque", "Piedra del sotobosque",
     "Un claro breve entre troncos y roca ofrece espacio y descanso bajo los árboles. El corredor de bajada hacia la ruta "
     "permanece visible a la espalda."),
    ("bm_04_ladera_grava", "Ladera de grava",
     "La cuesta asciende con mayor decisión. La capa de hojas disminuye y dan paso a grava suelta y piedra de montaña."),
    ("bm_05_saliente_raices", "Saliente de raíces",
     "Un saliente bajo combina raíces expuestas y roca firme, creando huecos protegidos. Es un punto intermedio reconocible "
     "antes de los riscos superiores."),
    ("bm_06_terraza_exterior", "Terraza exterior",
     "Una terraza rocosa se asoma por encima de las copas del bosque. El aire fresco y el espacio abierto recuperan una "
     "vista amplia hacia el exterior."),
    ("bm_07_risco_sombreado", "Risco sombreado",
     "La roca domina el paisaje con menos vegetación, salientes agudos y grietas profundas. El camino bordea la pared en un "
     "tramo frío y expuesto."),
    ("bm_08_antesala_boca", "Antesala de la boca",
     "Un suelo de grava fría se extiende al pie de una pared rocosa dominante. Detrás todavía se distingue la terraza "
     "exterior y la línea superior del bosque."),
    ("bm_09_boca_rocosa", "Boca rocosa",
     "Una abertura natural irregular se interna en la sierra. Paredes y techo de piedra empiezan a cerrar el paso, "
     "marcando el umbral hacia lo profundo de la montaña."),
]

for _branch_specs in (BRANCH_MOLINO_HUNDIDO, BRANCH_GRIETA_ECO_SECO, BRANCH_CANTERA_ABANDONADA, BRANCH_CANAL_QUIETO, BRANCH_BOCA_MONTANA):
    ROOMS.update(_route_rooms(_branch_specs))

# Enlaces bidireccionales de cada ramal superficial
_link_chain([r[0] for r in BRANCH_MOLINO_HUNDIDO], "S" * 9)
_link_chain([r[0] for r in BRANCH_GRIETA_ECO_SECO], "O" * 8)
_link_chain([r[0] for r in BRANCH_CANTERA_ABANDONADA], "S" * 8)
_link_chain([r[0] for r in BRANCH_CANAL_QUIETO], "E" * 8)
_link_chain([r[0] for r in BRANCH_BOCA_MONTANA], "N" * 8)

# Anclaje a las salas vigentes canónicas
link(SURFACE_BRANCH_ANCHORS["MH"]["anchor_room"], SURFACE_BRANCH_ANCHORS["MH"]["direction_from_anchor"], SURFACE_BRANCH_ANCHORS["MH"]["branch_entry"])
link(SURFACE_BRANCH_ANCHORS["GE"]["anchor_room"], SURFACE_BRANCH_ANCHORS["GE"]["direction_from_anchor"], SURFACE_BRANCH_ANCHORS["GE"]["branch_entry"])
link(SURFACE_BRANCH_ANCHORS["CA"]["anchor_room"], SURFACE_BRANCH_ANCHORS["CA"]["direction_from_anchor"], SURFACE_BRANCH_ANCHORS["CA"]["branch_entry"])
link(SURFACE_BRANCH_ANCHORS["CQ"]["anchor_room"], SURFACE_BRANCH_ANCHORS["CQ"]["direction_from_anchor"], SURFACE_BRANCH_ANCHORS["CQ"]["branch_entry"])
link(SURFACE_BRANCH_ANCHORS["BM"]["anchor_room"], SURFACE_BRANCH_ANCHORS["BM"]["direction_from_anchor"], SURFACE_BRANCH_ANCHORS["BM"]["branch_entry"])

ROOM_VISUAL_CONTEXT_OVERRIDES.update({
    # Primer tramo de cada camino, todavía pegado a su pueblo.
    "alto_terrazas": "zone.khariel",
    "piedra_patio_exterior": "zone.brumak",
    "juncos_plataformas": "zone.narevia",
    "sombra_borde": "zone.velmora",
    # Tramos dentro de la Cuenca de Veyra ("Caminos de la Cuenca de Veyra").
    **{room_id: "zone.veyra.road" for room_id in (
        _ids(ROUTE_A_BLOCK_2)[3:] + _ids(ROUTE_B)[-3:] + _ids(ROUTE_C)[-3:]
        + _ids(ROUTE_D)[-3:] + _ids(ROUTE_E)[-4:] + _ids(APPROACH_SOUTH))},
})
# Los tramos profundos de cada región (A8-A13 y los centrales de B-E) no
# tienen todavía contexto visual canónico: el marco queda vacío y quieto.

DYNAMIC_HABITAT_ROOMS.update({
    "campos_colinas": "veyra_transicion",  # A14: solo con pool propio de transición
    "alto_garganta": "hoshai_alto",        # B6
    "piedra_hendiduras": "korven_piedra",  # C6
    "juncos_juncal": "lethra_juncos",      # D5
    "sombra_niebla_baja": "nhal_bosque",   # E6
})


# examinar <objetivo> por sala -- las claves se comparan normalizadas
# (minusculas, sin acentos; ver app.py _normalize).
ROOM_EXAMINE_TARGETS = {}
ROOM_EXAMINE_TARGETS["valdren_camino_parcela"] = {
    "tallos": (
        "Los tallos están mordidos casi a ras del suelo, en un ángulo limpio. No "
        "es viento ni una herramienta: algo pequeño ha estado comiendo aquí."
    ),
    "monticulos": (
        "Los montículos de tierra son recientes y están huecos por dentro: la "
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
        "La madera no está podrida. Algo la forzó con suficiente violencia para "
        "partirla y seguir adelante."
    ),
    "huellas": (
        "Las marcas son mucho más profundas y anchas que las de las criaturas "
        "pequeñas que has visto cerca de Valdren."
    ),
}

# Camino de los Campos: huellas históricas públicas (NARRATIVE_ROUTES.md A2 y A7,
# capa "examinar"). No son secretos ni dan recompensa.
ROOM_EXAMINE_TARGETS["valdren_lindero_tres_piedras"] = {
    "piedras": 'Las piedras están gastadas y fueron movidas y reutilizadas. No coinciden del todo con las cercas de ahora: marcan una división más antigua. Valdren creció así, surco por surco.',
    "piedra": 'Las piedras están gastadas y fueron movidas y reutilizadas. No coinciden del todo con las cercas de ahora: marcan una división más antigua. Valdren creció así, surco por surco.',
}
ROOM_EXAMINE_TARGETS["valdren_zanja_vieja"] = {
    "zanja": 'Comparas los arreglos de la zanja: piedra en un tramo, tierra apisonada en otro, madera más adelante. Este camino se ha cuidado en épocas distintas.',
    "arreglos": 'Comparas los arreglos de la zanja: piedra en un tramo, tierra apisonada en otro, madera más adelante. Este camino se ha cuidado en épocas distintas.',
}
ROOM_EXAMINE_TARGETS["valdren_pastos_altos"] = {
    "cerca": "Los postes gruesos están quebrados hacia afuera a una altura considerable. Nada de lo que vive cerca del pueblo tiene esta fuerza.",
    "cercas": "Los postes gruesos están quebrados hacia afuera a una altura considerable. Nada de lo que vive cerca del pueblo tiene esta fuerza.",
    "huellas": "Depresiones muy anchas y profundas en la tierra blanda, con marcas de pezuñas grandes.",
    "huella": "Depresiones muy anchas y profundas en la tierra blanda, con marcas de pezuñas grandes.",
    "arboles": "La corteza de los troncos jóvenes fue raspada y arrancada a golpes o frotada con violencia.",
    "arbol": "La corteza de los troncos jóvenes fue raspada y arrancada a golpes o frotada con violencia.",
    "pasto": "El pasto áspero está aplastado por el paso de un animal ancho y muy pesado.",
}

# Encuentro posible por sala (id de vintage-telnet/server/creatures.py). El
# jugador decide si combate, evalua o sigue de largo -- la criatura nunca
# ataca primero (ver creatures.py, docstring).
ROOM_ENCOUNTER = {
    "valdren_camino_parcela": "mordelinde",
    "valdren_camino_cerca": "espinajo_rastrojo",
    "valdren_pastos_altos": "cornalomo",
    "alto_terrazas": "unapiedra",
    "alto_terraza_abandonada": "saltacresta",
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
        # Contrato Narrador/Historia/Jugabilidad #147, rescatado de PR #177.
        "reward_item": "acolchado_camino",
        "reward_text": (
            "Regresas a Valdren con el lindero resuelto. Entre el equipo de camino te "
            "entregan un Acolchado de Camino: sencillo, reforzado y hecho para volver a "
            "salir. Has obtenido: Acolchado de Camino."
        ),
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


# VT-SERVER: HOME-CORE (Issue #280 / Issue #114 / GAMEPLAY.md §34)
# Hogar personal persistente mínimo: base propia dinámica por personaje sin inflar ROOMS.
HOME_ROOM_NAME = "Tu hogar"
HOME_ROOM_DESCRIPTION = (
    "Este es tu hogar. Aquí comienza tu viaje y aquí conservas un lugar propio "
    "dentro del mundo. La salida conduce hacia tu comunidad."
)
HOME_EXIT_DIRECTION = "south"
HOME_ROOM_ART = {
    "humano": {
        "src": "/assets/locations/valdren-vivienda-patio.webp",
        "alt": "Patio de una vivienda en Valdren",
        "width": 1536, "height": 1024,
    },
    "felaryn": {
        "src": "/assets/locations/khariel-vivienda-felaryn-terraza.webp",
        "alt": "Terraza de una vivienda felaryn en Khariel",
        "width": 1536, "height": 1024,
    },
    "dravak": {
        "src": "/assets/locations/brumak-taller-domestico.webp",
        "alt": "Interior doméstico en Brumak",
        "width": 1536, "height": 1024,
    },
    "marevyn": {
        "src": "/assets/locations/narevia-vivienda-marevyn-canal.webp",
        "alt": "Vivienda marevyn junto al canal de Narevia",
        "width": 1536, "height": 1024,
    },
    "vesperi": {
        "src": "/assets/locations/velmora-vivienda-vesperi-raices.webp",
        "alt": "Vivienda vesperi entre las raíces de Velmora",
        "width": 1536, "height": 1024,
    },
}

_HOME_SPECIES_RESOLVER = None


def set_home_species_resolver(resolver):
    global _HOME_SPECIES_RESOLVER
    _HOME_SPECIES_RESOLVER = resolver


def get_home_room_id(player_id, species=None):
    if not player_id:
        raise ValueError("player_id es obligatorio para el hogar personal.")
    return f"home:{player_id}"


def is_home_room(room_id):
    return isinstance(room_id, str) and room_id.startswith("home:")


def parse_home_player_id(room_id):
    if is_home_room(room_id):
        return room_id.split("home:", 1)[1]
    return None


def get_room(room_id):
    room = ROOMS.get(room_id)
    if room is not None:
        return room
    if is_home_room(room_id):
        player_id = parse_home_player_id(room_id)
        species = None
        if _HOME_SPECIES_RESOLVER and player_id:
            try:
                species = _HOME_SPECIES_RESOLVER(player_id)
            except Exception:
                species = None
        resolved_species = species if species in STARTING_ROOM_BY_SPECIES else None
        town_room = get_starting_room_for_species(resolved_species or "humano")
        return {
            "id": room_id,
            "name": HOME_ROOM_NAME,
            "description": HOME_ROOM_DESCRIPTION,
            "exits": {HOME_EXIT_DIRECTION: town_room},
            "is_home": True,
            "owner_player_id": player_id,
            "species": resolved_species,
        }
    return None


def get_starting_room_for_species(species_id):
    return STARTING_ROOM_BY_SPECIES.get(species_id, "vaisgard")



def get_examine_text(room_id, normalized_target):
    return ROOM_EXAMINE_TARGETS.get(room_id, {}).get(normalized_target)


def get_room_encounter(room_id):
    return ROOM_ENCOUNTER.get(room_id)


def get_discovery(key):
    return DISCOVERIES.get(key)


# Hora del día y clima (Issue #138, petición directa de Javier). La pantalla
# ya tiene su espacio en la barra de lugar. Contrato: cada campo es None o
# {"label": texto visible, "icon": clave}. Las claves de icono disponibles en
# la interfaz son AMBIENT_ICONS; un icono desconocido se muestra solo texto.
AMBIENT_ICONS = ("sol", "luna", "amanecer", "atardecer", "nube", "lluvia", "niebla", "nieve", "tormenta", "viento")

# Hora del día: handoff de Jugabilidad en el Issue #138 (2026-09-25, todavía
# sin registrar en GAMEPLAY.md al momento de implementar esto — el criterio
# de salida de la issue sigue abierto por ese lado, pero Jugabilidad autorizó
# explícitamente implementar ya el reloj). Reloj de juego global y compartido
# por todos los jugadores, no personal ni por acciones: amanecer -> día ->
# atardecer -> noche, ciclo completo de 4 horas reales, 60 minutos reales por
# estado. Etiquetas del Narrador en el mismo issue.
_TIME_OF_DAY_STATES = (
    {"label": "Amanecer", "icon": "amanecer"},
    {"label": "Día", "icon": "sol"},
    {"label": "Atardecer", "icon": "atardecer"},
    {"label": "Noche", "icon": "luna"},
)
_TIME_OF_DAY_STATE_SECONDS = 60 * 60  # 60 min reales por estado (ciclo de 4h)


def _current_time_of_day(now=None):
    """Estado del reloj global de hora del día para `now` (segundos Unix,
    por defecto time.time()). Es una función pura del tiempo real, no un
    contador persistente: reiniciar el servidor no reinicia el día de forma
    arbitraria. `now` es inyectable para pruebas reproducibles."""
    if now is None:
        now = time.time()
    index = int(now // _TIME_OF_DAY_STATE_SECONDS) % len(_TIME_OF_DAY_STATES)
    return _TIME_OF_DAY_STATES[index]


def get_room_region(room_id):
    """Devuelve el identificador canónico de región para `room_id`
    ('veyra', 'edran', 'hoshai', 'korven', 'lethra', 'nhal').
    Si la sala define explícitamente un atributo 'region', este prevalece;
    en caso contrario se resuelve según la geografía canónica de rutas,
    pueblos y accesos a la Cuenca de Veyra."""
    if not room_id:
        return "veyra"
    if is_home_room(room_id):
        home = get_room(room_id)
        if home and HOME_EXIT_DIRECTION in home.get("exits", {}):
            return get_room_region(home["exits"][HOME_EXIT_DIRECTION])
        return "edran"
    room = ROOMS.get(room_id)
    if room and "region" in room:
        return room["region"]
    if room_id in ("vaisgard", "cuenca_aproximacion_sur"):
        return "veyra"
    # Tramos del anillo exterior que entran a la Cuenca de Veyra
    if room_id in (
        "campos_colinas", "campos_almacen", "campos_vista_vaisgard",
        "campos_camino_exterior", "campos_acceso",
        "alto_cuenca_norte", "alto_vista_vaisgard", "alto_aproximacion",
        "piedra_entrada_veyra", "piedra_vista_vaisgard", "piedra_aproximacion",
        "juncos_entrada_veyra", "juncos_vista_vaisgard", "juncos_aproximacion",
        "sombra_entrada_veyra", "sombra_cruce_viajeros", "sombra_vista_vaisgard",
        "sombra_aproximacion",
    ):
        return "veyra"
    if room_id.startswith("valdren_") or room_id.startswith("campos_"):
        return "edran"
    if room_id.startswith("khariel_") or room_id.startswith("alto_"):
        return "hoshai"
    if room_id.startswith("brumak_") or room_id.startswith("piedra_"):
        return "korven"
    if room_id.startswith("narevia_") or room_id.startswith("juncos_"):
        return "lethra"
    if room_id.startswith("velmora_") or room_id.startswith("sombra_"):
        return "nhal"
    return "veyra"


def get_ambient(room_id, now=None):
    """Ambiente visible de una sala: {"time_of_day": ..., "weather": ...}.
    time_of_day usa el reloj global compartido (Issue #138). weather usa
    el clima regional compartido v1 determinista (GAMEPLAY §37,
    REGIONAL_WEATHER_CANON.md). `now` se reenvía a ambas funciones."""
    from . import weather
    region = get_room_region(room_id)
    return {
        "time_of_day": _current_time_of_day(now),
        "weather": weather.get_region_weather(region, now=now),
    }


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
    art = VISUAL_CONTEXT_ART.get(visual_context_id)
    if room.get("is_home"):
        species = room.get("species")
        visual_context_id = f"home.{species}" if species in HOME_ROOM_ART else None
        art = HOME_ROOM_ART.get(species)
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
        "art": art,
        "ambient": get_ambient(room_id),
    }
