# C16: recorrido rápido, evidencia previa

Dos cuentas temporales del servidor aislado8099, Chromium real, 320/393px. Veinte movimientos por ancho mediante las flechas visibles, entre Plaza de Valdren y su salida norte, seguidos de `mirar` y `observar` escritos. Es una prueba breve dirigida, no una sesión humana ni medición de GPU/Android físico.

Prioridad: después de enviar una decisión escrita, el scroll automático al formulario se conserva y oculta la respuesta. A320px la lectura está entre −243 y99px, el contenido entre −193 y87px; a393px entre −248 y96px. Las capturas settled muestran sólo el final de la respuesta arriba, mientras formulario y presencia dominan la pantalla. La interfaz confirma la acción pero exige al usuario subir para leer lo ocurrido. Propuesta: tras una decisión explícita escrita exitosa, devolver la vista a la lectura/contexto (respetando reducedmotion); conservar anclaje en polls y cuando se está releyendo historial. No aplicado todavía.

Los40 movimientos observados cambian lugar en0,11–0,23s, mantienen el scrollY6 y flechas fijas sin erroresJS ni desbordamiento. El texto progresa y reinicia por llegada; los movimientos rápidos no esperan la impresión. No se creó canvas durante este recorrido textual. Esto no acredita rendimiento de mapa3D/GPU, que no se abrió en esta muestra.

Script reproducible y medidas en browser.py/report.json; capturas step1/2/20, observe y settled por ancho. Sin edición del cliente ni cambios de contenido.
