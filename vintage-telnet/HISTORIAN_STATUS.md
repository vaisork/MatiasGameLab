# Vintage Telnet — Estado del Historiador

Documento de coordinación para que el Arquitecto y otros agentes puedan conocer **qué está establecido, qué controla el Historiador y qué trabajo sigue abierto** sin reconstruir la conversación.

## Estado actual

Vintage Telnet está en fase de **construcción inicial del mundo**. Ya existen suficientes pilares para que el Historiador empiece a expandir ciertas áreas con autonomía, pero todavía hay componentes importantes que pueden beneficiarse de especialistas.

## Canon y dirección ya establecidos

- Fantasía mágica clásica.
- Mundo grande, persistente y multijugador.
- Ciudad principal: **Vaisgard**.
- **Vaisgard es anterior a los cinco pueblos**; las cinco poblaciones se asentaron primero allí y posteriormente fundaron sus pueblos propios.
- Dungeon Master: **Vaisork**.
- Cinco especies jugables actuales: **Humanos, Felaryn, Dravak, Marevyn y Vesperi**.
- Cinco pueblos pequeños de inicio:
  - **Valdren** — Humanos.
  - **Khariel** — Felaryn.
  - **Brumak** — Dravak.
  - **Narevia** — Marevyn.
  - **Velmora** — Vesperi.
- Las especies jugables no tendrán vuelo natural.
- Las referencias a animales, elfos u otras inspiraciones son herramientas internas de diseño y no se presentan así al jugador.
- No se utilizará la lista clásica humano/elfo/enano/etc. como base del reparto jugable; se crearán especies propias.
- Existen animales normales y seres llamados **Arcanes**.
- Existen magia oscura y necromancia; la necromancia está mal vista y su acceso jugable será avanzado.
- Algunas armas/mejoras importantes tendrán piezas físicas impresas y seguirán el sistema de Forja definido en `GAMEPLAY.md`.

## Autoridad delegada al Historiador

Javier autoriza al Historiador a:
- nombrar y diseñar pueblos principales y secundarios;
- desarrollar historia, geografía, acontecimientos, lugares, culturas, ruinas, conflictos, misterios y secretos dentro del canon confirmado, proporcionando la arquitectura histórica que después puede usar el Narrador;
- ampliar autónomamente contenido que no cambie los pilares fundamentales;
- establecer qué NPC necesita una historia y qué función debe cumplir, sin construir al NPC completo;
- identificar necesidades de mecánicas sin convertirlas unilateralmente en reglas.

Los asentamientos se documentan en `SETTLEMENTS.md`.

## Límites

El Historiador no sustituye:
- al Narrador, que convierte la historia y arquitectura del mundo en relatos, escenas, encuentros y experiencias concretas para los jugadores;
- al Diseñador de Jugabilidad para reglas, fórmulas, balance o progresión mecánica;
- al futuro Creador de NPCs;
- a programación, arte, publicación u otros especialistas;
- al Arquitecto cuando exista una duda de fronteras.

## Entregas a otros especialistas

- **Director de Arte / Issue #31 — anatomía de especies:** completada. Las cuatro especies no humanas ya pueden representarse en vista frontal/lateral/trasera sin que Arte tenga que inventar tipo de pie, estructura facial, escala, orejas o distribución esencial de rasgos.

- **Jugabilidad / VT-GAME-001 — Rasgos de especies:** aportación del Historiador entregada en `SPECIES.md`. La solicitud ya cuenta también con la aportación del Narrador.
- **Jugabilidad / VT-GAME-002 — Matriz de 8 atributos para juego de lectura:** revisión canónica entregada en `ATTRIBUTES_CANON_REVIEW.md`. Los ocho atributos son compatibles si no sustituyen especie, clase, conocimiento, poder, equipo ni decisiones de lectura del jugador.
- **Jugabilidad / Issue #55 — catálogo inicial de armaduras:** entregado en `ARMOR_CATALOG.md`. El Historiador fijó ocho identidades de equipo, procedencia cultural, obtención y uso de Forja física. Los valores 10/20/30/35 % quedan explícitamente como propuestas pendientes de validación de Jugabilidad; no se añadieron fórmulas, bonos de atributos, durabilidad ni resistencias nuevas.

## Entrega para presentación

- **Presentación pública de Vintage Telnet:** texto del Historiador preparado en `PRESENTATION_HISTORIAN.md`, sin spoilers ni secretos del Dungeon Master. Incluye mundo, Vaisgard, cinco pueblos/especies, exploración mediante lectura, atributos narrados y promesa de expansión.

## Handoff a Arte

