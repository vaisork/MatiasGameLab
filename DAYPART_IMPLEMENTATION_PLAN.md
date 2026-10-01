# 🌅 DAYPART_POPULATION_ENGINE — Plan de Implementación

**Issue:** #554 DAYPART-POPULATION-01  
**Ref:** vintage-telnet/DAYPART_POPULATION_CANON.md  
**Responsable:** VT (programador backend)

---

## 📋 Objetivo

Modificar `population.py` para que mostrar NPCs diferentes según la hora del día (**daypart**):
- 🌅 Amanecer
- ☀️ Día
- 🌇 Atardecer
- 🌙 Noche

Actualmente, la población N0 no varía por hora. Con esto, la presencia será plausible según la hora.

---

## 🔄 Flujo Actual vs. Nuevo

### ANTES:
```
get_room_n0_presence(room_id)
  → población_profile de la sala
  → elige rol aleatorio
  → retorna NPCs (igual para todas las horas)
```

### DESPUÉS:
```
get_room_n0_presence(room_id, timestamp)
  → población_profile de la sala
  → NUEVO: get_daypart(timestamp) → "día", "noche", etc.
  → NUEVO: checa si rol/lugar está permitido en este daypart
  → elige rol (respetando daypart)
  → retorna NPCs (diferentes según hora)
```

---

## 🛠️ Cambios Técnicos

### 1. Agregar función `get_daypart()`

```python
def get_daypart(timestamp: Optional[float] = None) -> str:
    """Retorna el daypart actual: 'amanecer', 'día', 'atardecer', 'noche'
    
    Definición:
    - amanecer: 06:00 - 09:00
    - día: 09:00 - 17:00
    - atardecer: 17:00 - 21:00
    - noche: 21:00 - 06:00
    """
    if timestamp is None:
        timestamp = time.time()
    
    hour = time.gmtime(timestamp).tm_hour  # UTC
    
    if 6 <= hour < 9:
        return "amanecer"
    elif 9 <= hour < 17:
        return "día"
    elif 17 <= hour < 21:
        return "atardecer"
    else:
        return "noche"
```

### 2. Agregar `DAYPART_POPULATION_TABLE`

Mapear cada (rol, lugar) a su disponibilidad en cada daypart:

```python
DAYPART_POPULATION_TABLE: Dict[tuple[str, str], Dict[str, str]] = {
    # (rol, lugar) → {amanecer, día, atardecer, noche}
    
    # Habitantes
    ("habitante", "pueblo_centro"): {"amanecer": "reducida", "día": "normal", "atardecer": "normal", "noche": "reducida"},
    ("habitante", "pueblo_borde"): {"amanecer": "normal", "día": "normal", "atardecer": "normal", "noche": "reducida"},
    
    # Trabajadores
    ("trabajador", "campo-terraza-orilla"): {"amanecer": "normal", "día": "normal", "atardecer": "reducida", "noche": "excluida"},
    ("trabajador", "taller_borde"): {"amanecer": "reducida", "día": "normal", "atardecer": "normal", "noche": "improbable"},
    
    # Cargadores
    ("cargador", "mercado-pueblo_borde"): {"amanecer": "reducida", "día": "normal", "atardecer": "normal", "noche": "improbable"},
    ("cargador", "camino-cruce"): {"amanecer": "reducida", "día": "normal", "atardecer": "reducida", "noche": "improbable"},
    
    # Viajeros
    ("viajero", "camino-cruce"): {"amanecer": "reducida", "día": "normal", "atardecer": "normal", "noche": "reducida"},
    ("viajero", "refugio_ruta"): {"amanecer": "normal", "día": "reducida", "atardecer": "normal", "noche": "normal"},
    
    # Recolectores
    ("recolector", "campo-orilla-bosque"): {"amanecer": "normal", "día": "normal", "atardecer": "reducida", "noche": "improbable"},
    ("recolector", "bosque_nhal"): {"amanecer": "reducida", "día": "normal", "atardecer": "reducida", "noche": "reducida"},
}
```

