# Criatura vencida, números y visor — 2026-10-07

Se cerraron los tres reportes del usuario:

- Evaluar requería conocimiento en bestiario pero no presencia viva. Ahora usa la misma presencia que combate/examinar criatura y rechaza acciones antiguas contra un enemigo ausente. La evaluación indica nivel del rival y del jugador; no afirma que un jugador30 siga en primera formación. En Surcos, day/examine se adaptan al enfriamiento de la derrota o refugio: tallos aplastados y ausencia de movimiento. Al volver una criatura tras el plazo se restaura el contenido habitual. No cambia el plazo de reaparición ni recompensa/balance.
- Personaje e información de la sala muestran vitalidad/fatiga enteras, usando ceil como ya hacía el panel de combate. El cálculo interno conserva fracciones. Herida null se muestra «Sin herida», en lugar del anterior «Sin información».
- El visor de especies en computadora aumenta de260px a340–540px según pantalla; móvil conserva260px. Los fondos existentes se muestran como capa CSS desenfocada4px, saturación65%, opacidad38%, detrás de un canvas transparente. La figura permanece nítida. No nuevas imágenes de paisajes ni cambios en originales. Carga/controles quedan por encima; cierre elimina capa y cancela callbacks de imagen.

Validación: suite104PASS40.927s, incluidas tres regresiones: victoria real mediante tick elimina evaluar/contactos, detalle sin movimiento hasta reaparición; huella persistente/refugio no habilita evaluación; personaje30 evalúa con nivel real. Chrome320/393/1440 cinco modelos/fondos/zoom/cierre sin overflow ni excepciones; adicional888px y captura Felaryn inspeccionada. Prueba de enteros274/274, fatiga3 y Sin herida en Personaje/información sala, valores internos intactos. Zoom botones/rueda/pinch/reset/disposal320/393/1440PASS. QA lectura29 y pasiva4PASS, sintaxis/diffPASS. Pruebas visuales interceptan snapshot de copia read-only, sin acciones ni escrituras en producción.

Servidor reiniciado tras respaldo consistente privado. Partidas preservadas; HTTP200 local/Tailscale. Los textos antiguos en el historial siguen siendo recuerdos; una nueva decisión Mirar/Observar muestra el estado corregido.
