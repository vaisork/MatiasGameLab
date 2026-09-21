# Vintage Telnet — Investigación: comandos en español e interfaz web aumentada

**Fecha:** 2026-09-20
**HEAD revisado:** 3cddf66d477542ef974f7e761107ec8f8f63671e
**Estado:** INVESTIGADO — NO IMPLEMENTADO
**Consumidores:** Arquitecto, Jugabilidad, Narrador, Integrador HTML y futuro Desarrollador de Servidor.

## PROBLEMA

Vintage Telnet quiere conservar el núcleo de un MUD textual, pero:
- sus comandos serán principalmente en español;
- se jugará desde teléfono, iPad y computadora;
- el HTML puede ayudar visualmente con mapa, botones, estado, inventario y acciones;
- el navegador no debe convertirse en autoridad del personaje ni duplicar las reglas del servidor.

Hay que entender cómo funcionan los parsers de comandos y cómo juegos modernos conservan texto/comandos mientras añaden una interfaz gráfica útil.

## ESTADO ACTUAL

GAMEPLAY.md ya confirma movimiento cardinal, mapa general con descubrimiento, mundo persistente, multijugador textual y combate semi-automático.

vintage-telnet.html es hoy una pantalla de acceso “En construcción”; todavía no existe conexión al servidor ni interfaz jugable.

No hay todavía un parser, protocolo cliente-servidor ni servidor implementados en el repositorio.

## CÓMO FUNCIONA REALMENTE UN SISTEMA DE COMANDOS

### 1. No hace falta comprender español libre como una IA

Los MUD suelen usar un vocabulario controlado. El servidor intenta reconocer primero un comando y después interpreta el resto como argumentos.

Ejemplos conceptuales:
- mirar
- mirar puerta
- tomar espada
- atacar rata
- dar espada a Matías
- usar llave en puerta

Un parser sencillo puede trabajar como:
**VERBO + OBJETO + complementos opcionales**.

Los parsers más avanzados de aventura añaden objeto directo, preposición y objeto indirecto, además de preguntas de desambiguación.

### 2. En español conviene tener un verbo canónico y varios alias

Internamente puede existir una sola acción MIRAR aunque el jugador escriba:
- mirar
- mira
- observar
- examinar
- m

Y una sola acción TOMAR aunque acepte:
- tomar
- toma
- coger
- recoger

No conviene intentar aceptar cualquier conjugación del idioma desde el primer día. Es más sólido mantener una tabla explícita de alias aprobados.

### 3. Los objetos también necesitan alias

Una entidad puede tener:
- nombre mostrado: “espada oxidada”
- identificador interno: sword_rusted_001
- palabras reconocibles: espada, oxidada

El servidor resuelve “tomar espada” contra objetos visibles/accesibles en el contexto actual.

### 4. El contexto reduce muchísimo la complejidad

Si hay una espada en la habitación y ninguna en inventario, “tomar espada” es inequívoco.

Si hay dos espadas, el servidor no debe adivinar peligrosamente. Puede responder:
“¿Cuál espada? 1) espada oxidada 2) espada corta”.

Evennia demuestra un patrón similar con multimatches y objetivos numerados.

### 5. Movimiento puede ser comando aunque visualmente sea botón

Un botón NORTE en HTML debería enviar exactamente la misma intención que escribir:
- norte
- n

Así solo existe una regla de movimiento en el servidor.

Lo mismo puede aplicarse a:
- mirar;
- inventario;
- huir;
- atacar;
- habilidades;
- recoger;
- hablar.

### 6. Los errores deben enseñar el vocabulario

Mala respuesta:
“Comando inválido.”

Mejor patrón:
“No entiendo ‘cojer’. ¿Quisiste decir ‘coger’ o ‘tomar’?”

O:
“No puedes ‘tomar dragón’. Puedes: mirar dragón / considerar dragón / atacar dragón.”

Esto hace que el parser sea parte del aprendizaje sin exigir memorizar un manual.

