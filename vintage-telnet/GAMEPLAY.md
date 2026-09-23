# Vintage Telnet — Principios de Jugabilidad

Este documento es la **fuente de verdad de los criterios y límites de jugabilidad de Vintage Telnet** dentro de MatiasGameLab.

## Frontera entre Jugabilidad e Historiador

El **Historiador** propone y desarrolla el contenido del juego: clases, magias, poderes, monstruos, zonas, objetos, armas, aventuras, personajes, narrativa y demás elementos del mundo.

El **Diseñador de Jugabilidad**, trabajando con Javier/Matías, NO sustituye al Historiador ni inventa ese contenido. Su responsabilidad es establecer los **criterios de avance, límites y principios mecánicos generales** que ese contenido debe respetar.

Cuando el Historiador cree una zona nueva, debe presentar también las necesidades o criterios de jugabilidad que esa zona introduce. Javier y el Diseñador de Jugabilidad revisarán esas necesidades y definirán o aprobarán los criterios correspondientes antes de que se conviertan en reglas.

El Historiador puede proponer nuevas mecánicas o necesidades. No debe convertir unilateralmente una propuesta en regla de jugabilidad. De la misma manera, Jugabilidad no debe decidir por su cuenta qué clases, magias, monstruos o historias deben existir.

El Arquitecto de MatiasGameLab coordina arquitectura, responsabilidades y límites entre agentes.

## Principios confirmados

### 1. RPG de progresión
El personaje comienza con capacidades limitadas y puede hacerse más poderoso conforme avanza en el juego. Los criterios de avance deben permitir crecimiento sostenido sin obligar al jugador a permanecer para siempre en una sola especialización.

### 2. Clase inicial con especialización flexible
Todo jugador comienza con una clase básica. Las clases concretas y su contenido serán propuestas por el Historiador.

La clase inicial establece una dirección de desarrollo, pero no encierra permanentemente al personaje. En el futuro, un jugador podrá adquirir parte de las fortalezas de otras clases o desplazarse hacia otra especialización.

Avanzar dentro de la orientación natural de la clase debe ser más eficiente. Como regla v1, desarrollar una capacidad equivalente fuera de la orientación natural de la clase tendrá un **sobrecoste base del 50%** respecto de su coste normal, siempre que el canon permita adquirirla. Los poderes y restricciones concretas siguen perteneciendo al Historiador.

No se debe permitir que un personaje obtenga fácilmente todas las ventajas de todas las clases.

### 3. Mundo persistente
El jugador regresa al juego en el lugar donde quedó la última vez y continúa desde allí. No comienza una partida nueva cada vez que entra.

Las acciones importantes pueden dejar consecuencias visibles para otros jugadores.

### 4. Exploración Telnet
El desplazamiento básico conserva la lógica clásica de Telnet: norte, sur, este y oeste.

El mundo puede contener ciudades, caminos, mazmorras y otros lugares conectados. Los trayectos largos pueden recorrerse como caminos reales dentro del mundo en lugar de ser únicamente saltos instantáneos entre destinos.

### 5. Mapa general y descubrimiento
El jugador dispondrá de orientación mediante un mapa general, pero el mapa no tiene que revelar todo lo que existe.

Pueden existir zonas escondidas que deban descubrirse mediante palabras secretas, pistas, condiciones u otros mecanismos propuestos por el Historiador y aprobados en sus criterios de jugabilidad.

Descubrir que existe un lugar oculto forma parte de la exploración.

### 6. Persistencia de monstruos
Los monstruos comunes reaparecen después de cierto tiempo. Como referencia v1, el respawn común será de aproximadamente **5 minutos**, configurable por criatura/zona. Enemigos especiales pueden tener tiempos mayores.

Los monstruos principales, especialmente fuertes o difíciles de vencer, pueden ser únicos y persistentes. Una vez derrotados permanecen muertos para los demás jugadores.

El mundo debe conservar evidencia de que ese monstruo existió y fue derrotado —por ejemplo restos u otra señal definida por el contenido— y debe poder quedar registrado quién logró la derrota.

### 7. Mundo multijugador e interacción
Los jugadores pueden coincidir en el mismo mundo y comunicarse mediante texto.

La primera versión utiliza comunicación local explícita en la sala mediante `decir <texto>`; el detalle queda fijado en §26. Chat global u otros canales pueden añadirse posteriormente.

El PvP está permitido. Un jugador puede iniciar un ataque directo contra otro sin que sea obligatorio aceptar previamente un duelo o mantener una conversación.

El jugador atacado debe recibir información clara de que está siendo atacado.

### 8. Protección ante diferencias extremas de poder
El PvP abierto no debe convertir una diferencia enorme de poder en una muerte inevitable para el jugador débil.

Cuando un jugador extremadamente fuerte ataca a uno claramente inferior, el jugador débil debe disponer de una oportunidad real de escapar. La fórmula v1 de huida y la protección por diferencia de nivel quedan definidas en la sección 20.

### 9. Combate semi-automático con intervención estratégica
Una vez iniciado el combate, los ataques básicos pueden continuar automáticamente.

El jugador no necesita ordenar manualmente cada golpe, especialmente contra enemigos comunes. Durante el combate debe poder intervenir estratégicamente mediante las capacidades que el contenido del juego le proporcione: por ejemplo magia, poderes especiales, objetos, defensa o huida.

Las capacidades especiales no deben estar disponibles sin límite todo el tiempo. La v1 utiliza categorías de recarga aproximadas de 2, 4 y 8 rondas según potencia; el Historiador propone cada poder y Jugabilidad lo asigna a una categoría compatible.

Los combates rutinarios pueden requerir poca intervención; los enfrentamientos peligrosos deben hacer que las decisiones del jugador tengan mayor importancia.

### 10. Muerte, derrota y reaparición
Cuando la vida del personaje llega a **0 HP**, el personaje cae muerto y el combate termina. Esta muerte no elimina permanentemente al personaje ni borra todo su progreso.

Después de morir, el personaje reaparece en un **punto de reaparición válido y seguro**.

El hogar del personaje puede funcionar como punto de reaparición cuando corresponda, pero no será obligatoriamente el destino después de cada muerte. En viajes largos, mazmorras u otras zonas extensas pueden existir puntos de reaparición que eviten obligar al jugador a repetir innecesariamente un trayecto largo hasta regresar desde su pueblo.

El punto utilizado debe respetar el contexto de la zona y no colocar al personaje inmediatamente en una situación inevitable de nuevo combate o muerte.

**Jugabilidad define el comportamiento general de muerte y reaparición. El Narrador define qué lugares concretos del mundo funcionan como puntos de reaparición y cómo se presentan o justifican dentro de la experiencia narrativa.**

Una muerte no borra al personaje ni destruye todo el progreso acumulado. Esto es especialmente importante porque el personaje puede estar vinculado a piezas físicas impresas.

La recuperación v1 después de morir queda fijada en la sección 20. La selección concreta entre puntos válidos y cualquier requisito de descubrimiento/activación siguen dependiendo del diseño narrativo y de zona.

### 11. Riesgo de pérdida de armas
Morir frente a monstruos comunes no provoca pérdida del arma por este principio.

Las derrotas contra monstruos excepcionalmente poderosos y las derrotas en PvP sí pueden provocar pérdida de armas.

Cuando un jugador pierde el derecho sobre un arma, conservar físicamente una pieza impresa no le permite seguir utilizándola dentro del juego. Debe volver a obtener legítimamente el derecho a usarla conforme a las reglas del juego.

### 12. Equipamiento físico
No todo objeto requiere representación física. Determinadas mejoras importantes tendrán una pieza imprimible en 3D que pueda aplicarse a la figura base del jugador.

Las piezas deben favorecer un sistema práctico de accesorios —armas, báculos, prendas u otros elementos que proponga el contenido— en vez de exigir imprimir una figura completa en cada mejora.

Pueden imprimirse en un solo color. Pintarlas posteriormente es opcional.

### 13. Activación de piezas físicas
Ganar una mejora que requiere pieza física no basta para poder utilizarla.

El ciclo acordado es:

**Ganar la mejora → fabricar/recibir la pieza → colocarla físicamente en la figura del jugador → enviar evidencia fotográfica → validar la evidencia → habilitar su uso dentro del juego.**

Que el Maestro de Forja fabrique o entregue la pieza no la activa por sí solo.

### 14. Maestro y Validador de Forja
Javier Díaz es el **Maestro de Forja** y también puede participar como jugador y ejercer como Maestro del Juego.

El jugador debe presentar evidencia de haber aplicado la pieza a su figura.

Se prevé un **Validador de Forja** separado que comprueba esa evidencia y registra la validación. El Validador aplica las reglas; no las inventa.


## 15. Interfaz híbrida — espíritu Telnet con capacidades HTML

Vintage Telnet conservará el **texto, la lectura, el descubrimiento y la estructura de mundo de un MUD/Telnet**, pero no obligará al jugador a utilizar una terminal antigua ni a memorizar comandos frecuentes.

La interfaz HTML forma parte deliberada de la experiencia. Su función es hacer más accesibles y legibles las acciones habituales sin eliminar el carácter textual del juego.

