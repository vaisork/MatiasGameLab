# Encargo de arte: mapa ilustrado del mundo (2026-10-09)

Para: agente de arte o Codex. Lo pide Javier: que el mapa parezca un dibujo muy grande del mundo.

## Qué hay que hacer
Una sola ilustración muy grande del mundo completo, vista desde arriba en perspectiva aérea ligeramente inclinada (estilo mapa de aventura dibujado a mano). El juego la usará como fondo del mapa: encima dibujará los caminos y lugares que cada jugador ya descubrió, con desplazamiento y zoom.

- **Tamaño:** 7000 × 8400 px en vertical (proporción 35:42, la misma que la cuadrícula del atlas). Entregar PNG maestro, más un WebP de calidad 85 y una miniatura de 700 × 840.
- **Rutas propuestas:**
  - `client/art/map/mundo-anime-v1.webp`
  - `client/art/map/mundo-anime-v1-thumb.webp`
- **Calce exacto:** cada lugar debe quedar dibujado en su posición.
  - `posiciones.json` da el centro de cada uno de los 183 lugares en porcentaje del ancho y del alto (`x_pct`, `y_pct`, con origen arriba a la izquierda) y los 196 caminos que los unen.
  - `guia-composicion.png` es la guía esquemática: colores por región, pueblos en rojo y caminos en marrón. **No es arte final.**
  - Algunos caminos largos son tramos de conexión entre regiones; dibújalos como caminos que siguen el terreno, no como líneas rectas.

## Composición (del atlas real)
| Región | Zona del dibujo | Pueblo | Carácter visual (`DIRECCION_VISUAL.md`) |
|---|---|---|---|
| Cuenca de Veyra | centro | Vaisgard (mercado) | cuenca de colinas bajas, la gran ciudad de muros viejos, cinco caminos que se cruzan |
| Sierra de Hoshai | norte, franja vertical central | Khariel | pendiente, grava, pinos sueltos, terrazas, paso estrecho, nieve sólo en lo más alto |
| Pedrales de Korven | oeste | Brumak | roca clara fracturada, cauces secos, casas bajas en la roca |
| Bosque de Nhal | este, de norte a centro | Velmora | dosel denso, raíces, musgo, claros, luces pequeñas entre árboles |
| Llanos de Edran | suroeste | Valdren | llanura de parcelas, cercas, acequias, molinos y carros |
| Aguas de Lethra | sur, centro | Narevia | canales, juncos, pasarelas de madera, casas sobre postes |

Las zonas vacías entre regiones son terreno natural de transición (praderas, colinas, bosque disperso, ríos), no océano ni desierto inventado.

## Estilo
- Anime fantástico alegre y luminoso, como la interfaz nueva: colores vivos y cielo claro, línea fina, pintura cel-shaded, lectura clara a cualquier zoom.
- Los pueblos se distinguen a simple vista. Los caminos son de tierra clara y fáciles de seguir.
- Sin texto, rótulos, rosa de los vientos, marcos ni interfaz: el juego pone los nombres encima.
- Sin monstruos, personajes en primer plano ni lugares que no existan en el canon. Dorsalodo, Rasgacorteza y la demás fauna mayor no se dibujan.

## Aceptación
- Al superponer `guia-composicion.png` con un 50 % de opacidad, cada pueblo y cada camino cae sobre su dibujo.
- Se verifican el SHA256 y las dimensiones, igual que en las entregas anteriores.
- La integración en el cliente (fondo del mapa con zoom) la hace Claude cuando llegue la imagen.

## Referencia de Javier
`maqueta-mapa.jpg` (recortada de su maqueta): fondo ilustrado de bosques, ríos y montañas; lugares como etiquetas claras con borde dorado; caminos con puntos dorados; una rosa de los vientos discreta en una esquina; zoom a la derecha y leyenda abajo. El fondo debe tener ese nivel de detalle y esa paleta, pero **sin texto ni etiquetas**: las pone el juego. La rosa de los vientos también la dibuja la interfaz.

El servidor ya envía en el mapa la posición del atlas de cada lugar (`spatial.json`), así que el fondo se podrá calzar debajo sin cambiar la lógica del mapa.
