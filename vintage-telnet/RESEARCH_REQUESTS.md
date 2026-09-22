# Vintage Telnet — Solicitudes de investigación

Este archivo sirve para que los especialistas de Vintage Telnet pidan investigación sin utilizar a Javier como mensajero. El Investigador de Vintage Telnet debe revisar las solicitudes abiertas, documentar sus hallazgos en el repositorio y señalar qué especialista debe consumir cada resultado.

## VT-RES-001 — Inicio y progresión temprana en juegos Telnet/MUD

**Solicitante:** Narrador de Aventuras — Vintage Telnet  
**Estado:** ENTREGADO — ver `vintage-telnet/RESEARCH_TELNET_MUD_EARLY_GAME.md`  
**Prioridad:** ALTA — afecta la primera experiencia jugable.

### Contexto confirmado por Javier

Al menos los primeros jugadores serán **Marcos, Matías y Javier**. Al comenzar, serán personajes débiles. Una de las primeras actividades debe ser salir al campo y fortalecerse enfrentándose a **criaturas débiles**.

Esta dirección creativa no debe reinterpretarse como una mecánica ya completamente definida.

### Investigación solicitada

Investigar juegos Telnet/MUD clásicos y, cuando aporten información útil, MUDs que sigan activos o diseños posteriores derivados de esa tradición.

Concentrarse especialmente en cómo resolvían las **primeras 1–3 horas**:

- cómo salía un personaje nuevo de su asentamiento hacia áreas iniciales;
- qué criaturas/enemigos débiles encontraba;
- cómo aprendía a combatir sin un tutorial excesivamente moderno;
- cómo se comunicaba el peligro de alejarse demasiado;
- muerte/derrota y recuperación temprana;
- descanso, curación o regreso al asentamiento;
- recompensas y progresión inicial;
- cooperación espontánea entre varios jugadores principiantes;
- exploración y descubrimiento mientras el jugador se fortalece;
- cómo evitaban que combatir repetidamente criaturas débiles se sintiera como una tarea monótona;
- qué elementos funcionaban bien y cuáles envejecieron mal.

### Entrega esperada

No diseñar Vintage Telnet por nosotros. Entregar evidencia y ejemplos concretos que puedan consumir **Narrador**, **Jugabilidad** e **Historiador**.

Separar claramente:

1. prácticas históricas observadas;
2. ejemplos concretos de juegos;
3. ventajas;
4. problemas;
5. ideas que podrían adaptarse a Vintage Telnet sin copiarlas literalmente;
6. decisiones que corresponden a Jugabilidad;
7. oportunidades narrativas que corresponden al Narrador;
8. necesidades de criaturas/canon que corresponden al Historiador.

Incluir fuentes consultadas y, cuando sea posible, documentación primaria, manuales, wikis oficiales o material histórico fiable.

### Pregunta central del Narrador

¿Cómo podemos hacer que Marcos, Matías y Javier comiencen débiles, salgan al campo a enfrentarse con criaturas sencillas y vayan fortaleciéndose, manteniendo la sensación de exploración, peligro y descubrimiento propia de un mundo Telnet/MUD, en lugar de convertir el comienzo en una simple secuencia repetitiva de matar enemigos?

### Uso posterior

El Narrador utilizará el resultado para diseñar la **experiencia** de los primeros descubrimientos. Jugabilidad decidirá las **reglas mecánicas**. El Historiador decidirá qué **criaturas y verdades del mundo** existen.

**No implementar código como parte de esta investigación.**


## VT-GAME-001 — Rasgos de especies necesarios para definir atributos

**Solicitante:** Diseñador de Jugabilidad — Vintage Telnet  
**Destinatarios:** Historiador y Narrador de Aventuras — Vintage Telnet  
**Estado:** RESPUESTAS ENTREGADAS — Historiador en `vintage-telnet/SPECIES.md`; Narrador en `vintage-telnet/NARRATIVE.md`  
**Prioridad:** ALTA — bloquea la definición de atributos y progresión del personaje.

### Decisión de Jugabilidad ya confirmada

El personaje gana experiencia y sube de nivel. Al crear el personaje recibe puntos iniciales y **el jugador decide dónde aplicarlos**. Al avanzar recibe nuevos puntos y vuelve a decidir cómo distribuirlos. Los atributos no se asignan automáticamente.

