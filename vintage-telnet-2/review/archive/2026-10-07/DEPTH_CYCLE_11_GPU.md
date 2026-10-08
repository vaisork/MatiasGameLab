# C11 — conservar el mapa 3D durante actualizaciones pasivas

## Jugar y criticar

La evidencia real de C10 (`depth-cycle10-after/report.json`) mostró que a 320, 393 y 1440 píxeles la cámara ya sobrevivía al cooldown, pero el canvas se reemplazaba. Un cambio de disponibilidad de buscar reconstruía recursos WebGL aunque lugar, rutas conocidas, personaje y ambiente no habían cambiado. No se midieron batería, FPS ni milisegundos; la debilidad demostrada era la reconstrucción innecesaria.

## Implementar

`client/app.js` asigna una clave al mapa visual: personaje, especie, clase, equipo y sus objetos representados, mapa descubierto, posiciones, selección, momento del día y clima. Cuando esa clave coincide, `applyPassiveSnapshot` devuelve el nodo existente a la vista de forma síncrona después del render normal. El MutationObserver comprueba un nodo conectado y conserva el renderer. El placeholder nuevo se descarta sin crear otro renderer. Planner, acciones, narrativa, token y restauración de foco siguen su actualización habitual.

Un cambio relevante de geometría, ubicación, personaje, equipo o ambiente conserva el flujo existente de desmontaje y montaje. El cierre y el fallo WebGL siguen liberando recursos. No se añadió otra arquitectura ni se modificó world3d.js.

## Rejugar y comparar

Servidor real aislado en 8099, reloj controlado y cuentas nuevas; nunca la base o usuarios reales. `scripts/depth-cycle11-gpu.mjs` reproduce buscar, abrir mapa, acercar, girar, desplazar, avanzar diez segundos con CSRF y esperar actualización pasiva.

- 320, 393 y 1440: cooldown 61 → 51 segundos; mismo objeto canvas y mismas proyecciones de etiquetas; sin errores de navegador.
- 393 adicional: el identificador DOM del planner cambia mientras el canvas permanece, confirmando actualización de controles autoritativos.
- Ambiente real: 24 avances autorizados de 300 segundos llevan Despejado → Lluvia; cambia el canvas y el color WebGL de fondo. La captura de lluvia se inspeccionó visualmente.
- Cerrar, cambiar vista y cambiar personaje liberan o separan la vista; otro personaje no hereda la cámara manipulada.
- Pérdida provocada de contexto vuelve al mapa 2D. Otro avance y refresh no reabre automáticamente la vista fallida.

Evidencias: `depth-cycle11-after/report.json` y sus doce capturas; `depth-cycle11-after-environment/report.json` y seis capturas, incluida `393-rain.png`. Checks: sintaxis de app.js, cuatro casos de QA passive (foco, borrador, acciones, token) y QA de rutas pasan.

## Autocrítica y límites

El beneficio probado es evitar un montaje WebGL completo en un refresh sin cambios visuales; no es una estimación de autonomía móvil. Los modelos siguen siendo miniaturas esquemáticas y las etiquetas largas se abrevian en móvil. La conservación depende del render síncrono y del checkpoint posterior de MutationObserver; una futura conversión de render a asincronía debe revisar este contrato. Esta prueba no recorrió cada región ni cada combinación de equipo, pero la clave incluye sus datos representados para invalidar la reutilización cuando cambian.
