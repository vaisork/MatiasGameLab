# Actualización Raspberry — 8 octubre 2026

Javier autorizó explícitamente «Sube a raspberry». Se desplegó el código integrado por PR #657, commit `f55188f80ae1c2884c6959c2bbb8d7aebb1115aa`, en `/home/jdiaz/proyectos/vintage-telnet-nuevo`. Servicio `vintage-telnet-nuevo.service`, activo y habilitado, puerto local 8083. El enlace y la configuración del túnel se conservan.

- 1002 archivos del checkout verificados por SHA256 en preparación y después de instalar.
- 45 pruebas del piloto, narrativa, catálogo, posvictoria y mundo nocturno pasan en Raspberry antes del cambio, usando bases temporales.
- Respaldo previo del código, configuración privada y copia consistente de SQLite en `/home/jdiaz/backups/vt2-before-f55188f-20261008`, protegido con permisos privados. Integridad SQLite comprobada.
- Tras el reinicio se compararon las tablas accounts, account_access, characters, world, approvals, requests, dm_requests y dm_grants con el respaldo: idénticas. Tres cuentas y tres personajes conservados. No se sustituyó la base con una copia Ubuntu.
- Instalación aditiva: archivos privados, runtime, venv y arte anterior conservados. No se elimina contenido local no incluido en Git. Dependencias existentes compatibles.
- Juego `/`, director `/dm`, nuevas ilustraciones y miniaturas responden HTTP200 en HTTPS público. POST públicos con CSRF/Origin correctos y credenciales deliberadamente inválidas reciben401: llegan a validación de credenciales, sin el antiguo403 de origen.
- Chrome real, anónimo, 393 y 1440 px: entrada del juego y del DM sin desbordamiento ni errores de ejecución. No se afirma sesión autenticada real ni partida humana prolongada. Evidencia en `public-check.json`.

El servicio se detuvo durante la copia del código y volvió a iniciar correctamente. Se preparó reversión automática del código si fallaba la activación; no fue necesaria. No se reinició físicamente el equipo ni se modificaron otros servicios.

Marca de versión instalada: `runtime/deployed-version.txt`. Para revertir, detener el servicio, restaurar el código de la carpeta `code/` del respaldo y reiniciarlo, preservando runtime y partidas. No restaurar SQLite sobre una partida activa.
