# VT-RES-001 — Inicio y progresión temprana en juegos Telnet/MUD

**Solicitante:** Narrador de Aventuras — Vintage Telnet
**Estado:** INVESTIGACIÓN ENTREGADA
**Fecha:** 2026-09-20
**Consumidores:** Narrador, Diseñador de Jugabilidad, Historiador y Arquitecto.

## PROBLEMA
Investigar cómo los MUD/Telnet clásicos y sus descendientes resolvían el comienzo de un personaje débil: salir a explorar, encontrar criaturas sencillas, aprender combate, percibir peligro, regresar/recuperarse, progresar y cooperar sin que las primeras horas se reduzcan a repetir una misma muerte de enemigos.

No se diseña aquí la aventura inicial de Vintage Telnet ni se fijan reglas nuevas.

## ESTADO ACTUAL DE VINTAGE TELNET
GAMEPLAY.md ya confirma: RPG de progresión; clase inicial flexible; mundo persistente; movimiento Telnet cardinal; mapa con descubrimiento; monstruos comunes que reaparecen y monstruos principales persistentes; multijugador textual; PvP; protección ante diferencias extremas de poder; combate semi-automático con intervención estratégica; derrota sin borrado permanente del personaje.

El Narrador ha pedido que los primeros jugadores (Marcos, Matías y Javier) comiencen débiles y una de sus primeras actividades sea salir al campo a fortalecerse con criaturas débiles.

## PRÁCTICAS HISTÓRICAS OBSERVADAS

### 1. El mundo se entendía como una red de habitaciones, no como un mapa que lo explicaba todo
MUD1 nació como una serie de localizaciones interconectadas donde los jugadores podían moverse y conversar. La versión histórica conservada muestra habitaciones descritas en texto y comandos de movimiento. Su ayuda para principiantes da prioridad a LOOK, EXITS, inventario, puntuación y direcciones.

DikuMUD formalizó esta tradición: cada habitación tiene título, descripción y salidas; entrar o usar LOOK revela el lugar. Además, el terreno puede tener distintos costos de movimiento.

**Ventaja:** explorar ya es una actividad: leer, orientarse y decidir una salida.
**Problema envejecido:** descripciones demasiado largas o salidas poco claras pueden convertir orientación en frustración.

### 2. Las zonas iniciales reducían el riesgo de perderse sin eliminar la exploración
El manual de BatMUD de 1995 describe Digga's newbie area como un lugar deliberadamente difícil de perder: si el jugador se confunde, puede avanzar hacia el este hasta regresar a la entrada. Al mismo tiempo debe caminar y localizar criaturas.

BatMUD moderno sigue premiando descubrir habitaciones con experiencia de exploración y advierte que las áreas desconocidas pueden ser peligrosas. Achaea mantiene áreas reservadas para novatos y recomienda comenzar explorando para abrir oportunidades, quests y encuentros.

**Ventaja:** el jugador aprende navegación real pero conserva una salida comprensible.
**Problema envejecido:** un área totalmente aislada y artificial puede sentirse como tutorial separado del mundo.

### 3. No todas las criaturas débiles eran iguales
El manual histórico de BatMUD recomienda empezar con ranas, patos o conejos, pero evitar hormigas y ciervos inicialmente. Achaea utiliza CONSIDER/PROBE para estimar la fuerza de criaturas. Su sistema de ratas contiene varios tipos con fuerza/valor creciente, y la caza temprana convive con otras criaturas y quests.

**Ventaja:** crea lectura del mundo, elección de riesgo y aprendizaje por observación.
**Problema envejecido:** si las diferencias solo se descubren muriendo sin señales, se vuelve prueba y error punitiva.

### 4. El combate podía iniciarse con una orden y continuar automáticamente
BatMUD documenta rondas de combate: KILL u otra acción ofensiva inicia la pelea y los ataques con armas continúan automáticamente; durante el combate el jugador puede usar habilidades/hechizos, vigilar salud o huir. Esto se parece al principio ya confirmado de Vintage Telnet.

**Ventaja:** pocos comandos iniciales, ritmo textual legible y espacio para decisiones importantes.
**Problema envejecido:** si el jugador solo escribe KILL y espera, la repetición se vuelve pasiva.

### 5. La retirada era parte del aprendizaje
El manual de BatMUD recomienda configurar “wimpy” para retirarse automáticamente con poca salud y huir manualmente si se agotan recursos. También advierte que algunos monstruos pueden perseguir al jugador.

