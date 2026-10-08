# 🎨 Guía de Generación de Arte — Vintage Telnet

Flujo completo para generar y publicar arte que aparezca correctamente en el juego.

## ⚠️ ANTES DE EMPEZAR

**Cada ficha de arte JSON DEBE tener `visual_context_id`** para que la imagen aparezca en el juego.

- **Locations (paisajes)**: Tienen `visual_context_id` que mapea a una zona (ej: `zone.nhal`, `zone.korven`)
- **Creatures (criaturas)**: NO tienen `visual_context_id` (usan otro sistema)

---

## 📋 PASO 1: Crear la ficha JSON

Archivo: `vintage-telnet/art_requests/<nombre>.json`

### Estructura mínima:
```json
{
  "asset_id": "claro_niebla_baja",
  "asset_type": "location",  // ← "location" o "creature"
  "target": "Paisaje para el Claro de Niebla Baja",
  "canonical_name": "Claro de la Niebla Baja",
  "art_direction": "SUBJECT TYPE: LOCATION / ENVIRONMENT. Describir el lugar...",
  "prompt": "Create one landscape environment scene...",
  "references": [],
  "negative_constraints": ["No creatures", "No magic"],
  "aspect_ratio": "1536x1024",
  "output_destination": "vintage-telnet/art_generations",
  "status": "draft",
  
  // ⭐ CRÍTICO: Sin esto NO aparece en el juego
  "visual_context_id": "zone.nhal",
  
  "quality": "low",
  "output_format": "png",
  "background": "opaque"
}
```

### ¿Cómo elegir `visual_context_id`?

Zonas disponibles en `vintage-telnet/server/world.py`:
```
zone.valdren             → Valdren general
zone.valdren.forja_daro  → Forja de Daro específicamente
zone.khariel            → Khariel general
zone.khariel.terraza_comunitaria → Terraza específicamente
zone.brumak             → Brumak general
zone.brumak.patio_recepcion → Patio específicamente
zone.narevia            → Narevia general
zone.narevia.mercado_acuatico → Mercado específicamente
zone.velmora            → Velmora general
zone.velmora.forja_taller → Forja específicamente
zone.velmora.cruce_reunion → Cruce específicamente
zone.nhal               → Nhal general
zone.nhal.claro_cielo_estrecho → Claro específicamente
zone.hoshai             → Hoshai general
zone.hoshai.garganta_lajas → Garganta específicamente
zone.hoshai.paso_alto   → Paso Alto específicamente
zone.korven             → Korven general
zone.edran              → Edran general
zone.edran.primeros_juncos → Primeros juncos específicamente
zone.lethra             → Lethra general
zone.lethra.canal_bajo_islas → Canal específicamente
zone.veyra              → Veyra general
zone.veyra.road         → Camino específicamente
```

**REGLA:** Si es una location, DEBE tener `visual_context_id`. Si es creature, NO incluir.

---

## 🎬 PASO 2: Generar la imagen

En la Raspberry:

```bash
./run-art-generator.sh
```

**Qué pasa:**
1. ✅ Corre `generate_all_art.py`
2. ✅ Llama a OpenAI Image API
3. ✅ Guarda PNG en `art-masters/{creatures,locations}/`
4. ✅ Convierte a WebP y guarda en `assets/vintage-telnet/{creatures,locations}/`
5. ✅ Muestra instrucciones para el siguiente paso

**Archivos generados:**
```
art-masters/locations/claro_niebla_baja_hq.png
  ↓ (convertido a WebP)
assets/vintage-telnet/locations/claro_niebla_baja.webp
  ↓ (será sincronizado por vt-deploy)
```

---

## 🚀 PASO 3: Deploy a producción

En la Raspberry:

```bash
sudo vt-deploy main
```

**Qué pasa automáticamente:**
1. ✅ Valida que main está limpio
2. ✅ Corre 767+ tests del servidor
3. ✅ Hace backup de la base de datos
4. ✅ Cambia la versión en producción
5. ✅ **AUTOMÁTICO:** Sincroniza todos los WebP de `assets/vintage-telnet/` al servidor
6. ✅ Verifica que el servidor esté sano

