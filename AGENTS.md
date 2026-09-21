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

### Investigador Técnico y de Implementación — Senku
Es el especialista de investigación técnica de Senku. Su función es estudiar **cómo conviene implementar** ideas o mejoras antes de que desarrollo programe cambios técnicamente inciertos, costosos o con varias soluciones posibles.

Puede investigar arquitectura y técnicas para movimiento 2D, Canvas, controles táctiles, animaciones, cámara, mapas, colisiones, audio, carga de assets, rendimiento móvil, guardado, PWA, organización del código y otras necesidades técnicas de Senku. Debe partir siempre del estado real del juego y priorizar soluciones apropiadas para su arquitectura actual sobre tecnologías innecesariamente complejas.

No decide qué juego quieren Javier/Matías, no sustituye al Arquitecto, no produce Pixel Art y no es el desarrollador ni publicador. Entrega investigación accionable: problema, estado actual, opciones, ventajas/desventajas, recomendación técnica, impacto, riesgos y forma de probarla.

**Cuándo consultarlo:** antes de implementar una mejora de Senku cuando no esté claro cómo hacerla, existan varias soluciones técnicas relevantes, pueda afectar arquitectura/rendimiento/compatibilidad móvil, o una mala decisión pueda obligar a rehacer trabajo después. Los cambios pequeños, obvios y ya definidos no necesitan pasar obligatoriamente por Investigación.

Cuando el Investigador entregue una recomendación, Claude/Codex puede utilizarla como base de implementación; el Arquitecto conserva la coordinación y Javier/Matías la dirección creativa.

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

Para planificar el crecimiento técnico de nuevos niveles o países de Senku, el Arquitecto y desarrollo deben consultar `SENKU_GROWTH_RESEARCH.md` cuando la tarea afecte estructura de escenas, reutilización de sistemas o incorporación progresiva de capacidades nuevas.

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

Arte y programación pueden avanzar en paralelo. Los chats de arte suben recursos a `assets/`; Codex/Cloud consume esas rutas desde el código. Evitar transportar ZIP, Base64, parches o copias completas de HTML entre agentes cuando el repositorio puede ser la fuente común.

Si dos trabajos dependen del mismo archivo o ruta, comprobar el HEAD antes de integrar. Nunca sobrescribir silenciosamente trabajo ajeno.

## Coordinación entre desarrolladores de Senku

Senku puede tener más de un desarrollador disponible. Son colaboradores al mismo nivel de coordinación; Javier asigna las tareas y decide quién trabaja en cada una.

- Una tarea tiene por defecto **un desarrollador responsable a la vez**.
- Antes de empezar, el desarrollador responsable comprueba `main` y las entregas recientes relevantes para no trabajar desde una versión antigua.
- Si toma el relevo de trabajo hecho por otro desarrollador, debe leer su rama/handoff y conservar las decisiones aprobadas.
- Cada desarrollador trabaja en su propia rama de entrega y deja trazabilidad suficiente para que el otro pueda entender qué cambió sin que Javier tenga que transportar código o explicaciones manualmente.
- Una entrega debe indicar, cuando aplique: **DESARROLLADOR**, **HEAD BASE**, **TAREA ASIGNADA**, **RAMA/COMMIT**, **CAMBIOS**, **PRUEBAS**, **TRABAJO PREVIO AFECTADO**, **PENDIENTES** y **AVISO PARA EL OTRO DESARROLLADOR**.
- Revisar el trabajo del compañero está permitido y se fomenta. Reemplazarlo silenciosamente no.
- Si ambos necesitan tocar la misma zona del juego por tareas distintas, deben señalar el posible conflicto antes de integrar.
- El Chat Integrador sigue siendo el punto final: una rama de cualquiera de los desarrolladores no pasa a `main` hasta la autorización de Javier.

## Protocolo de ramas para entregas de desarrollo

Los agentes de desarrollo pueden guardar y subir su trabajo al repositorio sin publicarlo en `main`. Para evitar que Javier tenga que transportar archivos, parches o copias de código entre chats, toda entrega de código preparada por un desarrollador debe preferir una **rama de trabajo/entrega**.

