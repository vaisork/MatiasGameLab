# HANDOFF — Entrega técnica

## ENTREGA — Respuesta a la revisión del Arquitecto (PR #6)

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN

**Rama:** `claude/vintage-telnet-server-v2`

### Objetivo
Responder punto por punto a la revisión del Arquitecto en el PR #6 (`REVISIÓN DEL ARQUITECTO — NO LISTA PARA INTEGRAR TODAVÍA`).

### 1. Rebase/actualización contra `main`
Mergeado `origin/main` (traía la integración de arte, `DATABASE_GAMEPLAY_PREP.md` y `FIRST_PLAYABLE_SLICE.md`, el documento de prioridad P0 de Javier). Conflicto real solo en `AGENTS.md` (dos secciones nuevas en paralelo), resuelto conservando ambas. `HANDOFF.md` mergeó solo. 25/25 pruebas pasan después del merge.

### 2. CSP para assets — bug real confirmado y corregido
Verifiqué en consola del navegador **antes** de tocar nada: la política `default-src 'none'` sin `img-src` bloqueaba de verdad las 4 imágenes de fondo/botones (`net::ERR_BLOCKED_BY_RESPONSE` / CSP violation) — se veían en mis pruebas anteriores porque las había probado sobre `vintage-telnet.html` (PR #7, sin CSP) o sin fijarme en la consola de esta página en particular. También descubrí que el `<script>` inline de los diálogos (Personaje/Inventario/Poderes/Ayuda) estaba bloqueado por la misma razón — nunca abrían en el servidor real.
- Agregué `img-src 'self'`.
- Para el script, en vez de `'unsafe-inline'` (que debilita CSP para todo el sitio), implementé un **nonce por request** (`g.csp_nonce`, inyectado en la plantilla vía `context_processor`) y `script-src 'nonce-...'`.
- Verificado en consola: cero violaciones CSP después del cambio; los 4 diálogos abren correctamente.

### 3. Microzona interna por pueblo (P0)
`world.py` reescrito: cada uno de los 5 pueblos de inicio ahora es una microzona de 3-4 salas (`_centro`, `_forja`, `_mercado`, y `_sendero` cuando queda una cuarta dirección libre), no una sala única. El punto central conserva exactamente las mismas conexiones externas que ya existían hacia Vaisgard/caminos. Narevia (que ya usaba 2 direcciones para caminos externos) solo tiene forja+mercado, sin sendero adicional — sus 4 direcciones ya prueban N/S/E/O igualmente. Verificado con un BFS que las 22 salas resultantes son alcanzables desde Vaisgard y no hay salidas colgantes. Todo sigue marcado `[PLACEHOLDER]` explícitamente: no se presenta como canon.

### 4. Botón y comando = misma acción
Extraje la lógica de movimiento a una función única `attempt_move()`, usada por el botón (`/move`), el contrato JSON (`/api/move`) y el nuevo cuadro de texto. El cuadro de texto ahora postea a `/command`: si el texto es norte/sur/este/oeste (o n/s/e/o), ejecuta exactamente la misma acción autoritativa que el botón correspondiente; si es "mirar", refresca; cualquier otro texto sigue funcionando como chat local (fuera de alcance P0 según `FIRST_PLAYABLE_SLICE.md`, pero se conserva porque ya funcionaba y no cuesta nada mantenerlo).

### 5. Contrato estructurado de movimiento/especie
Agregué `POST /api/species` y `POST /api/move` (JSON in/out), compartiendo la misma lógica autoritativa que las rutas HTML (`attempt_choose_species`, `attempt_move`). `/api/move` responde `{accepted, previous_room, current_room: {id, name, description, exits, ...}, reason}` tal como pide `FIRST_PLAYABLE_SLICE.md`. Las rutas HTML (`/move`, `/species`) se conservan como fallback funcional para la plantilla actual, tal como el Arquitecto autorizó explícitamente. Para que un cliente JSON pueda enviar el CSRF sin parsear HTML, `GET /api/me` ahora también devuelve el token `csrf` vigente.

### 6. Pruebas agregadas (6 nuevas, 25 en total)
- CSP: `img-src 'self'` y `script-src 'nonce-...'` presentes en la respuesta, y el nonce del header coincide con el del `<script>` renderizado.
- Segunda especie (`marevyn`) confirmando que cada una llega a su propio pueblo (`narevia_centro`).
- Persistencia de especie **y sala** (no solo sesión) tras recrear la app con un dispositivo nuevo.
- Comando escrito ("norte", alias "s", "mirar", y texto libre) produciendo exactamente el mismo resultado que los botones/chat.
- Contrato estructurado `/api/species` + `/api/move` (aceptado y rechazado).
- Rate limit propio de `/dm/login` (clave separada de `/register`/`/login`, no comparten cupo).

### Bug real encontrado y corregido durante esta entrega
Al extraer `attempt_choose_species()`, el caso "ya tenías especie elegida" pasó de ser un redirect silencioso a tratarse como error renderizando la plantilla sin pasarle `room` — como en ese punto el jugador ya tenía especie, la plantilla intentaba la vista de mundo y fallaba con `UndefinedError`. Corregido separando "ya elegida" (no-op, redirect) de "especie inválida" (error real, sin necesitar `room` porque el jugador sigue sin especie en ese caso). Detectado por la propia suite de pruebas, no en manual.

### Riesgo/nota para el Arquitecto
El mínimo de contraseña de 8 caracteres sigue igual (decisión explícita de Javier, ya registrada en la entrega anterior) — no es parte de esta respuesta a la revisión.

**LISTO PARA PUBLICAR:** NO — vuelve a quedar para revisión del Arquitecto según pidió ("cuando la rama se actualice con estos puntos, volver a revisión").

---

## ENTREGA — Login real + arte integrado en el servidor (mismo origen)

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN

**Rama:** `claude/vintage-telnet-server-v2` (mismo commit base que la entrega anterior de esta rama)

### Objetivo
Javier pidió una pantalla de login real antes de entrar al mundo — no la demo local de `vintage-telnet.html` (PR #7), sino el servidor real (PR #6) con la misma identidad visual. Esto reemplaza `server/templates/entry.html` por una versión que reutiliza el arte de `vintage-telnet/assets/html-ui/` (mismo origen, sin CORS) y conecta login/registro/mundo/movimiento/chat a las rutas reales que ya existían.

### Archivos nuevos
- `vintage-telnet/assets/html-ui/` — traída desde `origin/main` (ya estaba fusionada ahí vía el PR de Arte HTML); esta rama no la tenía porque nació de un commit de `main` anterior a esa fusión.

### Archivos modificados
- `vintage-telnet/server/app.py`:
  - Nueva ruta `GET /assets/html-ui/<path:filename>` (vía `send_from_directory`, con `before_request` saltando la verificación de sesión/CSRF para esa ruta) — el servidor no tenía carpeta estática habilitada (`static_folder=None` deliberado, ver pruebas de seguridad existentes), así que agregué exactamente esta carpeta, no una carpeta estática general.
  - **Cambio de política de contraseña, a pedido explícito de Javier**: el mínimo bajó de 12 a **8 caracteres**. Se lo señalé como una reducción real de seguridad antes de hacerlo; Javier lo confirmó explícitamente sabiendo el trade-off.
- `vintage-telnet/server/templates/entry.html` — reescrito completo:
  - Login/registro real con el arte nuevo (pizarra azul + bronce + marfil), mismas rutas/campos de siempre (`/login`, `/register`, csrf).
  - Vista de mundo real: sala/descripción/salidas vienen de `GET` a `/` con los datos reales del jugador (ya no hay `rooms` simulado en JavaScript). Los botones N/S/E/O son formularios reales a `/move`; se deshabilitan cuando esa dirección no es una salida real de la sala actual.
  - Chat real: formulario a `/room/say`, mensajes mostrados vienen de `room.messages`.
  - Atacar/Huir quedan visiblemente deshabilitados con `title="Combate todavía no implementado"` — no se simula combate que no existe.
  - Personaje/Inventario/Poderes/Ayuda siguen como diálogos informativos honestos (igual que en la demo), sin JavaScript de simulación de mundo.

### Cuenta real creada
Registré la cuenta `vaisork` a través del formulario real del navegador (no por comando, para no dejar la contraseña en ningún archivo ni historial de shell) y la aprobé desde `/dm`. Contraseña con hash `scrypt` vía `werkzeug`, nunca almacenada ni mostrada en texto plano en ningún archivo de este repositorio.

### Pruebas realizadas
- Suite completa: **19/19 pruebas siguen pasando** sin modificarlas (el cambio de mínimo de contraseña no rompe ninguna, ya usaban contraseñas de prueba más largas).
- Prueba real de punta a punta en el navegador, con la cuenta `vaisork` real: registro → visible en `/dm` → aprobar → elegir especie (Dravak) → aparece en Brumak con solo la salida norte habilitada → mover al norte → llega a Vaisgard con las 4 salidas habilitadas → confirmado en `/dm` que quedó `especie=dravak`, `sala=vaisgard`.
- Verifiqué (renderizando la plantilla directo con Jinja2, con datos de Brumak) que los botones de dirección sin salida real quedan con el atributo `disabled` — al principio pensé que había un bug porque los 4 botones aparecían habilitados, pero era porque el jugador ya se había movido a Vaisgard (que sí tiene las 4 salidas) mientras yo revisaba otra pestaña.

### Qué sigue sin existir (a propósito)
Combate, inventario, personaje, poderes reales — solo quedan como paneles honestos que dicen que no existen todavía. Mapa lateral con nodos visuales (el de la demo) no se replicó; el panel lateral ahora muestra datos reales (jugador, especie, sala) en vez del mapa ficticio.

### Riesgos/conflictos
Ninguno nuevo: esta entrega solo toca archivos ya propios de esta rama (`app.py`, `entry.html`) más la carpeta de arte que ya es idéntica a la de `main`, así que al fusionar no debería haber conflicto contra la integración de arte ya publicada.

### Aviso
El mínimo de contraseña de 8 caracteres es más bajo que el estándar recomendado (12+). Fue una decisión explícita de Javier después de que se lo señalé; si más adelante se agrega más gente al servidor, vale la pena reconsiderarlo.

**LISTO PARA PUBLICAR:** NO — sigue pendiente la revisión del Arquitecto de Vintage Telnet y autorización de Javier para `main`. El servidor de prueba con la cuenta real de Javier quedó corriendo localmente para que pueda seguir jugando; no es la Raspberry Pi ni un despliegue público.

---

## ENTREGA — Claude, Desarrollador de Servidor de Vintage Telnet

**Estado:** ENTREGA PREPARADA EN RAMA, PENDIENTE DE REVISIÓN

### Desarrollador
Claude — Desarrollador de Servidor de Vintage Telnet

### Estado base
Commit/HEAD de `main` sobre el que se trabajó:
`fffc5e6ab1e295f02b76c2b6809dc07622f28b38`

### Rama
`claude/vintage-telnet-server-v2`

### Objetivo
Javier decidió adoptar la base técnica ya elegida por el Arquitecto de Vintage Telnet y Raspberry Pi (Python + Flask/Waitress + SQLite, rescatando el diseño de `codex/vintage-telnet-server` / PR #1) y pidió explícitamente sumarle encima la parte jugable que yo ya había explorado en una implementación previa en Node.js (nunca publicada): aprobación de cuentas por el Dungeon Master, especies, mundo/movimiento y chat.

### Qué se rescató de PR #1 (sin cambios de lógica)
- `vintage-telnet/server/__init__.py`, `__main__.py`
- Capa de cuentas/sesión/CSRF/rate-limit de `app.py` y `store.py` (login, registro, logout, `/api/me`, `/healthz`)
- `vintage-telnet/tests/test_entry.py`, `test_http.py` (con 2 aserciones actualizadas por el cambio de esquema, ver abajo)
- `vintage-telnet/requirements.txt`, `.gitignore`
- `vintage-telnet/ops/server.env.example`, `vintage-telnet/ops/vintage-telnet.service`, `vintage-telnet/ops/RASPBERRY_REPORT.md`

No se rescató `AGENTS.md`/`HANDOFF.md` de esa rama vieja (documentación de coordinación obsoleta) ni `vintage-telnet/ops/RASPBERRY_HANDOFF.md` (referenciaba una rama/commit ya inexistente).

### Archivos nuevos
- `vintage-telnet/server/world.py` — especies y salas (placeholder de geografía, marcado explícitamente)
- `vintage-telnet/server/dm_auth.py` — verificación del secreto del Dungeon Master (`VT_DM_PASSWORD`)
- `vintage-telnet/server/templates/dm.html` — panel del Dungeon Master
- `vintage-telnet/server/README.md` — documentación técnica del servidor
- `vintage-telnet/tests/test_gameplay.py` — 10 pruebas nuevas

### Archivos modificados
- `vintage-telnet/server/store.py` — esquema versión 2: columnas `status`/`species`/`room` en `players`, tabla `room_messages`; funciones nuevas (`set_status`, `set_species`, `move_player`, `players_in_room`, `add_message`, `recent_messages`, `list_by_status`)
- `vintage-telnet/server/app.py` — rutas nuevas: `/species`, `/move`, `/room/say`, `/api/room`, `/dm`, `/dm/login`, `/dm/logout`, `/dm/approve`, `/dm/reject`, `/dm/remove`
- `vintage-telnet/server/templates/entry.html` — estados nuevos: pendiente, rechazado/eliminado, elegir especie, vista de mundo con movimiento y chat
- `vintage-telnet/server/admin.py` — el comando `players` ahora incluye `status`/`species`/`room` (sigue sin exponer `password_hash`)
- `vintage-telnet/tests/test_entry.py` — 2 aserciones actualizadas: `schema_version` esperado pasa de 1 a 2; la prueba de "versión de esquema desconocida" ahora usa 3 en vez de 2 (porque 2 ya es una versión válida)
- `AGENTS.md` — reactivé mi firma como "Desarrollador de Servidor — Vintage Telnet", explícitamente subordinada a la autoridad arquitectónica del Arquitecto de Vintage Telnet y Raspberry Pi

### Cambios realizados
- **Cuentas y aprobación:** el registro ahora deja la cuenta en `status = pending` (antes cualquiera que se registraba ya podía jugar; ahora nadie juega sin aprobación). El Dungeon Master aprueba/rechaza desde `/dm`. Eliminar una cuenta aprobada la marca `removed` (no se borra el registro) y **revoca sus sesiones activas en la base de datos**, así que el efecto es inmediato aunque la persona no esté conectada en ese momento — no hace falta un socket en vivo para lograrlo, a diferencia de mi prototipo anterior en Node.js.
- **Especies y mundo:** al aprobar, la cuenta elige una de las 5 especies confirmadas y aparece en su pueblo de inicio confirmado (`CONFIRMED_IDEAS.md`). Movimiento N/S/E/O sobre un grafo de salas placeholder (Vaisgard + 5 pueblos), igual en espíritu al que ya había probado en Node.js pero reescrito en Python/SQLite.
- **Chat:** local por sala, visible para quien esté en la misma sala, con lista de "quién más está aquí".
- **Contrato explícito:** `GET /api/room` devuelve JSON estructurado (no texto libre) pensando en que `vintage-telnet.html` pueda consumirlo en el futuro, siguiendo el principio de `ARCHITECTURE_STATUS.md` de que el cliente no debe inferir estado autoritativo leyendo texto.
- Deliberadamente NO se implementó: combate, PvP, clases/estadísticas, reaparición de monstruos, chat global, recuperación de contraseña — sigue abierto en `GAMEPLAY.md` o es endurecimiento de seguridad para después.

### Pruebas realizadas
- Suite completa: **19/19 pruebas pasan** (`python -m unittest discover -s tests -v`), incluidas las 9 heredadas sin cambios de comportamiento y las 10 nuevas de aprobación/especies/movimiento/chat.
- Prueba manual end-to-end con el servidor real (Waitress, no el cliente de test de Flask) vía `curl`: registro → pendiente → login del DM → aprobar → elegir especie (Felaryn → Khariel) → moverse al oeste (→ Vaisgard) → chat local → eliminar desde el DM → `/api/me` devuelve 401 inmediatamente después.
- Verifiqué que un jugador removido no puede volver a entrar con las mismas credenciales (queda en `status = removed`).

### Qué es funcional
- Todo lo descrito arriba, corriendo de verdad (no es una demo): cuentas, aprobación, especies, mundo, movimiento, chat, persistencia en SQLite que sobrevive a reinicio del proceso.

### Qué sigue siendo pendiente
- Geografía y descripciones reales del mundo (reemplazar el placeholder de `world.py`) — corresponde al Historiador.
- Todo combate/clases/progresión — corresponde a Jugabilidad, junto con Javier.
- Conectar `vintage-telnet.html` (cliente móvil actual, sigue siendo demo local) contra esta API real — requiere que el Arquitecto de Vintage Telnet y Raspberry Pi defina el contrato cliente-servidor en detalle antes de tocar ese HTML.
- Despliegue real en Raspberry Pi — corresponde al agente de Raspberry Pi, siguiendo la secuencia de `ARCHITECTURE_STATUS.md` (esta rama ya pasó "fuera de Raspberry": sintaxis, unit tests, integración HTTP local; falta systemd real, puertos/firewall, backup/restauración probada en el equipo real).
- Recuperación de contraseña, verificación de correo, HTTPS si sale de la red local.

### NECESIDAD DE JUGABILIDAD
- Sin cambios: fórmulas de combate, esfuerzo para cambiar de clase, tiempos de reaparición de monstruos, mecanismo de habilidades limitadas, fórmula de huida, protección ante diferencias extremas de poder — todo sigue "abierto" en `GAMEPLAY.md`.

### Riesgos/conflictos
- Ninguno detectado contra `main`: esta rama nació de `origin/main` vigente (no de la rama vieja divergida de PR #1), así que no hereda su desactualización.
- `vintage-telnet.html` no se tocó; sigue siendo la demo local del Desarrollador Junior, sin relación funcional con este servidor todavía.

### Aviso para el Arquitecto de Vintage Telnet y Raspberry Pi
Esta entrega implementa dentro del stack y la secuencia que ya publicaste en `ARCHITECTURE_STATUS.md` (rescatar PR #1, HTTP primero, contrato estructurado). Si algo de lo que agregué (esquema de `players`, rutas de aprobación/mundo/chat) no encaja con una decisión tuya que yo no haya visto, avisame y lo ajusto — no pretendo sustituir tu autoridad arquitectónica, solo ejecuté la siguiente pieza dentro de lo ya decidido.

### Aviso para el Integrador/Publicador
No publicar hasta autorización expresa de Javier. Comparar esta rama contra el HEAD vigente de `main` antes de integrar (mi rama y `vintage-telnet.html` no tocan los mismos archivos, pero `main` puede haber avanzado desde que la creé).

**LISTO PARA REVISIÓN:** SÍ
**LISTO PARA PUBLICAR:** NO — falta revisión del Arquitecto de Vintage Telnet y del Integrador, y autorización de Javier ("sube").

---

## ENTREGA PARA CHATGPT (histórico — publicada)

**Estado:** PUBLICADA EN `main`

### Desarrollador
Desarrollador Junior de Vintage Telnet

### Estado base
Commit/HEAD de `main`:
`4f015d48a7cfbc7cdf0fbac0e1fd7afe70876270`

### Rama
`junior/vintage-telnet-mobile-v2`

### Objetivo
Aplicar la investigación `VT-RES-002` para optimizar la interfaz HTML de Vintage Telnet en celular y separar visualmente la carcasa HTML café de la terminal Telnet negra/verde.

### Archivos modificados
- `vintage-telnet.html`
- `HANDOFF.md`

### Investigación consumida
- `vintage-telnet/RESEARCH_MOBILE_TELNET_UI.md`

### Cambios realizados
- Terminal Telnet convertida en una zona visual inequívoca: negro casi puro, texto verde y tipografía monoespaciada.
- Carcasa HTML conservada en tonos café/ocre para distinguir herramientas web de la sesión Telnet.
- Layout móvil rehecho como shell de alto visible con terminal flexible y scroll interno.
- En teléfono, mapa/estado dejan de ocupar espacio permanente; mapa/personaje/inventario/ayuda se abren en dialogs.
- Controles principales compactados sin reducirlos por debajo de objetivos táctiles prácticos.
- Cruceta N/O/Mirar/E/S mantenida con relación espacial clara.
- Atacar y Huir permanecen visibles como acciones principales de demo.
- Entrada de comandos conserva 16 px, añade `enterkeyhint="send"` y permanece próxima a la terminal.
- Safe areas incorporadas para notch/home indicator.
- Se eliminó `scrollIntoView` del documento: ahora solo se desplaza el log interno de terminal.
- Añadido soporte `prefers-reduced-motion`.
- Responsive reorganizado: compacto <=640 px, intermedio hasta 959 px, lateral persistente desde 960 px.
- No se añadieron frameworks ni lógica paralela de botones.

### Qué es funcional
- Navegación local de demo por N/S/E/O.
- Mirar.
- Entrada escrita de comandos y alias n/s/e/o.
- Botones y comandos siguen entrando por la misma función `perform()`.
- Mapa/personaje/inventario/ayuda mediante dialogs.
- Scroll interno de terminal.
- Layout compacto para teléfono y dos columnas en escritorio.
- Indicadores locales de última acción y combate.

### Qué sigue siendo demostración
- Ubicación y conectividad de la microzona.
- Mapa mostrado.
- Estado de sesión.
- Combate.
- Inventario/personaje.
- Todo continúa sin Raspberry Pi ni persistencia real.

### NECESIDAD DEL SERVIDOR
- Sin cambios respecto a la entrega anterior: contrato de acciones, estado persistente, ubicación real, inventario, combate, descubrimiento y resincronización.

### NECESIDAD DE JUGABILIDAD
- Sin cambios respecto a la entrega anterior: objetivo de ataque, huida, vocabulario definitivo y datos exactos de combate/personaje/mapa.

### Pruebas realizadas
- Comprobación estructural de terminal negra/verde.
- Comprobación de media query móvil <=640 px.
- Comprobación de terminal con scroll interno.
- Comprobación de targets táctiles de 44–46 px o mayores.
- Comprobación de safe areas superior e inferior.
- Comprobación de dialogs para mapa/personaje/inventario/ayuda.
- Comprobación de `enterkeyhint="send"`.
- Comprobación de ruta única `perform()` para botón y comando.
- Comprobación de ausencia de `scrollIntoView`.
- Comprobación de `prefers-reduced-motion`.
- Confirmación de que no se añadió framework externo.

### Prueba visual que Javier/Matías deben hacer
1. Abrir en teléfono vertical.
2. Confirmar que se percibe inmediatamente la separación: café = cliente HTML; negro/verde = Telnet.
3. Revisar cuántas líneas de texto caben sin scroll de página.
4. Moverse con una mano usando N/S/E/O.
5. Probar Mirar, Atacar y Huir.
6. Escribir 5–10 comandos seguidos con el teclado abierto.
7. Abrir/cerrar mapa, personaje, inventario y ayuda.
8. Girar teléfono a horizontal y regresar.
9. Probar en iPad vertical/horizontal.
10. Decidir si los controles siguen ocupando demasiado o si la proporción ya se siente correcta.

### Riesgos/conflictos
- Validación visual final requiere teléfono/iPad real.
- La terminal usa scroll interno en móvil; Javier/Matías deben confirmar que esta interacción resulta natural.
- Si `main` cambia antes de integrar, el Integrador debe volver a comparar la rama.

### Aviso para el Integrador/Publicador
No publicar hasta autorización expresa de Javier. Comparar esta rama contra el HEAD vigente de `main` antes de integrar.

**LISTO PARA REVISIÓN:** SÍ  
**PUBLICADA EN `main`:** SÍ — autorización “Sube” recibida el 2026-09-21  
**MERGE COMMIT:** `c156fce377203534f7d9cb14632ef4f36815310c`


## INTEGRACIÓN DE ARTE HTML — Vintage Telnet

**Fecha:** 2026-09-21  
**Estado:** INTEGRADO EN `main`

### Origen de la entrega
- Rama: `art/vintage-telnet-html-assets`
- Commit de arte revisado: `886314bfd9be648938cc7668e2527a079050d231`
- Estado antes de integrar: rama 1 commit adelante de `main` y 0 atrás.

### Qué se integró
Biblioteca modular de arte para la carcasa HTML de Vintage Telnet en:
`vintage-telnet/assets/html-ui/`

Incluye:
- botones para Inventario, Mapa, Huir y Poderes;
- ornamento de esquina;
- divisor horizontal dorado;
- textura azul/pizarra repetible;
- preview móvil de referencia;
- `README.md` y `ASSET_MANIFEST.md` con instrucciones de uso, tamaños y alcance.

### Criterio de revisión aplicado
- Los PNG son assets modulares; no sustituyen controles HTML reales.
- La terminal Telnet negro/verde debe mantenerse separada de la carcasa visual exterior.
- El arte sigue una dirección más juvenil/mobile-first y menos recargada.
- El botón `Poderes` queda como categoría visual; no define mecánicas ni poderes concretos.
- No se modificó `vintage-telnet.html` durante esta integración.
- No se modificó Senku.

### Pendiente
La siguiente tarea separada será adaptar `vintage-telnet.html` para consumir estos assets sin romper la lógica existente ni la ruta única de acciones del cliente.

### Resultado
- Arte integrado a `main`: SÍ.
- HTML actualizado para usar el arte: NO, pendiente de una tarea posterior.
- Publicación/servidor Raspberry: sin cambios por esta integración.


## PREPARACIÓN DE BASE DE DATOS Y JUGABILIDAD REAL — Vintage Telnet

**Fecha:** 2026-09-21  
**Estado:** PREPARACIÓN DOCUMENTADA; SERVIDOR V2 NO INTEGRADO

### Trabajo realizado
- Revisada la rama `claude/vintage-telnet-server-v2`.
- Commit revisado: `ca7be621cc7862cf4cbb7a34eaea0a787820cf63`.
- La entrega reporta SQLite real, cuentas/sesiones, aprobación del Dungeon Master, especies, ubicación persistente, movimiento N/S/E/O, chat local y API estructurada.
- La rama está divergida respecto a `main`; no se integró automáticamente.
- Se creó `vintage-telnet/DATABASE_GAMEPLAY_PREP.md` con el primer vertical slice jugable real, requisitos mínimos de persistencia, contrato cliente-servidor necesario, seguridad, pruebas y secuencia recomendada.

### Primer hito jugable acordado para preparación
`Abrir → entrar → aprobar cuenta → elegir especie → aparecer en pueblo → moverse → ver otro jugador → hablar → cerrar → volver → conservar ubicación.`

### Importante
- No se implementó ni inventó combate.
- No se modificó `vintage-telnet.html`.
- No se desplegó nada a Raspberry Pi.
- No se integró la rama de servidor V2.
- La siguiente acción técnica corresponde a revisión/actualización del servidor V2 contra el `main` vigente y cierre del contrato cliente-servidor.


## PRIORIDAD P0 — PRIMER SLICE JUGABLE REAL

Javier fijó la prioridad del siguiente hito:

**ENTRAR → ELEGIR ESPECIE → MOVERSE POR EL PUEBLO**

Se creó `vintage-telnet/FIRST_PLAYABLE_SLICE.md` con el alcance completo, contrato mínimo requerido, persistencia, responsabilidades y prueba de aceptación.

Por decisión de alcance, quedan fuera de este primer slice: chat, combate, PvP, clases, estadísticas, inventario, Arcanes, poderes, economía, monstruos, secretos y mapa completo.

El objetivo es llegar antes a una versión realmente persistente y jugable en teléfono.