### Texto e historia como núcleo
Las descripciones de lugares, encuentros, criaturas, conversaciones, rumores, historia y descubrimientos continúan presentándose principalmente mediante texto. Leer el mundo sigue siendo una parte fundamental de jugar.

Las mejoras visuales no deben convertir Vintage Telnet en un juego gráfico convencional que relegue el texto a un elemento secundario.

### Botones para acciones frecuentes
Las acciones que el jugador realiza constantemente pueden tener botones visibles y táctiles.

Quedan confirmados como ejemplos fundamentales:
- movimiento por direcciones;
- atacar;
- huir.

La interfaz podrá añadir otras acciones frecuentes cuando Jugabilidad las apruebe. El jugador no debe necesitar abrir el teclado y escribir una dirección cada vez que quiera desplazarse.

### Una acción, distintas formas de entrada
Cuando una acción pueda ejecutarse mediante botón y mediante comando escrito, ambas entradas representan **la misma acción del juego**. No existen reglas diferentes por utilizar botón o texto.

Los comandos escritos pueden conservarse para jugadores que prefieran utilizarlos y para interacciones especiales, conversación, descubrimientos o secretos cuando corresponda.

### Mapa HTML más detallado
Vintage Telnet aprovechará HTML para ofrecer un mapa visual más claro y detallado que el que sería habitual en una terminal clásica.

El mapa ayuda a comprender lugares, caminos y orientación, pero **no revela automáticamente zonas secretas, rutas ocultas ni información que el personaje todavía no haya descubierto**.

La interfaz puede mejorar la orientación sin eliminar la exploración.

### Información en pantallas legibles
Información que resulte incómoda dentro del flujo continuo de texto puede mostrarse mediante pantallas o paneles HTML fáciles de consultar.

Esto puede incluir, según las reglas que se definan posteriormente, personaje, inventario, equipo, mapa, ayuda, instrucciones y estado de combate.

El objetivo es evitar que información importante quede enterrada entre mensajes y facilitar el uso desde teléfono, iPad/tablet y computadora.

### Principio de diseño
**El mundo se descubre y se narra con el espíritu de un Telnet; las acciones frecuentes y la información compleja aprovechan una interfaz web moderna.**

HTML debe reducir fricción, no resolver automáticamente decisiones del jugador ni revelar aquello que todavía debe descubrir.

## 16. Atributos base orientados a lectura — confirmados conceptualmente

Después de las revisiones VT-GAME-002 del Narrador e Historiador y VT-PSY-001/001A de Psicopedagogía, se mantienen los ocho atributos base: **Fuerza, Resistencia, Agilidad, Percepción, Intelecto, Voluntad, Destreza y Presencia**.

Los rasgos naturales de especie son una capa distinta. Un atributo alto no crea anatomía, sentidos, magia, conocimientos, equipo, reputación ni técnicas que el personaje no posea.

### Regla de lectura

Para escenas que pretendan premiar comprensión se adopta:

**Información → Comprensión → Acción → Consecuencia.**

Los atributos pueden cambiar la información recibida, qué puede intentar el personaje, la calidad de ejecución o las consecuencias. No deben sustituir sistemáticamente la comprensión del jugador.

- **Percepción aporta señales; Intelecto aporta contexto/conocimiento; el jugador realiza la deducción final cuando corresponda.**
- **Agilidad gobierna ejecución corporal; Destreza, ejecución manual fina.**
- **Fuerza gobierna potencia; Resistencia, capacidad de sostener y soportar esfuerzo.**
- **Presencia mejora la recepción de una propuesta plausible; no convierte automáticamente una mala decisión o argumento absurdo en éxito.**

Los fallos relevantes deben tener una causa narrativamente interpretable cuando sea razonable, aunque la fórmula interna permanezca oculta.

## 17. Principios confirmados del combate físico basado en atributos

El combate continúa siendo **semi-automático**, pero leer debe mejorar las decisiones del jugador incluso cuando sus atributos no cambien.

**Leer la situación → decidir qué intentar → ejecutar según atributos, equipo, estado y contexto → recibir una consecuencia narrada.**

### Ataque físico normal

- **Destreza:** precisión y calidad con que se coloca el ataque.
- **Fuerza:** potencia física transmitida cuando conecta.

Fuerza no determina por regla general tanto precisión como potencia.

Los demás atributos intervienen solo cuando el contexto lo justifica: Percepción puede revelar aperturas; Agilidad ayuda en movimiento/reacción/posición; Resistencia sostiene rendimiento prolongado; Voluntad actúa bajo presión mental, dolor o concentración; Intelecto aporta conocimiento legítimo; Presencia puede intervenir en intimidación, coordinación o provocación. Ninguno aumenta automáticamente cada golpe.

Los poderes concretos pertenecen al contenido del Historiador. Jugabilidad decidirá posteriormente qué atributos afectan cada tipo de poder; no se establece un atributo mágico universal.

Un resultado incompleto no debe narrarse siempre como “fallaste”: puede ser esquivado, bloqueado, desviado, interrumpido, mal colocado o superficial según lo ocurrido.

### Defensa física

| Defensa | Atributo principal | Función |
| --- | --- | --- |
| **Esquivar** | Agilidad | evitar que el ataque conecte mediante movimiento corporal |
| **Bloquear/desviar** | Destreza | manejar correctamente arma, escudo u objeto apropiado |
| **Resistir** | Resistencia | soportar mejor las consecuencias cuando el ataque conecta |

Percepción puede aportar una señal previa cuando exista algo legítimo que detectar, pero no elige la respuesta.

Resistencia no dificulta por sí sola que te golpeen; Agilidad no absorbe daño; Destreza no garantiza bloqueo si equipo, posición o ataque lo hacen inapropiado.

**Ninguna defensa debe ser siempre la mejor.** La descripción del ataque, enemigo, terreno, equipo y estado debe poder ayudar al jugador a decidir. Las alternativas no deben ser botones equivalentes que ejecutan la misma tirada con nombres diferentes.

### Vida, heridas y fatiga

Se confirma un modelo híbrido de información: el jugador podrá consultar **vida numérica exacta (HP)** y, simultáneamente, recibir un **estado narrativo** comprensible sobre la condición del personaje. La interfaz no debe obligar a elegir entre precisión matemática y lectura narrativa.

Se mantienen separados tres conceptos:
- **Vida/HP:** cuánto daño puede soportar el personaje antes de ser derrotado.
- **Heridas:** consecuencias concretas del daño que pueden llegar a afectar temporalmente determinadas capacidades. Su catálogo y efectos exactos siguen pendientes.
- **Fatiga:** desgaste producido por esfuerzo; no es equivalente al daño ni constituye una segunda barra de vida.

La fatiga tendrá una **barra/valor visible** y también estados o señales narrativas comprensibles. Resistencia influye según §20.7 y los efectos/costes operativos quedan cerrados en §24.

Una fatiga elevada no provoca automáticamente derrota. Debe afectar de manera comprensible la capacidad de mantener determinadas acciones, su coste o eficacia, favoreciendo cambios de estrategia.

La recuperación de fatiga será **combinada**:
1. existe recuperación gradual cuando cesa el esfuerzo que la genera;
2. una acción explícita de descanso permite una recuperación más rápida o eficaz.

Los ritmos, condiciones, interrupciones y cantidades v1 de recuperación quedan definidos en §24.

El diseño debe evitar una proliferación innecesaria de estados difíciles de recordar. Las condiciones importantes deben ser pocas, significativas y comunicadas con claridad.

### Pendiente antes de las matemáticas de combate

La v1 ya define valores iniciales, crecimiento, HP, precisión, daño físico, defensa, fatiga, heridas, reaparición y huida en las secciones 19–20. Siguen abiertos los valores concretos de armas/armaduras, críticos, poderes individuales y ajustes finos derivados de pruebas reales.

## 18. Progresión incremental de la dificultad

La progresión del personaje y la progresión de la dificultad del mundo son **curvas relacionadas pero distintas**.

Subir de nivel aumenta las capacidades del personaje. Al mismo tiempo, conforme el jugador avanza, los desafíos pueden exigir progresivamente mejores decisiones, mayor comprensión de la información disponible y mejor administración de atributos, estado y recursos.

**El aumento de dificultad no debe limitarse a inflar HP, daño u otras estadísticas de enemigos.** La dificultad también puede crecer mediante situaciones que exijan relacionar más información y tomar decisiones más complejas.

Como orientación psicopedagógica ya investigada, la exigencia cognitiva puede crecer gradualmente desde señales evidentes hacia combinaciones de señales, ambigüedad, ausencia o contradicción de información y, posteriormente, memoria de información anterior. La aplicación concreta de estos principios a escenas pertenece al Narrador y a Psicopedagogía; Jugabilidad establece únicamente el criterio de progresión.

La curva matemática de atributos deberá evaluarse junto con esta dificultad incremental. Un coste creciente de especialización y una dificultad creciente pueden castigar dos veces al jugador si ambas curvas son demasiado agresivas.