Flujo estándar:

1. El desarrollador lee y registra el HEAD actual de `main` antes de empezar.
2. Crea o utiliza una rama de entrega identificable para su tarea, por ejemplo `claude/senku-<tarea>` o `codex/<proyecto>-<tarea>`.
3. Puede hacer commits y push de su trabajo **únicamente a esa rama de entrega**.
4. Deja en la propia rama la documentación de entrega correspondiente, incluyendo el HEAD base, cambios, pruebas, pendientes y estado de publicación.
5. Comunica a Javier y al Chat Integrador el nombre exacto de la rama y el commit de entrega.
6. El Chat Integrador compara la rama contra el `main` actual, revisa conflictos y valida la entrega.
7. Solo cuando Javier autoriza **"sube"**, el Chat Integrador lleva los cambios aprobados a `main` y verifica la publicación.

**Hacer push a una rama de entrega NO equivale a publicar.** Los desarrolladores no deben hacer merge, push directo ni integración final a `main` salvo autorización expresa que cambie su función.

Si `main` cambió desde el HEAD base de la entrega, el Integrador debe detectar la divergencia antes de integrar. No debe sobrescribir silenciosamente ni pedir a Javier que transporte manualmente archivos si el trabajo ya puede compartirse mediante una rama del repositorio.

Este protocolo aplica a Claude, Codex/Cloud y futuros agentes que preparen código, salvo que su función específica establezca un flujo diferente.

## Flujo de desarrollo y Raspberry Pi — Vintage Telnet

Vintage Telnet utiliza el mismo principio de ramas de entrega, adaptado a su arquitectura de servidor persistente.

- GitHub/`main` es la fuente de verdad del código y la documentación.
- La Raspberry Pi es el entorno de ejecución del servidor y la autoridad del estado persistente vivo de jugadores y mundo.
- El **Desarrollador de Servidor — Vintage Telnet** prepara código en una rama de entrega y puede hacer commits/push a esa rama; no integra directamente a `main`.
- El agente que opere la **Raspberry Pi** despliega y prueba la entrega en el equipo real, revisa procesos, dependencias, logs, almacenamiento, puertos y persistencia, y devuelve resultados concretos al desarrollador/integrador.
- Desplegar una rama en la Raspberry para probarla **no significa aprobarla ni publicarla en `main`**.
- El agente de Raspberry no debe improvisar grandes cambios incompatibles al código para resolver problemas localmente. Si encuentra un defecto de desarrollo, documenta el error/log y lo devuelve al desarrollador para que la corrección quede registrada en el repositorio.
- Javier no debe actuar como transportista manual de parches o archivos entre estos agentes cuando la entrega pueda compartirse mediante una rama.

Flujo preferido:

`Desarrollador de Servidor → rama de entrega → Raspberry Pi despliega/prueba → resultados/logs → corrección si hace falta → Chat Integrador → main`

Antes de integrar, el Chat Integrador comprueba el HEAD base, el `main` actual, los resultados de prueba disponibles y cualquier conflicto. Solo con autorización de Javier para **"sube"** lleva la entrega aprobada a `main`.

El estado persistente vivo de la Raspberry (cuentas, posiciones, inventarios, progreso y estado compartido del mundo cuando existan) no debe tratarse como código para sobrescribirlo desde GitHub durante una actualización.

## Solicitudes de Pixel Art

`PIXEL_ART_REQUESTS.md` es la cola común de solicitudes visuales de MatiasGameLab. Aplica a Senku, Vintage Telnet y futuros juegos.

Cuando un agente de juego, diseño, narrativa, programación u otra especialidad necesite una imagen jugable:

