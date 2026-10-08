# Estándar de narrativa MUD clásica: propuesta y prueba acotada (Valdren)

Es una propuesta, no un cambio aplicado. No se modificaron `content/`, `server/` ni `client/`, y no se desplegó nada. Todo lo de esta carpeta se puede reproducir:

| Archivo | Qué es |
|---|---|
| `hoshai_propuesta.json`, `korven_propuesta.json`, `lethra_propuesta.json`, `nhal_propuesta.json` | Las cuatro regiones restantes: 29, 32, 27 y 27 salas, con sus estados. |
| `veyra_propuesta.json` | Las 24 salas de Veyra, incluidos los estados de los toldos y de la colina (niebla, lluvia y noche). |
| `edran_propuesta.json` | Las otras 32 salas de Edran con el mismo estándar, más 3 estados y 9 textos de regreso que repetían la descripción. |
| `valdren_propuesta.json` | Texto nuevo para las 12 salas de Valdren: `description` permanente y `brief` (seña breve). También reescribe un estado. |
| `hacer_parche.py` | Genera los dos parches desde el código actual. Falla si Codex cambió el código que se parchea. |
| `renderer.patch` | Ajuste mínimo de `server/engine.py` (37 líneas). |
| `cliente.patch` | Línea «Salidas:» en `client/ui-data.js` (1 línea). |
| `prueba.py` | Copia el proyecto a un directorio temporal, aplica los parches y el texto, recorre rutas con el motor real, pasa los tests y las QA del cliente, y mide. |
| `salida/` | Las 6 transcripciones (día y noche × 3 configuraciones) y `metricas.json`. |

## 1. Auditoría de Edran (44 salas)

| Medida | Resultado |
|---|---|
| Longitud de las descripciones | media de 40 palabras (22–70); solo 4 fuera de 30–65. La longitud **no** es el problema. |
| Frases que solo enumeran salidas | **69 de 185 (37 %)**. Repiten los botones de movimiento. |
| Descripciones permanentes con un NPC en acción | 6: «Daro trabaja…», «Iria guarda…», «Bren guarda…», «Elva sirve…», «…y Daro al norte», «Oren…». El texto fijo afirma algo que depende de que esa persona esté. |
| Solapes entre la descripción y las capas de hora/regreso | 2 (canal). Bajo. |
| **Repetición al jugar** | El cliente imprime la escena **completa en cada llegada**, también al volver. En 26 movimientos por Valdren, la plaza salió entera 7 veces y la calle 5. **El 52 % de las palabras leídas ya se habían leído antes.** |

Conclusión: el texto de Edran ya es bastante concreto. Lo que lo vuelve pesado es el **renderizado**: repetir la escena completa al volver, enumerar salidas en prosa y mezclar quién está aquí con la descripción fija.

## 2. Separar lo permanente de lo dinámico

| Capa | Campo | Cuándo se lee |
|---|---|---|
| Lugar permanente | `description` (30–65 palabras): qué se ve siempre, qué lo distingue, qué hay alrededor | Primera llegada y cada **Mirar** |
| Seña breve (nueva) | `brief` (≤ 15 palabras): lo que permite reconocer el sitio en un segundo | Al **volver caminando** |
| Hora y clima | `day`/`night`/`dawn`/`dusk`, `rain`/`weather` | Capa variable. En una revisita, una sola que rota |
| Personas | NPC `day`/`night` | Fuera del presupuesto de capas. En una revisita: «Daro está aquí.» |
| Memoria | `return`, `memories` | Capa variable. Nunca anuncia presencia |
| Peligro | `signals`, `wildlife_pool` | Siempre gana |
| Navegación | `exits` → «Salidas: norte (Calle de la fragua), sur.» | Una vez por llegada. Sólo nombra destinos ya visitados. |
| Detalle | `examine`, Observar | A petición |

Reglas de escritura para `description`:
- Sin listas de salidas. Se pueden nombrar *lo que se ve o se oye* en otra dirección («calle arriba se oye la fragua»), no la lista.
- Sin NPC actuando.
- Sin hora ni clima.

## 3. Antes y después

