# Geografía estable de todo VT2 — 8 de octubre de 2026

Encargo: corregir superposición y falsas conexiones a escala del mundo existente.

## Diagnóstico

183 salas alcanzables, seis pueblos y 196 conexiones públicas. No había destinos rotos. El cliente anterior colocaba salas según el orden de descubrimiento: invertir la lista cambiaba 158 posiciones relativas. Seis pares de salidas representan caminos que doblan; no son conexiones cardinales inversas.

## Cambio

Atlas esquemático fijo, 183 posiciones públicas distintas y seis reservas de hogar. 202 caminos congelados incluyen las reservas; cada partida sólo muestra su hogar. Se apartaron interiores de calles públicas y se abrieron manzanas existentes, sin añadir salas ni alterar una sola salida. Siete descripciones aclaran curvas ya existentes. Los cruces inevitables se interrumpen visualmente para distinguirlos de una unión. HTML y 3D comparten posición y trazado; no hay canon 3D paralelo.

No equivale a un plano métrico: separación gráfica no cambia coste de movimiento. Descubrir una sala no mueve lugares ni caminos aprendidos. El servidor no revela salas o conexiones ocultas.

## Reproducción

`python3 review/spatial-world/author_positions.py` y después `node review/spatial-world/author_roads.mjs` generan el atlas completo. Los generadores son herramientas editoriales, nunca se ejecutan durante una partida. QA: `tests/test_spatial_world.py`, `client/qa-map-spatial.mjs`, `client/qa-map-frozen-roads.mjs` y evidencia navegador en `review/spatial-map-client/`.

No se ha desplegado este cambio en Raspberry. Las partidas reales no se utilizaron como fixtures.

## Validación

- Pruebas Python focales de mapa, contenido real, narración y piloto MUD; nueve pruebas espaciales, incluido un viaje API/SQLite nuevo por seis pueblos, más de 60 movimientos y regreso al hogar. Se compara la geometría aprendida después de cada paso.
- QA Node: 202 rutas congeladas y 189 posiciones con seis reservas; ninguna atraviesa otra casilla, sin segmentos compartidos y puertos cardinales coherentes. Ocho cruces en el atlas completo; cinco en el escenario humano con un hogar. Los cruces gráficos se interrumpen para no simular conexiones.
- QA navegador: seis pueblos a 393 y 1440 píxeles, sin etiquetas recortadas, errores JS o desbordamiento horizontal. Fixture completo: 184 lugares y 197 conexiones, sin afirmar que es una sesión humana.
- Revisión independiente: ninguna salida modificada, privacidad correcta. Se corrigieron dos lagunas: rechazo de atlas con posiciones pero sin rutas y QA del atlas congelado completo.

Las capturas y verificaciones certifican el renderizado local, no producción ni rendimiento físico de un teléfono.
