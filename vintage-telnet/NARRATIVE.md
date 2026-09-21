# Vintage Telnet — Narrativa y Aventuras

Este documento coordina la experiencia narrativa jugable de Vintage Telnet. No sustituye el canon del Historiador ni las reglas de `GAMEPLAY.md`.

## Regla de lectura

Antes de diseñar una aventura, consultar `WORLD.md` y las fuentes que éste indique. La narrativa puede presentar VERDAD DEL MUNDO ya establecida, LO QUE CREE UN PERSONAJE, RUMOR o LEYENDA. Solo la primera es canon factual.

Las soluciones, causas reales, ubicaciones ocultas y sorpresas que Javier u otros jugadores no deban conocer se guardan en `NARRATIVE_RESERVED.md` y se mencionan aquí únicamente por identificador y estado.

## Estructura de una aventura

Cada aventura debe registrar, sin necesidad de crear un archivo separado:
- **AVENTURA:** nombre o identificador.
- **Estado:** idea / diseño / lista para implementación / activa / cerrada.
- **Punto de entrada:** qué puede percibir el jugador sin explicación externa.
- **Experiencia buscada:** qué hace y siente el jugador.
- **Pistas y descubrimientos:** información visible sin revelar la solución reservada.
- **Conexión con el mundo:** lugar, ruta, pueblo o hecho canónico utilizado.
- **Consecuencia narrativa persistente:** si existe, qué estado sería importante recordar.
- Dependencias: **NECESIDAD DEL HISTORIADOR**, **NECESIDAD DE NPC**, **NECESIDAD DE JUGABILIDAD** o **NECESIDAD TÉCNICA**.
- **SPOILER / INFORMACIÓN RESERVADA:** referencia al bloque correspondiente de `NARRATIVE_RESERVED.md`.

## Principio para el jugador nuevo

El comienzo no debe explicar el mundo entero. Debe enseñar que el lugar de origen es pequeño, que existen viajeros y noticias de otros sitios, que una ruta conduce hacia Vaisgard y que el mundo conserva huellas anteriores a la memoria de sus habitantes.

La primera experiencia narrativa debe funcionar con cualquiera de los cinco pueblos de inicio y cambiar su ambientación según el origen del personaje. La intención es producir curiosidad antes que exposición.

## Primer arco de descubrimiento — Las señales del camino

**AVENTURA:** VT-NAR-001 — Las señales del camino  
**Estado:** DISEÑO INICIAL  
**Alcance:** primeros descubrimientos de un personaje nuevo.

### Entrada

El jugador comienza en su pueblo y encuentra señales cotidianas de que el asentamiento no está aislado: mercancías, noticias, marcas de viaje o referencias a la ruta que conecta con Vaisgard. No se presenta una misión épica inmediata.

### Experiencia

1. Conocer el pueblo mediante observación y conversaciones breves.
2. Encontrar un **RUMOR** relacionado con algo visto o traído desde el camino.
3. Seguir una pista hasta un punto cercano al asentamiento.
4. Encontrar un **DESCUBRIMIENTO** pequeño que demuestra que la historia local se conecta con una historia más antigua o más amplia.
5. Obtener una razón narrativa para avanzar algún día hacia Vaisgard, sin obligar al jugador a abandonar inmediatamente su región.

### Variantes de ambientación

- **Valdren / Llanos de Edran:** noticias y objetos viajan por el Camino de los Campos.
- **Khariel / Sierra de Hoshai:** una señal puede observarse a distancia desde terrazas o miradores; cualquier ventaja mecánica de visión/salto queda pendiente de Jugabilidad.
- **Brumak / Pedrales de Korven:** marcas de piedra y rutas fragmentadas permiten descubrir que otros viajeros han cruzado el territorio.
- **Narevia / Aguas de Lethra:** los senderos, pasarelas y embarcaderos del Camino de los Juncos traen indicios desde fuera.
- **Velmora / Bosque de Nhal:** señales discretas del Camino de la Sombra Verde pueden pasar inadvertidas para un visitante.

