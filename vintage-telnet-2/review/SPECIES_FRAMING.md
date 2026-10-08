# Encuadre y carga de especies — 2026-10-07

El visor de los modelos Meshy ajusta su cámara a los límites proyectados del modelo, reservando un margen del 16%. Centra la figura completa y recalcula el encuadre al cambiar el tamaño y al girar. Durante la descarga oculta la representación procedural y muestra un estado de carga; solamente un fallo de descarga muestra la figura sencilla con un aviso explícito. El cierre elimina el aviso y libera el visor, incluyendo descargas tardías.

Validación: Felaryn, Marevyn y Vesperi cargaron, giraron y liberaron recursos a 320/393/1100 px; sus pruebas de fallo y cierre anticipado pasaron sin excepciones. Prueba adicional de carga demorada y altura real de visor (260 px) a 320/393/1440 px: aviso presente durante descarga, eliminado al completar, cierre sin canvas ni aviso residual. Capturas inspeccionadas de Felaryn completo a 393 px. QA de lectura y actualización pasiva: 29 y 4 comprobaciones. JavaScript y diff sin errores.

Cambios estáticos servidos por el servidor actual: no requieren reiniciar Python. No se alteraron partidas ni archivos GLB originales.

## Fondos de los pueblos

El visor de especies utiliza las ilustraciones locales existentes como fondo 2D: humano/Valdren, Felaryn/Khariel, Dravak/Brumak, Marevyn/Narevia, Vesperi/Velmora. Recorta proporcionalmente para cubrir el visor sin estirar la imagen, recalcula al cambiar el tamaño y libera la textura al cerrar. Una descarga tardía también libera su textura; un fallo conserva el fondo de color. Comprobadas las cinco asociaciones y el cierre; carga demorada y capturas del visor real a 320/393/1440 px vuelven a pasar. Captura de Felaryn en Khariel inspeccionada.

## Zoom de las figuras

Botones + y −, rueda del ratón y gesto de dos dedos ajustan el acercamiento entre 0.65× y 4× del encuadre inicial. Un dedo sigue girando; dos dedos no giran al ampliar. El zoom se conserva al redimensionar o girar y ⌂ restaura giro y acercamiento. Al cerrar se liberan listeners y punteros. Prueba de navegador a 320/393/1440 px: imágenes del área de figura cambian con botones, rueda y pinch; el restablecimiento reproduce el encuadre inicial; sin excepciones y sin canvas tras cerrar. Comparación visual excluye controles para no confundir estilos de foco/hover con cambios de cámara. Los gestos son emulados en Chrome; Android físico pendiente. Prueba de carga/encuadre vuelve a pasar.
