# MatiasGameLab — Solicitudes de Pixel Art

Esta es la cola común para recursos visuales jugables que todavía necesitan trabajo de Pixel Art.

Antes de añadir una solicitud, revisar `assets/` y las solicitudes existentes para evitar duplicados. Las reglas completas están en `AGENTS.md`.

## Cómo solicitar un recurso

Copiar esta plantilla al final del documento:

```
### [ID o nombre breve] — [recurso]

Juego:
[Senku / Vintage Telnet / otro]

Solicitado por:
[agente o función]

Estado:
SOLICITADO

Objetivo en el juego:
[para qué se necesita]

Recurso:
[personaje / NPC / enemigo / objeto / fondo / traje / icono / animación / otro]

Requisitos conocidos:
- Tamaño o escala:
- Formato:
- Transparencia:
- Frames/poses:
- Dirección/orientación:
- Referencias existentes:
- Ruta relacionada en assets:

Decisiones visuales ya aprobadas:
[solo decisiones realmente aprobadas]

Necesita material de Javier/Matías:
[Sí / No / Por determinar]

Entrega:
- Ruta final:
- Dimensiones:
- Formato:
- Frames/orden:

Observaciones:
[dependencias, dudas o contexto]
```

## Reglas de estado

- **SOLICITADO** — esperando revisión de Pixel Art.
- **PENDIENTE DE JAVIER/MATÍAS** — Pixel Art debe pedir directamente el material o decisión que falta.
- **EN ARTE** — recurso en preparación.
- **LISTO EN ASSETS** — archivo subido; la solicitud debe incluir la ruta exacta.
- **BLOQUEADO** — indicar qué dependencia bloquea.
- **CANCELADO** — indicar brevemente por qué.

## Solicitudes activas

### senku-dog-standing-rework — Perro de la calle, pose "de pie"

Juego:
Senku

Solicitado por:
Claude — Desarrollador y Revisor de Senku

Estado:
LISTO EN ASSETS

Objetivo en el juego:
Sprite que se muestra cuando Senku se acerca al perro de la banqueta en la escena Calle (cambia de agachado a de pie).

Recurso:
Personaje/NPC

Requisitos conocidos:
- Tamaño o escala: se dibuja escalado a máx. 150×105px conservando proporción; el archivo actual mide 96×65px.
- Formato: PNG con transparencia.
- Frames/poses: pose única "de pie" (sin animación).
- Dirección/orientación: igual que `dog-crouched.png` (misma escena, mismo punto de anclaje).
- Referencias existentes: `assets/perro/dog-crouched.png` (esta sí funciona bien, sirve de referencia de calidad/estilo).
- Ruta relacionada en assets: `assets/perro/dog-standing.png` (reemplazar en el mismo archivo).

Decisiones visuales ya aprobadas:
Ninguna — hay que empezar de cero. Se revisaron las 3 versiones que ha tenido este archivo en el historial del repo y **ninguna sirve**:
- `f504221` (la más reciente): corrupta — dos fragmentos diminutos en esquinas opuestas del lienzo, centro transparente.
- `d03f203` ("reemplazo con versión limpia"): completamente en blanco/transparente.
- `2ce3f94` (original, dos poses): la cabeza se ve bien pero el cuerpo tiene ruido de píxeles corrupto.
`dog-crouched.png` sí es una referencia válida de calidad/estilo a seguir.

Necesita material de Javier/Matías:
No.

Entrega:
- Ruta final: `assets/perro/dog-standing.png`
- Dimensiones: 96×65 px
- Formato: PNG con transparencia
- Frames/orden: pose única "de pie"; sin animación

Observaciones:
El archivo `assets/perro/dog-standing.png` fue eliminado del repo (no existía ninguna versión funcional en el historial a la cual revertir). El próximo agente de Pixel Art debe crearlo desde cero, no restaurar una versión anterior. Verificado abriendo cada PNG directamente en navegador a escala 5x, fuera del juego — no es un problema de cómo el juego los usa, los archivos en sí estaban dañados.

---

### senku-rat-sprite-rework — Rata blanca de la taquería (NPC)

Juego:
Senku

Solicitado por:
Claude — Desarrollador y Revisor de Senku

Estado:
LISTO EN ASSETS

Objetivo en el juego:
Sprite animado de la rata escondida en la Taquería (escena `taco`), NPC que entrega el traje secreto.

Recurso:
NPC / animación

Requisitos conocidos:
- Tamaño o escala: cada frame 160×136px; el juego recorta 3 frames de 160px de ancho consecutivos.
- Formato: PNG con transparencia.
- Frames/poses: 3 frames para animación de espera/parpadeo (secuencia usada en `drawRat()`: `[0,0,0,1,2,1,0,0]` en reposo, `[0,1,2,1]` cuando Senku está cerca).
- Dirección/orientación: sin archivo de referencia en el repo ahora mismo (ver Observaciones) — pedir a Javier/Matías una referencia visual si hace falta.
- Referencias existentes: ninguna en `assets/` (se eliminaron las 3 que había, ver Observaciones).
- Ruta relacionada en assets: el código lee un spritesheet combinado en `assets/rata/white-rat-sprite-v2.png` (480×136px = 3 frames de 160px pegados). El plan más simple es entregar así: **un solo PNG de 480×136px con los 3 frames pegados en fila**, mismo nombre de archivo. Si se prefiere entregar 3 archivos sueltos (por ejemplo `rata_1.png`, `rata_2.png`, `rata_3.png` de 160×136px cada uno), avisar en esta entrada y Claude actualiza `senku.html` para leerlos así en vez del spritesheet.

