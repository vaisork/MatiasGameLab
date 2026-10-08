# Evaluación narrativa por iteraciones (Prompt Maestro §6, §33–36)

Recorrido fijo, reproducible con `recorrido.py [hora]`: hogar → plaza de Valdren (quedarse 150 s, mirar al norte) → huertos → acequia (observar) → estanque → sauces → Vado de Juncos (examinar apoyos) → Lethra → plaza de Narevia (quedarse) → mercado (comprar) → senda, embarcadero, pasarela, ribera de cargas, cruce de canales, tablas → juncal (buscar) → ribera hacia Edran → salteador (hablar, combate) → regreso a Valdren.

Usa el motor real en memoria, con la composición del diario del cliente, sin base de datos ni partidas reales. Las notas son de lectura crítica, no de tests. Por debajo de 4 hay que trabajar.

## Iteración 1 — base `c65b2b8`, de día

| Categoría | Nota | Evidencia |
|---|---|---|
| Identidad espacial | 4 | Valdren, campos, puente y Narevia se distinguen sin el nombre. |
| Continuidad | **3** | Llegando desde Edran: «Detrás queda la senda de Narevia; por delante, un puente cruza hacia Edran», al revés del viaje. «A medida que te alejas de Narevia» mientras se camina hacia ella. |
| Ritmo | **3** | Casi todas las llegadas tienen 3–4 bloques largos; hay pocos silencios. |
| Vida ambiental | 4 | Ecos, gente trabajando, fauna en movimiento. |
| Densidad sensorial | 4 | Suelo, luz, sonido y olor en las descripciones largas. |
| Identidad regional | 4 | Edran (cercas, acequia) frente a Lethra (pasarelas, barcas). |
| Tiempo y clima | 3 | Sin comprobar de noche. |
| Exploración | **3** | Buscar devuelve «una huella antigua» sin más. |
| Encuentros | **3** | Un Saltalodo inofensivo aparece como [peligro]. |
| Memoria | 4 | Seña breve y regreso al volver. |
| Color semántico | **3** | El rojo de peligro se usa con fauna que no amenaza. |
| Curiosidad | 4 | |

**Problemas principales y cambios realizados:**
1. Perspectivas fijas en caminos de doble sentido. Son 30 frases en 26 salas, sustituidas por puntos cardinales sacados de las salidas reales («Al este queda la senda de Narevia; al oeste, un puente cruza hacia Edran»).
2. Una señal de una criatura sin perfil de combate se emite como `trace`, no como `danger` (`engine.narrative`, dos líneas).
3. «Iria» en el mercado de Narevia pasa a «una vendedora». Al vencer a un humano, «recuperas N sellos» pasa a «ganas N sellos».

## Iteración 2 — mismo recorrido, de día y de noche

- **Continuidad:** las direcciones son correctas en los dos sentidos. Nota: **4**.
- **Color:** las líneas de peligro bajan de 7 a 4, y ahora sólo las da el salteador. Nota: **4**.
- **Encuentros:** **4**. El salteador tiene motivo y voz, y el combate está narrado por arma.
- **De noche** apareció un fallo nuevo: los ecos y las vistas por dirección no tenían en cuenta la hora («golpes de martillo de la fragua» y gorriones a medianoche).
  - Cambio: los ecos admiten `requires_time`. Se clasificaron los 54 existentes y se añadieron 8 ecos nocturnos en plazas y mercados.
  - Se reescribieron 19 vistas por dirección para describir lo visible a cualquier hora.
  - Se cambió una paloma (ave real) por un Gorrión de ruta, de la fauna ambiental canónica.

| Categoría | Nota |
|---|---|
| Identidad espacial | 4 |
| Continuidad | 4 |
| Ritmo | **3** |
| Vida ambiental | 4 |
| Densidad sensorial | 4 |
| Identidad regional | 4 |
| Tiempo y clima | 4 |
| Exploración | **3** |
| Encuentros | 4 |
| Memoria | 4 |
| Color semántico | 4 |
| Curiosidad | 4 |

Pruebas: 150 tests OK; QA del cliente OK. `qa-mobile-controls` se reparó tras los cambios del mapa; `qa-contracts` necesita un fixture de navegador como argumento.

**Siguiente prioridad:**
- **Ritmo:** llegadas uniformes. Hay que dejar que algunos sitios respiren con una sola línea y concentrar la escena donde importa.
- **Exploración:** buscar y observar deberían revelar más cosas propias del lugar.
- **Repetición estructural:** «Reconoces la…» y «Recuerdas la…» abren 7 textos de regreso en un solo recorrido.

## Iteración 3 — ritmo, exploración y repetición