Por ello, antes de aprobar PA por nivel, costes de atributos o tramos definitivos, las simulaciones deberán comprobar conjuntamente:
- crecimiento del especialista, doble especialista y generalista;
- aumento esperado de exigencia de los desafíos;
- que los niveles altos sigan ofreciendo decisiones útiles de progreso;
- que especializarse siga siendo viable sin convertirse en una solución universal;
- que la dificultad avanzada premie mejor lectura y decisión, no solamente cifras mayores.

**Principio confirmado:** subir de nivel aumenta la capacidad del personaje, pero el aumento de dificultad debe ser incremental y no limitarse a aumentar estadísticas enemigas; también debe introducir gradualmente situaciones que exijan mejores decisiones y comprensión de la información.


## 19. Crecimiento de atributos y competencia general — confirmado

Después de comparar múltiples perfiles de jugador —especialista, doble especialista, equilibrado, irregular y casual/no optimizado— se confirma como base de crecimiento de la primera etapa de niveles 1–100:

### Puntos de Atributo

- Cada subida de nivel entrega **2 Puntos de Atributo (PA)**.
- Los PA se gastan únicamente en atributos y continúan separados de los Puntos de Poder (PP).
- El coste de aumentar un atributo es creciente y visible.

| Valor actual del atributo | Coste del siguiente +1 |
| --- | ---: |
| 10–19 | 1 PA |
| 20–34 | 2 PA |
| 35–44 | 3 PA |
| 45–59 | 4 PA |
| 60+ | 5 PA |

Esta curva busca conservar tres estilos viables:
- un especialista puede alcanzar valores extraordinarios a cambio de sacrificar desarrollo general;
- un doble especialista puede mantener dos fortalezas claras;
- un personaje equilibrado o casual obtiene mayor versatilidad total y no queda inutilizado por una distribución imperfecta.

El diseño no debe exigir una build matemáticamente perfecta para poder progresar.

### Competencia general por nivel

Además de los PA, el crecimiento de nivel aporta una **competencia general** que evita que un personaje de nivel alto siga comportándose como novato en todas las áreas que no especializó.

Como referencia aprobada para la primera etapa, la competencia general acumulada equivale aproximadamente a **+8 unidades de capacidad base al nivel 100**. Su aplicación debe escalar gradualmente a lo largo de los niveles; no debe entregarse de golpe al final.

Esta competencia general:
- no sustituye los atributos;
- no borra las diferencias entre builds;
- no convierte a todos los personajes en iguales;
- proporciona un piso de experiencia acumulada para que especialista, generalista y jugador casual sigan siendo funcionales.

Para la v1 se adopta una progresión lineal de esa competencia general, detallada en la sección 20: `CG = 8 × (nivel - 1) / 99`.

### Principio de balance

**Nivel aporta competencia general; PA aportan identidad y especialización.**

Ningún atributo debe convertirse por sí solo en una solución universal. Las fórmulas derivadas pueden combinar atributos y aplicar límites naturales cuando sea necesario, pero no deben aplicar rendimientos decrecientes de forma indiscriminada si el coste creciente ya controla la especialización.

La dificultad incremental del mundo deberá calibrarse contra este modelo de crecimiento, de modo que:
- todos los perfiles razonables puedan progresar;
- especializarse otorgue ventajas reales en el área elegida;
- un personaje equilibrado conserve valor por versatilidad;
- una distribución casual o imperfecta no arruine permanentemente al personaje.

Los valores iniciales y las fórmulas físicas base de la v1 ya están definidos en la sección 20. Exploración, investigación y social conservan los principios de atributos confirmados y se afinarán con contenido real sin permitir que los atributos sustituyan la comprensión del jugador.


## 20. Matemática de Jugabilidad v1 — lista para implementación

**Estado:** APROBADA COMO BASE V1 PARA ARRANCAR EL JUEGO.  
**Objetivo:** disponer de una matemática completa y coherente para la primera implementación y ajustar posteriormente con partidas reales sin cambiar los principios de diseño.

### 20.1 Valores iniciales

Todo personaje comienza con **10** en cada uno de los ocho atributos base:

- Fuerza 10
- Resistencia 10
- Agilidad 10
- Percepción 10
- Intelecto 10
- Voluntad 10
- Destreza 10
- Presencia 10

La progresión posterior usa los **2 PA por nivel** y la curva de costes confirmada en la sección 19.

### 20.2 Competencia general

La competencia general crece gradualmente desde 0 en nivel 1 hasta aproximadamente **+8 en nivel 100**.

Referencia lineal v1:

`CG = 8 × (nivel - 1) / 99`

El motor puede almacenar este valor internamente con decimales aunque la interfaz no necesite mostrarlo como atributo independiente.

**Nivel aporta competencia general; PA aportan identidad y especialización.**

### 20.3 Vida máxima

Fórmula base v1:

`HPmax = 100 + 1.25 × (nivel - 1) + 2.5 × (Resistencia - 10) + 0.5 × (Voluntad - 10)`

Objetivo:
- todos ganan vida por experiencia;
- Resistencia es la principal fuente atributiva de supervivencia;
- Voluntad aporta una contribución secundaria;
- ningún atributo de ataque aumenta HP.

### 20.4 Ataque físico

La precisión y la potencia permanecen separadas.

**Probabilidad base de impacto v1:**

`Impacto = limitar(55 + 0.45×(Destreza-10) + 0.18×(Percepción-10) + 0.5×(CG_atacante-CG_defensor), 25, 90)`

**Daño físico bruto v1 con arma base 10:**

`DañoBruto = BaseArma + 0.48×(Fuerza-10) + 0.12×(Destreza-10) + 0.25×CG`

`BaseArma = 10` es únicamente la referencia de arma básica para arrancar. Armas concretas podrán cambiar ese valor cuando el contenido/equipamiento sea definido.

Principios:
- Destreza coloca el golpe;
- Fuerza aporta la mayor parte de la potencia;
- Percepción ayuda moderadamente a detectar una oportunidad;
- Destreza no debe convertirse simultáneamente en mejor ataque y mejor defensa universal.

### 20.5 Defensas físicas

El jugador puede elegir una respuesta apropiada cuando el contexto lo permita.

**Esquivar — Agilidad:**

`ImpactoTrasEsquiva = limitar(Impacto - 0.48×(AgilidadDefensor-10) - 0.12×(PercepciónDefensor-10), 20, 90)`

Evita contacto; no reduce daño si el golpe finalmente conecta.

**Bloquear/desviar — Destreza:**

Requiere arma, escudo u objeto adecuado.

`ReducciónBloqueo = mínimo(32%, 10% + 0.35%×(DestrezaDefensor-10))`

Bloquear no debe estar disponible cuando el ataque, posición o equipo lo hagan incoherente.

**Resistir — Resistencia:**

`ReducciónResistencia = mínimo(38%, 0.55%×(ResistenciaDefensor-10))`

Resistir acepta el impacto y reduce sus consecuencias; no reduce la probabilidad de ser golpeado.

**Regla:** ninguna de las tres defensas debe ser siempre óptima. El texto del ataque, terreno, equipo y estado debe dar información útil para elegir.

### 20.6 Escala de dificultad de enemigos

Para la primera implementación se usa una referencia relativa al desafío esperado del nivel:

- **enemigo común:** alrededor del 80% de la referencia de poder del nivel;
- **enemigo peligroso:** alrededor del 100%;
- **jefe/desafío superior:** alrededor del 120% o más según contenido.

Estos porcentajes son referencias de calibración, no obligación de que todos los monstruos se generen por multiplicación automática.

**Regla de diseño:** todos los perfiles razonables deben poder progresar contra contenido común. La especialización determina qué desafíos superiores resultan más accesibles.

Los jefes pueden requerir mejor lectura, estrategia, equipo, poderes o cooperación y no están obligados a ser derrotables por toda build solo por compartir nivel.

### 20.7 Fatiga

La fatiga usa una escala visible de **0–100**.

Estados v1:
- 0–69: operativo;
- 70–89: **cansado**;
- 90–100: **agotado**.

Llegar a 100 de fatiga **no mata** al personaje. Limita la capacidad de mantener acciones exigentes y/o reduce su eficacia.

Resistencia reduce la fatiga generada por acciones mediante el modificador base:

`ModFatiga = máximo(0.55, 1 - 0.007×(Resistencia-10))`

`FatigaGanada = CosteBaseAcción × ModFatiga`

El coste base de cada acción concreta pertenece a la tabla de acciones/poderes y puede balancearse sin cambiar esta regla.

**Descanso:** una acción explícita de descanso produce recuperación fuerte de fatiga y puede ser interrumpida por peligro/combate. Además existe recuperación gradual fuera de esfuerzo intenso.

### 20.8 Heridas

Para evitar saturación de estados, la v1 utiliza únicamente tres grados:

1. **leve**
2. **moderada**
3. **grave**

Las heridas son consecuencias concretas diferentes del HP y de la fatiga. Sus efectos deben ser comprensibles y temporales.

No se deben acumular listas largas de estados menores. El contenido puede describir una herida de muchas maneras, pero mecánicamente debe mapearla a uno de estos tres grados.

### 20.9 Muerte y reaparición

Al llegar a 0 HP:
- el personaje muere;
- termina el combate;
- no pierde nivel, PA ni XP por la muerte;
- reaparece en un punto seguro válido definido para la zona.

