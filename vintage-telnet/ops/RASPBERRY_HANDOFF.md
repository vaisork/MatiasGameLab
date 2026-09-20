# Transferencia al operador Raspberry — Vintage Telnet 0.1.0

## Estado y coordinación

Preparado por **Desarrollador de Servidor de Vintage Telnet**, 2026-09-20.
El estado real de despliegue se registra en `RASPBERRY_REPORT.md`; la preparación
original solo se probó localmente. Javier amplió la función del desarrollador
para actuar también como puente directo con el operador remoto (2026-09-20).
El operador instala, configura y verifica; no diseña mecánicas ni hace cambios
independientes en el servidor. Devuelve resultados mediante `RASPBERRY_REPORT.md`.
Si encuentra un problema, conserva evidencia sin secretos y lo devuelve al agente
del repositorio. Este corrige, prueba y entrega un nuevo commit; el operador instala
ese commit. No editar código directamente en `/opt` ni hacer commits de datos vivos.

Versión de esta entrega: **0.1.0**, etiqueta propuesta **`vintage-telnet-v0.1.0`**,
rama de preparación `codex/vintage-telnet-server`. Base leída:
`bb2fef58ee1607d216e3bbc77b3d623489d24e9b`.
El commit de implementación se informa en la entrega final del agente. No instalar
el HEAD base: solo contiene documentación. El puente publica la rama técnica
para instalación por SHA y revisión; esto no integra `main` ni publica Senku.
La etiqueta 0.1.0 identifica la preparación inicial; el operador debe usar el SHA
de despliegue comunicado por el puente, que puede incluir correcciones posteriores.
No sustituir el SHA por `main` o `latest`.

El integrador debe volver a leer `main`, preservar trabajo concurrente y publicar
la versión revisada. Si integra por squash o cambia código, debe comunicar el
**nuevo SHA completo**, volver a validar y actualizar la referencia de entrega.
El operador registra y verifica ese SHA antes de instalar. Nunca mueve una etiqueta
existente para representar otro contenido.

## Requisitos

- Proyecto remoto exclusivo de MatiasGameLab y tarea exclusiva de Vintage Telnet.
  No usar el proyecto `/home/jdiaz/ojo-de-agua` ni conversaciones de ese proyecto.
  Checkout propuesto: `/home/jdiaz/MatiasGameLab-deploy`; debe registrarse como un
  proyecto remoto independiente en Codex antes de asignar trabajo al operador.
  Las instrucciones enviadas inicialmente al hilo general «Conéctate desde tu
  celular» quedaron revocadas por el puente el 2026-09-20. No retomarlas allí.

- Raspberry Pi OS/Debian con systemd, Python **3.11+**, módulo sqlite3, venv y pip.
- Git, acceso de lectura a `vaisork/MatiasGameLab`, sudo para preparar el servicio.
- Disco local persistente con espacio libre. Registrar modelo, arquitectura, SO,
  Python y SQLite; este repositorio no presupone qué Raspberry tiene Javier.
- Dependencias Python fijadas en `requirements.txt`; sin Docker, Node ni base externa.
- Archivos: checkout exacto para trazabilidad; en ejecución solo `server/`, plantillas,
  `requirements.txt` y configuración externa. `tests/` para verificar; `ops/` para operar.
  No copiar documentos del mundo al cliente ni servir todo el checkout por HTTP.

## Instalación inicial (ejecutar en la Raspberry, no en el equipo del repositorio)

Obtener primero del puente o integrador el SHA publicado. Reemplazar el marcador; no seguir
si falta. Los comandos asumen una instalación nueva y rutas libres. Si ya existe
un servicio/base, inspeccionarlos y seguir el apartado de actualización, sin borrarlos.

```sh
sudo apt-get update
sudo apt-get install -y python3 python3-venv git curl
python3 --version
python3 -c 'import sqlite3; print(sqlite3.sqlite_version)'
uname -a
df -h /var/lib
export VT_RELEASE='PEGAR_SHA_COMPLETO_PUBLICADO_POR_EL_INTEGRADOR'
test "${#VT_RELEASE}" -eq 40 || exit 1
git clone https://github.com/vaisork/MatiasGameLab.git "$HOME/MatiasGameLab-deploy"
cd "$HOME/MatiasGameLab-deploy"
git fetch origin --tags
git checkout --detach "$VT_RELEASE"
test "$(git rev-parse HEAD)" = "$VT_RELEASE" || exit 1
test -z "$(git status --porcelain)" || exit 1

sudo useradd --system --user-group --home-dir /var/lib/vintage-telnet --shell /usr/sbin/nologin vintage-telnet
sudo install -d -m 0755 /opt/vintage-telnet/releases
sudo install -d -m 0700 -o vintage-telnet -g vintage-telnet /var/lib/vintage-telnet
sudo install -d -m 0700 /etc/vintage-telnet
sudo install -d -m 0755 "/opt/vintage-telnet/releases/$VT_RELEASE"
git archive "$VT_RELEASE" | sudo tar -x -C "/opt/vintage-telnet/releases/$VT_RELEASE"
sudo python3 -m venv "/opt/vintage-telnet/releases/$VT_RELEASE/vintage-telnet/.venv"
sudo "/opt/vintage-telnet/releases/$VT_RELEASE/vintage-telnet/.venv/bin/python" -m pip install -r "/opt/vintage-telnet/releases/$VT_RELEASE/vintage-telnet/requirements.txt"
sudo ln -s "/opt/vintage-telnet/releases/$VT_RELEASE" /opt/vintage-telnet/current
sudo install -m 0600 vintage-telnet/ops/server.env.example /etc/vintage-telnet/server.env
python3 -c 'import secrets; print(secrets.token_hex(32))'
sudoedit /etc/vintage-telnet/server.env
```

