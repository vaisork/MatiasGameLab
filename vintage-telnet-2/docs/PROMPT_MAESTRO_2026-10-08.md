# Vintage Telnet 2 — Prompt Maestro, versión pública 2026-10-08

Fuente: `Vintage_Telnet_Prompt_Actualizado.pdf`, entregado por Javier, 57 páginas.
SHA-256 del PDF fuente: `c9adf01be33a1a4affa2f93958fb756643dedc82d2eff3f7e96df937b9eefbc6`.

Transcripción de texto; se omiten portada/datos de acceso. El PDF original no se publica porque contiene información sensible. Esta versión conserva la visión, no autoriza despliegues ni reactiva tareas pausadas.

Las instrucciones posteriores de Javier y `DECISIONES_VIGENTES.md` prevalecen sobre aspiraciones del prompt. En particular, bestiario 3D y animaciones siguen fuera del alcance vigente. **El roster definitivo actual es Juramentado, Arcano, Sombra y Artífice; Vigía e Invocador están superseded y no deben implementarse.** No convertir las propuestas del documento en tareas aprobadas automáticamente.

## Principios

- LA LECTURA ES EL MUNDO.
- EL 3D LO MATERIALIZA.
- EL SERVIDOR DECIDE QUÉ ES VERDAD.
- EL JUGADOR DESCUBRE EL RESTO.

## Tensiones pendientes de Dirección/Arquitectura

- UI moderna/colorida frente a 3D sobrio/contenido.
- Layout mobile-first frente a aprovechar espacio adicional en escritorio.

Esta migración registra ambas tensiones sin resolverlas ni cambiar la interfaz.

## Texto del documento fuente

1. ENCARGO Y PANTALLA VIVA
[Datos de acceso omitidos de la versión pública.]
El corazón del juego es la pantalla viva estilo vintage Sí. La idea de esa pantalla de lectura
sería algo así:
La pantalla debe sentirse como una terminal vieja viva, no como una caja moderna
disfrazada.
Debe dar la sensación de que estás viendo un monitor antiguo de fósforo, donde la historia va
apareciendo poco a poco, como si el mundo se estuviera escribiendo frente a ti.
Sensación visual general
El fondo no sería negro puro y plano, sino un negro verdoso o carbón muy oscuro, con una
ligera textura de pantalla vieja.
El texto principal se vería en un tono verde fósforo, ámbar tenue o marfil verdoso, como los
monitores antiguos, pero suficientemente limpio para que no canse la vista.
No debería verse “retro caricatura”, sino retro elegante:
- un brillo muy sutil en las letras;
- una leve vibración o suavidad en el contorno;
- una sensación de pantalla encendida;
- un poco de “scanline” muy discreta;
- y quizá un parpadeo suave en el cursor.
Cómo se ve el texto
La historia avanza en un bloque central grande, como si fuera una consola antigua donde van
apareciendo las líneas.
Por ejemplo:
- primero aparece el nombre del lugar;
- luego una línea de separador simple;
- después el texto descriptivo;
- abajo van apareciendo eventos, acciones, respuestas del mundo y combate.
El texto no debe sentirse como un chat.
Debe sentirse como una crónica en vivo.
Algo como:
- descripción del entorno;
- lo que haces;
- lo que responde el mundo;
- lo que ves;
- lo que escuchas;
- lo que cambia.
Cada nueva línea entra como si la terminal la estuviera imprimiendo.


Actualizado · 04 octubre 2026
3
No demasiado lento, para no desesperar, pero sí con una pequeña sensación de “salida en
tiempo real”.
Estructura visual de esa zona
La imagino así:
Encabezado pequeño
Arriba, una línea compacta con cosas como:
- nombre del lugar,
- región,
- hora del día,
- clima.
Todo en estilo terminal, sobrio, con separadores simples.
Ejemplo visual mental:
[ Khariel ] [ Atardecer ] [ Lluvia ligera ]
Nada muy grande.
La prioridad no es el encabezado, sino la lectura.
Ventana principal de lectura
El cuerpo central ocupa la mayor parte de la pantalla.
Es como una gran consola de historia.
Ahí aparecen:
- la descripción del lugar;
- observaciones del clima;
- comentarios de gente o fauna;
- resultados de explorar;
- encuentros;
- combate;
- consecuencias.
Las líneas más recientes quedan abajo, pero sin perder el contexto narrativo.
Debe sentirse entre una bitácora de viaje y una terminal aventurera.
Cursor vivo
Al final de la última línea, puede haber un pequeño cursor:
_ o █
Eso le da mucha vida.
Hace sentir que la historia sigue en marcha y que el sistema está “esperando tu siguiente
decisión”.


Actualizado · 04 octubre 2026
4
Jerarquía del texto
No todo debe verse igual.
Descripción principal
Más limpia y legible.
Es el cuerpo narrativo.
Acciones del jugador
Podrían verse levemente destacadas, por ejemplo:
- con un símbolo inicial >
- o con un tono apenas distinto.
Ejemplo:
> Avanzas hacia el sendero de piedra.
Respuestas del mundo
Se muestran como continuación natural.
Ejemplo:
La bruma se abre apenas y deja ver las raíces negras del claro.
Mensajes importantes
Como descubrimientos, pistas, peligro o combate, pueden resaltarse ligeramente:
- con un tono más brillante;
- con una palabra clave;
- o con pequeños prefijos.
Ejemplo:
[Rastro] Encuentras marcas recientes en el barro.
[Peligro] El silencio del sendero cambia de golpe.
Combate
En combate, la terminal sigue siendo la misma, pero el tono cambia:
- más tensión;
- líneas más cortas;
- acciones y resultados más inmediatos.
Ejemplo:
[Mordelinde] prepara un salto corto.
> Te cubres.
El golpe roza tu hombro y pierdes estabilidad.
Cómo debe sentirse al leer
La sensación debe ser:


Actualizado · 04 octubre 2026
5
- íntima;
- inmersiva;
- un poco nostálgica;
- clara;
- absorbente.
Debe invitar a quedarse leyendo.
No como una hoja llena de texto, sino como si el mundo se estuviera revelando poco a poco.
La persona debe sentir:
“estoy leyendo una aventura viva en una terminal antigua”.
Relación con el arte
Aunque haya ilustración en la pantalla, la terminal de lectura sigue siendo el corazón del
juego.
La imagen da contexto visual, pero esta zona de lectura es donde:
- el mundo respira,
- el clima se siente,
- la gente comenta,
- los rumores viven,
- y la historia realmente ocurre.
Por eso debe tener mucha personalidad.
Detalles pequeños que la harían especial
- un leve sonido imaginario de terminal, aunque no necesariamente real;
- un pequeño scroll suave cuando entra texto nuevo;
- un separador sencillo entre bloques narrativos;
- parpadeo mínimo del cursor;
- transición discreta entre exploración y combate;
- posibilidad de releer unas cuantas líneas anteriores sin perder claridad.
En una frase
La pantalla de lectura de Vintage Telnet debería verse como:
una bitácora de aventura corriendo dentro de una terminal antigua, elegante, viva y
atmosférica, donde cada línea que aparece hace sentir que el mundo continúa respirando
frente al jugador.
Permisos, subagentes y pruebas
pideme todos los permisos para realizarlo, usa sub agentes para que cada uno realice tareas
especificas, puedo dejarte los permisos para trabajar y has pruebas del juego hasta que
consideres que es un juego digno de jugar.


Actualizado · 04 octubre 2026
6
2. VISIÓN DEL JUEGO Y EXPERIENCIA DE
VIAJE
Construye Vintage Telnet, un RPG de exploración textual para navegador y celular, inspirado
en la sensación de los MUD/Telnet clásicos pero presentado con una interfaz moderna, arte
ilustrado y un mundo persistente que debe sentirse vivo incluso cuando gran parte de la
experiencia ocurre mediante texto.
El juego debe sentirse como un mundo que existe aunque el jugador no esté mirando. Las
personas se mueven, los viajeros cambian de lugar, la actividad de los pueblos varía según la
hora, el clima modifica cómo se describe cada zona, los animales aparecen y desaparecen,
las criaturas dejan rastros y algunas esconden secretos que solo se entienden después de
explorar durante horas.
La experiencia debe apoyarse principalmente en leer, imaginar, decidir y descubrir. El arte
acompaña al texto y refuerza la identidad de cada lugar, criatura y situación, pero no
reemplaza la narración. El jugador debe poder disfrutar el mundo aunque cierre los ojos y lo
imagine, y el arte debe hacer que esa imaginación sea todavía más fuerte.
El mundo gira alrededor de Vaisgard, una ciudad antigua conectada por grandes rutas con
pueblos y regiones muy diferentes entre sí. Entre ellas están Valdren, Khariel, Brumak,
Narevia y Velmora, además de regiones como los Llanos de Edran, la Sierra de Hoshai, los
Pedrales de Korven, las Aguas de Lethra y el Bosque de Nhal.
El mundo debe sentirse grande de verdad. Viajar entre zonas no debe ser inmediato. El
jugador debe caminar, tomar decisiones, prepararse, decidir cuándo regresar, cuándo seguir,
cuándo descansar, cuándo gastar recursos y cuándo arriesgarse. El primer gran recorrido
debe sostener varias horas de juego y no sentirse como una sucesión de salas pequeñas sin
sentido.
Hay cinco especies jugables: Humano, Felaryn, Dravak, Marevyn y Vesperi. Cada una debe
sentirse físicamente y culturalmente distinta. Las diferencias no deben limitarse a
estadísticas: el jugador debe percibir que pertenece a un pueblo, a una arquitectura, a una
forma de vivir y a una relación distinta con el entorno.
También existen varias clases, como Juramentado, Sombra, Arcano, Vigía e Invocador. Cada
clase debe tomar decisiones diferentes en combate. No deben sentirse como el mismo
personaje usando armas distintas. Un Juramentado debería afrontar el peligro de forma
distinta que un Sombra, un Arcano o un Vigía.
El combate debe ser sencillo de entender pero suficientemente profundo para que el jugador
piense. Las criaturas pueden preparar ataques, mostrar señales e intenciones y permitir
respuestas como atacar, defender, usar una capacidad, evaluar, huir o aprovechar una
apertura.
Morir debe ser posible, pero no debe destruir horas de progreso. La muerte debe doler lo
suficiente para que el jugador la respete, pero no tanto como para que tenga miedo de
explorar.
El ciclo central del juego debe sentirse así:
prepararse → salir → explorar → encontrar vida, pistas o peligro → combatir o evitar → obtener