### 7. Los comandos disponibles pueden depender del contexto

Evennia utiliza conjuntos de comandos que pueden variar según personaje, ubicación u objetos. Para Vintage Telnet esto abre una posibilidad técnica interesante: no es necesario que todas las acciones existan en todas partes.

Ejemplo conceptual: una puerta podría hacer disponible ABRIR; una fuente podría permitir BEBER; un NPC podría permitir HABLAR. Esto debe diseñarse con cuidado para que el vocabulario siga siendo predecible.

## PARTICULARIDADES DEL ESPAÑOL

### Acentos
Conviene que los comandos no fallen por acentos:
- examinar / examinár no debería ser un problema de teclado;
- dirección “oeste” no requiere acento;
- términos con tilde deberían poder normalizarse para matching.

La salida al jugador sí debe conservar ortografía correcta.

### Mayúsculas
Los comandos deberían ser insensibles a mayúsculas/minúsculas.

### Artículos
Sería útil tolerar artículos comunes sin convertirlos en parte del nombre:
- tomar espada
- tomar la espada

### Preposiciones
Un subconjunto pequeño y explícito basta inicialmente:
- dar X a Y
- usar X en/con Y
- hablar con Y
- mirar a Y

### Pronombres y lenguaje natural completo
“Dásela a él” exige resolver referentes previos y morfología. No es necesario para un primer sistema sólido. Puede añadirse después si aporta valor.

## VOCABULARIO INICIAL A EVALUAR CON JUGABILIDAD

No es una lista aprobada. Es una familia mínima razonable para pruebas:

**Orientación:** norte/n, sur/s, este/e, oeste/o, arriba, abajo, salidas, mirar.

**Objetos:** tomar/recoger, dejar/soltar, inventario/i, usar, equipar, quitar.

**Interacción:** mirar/examinar, hablar, decir, dar.

**Riesgo/combate:** considerar/evaluar, atacar, huir, estado.

**Sistema:** ayuda, comandos.

La cantidad visible al principiante debería ser pequeña aunque internamente existan más acciones.

## JUEGOS/CLIENTES ACTUALES QUE NO SON “TELNET PURO”

### Written Realms

Es el ejemplo web más cercano a la dirección propuesta.

Su documentación actual describe una “augmented text interface”: el texto desplazándose sigue siendo el registro de lo ocurrido, pero la interfaz añade paneles, botones, palabras interactivas y mapa.

En escritorio:
- salida textual central;
- campo de comandos;
- mapa;
- estado/vitales;
- inventario/equipo;
- información de habitación;
- listas contextuales;
- botones de habilidades durante combate.

En móvil:
- controles inferiores separan Look, Info, Type y Menu;
- el mapa puede ampliarse;
- las salidas se muestran como botones;
- tocar personajes/objetos abre acciones contextuales.

Punto arquitectónico especialmente valioso: muchas acciones visuales emiten los mismos comandos que el jugador podría escribir. El mapa adyacente mueve al jugador; no es fast travel.

### Iron Realms Nexus / Achaea

Nexus es el cliente oficial moderno de los MUD de Iron Realms y funciona en navegador y aplicaciones.

Incluye:
- ventana principal de texto;
- mapa gráfico;
- inventario;
- comunicaciones separadas;
- layouts redimensionables;
- indicadores;
- aliases, keybindings y triggers;
- navegación táctil por brújula en móvil;
- diseño adaptable según dispositivo.

También soporta datos estructurados del juego mediante GMCP para inventario, salud, habitaciones y otros estados.

Esto demuestra que un MUD puede conservar comandos y texto mientras el cliente presenta estado estructurado visualmente.

### Mudlet

No es un juego sino un cliente MUD moderno. Es relevante porque muestra la evolución de la terminal pura.

Puede presentar:
- mapa;
- chat separado;
- barras de salud;
- botones que ejecutan comandos;
- menús;
- interfaces personalizadas.

Su UI base para jugadores nuevos puede construirse a partir de datos que el juego envía.

