# Ciclo 1 — implementar, rejugar y comparar

Evaluación de agente sobre eventos reales de la aplicación, sin sesión humana ni evaluación visual. Compara los recorridos documentados en `DEPTH_CYCLE_1_BEFORE.md`. No se tocó runtime/world.sqlite3 ni cuentas reales.

## Qué se implementó

En el catálogo existente se corrigieron cuatro arranques de descripción de Hoshai para representar geometría estable, válida al subir y bajar. Se añadieron veinte llegadas según origen en pendientes, ribera y relevos; no hay nodos ni arquitectura nuevos. Cinco nodos existentes muestran ahora Refugio de Lajas, Parada de los Cardos, Vado de Juncos, Orilla Velada y Alto de las Raíces, con una función pequeña de descanso, cruce o relevo y sin tiendas ni misiones añadidas. Se recortaron seis finales de actividad que explicaban la moraleja de lo recién mostrado.

En paralelo, el coordinador cambió la prioridad del motor para que `return` aparezca antes de actividad y llegada, después de peligro/memoria, conservando tres capas. También unificó la selección climática de observar. Este informe mide el resultado conjunto; no atribuye la mejora de retorno sólo a la edición del contenido.

## Rejuego igual y prueba ciega distinta

Las rutas A y B se repitieron exactamente con el mismo origen, objetivos, hora inicial, minuto por acción y RNG. A mantiene 40 movimientos; B mantiene 57. Se usaron RNG=0 y RNG=0.9 como antes. Ambas regresaron al hogar, pasaron permisos legales y observaron los mismos centros.

- `review/archive/2026-10-07/depth-cycle-1/travel-after.json`: pasada con fauna.
- `review/archive/2026-10-07/depth-cycle-1/travel-quiet-after.json`: pasada silenciosa de encuentros aleatorios.
- `review/archive/2026-10-07/depth-cycle-1/travel-blind-after.json`: ruta C, elegida después de editar: hogar Marevyn → Narevia → Velmora → Paso del Dosel Alto → Khariel → retorno por bosque y ribera → Narevia → hogar. 40 movimientos reales. Incorpora una conexión no leída en BEFORE, sin preparar sus escenas para satisfacer una métrica.

Se leyeron bloques consecutivos de movimientos, incluidas las llegadas y el regreso. El script reproducible conserva sus opciones de semilla y archivo; `python3 scripts/depth-cycle-1-travel.py 0 travel-blind-after.json blind` reproduce C.

## Comparación observable

| Medida en A+B | Antes | Después |
|---|---:|---:|
| Movimientos reales | 97 | 97 |
| Regresos públicos con `return` disponible | 30 | 30 |
| `return` efectivamente visible, RNG=0 | 12 | 28 |
| Regresos que repiten exactamente todos los textos, RNG=0 | 13 | 2 |
| Regresos que repiten exactamente todos los textos, RNG=0.9 | 5 | 2 |
| Llegadas según origen visibles, RNG=0 | 0 | 11 |
| Llegadas según origen visibles, RNG=0.9 | 0 | 14 |
| Misma frase de Saltacresta en B, RNG=0 | 16 | 16 |

La mejora de continuidad y reconocimiento es perceptible en lectura consecutiva. La repetición de fauna NO mejoró. No es honesto declarar terminado el ritmo general por una reducción de párrafos idénticos.

## Muestras sin encabezados geográficos

Antes, bajando desde la plaza: «Subes por escalones de tamaños distintos». Después, la geometría dice que enlazan terraza y casas, y la llegada dice:

> Al dejar la plaza, el canal acompaña el descenso. Desde el primer peldaño ya ves las cuerdas tendidas en la terraza inferior.

Más adelante, antes comenzaba otra vez «Subes por una ladera abierta». Después:

> La roca deja de cerrarse a tus lados. Más abajo, una línea oscura de agua corta la ladera antes del pinar.

La forma de moverse ya enlaza roca estrecha, ladera y corriente. No depende de leer el nombre de la sala.

Primera transición al pedral:

> Al salir de la garganta puedes abrir los brazos sin tocar roca. Una cubierta baja ofrece sombra sobre las notas del Paso de las Lajas.

En la ruta ciega, el regreso del relevo alto muestra:

> El cordel de la sierra termina en un apoyo de raíz. Más allá de la cubierta, las marcas continúan en caras de corteza que reciben muy poca luz.

Ambas muestras distinguen soportes, amplitud y luz mediante cambios materiales. Las descripciones base conservan las salidas.

