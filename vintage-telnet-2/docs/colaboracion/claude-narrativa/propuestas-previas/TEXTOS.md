# Textos propuestos — Vintage Telnet 2

Generado por `generar.py` a partir de las mismas propuestas que `propuestas.json`. El «texto actual» se lee del contenido en el momento de generar.
Bloques con **requiere código: sí** no se pueden integrar sólo como texto. El resto encaja en campos que el motor ya lee.


## A1 · valdren_recado_forja · Daro (Valdren)

### `valdren_recado_forja` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Esta abrazadera tiene que sujetar un carro, pero hacerla más gruesa no servirá si no sé dónde cede. Ve al cobertizo y pregunta a Bren por la rueda. Escucha su respuesta y tráemela; la reparación la haremos nosotros. Te pago por llevar esa información, no por meterte entre las ruedas.

**Propuesto:** Bren, el de los carros, tiene una rueda que cruje cuando el carro avanza. Tengo que hacerle una abrazadera, pero si no sé de qué lado cede la rueda, la haré a ciegas. Baja a la plaza y entra en el cobertizo de los carros, al oeste. Pregúntale a Bren por la rueda y tráeme lo que te diga: de qué lado se sale la cuña y cuánto. No tienes que arreglar nada; con la medida me basta.

**Por qué:** Quién (Bren), qué (lado y cuánto se sale la cuña), por qué (no fabricar a ciegas), dónde (plaza → oeste) y cuándo está hecho (traer la medida). Sin cifras de pago: el motor ya añade la línea de sellos y el pago baja si se repite.

### `valdren_recado_forja` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Daro necesita que pases por el cobertizo y preguntes a Bren qué carro espera una abrazadera. El pago corresponde a llevar esa medida de vuelta, no a reparar la rueda.

**Propuesto:** Daro, el herrero, necesita saber de qué lado cede la rueda del carro de Bren para ajustar una abrazadera. Baja por la calle hasta la plaza y entra en el cobertizo de los carros, al oeste. Pregunta a Bren por la rueda y vuelve a la fragua con su respuesta. No hace falta reparar nada.

**Por qué:** Resumen en voz de narrador; se entiende sin la voz de Daro. El original hablaba de «medida» sin que Bren diera ninguna; ahora el tema de Bren la contiene (ver abajo).

### `valdren_recado_forja` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Daro en la fragua de Valdren para contarle el resultado y cobrar.

**Propuesto:** Ya sabes de qué lado se sale la cuña y cuánto. Vuelve a la fragua de Daro, al norte de la plaza, para darle la medida.

**Por qué:** Se dispara en el cobertizo al hablar con Bren: dice a quién volver y dónde está.

### `valdren_recado_forja` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** La fragua vuelve a oler a hierro y carbón. Al regresar con la respuesta de Bren, reconoces la abrazadera entre las piezas que esperan junto al umbral. Ya sabes a qué carro corresponde la pregunta que te llevó al cobertizo.

**Propuesto:** Repites lo que dijo Bren: un dedo, en la rueda izquierda. Daro lo escribe con tiza junto a la abrazadera.

**Por qué:** Consecuencia visible que ya existe en los estados de la fragua (marca de tiza tras encargo_pagado).

### `valdren_recado_forja` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Con lo que te contó Bren puedo comparar esta abrazadera con el trabajo que hace en el carro. Me ahorraste ir dejando la fragua a medias. Toma; el recado también lleva tiempo, aunque en la mano no traigas hierro.

**Propuesto:** Un dedo, lado izquierdo. Con eso ajusto la pieza a esa rueda y no gasto hierro de más. Bren tendrá su abrazadera antes de volver a cargar.

**Por qué:** Cierra el motivo de Daro («sin añadir hierro por añadirlo»). Repetible: el texto sigue siendo cierto en otra entrega.

### `edran_bren` · `topics.rueda`

- **Archivo:** `content/regions/edran.json` → `npcs`
- **Aparece:** Hablar con Bren · rueda, antes de que nadie haya fijado la cuña (sin edran_rueda_comprobada). Es la acción requerida del encargo.
- **Requiere código:** no

**Actual:** Escucha cuando lo empuje: ese crujido no aparece con el carro quieto. Quédate fuera de la cuerda mientras lo muevo despacio y fíjate en la cuña de la rueda. Si ves que se desplaza, avísame; yo detendré el carro. Daro necesita saber qué parte falla para preparar la abrazadera correcta.

**Propuesto:** Cruje cuando el carro avanza, no cuando para. Es la rueda izquierda: la cuña se sale como un dedo por fuera del aro. Si te manda Daro, dile eso: un dedo, lado izquierdo. Si quieres verlo, quédate fuera de la cuerda; yo muevo el carro despacio.

**Por qué:** Sin esto el encargo «llevar la medida» se completaba sin que nadie diera una medida. «Un dedo» y «izquierda» son detalle físico nuevo, coherente con el examen («la cuña… ha empezado a salir por un extremo»).

### `edran_bren` · `states[0].overrides.topics.rueda`

- **Archivo:** `content/regions/edran.json` → `npcs`
- **Aparece:** Hablar con Bren · rueda, después de que alguien fijó la cuña (edran_rueda_comprobada, mundo).
- **Requiere código:** no

**Actual:** La cuña ya está sujeta y la rueda gira sin aquel crujido. Lio vio cómo la revisamos antes de seguir con los sacos. La próxima prueba será con carga: que el carro vacío funcione no basta. Por lo menos ahora sabemos qué pieza vigilar al empujarlo.

**Propuesto:** Ya no cruje: la cuña está sujeta. Para Daro, la medida sigue siendo la misma: se salía un dedo por el lado izquierdo. Con eso puede ajustar la abrazadera. La próxima prueba la haré con el carro cargado.

**Por qué:** El encargo se puede aceptar después de que otro jugador arregló la cuña; Bren debe seguir dando la medida.

### `valdren_cobertizo` · `examine.rueda`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Examinar rueda en el cobertizo (antes de fijar la cuña).
- **Requiere código:** no

**Actual:** La cuña mantiene el aro apretado, pero ha empezado a salir por un extremo. Puede comprobarse mientras el carro avanza lentamente.

**Propuesto:** La cuña de la rueda izquierda ha empezado a salirse por un extremo, como un dedo. Se nota mejor mientras el carro avanza despacio.

**Por qué:** Alinea el examen con lo que Bren dice.


## A2 · valdren_revision_cobertizos · Elva (Valdren)

### `valdren_revision_cobertizos` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Cuando una carga llega tarde, no quiero decirle que cabe bajo techo y descubrir después que no tiene sitio. Revisa la esquina del paso entre los graneros y las estacas del cobertizo de campo. Mira los dos lugares y vuelve a contármelo. No hace falta vaciar sacos ni arreglar todo el cobertizo.

**Propuesto:** La última carreta del día trae la harina para el pan de mañana, y a veces llega cuando ya es de noche. Si la descargan en un sitio mojado, la harina se echa a perder. Necesito saber dos cosas: si la puerta baja del paso entre los graneros está seca, y si en el cobertizo de las estacas, pasado el lindero, queda un hueco bajo techo. Mira la esquina del granero y las estacas del cobertizo, y vuelve a contármelo.

**Por qué:** El original pedía «comprobar lugar para una carga tardía» pero los exámenes requeridos (esquina, estacas) no decían nada de espacio. Ahora hay un motivo de niño (pan de mañana) y los exámenes responden a la pregunta.

### `valdren_revision_cobertizos` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Elva te pide una comprobación de los dos espacios: el paso de graneros y el cobertizo de campo. Quiere saber si ambos conservan lugar para una carga que llegue tarde.

**Propuesto:** Elva, la del comedor, espera harina en la última carreta del día. Comprueba dos sitios donde podría descargarse sin mojarse: la esquina junto a la puerta baja, en el paso entre los graneros, y las estacas del cobertizo de campo, pasado el lindero. Examina ambos y vuelve al comedor.

**Por qué:** Resumen y alternativa sin voz.

### `valdren_revision_cobertizos` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Elva en el comedor de Valdren para contarle el resultado y cobrar.

**Propuesto:** Has visto los dos sitios. Vuelve al comedor de Elva, junto al pozo, para decirle dónde puede esperar la harina.

**Por qué:** Dirección real: el comedor sale al norte hacia el pozo.

### `valdren_revision_cobertizos` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** De regreso en el comedor, la lista de cargas tiene sentido de otra manera. Puedes recordar la esquina entre los graneros y las estacas bajo el techo del campo sin mezclarlas. Son dos lugares distintos para contar a quien prepara la llegada de un carro.

**Propuesto:** Le cuentas a Elva lo que viste en la esquina del granero y en el cobertizo de las estacas. Ella lo apunta en la lista de cargas, junto a las ollas.

**Por qué:** Coincide con el estado posterior del comedor («guarda tus noticias… junto a la lista de cargas»).

### `valdren_revision_cobertizos` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Gracias por mirar los dos sitios. Desde esta mesa parece que todo queda cerca, hasta que llega alguien mojado y hay que decidir dónde dejar su carga. Prefiero tener una noticia cierta de cada lugar antes de mandarlo de una puerta a otra.

**Propuesto:** Entonces ya sé dónde mandar la carreta si llega tarde. Mañana habrá pan para todos, también para quien todavía no ha vuelto.

**Por qué:** Vale tanto si la esquina estaba despejada como si no: Elva sabe cuál de los dos sitios usar.

### `valdren_graneros` · `examine.esquina`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Examinar esquina mientras la salida sigue tapada (sin edran_granero_despejado). Acción requerida.
- **Requiere código:** no

**Actual:** La tierra procede de arreglar el terraplén. Basta despejar la salida antigua para que el agua siga su camino.

**Propuesto:** La tierra del terraplén tapa la salida del agua. Cuando llueve, el charco llega hasta la puerta baja: ahí no conviene dejar sacos hasta despejarla.

**Por qué:** Da la respuesta que Elva necesita y apunta a la acción ya existente de despejar.

### `valdren_graneros` · `states[0].overrides.examine.esquina`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Examinar esquina después de despejarla (edran_granero_despejado, mundo).
- **Requiere código:** no

**Actual:** La salida queda abierta. La tierra retirada se ha colocado arriba de la pendiente, lejos de la corriente.

**Propuesto:** La salida queda abierta y la tierra retirada está arriba de la pendiente. La puerta baja se mantiene seca: ya se pueden dejar sacos.

**Por qué:** Misma pregunta, respuesta contraria: la consecuencia de despejar se nota en el encargo.

### `edran_cobertizo_campo` · `examine.estacas`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Examinar estacas. Acción requerida.
- **Requiere código:** no

**Actual:** Los números señalan tamaños que pueden reemplazarse. No identifican dueños de parcelas.

**Propuesto:** Las estacas cuelgan ordenadas por tamaño; los números indican medidas, no dueños. Debajo del banco queda un hueco seco y techado, con sitio para unos pocos sacos.

**Por qué:** Conserva el dato original (números = tamaños) y añade el hueco que Elva pregunta. Detalle físico nuevo, sin mecánica.


## A3 · valdren_estado_vado · Bren (Valdren)

### `valdren_estado_vado` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Un carro pesa bastante más que yo, y no quiero elegirle el camino mirando sólo desde el cobertizo. Ve al vado de juncos y revisa los apoyos desde la ribera. Después mira la losa junto al hito, en el paso hacia Veyra. Vuelve con noticias de ambos. No te pido entrar al agua ni pelear con nada.

**Propuesto:** Mis carros cargados salen hacia Lethra y hacia Veyra, y los dos caminos cruzan agua. Antes de cargar quiero saber si los pasos aguantan. Uno es el Vado de Juncos: sal del pueblo por el este, sigue la acequia y baja por los sauces hasta el puente; mira sus apoyos desde la orilla. El otro está en el Paso hacia Veyra, al final de la calzada, al norte: mira la losa junto al poste. No te metas en el agua ni te acerques a ningún animal. Sólo mira y vuelve a contármelo.

**Por qué:** Indicaciones comprobadas con las salidas reales (plaza → este … estanque → sur → sauces → sur → vado → este; vado → oeste … calzada → norte → hito).

### `valdren_estado_vado` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Bren quiere noticias de los dos cruces de esta ruta: el puente de juncos y las piedras junto al hito. No te pide entrar en el agua ni enfrentarte a ninguna criatura.

**Propuesto:** Bren quiere saber si sus carros cargados pueden cruzar dos pasos de agua. Examina los apoyos del puente en el Vado de Juncos (al este, pasados la acequia y los sauces) y la losa del Paso hacia Veyra (al norte, al final de la calzada). No hace falta entrar en el agua ni enfrentarse a ninguna criatura. Después vuelve al cobertizo de los carros.

**Por qué:** Resumen.

### `valdren_estado_vado` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Bren en el cobertizo de Valdren para contarle el resultado y cobrar.

**Propuesto:** Ya has visto el puente y la losa. Vuelve al cobertizo de Bren, en Valdren, para contarle si sus carros pueden cruzar.

**Por qué:** Se dispara lejos del pueblo: nombra el pueblo.

### `valdren_estado_vado` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** El cobertizo parece pequeño después del camino. Traes en la memoria los apoyos vistos desde la ribera y la losa junto al hito. Las ruedas que esperan bajo el techo recorrerán esos mismos cruces; ahora puedes explicar a Bren qué revisaste en cada uno.

**Propuesto:** Le explicas a Bren cómo están los apoyos del puente y la losa del poste. Él lo apunta en una tablilla y la cuelga fuera de la cuerda de giro, donde la vean los conductores.

**Por qué:** Coincide con el estado posterior del cobertizo (tablilla fuera de la cuerda).

### `valdren_estado_vado` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Ya tengo noticias de los dos cruces. Cuando preparemos el siguiente carro, compararé su carga con lo que me cuentas. Gracias por mirar desde un sitio seguro. No quería que te metieras en el agua para responderme una pregunta.

**Propuesto:** Bien. Con esto sé por dónde puede ir cada carro sin descargar a medio camino. Se lo diré a cada conductor antes de cargar.

**Por qué:** Evita repetir la frase de su memoria posterior («saldrán con el próximo carro»).

### `edran_puente_juncos` · `examine.apoyos`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Examinar apoyos en el Vado de Juncos. Acción requerida.
- **Requiere código:** no

**Actual:** Se ven desde la ribera para que pueda revisarse su estado sin desmontar el piso.