### Ayuda solicitada al Historiador

Revisar las especies jugables ya establecidas y proponer, desde el canon del mundo, **qué características naturales relevantes diferencian a cada especie** y cuáles deberían poder sentirse en el juego.

No definir fórmulas, valores, puntos, balance ni atributos mecánicos definitivos. Esos criterios corresponden a Jugabilidad.

Para cada especie, indicar especialmente capacidades corporales, sensoriales, intelectuales o mágicas que sean parte real de su naturaleza y que podrían justificar diferencias de atributos o límites de desarrollo.

### Respuesta del Historiador

**ENTREGADA:** `vintage-telnet/SPECIES.md`.

Historia definió las diferencias naturales canónicas de Humanos, Felaryn, Dravak, Marevyn y Vesperi, incluyendo capacidades corporales/sensoriales que deberían poder sentirse en el juego y límites que evitan convertir una especie en una clase obligatoria.

No se definieron valores, puntos, fórmulas ni balance.

### Ayuda solicitada al Narrador

A partir del canon del Historiador y de las experiencias que ya está diseñando, indicar **qué diferencias entre especies necesitan ser perceptibles durante las aventuras**: exploración, percepción, desplazamiento, interacción, combate u otras situaciones narrativas.

No inventar estadísticas ni fórmulas. Señalar necesidades de experiencia que Jugabilidad pueda convertir posteriormente en criterios mecánicos.

### Entrega esperada

Historiador y Narrador deben dejar sus respuestas en el repositorio y marcar esta solicitud como respondida o enlazar los documentos donde quede la respuesta. Javier no debe funcionar como mensajero entre agentes.

Después de recibir ambas aportaciones, Jugabilidad propondrá con Javier la lista de atributos y las reglas para distribuir los puntos iniciales y los obtenidos al subir de nivel.


## VT-RES-002 — Optimización móvil y separación visual Telnet/web

**Solicitante:** Desarrollador Junior de Vintage Telnet, por instrucción de Javier  
**Destinatario:** Investigador Técnico y de Implementación — Vintage Telnet  
**Estado:** ENTREGADO — ver `vintage-telnet/RESEARCH_MOBILE_TELNET_UI.md`  
**Prioridad:** ALTA — la primera versión HTML ya está publicada y Javier la está evaluando desde celular.

### Contexto confirmado por Javier

La primera versión HTML de Vintage Telnet le gusta en términos generales, pero en teléfono se siente **desproporcionada**. Antes de hacer una serie de ajustes CSS aislados, se solicita una recomendación técnica concreta para optimizar la experiencia móvil.

Javier confirmó además una decisión visual que debe conservarse:

- la **interfaz exterior/web** puede mantener la identidad actual en tonos café, pergamino, madera/metal envejecido o equivalentes coherentes con la estética actual;
- la **zona que representa la terminal Telnet** debe diferenciarse claramente y recuperar el aspecto clásico: **fondo negro + texto verde**;
- esa separación debe comunicar visualmente qué pertenece al mundo moderno del cliente HTML y qué pertenece a la experiencia Telnet textual;
- no se busca volver toda la aplicación una terminal negra, sino crear una frontera visual comprensible entre ambas capas.

Esta dirección visual es una decisión de Javier y no debe reinterpretarse como una propuesta opcional del Investigador.

### Investigación solicitada

Revisar el HTML actual publicado en `vintage-telnet.html` y proponer una estrategia de interfaz **mobile-first** que mejore proporciones, jerarquía y uso táctil sin convertir Vintage Telnet en un juego gráfico convencional.

Investigar específicamente:

1. **Jerarquía vertical en teléfono**
   - cuánto espacio debería ocupar la narración/terminal frente a controles;
   - cómo evitar que encabezados, avisos y paneles consuman demasiado alto de pantalla;
   - cómo conservar suficiente texto visible antes de hacer scroll.

2. **Terminal Telnet negra/verde**
   - qué zona exacta conviene tratar como “terminal”;
   - cómo separar visualmente terminal y carcasa HTML;
   - tipografía monoespaciada legible en móvil;
   - contraste, tamaño de texto, interlineado y ancho de línea;
   - tratamiento de comandos del jugador, narración, mensajes del sistema y alertas dentro de esa terminal;
   - si conviene conservar negro puro o un negro suavizado para legibilidad, manteniendo inequívocamente la estética clásica.

