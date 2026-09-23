# Vintage Telnet — Canon visible para interfaz

**Responsable:** Historiador y Constructor del Mundo — Vintage Telnet  
**Origen:** Issue #76  
**Consumidores:** #72, #74 y #75

Este documento contiene texto público corto que la interfaz puede consumir sin reinterpretar el canon. No define mecánicas, CSS, secretos, rutas no descubiertas ni comportamiento del servidor.

## Reglas de uso

- Mostrar únicamente contextos que el servidor ya haya autorizado/descubierto.
- Los textos de especie describen identidad visible y corporal; no prometen bonificaciones numéricas.
- `forja`, `mercado` y `senderos` son vocabulario de mundo. Que exista el texto no implica que la acción/sistema esté disponible.
- No usar nombres de secretos, niveles inferiores de Vaisgard ni destinos no descubiertos como ayuda anticipada.
- Para armas visibles usar nombres de `WEAPON_CATALOG.md`: Varita de aprendiz, Puñal de camino, Arco de ruta, Espada de juramento, Hoja de Hoshai y Martillo de Korven.

## Tabla `context_id → texto visible aprobado`

| context_id | texto visible aprobado |
| --- | --- |
| `portal.vintage_telnet` | **Vintage Telnet** — Un mundo persistente de fantasía para explorar leyendo, observando y tomando decisiones. Elige tu especie, parte desde uno de los pueblos de inicio y descubre caminos, criaturas y lugares junto a otros jugadores. |
| `entry.login` | **Vuelve al mundo** — Entra con tu personaje y continúa desde donde quedó tu viaje. |
| `entry.register` | **Comienza tu viaje** — Crea tu acceso. Durante esta fase de pruebas, un personaje nuevo entra al mundo después de la aprobación del Dungeon Master. |
| `entry.wait_dm` | **Tu entrada está siendo preparada** — El Dungeon Master debe aprobar a los personajes nuevos antes de que comiencen su viaje. |
| `species.choose` | **Elige tu especie** — Tu especie cambia la forma natural de habitar y percibir el mundo, pero no decide por ti qué camino, oficio o estilo seguirás. |
| `species.human` | **Humano** — De fisiología generalista y sin una adaptación extrema, los Humanos se desenvuelven en entornos muy distintos mediante experiencia, herramientas y conocimiento. |
| `species.felaryn` | **Felaryn** — Humanoides de pelaje fino, orejas y cola felinas, gran visión y equilibrio preciso; su cuerpo está especialmente adaptado a alturas, saltos y terreno montañoso. |
| `species.dravak` | **Dravak** — Adultos compactos de cuerpo robusto y zonas dérmicas endurecidas de aspecto mineral; se desenvuelven con naturalidad entre roca, espacios reducidos y superficies fragmentadas. |
| `species.marevyn` | **Marevyn** — Altos y estilizados, con escamas parciales y una anatomía adaptada a vivir y desplazarse alrededor del agua sin ser una especie completamente acuática. |
| `species.vesperi` | **Vesperi** — Humanoides adaptados a ambientes de luz reducida, atentos a detalles que pueden perderse en la penumbra; no poseen vuelo natural. |
| `place.valdren` | **Valdren** — Pueblo abierto de caminos de tierra, madera, piedra y pequeñas parcelas. Es un lugar práctico y comunitario desde el que parten rutas hacia los Llanos de Edran y el resto del mundo. |
| `place.vaisgard` | **Vaisgard** — La ciudad principal del mundo conocido: antigua, multicultural y levantada en capas alrededor de la Cuenca de Veyra. Sus rutas reúnen viajeros, talleres, comercio y memorias anteriores a los cinco pueblos. |
| `place.valdren.center` | **Centro de Valdren** — Una pequeña plaza comunitaria entre viviendas, huertos y talleres básicos. Viajeros y noticias de otras regiones pasan con frecuencia por aquí. |
| `service.workshop` | **Forja y taller** — En los pueblos, estos espacios sirven para fabricar, reparar o comerciar armas, herramientas y otros trabajos permitidos por el mundo. |
| `service.market` | **Alimentos y comercio** — Bienes básicos, comida y productos de distintas regiones circulan por pueblos y caminos. En Vaisgard, el Mercado de las Rutas reúne mercancías de las cinco poblaciones. |
| `path.trails` | **Caminos y senderos** — Los pueblos están conectados por rutas que atraviesan regiones distintas. Observa antes de avanzar: huellas, cambios del terreno y señales del entorno pueden importar. |
| `help.explore` | **Explora** — Mira el lugar y examina aquello que llame tu atención. El mundo no revela todos sus caminos, señales o descubrimientos antes de que los encuentres. |
| `help.travel` | **Muévete** — Usa las direcciones disponibles para recorrer caminos ya accesibles. El mapa debe mostrar únicamente lugares y rutas que tu personaje haya descubierto. |
| `help.encounters` | **Encuentros** — Si aparece una criatura, observa el contexto antes de decidir. Evaluar, atacar o huir dependen de la situación y de las acciones que el mundo permita en ese momento. |
| `help.talk` | **Habla** — Cuando haya alguien con quien conversar, usa la acción disponible. Para hablar con otros jugadores, el chat utiliza `decir <texto>`. |
| `help.rest` | **Recupérate** — Descansar es una acción del personaje cuando el juego la permita. No todos los momentos o lugares ofrecen las mismas opciones. |
| `help.forge` | **Forja física** — Algunas mejoras importantes pueden requerir una pieza física para la figura del jugador. Ganarla no basta: debe fabricarse, colocarse y validarse antes de habilitar su uso. |

## Auditoría pública — vocabulario aprobado

### Entrada al mundo
Preferir **entrar al mundo**, **comenzar el viaje**, **personaje**, **Dungeon Master** y **especie**. Evitar presentar el flujo al jugador como “alta”, “workflow”, “estado de cuenta” o “aprobación administrativa”.

### Valdren y caminos
Valdren puede mostrarse como pueblo humano de inicio, plaza/centro comunitario, huertos, talleres básicos, caminos y presencia de viajeros. No convertirlo en capital, fortaleza, gremio ni sede de una autoridad nueva.

### Vaisgard
Puede mostrarse públicamente como ciudad principal, mercado multicultural, punto neutral y origen de las Cinco Rutas. Su antigüedad es pública; el contenido concreto de estructuras selladas o desconocidas no debe adelantarse.

### Taller y comercio
Los cinco pueblos pueden tener forja/taller, alimentos/comercio y centro comunitario. La interfaz no debe inferir precios, inventario, calidad, disponibilidad o efectos hasta que los sistemas correspondientes los autoricen.

### Senderos y descubrimiento
Usar lenguaje de **observar**, **examinar**, **señales**, **huellas**, **caminos** y **descubrimientos**. No anunciar de antemano rutas ocultas, criaturas no vistas o conclusiones que el jugador todavía debe deducir.

## Notas para #72 / #74 / #75

- **#72:** puede usar `help.*`, `service.*` y `path.trails` como microcopy; las condiciones de aparición siguen perteneciendo a Jugabilidad/servidor.
- **#74:** puede usar `portal.*`, `entry.*`, `species.*` y `place.valdren` para dar continuidad desde portal hasta entrada al mundo.
- **#75:** puede asociar visualmente `place.valdren` y `place.vaisgard` a assets aprobados mediante IDs estructurados; este documento no autoriza imágenes nuevas ni revela contextos no descubiertos.

**Estado:** ENTREGA CANÓNICA CONSUMIBLE — Issue #76.
