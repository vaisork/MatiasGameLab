# Controles y mapa — 2026-10-05

La cruceta conserva cuatro posiciones, incluso cuando una salida no existe. Vive en un panel fijo inferior; la página reserva espacio y mantiene blancos táctiles de al menos 44 px. Menús y herramientas usan caracteres como iconos, con nombres accesibles y títulos. Las decisiones narrativas conservan etiquetas claras. El encabezado ocupa menos espacio.

La lectura pasa de 45 caracteres/32 ms a 2 caracteres/70 ms, con pausa de 450 ms al terminar un párrafo. Mostrar completo y movimiento reducido conservan salida inmediata. Se ajustó la altura de lectura al espacio disponible.

El usuario autorizó reutilizar el mapa anterior. Se adaptó el algoritmo de colocación direccional de vintage-telnet/server/world.py:map_layout, leyendo únicamente datos de lugares y rutas conocidos del mundo nuevo. No se importaron escenas, historias, imágenes ni modelos del juego anterior. Casillas seleccionables y líneas CSS muestran un esquema de caminos, sin escala; las colisiones desplazan casillas en la dirección aprendida. La selección consulta el recorrido y no mueve al jugador. La cruceta local distingue salidas desconocidas sin revelar destinos.

Pruebas: qa-mobile-controls, qa-map, qa-map-view, qa-printing, qa-narrative y qa-passive aprobadas; sintaxis JS y diff sin errores. Adaptadores técnicos de DOM, sin aprobación visual ni prueba física Android. No cambió el servidor ni la base de datos. Recargar con Ctrl+F5 carga los cambios.

## Ajuste a las capturas reales de Android

Las capturas del usuario mostraron exceso de encabezado y herramientas. Hasta 600 px, la aventura oculta la marca y el título repetido de la crónica; mantiene el lugar en una fila y deja estado, región y clima en un desplegable ⓘ. Las herramientas muestran iconos de 30 px dentro de blancos de 44 px. A− selecciona texto de 14 px; A+ selecciona 18 px; volver a pulsar restaura 16 px. Tamaños mutuamente exclusivos y persistidos en navegador. El área de lectura aprovecha el espacio liberado. Las pruebas de controles, tipografía, impresión y refresco pasivo pasan. El resultado final aún requiere verlo en el celular del usuario.

## Mapa en las capturas posteriores

Se retiraron la marca y los párrafos de introducción de la vista móvil del mapa, conservando título y ubicación en una fila. El plano abre ajustado a la extensión de los lugares conocidos y ofrece alejar, acercar, ver todo y volver a la posición actual. El desplazamiento y centrado usan las coordenadas multiplicadas por el zoom. Las conexiones se conservan en el mismo plano transformado que las casillas. El menú del mapa usa una fila desde 360 px y dos filas en pantallas menores; la aventura conserva su cruceta fija. Las pruebas técnicas incluyen ajustar y ampliar sin mover al personaje. Pendiente verificar el resultado en Android real.

## Ritmo y límite de altura solicitados

Lectura aproximadamente 30 % más rápida: 2 caracteres cada 54 ms (antes 70 ms), pausa de 346 ms entre párrafos (antes 450 ms). El encabezado móvil conserva blancos táctiles de 44 px, elimina relleno vertical y reduce el título. El lector tiene altura fija relativa a la pantalla, acotada entre 160 y 280 px en celular; los nuevos párrafos desplazan el contenido interno sin ampliar la tarjeta. Se conservan controles de texto y lectura completa.

## Posición de lectura al decidir

La reconstrucción de Aventura conserva el desplazamiento interno del lector, el seguimiento del final y la posición de la página. Se capturan antes de desmontar el cuadro y se restauran después de montarlo. La prueba del renderizador simula desplazamiento reiniciado y verifica restauración. Chromium está instalado, pero la comprobación actual de socket devuelve EPERM antes de conectar; sigue pendiente reproducir el resultado en navegador real.