Estado v1 al reaparecer:
- **60% del HP máximo**;
- **40 puntos de fatiga**;
- una herida grave baja a moderada;
- una herida moderada baja a leve;
- una herida leve desaparece;
- como regla de simplicidad, tras el respawn no debe persistir más de **una herida**.

Esto implementa la recuperación intermedia aprobada: morir tiene consecuencia, pero no crea un ciclo de muerte inmediata.

### 20.10 Huida y protección PvP

La huida parte de aproximadamente **50%** cuando atacante y defensor tienen condiciones comparables.

Fórmula v1 de referencia:

`Huir% = limitar(50 + 0.45×ΔAgilidad + 0.15×ΔPercepción + ProtecciónDesnivel + 15×FallosPrevios - PenalizaciónFatiga, 20, 95)`

Donde:
- `ΔAgilidad = AgilidadJugador - AgilidadOponente`;
- `ΔPercepción = PercepciónJugador - PercepciónOponente`;
- `ProtecciónDesnivel = mínimo(30, 0.6 × niveles que el atacante supera al jugador)`;
- cada intento fallido consecutivo aporta **+15 puntos porcentuales** al siguiente intento;
- una fatiga superior a 70 puede aplicar penalización.

Esto hace que una diferencia extrema de poder incremente, en vez de reducir, la posibilidad de escape del jugador débil.

El máximo de 95% preserva incertidumbre sin convertir una enorme diferencia de nivel en ejecución inevitable.

### 20.11 Poderes y PP

PA y PP siguen siendo economías completamente separadas.

Se fija para la v1:
- **1 PP en cada hito de 5 niveles**;
- niveles 5, 10, 15... 100;
- **20 hitos/PP potenciales** durante la primera etapa 1–100.

Categorías base de recarga:
- **poder rápido:** alrededor de 2 rondas;
- **poder fuerte:** alrededor de 4 rondas;
- **poder mayor:** alrededor de 8 rondas o una restricción equivalente más fuerte.

El Historiador propone poderes concretos. Jugabilidad decide su coste en PP, categoría de recarga y cualquier atributo que afecte su ejecución.

No existe un atributo mágico universal.

### 20.12 Desarrollo fuera de clase

Como regla v1, una capacidad equivalente fuera de la orientación natural de la clase tiene un **sobrecoste base del 50%**.

Este sobrecoste:
- no permite aprender algo prohibido por canon;
- no crea poderes que el Historiador no haya definido;
- no convierte todas las clases en equivalentes;
- sí permite movilidad de especialización a largo plazo.

### 20.13 Mirar, observar y examinar

Se fijan tres niveles mínimos de inspección textual:

- **mirar:** descripción general de la situación/lugar;
- **observar:** enfoca señales relevantes de una zona, objetivo o cambio;
- **examinar:** inspección detallada de un elemento concreto.

Una pista no debe revelarse automáticamente mediante un botón contextual antes de que el jugador tenga información legítima para buscarla.

En las primeras experiencias, repetir mirar/observar no debe consumir irreversiblemente una oportunidad crítica de comprensión. Los primeros errores razonables deben ser recuperables.

### 20.14 Respawn de monstruos

Referencia v1:
- monstruo común: alrededor de **5 minutos**;
- monstruo especial: tiempo mayor/configurable por contenido;
- monstruo principal único: permanece muerto según la regla persistente ya confirmada.

El respawn concreto puede configurarse por criatura/zona sin cambiar este principio.

### 20.15 Parámetros afinables después de pruebas reales

La v1 está lista para implementación, pero estos valores se consideran **afinables sin rediseñar el sistema**:

- BaseArma y valores de armas/armaduras;
- costes base de fatiga por acción;
- impacto exacto de estados cansado/agotado;
- efectos concretos de heridas leve/moderada/grave;
- porcentajes finos de precisión, bloqueo, resistencia y huida;
- dificultad concreta de cada enemigo;
- cooldown/coste PP de cada poder;
- tiempos de respawn de criaturas especiales.

Modificar estos parámetros requiere pruebas y registro de balance, pero no reabrir los principios de Jugabilidad completos.

### 20.16 Criterio de lanzamiento

Esta matemática se considera suficiente para **arrancar la implementación jugable**.

El siguiente ciclo de balance debe basarse en partidas reales y telemetría/pruebas con varios perfiles:
- especialista;
- doble especialista;
- equilibrado;
- irregular;
- casual/no optimizado.

Especialmente importante: un niño que haya distribuido PA de forma imperfecta debe poder seguir progresando y entender por qué una acción funcionó o falló.



## 21. Arcanes — vínculo, compañía y poder único

**Estado:** CRITERIO V1 APROBADO.  
**Canon de referencia:** `vintage-telnet/ARCANES.md`.

Los Arcanes son contenido del mundo definido por el Historiador y presentado mediante escenas por el Narrador. Jugabilidad define únicamente cómo un jugador puede establecer el vínculo y qué límites mecánicos tiene después.

### 21.1 No se capturan automáticamente

Un Arcane **no se obtiene simplemente derrotándolo, tocándolo o repitiendo una acción**.

El flujo general aprobado es:

**encontrar → observar → comprender su comportamiento → comprobar compatibilidad → generar confianza mediante decisiones → vínculo voluntario → nombrar.**

El Narrador decide la escena concreta, las señales y el comportamiento. El sistema debe permitir que leer esas señales mejore las decisiones del jugador.

### 21.2 Confianza sin barra numérica visible

La confianza puede representarse internamente mediante pocos estados discretos, por ejemplo:

- desconfiado;
- tolera la presencia;
- se acerca;
- confía;
- vínculo posible.

No se mostrará una barra tipo `63/100` ni se diseñará el vínculo como una actividad de farmeo.

**Repetir indefinidamente la misma acción no aumenta confianza por sí solo.** El avance depende del contexto y de decisiones compatibles con lo que el Arcane comunica mediante su comportamiento.

Un error razonable puede cerrar el vínculo durante ese encuentro sin convertir necesariamente al Arcane en imposible para siempre, salvo que el contenido establezca una condición real distinta.

### 21.3 Compatibilidad basada en poderes ya adquiridos

Algunos Arcanes pueden aceptar prácticamente a cualquier personaje. Otros pueden tener incompatibilidades concretas.

Para mantener el sistema simple, en la v1 la compatibilidad especial **solo consulta poderes concretos que el personaje ya haya adquirido**.

No se calcula con:
- porcentajes;
- una puntuación de afinidad;
- el valor total de atributos;
- la clase por sí sola;
- una etiqueta genérica de “especialista”.

El contenido de un Arcane puede declarar una lista simple de poderes incompatibles. Si el jugador ya posee uno de esos poderes, ese Arcane no puede establecer vínculo con él.

La incompatibilidad es una condición real del mundo, no una tirada con una probabilidad pequeña de éxito.

El Narrador debe presentar el rechazo mediante comportamiento comprensible del Arcane y, cuando sea posible, dar señales antes de que el jugador invierta mucho tiempo intentando el vínculo.

### 21.4 Un vínculo existente no se rompe retroactivamente

Por defecto, adquirir después un poder que habría impedido el vínculo **no elimina un Arcane que ya era compañero del jugador**.

Una excepción futura tendría que ser diseñada explícitamente como contenido especial y revisada por Jugabilidad; no debe surgir automáticamente de la comprobación de compatibilidad.

### 21.5 Nombre elegido por el jugador

Antes del vínculo, el Arcane se identifica únicamente mediante apariencia, comportamiento y anomalía, conforme a `ARCANES.md`.

Cuando el vínculo queda establecido, **el jugador elige su nombre individual** y el servidor lo guarda de forma persistente.

El Historiador, Narrador, Arte y el sistema no deben imponer previamente un nombre propio a un Arcane todavía no vinculado.

### 21.6 Límite y acompañante activo

Un jugador puede tener como máximo **tres Arcanes vinculados**.

- Puede conservarlos en su casa.
- Solo **un Arcane puede viajar como acompañante activo a la vez**.
- Los demás permanecen guardados en casa hasta que el jugador cambie su acompañante.
- Un Arcane que permanece en casa no aporta su poder al personaje.

Esto evita acumulación simultánea de beneficios y mantiene legible la relación con cada compañero.

### 21.7 Un solo poder fijo por Arcane

Cada Arcane aporta:

1. **compañía**;
2. **un único poder propio fijo**.

El Arcane:
- no sube de nivel;
- no gana PA ni PP;
- no posee árbol de habilidades;
- no desbloquea poderes adicionales;
- no mejora progresivamente su poder;
- no necesita una segunda matemática de atributos paralela a la del jugador.

El Historiador define/valida qué poder pertenece a cada tipo de Arcane. El Narrador decide cómo se descubre o se expresa en la experiencia. Jugabilidad valida únicamente su efecto mecánico y balance antes de implementarlo.

El poder puede ser activo, pasivo o contextual según el contenido concreto, pero **solo el Arcane acompañante activo puede aportar ese poder**.

### 21.8 Sin muerte permanente ordinaria

Un Arcane vinculado no se pierde permanentemente por una derrota ordinaria del jugador o por quedar incapacitado durante una situación peligrosa.

