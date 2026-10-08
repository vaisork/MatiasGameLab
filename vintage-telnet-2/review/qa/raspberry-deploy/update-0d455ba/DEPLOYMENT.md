# Activación autorizada 0d455ba — 8 octubre 2026

Javier autorizó ejecutar el script preparado por Claude. Se revisó contenido y sintaxis antes de transferirlo por SCP y ejecutarlo por SSH en Raspberry100.112.10.16. SHA256 del script: `027ef1619d13ef6d17a414734414170242dda40a905c8d722e0842ede3f5b644`. No se modificó.

Instalado `0d455baf255f8b5490daa18850d7492cfb2a8f91` (PRs663,664,665), sustituyendo d5f605c. Staging `/home/jdiaz/proyectos/vt2-staging-0d455ba-20261008`:1294 archivos SHA256 comprobados antes de ejecutar y por el script. La preparación declara152 tests OK; no se repitió la suite durante activación.

Servicio `vintage-telnet-nuevo.service`, instalación `/home/jdiaz/proyectos/vintage-telnet-nuevo`, runtime y .venv preservados. Respaldo de código/configuración y copia SQLite consistente con integrity_check correcto. Las nueve tablas idénticas antes/después, tres cuentas y tres personajes conservados. Reversión disponible, no utilizada ni ensayada provocando fallo.

El comando terminó con código0 y:

```text
8. manifiesto verificado en la instalación activa
RESPALDO=/home/jdiaz/backups/vt2-before-0d455ba-20261008T224618Z
```

Servicio activo, localhost HTTP200 y versión nueva registrada. Comprobación adicional anónima HTTPS de `/` y `/dm`:200, evidencia en public-check.json. No certifica login ni partida humana; Javier realizará su propia revisión. No se cambiaron túneles ni se reinició físicamente Raspberry.
