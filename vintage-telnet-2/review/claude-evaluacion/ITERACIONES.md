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
