# VT-RES-002 — Optimización móvil y separación visual Telnet/web

**Solicitante:** Desarrollador Junior de Vintage Telnet, por instrucción de Javier  
**Estado:** INVESTIGACIÓN ENTREGADA — NO IMPLEMENTADA  
**Fecha:** 2026-09-21  
**HEAD revisado:** 0a160f1f477d7345897e0b2dc7d44d260526376c  
**Consumidor principal:** Desarrollador Junior de Vintage Telnet

## PROBLEMA

La primera interfaz jugable de Vintage Telnet funciona como vertical slice, pero en teléfono acumula demasiadas capas verticales y la parte textual pierde protagonismo. Javier ha confirmado además una separación visual obligatoria:

- carcasa/cliente HTML exterior con identidad café, pergamino, madera/metal envejecido;
- terminal Telnet inequívocamente negra con texto verde;
- no convertir toda la aplicación en terminal negra;
- conservar texto primero y usar HTML para reducir fricción.

La investigación debe indicar cómo reorganizar la interfaz sin cambiar jugabilidad ni servidor.

## ESTADO ACTUAL DEL HTML

El HTML actual ya tiene buenas bases que conviene conservar:

- viewport con `viewport-fit=cover`;
- `100dvh`;
- botones con `touch-action: manipulation`;
- campo de comandos a 16 px, útil para evitar zoom automático en iOS;
- controles y comandos que convergen en la misma función `perform()`;
- mapa y estado colapsables en <=620 px;
- dialogs para mapa/personaje/inventario;
- breakpoints actuales a 900 y 620 px;
- botones generalmente de 50–56 px de alto;
- HTML/CSS/JS simple, sin framework.

No se recomienda reconstruir desde cero.

## PROBLEMAS OBSERVADOS EN MÓVIL

### 1. Exceso de altura antes y después del texto

En <=620 px la interfaz apila:
1. topbar;
2. aviso de demo;
3. cabecera de ubicación;
4. narración;
5. aviso importante;
6. cruceta de tres filas;
7. grupo Atacar/Huir/Mapa;
8. grupo Personaje/Inventario/Ayuda;
9. entrada de comando;
10. mapa;
11. estado.

Los botones tienen buen tamaño individual, pero la suma obliga a desplazarse y separa la narración de la acción que la produjo.

### 2. La “terminal” todavía no existe visualmente como capa separada

La narración usa fondo café oscuro y tipografía Georgia. Los comandos sí usan monospace verde, pero la experiencia completa no comunica claramente “ahora estoy dentro de Telnet”.

### 3. Los paneles secundarios siguen compitiendo con el flujo principal

Aunque mapa/estado pueden colapsarse, continúan dentro del documento debajo de los controles. En teléfono es mejor tratarlos como información secundaria invocable.

### 4. El teclado virtual puede romper el contexto

El formulario está dentro del flujo normal. Cuando aparece el teclado, el viewport visual se reduce y el navegador puede desplazar el input hasta dejar fuera el último texto importante. `100dvh` ayuda al layout general, pero no resuelve por sí solo el seguimiento del teclado.

### 5. Hay acciones duplicadas visualmente

Mirar aparece en cabecera y centro de cruceta. Mapa aparece como botón y panel. Esa redundancia puede ser útil en escritorio, pero cuesta altura en teléfono.

## PROPUESTA DE JERARQUÍA DE PANTALLA

En teléfono la prioridad debe ser:

**1. Terminal/narración → 2. movimiento/acción inmediata → 3. entrada de comandos → 4. herramientas secundarias.**

Objetivo práctico: al abrir la pantalla en vertical, el jugador debería ver simultáneamente:
- ubicación compacta;
- varias líneas de narración reciente;
- al menos el control de movimiento/acciones inmediatas;
- acceso al campo de comando sin atravesar mapa/inventario.

La terminal debe ocupar la mayor parte del espacio variable. Los controles deben tener altura relativamente estable.

## PROPUESTA DE SEPARACIÓN VISUAL TERMINAL / CLIENTE HTML

### Carcasa HTML

