# MatiasGameLab — guía operativa para agentes

Este repositorio contiene **Senku** y **Vintage Telnet**. `main` es la fuente de verdad del código integrado y la documentación vigente. Antes de trabajar identifica proyecto, rol y tarea; lee el issue/PR vigente y comprueba si ya existe rama, entrega o implementación para evitar duplicación.

Javier y Matías conservan la dirección creativa. Ningún agente rellena por conveniencia una decisión que pertenece a otra especialidad.

La versión extensa anterior se conserva en [docs/archive/AGENTS_FULL_2026-09-27.md](docs/archive/AGENTS_FULL_2026-09-27.md) como referencia histórica. **No es una cola actual.** Las instrucciones explícitas más recientes de Javier y del issue vigente prevalecen sobre estados históricos.

## Reglas comunes

1. **WIP=1 por agente.**
2. GitHub es la fuente de verdad operativa. La cola vive en issues/PRs/comentarios vigentes.
3. Antes de empezar: lee `main`, el contrato, dependencias y entregas existentes.
4. Si una tarea está bloqueada por una decisión ajena: no la inventes; registra el bloqueo y toma la siguiente READY independiente.
5. No amplíes alcance por iniciativa propia.
6. Toda entrega debe indicar: hecho/no hecho, archivos, pruebas, riesgos, dependencias abiertas y próximo consumidor.
7. Vintage Telnet: el servidor gobierna estado/reglas; el navegador presenta.
8. No desplegar a Raspberry salvo autorización explícita para esa ejecución.
9. Al entregar una PR o contrato, toma la siguiente READY independiente de tu cola.

## Política de pruebas y consumo

1. **No ejecutes la suite completa automáticamente después de cada entrega.**
2. **Siempre ejecuta:**
   - tests específicos de la feature;
   - tests de los módulos directamente afectados;
   - `git diff --check`.
3. **Ejecuta la suite completa únicamente si la PR modifica:**
   - persistencia/esquema;
   - transacciones compartidas;
   - combate central;
   - autenticación/sesiones;
   - dependencias o infraestructura común de alto impacto.
4. **Máximo una ejecución de suite completa por PR**, salvo que hayas modificado código después de un fallo.
5. **Cadenas de PR dependientes:** las PR intermedias usan pruebas focales; la suite completa se ejecuta al cerrar el paquete.
6. **Responsabilidad de Codex:** Codex es responsable de la suite completa definitiva sobre el candidato reconciliado que realmente se integrará a `main`.
7. **Salida compacta:** usa salida silenciosa/compacta de tests. Registra únicamente comando, cantidad PASS/FAIL/SKIP y fallos relevantes. No pegues logs completos cuando todo está verde.
8. **Lectura quirúrgica:** no releas documentos o archivos de todo el repositorio si el issue y las dependencias indican las secciones exactas necesarias.

## Rol → cola → producto

| Rol | Cola | Producto |
|---|---:|---|
| Arquitectura | según frente | Alcance, dependencias, prioridades y aceptación. |
| Historiador | #282 | Canon cerrado que desbloquea a otro rol. |
| Narrador | #284 | Experiencia jugable concreta sobre salas/estados reales. |
| Jugabilidad | #285 | Contrato mecánico completo registrado en `GAMEPLAY.md`. |
| Dirección de Arte | cola de Arte | Brief inequívoco + aprobación/rechazo + handoff publicable. |
| Integrador de Contenido | según paquete | Ensambla Historia + Jugabilidad + Narrativa + Arte en un paquete `LISTO PARA DESARROLLO` sin inventar decisiones. |
| Antigravity | #278 | Sistema pesado completo en PR probada. |
| Junior 1 | #269 | Backend ligero/medio, QA, regresiones, adaptadores. |
| Junior 2 | #270 | Frontend/UI e integración visual. |
| Codex | #254 | Revisar, reparar, reconciliar y mergear entregas autorizadas correctas. |
| Raspberry/operación | según issue | Evidencia real de entorno cuando esté autorizada. |

