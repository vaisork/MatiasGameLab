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
