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