**Plaza, primera llegada**
> **Antes:** Un banco largo cruza la plaza. Hay espacio para girar los carros sin tapar las puertas. La fragua queda al norte, los huertos al este, el pozo al sur y el cobertizo al oeste. Una piedra sobresale entre las tablas del asiento.
>
> **Después:** La plaza de Valdren se abre entre casas bajas y deja sitio para que un carro gire sin tapar ninguna puerta. Un banco largo la cruza de lado a lado, interrumpido por una piedra que asoma entre las tablas: nadie quiso arrancarla. Calle arriba se oye la fragua.
> *Salidas: norte, este, sur, oeste.*

**Plaza, volviendo por cuarta vez (transcripción real del arnés, de día)**

Antes:
> Llegas a Plaza de Valdren.
> Un banco largo cruza la plaza. Hay espacio para girar… (descripción completa otra vez)
> La vecina aparta una semilla mordida…
> Reconoces el extremo del banco por la piedra que obliga a interrumpirlo. La fragua queda detrás de las casas más altas…

Después:
> Llegas a Plaza de Valdren.
> La plaza de Valdren, con su banco largo partido por una piedra.
> El cuenco del banco traquetea bajo su tapa. La lámpara oscila junto al corredor…
> *Salidas: norte (Calle de la fragua), este, sur, oeste.*

**Fragua (texto fijo)**
> **Antes:** Daro trabaja entre el fuego y un barreño de agua. … La salida sur baja por la calle hacia la plaza.
>
> **Después:** Dentro hace calor. El fuego ocupa el fondo, junto a las herramientas calientes, y un barreño de agua espera a su lado. Las piezas terminadas se apoyan junto a la puerta. El centro queda libre para pasar sin rozar nada. Huele a carbón y a hierro.
>
> Daro sigue presente mediante su capa de persona y el nombre de la sala.

## 4. Ajustes mínimos de renderizado

`renderer.patch`, en `server/engine.py`:
1. **Modo breve:** al llegar caminando a una sala ya visitada que tenga `brief`, se muestra la seña breve más **una** capa viva. Esa capa es el peligro si lo hay; si no, rota con el número de visitas entre hora, clima, recuerdo y llegada. **Mirar** siempre da la descripción completa. Una sala sin `brief` se comporta como hoy, así que se puede adoptar sala por sala.
2. `state['arrival']` se limpia en cada acción aceptada, después de validarla. Una acción rechazada no cambia nada, como ya exigen dos tests.
3. Quién está aquí queda fuera del límite de capas, para que no lo desplace el clima. En modo breve se lee «Bren está aquí.». Esa línea se omite sólo si la capa elegida es del presente y ya nombra a esa persona; un recuerdo que la nombra no cuenta.
4. `brief` se puede sobrescribir desde `states`.

`cliente.patch`, en `client/ui-data.js`: al llegar, una línea «Salidas: …» construida con las acciones `mover` que ya envía el servidor. Se pone en el cliente para no cambiar el contrato de capas del motor: hay un test que exige exactamente 3 líneas de escena.

## 5. Pruebas (motor real, base de datos en memoria, sin partidas reales)

Recorrido:
- 26 movimientos por las 12 salas de Valdren, con revisitas.
- Mirar, Observar y Examinar en sala visitada.
- Salida a los campos con un Espinajo presente y combate completo hasta resolverse.
- Regreso a la plaza.
- Todo de día (10:00) y de noche (22:00).

| Configuración | Palabras leídas | Palabras repetidas | Combate | Regreso |
|---|---|---|---|---|
| Hoy, de día | 3070 | 1611 (52 %) | resuelto | plaza |
| Renderizador propuesto, texto actual, de día | 3021 | 1611 | resuelto | plaza |
| **Renderizador y texto propuestos, de día** | **2053 (−33 %)** | **538 (−67 %)** | resuelto | plaza |
| Hoy, de noche | 2978 | 1577 | resuelto | plaza |
| **Renderizador y texto propuestos, de noche** | **2029 (−32 %)** | **548 (−65 %)** | resuelto | plaza |

Notas sobre las cifras:
- No incluyen las líneas «Salidas:», que se cuentan aparte como navegación.
- Sin `brief`, el renderizador apenas cambia la lectura (−2 %): es seguro adoptarlo antes de reescribir salas.

