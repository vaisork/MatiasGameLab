# Revisión narrativa

Revisión de los 10 encargos de `content/world.json`, del Salteador de cargas y de la fauna de Edran. Se leyó el contenido real y `server/engine.py`, solo para consultarlo. **No se ha probado nada en el juego.** Todo lo que sigue sale de leer los datos y de recorrer mentalmente cómo el motor encadena los eventos.

## Cómo encadena el motor un encargo (base de toda la revisión)

1. **Aceptar** (en `accept_room`): si el NPC está presente y existe `accept_dialogue`, se lee «Nombre: …». Si falta alguna de las dos cosas, se lee `accept_text` como narración. Después siempre aparece «Anotas el encargo… pago de referencia N sellos».
2. **Diario**: muestra `accept_text` mientras el encargo está en marcha y `ready_text` cuando está listo.
3. **Listo**: `ready_text` aparece una sola vez, en la sala donde se cumple la última condición. Si no existe, sale «El encargo ya puede entregarse.».
4. **Entregar**: `delivery_text` (narración, aunque el NPC no esté), luego `payment_dialogue` (solo si el NPC está) y luego la línea de sellos.

Consecuencias para la escritura:
- `accept_dialogue` lleva toda la petición, porque `accept_text` no se lee en ese momento.
- `accept_text` tiene que entenderse sin el diálogo.
- Ningún texto de diálogo menciona cifras, porque los encargos de Valdren pagan menos si se repiten.

## Problemas detectados

### Contradicciones con el contenido o con el motor

| # | Dónde | Problema | Corrección |
|---|---|---|---|
| 1 | `valdren_recado_forja` | Se pide «llevar la medida», pero el tema `rueda` de Bren no da ninguna medida. | Bren dice «un dedo, lado izquierdo» antes y después de fijar la cuña. El examen de la rueda concuerda. |
| 2 | `valdren_revision_cobertizos` | Elva pregunta si hay sitio para una carga, pero los exámenes requeridos (`esquina`, `estacas`) no hablan de sitio. | Motivo nuevo: la harina del pan. Los dos exámenes ahora responden «¿está seco?». |
| 3 | `valdren_estado_vado` | `apoyos` solo dice que «pueden revisarse», así que no hay noticia que llevar. | Los apoyos están firmes y la losa ya no se mueve. |
| 4 | `khariel_polea` | Seran (NPC) y «Salteador de cargas» (criatura) son la misma persona con dos voces. El genérico «La carga se queda aquí» choca con «quiero mi pago». | La señal y la descripción nombran a Seran. Su diálogo propio **requiere código** (ver ENTREGA). |
| 5 | `velmora_recipiente` | Varo menciona a Leris (otra historia). Elin dice «el aro es mío», pero la acción y los estados dejan el aro en el taller. Desi dice «el aro puede llevarse». | Un objeto, una dueña, aro y tabla de Desi. Orden Elin → Desi → secadero → Elin. |
| 6 | `brumak_taza` | Las dos opciones no eran opuestas: «conservar aro y aligerar base» frente a «base ancha manteniendo el aro». | Una sola pregunta: base ligera o base estable. |
| 7 | `khariel_cornisa` | El texto decía «unos pocos pasos», pero son cinco tramos. El examen de la cornisa no daba base para decidir. | Se describe la cornisa (apoyos, bulto pequeño, carro no cabe, tramo oculto). |
| 8 | Fauna de Edran | La misma frase aparece en 10 lugares: «tallos viejos» en la calzada de piedra y «sombra sobre el agua» en el terraplén, donde no hay agua. | Un texto por lugar y por criatura (33 textos). |

### Narración impresa como voz del personaje

El motor imprime `Nombre: texto`. Estos textos empezaban con narración o con comillas, y salían cosas como «Seran: Acuerdas devolver…» o «Luma: Luma escucha…». Están todos corregidos en TEXTOS (grupos A y D):

- Seran: `cuenta`, `acuerdo`
- Luma: `cornisa`
- Nima: `preparativos`
- Nera: `aviso_preciso`, `pedir_comprobacion`
- Tov: `aviso`
- Taren: `medidas`, `recomendación`
- Elin: `entrega`
- Desi: `apoyo`
- Nela: `cuerda`
- Oren: `caja`, `ayuda`

Encontrado con un barrido automático: textos que empiezan por el nombre del NPC, por `«` o por un verbo en segunda persona.

### Repetición