Estas variantes usan geografía ya establecida; no crean cinco campañas separadas. Todas apuntan gradualmente a la misma red regional y a Vaisgard.

### Pistas públicas posibles

**PISTA:** un objeto corriente de otra región que ha pasado por varias manos.  
**RUMOR:** versiones contradictorias sobre algo extraño visto en una ruta.  
**LEYENDA:** una explicación local antigua que no debe tratarse automáticamente como verdad.  
**DESCUBRIMIENTO:** una huella material que conecta el presente del pueblo con una capa histórica anterior.

### Dependencias

**NECESIDAD DE NPC:** roles mínimos para transmitir rumor, memoria local o información de viaje. El Narrador definirá qué deben saber/ocultar; el especialista de NPCs construirá a los personajes.

**NECESIDAD DE JUGABILIDAD:** definir qué acciones de investigar/observar/buscar existen de forma general y cómo se representa el descubrimiento sin convertir una pista narrativa en una regla improvisada.

**NECESIDAD TÉCNICA:** el servidor debería poder recordar descubrimientos narrativos importantes por personaje y, cuando corresponda, cambios persistentes compartidos. Desarrollo debe decidir el modelo técnico.

**SPOILER / INFORMACIÓN RESERVADA:** VT-NAR-001-R. La solución y la conexión canónica concreta no se describen en este archivo.

## Vaisgard como segundo horizonte

Vaisgard debe aparecer primero como destino mencionado y conectado con los cinco caminos, no como una enciclopedia. Al llegar, el jugador puede percibir simultáneamente actividad cotidiana y antigüedad: Plaza de las Cinco Rutas, mercado, capas arquitectónicas y señales del Núcleo Antiguo.

Las entradas selladas y niveles inferiores pueden alimentar aventuras posteriores, pero ninguna explicación sobre su origen debe inventarse fuera del canon del Historiador.

## Trabajo siguiente del Narrador

- Convertir VT-NAR-001 en una cadena concreta cuando existan los roles NPC mínimos y se confirme qué interacción de investigación soportará Jugabilidad.
- Diseñar una primera experiencia de llegada a Vaisgard que conecte las cinco procedencias sin borrar sus diferencias.
- Utilizar secretos existentes solo desde documentación reservada.
- Pedir al Historiador nuevas verdades únicamente cuando una aventura realmente las necesite.

**Responsable:** Narrador de Aventuras — Vintage Telnet  
**Estado:** estructura inicial creada — 2026-09-20.


## Experiencia inicial de fortalecimiento — Salidas al campo

**AVENTURA:** VT-NAR-002 — Primeras salidas  
**Estado:** PROPUESTA NARRATIVA / DEPENDENCIAS ABIERTAS  
**Jugadores iniciales conocidos:** Marcos, Matías y Javier.

### Intención

Los personajes comienzan débiles. Fortalecerse enfrentándose a criaturas débiles forma parte natural de sus primeras salidas fuera del asentamiento, pero el campo no debe sentirse como una habitación donde se repite `matar criatura` hasta alcanzar un número.

Cada salida debe poder producir al menos dos tipos de experiencia: **fortalecimiento** y **descubrimiento**. Un jugador puede regresar porque consiguió progreso, porque encontró algo interesante, porque descubrió una ruta, porque percibió un peligro que todavía no puede afrontar o porque ayudó a otro jugador.

### Ritmo narrativo propuesto

**1. El borde seguro.**  
Al salir del pueblo, el jugador entra en un entorno reconocible y cercano. Puede encontrar criaturas apropiadas para un principiante y aprender que observar el lugar antes de atacar tiene valor.

**2. El campo empieza a hablar.**  
Entre encuentros aparecen pequeñas señales: huellas, restos, sonidos, vegetación alterada, objetos perdidos, rastros de viajeros o cambios en el terreno. No todo hallazgo conduce a una misión ni todo tiene que ser importante.

