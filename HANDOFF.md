# HANDOFF — Entrega técnica

Este archivo es el contrato de traspaso entre Codex/Cloud y el chat integrador. Codex/Cloud debe actualizarlo al terminar una entrega de programación. El integrador debe leerlo y contrastarlo con el estado real del repositorio antes de publicar.

## ENTREGA PARA CHATGPT

**Estado:** ENTREGA LISTA PARA REVISIÓN

### Estado base
Commit/HEAD sobre el que se trabajó:
`bb2fef58ee1607d216e3bbc77b3d623489d24e9b` (confirmado igual a `origin/main` justo antes de esta entrega — sin cambios concurrentes)

### Objetivo
Revisión general de Senku solicitada por Javier: detectar problemas técnicos, corregir los seguros/claros directamente, e implementar dos ajustes de jugabilidad que Javier pidió explícitamente (churus no duplicables, taza que cae en Casa).

### Archivos modificados
- `senku.html`
- `AGENTS.md` (solo para registrar y firmar mi función; no toca reglas de otros agentes)

### Archivos nuevos
- Ninguno.

### Assets utilizados o añadidos
- Ninguno. Todos los cambios son de código, no de arte.

### Cambios realizados
1. **Bug de HUD:** había un `\n` literal (texto, no salto de línea real) entre el botón de casa y el de trajes, presente desde el 18-sep (v0.5.0–v0.5.2). Se veía como texto suelto "\n" en el HUD. Corregido con salto de línea real.
2. **Duplicación injusta de churus (pedido por Javier):** los churus de calle/taquería y la caja secreta se podían volver a recolectar cada vez que se reiniciaba el juego, porque el contador total se guardaba en localStorage pero qué churus ya se habían agarrado no. Ahora cada churu/caja tiene un id estable y se guarda en `localStorage.senku_collected` cuáles ya se dieron; no se vuelven a otorgar. El juego sigue reiniciando en Casa cada vez (así lo pidió Javier, sin guardar posición/escena). También corregido que la caja secreta podía darse +3 churus repetidamente parado ahí sin cerrar el juego.
3. **Taza que cae en Casa (pedido por Javier):** la taza (círculo amarillo dentro de la ventana) estaba fija en el aire. Ahora cae con la misma gravedad que el salto de Senku hasta el piso real de la habitación (no la repisa de la ventana) y se queda ahí. Tarda ~0.65s en caer. Solo aplica a la escena Casa.

### Actualización posterior a esta entrega (mismo HEAD base, misma rama)
Javier pidió, por el momento, revertir solo la parte de persistencia del cambio #2: quiere que el conteo de churus **arranque siempre en 0** al cargar el juego, en vez de recordar entre sesiones lo ya recolectado. Cambio mínimo y acotado a esa petición:
- `churus` y `collected` ya no se inicializan leyendo `localStorage.senku_churus` / `localStorage.senku_collected`; siempre inician en `0` / vacío al cargar la página.
- Dentro de una misma sesión (sin recargar), un churu/caja ya recolectado sigue sin poder volver a darse — eso no cambió.
- `selectedSkin` y `secret` (traje/rata secreta) siguen persistiendo igual que antes; no se tocó esa parte a propósito (Javier pidió solo este cambio).
- `save()` no se modificó: sigue escribiendo `senku_churus`/`senku_collected` en `localStorage`, pero ya no se leen al iniciar, así que quedan sin efecto por ahora. Se puede limpiar ese guardado muerto si Javier confirma que este es el comportamiento definitivo y no algo temporal.
- Nota: esto no resuelve el pendiente del traje "Gato dorado" (300 churus) — lo deja igual de inalcanzable, ya que el máximo por sesión sigue siendo 10.

### Segunda actualización posterior (mismo HEAD base, misma rama)
Javier pidió el mismo tratamiento para el traje secreto de la rata: que el desbloqueo tampoco persista entre cargas del juego.
- `secret` (si ya se desbloqueó el traje de la rata) ya no se inicializa leyendo `localStorage.senku_secret`; ahora siempre arranca en `false` al cargar la página. Hay que volver a encontrar a la rata en la taquería en cada sesión para desbloquearlo.
- No hizo falta tocar nada más: si `selectedSkin` guardado en `localStorage.senku_skin` era `'secret'`, la lógica ya existente en `renderWardrobe()` (`if(selectedSkin==='secret'&&!secret)selectedSkin='normal'`) lo regresa solo a `'normal'` cuando `secret` es `false`.
- `save()` tampoco se tocó: sigue escribiendo `senku_secret` en `localStorage`, pero ya no se lee al iniciar, igual que pasó con los churus.
- El traje "Gato dorado" y la selección general de traje (`selectedSkin`) no se tocaron fuera de este efecto en cascada.