- **Anatomía visual de especies — Issue #31 del Director de Arte:** cerrada con detalle suficiente para hojas frontal/lateral/trasera. Felaryn: pelaje real, rostro humanoide-felino sin hocico largo, apoyo digitígrado, pies de cuatro dedos, cola y orejas felinas; Dravak: 65–75 % de altura humana comparable, proporciones adultas, placas dérmicas minerales con distribución definida, pies plantígrados; Marevyn: 105–115 % de altura humana comparable, escamas parciales con zonas definidas, oreja corta de aspecto de aleta, manos/pies parcialmente palmeados; Vesperi: ojos muy grandes, cabeza superior ancha, orejas cortas redondeadas, brazos largos, piel mate, pies plantígrados y postura natural inclinada 10–15°. Fuente de verdad: `SPECIES.md`; resumen obligatorio para Arte: `ART_WORLD_GUIDE.md`.
- **Canon visual del mundo:** creado `ART_WORLD_GUIDE.md` como puerta de entrada obligatoria para ilustraciones de Vintage Telnet. Establece qué documentos debe leer Arte según la tarea, qué puede interpretar y qué debe devolver al Historiador en vez de inventar.
- **Arcanes:** creado `ARCANES.md` con su identidad visual/narrativa, separación de animales y criaturas, regla de nombre elegido por el jugador y ocho formas iniciales basadas en perro, gato, conejo, ave y ratón.

## Trabajo narrativo todavía abierto

Áreas importantes aún por desarrollar o repartir:
- diseño completo de **Vaisgard** — **primera versión completada en `VAISGARD.md`; queda abierta a expansión**;
- cultura e historia final de cada especie — **la anatomía necesaria para hojas anatómicas definitivas está cerrada en `SPECIES.md`; cultura e historia profunda siguen abiertas**;
- capacidades narrativas de Dravak, Marevyn y Vesperi — **primera definición completada en `SPECIES.md`; expansión posterior abierta**;
- mapa regional y conexiones entre los cinco pueblos y Vaisgard — **primera arquitectura definida en `REGIONS.md`**;
- historia antigua del mundo — **iniciada en `HISTORY.md`; faltan eras y causas anteriores/posteriores**;
- nombres y funciones de regiones;
- primeras mazmorras;
- monstruos y criaturas — **primera fauna regional y amenazas iniciales completadas en `CREATURES.md`; expansión posterior abierta**;
- clases, magias, objetos y armas desde su función narrativa — **armaduras: primer catálogo entregado en `ARMOR_CATALOG.md`; porcentajes pendientes de validación de Jugabilidad**;
- necesidades de NPCs;
- estructura de secretos y descubrimientos;
- expansión posterior con pueblos secundarios.

## Posibles especialidades que el Arquitecto puede evaluar

El Arquitecto puede decidir si alguna parte conviene separarla en agentes especializados, por ejemplo:
- **Creador de NPCs** — ya previsto.
- Especialista de especies/culturas.
- Diseñador de criaturas y monstruos.
- Diseñador de magia, objetos o armas.
- Cartógrafo/geógrafo del mundo.

Estos especialistas no son necesarios automáticamente. El Arquitecto decidirá si ayudan a mantener velocidad y claridad o si el Historiador debe conservar esas áreas.

## Documentos de referencia

- `WORLD.md` — índice narrativo.
- `CONFIRMED_IDEAS.md` — decisiones activas.
- `FUTURE_IDEAS.md` — incubadora de ideas no activas.
- `SETTLEMENTS.md` — pueblos y asentamientos.
- `HISTORY.md` — arquitectura histórica y cronología del mundo.
- `VAISGARD.md` — ciudad principal, estructura e historia.
- `REGIONS.md` — geografía inicial y caminos.
- `CREATURES.md` — fauna inicial, rastros y amenazas regionales; entrega para VT-NAR-002.
- `SPECIES.md` — rasgos naturales de las cinco especies; entrega del Historiador para VT-GAME-001.
- `SECRETS.md` — información reservada del Dungeon Master.
- `PRESENTATION_HISTORIAN.md` — texto público del mundo para la presentación.
- `ART_WORLD_GUIDE.md` — jerarquía y canon visual para Arte.
- `ARMOR_CATALOG.md` — primer catálogo canónico de armaduras; identidad/obtención/Forja definidas por Historia y porcentajes propuestos para revisión de Jugabilidad.
- `GAMEPLAY.md` — fuente de verdad mecánica.

---

**Estado:** listo para revisión del Arquitecto.  
**Responsable:** Historiador y Constructor del Mundo de Vintage Telnet.
