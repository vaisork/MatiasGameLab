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

### 001 — Perro de pie (sprite vacío)

Juego:
Senku

Solicitado por:
Claude — Desarrollador y Revisor de Senku

Estado:
SOLICITADO

Objetivo en el juego:
Sprite fijo del perro parado junto al autobús, en la escena de calle.

Recurso:
personaje

Requisitos conocidos:
- Tamaño o escala: ~96×65 px o un múltiplo prolijo (ej. 192×130)
- Formato: PNG
- Transparencia: Sí, fondo transparente real
- Frames/poses: 1 (de pie, sin animación)
- Dirección/orientación: la misma que usa hoy `dog-crouched.png`
- Referencias existentes: `assets/perro/dog-crouched.png` (mismo perro, mismo estilo/color café-canela, orejas caídas)
- Ruta relacionada en assets: `assets/perro/dog-standing.png`

Decisiones visuales ya aprobadas:
Debe ser el mismo perro que `assets/perro/dog-crouched.png`, solo que de pie.

Necesita material de Javier/Matías:
No

Entrega:
- Ruta final:
- Dimensiones:
- Formato:
- Frames/orden:

Observaciones:
El archivo `assets/perro/dog-standing.png` ya existe en esa ruta y el juego lo carga (`senku.html`, variable `dogStand`), pero el PNG está completamente transparente/vacío (sin dibujo). No es un recurso nuevo: es un reemplazo del contenido en la misma ruta y con el mismo nombre.

### 002 — Rata blanca del callejón (sprite sheet vacío)

Juego:
Senku

Solicitado por:
Claude — Desarrollador y Revisor de Senku

Estado:
SOLICITADO

Objetivo en el juego:
NPC de la rata escondida en la taquería (ciclo simple de espera/caminata).

Recurso:
NPC

Requisitos conocidos:
- Tamaño o escala: sprite sheet de 3 frames en fila, cada frame 160×136 px, hoja total 480×136 px exactos
- Formato: PNG
- Transparencia: Sí, fondo transparente real
- Frames/poses: 3, en fila horizontal (el código corta cada frame con `frame*160, 0, 160, 136`)
- Dirección/orientación: vista lateral, igual que el sheet actual
- Referencias existentes: ninguna equivalente — NO usar `assets/trajes/rata/walk-sheet.png` como referencia de color, esa es una rata gris distinta (traje secreto)
- Ruta relacionada en assets: `assets/rata/white-rat-sprite-v2.png`

Decisiones visuales ya aprobadas:
Rata blanca/clara (para diferenciarla visualmente de la rata gris del traje secreto).

Necesita material de Javier/Matías:
No

Entrega:
- Ruta final:
- Dimensiones:
- Formato:
- Frames/orden:

Observaciones:
El archivo `assets/rata/white-rat-sprite-v2.png` ya existe en esa ruta y el juego lo carga (`senku.html`, variable `ratSheet`), pero el PNG está completamente transparente/vacío (sin dibujo). No es un recurso nuevo: es un reemplazo del contenido en la misma ruta y con el mismo nombre. Aparte: `assets/asset-map.json` todavía referencia el nombre viejo `white-rat-sheet.png` en vez de `white-rat-sprite-v2.png` (que es el que usa `senku.html`); queda señalado acá pero no bloquea esta solicitud.
