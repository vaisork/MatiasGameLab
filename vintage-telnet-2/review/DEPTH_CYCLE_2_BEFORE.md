# Ciclo 2 · identidad regional, hora, clima y microvida · ANTES

Recorrido jugado mediante la API real y contenido publicado: 115 movimientos, 104 muestras de fase/clima, seis regiones; base temporal eliminada, CLOCK controlado y RNG=.9. Sin editar world.sqlite3, personajes reales, motor o contenido. Script reproducible: `python3 scripts/depth-cycle2-journey.py review/DEPTH_CYCLE_2_AFTER.json`. Evidencia completa: `DEPTH_CYCLE_2_BEFORE.json`. No se inventa clima: se recorren 72 horas del selector existente. Hoshai ofrece nieve y no niebla; Korven y Edran ofrecen despejado y no niebla; Nhal, Lethra y Veyra ofrecen niebla. Noche, amanecer, día y atardecer se prueban donde el calendario permite combinarlos con cada clima.

Secuencia fija: Valdren → surcos → mercado de Vaisgard → plaza de rutas → estribación de Hoshai → Khariel → pared de sotavento de Korven → Brumak → cruce de canales de Lethra → Narevia → suelo de hojas de Nhal → Velmora → Valdren. Cada transición se camina por salidas reales; no hay teletransporte. Este ciclo deliberadamente mide caminar sin combate; los ciclos de combate complementan esa cobertura.

## Autocrítica y prueba a ciegas

Lo mejor: el banco agrícola, las terrazas Felaryn, la pared de sotavento y los canales ofrecen apoyos físicos concretos. Quitando nombres de habitación y región, se reconocen campos, montaña, roca, agua y bosque. El centro antiguo se reconoce por empedrado, patios y acumulación de rutas, aunque todavía depende demasiado de esas etiquetas funcionales. No hay ciudades submarinas ni caricaturas culturales. El origen de Vaisgard permanece abierto.

Lo débil: se reconocen ecosistemas mejor que formas de vida. Los seis lugares repiten la preocupación por cargas, apoyos y dejar libre el corredor. Se entiende cómo circula mercancía, pero cuesta recordar habitantes por algo que no sea acomodar objetos. Muchos párrafos cierran con una explicación editorial: «no recibe una aparición por haber esperado», «sin necesitar un centro vacío para parecer importante», «sin llamar a todas las viviendas». Es el autor justificando el diseño en lugar de alguien viviendo allí.

Aburrimiento: tras ocho a doce pasos los sustantivos cambian, pero el ritmo vuelve al mismo arreglo de espacio → trabajo cuidadoso → reflexión sobre orientarse. La actividad es causal en la lluvia (barro en juntas; hojas adheridas; plataformas altas), menos en viento y niebla. La escena continúa en el mismo gesto indefinidamente aunque se visite de noche y varias veces.

Plantilla: no es copia literal universal; es repetición de estructura y motivo. Tres ejemplos intercambiables sin nombre: «mantener libre el paso», «las cargas se orientan», «los apoyos conservan espacio». El bosque tiene un animal concreto y espera sin recompensa, pero también una afirmación metanarrativa que rompe esa vida pequeña.

Mundo: en `nhal_suelo_hojas`, Noche/Niebla y Noche/Viento muestran exactamente la misma escena. La lluvia sí mueve al animal hacia un hueco seco. En `korven_pared_sotavento` la lluvia lleva barro a las juntas: la herramienta habitual conserva relación causal con el clima. En Valdren el viento sujeta el paño de semillas incluso de noche, cuando el texto nocturno sólo muestra el cuenco cubierto y la cena: dos capas compatibles en lo físico, poco sincronizadas en quién sigue trabajando.

Sistema infrautilizado: `room.weather`, `dawn`, `dusk`, `return`, `focus` y condiciones ya existen. No hace falta arquitectura nueva. `observar` omite `room.weather` y sólo consulta `rain/clear`: el viento del paño aparece en mirar y desaparece al observar. Es una incoherencia visible que oculta trabajo ya escrito.

Canon invisible: microvida no comercial, hábitos de cuerpos distintos y reutilización de estructuras podrían producir decisiones y huellas recordables. En cambio domina logística genérica. El misterio antiguo está correctamente protegido, pero faltan rastros cotidianos de usos incompatibles de una misma estructura.

## Puntuaciones honestas (1–5)

| Criterio | Antes | Motivo |
|---|---:|---|
| Identidad espacial | 4 | Suelo y salidas reconocibles |
| Continuidad | 4 | Transiciones caminadas, terreno gradual |
| Ritmo | 3 | Predomina acomodar cargas y leer referencias |
| Vida ambiental | 3 | Buenas escenas, gesto estático y autor explicativo |
| Densidad sensorial | 4 | Materiales, suelo, sonidos y luz concretos |
| Identidad regional | 4 | Ecosistema distinguible sin nombres; cultura todavía menos |
| Tiempo y clima | 3 | Lluvia causal; niebla/viento invisibles en muestras |
| Exploración | 4 | Examinar revela huellas sin exigir loot |
| Encuentros | 4 | Animal situado en raíz y suelo; aquí sin combate |
| Memoria | 3 | Textos de regreso existen, compiten por último lugar |
| Color semántico | 4 | API distingue world/trace; no evaluación visual adicional |
| Curiosidad | 3 | Quiero algunas conexiones; diez pasos fatigan |

## Tres causas de escala y cambio concreto propuesto

1. **Clima desigual entre lectura y observación.** Reutilizar el selector local de `room.weather` también al observar; completar niebla/viento en lugares representativos con efectos físicos propios del ecosistema. Evitar una frase regional añadida a todas las habitaciones. La comparación debe mostrar qué apoyo cambia, qué sonido se pierde y qué actividad continúa.
2. **Predominio logístico y explicaciones del autor.** En centros y segmentos clave sustituir una proporción de gestos de carga por microvida doméstica, alimento, ocio, mantenimiento específico y fauna sin recompensa. Cortar frases que explican al lector por qué el mundo no es una plantilla. No resolver con sinónimos de carga/apoyo.
3. **Regreso relegado a una capa que no llega a verse.** Dar prioridad al regreso donde ya existe una referencia realmente útil; combinarlo con cambio observable de clima/hora sin imprimir otra descripción completa. El último regreso a Valdren debe conservar la piedra del banco y mostrar lectura nueva del lugar.

Aceptación: repetir exactamente script, objetivos y reloj; contrastar mismas condiciones, no comparar escenas de diferentes horas. Exigir mejora legible en viento/niebla, variedad de actividad y regreso, además de pruebas técnicas dirigidas del selector. Mi valoración no sube automáticamente por pasar pruebas.
