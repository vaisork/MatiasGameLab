# Revisión de main0e8a1cc

Revisión solicitada por Javier, sin modificar juego ni desplegar. Comparación contra707ee34. Fuente exacta origin/main0e8a1cc extraída con git archive, dejando intacta la rama del otro programador. El SHA256 de client/app.js público coincide con ese main; no se leyó la marca instalada por SSH, pues Tailscale solicitó renovar autenticación.

## Hallazgo reproducible

P2 — Alejar mapa acerca después de Ver todo en móviles con mundo completo conocido. client/app.js:273 fija mínimo0.05, mientras que el encuadre automático puede ser menor. Fixture de183salas conocidas, cuenta temporal y encuentro real iniciado por API:320px, escala0.0328587→0.05;393px,0.0428532→0.05. Solución propuesta: mínimo de zoom compatible con escala de encuadre, y asegurar que el botón de alejar nunca aumente escala. No se implementó en esta revisión.

## Cambios y comprobaciones

Mapa ilustrado2400x2880 con máscara de niebla, celdas cuadradas, zoom ampliado. Su entrega review/art-integration-20261009-mapa/REVIEW.md declara que el candidato no está aprobado artísticamente y algunos ramales no calzan; se integra como prueba autorizada. No atribuirle correspondencia exacta de todos los caminos.

Bestiario prioriza enemigo actual, luego criaturas cercanas. Confirmado visualmente: Espinajo antes de Pinzajunco, etiqueta Te enfrentas ahora. No aparecen criaturas nuevas por la ordenación.

Terminal sigue líneas urgentes: prueba393/1440 con snapshot propio generado y eventos sintéticos, siguiendo después de Ir a lo último. Llega al fondo con mensajes nuevos y conserva posición si el lector sube manualmente. Inicio arriba tras nueva visita es comportamiento deliberado, no fallo. Se ajustó la prueba para esperar el intervalo real de polling3s.

Navegador Chrome320/393/768/1440: sin overflow horizontal ni errores JS en mapa y bestiario. Capturas393 inspeccionadas. QA mapa15checks y passive4casos aprobados; cuatro tests Python test_map aprobados. No se repitió suite completa. No certifica dispositivo móvil físico, juego prolongado ni perfección visual de las183salas.

Género se elige al crear; el perfil sólo permite completar personajes antiguos sin género. El último diff no cambia reglas numéricas de combate. No se reescribió narrativa ni balance.

Evidencia: browser.json, terminal.json, capturas y scripts. Fixture en SQLite temporal, sin jugadores/DB reales. Los scripts mantienen rutas locales explícitas de herramientas y fuente archivada; no son comandos de producción. Informe publicado junto al registro del despliegue de 3aac5a8. El hallazgo de zoom queda pendiente; esta entrega no modifica el juego.