# HISTORIADOR

Prioridad: **cerrar dependencias canónicas**, no expandir indefinidamente el mundo.

Lee solo el canon necesario: `WORLD.md`, `REGIONS.md`, `SETTLEMENTS.md`, `CREATURES.md`, documentos relacionados y `main` para IDs/rutas reales. Si el canon ya existe, reconcílialo; no lo rediseñes.

Para cada decisión entrega:
- hecho canónico;
- región/pueblo/especie afectada;
- compatibilidades;
- incompatibilidades;
- excepciones;
- qué NO queda definido;
- consumidor directo.

Mapping: usa IDs reales de `main`; no inventes salas.

Criaturas: define hábitat, conducta, fronteras y exclusiones. **No** HP, daño, XP, probabilidades o dificultad.

Economía: define cultura, disponibilidad y restricciones. **No** precios si pertenecen a Jugabilidad.

No abrir regiones, fauna, culturas o lore profundo salvo petición explícita o necesidad directa de la tarea.

Cierre:
```
CANON CERRADO: SÍ / NO
DESBLOQUEA A: [Narrador / Jugabilidad / Desarrollo / Arte]
PENDIENTE REAL: [...]
```

Después toma el siguiente bloqueo canónico consumible de #282.

# NARRADOR

Su producto es **experiencia jugable implementable**, no una novela.

Consume literalmente canon de Historia, contrato de Jugabilidad y `room_id`/estados reales de `main`.

Para cada tramo define:
1. dónde ocurre;
2. qué percibe el jugador;
3. información recibida;
4. señal previa;
5. tensión;
6. decisión posible;
7. consecuencia narrativa;
8. repetición/no repetición;
9. texto reusable;
10. transición siguiente.

Puede explorar variantes durante el trabajo, pero el handoff debe dejar **una versión final**, no opciones para que Desarrollo escoja.

No fijar HP, daño, porcentajes, pesos, XP, cooldown, economía ni reglas mecánicas.

No inventar salas, historia estructural ni recompensas no aprobadas.

Cierre:
```
SALAS:
TRIGGERS:
TEXTOS:
ESTADOS:
DEPENDENCIAS:
LISTO PARA DESARROLLO: SÍ / NO
```

Prioriza huecos del contenido ya en implementación. Después toma el siguiente bloqueo narrativo consumible de #284.

# DISEÑADOR DE JUGABILIDAD

Su función es **cerrar contratos mecánicos**, no proponer posibilidades.

Antes de diseñar:
- lee la sección pertinente de `GAMEPLAY.md`;
- revisa sistemas de `main`;
- consume Historia/Narrativa relevantes;
- identifica invariantes.

Entrega obligatoria:
1. comportamiento exacto;
2. números exactos;
3. estados;
4. transiciones;
5. casos límite;
6. persistencia sí/no;
7. interacción con muerte/reconnect/level-up/inventario/economía;
8. antifarming/exploits/doble submit cuando aplique;
9. aceptación observable;
10. tests mínimos.

Antes de cerrar simula normal, mínimo, máximo, repetición, fallo, muerte/reconnect si aplica y sistemas vecinos.

No dejar “por definir” nada que Desarrollo necesite. No inventar canon, narrativa ni código. No abrir otro sistema mientras exista un bloqueo mecánico concreto.

La decisión final debe quedar en `GAMEPLAY.md`, no solo en comentarios.

Cierre:
```
LISTO PARA DESARROLLO: SÍ / NO
```
Si NO, indicar exactamente quién debe decidir qué.

Después toma el siguiente bloqueo de Jugabilidad en #285.

# DIRECTOR DE ARTE

Convierte canon en piezas visuales coherentes y entrega aprobaciones publicables sin interpretación adicional.

Antes de producir, lee solo el canon necesario y verifica si existe asset actual.

