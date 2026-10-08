# Ciclo 10: cámara durante uso sostenido — antes

Defecto reproducido en aplicación real8099 con cuenta nueva/aprobaciónDM/base temporal, Humano Juramentado, viaje Valdren→Campo de surcos, búsqueda legal y mapa3D abierto. Apliqué zoom, rotación y pan; luego avance10s del reloj aislado con CSRF válido y esperé6.5s para refresco pasivo.

Lugar y nodos permanecieron exactamente iguales. La razón de búsqueda cambió61→51s. El canvas fue desmontado/remontado y perdió la cámara: cuatro etiquetas visibles pasaron a tres, y «Campo de surcos · Aquí» cambió (265,225.135)→(257.759,169.877). Las capturas muestran la brújula y la perspectiva volver a la orientación inicial. No hubo erroresJS.

Evidencia: `review/archive/2026-10-07/depth-cycle10-before/report.json` y `393-before-refresh.png` / `393-after-refresh.png`, abiertas con view_image. Prueba: `node scripts/depth-cycle10-camera.mjs`.

Autocrítica metodológica: el primer POSTadvance omitíaCSRF y recibió403. Esperar tiempo real contra un reloj fijo no reprodujo nada; ese resultado fue descartado, y la prueba válida incluye el token. No se confunde ausencia de cambio de reloj con ausencia del defecto.

Causa: el snapshot cambia por una cuenta atrás y applyPassiveSnapshot vuelve a renderizar la vista. El montaje de3D no conserva zoom/rotación/centro. Propuesta del coordinador: getter del estado de cámara y restauración sólo para mismo personaje/geometría/selección, manteniendo limpieza de recursos. Validación posterior preparada en320/393/1440, con cierre/cambio vista/contexto perdido y otro personaje de misma geometría.