**3. Elegir hasta dónde seguir.**  
Alejarse debe sentirse como una decisión. Las descripciones pueden advertir gradualmente que el entorno está cambiando o que existen criaturas/amenazas que todavía no conviene enfrentar. El Narrador puede comunicar peligro; la forma mecánica de medirlo corresponde a Jugabilidad.

**4. Regresar también es jugar.**  
Volver al asentamiento no debe sentirse necesariamente como fracaso. El jugador puede regresar con progreso, información, objetos permitidos por Jugabilidad, rumores o conocimiento de un camino que después querrá explorar.

**5. Los tres jugadores pueden contar historias distintas.**  
Marcos, Matías y Javier no tienen que realizar exactamente los mismos encuentros en el mismo orden. El mundo persistente debe permitir que uno encuentre algo y se lo comunique a los demás, que dos jugadores ayuden a un tercero o que descubran juntos que una zona supera todavía sus capacidades.

### Principios narrativos

- Evitar como estructura principal encargos artificiales del tipo “mata 10 criaturas” sin una razón dentro del mundo.
- Las criaturas débiles deben pertenecer al entorno y tener sentido allí; el Historiador decide cuáles son.
- Una criatura débil no tiene que ser únicamente una bolsa de experiencia: su presencia puede revelar algo del terreno, clima, ecosistema o actividad cercana.
- Deben existir señales narrativas antes de ciertos peligros importantes. El jugador puede equivocarse, pero el mundo debe darle información que pueda aprender a leer.
- Encontrar algo que todavía no se puede vencer puede ser un descubrimiento satisfactorio.
- La cooperación debe poder surgir del mundo: avisar de peligro, acompañarse, compartir un hallazgo o ayudar a regresar. Las ventajas mecánicas de grupo pertenecen a Jugabilidad.
- El comienzo no revela los grandes secretos del mundo. Los primeros descubrimientos deben abrir preguntas.

### Relación con VT-NAR-001

VT-NAR-001, **Las señales del camino**, no necesita ocurrir como una misión separada. Sus rumores, pistas y pequeños descubrimientos pueden aparecer durante estas primeras salidas de fortalecimiento. Así, progresión y narrativa comienzan juntas.

### NECESIDAD DEL HISTORIADOR — criaturas iniciales

Para continuar, el Historiador debe definir contenido canónico apropiado para las regiones iniciales:

- criaturas débiles que un personaje principiante pueda encontrar cerca de cada pueblo;
- comportamiento visible y relación de esas criaturas con su entorno;
- rastros/restos/recursos que puedan tener sentido narrativo;
- amenazas claramente superiores que puedan percibirse temprano sin estar destinadas a ser vencidas todavía;
- diferencias regionales suficientes para que salir desde Valdren, Khariel, Brumak, Narevia o Velmora no sea la misma experiencia con nombres cambiados.

El Historiador no necesita fijar estadísticas, XP, daño, respawn ni balance.

### NECESIDAD DE JUGABILIDAD — bucle inicial

Para convertir esta experiencia en algo jugable hace falta definir criterios generales para:

- cómo sabe aproximadamente un principiante si una criatura parece adecuada, peligrosa o muy superior;
- qué obtiene al vencer criaturas comunes y cómo contribuye eso al fortalecimiento;
- qué valor mecánico, si alguno, tiene explorar/descubrir;
- cómo funciona la retirada contra criaturas;
- recuperación/descanso entre encuentros;
- cooperación y reparto de recompensas cuando varios principiantes combaten juntos;
- cómo impedir que la estrategia óptima sea permanecer indefinidamente en un punto matando la misma criatura reaparecida;
- qué consecuencias tiene una derrota durante esta etapa, respetando que no existe muerte permanente.

### NECESIDAD TÉCNICA — más adelante

Cuando Historiador y Jugabilidad resuelvan lo anterior, Desarrollo necesitará poder representar al menos habitaciones/salidas, criaturas, encuentros, descubrimientos y estado persistente. Esta sección describe una necesidad, no una arquitectura técnica obligatoria.