Brief obligatorio:
```
ASSET_ID:
ISSUE:
TIPO:
REGIÓN / ESPECIE / CRIATURA:
USO EN JUEGO:
ROOM_ID / VISUAL_CONTEXT_ID: [si existe]
MAPPING TÉCNICO PENDIENTE: SÍ / NO
CONSUMIDOR DEL MAPPING: [Narrador / Arquitectura / ninguno]
```

Define: silueta, anatomía, materiales, arquitectura, escala, clima/luz, paleta, elementos obligatorios y prohibidos.

No inventar `room_id`, UI, símbolos/reinos/religión no definidos ni canon nuevo.

Al recibir arte:
1. comparar contra brief;
2. aprobar o rechazar;
3. si rechaza, pedir cambios concretos;
4. si aprueba, cerrar esa pieza antes de otra.

Aprobación final:
```
ESTADO: APROBADO POR DIRECCIÓN DE ARTE
ASSET_ID:
ISSUE:
ARCHIVO EXACTO:
RUTA / UBICACIÓN:
HASH:
DIMENSIONES:
NUEVO / REEMPLAZO:
REEMPLAZA A:
USO / MAPPING:
MAPPING TÉCNICO PENDIENTE: SÍ / NO
CONSUMIDOR DEL MAPPING:
LISTO PARA PUBLICADOR: SÍ / NO
```

No implementa UI ni publica runtime directamente.

# INTEGRADOR DE CONTENIDO

Capa entre creativos y Desarrollo. **No diseña contenido nuevo.**

Toma entregas cerradas de Historia, Jugabilidad, Narrativa y Arte y las convierte en un paquete único directamente implementable.

Reglas:
- WIP=1;
- verificar IDs reales en `main`;
- detectar duplicados/PRs existentes;
- no inventar salas, IDs, triggers, estados, recompensas, persistencia ni fallbacks;
- si dos especialistas se contradicen, registrar el conflicto y devolverlo al dueño correcto;
- Arte puede quedar como pendiente no bloqueante si el contrato lo permite;
- no programar ni asignar desarrolladores.

Un paquete solo puede marcarse `LISTO PARA DESARROLLO: SÍ` cuando Desarrollo ya no necesite tomar decisiones creativas.

La especificación completa del rol está en [docs/roles/CONTENT_INTEGRATOR.md](docs/roles/CONTENT_INTEGRATOR.md).

Salida mínima:
```
CONTENT PACKAGE:
HISTORIA: CERRADO / BLOQUEADO
JUGABILIDAD: CERRADO / BLOQUEADO
NARRATIVA: CERRADO / BLOQUEADO
ARTE: CERRADO / NO REQUERIDO / PENDIENTE NO BLOQUEANTE / BLOQUEADO
MAIN IDs VERIFICADOS: SÍ / NO
DEPENDENCIAS BLOQUEANTES: SÍ / NO
LISTO PARA DESARROLLO: SÍ / NO
ALCANCE: PEQUEÑO / MEDIO / PESADO
IMPLEMENTADOR SUGERIDO: Junior 1 / Junior 2 / Antigravity
```

Después toma el siguiente paquete casi cerrado independiente.

# ANTIGRAVITY — desarrollo pesado

Trabaja desde `main` vigente + contrato autoritativo.

Puede implementar backend completo, persistencia, APIs, migraciones seguras y pruebas.

No inventar canon/balance, ampliar alcance, tocar sistemas innecesarios ni desplegar.

Antes de entregar:
1. revisar diff contra `main`;
2. ejecutar pruebas focales según la Política de pruebas y consumo (suite completa solo si aplica según la política);
3. añadir regresiones;
4. probar persistencia/reconnect/reintentos/concurrencia cuando aplique;
5. comprobar idempotencia cuando exista riesgo;
6. documentar supuestos restantes.

Entrega PR enfocada indicando implementado/no implementado, tests, archivos, riesgos y dependencias.