La v1 debe permitir narrar retirada, incapacidad o regreso/recuperación en casa sin borrar el vínculo ni el nombre elegido por el jugador.

Las condiciones exactas de recuperación pueden ajustarse cuando existan los primeros poderes y escenas concretas.

### 21.9 Principio de diseño

**El Arcane se consigue comprendiendo y construyendo un vínculo, no farmeando una barra; después es compañía + un poder fijo, no un segundo personaje que haya que levelear.**

Esta simplicidad es deliberada: los Arcanes deben añadir identidad, exploración y decisiones al mundo sin crear un sistema paralelo de progresión.

### 21.10 Handoff al Narrador

Con estas reglas cerradas, el Narrador ya puede diseñar encuentros concretos donde:
- el Arcane inicialmente se presenta según el canon de `ARCANES.md`;
- el jugador recibe señales de su comportamiento;
- existen acciones adecuadas e inadecuadas;
- puede aparecer una incompatibilidad con un poder ya adquirido;
- el vínculo requiere decisiones y no repetición;
- al aceptar permanecer con el jugador se habilita el momento de nombrarlo;
- la escena no necesita inventar niveles, estadísticas ni progresión para el Arcane.

El Narrador puede proponer para cada Arcane qué conductas permiten ganar confianza y qué señales muestran rechazo. Si necesita una nueva regla mecánica, debe devolverla a Jugabilidad antes de convertirla en norma.


## 22. XP, recompensas, cooperación y antifarmeo — v1

**Estado:** APROBADO PARA IMPLEMENTACIÓN.  
**Objetivo:** cerrar el bucle `explorar → combatir/descubrir → ganar progreso → subir de nivel → repartir PA → seguir explorando` sin convertir el juego en una rutina de matar siempre la misma criatura.

### 22.1 Curva de XP 1–100

La XP necesaria para pasar del nivel `L` al siguiente nivel usa:

`XP_siguiente(L) = redondear(100 + 18×(L-1) + 0.25×(L-1)^2)`

Referencias:

| Nivel actual | XP para subir |
| ---: | ---: |
| 1 | 100 |
| 5 | 176 |
| 10 | 282 |
| 25 | 676 |
| 50 | 1,582 |
| 75 | 2,801 |
| 99 | 4,265 |

La XP acumulada aproximada para alcanzar nivel 100 desde nivel 1 es **176,843**.

Reglas:
- la XP es una economía separada de PA y PP;
- subir de nivel entrega los PA/PP ya definidos en las secciones anteriores;
- el exceso de XP se conserva al cruzar un nivel;
- en nivel 100 no se acumula progreso hacia un nivel 101 durante la v1.

### 22.2 Nivel de referencia del contenido

Cada criatura, descubrimiento o hito que otorgue XP debe tener un **nivel de referencia de progresión** asignado por Jugabilidad al integrarse.

Ese nivel:
- no cambia el canon del Historiador;
- no necesita mostrarse al jugador;
- sirve únicamente para calcular una recompensa razonable;
- evita que contenido de nivel inicial entregue grandes cantidades de XP a un personaje veterano.

La recompensa usa como base la curva de XP del **nivel de referencia del contenido**, no solamente el nivel actual del jugador.

### 22.3 Categorías personales de peligro

Una misma criatura puede ser un reto distinto para personajes diferentes.

El servidor clasifica el encuentro para cada jugador, usando la matemática real disponible de HP, daño esperado, defensa, equipo, estado y poderes conocidos por el sistema.

Categorías v1:
- **Trivial**
- **Favorable**
- **Comparable**
- **Peligroso**
- **Abrumador**

La interfaz y el texto muestran únicamente la categoría cualitativa o una frase equivalente. No muestran porcentaje exacto de victoria ni estadísticas ocultas.

Como referencia técnica inicial, puede usarse el margen esperado de supervivencia/derrota del modelo de combate para establecer bandas aproximadas. Los umbrales concretos son afinables de balance sin cambiar estas cinco categorías.

### 22.4 XP de combate

Coeficiente base según la categoría personal del encuentro:

| Categoría | Coeficiente XP |
| --- | ---: |
| Trivial | 2% |
| Favorable | 7% |
| Comparable | 12% |
| Peligroso | 20% |
| Abrumador | 25% |

Referencia:

`XP_combate_bruta = XP_siguiente(nivel_referencia_enemigo) × coeficiente_categoria`

Para impedir saltos extremos de nivel:

`XP_combate = mínimo(XP_combate_bruta, 25% de XP_siguiente(nivel_jugador))`

Después se aplican multiplicadores de cooperación y repetición cuando correspondan.

Consecuencias buscadas:
- un enemigo apropiado suele aportar alrededor de 8–9 victorias comparables por nivel si el jugador solo progresa combatiendo;
- un enemigo muy por debajo del jugador aporta muy poco;
- un enemigo muchísimo más fuerte no puede regalar más de un cuarto de nivel por una sola victoria;
- una build muy poderosa contra cierto enemigo puede verlo como Favorable y recibir menos XP que una build para la que el mismo encuentro sea Comparable.

### 22.5 Primera victoria y variedad de criaturas

La primera victoria significativa de un personaje contra una **familia de criatura** en una región puede otorgar una bonificación única equivalente a **5% de la XP de referencia** de ese contenido.

Esto recompensa descubrir y aprender criaturas nuevas sin convertir cada individuo en una recompensa única.

El Historiador define las familias de criaturas; Jugabilidad asigna su nivel de referencia y balance.

### 22.6 Antifarmeo por repetición

La repetición no deja de dar XP, pero deja de ser la forma óptima de progresar.

Para cada jugador, el servidor observa las **últimas 10 victorias PvE** y cuenta cuántas pertenecen a la misma familia de criatura que acaba de derrotar.

Multiplicador v1:

| Repeticiones de esa familia dentro de las últimas 10 victorias | Multiplicador |
| ---: | ---: |
| 1–3 | 100% |
| 4–5 | 60% |
| 6 o más | 25% |

Esto permite seguir cazando una criatura si el jugador quiere, pero premia variar enemigos, cambiar de zona y explorar.

Cuando la reducción sea relevante, el juego debe comunicarla de forma comprensible, por ejemplo indicando que **esa presa ya enseña poco y explorar otros peligros hará progresar más**. No ocultar completamente el motivo de una caída grande de XP.

### 22.7 XP por exploración y descubrimiento

La progresión no depende exclusivamente de matar.

Un contenido marcado explícitamente puede otorgar XP una sola vez por personaje:

- **descubrimiento significativo:** 5% de la XP de su nivel de referencia;
- **descubrimiento mayor:** 10%;
- **hito narrativo menor:** 10%;
- **hito narrativo importante:** 15%;
- **hito narrativo excepcional:** hasta 25%.

No toda habitación, conversación o uso de `mirar` entrega XP.

La recompensa requiere un estado persistente de descubrimiento/hito para evitar repetirla.

Un Narrador o Historiador puede proponer que un evento sea descubrimiento o hito, pero Jugabilidad valida la categoría de recompensa.

### 22.8 Cooperación y reparto de XP

Jugar acompañado debe ser útil sin duplicar íntegramente la recompensa para todos.

Solo recibe XP de combate quien haya realizado una **participación significativa** durante el encuentro. Estar simplemente presente en la sala no basta.

La participación puede incluir, según las mecánicas disponibles:
- ataque;
- defensa relevante;
- curación;
- protección;
- control;
- apoyo mediante poderes;
- otras acciones que el servidor marque como contribución real.

Multiplicador individual por número de participantes elegibles:

| Participantes | Multiplicador por jugador |
| ---: | ---: |
| 1 | 100% |
| 2 | 80% |
| 3 | 70% |
| 4 o más | 60% |

Cada jugador calcula primero la categoría del encuentro **respecto de su propio personaje**. Por eso un veterano que ayuda contra una criatura débil puede recibir XP Trivial mientras un principiante recibe XP Comparable.

La recompensa individual sigue limitada al **25% de la XP necesaria para el siguiente nivel** antes de aplicar el multiplicador de grupo.

### 22.9 Protección contra power-leveling

La combinación de:
- nivel de referencia del enemigo;
- categoría personal del reto;
- tope del 25% del nivel;
- participación significativa;
- multiplicador de grupo;

debe impedir que acompañar pasivamente a un personaje muy poderoso sea la forma dominante de subir niveles.

Una criatura de nivel bajo derrotada por un veterano conserva su bajo nivel de referencia y por tanto entrega XP mínima al veterano.

Un principiante presente en una pelea muy por encima de su capacidad no puede recibir más del tope individual por una sola victoria.

Si las pruebas reales muestran abuso todavía significativo, Jugabilidad puede añadir un límite adicional de mentoría sin rehacer esta estructura.

### 22.10 PvP y XP

**Derrotar jugadores no entrega XP de progresión en la v1.**

PvP conserva sus propias consecuencias de riesgo, huida, armas y mundo persistente, pero no debe convertirse en una fuente fácilmente explotable de niveles mediante muertes pactadas o repetidas.

### 22.11 Acción `evaluar`

Se aprueba una acción equivalente al clásico `consider/considerar`:

