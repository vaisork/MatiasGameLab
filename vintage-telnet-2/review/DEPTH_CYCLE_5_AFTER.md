# Ciclo 5 — implementar, rejugar y comparar sesión larga

Evaluación de agente sobre API real y base temporal; no sesión humana, visual ni prueba estadística de frecuencia. Se repitió exactamente `scripts/depth-cycle5-long.py`, con mismos personaje/origen, destinos, acciones, hora inicial y RNG=0. Evidencia: `review/depth-cycle5-before.json` y `review/depth-cycle5-after.json`.

## Cambio aplicado

Sólo se editó texto en `content/regions/*.json`: 30 señales de fauna ligadas a soportes locales en sierra, pedral, agua y bosque; 23 retornos convertidos de explicación social a reconocimiento de rampas, umbrales, bancos, fibras y marcas; seis salas del canal con luz, agua residual y referencias de regreso propias. Ninguna distribución de encuentros, requisito, precio, recompensa, misión, perfil de combate ni servicio cambió. Los sistemas existentes sostienen la sesión; no se añadió arquitectura.

## Rejuego y resultados

Ambas sesiones completan 211 movimientos, 107 ubicaciones y 266 acciones. Terminan en el hogar con 50 sellos y 55.9 HP. Las siete misiones se entregan igual; comprar/vender, afinar con material de combate y descansar conservan sus resultados. El retiro ante Cornalomo sigue seguro. El combate humano y Espinajo se resuelven sin cambiar riesgos ni premios. El guion no fuerza una derrota ni demuestra recuperación por muerte.

| Evidencia leída en movimientos | Antes | Después |
|---|---:|---:|
| Misma frase regional de Saltacresta | 19 | 0 |
| Mayor repetición de una señal de Saltacresta | 19 | 5 (misma sala revisitada) |
| Frase regional genérica de Cascapedernal | 11 | 5 |
| Frase regional genérica de Pinzajunco | 10 | 5 |
| Frase regional genérica de Rondamusgo | 10 | 0 |
| Frase genérica de luz del canal | 9 | 0 |
| Retorno genérico «Reconoces los apoyos y la salida...» | 4 | 0 |
| Dos frases moralizantes de plaza/patio Felaryn señaladas en BEFORE | 9 | 0 |

Se compararon eventos completos y bloques consecutivos, además de estas cuentas. Reducir una frase a cero no acredita automáticamente mejor experiencia: aquí el cambio perceptible es que su sustitución explica qué hace el animal en EL soporte que acabas de leer, y el retorno sitúa el cruce recordado en vez de explicar una norma.

## Muestras consecutivas sin encabezados geográficos

Antes, ocho de diez pasos del descenso emitían el mismo salto. Después, entre la roca estrecha y el arroyo:

> En una repisa alta del cuello, el Saltacresta queda inmóvil al oír el golpe de aviso. Sólo baja cuando el estrechamiento vuelve a estar libre.

> Un Saltacresta se afirma en una laja por encima de los hitos. Desde el sendero ves su sombra pequeña antes de distinguir el cuerpo.

> El Saltacresta extiende las patas sobre la piedra que divide la corriente. La salpicadura alcanza su apoyo inferior; recoge una pata y espera.

> Una piña rueda desde un apoyo bajo. Detrás asoman las patas del Saltacresta, que espera entre dos troncos antes de cruzar el claro.

El animal ya no es intercambiable entre agua, pinar y repisa. Sigue siendo fauna observada, sin obligar al combate; no se afirma que estos comportamientos estén simulados más allá del evento escrito.

Antes, entrada/bifurcación/refugio ofrecían la misma luz. Después:

> La claridad de la zanja alcanza los tres peldaños y termina en la primera curva.

> La claridad del oeste recorta el escalón de la cámara sur. Hacia la compuerta sólo se distingue un brillo bajo, a la altura del agua.

> La taza devuelve un reflejo pequeño desde el umbral. La manta está fuera de esa luz; sólo su borde doblado se separa de la pared.

Y al volver:

> La cuerda de salida reaparece junto a los peldaños. El aire de la zanja llega hasta aquí con olor a raíces.

