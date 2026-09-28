# Handoff — Desarrollador de Servidor — Vintage Telnet

## Integración lista para revisión: arte de Cornalomo en combate (#365) — 2026-09-28

- **RESPONSABLE:** Codex — Integrador.
- **HEAD BASE:** `daaa728eddde629cb0c694a4c00b40c8bc438cb9` (incluye el asset aprobado integrado por PR #188).
- **RAMA:** `codex/vt-365-cornalomo-art`.
- **CAMBIO:** `server/creatures.py` conecta `cornalomo` con `/assets/creatures/cornalomo.webp`; la prueba de `test_cornalomo_death.py` ahora comprueba el catálogo, el HTML de combate y la respuesta HTTP `image/webp`.
- **AUDITORÍA:** Cornalomo era el único asset de criatura publicado en `main` que carecía de entrada en `CREATURE_ART`. Los demás assets de criatura publicados ya estaban registrados; las entregas que aún están en PR abiertas no se cuentan como assets integrados.
- **PR #188:** fusionada como `daaa728`; SHA-256 runtime comprobado contra #180: `476a3304e5b2da49fe50fd21cc2e772cfa7c6b10f6cc77bcfe9dcc1f5ff428ee`. El workflow de publicación pasó después de actualizar su base.
- **PRUEBAS:** `python -m unittest tests.test_cornalomo_death tests.test_published_art tests.test_entry -v` — **53/53 PASS**. `git diff --check` — **PASS**.
- **PENDIENTES:** revisión e integración de esta corrección. **MERGE: NO / DEPLOY: NO.**

## Entrega lista para revisión: HOME-CORE — hogar personal persistente mínimo (#280) — 2026-09-27

- **DESARROLLADOR:** Antigravity (Desarrollador principal para implementaciones pesadas).
- **HEAD BASE:** `39349d0` (`origin/main` remoto vigente tras rebase limpio).
- **TAREA:** Issue #280 — `VT-SERVER: HOME-CORE — hogar personal persistente mínimo` (HOME-01 / GAMEPLAY §34).
- **RAMA:** `antigravity/vt-280-home-core`
- **CONTRATO APROBADO Y ALCANCE (GAMEPLAY §34 / HOME-01):**
  - **Un hogar por personaje dinámico:** Cada personaje aprobado y con onboarding completo dispone de su propio espacio `home:<player_id>` aislado, sin miles de filas estáticas en `world.py`.
  - **Primera entrada jugable en su hogar:** Todo personaje nuevo que completa especie y clase inicia en su hogar personal (`Tu hogar`), no directamente en el centro del pueblo.
  - **Salida hacia comunidad según especie:** Una única salida funcional (`sur` o comando `salir` / `salida` / `out` / `leave`) conduce hacia el asentamiento inicial de su especie (Humano → Valdren, Felaryn → Khariel, Dravak → Brumak, Marevyn → Narevia, Vesperi → Velmora).
  - **Sin alteración del mapa regional:** No crea rutas ficticias en `traversed_routes` entre el hogar y el mundo exterior ni altera el mapa regional.
  - **Seguridad total:** 0 encuentros aleatorios, 0 encuentros fijos ordinarios y 0 PvP en el hogar. Descanso normal permitido; sin curación mágica instantánea.
  - **Persistencia honesta:** Desconectar dentro del hogar recupera la posición en el hogar; salir al pueblo y desconectar conserva la posición en el pueblo (el hogar no "atrae" magnéticamente al personaje).
  - **Preservación de jugadores existentes:** Personajes existentes con posición válida en el mundo no son reubicados. La verificación de inicio (`relocate_players_outside_world`) protege explícitamente a los personajes ubicados en sus hogares legítimos.
  - **Cero almacenamiento / economía doméstica:** No se crearon cofres, bancos, muebles, stash ni economía doméstica en esta fase.
  - **Cero pantalla nueva:** Renderizado directo en las vistas existentes con nombre `Tu hogar`, descripción neutra autorizada y controles ordinarios.
- **ARCHIVOS MODIFICADOS / CREADOS:**
  - `vintage-telnet/server/world.py`: constantes canónicas de hogar, resolver hook de especie, `get_home_room_id`, `is_home_room`, `parse_home_player_id`, construcción dinámica de sala en `get_room`.
  - `vintage-telnet/server/store.py`: `get_player_species`, salvaguarda de salas de hogar en `relocate_players_outside_world`.
  - `vintage-telnet/server/app.py`: registro de resolver de especie en inicio, asignación de sala hogar en `attempt_choose_species`, resolución del pueblo en `/api/species`, exclusión de rutas regionales al salir/entrar de casa en `attempt_move`, soporte de comandos literales (`salir`/`salida`/`out`/`leave`) mapeados a `world.HOME_EXIT_DIRECTION`.
  - `vintage-telnet/tests/test_home_core.py` (nuevo): 12 tests exhaustivos verificando cada caso de aceptación del Issue #280 y la regresión de aislamiento de rutas regional (incorporada desde PR apilada #351 de Junior 1).
  - Suites adaptadas para salir del hogar al centro de comunidad: `tests/test_cinco_rutas.py`, `tests/test_class_choice.py`, `tests/test_combat_actions.py`, `tests/test_cornalomo_death.py`, `tests/test_death_regression.py`, `tests/test_entry.py`, `tests/test_gameplay.py`, `tests/test_inventory.py`, `tests/test_navigation.py`, `tests/test_npc_actions.py`, `tests/test_npc_dialogue.py`, `tests/test_npc_memory.py`, `tests/test_pilot_lindero_roto.py`, `tests/test_progression.py`, `tests/test_published_art.py`, `tests/test_random_encounters.py`, `tests/test_screen_stability.py`, `tests/test_unapiedra.py`.
  - `vintage-telnet/server/HANDOFF.md`: este registro.

### Pruebas ejecutadas y verificación

1. `tests/test_home_core.py`: **12/12 tests PASS**.
   - Dos personajes de la misma cuenta obtienen hogares distintos (`home:<id1>` != `home:<id2>`).
   - Dos cuentas no comparten hogar ni mensajes privados.
   - Personaje nuevo inicia en su hogar tras completar onboarding (nombre `Tu hogar`, descripción y controles limpios).
   - Salida conduce al pueblo inicial exacto por cada una de las 5 especies (vía botón dirección y comando `salir`).
   - Reconectar dentro del hogar conserva la ubicación en el hogar.
   - Salir y reconectar fuera no devuelve automáticamente al hogar.
   - Cero encuentros fijos y aleatorios; descanso normal permitido.
   - Cero PvP en el hogar.
   - Inventario y equipo operan sin sistema de almacenamiento nuevo.
   - Personajes existentes con posición válida no son teletransportados.
   - Reinicio de servidor / verificación de esquema preserva personajes en su hogar.
   - Salir del hogar no crea ruta regional falsa en `traversed_routes` y el viaje normal sí registra rutas (test de Junior 1).
2. Suite completa descubierta (`python -m unittest discover -s tests`): **401 tests PASS (0 fallos, 0 errores, 1 skipped en Windows)**.
3. MERGE: NO / DEPLOY: NO.

---

## Entrega lista para revisión: Acciones estructuradas derivadas del diálogo con gate autoritativo (#247) — 2026-09-27

- **DESARROLLADOR:** Antigravity (Desarrollador principal para implementaciones pesadas).
- **HEAD BASE:** `3d95121` (commit de PR #272, rama `antigravity/vt-246-npc-memory`).
- **TAREA:** Issue #247 — `VT-NPC/DEV: acciones estructuradas derivadas del diálogo con gate autoritativo`.
- **RAMA:** `antigravity/vt-247-npc-actions`
- **CONTRATO APROBADO Y ALCANCE (GAMEPLAY §35.7 y §35.8):**
  - **Separación estricta de canales:** El texto narrativo/conversacional jamás ejecuta acciones ni altera el mundo. La respuesta narrativa al jugador está completamente limpia de marcas técnicas (`<!--ACTION: {...}-->` es parseada y removida de la prosa).
  - **Catálogo allowlisted cerrado:** Solo 3 acciones válidas:
    1. `indicate_route`: señalar salida cardinal existente en la sala actual.
    2. `reveal_lore_topic`: revelar tema permitido dentro de `knowledge_allowed` del NPC (rechazo tajante si está en `knowledge_forbidden` o es desconocido).
    3. `show_workshop_item`: mostrar herramienta del taller presente en `VALID_WORKSHOP_TOOLS` (ej. `martillo_forja`, `tenazas_bronce`, `fuelle_cuero`).
  - **Gate autoritativo en servidor (`evaluate_action_gate`):**
    - Valida precondiciones objetivas: presencia de jugador y NPC en la misma sala (`room_id`), coincidencia de IDs, validez de targets frente a la topología del mundo (`world.ROOMS[room_id]["exits"]`) y la base de conocimiento autorizada (`knowledge_allowed` / `knowledge_forbidden`).
    - Si falla cualquier validación o la acción no está en la allowlist, `accepted=False`, se detalla la razón del rechazo y no ocurre mutación alguna.
  - **Cero mutaciones en estado de juego:** Ninguna acción de diálogo altera oro, inventario, stats, HP, XP, nivel ni equipamiento.
  - **Prevención de inyecciones maliciosas:** Intentos de inyectar acciones económicas (`give_gold`, `grant_item`, `execute_sql`, etc.) son rechazados tajantemente en el gate (`accepted=False`, reason `action_not_allowlisted`).
  - **Auditoría persistente en SQLite:** Tabla `npc_action_logs` con migración v13 idempotente (`IF NOT EXISTS`) e índice `npc_action_logs_player_npc`. Registra cada propuesta evaluada con timestamp, jugador, npc, sala, acción, payload, estado de aceptación y razón de rechazo.
  - **Endpoints integrados:** `/api/intent` y `POST /api/talk` exponen de manera estructurada `proposed_action` y `gate_result`.
- **ARCHIVOS MODIFICADOS / CREADOS:**
  - `vintage-telnet/server/store.py`: `SCHEMA_VERSION = 13`, tabla e índice de `npc_action_logs`, funciones `record_npc_action_gate_evaluation` y `list_npc_action_logs`.
  - `vintage-telnet/server/npc_dialogue.py`: `ProposedAction`, `ActionGateResult`, allowlist de acciones y herramientas, extracción limpia regex `extract_proposed_action`, evaluación del gate `evaluate_action_gate`, integración en `converse`.
  - `vintage-telnet/server/app.py`: propagación estructurada de `proposed_action` y `gate_result` en `/api/intent` y `POST /api/talk`.
  - `vintage-telnet/tests/test_npc_actions.py` (nuevo): 16 tests de catálogo allowlist, validaciones de gate, inyecciones, rechazo de secretos, auditoría SQLite, endpoints HTTP e inmutabilidad de estadísticas.
  - `vintage-telnet/server/HANDOFF.md`: este registro.

### Pruebas ejecutadas y verificación

1. `vintage-telnet/tests/test_npc_actions.py`: **16/16 tests PASS**.
   - Validación de extracción limpia de prosa vs acción propuesta.
   - Aceptación de `indicate_route` con salida válida.
   - Rechazo de `indicate_route` si la salida no existe en la sala.
   - Aceptación de `reveal_lore_topic` para temas permitidos.
   - Rechazo tajante de `reveal_lore_topic` para temas prohibidos o desconocidos.
   - Aceptación de `show_workshop_item` para herramientas del catálogo.
   - Rechazo tajante de inyecciones arbitrarias (`give_gold`, `grant_item`, `execute_sql`).
   - Cero mutaciones en estado de jugador (HP, XP, oro, inventario, equipo intactos).
   - Auditoría completa persistida en tabla `npc_action_logs`.
   - Rechazo en gate cuando jugador o NPC no están en la sala.
   - Integración end-to-end vía `/api/intent` y `POST /api/talk`.
2. Las 3 suites de NPCs (`test_npc_dialogue.py`, `test_npc_memory.py`, `test_npc_actions.py`): **41/41 tests PASS**.
3. Suite completa descubierta (`python -m unittest discover tests`): **389 tests PASS (0 fallos, 0 errores, 1 skipped en Windows)**.
4. MERGE: NO / DEPLOY: NO.

---

## Entrega lista para revisión: Memoria conversacional acotada por jugador y NPC (#246) — 2026-09-27

- **DESARROLLADOR:** Antigravity (Desarrollador principal para implementaciones pesadas).
- **HEAD BASE:** `7dd5186` (commit de PR #271, sobre `dfa97d0` de `origin/main`).
- **TAREA:** Issue #246 — `VT-NPC/DEV: memoria conversacional acotada por jugador y NPC`.
- **RAMA:** `antigravity/vt-246-npc-memory`
- **CONTRATO APROBADO Y ALCANCE:**
  - **Memoria por pareja jugador ↔ NPC:** Clave compuesta estricta `(player_id, npc_id)`.
  - **Aislamiento absoluto entre jugadores:** El prompt y contexto del jugador B jamás contienen información hablada entre el jugador A y el NPC.
  - **Aislamiento entre diferentes NPCs:** El historial de conversación de un jugador con un NPC (ej. Daro el herrero) no contamina el contexto con otro NPC (ej. Elena la boticaria).
  - **Ventana limitada y poda determinista FIFO:** Tamaño de ventana configurable (`window_size`, por defecto 5 turnos / 10 mensajes). Poda automática por SQL (`DELETE ... WHERE id NOT IN (SELECT id ... LIMIT ?)`), garantizando que la tabla nunca crezca indefinidamente.
  - **Inmutabilidad de la personalidad autoritativa:** La personalidad base (`temperament`, `speech_style`, `formality`, `traits`, `example_phrases`) y los conocimientos autorizados (`knowledge_allowed`) continúan siendo la regla suprema. El historial se inyecta como contexto conversacional reciente debidamente delimitado sin capacidad de alterar las directrices del NPC.
  - **Cero hechos de mundo:** La memoria es estrictamente dialógica; registrar intercambios no altera oro, inventario, nivel, atributos, HP ni salas del jugador.
  - **Persistencia y supervivencia a reconexión:** Almacenado en tabla SQLite `npc_memories` con migración v12 idempotente (`IF NOT EXISTS`). El historial reciente permanece disponible tras reconexión del jugador.
  - **Sin UI nueva, sin economía, sin quests automáticas:** Se preserva el flujo existente sin agregar elementos fuera de contrato.
- **ARCHIVOS MODIFICADOS / CREADOS:**
  - `vintage-telnet/server/store.py`: `SCHEMA_VERSION = 12`, migración v12 idempotente de `npc_memories`, funciones `record_npc_dialogue_exchange`, `get_npc_memory`, `clear_npc_memory`.
  - `vintage-telnet/server/npc_dialogue.py`: `history` en `DialoguePrompt`, formateo contextual en `build_dialogue_prompt`, lectura y guardado atómico en `converse(..., db_path=path)`.
  - `vintage-telnet/server/app.py`: propagación de `db_path=path` a `converse` en `/command`, `/api/intent` y `/api/talk`.
  - `vintage-telnet/tests/test_npc_memory.py` (nuevo): 9 tests de aislamiento entre jugadores/NPCs, poda FIFO, reconexión, inmutabilidad de mundo e integración HTTP.
  - `vintage-telnet/tests/test_npc_dialogue.py`: volcado de base de datos adaptado para aislar tablas de juego respecto a `npc_memories`.
  - `vintage-telnet/server/HANDOFF.md`: este registro.

### Pruebas ejecutadas y verificación

1. `vintage-telnet/tests/test_npc_memory.py`: **9/9 tests PASS**.
   - Aislamiento estricto entre jugadores (Matías vs Sofía).
   - Aislamiento estricto entre NPCs (Daro vs Elena).
   - Poda determinista FIFO con ventana 3 (de 7 turnos conserva solo 5, 6 y 7; turnos 1 a 4 eliminados).
   - Caso borde ventana 1 (conserva exactamente el último intercambio de 2 mensajes).
   - Inmutabilidad de la personalidad ante intentos de reescritura.
   - Persistencia tras recargar personaje desde la base de datos (reconexión).
   - `clear_npc_memory` selectivo por pareja.
   - Cero mutaciones en columnas de personaje (HP, XP, nivel, oro, equipo intactos).
   - Acumulación secuencial a través de `/command`, `/api/intent` y `/api/talk`.
2. `vintage-telnet/tests/test_npc_dialogue.py`: **16/16 tests PASS**.
3. Suite completa descubierta (`discover tests`): **373 tests PASS (0 fallos, 0 errores, 1 skipped en Windows)**.
4. MERGE: NO / DEPLOY: NO.

---

## Entrega lista para revisión: Contrato seguro de conversación dinámica con NPC (#245) — 2026-09-27

- **DESARROLLADOR:** Antigravity (Desarrollador principal para implementaciones pesadas).
- **HEAD BASE:** `dfa97d07945d8b85775796c82fa08d9980b191c9` (`origin/main` remoto vigente tras merge de Uñapiedra v1 / PR #239).
- **TAREA:** Issue #245 — `VT-NPC/DEV: contrato seguro de conversación dinámica con un NPC`.
- **RAMA:** `antigravity/vt-245-npc-dialogue`
- **CONTRATO APROBADO Y ALCANCE (GAMEPLAY §35):**
  - **Presencia autoritativa (Criterio 1):** Fail closed. Si el NPC no existe o no está en la misma sala del jugador (`room_id`), no conversa (`accepted=False`, reason explicativa). El proveedor de diálogo no es invocado bajo ninguna circunstancia de ausencia o inexistencia.
  - **Personalidad persistente (Criterio 2):** `build_dialogue_prompt` consume la personalidad persistente autoritativa (`temperament`, `speech_style`, `formality`, `traits`, `example_phrases`).
  - **Exclusión estricta de secretos (Criterio 3):** ÚNICAMENTE los elementos de `knowledge_allowed` entran al prompt. `knowledge_forbidden`, secretos del DM, tramas futuras y datos privados quedan completamente excluidos del contexto.
  - **Cero mutaciones en el mundo (Criterio 4 / GAMEPLAY §35.7):** Separación estricta entre diálogo y mecánica. Ningún texto generado altera SQLite, HP, Max HP, XP, monedas, inventario, equipo ni estado del mundo.
  - **Proveedor desacoplado (Criterio 5):** Interfaz abstracta `DialogueProvider`, desacoplada de cualquier LLM específico (Ollama/llama.cpp/API externa). Implementaciones `FixedDialogueProvider` y `MockDialogueProvider` para pruebas deterministas y configurable en runtime.
  - **Degradación segura (Criterio 6 / GAMEPLAY §35.9):** Cualquier excepción, timeout o respuesta vacía del proveedor es capturada silenciosamente, degradando de inmediato a `fallback_dialogue` del NPC con flag `is_fallback=True`.
  - **NPC canónico inicial:** Registrado Daro (`daro_herrero`) en `valdren_forja` (Valdren) con personalidad completa, conocimientos de forja/caminos y exclusión de secretos de Vaisgard.
  - **Endpoints y vistas integradas:**
    - `room_view`: expone `npcs` y añade acción `hablar` con targets correspondientes cuando hay NPCs en la sala.
    - `/command`: procesa `talk_npc` con soporte para mensajes contextuales (`hablar daro <mensaje>`).
    - `/api/intent`: procesa `talk_npc`, preservando código 409 cuando el NPC no está presente para total compatibilidad con la suite preexistente (`test_gameplay.py`).
    - `POST /api/talk`: nuevo endpoint estructurado para interacción conversacional cliente-servidor.
- **ARCHIVOS MODIFICADOS / CREADOS:**
  - `vintage-telnet/server/npc_dialogue.py` (nuevo): contrato de datos `DialoguePrompt`, `DialogueResult`, interfaz `DialogueProvider`, registro autoritativo `NPCRegistry`, función `build_dialogue_prompt`, motor autoritativo `converse` y carga de NPCs canónicos.
  - `vintage-telnet/server/app.py`: integración con `room_view`, `parse_intent`, `/command`, `/api/intent` y endpoint `POST /api/talk`.
  - `vintage-telnet/tests/test_npc_dialogue.py` (nuevo): 16 tests de aislamiento, criterios 1 a 6, inmutabilidad estricta de base de datos e integración HTTP.
  - `vintage-telnet/server/HANDOFF.md`: este registro.

### Pruebas ejecutadas y verificación

1. `vintage-telnet/tests/test_npc_dialogue.py`: **16/16 tests PASS**.
   - Criterio 1: target vacío, NPC inexistente y NPC en otra sala devuelven `success=False` y no llaman al proveedor.
   - Criterios 2 y 3: prompt contiene personalidad y solo `knowledge_allowed`; excluye totalmente `knowledge_forbidden` y secretos.
   - Criterio 4: snapshot comparativo de base de datos SQLite antes y después de 15 diálogos variados (vía `/command`, `/api/intent`, `/api/talk`) confirma 0 mutaciones en tablas ni en el jugador.
   - Criterio 5: `DialogueProvider` es abstracto; `FixedDialogueProvider` y `MockDialogueProvider` funcionan correctamente.
   - Criterio 6: timeout o excepción del proveedor degrada a `fallback_dialogue` sin arrojar error.
   - Vistas HTTP: `/command`, `/api/intent` y `/api/talk` funcionan en `valdren_forja` y rechazan adecuadamente en `valdren_centro`.
2. Suite completa descubierta (`discover tests`): **364 tests PASS (0 fallos, 0 errores, 1 skipped en Windows)**.
3. MERGE: NO / DEPLOY: NO.

---

## Entrega lista para revisión: Uñapiedra v1 para Hoshai / Khariel — Bloque A (#229) — 2026-09-27

- **DESARROLLADOR:** Antigravity (Desarrollador principal para implementaciones pesadas).
- **HEAD BASE:** `dc5721fa6bb3d58ef8a5c36720f4f9f60cb05372` (`origin/main` remoto vigente tras merge de PR #224, #225, #230).
- **TAREA:** Issue #229 — Bloque A (Fauna combatible para Hoshai/Khariel: Uñapiedra v1).
- **RAMA:** `antigravity/vt-229-unapiedra`
- **CONTRATO APROBADO:** Transferencia directa de Jugabilidad y Arquitectura en Issue #229 (2026-09-27) y asignación formal de Arquitectura (`ASIGNACIÓN ACTIVA — Antigravity`).
  - Perfil exacto: `unapiedra`, family `unapiedra`, ref 1, HP 30, precisión 45, daño 5, flee_agilidad 15, flee_percepcion 12, armadura 0.0.
  - Comportamiento canónico: evasivo, sisea y defiende refugio/grieta con mordida corta si es acorralada; no persigue.
  - Arte: no bloqueante; marco de combate neutral/vacío (`art` is None).
  - Contextos identificados: `alto_terrazas`, `alto_garganta`, hábitat `hoshai_alto`. Sala de encuentro autorizada: `alto_terrazas` (Sierra de Hoshai, terraza exterior de Khariel). 0% en interiores, forja, centro de Khariel y salas seguras. Sin spawn productivo inventado en pools.
- **ARCHIVOS MODIFICADOS / CREADOS:**
  - `vintage-telnet/server/creatures.py`: añade perfil de `unapiedra` en `CREATURES` y conserva `CREATURE_ART` sin entrada para marco neutral.
  - `vintage-telnet/server/world.py`: conecta encuentro en `alto_terrazas` (`ROOM_ENCOUNTER["alto_terrazas"] = "unapiedra"`).
  - `vintage-telnet/tests/test_unapiedra.py`: suite completa de 13 tests con playtest estadístico (40 combates por cada una de las 4 clases = 160 combates simulados), validación de contextos/hábitats/exclusiones e integración Flask/SQLite.
  - `vintage-telnet/tests/test_cinco_rutas.py`: incorpora `alto_terrazas` en la validación de encuentros autorizados en rutas y robustece limpieza SQLite.
  - `vintage-telnet/tests/test_screen_stability.py`: asegura paso determinista por `valdren_sendero` sin activación de encuentros espurios.
  - `vintage-telnet/tests/test_class_choice.py`: robustece importación de esquema y limpieza SQLite.
  - `vintage-telnet/tests/test_vt_deploy.py`: omite de forma limpia en plataformas Windows (específico de Linux/Raspberry Pi).
  - `vintage-telnet/server/HANDOFF.md`: este registro.

### Pruebas ejecutadas y verificación

1. `vintage-telnet/tests/test_unapiedra.py`: **13/13 tests PASS**.
   - Perfil de combate exacto y textos canónicos aprobados.
   - Marco de arte neutral/vacío (`art` is None) verificado tanto unitariamente como en `view["art"]` y en la API estructurada `/api/room`.
   - Evaluación contra nivel 1: clasifica como `favorable` (`combat.encounter_category(...) == "favorable"`).
   - Duración de combate comparable a Mordelinde (~5 rondas esperadas).
   - Huida estándar contra Agilidad 15 / Percepción 12 (47.45% base, 62.45% tras fallo).
   - Cero apariciones en salas civiles o seguras (`khariel_centro`, forjas, mercados, senderos interiores, Vaisgard).
   - No es boss, no quita armas, no introduce amenazas superiores.
   - **Playtest estadístico (Criterios 3 y 9):** 40 combates completos a muerte por clase a nivel 1 (Arcano, Juramentado, Sombra, Artífice = 160 combates):
     - **0 derrotas** (160/160 victorias).
     - HP final promedio > 70 HP en todas las clases.
     - 100% de éxito en 160 intentos de huida desde combate activo.
   - **Integración cliente-servidor real:**
     - Personaje Felaryn saliendo de `khariel_centro` a `alto_terrazas` encuentra a Uñapiedra.
     - `evaluar` devuelve encuentro favorable en `combat_log`.
     - Derrota otorga XP de familia `unapiedra` y limpia el encuentro en SQLite.
     - Huida con éxito retira al personaje a `khariel_centro` y limpia el encuentro.
2. Suite completa descubierta (`discover tests`): **330 tests PASS (0 fallos, 0 errores, 1 skipped)**.
3. MERGE: NO / DEPLOY: NO.

---

## Subentrega de #213 / DEATH-01 — Regresión del motor de muerte y respawn — 2026-09-26

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