- comando principal: **`evaluar <objetivo>`**;
- la interfaz puede ofrecer **Evaluar** sobre una criatura visible;
- botón y comando representan la misma intención del servidor.

`evaluar` solo funciona sobre un objetivo que el personaje pueda percibir legítimamente.

Devuelve una valoración cualitativa como:
- parece muy inferior a ti;
- parece favorable;
- parece comparable a ti;
- parece peligroso;
- te supera claramente.

Percepción, conocimiento legítimo, equipo visible y observación previa pueden enriquecer la explicación de **por qué** parece peligroso, pero nunca revelan automáticamente:
- HP exacto;
- daño exacto;
- porcentaje de victoria;
- poderes ocultos;
- resistencias secretas;
- información que el personaje no puede conocer.

El Narrador puede reforzar la misma evaluación mediante señales del mundo. `evaluar` organiza la información disponible; no reemplaza leer.

### 22.12 Ejemplos de comportamiento esperado

Con la v1:
- un nivel 10 contra un enemigo Comparable de referencia 10 recibe aproximadamente **34 XP**, alrededor de 12% de su nivel;
- un nivel 50 contra referencia 50 Comparable recibe alrededor de **190 XP**, también cerca de 12%;
- un nivel 99 matando un enemigo trivial de referencia 1 recibe alrededor de **2 XP**;
- dos principiantes contra un encuentro Comparable reciben alrededor de **9.6% de su nivel cada uno** antes de otras bonificaciones;
- tres principiantes reciben alrededor de **8.4% cada uno**;
- repetir veinte victorias seguidas contra la misma familia ronda aproximadamente un nivel completo o menos, mientras una ruta que mezcla combates, descubrimientos e hitos puede alcanzar el nivel con muchas menos repeticiones.

### 22.13 Principio de progresión

**Combatir fortalece al personaje, pero explorar, comprender y variar el riesgo debe ser una ruta competitiva de progreso.**

La estrategia óptima no debe ser permanecer inmóvil esperando el mismo respawn.



## 23. Mapa progresivo y conocimiento cartográfico — v1

**Estado:** APROBADO PARA IMPLEMENTACIÓN.

El mapa del jugador representa **lo que ese personaje conoce legítimamente**, no el mapa completo de producción del mundo.

### 23.1 Estados de un lugar

Cada localización relevante puede estar para un personaje en uno de tres estados:

1. **desconocido**
   - no aparece en el mapa del jugador;
   - no debe dejar huecos, iconos apagados ni pistas visuales que revelen su existencia.

2. **conocido**
   - el personaje recibió información legítima de que el lugar existe;
   - puede mostrarse su nombre o una referencia aproximada cuando el contenido lo permita;
   - conocer un lugar **no significa conocer automáticamente cómo llegar**.

3. **visitado**
   - el personaje estuvo físicamente allí;
   - el lugar puede mostrarse con posición/ruta conforme al conocimiento adquirido.

Entrar legítimamente en una localización la marca como **visitada**.

### 23.2 Estados de una ruta

Las conexiones/rutas se registran por separado:

- **desconocida:** no se muestra;
- **conocida:** el personaje sabe que existe una conexión o dirección general;
- **recorrida:** el personaje atravesó esa ruta y el mapa puede representarla con precisión autorizada.

Atravesar una salida normal marca esa conexión como recorrida.

### 23.3 Rutas y lugares secretos

Una salida oculta, puerta secreta, palabra especial, túnel o ruta condicionada:
- no aparece como botón deshabilitado;
- no aparece como línea vacía en el mapa;
- no se registra hasta que el personaje la descubre legítimamente.

Una vez descubierta, puede pasar a conocida o recorrida según lo que realmente haya ocurrido.

### 23.4 Información recibida de NPCs, objetos o eventos

El Narrador/Historiador pueden marcar contenido que otorgue conocimiento cartográfico.

Ejemplos mecánicos posibles:
- un NPC menciona que existe un lugar → puede pasar de desconocido a conocido;
- un mapa físico legítimo revela una ruta → la ruta puede pasar a conocida;
- el personaje atraviesa la ruta → pasa a recorrida.

El contenido define **qué información se entrega**; Jugabilidad define estos estados.

### 23.5 Chat entre jugadores

Que otro jugador escriba por chat el nombre o ubicación de un lugar **no actualiza automáticamente el mapa**.

El jugador humano puede recordar la conversación y actuar con ella, pero el estado cartográfico persistente solo cambia mediante eventos autorizados por el servidor.

Esto preserva la diferencia entre información social y descubrimiento formal.

### 23.6 Reaparición y desplazamientos especiales

Si el sistema coloca legítimamente al personaje en una localización mediante reaparición u otro traslado autorizado, esa localización pasa a **visitada**, porque el personaje realmente está allí.

Esto no revela automáticamente rutas que no recorrió.

### 23.7 Mapa no es viaje rápido

Tocar una localización del mapa sirve para consultar información conocida.

La v1 **no convierte el mapa en teletransporte o viaje rápido**.

Cualquier sistema futuro de viaje rápido debe aprobarse aparte.

### 23.8 XP y mapa

Descubrir una habitación cualquiera no entrega XP automáticamente.

Solo los lugares/eventos marcados como **descubrimiento significativo o mayor** según la sección 22 conceden XP una vez por personaje.

### 23.9 Persistencia

Los estados de lugares y rutas son persistentes por personaje.

Cerrar sesión, cambiar de dispositivo o reiniciar el servidor no borra el mapa descubierto.

### 23.10 Interfaz

La interfaz puede representar visualmente:
- lugares conocidos;
- lugares visitados;
- rutas conocidas;
- rutas recorridas.

Debe evitar una presentación que permita deducir secretos por ausencia, espacios reservados, numeración, conexiones fantasma o controles deshabilitados.

La ilustración contextual de una ciudad o región es independiente del mapa y no cambia por sí sola el estado cartográfico.

### 23.11 Principio

**El mapa recuerda lo que el personaje ha aprendido del mundo; no le enseña el mundo por adelantado.**


## 24. Ritmo de combate, fatiga, heridas y recuperación — v1

**Estado:** APROBADO PARA PRIMER COMBATE REAL / AFINABLE POR PLAYTEST.

Esta sección cierra los parámetros operativos que faltaban para que Desarrollo pueda implementar el bucle de combate de §20 sin inventar comportamiento.

### 24.1 Rondas semi-automáticas

El combate se resuelve por **rondas autoritativas del servidor**.

Referencia de cadencia v1:
- objetivo inicial: **1 ronda cada ~4 segundos**;
- el valor puede afinarse aproximadamente entre 3–5 segundos después de probar lectura y respuesta en teléfono;
- cambiar la duración de la ronda no cambia las fórmulas de combate.

Al comenzar un combate:
- el personaje queda con **ataque básico automático** como acción por defecto;
- si el jugador no hace nada, los ataques básicos continúan ronda tras ronda;
- antes de resolver la siguiente ronda, el jugador puede enviar **una intervención**;
- esa intervención sustituye la acción básica de esa ronda.

Intervenciones posibles cuando el contexto/servidor las habilita:
- usar un poder;
- huir;
- adoptar una defensa contextual;
- utilizar un objeto cuando el sistema de objetos exista.

Esto permite que un combate rutinario avance con poca intervención, pero hace que una decisión estratégica tenga coste de oportunidad: defenderse, huir o usar una capacidad sustituye el ataque básico de esa ronda.

### 24.2 Defensa contextual dentro de la ronda

Cuando el jugador elige:
- **Esquivar**;
- **Bloquear/desviar**;
- **Resistir**;

esa respuesta se aplica contra el ataque enemigo correspondiente de la siguiente resolución y **sustituye el ataque básico del personaje en esa ronda**.

La interfaz solo presenta defensas que tengan sentido según:
- ataque visible/telegráfico;
- posición;
- equipo;
- estado;
- información que el personaje realmente percibió.

No existe un botón universal de “mejor defensa” y el cliente no calcula cuál conviene.

### 24.3 Costes base de fatiga

Costes v1 antes del modificador por Resistencia de §20.7:

| Acción | Fatiga base |
| --- | ---: |
| Ataque básico físico | 4 |
| Resistir | 3 |
| Bloquear/desviar | 5 |
| Esquivar | 6 |
| Huir | 8 |

Los poderes reciben coste concreto cuando Jugabilidad valide cada poder. Como guía:
- poder rápido: normalmente **6–10**;
- poder fuerte: normalmente **10–15**;
- poder mayor: normalmente **15–25** o una restricción equivalente.

No existe un coste mágico universal.

### 24.4 Efectos exactos de cansancio y agotamiento

**0–69 — operativo**
- sin penalización general por fatiga.

**70–89 — cansado**
- -5 puntos porcentuales a precisión física, esquiva, bloqueo y huida;
- potencia/daño físico final × **0.90**;
- reducción de Resistir disminuye 5 puntos porcentuales, nunca por debajo de 0.

**90–100 — agotado**
- -10 puntos porcentuales a precisión física, esquiva, bloqueo y huida;
- potencia/daño físico final × **0.80**;
- reducción de Resistir disminuye 10 puntos porcentuales, nunca por debajo de 0.

