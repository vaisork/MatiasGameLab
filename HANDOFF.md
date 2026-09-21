# HANDOFF — Entrega técnica

## ENTREGA — Integración de arte HTML en vintage-telnet.html

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet, autorizado por Javier expresamente para esta tarea puntual de cliente — no es mi función firmada habitual)

**Estado:** LISTO PARA REVISIÓN

### Estado base
Commit/HEAD de `main`: `8e7042f6aab3974a939f639f51a7fbf37bcd457a` (incluye la integración de la biblioteca de arte a `main`, ver entrada "INTEGRACIÓN DE ARTE HTML" más abajo).

### Rama
`junior/vintage-telnet-art-integration`

### Tarea asignada
Javier pidió adaptar `vintage-telnet.html` para consumir la biblioteca de arte ya subida en `vintage-telnet/assets/html-ui/` (ver la integración previa de esa biblioteca a `main` más abajo en este mismo archivo), sin romper la lógica existente ni la ruta única de acciones (`perform()`).

### Archivos modificados
- `vintage-telnet.html` únicamente.

### Cambios realizados
- **Paleta:** las variables CSS de la carcasa exterior (`--shell`, `--shell2`, `--panel`, `--line`, `--ink`, `--muted`) pasan de café/ocre a pizarra azul + bronce + marfil, siguiendo la dirección "juvenil, mobile-first, menos cargada" del `README.md`/`AGENTS.md` de la biblioteca. La terminal (`--term*`, `--green*`) **no se tocó**.
- **Textura de fondo:** se agregó `background-slate-blue-subtle-tile.png` como capa adicional del fondo general (sutil, no interfiere con la lectura).
- **Esquina ornamental:** `corner-ornament-top-left.png` aplicada como `::before` decorativo en la esquina superior izquierda de `.game-shell` (no interactivo, `pointer-events:none`).
- **Divisor:** `divider-horizontal-gold-diamond.png` como separador entre los controles de combate y la barra de comandos.
- **Tres botones reales reemplazados por el arte** (mismo `data-action`, mismo `perform()`, sin cambios de comportamiento):
  - `Mapa` → `button-mapa-important.png`
  - `Inventario` → `button-inventario-normal.png`
  - `Huir` → `button-huir-danger.png`
- **Botón nuevo `Poderes`** (`button-poderes-special.png`) agregado al `tool-row`, con su propio diálogo modal siguiendo el mismo patrón que "Personaje"/"Inventario" (panel preparado, sin inventar mecánicas: el texto aclara explícitamente que no define qué poderes existen). Se agregó también al listado de comandos del diálogo de Ayuda y como rama nueva en `perform()`.
- `Atacar` y `Personaje` (sin asset dedicado en la biblioteca) quedan como botones CSS planos, heredando la nueva paleta automáticamente vía las variables.
- `tool-row` pasó de grid de 4 columnas fijas a `flex-wrap`, para que los botones con imagen (proporción 3:1 fija) no se compriman ilegibles en pantallas angostas — se acomodan 2 por fila en vez de 4-5 forzados.
- Cada botón con imagen conserva accesibilidad real: elemento `<button>`, `aria-label` explícito y texto visualmente oculto (`.sr-only`) para lectores de pantalla — no son solo un `<img>` decorativo.

### Bug encontrado y corregido durante la implementación
Las clases inicialmente usadas para los botones (`.map`, `.inventory`, etc.) colisionaban con la clase `.map` ya existente (la cuadrícula del mini-mapa en el panel lateral), que fija `background:#100b07` por shorthand y reseteaba silenciosamente `background-size`/`background-repeat` de los botones (el arte se veía repetido en mosaico en vez de contenido). Se renombraron a `.btn-map`, `.btn-inventory`, `.btn-flee`, `.btn-powers` para evitar cualquier colisión de nombres.

### Pruebas realizadas
- Verificado en navegador (Browser pane) en desktop (~1345px) y móvil (375×812, iPhone): los 7 assets cargan con 200 OK, sin errores de consola.
- Confirmado por `getComputedStyle` que `background-size:contain`/`background-repeat:no-repeat` se aplican correctamente tras corregir la colisión de clases.
- Probada la interacción real: click en Mapa/Inventario/Poderes abre su diálogo; click en Huir dispara el mismo mensaje de `perform()` que antes ("No hay combate activo..."); todo pasa por la misma función única, sin lógica paralela.
- Confirmado que en móvil (375×812) todo el contenido entra sin scroll de página (`scrollHeight === innerHeight`).
- Confirmado con `read_page` (árbol de accesibilidad) que los 4 botones con imagen exponen nombre accesible ("Mapa", "Inventario", "Huir", "Poderes") — inicialmente fallaba (el `.sr-only` no bastaba en la herramienta de lectura usada) y se corrigió agregando `aria-label` explícito además del texto oculto.
- No se agregaron frameworks ni dependencias nuevas.