**Ventaja:** enseña evaluación de riesgo y permite que un encuentro peligroso produzca historia aunque no termine en victoria.
**Problema envejecido:** una huida automática opaca puede quitar agencia si el jugador no entiende por qué ocurrió.

### 6. El combate débil se mezclaba con economía, exploración y encargos
Achaea convirtió “ratting” en una actividad económica: matar ratas, conservar cadáveres y entregarlos a compradores por oro. Sus áreas de novatos también incluyen quests y recomiendan explorar y saludar habitantes para descubrir oportunidades. BatMUD concede experiencia por exploración y combina áreas, quests y progresión.

**Ventaja:** una misma salida al campo puede producir combate + hallazgo + objeto + información + regreso.
**Problema envejecido:** repetir indefinidamente la criatura de mejor rendimiento puede convertirse en grind si la economía recompensa una sola rutina.

### 7. Los otros jugadores eran parte del tutorial
Los MUD son mundos compartidos desde su origen. Achaea conserva canal de novatos, mentores y cooperación; BatMUD permite formar parties para combatir enemigos mayores o hacerlo con más eficacia.

**Ventaja:** varios principiantes pueden aprender juntos sin necesitar tutoriales individuales.
**Problema envejecido:** depender de veteranos conectados para explicar sistemas esenciales deja mal atendido a quien juega solo.

## EJEMPLOS CONCRETOS

### MUD1 / British Legends
- Unidad de mundo: habitación textual conectada por salidas.
- Comandos compactos: LOOK, EXITS, GET, DROP, KILL, FLEE, INVENTORY, SCORE y direcciones.
- Exploración y conversación multiusuario están en el núcleo histórico.

### BatMUD
- Área inicial con una regla espacial sencilla para volver a la entrada.
- Diferentes criaturas tempranas, algunas recomendadas y otras a evitar.
- CONSIDER ayuda a valorar riesgo.
- Combate automático por rondas después de iniciarlo.
- FLEE/wimpy y recuperación forman parte de aprender a sobrevivir.
- Exploración puede dar experiencia.

### Achaea
- Áreas protegidas para novatos.
- Exploración recomendada para descubrir quests y oportunidades.
- Ratting combina enemigo débil con economía.
- CONSIDER/PROBE comunica fuerza relativa.
- Canales/mentores y cooperación acompañan la entrada al mundo.

## QUÉ PARECE HABER ENVEJECIDO BIEN
- Habitaciones breves con identidad y salidas comprensibles.
- Comandos pequeños y reutilizables.
- Aprender haciendo dentro del mundo.
- Señales para estimar peligro.
- Posibilidad real de retirarse.
- Variar recompensas: experiencia, dinero, objetos, información y descubrimiento.
- Progresión por exploración además de combate.
- Cooperación espontánea.
- Regreso sencillo a una zona segura.

## QUÉ PARECE HABER ENVEJECIDO MAL
- Memorizar demasiados comandos antes de jugar.
- Zonas iniciales que parecen una sala de tutorial ajena al mundo.
- Grind de una criatura óptima durante horas.
- Castigos fuertes por una muerte ocurrida mientras todavía se aprende la interfaz.
- Peligro invisible que solo se aprende muriendo.
- Esperas largas de regeneración sin decisiones.
- Dependencia absoluta de guías externas o jugadores veteranos.
- Texto excesivo y spam de combate que oculta la información importante.

## IDEAS ADAPTABLES A VINTAGE TELNET SIN COPIAR LITERALMENTE
Estas son patrones para que otros especialistas evalúen, no reglas aprobadas:

1. Un conjunto de caminos iniciales conectado al pueblo donde alejarse sea una decisión visible y regresar sea comprensible.
2. Varias familias de criaturas tempranas con señales narrativas de peligrosidad, no una sola criatura repetida.
3. Combinar las salidas de entrenamiento con pequeños descubrimientos: rastros, objetos, rumores, lugares, cambios de terreno o rutas.
4. Dar valor a LOOK/EXITS y a un posible equivalente de CONSIDER para que leer el mundo sea parte del juego.
5. Hacer que retirarse y regresar al pueblo sea una decisión válida.
6. Permitir que tres principiantes que viajan juntos encuentren motivos para cooperar, no solo sumar daño.
7. Evitar que la recompensa óptima sea permanecer inmóvil matando la misma criatura que reaparece.
8. Mantener tutoriales/hints como ayuda discreta y contextual, no como explicación completa del mundo.