La fatiga no impide por sí sola actuar ni mata al personaje.

Un poder no recibe automáticamente estas penalizaciones si su ejecución no es física. Su regla concreta decide qué estado le afecta.

### 24.5 Heridas — disparador simple

Para la v1 se evita una tabla compleja de críticos.

Después de mitigación, comparar el daño de **un solo impacto** con el HP máximo del objetivo:

| Daño de un solo impacto | Herida mínima provocada |
| --- | --- |
| menos de 20% HPmax | ninguna por daño bruto solamente |
| 20%–34% HPmax | leve |
| 35%–49% HPmax | moderada |
| 50%+ HPmax | grave |

Contenido especial puede declarar una herida explícita solamente cuando Jugabilidad la valide.

Un personaje mantiene como máximo **una herida mecánica principal**. Una herida mayor reemplaza a una menor; heridas iguales no se acumulan indefinidamente.

### 24.6 Efectos de heridas

**Leve**
- fatiga generada × **1.10**.

**Moderada**
- fatiga generada × **1.20**;
- -5 puntos porcentuales a precisión física, esquiva, bloqueo y huida;
- el descanso de campo no puede recuperar HP por encima de **85% del HP máximo**.

**Grave**
- fatiga generada × **1.35**;
- -10 puntos porcentuales a precisión física, esquiva, bloqueo y huida;
- daño/potencia física final × **0.90**;
- el descanso de campo no puede recuperar HP por encima de **65% del HP máximo**.

Las penalizaciones de herida y fatiga pueden coexistir, pero deben mostrarse narrativamente con claridad para que el jugador comprenda por qué su rendimiento empeoró.

### 24.7 Recuperación gradual fuera de combate

Se conserva el principio combinado ya aprobado.

Cuando el personaje está fuera de combate y no realiza esfuerzo intenso:
- recupera aproximadamente **1 punto de fatiga cada 10 segundos**;
- esta recuperación puede calcularse por tiempo transcurrido en servidor;
- no recupera heridas;
- HP no se regenera pasivamente por esta regla.

La recuperación pasiva evita que una pausa breve sea inútil sin convertir esperar en la estrategia principal.

### 24.8 Acción explícita `descansar`

Fuera de combate y cuando el contexto sea seguro, el jugador puede usar:

**`descansar`**

Una acción de descanso v1:
- recupera **10% del HP máximo**;
- reduce fatiga en **25 puntos + 0.2 × (Resistencia - 10)**;
- respeta el límite de recuperación de HP impuesto por una herida moderada/grave;
- puede ser rechazada/interrumpida si existe peligro inmediato.

La interfaz puede ofrecer **Descansar** como acción contextual; botón y comando son la misma intención.

### 24.9 Recuperación segura

Un lugar que Narrativa/Historia marque como punto válido de recuperación segura puede ofrecer una recuperación superior.

Una recuperación segura completa:
- restaura HP al 100%;
- reduce fatiga a 0;
- mejora una herida en **un grado**:
  - grave → moderada;
  - moderada → leve;
  - leve → ninguna.

El contenido decide qué lugares ofrecen esta recuperación; Jugabilidad fija el efecto.

Para evitar spam, una nueva mejora de herida requiere **un nuevo ciclo legítimo de recuperación** definido por el servidor/contenido, no pulsar el mismo botón repetidamente en el mismo instante.

### 24.10 Ataque básico antes del equipamiento definitivo

Mientras el sistema real de armas iniciales todavía no esté integrado, el primer piloto puede usar internamente:

`BaseArma = 10`

como **perfil técnico de ataque básico**.

Esto:
- no inventa un arma canónica;
- no muestra al jugador un objeto inexistente;
- permite probar combate real;
- debe ser sustituido por el valor del equipo real cuando Historiador/Forja/Desarrollo integren armas iniciales.

### 24.11 Validación del piloto de Edran

Con personaje nivel 1, atributos 10 y BaseArma 10, la simulación de referencia produce aproximadamente:

| Criatura | Rondas esperadas para derrotarla | Daño esperado recibido |
| --- | ---: | ---: |
| Mordelinde | ~6 | ~14 HP |
| Espinajo | ~8 | ~32 HP |
| Cornalomo | ~27 | >300 HP |

Interpretación:
- Mordelinde enseña el sistema con riesgo bajo;
- Espinajo obliga a prestar más atención y hace que descansar/huir tengan valor;
- Cornalomo mata claramente al principiante en combate prolongado y por eso sus señales + `evaluar` importan.

Estos son valores medios antes de decisiones defensivas, huida, poderes y variación aleatoria. Se usan para detectar desbalance, no como resultado garantizado.

### 24.12 Principio

**El combate básico avanza solo; intervenir debe ser una decisión real. El desgaste obliga a leer el estado y decidir si continuar, descansar, defenderse o regresar.**


## 25. Resolución de subida de nivel y gasto de progreso — v1

**Estado:** APROBADO PARA IMPLEMENTACIÓN.

Esta sección convierte las reglas de §§19 y 22 en un flujo persistente concreto.

### 25.1 XP acumulada y subida

La XP se acumula de forma persistente.

Cuando la XP acumulada alcanza el requisito del siguiente nivel:
1. se descuenta el requisito correspondiente;
2. el personaje sube un nivel;
3. la XP sobrante **se conserva** hacia el siguiente nivel;
4. se conceden **2 PA**;
5. si el nuevo nivel es múltiplo de 5, se concede **1 PP**;
6. se recalculan competencia general y HP máximo.

Si una sola recompensa alcanza para más de un nivel, el servidor repite el proceso hasta que la XP restante ya no alcance el siguiente requisito o el personaje llegue al nivel 100.

### 25.2 Nivel máximo inicial

La primera etapa tiene tope en **nivel 100**.

Al llegar a 100:
- no se generan niveles 101+;
- la implementación v1 puede dejar de acumular XP de nivel o registrarla únicamente como dato no utilizable si Arquitectura lo necesita;
- no se conceden PA/PP adicionales por XP después del nivel 100.

Una futura expansión de nivel debe aprobarse antes de utilizar XP acumulada más allá del tope.

### 25.3 PA no se distribuyen automáticamente

Los **Puntos de Atributo (PA)** quedan en una reserva del personaje hasta que el jugador decida gastarlos.

- no caducan;
- pueden acumularse durante muchos niveles;
- el juego no elige atributos por el jugador;
- no existe conversión PA ↔ PP.

### 25.4 Gasto de PA

Para aumentar un atributo en +1:
1. consultar su valor actual;
2. consultar el coste de §19;
3. comprobar que existe PA suficiente;
4. mostrar al jugador atributo, valor actual, nuevo valor y coste;
5. confirmar el gasto;
6. descontar PA y aplicar +1 de forma atómica.

El gasto de PA:
- solo puede hacerse **fuera de combate**;
- no requiere regresar obligatoriamente a la ciudad;
- no puede dejar PA negativos;
- no puede ejecutarse dos veces sobre el mismo saldo por solicitudes concurrentes.

### 25.5 Confirmación y errores de niños

La interfaz debe exigir una confirmación clara antes de gastar PA, especialmente en móvil.

La v1 no incluye un botón libre de “deshacer” después de confirmar.

Sin embargo, una distribución imperfecta no debe arruinar el personaje porque:
- existe competencia general por nivel;
- la curva de coste favorece diversificación;
- el contenido común debe admitir perfiles razonables/casuales.

Un sistema futuro de reespecialización puede existir, pero deberá definirse aparte; no debe inventarse ahora.

### 25.6 Efecto inmediato del nivel sobre HP

Al subir de nivel se recalcula `HPmax`.

El personaje **no se cura completamente por subir de nivel**.

Si el HP máximo aumenta, el HP actual aumenta únicamente por la misma diferencia positiva:

`HP_actual_nuevo = HP_actual_anterior + (HPmax_nuevo - HPmax_anterior)`

sin superar el nuevo HP máximo.

Ejemplo: si pasa de 100/100 a un máximo de 102, queda aproximadamente 102/102 si estaba sano, o 62/102 si estaba en 60/100.

Esto evita usar una subida de nivel como curación completa artificial.

### 25.7 Gasto de PA y HP derivado

Si aumentar Resistencia o Voluntad incrementa HP máximo mediante §20.3, se aplica la misma regla:
- aumenta HP actual por la diferencia positiva del máximo;
- no produce curación completa adicional.

### 25.8 PP

Los **Puntos de Poder (PP)**:
- se conceden en niveles 5, 10, 15... 100;
- pueden acumularse;
- no caducan;
- no se convierten en PA.

Comprar/desbloquear un poder solo será posible cuando exista contenido de poder validado. La interfaz puede mostrar PP disponibles antes, pero no debe ofrecer poderes ficticios.

### 25.9 Notificación de progreso

Al subir de nivel, el jugador debe recibir una notificación breve y persistente en la sesión que indique:
- nuevo nivel;
- PA obtenidos;
- PP obtenido cuando corresponda.

No mostrar automáticamente una ventana obligatoria de distribución en medio de combate o lectura. El jugador decide cuándo abrir Personaje y gastar sus PA.