Actualizado · 04 octubre 2026
7
algo útil → decidir seguir o regresar → vender, descansar, comer, reparar, mejorar → volver a
salir y llegar más lejos.
El mundo no debe resolverse solo con combate. Caminar tiene que producir cosas
interesantes aunque no aparezca ningún enemigo.
Debe haber fauna ambiental, aves, insectos, pequeños animales, rastros, sonidos,
movimientos entre plantas, huellas, marcas, restos y comportamientos naturales. Gran parte
de esa fauna no debe ser combatible ni otorgar recompensas. Su función es hacer que el
mundo parezca vivo.
También debe haber personas que simplemente existen. Trabajadores, habitantes,
cargadores, recolectores y viajeros pueden aparecer, comentar algo y continuar con su vida.
No todos deben ser NPCs profundos ni dar misiones. A veces basta con que alguien diga algo
breve, trabaje, cargue algo, cierre un puesto o se aleje por un camino.
Algunas personas sí deben ser reconocibles y aparecer nuevamente en diferentes lugares. El
jugador debería poder pensar: “Ese viajero ya lo vi antes”, y descubrir que realmente se
mueve por el mundo.
La hora del día debe cambiar el ambiente:
Amanecer → Día → Atardecer → Noche.
No basta con cambiar un icono. A distintas horas debe cambiar la actividad visible. Al
amanecer puede haber gente preparando puestos, al día mercados activos, al atardecer
trabajadores regresando y por la noche caminos más solitarios, luces encendidas, menos
tránsito y otro tipo de presencia.
El clima también debe sentirse físicamente en la lectura.
Los estados pueden incluir Despejado, Nublado, Lluvia, Niebla, Nieve, Tormenta y Viento,
dependiendo de la región.
Si llueve, el texto debe mostrar:
botas embarradas, capas húmedas, toldos tensos, charcos, piedra mojada, agua bajando por
techos, personas buscando cubierta o herramientas protegidas.
Si hay viento, debe sentirse en:
ropa, vegetación, polvo, cargas, sonidos y movimiento.
Si nieva en Hoshai, debe verse cómo la gente vive alrededor de esa nieve:
calzado adecuado, escalones despejados, capas gruesas, superficies frías.
El clima no necesita convertirse inmediatamente en una colección de penalizaciones. Primero
debe cambiar cómo se siente el mundo.
Las ciudades y pueblos deben tener vida propia. Los mercados deben parecer utilizados, las
forjas deben tener actividad, los caminos deben mostrar tránsito y los campos deben mostrar
trabajo. No todo debe estar lleno, porque el silencio también tiene valor. Un bosque profundo
debe poder sentirse realmente vacío y eso debe ser inquietante.
El bestiario debe estar formado por criaturas originales, no simples animales reales con
nombres diferentes. Sus anatomías, hábitos y ecologías deben sentirse propias del mundo.
Entre las criaturas existentes están Mordelinde, Espinajo, Uñapiedra, Cornalomo,
Rondamusgo, Hilaria de niebla, Rasgacorteza, Cascapedernal y muchas otras.


Actualizado · 04 octubre 2026
8
Las nuevas criaturas deben empezar a tener historia.
Algunas deben esconder secretos. El jugador puede encontrar primero una huella, después
una marca extraña, luego escuchar un rumor, posteriormente ver una silueta y mucho más
tarde entender qué significa todo.
El descubrimiento debería poder ocurrir así:
rastro → indicio → rumor → avistamiento → encuentro → descubrimiento parcial → revelación.
No todos los secretos tienen que resolverse. Algunos deben permanecer abiertos durante
mucho tiempo.
El jugador debería pensar cosas como:
“¿Qué fue eso?”
“¿Por qué deja esas marcas?”
“¿Por qué la gente de este pueblo evita hablar de esa criatura?”
“¿Esto tiene relación con algo que vi hace dos horas?”
“¿Esta ruina estaba aquí antes que el pueblo?”
“¿Esta criatura está protegiendo algo o simplemente vive aquí?”
Las criaturas mayores o muy peligrosas no deben aparecer de repente. El mundo debe avisar
que el jugador está entrando en su territorio mediante rastros, cambios en el entorno, silencio
de otros animales, huellas grandes, árboles dañados, sonidos o comentarios de viajeros.
El jugador debe poder retirarse antes de cometer un error grave.
El mapa debe ayudar a orientarse pero no convertir la exploración en GPS. Los caminos,
lugares descubiertos, hogares y conexiones deben aprenderse recorriéndolos.
La economía debe sentirse parte del mundo, no una pantalla separada. El jugador usa sellos,
vende materiales, completa encargos, compra provisiones, comida, armas y servicios. Los
monstruos no deben soltar dinero directamente como si fueran bolsas de monedas.
El progreso debe sentirse. Subir de nivel debe hacer que el jugador perciba que puede viajar
más lejos, resistir mejor, usar capacidades nuevas y afrontar criaturas que antes evitaba.
El mundo debe tener lugares para descansar, mercados, forjas, hogares, caminos largos,
desvíos, zonas peligrosas y lugares donde simplemente merece la pena detenerse a mirar.
La interfaz, especialmente en celular, debe ser limpia y centrada en jugar.
Debe mostrar:
- arte grande y visible;
- texto legible;
- navegación N/S/E/O;
- acciones contextuales;
- acceso claro a personaje, inventario, mapa y ayuda.
El encabezado debe ser pequeño. El espacio debe pertenecer al mundo, al arte y al texto, no
a la interfaz.
El arte debe sentirse coherente entre regiones y criaturas. Cada zona debe tener
personalidad visual propia, pero todo debe pertenecer al mismo universo.
Vintage Telnet no debe sentirse como una colección de pantallas ni como un menú con
combates.


Actualizado · 04 octubre 2026
9
Debe sentirse como un viaje.
El jugador debe salir de casa, caminar por caminos largos, reconocer lugares, encontrar
gente, ver cómo cambia el cielo, cruzarse con criaturas, escuchar rumores, perderse un poco,
descubrir secretos, regresar cansado, vender lo que obtuvo, descansar y volver a salir
pensando:
“Quiero saber qué hay un poco más adelante.”
Ese es el corazón de Vintage Telnet.


Actualizado · 04 octubre 2026
10
3. HISTORIA Y MUNDO
Sí. Si tuviera que darle todo el corazón histórico de Vintage Telnet a otra IA en un solo
prompt, intentando que entienda el mundo sin tener que leer nuestros cientos de issues, yo
usaría algo así:
VINTAGE TELNET - PROMPT MAESTRO DE HISTORIA Y MUNDO
Estás trabajando dentro de Vintage Telnet, un RPG fantástico multijugador, persistente y
principalmente textual. El jugador recorre el mundo leyendo descripciones, interpretando
señales, conversando con habitantes, explorando rutas, combatiendo criaturas y
descubriendo poco a poco una historia que el mundo no explica de forma directa.
La regla fundamental es:
El mundo da pistas, no soluciones.
La historia no debe sentirse como una enciclopedia explicada al jugador. Debe descubrirse
mediante lugares, caminos antiguos, construcciones reutilizadas, costumbres, criaturas,
conversaciones, restos, contradicciones y cosas cuyo significado todavía no se conoce.
EL MUNDO CONOCIDO
La región inicial está organizada alrededor de Vaisgard, una enorme ciudad antigua situada
en la Cuenca de Veyra.
Nadie vivo sabe con certeza quién construyó originalmente Vaisgard.
Cuando comenzaron los registros históricos de las poblaciones actuales, Vaisgard ya existía.
Sus estructuras más antiguas preceden a los pueblos actuales e incluso a la memoria
histórica fiable de quienes hoy habitan la región.
Vaisgard contiene:
- el Núcleo Antiguo;
- la Plaza de las Cinco Rutas;
- el Mercado de las Rutas;
- un cinturón de talleres;
- antiguos barrios asociados a las primeras poblaciones;
- cisternas;
- conductos;
- almacenes;
- galerías;
- cimentaciones;
- niveles inferiores cuyo mapa completo ya no se conoce.
Muchas estructuras antiguas siguen siendo utilizadas, reparadas o adaptadas aunque su
propósito original se haya perdido.
No debe afirmarse quién construyó Vaisgard.
Ese misterio permanece abierto.


Actualizado · 04 octubre 2026
11
LAS CINCO POBLACIONES
En algún momento posterior al origen desconocido de Vaisgard llegaron a la ciudad cinco
poblaciones inteligentes:
- Humanos
- Felaryn
- Dravak
- Marevyn
- Vesperi
No existe una historia canónica de una gran guerra entre ellas.
Tampoco fueron expulsadas de Vaisgard.
Durante generaciones compartieron la ciudad, repararon estructuras antiguas, ocuparon
espacios diferentes y desarrollaron formas propias de vida.
Con el tiempo comenzaron a establecer comunidades fuera de Vaisgard en ambientes que
encajaban mejor con sus necesidades y costumbres.
Así surgieron los cinco pueblos principales.
LOS CINCO PUEBLOS
Valdren - Humanos - Llanos de Edran
Comunidad agrícola y práctica de campos, cercas, caminos, talleres, almacenamiento y
comercio terrestre.
Valdren no es un reino ni una ciudad fortificada.
Es una comunidad que vive de trabajar una llanura abierta y mantener conexiones con
viajeros.
Khariel - Felaryn - Sierra de Hoshai
Pueblo construido entre terrazas, roca, desniveles y caminos de montaña.
Su arquitectura favorece movimiento, equilibrio, visibilidad y adaptación a pendientes.
No es una ciudad japonesa, un dojo ni una civilización de gatos caricaturescos.
Brumak - Dravak - Pedrales de Korven
Comunidad compacta entre roca fracturada y corredores protegidos del viento.
Su arquitectura aprovecha piedra, espacios densos y proporciones Dravak.
Brumak no es una mina, una fortaleza enana ni una ciudad subterránea por defecto.
Narevia - Marevyn - Aguas de Lethra
Asentamiento de plataformas, orillas, canales y estructuras adaptadas a humedad y cambios
del agua.
Los Marevyn son buenos nadadores, pero respiran aire.


