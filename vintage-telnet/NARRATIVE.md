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


## Respuesta del Narrador — VT-GAME-001: rasgos de especie perceptibles en aventura

A partir de SPECIES.md y de VT-NAR-002, Narrativa necesita que la especie elegida cambie **cómo se experimenta una situación**, sin determinar la clase ni sustituir los atributos que el jugador decide desarrollar.

### Humanos — generalidad y decisiones del jugador

Narrativamente, el Humano no necesita recibir una percepción extraordinaria. Su experiencia debe servir como referencia general del mundo: observa, se desplaza y manipula el entorno sin una adaptación corporal extrema.

La identidad humana no debería depender de inventar una ventaja espectacular para competir con las demás especies. Si Jugabilidad representa mecánicamente su fisiología generalista, debe hacerlo sin convertirla en superioridad universal.

**Necesidad narrativa:** que la ausencia de especialización racial deje especialmente visible el desarrollo elegido por el propio jugador.

### Felaryn — ver y alcanzar posibilidades

En aventuras con altura o terreno abierto, un Felaryn debería poder percibir detalles lejanos que otros personajes pueden no distinguir todavía. También deben existir situaciones donde su salto, equilibrio o control corporal hagan concebible una ruta o posición diferente.

Esto no significa que toda ruta elevada sea exclusiva ni que la visión revele secretos detrás de obstáculos.

**Necesidad narrativa:** poder presentar información o posibilidades espaciales condicionadas por distancia, altura, equilibrio y capacidad natural de salto.

### Dravak — otra escala del mismo mundo

Un Dravak debe experimentar algunos espacios de manera distinta debido a su tamaño. Una abertura secundaria puede ser una ruta real para él; un mecanismo pequeño puede resultar más accesible; una vibración en piedra puede convertirse en advertencia narrativa.

La diferencia también puede producir obstáculos: altura, alcance o equipo construido para cuerpos mayores.

**Necesidad narrativa:** que tamaño y vibración puedan cambiar rutas perceptibles, acceso físico y señales ambientales sin convertirse en detección mágica.

### Marevyn — el agua como espacio explorable

Un Marevyn debería poder tratar agua, plataformas húmedas, corrientes e inmersiones con mayor naturalidad. En una aventura, una corriente o movimiento del agua puede proporcionarle información que otro personaje no interpreta igual.

No debe significar respiración acuática ni detección perfecta bajo el agua.

**Necesidad narrativa:** que agua, respiración, natación, equilibrio húmedo y corrientes puedan modificar opciones de exploración y percepción.

### Vesperi — información donde otros reciben incertidumbre

En penumbra, un Vesperi debería conservar información visual útil y percibir sonidos o cambios sutiles que otros pueden perder. Esto encaja directamente con Nhal: movimiento, silencio y pequeñas variaciones pueden ser pistas.

No debe equivaler a visión en oscuridad absoluta, ecolocalización ni sigilo automático.

**Necesidad narrativa:** permitir diferencias de información según iluminación, sonido y señales ambientales sutiles.

### Principio transversal para Jugabilidad

Narrativa recomienda distinguir dos tipos de diferencia racial:

1. **Capacidad natural contextual:** cambia qué puede percibir, intentar o recorrer el personaje por su cuerpo/especie.
2. **Desarrollo elegido:** los puntos iniciales y de nivel expresan en qué decide fortalecerse el jugador.

No conviene que los puntos borren completamente las verdades biológicas del canon, ni que la especie predetermine el desarrollo. Un Felaryn sin inversión especializada sigue siendo Felaryn y conserva su naturaleza; un Humano muy desarrollado puede superar a personajes de otras especies en capacidades que las reglas permitan, sin adquirir por ello automáticamente su anatomía o sentidos raciales.

### Aplicación narrativa a grupos mixtos

Las diferencias ganan valor cuando los jugadores cooperan. En una misma expedición, distintos personajes pueden recibir o habilitar información contextual diferente: uno distingue algo lejano, otro nota una vibración, otro interpreta una corriente o percibe mejor en penumbra. Después pueden comunicarlo mediante el sistema de conversación ya propuesto.

Esto crea razones para colaborar sin exigir una composición concreta del grupo.

### Petición concreta a Jugabilidad

Al definir atributos y reparto de puntos, conservar espacio mecánico para que:
- los rasgos naturales anteriores sigan siendo perceptibles aunque no todos sean atributos;
- invertir puntos pueda mejorar capacidades sin convertir automáticamente al personaje en otra especie;
- ninguna especie quede obligada a una clase;
- percepción contextual pueda cambiar la información presentada por la narración/interfaz;
- rutas contextuales puedan depender de condiciones corporales cuando el contenido lo requiera;
- un grupo mixto pueda beneficiarse de perspectivas diferentes sin necesitar todas las especies para completar aventuras normales.