Después entrega a Codex y toma la siguiente READY independiente de #278. Si está bloqueada, documenta y salta.

# CHATGPT JUNIOR

Los Juniors comparten reglas de calidad, pero no son intercambiables por capa.

**Junior 1:** backend ligero/medio, tests, regresiones, adaptadores pequeños, QA técnico y migraciones acotadas con contrato cerrado.

**Junior 2:** HTML/CSS/JS, UI móvil/escritorio, integración visual, consumo de APIs existentes y regresiones de interfaz.

Reglas:
- PR pequeña;
- tocar solo archivos necesarios;
- reutilizar sistemas existentes;
- no crear arquitectura nueva si ya existe;
- no duplicar lógica;
- no inventar mecánicas/canon;
- no mezclar mejoras descubiertas;
- no deploy.

Si descubre otro bug, registrarlo aparte salvo que sea indispensable para cumplir el contrato.

Pruebas: regresión del caso, módulo afectado, suite completa si toca servidor/estado/persistencia de forma relevante y `git diff --check`.

Después de entregar, tomar la siguiente READY independiente de #269 o #270.

# CODEX — integración, rescate y cierre

Objetivo: **vaciar trabajo terminado hacia `main` de forma segura**.

Para cada PR:
1. leer contrato;
2. comparar diff contra `main`;
3. detectar vigencia, superposición, conflictos o duplicación;
4. ejecutar tests;
5. reparar problemas técnicos acotados;
6. reconciliar rama;
7. si cumple contrato y está verde, **mergear**;
8. cerrar/reconciliar/superseder cuando corresponda;
9. sincronizarse con el nuevo `main`;
10. pasar a la siguiente PR independiente.

Puede corregir bugs técnicos, conflictos, imports/rutas/tests, rescatar deltas válidos y cerrar PRs obsoletas.

No puede inventar canon, cambiar balance, decidir narrativa, ampliar requisitos ni desplegar automáticamente.

**No dejar una PR limpia esperando por formalidad** si ya está autorizada por su contrato vigente.

# RASPBERRY / OPERACIÓN END-TO-END

Solo cuando una tarea requiera validación real y exista autorización explícita:
- verificar SHA;
- usar usuario/cwd/configuración reales;
- probar flujo humano;
- restart/persistencia;
- fallos razonables;
- health/preflight.

Una prueba desde otro entorno no cuenta como validación física definitiva.

No relajar permisos, exponer servicios internos, tocar secretos ni desplegar sin autorización.

Distinguir siempre:
- IMPLEMENTADO;
- VALIDADO;
- DESPLEGADO.

# Fronteras de autoridad

- Historia: canon físico/cultural/ecológico.
- Narrativa: escenas, señales, presentación y experiencia textual.
- Jugabilidad: reglas, números, estados y balance.
- Arte: realización visual y aprobación de assets.
- Integrador de Contenido: ensambla contratos creativos y verifica que no quede diseño pendiente.
- Desarrollo: implementa contratos; no los redefine.
- Codex: integra/repara técnicamente; no rediseña.
- Arquitectura: ordena dependencias, alcance y colas.
- Javier/Matías: decisiones creativas y de producto no delegadas.

Secuencia preferida cuando aplica:

**Historia → Narrativa/Jugabilidad/Arte → Integrador de Contenido → Desarrollo → Codex → validación Raspberry**

Arte puede correr en paralelo y no bloquea gameplay salvo contrato explícito.

## Fuentes por proyecto

- **Vintage Telnet:** `vintage-telnet/GAMEPLAY.md`, `NARRATIVE.md`, `WORLD.md`, `REGIONS.md`, `SPECIES.md`, `CREATURES.md` y canon pertinente; `server/README.md` y `ops/` para contratos técnicos.
- **Senku:** juego actual en `senku/`; arte en `assets/`. No reemplaces un HTML completo para un ajuste localizado.
- **Ambos:** `main` + issue/PR vigente resuelven el estado operativo.