Pegar la clave recién generada como `VT_SECRET_KEY`, conservarla solo en la Raspberry
y en su respaldo privado de configuración. El ejemplo sin reemplazar no arranca.
No pegar esa clave en reportes. Dejar inicialmente `VT_HOST=127.0.0.1`, puerto 8080,
hosts permitidos `localhost,127.0.0.1`, `VT_ALLOW_HTTP=1` y datos en `/var/lib/vintage-telnet`.
La base `vintage.sqlite3` y sus auxiliares WAL/SHM se crearán allí al iniciar.

```sh
cd /opt/vintage-telnet/current/vintage-telnet
sudo -u vintage-telnet .venv/bin/python -B -m unittest discover -s tests -v
sudo .venv/bin/python -m pip check
sudo install -m 0644 ops/vintage-telnet.service /etc/systemd/system/vintage-telnet.service
sudo systemctl daemon-reload
sudo systemctl enable --now vintage-telnet
sudo systemctl status vintage-telnet --no-pager
curl --fail http://127.0.0.1:8080/healthz
sudo ss -ltnp | grep ':8080'
```

Esperado: pruebas correctas, servicio activo, listener en loopback y JSON
`{"schema_version":1,"status":"ok"}`. Un fallo debe investigarse antes de continuar.
El test HTTP utiliza su propia base temporal y no registra jugadores reales.

## Prueba desde un iPad/teléfono en la misma LAN

Identificar la IPv4 privada real de la Raspberry (`hostname -I`, revisar interfaz).
En `server.env`, cambiar `VT_HOST` a **esa IP privada** y añadirla a
`VT_TRUSTED_HOSTS` (valores separados por comas, sin esquema ni puerto).
Reiniciar. Abrir `http://IP_PRIVADA:8080` desde el dispositivo en la misma LAN.
HTTP permite ver credenciales a quien intercepte la red: utilizar solo cuentas
de prueba y contraseñas no reutilizadas en una LAN confiable. Si la red no es
confiable, mantener loopback y remitir al Arquitecto la configuración HTTPS/acceso.
No abrir router, UPnP, port-forwarding, túneles ni publicar este listener en Internet.
Si hay firewall local, reportar el bloqueo y acordar con Javier su alcance LAN;
no deshabilitarlo globalmente. Tras cambiar a IP privada, usar esa misma IP en curl.

## Operación y observabilidad

```sh
sudo systemctl start vintage-telnet
sudo systemctl stop vintage-telnet
sudo systemctl restart vintage-telnet
sudo systemctl status vintage-telnet --no-pager
sudo journalctl -u vintage-telnet -n 100 --no-pager
sudo journalctl -u vintage-telnet -f
cd /opt/vintage-telnet/current/vintage-telnet
sudo -u vintage-telnet .venv/bin/python -m server.admin --data-dir /var/lib/vintage-telnet players
sudo -u vintage-telnet .venv/bin/python -m server.admin --data-dir /var/lib/vintage-telnet accesses
sudo -u vintage-telnet .venv/bin/python -m server.admin --data-dir /var/lib/vintage-telnet check
sudo ls -ld /var/lib/vintage-telnet
sudo ls -l /var/lib/vintage-telnet
df -h /var/lib/vintage-telnet
readlink -f /opt/vintage-telnet/current
```

Journald recoge arranque y errores, sin volcar contraseñas/formularios. La evidencia
de quién entró está en `access_events`, consultable con `accesses` (últimos 100).
`players` muestra ID, número, usuario, nombre y fechas; no hashes ni tokens.
`healthz` verifica lectura; el registro y login prueban escritura. No confundir
un servicio activo con una prueba funcional satisfactoria desde el dispositivo.

## Respaldo, actualización y retorno

Respaldar antes de actualizar y acordar copias periódicas fuera de la tarjeta SD.
La copia contiene datos privados y hashes: conservar permisos restrictivos y
almacenamiento privado; nunca adjuntarla a GitHub. La frecuencia/retención queda
por acordar con Javier. No copiar solo el archivo principal mientras hay WAL activo.

