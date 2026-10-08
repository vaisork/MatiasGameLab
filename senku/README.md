# Senku

Proyecto independiente de Vintage Telnet.

- `legacy/`: versión anterior recuperable y jugable.
- `v2/`: espacio limpio preparado; pendiente encargo de Javier.
- `index.html` y `juego.html`: accesos compatibles que redirigen al legacy.

El almacenamiento local del juego conserva sus claves `senku_*`; los redirects no cambian origen ni partidas. Assets de legacy permanecen en `../assets/` por compatibilidad con URLs existentes; esa ubicación no los convierte en assets compartidos con VT2. Senku v2 debe tener assets propios.
