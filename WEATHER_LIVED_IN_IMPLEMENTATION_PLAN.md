# 🌦️ WEATHER_LIVED_IN — Plan de Implementación

**Issue:** #555 WEATHER-LIVED-IN-01  
**Ref:** vintage-telnet/WEATHER_LIVED_IN_CANON.md  
**Responsable:** VT (programador backend)

---

## 📋 Objetivo

El clima (ya existente en `weather.py`) debe afectar cómo se **describen** las salas. No cambia mecánicas ni añade objetos.

**Ejemplo:**
```
Sin clima (o clima despejado):
"Valdren, plaza central. Casas alrededor."

Con lluvia:
"Valdren, plaza central. Casas alrededor. [Lluvia] Barro en caminos, 
huellas profundas, herramientas y grano protegidos bajo aleros."
```

**Resultado:** El mundo responde visualmente al clima sin afectar gameplay.

---

## 🛠️ Implementación

### Arquitectura Existente

El sistema de clima ya existe:
- `vintage-telnet/server/weather.py`: calcula clima por región/hora
- `world.get_ambient(room_id)` retorna clima actual
- `describe_room()` ya llama a `get_ambient()`

### Qué Agregar

Para cada sala (especialmente centros, forjas, mercados, rutas principales), agregar tabla de clima:

```python
ROOMS = {
    "valdren_centro": {
        "name": "Valdren, plaza central",
        "description": "Casas alrededor, camino principal.",
        ...
        # ⭐ NUEVO
        "weather_details": {
            "rain": "Barro en caminos, huellas profundas, herramientas y grano protegidos bajo aleros.",
            "fog": "Capa baja sobre parcelas y zanjas; cercas aparecen a poca distancia.",
            "wind": "Tallos, rastrojo y ropa se inclinan; cargas ligeras se atan.",
            "storm": "Trabajo de campo se interrumpe y animales/cargas se llevan a resguardo.",
            "clear": None,  # Usar descripción base
            "cloudy": None,  # Usar descripción base
        },
    },
}
```

### Tipos de Clima

Según `REGIONAL_WEATHER_CANON.md`:
- `rain` — lluvia
- `fog` — niebla
- `wind` — viento
- `storm` — tormenta
- `snow` — nieve (solo Hoshai/Khariel)
- `clear` — despejado (sin efecto visual)
- `cloudy` — nublado (sin efecto visual)

### Mostrar en `describe_room()`

En `app.py`:

```python
def describe_room(room_id, ...):
    room = get_room(room_id)
    ambient = get_ambient(room_id)  # {'condition': 'rain', 'region': 'edran', ...}
    
    description = room.get("description", "")
    
    # ⭐ NUEVO: Agregar detalle de clima si existe
    weather_details = room.get("weather_details", {})
    if ambient and weather_details:
        condition = ambient.get("condition")
        detail = weather_details.get(condition)
        if detail:  # Solo si no es None
            description += f"\n[Clima] {detail}"
    
    return {
        "id": room_id,
        "name": room["name"],
        "description": description,
        ...
    }
```

---

## 🗂️ Salas a Actualizar

Prioridad: centros, forjas, mercados, rutas principales.

### Por Región

#### **Veyra/Vaisgard** (5-7 salas)
Ref: `WEATHER_LIVED_IN_CANON.md` línea 10

Clima: lluvia, niebla, viento, tormenta, despejado/nublado
NO: nieve

```
vaisgard (centro)
campos_almacen (ruta principal)
campos_acceso (ruta principal)
```

#### **Edran/Valdren** (5-7 salas)
Ref: línea 18

Clima: lluvia, niebla, viento, tormenta, despejado/nublado
NO: nieve

```
valdren_centro
valdren_forja
valdren_mercado
valdren_camino_hundido (ruta)
valdren_arbol_descanso (ruta)
```

#### **Hoshai/Khariel** (5-7 salas)
Ref: línea 26

Clima: lluvia, niebla, **nieve**, viento, tormenta, despejado/nublado

```
khariel_centro
khariel_forja
khariel_mercado
alto_mirador (ruta)
alto_terrazas (ruta)
```

#### **Korven/Brumak** (5-7 salas)
Ref: línea 35

Clima: lluvia, viento, tormenta, despejado/nublado
NO: niebla, nieve

```
brumak_centro
brumak_forja
brumak_mercado
piedra_patio_abierto (ruta)
piedra_abrigo_viento (ruta)
```

#### **Lethra/Narevia** (5-7 salas)
Ref: línea 43

Clima: lluvia, niebla, viento, tormenta, despejado/nublado
NO: nieve

```
narevia_centro
narevia_forja
narevia_mercado
juncos_plataformas (ruta)
juncos_embarcadero (ruta)
```

#### **Nhal/Velmora** (5-7 salas)
Ref: línea 51

Clima: lluvia, niebla, viento, tormenta, despejado/nublado
NO: nieve

```
velmora_centro
velmora_forja
velmora_mercado
sombra_claro_pequeno (ruta)
sombra_niebla_baja (ruta)
```

**Total: ~36-42 salas**

---

## ⚠️ Reglas a Respetar

- ✅ Solo presentacional (no afecta mecánicas)
- ✅ No concede bonus/penalización
- ✅ No cambia pools/fauna
- ✅ No daña ni bloquea rutas
- ✅ No crea objetos equipables
- ✅ No implica estaciones
- ✅ Agregar como **detalle breve**, no reescribir sala completa
- ✅ Max 1 línea por clima (no acumular)

---

## 🧪 Testing

```bash
cd vintage-telnet

# Verificar que weather_details está en salas
python3 -c "from server.world import ROOMS; print(len([r for r in ROOMS.values() if r.get('weather_details')]))"
# Debe ser ~36-42

# Manual test: cambiar clima en describe_room y verificar texto
# (requiere estar en juego con diferentes climas)
```

---

## 📋 Integración

**Esta es la ÚLTIMA tarea de la ola #558.**

Después de implementar los 3 (ROOM_MICRO_PRESENCE + ROUTE_LIVENESS + WEATHER_LIVED_IN):
- El mundo se sentirá más habitado
- Las rutas mostrarán signos de viajeros
- El clima afectará visualmente las descripciones
- Todo sin crear NPCs nuevos ni afectar gameplay

---

## 📊 Resumen de Textos a Copiar

| Tarea | Archivo | Salas | Textos |
|-------|---------|-------|--------|
| ROOM_MICRO_PRESENCE | ROOM_MICRO_PRESENCE_NARRATIVE.md | 16 | Líneas de actividad (gente, trabajo) |
| ROUTE_LIVENESS | ROUTE_LIVENESS_*.md | ~37 | Líneas de tránsito/evidencia |
| WEATHER_LIVED_IN | WEATHER_LIVED_IN_CANON.md | ~36-42 | Líneas por tipo de clima |

**Total de salas a actualizar: ~89-95**