- En Edran, los textos de wildlife_pool eran idénticos en 10 salas. Corregido. Las otras regiones tienen la misma repetición (10–12 salas por texto) y siguen pendientes.
- `payment_dialogue` y las memorias `encargo_pagado:*` existentes se leen en momentos distintos (al cobrar y en conversaciones posteriores). Se evitó repetir la misma frase. Ejemplo: Bren ya no dice «saldrán con el próximo carro», porque esa frase es de su memoria.
- Los tres encargos de Valdren son repetibles, así que su historia se repite igual. Se escribió para que siga siendo cierta (la misma rueda, la misma harina). Un niño que repite notará la repetición. **Propuesta, no integrable:** dar variantes por repetición requiere código.

### Fuera de alcance, pero visto

- `lethra_mercado_hojas`: los textos `day` y `viento` nombran a «Iria». Ese nombre ya es de una Felaryn de Hoshai y de un personaje de Edran. La vendedora de ese puesto es Tila (`lethra_nera_mercado`). Conviene cambiarlo por Tila o por «una vendedora».
- Hay un Cornalomo (`abrumador`) en el pool de la Senda de regreso y de la Calzada, a uno o dos pasos de Valdren. Es una decisión de equilibrio, no de texto. Los textos lo sitúan lejos.
- Al vencer a un humano, el motor dice «recuperas 4 sellos». Si el salteador no te había quitado nada, «recuperar» es falso. Mejor «ganas» o «el salteador deja caer». Es una cadena del motor.
- `veyra_anotar_demora` (acción) y el tema `aviso` de Tov hacen lo mismo con flags distintos (`veyra_demora_conocida` / `encargo_veyra_demora_conocida`). No rompe nada, pero el jugador puede «preguntar por la demora» dos veces.

## Pasadas realizadas

### Pasada 1: coherencia con datos y motor

Para cada encargo se leyeron el NPC, las salas, los exámenes, las acciones, los flags y las rutas (calculadas por BFS con las salidas reales). Todas las indicaciones de dirección de los diálogos coinciden con la ruta más corta.

Antes / después (Daro, al aceptar):
> **Antes** (narración): «Daro necesita que pases por el cobertizo y preguntes a Bren qué carro espera una abrazadera. El pago corresponde a llevar esa medida de vuelta, no a reparar la rueda.»
> **Después** (voz): «Bren, el de los carros, tiene una rueda que cruje cuando el carro avanza. Tengo que hacerle una abrazadera, pero si no sé de qué lado cede la rueda, la haré a ciegas…»

### Pasada 2: voz frente a narración y presencia

El barrido de la sección anterior encontró 13 textos. Se comprobó también:
- Que ningún `delivery_text` haga hablar al NPC, porque puede estar ausente.
- Que ningún diálogo prometa una elección que no existe.

Antes / después (Seran):
> **Antes:** «Seran: Acuerdas devolver la polea e indicar que Seran reclama una cuenta pendiente…»
> **Después:** «Seran: Está bien. La polea está en las cajas del sendero sur; llévatela. Y llévate esta tablilla: ahí está escrita mi cuenta…»

### Pasada 3: secuencias completas leídas en orden

- **Daro**: Aceptar → Bren·rueda (listo, en el cobertizo) → fragua → Entregar. Cada paso dice adónde ir. Se comprobó el caso «otro jugador ya fijó la cuña»: el estado de Bren sigue dando la medida.
- **Daren / Seran, camino pacífico**: cuenta → acuerdo (desaparece la señal del salteador) → recoger en las cajas → taller, devolver (listo) → Entregar. Las acciones de devolver y de entregar no repiten el mismo gesto.
- **Daren / Seran, camino de pelea**: enfrentarse → `defeat_text` («se aparta del camino»; Seran sigue en el campamento como NPC, lo cual es coherente) → recoger tras la pelea → taller → Entregar. `payment_dialogue` sirve en los dos caminos; el reproche llega por la memoria `hoshai_polea_por_fuerza`.
- **Varo / Elin / Desi**: si el jugador va primero al secadero, la acción no aparece. El diálogo de aceptación da el orden correcto.
- **Arel**: las dos opciones de Nera llevan a «listo» y ninguna habla de robo.
- **Taren de noche**: no está (schedule día). Se acepta con `accept_text`, que avisa de que trabaja de día. Ver la dependencia D2 en ENTREGA.