Decisiones visuales ya aprobadas:
Ninguna — se pide el set completo desde cero, sin partir de ningún archivo existente.

Necesita material de Javier/Matías:
No — Javier proporcionó directamente los 3 frames visuales el 2026-09-20.

Entrega:
- Ruta final: `assets/rata/white-rat-sprite-v2.png`
- Dimensiones: 480×136 px; 3 frames de 160×136 px
- Formato: PNG con transparencia
- Frames/orden: izquierda→derecha: Frame 1, Frame 2, Frame 3

Observaciones:
Se revisaron los 4 archivos de rata que había en el repo abriéndolos directamente en navegador, fuera del juego (no era un problema de cómo el juego los usa, los archivos en sí estaban dañados):
- `assets/rata/white-rat-sprite-v2.png` (el spritesheet que lee el código) y su duplicado `white-rat-sheet.png` — completamente transparentes/en blanco. Sin historial de una versión buena.
- `rata_1.png` (commit `9ccdbd1`) — este sí se veía bien, pero por instrucción de Javier se eliminó también para que la entrega completa se rehaga de cero, sin mezclar con trabajo del agente anterior.
- `rata_2.png` (commit `e86f085`/`16b4172`) — completamente transparente/en blanco.
- `rata_3.png` (commit `b01d86c`) — corrompido/fragmentado: pedazos sueltos (orejas, cola) y una línea de píxeles de colores random abajo, no una rata completa.
Los 4 archivos se eliminaron del repo. El próximo agente de Pixel Art debe producir los 3 frames nuevos sin ningún archivo de referencia existente en `assets/rata/`.

## Diagnóstico temporal — flujo de subida de Pixel Art

Solicitado por:
Investigador Técnico y de Implementación — Senku

En la **próxima entrega real de Pixel Art**, antes de cambiar el procedimiento actual, documentar brevemente cómo se está haciendo hoy la subida al repositorio y dónde se consume más tiempo.

Responder al terminar esa próxima subida:

1. ¿Cuántos archivos se subieron en esa entrega?
2. ¿Los PNG se reciben uno por uno, en lote, carpeta o ZIP?
3. ¿Qué pasos manuales se realizan desde que Javier entrega la imagen hasta que queda en `assets/`?
4. ¿Se recorta, transparenta, redimensiona o renombra cada imagen individualmente?
5. ¿Cómo se suben actualmente a GitHub: un archivo/commit por vez, varios archivos en un solo commit, u otro método?
6. ¿Qué paso concreto tarda más?
7. ¿Hay esperas debidas al chat/herramienta, procesamiento de imagen, descarga/subida de archivos, validación o GitHub?
8. Aproximadamente, ¿qué parte del proceso podría hacerse por lote sin perder la validación visual?
9. Si hubo algún error, límite de herramienta o motivo por el que no pudo hacerse en lote, indicarlo exactamente.

**Importante:** esta petición es de diagnóstico. En esa próxima entrega no hace falta cambiar el flujo ni experimentar con una nueva automatización salvo que Javier lo pida. Primero necesitamos medir el proceso real.

Una vez respondido este diagnóstico, el Investigador Técnico podrá proponer una mejora concreta para reducir el tiempo de subida sin comprometer nombres, transparencia, orden de frames ni rutas existentes.



## Diagnóstico de subida — entrega rata blanca 2026-09-20

1. Archivos subidos: 1 spritesheet final, construido a partir de 3 PNG entregados juntos por Javier.
2. Recepción: lote de 3 PNG en el mismo mensaje.
3. Pasos: revisar solicitud y HEAD; inspeccionar dimensiones; retirar únicamente el fondo oscuro conectado al borde conservando contornos; recortar; normalizar cada pose a 160×136; mantener línea de apoyo consistente; componer los 3 frames en fila; conservar transparencia; reducir a pixel-art por vecino más cercano; validar dimensiones; subir el PNG y documentar la ruta.
4. Los tres originales necesitaron preparación y se procesaron como lote con las mismas reglas.
5. GitHub: spritesheet y documentación en un solo commit.
6. Paso más costoso: transparencia y encuadre consistente de los tres originales.
7. Esperas: principalmente procesamiento/validación de imagen; GitHub no fue el cuello principal.
8. Recorte, transparencia, escalado, alineación y composición pueden hacerse por lote; conservar validación visual final.
9. Limitación: los originales llegaron RGB sin alfa y fondo negro; borrar todo negro dañaría el contorno. Se eliminó solo el fondo oscuro conectado al borde.
