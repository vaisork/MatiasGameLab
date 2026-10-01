# 🛤️ ROUTE_LIVENESS — Plan de Implementación

**Issue:** #558 (cola de Narrativa #284)  
**Ref:** vintage-telnet/ROUTE_LIVENESS_*.md (4 archivos por región)  
**Responsable:** VT (programador backend)

---

## 📋 Objetivo

Enriquecer salas de rutas (caminos entre pueblos) con texto que describe tránsito, mantenimiento y señales de viajeros.

**Ejemplo:**
```
Antes: "Camino de los campos. Tierra pisada."

Después: "Camino de los campos. Tierra pisada.
[Ruta] Una huella reciente cruza el lindero sin seguir ninguna cerca. 
El camino sigue siendo el paso más usado."
```

**Resultado:** Las rutas se sienten vivas sin crear NPCs nuevos. Pequeñas variaciones entre visitas.

---

## 🛠️ Implementación

### Dónde agregar

Archivo: `vintage-telnet/server/world.py`

En cada sala de ruta, agregar campo opcional:
```python
"route_liveness": "Texto descriptivo de evidencia de tránsito"
```

### Patrón

Cada sala es una **línea única** (observación física, nunca meta):

```python
ROOMS = {
    "valdren_lindero_tres_piedras": {
        "name": "Camino, lindero de tres piedras",
        "description": "...",
        ...
        # ⭐ NUEVO
        "route_liveness": "Una huella reciente cruza el lindero sin seguir ninguna cerca. El camino sigue siendo el paso más usado.",
    },
    # ... (más salas)
}
```

### Salas a actualizar (por región)

#### **Edran/Valdren** (9 salas)
Ref: `ROUTE_LIVENESS_EDRAN.md`

```
valdren_lindero_tres_piedras
valdren_camino_hundido
valdren_cobertizos_viejos
valdren_cruce_cercas
valdren_campo_rastrojo
valdren_zanja_vieja
valdren_arbol_descanso
valdren_campos_sin_cerca
valdren_vado_menor
```

#### **Veyra** (9 salas)
Ref: `ROUTE_LIVENESS_EDRAN.md` (parte 2)

```
campos_loma
campos_mojon
campos_camino_compartido
campos_colinas
campos_almacen
campos_vista_vaisgard
campos_camino_exterior
campos_acceso
cuenca_aproximacion_sur
```

#### **Hoshai** (salas TBD)
Ref: `ROUTE_LIVENESS_HOSHAI.md`

#### **Korven** (salas TBD)
Ref: `ROUTE_LIVENESS_KORVEN.md`

#### **Lethra/Nhal** (salas TBD)
Ref: `ROUTE_LIVENESS_LETHRA_NHAL.md`

---

### Mostrar en UI

Similar a ROOM_MICRO_PRESENCE, agregar a `describe_room()`:

```python
def describe_room(room_id, ...):
    room = get_room(room_id)
    ...
    
    description = room.get("description", "")
    
    # ⭐ NUEVO: Agregar liveness de ruta si existe
    if room.get("route_liveness"):
        description += f"\n[Ruta] {room['route_liveness']}"
    
    return {
        "id": room_id,
        "name": room["name"],
        "description": description,
        ...
    }
```

---

## ⚠️ Reglas a Respetar

- ✅ No nombrar personas
- ✅ No prometer que la señal estará siempre presente
- ✅ No crear atajos/rutas ocultas
- ✅ No convertir mantenimiento en quest
- ✅ No agregar rewards/comercio/fauna fija
- ✅ Ocultar si hay combate/escena scripted
- ✅ Daypart/clima pueden sustituir, no acumular (max 1 línea)

---

## 🧪 Testing

```bash
cd vintage-telnet

# Contar salas con route_liveness
python3 -c "from server.world import ROOMS; print(len([r for r in ROOMS.values() if r.get('route_liveness')]))"
# Debe ser ~37 salas (Edran + Veyra + Hoshai + Korven + Lethra/Nhal)

# Manual test: revisar texto en rutas clave
```

---

## 📋 Checklist

- [ ] Leer los 4 archivos ROUTE_LIVENESS_*.md
- [ ] Copiar textos exactos al diccionario ROOMS en world.py
- [ ] Agregar `route_liveness` a cada sala mencionada
- [ ] Verificar que no hay errores de sintaxis
- [ ] Actualizar describe_room() en app.py
- [ ] Testing: verificar que el texto aparece en UI

---

## 📞 Próximo Paso

Después de este, implementar:
- **WEATHER_LIVED_IN** — clima afecta descripciones