## PATRÓN ARQUITECTÓNICO RECOMENDADO PARA VINTAGE TELNET

**Una acción, dos formas de introducirla.**

Ejemplo:
Jugador escribe:
> norte

o toca:
[NORTE]

Ambos producen la misma intención hacia el servidor:
MOVE north

El servidor comprueba si existe salida, si el personaje puede moverse, actualiza posición persistente y devuelve el resultado.

El HTML solo representa lo que el servidor confirmó.

Este patrón evita tener:
- “reglas de botones” por un lado;
- “reglas de comandos” por otro.

## HTML: QUÉ PODRÍA SER VISUAL SIN DEJAR DE SER UN MUD

Una dirección prometedora para evaluación es mantener el texto como centro y añadir:

1. **Mapa descubierto** — solo habitaciones/rutas que el servidor autorice a mostrar.
2. **Brújula/salidas** — botones N/S/E/O para móvil.
3. **Barra de estado** — vida y recursos ya conocidos por el jugador.
4. **Inventario** — panel visual sincronizado desde servidor.
5. **Objetos/personajes presentes** — nombres clicables que abran acciones válidas.
6. **Acciones contextuales** — Mirar, Hablar, Tomar, Atacar, etc.
7. **Combate** — botones para habilidades disponibles y Huír, manteniendo el registro textual del combate.
8. **Chat** — visualmente separado del flujo de combate si resulta necesario.
9. **Campo de comando siempre disponible** — el jugador avanzado nunca queda limitado por botones.

No todo debe estar visible simultáneamente en teléfono. Written Realms y Nexus muestran que el layout puede cambiar por dispositivo.

## DATO ESTRUCTURADO EN VEZ DE “RASPAR” TEXTO

Para nuestro propio cliente HTML no conviene deducir la vida o las salidas leyendo frases impresas por el servidor.

El servidor debería poder enviar dos tipos de información:
1. texto narrativo para el registro;
2. eventos/estado estructurado para actualizar UI.

Ejemplo conceptual, NO protocolo aprobado:

Evento textual:
“El camino continúa hacia el norte.”

Estado:
room_id, exits=[north], hp=..., inventory=...

El cliente dibuja la brújula/mapa desde estado autorizado por servidor. No inventa salidas ni modifica vida localmente.

Nexus/GMCP demuestra el valor de separar datos estructurados del texto que ve el jugador.

## VENTAJAS

- conserva la identidad Telnet/MUD;
- escribir comandos sigue siendo una habilidad real;
- teléfono/iPad se vuelven cómodos;
- principiantes pueden descubrir acciones tocando;
- jugadores avanzados pueden ser rápidos escribiendo;
- accesibilidad: varias formas de ejecutar la misma acción;
- el servidor conserva una sola lógica;
- la UI puede crecer sin cambiar las reglas del mundo.

## RIESGOS

### Demasiados botones
Si cada verbo se convierte en botón permanente, termina pareciendo un RPG web normal y pierde el placer de descubrir/escribir.

**Mitigación:** controles visuales para acciones frecuentes y contextuales; comandos para profundidad.

### El mapa revela secretos
Un mapa generado automáticamente podría descubrir habitaciones ocultas.

**Mitigación:** el servidor decide qué nodos y salidas están descubiertos.

### Cliente desincronizado
La UI podría mostrar vida, inventario o posición antigua después de reconectar.

**Mitigación:** al reconectar, el servidor envía snapshot autorizado del estado.

### Parser demasiado ambicioso
Intentar entender español libre completo puede consumir mucho desarrollo y generar resultados impredecibles.

**Mitigación:** vocabulario controlado + alias + mensajes útiles + expansión gradual.

## SEGURIDAD

El cliente nunca debe poder decir “mi vida ahora es 100”, “tengo esta espada” o “estoy en esta habitación” como hechos autoritativos.

Los botones solo solicitan acciones. El servidor valida permisos, posición, objetivos, inventario, combate y cambios persistentes.