### Qué sigue siendo demostración
Sin cambios respecto a la entrega anterior: todo sigue siendo cliente local sin servidor ni persistencia. Esta tarea es puramente visual/de integración de arte.

### NECESIDAD DEL SERVIDOR / NECESIDAD DE JUGABILIDAD
Sin cambios respecto a la entrega anterior. El nuevo botón "Poderes" es únicamente un acceso visual preparado; no define ni implica ninguna mecánica de magia/habilidades.

### Trabajo previo afectado
Ninguno: no se tocó lógica de `perform()`, `move()`, `rooms`, ni la estructura de datos existente. Los cuatro botones que ya abrían diálogos (Mapa, Personaje, Inventario, Ayuda) siguen abriendo exactamente los mismos diálogos que antes.

### Pendiente / aviso para el Desarrollador Junior y Arte HTML
- No se usó el asset de fondo (`background-slate-blue-subtle-tile.png`) más que como textura general; si Arte HTML quiere un uso distinto, es una iteración visual separada.
- Quedan sin arte dedicado: Personaje, Atacar, Ayuda — si Arte HTML produce esos assets más adelante, se pueden integrar con el mismo patrón (`.btn-art` + clase modificadora + `aria-label`).
- Esta entrega fue hecha por mí (rol de servidor) con autorización puntual de Javier porque no había nadie más trabajando en ello en ese momento; el Desarrollador Junior de Vintage Telnet sigue siendo el responsable natural de este archivo hacia adelante.

### Aviso para el Integrador/Publicador
No publicar hasta autorización expresa de Javier. Comparar contra el HEAD vigente de `main` antes de integrar — esta rama solo toca `vintage-telnet.html`, sin solapamiento con las otras ramas activas (`claude/vintage-telnet-server-v2`, que no toca este archivo).

**LISTO PARA REVISIÓN:** SÍ
**LISTO PARA PUBLICAR:** NO — falta autorización de Javier ("sube").

---

## ENTREGA PARA CHATGPT (histórico — publicada)

**Estado:** PUBLICADA EN `main`

### Desarrollador
Desarrollador Junior de Vintage Telnet

### Estado base
Commit/HEAD de `main`:
`4f015d48a7cfbc7cdf0fbac0e1fd7afe70876270`

### Rama
`junior/vintage-telnet-mobile-v2`

### Objetivo
Aplicar la investigación `VT-RES-002` para optimizar la interfaz HTML de Vintage Telnet en celular y separar visualmente la carcasa HTML café de la terminal Telnet negra/verde.

### Archivos modificados
- `vintage-telnet.html`
- `HANDOFF.md`

### Investigación consumida
- `vintage-telnet/RESEARCH_MOBILE_TELNET_UI.md`

### Cambios realizados
- Terminal Telnet convertida en una zona visual inequívoca: negro casi puro, texto verde y tipografía monoespaciada.
- Carcasa HTML conservada en tonos café/ocre para distinguir herramientas web de la sesión Telnet.
- Layout móvil rehecho como shell de alto visible con terminal flexible y scroll interno.
- En teléfono, mapa/estado dejan de ocupar espacio permanente; mapa/personaje/inventario/ayuda se abren en dialogs.
- Controles principales compactados sin reducirlos por debajo de objetivos táctiles prácticos.
- Cruceta N/O/Mirar/E/S mantenida con relación espacial clara.
- Atacar y Huir permanecen visibles como acciones principales de demo.
- Entrada de comandos conserva 16 px, añade `enterkeyhint="send"` y permanece próxima a la terminal.
- Safe areas incorporadas para notch/home indicator.
- Se eliminó `scrollIntoView` del documento: ahora solo se desplaza el log interno de terminal.
- Añadido soporte `prefers-reduced-motion`.
- Responsive reorganizado: compacto <=640 px, intermedio hasta 959 px, lateral persistente desde 960 px.
- No se añadieron frameworks ni lógica paralela de botones.

### Qué es funcional
- Navegación local de demo por N/S/E/O.
- Mirar.
- Entrada escrita de comandos y alias n/s/e/o.
- Botones y comandos siguen entrando por la misma función `perform()`.
- Mapa/personaje/inventario/ayuda mediante dialogs.
- Scroll interno de terminal.
- Layout compacto para teléfono y dos columnas en escritorio.
- Indicadores locales de última acción y combate.