**Mapeo de presencia a probabilidad:**
```python
DAYPART_PRESENCE_TO_PROBABILITY = {
    "excluida": 0.0,      # No aparece
    "improbable": 0.10,   # 10% chance
    "reducida": 0.20,     # 20% chance
    "normal": 0.30,       # 30% chance (default actual)
}
```

### 3. Mapear salas a (rol, lugar)

Cada sala necesita tags que identifiquen:
- **rol**: habitante, trabajador, cargador, viajero, recolector
- **lugar**: pueblo_centro, campo-terraza-orilla, refugio_ruta, etc.

Ejemplo en `world.py`:
```python
ROOMS = {
    "valdren_centro": {
        "name": "Valdren, plaza central",
        ...
        "daypart_role": "habitante",
        "daypart_location": "pueblo_centro",
    },
    ...
}
```

### 4. Modificar `get_room_n0_presence()`

Agregar lógica de daypart:

```python
def get_room_n0_presence(...):
    # ... código existente ...
    
    epoch = get_population_epoch(timestamp)
    daypart = get_daypart(timestamp)  # ← NUEVO
    
    # NUEVO: Checa si el rol está permitido en este daypart
    daypart_role = room_data.get("daypart_role")
    daypart_location = room_data.get("daypart_location")
    
    if daypart_role and daypart_location:
        key = (daypart_role, daypart_location)
        daypart_probs = DAYPART_POPULATION_TABLE.get(key, {})
        daypart_presence = daypart_probs.get(daypart, "normal")
        
        # Sobrescribir probabilidad con la del daypart
        prob = DAYPART_PRESENCE_TO_PROBABILITY.get(daypart_presence, 0.3)
    else:
        # Sin tags daypart, usar la probabilidad del perfil
        prob = DENSITY_PROFILES.get(density_profile, 0.0)
    
    # ... resto del código existente ...
```

---

## 📋 Checklist de Implementación

- [ ] Agregar `get_daypart()` a population.py
- [ ] Agregar `DAYPART_POPULATION_TABLE` a population.py
- [ ] Agregar `DAYPART_PRESENCE_TO_PROBABILITY` a population.py
- [ ] Modificar `get_room_n0_presence()` para usar daypart
- [ ] Agregar campos `daypart_role` y `daypart_location` a todas las salas en world.py
- [ ] Ejecutar tests: `python3 -m unittest discover -s vintage-telnet/tests -k population -v`
- [ ] Verificar que NPCs cambian según hora del día (manual playtest)
- [ ] Commit: "Implement DAYPART_POPULATION_ENGINE (#554)"
- [ ] Merge a main

---

## 🧪 Testing

### Unit Tests:
```python
def test_get_daypart_boundaries():
    assert get_daypart(timestamp_for_08_00) == "amanecer"
    assert get_daypart(timestamp_for_12_00) == "día"
    assert get_daypart(timestamp_for_18_00) == "atardecer"
    assert get_daypart(timestamp_for_23_00) == "noche"

def test_daypart_affects_population():
    # A las 8am (amanecer), habitante/pueblo_centro debe ser "reducida"
    # A las 12pm (día), debe ser "normal"
```

### Manual Playtest:
1. Juega de día → ve "Habitante" frecuentemente en plaza
2. Juega de noche → ve "Habitante" raramente, "Viajero" en rutas
3. Verifica que cambios se aplican sin restart (determinismo por epoch)

---

## ⚠️ Consideraciones

1. **Reglas que no romper:**
   - scripted NPC > N0 (un NPC script bloquea N0)
   - máximo 1 N0 por sala (vigente)
   - daypart modifica plausibilidad, no identidad

2. **Regional adjustments:**
   - Edran: trabajo agrícola amanece/día
   - Hoshai: actividad baja de madrugada
   - Korven: viento nocturno improbable
   - Lethra: orilla siempre tiene vida
   - Nhal: noche ≠ vacío (Vesperi siguen)
   - Veyra: máximo tránsito día/atardecer

3. **Performance:**
   - `get_daypart()` es O(1)
   - Tablas lookup son O(1)
   - No añade DB queries

---

## 📞 Próximo Paso

Una vez mergeado, pasamos a **#557 N5-LITE-WAVE-01** (materializar 5 viajeros recurrentes).