**Estado Narrador VT-GAME-001: ENTREGADO.**


## Handoff explícito Narrador ↔ Jugabilidad — estado 2026-09-21

Este bloque elimina una ambigüedad de coordinación detectada entre Narrador y Diseñador de Jugabilidad.

### Lo que el Narrador ya entregó a Jugabilidad

- **VT-GAME-001:** aportación narrativa sobre diferencias de especies — ENTREGADA.
- Cinco variantes regionales de **VT-NAR-002** según especie/pueblo inicial — ENTREGADAS.
- Señales narrativas regionales para comunicar peligro — ENTREGADAS.
- Recomendación sobre acción/función de evaluar peligro — ENTREGADA como necesidad narrativa, pendiente de criterio mecánico.
- Propuesta de chat general + conversación local al coincidir jugadores — ENTREGADA.
- Criterio inicial de conocimiento: el chat comunica información, pero no transfiere automáticamente descubrimientos ni mapa — ENTREGADO.

### Lo que el Narrador espera ahora de Jugabilidad

Estas decisiones siguen abiertas en GAMEPLAY.md o son necesarias para convertir VT-NAR-001/002 en contenido listo para implementación:

1. **Progresión temprana:** cómo contribuyen los encuentros comunes al fortalecimiento y qué recompensas/progreso puede esperar un principiante.
2. **Peligro / evaluar:** qué información mecánica recibe el jugador para distinguir una criatura apropiada, peligrosa o claramente superior, y si existe botón/comando Evaluar.
3. **Retirada:** criterio general de huida contra criaturas durante las primeras salidas.
4. **Recuperación:** cómo recupera un principiante recursos/estado entre encuentros y qué papel tiene volver al pueblo.
5. **Derrota temprana:** consecuencias mecánicas de ser derrotado por fauna común, respetando ausencia de muerte permanente y ausencia de pérdida de arma frente a monstruos comunes.
6. **Cooperación:** criterio básico para combatir juntos y tratamiento general de recompensas/progreso compartido.
7. **Antifarmeo / reaparición:** criterio suficiente para que la estrategia óptima no sea permanecer indefinidamente matando la misma criatura común.
8. **Descubrimiento e investigación:** qué acciones generales existen para observar/investigar/buscar y qué estado mecánico, si alguno, registra un descubrimiento personal.
9. **Chat:** cerrar el criterio mínimo de chat general y chat local ya propuesto por Javier/Narrador; los detalles técnicos pueden quedar para Arquitectura/Desarrollo.
10. **Atributos:** después de VT-GAME-001, definir con Javier la lista de atributos y la distribución de puntos iniciales/de nivel, preservando los rasgos naturales de especie.

### Lo que NO estoy esperando de Jugabilidad

Narrativa no necesita que Jugabilidad invente criaturas, historias, pistas, NPCs, secretos, nombres, regiones ni escenas. Tampoco necesita fórmulas finales de balance para empezar a redactar contenido; necesita criterios generales suficientes para no contradecir las reglas.

### Trabajo que debe el Narrador después del handoff

Cuando Jugabilidad cierre un mínimo suficiente de los puntos anteriores, el Narrador debe:

- convertir las cinco variantes de VT-NAR-002 en secuencias concretas de primera salida;
- concretar VT-NAR-001 donde las acciones de observación/investigación ya estén claras;
- escribir textos, pistas, señales de peligro, decisiones y retornos correspondientes;
- indicar a Desarrollo qué contenido narrativo queda listo para implementar, sin diseñar su arquitectura.

### Estado de coordinación

**VT-GAME-001 no está pendiente del Narrador.** Esa entrega está cerrada.

**Sí existe una dependencia activa Narrador ← Jugabilidad** para pasar de diseño narrativo a aventuras iniciales listas para implementación.

El Narrador puede seguir escribiendo ambientación mientras tanto, pero no debe convertir las decisiones mecánicas anteriores en reglas por su cuenta.

**Próximo responsable:** Diseñador de Jugabilidad, para responder/cerrar los criterios anteriores en GAMEPLAY.md. Después vuelve el turno al Narrador.


## Respuesta del Narrador — VT-GAME-002: los ocho atributos en un RPG de lectura

### Criterio narrativo central

Los ocho atributos propuestos **pueden funcionar en Vintage Telnet**, pero solo si se diseñan como modificadores de la experiencia textual y no como una simulación invisible de animaciones propias de un videojuego gráfico.

Un atributo merece existir si puede cambiar de manera comprensible al menos una de estas cosas:

1. **lo que el personaje percibe o comprende en el texto;**
2. **las acciones/opciones que puede intentar;**
3. **la manera en que el texto describe el resultado de una acción;**
4. **las consecuencias que produce esa acción.**

El jugador no necesita reflejos físicos para que su personaje sea ágil ni habilidad manual real para que sea diestro. El jugador toma decisiones; el personaje ejecuta de acuerdo con sus capacidades.