Mantener:
- cafés/ocres;
- bordes metálicos/madera/pergamino si el diseño evoluciona;
- tipografía de interfaz distinta a terminal;
- mapa, inventario, personaje y navegación secundaria en esta capa.

### Terminal

Tratar como una “pantalla” física dentro de la carcasa:
- fondo recomendado: negro casi puro `#030806` o `#050705`, no gris/café;
- verde principal aproximado: `#8dff9f` o equivalente con contraste alto;
- verde atenuado para mensajes secundarios;
- monospace de sistema: `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`;
- borde interior fino verde apagado y, si se desea, brillo muy sutil;
- evitar filtros CRT fuertes, scanlines animadas o blur que reduzcan legibilidad.

Negro puro `#000` es históricamente reconocible, pero un negro ligeramente suavizado reduce dureza sin perder la lectura “terminal”. La diferencia debe ser inequívoca frente a la carcasa café.

### Jerarquía dentro de terminal

No depender solo del color:
- **narración:** verde principal, peso normal;
- **comando del jugador:** prefijo `>`, verde más brillante y/o peso fuerte;
- **sistema:** verde atenuado + prefijo o etiqueta textual;
- **alerta/peligro:** puede usar un acento adicional de la paleta exterior o texto/ícono, pero debe conservar contraste y no depender exclusivamente de rojo/verde;
- **ubicación:** una línea compacta encima del log o dentro de la terminal.

No hacer que cada párrafo sea enorme. En móvil interesa densidad legible.

## LAYOUT RECOMENDADO PARA TELÉFONO

### Wireframe vertical

```
┌─────────────────────────────┐
│ VINTAGE TELNET      ● DEMO  │  <- 44–52 px
├─────────────────────────────┤
│ carcasa café / ubicación    │  <- compacta
│ ┌─────────────────────────┐ │
│ │ TERMINAL NEGRA / VERDE  │ │
│ │ > mirar                 │ │
│ │ Valdren...              │ │
│ │                         │ │
│ │ texto reciente...       │ │  <- área flexible,
│ │                         │ │     scroll interno
│ └─────────────────────────┘ │
├─────────────────────────────┤
│       [ N ]                 │
│ [ O ] [◎] [ E ]   [HUIR]   │  <- controles esenciales
│       [ S ]        [ATACAR] │
├─────────────────────────────┤
│ > comando...       [Enviar] │  <- fijo cerca del fondo
├─────────────────────────────┤
│ Mapa  Pers.  Inv.  Ayuda   │  <- barra secundaria
└─────────────────────────────┘
   safe-area-inset-bottom
```

### Recomendación principal

En móvil, **mapa, personaje e inventario no deben ocupar espacio permanente en el documento**. Abrirlos como `dialog` adaptado a bottom sheet o panel casi completo. El HTML ya posee dialogs, así que puede evolucionarse sin introducir una biblioteca.

El mapa puede abrirse desde botón y, si se desea, permitir pulsar una salida conocida; al cerrar vuelve exactamente al texto.

### Cruceta

No hace falta una cuadrícula de tres filas si se puede compactar manteniendo targets grandes. Conservar la relación espacial N/O/E/S porque se entiende sin texto largo.

El centro “Mirar” es razonable porque LOOK/MIRAR es una acción central del género.

Atacar/Huir solo deberían ocupar espacio destacado cuando Jugabilidad determine que son relevantes; mientras no haya combate, pueden estar atenuados o una zona contextual puede reemplazarlos. No ocultar una acción necesaria de forma impredecible.

## LAYOUT RECOMENDADO PARA TABLET

Rango aproximado orientativo: desde ~700–760 CSS px de ancho útil, decidido por cuándo caben dos columnas sin comprimir la terminal.

Propuesta:
- terminal/narración: 60–70% del ancho;
- lateral: 30–40% para mapa/estado;
- controles y comando debajo de terminal;
- personaje/inventario mediante dialog/drawer;
- en horizontal, mantener dos columnas;
- en vertical estrecha, permitir que el lateral pase a overlay en lugar de empujar la terminal.

iPad no debe recibir automáticamente el layout de escritorio solo por ser tablet; probar el ancho real y orientación.

## LAYOUT RECOMENDADO PARA ESCRITORIO