### Criterio narrativo para una primera prueba

Una microzona inicial debería permitir comprobar la experiencia antes de construir regiones enormes: varias habitaciones cercanas al pueblo, más de un tipo de encuentro débil, alguna señal de peligro superior, un descubrimiento que no dependa de matar y una razón natural para regresar.

Las cantidades exactas y la estructura técnica deben decidirlas Jugabilidad/Desarrollo. El objetivo narrativo de la prueba es comprobar si un jugador termina su primera salida pensando **“quiero volver a ver qué hay más adelante”**, no solamente **“necesito repetir esto para subir”.**


## VT-NAR-002A–E — Primeras salidas según la especie

**Decisión de dirección creativa:** el punto de partida no se elige independientemente de la especie. Cada personaje comienza en el pueblo correspondiente a su especie y su primera salida ocurre en esa región.

- **Humano → Valdren → Llanos de Edran.**
- **Felaryn → Khariel → Sierra de Hoshai.**
- **Dravak → Brumak → Pedrales de Korven.**
- **Marevyn → Narevia → Aguas de Lethra.**
- **Vesperi → Velmora → Bosque de Nhal.**

Marcos, Matías y Javier podrán por ello comenzar separados si eligen especies distintas. Sus primeras experiencias no necesitan sincronizarse ni conducirlos inmediatamente al mismo lugar.

### VT-NAR-002A — Humano: salir de Valdren

El primer exterior debe sentirse abierto y cotidiano: parcelas, caminos de tierra, cercas y tránsito rural. El jugador puede detectar señales de **Mordelindes** antes de verlos —tallos roídos, pequeños montículos o huellas— y encontrar también **Espinajos de rastrojo**, cuya postura y púas comunican que no toda criatura reacciona igual al acercamiento.

La salida empieza enseñando a leer un terreno aparentemente sencillo. Más adelante, cercas partidas, huellas profundas o el silencio de la fauna menor pueden anunciar que un **Cornalomo** ha pasado por la zona. El descubrimiento importante para un principiante no es derrotarlo: es comprender que el campo continúa más allá de su capacidad actual.

**Sensación buscada:** “Conozco este paisaje, pero todavía no conozco todo lo que vive en él.”

### VT-NAR-002B — Felaryn: descender desde Khariel

La primera salida aprovecha terrazas, roca, desnivel y líneas de visión. **Uñapiedras** pueden descubrirse por arañazos, mudas o piedras pulidas; los **Saltacrestas** introducen movimiento entre niveles y señales de alarma.

El paisaje permite percibir acontecimientos antes de alcanzarlos. Marcas profundas, restos en lugares elevados o un silencio repentino pueden indicar territorio de un **Rasgacumbres**. La narración debe recompensar observar desde una posición segura antes de avanzar, sin asumir todavía una bonificación mecánica de visión Felaryn.

**Sensación buscada:** “Desde aquí puedo ver lejos; entender lo que estoy viendo es otra cosa.”

### VT-NAR-002C — Dravak: recorrer las grietas de Brumak

La primera salida se construye alrededor de detalles pequeños: hendiduras, piedra cálida, sombras y espacios que un viajero grande podría ignorar. Los **Cascapedernales** dejan raspaduras, mudas y golpeteos; los **Colagrietas** hacen que alimento desaparecido o marcas en el polvo puedan conducir a un encuentro.

El primer aviso de una amenaza superior puede llegar sin que el jugador vea criatura alguna: vibraciones, grietas nuevas y fauna menor abandonando una zona anuncian un posible **Quebrarrocas**.

**Sensación buscada:** “Lo importante no siempre está delante de mí; a veces está debajo o dentro de la piedra.”

### VT-NAR-002D — Marevyn: abandonar las plataformas de Narevia

La primera salida mezcla orillas, barro, raíces, juncos y agua. Los **Pinzajuncos** pueden descubrirse por agujeros y juncos cortados; los **Saltalodos**, por llamadas, salpicaduras y huellas cerca del agua.