### Pruebas realizadas
- Parseo del HTML completo sin errores tras cada cambio.
- Parseo/ejecución del JS embebido con Node (`new Function(...)`) sin errores de sintaxis tras cada cambio.
- Simulación en Node de dos sesiones de juego (recolectar todo → "reiniciar" → volver a entrar a calle): confirmado que el contador de churus no vuelve a subir en la segunda sesión.
- Simulación de la caída de la taza: llega al piso en 0.65s y se detiene exactamente en el borde (sin atravesarlo).
- Reconstrucción pixel-exacta de la escena "Casa" (mismas coordenadas/colores del código) en imagen estática, antes y después de la caída, para confirmar visualmente que la taza no choca con el clóset ni la mesa y no se queda flotando.

### Prueba visual para Javier/Matías
1. Abrir Senku, entrar a Casa: la taza debe caer desde la ventana hasta el piso en menos de un segundo y quedarse ahí quieta (ya no debe verse pegada arriba en el vidrio).
2. Revisar el HUD arriba a la derecha: ya no debe aparecer texto "\n" suelto entre el botón de casa y el de trajes.
3. Jugar hasta agarrar todos los churus de calle + la caja secreta + los de taquería, anotar el total. Cerrar el juego (recargar la página) y volver a jugar toda la ruta: el contador NO debe subir de nuevo con los mismos churus/caja.

### Pendiente
- **Importante para diseño:** con el nivel actual, el máximo de churus obtenibles de forma legítima es 10 (4 calle + 3 caja + 3 taquería). El traje "Gato dorado" cuesta 300 churus y, con el bug de duplicado corregido, **ya no es alcanzable** con el contenido actual. Antes solo se conseguía explotando el bug. Requiere decisión de Javier/Matías: más fuentes de churus, o bajar el costo del traje, o dejarlo como meta futura para cuando haya más escenas.
- `assets/asset-map.json` desactualizado (referencia `white-rat-sheet.png`, el código usa `white-rat-sprite-v2.png`). No afecta el juego, solo la documentación.
- `ctx.roundRect()` (usado para dibujar los churus) no existe en iOS < 16; no lo toqué sin autorización porque implica agregar una rama de compatibilidad al código de dibujo. Puedo agregar un fallback de una línea si Javier lo autoriza.
- `save()` no tiene try/catch alrededor de `localStorage`; en navegación privada podría fallar silenciosamente. No lo toqué sin autorización.
- Assets sin usar en el repo (`white-rat-sheet.png`, `rata_sprite.svg`, `secret-rat-menu.webp`): le corresponde al chat de arte decidir si se limpian.
- `index.html` enlaza a `vintage-telnet.html`, que no existe todavía en el repo. Fuera de mi alcance (Senku); lo señalo nada más.

### Riesgos/conflictos
- Ninguno detectado: `main` no cambió desde el HEAD base durante esta entrega.
- Los cambios son acotados (líneas puntuales, sin reestructurar `senku.html`), reversibles y no tocan `assets/` ni `vintage-telnet/`.

**LISTO PARA PUBLICAR:** SÍ, con la salvedad del pendiente del "Gato dorado" — no rompe nada, pero Javier/Matías deberían decidir qué hacer con ese traje antes o después de publicar, como prefieran.

---

## Plantilla obligatoria para próximas entregas

```
ENTREGA PARA CHATGPT

Estado base:
[commit/HEAD sobre el que se trabajó]

Objetivo:
[qué pidió el Arquitecto]

Archivos modificados:
- ...

Archivos nuevos:
- ...

Assets utilizados o añadidos:
- ruta exacta → uso

Cambios realizados:
- ...

Pruebas realizadas:
- ...

Prueba visual para Javier/Matías:
1. ...
2. ...

Pendiente:
- ...

Riesgos/conflictos:
- ...

LISTO PARA PUBLICAR: SÍ / NO
```

Si `main` cambió respecto al Estado base, el integrador debe detectar y revisar el conflicto antes de publicar. No sobrescribir silenciosamente cambios posteriores.