Conservar el patrón actual de dos columnas, pero:
- terminal negra/verde en columna principal;
- mapa y estado visibles en lateral;
- controles debajo de terminal o en franja compacta;
- línea de comando siempre accesible;
- ancho de texto de terminal limitado para evitar líneas excesivamente largas;
- no agrandar botones proporcionalmente al monitor.

El máximo actual de 1380 px es razonable como límite general.

## RESPONSIVE POR CONTENIDO

No atar CSS a nombres de dispositivos. Propuesta inicial para probar:

- **compacto:** <= 640 px: una columna; secundarios en dialog/bottom sheet; controles compactos.
- **intermedio:** 641–959 px: terminal protagonista; secundarios pueden alternar entre overlay y dos columnas según espacio.
- **amplio:** >= 960 px: dos columnas persistentes.

Estos valores no son dogma. Deben ajustarse mirando cuándo los controles dejan de caber cómodamente, no según “iPhone/iPad” como etiquetas.

Usar también `@media (orientation: landscape)` solo cuando aporte una mejora concreta; no duplicar toda la hoja de estilos.

## RECOMENDACIONES DE TAMAÑOS Y ESPACIADOS

### Targets táctiles

WCAG 2.2 establece un mínimo de 24×24 CSS px para Target Size (Minimum), con excepciones; Apple recomienda controles táctiles de al menos 44×44 pt y Android/Material suele recomendar 48×48 dp.

Para este juego, usar **44–48 CSS px como objetivo mínimo práctico** para controles principales, con separación suficiente para no pulsar el vecino. La interfaz actual ya está cerca o por encima; el problema es densidad total, no botones demasiado pequeños.

### Texto

- terminal móvil: empezar alrededor de 16 px;
- interlineado: ~1.45–1.6;
- texto auxiliar: evitar bajar de ~13–14 px cuando sea información funcional;
- entrada de comando: mantener **16 px mínimo** en móvil para evitar zoom de enfoque en Safari/iOS;
- ancho de línea en escritorio: aproximadamente 60–80 caracteres para narración terminal.

### Espaciado

- borde exterior móvil: 8–12 px cuando la carcasa necesite verse;
- separación entre controles: 6–8 px mínimo;
- padding terminal: 12–16 px;
- evitar grandes márgenes verticales decorativos en móvil.

### Safe areas

El viewport ya incluye `viewport-fit=cover`. Añadir donde corresponda:
- `padding-top: env(safe-area-inset-top)`;
- `padding-bottom: env(safe-area-inset-bottom)`.

Especialmente importante si la barra de comandos/acciones se aproxima al borde inferior.

## COMPORTAMIENTO CON TECLADO VIRTUAL

### Objetivo

Cuando el jugador toca el campo:
- la línea de comando permanece visible;
- el último mensaje/resultado relevante permanece justo encima;
- mapa/paneles secundarios no ocupan el viewport reducido;
- cerrar teclado devuelve la interfaz sin salto grande.

### Estrategia CSS/HTML primero

1. En móvil, convertir la zona principal en un contenedor de altura basada en `100dvh`.
2. Dar a la terminal `min-height: 0` y scroll interno.
3. Mantener controles + comando como zona estable debajo de la terminal.
4. Al enviar un comando, hacer scroll del log al final, no `scrollIntoView` de todo el documento.
5. Evitar `position: fixed` indiscriminado porque el teclado móvil y Safari pueden producir saltos.

### VisualViewport como mejora progresiva

La API `window.visualViewport` está ampliamente disponible en navegadores modernos y permite conocer el viewport visible cuando aparece teclado/zoom. Puede usarse como mejora progresiva si las pruebas reales muestran problemas, por ejemplo para ajustar una variable CSS de altura.

No hacer que la interfaz dependa exclusivamente de esa API: CSS con `dvh` y scroll interno debe seguir funcionando si no está disponible.

### Input

Conservar:
- `font-size:16px`;
- `autocapitalize="none"`;
- `autocomplete="off"`;
- `spellcheck="false"`.

Considerar `enterkeyhint="send"` para que el teclado virtual comunique mejor la acción de enviar.

No usar `inputmode` restrictivo: los comandos necesitan letras, espacios y posiblemente signos.