**Propuesto:** Los apoyos del puente están firmes. El agua empuja unos juncos contra uno de ellos, pero la madera no se mueve. Un carro cargado puede pasar si cruza despacio.

**Por qué:** El original sólo decía que los apoyos «pueden revisarse»; el jugador no tenía noticia que llevar.

### `edran_hito_campos` · `examine.losa`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Examinar losa en el Paso hacia Veyra. Acción requerida.
- **Requiere código:** no

**Actual:** Sus reparaciones reúnen piedras distintas. Una piedra clara encaja bajo el borde gastado de la losa.

**Propuesto:** La losa tiene parches de piedras distintas. Una piedra clara, más nueva, sujeta el borde gastado: la losa ya no se mueve al pisarla.

**Por qué:** Conserva el detalle original (piedra clara bajo el borde) y lo convierte en noticia.


## A4 · khariel_polea · Daren y Seran (Hoshai)

### `khariel_polea` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Me falta una polea del taller. Sin ella, subir una carga pequeña se vuelve un trabajo de varias manos. Está por el campamento de lona azul y las cajas bajo la terraza. Habla primero con Seran: dice que quedó una cuenta del transporte sin pagar. Quiero recuperar la pieza y saber qué reclama, no hacer desaparecer su queja.

**Propuesto:** Me falta una polea del taller, la que usamos para subir cargas cortas por los peldaños. Ha aparecido en un campamento con una lona azul. Desde la plaza, baja dos tramos de escalones hasta la terraza de las cargas y toma el desvío del oeste. Allí acampa un viajero, Seran. Dice que la polea es suya hasta que alguien le pague un transporte. Habla con él antes de tocar nada: quiero la polea, pero también quiero saber qué cuenta reclama. Si vuelves con las dos cosas, habrás hecho el trabajo.

**Por qué:** Sustituye «Hablar con Seran permite resolverlo sin combatir» (voz de diseño) por un motivo: Daren quiere la pieza y la verdad de la cuenta.

### `khariel_polea` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Daren paga por recuperar su polea y traer información sobre la cuenta pendiente. Desde la plaza: dos tramos hacia abajo y el desvío occidental. Hablar con Seran permite resolverlo sin combatir.

**Propuesto:** Daren, el maestro de reparaciones, necesita recuperar la polea de su taller. Está en el campamento de la lona azul: desde la plaza, baja dos tramos hasta la terraza de las cargas y toma el desvío del oeste. Un viajero llamado Seran la retiene y reclama un pago pendiente. Habla con él, recoge la polea en las cajas del sendero sur y devuélvela al taller junto con lo que Seran reclama.

**Por qué:** Resumen con el orden real: hablar (cuenta → acuerdo), recoger en Cajas bajo la terraza, entregar en el taller.

### `khariel_polea` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Daren en el taller de apoyos de Khariel para contarle el resultado y cobrar.

**Propuesto:** La polea ha vuelto al banco de Daren y la cuenta de Seran queda apuntada a su lado. Puedes cerrar el encargo con Daren aquí mismo.

**Por qué:** Se cumple dentro del taller (acción hoshai_entregar_polea), por eso «aquí mismo».

### `khariel_polea` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** Al volver al taller, el hueco que dejó la polea ya tiene una historia: una caja marcada, la lona azul y una cuenta de transporte pendiente. La pieza regresó al lugar donde hacía falta. Lo ocurrido con Seran también vuelve contigo.

**Propuesto:** La polea vuelve a su gancho, encima del banco bajo. Ya pueden subir otra vez cargas cortas por los peldaños sin llevarlas a mano.

**Por qué:** No repite la acción de devolver (que ya narra la marca y la tablilla); cuenta para qué sirve haberla recuperado.

### `khariel_polea` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** La pieza ha vuelto. Puedo seguir con las cargas del taller, y esa ayuda te la pago ahora. La cuenta de Seran me toca hablarla con él; no voy a esconderla debajo de las herramientas. Gracias por traer lo que faltaba.

**Propuesto:** Gracias. La polea es del taller y vuelve a trabajar. Lo de Seran lo miraré con calma: si le debemos un transporte, se lo pagaremos.

**Por qué:** Sirve para el camino pacífico y para el de pelea; en el segundo, la memoria hoshai_polea_por_fuerza añade el reproche de Daren.

### `hoshai_seran` · `topics.cuenta.text`

- **Archivo:** `content/regions/hoshai.json` → `npcs`
- **Aparece:** Hablar con Seran · cuenta (fija hoshai_seran_escuchado).
- **Requiere código:** no

**Actual:** Transporté estas cajas y esperaba que me pagaran. Daren puede revisar la cuenta, pero la polea sigue aquí y no quiero que parezca que desapareció. Si vas a llevarla al taller, dile que yo la entregué y que aún espero una explicación del transporte. No te estoy pidiendo que decidas quién tiene razón por una sola conversación.

**Propuesto:** Subí estas cajas hasta aquí porque me dijeron que el taller pagaría al llegar. Nadie me ha pagado. Por eso me quedé la polea: no la quiero, quiero mi pago. Si se la llevas a Daren, dile también quién la trajo y qué se me debe.

**Por qué:** Quita las comillas «» dentro de la voz (se leían «Seran: «…»») y explica el motivo: no es un ladrón, es un transportista sin cobrar.

### `hoshai_seran` · `topics.acuerdo.text`

- **Archivo:** `content/regions/hoshai.json` → `npcs`
- **Aparece:** Hablar con Seran · acuerdo (tras cuenta, sin haber peleado). Fija hoshai_polea_acordada.
- **Requiere código:** no

**Actual:** De acuerdo. Puedes recoger la polea de la caja del sendero sur y llevarla al taller. Que mi nombre vaya con la cuenta: no quiero que devuelvan la herramienta y se olviden de por qué está aquí. Apartaré el palo. Tú lleva la explicación; no te estoy pidiendo que pagues la deuda de Daren.

**Propuesto:** Está bien. La polea está en las cajas del sendero sur; llévatela. Y llévate esta tablilla: ahí está escrita mi cuenta. Que Daren la lea. No te pido sellos a ti; te pido que no se pierda mi parte.

**Por qué:** El original era narración del jugador («Acuerdas devolver…») impresa como «Seran: Acuerdas…». Ahora habla Seran y conserva el hecho: no se pagan sellos.

### `hoshai_campamento_lona` · `description`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Descripción base del campamento (antes del acuerdo o la devolución).
- **Requiere código:** no

**Actual:** Una lona azul cubre tres cajas de viaje. La terraza queda al este y un sendero corto baja al sur hasta las cargas. Un viajero afirma que una polea del taller le pertenece. Puedes hablar antes de acercarte a su palo.

**Propuesto:** Una lona azul cubre tres cajas de viaje. La terraza queda al este y un sendero corto baja al sur hasta más cajas. Seran, un viajero con un palo corto, vigila la carga y dice que la polea del taller es suya hasta que le paguen. Puedes hablar con él antes de acercarte.

**Por qué:** Presenta a Seran por su nombre antes de que aparezca el aviso del salteador: así el niño entiende que es la misma persona.

### `hoshai_campamento_lona` · `signals[creature=forajido_camino].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Señal del salteador en el campamento, mientras no hay acuerdo.
- **Requiere código:** no

**Actual:** Un salteador golpea una caja con un palo corto para que no te acerques. La terraza permanece libre al este.

**Propuesto:** Seran golpea una caja con su palo corto para que no te acerques a la carga. No te corta el paso: la terraza sigue libre al este.

**Por qué:** Integrable ya. Ver la propuesta de código siguiente: el botón seguirá diciendo «Salteador de cargas».

### `hoshai_campamento_lona` · `signals[creature=forajido_camino].dialogue`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** REQUIERE CÓDIGO: diálogo de adversario propio de esta señal (y nombre visible «Seran»), en lugar del diálogo común del Salteador de cargas.
- **Requiere código:** sí

**Actual:** (no existe)

**Propuesto:** {"qué quieres": "Que me paguen el transporte. Mientras no me paguen, la polea se queda conmigo.", "por qué": "Subí estas cajas hasta aquí y nadie me pagó. No soy un ladrón: es lo único que tengo para que me escuchen.", "dejar paso": "La terraza está libre. Si quieres arreglarlo hablando, habla conmigo, no con mi palo."}

**Por qué:** Hoy el jugador ve a la vez «Seran · cuenta» y «Hablar con Salteador de cargas · exigencia» con el texto genérico «La carga se queda aquí». Son la misma persona con dos voces. Necesita un campo por señal (p. ej. signals[].name y signals[].dialogue) que el motor prefiera al de la criatura.

### `hoshai_taller_apoyos` · `actions[id=hoshai_entregar_polea].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Acción «Devolver la polea y explicar la cuenta» con la polea en la mochila y Daren presente.
- **Requiere código:** no

**Actual:** Daren compara la marca de la polea con las herramientas del taller. «Sí, es la nuestra. Sin ella teníamos que levantar cada carga a mano.» La deja junto al banco y anota la reclamación de Seran. «Revisaré también el transporte. Que la pieza haya vuelto no me dice todavía quién tiene razón con la cuenta.» Has devuelto la herramienta y llevado la explicación sin convertirla en una sentencia.

**Propuesto:** Pones la polea sobre el banco y le das a Daren la tablilla de Seran. Daren reconoce la marca del mango enseguida. Lee la cuenta despacio y la deja junto al dibujo de los escalones: «Antes de decir quién tiene razón, quiero compararlo con mis notas del transporte.»

**Por qué:** Narración con cita breve (no voz «Daren:»), para que no choque con delivery_text y payment_dialogue que llegan justo después.


## A5 · khariel_cornisa · Luma (Hoshai)

### `khariel_cornisa` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Cuando preparo una entrega, una caja pequeña y una carga de carro no me piden el mismo camino. Revisa el depósito y el balcón sobre el valle; desde allí puedes examinar la cornisa. Puedes recomendarla para cargas pequeñas o pedir que revisemos los apoyos primero. Después ven a explicarme qué elegiste. No necesito que te arriesgues para demostrar nada.

**Propuesto:** Mando paquetes a los pueblos de abajo por la cornisa, ese camino estrecho pegado a la roca. El otro día, el observador del balcón apuntó en su cuaderno que una carga desapareció detrás de la roca, y ahora hay quien dice que la cornisa es peligrosa. Puede que sólo la perdiera de vista. Ve al balcón sobre el valle, pasado el depósito de herramientas. Mira la cornisa y deja allí una nota: que sólo pasen cargas pequeñas, o que alguien revise los apoyos antes. Luego vuelve y dímelo.

**Por qué:** Une el encargo con un detalle que ya existía y nadie usaba (cuaderno: «se perdió de vista una carga, no la carga»). La ruta detallada (plaza → norte → este → norte → oeste) queda en accept_text para no alargar la voz.

### `khariel_cornisa` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Luma necesita una recomendación de la cornisa. Revisa el balcón junto al depósito y decide si recomendar cargas pequeñas o una revisión previa. Son unos pocos pasos dentro de Khariel.

**Propuesto:** Luma, la comerciante de cintas, envía paquetes por la cornisa del valle y ha oído que es peligrosa. Ve al balcón sobre el valle (desde la plaza: norte al patio de las casas, este al lavadero, norte al depósito; el balcón está al oeste), examina la cornisa y deja allí tu recomendación: sólo cargas pequeñas, o revisar los apoyos antes de usarla. Después vuelve al mercado y cuéntaselo a Luma.

**Por qué:** Quita «Son unos pocos pasos» (no son pocos: cinco tramos).

### `khariel_cornisa` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Luma en el mercado de las cintas para contarle el resultado y cobrar.

**Propuesto:** Luma ya tiene tu recomendación. Puedes cerrar el encargo con ella aquí, en el mercado.

**Por qué:** La última condición es hablar con Luma en el mercado.

### `khariel_cornisa` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** Las cintas del mercado se mueven con el aire que llega de la plaza. Después de mirar el balcón, ya no imaginas la cornisa como una línea cualquiera en el valle. Tu recomendación tiene un lugar concreto detrás: el borde que viste y la decisión que comunicaste.

**Propuesto:** Luma ata una cinta clara a la tablilla de los envíos y escribe al lado lo que recomendaste para la cornisa.

**Por qué:** Usa el código de colores de cintas ya descrito en el mercado.

### `khariel_cornisa` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Gracias por traerme una propuesta que puedo usar. Una carga grande seguirá por el camino principal. Para las pequeñas tendré presente lo que elegiste sobre la cornisa. Antes estaba envolviendo bultos sin saber qué consejo dar a quien preguntara por ese paso.

**Propuesto:** Cuando alguien vuelva a decir que la cornisa es peligrosa, le enseñaré esta nota. Es mejor que un rumor.

**Por qué:** Consecuencia social, válida para las dos recomendaciones.

### `hoshai_luma` · `topics.cornisa.text`

- **Archivo:** `content/regions/hoshai.json` → `npcs`
- **Aparece:** Hablar con Luma · cornisa, tras dejar la nota (hoshai_cornisa_decidida). Fija hoshai_cornisa_informada. Acción requerida.
- **Requiere código:** no

**Actual:** Me sirve saber qué cargas aconsejas y qué parte necesita otra revisión. Ya lo he anotado para las próximas salidas. No enviaré las voluminosas por la cornisa sólo porque alguien haya pasado sin equipaje. Gracias por mirar pensando también en quien vendrá con una caja entre las manos.

**Propuesto:** Así que la viste con tus propios ojos. Eso me sirve más que lo que se oye en la plaza. Las cargas grandes seguirán por el camino principal; para lo demás, haré caso a tu nota.

**Por qué:** El original se imprimía como «Luma: Luma escucha tu recomendación…». Ahora es voz; los estados posteriores ya distinguen las dos recomendaciones.

### `hoshai_balcon_valle` · `examine.cornisa`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Examinar cornisa antes de dejar la nota. Acción requerida.
- **Requiere código:** no

**Actual:** Oculta el paso frío incluso con buena luz.

**Propuesto:** La cornisa es un camino estrecho pegado a la roca. Tiene apoyos para los pies y sitio para una persona con un bulto pequeño; un carro no cabe. Detrás de la roca el camino se pierde de vista un rato y vuelve a aparecer más abajo.

**Por qué:** El original («Oculta el paso frío incluso con buena luz») no daba base para decidir. Ahora las dos notas tienen sentido.


## A6 · velmora_recipiente · Varo, Elin y Desi (Nhal)