1. Primero revisa `assets/` para comprobar si el recurso ya existe.
2. Si no existe, registra la necesidad en `PIXEL_ART_REQUESTS.md` con el contexto suficiente para que Pixel Art entienda qué se necesita, sin inventar decisiones que correspondan a Javier, Matías u otro especialista.
3. El agente de Pixel Art revisa esa cola como punto de entrada de trabajo y vuelve a comprobar los assets existentes antes de crear o pedir material.
4. Si para completar la solicitud hace falta una imagen original, referencia, fotografía, dibujo o decisión visual que deba proporcionar Javier/Matías, **Pixel Art se la pide directamente a Javier**. Javier no debe tener que adivinar qué archivo falta ni transportar solicitudes entre agentes.
5. Pixel Art prepara el recurso dentro de su frontera de trabajo, lo sube a `assets/` y actualiza la solicitud con la ruta exacta y el estado.
6. El agente solicitante consume la ruta del repositorio cuando el estado sea **LISTO EN ASSETS**.

Los agentes solicitantes no deben generar silenciosamente arte definitivo para saltarse este flujo. Pueden describir la función que debe cumplir el recurso, dimensiones o requisitos técnicos conocidos, pero la dirección creativa continúa perteneciendo a Javier/Matías y las decisiones propias de Pixel Art corresponden al agente de arte.

Estados estándar de una solicitud:

- **SOLICITADO** — necesidad registrada.
- **PENDIENTE DE JAVIER/MATÍAS** — Pixel Art necesita material o decisión de dirección creativa.
- **EN ARTE** — Pixel Art está preparando el recurso.
- **LISTO EN ASSETS** — recurso subido y ruta documentada.
- **BLOQUEADO** — existe una dependencia que impide continuar.
- **CANCELADO** — la necesidad dejó de existir.

`PIXEL_ART_REQUESTS.md` coordina trabajo; no sustituye los archivos de arte ni es una fuente de canon, jugabilidad o historia.

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

## Contratos individuales y lectura mínima

Los contratos firmados viven en `agentes/`. Este archivo conserva las reglas comunes y un índice corto.

Antes de trabajar, cada agente lee:
1. el HEAD vigente de `main`;
2. este `AGENTS.md`;
3. su propio contrato en `agentes/<identificador>.md`;
4. únicamente los contratos ajenos necesarios para entender una frontera concreta.

No es obligatorio cargar todos los contratos en cada onboarding.

La firma es un contrato operativo. Un agente no se autoasigna otra función ni modifica silenciosamente su propio alcance. Un cambio de función requiere instrucción de Javier y debe conservar la trazabilidad de la función anterior.

## Automatizar antes que delegar

Antes de asignar una tarea recurrente a un agente, comprobar si es mecánica y determinista.

- Si con la misma entrada debería producir el mismo resultado, preferir script, CI, servicio o comando reproducible.
- Si exige interpretar contexto, investigar, evaluar riesgo o decidir entre alternativas, corresponde a un agente.

Pruebas repetitivas, inspecciones deterministas y despliegues deben tender a automatización versionada. El agente interpreta fallos y excepciones; no debe gastar razonamiento repitiendo una secuencia mecánica que una máquina puede ejecutar.

## Índice de ramas

`RAMAS_ACTIVAS.md` es el índice operativo de ramas.

- Nunca confiar solo en el Markdown: contrastar con Git antes de actuar.
- Tras cada fusión a `main`, el arquitecto responsable del proyecto verifica inmediatamente sus filas.
- Una rama absorbida deja de figurar como activa.
- Si otra solución volvió obsoleta una rama pendiente, marcarla **SUPERADA** hasta decidir cierre o rescate.
- El Arquitecto de Senku mantiene las filas de Senku y recursos compartidos bajo su alcance.
- El Arquitecto de Vintage Telnet y Raspberry Pi mantiene las filas de Vintage Telnet.
- Mantener filas no transfiere autoridad entre juegos.
- `scripts/audit-branches.py` automatiza ahead/behind contra `origin/main`; decidir ACTIVA/SUPERADA/RESCATAR sigue requiriendo criterio.

## Pruebas proporcionales al riesgo

El nivel de prueba depende del riesgo del cambio, no de una suite uniforme.