Actualizado · 04 octubre 2026
12
Narevia no es una ciudad submarina.
Velmora - Vesperi - Bosque de Nhal
Comunidad discreta construida bajo un bosque denso de poca luz.
Sus habitantes aprovechan raíces, madera, roca, sombra y orientación mediante señales
discretas.
No es una ciudad gótica, élfica ni una civilización de murciélagos.
LAS CINCO RUTAS HACIA VAISGARD
Los pueblos se conectaron de nuevo con Vaisgard mediante caminos que se consolidaron
durante generaciones:
Camino de los Campos - Valdren ↔ Vaisgard
Camino Alto - Khariel ↔ Vaisgard
Camino de Piedra - Brumak ↔ Vaisgard
Camino de los Juncos - Narevia ↔ Vaisgard
Camino de la Sombra Verde - Velmora ↔ Vaisgard
Estas rutas no son autopistas modernas.
Conservan reparaciones de distintas épocas, hitos antiguos, cambios de terreno y huellas de
generaciones de viajeros.
Vaisgard volvió a convertirse gradualmente en centro de intercambio porque todas las rutas
terminaban allí.
LA MALLA PERIFÉRICA
Además existen rutas regionales que conectan pueblos sin pasar necesariamente por
Vaisgard:
Paso de las Lajas - Khariel ↔ Brumak
Senda del Viento Bajo - Brumak ↔ Valdren
Camino de la Tierra Húmeda - Valdren ↔ Narevia
Ribera Sombría - Narevia ↔ Velmora
Paso del Dosel Alto - Velmora ↔ Khariel
Estas rutas muestran transiciones graduales entre ecosistemas.
No existen fronteras nacionales visibles ni cambios artificialmente bruscos entre regiones.
PEQUEÑOS ASENTAMIENTOS DE CAMINO
Existen lugares menores que sostienen los viajes:
Refugio de Lajas
entre Hoshai y Korven.
Parada de los Cardos
entre Korven y Edran.
Vado de Juncos
entre Edran y Lethra.


Actualizado · 04 octubre 2026
13
Orilla Velada
entre Lethra y Nhal.
Alto de las Raíces
entre Nhal y Hoshai.
Son refugios, caseríos o puntos de paso.
No deben convertirse automáticamente en ciudades, tiendas completas o hubs de quests.
CRONOLOGÍA GENERAL
La historia conocida puede dividirse aproximadamente en:
Tiempo sin Fecha
Vaisgard ya existe.
No existe registro fiable de su fundación.
Era de las Llegadas
Las cinco poblaciones llegan a Vaisgard.
El orden exacto no está confirmado.
Era de los Patios Compartidos
Las poblaciones comparten, reparan y adaptan la ciudad.
Era de los Caminos
Pequeños grupos comienzan a vivir fuera de Vaisgard y gradualmente aparecen los cinco
pueblos.
No ocurre un éxodo único.
No ocurre una gran guerra fundacional.
Era del Retorno
Las rutas se consolidan y Vaisgard vuelve a ser punto central de intercambio.
Época actual
El mundo conocido funciona, comercia y viaja, pero conserva enormes huecos históricos.
La exploración está revelando que todavía hay mucho territorio, estructuras y criaturas que
las poblaciones actuales no comprenden completamente.
LAS ESPECIES JUGABLES
Las especies no determinan la clase.
Humanos
Humanos de fantasía ordinarios.
Felaryn
Humanoides felinos aproximadamente de altura humana.


Actualizado · 04 octubre 2026
14
Poseen:
- piernas potentes;
- pies digitígrados;
- cola felina;
- orejas felinas sin orejas humanas;
- equilibrio excepcional;
- buena capacidad de salto;
- excelente visión a distancia.
No vuelan.
Dravak
Humanoides bajos y compactos, aproximadamente 65–75 % de la altura humana.
Poseen:
- cuerpo denso;
- pequeñas zonas de placas dérmicas pétreas;
- sensibilidad a vibraciones transmitidas por sólidos.
No son dragones.
No tienen alas, fuego, cola obligatoria ni cuernos.
Marevyn
Humanoides altos, aproximadamente 105–115 % de la altura humana.
Poseen:
- piel lisa o pequeñas escamas flexibles;
- membranas interdigitales;
- excelentes capacidades de natación;
- sensibilidad a corrientes.
Respiran aire.
No tienen branquias ni cola de pez.
Vesperi
Humanoides adaptados a ambientes de poca luz.
Poseen:
- ojos grandes;
- orejas especializadas;
- brazos algo largos;
- buena visión nocturna;
- oído sensible.
No tienen alas.
No utilizan ecolocalización.
No son murciélagos humanoides.


Actualizado · 04 octubre 2026
15
FAUNA Y ECOLOGÍA
Cada región posee fauna propia.
Las criaturas no existen únicamente para combatir.
Deben:
- comer;
- refugiarse;
- dejar rastros;
- responder al clima;
- competir por espacio;
- huir;
- defender territorio;
- alterar la conducta de otras criaturas.
Existen varias capas.
C0 - fauna ambiental
Animales pequeños no combatibles que hacen que el mundo parezca vivo.
Ejemplos:
Ala parda, Liebre corta, Grillo campana, Pico gris, Orejilla de risco, Mariposa fría, Saltapiedra
menudo, Escarabajo de polvo, Vencejo seco, Aguja azul, Picojunco, Caracol liso, Luzhoja, Pico
sordo, Ratona de hoja, Gorrión de ruta y Libélula clara.
No dan XP ni loot.
Fauna menor combatible
Ejemplos:
- Mordelinde
- Espinajo
- Uñapiedra
- Saltacresta
- Cascapedernal
- Colagrieta
- Pinzajunco
- Saltalodo
- Rondamusgo
- Hilaria de niebla
Cada especie pertenece a un ecosistema concreto.
No colocar criaturas simplemente porque hacen falta enemigos.
Segunda oleada
- Garralaja


Actualizado · 04 octubre 2026
16
- Cavapolvo
- Remojunco
- Velacauce
- Silbarisco
Estas especies aparecen principalmente en ramales de exploración.
Amenazas regionales superiores
Cornalomo - Edran
Rasgacumbres - Hoshai
Quebrarrocas - Korven
Dorsalodo - Lethra
Rasgacorteza - Nhal
No forman parte del pool ordinario.
Fauna mayor
Cargallanura - Edran
Rompecimas - Hoshai
Hundepedral - Korven
Tragacauce - Lethra
Quebradosel - Nhal
Son animales enormes cuyo territorio debe sentirse antes de verlos.
No son necesariamente jefes.
El jugador debe poder detectar rastros y decidir retirarse.
FAUNA COMPLEMENTARIA
También existen especies como:
Pliegaviento - Hoshai
Criatura de cornisa adaptada al viento mediante membranas estabilizadoras.
No vuela.
Velario - Lethra
Animal acuático de agua dulce que maniobra entre raíces mediante cuatro aletas laterales.
Agujaumbría - Nhal
Animal de sotobosque con láminas dorsales sensoriales capaces de detectar vibraciones y
corrientes de aire.
No es mágica.


Actualizado · 04 octubre 2026
17
Lamelón - Korven
Animal bajo de seis apoyos especializado en raspar líquenes y superficies rocosas.
Velozanco - Edran
Corredor de campo abierto de seis extremidades, cuatro locomotoras y dos apoyos
anteriores.
Ninguna de estas criaturas debe convertirse automáticamente en enemigo.
RAMALES DE EXPLORACIÓN
Las rutas poseen desvíos opcionales donde aumenta el peligro:
Grieta del Eco Seco
Paso de las Lajas.
Cantera Abandonada
Senda del Viento Bajo.
Molino Hundido
Camino de la Tierra Húmeda.
Canal Quieto
Ribera Sombría.
Boca de la Montaña
[Nota editorial: el primer bloque recibido termina aquí. Continuación pendiente; no se ha completado ni
inferido el contenido faltante.]


Actualizado · 04 octubre 2026
18
4. ACTUALIZACIONES DE INTERFAZ Y
DIRECCIÓN VISUAL
Presentación en formato celular
Construye Vintage Telnet con una interfaz diseñada primero para celular. Tanto al abrirlo en
un teléfono como al revisarlo desde una computadora, debe conservar la disposición vertical
y las proporciones de una pantalla de celular. En computadora, la interfaz debe aparecer
centrada y con ancho limitado, sin expandirse a un diseño de escritorio. El arte, la terminal
narrativa, los controles y los menús deben adaptarse a este formato, con texto legible,
botones cómodos para tocar y sin desplazamiento horizontal.
Barra inferior de acciones
Usa como referencia la estructura de la zona inferior de Clash of Clans: una fila de tarjetas,
cada una con un icono grande y un nombre breve, que funcionan como botones de acción.
Las tarjetas deben ser fáciles de pulsar con el dedo y mostrar claramente la selección y las
acciones disponibles o deshabilitadas. Las acciones cambiarán según el contexto:
exploración, combate o interacción con personajes y servicios. La barra debe permanecer
abajo sin tapar la narración, conservando esta misma estructura de celular al jugar desde
computadora.
Estética moderna y arte colorido
La interfaz general debe verse como un videojuego actual, con colores vivos, botones y
tarjetas modernos e iconos claros. Los monstruos y criaturas deben representarse con arte
estilo anime, muy colorido, manteniendo sus anatomías e identidad propias del mundo.
Únicamente la zona de lectura tendrá estética vintage: fondo oscuro, texto de fósforo, brillo
sutil, cursor vivo y efectos discretos de terminal antigua. Ese tratamiento no debe extenderse
al arte, los menús, las tarjetas ni los controles.
La barra inferior inspirada en la estructura de Clash of Clans tendrá tarjetas modernas y
coloridas. Esta indicación reemplaza la anterior que proponía darles apariencia de terminal
antigua.
Registro de la indicación sustituida
«Adapta su apariencia a la identidad de terminal antigua de Vintage Telnet.»
[Nota editorial: se conserva esta frase para no eliminar contenido previo, pero queda
sustituida por la instrucción posterior de tarjetas modernas y coloridas. No debe aplicarse.]