Antes / después (Desi):
> **Antes:** «Desi: «El aro puede llevarse. La tabla debe quedarse…»»
> **Después:** «Desi: Llévate sólo el recipiente. El aro y la tabla se quedan: la tabla sostiene el juguete, que todavía está húmedo…»

### Pasada 4: ritmo y lectura infantil

- Se acortó el diálogo de Luma: la ruta larga pasó a `accept_text`.
- Se quitaron marcas de tiempo que el motor no controla. «Esta noche Mira y Sola cenan» quedaría en el diario para siempre.
- `ready_text` y `delivery_text` tienen una o dos frases. La escena larga está en la petición y en la conversación clave, no en cada paso.
- Fauna: una o dos frases por aparición. Cuentan qué hace el animal y dónde se refugia, sin afirmar que se va (sigue presente y se puede interactuar con él). El Cornalomo se ve siempre lejos.

Antes / después (fauna, Calzada de piedra):
> **Antes:** «Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.»
> **Después:** «Un Espinajo cruza los cantos a saltitos y se mete en el borde de hierba. Desde allí te sigue con la mirada.»

## Sin verificar en el juego

- Ningún texto se ha leído en el cliente real: falta comprobar la longitud en 320 px y el ritmo de impresión de la cola narrativa.
- Falta ver cómo se muestran las claves con espacios en el diálogo del salteador («qué quieres»). El parser normaliza los acentos, pero no se ha probado.
- Falta comprobar el orden real de eventos al cobrar con el parche narrativo guardado y sin desplegar.
- No hay lectura de un niño. Los conteos de esta revisión no prueban que la historia guste.

## Bloques 2 y 3: revisión

### Fauna (E–H)

- **Animales grandes** (Rasgacumbres, Quebrarrocas, Dorsalodo, Rasgacorteza): siempre se ven de lejos. El texto no los acerca ni les hace atacar, porque el aviso de acercarse ya existe aparte.
- **Animales pequeños:** hacen algo concreto en ese sitio y se refugian a la vista, sin desaparecer.
- **Colocación dudosa** (no es cosa de texto): hay un Rasgacorteza, de nivel abrumador, en el pool de la Entrada de Velmora, de la Senda hacia Elin y del Claro tranquilo. Según el canon, el claro silencioso no tiene encargo ni secreto obligatorio, y su calma choca con un animal así. Mis textos lo sitúan lejos, pero conviene revisar si debe estar en ese pool.
- **Rondamusgo:** cuando aparece en un pool, el motor ofrece «Examinar Rondamusgo». Sin embargo, el texto original sólo mostraba pelo y semillas, es decir, un rastro. Mis textos muestran al animal vivo para que concuerden con la acción. La señal fija del Rincón de semillas sigue siendo un rastro: falta decidir si allí debe poder examinarse.

Antes / después (Uñapiedra, Paso entre paredes):
> **Antes:** «Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.» (la misma frase en 12 salas)
> **Después:** «En la pared del paso estrecho, un Uñapiedra se pega a la roca por encima de las cabezas. Cuando alguien golpea la piedra de aviso, se queda inmóvil.»

### Secretos (I): las cuatro lecturas

1. **Petición:** los secretos no piden nada. Se encuentran sólo porque el niño mira. Cada uno tiene una pista que se puede leer: la taza del texto nocturno, «no ves el fondo», «cabe una mano», «haría falta saltar como un Felaryn».
2. **Desarrollo:** cada revelación describe lo que el niño ve con sus propios ojos. No da premios.
3. **Regreso:**
   - La barquita cambia la orilla para todos los jugadores.
   - El dibujo de Korven cambia con las visitas.
   - Los demás secretos dejan una línea en el diario y un tema de conversación nuevo.
   - Ningún tema nuevo vuelve a pedir algo que ya se hizo.
4. **Ruta independiente:**
   - Un Felaryn en el Paso entre paredes ve la pista y además el botón de saltar. Un humano ve sólo la pista, que le dice a quién preguntar.
   - En la figura de Nhal, la hora evita que el mismo objeto esté en tres sitios a la vez.

Riesgos a vigilar en el juego:
- **Botones:** una acción secreta aparece como botón en cuanto se cumplen sus condiciones. El secreto está en *cuándo* aparece (de noche, en la segunda visita, con una especie), no en que el botón esté escondido.
- **Personajes:** que Sola y Mira se contradigan es intencional. Un tema nuevo que no se ha probado podría quedar mal ordenado entre los botones de esos personajes.
