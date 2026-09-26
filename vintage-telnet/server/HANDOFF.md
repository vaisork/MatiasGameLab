# Handoff — Desarrollador de Servidor — Vintage Telnet

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