### `velmora_recipiente` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Elin espera su recipiente pequeño, pero en el secadero también está el juguete de Desi. Una tabla le sirve de apoyo. Pregunta a Elin cuál es su pieza y a Desi cómo retirarla sin tirar el juguete. Devuelve el recipiente a Elin y vuelve a verme. No quiero que arreglemos un préstamo dejando otro trabajo en el suelo.

**Propuesto:** Elin, la artesana, dejó a reparar su recipiente pequeño en el taller de Desi y me pidió que se lo llevara. Yo no puedo dejar el puesto. Ya está arreglado y se está secando en el secadero, al lado de un juguete recién pegado. Comparten apoyo: si lo levantas mal, el juguete se cae. Habla primero con Elin, en su puerta, pasado el patio de reuniones, para saber cuál es el suyo. Luego pregunta a Desi, en el taller, cómo sacarlo. Llévaselo a Elin y vuelve a decirme que lo tiene.

**Por qué:** El original mezclaba dos recipientes y nombraba a Leris (otra historia). Ahora: un objeto, una dueña, un peligro concreto (el juguete), el orden real que exige el motor (Elin → Desi → secadero → Elin).

### `velmora_recipiente` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Varo paga por aclarar el préstamo del recipiente y devolverlo a Elin. Pregunta a Desi en el taller y a Elin junto al patio del relato. Conserva la tabla que sostiene el juguete.

**Propuesto:** Varo, el comerciante, te pide llevar a Elin su recipiente pequeño, que se está secando en el taller de Desi junto a un juguete. Pregunta a Elin cuál es (su puerta está al este del patio de reuniones) y a Desi cómo sacarlo sin mover el apoyo del juguete (el taller está al norte del claro). Recógelo en el secadero, entrégaselo a Elin y vuelve al mercado.

**Por qué:** Resumen. Quita «Conserva la tabla que sostiene el juguete» sin explicar por qué.

### `velmora_recipiente` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Varo en el mercado de Velmora para contarle el resultado y cobrar.

**Propuesto:** Elin ya tiene su recipiente y el juguete sigue secándose en su tabla. Vuelve al mercado de Velmora para contárselo a Varo.

**Por qué:** Se dispara en la puerta de Elin.

### `velmora_recipiente` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** En el camino de vuelta al mercado recuerdas la tabla que quedó bajo el juguete. El recipiente pequeño llegó a Elin, y el apoyo de Desi siguió haciendo su trabajo. Dos piezas que parecían estorbarse terminaron cada una donde hacía falta.

**Propuesto:** Le cuentas a Varo que Elin recibió su recipiente y que el juguete sigue en su apoyo del secadero.

**Por qué:** Varo no ve nada desde el puesto; la entrega es la noticia.

### `velmora_recipiente` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Así sí. Elin tiene su recipiente y el juguete no quedó tirado cuando lo retiraste. Yo veía una pieza que había que devolver; tú preguntaste por lo que la sostenía. Toma el pago. Me alegra que el préstamo terminara sin una discusión por otra cosa rota.

**Propuesto:** Bien hecho. Elin tiene lo suyo y Desi no tendrá que volver a arreglar el juguete. Así me gusta que se hagan los recados.

**Por qué:** Consecuencia doble, sin acusar a nadie.

### `nhal_varo` · `topics.recipiente`

- **Archivo:** `content/regions/nhal.json` → `npcs`
- **Aparece:** Hablar con Varo · recipiente, antes de completar la entrega.
- **Requiere código:** no

**Actual:** Elin espera su recipiente pequeño y el taller lo necesita separar con cuidado. Leris conoce una parte de la historia; Elin y Desi pueden explicarte el resto. Pregunta antes de mover el apoyo del secadero. Quiero que la devolución ayude a Elin sin dejar a Desi con un juguete roto.

**Propuesto:** Elin dejó a reparar su recipiente pequeño en el taller de Desi. Ya está arreglado, secándose al lado de un juguete. No lo cojas sin preguntar: primero habla con Elin para saber cuál es, y con Desi para saber cómo sacarlo.

**Por qué:** Mismo orden y mismas personas que el encargo; quita a Leris de este hilo.

### `nhal_elin` · `topics.entrega.text`

- **Archivo:** `content/regions/nhal.json` → `npcs`
- **Aparece:** Hablar con Elin · entrega. Fija nhal_elin_recipiente_reconocido.
- **Requiere código:** no

**Actual:** El recipiente pequeño que espero está junto al secadero. No es el que usamos para repartir comida en el patio. Allí hay un aro mío que lo apoya y una tabla de Desi bajo un juguete reparado. Pregúntale qué puedes levantar antes de traerlo: quiero recuperar mi recipiente sin desmontar ese trabajo.

**Propuesto:** El pequeño, el que está en el taller, es mío. No lo confundas con el cuenco grande del patio, que es de todos. El aro y la tabla donde se seca son de Desi. Pregúntale cómo sacarlo sin tirar nada.

**Por qué:** Corrige una contradicción: decía «el aro es mío», pero la acción y los estados dejan el aro en el taller. También era narración dentro de la voz.

### `nhal_desi` · `topics.apoyo.text`

- **Archivo:** `content/regions/nhal.json` → `npcs`
- **Aparece:** Hablar con Desi · apoyo. Fija nhal_desi_apoyo_aclarado.
- **Requiere código:** no

**Actual:** El recipiente pequeño de Elin se puede levantar, pero no tires de todo lo que hay debajo. La tabla sostiene el juguete reparado del secadero, que es otra pieza distinta de mi figura de Rondamusgo. El aro apoya el recipiente; déjalo también aquí cuando lo levantes. Lleva sólo el recipiente a Elin. Así ella podrá usarlo sin desmontar el trabajo del secadero.

**Propuesto:** Llévate sólo el recipiente. El aro y la tabla se quedan: la tabla sostiene el juguete, que todavía está húmedo. Si la mueves, la pata se tuerce y vuelta a empezar.

**Por qué:** Decía «el aro puede llevarse», contrario a la acción del secadero. Quita las comillas internas.

### `nhal_umbral_elin` · `actions[id=nhal_entregar_recipiente].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Acción «Devolver el recipiente a Elin» con el recipiente en la mochila y Elin presente.
- **Requiere código:** no

**Actual:** Elin recibe el recipiente pequeño y lo deja junto a su puerta. Le explicas que la tabla sigue bajo el juguete y el aro vacío quedó en el secadero. «Me alegra tenerlo de vuelta», dice. «Y me alegra que ella pueda terminar lo suyo. Gracias por preguntar antes de tirar de todo.» La pieza vuelve a su dueña sin desmontar el apoyo del taller.

**Propuesto:** Le das a Elin su recipiente pequeño. Lo gira con la mano buena y sonríe al ver la reparación. Cuando le cuentas que la tabla se quedó sosteniendo el juguete, asiente: «Bien. Que una ayuda no deje otra cosa rota detrás.»

**Por qué:** Más concreto (mano buena: su lesión es canon) y la cita queda como narración.


## A7 · narevia_preparativos · Tila, Nima y el paño (Lethra)

### `narevia_preparativos` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Tengo que llevar cuencos para la reunión, pero Nima necesita saber dónde ponerlos. Mira el paño de Mira en la plataforma de secado y revisa sus costuras. Puedes proponer esperar a que seque o usar el rincón cubierto de la cocina. Cuéntaselo a Nima y vuelve con esa decisión. No hace falta llevar un paño mojado encima de la comida.

**Propuesto:** Mira y su hermana Sola van a cenar con sus familias en la cocina vecinal. Yo llevo los cuencos, pero no sé dónde ponerlos. Mira quiere cubrir la mesa con el paño común, el que tiene costuras de toda la familia, y todavía está secándose en la plataforma. Ve a mirar las costuras: desde la plaza, entra en el taller de fibras y baja a la plataforma de secado. Decide si conviene esperar a que seque o cenar bajo la cubierta y dejarlo tendido. Cuéntaselo a Nima, en la cocina, y vuelve para decirme adónde llevo los cuencos.

**Por qué:** Da a Tila un motivo propio (lleva los cuencos) y presenta la cena de las hermanas, que es el corazón de la historia de Lethra. Ruta: mercado → norte → este → sur; cocina: este → sur.

### `narevia_preparativos` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Tila paga por comprobar el paño en la plataforma de Mira y llevar una propuesta a Nima en la cocina. Puedes elegir esperar a que seque o mantener la reunión bajo cubierta.

**Propuesto:** Tila lleva los cuencos para la cena de Mira y Sola en la cocina vecinal. Mira las costuras del paño común en la plataforma de secado (al sur del taller de fibras) y elige: esperar a que seque para cubrir la mesa, o cenar bajo la cubierta y dejarlo tendido. Lleva tu propuesta a Nima, en la cocina, y vuelve al mercado con Tila.

**Por qué:** Resumen. Quita el «Puedes elegir…» abstracto.

### `narevia_preparativos` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Tila en el mercado de hojas de Narevia para contarle el resultado y cobrar.

**Propuesto:** Nima ya sabe dónde irán los cuencos. Vuelve al mercado de Narevia para decírselo a Tila.

**Por qué:** Se dispara en la cocina.

### `narevia_preparativos` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** Vuelves al mercado con el recuerdo de las costuras del paño y de los cuencos que esperan en la cocina. Nima ya recibió tu propuesta. Ahora puedes contar a Tila dónde acordaron preparar la reunión.

**Propuesto:** Le dices a Tila lo que acordaste con Nima. Tila cuenta los cuencos y los pasa a la cesta de arriba, la que no se moja.

**Por qué:** Usa el detalle del mercado: las cestas se levantan del fondo para no mojarse.

### `narevia_preparativos` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Gracias. Saber dónde van los cuencos me ayuda más que apilarlos deprisa y cambiarlos de sitio después. Nima ya tiene tu propuesta; yo puedo preparar la entrega pensando en ese lugar. Cuando empiece la reunión, cada persona tendrá bastante que hacer sin perseguir una mesa.

**Propuesto:** Entonces ya sé adónde ir. Llevaré los cuencos antes de que empiece la cena.

**Por qué:** Breve: la escena fuerte ya ocurrió en la cocina.

### `lethra_nima` · `topics.preparativos.text`

- **Archivo:** `content/regions/lethra.json` → `npcs`
- **Aparece:** Hablar con Nima · preparativos, tras elegir en la plataforma (lethra_plan_elegido). Fija lethra_reunion_comunicada. Acción requerida.
- **Requiere código:** no

**Actual:** Nima deja la cuchara en un plato para escucharte. Anota dónde reunir los cuencos y llama a Mira desde la cocina para preguntar cómo sigue el paño. «Bien, ya sé dónde preparar la mesa. Así no tendré que buscar sitio con la olla en las manos.»

**Propuesto:** Bien pensado. Apunto dónde van los cuencos, así no los movemos dos veces. Ahora le aviso a Mira para que sepa qué hacemos con el paño.

**Por qué:** Era narración impresa como «Nima: Nima escucha…».

### `lethra_plataforma_secado` · `examine.costuras`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Examinar costuras en la plataforma. Acción requerida.
- **Requiere código:** no

**Actual:** Distintas manos repararon el paño a lo largo de reuniones familiares.

**Propuesto:** Distintas manos repararon el paño en distintas reuniones familiares. La costura más corta todavía está húmeda al tocarla; las demás ya secaron.

**Por qué:** Da al jugador un dato para elegir entre esperar o cenar bajo cubierta. La costura corta es la de Sola (canon).


## A8 · vaisgard_aviso_carga · Arel, Tov y Nera (Veyra)

### `vaisgard_aviso_carga` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Una carga se ha retrasado y el aviso tiene que llegar al archivo. Ve a la puerta del camino de Korven y escucha a Tov; después habla con Nera en el archivo de cargas. Puedes transmitir lo que te dijo, indicando de quién viene, o pedir que lo comprueben. No escribas que hubo un robo sólo porque el envío aún no llegó.

**Propuesto:** Ha llegado un rumor: dicen que a Tov, la porteadora de piedra, le han robado la carga. No pienso repetirlo sin saber de dónde viene. Tov está con su carro en la puerta del camino de Korven: desde la plaza de las cinco rutas, cruza el patio de los animales hacia el oeste. Pregúntale qué pasó de verdad. Después lleva su noticia a Nera, en el archivo de cargas, aquí al lado, al este. Vuelve cuando Nera lo haya apuntado.

**Por qué:** El rumor de robo se vuelve el problema concreto. Rutas comprobadas (patio de mensajes → oeste ×3; archivo al este).

### `vaisgard_aviso_carga` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Arel paga por escuchar a Tov junto a la puerta de piedra y llevar a Nera un aviso con su procedencia. Puedes registrar lo que Tov dijo o pedir una comprobación; ninguna opción debe inventar un robo.

**Propuesto:** Arel, la mensajera, ha oído que robaron la carga de Tov y no quiere repetirlo sin comprobarlo. Pregunta a Tov en la puerta del camino de Korven (al oeste, pasado el patio de los animales) y lleva su noticia a Nera, en el archivo de cargas, al este del patio de mensajes. Vuelve con Arel cuando Nera lo haya apuntado.

**Por qué:** Quita «ninguna opción debe inventar un robo» (voz de diseño).

### `vaisgard_aviso_carga` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Arel en el patio de señales de Vaisgard para contarle el resultado y cobrar.

**Propuesto:** Nera ya tiene apuntada la noticia de Tov. Vuelve al patio de mensajes, al oeste, para contárselo a Arel.

**Por qué:** Se dispara en el archivo; el patio está justo al oeste.

### `vaisgard_aviso_carga` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** El patio de señales tiene muchas noticias esperando camino. La que traes conserva un nombre y un lugar: Tov, junto a la puerta de piedra. Tu aviso llegó al archivo con ese origen; puedes volver a él si alguien necesita preguntar más.

**Propuesto:** Le cuentas a Arel lo que dijo Tov y lo que apuntó Nera. Arel copia el aviso en una tablilla nueva y escribe debajo de dónde viene.

**Por qué:** Coincide con la memoria posterior de Arel (copia con fuente).

### `vaisgard_aviso_carga` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Gracias por escuchar antes de traer la noticia. Si alguien pregunta, sabremos con quién hablar y dónde encontrarlo. Una carga que tarda ya preocupa bastante; no quiero añadir un susto que nadie pueda explicar. Tu recado llegó al archivo con su procedencia.

**Propuesto:** Separador roto, no robo. Eso es lo que saldrá por los caminos. Si hubiera repetido el rumor, Tov habría tenido que arreglar también su nombre.