La región debe enseñar pronto que una superficie tranquila no equivale a seguridad. Juncos aplastados, ondas grandes o la desaparición repentina de fauna menor pueden anunciar un **Dorsalodo** antes de verlo.

**Sensación buscada:** “El agua muestra señales, pero también esconde cosas.”

### VT-NAR-002E — Vesperi: internarse fuera de Velmora

La primera salida utiliza poca luz, raíces, niebla y señales sutiles. Los **Rondamusgos** pueden confundirse con el entorno hasta moverse; las redes de una **Hilaria de niebla** pueden revelarse por gotas suspendidas o follaje unido de forma extraña.

Aquí el jugador aprende una lección distinta: la ausencia también informa. Un tramo demasiado silencioso, árboles dañados o fauna que cambia sus rutas pueden indicar el territorio de un **Rasgacorteza**.

**Sensación buscada:** “Ver no basta; tengo que notar qué cambió.”

### Estructura compartida sin convertirlas en la misma aventura

Las cinco primeras salidas pueden compartir una estructura técnica sencilla —pueblo → borde conocido → exterior → señal de riesgo → posibilidad de regresar—, pero narrativamente enseñan cinco maneras diferentes de leer el mundo:

- Edran: rastros visibles en un paisaje abierto.
- Hoshai: distancia, altura y señales verticales.
- Korven: vibración, grietas y espacios pequeños.
- Lethra: orillas, sonido y lo oculto bajo el agua.
- Nhal: camuflaje, silencio y cambios sutiles.

No es necesario que los tres jugadores se reúnan durante esta fase. Si eligen especies diferentes, la separación inicial puede hacer valioso el momento futuro en que comparen lo que cada uno conoce o finalmente coincidan en una ruta o en Vaisgard.

### Estado de dependencias

**NECESIDAD DEL HISTORIADOR — RESUELTA PARA PRIMERA VERSIÓN:** CREATURES.md aporta fauna menor, amenazas superiores, comportamiento y señales ambientales para las cinco regiones.

**NECESIDAD DE JUGABILIDAD — ABIERTA:** siguen pendientes las reglas que convierten estos encuentros en progresión: peligro relativo, recompensas, recuperación, retirada, cooperación, reaparición, derrota y medidas contra repetición óptima.

**NECESIDAD DE NPC — NO BLOQUEANTE PARA ESTA PRUEBA:** estas primeras salidas pueden empezar mediante entorno y criaturas. Los NPC serán necesarios cuando se incorporen encargos, rumores personales, comercio o relaciones.

**NECESIDAD TÉCNICA — POSTERIOR:** implementar una microzona por especie solo después de que Jugabilidad haya definido el mínimo mecánico necesario.


## Señales narrativas de peligro para Jugabilidad — VT-NAR-002

