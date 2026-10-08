# Cinco especies Meshy con fondo — 2026-10-07

Se integraron los GLB de Humano y Dravak que estaban en la carpeta Meshy del escritorio. Humano se reduce de46.61MB/966476triángulos a1.74MB/43484triángulos; Dravak de24.31MB a3.95MB, conservando sus15566triángulos completos. Originales preservados, SHA y metadatos registrados en optimization.json. Ninguno tiene skins ni animaciones; el usuario no requiere animaciones.

Las cinco especies utilizan modelos Meshy locales, fondo de pueblo, encuadre completo, indicador de carga, giro, zoom y restablecimiento. Se extendieron las listas explícitas del cargador, visor, UI y servidor a Humano/Dravak, sin habilitar archivos arbitrarios. Dravak normaliza a altura1.4 frente a2Humano (el visor encuadra individualmente). Su ropa sigue siendo representación de la especie, no equipo real del personaje. El bestiario permanece2D.

Comparación original/optimizado de Humano y Dravak a320px inspeccionada; optimizados probados320/393/1440 con fondos, zoom, giro, reset y liberación. Prueba del menú real de las cinco especies sobre Tailscale a320/393/1440 con snapshot de jugador copiado e interceptado, sin acciones ni cambios de partida: modelos y fondos cargan, zoom/reset funciona, al cerrar se espera el evento asíncrono del diálogo y no quedan canvas, sin overflow ni excepciones. Captura Dravak393 inspeccionada. Prueba backend de assets/CSRF/archivos privados PASS; QA pasiva4 y lectura29PASS; sintaxis/diffPASS.

Servidor actualizado PID316928 tras respaldo consistente privado before-final-species-20261007-102605.sqlite3. Ambos archivos GLB comprobados por Tailscale HTTP200/cabecera glTF; no se alteraron datos de jugadores. No nuevos paisajes ni animaciones.