Cambios:
- **Regresos:** de 182 textos de regreso, 97 empezaban por «Reconoces/Recuerdas»; ahora quedan 10. Se reescribieron por lo que ha cambiado o por lo que el jugador ya sabe. La muletilla «sigue/siguen» que apareció al reescribir baja de 94 a 28.
- **Buscar:** cada región tiene ahora 8 rastros y 4 resultados vacíos, todos propios del lugar.
  - Antes: 2 rastros, uno de ellos la «huella antigua» genérica, compartida por todas las regiones.
  - Fauna canónica C0 por región (Liebre corta, Mariposa fría, Aguja azul, Ratona de hoja…).
  - Una pista de algo grande que pasó, sin nombrarlo, para despertar curiosidad.
  - Un objeto o una marca antigua que sugiere historia.
- **Ritmo:** con `max_layers`, las 17 salas salvajes o silenciosas muestran como mucho 2 capas y respiran; los 28 asentamientos admiten 4.
- **Luz:** 6 frases fijas que hablaban del sol aparecían de noche («calientes por el sol de la mañana», «terraza soleada»). Se reescribieron con una forma válida a cualquier hora.
- **Test:** `test_search_uses_both_authored_empty_and_trace_variants` calcula el índice con la misma regla proporcional que `Engine.search`, en vez de suponer listas de 2.

Comprobación:
- **Ruta A**, la de las iteraciones anteriores, de día: «Reconoces/Recuerdas» pasa de 11 apariciones a 2.
- **Ruta B**, de control y de noche, nunca usada para ajustar textos (Brumak → Refugio de Lajas → garganta → aprisco → pinar → Khariel):
  - Las búsquedas dan rastros distintos y propios del lugar; un Rasgacumbres aparece a lo lejos sin amenazar.
  - Los tramos salvajes son más cortos y Khariel es denso.
  - Tras la corrección de la luz, ningún texto de día aparece de noche.

| Categoría | Nota |
|---|---|
| Identidad espacial | 4 |
| Continuidad | 4 |
| Ritmo | 4 |
| Vida ambiental | 4 |
| Densidad sensorial | 4 |
| Identidad regional | 4 |
| Tiempo y clima | 4 |
| Exploración | 4 |
| Encuentros | 4 |
| Memoria | 4 |
| Color semántico | 4 |
| Curiosidad | 4 |

Pruebas: 150 tests OK; QA del cliente OK.

Pendiente: algunas búsquedas repiten el mismo rastro dos veces seguidas. El motor no evita la repetición inmediata; mejorarlo exige tocar código y queda para la próxima iteración.

## Iteración 4 — lectura larga y clara: dónde estoy, qué hago

Petición: que en cada lugar la lectura sea larga, constante, interesante y agradable para todos, y que se note mejor dónde estamos y qué estamos haciendo.

Cambios:
- **Se retira el tope de 2 capas** de la iteración 3. `max_layers` cuenta también la descripción, así que dejaba las zonas salvajes en descripción más una sola capa. Vuelven al valor por defecto (3); los asentamientos mantienen 4.
- **Qué estoy haciendo:** 38 textos de llegada (`arrivals`) nuevos.
  - Cubren los 22 cruces entre regiones y todas las entradas a las plazas de cada pueblo.
  - Antes había 21 textos de llegada para 392 caminos.
  - El texto de llegada se lee **antes** de la descripción: primero el movimiento («Subes el último escalón… y te encuentras en la plaza de Khariel»), después el lugar.
- **Dónde estoy:** cada región tiene una bienvenida (`regions.<id>.entry`), escrita para niños.
  - Se muestra la primera vez que entras en la región, antes de todo lo demás.
  - Se decide sin guardar estado nuevo: sólo mira si ya visitaste otra sala de esa región.
  - Test: `test_region_entry_only_on_first_step_into_region`.
- **Claridad:** 197 capas de ambiente (día, noche, amanecer, atardecer y lluvia) reescritas en lenguaje concreto.
  - Se retiran frases abstractas o de manual («La diferencia entre cauce conducido y escorrentía mantiene su importancia», «sin forzar una revelación para cerrar la velada»).
  - Se mantienen el contenido, los personajes y la hora de cada capa.
- **Fauna canónica:** las 12 ranas pasan a Saltalodo, el anfibio del bestiario; la lagartija pasa a Escarabajo de polvo. El objetivo «examinar rana» pasa a «examinar saltalodo».

Comprobación:
- Ruta A, de día: 119 palabras por llegada (antes, 117).
- Ruta B, de control y de noche: 147 palabras por llegada (antes, 137).
- En las dos, la entrada en Lethra y en Hoshai empieza con la bienvenida de la región, y las plazas empiezan contando cómo llegas.

Pruebas: 151 tests OK; QA del cliente OK.

Pendiente: quedan 354 caminos sin texto de llegada; siguiente tanda, los caminos de la ruta principal dentro de cada región.