Comprobaciones de no regresión con los dos parches aplicados:
- `unittest discover`: **141 tests, OK**. Es el mismo resultado que sin parche.
- `qa-narrative.mjs`, `qa-printing.mjs` y `qa-passive.mjs`: **PASS**.

## 6. Información conservada

`prueba.py` compara las palabras con contenido de cada descripción original con todo el texto visible de la sala propuesta. Las que no aparecen literalmente se revisaron una a una:

- **Paráfrasis**: espacio → sitio, girar → gire, sobresale → asoma, vueltas → boca abajo, distintos → no son iguales, permiten rodearlos → para poder hablar por encima.
- **Salidas**: salida, plaza, sur, volver, vuelve. Ahora están en «Salidas:».
- **Acciones de NPC**: trabaja, sirve. Ahora están en la capa de personas.

No se perdió ningún hecho del canon: el banco interrumpido por una piedra anterior, las dos puertas de los graneros, el patio inclinado y la separación de paños de Sena siguen ahí. Tampoco se perdió ninguna relación espacial que no esté cubierta por «Salidas:» o por algo visible desde la sala.

## 7. Límites y siguiente paso

- No se ha probado en el navegador. El arnés reproduce en Python la lógica de `NarrativeJournal.consume`; las QA del cliente pasan, pero falta ver la línea «Salidas:» en 320 px.
- La rotación en modo breve depende del número de visitas, no del tiempo. Dos llegadas seguidas nunca dan la misma capa si hay más de una disponible.
- Para extenderlo a todo Edran hacen falta 32 salas más: un `brief` cada una y quitar las enumeraciones de salidas (69 frases). Después, una región por bloque, con la misma prueba.
- Para integrar, primero `renderer.patch` y `cliente.patch` (sin efecto visible en salas sin `brief`), y después el texto por regiones.
- No hay ningún despliegue en la Raspberry: eso queda pendiente de autorización.

## 8. Extensión a todo Edran (44 salas)

`edran_propuesta.json` completa la región. `prueba.py` une las dos propuestas y, después del recorrido de Valdren y del combate, visita **todas** las salas de Edran por el camino más corto y vuelve a la plaza.

| Configuración | Palabras | Repetidas | % repetido | Salas | Movimientos fallidos |
|---|---|---|---|---|---|
| Hoy, de día | 15 273 | 10 904 | 71 % | 44/44 | 0 |
| **Propuesta, de día** | **8 359 (−45 %)** | **3 999 (−63 %)** | 48 % | 44/44 | 0 |
| Hoy, de noche | 15 012 | 10 744 | 72 % | 44/44 | 0 |
| **Propuesta, de noche** | **8 258 (−45 %)** | **3 962 (−63 %)** | 48 % | 44/44 | 0 |

Con los parches: 141 tests OK, y `qa-narrative`, `qa-printing` y `qa-passive` en PASS.

Las cifras base son más altas que en la sección 5 por dos motivos: el recorrido es más largo y Codex cambió `content/` entre las dos ejecuciones. Cada comparación se hace siempre sobre el mismo contenido.

**Qué se sigue repitiendo:**
- La cabecera «Llegas a…» del cliente, que es navegación.
- Las señas breves, que se repiten a propósito porque es la forma clásica de reconocer un sitio.
- El ambiente rotatorio en las salas que tienen una sola capa.
- **Las señales de fauna genéricas**: unas 740 palabras, casi todas «Entre los tallos viejos se arquea un lomo…». Las corrige el bloque C de `TEXTOS.md`, que todavía no está integrado. Con él, la repetición baja más.

**Rangos de las descripciones nuevas:**
- 23–56 palabras, con una media de 41.
- Cuatro salas quedan por debajo de 30: la hondonada, el refugio del canal, la compuerta y la repisa. Son rincones sin salida y es una excepción intencionada.
- Las señas breves tienen 15 palabras como máximo.

**Hechos que la revisión manual de cobertura obligó a reponer:**
- El agua actual de la zanja corre por otra parte de la parcela.
- La senda de regreso da un rodeo, así que no sale enfrente de donde entra. Es una aclaración de orientación pedida antes para evitar confusiones.

