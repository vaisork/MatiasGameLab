# Cinco ciclos de coherencia al caminar — 8 de octubre de 2026

Encargo de Javier: revisar cinco veces que el mundo no forme nudos y conserve coherencia espacial al caminar. Trabajo sobre la implementación de PR #659; sin añadir salas, cambiar salidas ni tocar partidas reales.

## Recorrer → criticar → corregir → comprobar

| Ciclo | Recorrido real por API/SQLite aislados | Defecto y resultado |
|---|---|---|
| 1. Pueblos | 50 movimientos: Valdren, ribera de Lethra y viviendas de Velmora; regreso al hogar | El acceso privado al hogar consumía un puerto cardinal de las calles. Se separaron sus puertos: el hogar deja de obligar a las calles públicas a desviarse. Se compararon rutas aprendidas después de cada paso. |
| 2. Regiones | 82 movimientos: Khariel, meseta de Korven, Brumak, Edran, Vaisgard y Narevia; regreso | La búsqueda elegía cualquiera de los caminos de igual longitud y dibujaba escaleras de hasta 29 giros para una curva. La búsqueda conserva primero la longitud mínima y después minimiza los giros. Las seis curvas reales pasan a un giro cada una. |
| 3. Campos y riberas | 61 movimientos: era, zanja, arboleda, sauces, observación del canal y relevo; regreso | Dos edificios y una reserva de hogar quedaban en la línea de otras calles, aunque el trazador los rodeara. Se añadieron dos separaciones editoriales y se impidió reservar hogares dentro de calles. Desaparecen los tres rodeos públicos restantes. |
| 4. Interiores | 61 movimientos: canal cubierto y refugio de Edran; balanzas, pasillo lateral, fondo del almacén y cauce de Korven; regreso | El canal tiene fondo cerrado, no conecta mágicamente con otro pueblo; el circuito del almacén coincide con su curva descrita. Se simplificaron también las conexiones abstractas de los hogares a una línea diagonal sin consumir salidas cardinales. Antes de aprenderlos, salir/hogar no dibujan una falsa orientación cardinal. No se inventan túneles ni niveles. |
| 5. Control independiente | 374 movimientos, las 183 salas públicas y las seis regiones, con retorno final al hogar | Se validaron direcciones, salas de llegada, permanencia de trazados y acceso mediante permisos reales. El primer recorrido pasó, pero la revisión del diagrama detectó que el acceso al secadero cruzaba la calle de hogares de Velmora. Se abrió la manzana y se repitieron los 374 movimientos. Se añadió una protección automática contra regresiones en los nudos y giros artificiales. |

Cinco ciclos finales: **628 movimientos**; con la primera pasada del quinto, **1002 movimientos**, seis personajes temporales distintos. `cycle-1.json` a `cycle-5.json` conservan cada paso, dirección, destino, posición, descripción y lectura recibida. Los primeros ciclos corresponden a estados intermedios; el quinto recorre todo el catálogo con el candidato final. Son acciones del API real sobre SQLite temporal, no una sesión humana ni una partida en Raspberry. No se teletransporta ni se cambian flags para saltar permisos.

## Resultado final y comparación

- 190 conexiones públicas rectas, seis caminos con una sola curva y seis hogares con enlace simple. Las 202 conexiones conservan su longitud geométrica mínima, sin retrocesos artificiales.
- Antes: máximo de 29 giros, 14 caminos públicos con más de dos giros. Después: máximo público de uno, ninguno con más de dos. `baseline.json` conserva la medición anterior.
- Ninguna salida, sala, NPC, misión o regla de movimiento modificada. El atlas sigue siendo esquemático; su separación gráfica no promete distancias métricas o número de pasos.
- QA del atlas completo: sin intersecciones con casillas ajenas ni segmentos compartidos; dos cruces rurales se distinguen con interrupciones cartográficas, sin convertirlos en conexiones.
- Navegador real: seis pueblos y mapa completo a 393/1440 píxeles; sin etiquetas recortadas, errores JS o desbordamiento horizontal. WebGL activo y eliminación correcta del canvas al cerrar. El fixture visual tiene todo descubierto deliberadamente; los recorridos API están documentados aparte.
- Trece pruebas Python focales de mapa y geografía, más QA Node de rutas, geometría, descubrimiento y simplicidad. `qa-map-paths.mjs`, ya ejecutado en CI, incorpora la nueva protección `qa-map-simplicity.mjs`.

## Reproducir

Desde la raíz de VT2, con las dependencias de `requirements.txt` instaladas: `python3 review/spatial-five-cycles/audit.py N` para cada número 1–5. Se crea y elimina una base temporal por ejecución. Para diagramas: `python3 review/spatial-five-cycles/serve.py`, seguido de `node review/spatial-five-cycles/browser.mjs` y `node review/spatial-five-cycles/crossings.mjs`. El ejemplo de navegador usa el Playwright local de Ubuntu; ajustar su importación al entorno propio. Servidor de revisión sólo localhost y sin POST.

**Sin despliegue en Raspberry.** Este encargo autoriza corregir y verificar, no reiniciar producción.