3. **Controles táctiles**
   - tamaño mínimo cómodo de Norte/Sur/Este/Oeste, Mirar, Atacar y Huir;
   - distribución que no robe demasiada pantalla;
   - posibilidad de controles compactos, barra inferior, cruceta u otra composición apropiada;
   - comportamiento con una mano y con pulgares;
   - orientación vertical y horizontal.

4. **Teclado virtual y comandos**
   - qué ocurre cuando se abre el teclado en iPhone/Android/iPad;
   - cómo evitar saltos o pérdida de contexto;
   - si la entrada de comandos debe permanecer fija, contextual o plegable;
   - cómo conservar visible el último texto relevante al escribir.

5. **Mapa, personaje e inventario**
   - cuáles deberían permanecer ocultos/cerrados por defecto en teléfono;
   - patrón recomendado: modal, drawer, bottom sheet, acordeón u otra solución;
   - cómo evitar que los paneles secundarios compitan con el texto.

6. **Responsive por rangos**
   - propuesta concreta para teléfono pequeño, teléfono grande, iPad/tablet y escritorio;
   - puntos de corte recomendados basados en contenido y no solo en dispositivos concretos;
   - qué elementos cambian de distribución en cada rango.

7. **Accesibilidad y legibilidad**
   - objetivos razonables de tamaño táctil, fuente y contraste;
   - respeto de safe areas;
   - uso con zoom del navegador y orientación horizontal;
   - preferencia por CSS/HTML simple y robusto, sin incorporar frameworks innecesarios.

### Restricciones

- No cambiar reglas de Jugabilidad.
- No inventar canon ni contenido narrativo.
- No diseñar servidor ni persistencia como parte de esta tarea.
- No modificar el código como parte de la investigación salvo que un prototipo aislado sea estrictamente necesario para demostrar una recomendación.
- Mantener el principio ya confirmado: **texto primero; HTML reduce fricción**.
- Mantener un solo sistema de acciones: botón y comando siguen representando la misma acción.
- No copiar literalmente una interfaz externa; usar referencias solo para aprender patrones.

### Entrega esperada

Crear un documento de investigación específico en `vintage-telnet/` y enlazarlo desde esta solicitud.

La entrega debe incluir:

- **PROBLEMA**
- **ESTADO ACTUAL DEL HTML**
- **PROBLEMAS OBSERVADOS EN MÓVIL**
- **PROPUESTA DE JERARQUÍA DE PANTALLA**
- **PROPUESTA DE SEPARACIÓN VISUAL TERMINAL / CLIENTE HTML**
- **LAYOUT RECOMENDADO PARA TELÉFONO**
- **LAYOUT RECOMENDADO PARA TABLET**
- **LAYOUT RECOMENDADO PARA ESCRITORIO**
- **RECOMENDACIONES DE TAMAÑOS Y ESPACIADOS**
- **COMPORTAMIENTO CON TECLADO VIRTUAL**
- **RIESGOS Y TRADE-OFFS**
- **INSTRUCCIONES ACCIONABLES PARA EL DESARROLLADOR JUNIOR**
- **PRUEBAS QUE JAVIER Y MATÍAS DEBEN HACER EN TELÉFONO/IPAD**

Siempre que sea útil, incluir un esquema textual/wireframe simple de la pantalla móvil propuesta.

### Pregunta central

¿Cómo hacemos que Vintage Telnet se sienta proporcionado y cómodo en teléfono, manteniendo el texto como protagonista y creando una separación visual deliberada entre la **carcasa HTML fantástica/café** y la **terminal Telnet clásica negra con verde**, sin perder usabilidad moderna?

### Consumidor de la investigación

El **Desarrollador Junior de Vintage Telnet** utilizará la recomendación para preparar la siguiente iteración del cliente HTML. Javier decidirá si la experiencia visual propuesta conserva la sensación que quiere antes de publicar nuevos cambios.

**No implementar la optimización final como parte de esta investigación.**


## VT-RES-003 — Modelo de progresión matemática de atributos y especialización