**Sincronización (línea 377-398 de vt_deploy.py):**
```
Copia: assets/vintage-telnet/locations/*.webp
    → /opt/vintage-telnet/current/assets/vintage-telnet/locations/

Copia: assets/vintage-telnet/creatures/*.webp
    → /opt/vintage-telnet/current/assets/vintage-telnet/creatures/
```

---

## 🎮 PASO 4: Aparece en el juego

Cuando el servidor sirve la sala:

```python
# vintage-telnet/server/world.py

VISUAL_CONTEXT_ART = {
    "zone.nhal": {
        "src": "/assets/locations/claro_niebla_baja.webp",  # ← Que acabas de publicar
        "alt": "Claro de la Niebla Baja",
        "width": 1536,
        "height": 1024,
    },
    ...
}
```

**Flujo en-game:**
1. Jugador entra a sala en Nhal
2. `world.describe_room("nhal_plaza")` 
   → Detecta `visual_context_id = "zone.nhal"`
   → Busca en `VISUAL_CONTEXT_ART["zone.nhal"]`
   → Retorna `src: "/assets/locations/claro_niebla_baja.webp"`
3. Servidor sirve `/assets/locations/claro_niebla_baja.webp`
4. HTML renderiza `<img class="location-art" src="/assets/locations/claro_niebla_baja.webp">`
5. ✨ La imagen aparece en pantalla

---

## ❌ ERRORES COMUNES

### ❌ Error: "La imagen no aparece en el juego"

**Causa probable:** Falta `visual_context_id` en la ficha JSON

**Solución:**
1. Abre `vintage-telnet/art_requests/<nombre>.json`
2. Agrega `"visual_context_id": "zone.nhal"` (o zona corresponda)
3. Guarda
4. Vuelve a ejecutar `sudo vt-deploy main`

### ❌ Error: "visual_context_id no existe"

**Causa probable:** Escribiste mal el zone ID

**Solución:**
Verifica que exista en `vintage-telnet/server/world.py` línea 41-179

### ❌ Error: "La imagen se ve borrosa/mala en el juego"

**Causa probable:** El WebP se generó con mala calidad

**Solución:**
1. Aumenta `quality` en la ficha JSON: `"quality": "high"` o `"quality": "max"`
2. Regenera con `./run-art-generator.sh`
3. Deploy nuevamente

### ⚠️ Creatures no aparecen con imagen

**Nota:** Las criaturas usan otro sistema de arte (no locations). No usan `visual_context_id`.
Si una criatura tiene `visual_context_id`, **QUÍTALO** que romperá el mapeo de zonas.

---

## 📊 Checklist antes de hacer deploy

- [ ] Ficha JSON tiene `visual_context_id` (si es location)
- [ ] El `visual_context_id` existe en `world.py`
- [ ] El WebP se generó correctamente en `assets/vintage-telnet/locations/` o `creatures/`
- [ ] Corri `./run-art-generator.sh` localmente y completó sin errores
- [ ] No hay cambios sin commitear en git
- [ ] Ejecuté `sudo vt-deploy main` y completó exitosamente
- [ ] La imagen aparece en el juego cuando juego en esa zona

---

## 🛠️ Scripts de utilidad

### Ver qué assets faltan en world.py:
```bash
python3 tools/vt_art/sync_assets_to_world.py
```

### Auto-mapear fichas a zonas:
```bash
python3 tools/vt_art/apply_visual_context_mappings.py
```

### Validar que los assets publicados están correctos:
```bash
python3 tools/vt_art/validate_published_assets.py
```

---

## 📞 Preguntas?

Si una imagen no aparece:
1. Revisa que tiene `visual_context_id`
2. Revisa que existe en `world.py`
3. Revisa que el WebP existe en `assets/vintage-telnet/`
4. Corre `python3 tools/vt_art/sync_assets_to_world.py`

Si el deploy falla:
1. Revisa que main está limpio: `git status`
2. Revisa que los tests pasan: `cd vintage-telnet && python3 -m unittest discover -s tests`
3. Revisa los logs del deploy: `sudo journalctl -u vintage-telnet.service`