**Dinámico que se sacó del texto fijo:**
- «Una mujer está comprobando su entrada» (zanja).
- «Oren sostiene una taza…» (refugio). Ya lo dice la capa de personas.

**Siguiente paso:** el mismo proceso por regiones, en este orden: Veyra (24 salas), Hoshai, Korven, Lethra y Nhal. Cada una con su propuesta y la misma prueba.

## 9. Veyra (24 salas) y recorrido conjunto

`prueba.py` carga ahora todos los `*_propuesta.json` y recorre todas las salas de las regiones propuestas. Si una puerta pide permiso, usa la acción de permiso que ya existe en el juego.

| Edran + Veyra (68 salas) | Palabras | Repetidas | % repetido | Salas | Fallidos |
|---|---|---|---|---|---|
| Hoy, de día | 24 670 | 17 307 | 70 % | 68/68 | 0 |
| **Propuesta, de día** | **14 161 (−43 %)** | **6 893 (−60 %)** | 49 % | 68/68 | 0 |
| Hoy, de noche | 24 219 | 16 997 | 70 % | 68/68 | 0 |
| **Propuesta, de noche** | **13 855 (−43 %)** | **6 724 (−60 %)** | 49 % | 68/68 | 0 |

Con los parches: 141 tests OK y la QA del cliente en PASS.

**Pérdida que encontró la prueba de cobertura:** al quitar las listas de salidas también se perdía hacia qué región lleva cada salida (Hoshai, Lethra, Nhal, Korven). Con un destino todavía sin visitar, la línea «Salidas:» no da nombre, así que esa pista de orientación sólo estaba en la descripción. Está repuesta en 9 salas, en forma de algo que se ve: «por aquí sale el camino de la sierra de Hoshai», «aquí empieza el bosque de Nhal».

Hay un control automático que comprueba que ninguna descripción propuesta deja de nombrar una región o pueblo que la original nombraba como destino. Las únicas excepciones son las menciones de la región en la que ya estás.

**También sale del texto fijo** lo que hacían los NPC: «una mensajera organiza avisos…» (plaza y patio de mensajes). Ahora lo dice la capa de personas.

**Coherencia con los secretos:** el patio de mensajes conserva el hueco entre el armazón y la pared antigua, que es la pista del secreto I5.

## 10. Mundo completo (183 salas, 6 regiones)

Ahora hay propuesta para **todas** las salas del juego. `prueba.py` recorre las 183, más Valdren, el combate y el regreso, de día y de noche.

| Mundo completo | Palabras | Repetidas | Salas | Fallidos |
|---|---|---|---|---|
| Hoy, de día | 110 555 | 89 576 (81 %) | 183/183 | 0 |
| **Propuesta, de día** | **53 632 (−51 %)** | **33 384 (−63 %)** | 183/183 | 0 |
| Hoy, de noche | 109 391 | 89 069 (81 %) | 183/183 | 0 |
| **Propuesta, de noche** | **52 805 (−52 %)** | **33 031 (−63 %)** | 183/183 | 0 |

Con los parches: 141 tests OK; `qa-narrative`, `qa-printing` y `qa-passive` en PASS.

**De dónde sale la reducción.** Las descripciones en sí sólo bajan un 8 % (de 7 852 a 7 236 palabras, con una media de 39 por sala). La reducción grande viene de otros dos cambios:
- Al volver a una sala no se repite la descripción: se lee la seña breve, que tiene 8 palabras de media.
- Las salidas ya no se cuentan en prosa.

El primer contacto con cada lugar sigue siendo una escena completa.

**El porcentaje de repetición sigue alto (62 %) por cómo es el recorrido.** La ruta automática pasa por las plazas y los cruces decenas de veces para llegar a las 183 salas, y cada paso imprime la cabecera «Llegas a…» y la seña breve. Una partida normal pasa mucho menos por el mismo sitio.