## DECISIONES QUE CORRESPONDEN A JUGABILIDAD
- Si existirá un comando o indicador equivalente a CONSIDER.
- Fórmula de dificultad y señales exactas de fuerza.
- Recompensas por exploración y combate.
- Curación, descanso y regeneración.
- Reglas de huida.
- Penalización de derrota temprana.
- Reaparición y distribución de criaturas comunes.
- Reglas de grupo/party y reparto de recompensas.
- Límites de áreas de novatos, si existen.
- Qué parte del combate será automática y qué acciones estratégicas estarán disponibles.

## OPORTUNIDADES PARA EL NARRADOR
- Enseñar peligro mediante descripción, huellas, sonidos, cadáveres, viajeros que regresan heridos o cambios de ambiente.
- Hacer que los primeros combates revelen información sobre el lugar.
- Usar el camino de regreso como parte de la experiencia, no como tiempo muerto.
- Colocar pistas y pequeños hallazgos entre encuentros para que explorar sea tan importante como combatir.
- Diseñar situaciones donde varios jugadores se avisen de un hallazgo o se ayuden a escapar.
- Evitar convertir el inicio en una lista explícita de “mata 10 X” salvo que exista una razón narrativa fuerte.

## NECESIDADES PARA EL HISTORIADOR
El Historiador puede decidir, sin que esta investigación lo haga por él:
- qué criaturas débiles existen en cada región inicial;
- qué comportamiento visible permite intuir su peligrosidad;
- qué restos, rastros o recursos dejan;
- qué relación tienen con cada pueblo y su entorno;
- qué amenazas mayores pueden percibirse temprano sin estar destinadas a ser vencidas todavía.

## RECOMENDACIÓN TÉCNICA PARA FUTURAS IMPLEMENTACIONES
Cuando Desarrollo llegue a esta etapa, conviene investigar una separación de datos entre habitaciones/salidas, criaturas, combate, recompensas, descubrimientos, estado persistente del jugador y estado persistente del mundo. Así Narrador podrá colocar descubrimientos o consecuencias sin convertir cada evento en código especial, y Jugabilidad podrá ajustar reglas sin reescribir contenido.

Esto es una recomendación de estructura a investigar con más detalle, no una implementación aprobada.

## PRUEBA PROPUESTA
Antes de construir un mapa grande, probar una microzona de 8–15 habitaciones conectada a un pueblo con 3 tipos de criatura de riesgo diferente, una ruta clara de regreso, al menos un hallazgo que no dependa de matar, un encuentro que invite a huir, una razón para cooperar y un cambio persistente sencillo.

Observar si un jugador nuevo puede descubrir qué hacer principalmente mediante el mundo y comandos básicos.

## FUENTES
- MUD1, historia del port del código original: https://core.mud1.org/CMS/about-mud1-bl/history
- MUD1/British Legends, consejos y comandos: https://british-legends.com/CMS/index.php/help/more-advice
- Código fuente histórico MUD1 (1986): https://github.com/PDP-10/MUD1
- Richard Bartle, historia temprana de MUD: https://www-old.caida.org/projects/iec/courses/ife97/lectures/MUD-history.html
- DikuMUD, manual de habitaciones: https://wiki.dikumud.com/wiki/Manual%3AZone_Manual/The_Room_Section
- BatMUD, Beginner's Handbook (1995): https://www.bat.org/community/library?str=80
- BatMUD, ayuda oficial de combate: https://www.bat.org/help/help?htype=extra&str=combat
- BatMUD, quickstart/exploración: https://www.bat.org/help/help?htype=basic&str=quickstart
- Achaea, guía oficial para principiantes: https://www.achaea.com/newbie-guide
- Achaea, ayuda oficial “What to do now”: https://newclient.achaea.com/game-help?what=what-to-do-now
- AchaeaWiki, Newbie Guide: https://wiki.achaea.com/Newbie_Guide

## CONCLUSIÓN PARA EL NARRADOR
La lección histórica más consistente no es “poner monstruos débiles”. Es poner monstruos débiles dentro de un espacio que el jugador necesita leer y explorar. Los patrones encontrados mezclan combate con orientación, evaluación del peligro, retirada, economía, descubrimientos y presencia de otros jugadores. El combate repetido puede existir como una vía de fortalecimiento, pero deja de sentirse como tarea cuando cada salida también puede enseñar algo sobre el mundo.
