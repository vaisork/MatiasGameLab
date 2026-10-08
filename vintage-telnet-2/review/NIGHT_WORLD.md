# Campaña de exploración, contactos y comercio

Ampliación original basada en pueblos, culturas y rutas del PDF maestro. Brumak sigue siendo un pueblo de roca, no una ciudad subterránea; Valdren sigue abierto y agrícola. Los nuevos interiores son un canal de riego cubierto y un almacén de cargas excavado parcialmente en una ladera. No conectan con pueblos lejanos ni introducen guerras entre especies.

## Dos recorridos integrados

- **Edran:** desde Zanja antigua, la entrada del canal presenta a Nela. Su conversación orienta hacia herramientas y la caja perdida. Oren, en un refugio lateral, localiza la caja y puede recibir una indicación para pedir trabajo. El tramo de la compuerta permite combatir a un salteador o pasar por el borde. Recuperar y devolver la caja concede una provisión una sola vez. Nela recuerda la devolución y puede recibir una cuerda hallada en Veyra para reforzar la escalera.
- **Korven:** desde Peldaños cortos, Ruma ofrece localizar una placa de balanza. El cruce tiene un salteador y un pasillo alternativo. Recuperar la placa y volver a la entrada concede una provisión una sola vez. Ruma recuerda la ayuda y explica para qué sirve la reparación.

Las piezas de encargo no tienen precio de venta. Recolección y entrega quedan protegidas por flags persistentes y consumo de la pieza; conversar no inventa XP ni monedas. Los salteadores son personas concretas que amenazan cargas, no representantes hostiles de una especie; su derrota no entrega partes animales ni entrada al bestiario.

## Servicios cotidianos

Nuevos comerciantes estacionarios en Khariel, Narevia, Velmora y Vaisgard ofrecen provisiones y armas comunes con precios existentes. Cada uno explica compra, equipo posterior y venta de materiales. Los seis hallazgos regionales tienen venta de dos sellos, como extensión económica explícita. Sena acepta materiales en el lugar de cuidados; Ruma los recibe en el almacén. Daro y Beran explican un afinado común limitado a una mejora de un punto por doce sellos y material local; no se presenta como Forja mágica.

Lina y Ved reciben viajeros en los accesos existentes de Valdren y Brumak. Pedir entrada es gratuito, persistente y accesible antes de la condición de paso. La mecánica debe eximir origen y recuperación de cualquier bloqueo; no es un sistema policial ni una muralla nueva.

## Evidencia y límites

`tests/test_night_world.py`: cuatro pruebas pasan: carga del catálogo y rutas de retorno, objetos/recompensas no repetibles, localización única de nuevos contactos y permiso disponible antes del paso. Las pruebas de motor y partidas completas corresponden a la integración coordinada, no se consideran demostradas sólo por estos invariantes.

Dos recorridos, once salas interiores y diez contactos nuevos. Las conversaciones tienen consecuencias pequeñas y visibles; no se afirma disponer de un árbol social completo, movimiento de NPC o IA conversacional libre. El rodeo pacífico es deliberado: combatir es una decisión, no un peaje obligatorio para obtener un objeto.

## Segunda iteración: aventuras cerca del origen

Cuatro encargos locales usan el sistema remunerado existente, con pagos únicos de seis u ocho sellos y registro persistente al cobrarlos:

- **Khariel: polea y cuenta pendiente.** Daren ofrece recuperar una polea del campamento de lona azul, a tres movimientos de la plaza. Seran reclama el pago de un transporte; escucharlo y acordar la devolución permite evitar la pelea. También se puede vencer al salteador local y recuperar la polea: el recuerdo de Daren distingue esa decisión y advierte que la cuenta sigue pendiente. Ambas ramas comparten el bloqueo de recogida para evitar duplicar la pieza.
- **Khariel: recomendación de la cornisa.** Luma paga por inspeccionar el balcón y devolver una recomendación. Se elige entre cargas pequeñas o revisión previa; su memoria conserva la elección. No hay otro objeto perdido ni violencia requerida.
- **Velmora: un recipiente, dos trabajos.** Varo pide hablar con Elin y Desi antes de separar un recipiente de la tabla que sostiene un juguete. La entrega preserva ambos trabajos y crea recuerdos locales.
- **Narevia: dónde poner los cuencos.** Tila paga por revisar costuras, escoger entre esperar al secado o usar cubierta y comunicar el plan a Nima. La elección se conserva en el diálogo de la cocina.

Los destinos de los encargos están a seis movimientos o menos del centro regional. El campamento añade dos salas y un interlocutor; la amenaza humana es accesible, mantiene una salida y no mezcla jefes abrumadores en el mismo sitio. La negociación retira la señal hostil para ese personaje y cambia la escena.

Cinco pruebas de contenido pasan en total, incluyendo distancias reales del grafo, pagos únicos, memoria de pago y alternativas protegidas por el mismo flag de recogida. Un recorrido funcional aislado de la primera iteración ya comprobó búsqueda, venta, compra, combate sin bestiario humano y devolución de caja; la segunda iteración requiere sus recorridos de motor coordinados con playtest.

Corrección de oficio: Taren conserva su alfarería y el puesto de recipientes. Beran, nuevo herrero estacionario del Taller de Brumak, ofrece el afinado y las armas. Se verifica que Taren no tenga servicio de forja y que Beran esté realmente presente en su taller. Siete pruebas de contenido pasan después de aislar la entrega personal de Elin de su antigua marca mundial.

