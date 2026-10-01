# 🏛️ ROOM_MICRO_PRESENCE — Plan de Implementación

**Issue:** #558 (cola de Narrativa #284)  
**Ref:** vintage-telnet/ROOM_MICRO_PRESENCE_NARRATIVE.md  
**Responsable:** VT (programador backend)

---

## 📋 Objetivo

Enriquecer salas existentes con texto de "micro-presencia" que muestre actividad ambiental cuando el jugador las examina.

**Ejemplo:**
```
Antes: "Valdren, plaza central. Casas alrededor, camino principal."

Después: "Valdren, plaza central. Casas alrededor, camino principal.
[Micro-presencia] Alguien cruza la plaza con una cesta, otro se detiene 
a intercambiar unas palabras y el paso vuelve a quedar libre."
```

**Resultado:** El mundo se siente más habitado sin crear NPCs nuevos.

---

## 🛠️ Implementación

### Dónde agregar

Archivo: `vintage-telnet/server/world.py`

En cada sala dict, agregar campo opcional:
```python
"micro_presence": "Texto descriptivo de actividad ambiental"
```

### Patrón

Cada sala es una **línea única**, máximo 1-2 oraciones:

```python
ROOMS = {
    "valdren_centro": {
        "name": "Valdren, plaza central",
        "description": "...",
        ...
        # ⭐ NUEVO
        "micro_presence": "Alguien cruza la plaza con una cesta, otro se detiene a intercambiar unas palabras y el paso vuelve a quedar libre.",
    },
    "valdren_forja": {
        "name": "Valdren, taller de herramientas",
        "description": "...",
        ...
        # ⭐ NUEVO
        "micro_presence": "Entre golpes de herramienta y piezas apoyadas contra la pared, el trabajo sigue aunque nadie te esté atendiendo directamente.",
    },
    # ... (más salas)
}
```

### Salas a actualizar (por región)

Copiar de `ROOM_MICRO_PRESENCE_NARRATIVE.md`:

**Valdren** (3 salas):
- `valdren_centro`
- `valdren_forja`
- `valdren_mercado`

**Khariel** (3 salas):
- `khariel_centro`
- `khariel_forja`
- `khariel_mercado`

**Brumak** (3 salas):
- `brumak_centro`
- `brumak_forja`
- `brumak_mercado`

**Narevia** (3 salas):
- `narevia_centro`
- `narevia_forja`
- `narevia_mercado`

**Velmora** (3 salas):
- `velmora_centro`
- `velmora_forja`
- `velmora_mercado`

**Vaisgard** (1 sala):
- `vaisgard`

**Total: 16 salas**

---

### Mostrar en UI

En `app.py`, función `describe_room()`:

```python
def describe_room(room_id, ...):
    room = get_room(room_id)
    ...
    
    description = room.get("description", "")
    
    # ⭐ NUEVO: Agregar micro-presencia si existe
    if room.get("micro_presence"):
        description += f"\n[Ambiente] {room['micro_presence']}"
    
    return {
        "id": room_id,
        "name": room["name"],
        "description": description,
        ...
    }
```

O en HTML `entry.html.jinja2`, si prefieres:

```html
<div class="room-description">
    {{ room.description }}
    {% if room.micro_presence %}
    <div class="micro-presence">{{ room.micro_presence }}</div>
    {% endif %}
</div>
```

---

## ⚠️ Reglas a Respetar

- ✅ No nombrar personas (excepto NPCs scripted)
- ✅ No implicar misiones ocultas
- ✅ No crear venta/compra nueva
- ✅ No prometer interacción con cada figura
- ✅ Ocultar si hay combate activo
- ✅ Ocultar si hay escena scripted que requiere aislamiento
- ✅ Daypart/clima pueden sustituir, no acumular (max 1 línea)

---

## 🧪 Testing

```bash
cd vintage-telnet

# Verificar que no hay errores de sintaxis
python3 -c "from server.world import ROOMS; print(len([r for r in ROOMS.values() if r.get('micro_presence')]))"
# Debe imprimir: 16

# Manual test: revisar que el texto aparece al ver una sala
# (requiere estar en el juego)
```

---

## 📞 Próximos Pasos

Después de este, implementar:
1. **ROUTE_LIVENESS** — narrativa en rutas
2. **WEATHER_LIVED_IN** — clima afecta descripciones