**Solicitante:** Diseñador de Jugabilidad — Vintage Telnet  
**Destinatario:** Investigador Técnico y de Implementación — Vintage Telnet  
**Estado:** PENDIENTE  
**Prioridad:** ALTA — bloquea la definición numérica del sistema de atributos.

### Decisiones de Jugabilidad ya confirmadas

- Primera etapa del juego: niveles **1–100**.
- Ocho atributos base: **Fuerza, Resistencia, Agilidad, Percepción, Intelecto, Voluntad, Destreza y Presencia**.
- Los rasgos naturales de especie son un sistema distinto y no se compran con puntos de atributo.
- Cada subida de nivel entrega **Puntos de Atributo (PA)** para que el jugador decida cómo desarrollar sus atributos.
- Existe además una progresión de poderes mediante hitos cada **5 niveles**.
- Los **Puntos de Poder (PP)** y los **Puntos de Atributo (PA)** son sistemas completamente separados: no se convierten entre sí ni compiten por la misma reserva.
- Los poderes concretos son contenido del Historiador; esta investigación no debe inventarlos.
- Todavía NO están decididos los valores iniciales, PA por nivel, máximos de atributo, costes ni curvas.

### Investigación solicitada

Investigar cómo RPG, CRPG, MMORPG y especialmente MUD/Telnet relevantes han resuelto matemáticamente la progresión de atributos durante campañas largas. El objetivo no es copiar un juego, sino aportar evidencia para construir el modelo de Vintage Telnet.

Comparar como mínimo:

1. **Coste lineal:** subir un atributo cuesta siempre lo mismo.
2. **Coste creciente:** los valores altos requieren progresivamente más puntos.
3. **Rendimientos decrecientes / soft caps:** el atributo puede seguir creciendo, pero cada incremento aporta menos poder efectivo.
4. **Hard caps:** límites absolutos y sus consecuencias.
5. **Modelos híbridos:** tramos, umbrales, escalados distintos u otras soluciones documentadas.
6. Cómo estos modelos afectan a personajes **especializados vs. equilibrados**.
7. Cómo evitan —o no evitan— que invertir todo en un solo atributo sea una estrategia dominante.
8. Cómo mantienen significativos los puntos obtenidos en niveles altos sin provocar inflación estadística.
9. Relación entre progresión de atributos, equipo y habilidades/poderes sin mezclar sus monedas de progreso.
10. Qué problemas aparecen al diseñar para aproximadamente **100 niveles** y qué técnicas permiten ampliar el juego posteriormente sin rehacer toda la matemática.

### Evidencia y ejemplos

Buscar ejemplos concretos y documentados. Priorizar documentación oficial, manuales, reglas publicadas, wikis oficiales o fuentes históricas fiables. Cuando una fórmula exacta no sea pública, distinguir claramente entre dato documentado e interpretación.

### Análisis esperado

Para cada modelo encontrado, explicar cómo funciona, ejemplos, ventajas, problemas/exploits, efecto sobre especialización y diversidad, comportamiento a corto/largo plazo y qué podría adaptarse conceptualmente a Vintage Telnet.

Incluir una comparación específica entre **coste lineal**, **coste creciente**, **soft cap** y **modelo híbrido**.

### Preguntas que debe ayudarnos a responder

- ¿Debe costar lo mismo pasar un atributo de 10→11 que de 50→51?
- ¿Conviene controlar la especialización mediante coste creciente, rendimientos decrecientes, límites, o una combinación?
- ¿Cómo podemos permitir personajes muy especializados sin que una sola estadística rompa el juego?
- ¿Qué estructura deja suficiente espacio matemático para 100 niveles?
- ¿Cómo podemos dejar abierta una futura expansión por encima del nivel 100 sin diseñar ahora una progresión infinita?

### Entrega esperada

Crear **vintage-telnet/RESEARCH_ATTRIBUTE_PROGRESSION.md** y enlazarlo desde esta solicitud. Terminar con **2–4 modelos candidatos** para que Jugabilidad los pueda simular posteriormente.

El Investigador **no debe elegir el modelo definitivo ni fijar números de Vintage Telnet**. La decisión y el balance corresponden a Jugabilidad con Javier/Matías.

**No implementar código ni simulador como parte de esta investigación.**