Los identificadores internos sensibles o secretos del mundo tampoco deberían enviarse al navegador antes de que el jugador pueda conocerlos.

## PRUEBA PROPUESTA

Antes de construir la interfaz completa, una microprueba debería contener:
- 5–10 habitaciones;
- comandos españoles: mirar, norte/sur/este/oeste, tomar, inventario, atacar, huir;
- alias cortos n/s/e/o/i;
- una habitación con dos objetos del mismo tipo para probar ambigüedad;
- un mapa HTML pequeño;
- botones N/S/E/O;
- un objeto clicable;
- campo de texto de comandos;
- ambos caminos enviando exactamente las mismas acciones al servidor.

Criterio clave: realizar una acción por botón y por texto debe producir el mismo cambio autorizado del mundo.

## INSTRUCCIONES PARA DESARROLLO

Todavía no implementar hasta decisión del Arquitecto/Jugabilidad.

Cuando se autorice un prototipo:
1. definir primero el contrato de acción servidor-cliente;
2. hacer que el parser español traduzca texto a acciones canónicas;
3. hacer que botones produzcan esas mismas acciones canónicas;
4. ejecutar toda validación en servidor;
5. devolver texto + estado/eventos estructurados;
6. renderizar la UI desde el estado recibido;
7. probar reconexión y resincronización.

## DECISIONES PARA JUGABILIDAD

Jugabilidad debe decidir:
- vocabulario inicial oficial;
- alias permitidos;
- si existirá CONSIDERAR/EVALUAR;
- cuánto puede revelar una acción contextual;
- qué información de combate/estado se muestra;
- si pulsar un enemigo ofrece ATACAR inmediatamente;
- qué partes del mapa se muestran y cuándo.

## DECISIONES PARA NARRADOR/HISTORIADOR

- qué acciones especiales pueden descubrirse mediante texto;
- qué detalles de habitación son interactivos;
- qué salidas o lugares permanecen ocultos;
- cómo las descripciones sugieren verbos sin mostrar siempre un botón;
- qué información del mundo debe aprenderse explorando.

## FUENTES CONSULTADAS

- Written Realms, Interface and Commands: https://docs.writtenrealms.com/playing/interface-and-commands/
- Written Realms, First Ten Minutes: https://docs.writtenrealms.com/playing/first-ten-minutes/
- Written Realms, Exploring and Interacting: https://docs.writtenrealms.com/playing/exploring-and-interacting/
- Written Realms: https://writtenrealms.com/home
- Iron Realms, Nexus Client: https://www.ironrealms.com/the-nexus-client/
- Achaea, clientes/Nexus: https://www.achaea.com/game-help?what=clients-mud-clients-telnet-clients
- Mudlet, introducción/UI: https://wiki.mudlet.org/w/Special%3AMyLanguage/Manual%3AIntroduction
- Mudlet, User Interface: https://wiki.mudlet.org/w/Manual%3AMudlet_User_Interface
- Evennia, command parser: https://www.evennia.com/docs/latest/api/evennia.commands.cmdparser.html
- Evennia, Commands: https://www.evennia.com/docs/2.x/Components/Commands.html
- Referencia histórica de parser tipo Infocom: https://www.ifwiki.org/Infocom-type_parser

## CONCLUSIÓN

Vintage Telnet no necesita elegir entre “Telnet puro” y “RPG web gráfico”.

Existe una tercera vía ya probada: **texto y comandos como núcleo + HTML como instrumento de orientación y acceso**.

La interfaz puede enseñar mapa, brújula, inventario, salud y acciones contextuales mientras el jugador conserva una línea de comandos completa. Técnicamente, la clave es que escribir y tocar sean dos entradas hacia la misma acción validada por el servidor.

Para español, la opción inicial más sólida no es un parser de lenguaje natural ilimitado. Es un parser predecible de verbos canónicos, alias, objetos contextuales, artículos/preposiciones tolerados y buenas preguntas de desambiguación. Puede crecer después sin obligar a reconstruir el juego.
