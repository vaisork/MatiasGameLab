# Vintage Telnet — Capa narrativa de encuentros de Nhal

**Issue:** #306  
**Rol:** Narrador  
**Alcance:** Camino de la Sombra Verde vigente en `main`.  
**Canon ecológico:** #166 / PR #281 y mapping de Historia #323.

Esta capa no fija porcentajes, pesos, números de combate ni nuevas mecánicas. Su función es impedir que poblar Nhal convierta el bosque en una sucesión uniforme de peleas.

## Mapping narrativo por sala

| room_id | estado | señal / exclusión narrativa |
| --- | --- | --- |
| `sombra_borde` | tranquila | Borde habitado de Velmora. Mantener sin fauna aleatoria para que la salida del pueblo sea legible. |
| `sombra_tronco` | tranquila | Hito cuidado por viajeros. No contaminar con encuentro ordinario. |
| `sombra_raices_cruzadas` | presencia posible | Primer punto donde la ruta deja de sentirse construida. Movimiento breve entre raíces puede anunciar Rondamusgo sin forzar combate. |
| `sombra_claro_pequeno` | presencia posible | Cobertura periférica; el claro mismo debe conservar respiración. Fauna puede retirarse hacia raíces/copas. |
| `sombra_sendero_doble` | presencia posible | Vegetación espesa a ambos lados permite presencia evasiva. No convertir la bifurcación visual en emboscada obligatoria. |
| `sombra_niebla_baja` | territorial | La niebla puede revelar filamentos sólo si Historia marca anclajes compatibles. Antes de Hilaria: hilo tensado, gotas suspendidas o vibración de red; nunca aparición limpia desde la niebla. |
| `sombra_arbol_caido` | territorial | Tronco y raíces son anclaje natural. Si aparece Hilaria, mostrar primero red/filamentos; Rondamusgo puede usar huecos sin perseguir. |
| `sombra_tres_marcas` | tranquila | Hito de orientación. Mantener sin fauna aleatoria para que observar las marcas siga siendo la decisión principal. |
| `sombra_claro_escucha` | tranquila | Espacio deliberado para detenerse y leer sonidos. La ausencia de combate forma parte del ritmo. |
| `sombra_raiz_alta` | territorial | Bosque profundo y raíz dominante. Antes de fauna territorial, dar señal física clara; no usar sorpresa sin lectura. |
| `sombra_bosque_abierto` | presencia posible | Último tramo todavía Nhal según Historia. Menos cobertura: priorizar fauna evasiva; Hilaria sólo si existen anclajes válidos. |
| `sombra_hojas_claras` | tranquila | Inicio de transición. La reducción de fauna debe sentirse como salida gradual del bosque. |
| `sombra_ultimas_senales` | tranquila | Última influencia de Nhal. Reservar como cambio de lenguaje del camino, no como punto de combate. |
| `sombra_entrada_veyra` | tranquila / excluida | Veyra. Sin pool Nhal. |
| `sombra_cruce_viajeros` | excluida | Fuera de Nhal; tránsito compartido. |
| `sombra_vista_vaisgard` | excluida | Aproximación a Vaisgard. |
| `sombra_aproximacion` | excluida | Aproximación urbana. |

## Lectura de las criaturas

### Rondamusgo
Su presencia debe sentirse primero como fauna del bosque, no como enemigo que espera turno:
- hojas movidas cerca de una raíz;
- cuerpo inmóvil al oír pasos;
- retirada hacia cobertura si no se le fuerza;
- combate sólo cuando el sistema/acción lo desencadene.

No narrarlo persiguiendo al jugador a través de salas.

### Hilaria de niebla
Es territorial y depende de una red. La advertencia es obligatoria cuando el encuentro pueda escalar:
- filamentos visibles por humedad o contraluz;
- tensión entre dos puntos de anclaje;
- vibración breve en una red;
- espacio que obliga a notar la estructura antes de tocarla.

La niebla por sí sola **no** es señal suficiente y tampoco habilita a Hilaria si no hay anclajes ecológicos válidos.

## Amenaza superior: Rasgacorteza

Permanece fuera del pool ordinario. Si se usa después, debe alterar el bosque antes de aparecer: marcas en corteza, rutas menores desviadas, silencio anormal o fauna que abandona cobertura. No convertir estas señales en presencia aleatoria de Rasgacorteza.

## Ritmo buscado

El recorrido debe alternar:
**seguridad habitada → presencia discreta → bosque profundo con territorialidad → pausa → salida gradual**.

Un jugador que recorra Nhal varias veces debe poder tener trayectos con poca pelea, otros con fauna observable y algunos con combate. Poblar el mundo significa que está vivo, no que cada sala contiene un enemigo.

## Handoff

Con el mapping ecológico de Historia #323 y esta capa narrativa, #306 queda listo para que Jugabilidad cierre NHAL-01 con densidades, pesos y exclusiones y lo entregue a Desarrollo.
