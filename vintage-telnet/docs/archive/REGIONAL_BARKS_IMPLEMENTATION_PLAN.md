# 🗣️ REGIONAL_BARKS — Plan de Implementación (Bonus)

**Issue:** #559 (cola de Narrativa #284)  
**Ref:** vintage-telnet/WORLD_POPULATION_REGIONAL_BARKS.md  
**Responsable:** VT (programador backend)

---

## 📋 Objetivo

Las frases que dice la población N0 deben reflejar la región donde aparecen.

**Ejemplo:**
```
Antes (genérico):
- "Buen camino."
- "Hoy hay más movimiento."

Después (región Edran):
- "Todavía queda trabajo entre las parcelas."
- "El camino está más usado que ayer."

Después (región Hoshai):
- "Desde aquí arriba se ve quién viene antes de que llegue."
- "Los pasos cambian con el viento."
```

**Resultado:** La población suena como si perteneciera a su región.

---

## 🛠️ Implementación

### Dónde agregar

Archivo: `vintage-telnet/server/population.py`

**Estructura actual:**
```python
CANONICAL_N0_DATA = {
    "habitante": {
        "role_id": "habitante",
        "label": "Habitante",
        "barks": [
            "Buen camino.",
            "Hoy hay más movimiento de lo normal.",
            ...
        ],
        ...
    },
}
```

**Estructura nueva:**
```python
CANONICAL_N0_DATA = {
    "habitante": {
        "role_id": "habitante",
        "label": "Habitante",
        "barks": {
            "default": [
                "Buen camino.",
                "Hoy hay más movimiento de lo normal.",
            ],
            "edran": [
                "Todavía queda trabajo entre las parcelas.",
                "El camino está más usado que ayer.",
                "Si vienes de Vaisgard, seguro traes noticias.",
            ],
            "hoshai": [
                "Desde aquí arriba se ve quién viene antes de que llegue.",
                "Los pasos cambian con el viento, pero no todos por igual.",
            ],
            # ... (más regiones)
        },
        ...
    },
}
```

### Lógica en `get_room_n0_presence()`

```python
def get_room_n0_presence(room_id, ...):
    ...
    
    # Obtener región del room_data
    region = room_data.get("region") if room_data else None
    
    # Obtener barks del rol (ahora es dict por región)
    role_barks = chosen_role.get("barks", [])
    
    # Si barks es dict, seleccionar por región
    if isinstance(role_barks, dict):
        barks = role_barks.get(region, role_barks.get("default", []))
    else:
        barks = role_barks  # Backwards compatibility
    
    # Seleccionar bark determinísticamente
    bark = ""
    if barks:
        bark_idx = int.from_bytes(digest[8:12], byteorder="big") % len(barks)
        bark = barks[bark_idx]
    
    ...
```

### Regiones a Cubrir

Copiar de `WORLD_POPULATION_REGIONAL_BARKS.md`:

| Región | Roles | Frases por rol |
|--------|-------|---|
| **Edran/Valdren** | habitante, trabajador, cargador, recolector | 3-4 por rol |
| **Veyra/Vaisgard** | habitante, trabajador, cargador, viajero | 3-4 por rol |
| **Hoshai/Khariel** | habitante, trabajador, viajero, recolector | 3-4 por rol |
| **Korven/Brumak** | habitante, trabajador, cargador, recolector | 3-4 por rol |
| **Lethra/Narevia** | habitante, trabajador, cargador, viajero | 3-4 por rol |
| **Nhal/Velmora** | habitante, trabajador, viajero, recolector | 3-4 por rol |

---

## 📋 Cambios Necesarios

### 1. Actualizar `CANONICAL_N0_DATA` en population.py

Convertir cada rol de:
```python
"barks": [
    "Frase 1",
    "Frase 2",
]
```

A:
```python
"barks": {
    "default": ["Frase 1", "Frase 2"],
    "edran": ["Frase regional 1", "Frase regional 2"],
    "hoshai": [...],
    # ... (6 regiones)
}
```

### 2. Agregar `region` a world.py

Cada sala debe tener:
```python
ROOMS = {
    "valdren_centro": {
        "name": "...",
        ...
        "region": "edran",  # ⭐ NUEVO
    },
}
```

### 3. Actualizar lógica en `get_room_n0_presence()`

Ver código arriba (seleccionar barks por región).

---

## ⚠️ Reglas

- ✅ Solo cambia frases (barks), no densidad ni elegibilidad
- ✅ Rol debe ser compatible con región (historiador validó)
- ✅ `default` como fallback si región no tiene barks
- ✅ Mantener backwards compatibility (si barks es list, usar directo)

---

## 🧪 Testing

```bash
cd vintage-telnet

# Verificar que no hay errores de sintaxis
python3 -c "from server.population import CANONICAL_N0_DATA; print(type(CANONICAL_N0_DATA['habitante']['barks']))"
# Debe imprimir: <class 'dict'>

# Verificar que cada región tiene barks
python3 -c "
from server.population import CANONICAL_N0_DATA
for role_name, role_data in CANONICAL_N0_DATA.items():
    barks = role_data.get('barks', {})
    if isinstance(barks, dict):
        regions = list(barks.keys())
        print(f'{role_name}: {regions}')
"
```

---

## 📊 Effort Estimate

- Modificar `CANONICAL_N0_DATA`: ~200 líneas (copy-paste de canon)
- Agregar `region` a 20-30 salas principales: ~30 líneas
- Actualizar lógica en `get_room_n0_presence()`: ~10 líneas
- **Total: ~240 líneas**

---

## 📞 Nota

Esta es una tarea **BONUS/PULIDO** (prioridad 3).
No es necesaria para que el mundo funcione, pero hace que sea más inmersivo.

Puede hacerse **después** de las 5 tareas principales.