## MAPA, PERSONAJE E INVENTARIO

### Teléfono

**Cerrados por defecto.** Recomendación:
- mapa: dialog/bottom sheet grande, porque necesita espacio;
- personaje: dialog/bottom sheet;
- inventario: dialog/bottom sheet con scroll propio;
- ayuda: dialog ligero.

Un bottom sheet puede implementarse con `<dialog>` + CSS, conservando accesibilidad/foco nativo en vez de crear un sistema de overlays artesanal.

### Tablet

Mapa puede permanecer visible cuando haya ancho suficiente. Inventario/personaje siguen siendo secundarios salvo que pruebas indiquen lo contrario.

### Escritorio

Mapa/estado pueden permanecer visibles en lateral. Inventario/personaje pueden abrir panel/dialog para no estrechar la narración.

## ACCESIBILIDAD Y LEGIBILIDAD

- Mantener contraste mínimo WCAG: 4.5:1 para texto normal y 3:1 para texto grande; elegir verdes de terminal que superen esos valores sobre negro.
- No comunicar combate/peligro únicamente por color.
- Mantener focus visible.
- Los botones cardinales necesitan `aria-label`, como ya ocurre.
- No bloquear pinch zoom mediante viewport.
- Probar al 200% de zoom.
- Respetar `prefers-reduced-motion`: la animación `reveal` debería desactivarse/reducirse si el usuario lo solicita.
- La terminal con `aria-live="polite"` debe probarse con lector de pantalla para evitar que un combate muy activo anuncie texto continuamente de forma inutilizable. Es posible que convenga una región de estado separada para eventos prioritarios.

## RIESGOS Y TRADE-OFFS

### Terminal con scroll interno

**Ventaja:** conserva texto y controles juntos.  
**Riesgo:** scroll anidado puede confundir si toda la página también hace scroll.

**Mitigación:** en móvil, hacer que el shell principal quepa en el viewport y que el scroll primario de juego sea la terminal; secundarios se abren aparte.

### Barra inferior persistente

**Ventaja:** acciones siempre disponibles.  
**Riesgo:** roba altura y puede chocar con teclado/safe area.

**Mitigación:** hacerla compacta y permitir que acciones secundarias vivan en dialogs.

### Bottom sheets

**Ventaja:** excelentes para móvil.  
**Riesgo:** una implementación manual puede crear problemas de foco/accesibilidad.

**Mitigación:** reutilizar `<dialog>` existente y estilizarlo responsivamente.

### Negro/verde muy “retro”

**Ventaja:** separación visual inmediata y fuerte identidad.  
**Riesgo:** efectos CRT excesivos reducen legibilidad.

**Mitigación:** estética mediante color, borde y tipografía; efectos decorativos mínimos.

## INSTRUCCIONES ACCIONABLES PARA EL DESARROLLADOR JUNIOR

No reescribir la aplicación. Iterar sobre el HTML actual.

### Paso 1 — crear terminal real
- Cambiar visualmente la tarjeta de ubicación/narración a un contenedor de terminal negro/verde.
- Aplicar monospace a ubicación, log, comandos y mensajes internos de terminal.
- Mantener carcasa, topbar, herramientas y overlays en paleta café.
- Conservar el contenido temporal y las advertencias de demo.

### Paso 2 — hacer el shell mobile-first
- En <=640 px, reducir topbar y aviso a la mínima altura necesaria.
- Hacer que la zona de juego use el alto visible.
- Terminal = área flexible con scroll propio.
- Controles + input = área compacta estable.
- Evitar que mapa/estado queden como largas tarjetas debajo.

### Paso 3 — secundarios a dialogs en teléfono
- Reutilizar los dialogs existentes para mapa/personaje/inventario.
- En móvil, ocultar las tarjetas laterales persistentes.
- Estilizar dialogs como panel inferior o casi pantalla completa.
- En >=960 px recuperar lateral persistente para mapa/estado.

### Paso 4 — compactar controles
- Mantener targets >=44–48 px.
- Conservar cruceta espacial.
- Eliminar duplicación móvil de Mirar fuera de la cruceta.
- Mover Mapa/Personaje/Inventario/Ayuda a una barra secundaria compacta.
- No cambiar qué hace cada acción.