### 25.10 Principio

**Subir de nivel entrega posibilidades; no toma decisiones por el jugador ni funciona como curación total.**


## 26. Cooperación y comunicación local — v1

**Estado:** APROBADO PARA PRIMER MULTIJUGADOR.

La primera versión no necesita un sistema complejo de guilds/parties para permitir que varios jugadores exploren y peleen juntos.

### 26.1 Chat local como canal inicial

La comunicación v1 entre jugadores es **local a la sala/ubicación actual**.

Comando explícito:

`decir <texto>`

Reglas:
- solo jugadores presentes en la misma sala reciben el mensaje;
- un comando desconocido nunca se convierte automáticamente en chat;
- `hablar <npc>` pertenece a conversación con NPC y es una intención diferente;
- la interfaz debe distinguir visualmente acción/comando de chat.

El chat global, susurros, grupos permanentes y otros canales pueden añadirse más adelante; no son requisito del primer bucle jugable.

### 26.2 Cooperar sin party formal

Para la v1, dos o más jugadores en la misma sala pueden cooperar contra una criatura **sin crear previamente un grupo formal**.

Un jugador entra como participante del encuentro cuando realiza una contribución significativa aprobada por §22.8, por ejemplo:
- atacar al mismo objetivo;
- defender/proteger de forma relevante;
- curar;
- controlar;
- usar un poder de apoyo.

Estar mirando o simplemente compartir sala no da XP.

### 26.3 Unirse a un combate existente

Si una criatura ya está combatiendo:
- otro jugador de la misma sala puede usar **Atacar <objetivo>**;
- pasa a formar parte del mismo encuentro;
- no se crea una copia privada de la criatura;
- HP/estado de la criatura son autoritativos y compartidos por quienes participan.

Esto conserva el mundo compartido y permite cooperación espontánea.

### 26.4 Objetivo del enemigo

Como comportamiento base para criaturas comunes:
- la criatura mantiene como objetivo principal al jugador que inició/agredió el encuentro;
- puede cambiar de objetivo si ese jugador huye, muere, deja de ser válido o una capacidad/conducta concreta lo justifica;
- el contenido especial puede definir conducta distinta.

No se introduce todavía una barra compleja de amenaza/aggro.

### 26.5 Movimiento durante combate

Un personaje involucrado en combate **no puede usar movimiento cardinal normal para escapar gratis**.

Si intenta salir mientras sigue comprometido:
- el servidor debe exigir la acción **Huir**;
- Huir usa §20.10 y §24;
- tras una huida exitosa, el personaje puede quedar en la salida/destino que el servidor determine válidamente;
- una huida fallida consume la intervención de esa ronda.

Esto evita que escribir `norte` sustituya el sistema de huida.

### 26.6 Fin del encuentro

El encuentro termina para un jugador cuando:
- la criatura es derrotada;
- el jugador muere;
- logra huir;
- otra regla explícita del contenido termina el combate.

La derrota de la criatura distribuye XP individualmente según §22:
- categoría personal;
- participación;
- repetición;
- número de participantes.

No existe una bolsa de XP que el primer jugador pueda apropiarse completa.

### 26.7 Jugador fuerte ayudando a principiante

La cooperación no iguala automáticamente recompensas.

Cada participante calcula su categoría personal:
- un veterano contra criatura pequeña puede recibir recompensa Trivial;
- un principiante contra la misma criatura puede recibir Comparable/Favorable;
- ambos deben haber participado significativamente.

Por tanto, ayudar es posible sin convertir matar criaturas débiles para otro jugador en el método dominante de power-leveling.

### 26.8 Principio

**Compartir sala permite colaborar; compartir sala no entrega progreso. Cooperar requiere actuar.**

## Investigación disponible para Jugabilidad — capacidades HTML y comandos

**ESTADO: INVESTIGACIÓN CONSUMIDA — la dirección híbrida HTML/Telnet, inspección, evaluación de peligro y mapa progresivo ya tienen criterios v1; las ampliaciones futuras se decidirán cuando aparezcan nuevas necesidades.**

El Investigador Técnico completó `vintage-telnet/RESEARCH_SPANISH_COMMANDS_WEB_UI.md`. El Diseñador de Jugabilidad debe leerla antes de cerrar las reglas de exploración, interacción, combate, inventario, mapa y controles.

La investigación demuestra que Vintage Telnet no está limitado a una terminal Telnet pura. Clientes/juegos MUD modernos como Written Realms, Nexus/Iron Realms y Mudlet conservan texto y comandos como núcleo, pero aprovechan HTML/interfaz moderna para añadir mapa, brújula, inventario, barras de estado, objetos/personajes interactivos, botones de habilidades, chat separado y adaptación táctil.

### Capacidad especialmente importante

Una misma acción puede tener dos entradas sin crear dos juegos distintos:

- el jugador escribe `norte`; o
- toca un botón **Norte**.

Ambas pueden convertirse en la misma acción canónica validada por el servidor. El navegador presenta y solicita; el servidor continúa siendo autoridad del personaje y del mundo.

Esto también puede aplicarse a mirar, inventario, tomar, hablar, atacar, huir, habilidades y otras acciones que Jugabilidad apruebe.

### Preguntas que Jugabilidad debe decidir aprovechando estas capacidades

- ¿Qué acciones deben seguir premiando que el jugador descubra/escriba un comando?
- ¿Qué acciones frecuentes deben tener botón táctil para evitar fricción innecesaria?
- ¿Qué comandos y abreviaciones en español forman el vocabulario inicial?
- ¿El mapa es interactivo? ¿Qué permite tocar y qué permanece oculto?
- ¿Los objetos/personajes visibles pueden tocarse para mostrar acciones contextuales?
- ¿Qué información de vida, recursos, equipo y combate merece representación visual?
- ¿Qué acciones de combate aparecen como botones y cuáles requieren comando?
- ¿Cómo se evita que los botones revelen secretos que el jugador todavía no descubrió?
- ¿Cómo debe funcionar un equivalente de `considerar/evaluar` para comunicar peligro?
- ¿Qué interfaz necesita teléfono/iPad frente a computadora sin cambiar las reglas del mundo?

### Principio técnico propuesto para evaluación

**Texto/comandos como núcleo + HTML como ayuda de orientación e interacción + servidor como única autoridad.**

Esto es una posibilidad técnica investigada, no una decisión aprobada. Jugabilidad debe decidir qué partes mejoran realmente la experiencia de Vintage Telnet. Arquitecto y Desarrollo decidirán después cómo implementar las reglas aprobadas.

## Cómo debe trabajar el Historiador con este documento

El Historiador debe usar estos principios como límites para crear contenido.

Puede proponer libremente clases, magias, poderes, enemigos, zonas, objetos, armas, personajes y aventuras siempre que no contradigan los criterios confirmados.

Para una zona o contenido que necesite un criterio nuevo, debe indicar claramente:

- qué propone;
- qué necesidad de jugabilidad aparece;
- qué comportamiento necesita que el sistema permita.

Jugabilidad definirá con Javier el criterio general necesario. Después el Historiador podrá continuar desarrollando el contenido dentro de ese criterio.

## Decisiones mecánicas todavía abiertas

Siguen sin fijarse, entre otras:

- valores concretos de armas y armaduras;
- críticos y otros efectos avanzados de combate;
- balance de poderes concretos propuestos por el Historiador;
- reglas exactas de transferencia o recuperación de armas perdidas;
- frecuencia y rareza de recompensas físicas.

Que algo esté abierto significa que **no debe inventarse como regla definitiva para poder implementar**.

## Regla para otros agentes

Antes de implementar una mecánica de Vintage Telnet, revisar este documento.

Si un criterio está confirmado, debe respetarse. Si está pendiente, debe devolverse para decisión. Una propuesta no se convierte en regla hasta que se aprueba y se incorpora aquí.

---

**Estado:** matemática v1 aprobada y lista para implementación; quedan contenido concreto y ajustes de balance por pruebas reales.  
**Juego:** Vintage Telnet  
**Fuente de verdad de jugabilidad:** `vintage-telnet/GAMEPLAY.md`


## Handoff del Narrador — mapa conceptual vs. mapa descubierto

**Origen:** VT-ART-001 en \`NARRATIVE.md\`.  
**Estado:** PROPUESTA PARA JUGABILIDAD.

Narrativa recomienda separar dos objetos que cumplen funciones distintas:

- **Mapa conceptual/de producción:** puede servir al equipo para comprender la relación general entre regiones y Vaisgard, siempre sujeto al canon del Historiador.
- **Mapa del jugador:** debe representar únicamente conocimiento que el personaje pueda poseer legítimamente y no revelar de antemano lugares, rutas, ruinas, mazmorras, peligros o secretos no descubiertos.

El mapa jugable puede crecer conforme el personaje explora, recibe información legítima o utiliza futuros objetos/capacidades que Jugabilidad apruebe. Que otro jugador mencione un lugar por chat no debería convertir automáticamente esa información en una ubicación exacta del mapa.

**RESUELTO POR JUGABILIDAD:** la sección 23 define estados de lugares/rutas, persistencia y qué eventos actualizan el mapa sin destruir la exploración.
