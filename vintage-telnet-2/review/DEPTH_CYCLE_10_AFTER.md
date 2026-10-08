# Ciclo 10: cámara durante uso sostenido — después

La matriz AFTER ya estaba terminada y guardada al reanudar el trabajo. Se verificó `review/depth-cycle10-after/report.json` y sus doce capturas, sin repetirla por suponer que el proceso había fallado. Aplicación real en 8099, cuentas nuevas aprobadas por DM, base temporal, Humano Juramentado, Campo de surcos y búsqueda legal. Reloj controlado: avance de 10 s con CSRF y espera de 6.5 s de refresco.

| Ancho emulado | Cuenta atrás | Lugar/nodos | Proyección de etiquetas | Canvas | Otra cuenta |
| --- | --- | --- | --- | --- | --- |
| 320 | 61→51s | Iguales | Conservada | Reemplazado | Cámara inicial nueva |
| 393 | 61→51s | Iguales | Conservada | Reemplazado | Cámara inicial nueva |
| 1440 | 61→51s | Iguales | Conservada | Reemplazado | Cámara inicial nueva |

El coordinador implementó `dispose.getViewState()` y restauración de ángulo/zoom/centro para la misma identidad de personaje, lugar actual, selección y posiciones conocidas. El canvas puede recrearse por el snapshot, pero la cámara ya no salta. La comparación de coordenadas de etiquetas es exacta en los tres anchos. Antes, en 393, el lugar actual pasaba (265,225.135)→(257.759,169.877); después conserva (265,225.135). Se inspeccionaron capturas finales: orientación de brújula y composición visual coinciden antes/después.

Cerrar la vista 3D o cambiar a Aventura deja cero canvas. El arnés espera el evento asíncrono de cierre antes de medir, evitando un falso fallo por leer antes del evento toggle. Cambiar de cuenta dentro del mismo documento (sin reload), con otra cuenta aprobada y la misma especie/ruta, da una cámara inicial nueva. La segunda cuenta se prepara en un contexto de navegador separado para no rotar el CSRF del formulario de la primera; el intento inicial que mezclaba sesiones se descartó como error del arnés.

Contexto perdido: se provoca `WEBGL_lose_context`; el canvas se libera y la representación 2D queda visible con explicación breve. La matriz comprobó esa degradación en 320/393/1440. Sólo se añadió una prueba adicional a 393 px para la condición no cubierta: avanzar otros 10 s y esperar refresco después de perder WebGL. PASS: cero canvas, ninguna visual-ready y no reapertura automática. Evidencia adicional `review/depth-cycle10-after-fallback/report.json` y captura `393-context-lost-after-refresh.png`, abierta con view_image. Todas las ejecuciones registran errors=[]; no se modificaron archivos del juego durante esta validación.

## Revisión de lectura y representación después de C9

Se revisó evidencia `DEPTH_FINAL_BLIND_ROUTE.json`: 115 eventos (102 desplazamientos y 13 observaciones), 58 lugares de Edran/Veyra/Hoshai/Nhal. No se presenta esta ruta como cobertura de las seis regiones. Ninguna frase de escena exacta se repite entre salas distintas; las vueltas a una misma sala conservan referencias reconocibles. La prosa ahora permite orientarse por acequia/cercas/rodadas, arco bajo y cargas, transición de luz a dosel, raíces y apoyos. Espinajo aparece acompañado por lomo/rastro y margen seguro; raíz marcada permite detenerse sin pisar la señal. La observación produce conocimiento y opciones antes de contacto, coherente con el combate voluntario y el bestiario descubierto.

El mapa 3D complementa esa memoria espacial y conserva los nodos/rutas que recibe. Sigue siendo un esquema: no muestra la precisa forma de cada acequia, cada repisa o la escena cotidiana completa descrita por el texto. Las miniaturas procedurales de fauna/especies tienen rasgos canónicos diferenciados, pero comparten primitivas visibles y no igualan la riqueza anime 2D. Las etiquetas pueden ocultar detalles de un marcador pequeño en overview; acercar facilita leer terreno, no convierte el modelo en una simulación geográfica. Estos límites siguen explícitos y no bloquean el juego mientras se preparan modelos futuros.

Autocrítica: las capturas y coordenadas prueban estabilidad visual en Chromium emulado, no rendimiento térmico ni tacto de un móvil físico. La cámara sigue reconstruyendo recursos al cambiar otros datos de snapshot; se corrigió la pérdida del encuadre, no se afirma que desaparezca todo coste de recreación. No se inventó un fallo cuando un intento sin avance de reloj no lo reproducía: se corrigió CSRF y se guardó la reproducción válida.
