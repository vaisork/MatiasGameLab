# HANDOFF — Entrega técnica

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