La geometría construye tensión sin insertar otro enemigo ni otra misión. Los rastros de crecida y agua residual hacen visible el uso hidráulico anterior de la estructura.

## Autocrítica honesta

**Lo mejor:** el tramo largo de sierra conserva hilo animal propio de cada soporte; el canal ahora distingue umbral, ramal, refugio, compuerta y fondo por luz y agua. Las misiones mantienen continuidad y los retornos más breves dejan espacio para leer la siguiente dirección.

**Lo más débil:** el sistema genera los mismos tipos de encuentro con la misma frecuencia. La señal nueva del peldaño aparece cinco veces porque esa sala se cruza cinco veces. La localización aporta identidad, pero no transforma una presencia fija en vida dinámica. El Espinajo aún repite nueve veces su advertencia regional; otros pools menos seleccionados también conservan textos comunes. No se declara resuelto todo el catálogo.

**Aburrimiento:** en el regreso final, ya no leo el mismo salto en cada sala; sí detecto la misma estructura «descripción + fauna + reconocimiento» durante muchos movimientos. Esa selección requiere otro cambio de prioridad/presencia si se quiere silencio más frecuente; este ciclo de contenido no lo hizo. La diferencia material mejora lectura, pero una sesión de más de doscientos movimientos sigue acumulando fatiga.

**Plantilla:** queda prosa explicativa en algunas actividades y retornos no elegidos. Se recortó el conjunto observado más perjudicial, no se hizo reemplazo masivo automático. En Orilla Velada, retorno y llegada pueden mencionar luz semejante en el mismo evento: repetición semántica menor, todavía perceptible.

**Mundo:** NPC y encargos tienen consecuencias, pero las actividades siguen recurriendo estáticamente. El canal conserva referencias a caja/salteador en descripciones base después de resolver su misión; esto demanda revisión de variantes/flags con el coordinador y no se corrigió introduciendo estados sin conocer su contrato. Se prefiere consignar el defecto a ocultarlo en esta evaluación.

**Sistema infrautilizado:** `wildlife_pool.text` y `return` ahora usan más geografía existente. Las variantes por historia local y la selección de pausas aún pueden hacer más; no se añadieron nuevos subsistemas para anticiparlo.

**Canon invisible:** los pequeños refugios siguen visibles y tienen escala apropiada. La arquitectura hidráulica antigua gana luz residual, marcas de crecida y adaptación como almacenamiento. El misterio de origen de Vaisgard sigue abierto, aunque este circuito de mercado no explora su profundidad histórica. Nada en la nueva prosa identifica constructores ni inventa una guerra fundacional.

**Cambio siguiente concreto:** antes de ampliar prosa, revisar con el coordinador las variantes de la compuerta/repisa tras devolver la caja; después probar una ruta realmente ciega e independiente con el catálogo final. La sesión larga usa objetivos elegidos por el agente: no sustituye esa prueba ni una sesión humana.

| Criterio | Antes | Después |
|---|---:|---:|
| Identidad espacial | 4 | 4 |
| Continuidad | 4 | 4 |
| Ritmo | 3 | 3 |
| Vida ambiental | 3 | 3 |
| Densidad sensorial | 4 | 4 |
| Identidad regional | 4 | 4 |
| Tiempo/clima | 3 | 3 (misma franja diurna) |
| Exploración | 3 | 4 (canal legible sin premio adicional) |
| Encuentros | 2 | 3 (identidad local mejora; recurrencia estática) |
| Memoria | 3 | 4 (referencias breves y concretas) |
| Color semántico | Sin evaluación | Sin evaluación |
| Curiosidad | 3 | 4 (luz/ramales y presencia situada sostienen siguiente paso) |

El umbral canónico todavía no se cumple en ritmo, vida ambiental, encuentros y tiempo. Este ciclo demuestra mejora editorial acotada, no calidad humana garantizada ni fin del trabajo narrativo.

Validación técnica complementaria: los 14 casos de `test_real_content.py` pasan sobre contenido real y bases temporales. El rejuego completo de 266 acciones es la prueba de compatibilidad de la sesión; los tests no sustituyen la crítica.