## Autocrítica después

**Lo mejor:** el descenso dejó de contradecir la posición del personaje; el reconocimiento de retornos aparece en el flujo normal; los refugios tienen escala cotidiana y geografía canónica. La nueva memoria de la mesa/plataforma y los hitos existentes ayuda sin pedir mapa omnisciente.

**Lo más débil:** las dos revisitas de A donde peligro y otra memoria desplazan `return` siguen reproduciendo eventos idénticos. Más importante: el animal regional vuelve a saltar exactamente igual en B dieciséis veces. El mundo tiene soportes locales, pero el encuentro aún no los usa para distinguir presencia e indicio.

**Dónde me aburrí:** el bloque descendente de Hoshai mejora su hilo espacial; aun así la señal idéntica interrumpe casi cada paso. El regreso ahora ofrece variación escrita, pero treinta avisos de reconocimiento pueden volverse un segundo patrón. En algunos barrios ese reconocimiento explica derechos, relaciones y límites sociales en vez de mostrar un recuerdo breve.

**Dónde se ve la plantilla:** hay textos de retorno con «haber vuelto no concede...» o «conocer su entrada no entrega...». Ahora son más visibles gracias a la prioridad. El recorte de seis finales de `day` no resuelve la voz explicativa de todos los `return`. La solución siguiente sería seleccionar sólo algunas memorias para revisión editorial, no reemplazar todas por otra frase prefabricada.

**Dónde deja de sentirse mundo:** retornar todavía no modifica la actividad del vecino. A veces la memoria dice que las personas pueden cambiar, pero el siguiente evento repite la misma persona y tarea. Reconocimiento estático y vida dinámica son cualidades diferentes; aquí mejoró principalmente la primera.

**Sistema infrautilizado:** la prioridad sigue compartiendo un presupuesto reducido entre peligro, memoria y llegada. Las llegadas añadidas no aparecen en todas las revisitas porque retorno gana: un intercambio razonable, pero no todas las capas pueden prometerse a la vez. Las señales de fauna podrían estar ligadas al soporte local y reservar silencios sin añadir un motor nuevo.

**Canon antes invisible:** los cinco pequeños refugios ya existen como hitos de nodos actuales; C confirmó en juego Alto de las Raíces. El origen desconocido y las distintas épocas de reparación de Vaisgard siguen apenas insinuados en el paseo de mercado/plaza; no se resolvió ese frente dentro de este ciclo.

**Cambio siguiente concreto:** atacar repetición de fauna en su dueño compartido, manteniendo presencia real del mundo y advertencia de peligro. Después recortar 3–4 memorias largas en la conexión de bosque y asentamiento donde el reconocimiento se vuelve explicación social. No aumentar capas globalmente.

## Puntuaciones, 1–5

| Criterio | Antes | Después | Lectura honesta |
|---|---:|---:|---|
| Identidad espacial | 4 | 4 | Se conserva geometría legible |
| Continuidad | 3 | 4 | Descenso coherente y transiciones de materiales |
| Ritmo | 2 | 3 | Llegadas aportan transformación; señal repetida persiste |
| Vida ambiental | 3 | 3 | Tareas creíbles, sin cambio real de participantes |
| Densidad sensorial | 4 | 4 | Amplitud, agua y polvo ahora enlazan pasos |
| Identidad regional | 4 | 4 | C confirma bosque→sierra mediante apoyos y luz |
| Tiempo y clima | 3 | 3 | Sólo hora diurna; esta sesión no acredita ciclo temporal |
| Exploración | 3 | 3 | Observar aún puede repetir actividad |
| Encuentros | 2 | 2 | Dieciséis repeticiones, sin mejora demostrada |
| Memoria | 2 | 4 | 28/30 retornos muestran reconocimiento |
| Color semántico | — | — | No hubo evaluación visual |
| Curiosidad | 3 | 4 | Las llegadas anticipan apoyos y el terreno próximo |

COMPARAR confirma mejora en continuidad y memoria. Ritmo, vida ambiental y encuentros siguen bajo el umbral canónico de 4/5 y exigen siguientes ciclos. No se sustituyó el juicio humano por esta evaluación de agente.

Validación técnica complementaria: `PYTHONPATH=runtime/python-deps:tests python3 -m unittest discover -s tests -p test_real_content.py -q` pasó los 14 casos. Esto confirma compatibilidad de contenido con API/recorridos y servicios existentes; no demuestra por sí solo calidad narrativa.
