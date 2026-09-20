# MatiasGameLab — Reglas de trabajo para agentes

Este repositorio es la fuente de verdad del juego de Senku. Antes de trabajar, leer el estado actual de `main` y este archivo. No trabajar desde copias antiguas del HTML.

## Principio central

Primero entender, después estructurar, después implementar. La diversión y claridad para el jugador tienen prioridad sobre la sofisticación técnica.

## Roles

### Javier + Matías — Dirección creativa
Deciden qué juego quieren, qué debe sentirse divertido, personajes, mundo, mecánicas, prioridades y qué entra o no entra. No necesitan traducir sus ideas a lenguaje técnico.

### Arquitecto — Coordinación
Convierte las ideas en decisiones claras y tareas delimitadas. Aclara intención, alcance, restricciones y criterios de aceptación; detecta contradicciones; decide cuándo hace falta investigación o implementación. No programa ni hace push por defecto.

### Codex / Cloud — Desarrollo
Puede trabajar directamente sobre el código del repositorio y tocar varios archivos cuando la tarea lo requiera: HTML, JavaScript, CSS, manifiesto, estructura y referencias a assets.
Debe:
- leer `main` antes de empezar;
- respetar la intención y alcance definidos por el Arquitecto;
- hacer cambios pequeños y comprensibles cuando sea posible;
- probar lo que modifica;
- no aprovechar una tarea pequeña para hacer una refactorización grande no solicitada;
- dejar recomendaciones adicionales como pendientes, no introducirlas silenciosamente;
- actualizar `HANDOFF.md` al terminar.

Codex/Cloud puede preparar cambios, pero la publicación/integración final corresponde al chat integrador.

### Chats de arte — Assets
Crean, editan, recortan, transparentan, renombran y suben imágenes. Su frontera es `assets/`.

Pueden crear subcarpetas dentro de `assets/` cuando corresponda.

NO deben modificar:
- `senku.html`
- `index.html`
- JavaScript o CSS
- `senku.webmanifest`
- lógica del juego
- archivos de coordinación fuera de `assets/`, salvo que una tarea lo autorice expresamente.

No deben borrar ni sustituir un asset existente salvo que la tarea indique explícitamente que es un reemplazo. Una ruta que ya usa el juego debe considerarse estable.

Al terminar, deben informar ruta exacta, dimensiones, formato, transparencia, uso previsto y, si aplica, frames/orden de animación.

### Chat integrador / publicación
Es el punto final de control. Revisa el estado real del repositorio y las entregas preparadas. Antes de publicar:
1. vuelve a leer `main`;
2. comprueba el HEAD base de la entrega;
3. detecta conflictos o cambios concurrentes;
4. verifica que existan los assets declarados;
5. revisa `HANDOFF.md`;
6. no reimplementa silenciosamente el trabajo de Codex.

Cuando Javier diga **"revisa lo que dejó Codex"**, revisa sin publicar.
Cuando Javier autorice **"sube"**, publica la entrega aprobada, verifica el nuevo HEAD y comprueba la versión pública/GitHub Pages.

## Arquitectura del proyecto

El juego principal es `senku.html`, un juego HTML/Canvas 2D orientado especialmente a teléfono/tablet.

Mantener el HTML ligero. No incrustar grandes imágenes Base64. El arte vive en `assets/`.

Estructura prevista:

```
assets/
├── backgrounds/
├── icon/
├── senku/
├── perro/
├── rata/
├── trajes/
├── enemigos/
├── npc/
└── objetos/
```

No crear carpetas vacías sólo por completar la estructura.

Para movimientos o animaciones experimentales, se recomienda un HTML de prueba ligero e independiente. Una vez aprobado visualmente, integrar el cambio mínimo necesario al juego real.

No reemplazar todo `senku.html` para cambiar una rata, perro, traje, fondo u otro detalle localizado.

## Trabajo paralelo

Arte y programación pueden avanzar en paralelo. Los chats de arte suben recursos a `assets/`; Codex/Cloud consume esas rutas desde el código. Evitar transportar ZIP, Base64 o copias completas de HTML entre agentes cuando el repositorio puede ser la fuente común.

Si dos trabajos dependen del mismo archivo o ruta, comprobar el HEAD antes de integrar. Nunca sobrescribir silenciosamente trabajo ajeno.

## Contrato de entrega de assets

Cada entrega de arte debe comunicar:

```
ENTREGA DE ASSETS — MATIASGAMELAB

Tipo:
[personaje / NPC / enemigo / objeto / fondo / traje / icono]

Objetivo:
[para qué se creó]

ARCHIVOS SUBIDOS

1.
Ruta: assets/...
Archivo: nombre.png
Tamaño: ancho × alto px
Formato: PNG/WebP/JPG
Transparencia: Sí/No
Uso previsto: ...

Animación:
[ninguna / número de frames / orden de frames]
[si es spritesheet: dimensiones totales y dimensiones por frame]

Estado:
LISTO PARA USAR: SÍ / NO

Observaciones:
[detalles que Codex deba conocer]
```

## Reglas de nombres y rutas

- Usar nombres claros, estables y consistentes.
- No añadir sufijos como `final2`, `nuevo-final` o similares a recursos que ya tienen una ruta funcional.
- Si se reemplaza el arte manteniendo la misma función, preferir conservar la ruta existente.
- Codex no debe asumir que un asset está bien sólo porque existe: los cambios visuales deben comprobarse en pantalla.

## Criterio de aceptación

Toda tarea debe poder verificarse. Para cambios visuales, indicar qué debe verse realmente en pantalla. Para cambios de comportamiento, describir acciones y resultado esperado. Las pruebas técnicas no sustituyen la prueba de juego de Javier y Matías.

## Fuente de verdad

GitHub/`main` es la fuente de verdad. Antes de modificar o integrar, leer el estado real del repositorio. No reconstruir el juego desde prototipos, copias viejas o bloques de HTML de otros chats.

## Comunicación

No pasar enormes bloques de `senku.html` entre chats salvo necesidad expresa. Usar rutas del repositorio y `HANDOFF.md` para el traspaso técnico.

Si una instrucción entra en conflicto con estas reglas o el estado real del repositorio, detener la integración y señalar el conflicto antes de sobrescribir trabajo.
