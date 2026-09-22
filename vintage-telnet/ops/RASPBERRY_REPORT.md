# Respuesta del operador Raspberry

Estado actual: **INSTALADO COMO SERVICIO SYSTEMD Y VERIFICADO**. El despliegue
histórico de `codex/vintage-telnet-server` (PR #1) fue dado de baja y
reemplazado por `claude/vintage-telnet-server-v2` (PR #6) en el mismo puerto
(8080, loopback). Los apartados de abajo documentan primero la prueba manual
previa (sin systemd) y luego la instalación systemd final.

## Instalación systemd final — 2026-09-22T05:27:53Z

- Ejecutado por Javier con `sudo` localmente (`ops/install_v2_authorized.py`,
  script preparado por el operador; no ejecutado por el operador porque no
  hay sudo no interactivo disponible en esta sesión).
- SHA instalado: `8b1e13859fc02c636963d93c1533e482d1565dc9` (HEAD de
  `claude/vintage-telnet-server-v2` en el momento de instalar; solo
  `AGENTS.md`/`RASPBERRY_REPORT.md` cambiaron respecto a `db50026`, cero
  cambios de código servidor).
- Servicio viejo (Codex, PR #1) detenido y deshabilitado; su symlink de
  `multi-user.target.wants` removido. Datos viejos (schema_version 1)
  movidos a `/var/lib/vintage-telnet-codex-old-20260922T051927Z`, **no
  borrados**. `server.env` viejo movido a
  `/etc/vintage-telnet/server.env.codex-old-20260922T052753Z`. Unit anterior
  respaldada en `/etc/systemd/system/vintage-telnet.service.codex-old-20260922T051927Z`.
- Instalación nueva: venv + dependencias exactas de `requirements.txt`
  instaladas; **28/28 pruebas OK** (7.9s) corridas como usuario `vintage-telnet`
  antes de activar el servicio; `pip check` OK.
- `VT_SECRET_KEY` generado en la Raspberry (32 bytes aleatorios, no
  compartido); `VT_DM_PASSWORD` provisto por Javier en el momento de
  instalar, escrito únicamente en `/etc/vintage-telnet/server.env`
  (root:root, 0600), nunca en un archivo del repositorio ni mostrado en logs.
- Verificación independiente del operador tras la instalación:
  `systemctl status` → `active (running)`, `enabled` (sobrevive reinicio de
  la Raspberry). `curl http://127.0.0.1:8080/healthz` →
  `{"schema_version":2,"status":"ok"}`. `readlink -f /opt/vintage-telnet/current`
  → apunta al release `8b1e138...` correcto.
- **Primer intento de instalación falló** por dos bugs del script preparado
  por el operador, ambos corregidos en el momento y documentados aquí para
  quien reutilice `install_v2_authorized.py`:
  1. El SHA autorizado quedó desactualizado en el script porque el operador
     hizo push de un commit de documentación (firma en `AGENTS.md` + este
     reporte) *después* de escribir el script pero *antes* de que Javier lo
     corriera — el script exigía el HEAD viejo. Corregido apuntando al HEAD
     real. Lección: generar el script leyendo el HEAD en el momento de
     ejecutarlo, no fijarlo de antemano si puede haber commits de
     documentación entre medio.
  2. `server.env` se escribía con modo `"x"` (crear solo si no existe), que
     falló porque el despliegue viejo de Codex ya tenía un `server.env` en
     esa ruta. El primer intento alcanzó a apagar el servicio viejo, mover
     sus datos y crear el release nuevo completo (venv, dependencias, 28
     pruebas OK) pero se cortó ahí, dejando **el servicio completamente
     caído unos minutos** (ni el viejo ni el nuevo respondían) hasta la
     segunda corrida corregida. Ningún dato se perdió (todo movido, no
     borrado), pero es un hueco de disponibilidad real a tener en cuenta
     para el próximo cambio de release: idealmente no detener/deshabilitar
     el servicio viejo hasta que el nuevo esté listo para activarse.
- Accesos directos creados en el escritorio de la Raspberry a pedido de
  Javier: `Vintage-Telnet-Juego.desktop` (`http://127.0.0.1:8080`) y
  `Vintage-Telnet-DM.desktop` (`http://127.0.0.1:8080/dm`). Existía además un
  `Vintage-Telnet.desktop` previo que apuntaba a la misma URL del juego
  (antes servía Codex, ahora sirve esta entrega); queda duplicado, pendiente
  de que Javier decida si lo borra.
- **Prueba de navegador contra el servicio systemd (127.0.0.1:8080), 2026-09-22
  ~05:32 UTC:** hecha desde el navegador de escritorio de la propia Raspberry
  ("Browser 1", Linux — no la PC de Javier), usando los dos accesos directos
  recién creados. Cuenta `vtprueba_systemd` registrada → jugador **#0001**
  pendiente visible en `/dm` con la contraseña real de producción → aprobada
  → especie **Humano** elegida → aparece en sala inicial "Valdren". Confirma
  que la instalación systemd funciona igual que la prueba manual anterior
  (puerto 8081) y que los dos accesos directos del escritorio apuntan a la
  URL correcta.
- Javier borró el `Vintage-Telnet.desktop` duplicado; quedan solo
  `Vintage-Telnet-Juego.desktop` y `Vintage-Telnet-DM.desktop` en el escritorio.
- **Pendiente:** reinicio físico de la Raspberry con el servicio activo,
  todavía no probado.

## Prueba manual previa (sin systemd) — 2026-09-22

- **Fecha UTC y operador:** 2026-09-22T04:47–05:02 UTC aprox.; Agente que opera
  la Raspberry Pi — Vintage Telnet (Claude).
- **Commit completo instalado / versión:** `db5002684f5b8cd5d8b915e6e586cf6f1cf79a8f`,
  rama `claude/vintage-telnet-server-v2` (PR #6), checkout `/home/jdiaz/MatiasGameLab`,
  árbol limpio (`git status` sin cambios de código antes de empezar).
- **Directorio release y checkout limpio comprobado:** sí, `git status` limpio
  tras `git checkout` + `git pull origin claude/vintage-telnet-server-v2`
  (fast-forward `18d0fc6..db50026`).
- **Modelo / arquitectura / SO / Python / SQLite:** Raspberry Pi 5 Model B,
  aarch64, Debian 13 (trixie), kernel `6.18.50+rpt-rpi-2712`; Python 3.13.5;
  SQLite 3.46.1 (módulo `sqlite3` del venv).
- **`pip check` y suite (comando, salida resumida, código de salida):**
  `.venv/bin/pip install -r requirements.txt` OK (Flask 3.1.3, Werkzeug 3.1.6,
  waitress 3.0.2, click 8.5.0, itsdangerous 2.2.0, blinker 1.9.0, Jinja2 3.1.6,
  MarkupSafe 3.0.3). `.venv/bin/python -m pip check` → `No broken requirements
  found.`, código 0. `.venv/bin/python -B -m unittest discover -s tests -v` →
  **28/28 pruebas OK**, 7.937s, código 0 (8 en `test_entry.py`, 19 en
  `test_gameplay.py`, 1 en `test_http.py`).
- **Configuración no secreta (bind, puerto, hosts, HTTP/HTTPS, ruta datos):**
  `VT_HOST=192.168.86.34` (IP LAN real de la Pi, no loopback — ver nota),
  `VT_PORT=8081` (8080 ya ocupado por el despliegue systemd previo de
  `codex/vintage-telnet-server`, PR #1 histórico), `VT_TRUSTED_HOSTS=
  localhost,127.0.0.1,192.168.86.34`, `VT_ALLOW_HTTP=1` (solo prueba LAN),
  `VT_DATA_DIR=/home/jdiaz/vintage-telnet-data-claude` (fuera del checkout;
  no pude usar `/var/lib/vintage-telnet` porque requiere sudo y no hay sudo
  no interactivo disponible ahora — además esa ruta ya la usa el proceso
  systemd de PR #1 con un esquema incompatible, así que de todos modos
  convenía mantenerlas separadas). `VT_SECRET_KEY` generado con
  `secrets.token_hex(32)`, no compartido aquí. `VT_DM_PASSWORD` provisto
  directamente por Javier en el chat, no escrito en ningún archivo del repo.
- **Servicio / listener / salud (comandos y resultados):** sin systemd; proceso
  manual (`nohup ... python -m server &`), ejecutado **fuera del sandbox de
  la herramienta de shell** (ver nota) para que fuera alcanzable por un
  navegador real. `ss -ltnp` confirma `LISTEN 192.168.86.34:8081`.
  `curl http://192.168.86.34:8081/healthz` → `{"schema_version":2,"status":"ok"}`.
  Reinicio manual del proceso durante la prueba (ver más abajo) sin errores
  en el log (`INFO:root:...inicia...`, `INFO:waitress:Serving on...`, sin
  tracebacks).
- **Dispositivo y navegador utilizado / misma LAN:** Chrome real en la PC
  Windows de Javier (extensión "Claude in Chrome", dispositivo "Browser 2"),
  confirmado explícitamente por Javier, conectado a la IP LAN de la Pi
  (`192.168.86.34:8081`) — no localhost del propio dispositivo. Cumple la
  prueba de "otro dispositivo en la misma LAN" del protocolo.
- **Nota — sandbox vs. red real:** el primer intento de arrancar el servidor
  desde el shell quedó dentro de un sandbox de red que no era alcanzable por
  el navegador real (aunque sí por `curl` desde el mismo shell). Se relanzó
  el proceso con el sandbox deshabilitado para esa operación puntual; una vez
  hecho, quedó alcanzable normalmente desde la LAN.
- **Jugador de prueba: UUID y número antes/después de desconectar:**
  `6da9bd7a-99fc-4445-9ee1-433fae6f0e63`, jugador **#0001**, usuario
  `vtprueba_operador`. Igual antes y después de cerrar la pestaña y abrir una
  nueva (simulación de "cerrar y volver a entrar"): misma sala
  (`Forja de Valdren` / `valdren_forja`), misma especie (`humano`).
- **UUID/número antes/después de reiniciar servidor:** idénticos
  (`6da9bd7a-...`, #0001) tras matar y relanzar el proceso `python -m server`
  con la misma configuración; sala y especie también idénticas después del
  reinicio, confirmado en el navegador y con `server.admin ... players`.
- **Fecha de creación intacta / último acceso actualizado / eventos
  observados:** `created_at` = `2026-09-22T04:50:42.878319+00:00`, sin
  cambios en ninguna verificación. `last_access_at` no se actualizó porque no
  se ejecutó un `/login` explícito después del registro inicial (la sesión
  siguió viva por cookie); no se probó el flujo de login con usuario/clave
  por separado en esta entrega — **pendiente** si se considera necesario.
  Único evento en `access_events`: `register` (id 1).
- **Contraseña incorrecta / duplicado / logout / segundo jugador:** no
  probado manualmente en esta sesión (sí lo cubre la suite automatizada:
  `test_wrong_password_duplicate_and_unique_numbers`,
  `test_csrf_logout_revocation_and_expiry`, `test_dm_login_wrong_password_rejected`,
  todas OK). Prueba manual específica de estos casos: **pendiente**.
- **Permisos / espacio / respaldo / integridad / restauración aislada:**
  `VT_DATA_DIR` en `/home/jdiaz/vintage-telnet-data-claude`, propiedad de
  `jdiaz` (no del usuario de sistema `vintage-telnet`, porque no hay
  instalación systemd todavía). `server.admin ... check` →
  `{"integrity": ["ok"], "foreign_key_errors": 0, "schema_version": 2}`.
  Espacio libre en disco: 34 GB de 59 GB. No se hizo respaldo
  (`server.admin ... backup`) en esta entrega porque no es una instalación de
  producción; **pendiente** para cuando se instale como servicio real.
- **Reinicio físico:** no realizado (no fue solicitado para esta prueba;
  solo se reinició el proceso del servidor, no la Raspberry).
- **Logs saneados relevantes:** log completo del proceso (`stdout`/`stderr`
  combinados), sin contraseñas ni tokens:
  ```
  INFO:root:Vintage Telnet inicia en 192.168.86.34:8081; esquema 1
  INFO:waitress:Serving on http://192.168.86.34:8081
  ```
  (repetido igual tras el reinicio del proceso). Nota menor para el
  desarrollador: el mensaje de log dice "esquema 1" pero `/healthz` informa
  `schema_version: 2` — mensaje de log desactualizado, no es un fallo
  funcional; lo devuelvo como observación, no lo corregí yo.
- **Errores: pasos exactos, esperado, obtenido:** ninguno funcional. Único
  contratiempo fue operativo (browser no alcanzaba `127.0.0.1` por estar en
  otra máquina/sandbox que el servidor) y se resolvió usando la IP LAN real,
  como indica `RASPBERRY_HANDOFF.md` para pruebas de dispositivo.
- **Cambios operativos realizados:** creación de venv e instalación de
  dependencias en `vintage-telnet/.venv` (no versionado); creación de
  `/home/jdiaz/vintage-telnet-data-claude` (fuera del repo, no versionado);
  un proceso manual del servidor arrancado y luego reiniciado una vez para
  la prueba de persistencia; sin cambios de código, sin cambios en Ojo de
  Agua, sin tocar router/firewall/túneles; nada expuesto a Internet.
- **Pendientes y decisión necesaria del agente repositorio/Arquitecto/Javier:**
  1. Definir si instalar como servicio systemd real (`ops/vintage-telnet.service`
     usa las mismas rutas `/opt/vintage-telnet` y `/var/lib/vintage-telnet`
     que ya ocupa el despliegue histórico de `codex/vintage-telnet-server`
     PR #1 — **colisionarían** si se instalan ambos con la config actual;
     hay que decidir si el PR #1 se da de baja primero, o si esta entrega usa
     rutas/puerto distintos en producción).
  2. Probar explícitamente login con usuario/contraseña por separado del
     registro (para refrescar `last_access_at`), y los casos de contraseña
     incorrecta/duplicado/logout manualmente desde el navegador (ya cubiertos
     por la suite, pero no por mí a mano).
  3. Probar segunda especie / segundo jugador y verificar números distintos
     manualmente (cubierto por suite, no por mí a mano).
  4. Decidir política de respaldo antes de cualquier instalación real con
     datos que importen.
  5. Reinicio físico de la Raspberry con el servicio activo: no probado,
     pendiente si se decide instalar como systemd.

No adjuntar contraseñas, claves, cookies, hashes ni bases. No afirmar resultados
de pruebas que no se ejecutaron. Acceso desde fuera de casa: fuera de esta entrega.