### Qué sigue siendo demostración
- Ubicación y conectividad de la microzona.
- Mapa mostrado.
- Estado de sesión.
- Combate.
- Inventario/personaje.
- Todo continúa sin Raspberry Pi ni persistencia real.

### NECESIDAD DEL SERVIDOR
- Sin cambios respecto a la entrega anterior: contrato de acciones, estado persistente, ubicación real, inventario, combate, descubrimiento y resincronización.

### NECESIDAD DE JUGABILIDAD
- Sin cambios respecto a la entrega anterior: objetivo de ataque, huida, vocabulario definitivo y datos exactos de combate/personaje/mapa.

### Pruebas realizadas
- Comprobación estructural de terminal negra/verde.
- Comprobación de media query móvil <=640 px.
- Comprobación de terminal con scroll interno.
- Comprobación de targets táctiles de 44–46 px o mayores.
- Comprobación de safe areas superior e inferior.
- Comprobación de dialogs para mapa/personaje/inventario/ayuda.
- Comprobación de `enterkeyhint="send"`.
- Comprobación de ruta única `perform()` para botón y comando.
- Comprobación de ausencia de `scrollIntoView`.
- Comprobación de `prefers-reduced-motion`.
- Confirmación de que no se añadió framework externo.

### Prueba visual que Javier/Matías deben hacer
1. Abrir en teléfono vertical.
2. Confirmar que se percibe inmediatamente la separación: café = cliente HTML; negro/verde = Telnet.
3. Revisar cuántas líneas de texto caben sin scroll de página.
4. Moverse con una mano usando N/S/E/O.
5. Probar Mirar, Atacar y Huir.
6. Escribir 5–10 comandos seguidos con el teclado abierto.
7. Abrir/cerrar mapa, personaje, inventario y ayuda.
8. Girar teléfono a horizontal y regresar.
9. Probar en iPad vertical/horizontal.
10. Decidir si los controles siguen ocupando demasiado o si la proporción ya se siente correcta.

### Riesgos/conflictos
- Validación visual final requiere teléfono/iPad real.
- La terminal usa scroll interno en móvil; Javier/Matías deben confirmar que esta interacción resulta natural.
- Si `main` cambia antes de integrar, el Integrador debe volver a comparar la rama.

### Aviso para el Integrador/Publicador
No publicar hasta autorización expresa de Javier. Comparar esta rama contra el HEAD vigente de `main` antes de integrar.

**LISTO PARA REVISIÓN:** SÍ  
**PUBLICADA EN `main`:** SÍ — autorización “Sube” recibida el 2026-09-21  
**MERGE COMMIT:** `c156fce377203534f7d9cb14632ef4f36815310c`


## INTEGRACIÓN DE ARTE HTML — Vintage Telnet

**Fecha:** 2026-09-21  
**Estado:** INTEGRADO EN `main`

### Origen de la entrega
- Rama: `art/vintage-telnet-html-assets`
- Commit de arte revisado: `886314bfd9be648938cc7668e2527a079050d231`
- Estado antes de integrar: rama 1 commit adelante de `main` y 0 atrás.

### Qué se integró
Biblioteca modular de arte para la carcasa HTML de Vintage Telnet en:
`vintage-telnet/assets/html-ui/`

Incluye:
- botones para Inventario, Mapa, Huir y Poderes;
- ornamento de esquina;
- divisor horizontal dorado;
- textura azul/pizarra repetible;
- preview móvil de referencia;
- `README.md` y `ASSET_MANIFEST.md` con instrucciones de uso, tamaños y alcance.

### Criterio de revisión aplicado
- Los PNG son assets modulares; no sustituyen controles HTML reales.
- La terminal Telnet negro/verde debe mantenerse separada de la carcasa visual exterior.
- El arte sigue una dirección más juvenil/mobile-first y menos recargada.
- El botón `Poderes` queda como categoría visual; no define mecánicas ni poderes concretos.
- No se modificó `vintage-telnet.html` durante esta integración.
- No se modificó Senku.

### Pendiente
La siguiente tarea separada será adaptar `vintage-telnet.html` para consumir estos assets sin romper la lógica existente ni la ruta única de acciones del cliente.

### Resultado
- Arte integrado a `main`: SÍ.
- HTML actualizado para usar el arte: NO, pendiente de una tarea posterior.
- Publicación/servidor Raspberry: sin cambios por esta integración.