**Controles finales:**
- **Destinos:** ninguna descripción deja de nombrar una región o pueblo de destino que la original nombraba. El control excluye sólo las menciones de la región en la que estás. Este control obligó a reponer 15 vistas hacia otras regiones o hacia atrás («Detrás queda la senda de Narevia», «Abajo queda Velmora»…).
- **Longitud:** todas las descripciones tienen menos de 65 palabras. Hay 17 por debajo de 30: rincones sin salida, cuartos de cuidados, almacenes y pausas como la Orilla de las aves. Se dejan cortas para que el ritmo cambie entre sitios grandes y sitios pequeños.
- **NPC:** se sacaron del texto fijo Taren, Mira, Sola, Leris, Elin, Arel y las acciones de otros personajes sin nombre. Ahora los muestra la capa de personas.
- **Secretos:** se mantienen las pistas que usan.
  - La taza (en el texto nocturno de la fragua).
  - El hueco del armazón (patio de mensajes).
  - «No ves el fondo» (orilla del canal).
  - La piedra del claro y los bancos del patio (Nhal).
  - El dibujo de la Ladera de las señales (Hoshai).

**Lo que falta:**
- La revisión humana de las 183 descripciones. La prueba garantiza que funcionan y que no se pierden datos, no que se lean bien.
- Probar el cliente en el navegador a 320 px.
- Que Codex integre, región por región.

**Orden recomendado de integración:** primero los dos parches, que no cambian nada visible en las salas sin `brief`. Después una región, una partida de prueba, y la siguiente.

## 11. Combate: cada arma se mueve distinto (`combate.patch`)

Es un parche de **sólo narración** sobre `server/mechanics.py`, generado por `hacer_parche.py`.

| Arma | Al acertar | Al fallar | Golpe final |
|---|---|---|---|
| Espada | tajos, paradas con la hoja, estocadas | 4/3 variantes | 1 |
| Puñal | entradas rápidas, amagos, golpes cortos | 4/3 | 1 |
| Arco | tensar, apuntar, disparar con prisa | 4/3 | 1 |
| Varita | impulso, concentración, círculo en el aire | 4/3 | 1 |

- Las defensas tienen texto propio: esquivar, bloquear y resistir, con 3 variantes cada una.
- Si aparece un arma nueva que no está en la tabla, se elige el texto por sus propiedades: a distancia, foco o bloqueo.
- La variante sale del número de ronda. **No se consume azar**: daño, precisión y probabilidades no cambian. Lo verifiqué con la misma semilla y las cuatro armas: salen los mismos números y sólo cambian los movimientos.
- Con los tres parches aplicados: 141 tests OK. El parche se aplica sin conflictos sobre la base desplegada (`vt2-mud-piloto`).
- `combatReading` del cliente deja pasar estos textos tal cual, porque sólo reescribe las frases genéricas antiguas.

## 12. Escenas que avanzan al volver (`escenas_visita.json`)

Son 11 lugares de mucho paso:
- Valdren: plaza, calle de la fragua, pozo, huertos y salida.
- Las plazas de las otras cinco regiones y el mercado de Vaisgard.

Cada lugar tiene **4 formas de contarse de día** (base, visita 3, 5 y 8) y **3 de noche** (base, visita 3 y 6). Cada una es una pequeña historia que avanza con las visitas:
- El niño de la plaza acaba descubriendo qué pájaro come sus semillas.
- La semilla de la niña del mercado brota.
- El viajero humano de Khariel aprende a saltar como los Felaryn.

Detalles de integración:
- Sólo usa `states` con `requires_visits` y `requires_time`.
- `insertar_en` coloca cada escena después de las variantes de visita que ya existen y antes de las de clima o misión. La lluvia, el viento, la niebla, la nieve y las consecuencias de los encargos siguen mandando.
- Se verificó en memoria contra la base desplegada: 4 formas de día y 3 de noche en las 11 salas, en cualquier clima que no tenga escena propia.

## 13. Lo aprovechable de las herramientas MUD (Diku/Circle/Merc/ROM)

