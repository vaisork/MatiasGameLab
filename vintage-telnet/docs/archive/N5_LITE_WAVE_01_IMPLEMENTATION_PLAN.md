# 🧭 N5-LITE-WAVE-01 — Plan de Implementación

**Issue:** #557 N5-LITE-WAVE-01  
**Ref:** vintage-telnet/N5_LITE_WAVE_01_CANON.md  
**Responsable:** VT (programador backend)

---

## 📋 Objetivo

Agregar 5 viajeros recurrentes al mundo. Estos son NPCs que se mueven por rutas fijas en cada región.

**Diferencia con Loren (piloto):**
- Loren: 1 viajero solo en Edran (piloto/prueba)
- N5-lite Wave 01: 5 viajeros, uno por región (Hoshai, Korven, Lethra, Nhal, Veyra)

**Resultado:** El mundo se siente más vivo porque los jugadores encuentran gente viajando por las rutas.

---

## 🧭 Los 5 Viajeros

### 1. **Hoshai** — `traveler_hoshai_01`

```python
Traveler(
    npc_id="traveler_hoshai_01",
    name="[NOMBRE POR DEFINIR - Felaryn de Khariel]",  # ← Creador de NPCs elige
    role="Felaryn que lleva avisos cotidianos entre terrazas",
    species="Felaryn",
    town="Khariel",
    route_id="hoshai_terrazas_01",
    route=[
        "khariel_centro",
        "alto_terrazas",
        "alto_mirador",
        "alto_anclajes",
        "alto_escalones",
        "alto_terraza_abandonada",
        "alto_garganta",
        "alto_cruce_alturas",
        "alto_puente_viento",
    ],
    step_seconds=600,  # 10 minutos por paso
    terminal="reverse",  # Ida y vuelta
    persistent_traveler=False,  # Determinístico, sin DB
    pauses=["khariel_centro", "alto_mirador", "alto_terraza_abandonada"],
    fallback_dialogue="El Felaryn continúa revisando el estado del paso.",
    phrases=[
        # Creador de NPCs proporciona 3-5 frases según personalidad
        "El paso de..." # ← Por completar
    ],
)
```

**Función:** Lleva avisos cotidianos entre terrazas y revisa estado de pasos.  
**Conoce:** estado visible del camino, clima inmediato, tránsito reciente.  
**No conoce:** secretos, Rompecimas oculto, rutas no recorridas.

### 2. **Korven** — `traveler_korven_01`

```python
Traveler(
    npc_id="traveler_korven_01",
    name="[NOMBRE POR DEFINIR - Dravak de Brumak]",  # ← Creador de NPCs elige
    role="Dravak corredor de herramientas y recados",
    species="Dravak",
    town="Brumak",
    route_id="korven_trabajo_01",
    route=[
        "brumak_centro",
        "piedra_patio_exterior",
        "piedra_pared_anclajes",
        "piedra_paso_corto",
        "piedra_patio_abierto",
        "piedra_primer_monton",
        "piedra_hendiduras",
        "piedra_pared_partida",
        "piedra_abrigo_viento",
    ],
    step_seconds=600,
    terminal="reverse",
    persistent_traveler=False,
    pauses=["brumak_centro", "piedra_patio_abierto", "piedra_abrigo_viento"],
    fallback_dialogue="El Dravak continúa cuidadosamente su ruta entre montones de roca.",
    phrases=[],  # ← Por completar
)
```

**Función:** Corredor de herramientas y recados entre Brumak y trabajo exterior.  
**Conoce:** reparaciones, montones de orientación, viento y pasos usados.

### 3. **Lethra** — `traveler_lethra_01`

```python
Traveler(
    npc_id="traveler_lethra_01",
    name="[NOMBRE POR DEFINIR - Marevyn de Narevia]",  # ← Creador de NPCs elige
    role="Marevyn enlace cotidiano entre plataformas",
    species="Marevyn",
    town="Narevia",
    route_id="lethra_plataformas_01",
    route=[
        "narevia_centro",
        "juncos_plataformas",
        "juncos_postes",
        "juncos_pasarela_antigua",
        "juncos_isla_refugio",
        "juncos_juncal",
        "juncos_paso_raices",
        "juncos_embarcadero",
        "juncos_agua_entre_caminos",
    ],
    step_seconds=600,
    terminal="reverse",
    persistent_traveler=False,
    pauses=["narevia_centro", "juncos_isla_refugio", "juncos_embarcadero"],
    fallback_dialogue="La Marevyn continúa vigilando el nivel del agua.",
    phrases=[],  # ← Por completar
)
```

**Función:** Enlace cotidiano entre plataformas y tramos de agua.  
**Conoce:** nivel del agua, pasos, plataformas y tránsito.

### 4. **Nhal** — `traveler_nhal_01`

```python
Traveler(
    npc_id="traveler_nhal_01",
    name="[NOMBRE POR DEFINIR - Vesperi de Velmora]",  # ← Creador de NPCs elige
    role="Vesperi que mantiene orientación y lleva mensajes",
    species="Vesperi",
    town="Velmora",
    route_id="nhal_bosque_01",
    route=[
        "velmora_centro",
        "sombra_borde",
        "sombra_tronco",
        "sombra_raices_cruzadas",
        "sombra_claro_pequeno",
        "sombra_sendero_doble",
        "sombra_niebla_baja",
        "sombra_arbol_caido",
        "sombra_tres_marcas",
        "sombra_claro_escucha",
    ],
    step_seconds=600,
    terminal="reverse",
    persistent_traveler=False,
    pauses=["velmora_centro", "sombra_claro_pequeno", "sombra_claro_escucha"],
    fallback_dialogue="El Vesperi continúa atento a las señales del sendero.",
    phrases=[],  # ← Por completar
)
```

