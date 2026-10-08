# Revisión real de Chromium — 2026-10-05

La nueva sesión permite conexión local. El juego activo responde HTTP 200. Se instalaron herramientas de Playwright en /tmp/vt-new-browser-tools y se lanzó Chrome en modo headless. La revisión utilizó el código y contenido del proyecto con una base de datos temporal en un servidor separado; no cambió personajes ni permisos reales.

Resultado PASS: registro, aprobación, lectura, observación, tres tamaños de pantalla (320×740, 390×844, 1440×1000), recorrido real de 19 pasos hasta Tierra blanda, mapa, salida de cuenta y reconexión. Sin desbordamiento horizontal ni errores de página/consola. Al pulsar Mirar, scrollTop permanece en 45 px y el lector permanece en 280 px de altura.

La revisión detectó que botones persistentes fuera del área reconstruida quedaban deshabilitados después de una petición. Se restauran los botones que estaban habilitados antes de la operación. También se abre el mapa al tamaño legible de las casillas y centrado en el destino actual; ajustar todo queda disponible mediante su control.

Evidencia: browser-current/report.json, scroll-proof.json y capturas. Se inspeccionaron visualmente las capturas de lectura y mapa. scripts/browser-review-new.mjs reproduce el flujo con VT_REVIEW_PLAYWRIGHT apuntando al módulo de Playwright, VT_REVIEW_URL al servidor de prueba y VT_REVIEW_DM_PASSWORD al director del entorno de prueba. Las credenciales no aparecen en los informes.

Límites: emulación de Chromium; no equivale a prueba física Android ni a la validación humana de 20–30 minutos del prompt. Los archivos BROWSER_STARTUP.log anteriores conservan el fallo histórico del entorno restringido.

Ampliación validada: búsqueda regional, hallazgo persistente, bifurcaciones sin destinos ocultos, imagen de Pinzajunco cargada, encuentro de hábitat, capacidad Sombra y retirada. Servidor aislado con azar fijado para reproducibilidad; 46 pruebas backend pasan. Capturas e informe en browser-rich/. Se inspeccionaron lectura, mapa, bestiario y combate.

Bestiario actualizado: miniaturas de 56 px, ilustración anime infantil del Pinzajunco ampliada sólo por clic y diálogo nativo con cierre accesible. Prueba aislada y capturas en browser-anime/.

Mapa y especies: revisión del mapa guardado de 89 nodos con vista local, vista completa y direcciones reales, ficha de personaje y cinco ilustraciones ampliables. Evidencia en world-map-species/. Recorrido completo de exploración y combate validado antes del último ajuste de márgenes; evidencia en map-species-browser/. Suite de servidor: 47 pruebas pasan.
