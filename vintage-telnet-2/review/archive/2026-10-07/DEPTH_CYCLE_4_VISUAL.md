# Ciclo 4 · integración visual y canon · recorrido real

Prueba independiente de la aplicación Flask actual en8099, DB temporal del servidor de prueba; cuentas nuevas aprobadas sólo ahí. No se intercepta `/api/state`, no se inserta mapa artificial, no se manipula SQLite. Chromium real headless con WebGL SwiftShader; viewport320/393/1440. Datos, capturas y script en `review/world3d-live`.

## Jugar, criticar y corregir

Recorrido real: hogar Felaryn → salida Khariel → camino hasta Edran y Mordelinde → juncal Lethra y Pinzajunco → Narevia → sendero de hojas → Velmora → regreso Valdren.90acciones de viaje/observación,87movimientos registrados y un paso adicional manual desde el planificador;44nodos realmente conocidos, seis criaturas descubiertas por señales/observación. Dos modales de fauna son encuentros reales, no entradas añadidas por fixture.

La primera crítica visual de81nodos encontró una torre de etiquetas que tapaba la geometría, figura móvil cortada por imagen2D anterior y blanco excesivo al fallar3D. Se corrigieron etiquetas por colisión, prioridad actual/seleccionado, figura encuadrada y sustitución de imagen sólo tras mountsuccess; fallo restaura2D. La primera prueba de APP REAL descubrió404 del servidor para world3d.js y Three: la prueba estática anterior no podía detectar ese fallo. Se amplió allowlist explícita y se reinició servidor temporal. La primera pérdida real de contexto tampoco restauraba2D: se añadió manejo del evento del módulo y se repitió.

## Rejugar y comparar

Capturas actuales realmente inspeccionadas: mapa320/393/1440 deja pocos rótulos y muestra terrenos de colores con laderas, piedra, árboles y canales en nodos conocidos. La etiqueta actual ya no sale fuera del host320; el texto puede truncarse, nombre completo está en aria/title y encabezado de posición. Figura Felaryn completa tiene cola y orejas; Mordelinde bajo/alargado con patas y cola corta; Pinzajunco muestra pinza mayor. Las figuras son miniaturas esquemáticas, no sustituyen el arte2D detallado ni el retrato textual.

Seleccionar etiqueta y cambiar destino del planificador NO mueve al personaje (comparación API location). El botón «Dar siguiente paso» SÍ ejecuta un movimiento legal. Zoom/rotación cambian la proyección; arrastre se ejercita con pointer real; centrado restaura vista. La flecha↑ expresa orientación relativa sin inventar norte geográfico. Escape y Cerrar retiran modales/canvas. La pérdida provocada con WEBGL_lose_context produce mensaje y restaura mapa2D conocido. Sin erroresJS ni overflow horizontal en tres tamaños.

## Geografía visual frente al texto

El mapa sigue las rutas conocidas del backend, no todas las salas del catálogo; no revela destinos de fronteras aún no recorridas. Punteadas terminan en dirección de salida, no en un nodo oculto inventado. Las formas regionales conservan agricultura llana, pendiente de Hoshai, roca de Korven, agua/plataformas de Lethra, bosque de Nhal y ciudad antigua Veyra. Esa lectura funciona como orientación de relaciones y materiales. No pretende coordenadas cartográficas reales; el backend no las publica.

Lo mejor: se puede reconocer región material y distinguir actual/destino antes de ejecutar un paso. Lo débil: el resumen aún reduce arquitectura local a siluetas pequeñas; una plaza concreta no se identifica por anatomía visual con la riqueza del texto. En320 el planificador bajo el mapa requiere scroll y navegación ocupa dos filas. No hay simulación tridimensional de cada párrafo ni se comunica que exista.

| Criterio visual | Antes | Después | Evidencia |
|---|---:|---:|---|
| Orientación/utilidad | 2 | 4 | Rótulos legibles, actual, planificador manual |
| Identidad regional material | 2 | 4 | Pendiente/roca/agua/bosque/llano diferenciados |
| Legibilidad móvil | 2 | 4 |320/393sin overflow; modal completo |
| Continuidad con recorrido | 3 | 4 |44nodos aprendidos, rutas reales, sin movimiento al seleccionar |
| Recuperación gráfica | 1 | 4 |404resuelto, WebGLfallo/contextloss restauran2D |
| Fidelidad de miniaturas | 2 | 4 | Felaryn/Mordelinde/Pinzajunco reconocibles sin anatomía incompatible |

Son valoraciones de esta muestra y capturas, no encuesta humana. No se verificaron todas las especies/clases/equipos ni107nodos en la prueba final real; la anterior captura81nodos sirve como estrés editorial independiente. No se afirma juego3D completo, detalle arquitectónico exhaustivo ni pruebas enAndroid físico.