**Por qué:** Retoma la frase de Tov («tendré que reparar también esa historia»).

### `veyra_tov` · `topics.aviso.text`

- **Archivo:** `content/regions/veyra.json` → `npcs`
- **Aparece:** Hablar con Tov · aviso. Fija encargo_veyra_demora_conocida. Acción requerida.
- **Requiere código:** no

**Actual:** «Mi carga está entera. Se ha roto un separador; necesito recolocarla antes de entrar. Dile a Nera que llegaré tarde, no que se ha perdido.»

**Propuesto:** Nadie me ha robado nada. La carga está entera, mírala. Se rompió un separador, esta tabla de aquí, y tengo que volver a colocar las piedras antes de entrar. Dile a Nera que llegaré tarde, no que he perdido la carga.

**Por qué:** Quita las comillas internas y añade el gesto de mostrar la tabla rota.

### `veyra_nera` · `topics.aviso_preciso.text`

- **Archivo:** `content/regions/veyra.json` → `npcs`
- **Aparece:** Hablar con Nera · aviso_preciso, tras escuchar a Tov y antes de entregar. Fija encargo_veyra_aviso_entregado y _preciso.
- **Requiere código:** no

**Actual:** Nera escucha el nombre de Tov y anota: «Puerta de piedra. Tabla separadora rota. Carga entera, llegada tardía». Deja el envío en la lista de llegadas. «Así sé qué ocurrió y quién te lo mostró. No voy a escribir que hubo un robo.»

**Propuesto:** Separador roto, carga entera, llegará tarde. Y lo dice la propia Tov. Lo apunto así, con su nombre. La carga sigue en la lista de llegadas; nadie va a hablar de robo.

**Por qué:** Era narración («Nera anota…») dentro de la voz.

### `veyra_nera` · `topics.pedir_comprobacion.text`

- **Archivo:** `content/regions/veyra.json` → `npcs`
- **Aparece:** Hablar con Nera · pedir_comprobacion (alternativa a la anterior). Fija encargo_veyra_aviso_entregado y _comprobar.
- **Requiere código:** no

**Actual:** Le pides a Nera que compruebe la noticia con Tov. Ella deja una marca de espera junto al envío. «Hablaré con ella sobre la tabla rota antes de cambiar la lista. Mientras tanto seguirá pendiente; no lo daré por perdido.»

**Propuesto:** De acuerdo, no cambio nada todavía. Dejo la carga como pendiente. Antes de tocar la lista iré a ver ese separador con Tov. Hasta entonces no está perdida: sólo tarda.

**Por qué:** Era narración del jugador («Pides a Nera…»). Mantiene el hecho: queda pendiente, no perdida.

### `veyra_nera` · `topics (claves)`

- **Archivo:** `content/regions/veyra.json` → `npcs`
- **Aparece:** Etiquetas de los botones «Nera · aviso_preciso» y «Nera · pedir_comprobacion».
- **Requiere código:** no

**Actual:** (no existe)

**Propuesto:** {"aviso_preciso": "anotar lo que dijo Tov", "pedir_comprobacion": "pedir que lo compruebe"}

**Por qué:** Cambio de datos opcional: renombrar las dos claves para que el botón no muestre guiones bajos. Ningún encargo referencia estos temas por clave; revisar tests antes.


## A9 · vaisgard_toldo · Seli (Veyra)

### `vaisgard_toldo` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Esta costura vieja se está abriendo. Si la sujeto tapando por dónde sale el agua, el taller de abajo tendrá otro problema. Examina la unión antes de ayudarme. Podemos usar el junco que presta Bela o preparar las perchas para que yo termine la sujeción. Las dos formas sirven; no necesitas comprar material sólo para este encargo.

**Propuesto:** El toldo que comparto con mi vecino se ha rasgado por una costura vieja. Cuando llueve, el agua cae justo en la puerta del taller de abajo, y ya hablan de cerrarlo. No hace falta: basta con coser bien y dejar que el agua salga hacia la calle. Primero mira la costura, para ver dónde está el daño. Después puedes ayudarme de dos maneras: traer un haz de junco (Bela, en el mercado de aquí al oeste, presta uno para esto) y lo atamos, o sujetarme las perchas mientras marco la costura, y yo la termino después sin gastar junco.

**Por qué:** Qué pasa, a quién perjudica, qué no hay que hacer (cerrar el taller) y las dos formas reales de ayudar que ofrece la sala.

### `vaisgard_toldo` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Seli paga por comprobar la costura y ayudar a sujetar el toldo. Puedes utilizar junco —Bela presta un haz una sola vez— o preparar las perchas para que Seli termine sin gastar material.

**Propuesto:** Seli tiene un toldo rasgado que moja la puerta del taller de abajo. Examina la costura en la calle de los toldos. Luego elige: llevarle un haz de junco (Bela, en el mercado al oeste, presta uno) para atar el desgarro, o sujetar las perchas para que Seli lo termine. El encargo se entrega aquí mismo, a Seli.

**Por qué:** Resumen.

### `vaisgard_toldo` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Seli en la calle de los toldos para contarle el resultado y cobrar.

**Propuesto:** El toldo ya tiene arreglo y el agua podrá salir hacia la calle. Puedes cerrar el encargo con Seli aquí mismo.

**Por qué:** Todo ocurre en la misma calle.

### `vaisgard_toldo` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** La costura vieja ya no es sólo una raya que viste al pasar. Sabes dónde hace falta sujetarla y has ayudado a preparar ese trabajo. El borde por donde sale el agua sigue libre; al volver junto al toldo, reconoces los apoyos de la unión antes de levantar la vista hacia la tela.

**Propuesto:** Seli tira del borde del toldo para probarlo. Esta vez, cuando llueva, el agua resbalará hacia la calle y no hacia la puerta del taller.

**Por qué:** No depende de que esté lloviendo ahora.

### `vaisgard_toldo` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Me has dejado una ayuda concreta. Si usamos junco, revisaré el amarre; si preparaste las perchas, seguiré desde esas marcas. Lo importante es que el agua aún tiene por dónde salir. Gracias. A veces un arreglo pequeño evita que dos vecinos se pasen la tarde discutiendo.

**Propuesto:** El taller de abajo podrá seguir abierto. Ya les diré a los vecinos que no hacía falta cerrar nada: sólo coser bien.

**Por qué:** Cierra el motivo de Seli (tema «vecinos»).

### `veyra_calle_toldos` · `actions[id=veyra_preparar_perchas].text`

- **Archivo:** `content/regions/veyra.json` → `rooms`
- **Aparece:** Acción «Preparar las perchas para que Seli termine» con Seli presente.
- **Requiere código:** no

**Actual:** Sostienes la percha para que Seli alcance la costura. Ella marca el comienzo del desgarro y el borde por donde debe salir el agua. «Con esto preparado puedo seguir sin tener que buscar de nuevo la rotura.» No gastas junco ni terminas el amarre; si llevas fibra prestada, puedes devolverla a Bela.

**Propuesto:** Sostienes las perchas mientras Seli marca con tiza dónde empieza el desgarro y por dónde debe salir el agua. Ella terminará la costura sin gastar junco. Si Bela te prestó un haz, puedes devolvérselo en el mercado.

**Por qué:** Convierte la orden «devuelve cualquier fibra prestada a Bela» en información, y nombra dónde.


## A10 · brumak_taza · Taren (Korven)

### `brumak_taza` · `accept_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.
- **Requiere código:** no

**Actual:** Quiero hacer una taza que mi madre pueda sostener, no ganar un concurso por la taza más grande. Pídeme las medidas y mira el recipiente del horno viejo. Después puedes recomendar conservar el aro pequeño o darle una base un poco más ancha. Vuelve a explicarme la elección. Fabricar y probar la taza será mi parte del trabajo.

**Propuesto:** Quiero hacerle una taza a mi madre. La primera me salió tan pequeña que no le cabía nada; la segunda, tan grande que no la puede levantar. Antes de hacer la tercera necesito otra mirada. Pídeme las medidas, ve al horno viejo, aquí al este, y mira el recipiente torcido del banco: ahí se ve qué pasa cuando la base no va de acuerdo con el resto. Marca allí lo que recomiendas y vuelve a decírmelo.

**Por qué:** Retoma la gracia del tema «pieza» (taza pequeña, taza enorme) y da un objetivo claro.

### `brumak_taza` · `accept_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.
- **Requiere código:** no

**Actual:** Taren paga por comparar sus muestras y recomendar una taza manejable. Pídele las medidas, comprueba las piezas del horno junto al entrante y vuelve con una decisión sobre aro y base.

**Propuesto:** Taren, la alfarera, quiere hacer una taza para su madre que no sea ni muy pequeña ni muy pesada. Pídele las medidas, examina el recipiente torcido del horno viejo (al este) y marca allí tu recomendación: base más ligera o base más ancha. Vuelve a contárselo. Taren trabaja de día.

**Por qué:** «Taren trabaja de día» avisa del horario real (schedule: día).

### `brumak_taza` · `ready_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».
- **Requiere código:** no

**Actual:** Ya completaste la tarea de este encargo. Vuelve a Taren en el entrante de piezas de Brumak para contarle el resultado y cobrar.

**Propuesto:** Taren ya tiene tu recomendación. Puedes cerrar el encargo con ella aquí, en el rincón de las muestras.

**Por qué:** La última condición es hablar con Taren en su rincón.

### `brumak_taza` · `delivery_text`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.
- **Requiere código:** no

**Actual:** De vuelta en el entrante, las piezas pequeñas llaman tu atención tanto como las grandes. Recuerdas las marcas de la mano y el espesor del recipiente junto al horno. Tu recomendación sobre el aro y la base ya tiene esas comparaciones detrás.

**Propuesto:** Taren pone tu marca junto a las medidas de la mano y aparta un trozo de arcilla para la prueba.

**Por qué:** Coincide con su memoria posterior («alinea la arcilla con tu marca»).

### `brumak_taza` · `payment_dialogue`

- **Archivo:** `content/world.json` → `quests`
- **Aparece:** Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.
- **Requiere código:** no

**Actual:** Con esto puedo empezar otra prueba sin volver a hacer una taza enorme por miedo a que quede pequeña. Gracias por mirar las muestras y explicarme tu elección. Todavía tendré que comprobar el peso y el agarre; quiero que mi madre la use, no que la admire desde el estante.

**Propuesto:** Esta vez empiezo por lo que necesita mi madre, no por lo que me sale de las manos. Gracias por mirar con calma.

**Por qué:** Prepara el remate cómico ya existente (la taza grande acaba siendo para su hermano).

### `korven_taren` · `topics.medidas.text`

- **Archivo:** `content/regions/korven.json` → `npcs`
- **Aparece:** Hablar con Taren · medidas (de día). Fija encargo_korven_taza_medida. Acción requerida.
- **Requiere código:** no

**Actual:** Quiero que mi madre pueda sostener la taza sin apretar las dos manos. Tengo sus medidas marcadas en esta tabla. La muestra está junto al horno, un paso al este: mira el borde y compara conservar el aro con ensanchar la base. No busco la taza más grande; busco una que pueda usar a gusto.

**Propuesto:** Mira estas dos marcas: la de la izquierda es la mano de mi madre; la de la derecha, la taza grande. El aro pequeño le queda bien a la mano, eso no lo cambio. Lo que dudo es la base: más ligera, para que pese menos, o más ancha, para que no se vuelque. Mira el recipiente torcido del horno y decide tú.

**Por qué:** Las dos opciones del horno no eran opuestas («conservar el aro» frente a «base ancha manteniendo el aro»). Ahora la elección es una sola pregunta: ligera o estable.

### `korven_taren` · `topics.recomendación.text`

- **Archivo:** `content/regions/korven.json` → `npcs`
- **Aparece:** Hablar con Taren · recomendación, tras marcar en el horno. Fija encargo_korven_taza_informada. Acción requerida.
- **Requiere código:** no

**Actual:** Taren compara tu recomendación con las marcas de la mano. «No has elegido sólo por tamaño. Haré una prueba antes de entregarla.»

**Propuesto:** Así que esto es lo que viste en el horno. Bien: no elegiste sólo por tamaño, pensaste en quien la va a usar. Haré una prueba con tu marca antes de dársela a mi madre.

**Por qué:** Era narración («Taren compara…») dentro de la voz.

### `korven_horno_reposo` · `actions[id=korven_recomendar_aro].label`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Botón en el horno tras pedir las medidas.
- **Requiere código:** no

**Actual:** Recomendar conservar el aro y aligerar la base

**Propuesto:** Recomendar una base más ligera

**Por qué:** Etiqueta simétrica con «Recomendar una base más estable».

### `korven_horno_reposo` · `actions[id=korven_recomendar_aro].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Al pulsar el botón anterior.
- **Requiere código:** no

**Actual:** Comparas las muestras y marcas una base menos gruesa, conservando el aro pequeño que Taren eligió para la mano de su madre. La marca propone una taza más ligera; falta que Taren compruebe cómo se sostiene antes de darla por buena.

**Propuesto:** Comparas el recipiente torcido con las medidas: lo que más pesa es la base, demasiado gruesa. Marcas una base más fina y dejas el aro como está, a la medida de la mano de la madre de Taren.

**Por qué:** Relaciona la decisión con lo que se ve en el recipiente.

### `korven_horno_reposo` · `actions[id=korven_recomendar_base].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Al pulsar «Recomendar una base más estable».
- **Requiere código:** no

**Actual:** Comparas las muestras y dibujas una base un poco más ancha sin agrandar el aro. Una taza necesita apoyo, pero también debe poder levantarse. Dejas la marca para que Taren pruebe cuánto peso añade esa base antes de hacer otra pieza.

**Propuesto:** Comparas el recipiente torcido con las medidas: se inclina porque la base es estrecha. Marcas una base un poco más ancha y dejas el aro pequeño. La taza pesará algo más, pero no se volcará.

**Por qué:** Consecuencia comprensible de la otra opción.


## B · Salteador de cargas (forajido_camino, común a 5 lugares)

### `forajido_camino` · `dialogue`

- **Archivo:** `content/world.json` → `creatures`
- **Aparece:** Botones «Hablar con Salteador de cargas · …» mientras está presente y no ha empezado el enfrentamiento. Común a Compuerta abierta (Edran), Campamento de la lona azul (Hoshai), Cruce de los sacos vacíos (Korven), Ribera hacia Edran (Lethra) y Subida entre árboles (Nhal). Debe valer en los cinco.
- **Requiere código:** no

