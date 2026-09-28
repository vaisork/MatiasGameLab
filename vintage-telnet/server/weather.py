"""Módulo autoritativo de clima regional compartido v1.

Contrato: GAMEPLAY.md §37 y REGIONAL_WEATHER_CANON.md (Issue #138 / PR #293).
El clima es ambiental/presentacional en v1:
- no modifica daño ni defensa;
- no modifica Percepción ni fatiga;
- no modifica movimiento ni encuentros;
- no modifica especies ni capacidades ni available_actions.

Cadencia:
- Fase climática global de 2 horas reales (7200 segundos).
- weather_epoch = floor(unix_time / 7200).
- Reiniciar el servidor no reinicia ni adelanta el clima (función pura del tiempo real).
- No requiere tabla SQLite ni job programado.

Selección determinista por región:
- index = (weather_epoch + region_offset) mod len(allowed_weather)
- weather = allowed_weather[index]
- Offsets fijos y estables por región.
- Respeta estrictamente las exclusiones canónicas del Historiador:
    * Nieve: solo Hoshai en v1.
    * Korven: sin Niebla ni Nieve.
    * Veyra, Edran, Lethra, Nhal: sin Nieve.
"""

import time

# Vocabulario de presentación aprobado (#138 / REGIONAL_WEATHER_CANON.md).
# Las claves de icono corresponden a AMBIENT_ICONS en server/world.py y a los
# símbolos SVG #icon-amb-* en server/templates/entry.html.
WEATHER_STATES = {
    "despejado": {"label": "Despejado", "icon": "sol", "key": "despejado"},
    "nublado": {"label": "Nublado", "icon": "nube", "key": "nublado"},
    "lluvia": {"label": "Lluvia", "icon": "lluvia", "key": "lluvia"},
    "niebla": {"label": "Niebla", "icon": "niebla", "key": "niebla"},
    "nieve": {"label": "Nieve", "icon": "nieve", "key": "nieve"},
    "tormenta": {"label": "Tormenta", "icon": "tormenta", "key": "tormenta"},
    "viento": {"label": "Viento", "icon": "viento", "key": "viento"},
}

# Identificadores de las seis regiones canónicas iniciales
REGIONS = ("veyra", "edran", "hoshai", "korven", "lethra", "nhal")

REGIONAL_NAMES = {
    "veyra": "Cuenca de Veyra",
    "edran": "Llanos de Edran",
    "hoshai": "Sierra de Hoshai",
    "korven": "Pedrales de Korven",
    "lethra": "Aguas de Lethra",
    "nhal": "Bosque de Nhal",
}

# Listas ordenadas tomadas literalmente de REGIONAL_WEATHER_CANON.md.
REGIONAL_ALLOWED_WEATHER = {
    "veyra": ["despejado", "nublado", "lluvia", "niebla", "tormenta", "viento"],
    "edran": ["despejado", "nublado", "lluvia", "niebla", "tormenta", "viento"],
    "hoshai": ["despejado", "nublado", "lluvia", "niebla", "nieve", "tormenta", "viento"],
    "korven": ["despejado", "nublado", "lluvia", "tormenta", "viento"],
    "lethra": ["despejado", "nublado", "lluvia", "niebla", "tormenta", "viento"],
    "nhal": ["despejado", "nublado", "lluvia", "niebla", "tormenta", "viento"],
}

# Offsets fijos y estables por configuración técnica (GAMEPLAY §37.3), no aleatorios.
# Permiten que regiones diferentes no manifiesten idéntico clima simultáneo en cada fase.
REGIONAL_OFFSETS = {
    "veyra": 0,
    "edran": 1,
    "hoshai": 2,
    "korven": 3,
    "lethra": 4,
    "nhal": 5,
}

WEATHER_CYCLE_SECONDS = 2 * 60 * 60  # 7200 segundos (2 horas reales)


def weather_epoch(now=None):
    """Fase climática global determinista derivada del tiempo Unix.
    weather_epoch = floor(unix_time / 7200)."""
    if now is None:
        now = time.time()
    return int(now // WEATHER_CYCLE_SECONDS)


def get_region_weather(region, now=None):
    """Retorna el estado de clima visible {"label": ..., "icon": ..., "key": ...}
    para la región dada en el instante `now`.
    Fórmula de GAMEPLAY §37.3:
      index = (weather_epoch + region_offset) mod len(allowed_weather)
      weather = allowed_weather[index]
    """
    allowed = REGIONAL_ALLOWED_WEATHER.get(region)
    if not allowed:
        allowed = REGIONAL_ALLOWED_WEATHER["veyra"]
    offset = REGIONAL_OFFSETS.get(region, 0)
    epoch = weather_epoch(now)
    index = (epoch + offset) % len(allowed)
    weather_key = allowed[index]
    return WEATHER_STATES[weather_key]


def get_weather_for_room(room_id, now=None):
    """Resuelve el clima regional para una sala específica."""
    from . import world
    region = world.get_room_region(room_id)
    return get_region_weather(region, now=now)
