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
    # Caminos ("zone.veyra.road", "zone.edran.valdren_outskirts"): cuando Arte
    # publique su ilustración, basta con agregar aquí la fila; hasta entonces
    # el marco queda vacío y quieto (petición de Javier, 2026-09-25).
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
    "valdren_arbol_descanso": "zone.edran.valdren_outskirts",
    "valdren_campos_sin_cerca": "zone.edran.valdren_outskirts",
    "valdren_vado_menor": "zone.edran.valdren_outskirts",
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