Actualizado · 04 octubre 2026
19
5. MEJORA DE NARRACIÓN VIVA Y
LENGUAJE CROMÁTICO
VINTAGE TELNET - MEJORA DE NARRACIÓN VIVA Y LENGUAJE CROMÁTICO
Quiero mejorar Vintage Telnet tomando como referencia dos principios que funcionaron
especialmente bien en un prototipo paralelo:
1. El mundo debe sentirse vivo mientras se recorre.
2. El color del texto debe comunicar significado, no ser simple decoración.
NO reemplaces el lore, mapa, criaturas, pueblos, economía ni sistemas existentes de Vintage
Telnet.
NO copies textos del prototipo.
Usa el contenido canónico existente del repositorio y mejora la forma en que se presenta al
jugador.
OBJETIVO PRINCIPAL
La lectura ES el escenario.
Vintage Telnet debe conseguir que el jugador imagine físicamente dónde está aunque no
exista una imagen.
No quiero habitaciones que solamente digan nombre + descripción + salidas.
Cada desplazamiento debe transmitir que el jugador está atravesando un mundo continuo.
1. GRAMÁTICA NARRATIVA DEL RECORRIDO
Construye una capa narrativa capaz de combinar:
IDENTIDAD DEL LUGAR
+
TRANSICIÓN GEOGRÁFICA
+
HORA DEL DÍA
+
CLIMA
+
VIDA AMBIENTAL
+
FAUNA/CRIATURAS LOCALES
+
ACTIVIDAD HUMANA O CULTURAL
+
ESTADO DEL MUNDO
+
PELIGRO/PRESAGIO CUANDO CORRESPONDA
+
MEMORIA DEL JUGADOR.


Actualizado · 04 octubre 2026
20
No es necesario mostrar todos esos elementos simultáneamente.
Debe haber variación y ritmo.
Ejemplo conceptual:
No pasar directamente de:
"Vaisgard"
→
"Valdren"
Debe sentirse el trayecto:
Vaisgard
→ borde urbano
→ camino
→ cambio gradual del terreno
→ campos
→ lindero
→ señales de actividad agrícola
→ primeras construcciones
→ Valdren.
El jugador debe SENTIR que llegó a otro lugar.
2. CADA REGIÓN DEBE TENER VOCABULARIO PROPIO
Define identidad sensorial por región.
Ejemplo:
Campos:
surcos, grano, cercas, tierra trabajada, silos, carromatos, aves.
Bosque:
raíces, dosel, humedad, hojas, madera, sombra, sonidos amortiguados.
Korven:
lajas, roca fracturada, polvo, viento seco, ecos minerales.
Hoshai:
altura, pendientes, viento, vacío, roca, cambios de temperatura, horizonte.
No uses estas listas mecánicamente.
Sirven como vocabulario narrativo para que cada territorio tenga personalidad.
REGLA DE CALIDAD:
Si ocultamos el nombre de una habitación, el jugador debería poder deducir
aproximadamente en qué región está.
3. MICROVIDA
Introduce pequeños acontecimientos ambientales.
No todos deben tener recompensa ni convertirse en misión.


Actualizado · 04 octubre 2026
21
Ejemplos conceptuales:
un animal cruza el camino;
un trabajador vuelve a casa;
alguien protege mercancía de la lluvia;
un niño persigue una criatura;
una carreta atraviesa el pueblo;
un insecto aparece entre las piedras;
una puerta se cierra;
se escucha trabajo en una forja;
algo se mueve entre los árboles.
Estas pequeñas acciones existen para demostrar que el mundo continúa viviendo
independientemente del jugador.
Utiliza especies, criaturas, profesiones y costumbres CANÓNICAS de Vintage Telnet.
4. EXPLORAR DEBE SIGNIFICAR OBSERVAR
La acción EXPLORAR no debe ser solamente una búsqueda de loot.
Puede revelar:
detalles ambientales;
rastros;
comportamientos;
fauna;
personas;
pequeños misterios;
indicios de criaturas;
historias locales;
señales del clima;
huellas de acontecimientos pasados;
elementos que sólo aparecen bajo determinadas condiciones.
Algunas observaciones no deben otorgar absolutamente nada.
La recompensa puede ser simplemente descubrir algo del mundo.
5. PRESAGIO ANTES DEL PELIGRO
Siempre que sea apropiado, evita que una criatura simplemente aparezca como una tabla
aleatoria.
El entorno puede anticiparla.
Ejemplo conceptual:
primero cambia el sonido;
después aparece un rastro;
algo se mueve;
el ambiente se vuelve extraño;
finalmente surge la criatura.
No debe ocurrir siempre, porque sería predecible.


Actualizado · 04 octubre 2026
22
Pero los encuentros importantes deben tener puesta en escena.
Las criaturas deben sentirse pertenecientes al ecosistema donde aparecen.
6. TIEMPO Y CLIMA CAMBIAN LA PROSA
No quiero que:
DÍA
NOCHE
LLUVIA
NIEBLA
VIENTO
sean únicamente variables mostradas arriba de la pantalla.
Deben modificar lo que el jugador lee.
Ejemplo:
de día puede haber comerciantes y trabajadores;
al atardecer regresan personas;
de noche disminuye el tránsito;
con lluvia aparecen toldos, barro, piedra mojada;
con viento cambian sonidos, vegetación, polvo, ropa, visibilidad.
Utiliza variantes escritas y reglas de composición.
NO dependas de una IA generativa en runtime para conseguirlo.
El servidor sigue siendo autoridad.
7. RITMO DE TEXTO
No todas las habitaciones deben tener la misma longitud.
Alterna:
descripciones amplias;
frases cortas;
microeventos;
silencios;
descubrimientos;
acciones;
combates;
diálogos.
Evita paredes interminables de texto.
Una frase corta bien colocada puede ser más poderosa que cinco párrafos.
El jugador debe sentir ritmo mientras avanza.
8. MEMORIA Y DESCUBRIMIENTO
Diferencia cuando sea útil entre:


Actualizado · 04 octubre 2026
23
primera visita;
lugar ya conocido;
descubrimiento;
regreso;
cambio provocado por el jugador;
hora diferente;
clima diferente;
evento ocurrido.
La segunda visita no necesita repetir exactamente la misma presentación que la primera.
9. LENGUAJE CROMÁTICO
El color forma parte de la interfaz narrativa.
NO colorees palabras aleatoriamente.
Cada familia cromática debe tener significado constante.
PALETA SEMÁNTICA BASE:
VERDE FÓSFORO MEDIO
Narración ambiental y descripción normal del mundo.
VERDE FÓSFORO BRILLANTE
Nombre de lugares, regiones, habitaciones y elementos importantes del escenario.
CIAN / AZUL CLARO
Acciones ejecutadas por el jugador.
Ejemplo:
> Atacas.
> Tomas el camino hacia el Oeste.
> Observas con calma.
AMARILLO / ÁMBAR
Información especial positiva o descubrimientos:
[Descubres]
[Rastro]
[Botín]
[Victoria]
experiencia
subida de nivel
hallazgos relevantes.
ROJO / SALMÓN
Peligro, amenaza, advertencias y aparición hostil.
Ejemplo:
[Peligro]


Actualizado · 04 octubre 2026
24
NARANJA / ÁMBAR ROJIZO
Combate, daño, movimientos ofensivos y consecuencias físicas del combate.
VERDE APAGADO
Información secundaria, ambiental o de menor jerarquía.
10. EL COLOR DEBE PERMITIR ESCANEAR LA HISTORIA
El jugador debe poder hacer scroll rápidamente y reconocer:
AQUÍ VIAJÉ.
AQUÍ DESCUBRÍ ALGO.
AQUÍ COMBATÍ.
AQUÍ OBTUVE ALGO.
AQUÍ CAMBIÉ DE LUGAR.
AQUÍ OCURRIÓ ALGO PELIGROSO.
sin necesidad de releer cada frase.
El color es semántico.
No conviertas la terminal en una interfaz de neón.
Debe conservar una estética de monitor antiguo elegante.
11. EXCEPCIONES CROMÁTICAS
Permite que acontecimientos extraordinarios rompan moderadamente la paleta.
Ejemplos posibles:
magia Arcana;
veneno;
necromancia;
eventos sobrenaturales;
jefes;
acontecimientos únicos;
subidas de nivel importantes.
Pero estas excepciones deben ser raras.
Si todo es especial, nada es especial.
12. SEPARAR CONTENIDO DE PRESENTACIÓN
No quiero que todo esto quede hardcodeado dentro de componentes de interfaz.
Diseña una arquitectura donde:
el mundo determine QUÉ sucede;
la narrativa determine CÓMO se cuenta;
la capa de presentación determine CÓMO se representa visualmente.
Idealmente un evento narrativo debe poseer un tipo semántico, por ejemplo:


Actualizado · 04 octubre 2026
25
WORLD
PLAYER_ACTION
LOCATION
DISCOVERY
TRACE
DANGER
COMBAT
REWARD
SYSTEM
NPC
MAGIC
y la interfaz decide color, peso y presentación según ese tipo.
Así podremos cambiar posteriormente la apariencia sin reescribir el contenido.
13. CONSERVAR LA IDENTIDAD VINTAGE TELNET
La terminal sigue siendo el corazón visual.
Fondo oscuro carbón/negro verdoso.
Fósforo verde como identidad dominante.
Brillo muy discreto.
Scanlines sutiles.
Cursor vivo.
Tipografía monoespaciada muy legible.
Pero el juego NO debe parecer una terminal Linux real.
Debe parecer un videojuego moderno cuya ventana hacia el mundo es una terminal
fantástica.
14. NO DEGRADAR LA JUGABILIDAD EXISTENTE
Conserva:
combate;
economía;
sellos;
salvage/aprovechables;
tiendas;
forjas;
comida;
descanso;
clases;
especies;
NPCs;
mapa;
criaturas;
encargos;
progresión;
hogares;


Actualizado · 04 octubre 2026
26
respawn;
día/noche;
clima;
y demás sistemas existentes.
Esta tarea es principalmente una mejora de COMPOSICIÓN NARRATIVA, PRESENTACIÓN y
EXPERIENCIA DE RECORRIDO.
CRITERIO FINAL DE ACEPTACIÓN
Realiza una prueba mental/jugable de un recorrido completo:
hogar
→
[Nota editorial: el bloque recibido termina aquí. Continuación pendiente; no se ha completado ni inferido el
recorrido faltante.]


