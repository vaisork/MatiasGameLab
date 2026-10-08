# Despliegue autorizado d5ee227 — 2026-10-08

Javier pidió «despliega» tras PR #660. Instalado `d5ee22799c83e7c32cb076fd70df1b1885e45d9f` en `/home/jdiaz/proyectos/vintage-telnet-nuevo`, servicio usuario `vintage-telnet-nuevo.service`, localhost8083. Activo y habilitado.

- 1072 archivos verificados SHA256 antes y después de instalar. Archivo transferido: SHA256 `579f6a672c1457a9158c11e2509664372abe42fe14e47d176b9d4ff1b04fda42`.
- Staging `/home/jdiaz/proyectos/vt2-staging-d5ee227-20261008`.
- 32 pruebas focales en Raspberry pasan (spatial_world, map, real_content, mud_pilot), usando datos aislados.
- Respaldo privado: `/home/jdiaz/backups/vt2-before-d5ee227-20261008T190419Z`, código, configuración y copia SQLite consistente. Integridad correcta.
- Todas las nueve tablas idénticas antes de arrancar. Tras activar, cuentas, accesos, personajes, mundo, aprobaciones, requests, dm_requests y dm_grants idénticos al respaldo. Tres cuentas y tres personajes conservados.
- Copia aditiva preserva runtime, venv y contenido local. No se restauró una base Ubuntu, no se alteró el proxy ni se reinició físicamente Raspberry.
- Juego, DM y arte de muestra responden200 en HTTPS. POST con CSRF/Origin y credenciales falsas recibe401: validación de origen correcta, sin usar contraseñas reales.
- Chrome anónimo393/1440: sin desbordamiento ni errores; evidencia `public-check.json`. No certifica sesión autenticada humana ni juego prolongado.

Marca instalada `runtime/deployed-version.txt`. La autorización cubre esta ejecución, no versiones posteriores. Guía de entornos/SSH/actualizaciones: `docs/VT2_RELEVO_20261008.md` en la raíz del monorepo.