La narración debe evitar resolver automáticamente la aventura porque un número sea alto. Los atributos deben aportar posibilidades e información, no reemplazar la lectura, la deducción ni la elección.

### 1. Fuerza

**Sí funciona claramente en texto.**

Puede manifestarse mediante acciones como levantar, empujar, arrastrar, sujetar, forzar, romper o mover objetos; también puede influir narrativamente en golpes físicos cuando Jugabilidad lo considere.

Ejemplo de diferencia textual: ante una puerta deformada, todos pueden verla; un personaje suficientemente fuerte puede tener una opción viable de forzarla. Otro puede buscar una llave, mecanismo, ruta alternativa o ayuda.

**Cuidado:** Fuerza no debe convertirse en “abre todos los obstáculos”. Una puerta puede requerir conocimiento, herramienta, llave o condición narrativa aunque el personaje sea muy fuerte.

### 2. Resistencia

**Funciona, pero corre riesgo de sentirse invisible si solo significa más vida.**

Narrativamente puede expresarse mediante cuánto esfuerzo físico puede sostener el personaje, exposición a condiciones adversas, marchas, fatiga y capacidad de continuar después de situaciones físicamente exigentes.

El texto puede comunicar estados: respiración pesada, agotamiento, recuperación, dificultad creciente para continuar.

**Recomendación:** si Resistencia termina reducida únicamente a una cifra de vida/HP, aporta poco a la experiencia de lectura. Debe tener consecuencias legibles fuera del daño directo para justificar su identidad separada.

### 3. Agilidad

**Puede funcionar, pero debe traducirse de “movimiento visual” a decisiones y resultados textuales.**

No necesitamos que el jugador esquive físicamente. Ante una criatura que embiste, una cornisa inestable o un terreno peligroso, el jugador decide qué intentar y Agilidad influye en cómo lo ejecuta el personaje.

Puede afectar esquiva, reacción corporal, equilibrio dinámico, atravesar rápidamente un peligro o reposicionarse durante combate.

**Solapamiento a vigilar:** equilibrio ya forma parte natural de algunos rasgos de especie y también aparece en la definición provisional de Agilidad. Jugabilidad debe distinguir entre capacidad racial contextual y desarrollo general del atributo.

### 4. Percepción

**Es uno de los atributos más naturalmente compatibles con un juego de lectura.**

Puede cambiar directamente la descripción recibida. Dos jugadores en el mismo lugar no tienen por qué leer exactamente la misma cantidad de información.

Una descripción base puede decir que el camino está tranquilo. Un personaje que percibe mejor puede recibir además una anomalía: huellas, silencio extraño, vegetación movida, olor, sonido o detalle material.

Esto encaja especialmente bien con las señales de peligro de VT-NAR-002.

**Regla narrativa importante:** Percepción entrega señales, no conclusiones. Notar una marca no significa comprender quién la hizo ni qué significa.

### 5. Intelecto

**También funciona muy bien en texto si se usa para comprender y relacionar información, no para pensar en lugar del jugador.**

Puede ayudar con escritura, símbolos, mecanismos conceptuales, conocimiento estudiado, comparación de evidencias y comprensión de ciertos indicios.

Pero el juego no debe responder automáticamente un misterio porque Intelecto sea alto.

Una buena separación sería:
- Percepción: “ves tres marcas paralelas bajo el polvo”.
- Intelecto/conocimiento aplicable: “reconoces que no parecen desgaste normal”.
- Jugador: decide qué cree, qué investiga y qué hace después.

**Riesgo:** convertir Intelecto en botón “resolver acertijo”. Eso dañaría el núcleo de lectura y descubrimiento.

### 6. Voluntad

**Puede funcionar, aunque necesita situaciones narrativas reales para no convertirse en una estadística abstracta.**

Puede manifestarse ante miedo, coerción, dolor, presión sobrenatural, concentración o mantenimiento de determinadas acciones/poderes cuando el contenido del mundo lo justifique.

El texto puede mostrar que el personaje siente la presión aunque consiga resistirla. Resistir no debe borrar la escena.

**Riesgo:** si casi ninguna aventura contiene presión mental, miedo, concentración o efectos equivalentes, Voluntad se vuelve un atributo que el jugador apenas percibe. Jugabilidad e Historiador deben confirmar que tendrá suficiente uso real.

### 7. Destreza

**Funciona en texto siempre que signifique ejecución precisa y no reflejos del jugador.**

Puede afectar manipulación fina, mecanismos, herramientas, reparación/fabricación y uso preciso de determinadas armas o acciones.

El jugador puede decidir “intento liberar el mecanismo sin romperlo”; Destreza ayuda a determinar cómo lo ejecuta el personaje.

