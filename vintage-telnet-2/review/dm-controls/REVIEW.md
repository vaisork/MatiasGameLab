# Controles e imágenes del director

Los menús desplegables y botones comparten tamaño, tipografía, borde y superficie. Las flechas indican apertura y mantienen semántica nativa de details/summary y uso por teclado. Cambios acotados a /dm.

El submenú del jugador muestra su imagen personal actual, ampliable; sólo usa referencia genérica si aún no existe una imagen personal. El selector de archivos se reemplaza por una galería de miniaturas con etiquetas de nivel, cuerpo completo/retrato y versión; las imágenes de otros personajes permanecen plegadas. Cambiarla mantiene confirmación, registro e idempotencia.

Validación: estilos computados iguales y apertura por teclado en 1440/393/320; gestión, galería con WebP reales decodificados y revisión independiente en esos tamaños; API real con SQLite temporal en 393/1440; prueba de exposición del retrato correcto en estado del DM. Servidor Raspberry activo después de publicar. Comprobación final con HTML/JS/CSS e imágenes públicos de Raspberry en 393/1440 confirma retrato personal cargado, tres variantes propias visibles, sin dropdown de nombres ni desbordamiento. Las APIs autenticadas de esa comprobación final están simuladas, sin alterar jugadores reales.

Las primeras capturas de la galería tenían rutas de fixture rotas: se descartaron y regeneraron con comprobaciones img.decode/naturalWidth. Los informes especifican claramente las simulaciones.

## Jerarquía de menús

Refinamiento posterior: menús principales azul oscuro; submenús blancos, alineados a la izquierda e indentados dentro de un panel tenue. Acciones mantienen forma consistente y colores de intención. Revisión independiente de capturas 320/393 aprobada, prueba de estilos e interacción 1440/393/320. Se retira Actualizar jugadores de la ficha individual; queda en la lista general. Actualizar ficha sigue disponible dentro de Gestionar personaje.
