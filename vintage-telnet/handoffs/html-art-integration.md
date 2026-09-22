# Handoff — Integración de arte HTML Vintage Telnet

**Responsable:** Desarrollador Junior de Vintage Telnet  
**Base main:** `059a448cfac4fd84fb49c88d38093640b95e04b5`  
**Rama:** `junior/vintage-html-art-integration`

## Objetivo

Integrar la primera biblioteca real de Arte HTML ya presente en `main` sin reemplazar la terminal negra/verde ni convertir controles accesibles en imágenes.

También se recuperan dos decisiones previas de Javier que todavía no estaban publicadas:
- Ayuda a pantalla completa.
- Panel Personaje preparado para una futura imagen 3D del Dungeon Master.

## Assets usados

- `vintage-telnet/assets/html-ui/backgrounds/background-slate-blue-subtle-tile.png`
- `vintage-telnet/assets/html-ui/ornaments/corner-ornament-top-left.png`
- `vintage-telnet/assets/html-ui/dividers/divider-horizontal-gold-diamond.png`
- `vintage-telnet/assets/html-ui/buttons/button-mapa-important.png`
- `vintage-telnet/assets/html-ui/buttons/button-inventario-normal.png`
- `vintage-telnet/assets/html-ui/buttons/button-huir-danger.png`

El asset `button-poderes-special.png` no se conecta todavía a ninguna acción porque Jugabilidad no ha definido una acción `poderes` en este cliente.

## Cambios

- Carcasa exterior pasa de café dominante a pizarra/carbón/metal con bronce.
- Fondo exterior usa la textura repetible oficial.
- Terminal negro + verde fósforo se conserva intacta.
- Mapa, Inventario y Huir usan los PNG del artista como fondos decorativos de botones HTML reales.
- Ornamento modular aplicado a la esquina del panel principal.
- Divisor del artista aplicado entre controles de comando y herramientas.
- Ayuda abre en `100vw × 100dvh` con safe-area.
- Personaje incluye placeholder explícito para futura imagen 3D, sin inventar ruta.
- No se implementa Poderes todavía.

## Verificaciones estructurales

Comprobado en el HTML de la rama:
- todas las rutas de los seis assets usados están presentes;
- terminal conserva `--term:#030806` y `--green:#8dff9f`;
- controles siguen siendo elementos `<button>` con texto/ARIA;
- `perform(raw)` sigue siendo la ruta de acciones;
- Ayuda usa `dialog.fullscreen`;
- Personaje contiene `characterPreview`;
- no existe `data-action="poderes"` ni nueva mecánica inventada.

## Límites

No se modifica:
- servidor;
- Raspberry;
- SQLite;
- Jugabilidad;
- canon;
- NPCs;
- Ollama.

## Prueba visual recomendada

1. teléfono vertical: verificar que pizarra/metal no reduzca legibilidad;
2. confirmar terminal negro/verde sigue siendo protagonista;
3. comprobar Mapa/Inventario/Huir legibles sobre sus assets;
4. abrir Ayuda y confirmar pantalla completa;
5. abrir Personaje y confirmar espacio reservado 3D;
6. iPad vertical/horizontal;
7. desktop: revisar que el patrón de fondo no distraiga.

**LISTO PARA REVISIÓN VISUAL:** SÍ  
**NO PUBLICAR SIN AUTORIZACIÓN.**