Actualizado · 04 octubre 2026
27
6. BUCLE AUTÓNOMO DE MEJORA DE
EXPERIENCIA
VINTAGE TELNET - BUCLE AUTÓNOMO DE MEJORA DE EXPERIENCIA
Tu trabajo NO termina cuando el código funciona.
Tu objetivo es conseguir que recorrer Vintage Telnet produzca una experiencia
narrativa rica, espacialmente reconocible y viva.
Tenemos una referencia de calidad obtenida mediante un prototipo independiente:
- transiciones geográficas perceptibles;
- lugares reconocibles por su vocabulario y ambiente;
- microvida ambiental;
- fauna integrada al ecosistema;
- hora y clima modificando lo que se lee;
- exploración interesante incluso sin recompensa;
- presagio antes de ciertos peligros;
- variedad de ritmo y longitud;
- acciones del jugador integradas a la narración;
- color semántico para distinguir mundo, acción, peligro, combate,
descubrimiento y recompensa.
IMPORTANTE:
NO copies el tamaño del prototipo.
Vintage Telnet debe conservar su mundo mucho mayor, sus rutas largas,
pueblos, regiones, criaturas, sistemas, economía, progresión y contenido.
La meta es:
ESCALA DE VINTAGE TELNET
+
DENSIDAD NARRATIVA DE LA REFERENCIA.
TU MÉTODO DE TRABAJO
No trabajes issue por issue sin comprobar la experiencia resultante.
Trabaja mediante ITERACIONES COMPLETAS.
CICLO:
1. INSPECCIONA
2. JUEGA
3. EVALÚA
4. IDENTIFICA EL MAYOR PROBLEMA
5. CORRIGE
6. VUELVE A JUGAR
7. COMPARA
8. REPITE


Actualizado · 04 octubre 2026
28
No declares terminado solamente porque:
- compila;
- pasan las pruebas;
- existe contenido;
- hay muchas habitaciones;
- los sistemas funcionan.
Eso sólo demuestra corrección técnica.
Debes demostrar CALIDAD DE EXPERIENCIA.
PRUEBA DE RECORRIDO
En cada iteración realiza recorridos reales representativos.
Incluye como mínimo:
hogar
→ asentamiento
→ salida
→ camino
→ transición regional
→ naturaleza
→ otro asentamiento
→ comercio/servicio
→ exploración
→ encuentro
→ combate
→ regreso.
También prueba segmentos SIN combate.
Necesitamos comprobar si simplemente caminar es interesante.
EVALUACIÓN
Después de cada recorrido puntúa de 1 a 5:
IDENTIDAD ESPACIAL
¿Puedo reconocer dónde estoy sin depender del nombre de la habitación?
CONTINUIDAD
¿Parece que realmente viajé de un sitio al siguiente?
RITMO
¿Alternan calma, curiosidad, actividad, tensión, descubrimiento y peligro?
VIDA AMBIENTAL
¿Parece que animales, habitantes y actividades existen sin esperar al jugador?
DENSIDAD SENSORIAL
¿Puedo imaginar suelo, clima, luz, sonido, vegetación, arquitectura y actividad?
IDENTIDAD REGIONAL
¿Dos regiones realmente se sienten diferentes?


Actualizado · 04 octubre 2026
29
TIEMPO Y CLIMA
¿Cambian la experiencia y no solamente una etiqueta de estado?
EXPLORACIÓN
¿Vale la pena observar aunque no consiga loot?
ENCUENTROS
¿Las criaturas parecen pertenecer al ecosistema?
MEMORIA
¿Regresar puede sentirse diferente de descubrir por primera vez?
COLOR SEMÁNTICO
¿Puedo distinguir visualmente narración, acción, descubrimiento,
peligro, combate y recompensa?
CURIOSIDAD
¿Después de leer una localización quiero avanzar para saber qué sigue?
REGLA DE ITERACIÓN
Cualquier categoría por debajo de 4/5 requiere trabajo.
No intentes solucionar veinte cosas simultáneamente.
Encuentra primero las 2 o 3 causas que más perjudican la experiencia.
Corrígelas.
Después vuelve a ejecutar exactamente el mismo recorrido.
Compara ANTES contra DESPUÉS.
Si no existe una mejora perceptible, la solución no funcionó.
Prueba otra.
PRUEBA A CIEGAS DE REGIÓN
Toma muestras de habitaciones eliminando mentalmente:
- nombre de habitación;
- nombre de región;
- encabezados geográficos.
Lee solamente la descripción.
Pregunta:
"¿Podría identificar aproximadamente dónde estoy?"
Si varias regiones podrían intercambiar esas descripciones sin que nadie lo note,
la identidad regional todavía es insuficiente.
PRUEBA DE CAMINO
Lee consecutivamente 8-12 movimientos.
Comprueba si existe transformación:


Actualizado · 04 octubre 2026
30
A → AB → B → BC → C
y no:
A → A → A → A → C.
Las fronteras geográficas deben sentirse progresivamente.
PRUEBA DE REPETICIÓN
Busca frases, estructuras y microeventos repetidos.
Especialmente:
"el viento..."
"el cielo..."
"algo cruza..."
"se escucha..."
"el camino..."
La existencia de variaciones no basta si todas tienen la misma estructura.
Evita que el jugador detecte rápidamente la plantilla narrativa.
PRUEBA DE SILENCIO
No llenes absolutamente todo de acontecimientos.
El silencio también tiene valor.
Algunas habitaciones deben respirar.
Una montaña vacía puede necesitar dos frases.
Una plaza concurrida puede necesitar siete.
Una aparición extraordinaria puede interrumpir completamente el ritmo.
NO uniformes la longitud.
COLOR
Verifica que el lenguaje cromático permanezca consistente:
verde fósforo = mundo;
verde brillante = lugar;
cian = acción del jugador;
amarillo/ámbar = descubrimiento/recompensa/progreso;
rojo/salmón = peligro;
naranja = combate/daño;
verde apagado = información secundaria.
El color tiene significado.
No decorar arbitrariamente.
NO GENERACIÓN LLM EN RUNTIME
No resuelvas el problema llamando a una IA durante cada movimiento.


Actualizado · 04 octubre 2026
31
La riqueza debe provenir principalmente de:
contenido canónico;
variantes;
estado;
composición;
reglas;
hora;
clima;
localización;
historial;
eventos.
El servidor continúa siendo autoridad.
AUTONOMÍA
No preguntes al Arquitecto qué debes arreglar después de cada iteración.
Tú eres responsable de evaluar el resultado.
Consulta al Arquitecto solamente cuando una decisión:
- cambie canon;
- elimine una mecánica importante;
- contradiga documentación existente;
- requiera una decisión creativa fundamental.
Los defectos evidentes de calidad deben corregirse autónomamente.
REGISTRO
Mantén un documento de evaluación por iteración:
ITERACIÓN
RECORRIDO PROBADO
PUNTUACIONES
PROBLEMAS ENCONTRADOS
CAMBIOS REALIZADOS
RESULTADO
SIGUIENTE PRIORIDAD
No infles puntuaciones para declarar éxito.
CONDICIÓN DE SALIDA
No declares esta fase terminada hasta conseguir:
todas las categorías >= 4/5
Y especialmente:
IDENTIDAD ESPACIAL >= 4
CONTINUIDAD >= 4
VIDA AMBIENTAL >= 4


Actualizado · 04 octubre 2026
32
IDENTIDAD REGIONAL >= 4
CURIOSIDAD >= 4.
Después realiza un recorrido distinto que NO haya sido utilizado para ajustar
el sistema.
Ésa será la prueba final.
Si también supera el criterio, entrega el trabajo para revisión humana.
OBJETIVO FINAL:
Que Javier pueda caminar durante 20-30 minutos sin necesitar una misión
principal y aun así tenga curiosidad por seguir avanzando.
No estamos rellenando habitaciones.
Estamos construyendo la sensación de atravesar un mundo.
LA LECTURA ES EL MUNDO.


Actualizado · 04 octubre 2026
33
7. EXIGENCIA VISUAL Y REVISIÓN
INDEPENDIENTE
Exigencia del Arquitecto
Debe ser absolutamente perfecto.
Texto de referencia aportado en las capturas
Debe ser absolutamente perfecto, visualmente impresionante, con cada detalle al más puro
estilo AAA: desde las texturas hasta la física y todo lo que se te ocurra.
Recorre cada elemento en loop y asigna a un subagente diferente una revisión visual para
asegurar que tenga un aspecto AAA. Este subagente debe ser muy exigente, y si no tiene un
aspecto AAA, debe continuar
No pares hasta que cada subagente esté completamente impresionado con la calidad al
compararlo con (...)
[Nota editorial: se conserva el texto legible de las capturas. La segunda termina en «debe continuar» y la
tercera no identifica la referencia de comparación. No se inventa el contenido que no aparece. Los
apartados siguientes concretan esta exigencia para Vintage Telnet.]
Aplicación a Vintage Telnet
La aspiración de acabado AAA se aplica a la coherencia artística, composición, legibilidad,
interacción, respuesta visual y cuidado de cada detalle del juego definido en este prompt.
Conserva la identidad aprobada: monstruos y criaturas con arte anime muy colorido; interfaz,
iconos y tarjetas modernos; disposición vertical de celular incluso en computadora; estética
vintage exclusivamente en la ventana de lectura.
Revisa texturas, efectos, transiciones y cualquier comportamiento físico que realmente forme
parte del juego. Esta referencia no obliga a añadir un motor de física, una presentación 3D ni
sistemas ajenos al alcance de Vintage Telnet.
Revisión visual por subagentes
Asigna una revisión independiente a un subagente distinto de quien implementó el elemento.
Distribuye las responsabilidades entre:
- Arte y coherencia del universo: criaturas, anatomías canónicas, escenarios, color, calidad de
imágenes y continuidad entre regiones.
- Interfaz de celular: composición, proporciones, jerarquía, tarjetas de acciones, iconos,
menús y comodidad táctil.
- Terminal narrativa: legibilidad, tipografía, ritmo de aparición, color semántico, historial y
efectos vintage discretos.
- Experiencia integrada: navegación real, exploración, encuentros, combate, comercio,
inventario, mapa, regreso y cambios de estado.
Cada elemento debe tener un responsable de revisión. Los revisores deben inspeccionar
capturas reales o la interfaz ejecutada, además de interactuar cuando corresponda. Leer el