**Para enriquecer la lectura, sin tocar números:**
1. **Mensajes de daño según la fuerza del golpe** (los `dam_message` de Diku/Merc): el verbo crece según cuánta vida quita el golpe («rozas», «alcanzas», «golpe tremendo»). Es sólo narración. Siguiente parche recomendado.
2. **Ataques propios de cada criatura** (el tipo de ataque de los mobs): el Espinajo embiste con las espinas, el Mordelinde muerde y se escabulle, el Cornalomo cornea. Hoy todas dicen «X te alcanza». Sería un campo de contenido por criatura más una línea de código.
3. **Mirar en una dirección** (las descripciones de salida `D` de las áreas Diku): `mirar norte` describe lo que se ve hacia allí sin revelar el destino. Orienta mucho. Necesita código pequeño.
4. **Detalles ocultos** (las extra descriptions `E`): ya existen como `examinar`. Hay que escribir más palabras clave escondidas para los secretos.
5. **Ecos ambientales mientras te quedas en un sitio** (los room echoes de ROM): microescenas que aparecen sin moverte. Necesita un temporizador en el cliente o en el servidor.
6. **Presencia de las criaturas** («Un Espinajo te observa desde los tallos»): ya está cubierta por las señales.

**Necesita contrato de Jugabilidad antes de tocarlo:** tipos de daño con resistencias (ROM), THAC0/AC, ranuras de equipo, dados de arma y pérdida al morir. La propia investigación lo marca así.

### 11b. Intensidad del golpe y ataques de cada criatura

- **Intensidad del acierto**, según la parte de la vida máxima del rival que quita el golpe:
  - menos del 10 %: «Apenas rozas a…»
  - menos del 20 %: «Alcanzas a…»
  - menos del 30 %: «¡Das de lleno a…!»
  - el resto: «¡Golpe tremendo! … se tambalea».

  Así, la misma flecha de nivel 1 «apenas roza» a un Cornalomo y «da de lleno» a un Espinajo. El niño entiende sin números lo grande que es cada rival.
- **Ataque propio de cada criatura** (`CREATURE_PROSE`): 3 maneras de acertar y 2 de fallar para cada una.
  - El Espinajo embiste con las espinas.
  - El Mordelinde muerde los tobillos.
  - El Cornalomo cornea.
  - El Dorsalodo barre con el agua.
  - El Rasgacumbres lanza zarpazos.
  - El Quebrarrocas empuja como una pared.
  - El Rasgacorteza golpea con brazos de madera.
  - El Cascapedernal golpea con el caparazón.
  - El salteador usa el palo.

  Usa el nombre que se ve en pantalla, así que Seran conserva su nombre. Una criatura sin entrada en la tabla mantiene la frase actual.
- **Dónde se aplica:** en el combate individual (`combate.patch`, sobre `mechanics.py`) y en el compartido (`combate_motor.patch`, sobre `engine.tick_shared`).
- **Comprobado sobre la base desplegada (`vt2-mud-piloto`):** los dos parches entran limpios y pasan los 145 tests.
- `renderer.patch` ya no entra en esa base porque Codex integró su propia versión del modo breve. Se mantiene sólo como referencia.

## 14. Versión larga y sensoria de las 183 salas (petición de Javier)

Javier pidió lugares «mucho más largos», que se sientan como una historia de sentidos y dejen imaginar. Se reescribieron las descripciones de los siete archivos `*_propuesta.json` y los estados que sustituyen una descripción.

Cada descripción cuenta:
- lo que se ve;
- lo que se oye;
- lo que se huele;
- lo que se toca o la temperatura;
- un poco de la historia del sitio.

Siguen sin listas de salidas, sin personajes trabajando y sin hora ni clima fijados. Las revisitas muestran la seña breve más hasta tres capas vivas que van rotando (`renderer.patch`).

**Extensión:**
- Media por región: Valdren 84 palabras, resto de Edran 72, Veyra 65, Hoshai 59, Korven 54, Lethra 54 y Nhal 52.
- Total del mundo: de 7 852 a 11 237 palabras de descripción (+43 %).
- Los rincones pequeños se quedan cortos a propósito, para que el ritmo cambie.

**Recorrido completo** (183/183 salas, de día):

| | Hoy | Propuesta |
|---|---|---|
| Texto nuevo de verdad | 21 357 | **25 990 (+22 %)** |
| Texto repetido | 89 522 | **69 355 (−23 %)** |

Con los parches: 141 tests OK; `qa-narrative`, `qa-printing` y `qa-passive` en PASS.

**Controles:**
- Ningún destino de otra región se pierde.
- Las pistas de los secretos siguen en el texto: «no ves el fondo», el hueco del patio de mensajes y la piedra del claro.

