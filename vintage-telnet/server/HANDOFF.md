# Handoff — Desarrollador de Servidor — Vintage Telnet


## Subentrega de #213 / DEATH-01 — Regresión del motor de muerte y respawn — 2026-09-26

- **DESARROLLADOR:** Antigravity (Desarrollo de pruebas — Vintage Telnet).
- **HEAD BASE REAL:** `e0ca3a824e8e040c5da8cb08ea6b83f3e9c7042a` (origin/main vigente tras #222 y #223).
- **RAMA:** `antigravity/vt-death-regression-01`
- **COMMIT:** rama `antigravity/vt-death-regression-01` (subentrega #213).
- **ARCHIVOS MODIFICADOS:**
  - `vintage-telnet/tests/test_death_regression.py` (nuevo archivo de pruebas)
  - `vintage-telnet/server/HANDOFF.md`
- **ALCANCE Y NATURALEZA:** Subentrega exclusiva de regresión del motor de muerte y respawn existente (DEATH_PLAYTEST.md §7). No implementa Cornalomo, ramales, narrativa ni contenido nuevo. No cierra por sí sola todo #213.

### Implementado y verificado

1. **Aislamiento frente a #207:** control explícito de `encounters._rng.random` (retorna 0.50 >= 0.10) para que la sala `valdren_sendero` no genere encuentros aleatorios espurios mientras el test transita hacia `valdren_camino_parcela`.
2. **Cobertura de los 8 puntos autorizados de DEATH-01:**
   - Llegar a 0 HP concluye el combate inmediatamente con desenlace `defeat` y mensaje visible.
   - Eliminación total del encuentro de la base de datos (sin dejar registros fantasma en la tabla `room_encounters` ni en `store.get_encounter`).
   - Respawn autoritativo en `valdren_centro` (`SAFE_ROOM_ID`).
   - Estado de respawn según GAMEPLAY/DEATH_PLAYTEST: 60% HP máximo, 40 fatiga, y herida degradada en un grado (e.g. de 'moderada' a 'leve').
   - Conservación íntegra de progresión: nivel, XP, PA sin gastar y PP sin gastar antes y después de la derrota.
   - Conservación íntegra de inventario y equipo: comparación exhaustiva de `items`, `equipped` (arma y armadura), `armor_reduction_total` y `carga_multiplier` antes y después de morir.
   - Persistencia completa tras recreación/reconexión de cliente: una nueva sesión recupera exactamente el estado de respawn, progresión e inventario/equipo completo.
   - APIs autoritativas (`/api/me`, `/api/character`, `/api/room`) reflejan la sala segura sin combate activo (`in_combat = False`) y sin criaturas presentes.
3. **Flujos alternativos de derrota cubiertos:**
   - Derrota durante huida fallida (DEATH_PLAYTEST §7.B).
   - Derrota durante defensa activa (esquivar, DEATH_PLAYTEST §7.C).
   - Capacidad de reanudar exploración saliendo de la sala segura hacia `valdren_sendero` (DEATH_PLAYTEST §7.E).

### Pruebas ejecutadas

- **Prueba específica:** `python -m unittest vintage-telnet/tests/test_death_regression.py`
  - Ejecutada 4 veces consecutivas para verificar determinismo y ausencia de aleatoriedad.
  - Resultado: 4 tests OK en cada ejecución (~3.8s a 4.1s).
- **Suite completa en Windows:**
  - Comando: `python -m unittest discover -s vintage-telnet/tests -p "test_*.py"`
  - Resultado: 307 tests ejecutados, 0 fallos, 3 errores conocidos de baseline en entorno Windows.
  - No se declara la suite completa verde debido a las limitaciones del entorno Windows:
    1. `test_vt_deploy.py`: `ModuleNotFoundError: No module named 'fcntl'`. Requiere módulos POSIX (`fcntl`, `pwd`) exclusivos de Linux/Raspberry Pi.
    2. `test_cinco_rutas.py`: `PermissionError: [WinError 32]` en `tearDown` al intentar eliminar el archivo temporal de SQLite mientras Windows retiene el handle.
    3. `test_class_choice.py`: `PermissionError: [WinError 32]` idéntico en `tearDown` por lock de SQLite en Windows.
- **PENDIENTE EXPLÍCITO:** Validación completa de la suite en Raspberry Pi / Linux por Codex.

## Entrega de Issue #213 — Cornalomo como amenaza superior regional y prueba de muerte/respawn DEATH-01 — 2026-09-27

- **DESARROLLADOR:** Antigravity (Desarrollo principal para implementaciones pesadas).
- **HEAD BASE:** `4d8b36c8be4baaa78996b7f3fa5950e32f50dfa8` (`origin/main` tras merge de PR #228).
- **TAREA:** Issue #213 — Implementar Cornalomo como amenaza superior regional opcional y validar de extremo a extremo el flujo completo de combate real y muerte/reaparición segura conforme a `DEATH_PLAYTEST.md`.
- **RAMA:** `antigravity/vt-213-cornalomo-death` (rama limpia creada desde `origin/main`).
- **ARCHIVOS MODIFICADOS / CREADOS:**
  - `vintage-telnet/server/creatures.py`:
    - Incorpora el perfil v1 aprobado de Cornalomo (`name="Cornalomo"`, `family="cornalomo"`, `reference_level=8`, `hp=120`, `precision=65`, `damage=20`, `armor_reduction=0.20`, `flee_agilidad=8`, `flee_percepcion=9`, `behavior_text`).
    - Conserva `CREATURE_ART` sin entrada para `cornalomo` (marco de combate neutral/vacío conforme a las reglas).
  - `vintage-telnet/server/app.py`:
    - Aplica la reducción de armadura de la criatura (`combat.apply_armor_reduction(player_damage, creature.get("armor_reduction", 0.0))`) al impactar en combate, reduciendo el daño recibido por Cornalomo en un 20%.
  - `vintage-telnet/server/world.py`:
    - Añade la sala `valdren_pastos_altos` ("Pastos altos") como ramal opcional accesible al este desde `valdren_cruce_cercas`, fuera del recorrido obligatorio a Vaisgard.
    - Señales de peligro y descripciones canónicas (`CREATURES.md` / `NARRATIVE.md`) reflejadas fielmente en la sala y sus objetivos de `examinar` (`cerca`, `cercas`, `huellas`, `huella`, `arboles`, `arbol`, `pasto`).
    - Conecta el encuentro fijo autoritativo: `ROOM_ENCOUNTER["valdren_pastos_altos"] = "cornalomo"`.
    - Asigna contexto visual `zone.edran.valdren_outskirts`.
  - `vintage-telnet/tests/test_pilot_lindero_roto.py`:
    - Actualiza el test placeholder `test_cornalomo_has_no_playable_stats_yet` a `test_cornalomo_has_approved_playable_stats`, verificando que el perfil aprobado por Jugabilidad está activo.
  - `vintage-telnet/tests/test_cornalomo_death.py`:
    - Nueva suite integral con 11 tests automatizados que cubren de punta a punta: perfil, ramal opcional, señales previas, evaluación "Abrumador" ("te supera claramente"), reducción física de armadura, derrota atacando, derrota huyendo, derrota defendiendo, respawn seguro en `valdren_centro` (60% HP, 40 fatiga, degradación de herida, 0 pérdida de arma/equipo/XP/inventario), reconexión en nueva sesión, huida normal permitida, exploración continua tras respawn y ausencia de regresiones.
  - `vintage-telnet/server/HANDOFF.md`: este registro.
- **ESTADO:** LISTO PARA REVISIÓN / PR NUEVA Y AUTOCONTENIDA.
- **MERGE:** NO.
- **DEPLOY:** NO.

### Verificación y pruebas automatizadas

Ejecutado con Python 3.12 y `PYTHONPATH=vintage-telnet`:
- `tests.test_cornalomo_death`: **11 tests pasando verde (17.6 s)**.
- `tests.test_random_encounters`: **16 tests pasando verde**.
- `tests.test_pilot_lindero_roto`: **48 tests pasando verde**.
- `tests.test_valdren_route_expansion`: **13 tests pasando verde**.
- `tests.test_navigation`: **4 tests pasando verde**.
- `tests.test_entry`: **36 tests pasando verde**.
- `tests.test_public_onboarding`: **11 tests pasando verde**.
- Lote combinado de 139 tests: **139 tests pasando verde (78.6 s)**.
- Regresión del mundo y mapa 2D sin colisiones de coordenadas.
- Exclusión total de Cornalomo de los pools aleatorios ordinarios (`edran_01_*`).

### Cumplimiento estricto de restricciones

1. Cornalomo NO es un jefe; es amenaza superior regional.
2. Derrota NO provoca pérdida de arma: arma, armadura e inventario 100% intactos.
3. No se crearon comandos de muerte ficticios ni trampas; combate autoritativo real.
4. Señales previas tomadas directamente del canon (`CREATURES.md`).
5. Evaluación cualitativa devuelve exactamente "te supera claramente" ("abrumador").
6. El jugador puede retroceder antes de combatir si no desea pelear (la criatura no ataca primero).
7. Huida con fórmula general permitida.
8. Reaparición segura en `valdren_centro` con 60% HP, 40 fatiga y herida degradada 1 grado.
9. No queda combate ni encuentro fantasma en SQLite ni en memoria.
10. No se modificó el esquema de base de datos ni #216 (capacidades de clase).

---

## Entrega limpia de Issues #209 y #211 — Portada pública y lectores canónicos — 2026-09-26

- **DESARROLLADOR:** Antigravity (Relevo de desarrollo).
- **HEAD BASE:** `e0ca3a83e2ae2d1cf002bce64f956b92607ca64a` (`origin/main` remoto vigente).
- **TAREA:** Issues #209 y #211 — Implementación de la portada pública de Vintage Telnet con 3 accesos claros:
  1. *Conocer el Mundo* (contenido canónico de #211).
  2. *Guía del aventurero* (contenido de `ENTRY_ADVENTURER_GUIDE.md`).
  3. *Entrar / Crear cuenta* (acceso directo a formularios de autenticación).
- **RAMA:** `antigravity/vt-209-211-clean` (rama limpia creada desde `origin/main`; descarta totalmente la PR #219 de Jules y no reutiliza ramas divergentes).
- **ARCHIVOS MODIFICADOS / CREADOS:**
  - `vintage-telnet/KNOW_THE_WORLD_MENU.md`: rescatado intacto de `origin/historia/vt-conocer-el-mundo` (#211).
  - `vintage-telnet/HANDOFF_KNOW_THE_WORLD_UI.md`: rescatado intacto de #211.
  - `vintage-telnet/server/content_parser.py`: nuevo parser modular que estructura ambos documentos, aísla metadatos internos e inserta las imágenes canónicas aprobadas en sus marcadores sin requerir dependencias externas (sin `markdown==3.11`).
  - `vintage-telnet/server/app.py`: agrega rutas públicas de solo lectura `/mundo` y `/guia`, e integra parámetro `view` en `/` para acceso directo sin scroll.
  - `vintage-telnet/server/templates/_onboarding_guest.html`: reorganiza la pantalla de bienvenida con los 3 accesos claros de forma compacta y accesible.
  - `vintage-telnet/server/templates/entry.html`: estilos CSS y responsividad móvil para las opciones del portal público.
  - `vintage-telnet/server/templates/world.html`: plantilla dedicada de lectura con índice, navegación por 5 capítulos, opción "Leer todo", imágenes canónicas aprobadas y mejora progresiva para cambio instantáneo de pestañas con o sin JavaScript.
  - `vintage-telnet/server/templates/guide.html`: plantilla dedicada para la Guía del Aventurero con las 15 secciones aprobadas, índice jump navigation y enlaces de retorno.
  - `vintage-telnet/tests/test_public_onboarding.py`: suite exhaustiva de 11 tests automatizados que cubren accesos, navegación, ausencia de metadatos/notas internas y seguridad.
  - `vintage-telnet/server/HANDOFF.md`: este registro.
- **ESTADO:** LISTO PARA REVISIÓN / SUPERA Y REEMPLAZA A PR #219.

### Verificación y pruebas automatizadas

Ejecutado en Windows con Python 3.12:
- `tests.test_public_onboarding`: **11 tests pasando verde (1.696 s)**.
  - Portada con los 3 accesos visibles.
  - Acceso directo a `view=login` y `view=register`.
  - `/mundo`: público, de solo lectura, sin alterar base de datos.
  - `/mundo`: navegación por capítulos (1..5) e índice "Leer todo".
  - `/mundo`: cero fugas de notas internas (`Clasificación`, `Responsable`, `NOTA DE DISEÑO`, `Reglas de implementación`, etc.).
  - `/mundo`: imágenes canónicas insertadas en marcadores aprobados; marcador 3 omitido limpiamente sin placeholders.
  - `/guia`: público, de solo lectura, con las 15 secciones aprobadas e índice jump navigation.
  - `/guia`: cero fugas de notas editoriales (`Tipo:`, `Autoridad:`, `Regla editorial:`, `APROBADO POR JAVIER`).
  - Flujo de registro y login existente 100% preservado.
  - Cabeceras de seguridad y nonces CSP presentes y válidos.
- `tests.test_entry`: **36 tests pasando verde (10.579 s)**.
- `tests.test_http` y `tests.test_dm_private`: **5 tests pasando verde (3.675 s)**.

### Relación con #211 y PR #219

- Cumple la cadena solicitada: consume el paquete canónico de #211 y lo integra a la interfaz de usuario (#209).
- Reemplaza y deja obsoleta a la PR #219 de Jules, la cual modificó indebidamente archivos ajenos (`GAMEPLAY.md`, `DEATH_PLAYTEST.md`, `SHARED_RESEARCH.md`), agregó una dependencia innecesaria a `requirements.txt` y no implementó la interfaz requerida.
- No modifica `GAMEPLAY.md`, `DEATH_PLAYTEST.md`, `requirements.txt` ni archivos de Senku u Ojo de Agua.
- No realiza merge ni despliegue directo a `main`.

---


## Relevo de #207 — EDRAN-01 — 2026-09-26

- **DESARROLLADOR:** Codex.
- **HEAD BASE:** `271a92eba6f0e3b554328d57ed1c66a61a7624f0` (main remoto comprobado antes de trabajar).
- **RAMA:** `codex/vt-207-edran-pools`, creada desde ese main; no reutiliza ramas anteriores.
- **COMMIT de implementación:** `424caa8be4d77716d360913627b704257065d08f`.
- **ARCHIVOS MODIFICADOS:** `vintage-telnet/server/encounters.py`,
  `vintage-telnet/tests/test_random_encounters.py` y este HANDOFF.
- **Estado actual:** EN RELEVO / VALIDACIÓN COMPLETA PENDIENTE. Javier pide continuar
  desde Codex en Raspberry; esta sesión deja de implementar para evitar trabajo simultáneo.
- **Estado final requerido:** `LISTO PARA REVISIÓN`, solo tras resolver pendientes y
  obtener suite completa verde. No declarar ese criterio cumplido todavía.

### Implementado y verificado

Únicamente tres pools EDRAN-01: sendero 10% / 85:15; camino hundido y parcelas
exteriores 20% / 75:25; campo rastrojo y campos sin cerca 30% / 65:35.
Los pesos corresponden a Mordelinde y Espinajo de rastrojo, respectivamente.
Todas las demás salas y Cornalomo quedan fuera. No cambia ninguna función del motor.

Leídos AGENTS.md, Issue #207 completo, GAMEPLAY §33, RANDOM_ENCOUNTER_GAMEPLAY.md,
motor y tests. Comprobadas ramas remotas y búsqueda de PRs de #207: no se encontró
otra implementación activa. La rama histórica `claude/vt-random-encounters`
corresponde al motor anterior, no se reutilizó.

**TESTS ejecutados:** Windows, Python 3.12.14, desde `vintage-telnet/`:

```text
.venv/Scripts/python.exe -m unittest discover -s tests -p test_random_encounters.py -v
16 tests: OK
git diff --check
OK
```

Cubren configuración válida, allowlist exacta de cinco salas, chances y pesos
exactos, exclusión de todas las otras salas y Cornalomo, prioridad scripted sin
consumir RNG, distribución reproducible con semilla 207 e integración de movimiento
con la configuración real. La prueba de pools vacíos ahora los inyecta explícitamente.

**Suite completa:** `python -m unittest discover -s tests -v`, ejecutada en Windows
antes del último ajuste de tests: **306 tests, 1 fallo y 3 errores, 193.463 s**.
No está verde. Repetir sobre el commit entregado en Linux. Se observaron errores en
`test_players_left_on_removed_roads_are_sent_home` y
`test_existing_v8_character_keeps_progress_and_chooses_class_on_return`, y fallo en
`test_resting_outside_combat_heals_and_reduces_fatigue`. No atribuir automáticamente
todos los fallos a Windows o a #207: comparar con HEAD BASE en un checkout separado.
Los dos primeros errores son `PermissionError: [WinError 32]` en `tearDown`, al
borrar SQLite temporal aún abierto. El tercer error es la importación de
`test_vt_deploy`: `ModuleNotFoundError: No module named 'fcntl'`.
Ese módulo también importa `pwd`, exclusivo de Unix; este PC no tiene WSL.
El fallo de descanso es `AssertionError: 'Descansas un momento' not found`.

### Continuación por Codex en Raspberry (autorizada por Javier)

La Raspberry se usa aquí como **entorno aislado de desarrollo y pruebas**. No es
un despliegue. No usar Ojo de Agua ni modificar el checkout que ejecute producción.

1. Leer este bloque, AGENTS.md e Issue #207. Comprobar remoto y HEAD de esta rama.
   Esta rama es ahora el relevo autorizado; no comenzar otra implementación de #207.
2. Crear un checkout/worktree separado bajo el home del usuario, fuera de `/opt`,
   `/etc` y `/var`, y un virtualenv nuevo. No usar ni copiar la base de datos real,
   secretos o configuración del servicio. Los tests deben usar sus datos temporales.
3. Desde `vintage-telnet/`, instalar `requirements.txt` en ese virtualenv y ejecutar:

   ```sh
   python -m unittest discover -s tests -p test_random_encounters.py -v
   python -m unittest discover -s tests -v
   ```

4. Revisar la prueba antigua de descanso: entra a `valdren_sendero` suponiendo que
   está vacío. Ahora hay 10% de encuentro. Inyectar RNG de fallo de tirada en esa
   prueba para garantizar su precondición; no cambiar descanso, combate ni pools
   para hacerla pasar. Revisar otros supuestos similares solo si producen fallos.
5. Comparar los demás errores con HEAD BASE. Si son ajenos a #207, documentarlos
   para Arquitectura sin reparar lógica ajena ni inventar contratos. Si el contrato
   de #207 contradice el código, detener implementación y documentar el conflicto.
6. Continuar mediante commits/push en esta misma rama y actualizar su PR; no crear
   una PR duplicada. Devolver SHA probado, Python/SO, comandos, conteos, resultado
   y tracebacks relevantes sin secretos. Actualizar este HANDOFF con el estado real.

**Fronteras:** no cambiar combate, daño, XP, narrativa, canon, UI, SQLite, criaturas,
economía, probabilidades generales del motor ni Senku. No comenzar #216 ni #213.
No ejecutar `vt-deploy`, `systemctl`, migraciones sobre datos vivos, merge, reinicios
o instalaciones del sistema. Si falta un paquete del sistema, reportar la necesidad.

**Incompatibilidades:** no detectada incompatibilidad entre contrato #207 y la
configuración/motor. Hay precondiciones antiguas de tests por revisar y limitación
de entorno Windows. **Confirmación de alcance:** solo #207 y documentación de relevo;
sin merge, deploy ni pruebas físicas en Raspberry realizadas por esta sesión.

### Validación final en Raspberry — Codex — 2026-09-26

- **Estado:** LISTO PARA REVISIÓN.
- **Entorno aislado:** `/home/jdiaz/MatiasGameLab-vt207`, virtualenv
  `.venv-vt207`, Python 3.13.5; solo datos temporales de tests.
- Se controló `server.encounters._rng` en dos pruebas históricas que requieren
  `valdren_sendero` vacío: descanso de campo y retorno tras huir. No se cambió
  lógica de descanso, huida, combate ni configuración EDRAN-01.
- Los errores Windows de SQLite y `fcntl` no se reproducen en Linux. En HEAD BASE,
  la prueba de rutas eliminadas y `test_vt_deploy` también pasan; son limitaciones
  del entorno Windows, ajenas a #207. La migración v8 pasa en la suite Linux.
- Validación final desde `vintage-telnet/`:

  ```text
  ../.venv-vt207/bin/python -m unittest discover -s tests -p test_random_encounters.py -v
  16 tests, OK
  ../.venv-vt207/bin/python -m unittest tests.test_pilot_lindero_roto.PilotIntegrationTests.test_resting_outside_combat_heals_and_reduces_fatigue tests.test_pilot_lindero_roto.PilotIntegrationTests.test_fleeing_successfully_returns_toward_valdren_and_clears_encounter -v
  2 tests, OK
  ../.venv-vt207/bin/python -m unittest discover -s tests -v
  309 tests, OK (68.718 s)
  ../.venv-vt207/bin/python -m pip check
  No broken requirements found.
  git diff --check
  OK
  ```
- Sin producción, servicios, secretos, bases reales, deploy, merge ni reinicios.
- **Pendientes:** revisión e integración por el flujo normal; no hay pendiente
  técnico de #207. No se inició #216 ni #213.

---

## Entrega histórica — Issue #57 (conservada)

**Desarrollador:** Claude — Desarrollador de Servidor — Vintage Telnet.
**Estado:** entrega nueva, lista para revisión de Arquitectura/Jugabilidad.
**Tarea asignada:** Issue #57 — VT-GAME/DEV: implementar inventario y
equipamiento mínimo v1 (GAMEPLAY.md §32).
**Rama:** `claude/vintage-telnet-server-issue-57`.
**HEAD base de esta entrega:** `1a92420` (`origin/main`, "Reaudit reading
pilot and NPC conversation design").

## Contexto de esta ronda

Una ejecución automática anterior (revisión periódica VT-AUTO, Issue #47)
dejó un comentario "TOMADO" en la Issue #57 con este mismo HEAD base y esta
misma rama, pero nunca llegó a hacer push de código (probablemente cortada
por límite de uso justo después de publicar el comentario: la rama nunca
existió en `origin`). Esta entrega retoma la tarea desde cero contra el
`main` vigente, tal como indica el criterio de la Issue #47 para ese caso.

## Objetivo

Implementar exactamente GAMEPLAY.md §32 (Inventario y equipamiento mínimo
v1) y los 8 casos de aceptación de la Issue #57, conectando el catálogo ya
validado de `WEAPON_CATALOG.md`/`ARMOR_CATALOG.md` a la matemática de
combate real de §30 (armor_reduction, MultiplicadorCarga) y a `_can_block`
(Bloquear/desviar), que el Issue #73 dejó explícitamente pendiente de este
trabajo.

## Cambios

### Nuevo: `server/items.py`
Catálogo puro (sin Flask/DB) de las 6 armas y 8 armaduras ya validadas por
Historiador/Jugabilidad en `../WEAPON_CATALOG.md`/`../ARMOR_CATALOG.md`:
`base_damage`/`can_block` por arma, `armor_reduction` por armadura,
`forge_required` en ambos. No inventa objetos ni cifras nuevas.
`find_key_by_name` resuelve `"equipar <objeto>"` ignorando mayúsculas y
tildes. No existe todavía ningún objeto de bloqueo puro (escudo) en el
catálogo del Historiador — Bloquear en v1 depende de si el **arma**
equipada lo permite (columna "Bloquear/desviar" del catálogo), no de una
ranura de objeto de bloqueo separada; no se inventó esa ranura sin un
objeto real que la necesite.

### `server/store.py`
- Esquema v6: tabla `inventory_items` (una fila por instancia de objeto,
  §32.5 "identidad de objeto/instancia suficiente para impedir duplicación
  accidental") y columnas `equipped_weapon_id`/`equipped_armor_id` en
  `players`. Migración solo agrega tabla/columnas; no toca datos
  existentes de jugadores.
- `CHARACTER_COLUMNS` ahora incluye ambas columnas de equipo, así que
  `g.player`/`player_for_token` siempre traen el estado de equipo sin
  consulta aparte (mismo patrón que nivel/HP/fatiga/herida).
- `grant_item`: entrega autoritativa (§32.5) — recompensa, encargo válido,
  Forja o acción administrativa. Nunca compra directa del jugador en v1.
- `list_inventory`, `equipped_item_keys`, `character_by_player_id`: lecturas.
- `equip_item`: atómico de verdad vía `BEGIN IMMEDIATE` (mismo patrón que
  `set_species`/`allow_attempt`) — valida posesión y, si el catálogo lo
  exige, validación de Forja completa (§32.4) antes de reemplazar el
  objeto activo de esa categoría (§32.3, nunca destruye el reemplazado).
- `unequip_item`: sin coste, devuelve a poseído/no activo.

### `server/combat.py`
- `fatigue_gained` acepta ahora `armor_reduction` (por defecto `0.0`, así
  que el comportamiento previo sin armadura no cambia) y aplica
  `armor_load_multiplier` (§30.3: `MultiplicadorCarga = 1 + reducción`).
- Nuevas funciones puras `armor_load_multiplier` y `apply_armor_reduction`
  (§30.1/30.5: la armadura reduce el daño que ya conectó, después de
  cualquier defensa activa; las reducciones no se suman entre sí).

### `server/app.py`
- `_can_block(path, player_id)` deja de devolver `False` siempre: ahora
  consulta el arma equipada real y su flag `can_block` del catálogo. Sigue
  siendo la única función que hay que tocar para cambiar esa regla (tal
  como dejó documentado el Issue #73), y sigue siendo parcheable en los
  tests existentes (`@patch("server.app._can_block", ...)`) sin cambios.
- Nuevo helper `_equipment(player)`: resuelve arma/armadura equipadas a sus
  valores de catálogo (`weapon_base_damage` con fallback a
  `combat.BASE_ARMA` si no hay arma, `can_block`, `armor_reduction`).
- `attempt_attack`/`attempt_evaluate` usan el `base_damage` del arma real
  del jugador en vez del `BASE_ARMA` fijo (tanto para el golpe como para el
  DPS esperado usado en `evaluar`/categoría de XP).
- `attempt_attack`/`attempt_flee`/`attempt_dodge`/`attempt_resist`/
  `attempt_block`: el daño que el jugador recibe ahora pasa por
  `combat.apply_armor_reduction` con la reducción de su armadura equipada
  (§30.5: se aplica después de Bloquear/Resistir, nunca sumado a esas
  reducciones); el coste de fatiga de esas cinco acciones físicas ahora
  incluye el `MultiplicadorCarga` de esa misma armadura.
- Nuevos intents `equipar <objeto>`/`desequipar <objeto>` (§32.8),
  conectados a `/command` y `/api/intent` exactamente igual que el resto de
  intenciones (mismo patrón botón=comando ya establecido, aunque esta
  entrega no agrega botones — ver Pendiente). Nuevas funciones
  `attempt_equip`/`attempt_unequip`: rechazan la acción con un mensaje
  honesto si hay combate activo, si el objeto no existe en el catálogo, si
  no se posee, o si le falta validación de Forja.
- Nuevo `GET /api/inventory`: estado estructurado (objetos poseídos, cuál
  está activo, `armor_reduction_total`, `carga_multiplier`,
  `forge_validated`) para el futuro panel Inventario/Equipo — el servidor
  entrega el cálculo ya resuelto, el cliente no calcula nada autoritativo.

### `server/admin.py`
Nuevo subcomando `grant-item <username> <item_key> [--forge-validated]`:
la vía de "acción administrativa legítima" de §32.5 para que un
operador entregue un objeto en un despliegue real (CLI local, igual que
`players`/`backup`/`check` — nunca expuesto por HTTP a jugadores).

### `tests/test_inventory.py` (nuevo)
32 pruebas: catálogo puro, fórmulas de armadura, y los 8 casos de
aceptación de la Issue #57 (entrega → aparece en inventario → equipar
fuera de combate → cambia `armor_reduction`/fatiga → rechazado en combate →
desequipar vuelve a base → persiste tras logout/login → Forja no validada
rechazada), más reemplazo atómico de arma sin destruir la anterior,
supervivencia del equipo tras derrota/reaparición (§32.7), `bloquear`
habilitado/deshabilitado según el arma real equipada, y el CLI de
`admin.py`.

### `tests/test_entry.py`
Dos ajustes obligados por el nuevo esquema v6 (no relacionados con
comportamiento nuevo): `schema_version` esperado en `/healthz` (5 → 6) y la
versión "desconocida" usada para probar el fallo cerrado (6 → 7, porque 6
ya es una versión soportada).

## Pruebas

```
cd vintage-telnet && .venv/bin/python -m unittest discover -s tests -v
```

**144/144 OK** (112 previas + 32 nuevas de `test_inventory.py`).

## Trabajo previo afectado

Ninguna entrega concurrente tocaba `server/`, `tests/` ni `admin.py` en el
HEAD base (`git ls-remote` no mostró ninguna rama `claude/vintage-telnet-
server-*` con este trabajo ya en curso). El Issue #73 (`_can_block`,
`available_actions`) ya estaba integrado en `main` y se dejó explícitamente
listo para que esta entrega lo conectara — no se reimplementó nada suyo.

## Pendiente / NECESIDAD para otros especialistas

- **NECESIDAD DE FRONTEND (Junior/Integrador VT):** esta entrega
  deliberadamente no toca `templates/entry.html`. El servidor ya expone
  `GET /api/inventory` y los intents `equipar`/`desequipar` vía
  `/api/intent`; falta el panel Inventario/Equipo y los botones
  equivalentes que pide GAMEPLAY.md §32.8 (opcional, el texto ya funciona).
- **NECESIDAD DE CONTENIDO:** no existe todavía ningún flujo de juego real
  que llame a `store.grant_item` (recompensa de contenido, entrega de
  Forja). Hasta que exista, la única vía de adquisición es el CLI
  `admin.py grant-item` — suficiente para probar en Raspberry, no para que
  un jugador consiga equipo por su cuenta.
- **NECESIDAD DEL HISTORIADOR (opcional):** si en algún momento se quiere
  un objeto de bloqueo puro (escudo) independiente del arma, hace falta
  definirlo en el catálogo antes de crear esa ranura — no se inventó aquí.
- Regla de pérdida de arma al morir (§11, "excepción independiente que
  todavía requiere su flujo concreto") sigue sin implementarse — GAMEPLAY
  ya lo señala como pendiente aparte, no de esta Issue.

## Riesgos

- Cambio de fórmula: `fatigue_gained` ahora multiplica por
  `MultiplicadorCarga` (§30.3). Con `armor_reduction=0.0` (sin armadura
  equipada, el caso de todo personaje existente) el resultado es
  matemáticamente idéntico al de antes — verificado por la suite completa
  verde, incluida toda la cobertura previa de fatiga en
  `test_pilot_lindero_roto.py`/`test_combat_actions.py` sin modificar esos
  archivos.
- `_can_block` cambió de firma (`_can_block()` → `_can_block(path,
  player_id)`); los tests existentes que la parchean con
  `@patch("server.app._can_block", return_value=True)` siguen funcionando
  sin cambios porque `unittest.mock.patch` reemplaza la función completa,
  ignorando su firma real.

**LISTO PARA PUBLICAR:** SÍ, en cuanto Arquitectura/Jugabilidad revisen la
rama contra el criterio de aceptación de la Issue #57. No se hizo push a
`main`; corresponde al Chat Integrador tras autorización de Javier.