Un cambio visual localizado no exige por defecto pruebas completas de servidor. Persistencia, autenticación, migraciones, seguridad y recuperación requieren validación profunda aunque el diff sea pequeño.

Nunca afirmar que una prueba pasó si no se ejecutó realmente. Si falta el entorno, registrar **PENDIENTE DE PROBAR**.

## Entrega y relevo

Toda tarea terminada deja en el repositorio: HEAD base, objetivo y alcance, archivos tocados, pruebas ejecutadas con resultado, pendientes, bloqueos y qué debe revisar el siguiente agente.

Javier no debe transportar manualmente prompts, parches o contexto técnico entre chats cuando GitHub puede conservarlo.

Para **Vintage Telnet**, los handoffs nuevos no deben reutilizar `HANDOFF.md` raíz. Cada entrega técnica usa `vintage-telnet/handoffs/<identificador-de-tarea>.md` o un documento equivalente específico de la entrega. Esto evita que dos ramas o dos juegos sobrescriban el mismo archivo de coordinación.

## Registro de agentes

| Identificador | Función | Proyecto | Estado | Contrato |
|---|---|---|---|---|
| `senku-integrador-publicador-html` | Chat integrador / Publicador HTML | Senku | ACTIVO | [contrato](agentes/senku-integrador-publicador-html.md) |
| `pixel-art-anterior-inactivo` | Chat de arte — Assets jugables | MatiasGameLab | INACTIVO — función entregada | [contrato](agentes/pixel-art-anterior-inactivo.md) |
| `pixel-art-assets-jugables` | Pixel Art y Assets Jugables — MatiasGameLab | MatiasGameLab | ACTIVO | [contrato](agentes/pixel-art-assets-jugables.md) |
| `arquitecto-senku-coordinacion-general` | Arquitecto de Senku y coordinación general | Senku / compartido | ACTIVO; fuera de Vintage Telnet | [contrato](agentes/arquitecto-senku-coordinacion-general.md) |
| `arquitecto-vintage-telnet-raspberry` | Arquitecto de Vintage Telnet y Raspberry Pi | Vintage Telnet | ACTIVO | [contrato](agentes/arquitecto-vintage-telnet-raspberry.md) |
| `jugabilidad-vintage-telnet` | Diseñador de Jugabilidad | Vintage Telnet | ACTIVO | [contrato](agentes/jugabilidad-vintage-telnet.md) |
| `historiador-vintage-telnet` | Historiador y Constructor del Mundo | Vintage Telnet | ACTIVO | [contrato](agentes/historiador-vintage-telnet.md) |
| `desarrollador-senku-claude` | Desarrollador y Revisor — Claude | Senku | ACTIVO | [contrato](agentes/desarrollador-senku-claude.md) |
| `investigador-senku` | Investigador Técnico y de Implementación | Senku | ACTIVO | [contrato](agentes/investigador-senku.md) |
| `desarrollador-junior-senku` | Desarrollador Junior — segundo desarrollador | Senku | PENDIENTE DE FIRMA | [contrato](agentes/desarrollador-junior-senku.md) |
| `integrador-html-vintage-telnet` | Integrador y Publicador HTML | Vintage Telnet | ACTIVO | [contrato](agentes/integrador-html-vintage-telnet.md) |
| `narrador-vintage-telnet` | Narrador de Aventuras | Vintage Telnet | ACTIVO | [contrato](agentes/narrador-vintage-telnet.md) |
| `investigador-vintage-telnet` | Investigador Técnico y de Implementación | Vintage Telnet | ACTIVO | [contrato](agentes/investigador-vintage-telnet.md) |
| `desarrollador-junior-vintage-telnet` | Desarrollador Junior | Vintage Telnet | ACTIVO | [contrato](agentes/desarrollador-junior-vintage-telnet.md) |
| `arte-html-vintage-telnet` | Arte HTML | Vintage Telnet | ACTIVO | [contrato](agentes/arte-html-vintage-telnet.md) |