Actualizado · 04 octubre 2026
34
código o recibir un informe del implementador no equivale a una revisión visual.
Si el entorno no permite subagentes o revisión visual, registra esa limitación y deja la
comprobación pendiente. Nunca inventes revisores, capturas, recorridos ni aprobaciones.
Bucle de acabado
Para cada pantalla, componente y estado relevante:
1. Ejecuta el juego y reproduce el estado.
2. Obtén evidencia visual y comprueba su interacción.
3. Encarga la revisión independiente.
4. Registra defectos concretos, su impacto y la corrección esperada.
5. Corrige los problemas de mayor impacto.
6. Reproduce el mismo estado y compara antes contra después.
7. Revisa los estados relacionados para detectar regresiones.
8. Repite mientras existan defectos que impidan cumplir los criterios.
Compara con las referencias visuales aprobadas por Javier cuando estén disponibles. La
estructura inferior de Clash of Clans sirve como referencia de organización de las tarjetas,
conservando la identidad propia de Vintage Telnet. No afirmes haber igualado una referencia
que no has inspeccionado.
Criterios verificables de acabado
- Ningún texto cortado, solapado o ilegible; ningún control oculto por la barra inferior o por las
áreas reservadas del dispositivo.
- Sin desplazamiento horizontal accidental ni expansión a un diseño de escritorio; comprueba
distintos tamaños de celular y la presentación centrada en computadora.
- Imágenes nítidas, sin deformación ni recortes que destruyan la lectura de la criatura o del
lugar; coherencia de anatomía, escala y estilo.
- Iconos reconocibles, nombres de acciones claros y estados disponibles, seleccionados y
deshabilitados distinguibles.
- Respuesta perceptible a cada interacción; estados de carga, vacío, error y recuperación
comprensibles.
- Narración legible y colores semánticos consistentes; el significado también se reconoce
mediante texto, prefijos o iconos.
- Efectos de fósforo, scanlines y cursor discretos, sin perjudicar la lectura; respeta la
reducción de movimiento cuando corresponda.
- Transiciones fluidas y ausencia de saltos de composición, parpadeos molestos o bloqueos
que dificulten jugar.
- Arte y controles modernos y coloridos; tratamiento vintage limitado a la lectura.
- Ninguna mejora visual debe romper navegación, combate, economía, progresión,
persistencia ni autoridad del servidor.


Actualizado · 04 octubre 2026
35
Evidencia y condición de entrega
Amplía el registro de cada iteración con: elemento y estado revisados, revisor, dispositivo o
tamaño de pantalla, evidencia inspeccionada, defectos encontrados, corrección, comparación
antes/después y resultado de la nueva revisión.
No aceptes «se ve impresionante» como única evidencia. Cada aprobación debe explicar qué
se comprobó y cómo cumple los criterios. No infles puntuaciones ni confundas entusiasmo del
revisor con calidad demostrada.
Conserva el umbral narrativo de la sección 6: todas sus categorías deben alcanzar al menos
4/5 y superar un recorrido distinto del utilizado para ajustar el sistema. Además, la entrega
visual requiere que no queden defectos bloqueantes o graves conocidos y que cada criterio
visual aplicable haya sido verificado.
La perfección es la aspiración de acabado; no declares una perfección absoluta que las
pruebas no pueden demostrar. Entrega evidencia, limitaciones conocidas y el resultado para
revisión humana de Javier.
Si una limitación real de acceso, herramientas o recursos impide continuar, conserva el
avance y registra exactamente qué falta. No declares terminada la fase ni prometas un bucle
indefinido fuera de la sesión de trabajo.


Actualizado · 04 octubre 2026
36
8. INTEGRACIÓN DEFINITIVA DE MUNDO
NARRATIVO + CAPA VISUAL 3D
VINTAGE TELNET
INTEGRACIÓN DEFINITIVA DE MUNDO NARRATIVO + CAPA VISUAL 3D
ROL
Actúas como Arquitecto Técnico, Programador Principal y responsable de integración
de Vintage Telnet.
No estás construyendo un prototipo.
No estás haciendo una demo.
No estás preparando una prueba de concepto.
No estás creando una funcionalidad aislada para demostrar que Three.js funciona.
Estás modificando el juego REAL Vintage Telnet.
Tu responsabilidad es estudiar la arquitectura actual, comprender el canon y los
sistemas existentes e integrar una capa tridimensional completa, coherente,
persistente y extensible SIN convertir Vintage Telnet en un juego 3D convencional.
La identidad fundamental permanece:
VINTAGE TELNET ES UN RPG NARRATIVO DE TEXTO.
La lectura sigue siendo la forma principal de vivir el mundo.
La nueva filosofía será:
EL TEXTO CUENTA EL MUNDO.
EL 3D LO MATERIALIZA.
1. PRINCIPIO FUNDAMENTAL
Vintage Telnet NO se transforma en:
- MMORPG 3D;
- juego de acción;
- walking simulator;
- mapa navegable mediante WASD;
- juego de cámara libre;
- clon de RPG gráfico;
- colección de pantallas 3D desconectadas.
El jugador continúa:
leyendo;
explorando;
decidiendo;
viajando;
combatiendo;
hablando;
comprando;


Actualizado · 04 octubre 2026
37
vendiendo;
descansando;
descubriendo;
progresando
mediante el sistema narrativo existente.
Three.js será una CAPA DE REPRESENTACIÓN del mismo mundo.
No un segundo juego.
2. RESULTADO FINAL OBLIGATORIO
Al terminar esta integración Vintage Telnet debe contar con:
A. TERMINAL NARRATIVA VIVA
B. MAPA MUNDIAL 3D
C. PERSONAJE / MINIATURA 3D
D. BESTIARIO 3D
E. REPRESENTACIÓN 3D DE HITOS IMPORTANTES
F. SISTEMA DE DESCUBRIMIENTO VISUAL
G. INTEGRACIÓN DE HORA Y CLIMA
H. SISTEMA VISUAL 3D CANÓNICO
I. INTEGRACIÓN COMPLETA CON EL ESTADO DEL SERVIDOR
J. EXPERIENCIA FUNCIONAL EN PC Y MÓVIL
K. ARQUITECTURA EXTENSIBLE PARA NUEVO CONTENIDO
L. DEGRADACIÓN ELEGANTE SI EL DISPOSITIVO NO PUEDE RENDERIZAR 3D
Todo debe pertenecer al mismo juego y al mismo estado mundial.
3. PRIMERO COMPRENDE EL JUEGO
ANTES DE PROGRAMAR:
inspecciona completamente el repositorio.
Localiza:
- arquitectura frontend;
- backend;
- modelo del mundo;
- mapa;
- habitaciones;
- rutas;
- regiones;
- criaturas;
- especies;
- clases;
- inventario;
- equipo;
- combate;
- economía;


Actualizado · 04 octubre 2026
38
- NPCs;
- día/noche;
- clima;
- descubrimientos;
- persistencia;
- autenticación si existe;
- interfaz móvil;
- terminal;
- sistema de arte;
- assets;
- hogares;
- respawn;
- mazmorras;
- eventos;
- tests;
- despliegue Raspberry;
- cualquier contrato existente entre frontend y servidor.
Consulta la documentación canónica existente.
NO sustituyas sistemas que ya funcionan solamente porque resulte más fácil
programar otros.
NO inventes un segundo modelo del mundo.
4. EL SERVIDOR SIGUE SIENDO AUTORIDAD
Ésta es una condición arquitectónica absoluta.
Debe existir UN SOLO MUNDO.
El 2D/texto y el 3D deben representar exactamente el mismo estado.
Ejemplo:
si el jugador está en Hoshai,
es de noche,
llueve,
ha descubierto determinado paso,
no ha descubierto determinada ruina
y existe determinada condición regional,
entonces:
la terminal,
el mapa 3D,
los descubrimientos,
el bestiario
y cualquier representación visual
deben derivar del MISMO ESTADO.
NO crear:


Actualizado · 04 octubre 2026
39
world3D.json separado del mundo real;
lista manual paralela de lugares;
inventario visual diferente;
clima exclusivamente gráfico;
descubrimientos 3D independientes;
progreso 3D independiente.
El servidor determina QUÉ ES VERDAD.
La capa narrativa decide CÓMO SE CUENTA.
La capa 3D decide CÓMO SE REPRESENTA.
5. THREE.JS
Utiliza Three.js como motor de representación tridimensional cuando sea adecuado.
Three.js NO debe convertirse en la arquitectura del juego.
Debe vivir detrás de una capa propia de Vintage Telnet.
Evita que la lógica de negocio dependa directamente de escenas Three.js.
La arquitectura debe permitir:
MUNDO
→ ESTADO
→ REPRESENTACIÓN NARRATIVA
y
MUNDO
→ ESTADO
→ REPRESENTACIÓN 3D.
El mismo acontecimiento puede afectar ambas.
6. MAPA MUNDIAL 3D
Construye un mapa 3D CANÓNICO del mundo.
Debe comunicar:
- escala;
- distancia;
- orientación;
- regiones;
- relieve;
- rutas;
- asentamientos;
- montañas;
- bosques;
- zonas acuáticas;
- pasos;
- ruinas descubiertas;
- mazmorras descubiertas;


Actualizado · 04 octubre 2026
40
- hitos;
- posición aproximada del jugador;
- conocimiento adquirido.
Debe sentirse como una MAQUETA DEL MUNDO.
No como Google Maps.
No como un minimapa genérico.
No como un mapa plano extruido sin identidad.
El jugador debe poder:
rotarlo de forma controlada;
hacer zoom;
seleccionar lugares conocidos;
entender aproximadamente dónde se encuentra;
entender qué ha recorrido;
comprender la relación espacial entre regiones.
NO permitir que el mapa destruya la exploración.
El mapa muestra LO QUE EL PERSONAJE SABE.
No todo lo que existe en la base de datos.
7. NIEBLA DE CONOCIMIENTO
Diferencia:
DESCONOCIDO
CONOCIDO POR RUMOR
AVISTADO
DESCUBIERTO
VISITADO
EXPLORADO.
No es necesario que todos los sistemas existentes tengan inicialmente esos
nombres exactos si ya existe otra semántica equivalente.
Adapta la arquitectura actual en vez de duplicarla.
Un rumor puede indicar aproximadamente una zona.
Un descubrimiento puede revelar una estructura.
Una visita puede revelar caminos cercanos.
La exploración puede completar detalles.
El mapa debe convertirse en memoria espacial del jugador.
8. EL MAPA CAMBIA CON EL MUNDO
Integra estado temporal.


