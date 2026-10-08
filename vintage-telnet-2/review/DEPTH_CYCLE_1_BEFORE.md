# Ciclo 1 — jugar y criticar geografía y viaje, antes

Evaluación de un agente, no una sesión humana ni una prueba visual del cliente. Se leyó el canon actualizado, apartados de geografía y evaluación de recorridos; no se reutilizó prosa de versiones antiguas. Fecha: 2026-10-06. No se modificó contenido ni motor durante esta investigación.

## Sesiones reproducibles

`python3 scripts/depth-cycle-1-travel.py` usa API Flask real, creación/aprobación de personajes temporales, movimientos legales, permisos de entrada, observación y regreso al hogar. Cada personaje tiene base de datos temporal destruida al salir. No toca runtime/world.sqlite3 ni cuentas reales. El reloj avanza un minuto por acción desde mediodía. Las rutas se escogen en el grafo existente; no hay teletransporte.

- A: hogar humano → Valdren → ruta de Tierra Húmeda → Narevia → Ribera Sombría → Velmora → regreso por la misma ribera y campos → Valdren → hogar. 40 movimientos reales y tres observaciones.
- B: hogar Felaryn → Khariel → Paso de las Lajas → Brumak → Senda del Viento Bajo → Valdren → Camino de los Campos → Vaisgard → Camino Alto → Khariel → hogar. 57 movimientos reales, tres observaciones y dos permisos. Es un circuito distinto de A, no una extensión del mismo camino.

Se leyeron consecutivamente los eventos de ambos recorridos, incluidos bloques de 8–12 movimientos y los retornos. Evidencia íntegra: `review/depth-cycle-1/travel-before.json`. Las muestras aquí omiten nombres geográficos; los IDs de la evidencia se conservan para poder rejugar exactamente.

La primera pasada usa RNG=0 para exponer fauna siempre que el sistema permite generarla: es deliberadamente adversa, no representa frecuencia estadística de producción. Una segunda pasada con RNG=0.9 recorrió las MISMAS dos rutas sin generar fauna aleatoria: `travel-quiet-before.json`. Así se distingue repetición causada por encuentros de repetición inherente al paseo. No hubo combate, compra ni misión en este ciclo; esos aspectos necesitan otros ciclos. Las observaciones prueban exploración sin premio.

## Lo mejor

La transformación de Lethra hacia Nhal sí funciona. El canal pierde reflejos bajo hojas, se estrecha entre raíces, aparecen notas de nivel del agua y después una senda elevada con helechos. Hay AB entre A y B. La ruta de Hoshai a Korven también conserva un hilo material: agujas de pino entre cascajo, polvo sobre cubiertas y roca cada vez más expuesta. Los tamaños de puertas y apoyos distinguen Brumak de Khariel sin caricaturizar a sus habitantes. El canon ambiental ya sirve de fundamento real.

## Lo más débil y el punto de aburrimiento

El regreso repite tareas completas como si cada vecino siguiera congelado durante todo el viaje. En A, 7 de 19 retornos repiten exactamente todos los textos de su primera visita; en B, 6 de 11. Sin fauna aleatoria siguen siendo 4/19 y 1/11. Algunas memorias funcionan muy bien: la acequia, la plaza humana y la terraza de cargas recuperan referencias aprendidas. El problema no es ausencia total de memoria, sino su acceso inconsistente.

El aburrimiento llega antes de salir de la sierra: en los primeros 11 movimientos después de la plaza, nueve incluyen exactamente «Un Saltacresta salta entre dos piedras y mira hacia la ladera antes de seguir». La misma frase aparece 16 veces en B completo. En A, tres salas contiguas de bosque muestran la misma señal de pelo con musgo; se repite seis veces contando regreso. No basta cambiar los nombres de criaturas si el sistema sigue mostrando una instancia regional indistinguible en cada sala.

## Plantilla perceptible

Las descripciones espaciales suelen ser claras. La plantilla se nota más en el cierre de la actividad cotidiana: una persona ajusta una carga, otra deja libre un paso y una tercera frase explica la corrección social de la escena. Muestras sin nombres:

> Una vecina reconoce su cesta por el asa remendada y la levanta antes de que llegue otra carga. Un niño devuelve una que tomó su familia. Nadie necesita fijar un precio nuevo para recordar esa relación.

> Una pastora recoge lana atrapada en una rama baja sin perseguir al rebaño entre las piedras. Se queda donde puede ver el aprisco. La altura le da perspectiva, pero no control sobre todo lo que se mueve.

Estas escenas tienen detalles buenos; sus explicaciones finales interrumpen la lectura del mundo para enseñarme cómo debo interpretarlo. Otras escenas cortas —aves y silencio entre ramas, la corriente dividida por una losa— respiran mejor. No conviene sustituir todas las actividades por un nuevo patrón.

## Prueba ciega de región y de continuidad

Muestras originales, eliminando encabezados y nombres:

> Los apoyos se separan conforme te alejas [...]. Bajo una cubierta común puedes ajustar las envolturas. Los viajeros de los llanos retiran de sus pies tierra distinta al barro del canal.

Identificable como borde de región acuática; todavía comparte mucho vocabulario de cargas con cualquier otra ruta.

> Un pino aislado crece entre piedras partidas, con la copa doblada por el viento. Sus raíces sujetan un poco de tierra. [...] Entre las marcas de los viajeros hay huellas que rodean el árbol.

Identificable como collado montañoso incluso sin geografía.

> Las casas [...] tienen puertas bajas; el paso público deja más altura. [...] Bancos y cargas dejan libre el giro de los carros.

