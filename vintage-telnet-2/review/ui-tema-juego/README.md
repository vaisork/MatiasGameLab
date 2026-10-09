# Tema de juego: noche azul, oro y pergamino (2026-10-09)

Petición: que la interfaz se sienta como un juego veterano para niños y no como una herramienta técnica. La dirección visual sale de la maqueta que entregó el usuario: marcos azul noche con filete dorado, pergamino, letra con serifa, ilustración grande del lugar, salidas en lista, acciones rápidas en losetas y barra de cinco pestañas.

## Cambios
- **Escena:** la ilustración del lugar ocupa la cabecera, con el nombre, la región y la etiqueta de hora y clima. Antes era una miniatura de 42 px.
- **Barra de estado:** vida, energía, sellos y nivel siempre a la vista. Al pulsarla, abre la ficha.
- **Relato:** pergamino con letra de libro de 18 px en lugar de la terminal verde de letra de máquina. «Entorno» desaparece y los avisos de peligro, combate y progreso se distinguen con fondo de color.
- **Salidas:** panel con flecha dorada, dirección y destino, que sustituye al mando flotante que tapaba el contenido. También desaparece la línea «Salidas: …» del relato.
- **Acciones:** losetas azul noche con icono dorado y color según el tipo (combate rojo, comercio oro, conversación lila, cuidado turquesa, exploración azul).
- **Barra inferior:** Explorar, Mapa, Personaje, Inventario y Más. «Más» lleva a Bestiario, Diario y Ayuda.
- **Iconos:** 14 iconos nuevos dibujados como SVG en el estilo de línea de la maqueta (brújula, huella, fuego, poción, espadas, corazón, moneda, luna, sol, estrella, escudo, rayo…).
- **Ficha:** los atributos aparecen en cuadrícula con icono.
- **Combate:** panel rojo oscuro con tu vida en verde y la del rival en rojo.
- **Mapa, mochila, botones y formularios:** adaptados al tema.
- «Dónde vender» sólo aparece en la escena cuando hay algo que vender.

El tema va en una capa final de `client/style.css`. No elimina reglas anteriores ni cambia clases que usen las pruebas. Sólo cambia, a propósito, lo que comprueban dos pruebas del cliente (el número de pestañas y el orden de los paneles), que se actualizan en esta misma entrega.

## Capturas
- `antes-y-despues.jpg`: el antes en la plaza; el después en la plaza, el combate y el mapa (móvil de 390 px).
- `mas_inventario.jpg`: las vistas Más e Inventario.
- `despues_escritorio.jpg`: el juego en una pantalla de ordenador.

## Pendiente
Marcos ornamentados y texturas pintadas (filigrana dorada, papel envejecido) requieren arte; se pueden encargar al agente de arte. No hacen falta descargas: fuentes con serifa del sistema y SVG propios.

## Segunda ronda (2026-10-09): la letra manda y la tienda por secciones
- **Sin ilustración en la escena:** la cabecera queda compacta (nombre, región, hora y clima). La imagen del lugar, y el retrato del rival en combate, sólo aparecen como vista previa al pasar sobre el icono de imagen y a tamaño completo al pulsarlo.
- **Tienda:** las compras ya no salen como botones sueltos en la escena; hay una sola loseta «Tienda».
  - Dentro, secciones Pociones y comida, Armas, Armaduras, Anillos y amuletos, y Vender.
  - Las armaduras y joyas se agrupan por parte del cuerpo. Las ventas, por materiales, equipo y otros.
  - El servidor añade `category` y `slot` a cada acción de compra y venta.
- **Mochila:** en lugar de listar las compras, ofrece «Abrir la tienda».
- Captura: `tienda.jpg`.