**Actual:** {"exigencia": "Eh, viajero. Ese equipaje se queda aquí. Déjalo en el suelo y no des otro paso.", "salida": "¿Vas a volver por donde viniste? Entonces vuelve. Pero no pases junto a mí con esa carga.", "pelear": "No te acerques más. Tengo este palo y sé usarlo. Si quieres ese paso, tendrás que enfrentarte a mí."}

**Propuesto:** {"qué quieres": "Lo que lleves en la mochila. Déjala en el suelo y sigue tu camino. No me hace falta pelear contigo.", "por qué": "Este invierno nadie me ha contratado para cargar. Cuando no hay trabajo, el camino parece fácil de cobrar. Ya sé que no está bien. Hoy no se me ocurre otra cosa.", "dejar paso": "Por donde viniste está libre. Si das la vuelta, no te sigo."}

**Por qué:** Hoy usa el texto del motor («La carga se queda aquí…»). Tres temas: qué pide, por qué (motivo humano sin justificarlo) y la salida real. «No te sigo» es cierto: fuera de combate no hay persecución. No menciona agua, bosque ni piedra para servir en las cinco salas.

### `forajido_camino` · `description`

- **Archivo:** `content/world.json` → `creatures`
- **Aparece:** Examinar Salteador de cargas. Común a Compuerta abierta (Edran), Campamento de la lona azul (Hoshai), Cruce de los sacos vacíos (Korven), Ribera hacia Edran (Lethra) y Subida entre árboles (Nhal). Debe valer en los cinco.
- **Requiere código:** no

**Actual:** Una persona con ropa de viaje y un palo corto exige equipaje a quienes pasan. Mantiene una salida a su espalda. Su amenaza pertenece a este individuo, no a su pueblo ni a su especie.

**Propuesto:** Una persona con ropa de viaje gastada y un palo corto pide el equipaje a quien pasa. Se queda cerca de una salida, por si tiene que irse. Lo que hace es cosa suya: no habla por su pueblo ni por su especie.

**Por qué:** Mismo contenido canónico en lenguaje más llano.

### `forajido_camino` · `combat_intro`

- **Archivo:** `content/world.json` → `creatures`
- **Aparece:** Al elegir «Enfrentarte a Salteador de cargas».
- **Requiere código:** no

**Actual:** El salteador levanta el palo y se planta frente a ti. «¡La carga se queda!» Su pie tapa el paso mientras busca con la mirada tu próxima respuesta. El enfrentamiento ha empezado.

**Propuesto:** El salteador aprieta el palo con las dos manos y se planta delante de ti. «Está bien. Si no me das la carga, la tomaré yo.» Vigila el palo.

**Por qué:** Una frase suya antes del golpe, sin insultos. Usa «salteador», el nombre que ve el jugador, no «forajido».

### `forajido_camino` · `defeat_text`

- **Archivo:** `content/world.json` → `creatures`
- **Aparece:** Al vencer (antes de la línea de XP y sellos). El adversario vuelve a aparecer pasado un tiempo (world.deaths 300 s).
- **Requiere código:** no

**Actual:** El salteador baja el palo y se aparta del paso. Ya no avanza para cerrarte el camino. La pelea ha terminado; el espacio que ocupaba delante de ti queda libre.

**Propuesto:** El salteador tropieza y suelta el palo. Levanta las manos: «¡Basta! Ya está.» Lo recoge sin volver a alzarlo y se aparta del camino.

**Por qué:** No afirma muerte ni marcha definitiva (el motor lo repone). En Hoshai, Seran sigue en el campamento como NPC: «se aparta del camino» sigue siendo cierto.


## C · Fauna de Edran: una señal por lugar

### `edran_salida_huertos` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Salida de las Cercas Bajas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Algo pequeño y espinoso corre pegado a la cerca y se mete bajo una mata del borde. Desde allí asoma el hocico: es un Espinajo, y ese trozo de cerca es suyo.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_salida_huertos` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Salida de las Cercas Bajas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Una forma baja y alargada corre junto a la acequia y se para con la cabeza hacia un hueco de la cerca. Es un Mordelinde: busca por dónde irse, no a quién morder.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_salida_huertos` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Salida de las Cercas Bajas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** Lejos, más allá de la acequia, un lomo enorme asoma sobre la hierba. Es un Cornalomo. Cada paso suyo hunde la tierra. Mejor mirarlo desde aquí.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_arboleda` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Arboleda de los tres árboles. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Bajo las raíces levantadas del último árbol, un Espinajo escarba la tierra. Al oír tus pasos se pega al suelo con las espinas de punta y se queda quieto, vigilándote.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_arboleda` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Arboleda de los tres árboles. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Un Mordelinde sale de entre las raíces, aparta unas semillas con las manos y se queda quieto, mirando el hueco bajo la raíz más grande.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_arboleda` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Arboleda de los tres árboles. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** Entre los troncos se ve, a lo lejos, un Cornalomo arrancando hierba. Es más grande que el banco de tierra entero. No se acerca al sendero.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_camino_carros` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Camino de carros. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Un Espinajo cruza la rodada de la hondonada a toda prisa y se esconde entre las piedras bajas del borde. Las espinas le asoman por encima, quietas.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_camino_carros` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Camino de carros. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Un Mordelinde cruza la rodada alta pegado al suelo y se para junto a las piedras bajas, buscando un hueco entre ellas.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_camino_carros` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Camino de carros. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** En la hondonada, lejos de las rodadas, un Cornalomo se mueve despacio. El suelo tiembla un poco a cada paso.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_terraplen` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Terraplén de la Subida. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Entre las raíces del terraplén, un Espinajo baja la cabeza y eriza las espinas. Se ha quedado con el ensanche de media cuesta y no parece dispuesto a compartirlo.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_terraplen` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Terraplén de la Subida. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Un Mordelinde asoma de un agujero entre las raíces del terraplén. Mira el camino, mira el agujero, y espera.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_terraplen` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Terraplén de la Subida. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** Desde la media cuesta se ve un Cornalomo abajo, en el campo. Su lomo sobresale por encima de la hierba alta. Está lejos y no mira hacia el camino.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_linde_piedra` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Paso hacia Korven. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Entre las últimas matas antes de las piedras, un Espinajo corre unos pasos y se para. Vuelve al mismo borde y se agacha con las espinas hacia ti.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_linde_piedra` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Paso hacia Korven. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Entre dos piedras, un Mordelinde aparta semillas con las manos delanteras. Al notar tus pasos, gira la cabeza hacia la grieta más cercana.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_linde_piedra` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Paso hacia Korven. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** En el prado, al sur, un Cornalomo levanta la cabeza. Sus huellas son anchas como una rueda de carro. Desde las piedras se le ve bien, y de lejos.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sendero_juncos` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Sendero del Agua Oculta. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Un Espinajo sale de los juncos, cruza el sendero firme y se agacha en la zona despejada. Se queda ahí, de cara a ti, con las espinas levantadas.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sendero_juncos` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Sendero del Agua Oculta. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Un Mordelinde corre por el borde firme del sendero y se para a la entrada de los juncos, con el hocico hacia un paso entre los tallos.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sendero_juncos` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Sendero del Agua Oculta. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** Al otro lado de los juncos, un Cornalomo aplasta la hierba al pasar. Su peso se nota hasta en el agua quieta.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_parcela_vieja` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Parcela vieja. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Junto a la piedra de la parcela, un Espinajo da vueltas cortas entre las hileras viejas y siempre regresa al mismo rincón.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_parcela_vieja` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Parcela vieja. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Un Mordelinde escarba junto a la piedra, entre los brotes. Cuando te ve, deja de comer y mira hacia el rincón seco.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_parcela_vieja` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Parcela vieja. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** Más allá de la loma asoma el lomo de un Cornalomo. Va despacio y no se acerca a las hileras.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sauces` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Borde de los Sauces Bajos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Un Espinajo bebe entre las raíces del sauce. Al verte, retrocede hasta la hierba y se queda agazapado, con las espinas de punta.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sauces` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Borde de los Sauces Bajos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Un Mordelinde corre por la orilla bajo el sauce y se para con la cabeza hacia un hueco entre las raíces. Las aves del sauce ni se mueven.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sauces` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Borde de los Sauces Bajos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** Al otro lado del agua, un Cornalomo baja la cabeza para beber. Las aves del sauce se callan hasta que vuelve a levantarla.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_calzada` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Calzada de piedra. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Un Espinajo cruza los cantos a saltitos y se mete en el borde de hierba. Desde allí te sigue con la mirada.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_calzada` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Calzada de piedra. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Un Mordelinde cruza los cantos a toda prisa y se para en el borde de hierba, mirando un hueco entre las piedras.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_calzada` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Calzada de piedra. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** Detrás de la curva, fuera de la calzada, un Cornalomo pisa la hierba y la deja aplastada. Un carro espera a que se aleje antes de seguir subiendo.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sendero_regreso` · `wildlife_pool[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Senda de regreso. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** Al pie del árbol aislado, un Espinajo husmea el barro. Cuando te acercas, se aplasta contra la tierra y eriza las espinas.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sendero_regreso` · `wildlife_pool[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Senda de regreso. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Un Mordelinde aparece entre las raíces del árbol aislado, con semillas en las manos. Se queda quieto, mirando hacia un hueco bajo el tronco.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_sendero_regreso` · `wildlife_pool[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Senda de regreso. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** Lejos, en los campos, se ve el lomo de un Cornalomo por encima de la hierba. Desde el árbol aislado parece pequeño. No lo es.

**Por qué:** Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.

### `edran_surcos` · `signals[creature=espinajo_rastrojo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Señal fija del Campo de surcos (también la ven quienes buscan).
- **Requiere código:** no

**Actual:** Entre los tallos viejos se arquea un lomo provisto de espinas. El movimiento se mantiene alrededor de un espacio corto: acercarte abandonaría el sendero seguro.

**Propuesto:** En la hilera de tallos viejos, un Espinajo corre unos pasos, se para y vuelve al mismo borde. Cuando te mira, eriza las espinas y se agacha entre los tallos.

**Por qué:** Movimiento, refugio y reacción, como pidió Javier, sin prometer que se vaya.

### `edran_bajo_humedo` · `signals[creature=mordelinde].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Señal fija de la Hondonada húmeda.
- **Requiere código:** no

**Actual:** Una forma baja cruza entre raíces y se detiene con la cabeza orientada al borde. No persigue la sombra que pasa sobre el agua.

**Propuesto:** Una forma baja cruza la hierba oscura y se para en el borde del barro. El Mordelinde mira hacia un hueco entre las piedras: es la salida que vigila.

**Por qué:** La hondonada es barro, no agua abierta: quita la «sombra sobre el agua». No promete que huya (eso depende de cómo se acerque el jugador).

### `edran_prado` · `signals[creature=cornalomo].text`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Señal fija del Prado de las Marcas Anchas.
- **Requiere código:** no

**Actual:** Un cuerpo enorme aparta la hierba. El volumen de su lomo y la tierra hundida advierten una fuerza muy por encima de una primera formación.

**Propuesto:** En la zona aplastada del prado, un Cornalomo arranca hierba con calma. Cuando pisa, la tierra se hunde. Desde el sendero se le ve entero; acercarse ya es otra cosa.

**Por qué:** Quita «por encima de una primera formación» (lenguaje de reglas) y deja la advertencia en imagen.


## D · Narración metida en la voz de un NPC (fuera de encargos)

### `edran_nela` · `topics.cuerda.text`

- **Archivo:** `content/regions/edran.json` → `npcs`
- **Aparece:** Hablar con Nela · cuerda llevando una cuerda recuperada (la consume).
- **Requiere código:** no

**Actual:** Esta cuerda nos da otro apoyo para bajar. Ya la he atado al lado derecho de la escalera. La próxima vez podrás reconocer las dos desde arriba. Gracias por traer algo que también servirá a quienes vengan detrás de ti.

**Propuesto:** ¡Una cuerda buena! La ato en este tramo de la escalera. Ahora hay dos apoyos: cuando vuelvas a bajar, usa el de la derecha.

**Por qué:** Se imprimía «Nela: Nela prueba la cuerda… «…»».

### `edran_oren` · `topics.caja.text`

- **Archivo:** `content/regions/edran.json` → `npcs`
- **Aparece:** Hablar con Oren · caja. Fija edran_caja_localizada.
- **Requiere código:** no

**Actual:** Cuando entró agua, subí la caja a la repisa para que no se estropearan las cuñas. Está detrás de la compuerta, en el ramal este de la bifurcación. Dejé mi taza en el escalón seco para reconocer el regreso. Si la buscas para Nela, sigue la cuerda y no te metas donde el agua sea demasiado alta.

**Propuesto:** La subí a la repisa cuando entró agua. La repisa queda detrás de la compuerta, al este de la bifurcación. Por eso dejé la taza en el escalón seco.

**Por qué:** Sólo quita las comillas internas.

### `edran_oren` · `topics.ayuda.text`

- **Archivo:** `content/regions/edran.json` → `npcs`
- **Aparece:** Hablar con Oren · ayuda (una vez). Fija edran_oren_orientado.
- **Requiere código:** no

**Actual:** ¿Nela está junto a la entrada? Puedo ir a preguntarle si necesita ayuda con el canal. Voy a recoger la manta antes de salir. Gracias por hablar conmigo; llevaba tanto rato pensando en el carro que no veía por dónde empezar otra vez.

**Propuesto:** ¿Nela, la del canal? Si tiene trabajo, prefiero eso a seguir aquí abajo. Recojo la manta y voy a hablar con ella.

**Por qué:** Era narración del jugador («Le indicas…») dentro de la voz de Oren.


## E · Fauna de Hoshai

