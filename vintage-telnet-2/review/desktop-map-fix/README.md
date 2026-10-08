# Mapa 2D legible y centrado — 2026-10-07

La captura del usuario muestra casillas microscópicas en una esquina. El zoom anterior podía caer hasta 0.03 y «Ver todo» ajustaba a cualquier tamaño, volviendo ilegibles los textos de un mapa grande. Además el plano de dibujo podía ocupar menos que su visor y quedar arriba a la izquierda; el centrado por scroll no admite desplazamientos negativos.

Se limita la reducción a 0.85, aumenta la tipografía de casillas a 13px (mínimo efectivo 11.05px), y se utiliza un visor de altura delimitada. Un margen de medio visor alrededor del plano permite centrar cualquier casilla, incluso en sus bordes; un ResizeObserver ajusta geometría al cambiar el tamaño y se desconecta al retirar el visor. «Ver todo» incluye el mundo conocido con desplazamiento interno, manteniendo texto legible. La leyenda identifica de qué lugar son los alrededores cuando se consulta un destino lejano.

Defecto adicional encontrado: una actualización pasiva recreaba el visor y deshacía el desplazamiento del jugador. Ahora conserva scroll cuando identidad, geometría, selección y zoom del mapa no cambian.

Prueba Chrome con copia de estado de producción interceptada sólo para presentación (110 lugares conocidos, ninguna acción enviada ni escritura): 1440/1100/393/320 px. Tras «Ver todo» y cinco reducciones, escala anterior0.03/casilla3.48px/letra0.33px; actual0.85/casilla98.6px/letra11.05px. Selección visible, posición centrada con error0px en ambos ejes, sin desbordamiento ni errores. Captura1440 inspeccionada. Prueba pan/actualización conserva exactamente left482/top3102 y resize a393 sin desbordamiento. QA lectura29 y pasiva4 PASS; sintaxis y diff PASS. Cambios estáticos servidos de inmediato sin reiniciar el servidor ni tocar partidas.

Los scripts usan /tmp/vt-desktop-map-state.json, una copia temporal de snapshot sin claves de cuenta. No se incluye la partida real en el repositorio. No se afirma prueba física Android.