**Solapamiento a vigilar:** debe mantenerse claramente separada de Agilidad. Narrativamente propongo:
- Agilidad = control del cuerpo en movimiento.
- Destreza = control preciso de manos/herramientas/ejecución fina.

También debe respetar rasgos como la escala y manos Dravak: un atributo alto no cambia la anatomía del personaje.

### 8. Presencia

**Puede enriquecer mucho un juego textual, pero es el atributo que exige más cuidado narrativo.**

Vintage Telnet contiene conversación real entre jugadores y tendrá NPCs. Presencia nunca debe decidir si el jugador “puede hablar”.

Puede influir en cómo NPCs reciben un intento de persuadir, intimidar, negociar, liderar o causar una impresión concreta, siempre considerando contexto, relación, reputación y lo que se dijo/hizo.

**Regla narrativa importante:** Presencia no debe reemplazar el contenido de una conversación. Un jugador no debería poder escribir cualquier absurdo y obtener éxito automático porque su puntuación sea alta.

Tampoco debe aplicarse mecánicamente de la misma forma a conversación entre jugadores humanos: los jugadores reales deciden qué creen y cómo reaccionan.

### Solapamientos que deben resolverse antes de las fórmulas

Los ocho son narrativamente defendibles, pero hay cuatro fronteras especialmente importantes:

- **Fuerza / Resistencia:** producir fuerza vs sostener esfuerzo/soportar desgaste.
- **Agilidad / Destreza:** control corporal en movimiento vs precisión de ejecución fina.
- **Percepción / Intelecto:** encontrar/notar información vs interpretarla/comprenderla.
- **Intelecto / Voluntad:** comprender/aprender vs mantener control mental/concentración.

Si estas fronteras no aparecen en acciones textuales reales, entonces tener ocho atributos solo añade números.

### Cómo debería sentirse una comprobación sin convertir el juego en tiradas opacas

El texto debe explicar causalmente lo ocurrido siempre que sea razonable.

Mala experiencia:
> Fallaste. Requisito insuficiente.

Mejor experiencia:
> Empujas la losa, pero apenas consigues separarla del suelo. Es demasiado pesada para moverla así tú solo.

El jugador entiende el problema y puede decidir: fortalecerse, buscar ayuda, usar una herramienta o encontrar otra ruta.

No recomiendo que el jugador vea continuamente tiradas internas para cada frase. Los números pueden existir en el sistema, pero la experiencia principal debe comunicar **situación y consecuencia**.

### Los atributos no deben fabricar secretos

Un valor alto no debe hacer aparecer información que no existe en el contenido.

Narrativa debe preparar capas reales de información y opciones. El sistema decide cuáles son perceptibles o viables según personaje, especie, estado y contexto.

Esto permite que los atributos sean importantes sin generar texto arbitrario ni revelar automáticamente soluciones reservadas.

### Relación con rasgos de especie

La revisión de VT-GAME-001 se mantiene: especie y atributo son capas diferentes.

Ejemplos:
- Percepción alta no concede visión Felaryn ni visión Vesperi en baja luz.
- Agilidad alta no convierte a un Humano en un Felaryn ni reproduce automáticamente su salto natural.
- Destreza alta no reduce el tamaño corporal para acceder a un paso Dravak.
- Resistencia alta no concede adaptación Marevyn al agua.

Los atributos pueden mejorar capacidades generales; los rasgos de especie determinan posibilidades corporales/sensoriales propias cuando el canon las establece.

### Conclusión del Narrador

**No recomiendo eliminar ninguno de los ocho todavía.** Los ocho pueden traducirse a una experiencia textual real.

Pero antes de aprobar la matriz definitiva, Jugabilidad debería construir para cada atributo una pequeña lista de **acciones textuales concretas del juego**. Si dos atributos terminan resolviendo casi siempre las mismas acciones, deben revisarse o fusionarse antes de diseñar la matemática 1–100.

La prueba correcta no es “¿este atributo existe en otros RPG?”, sino:

> **¿Qué leerá, podrá intentar o experimentará de manera diferente un jugador de Vintage Telnet por haber desarrollado este atributo?**

Si no podemos responder eso con ejemplos de juego, ese atributo todavía no está listo.

**Estado Narrador VT-GAME-002: ENTREGADO.**


## Prueba textual de atributos — VT-GAME-002A

**Objetivo:** comprobar que los ocho atributos producen diferencias que el jugador pueda leer, decidir y experimentar en Vintage Telnet.

Los comandos siguientes son **propuestas narrativas de prueba**, no vocabulario mecánico aprobado. Jugabilidad debe decidir qué acciones serán comandos, botones o acciones contextuales.

### Fuerza — cambiar físicamente el entorno

**Situación base:**
> Una carreta volcada bloquea casi todo el sendero. Una de sus ruedas está hundida en el barro.