**Función:** Mantiene orientación cotidiana y lleva mensajes breves.  
**Conoce:** señales de orientación, estado del sendero.

### 5. **Veyra** — `traveler_veyra_01`

```python
Traveler(
    npc_id="traveler_veyra_01",
    name="[NOMBRE POR DEFINIR - Humano de Vaisgard]",  # ← Creador de NPCs elige
    role="Humano mensajero entre Vaisgard y Campos",
    species="Humano",
    town="Vaisgard",
    route_id="veyra_cuenca_01",
    route=[
        "vaisgard",
        "cuenca_aproximacion_sur",
        "campos_acceso",
        "campos_camino_exterior",
        "campos_vista_vaisgard",
        "campos_almacen",
    ],
    step_seconds=600,
    terminal="reverse",
    persistent_traveler=False,
    pauses=["vaisgard", "campos_almacen"],
    fallback_dialogue="El mensajero continúa su ruta entre la ciudad y los campos.",
    phrases=[],  # ← Por completar
)
```

**Función:** Mensajero informal de tránsito entre Vaisgard y Campos.  
**Conoce:** tránsito visible, estado del almacén.

---

## 🛠️ Dónde Implementar

### Archivo: `vintage-telnet/server/travelers.py`

**Dónde agregar:** Después de la definición de LOREN (línea 293), antes del final del archivo.

**Template para copiar/pegar:**

```python
# N5-LITE-WAVE-01: Hoshai (Issue #557 / N5_LITE_WAVE_01_CANON.md)
TRAVELER_HOSHAI_01 = Traveler(
    npc_id="traveler_hoshai_01",
    name="[NOMBRE AQUÍ]",
    role="lleva avisos cotidianos entre terrazas",
    species="Felaryn",
    town="Khariel",
    route_id="hoshai_terrazas_01",
    route=["khariel_centro", "alto_terrazas", "alto_mirador", "alto_anclajes", 
           "alto_escalones", "alto_terraza_abandonada", "alto_garganta", 
           "alto_cruce_alturas", "alto_puente_viento"],
    step_seconds=600,
    terminal="reverse",
    persistent_traveler=False,
    pauses=["khariel_centro", "alto_mirador", "alto_terraza_abandonada"],
    fallback_dialogue="El Felaryn continúa revisando el estado del paso.",
    phrases=[],  # Creador de NPCs proporciona frases
)
_REGISTRY.register(TRAVELER_HOSHAI_01)

# N5-LITE-WAVE-01: Korven (Issue #557)
TRAVELER_KORVEN_01 = Traveler(
    npc_id="traveler_korven_01",
    name="[NOMBRE AQUÍ]",
    # ... (similar a arriba)
)
_REGISTRY.register(TRAVELER_KORVEN_01)

# ... (y así para Lethra, Nhal, Veyra)
```

---

## 📋 Checklist de Implementación

**Por hacer en travelers.py:**
- [ ] Copiar/pegar template de 5 viajeros
- [ ] Completar nombres (o dejar TBD si Creador de NPCs los define)
- [ ] Agregar frases según personalidad
- [ ] Registrar cada viajero con `_REGISTRY.register()`
- [ ] Verificar que las rutas existen en world.py

**Por hacer (DESPUÉS, en otra PR):**
- [ ] Creador de NPCs: proporcionar nombres y personalidad
- [ ] Creador de NPCs: escribir 3-5 frases por viajero
- [ ] Tests: verificar que `get_position()` retorna posiciones correctas

---

## 🧪 Testing Básico

Una vez agregados los 5 viajeros, ejecutar:

```bash
cd vintage-telnet

# Verificar que no hay errores de import
python3 -c "from server.travelers import get_registry; print([t.npc_id for t in get_registry().list_all()])"

# Debería imprimir:
# ['viajero_loren', 'traveler_hoshai_01', 'traveler_korven_01', 'traveler_lethra_01', 'traveler_nhal_01', 'traveler_veyra_01']

# Verificar posiciones (determinísticas)
python3 -c "
from server.travelers import get_registry
import time
now = time.time()
for t in get_registry().list_all()[1:]:  # Skip Loren (piloto)
    pos = get_registry().get_position(t, now=now)
    print(f'{t.npc_id}: {pos}')
"
```

---

## ⚠️ Reglas a No Romper

Verificar que **ningún viajero:**
- Entra a interiores privados, forjas, mercados
- Tiene conflictos con NPCs scriptos (máximo 1 por sala)
- Cruza a zonas prohibidas (Cantera/Grieta para Korven, etc.)
- Vende, cura o da quests automáticamente

---

## 📞 Próxima Etapa

Una vez mergeado N5-LITE-WAVE-01, la siguiente prioridad es:

1. **ROOM_MICRO_PRESENCE** — Agregar narrativa de micro-presencia a salas
2. **ROUTE_LIVENESS** — Agregar diálogos contextuales a rutas
3. **WEATHER_LIVED_IN** — Clima afecta descripciones

---

## 🔗 Referencias

- Canon: `vintage-telnet/N5_LITE_WAVE_01_CANON.md`
- Código: `vintage-telnet/server/travelers.py` (línea 262 para ver Loren)
- Sistema de viajeros: `vintage-telnet/server/travelers.py` línea 1-60
