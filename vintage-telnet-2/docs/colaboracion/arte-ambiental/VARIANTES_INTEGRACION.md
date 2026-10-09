# Variantes de estado — integración propuesta

Tres imágenes adicionales seleccionadas. No integradas. No cambian la cobertura de 183 habitaciones. Rutas y archivos en `variantes-evaluadas.json`.

| Habitación | Flag verdadero | Variante |
|---|---|---|
| hoshai_cajas_camino | hoshai_polea_recogida | sin-polea |
| korven_almacen_fondo | korven_placa_recogida | sin-placa |
| korven_almacen_balanzas | korven_placa_devuelta | placa-devuelta |

Propuesta: resolver flags efectivos con su alcance canónico y elegir variante de esa habitación sólo cuando el flag se cumpla. En otro caso, usar base. No deducir los flags por imagen ni modificar persistencia de partidas. La estructura actual de `placeArt(room)` usa vistas fijas; el arquitecto debe verificar cómo exponer esos estados antes de integrar variantes. No se tocó motor.

Hora y clima: vistas representativas no sincronizadas. No se generaron cuatro copias por lugar. Propuestas ambientales relevantes en `DIRECCION_VISUAL.md`; requieren selector. La lluvia cambia información y materiales disponibles en la lectura; no afirmar que una vista seca corresponde a lluvia actual. La comparación base/variante está en `hojas-contacto/lote-37-variantes-estados.jpg`, revisada. Las marcas pequeñas de contacto tienen legibilidad limitada: conservar detalle textual.
