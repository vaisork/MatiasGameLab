# #163 — Vaisgard: primer hilo histórico jugable

Objetivo: convertir historia pública ya integrada en observaciones opcionales dentro del room_id existente `vaisgard`. No crea sub-salas, recompensas, NPCs, criaturas ni mecánicas nuevas.

Fuentes: VAISGARD.md + ENTRY_HISTORY_CANON.md.

## Targets observables dentro de `vaisgard`

| target | hito observable | texto de mirar/examinar | conocimiento público |
| --- | --- | --- | --- |
| `muro_antiguo` | bloque antiguo sosteniendo ampliación reciente | “Una hilada de piedra enorme queda atrapada dentro de una fachada mucho más nueva. La unión funciona, pero las técnicas no pertenecen a la misma época.” | Vaisgard tiene capas de construcción y es más antigua que los pueblos actuales. |
| `arco_cegado` | arco de piedra parcialmente cubierto por obra posterior | “El arco ya no conduce a ningún paso visible. Parte de su abertura quedó absorbida cuando el nivel de la calle y los edificios cambiaron.” | La ciudad ha cambiado de forma sin dejar de estar habitada. |
| `escalera_cubierta` | escalones que descienden y desaparecen bajo construcción posterior | “Los escalones bajan solo unos pasos antes de quedar ocultos por una obra más reciente. No hay acceso abierto ni indicación de lo que había al final.” | Existen estructuras antiguas cuyo propósito original no siempre se conoce; no revela niveles reservados. |
| `reparaciones_mezcladas` | materiales de distintas regiones en una misma reparación | “Piedra, madera y piezas de procedencias distintas conviven en la misma reparación. La ciudad fue modificada muchas veces por poblaciones que ya tenían técnicas propias.” | Vaisgard siguió siendo un centro compartido incluso después del surgimiento de los pueblos. |
| `marca_plaza_rutas` | cambio visible entre acceso viejo y ampliación de tránsito | “El paso más antiguo es estrecho para el movimiento actual. La ampliación posterior corrige el problema sin borrar del todo la entrada original.” | La Plaza de las Cinco Rutas y su tráfico actual son consecuencia de pueblos ya consolidados, no el origen de todos ellos. |

## Ritmo
- Cada target es opcional.
- Ninguno revela quién construyó Vaisgard.
- No abrir ni describir el interior de entradas selladas.
- No convertir una observación en misión o secreto.
- Tres o más targets permiten un resumen público, no una recompensa.

Resumen opcional:
“Vaisgard no parece una ruina ni una ciudad nueva. Parece una ciudad que nunca dejó de usarse mientras generaciones enteras construían encima, alrededor y a través de lo anterior.”

## Handoff
Narrativa Vaisgard #163: CERRADA.
Integración puede implementar estos targets sobre el room_id `vaisgard` usando mirar/examinar existente, sin crear geografía adicional.