Estas señales son información que la narración puede comunicar antes de un encuentro. **No establecen niveles, porcentajes ni fórmulas.** Jugabilidad decidirá si además existe una acción \`evaluar\`, un indicador HTML u otra ayuda.

### Principio común

El jugador principiante no debería necesitar perder un combate para descubrir que una amenaza era claramente superior. El mundo debe ofrecer señales interpretables. Tampoco debe mostrarse automáticamente “enemigo imposible” desde cualquier distancia: primero hay que percibir algo.

La interfaz HTML puede resaltar información que el personaje ya percibió, pero no debe anticipar una criatura oculta, una salida secreta ni la causa real de una señal.

### Valdren / Humano — peligro visible en el campo

Un tramo normal puede mostrar cultivos, actividad de Mordelindes o rastros de Espinajos. Antes de un posible Cornalomo, la descripción puede cambiar: cercas partidas, huellas profundas, árboles jóvenes raspados y ausencia de fauna menor. Si después aparece la criatura, el jugador ya tuvo oportunidad de comprender que algo grande está cerca.

**Lectura que aprende el jugador:** daños grandes y desaparición de fauna pequeña = conviene avanzar con cautela.

### Khariel / Felaryn — peligro observado a distancia

En Hoshai el aviso puede aparecer antes de entrar físicamente al lugar peligroso: restos en altura, marcas profundas, Saltacrestas alarmados o una terraza inesperadamente silenciosa pueden anunciar un Rasgacumbres.

**Lectura que aprende el jugador:** usar la distancia y observar antes de descender puede evitar un encuentro peligroso.

### Brumak / Dravak — peligro sentido en el terreno

En Korven no hace falta ver al Quebrarrocas. Vibraciones, piedras desplazadas, grietas recientes y Cascapedernales abandonando una zona pueden formar una advertencia progresiva.

**Lectura que aprende el jugador:** si el terreno cambia bajo sus pies, seguir adelante puede ser más peligroso que aquello que ve en pantalla.

### Narevia / Marevyn — peligro bajo una superficie tranquila

En Lethra, ondas grandes sin causa visible, juncos aplastados, marcas de arrastre y desaparición de Pinzajuncos o Saltalodos pueden preceder a un Dorsalodo.

**Lectura que aprende el jugador:** antes de cruzar o acercarse al agua, observar la orilla y la superficie importa.

### Velmora / Vesperi — el silencio como advertencia

En Nhal el cambio puede ser una ausencia: dejan de aparecer Rondamusgos, hay redes de Hilarias abandonadas, árboles marcados y un tramo del bosque queda demasiado silencioso antes de un posible Rasgacorteza.

**Lectura que aprende el jugador:** en un entorno normalmente lleno de señales pequeñas, que desaparezcan también comunica información.

### Requisito narrativo para la interfaz híbrida

Si Jugabilidad implementa \`evaluar\` o un botón equivalente, debería **complementar** estas señales y no reemplazarlas. La narración debe seguir teniendo valor.

Ejemplo de flujo deseado:

1. el jugador entra o mira hacia un lugar;
2. el texto presenta únicamente señales perceptibles;
3. el jugador decide observar/evaluar, avanzar, atacar o retirarse según lo que realmente tenga disponible;
4. la interfaz puede organizar la información ya descubierta;
5. ninguna ayuda HTML revela anticipadamente un enemigo oculto, una ruta secreta o la solución de una pista.

**NECESIDAD DE JUGABILIDAD:** decidir qué información adicional proporciona evaluar peligro, cuándo está disponible y cómo distingue una amenaza apropiada de una claramente superior sin convertir el sistema en una predicción perfecta.


## Propuesta para Jugabilidad — encuentro y comunicación entre jugadores

**Dirección aprobada por Javier:** existen dos contextos distintos de comunicación entre jugadores.

### Chat general

El chat general permite que jugadores que no están físicamente juntos hablen y que todos los participantes del canal puedan enterarse de aquello que un jugador decida contar.

Escuchar información por el chat general **no equivale a haberla descubierto personalmente**. Si un jugador publica que encontró una ruina, criatura, entrada o pista, los demás adquieren información social, pero el juego no debería marcar automáticamente el lugar como explorado ni revelar en su mapa aquello que su personaje todavía no ha visitado.

### Encuentro en la misma zona

Cuando dos o más jugadores coinciden en la misma zona, la interfaz puede abrir o habilitar un **menú local de interacción**. Su propósito es hacer evidente que hay otros jugadores presentes y permitir comunicación contextual sin obligar a escribir comandos especiales.

Desde Narrativa, las opciones iniciales útiles son:

- **Hablar:** abrir conversación local con los jugadores presentes.
- **Compartir información:** contar voluntariamente un descubrimiento, pista, rumor o lugar conocido.
- **Ver jugadores presentes:** identificar quién está actualmente en la zona.
- **Cerrar/minimizar conversación:** continuar explorando sin mantener abierto el panel.

Acciones mecánicas como comerciar, formar grupo, ayudar, desafiar o atacar pueden incorporarse al menú si Jugabilidad las aprueba; Narrativa no las establece aquí como reglas.

### Tres estados narrativos de conocimiento

Para preservar el valor de explorar, conviene distinguir conceptualmente:

1. **DESCUBRIMIENTO PERSONAL:** el personaje estuvo allí, examinó o cumplió la condición correspondiente.
2. **INFORMACIÓN COMPARTIDA:** otro jugador le contó voluntariamente algo.
3. **RUMOR:** información escuchada cuya exactitud puede no estar confirmada.

Un jugador puede utilizar información compartida para decidir adónde viajar, pero deberá llegar y descubrir personalmente el lugar para convertirla en descubrimiento propio cuando corresponda.

### Ejemplo

Matías descubre personalmente algo en las Aguas de Lethra y lo cuenta en el chat general. Javier, que comenzó en Hoshai, puede enterarse y decidir viajar en el futuro. El mapa de Javier no debería comportarse como si ya hubiera explorado Lethra.

Si posteriormente ambos coinciden en una zona, el menú local les permite hablar y compartir información directamente. Encontrarse físicamente conserva así un valor social propio aunque exista chat general.

### Protección de secretos

Compartir información debe transmitir **lo que el jugador conoce o decide decir**, no consultar la verdad reservada del mundo para completar su explicación.

La interfaz no debe convertir automáticamente un rumor en verdad, mostrar una solución secreta porque alguien mencionó una pista ni desbloquear una ruta oculta que el receptor todavía no ha descubierto según sus condiciones.

### NECESIDAD DE JUGABILIDAD

Jugabilidad debe decidir:

- funcionamiento y alcance exacto del chat general;
- definición mecánica de “misma zona” para habilitar conversación local;
- qué acciones adicionales aparecen en el menú de jugadores presentes;
- cómo se representa información compartida frente a descubrimiento personal;
- si compartir información puede crear anotaciones, pistas o referencias en el mapa sin marcar el lugar como explorado;
- cómo funcionan bloqueo, silencio, privacidad y otras protecciones de comunicación;
- relación entre conversación local, grupos y PvP.

**Criterio narrativo:** la comunicación debe permitir que los jugadores se enseñen cosas entre ellos sin convertir el conocimiento social en exploración automática.


## Recomendación inicial — compartir conocimiento sin transferencia automática

Para la primera versión jugable, el Narrador recomienda **no crear todavía un sistema formal de transferencia de descubrimientos entre personajes**.

La comunicación puede funcionar de forma natural:

- en el **chat general**, un jugador escribe libremente aquello que quiera contar;
- cuando varios jugadores coinciden físicamente en una misma zona, pueden utilizar el **chat local**;
- un jugador puede describir una ruta, advertir de una criatura, contar dónde vio algo o transmitir una pista utilizando sus propias palabras;
- escuchar esa información no modifica automáticamente el mapa, el registro de exploración ni el estado de descubrimiento del receptor.

Si Matías dice “encontré huellas enormes al norte de Valdren”, Javier puede recordar la información y decidir buscar el lugar. El sistema no necesita convertir esa frase automáticamente en un marcador exacto.

Esto conserva una característica valiosa del mundo: la información procedente de otros jugadores puede ser incompleta, imprecisa, exagerada, equivocada o incluso deliberadamente falsa. El descubrimiento personal sigue siendo diferente de aquello que alguien contó.

### Posible expansión futura

Más adelante, si el juego lo necesita, el Historiador puede proponer contenido que permita transmitir conocimiento de una manera más precisa: mapas físicos, cartas, documentos, habilidades, magia u otros recursos del mundo. Jugabilidad decidiría entonces qué efecto mecánico tiene cada uno.

Estos sistemas **no son necesarios para la primera versión** y no deben bloquear el desarrollo del chat.

### Recomendación para Jugabilidad

Para la primera implementación:

**chat = comunicación entre personas; descubrimiento = acción del personaje en el mundo.**

Mantener ambos conceptos separados hasta que las pruebas con jugadores demuestren que hace falta una mecánica adicional.