Identidad arquitectónica reconocible; la actividad posterior de mover un banco para pasar un carro sí podría intercambiarse con tres plazas.

Hay un defecto específico de orientación: saliendo de Khariel hacia el sur, `hoshai_escalones_sol` empieza «Subes por escalones», y `hoshai_ladera_hitos` empieza «Subes por una ladera abierta», aunque el personaje baja de la plaza hacia el collado y los textos enlazados presentan la plaza como destino superior. El mismo texto sirve para ambas direcciones. Durante TODOS los 97 movimientos, ninguna arista utilizada tenía una capa `arrivals` efectiva. El motor ya permite llegada según habitación de origen; el catálogo no la aprovecha en estas rutas. La descripción mantiene referencias de salida, pero la acción de viajar no siempre mantiene su dirección física.

## Sistema infrautilizado y contenido canónico invisible

El sistema `return` existe en los 30 retornos de habitaciones públicas medidos. Sólo 12 de esas 30 frases aparecen en narrativa con RNG=0 (A:8/19; B:4/11). La prioridad `danger,memory,arrival,activity,weather,people,return`, con descripción contada en `max_layers=3`, deja el reconocimiento al final. Dos capas anteriores bastan para expulsarlo. Este es un mecanismo observado, no una hipótesis estética.

`arrivals` puede introducir orientación y anticipación sin arquitectura nueva. `focus` puede decidir qué escena importa. No se propone aumentar todas las capas: eso añadiría fatiga.

No encontramos los cinco nombres canónicos de pequeños lugares de camino en el catálogo: Refugio de Lajas, Parada de los Cardos, Vado de Juncos, Orilla Velada y Alto de las Raíces. Los recorridos sí pasan por abrigos y plataformas con función parecida, pero estos lugares canónicos no se reconocen ni como hito visible. Tampoco aparecen los nombres canónicos de las rutas periféricas en las muestras leídas. No afirmamos ausencia universal de su función ni que deban convertirse en hubs. Lo mínimo útil sería reconocer un refugio existente mediante su señal/uso y una transición propia, preservando su escala.

En Vaisgard se ven muros y piedras antiguos, pero la profundidad de sus reparaciones de distintas épocas y su origen incierto no despiertan una pregunta en este trayecto de mercado/plaza. Este paseo no pasó por zonas inferiores: no acredita su inexistencia.

## Valoración honesta (1–5)

| Criterio | Antes | Evidencia/limitación |
|---|---:|---|
| Identidad espacial | 4 | Apoyos, curvas, agua, puertas y alturas legibles |
| Continuidad | 3 | Transiciones graduales buenas; verbos de subida contradicen descenso |
| Ritmo | 2 | Tareas constantes y fauna idéntica; poca verdadera pausa |
| Vida ambiental | 3 | Actividades materiales creíbles, pero retorno congela escenas |
| Densidad sensorial | 4 | Suelo/agua/luz/sonido y arquitectura suficientes |
| Identidad regional | 4 | Cinco ambientes se distinguen; actividades sociales demasiado similares |
| Tiempo y clima | 3 | Lluvia de Korven altera apoyos y barro; sólo mediodía observado |
| Exploración | 3 | Observar descubre detalle, repite primero la actividad ya leída |
| Encuentros | 2 | Hábitat coherente, señales repetidas y fauna inocua siempre como danger |
| Memoria | 2 | 18/30 retornos con frase disponible pero invisible en pasada adversa |
| Color semántico | — | API conserva kinds; no se hizo evaluación visual humana |
| Curiosidad | 3 | Transiciones invitan; moralejas y señal repetida acortan atención |

No se declara ≥4 en categorías cuyo resultado requiere una sesión visual o humana. La prueba silenciosa mejora memoria, pero no elimina la monotonía de actividades y orientación.

## Tres causas prioritarias y cambio concreto propuesto

1. **Llegada independiente de dirección y `arrivals` vacío en rutas jugadas.** Añadir llegadas breves en los dos puntos de pendiente que contradicen el recorrido y en dos transiciones principales; convertir el primer verbo direccional de la descripción en geometría estable («Los escalones enlazan...») cuando la sala sirve para subir y bajar. Anticipar el terreno que viene mediante una referencia observable. Rejugar B exactamente y leer el bloque completo.
2. **Memoria de retorno pierde el presupuesto frente a ambientación repetida.** Priorizar `return` después de peligro/memoria/llegada y antes de actividad cotidiana cuando revisita, o usar `focus` local en las salas de tránsito si se desea intervención sólo editorial. Mantener peligros reales. Comprobar que primer viaje conserva identidad y que regreso muestra al menos un reconocimiento, con y sin fauna. No inflar el número de capas por defecto.
3. **Fauna regional con misma señal y actividades con explicación repetitiva.** Introducir señales específicas del soporte local en unos pocos segmentos, y reservar danger a amenaza real; en bloque de Hoshai alternar indicio, presencia y pausa mediante herramientas actuales del catálogo. Recortar cierres explicativos en 4–6 escenas de camino elegidas; dejar que agujas, polvo y apoyos cuenten el cambio. Incorporar un pequeño refugio canónico mediante un hito existente, sin tienda ni quest nueva.

Estas propuestas están pendientes de coordinación. No se implementaron ni se declara mejora. El siguiente paso autorizado por el ciclo será IMPLEMENTAR y REJUGAR A/B con semillas idénticas, COMPARAR eventos completos y después probar una ruta ciega diferente.