### `hoshai_estribacion` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Primera subida. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Junto al arroyo, un Uñapiedra sube por una roca casi lisa. Sus uñas se agarran a bultos que tú ni ves. Se para a media altura y te mira de lado.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_estribacion` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Primera subida. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Muy arriba, en la sierra, una forma grande cruza una cornisa y deja caer piedrecitas. Es un Rasgacumbres. Desde aquí abajo parece pequeño.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_repecho_raices` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Cuesta de las raíces. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Un Uñapiedra trepa por la roca que asoma entre dos raíces. Cuando pasas, se aplasta contra la piedra y se queda quieto, del mismo color que ella.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_repecho_raices` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Cuesta de las raíces. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Por encima de los árboles inclinados, unas garras rascan la roca. Un Rasgacumbres asoma en un saliente lejano y vuelve a quedar tapado por la curva.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_pared_goteo` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Pared húmeda. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Sobre la pared húmeda, un Uñapiedra avanza por donde gotea el agua. Prueba cada saliente con una uña antes de apoyarse.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_pared_goteo` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Pared húmeda. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** En la ladera de enfrente, al otro lado del valle, un Rasgacumbres baja despacio entre rocas. Las piedras que suelta tardan en dejar de sonar.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_pinar_discontinuo` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Pinar abierto. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Un Uñapiedra pasa de un pino a una roca sin pisar las agujas del suelo. Se queda agarrado al lado de la piedra donde no da el viento.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_pinar_discontinuo` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Pinar abierto. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Desde un claro del pinar se ve, lejos y arriba, un Rasgacumbres sobre un risco. Tiene la cabeza vuelta hacia el valle, no hacia ti.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_agua_fria` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Cruce de agua fría. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** En la piedra grande que desvía el agua, un Uñapiedra bebe agarrado al borde. Cuando te acercas a la orilla, sube un palmo y espera.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_agua_fria` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Cruce de agua fría. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Río arriba, en las rocas, hay marcas frescas de garras. Más lejos todavía, un Rasgacumbres se mueve entre las piedras altas.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_ladera_hitos` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Ladera de las señales. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Un Uñapiedra se queda quieto encima de un grupo de piedras de señal, como si fuera una más. Sólo se le nota cuando cambia una uña de sitio.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_ladera_hitos` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Ladera de las señales. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Por encima del paso entre paredes, un Rasgacumbres cruza la ladera de lado. Una piedra suelta rueda desde donde pisó y se para lejos del sendero.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_cuello_roca` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Paso entre paredes. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** En la pared del paso estrecho, un Uñapiedra se pega a la roca por encima de las cabezas. Cuando alguien golpea la piedra de aviso, se queda inmóvil.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_cuello_roca` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Paso entre paredes. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Arriba, en el borde de las paredes, una sombra grande tapa la luz un momento. Un Rasgacumbres mira el paso desde lo alto y sigue de largo.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_escalones_sol` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Escalones al sol. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Un Uñapiedra toma el sol en un escalón tallado, lejos del canal. Al ver tus pies, se pasa al borde de una piedra nueva, sin estorbar a nadie.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_escalones_sol` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Escalones al sol. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Desde los escalones se ve la sierra. En una cornisa lejana, un Rasgacumbres se estira al sol. En los peldaños nadie deja de trabajar por él.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_collado_pino` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Paso del último pino. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Un Uñapiedra rodea el pino por las piedras partidas. Se para en la raíz más alta y te sigue con la mirada.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_collado_pino` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Paso del último pino. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Por encima del collado, un Rasgacumbres cruza una pared de roca. Cuando se detiene, sus garras dejan un rasguño claro en la piedra.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_aprisco_abierto` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Refugio del rebaño. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Un Uñapiedra se asoma por encima de la pared seca del aprisco. El rebaño no le hace caso, y él tampoco al rebaño.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_aprisco_abierto` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Refugio del rebaño. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** El rebaño se aprieta contra el lado protegido de la ladera. Muy arriba, un Rasgacumbres recorre la cresta. La pastora lo mira sin moverse.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_garganta_oeste` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Garganta hacia Korven. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** En la pared de la garganta, un Uñapiedra se agarra a una roca clara. Sus uñas levantan un poco de polvo.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_garganta_oeste` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Garganta hacia Korven. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Por encima de la garganta, un Rasgacumbres baja hasta media pared y se para. Desde el ensanchamiento sólo se ven sus patas y una lluvia de polvo.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.

### `hoshai_senda_dosel` · `wildlife_pool[creature=unapiedra].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Senda de los árboles altos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Unapiedra cruza la pendiente pegado a la roca. Sus uñas encuentran apoyos junto al camino.

**Propuesto:** Un Uñapiedra sube por una roca con musgo junto al banco seco. Se mueve despacio, una pata cada vez.

**Por qué:** Hoy la misma frase sale en 12 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `hoshai_senda_dosel` · `wildlife_pool[creature=rasgacumbres].text`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Senda de los árboles altos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Ves marcas profundas de garras. Más arriba, un Rasgacumbres se mueve entre las rocas; puedes mantener la distancia.

**Propuesto:** Entre los árboles altos se ve un trozo de montaña. Allí arriba, un Rasgacumbres cruza un paso de roca y se queda mirando el valle.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 12 lugares.


## F · Fauna de Korven

### `korven_loma_cascajo` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Loma de las piedras claras. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** Del montón de cascajo asoma una cabeza alargada. El Colagrieta mira la pala y retrocede hacia una grieta, apoyándose en la cola gruesa.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_loma_cascajo` · `wildlife_pool[creature=cascapedernal].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Loma de las piedras claras. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un pequeño caparazón moteado se aparta hacia una junta de roca al cambiar la sombra.

**Propuesto:** En el cascajo, un Cascapedernal se recoge contra una piedra grande cuando tu sombra lo cubre. Su caparazón da un golpe seco contra la roca.

**Por qué:** Hoy la misma frase sale en 4 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_loma_cascajo` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Loma de las piedras claras. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Hacia el oeste, entre las rocas del cauce, un bloque se mueve. Detrás, un Quebrarrocas sigue empujando. El polvo sube hasta la loma.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_cauce_duro` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Cauce seco. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** Un Colagrieta toma el sol en una piedra del cauce. Al notar tus pasos en la arena, se mete de golpe en una junta; sólo queda fuera la punta de la cola.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_cauce_duro` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Cauce seco. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Cauce abajo se oye piedra contra piedra. Un Quebrarrocas aparta bloques del fondo seco, lejos del cuenco de las herramientas.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_meseta_baja` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Meseta de las dos piedras. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** A la sombra de una de las dos piedras, un Colagrieta asoma la cabeza por una fisura. Cuando la sombra se mueve, él se mueve con ella.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_meseta_baja` · `wildlife_pool[creature=cascapedernal].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Meseta de las dos piedras. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un pequeño caparazón moteado se aparta hacia una junta de roca al cambiar la sombra.

**Propuesto:** Al pie de la otra piedra, un Cascapedernal raspa liquen. Cuando le cae tu sombra, recoge las patas y se queda pegado a la roca.

**Por qué:** Hoy la misma frase sale en 4 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_meseta_baja` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Meseta de las dos piedras. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Bajo la pared de la meseta, lejos de las dos piedras, un Quebrarrocas empuja una losa con el hombro. La losa cae de lado y el golpe rebota en la roca.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_hitos_paso` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Camino de los mojones. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** En la base de un mojón, un Colagrieta saca la cabeza de un hueco. Mira la pila de piedras y vuelve a meterse.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_hitos_paso` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Camino de los mojones. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Lejos de los mojones, un Quebrarrocas abre paso entre rocas que nadie ha marcado. Cada empujón deja una franja de polvo nueva.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_hendidura_transito` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Paso estrecho. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** Por una grieta alta del paso estrecho asoma un Colagrieta. Cuando una rueda golpea la tabla, se esconde de golpe y luego vuelve a asomar.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_hendidura_transito` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Paso estrecho. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Al otro lado de la pared se oye arrastrar piedra. Por un hueco alto se ve el lomo de un Quebrarrocas empujando un bloque, lejos del sendero.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_cauce_observacion` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Cauce de piedras movidas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** Entre las piedras movidas, un Colagrieta busca una grieta. Prueba una, no cabe, y prueba otra.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_cauce_observacion` · `wildlife_pool[creature=cascapedernal].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Cauce de piedras movidas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un pequeño caparazón moteado se aparta hacia una junta de roca al cambiar la sombra.

**Propuesto:** Bajo una piedra de cara limpia, un Cascapedernal se mete de lado. El borde del caparazón roza la roca con un golpe breve.

**Por qué:** Hoy la misma frase sale en 4 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_cauce_observacion` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Cauce de piedras movidas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Al fondo del cauce, un Quebrarrocas apoya el cuerpo contra un bloque y lo hace rodar. Así se ven las piedras de cara limpia: alguien las ha movido.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_desvio_horno` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Desvío al horno. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** Entre los trozos de recipientes, un Colagrieta asoma por encima del muro corto. Cuando un fragmento cruje bajo tu pie, retrocede.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_desvio_horno` · `wildlife_pool[creature=cascapedernal].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Desvío al horno. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un pequeño caparazón moteado se aparta hacia una junta de roca al cambiar la sombra.

**Propuesto:** Un Cascapedernal cruza la tierra quemada y se refugia bajo un fragmento grande de recipiente. El borde del caparazón asoma por un lado.

**Por qué:** Hoy la misma frase sale en 4 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_desvio_horno` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Desvío al horno. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Más allá del muro corto, lejos del horno, un Quebrarrocas empuja piedras. El temblor llega hasta los fragmentos del suelo.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_meseta_relevo` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Refugio de Lajas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** Junto a la pared baja, un Colagrieta asoma entre las lajas. Mira la mesa de las notas un momento y vuelve a su hueco.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_meseta_relevo` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Refugio de Lajas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Hacia la garganta, lejos del refugio, un Quebrarrocas aparta piedras bajadas de la sierra. Desde la mesa se oye cada golpe.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_senda_viento` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Senda del viento. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** Con el viento llega polvo, y un Colagrieta se pega a la pared más baja: la cabeza dentro de una grieta, la cola fuera.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_senda_viento` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Senda del viento. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Detrás del almacén, un Quebrarrocas empuja un bloque cuesta abajo. El viento se lleva el polvo antes de que llegue a las cubiertas.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_borde_tierra` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Parada de los Cardos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** En la zanja, un Colagrieta busca grieta entre las últimas rocas. Aquí hay más tierra que piedra y le cuesta encontrar dónde meterse.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_borde_tierra` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Parada de los Cardos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Al norte, donde todavía hay bloques grandes, un Quebrarrocas empuja una roca. Desde los pastos de la parada, el ruido llega flojo.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `korven_peldanos_cortos` · `wildlife_pool[creature=colagrieta].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Escalones bajos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una cola desaparece por una grieta. El Colagrieta asoma la cabeza y vuelve a esconderse.

**Propuesto:** Bajo la repisa de las cuñas, un Colagrieta saca la cabeza. Una vecina lo ve, sonríe y aparta el pie.

**Por qué:** Hoy la misma frase sale en 11 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `korven_peldanos_cortos` · `wildlife_pool[creature=quebrarrocas].text`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Escalones bajos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un bloque recién movido corta parte del suelo. El Quebrarrocas sigue empujando piedras a cierta distancia.

**Propuesto:** Lejos de las casas, fuera del camino, un Quebrarrocas mueve piedras en la ladera. Desde los escalones sólo se ve su polvo.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.


## G · Fauna de Lethra

### `lethra_ribera_seca` · `wildlife_pool[creature=pinzajunco].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera seca. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una pinza desigual se levanta al borde del agua. El Pinzajunco arrastra una hoja hacia su agujero cuando los pasos siguen por tierra.

**Propuesto:** En el borde del cauce, un Pinzajunco camina de lado con una hoja seca en la pinza grande. Al llegar a su agujero, la mete dentro.

**Por qué:** Hoy la misma frase sale en 6 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_ribera_seca` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera seca. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** Un Saltalodo hincha la bolsa del cuello entre las hierbas de la orilla. Su llamada suena hondo, como una gota grande al caer.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_ribera_seca` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera seca. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** En la parte ancha del cauce, una espalda rugosa asoma del agua y vuelve a hundirse. Un Dorsalodo descansa en lo hondo; sus ondas llegan hasta la orilla.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.

### `lethra_tierra_esponjosa` · `wildlife_pool[creature=pinzajunco].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Tierra blanda. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una pinza desigual se levanta al borde del agua. El Pinzajunco arrastra una hoja hacia su agujero cuando los pasos siguen por tierra.

**Propuesto:** Junto a las varas del paso estrecho, un Pinzajunco levanta la pinza mayor hacia tus pies. No retrocede: ésa es su orilla.

**Por qué:** Hoy la misma frase sale en 6 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_tierra_esponjosa` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Tierra blanda. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** Sobre el barro, un Saltalodo moteado infla el cuello y llama. Cuando pisas, salta a una mancha de hojas y vuelve a llamar desde allí.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_tierra_esponjosa` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Tierra blanda. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** Más allá, hacia el juncal, la hierba alta queda aplastada en una franja ancha. Un Dorsalodo se arrastra hacia el agua, lento y pesado.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.

### `lethra_tablas_primeras` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Primeras tablas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** Bajo las tablas, un Saltalodo llama entre los apoyos. Su voz suena por todo el tramo de madera.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_tablas_primeras` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Primeras tablas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** En uno de los dos canales, el agua se levanta en una ola sin viento. Un Dorsalodo pasa por debajo, lejos de las tablas.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.

### `lethra_ribera_firme` · `wildlife_pool[creature=pinzajunco].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera de las cargas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una pinza desigual se levanta al borde del agua. El Pinzajunco arrastra una hoja hacia su agujero cuando los pasos siguen por tierra.

**Propuesto:** Bajo un apoyo de madera, un Pinzajunco arrastra una hoja que se cayó de una envoltura. Nadie se la quita.

**Por qué:** Hoy la misma frase sale en 6 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_ribera_firme` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera de las cargas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** Un Saltalodo salta de un recipiente vacío al barro y llama una vez. Una vecina se sobresalta y luego se ríe.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_ribera_firme` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera de las cargas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** Lejos, donde el agua se ensancha, la espalda de un Dorsalodo asoma como una isla de barro. Quienes descargan siguen trabajando de este lado.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.

### `lethra_pasarela_curva` · `wildlife_pool[creature=pinzajunco].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Pasarela curva. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una pinza desigual se levanta al borde del agua. El Pinzajunco arrastra una hoja hacia su agujero cuando los pasos siguen por tierra.

**Propuesto:** Abajo, junto a un poste de la pasarela, un Pinzajunco corta una hoja con la pinza pequeña y sujeta el resto con la grande.

**Por qué:** Hoy la misma frase sale en 6 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_pasarela_curva` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Pasarela curva. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** En el agua quieta, junto a la baranda, un Saltalodo llama. Al oír tus pasos en la madera, salta a una hoja flotante.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_pasarela_curva` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Pasarela curva. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** En medio del agua quieta, una ola ancha avanza hacia la orilla. Un Dorsalodo nada por debajo, sin acercarse a la pasarela.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.

