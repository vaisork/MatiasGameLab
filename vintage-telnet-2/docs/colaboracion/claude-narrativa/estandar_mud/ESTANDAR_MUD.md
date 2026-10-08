# Estándar de narrativa MUD clásica: propuesta y prueba acotada (Valdren)

Es una propuesta, no un cambio aplicado. No se modificaron `content/`, `server/` ni `client/`, y no se desplegó nada. Todo lo de esta carpeta se puede reproducir:

| Archivo | Qué es |
|---|---|
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