La repetición que queda viene sobre todo del ambiente de las revisitas. La reducen las escenas por visita (`escenas_visita.json`, 11 lugares); el siguiente paso es extenderlas a más salas.

## 15. Segunda tanda de escenas por visita (`escenas_visita_2.json`)

Son 27 lugares más, unos cuatro por región: cruces, mercados, patios y sitios con personajes de encargos. Por ejemplo: cobertizo de Bren, comedor de Elva, fragua de Daro, calle de los toldos, patio de mensajes, terraza de las cargas, banco de revisión, cisterna, embarcadero, patio del relato…

**Escenas:**
- Hay 132 escenas nuevas.
- Cada lugar tiene variantes de día en las visitas 3, 5 y 8 y de noche en las visitas 3 y 6.
- Si un lugar ya tenía una variante de día en la visita 3, se respeta.

**Colocación automática (`insertar_en`):**
- Se calcula contra la base desplegada.
- Las escenas van detrás de la última variante que sólo depende de la hora o de las visitas, y delante de las de clima y de encargos.
- Por eso, en la visita 8 el cobertizo sigue mostrando la rueda ya fijada si Bren la arregló, y la fragua con viento sigue mostrando su escena de viento.

**En total, 38 lugares** tienen al menos 3 formas de contarse de día y otras 3 de noche, en cualquier clima que no tenga escena propia.

Comprobado con las dos tandas escritas en una copia del contenido desplegado: 145 tests OK.

Hay también pistas para quien vuelve:
- De noche, en la sexta visita, el patio de mensajes deja ver «algo pequeño que brilla» junto a la pared antigua: la pista del secreto de las piedras.
- La fragua de noche conserva la taza del secreto de Lio.

## 16. Mirar en una dirección, ecos y contador de secretos

Los parches se generan con `hacer_parche_extras.py` **directamente contra la base desplegada** (`vt2-mud-piloto`) y se prueban con `prueba_extras.py`.

| Parche | Archivo | Qué hace |
|---|---|---|
| `extras_motor.patch` | `server/engine.py` | Acción «Mirar hacia el norte» (también se entiende escrita: «mirar norte», «mirar al norte»), ecos al quedarse y `secrets.found` en el snapshot. |
| `extras_contenido.patch` | `server/content.py` | Tabla nueva `secrets`; rechaza un `look` que apunte a una dirección sin salida. |
| `extras_cliente.patch` | `client/app.js` | En Recuerdos: «Secretos encontrados: N. El mundo guarda más.», sólo si N > 0. |

**Datos:**
- `mirar_direcciones.json`: 20 salas, 62 direcciones (las seis plazas, el mercado de Vaisgard, las fronteras entre regiones y varios cruces). Describen lo que se ve; un destino que no has visitado no se nombra, salvo regiones o rasgos visibles.
- `ecos.json`: 18 salas con 3 microescenas cada una.
- `secretos.json`: los 10 hallazgos de los secretos I1–I6.

**Reglas de los ecos:**
- Sólo aparecen si te quedas: a partir de 60 s, uno nuevo cada 75 s, y se agotan.
- El orden cambia según la visita.
- Nunca aparecen junto a un peligro.
- Se calculan a partir de la hora de llegada, que se guarda al moverse. Consultar el estado no lo modifica: está probado.
- El diario del cliente los imprime solo, porque son líneas nuevas de la escena.

**Prueba (13 comprobaciones, todas OK):**
- `mirar`: cuatro direcciones en la plaza; entiende «mirar al norte»; devuelve el texto correcto; no mueve al personaje.
- Ecos: no aparecen al llegar; aparecen a los 70 s; cambian a los 150 s; se agotan; consultar no cambia el estado; se callan con un Espinajo presente.
- Secretos: el contador empieza en 0 y cuenta los flags propios y los de participación.
- Contenido: se rechaza una dirección sin salida.

Además: 145 tests OK, sintaxis de `app.js` correcta y `qa-narrative`, `qa-printing` y `qa-passive` en PASS.

**Límites:**
- Los ecos de Campo de surcos sólo se verán cuando el Espinajo no esté, porque su señal es fija.
- El contador sólo sube si se integran también los secretos I1–I6 de `TEXTOS.md`.