### `lethra_senda_elevada` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Senda sobre el agua. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** Entre dos plataformas, un Saltalodo llama desde una hoja. Desde una ventana, alguien le contesta imitándolo.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_senda_elevada` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Senda sobre el agua. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** Por un canal ancho entre las viviendas pasa despacio una espalda rugosa: un Dorsalodo. Las vecinas suben las cestas a las ventanas mientras pasa.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.

### `lethra_banco_barro` · `wildlife_pool[creature=pinzajunco].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Banco de barro. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una pinza desigual se levanta al borde del agua. El Pinzajunco arrastra una hoja hacia su agujero cuando los pasos siguen por tierra.

**Propuesto:** En el barro firme, un Pinzajunco excava su agujero con la pinza grande. Se para y la apunta hacia ti.

**Por qué:** Hoy la misma frase sale en 6 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_banco_barro` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Banco de barro. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** Un Saltalodo llama desde el borde del canal profundo. Después se queda quieto, mirando las ondas.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_banco_barro` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Banco de barro. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** Las ondas que van contra el viento las mueve un cuerpo grande. En el canal profundo, un Dorsalodo asoma los ojos y un trozo de espalda.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.

### `lethra_ribera_oeste` · `wildlife_pool[creature=pinzajunco].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera hacia Edran. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Una pinza desigual se levanta al borde del agua. El Pinzajunco arrastra una hoja hacia su agujero cuando los pasos siguen por tierra.

**Propuesto:** Un Pinzajunco cruza de lado por el barro, fuera de la cubierta, y arrastra un trozo de envoltura hasta su agujero.

**Por qué:** Hoy la misma frase sale en 6 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_ribera_oeste` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera hacia Edran. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** En el borde del barro, un Saltalodo llama hacia los pastos del oeste. Desde allí no le contesta ninguno.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_hito_tierra` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Cruce del puente. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** Entre las dos piedras del hito, un Saltalodo infla el cuello y llama. Otro le contesta desde el terreno inundable.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_hito_tierra` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Cruce del puente. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** Abajo, en el terreno inundable, la hierba está aplastada en una franja ancha. Un Dorsalodo descansa en el barro, medio hundido.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.

### `lethra_ribera_sombra` · `wildlife_pool[creature=saltalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera sombreada. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Un Saltalodo infla la bolsa del cuello y deja escapar una llamada baja. El salto siguiente rompe el reflejo lejos de la raíz seca.

**Propuesto:** Bajo la pasarela corta, un Saltalodo llama entre dos troncos. Su voz suena distinta debajo de los árboles.

**Por qué:** Hoy la misma frase sale en 10 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `lethra_ribera_sombra` · `wildlife_pool[creature=dorsalodo].text`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Ribera sombreada. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los juncos están aplastados junto al agua. Una espalda ancha se mueve bajo el barro: un Dorsalodo ocupa la orilla.

**Propuesto:** En el canal, a la sombra, una espalda rugosa parece un tronco más. Hasta que se mueve: es un Dorsalodo.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 9 lugares.


## H · Fauna de Nhal

### `nhal_arbol_umbral` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Primer árbol del bosque. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Más adentro, bajo las copas, los pájaros se callan de golpe. Junto a un tronco lejano, algo con piel de corteza levanta la cabeza: un Rasgacorteza.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_suelo_hojas` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Sendero de hojas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Hacia el este, un árbol tiene arañazos muy por encima de la altura de una persona. A su lado, quieto como otro tronco, hay un Rasgacorteza.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_tronco_acostado` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Tronco caído. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Al otro lado del tronco caído, entre los árboles, un Rasgacorteza se rasca contra la corteza. Las ramas altas tiemblan a cada movimiento.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_corteza_clara` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Árbol de corteza clara. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Lejos del árbol claro, entre troncos oscuros, un Rasgacorteza está inmóvil. Se le distingue porque los animales pequeños dan un rodeo para no pasar a su lado.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_corteza_clara` · `wildlife_pool[creature=rondamusgo].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Árbol de corteza clara. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Pelo áspero con musgo adherido queda entre hojas; varias semillas fueron transportadas hasta una raíz.

**Propuesto:** Un Rondamusgo hurga entre las hojas al pie del árbol claro. Al oírte se queda quieto, con una seta en la boca, y corre a una raíz hueca. Desde allí asoma el hocico.

**Por qué:** Hoy la misma frase sale en 5 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `nhal_raices_altas` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Paso de las raíces altas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Entre las raíces altas, lejos del sendero, un Rasgacorteza se separa un poco de su tronco y vuelve a pegarse a él.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_raices_altas` · `wildlife_pool[creature=rondamusgo].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Paso de las raíces altas. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Pelo áspero con musgo adherido queda entre hojas; varias semillas fueron transportadas hasta una raíz.

**Propuesto:** Un Rondamusgo sale de entre dos raíces con semillas pegadas al pelo. Al verte se para en seco y espera, sin moverse.

**Por qué:** Hoy la misma frase sale en 5 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `nhal_piedras_musgo` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Piedras con musgo. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Detrás de las piedras, hacia el puente, se oye romperse una corteza. Un Rasgacorteza deja marcas nuevas en un árbol, muy arriba.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_piedras_musgo` · `wildlife_pool[creature=rondamusgo].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Piedras con musgo. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Pelo áspero con musgo adherido queda entre hojas; varias semillas fueron transportadas hasta una raíz.

**Propuesto:** Sobre una piedra con musgo, un Rondamusgo se confunde con la piedra. Sólo se le nota cuando se rasca y le caen semillas.

**Por qué:** Hoy la misma frase sale en 5 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `nhal_helechos_bajos` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Sendero de helechos. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Entre los helechos altos, lejos de la franja elevada, asoma el lomo de un Rasgacorteza. No se acerca hacia los golpes de madera que llegan de las casas.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_umbral_velmora` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Entrada de Velmora. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Muy al fondo, detrás de las primeras casas, un Rasgacorteza asoma entre los troncos. La luz de las lámparas no llega hasta allí.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_claro_silencio` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Claro tranquilo. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Lejos del claro, donde los árboles se juntan, una forma grande se mueve despacio: un Rasgacorteza. Junto a la raíz sólo se oye caer alguna semilla.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_claro_silencio` · `wildlife_pool[creature=rondamusgo].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Claro tranquilo. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Pelo áspero con musgo adherido queda entre hojas; varias semillas fueron transportadas hasta una raíz.

**Propuesto:** Un Rondamusgo cruza el claro con prisa, se para junto a la raíz donde podrías sentarte y te mira. Después sigue buscando hongos.

**Por qué:** Hoy la misma frase sale en 5 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).

### `nhal_ribera_relevo` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Paso hacia Lethra. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Al otro lado del canal, un Rasgacorteza se apoya en un tronco grueso. Las ramas se doblan sobre el agua con su peso.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_senda_recipiente` · `wildlife_pool[creature=rasgacorteza].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Senda hacia Elin. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Los animales pequeños han dejado de moverse. Junto a un tronco, el Rasgacorteza levanta la cabeza.

**Propuesto:** Lejos de la casa de Elin, más allá de la cesta remendada, los pájaros dejan de cantar. Entre los troncos, un Rasgacorteza levanta la cabeza y vuelve a quedarse quieto.

**Por qué:** Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en 11 lugares.

### `nhal_sendero_altura` · `wildlife_pool[creature=rondamusgo].text`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Subida entre árboles. Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.
- **Requiere código:** no

**Actual:** Pelo áspero con musgo adherido queda entre hojas; varias semillas fueron transportadas hasta una raíz.

**Propuesto:** Un Rondamusgo baja la cuesta entre raíces con la boca llena de semillas. Al verte se mete en el descanso de raíces y espera a que pases.

**Por qué:** Hoy la misma frase sale en 5 lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).


## I1 · Secreto: los Espinajos de Lio (Valdren, cualquier especie)

### `valdren_fragua` · `examine.taza`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Sólo de noche. El texto nocturno de la fragua ya menciona «una taza vacía espera en el banco»: ésa es la pista.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_time": ["noche"], "text": "Por dentro, alguien dibujó con tiza un Espinajo muy redondo, con más espinas que cuerpo. Debajo hay una L."}

**Por qué:** Lio ya existe en el canon (taza pequeña, cuentas de graneros, se entretiene ayudando). Un dibujo suyo repetido es un easter egg que el niño reconoce de un sitio a otro.

### `valdren_fragua` · `actions[id=edran_secreto_lio_fragua]`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Botón visible sólo de noche y sólo hasta encontrarlo.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "edran_secreto_lio_fragua", "label": "Mirar de cerca el dibujo de la taza", "requires_time": ["noche"], "forbids_flags": ["edran_lio_dibujo_fragua"], "set_flags": ["edran_lio_dibujo_fragua"], "scope": "player", "text": "Acercas la taza a la línea roja del carbón. La tiza está más gruesa en las espinas, como si quien dibujaba hubiera tenido mucho tiempo. La L está hecha de un solo trazo.", "journal": "Un Espinajo de tiza dentro de una taza de la fragua de Daro, firmado con una L."}

**Por qué:** Lio ya existe en el canon (taza pequeña, cuentas de graneros, se entretiene ayudando). Un dibujo suyo repetido es un easter egg que el niño reconoce de un sitio a otro.

### `edran_cobertizo_campo` · `examine.banco`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Desde la segunda visita (requires_visits min 2).
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_visits": {"min": 2}, "text": "En la pata del banco hay otro dibujo pequeño: un Espinajo escondido detrás de una estaca pintada. Al lado, otra L."}

**Por qué:** Lio ya existe en el canon (taza pequeña, cuentas de graneros, se entretiene ayudando). Un dibujo suyo repetido es un easter egg que el niño reconoce de un sitio a otro.

### `edran_cobertizo_campo` · `actions[id=edran_secreto_lio_banco]`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** Desde la segunda visita, hasta encontrarlo.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "edran_secreto_lio_banco", "label": "Mirar el dibujo de la pata del banco", "requires_visits": {"min": 2}, "forbids_flags": ["edran_lio_dibujo_banco"], "set_flags": ["edran_lio_dibujo_banco"], "scope": "player", "text": "Te agachas. El Espinajo de la pata asoma por detrás de la estaca, igual que uno de verdad en los tallos. Quien lo hizo esperaba sentado justo aquí.", "journal": "Otro Espinajo con una L, escondido en la pata del banco del cobertizo de las estacas."}

**Por qué:** Lio ya existe en el canon (taza pequeña, cuentas de graneros, se entretiene ayudando). Un dibujo suyo repetido es un easter egg que el niño reconoce de un sitio a otro.

### `valdren_pozo` · `examine.brocal`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** De día (con luz para ver la raya).
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_time": ["día"], "text": "En la piedra del brocal hay un Espinajo rayado con otra piedra, asomado al pozo como si quisiera beber. Éste no se borra con la lluvia. Al lado, una L."}

**Por qué:** Lio ya existe en el canon (taza pequeña, cuentas de graneros, se entretiene ayudando). Un dibujo suyo repetido es un easter egg que el niño reconoce de un sitio a otro.

### `valdren_pozo` · `actions[id=edran_secreto_lio_pozo]`

- **Archivo:** `content/regions/edran.json` → `rooms`
- **Aparece:** De día, hasta encontrarlo.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "edran_secreto_lio_pozo", "label": "Seguir con el dedo el dibujo del brocal", "requires_time": ["día"], "forbids_flags": ["edran_lio_dibujo_pozo"], "set_flags": ["edran_lio_dibujo_pozo"], "scope": "player", "text": "La raya es vieja: el agua del cubo la ha suavizado. Este Espinajo es más pequeño y más torpe que los otros. Quien lo hizo dibujaba Espinajos desde hace mucho.", "journal": "El Espinajo más antiguo de la L está rayado en el brocal del pozo."}

**Por qué:** Lio ya existe en el canon (taza pequeña, cuentas de graneros, se entretiene ayudando). Un dibujo suyo repetido es un easter egg que el niño reconoce de un sitio a otro.

### `edran_elva` · `topics.dibujos`

- **Archivo:** `content/regions/edran.json` → `npcs`
- **Aparece:** Hablar con Elva tras encontrar los tres dibujos.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["edran_lio_dibujo_fragua", "edran_lio_dibujo_banco", "edran_lio_dibujo_pozo"], "text": "¿Has encontrado los Espinajos de Lio? Los dibuja cuando le toca esperar. El del pozo lo hizo de pequeño, el día que no le dejaban sacar agua solo. Si has visto los tres, ya sabes cuánto espera mi Lio. No se lo cuentes a Daro: cree que el de la taza se lo dibujó a él.", "journal": "Elva te contó que los Espinajos con una L son de Lio, que los dibuja cuando espera."}

**Por qué:** Remate: quien firma, por qué, y una broma que invita a hablar con Daro.

### `edran_daro` · `topics.dibujo`

- **Archivo:** `content/regions/edran.json` → `npcs`
- **Aparece:** Hablar con Daro tras ver el dibujo de la taza.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["edran_lio_dibujo_fragua"], "text": "¿El de la taza? No la lavo. Me gusta ese bicho: tiene cara de estar esperando a que alguien le dé trabajo."}

**Por qué:** Pequeña recompensa inmediata por el primer hallazgo, antes de completar los tres.


## I2 · Secreto Felaryn: la repisa de las marcas (Hoshai)

### `hoshai_cuello_roca` · `examine.repisa`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Para cualquier especie: pista.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** Muy arriba, en la pared del paso, hay una repisa estrecha. Desde abajo se ven rayas en la roca. Para llegar haría falta saltar como un Felaryn.

**Por qué:** Sólo un Felaryn puede saltar a la repisa (anatomía canónica: equilibrio y salto). Senku tiene algo propio; los demás reciben la pista y pueden preguntarle.

### `hoshai_cuello_roca` · `actions[id=hoshai_secreto_repisa]`

- **Archivo:** `content/regions/hoshai.json` → `rooms`
- **Aparece:** Sólo personajes Felaryn (requires_species), una vez.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "hoshai_secreto_repisa", "label": "Saltar a la repisa alta", "requires_species": ["felaryn"], "forbids_flags": ["hoshai_marca_repisa"], "set_flags": ["hoshai_marca_repisa"], "scope": "player", "text": "Tomas impulso en la piedra plana y alcanzas la repisa de un salto. Está llena de rayas de altura: cada una tiene al lado un nombre, una cola dibujada o las dos cosas. Son marcas de los niños de Khariel, de muchos años. Con una piedra haces la tuya, un poco más arriba de lo que esperabas.", "journal": "Dejaste tu marca de altura en la repisa alta del paso entre paredes, entre las de los niños de Khariel."}

