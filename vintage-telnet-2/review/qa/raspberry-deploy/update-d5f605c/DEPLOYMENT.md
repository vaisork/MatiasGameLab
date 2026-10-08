# Despliegue d5f605c — 8 octubre 2026

Javier autorizó ejecutar la activación preparada por Claude de PR #662. Instalado `d5f605c36b2fe33ae4bb95c94dc2cc5dd3bba2fb` en Raspberry `100.112.10.16`, carpeta `/home/jdiaz/proyectos/vintage-telnet-nuevo`. Servicio de usuario `vintage-telnet-nuevo.service` activo; puerto interno127.0.0.1:8083. Versión anterior: d5ee227.

## Revisión y ejecución

El script original se leyó en `/home/jdiaz/proyectos/vt2-deploy-d5f605c/activar.sh`. SHA256 `33cbed473aa723be5b4ad8b3a574d54df64c4793e5174efc36456a62c7efca19`; sintaxis bash correcta. La ruta temporal inicial no contenía el script, por lo que no se ejecutó aquella orden.

Antes de activar se preparó una copia revisada: `activar-ejecutado.sh`, SHA256 `52ea0d58af5ac09911b9a4e4743bfeebce2784027f8a7b2353aacf5ed1ca2637`. Se añadió trap ERR para fallos no cubiertos por los llamados explícitos a rollback, se detiene el servicio antes de restaurar código y se recupera la marca de versión previa; además se verifican manifiesto y tablas después de copiar, antes de arrancar. Se conserva `activar-claude.sh` como fuente original. La reversión no fue necesaria ni se probó provocando fallos en producción.

La copia revisada se transfirió como `/home/jdiaz/proyectos/vt2-activar-d5f605c.sh` y se ejecutó mediante SSH como jdiaz. Código de salida0. Terminó exactamente con:

```text
8. manifiesto verificado en la instalación activa
RESPALDO=/home/jdiaz/backups/vt2-before-d5f605c-20261008T202513Z
```

## Comprobaciones

- Staging `/home/jdiaz/proyectos/vt2-staging-d5f605c-20261008`:1239 archivos contra MANIFEST.sha256, sin discrepancias, comprobados previamente y nuevamente por la activación.
- Claude y Javier informaron150 pruebas aprobadas en Raspberry durante preparación. No se repitió la suite en esta ejecución; la activación añadió comprobaciones de integridad, hashes, servicio y conservación.
- Respaldo de código y configuración; servicio detenido para copia SQLite consistente mediante sqlite3.backup. integrity_check correcto. Directorio del respaldo700; SQLite600, comprobados después.
- Copia preserva runtime y .venv; no se restauró SQLite desde Ubuntu. Las nueve tablas coinciden antes/después de copiar y tras arrancar: accounts, account_access, approvals, audit, characters, dm_grants, dm_requests, requests y world. Tres cuentas y tres personajes conservados.
- Localhost HTTP200; marca `runtime/deployed-version.txt` contiene el SHA completo nuevo.
- GET HTTPS público del juego `/` y DM `/dm`:200 y contenido HTML de Vintage. Evidencia fechada: `public-check.json`. Comprobación anónima: no acredita login de usuarios, partida humana ni revisión visual móvil.
- No se cambiaron túneles, configuración privada ni otros servicios. No se reinició físicamente Raspberry.

Juego: https://raspberrypi.tail3d212e.ts.net/ . DM: https://raspberrypi.tail3d212e.ts.net/dm .

Este documento registra una ejecución concreta, no autoriza futuros despliegues. El respaldo conserva código y partida previos; restaurar la base sobre progreso posterior exige decisión independiente. Los scripts archivados son evidencia de esta ejecución, no instrucciones para volver a ejecutar automáticamente.