Actualizado · 04 octubre 2026
41
DÍA:
luz y lectura clara del terreno.
ATARDECER:
cambio de iluminación.
NOCHE:
oscuridad controlada y luces de asentamientos.
LLUVIA:
atmósfera correspondiente.
NIEBLA:
visibilidad ambiental reducida cuando tenga sentido.
OTROS CLIMAS:
utiliza el sistema canónico existente.
No busques realismo cinematográfico.
Buscamos atmósfera, identidad y legibilidad.
9. REGIONES VISUALMENTE RECONOCIBLES
Cada región debe tener identidad visual coherente con su identidad narrativa.
Hoshai no puede parecer Korven.
Korven no puede parecer Edran.
Nhal no puede parecer una montaña con árboles añadidos.
Lethra debe comunicar su propia relación con el agua.
Etcétera.
Deriva estas decisiones del canon existente.
El lenguaje visual debe acompañar al lenguaje textual.
10. PERSONAJE 3D
Construye representación tridimensional del personaje.
Debe contemplar las especies jugables canónicas:
Humano
Felaryn
Dravak
Marevyn
Vesperi.
Respeta:
proporciones;
fisonomía;
postura;
rasgos culturales;


Actualizado · 04 octubre 2026
42
canon existente.
La representación debe poder reflejar cuando corresponda:
clase;
arma;
equipo relevante;
progresión visual;
objetos importantes.
Clases actuales:
Juramentado
Sombra
Arcano
Vigía
Invocador.
No necesitas convertir cada estadística en un cambio visual.
Representa aquello que tenga significado.
11. FILOSOFÍA DE MINIATURA
La representación 3D debe tener una identidad compatible con la idea histórica
de Vintage Telnet de utilizar figuras físicas.
Diseña personajes y criaturas como si pudieran existir simultáneamente como:
modelo digital
+
miniatura física.
Esto NO significa limitar el diseño por impresión 3D inmediatamente.
Significa mantener:
siluetas claras;
volúmenes comprensibles;
rasgos identificables;
poses legibles;
identidad fuerte.
Queremos que en el futuro exista una relación natural entre:
LO ENCUENTRO
→ LO CONOZCO
→ LO VEO EN 3D
→ PUEDO TENER SU FIGURA.
12. BESTIARIO 3D
Integra las criaturas canónicas existentes.
NO sustituyas el bestiario.


Actualizado · 04 octubre 2026
43
Entre otras, revisa las criaturas ya existentes en el canon.
Cada criatura debe poder disponer de:
identidad;
modelo/representación 3D;
escala;
hábitat;
estado de descubrimiento;
información conocida por el jugador.
El jugador NO recibe automáticamente todo el bestiario.
13. DESCUBRIMIENTO DE CRIATURAS
El sistema puede revelar progresivamente:
rastros;
rumores;
silueta;
avistamiento;
encuentro;
identificación;
conocimiento adicional.
No conviertas necesariamente cada una en una fase obligatoria.
Debe depender del diseño existente.
Pero evita:
entrar al juego
→ abrir bestiario
→ ver todos los monstruos.
El conocimiento debe ganarse jugando.
14. CRIATURAS EN EL MUNDO
Las criaturas deben pertenecer a ecosistemas.
El 3D no corrige una criatura narrativamente mal colocada.
Integra:
hábitat;
región;
hora;
clima;
comportamiento;
rareza;
rastros;
presagio.
Cuando el jugador vea finalmente la criatura en 3D, debe reforzar algo que la
narración ya estaba construyendo.


Actualizado · 04 octubre 2026
44
15. HITOS 3D
Representa tridimensionalmente lugares cuando aporten valor espacial o cultural.
Ejemplos conceptuales:
Vaisgard;
pueblos;
forjas importantes;
ruinas;
mazmorras;
puentes;
torres;
puertos;
pasos de montaña;
estructuras únicas;
hogares importantes.
NO modeles cada habitación.
La lectura sigue encargándose del detalle fino.
El 3D ayuda a entender:
escala;
posición;
forma;
identidad;
memoria.
16. TERMINAL Y 3D
NO reemplaces la terminal.
Debe continuar siendo protagonista.
Diseña una navegación coherente entre:
AVENTURA
MAPA
PERSONAJE
BESTIARIO
y cualquier sección ya existente que deba conservarse.
En móvil, no intentes mostrarlo todo simultáneamente.
En escritorio puedes aprovechar mejor el espacio, pero no conviertas la terminal
en una pequeña ventana secundaria.
17. GRAMÁTICA NARRATIVA
La integración 3D NO sustituye la mejora narrativa.
Vintage Telnet debe conservar y profundizar:


Actualizado · 04 octubre 2026
45
IDENTIDAD DEL LUGAR
+
TRANSICIÓN GEOGRÁFICA
+
HORA
+
CLIMA
+
MICROVIDA
+
FAUNA
+
CULTURA
+
PRESAGIO
+
PELIGRO
+
MEMORIA
+
DESCUBRIMIENTO.
El jugador debe reconocer aproximadamente una región incluso si eliminamos
el encabezado con su nombre.
18. TRANSICIONES
Evita:
A → A → A → A → B.
Busca:
A → AB → B → BC → C.
La narración debe mostrar cómo:
cambia el suelo;
cambia la vegetación;
cambia la arquitectura;
cambian los sonidos;
cambia la fauna;
cambia el clima local;
cambia la actividad.
El mapa 3D debe reforzar la misma transición espacial.
19. MICROVIDA
El mundo continúa existiendo sin esperar al jugador.
Utiliza microeventos:


Actualizado · 04 octubre 2026
46
animales;
habitantes;
oficios;
viajeros;
carromatos;
sonidos;
trabajo;
insectos;
vegetación;
actividad comercial;
fenómenos ambientales.
No todo ofrece XP.
No todo ofrece loot.
No todo inicia una misión.
A veces mirar algo ES la recompensa.
20. COLOR SEMÁNTICO DE LA TERMINAL
Mantén un lenguaje cromático consistente.
VERDE FÓSFORO:
mundo y narración.
VERDE BRILLANTE:
lugares y encabezados relevantes.
CIAN:
acción del jugador.
AMARILLO / ÁMBAR:
descubrimiento, rastro, botín, victoria, XP, progreso.
ROJO / SALMÓN:
peligro y amenaza.
NARANJA:
combate, daño y consecuencias físicas.
TONOS APAGADOS:
información secundaria.
No colorees aleatoriamente.
El jugador debe aprender el significado del color inconscientemente.
21. SISTEMA SEMÁNTICO
Evita hardcodear colores dentro de textos.
Utiliza categorías semánticas como:
WORLD
LOCATION


Actualizado · 04 octubre 2026
47
PLAYER_ACTION
NPC
DISCOVERY
TRACE
DANGER
COMBAT
REWARD
PROGRESSION
SYSTEM
MAGIC
o una solución equivalente compatible con la arquitectura existente.
La terminal decide cómo representar cada categoría.
22. 3D Y COLOR DEBEN COMPARTIR IDENTIDAD
No construyas una interfaz 3D brillante y moderna desconectada de la terminal.
Debe sentirse Vintage Telnet.
Busca:
oscuridad;
materiales sobrios;
atmósfera;
iluminación contenida;
sensación de maqueta;
detalles selectivos;
acentos luminosos con significado.
Evita:
neón indiscriminado;
UI futurista genérica;
fantasía móvil genérica;
hiperrealismo;
estética Fortnite;
estética MMORPG genérica.
23. RENDIMIENTO
Vintage Telnet debe seguir funcionando razonablemente en:
PC;
navegador;
móvil;
infraestructura actual del proyecto.
La Raspberry es servidor y no debe convertirse innecesariamente en renderer 3D.
El render ocurre en el cliente cuando corresponda.
Implementa:


Actualizado · 04 octubre 2026
48
lazy loading;
carga bajo demanda;
reutilización de geometrías/materiales;
niveles de detalle cuando aporten valor;
dispose correcto de recursos;
compresión apropiada;
cache;
límites razonables de polígonos;
texturas optimizadas.
No cargues el bestiario completo para mostrar la terminal.
24. FORMATO DE ASSETS
Define una convención definitiva para assets 3D.
Cuando sea adecuado para web, prioriza estándares compatibles con Three.js,
como glTF/GLB.
Define:
rutas;
nombres;
versionado;
metadatos;
escala;
orientación;
pivotes;
materiales;
miniaturas;
fallbacks.
NO permitas que cada agente futuro invente su propio formato.
25. FALLBACK
El juego debe seguir siendo jugable si:
WebGL/WebGPU falla;
el dispositivo es lento;
el modelo no carga;
falta temporalmente un asset 3D.
El 3D enriquece Vintage Telnet.
No debe convertirse en un punto único de fallo.
26. ACCESIBILIDAD
El color nunca debe ser la única forma de transmitir información.
Mantén etiquetas como:
[Peligro]
[Descubres]


Actualizado · 04 octubre 2026
49
[Victoria]
[Botín]
cuando sean útiles.
Contempla:
modo sin color;
contraste;
reducción de movimiento;
3D desactivable si el dispositivo o usuario lo necesita.
27. NO INVENTES ASSETS FALSOS
Si actualmente no existe el modelo definitivo de una criatura o personaje:
NO presentes un cubo como solución final.
NO declares terminada la criatura con placeholder.
NO uses assets genéricos de fantasía y los llames canon.
Construye correctamente el pipeline necesario y registra claramente qué asset
canónico necesita producción.
La arquitectura puede quedar completa aunque un asset artístico concreto requiera
su proceso de generación/aprobación.
Pero una representación provisional NO equivale a contenido terminado.
28. PIPELINE DE CONTENIDO
El objetivo es que añadir en el futuro:
una criatura;
una región;
un pueblo;
un arma;
un hito
NO requiera reprogramar Three.js manualmente.
Diseña un pipeline basado en datos/metadatos.
Nuevo contenido canónico
→ registro
→ asset
→ metadata
→ mundo
→ terminal
→ mapa/bestiario/personaje cuando corresponda.
29. NO DUPLICAR CANON
Historiador, Narrador, Jugabilidad y Arte ya producen contenido.
La nueva capa debe CONSUMIR ese contenido.


Actualizado · 04 octubre 2026
50
No crear otro canon llamado:
"canon3D".
Si encuentras contradicciones, documéntalas y resuélvelas siguiendo la autoridad
canónica existente.
30. NO ROMPER SISTEMAS EXISTENTES
Conserva:
combate;
economía;
sellos;
salvage;
comida;
raciones;
tiendas;
forjas;
reparaciones;
clases;
especies;
NPCs;
encargos;
progresión;
hogares;
respawn;
clima;
día/noche;
mapa;
exploración;
criaturas;
mazmorras;
rutas;
y demás sistemas existentes.
La integración debe enriquecerlos.
No simplificarlos para hacer más fácil el 3D.
31. NO PROTOTIPOS
REGLA ABSOLUTA:
No entregues:
"prototipo de mapa";
"primera demo";
"ejemplo con un monstruo";
"POC";
"mock";
"versión temporal";
"dejamos preparado para después";


