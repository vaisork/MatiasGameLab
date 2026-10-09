# Despliegue 3aac5a8 — 9 octubre 2026 UTC

Autorizado por Javier: completar la última entrega de Claude y publicar el registro en GitHub. Ejecutado por Codex desde Ubuntu por SSH/Tailscale.

- Código activado: `3aac5a8e3cd80a15c9843301909c4562953bc80d`, PR #683. Versión anterior: `0e8a1cc47e04f639bc8e9dfcd9af9b9de2995b90`.
- Incluye arte de 16 criaturas de Lethra/Nhal y venta plegada al final de la mochila. No se añadió otra funcionalidad.
- Staging: `/home/jdiaz/proyectos/vt2-staging-3aac5a8-20261009`. Los 1493 archivos del paquete coinciden con los blobs de Git y sus SHA256; se verificó el manifiesto antes y después de activar.
- Pruebas aisladas en staging con Python de Raspberry: 169 tests, 56.997 s, OK. CI de main aprobado. Script: `bash -n` OK.
- Script adjunto SHA256: `189d2ae1af5f5c3318d04f1de3ad34ff828e0b84c1f0c9edf658614bf7bc94b0`. Se corrigieron las cadenas de verificación para que cualquier fallo active ERR/rollback.
- Instalación activa: `/home/jdiaz/proyectos/vintage-telnet-nuevo`; servicio de usuario `vintage-telnet-nuevo.service`, localhost 8083. No se modificaron túneles ni se reinició la máquina.
- Respaldo privado: `/home/jdiaz/backups/vt2-before-3aac5a8-20261009T043449Z`; código, configuración y copia SQLite consistente, integridad OK. No se publica base ni credenciales.
- Activación terminó en «8. manifiesto verificado» y `RESPALDO=...` con código 0. Tablas idénticas inmediatamente después de copiar código y antes de arrancar. Se conservaron 7 cuentas y 6 personajes.
- Tras arrancar hubo cambios en un personaje: events, fatigue, last_active, quests; y en mundo: presence, version. Son campos atendidos por ticks/polling del servidor activo; no se sustituyó la base ni se alteraron cuentas/aprobaciones. Integridad posterior OK. No afirmar tablas congeladas mientras hay juego activo.
- Producción: juego HTTPS y `/dm` responden 200. SHA256 público de `client/app.js` coincide con main: `484600b95ab93776a3a18e3599eeb6ef21b07c9cdc02c6ee101e32eec9f4513c`.

Juego: https://raspberrypi.tail3d212e.ts.net/ ; DM: https://raspberrypi.tail3d212e.ts.net/dm

## Límites y relevo

Se comprobó disponibilidad y código servido, sin entrar con jugadores reales ni certificar una sesión humana completa. La revisión visual de 0e8a1cc publicada en `review/latest-0e8a1cc/` detectó un problema del botón de alejar tras Ver todo a 320/393 px; sigue pendiente y no se modificó en este despliegue. El mapa ilustrado conserva el estado de candidato de arte documentado por su entrega.

Consumidor siguiente: programador/revisor de VT2. GitHub contiene código, arte, script y evidencia; Ubuntu conserva los paquetes; Raspberry ejecuta la versión indicada y conserva partidas privadas. La copia histórica de trabajo en `/tmp/vt2-github-publicacion` fue preservada en `/home/jdiaz/proyectos/vt2-github-publicacion-permanente`, con los 856 cambios originales intactos. No se publicó esa cola antigua encima de main.