**Por qué:** Sólo un Felaryn puede saltar a la repisa (anatomía canónica: equilibrio y salto). Senku tiene algo propio; los demás reciben la pista y pueden preguntarle.

### `hoshai_luma` · `topics.repisa`

- **Archivo:** `content/regions/hoshai.json` → `npcs`
- **Aparece:** Hablar con Luma tras dejar la marca.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["hoshai_marca_repisa"], "text": "¿Subiste a la repisa del paso? Mi marca es la tercera por abajo, la de la cola torcida. No la mires mucho: entonces era muy pequeña y muy orgullosa."}

**Por qué:** Luma es Felaryn de Khariel: tiene sentido que su marca esté allí.


## I3 · Secreto Marevyn: la barquita del fondo (Lethra)

### `lethra_orilla_silente` · `examine.fondo`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Sólo Marevyn. La descripción ya dice «no ves el fondo»: ésa es la pista para los demás.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_species": ["marevyn"], "text": "Acercas la cara al agua y tus ojos se acostumbran enseguida. En el fondo, entre el barro, hay una barquita de juguete con la vela rota. En el casco, rayado con cuidado: SOLA."}

**Por qué:** Usa la habilidad acuática Marevyn (mirar bajo el agua, sin respirar en ella) y la historia de las hermanas Mira y Sola. Lo saca un Marevyn y lo ven todos.

### `lethra_orilla_silente` · `actions[id=lethra_secreto_barquita]`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Sólo Marevyn, una vez para todo el mundo (scope world).
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "lethra_secreto_barquita", "label": "Sacar la barquita y dejarla en la raíz", "requires_species": ["marevyn"], "forbids_flags": ["lethra_barquita_rescatada"], "set_flags": ["lethra_barquita_rescatada"], "scope": "world", "text": "Metes el brazo hasta el codo, sin moverte del borde. La barquita sale llena de barro y agua. La vacías y la dejas en la raíz seca, con la vela hacia el sol.", "journal": "Sacaste del canal una barquita de juguete con el nombre de Sola y la dejaste secando en la raíz."}

**Por qué:** Usa la habilidad acuática Marevyn (mirar bajo el agua, sin respirar en ella) y la historia de las hermanas Mira y Sola. Lo saca un Marevyn y lo ven todos.

### `lethra_orilla_silente` · `states[+]`

- **Archivo:** `content/regions/lethra.json` → `rooms`
- **Aparece:** Para todos, después del rescate.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["lethra_barquita_rescatada"], "overrides": {"examine": {"raíces": "En la raíz seca hay una barquita de juguete con la vela rota. Alguien la sacó del canal; en el casco pone SOLA."}}}

**Por qué:** El hallazgo de un hermano cambia el mundo del otro: buen motivo para hablar entre ellos.

### `lethra_sola` · `topics.barquita`

- **Archivo:** `content/regions/lethra.json` → `npcs`
- **Aparece:** Hablar con Sola cuando la barquita está fuera (flag de mundo).
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["lethra_barquita_rescatada"], "text": "¿Mi barquita? ¡La hundió Mira! Teníamos siete y ocho años. Dijo que quería ver si flotaba con piedras dentro. No flotaba."}

**Por qué:** Primera versión de la historia.

### `lethra_mira` · `topics.barquita`

- **Archivo:** `content/regions/lethra.json` → `npcs`
- **Aparece:** Hablar con Mira cuando la barquita está fuera.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["lethra_barquita_rescatada"], "text": "Eso no es verdad. La hundió ella sola y luego me echó la culpa. Pregúntale por qué le rayó su nombre tan grande: era para que nadie más pudiera jugar con ella."}

**Por qué:** Segunda versión, contradictoria a propósito. El niño decide a quién creer; ninguna mecánica depende de ello.


## I4 · Secreto: la figura de corteza viaja (Nhal)

### `nhal_rincon_semillas` · `examine.figura`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Tras nhal_figura_firme y sólo en fase día.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["nhal_figura_firme"], "requires_time": ["día"], "text": "Entre las semillas de verdad hay una figura de corteza con forma de Rondamusgo, con una pata atada con una tira. Alguien le ha puesto tres semillas delante, como si fuera a comer."}

**Por qué:** Tras sostener la figura para Desi (nhal_figura_firme, mundo), el sobrino la lleva de paseo. Un único objeto, en un sitio distinto según la hora, para no estar en tres lugares a la vez.

### `nhal_rincon_semillas` · `actions[id=nhal_figura_vista_semillas]`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Tras nhal_figura_firme, en fase día, una vez.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "nhal_figura_vista_semillas", "label": "Mirar la figura de corteza", "requires_flags": ["nhal_figura_firme"], "requires_time": ["día"], "forbids_flags": ["nhal_figura_vista_semillas"], "set_flags": ["nhal_figura_vista_semillas"], "scope": "player", "text": "Miras la figura sin moverla. Las tres semillas están colocadas en fila. Un poco más allá, entre las raíces, hay pelo áspero de un Rondamusgo de verdad. Parece que la han traído a conocerlo.", "journal": "Viste la figura de corteza del sobrino de Desi: entre las semillas de verdad hay una figura de corteza con f…"}

**Por qué:** Tras sostener la figura para Desi (nhal_figura_firme, mundo), el sobrino la lleva de paseo. Un único objeto, en un sitio distinto según la hora, para no estar en tres lugares a la vez.

### `nhal_claro_silencio` · `examine.figura`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Tras nhal_figura_firme y sólo en fase atardecer.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["nhal_figura_firme"], "requires_time": ["atardecer"], "text": "Sobre la piedra del claro está la figura de corteza, mirando la abertura del cielo. Tiene al lado una hoja doblada, como una manta."}

**Por qué:** Tras sostener la figura para Desi (nhal_figura_firme, mundo), el sobrino la lleva de paseo. Un único objeto, en un sitio distinto según la hora, para no estar en tres lugares a la vez.

### `nhal_claro_silencio` · `actions[id=nhal_figura_vista_silencio]`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Tras nhal_figura_firme, en fase atardecer, una vez.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "nhal_figura_vista_silencio", "label": "Mirar la figura de corteza", "requires_flags": ["nhal_figura_firme"], "requires_time": ["atardecer"], "forbids_flags": ["nhal_figura_vista_silencio"], "set_flags": ["nhal_figura_vista_silencio"], "scope": "player", "text": "La figura mira hacia arriba, donde la luz entra entre las hojas. Alguien la ha dejado aquí para que viera el atardecer. La hoja doblada está bien remetida por debajo.", "journal": "Viste la figura de corteza del sobrino de Desi: sobre la piedra del claro está la figura de corteza, mirando…"}

**Por qué:** Tras sostener la figura para Desi (nhal_figura_firme, mundo), el sobrino la lleva de paseo. Un único objeto, en un sitio distinto según la hora, para no estar en tres lugares a la vez.

### `nhal_patio_relato` · `examine.figura`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Tras nhal_figura_firme y sólo en fase noche.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["nhal_figura_firme"], "requires_time": ["noche"], "text": "Bajo el banco del relato asoma la figura de corteza, de cara a donde Leris lee. Como si escuchara."}

**Por qué:** Tras sostener la figura para Desi (nhal_figura_firme, mundo), el sobrino la lleva de paseo. Un único objeto, en un sitio distinto según la hora, para no estar en tres lugares a la vez.

### `nhal_patio_relato` · `actions[id=nhal_figura_vista_relato]`

- **Archivo:** `content/regions/nhal.json` → `rooms`
- **Aparece:** Tras nhal_figura_firme, en fase noche, una vez.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "nhal_figura_vista_relato", "label": "Mirar la figura de corteza", "requires_flags": ["nhal_figura_firme"], "requires_time": ["noche"], "forbids_flags": ["nhal_figura_vista_relato"], "set_flags": ["nhal_figura_vista_relato"], "scope": "player", "text": "La dejas donde está. Desde aquí la figura oye entero el relato de Leris. Quien la puso eligió el mejor sitio del patio.", "journal": "Viste la figura de corteza del sobrino de Desi: bajo el banco del relato asoma la figura de corteza, de cara…"}

**Por qué:** Tras sostener la figura para Desi (nhal_figura_firme, mundo), el sobrino la lleva de paseo. Un único objeto, en un sitio distinto según la hora, para no estar en tres lugares a la vez.

### `nhal_desi` · `topics.paseo`

- **Archivo:** `content/regions/nhal.json` → `npcs`
- **Aparece:** Hablar con Desi tras ver la figura en los tres sitios.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["nhal_figura_vista_semillas", "nhal_figura_vista_silencio", "nhal_figura_vista_relato"], "text": "¿La has visto en el claro? ¿Y en el rincón de las semillas, y en el patio? Mi sobrino dice que la está llevando a conocer a los Rondamusgos de verdad. Todavía no ha conseguido que ninguno se quede quieto para saludarla."}

**Por qué:** Remate y guiño a la frase inicial de Desi («el de verdad tampoco quiso [quedarse quieto]»).


## I5 · Secreto: piedras para quien levantó el muro (Vaisgard)

### `veyra_patio_senales` · `examine.hueco`

- **Archivo:** `content/regions/veyra.json` → `rooms`
- **Aparece:** Desde la segunda visita. El examen «armazon» ya dice «cabe una mano»: es la pista.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_visits": {"min": 2}, "text": "Metes la mano entre el armazón y la pared antigua. Tocas piedrecitas lisas, muchas, de colores distintos. Alguien las ha ido dejando ahí, una a una."}

**Por qué:** Respeta el canon: nadie sabe quién construyó lo antiguo. El secreto no lo resuelve; muestra una costumbre de la gente de hoy.

### `veyra_patio_senales` · `actions[id=veyra_secreto_piedra]`

- **Archivo:** `content/regions/veyra.json` → `rooms`
- **Aparece:** Desde la segunda visita, una vez por personaje.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "veyra_secreto_piedra", "label": "Dejar una piedrecita en el hueco", "requires_visits": {"min": 2}, "forbids_flags": ["veyra_piedra_hueco"], "set_flags": ["veyra_piedra_hueco"], "scope": "player", "text": "Buscas en el suelo una piedra pequeña y lisa y la dejas con las demás, al fondo del hueco. Al sacar la mano notas que la pared antigua está fría, aunque el patio esté al sol.", "journal": "Dejaste una piedrecita en el hueco de la pared antigua del patio de mensajes."}

**Por qué:** Respeta el canon: nadie sabe quién construyó lo antiguo. El secreto no lo resuelve; muestra una costumbre de la gente de hoy.

### `veyra_arel` · `topics.hueco`

- **Archivo:** `content/regions/veyra.json` → `npcs`
- **Aparece:** Hablar con Arel tras dejar la piedra.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_flags": ["veyra_piedra_hueco"], "text": "¿Tú también has dejado una? Lo hacemos desde pequeños. Nadie sabe quién levantó esa pared. Así que le dejamos algo, para que sepa que seguimos aquí."}

**Por qué:** Emoción sin respuesta inventada.


## I6 · Secreto de regreso: el dibujo que crece (Refugio de Lajas, Korven)

### `korven_meseta_relevo` · `examine.dibujo`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Primeras visitas.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** En el margen de una nota hay un pino dibujado, con la copa doblada por el viento.

**Por qué:** Premia volver: el texto cambia con requires_visits, sin flags. La sala ya cuenta que dos viajeros dibujan «el último pino».

### `korven_meseta_relevo` · `states[+] (visitas ≥ 3)`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Desde la visita 3; colocar después de los anteriores para que gane el último.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_visits": {"min": 3}, "overrides": {"examine": {"dibujo": "El pino del margen tiene ahora piñas. Y raíces, sujetando un poco de tierra. Lo ha dibujado más de una mano."}}}

**Por qué:** Premia volver: el texto cambia con requires_visits, sin flags. La sala ya cuenta que dos viajeros dibujan «el último pino».

### `korven_meseta_relevo` · `states[+] (visitas ≥ 5)`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Desde la visita 5; colocar después de los anteriores para que gane el último.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_visits": {"min": 5}, "overrides": {"examine": {"dibujo": "Alguien ha colgado un Uñapiedra de una rama del pino. Debajo, con otra letra, pone: «¿Quién dibuja esto?»"}}}

**Por qué:** Premia volver: el texto cambia con requires_visits, sin flags. La sala ya cuenta que dos viajeros dibujan «el último pino».

### `korven_meseta_relevo` · `states[+] (visitas ≥ 8)`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Desde la visita 8; colocar después de los anteriores para que gane el último.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"requires_visits": {"min": 8}, "overrides": {"examine": {"dibujo": "Debajo de la pregunta hay respuesta, con una letra nueva: «Todos.» El pino ya casi no cabe en el margen."}}}

**Por qué:** Premia volver: el texto cambia con requires_visits, sin flags. La sala ya cuenta que dos viajeros dibujan «el último pino».

### `korven_meseta_relevo` · `actions[id=korven_secreto_dibujo]`

- **Archivo:** `content/regions/korven.json` → `rooms`
- **Aparece:** Desde la visita 5, una vez por personaje.
- **Requiere código:** no

**Actual:** (nuevo)

**Propuesto:** {"id": "korven_secreto_dibujo", "label": "Añadir algo al dibujo del pino", "requires_visits": {"min": 5}, "forbids_flags": ["korven_dibujo_aportado"], "set_flags": ["korven_dibujo_aportado"], "scope": "player", "text": "Buscas un hueco libre en el margen y dibujas algo pequeño junto al pino. Cuando vuelvas, quizá alguien le haya añadido algo a lo tuyo.", "journal": "Añadiste tu propio dibujo al pino del margen, en el Refugio de Lajas."}

**Por qué:** «Quizá» no promete una mecánica: sólo invita a volver.


## I7 · Para que el niño sepa que hay más (requiere código)

### `journal` · `secretos`

- **Archivo:** `client/app.js + server/engine.py` → `snapshot`
- **Aparece:** Diario: una línea «Secretos encontrados: N» calculada con los flags de los secretos de este bloque. Sin total ni lista, para no estropear la sorpresa.
- **Requiere código:** sí

**Actual:** (nuevo)

**Propuesto:** Secretos encontrados: {n}. El mundo guarda más.

**Por qué:** Un contador es lo que hace que un niño vuelva a mirar de noche, en la lluvia o en la tercera visita. Sin él, los secretos sólo los encuentra quien ya busca. Necesita una lista de flags marcados como secreto y una línea en el snapshot.