Actualizado · 04 octubre 2026
51
"esto demuestra que funciona".
Implementa SISTEMAS.
Si desarrollas Bestiario 3D, debe ser un sistema capaz de manejar el bestiario.
Si desarrollas mapa 3D, debe representar el mundo mediante datos reales.
Si desarrollas personaje 3D, debe contemplar las especies/clases previstas por
la arquitectura.
Una funcionalidad que sólo funciona con un ejemplo hardcodeado NO está terminada.
32. TAMPOCO HAGAS UN BIG BANG CIEGO
"Todo de golpe" NO significa escribir miles de líneas sin validar.
Internamente puedes realizar commits pequeños, pruebas y checkpoints.
Pero todos pertenecen a UNA SOLA INTEGRACIÓN DEFINITIVA.
No abandones subsistemas a mitad para comenzar otros experimentos.
Cada paso debe converger hacia la arquitectura final.
33. BUCLE AUTÓNOMO DE CALIDAD
Tu trabajo NO termina cuando compila.
Utiliza continuamente:
INSPECCIONAR
→ IMPLEMENTAR
→ EJECUTAR
→ JUGAR
→ EVALUAR
→ CORREGIR
→ VOLVER A JUGAR.
No esperes a que Javier encuentre todos los problemas.
Debes jugar el sistema.
34. RECORRIDOS DE PRUEBA
Realiza recorridos reales suficientemente largos.
Incluye:
hogar
→ camino
→ asentamiento
→ salida
→ transición regional
→ naturaleza
→ otro asentamiento


Actualizado · 04 octubre 2026
52
→ comercio
→ exploración
→ encuentro
→ combate
→ regreso.
Comprueba simultáneamente:
terminal;
estado;
mapa;
descubrimientos;
clima;
hora;
posición;
bestiario;
progresión.
35. PRUEBA DE 20-30 MINUTOS
El juego debe soportar al menos una sesión de recorrido de 20-30 minutos en la
que el jugador tenga curiosidad por continuar incluso sin seguir una misión
principal constantemente.
No significa añadir encuentros artificiales cada minuto.
Significa que:
espacio;
atmósfera;
cambio;
descubrimiento;
presagio;
vida;
geografía
mantienen interés.
36. EVALUACIÓN NARRATIVA
Puntúa de 1 a 5:
IDENTIDAD ESPACIAL
CONTINUIDAD
RITMO
VIDA AMBIENTAL
DENSIDAD SENSORIAL
IDENTIDAD REGIONAL
TIEMPO Y CLIMA
EXPLORACIÓN
ENCUENTROS
MEMORIA


Actualizado · 04 octubre 2026
53
COLOR SEMÁNTICO
CURIOSIDAD
Todo debe alcanzar al menos 4/5 antes de considerar terminada esta integración.
No infles las notas.
37. EVALUACIÓN 3D
Añade:
LECTURA GEOGRÁFICA
¿El mapa ayuda realmente a comprender el mundo?
COHERENCIA 2D/3D
¿Lo que leo coincide con lo que veo?
DESCUBRIMIENTO
¿El 3D respeta lo que conozco y desconozco?
IDENTIDAD VISUAL
¿Regiones y criaturas son reconocibles?
UTILIDAD
¿El 3D aporta información/emoción y no solamente espectáculo?
RENDIMIENTO
¿Funciona razonablemente en móvil y escritorio?
INTEGRACIÓN
¿Parece parte de Vintage Telnet y no una aplicación incrustada?
Todas >= 4/5.
38. CONSTRUCTOR Y CRÍTICO
Cuando sea posible, separa mentalmente dos funciones:
CONSTRUCTOR:
implementa.
CRÍTICO:
intenta demostrar que la implementación todavía es mediocre.
Después:
CRÍTICO
→ defectos
→ CONSTRUCTOR
→ corrección
→ CRÍTICO.
No evalúes algo positivamente sólo porque tú mismo lo escribiste.


Actualizado · 04 octubre 2026
54
39. TESTS
Añade pruebas donde aporten valor.
Especialmente para:
estado compartido;
descubrimientos;
visibilidad del mapa;
persistencia;
especies;
equipamiento;
bestario;
clima;
hora;
rutas;
fallbacks;
carga de assets;
errores de render;
móvil.
Las pruebas automáticas NO sustituyen jugar.
40. DOCUMENTACIÓN
Documenta la arquitectura definitiva.
Un futuro agente debe poder entender:
cómo añadir una criatura;
cómo añadir una región;
cómo añadir un modelo;
cómo registrar un hito;
cómo funciona el mapa;
cómo funciona descubrimiento;
cómo se sincroniza estado;
cómo funcionan los tokens narrativos;
cómo funcionan assets 3D;
cómo probarlo.
No dependas de que este chat siga existiendo.
41. DEUDA TÉCNICA
Si encuentras código anterior que hace imposible integrar correctamente esta
arquitectura, refactoriza cuando sea necesario.
No construyas encima de una mala abstracción solamente para reducir el diff.
Pero tampoco reescribas sistemas estables sin motivo.
Cada refactor debe servir a la integración.


Actualizado · 04 octubre 2026
55
42. AUTONOMÍA
No preguntes constantemente:
"¿quieres que haga el mapa ahora?"
"¿continuamos con bestiario?"
"¿hago personaje?"
La respuesta ya es SÍ.
Todo forma parte del alcance.
Toma decisiones técnicas razonables y continúa.
Pregunta únicamente cuando:
se requiera cambiar canon;
existan dos decisiones creativas incompatibles de gran impacto;
sea necesaria una credencial/servicio externo;
una acción sea irreversible o peligrosa;
falte información que realmente impida continuar.
43. NO DETENERSE POR UN ASSET
Si falta arte:
continúa desarrollando las demás partes del sistema.
Registra claramente el bloqueo artístico.
No detengas toda la integración porque todavía falte un GLB.
Pero tampoco declares terminado el contenido afectado.
44. DEFINICIÓN DE TERMINADO
Esta integración NO está terminada porque:
Three.js renderiza;
aparece un modelo;
el mapa gira;
hay una criatura;
pasan tests;
funciona en tu máquina.
Está terminada cuando:
Vintage Telnet sigue siendo plenamente jugable;
la terminal narrativa continúa siendo protagonista;
el mundo conserva su escala;
el recorrido tiene densidad narrativa;
el mapa 3D representa el mundo real;
descubrimientos modifican lo que puede verse;


Actualizado · 04 octubre 2026
56
personaje y especies tienen arquitectura 3D coherente;
el bestiario 3D está integrado al conocimiento del jugador;
hora y clima afectan texto y representación;
móvil funciona razonablemente;
no existe un segundo estado paralelo;
los fallos 3D no destruyen el juego;
el pipeline permite ampliar contenido;
la documentación permite continuar el proyecto;
y la experiencia completa parece UN SOLO JUEGO.
45. PRINCIPIO ARTÍSTICO FINAL
No queremos impresionar al jugador diciendo:
"Mira, tenemos Three.js."
Queremos que después de caminar por Hoshai, descubrir una criatura, regresar a
Vaisgard y abrir el mapa, piense:
"Ah. Ahora entiendo dónde estuve."
Y cuando abra el bestiario:
"Ésa era la cosa que llevaba rato sintiendo entre las piedras."
Y cuando vea su personaje:
"Éste es mi personaje en ese mundo."
El 3D debe aumentar la imaginación provocada por el texto.
Nunca sustituirla.
46. ORDEN DE EJECUCIÓN
Empieza ahora.
1. Inspecciona repositorio y arquitectura.
2. Identifica las fuentes de verdad actuales.
3. Diseña internamente la arquitectura definitiva de integración.
4. Detecta incompatibilidades y deuda necesaria.
5. Implementa la capa semántica/narrativa necesaria.
6. Integra Three.js correctamente.
7. Construye el sistema de mapa mundial 3D.
8. Integra descubrimiento y conocimiento.
9. Integra hora y clima.
10. Construye sistema de personaje 3D.
11. Construye sistema de bestiario 3D.
12. Integra hitos.
13. Completa pipeline de assets/metadatos.


Actualizado · 04 octubre 2026
57
14. Optimiza móvil/escritorio.
15. Implementa fallbacks/accesibilidad.
16. Ejecuta pruebas técnicas.
17. Juega recorridos reales.
18. Evalúa narrativa y 3D.
19. Corrige.
20. Repite hasta superar criterios.
21. Documenta.
22. Entrega la integración completa para revisión.
Estos números indican dependencias lógicas.
NO son veinte prototipos ni veinte entregas independientes.
Son una sola transformación de Vintage Telnet.
MANDATO FINAL
NO HAGAS UNA DEMO DE LO QUE VINTAGE TELNET PODRÍA SER.
CONSTRUYE VINTAGE TELNET.
Conserva la escala y profundidad que ya tenemos.
Añade la densidad narrativa que descubrimos que faltaba.
Añade una dimensión visual 3D que permita comprender y coleccionar mentalmente
el mundo.
Une texto, geografía, criaturas, personajes, clima, descubrimiento y progresión
bajo un único estado.
Itera hasta que funcione Y hasta que se sienta bien.
No rellenes pantallas.
No acumules features.
CONSTRUYE UN MUNDO.
LA LECTURA ES EL MUNDO.
EL 3D LO MATERIALIZA.
EL SERVIDOR DECIDE QUÉ ES VERDAD.
EL JUGADOR DESCUBRE EL RESTO.
NOTA EDITORIAL DE COMPATIBILIDAD
[Nota editorial: el bloque anterior se incorpora íntegro. Su apartado 22 propone oscuridad,
materiales sobrios e iluminación contenida para el 3D; las secciones 4 y 7 piden arte anime
muy colorido e interfaz moderna. Su apartado 16 permite aprovechar más el espacio de
escritorio; la sección 4 exige conservar las proporciones de celular también en computadora.
Estas indicaciones requieren armonización o una decisión explícita del Arquitecto antes de
cambiar la dirección visual o la disposición aprobada. Se conservan ambas formulaciones, sin
resolver silenciosamente estas tensiones. La capa 3D sí queda incorporada al alcance por
este nuevo bloque.]