## Tercera iteración: comercio regional y trabajo con consecuencias

La auditoría encontró puestos con listas idénticas, ausencia de encargos remunerados en Vaisgard/Brumak y un oficio mal atribuido ya corregido (Taren alfarera/Beran herrero). Se releyeron las identidades y rutas del canon: los cambios conservan la convivencia entre especies y la función de Vaisgard como centro de las cinco rutas.

Los mercados regionales conservan provisiones, pero ya ofrecen conjuntos diferentes de armas comunes. Khariel prioriza arco y puñal; Narevia, puñal y varita; Velmora, arco y varita; Beran en Brumak, espada y puñal. Vaisgard conserva las cuatro piezas; Daro conserva su catálogo existente. Las conversaciones explican dónde buscar el resto, sin inventar armas no implementadas. `buy_items` limita qué materiales recibe cada puesto según sus usos cotidianos; Vaisgard sigue siendo el comprador amplio.

Tres encargos únicos nuevos pagan cantidades ya anunciadas de seis u ocho sellos:

- **Aviso de Tov:** Arel encarga escuchar la causa de una demora y llevarla a Nera. Se puede registrar el aviso con su procedencia o pedir comprobación. Ambos evitan inventar un robo, y cada decisión queda en memoria local.
- **Toldo de Seli:** examinar una costura y elegir entre sujetar con junco o preparar las perchas sin gastar material. Bela puede prestar un haz una sola vez, como objeto de encargo sin precio de venta; el haz no usado puede devolverse. El material común recogido en Lethra también sirve para reparar.
- **Taza de Taren:** conversación de medidas, examen de la pieza y elección entre base más ligera o más estable. La alfarera recuerda la recomendación, sin atribuir magia ni recompensar un combate.

No se añadieron permisos repetitivos a los demás pueblos: antes de ampliar ese flujo se priorizó que el mundo ofreciera trabajos y comercio distintos. Todos los nuevos flags de progreso son personales y tienen prefijo `encargo_`, separado de las historias públicas existentes. Ocho pruebas de contenido pasan, incluida diversidad de mercados, catálogo de compra válido, protección del préstamo y pagos únicos. La comprobación funcional de estos nuevos recorridos sigue coordinada con playtest.

## Cuarta iteración: amenazas asequibles cerca de cada origen

Distancias mínimas auditadas por BFS sobre las salidas reales, antes del cambio: Valdren 2 movimientos; Khariel 3; Brumak 1; Narevia 4, pero ya en Edran; Velmora 12, hasta el campamento de Hoshai. Sólo se cuentan perfiles de combate no abrumadores, no señales de animales observacionales.

Se añadieron posibilidades humanas de campo en dos salas existentes: Ribera occidental de Narevia (1 movimiento) y Sendero de altura de Velmora (3 movimientos: este, norte, norte). Reutilizan el perfil menor del salteador y el sorteo/caché ya existente, sin añadir estadísticas. Las señales indican arma, terreno y salida de regreso; no obligan a luchar. La fauna observacional permanece, pero los dos pools iniciales dejan de seleccionar un enemigo abrumador en el mismo lugar.

Cada lugar ofrece conocer un borde visible que evita la parada. Es una elección personal persistente, sin pago, objetos ni XP: cambia qué amenaza puedes encontrar y queda recordada por el comerciante local. No expulsa personajes del mundo, no cierra la ruta a otro jugador y no revela un destino oculto. Luchar, retroceder o conocer ese rodeo siguen siendo decisiones diferentes.

Después: Valdren 2, Khariel 3, Brumak 1, Narevia 1, Velmora 3 movimientos hasta una amenaza comparable posible. La palabra posible importa: los nuevos encuentros siguen siendo aleatorios y no se fuerza una aparición en cada visita. Nueve pruebas de contenido pasan, incluida distancia de los cinco orígenes y ausencia de recompensas duplicables en los rodeos.

## Recuperación local: cerrar el circuito de jugar y volver

La auditoría mecánica detectó un único punto de cuidados en Valdren. Se añadieron cinco lugares pequeños, seguros y próximos a las plazas: Khariel junto al mercado, Brumak junto a la calle de casas, Narevia junto al taller de fibras, Velmora junto al mercado y Vaisgard junto al patio del agua. Todos quedan a dos movimientos de su centro. Cada espacio tiene cuidador propio estacionario, disponible de noche, con atención separada de comida, comercio y materiales sucios.

Se mantiene el servicio existente de dieciocho sellos: vitalidad hacia el límite del noventa por ciento, fatiga cero, un grado menos de herida y presupuesto de descanso reiniciado. No se añadieron estadísticas, hechizos ni funciones de cuidados a comerciantes o alfareras. Los diálogos distinguen descansar, provisiones y atención de heridas; comerciantes orientan al lugar cercano.

`recovery_npc` identifica al cuidador presente, manteniendo compatibilidad con el servicio booleano anterior. Once pruebas pasan: los cinco servicios nuevos se ejecutaron mediante el motor con dieciocho sellos, herida moderada y margen de descanso agotado; consumieron el precio, redujeron la herida a leve, retiraron fatiga y reiniciaron el margen. Los lugares de todos los pueblos se comprobaron por conexiones reales, no por coordenadas inventadas.
