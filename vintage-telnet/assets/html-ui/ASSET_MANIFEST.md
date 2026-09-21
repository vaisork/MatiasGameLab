# Asset Manifest — Vintage Telnet HTML UI

**Familia:** juvenil / mobile-first — pizarra azul + bronce + marfil.  
**Terminal:** negro + verde fósforo, fuera de esta biblioteca.

| Ruta | Tamaño | Uso | Transparencia / repetición |
|---|---:|---|---|
| `buttons/button-inventario-normal.png` | 480×160 | botón exterior estándar | PNG; pensado para fondo transparente |
| `buttons/button-mapa-important.png` | 480×160 | botón importante / navegación principal | PNG; pensado para fondo transparente |
| `buttons/button-huir-danger.png` | 480×160 | peligro / escape | PNG; pensado para fondo transparente |
| `buttons/button-poderes-special.png` | 360×120 | acceso a magia, habilidades y poderes | PNG; pensado para fondo transparente |
| `ornaments/corner-ornament-top-left.png` | 160×160 | esquina modular de panel | PNG; transparente |
| `dividers/divider-horizontal-gold-diamond.png` | 400×133 | separador horizontal | PNG; transparente; puede escalarse con moderación |
| `backgrounds/background-slate-blue-subtle-tile.png` | 96×96 | textura exterior silenciosa | PNG; repetible |
| `previews/vintage-telnet-ui-style-guide-mobile.png` | 256×384 | referencia de la familia en teléfono | preview, no usar como UI real |

## Integración

Los botones deben seguir siendo elementos HTML reales con texto/ARIA y estados de foco. El desarrollador puede usar estas imágenes como fondo/decoración y CSS para hover, focus, disabled y pressed.

**No convertir toda la aplicación en imágenes.**