**Acción propuesta:** \`empujar carreta\`

**Respuesta cuando la capacidad no basta:**
> Apoyas el hombro contra la madera y empujas. La carreta cruje, pero la rueda hundida apenas se mueve. Solo no parece suficiente.

**Respuesta cuando la capacidad sí basta:**
> Clavas los pies en el suelo y empujas. La rueda sale del barro con un golpe húmedo y la carreta se desplaza lo suficiente para dejar libre el sendero.

**Decisión que permanece en manos del jugador:** intentar con ayuda, buscar una palanca, rodear el obstáculo o volver después.

**Prueba superada:** Fuerza cambia una posibilidad física y su consecuencia es perfectamente narrable.

---

### Resistencia — sostener esfuerzo y soportar desgaste

**Situación base:**
> El ascenso continúa bajo una lluvia fría. El refugio que viste desde abajo todavía queda lejos.

**Acción propuesta:** \`continuar\`

**Respuesta con poca capacidad restante:**
> Sigues subiendo, pero las piernas empiezan a pesarte y el frío se mete bajo la ropa. Podrías continuar, aunque hacerlo así tendrá un costo físico cada vez mayor.

**Respuesta con buena capacidad para sostener el esfuerzo:**
> Mantienes un paso constante pese a la pendiente y la lluvia. Respiras con fuerza, pero todavía puedes continuar sin que el cansancio domine tus movimientos.

**Decisión que permanece en manos del jugador:** continuar, descansar, regresar o buscar otro refugio.

**Prueba superada con condición:** funciona si Resistencia afecta esfuerzo, fatiga y condiciones; si solo aumenta una barra de vida, narrativamente pierde gran parte de su identidad.

---

### Agilidad — ejecutar movimiento corporal bajo presión

**Situación base:**
> El Espinajo baja la cabeza y carga por el sendero estrecho. A tu derecha hay una zanja; a la izquierda, una cerca baja.

**Acciones propuestas:** \`esquivar\`, \`saltar cerca\`, \`retroceder\`

**Respuesta ante una ejecución corporal insuficiente:**
> Intentas apartarte en el último instante, pero tu pie resbala en la tierra suelta. Evitas el golpe de lleno, aunque el animal alcanza a rozarte al pasar.

**Respuesta ante una buena ejecución corporal:**
> Esperas hasta que la carga está cerca y te apartas con un movimiento rápido. El Espinajo pasa junto a ti y necesita espacio para girar.

**Decisión que permanece en manos del jugador:** qué maniobra intentar y cuándo abandonar el enfrentamiento.

**Prueba superada:** el jugador decide; Agilidad representa la capacidad del personaje para ejecutar el movimiento, no los reflejos físicos de quien sostiene el teléfono.

---

### Percepción — recibir señales adicionales, no soluciones

**Situación base para todos:**
> El camino atraviesa un campo aparentemente tranquilo. Más adelante se levanta una cerca de madera.

**Acción propuesta:** \`mirar\` o \`observar camino\`

**Descripción base:**
> La hierba se mueve con el viento. No ves animales cerca.

**Información adicional cuando Percepción/contexto lo permite:**
> Junto a la cerca distingues dos postes quebrados hacia afuera. En el barro hay marcas profundas y demasiado anchas para las criaturas pequeñas que has visto cerca del pueblo.

**Lo que NO debe decir automáticamente:**
> Hay un Cornalomo peligroso adelante. No avances.

El jugador debe interpretar las señales o buscar más información.

**Prueba superada con especial fuerza:** Percepción puede modificar directamente el texto sin convertirlo en una respuesta automática.

---

### Intelecto — comprender información sin resolver la decisión

**Situación base:**
El jugador ya encontró las marcas junto a la cerca.

**Acción propuesta:** \`examinar marcas\`

**Respuesta sin conocimiento/comprensión suficiente:**
> Las marcas son profundas y están separadas de forma irregular. Algo pesado pasó por aquí, pero no sabes determinar mucho más.

**Respuesta cuando la capacidad y el conocimiento contextual permiten interpretar más:**
> La profundidad no parece causada únicamente por peso: varias marcas están concentradas frente a los postes rotos. Lo que pasó por aquí probablemente empujó o golpeó la cerca antes de cruzarla.

**Lo que NO debe resolver:**
> Fue un Cornalomo y está exactamente dos habitaciones al norte.

**Decisión que permanece en manos del jugador:** relacionar esta información con rumores, criaturas conocidas, rutas y riesgos.

**Prueba superada:** Intelecto enriquece la interpretación; no juega el misterio por el jugador.

---

### Voluntad — mantener una decisión bajo presión mental

**Situación base:**
> Desde la galería oscura llega un sonido grave y repetitivo. Cada golpe parece acercarse. Una sensación de alarma difícil de explicar te empuja a abandonar el lugar.

**Acciones propuestas:** \`mantener posición\`, \`concentrarse\`, \`retirarse\`

**Respuesta cuando la presión supera al personaje:**
> Intentas permanecer inmóvil, pero la tensión rompe tu concentración. Das varios pasos hacia la salida antes de conseguir detenerte.

**Respuesta cuando logra sostenerse:**
> El miedo no desaparece. Aun así, controlas la respiración y consigues mantenerte donde estás el tiempo suficiente para decidir tu siguiente acción.

**Decisión que permanece en manos del jugador:** avanzar, observar, utilizar una capacidad o retirarse.

**Prueba superada con condición:** Voluntad funciona si el mundo contiene presión mental, miedo, concentración u otras situaciones reales que la utilicen. No debe significar simplemente “ignoras la narración de miedo”.

---

### Destreza — ejecutar una acción fina con precisión

**Situación base:**
> Una pequeña caja de viaje tiene el cierre doblado. Entre la tapa y el marco apenas cabe la punta de una herramienta.

**Acciones propuestas:** \`examinar cierre\`, \`manipular cierre\`, \`forzar caja\`

**Respuesta ante poca precisión:**
> Introduces la herramienta en el hueco, pero el cierre se mueve junto con toda la tapa. Si sigues haciendo fuerza de esta manera podrías dañar el mecanismo o lo que haya dentro.

**Respuesta ante buena precisión:**
> Mantienes la herramienta firme y haces presión justo bajo la pieza torcida. El cierre cede un poco sin deformarse más.

**Decisión que permanece en manos del jugador:** continuar cuidadosamente, usar fuerza, buscar otra herramienta o dejarlo.

**Prueba superada:** Destreza se siente distinta de Agilidad porque trabaja sobre precisión manual, herramienta y ejecución fina, no sobre desplazamiento corporal.

---

### Presencia — modificar la recepción social, no escribir la conversación por el jugador

**Situación base:**
> Un carretero enfadado bloquea el paso. “Nadie cruza hasta que encuentre lo que me robaron.”

El jugador puede escribir o seleccionar una intención de diálogo.

**Acciones posibles:** \`hablar carretero\`, \`persuadir carretero\`, \`intimidar carretero\` — nombres provisionales.

**Ejemplo de intención del jugador:**
> “Déjame pasar. Puedo buscar tu carga desde el otro lado y volver si encuentro alguna pista.”

**Respuesta cuando el intento causa poca impresión:**
> El carretero te mira con desconfianza. “Eso podría decirlo cualquiera. Si quieres ayudar, demuéstrame primero que no vienes con los ladrones.”

**Respuesta cuando contexto y Presencia favorecen el intento:**
> El carretero te observa unos segundos y finalmente se aparta. “Está bien. Si de verdad vas a buscarla, fíjate en las marcas de pintura azul de las cajas.”

En ambos casos la conversación continúa; un resultado desfavorable puede abrir otra vía en lugar de cerrar el juego.

**Reglas narrativas:**
- Presencia no bloquea la conversación normal.
- No convierte una mentira absurda en verdad.
- NPCs conservan conocimientos, intereses y límites.
- Contra otros jugadores humanos, Presencia no obliga a creer, obedecer ni aceptar una negociación.

**Prueba superada:** es especialmente apropiada para un RPG textual si afecta reacción y oportunidad sin sustituir lo que el jugador comunica.

---

## Prueba combinada — una misma escena, varios atributos

La utilidad real de los ocho aparece mejor cuando **una escena admite enfoques diferentes**.

> Al norte del camino hay una caseta abandonada. La puerta está trabada. Cerca de la pared encuentras barro removido y dentro se escucha un golpeteo débil.

Posibles aproximaciones:

- **Fuerza:** intentar forzar la puerta.
- **Resistencia:** llegar o continuar actuando tras una marcha/exposición que haya producido desgaste.
- **Agilidad:** alcanzar una abertura alta o atravesar con seguridad una zona físicamente inestable, si el espacio lo permite.
- **Percepción:** notar huellas, sonidos o detalles que no aparecen en la descripción básica.
- **Intelecto:** interpretar las señales o comprender cómo funciona un cierre/mecanismo conocido.
- **Voluntad:** mantener concentración o decisión si existe una presión mental real en la escena.
- **Destreza:** manipular cuidadosamente el cierre.
- **Presencia:** obtener información o cooperación de una persona relacionada con el lugar, si existe.

**Importante:** no es necesario ni recomendable que toda escena utilice los ocho. El contenido debe usar solamente los atributos que tengan sentido.

## Recomendación de interfaz narrativa

No recomiendo ocho botones permanentes llamados Fuerza, Resistencia, Agilidad, etc.

El jugador debe pensar en **acciones del mundo**, no en “usar una estadística”:

- mirar;
- examinar;
- empujar;
- saltar;
- manipular;
- hablar;
- continuar;
- retirarse.

El sistema puede consultar internamente los atributos pertinentes. La narración devuelve el resultado en lenguaje del mundo.

Esto mantiene el espíritu Telnet: **el jugador ordena una acción; el personaje la ejecuta según quién es y cómo se ha desarrollado.**

## Criterio de aceptación propuesto para Jugabilidad

Antes de fijar la matemática 1–100, cada atributo debería superar tres preguntas:

1. ¿Podemos escribir al menos varias acciones/situaciones frecuentes donde importe?
2. ¿El jugador puede entender por el texto por qué esa capacidad fue relevante?
3. ¿Produce una experiencia suficientemente distinta de los otros siete?

Si un atributo falla estas pruebas, debe revisarse antes de asignarle puntos, costes o curvas.

**Estado VT-GAME-002A: PRUEBA NARRATIVA ENTREGADA A JUGABILIDAD.**


## NECESIDAD DE NPC — VT-NPC-001: población mínima para primera prueba jugable

**Solicitante:** Narrador de Aventuras — Vintage Telnet  
**Prioridad:** ALTA — necesaria para convertir las primeras salidas en una experiencia jugable completa.  
**Estado:** SOLICITADO AL RESPONSABLE DE NPCs / HISTORIADOR SEGÚN ORGANIZACIÓN VIGENTE.

### Objetivo

Crear la población NPC mínima necesaria para probar las cinco experiencias iniciales sin intentar poblar todavía todo Vintage Telnet.

La primera versión debe favorecer **pocos NPCs memorables y funcionales** antes que una gran cantidad de personajes superficiales.

### Alcance inicial recomendado

Preparar aproximadamente **3–4 NPCs relevantes por pueblo inicial**:

- Valdren — Humanos / Llanos de Edran
- Khariel — Felaryn / Sierra de Hoshai
- Brumak — Dravak / Pedrales de Korven
- Narevia — Marevyn / Aguas de Lethra
- Velmora — Vesperi / Bosque de Nhal

Objetivo aproximado total: **15–20 NPCs iniciales**. No es una cuota obligatoria; si una función puede resolverse naturalmente con menos personajes, evitar crear NPCs innecesarios.

### Funciones narrativas que necesitamos cubrir

En cada pueblo, el conjunto de NPCs debería permitir cubrir estas necesidades:

1. **Vínculo con el hogar.**  
   Alguien que haga sentir que el personaje pertenece a un lugar real y que permita introducir de forma natural aspectos cotidianos del asentamiento.

2. **Vínculo con el exterior.**  
   Alguien cuya actividad, conocimiento o posición permita hablar naturalmente del campo, caminos, alrededores o peligros próximos sin convertirse en un tutorial ambulante.

3. **Información, rumor o memoria local.**  
   Alguien que pueda transmitir información incompleta, rumores, observaciones o recuerdos. Lo que diga un NPC no debe convertirse automáticamente en verdad canónica si habla desde conocimiento limitado.

4. **Razón para regresar.**  
   Uno de los anteriores —o un NPC adicional cuando tenga sentido— debe permitir que volver al pueblo después de explorar tenga valor narrativo: conversación nueva, reacción a un hallazgo, información contextual u otra consecuencia coherente.

### Necesidades para la primera prueba

Los NPCs deben poder sostener interacciones textuales sencillas como:

- hablar;
- preguntar por el pueblo o alrededores;
- preguntar por una criatura/señal después de haberla encontrado;
- escuchar un rumor;
- reaccionar a un descubrimiento o regreso cuando corresponda.

No necesitamos todavía árboles enormes de diálogo ni misiones enciclopédicas.

### Integración con VT-NAR-001 y VT-NAR-002

Los NPCs deben poder apoyar:

- **VT-NAR-001 — Las señales del camino**, aportando rumor, memoria local o conexión con rutas y mundo exterior;
- **VT-NAR-002 — Primeras salidas**, ayudando a que salir, observar, enfrentarse a fauna, reconocer peligro y regresar formen una experiencia narrativa continua.

No deben revelar automáticamente secretos, soluciones ni amenazas ocultas.

### Libertad del responsable de NPCs / Historiador

Narrativa solicita **funciones**, no personajes prefabricados.

El responsable correspondiente debe decidir, respetando el canon:

- nombre;
- especie;
- oficio/rol concreto;
- edad o etapa vital cuando sea relevante;
- personalidad;
- relaciones;
- forma de hablar;
- conocimiento real;
- creencias equivocadas;
- rumores que conoce;
- historia personal.

Evitar que todos los pueblos tengan copias con distinto nombre del mismo “guía”, “mercader” o “anciano”.

### Entrega que necesita Narrativa

Para cada NPC inicial, documentar como mínimo:

- pueblo y ubicación habitual;
- función en la comunidad;
- personalidad breve;
- qué sabe realmente;
- qué cree pero podría estar equivocado;
- qué puede contar inicialmente;
- qué información requiere que el jugador haya visto/hecho algo antes;
- relación relevante con otros NPCs, si existe;
- límites: qué no sabe o no debe revelar.

Después de esta entrega, el Narrador podrá escribir las escenas, conversaciones y variaciones necesarias para las primeras pruebas sin inventar unilateralmente el canon de los personajes.

**Próximo responsable:** especialista de NPCs / Historiador según la responsabilidad vigente en AGENTS.md.


## Dirección narrativa para Arte y cartografía — VT-ART-001

**Propósito:** impedir que una ilustración conceptual convierta por accidente arquetipos de fantasía, nombres generados o geografía decorativa en canon de Vintage Telnet.

### Regla principal

Arte **representa el canon; no lo completa**. Cuando falte una verdad del mundo, el espacio puede quedar ambiguo, sin nombre o pendiente del Historiador. Una imagen atractiva no convierte por sí sola un elemento en parte del mundo.

En una pieza que pretenda representar el mundo real de Vintage Telnet, solo deben aparecer como nombres, pueblos, regiones, rutas, monumentos, ruinas, mazmorras, mares, cordilleras o lugares identificables aquellos que ya estén confirmados por la fuente canónica correspondiente.

No deben introducirse nombres nuevos para llenar huecos de un mapa. Tampoco debe dibujarse un elemento espectacular —árbol sagrado, ciudad flotante, fortaleza ancestral, gran cascada, templo, ruina o mazmorra— de manera que parezca un hecho canónico si el Historiador no lo ha establecido.

### Anclas visuales ya establecidas para los cinco comienzos

- **Valdren / Humanos / Llanos de Edran:** paisaje abierto, caminos, parcelas, cercas, cultivos y vida terrestre cotidiana. La identidad humana es adaptabilidad y diversidad, no una profesión o clase única.
- **Khariel / Felaryn / Sierra de Hoshai:** montaña, desnivel, terrazas, roca, altura, equilibrio y líneas de visión. La cultura debe evocar la dirección japonesa ya establecida y la especie debe conservar rasgos felinos reconocibles.
- **Brumak / Dravak / Pedrales de Korven:** piedra, grietas, desniveles y espacios cuya escala tenga sentido para una especie mucho más pequeña que un humano. No convertirlos automáticamente en grandes dragonborn ni en una cultura definida solo por fuerza física.
- **Narevia / Marevyn / Aguas de Lethra:** agua, orillas, barro, raíces, juncos, humedad, pasarelas y espacios parcialmente acuáticos. No convertirlos automáticamente en “elfos del árbol mágico” ni deducir ciudades flotantes o cascadas monumentales sin canon.
- **Velmora / Vesperi / Bosque de Nhal:** bosque denso, penumbra, niebla, raíces, sombras, camuflaje natural y señales sutiles. No convertirlos automáticamente en enanos industriales, inventores o una cultura mecánica.

### Regla transversal de representación

**Especie ≠ clase ≠ profesión ≠ personalidad.**

Una ilustración de una especie no debe comunicar que todos sus miembros son guerreros, magos, artesanos, sombras o cualquier otra clase. Las clases siguen siendo independientes de la especie.

Las capacidades naturales tampoco deben exagerarse hasta convertirse en poderes no canónicos: Felaryn no vuelan; Dravak no poseen sonar ni visión a través de piedra; Marevyn respiran aire; Vesperi no ven en oscuridad absoluta.

### Vaisgard

Vaisgard es la ciudad común y el punto donde convergen las cinco rutas. No debe representarse como propiedad cultural exclusiva de una especie. Puede comunicar mezcla, tránsito y antigüedad, pero cualquier monumento, distrito oculto o explicación visual de su origen debe respetar lo ya establecido por el Historiador.

### Cartografía conceptual

Una ilustración puede mostrar de forma conceptual que los cinco territorios pertenecen a un mismo mundo y se relacionan con Vaisgard. Esto **no autoriza** a fijar distancias exactas, fronteras, orientación cardinal, accidentes geográficos, islas, desiertos, mares, cordilleras, rutas secundarias, ruinas o mazmorras que todavía no hayan sido establecidos.

Cuando Arte necesite completar una composición:
1. usar terreno ambiental sin nombre cuando sea compatible con el canon;
2. evitar etiquetas inventadas;
3. evitar iconos de lugares concretos no confirmados;
4. pedir al Historiador definición si el elemento necesita convertirse en lugar real;
5. marcar explícitamente una pieza como **CONCEPTUAL / NO CANÓNICA** cuando explore posibilidades todavía no aprobadas.

### Principio de descubrimiento

La documentación artística del proyecto y el conocimiento del jugador no son lo mismo. Aunque exista en el futuro un mapa interno completo para producción, la interfaz jugable no debe asumir que un personaje recién creado conoce automáticamente toda esa geografía.

**Estado VT-ART-001:** guía narrativa lista para Arte. No crea geografía nueva.
