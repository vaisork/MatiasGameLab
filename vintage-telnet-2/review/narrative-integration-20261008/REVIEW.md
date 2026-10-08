# Cierre de integración y relevo

Entrega narrativa reconciliada: `../../docs/colaboracion/CLAUDE_INTEGRACION_20261008.md` y `../CLAUDE_INTEGRATION_20261008.json`. Arte: `../art-integration-20261008/REVIEW.md`. Guía del arquitecto y operación en Ubuntu/GitHub/Raspberry: `../../../docs/VT2_RELEVO_20261008.md`.

Navegador Chrome con base temporal, sin datos reales: a320,393,1440px pasan primera visita completa, retorno breve, Mirar completo una sola vez, sin duplicación de lugar ni desbordamiento ni errores. `browser.json` comprueba arte anterior; `browser-new-art.json` verifica una ilustración recién integrada de Edran. Se abrió la imagen1200px en diálogo. No se certifica lectura a velocidad humana: se usa reduced motion para comprobar composición/interfaz.

La primera ejecución de la segunda prueba, concurrente con la suite pesada, agotó espera de30s al abrir la interfaz. Se repitió sin carga de suite y en puerto aislado8121, pasando las tres anchuras. No se modificó runtime para favorecer esta prueba. Los scripts requieren Node/Playwright en la ruta local declarada y Chrome; no son comandos Raspberry de producción.

Pruebas de servidor: 1440 comparaciones de combate preservan resultado, estado y RNG. Suite completa150 inicialmente148PASS y dos fallos de pruebas: fixture sin version y literal de niebla cambiado. Ambos corregidos; las siete pruebas afectadas pasan después. GitHub CI debe comprobar el candidato final antes de integrar. QA de mapa y trazados pasa (190rectos,6curvas,6hogares); atlas intacto.

Esta integración no se desplegó: Raspberry sigue en d5ee227. La evidencia de ese despliegue está en `../qa/raspberry-deploy/update-d5ee227/`. No se sustituyen bases ni configuración privada.
