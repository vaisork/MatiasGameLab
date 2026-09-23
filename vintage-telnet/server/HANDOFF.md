# Handoff — Desarrollador de Servidor — Vintage Telnet

**Desarrollador:** Claude — Desarrollador de Servidor — Vintage Telnet.
**Estado:** cuarta ronda de PR #49, respondiendo a la lista consolidada de
bloqueos de Arquitectura (comentario del 2026-09-23T14:13:52Z).
**Rama:** `claude/vintage-telnet-server-lindero-roto` (PR #49).
**HEAD base de esta ronda:** `188468bccf5479db805f3d64b8906d24d025dab5`
(commit anterior de esta misma rama), con un merge de `origin/main`
(`e732bc9cee7e6a269968f41bb48b212e89d45523`) para traer `GAMEPLAY.md`
§24/27/29/30/31 y demás documentación al día — la rama no tenía esos
cierres porque había divergido de `main` en un punto anterior a ellos; no
afecta a ningún archivo de mi área (`server/`, `tests/`, `ops/`).

## Objetivo

Resolver los 6 puntos que Arquitectura listó como bloqueo único antes de
poder considerar PR #49 lista para integración (Issue #45, VT-NAR-003 "El
lindero roto"):

1. Alinear Mordelinde/Espinajo de rastrojo con
   `STARTER_CREATURE_BALANCE.md`.
2. No identificar "Mordelinde" a partir de una sola señal ambigua.
3. No concluir "criatura mucho mayor" del lindero a partir de `examinar
   cerca` por sí sola.
4. Mostrar comportamiento diferenciado de Mordelinde/Espinajo antes de la
   decisión de combate.
5. Retirar el HP numérico exacto del enemigo de la interfaz (GAMEPLAY.md
   31).
6. Pruebas correspondientes + suite completa verde.

## Cambios

### 1. Perfil de criaturas alineado al balance aprobado
- `server/creatures.py`: Mordelinde y Espinajo de rastrojo ya no derivan
  HP/precisión/daño de un modelo genérico de atributos (`fuerza`,
  `destreza`, `percepcion`, `base_ataque`) — copian **tal cual** el
  perfil v1 aprobado por Jugabilidad en `STARTER_CREATURE_BALANCE.md`:
  Mordelinde HP 28 / precisión 45% / daño 5; Espinajo HP 40 / precisión
  50% / daño 8.
- `server/combat.py`: nuevas funciones puras `resolve_fixed_attack_roll` y
  `fixed_expected_dps`, que resuelven el golpe de una criatura con
  precisión/daño fijos en vez de `resolve_attack_roll`/`expected_dps`
  (que siguen usándose solo para el golpe del jugador, cuyos atributos sí
  son reales).
- `server/app.py`: `attempt_evaluate`, `attempt_attack` y `attempt_flee`
  usan las funciones fijas para el golpe/DPS del enemigo.
- Verificación cruzada con `GAMEPLAY.md` §24.11 ("Validación del piloto de
  Edran", ya cerrada en `main`): simulando con estos números exactos,
  Mordelinde tarda ~5.1 rondas en caer y el jugador recibe ~11.5 HP de
  daño esperado (referencia aprobada: ~6 rondas / ~14 HP); Espinajo ~7.3
  rondas / ~29.1 HP (referencia: ~8 rondas / ~32 HP) — coincide dentro del
  margen esperado de una simulación de referencia.
- `combat.encounter_category`: los umbrales de razón (explícitamente
  "afinables de balance, no un cambio de las 5 categorías" según
  GAMEPLAY.md §22.3) se recalibraron para que ese perfil aprobado
  reproduzca la banda que el propio `STARTER_CREATURE_BALANCE.md`
  describe en prosa: Mordelinde Favorable, Espinajo Comparable. Antes de
  este ajuste, los números exactos aprobados clasificaban a Mordelinde
  como Trivial y a Espinajo como Favorable — un desajuste entre la banda
  de riesgo esperada y la banda calculada, no de los números de combate en
  sí.

### 2-3. Ninguna señal aislada concluye más de lo que demuestra
- `server/store.py`: tabla nueva `examined_signals` (esquema v5) +
  `mark_examined_signal`/`has_examined_signal`, para saber qué señales
  examinó ya un jugador en una sala.
- `server/app.py` (`resolve_inspect`):
  - `senales_mordelinde` ahora exige haber examinado **tallos Y
    montículos** (antes bastaba cualquiera de las dos por separado;
    ninguna nombra "Mordelinde" por sí sola).
  - `lindero_roto` ya no se concede con `examinar cerca` (solo demuestra
    violencia, no tamaño); se concede con `examinar huellas`, que sí
    compara tamaño explícitamente contra las criaturas pequeñas ya
    vistas.

### 4. Comportamiento diferenciado antes de decidir
- `server/creatures.py`: campo nuevo `behavior_text` por criatura,
  reformulando sin inventar el comportamiento ya descrito en
  `CREATURES.md` ("corre en zigzag hacia agujeros o maleza" / "eriza las
  púas antes de atacar").
- `server/app.py` (`room_view`) y `templates/entry.html`: la caja de
  encuentro muestra esa línea de comportamiento junto al nombre, antes de
  que el jugador decida atacar/huir/evaluar.

### 5. Sin HP numérico de enemigos (GAMEPLAY.md 31)
- `server/combat.py`: `enemy_condition(hp_current, hp_max)` — bandas
  cualitativas exactas de GAMEPLAY.md 31.1 (entero/apenas afectado,
  herido, malherido, al borde de caer, derrotado).
- `server/app.py` (`room_view`) y `templates/entry.html`: la caja de
  encuentro ya no expone `hp_current`/`hp_max`; expone `condition`
  (cualitativa) y `behavior`. El HP propio del jugador sigue exacto
  (sin cambios).

### 6. Pruebas y documentación
- `tests/test_pilot_lindero_roto.py`: pruebas nuevas/ajustadas para los 5
  puntos anteriores (perfil de criatura, señal única insuficiente para
  Mordelinde, `cerca` insuficiente para el lindero, condición cualitativa
  sin HP numérico y su descenso de banda al recibir daño, comportamiento
  distinto Mordelinde/Espinajo). `CreatureCalibrationTests._category_for`
  actualizado a las funciones fijas.
- `tests/test_entry.py`: `schema_version` esperado actualizado de 4 a 5
  (nueva tabla `examined_signals`).
- `server/README.md`: sección de combate/descubrimientos actualizada para
  reflejar el perfil fijo, la condición cualitativa y el gating de
  señales; conteo de pruebas actualizado.

## Pruebas

`.venv/bin/python -m unittest discover -s tests -v` → **84/84 OK** (77
previas + 8 nuevas − 1 fusionada en una prueba existente ampliada).

## Pendiente (sin cambios respecto a la ronda anterior, no bloqueante para Issue #45)

- Recuperación pasiva de fatiga fuera de combate (GAMEPLAY.md 24.7).
- Rondas semi-automáticas y defensa contextual (24.1-24.2) — diferidas al
  Issue #43 por decisión del Arquitecto.
- Cornalomo sigue sin estadísticas: se pedirá tabla a Jugabilidad cuando
  exista combate real contra él.

## Riesgos

- La recalibración de los umbrales de `encounter_category` es un cambio de
  balance técnico (no de las 5 categorías ni de ninguna fórmula de
  GAMEPLAY.md), explícitamente autorizado como afinable por GAMEPLAY.md
  §22.3. Si Jugabilidad/Arquitectura prefiere otro punto de calibración,
  es un solo bloque de constantes en `combat.encounter_category` con su
  propio comentario citando esta decisión.

**LISTO PARA PUBLICAR: NO** — pendiente de una nueva revisión de
Arquitectura/Jugabilidad/Psicopedagogía antes de tocar `main`, como el
resto de esta entrega.