### Paso 5 — teclado
- Añadir `enterkeyhint="send"`.
- Evitar que `append()` haga scroll del documento completo; desplazar solo el log de terminal.
- Probar primero con `dvh` + flex/grid + `min-height:0`.
- Añadir VisualViewport solo si una prueba real demuestra necesidad.

### Paso 6 — accesibilidad
- Añadir `prefers-reduced-motion`.
- Verificar contraste negro/verde.
- Probar focus y dialogs solo con teclado.
- Revisar comportamiento de `aria-live` antes de un combate real.

### Lo que NO debe hacer en esta tarea
- no implementar servidor;
- no inventar estadísticas;
- no cambiar comandos/reglas;
- no convertir el mapa temporal en canon;
- no incorporar React/Vue/Tailwind u otro framework para resolver un problema que el CSS actual puede manejar;
- no crear lógica separada para botones.

## PRUEBAS QUE JAVIER Y MATÍAS DEBEN HACER

### Teléfono vertical
1. Abrir la página sin zoom manual.
2. Confirmar que se entiende inmediatamente qué es carcasa café y qué es terminal negra/verde.
3. Leer varias líneas sin que los controles dominen la pantalla.
4. Moverse N/S/E/O solo con pulgar.
5. Abrir/cerrar mapa, personaje e inventario.
6. Escribir 5–10 comandos seguidos.
7. Confirmar que al aparecer el teclado sigue visible el último texto relevante.
8. Girar el teléfono y volver a vertical.
9. Probar zoom del navegador.
10. Confirmar que ningún botón queda debajo de notch/home indicator.

### iPad/tablet
1. Probar vertical y horizontal.
2. Confirmar que el mapa lateral solo aparece cuando realmente cabe.
3. Comparar comodidad de tocar brújula vs escribir comandos.
4. Abrir inventario/personaje y comprobar que no destruyen la posición del log.
5. Mantener teclado abierto y ejecutar varios comandos.

### Prueba conceptual
Preguntar después de jugar:
- ¿El texto sigue siendo lo principal?
- ¿Se siente que la terminal es “el juego” y la carcasa HTML son herramientas?
- ¿Los botones ahorran trabajo o distraen?
- ¿Hay suficiente texto visible?
- ¿El mapa ayuda sin revelar demasiado?

## FUENTES

- W3C WCAG 2.2, Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- W3C WCAG, Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- Apple Human Interface Guidelines, Layout: https://developer.apple.com/design/human-interface-guidelines/layout
- web.dev, viewport units: https://web.dev/blog/viewport-units
- MDN, Visual Viewport API: https://developer.mozilla.org/en-US/docs/Web/API/Visual_Viewport_API
- MDN, dialog element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog
- MDN, env() / safe-area-inset: https://developer.mozilla.org/en-US/docs/Web/CSS/env
- Written Realms, Interface and Commands: https://docs.writtenrealms.com/playing/interface-and-commands/
- Iron Realms, Nexus Client: https://www.ironrealms.com/the-nexus-client/

## RECOMENDACIÓN TÉCNICA

Evolucionar el HTML actual, no reemplazarlo.

En teléfono, Vintage Telnet debería comportarse como **una terminal grande y estable dentro de una carcasa HTML compacta**. El texto ocupa el espacio flexible; movimiento, acción inmediata y comando permanecen próximos; mapa/personaje/inventario salen del flujo principal y aparecen bajo demanda.

En tablet/escritorio, el mismo modelo puede expandirse mostrando mapa/estado en lateral.

La separación negro/verde frente a café no es solo decorativa: puede convertirse en una gramática visual consistente. **Lo negro/verde pertenece a la sesión Telnet; lo café pertenece a las herramientas del cliente web.**

## ESTADO DE VALIDACIÓN

**INVESTIGADO:** sí.  
**IMPLEMENTADO:** no.  
**PROBADO EN RASPBERRY:** no aplica a esta investigación.  
**PROBADO EN TELÉFONO REAL POR INVESTIGADOR:** no. La validación final corresponde a las pruebas de Javier/Matías después de que el Junior prepare la iteración.
