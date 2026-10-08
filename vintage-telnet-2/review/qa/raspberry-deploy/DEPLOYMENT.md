# Despliegue real — 7 octubre 2026

Autorización explícita de Javier para desplegar por Tailscale y sustituir los enlaces del anterior. Raspberry `100.112.10.16`, aarch64, Python 3.13.5. SSH autorizada mediante comprobación de Tailscale. No se modificaron ACL ni se publicaron credenciales.

- Instalación en `/home/jdiaz/proyectos/vintage-telnet-nuevo`, venv con requirements fijados.
- Servicio de usuario `vintage-telnet-nuevo.service`, activo y habilitado; Linger=yes. Reinicio del servicio comprobado con HTTP200. No se reinició toda la Raspberry.
- Tailscale Funnel existente conserva `https://raspberrypi.tail3d212e.ts.net`, ahora proxy a `127.0.0.1:8083`.
- Juego `/`; director `/dm`, sin enlace en pantalla de jugador. Modelos y arte servidos por el mismo origen.
- Partida nueva de Ubuntu trasladada con copia consistente SQLite, cuentas1/personajes1, integridad ok. Configuración privada transferida fuera del archivo del código y con modo0600. La copia original en Ubuntu permanece; desde el cambio de enlace, Raspberry es la instancia pública. No se fusionaron datos del motor anterior.
- Antiguo servicio de sistema `vintage-telnet.service`: detenido y deshabilitado mediante SSH root autorizada. Archivos originales conservados, configuración/SQLite respaldadas en `/var/backups/vintage-telnet-retired-20261007`, integridad ok.
- Cloudflare Ojo de Agua y demás aplicaciones no se modificaron.

Validación: suite completa111PASS en Ubuntu (50.743s) y Raspberry (28.703s inicialmente). 36 pruebas específicas de economía/multijugador/contenido después del campo visual adicional (25.567s). Navegador público real de escritorio y móvil en browser.json, entrada anónima/director separado/modelo/arteHTTP200; no constituye una partida humana autenticada prolongada. El fallo inicial de comillas en WorkingDirectory del unit se corrigió en el instalador. Se detectó404 del retrato por whitelist estática; se autorizó art/encounters/*.webp y se validó por HTTP público. No se afirma prueba de reinicio físico del equipo.

GitHub: checkout sin remoto. Código y paquete preparados; no se afirma un push. Runtime y secretos excluidos. Archivo tar.gz y git.bundle generados en dist/ (ignorado), para entregar el código sin las partidas.

Reversión: restaurar proxy Funnel a127.0.0.1:8080 y habilitar el servicio antiguo conservado, tras detener el nuevo si se necesita. Nunca restaurar respaldos sobre una partida activa ni trasladar el schema antiguo al nuevo.

Corrección posterior al intento de acceso DM de Javier: POST público reproducía403 «Origen de petición no autorizado» porque HTTP interno no representaba HTTPS del Funnel. Se activó ProxyFix sólo para esquema, opt-in VT_NEW_TRUST_PROXY_PROTO=1 en servicio de loopback; Host reenviado no se confía, CSRF y rechazo de otros orígenes se conservan. Pruebas:4focalUbuntu(incluyeprotecciónarchivos),3Raspberry; configuración correcta permite login completo en base temporal con contraseña de prueba. POST público de diagnóstico con contraseña inválida ahora recibe401 del verificador de credenciales, no403 de Origin. La contraseña real no se cambió y no se afirma haber iniciado sesión real sin disponer de ella. Servicio activo tras reinicio.

Verificación definitiva del incidente: el primer ajuste de ProxyFix por sí solo seguía devolviendo403 (el Funnel no suministró el esquema esperado). Se configuró explícitamente el origen público exacto en runtime/server.env y se mantuvieron CSRF y rechazo de otros dominios. POST real público de director llega a verificación de contraseña401 intencionalmente inválida; POST de cuenta vaison llega a verificación de credenciales401 intencionalmente inválidas. No se cambiaron contraseñas ni cuentas.5pruebas focalesUbuntu/4Raspberry pasan, incluidas sesión DM completa temporal, ausencia de cabeceras del proxy y rechazo de otro Origin.
