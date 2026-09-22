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

Se contempla comunicación contextual cuando jugadores se encuentran. También puede existir un chat general; su forma exacta permanece pendiente.

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

La fatiga tendrá una **barra/valor visible** y también estados o señales narrativas comprensibles. Resistencia influirá en la relación del personaje con la fatiga, pero la fórmula exacta permanece pendiente.

Una fatiga elevada no provoca automáticamente derrota. Debe afectar de manera comprensible la capacidad de mantener determinadas acciones, su coste o eficacia, favoreciendo cambios de estrategia.

La recuperación de fatiga será **combinada**:
1. existe recuperación gradual cuando cesa el esfuerzo que la genera;
2. una acción explícita de descanso permite una recuperación más rápida o eficaz.

Los ritmos, condiciones, interrupciones y cantidades exactas de recuperación todavía no están definidos.

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


## Investigación disponible para Jugabilidad — capacidades HTML y comandos

**ESTADO: INVESTIGACIÓN CONSUMIDA PARCIALMENTE — la dirección híbrida HTML/Telnet ya está confirmada; quedan decisiones específicas por cerrar.**

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
- efectos exactos de cada herida y de los estados de fatiga tras pruebas reales;
- funcionamiento técnico y reglas finales de los canales de chat;
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

**NECESIDAD DE JUGABILIDAD:** definir más adelante qué estados de conocimiento cartográfico existen, qué acciones actualizan el mapa y qué información puede mostrarse sin destruir la exploración. Esta decisión no bloquea la implementación del bucle jugable inicial.