```sh
sudo install -d -m 0700 -o vintage-telnet -g vintage-telnet /var/backups/vintage-telnet
cd /opt/vintage-telnet/current/vintage-telnet
sudo -u vintage-telnet sh -c 'umask 077; .venv/bin/python -m server.admin --data-dir /var/lib/vintage-telnet backup "/var/backups/vintage-telnet/$(date -u +%Y%m%dT%H%M%SZ).sqlite3"'
```

El comando usa la API backup de SQLite y verifica integridad; no sobrescribe copias.
Guardar también `server.env` en almacenamiento privado root-only, separado del Git.

Para actualizar: obtener nuevo SHA del agente repositorio/integrador, ejecutar
`git fetch`, verificar checkout limpio y SHA, crear otro directorio `releases/SHA`,
extraer `git archive`, crear venv e instalar requisitos igual que arriba. Ejecutar
pruebas sobre esa versión antes de seleccionarla. Registrar el directorio anterior,
detener el servicio y hacer un nuevo respaldo final con escrituras detenidas.

```sh
sudo systemctl stop vintage-telnet
# Repetir el comando de backup anterior, con un nombre nuevo, antes de continuar.
readlink -f /opt/vintage-telnet/current
# VT_RELEASE debe contener el nuevo SHA, ya instalado y probado.
sudo ln -sfn "/opt/vintage-telnet/releases/$VT_RELEASE" /opt/vintage-telnet/current
sudo install -m 0644 /opt/vintage-telnet/current/vintage-telnet/ops/vintage-telnet.service /etc/systemd/system/vintage-telnet.service
sudo systemctl daemon-reload
sudo systemctl start vintage-telnet
```

Comprobar salud, inspección y login con ID anterior. No eliminar la versión anterior
ni los respaldos. Nunca ejecutar `git pull` sobre el árbol activo.

Retorno de código: solo si el esquema sigue siendo compatible, detener servicio,
apuntar `current` al directorio anterior registrado, restaurar su unidad systemd,
`daemon-reload` e iniciar. Una versión antigua rechaza esquemas desconocidos.
Si cambió el esquema, detener y devolver el problema al agente repositorio con el
respaldo disponible; no forzar una degradación ni restaurar perdiendo accesos nuevos
sin decisión explícita de Javier.

Prueba de restauración: copiar un backup a un **directorio temporal separado** con
nombre `vintage.sqlite3` y ejecutar `server.admin --data-dir RUTA_TEMPORAL check` y
`players`; comparar ID y número. Nunca usar `/var/lib/vintage-telnet` como destino
de esta prueba. No arrancar una segunda autoridad con una copia de producción.

## Pruebas físicas obligatorias y respuesta

1. Ejecutar suite y `pip check`; registrar resultado y versiones.
2. Abrir entrada desde dispositivo, registrar cuenta de prueba, anotar UUID mediante
   `/api/me` y número mostrado; verificar fila y evento con herramientas locales.
3. Cerrar navegador/iPad, volver e iniciar sesión: misma cuenta y número. Repetir
   desde otro dispositivo/navegador, sin crear otra cuenta.
4. Reiniciar servicio; verificar mismo UUID/número, `created_at` intacta,
   `last_access_at` actualizada tras nuevo login y nuevo evento.
5. Probar contraseña incorrecta y usuario repetido; no duplican cuenta ni accesos
   exitosos. Cerrar sesión; `/api/me` queda sin autorización.
6. Crear segundo jugador: UUID y número distintos. Inspeccionar ambas cuentas.
7. Ejecutar respaldo e inspeccionar copia restaurada en directorio temporal.
8. Comprobar persistencia y servicio tras reinicio de Raspberry **en una ventana
   acordada con Javier**, porque puede alojar otros servicios. Si no se ejecuta,
   consignar expresamente pendiente.
9. Registrar listener, permisos de datos, espacio libre, logs saneados y resultado
   de prueba en dispositivo. No declarar acceso remoto comprobado por probar LAN.

Completar `RASPBERRY_REPORT.md` con commit exacto, evidencia y pendientes. Entregar
ese reporte directamente al agente repositorio en la conversación remota; el puente
consulta resultados y conserva el reporte en Git, sin intervención manual de Javier.
No cambiar código para ocultar
errores. Excluir claves, passwords, cookies, bases completas y datos innecesarios.

## Fuera de la responsabilidad del operador

No modificar Senku, reglas/canon, contenido narrativo, firmas ajenas, esquema SQL,
hashes/IDs ni archivos servidor. No resolver fallos borrando la base. No instalar
otro HEAD por iniciativa propia ni habilitar servicios públicos. Los cambios de
configuración operativa deben quedar documentados en el reporte.
