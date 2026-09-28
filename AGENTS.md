# MatiasGameLab — guía de entrada para agentes

Este repositorio contiene **Senku** y **Vintage Telnet**. `main` es la fuente de verdad del código integrado y la documentación vigente. Antes de trabajar, identifica proyecto y rol, lee el issue asignado y comprueba PRs/rama existentes para evitar duplicación. Javier y Matías dirigen las decisiones creativas; no inventes canon ni reglas mecánicas ajenas a tu función.

La versión extensa anterior se conserva íntegra en [docs/archive/AGENTS_FULL_2026-09-27.md](docs/archive/AGENTS_FULL_2026-09-27.md) para consultar contratos especializados, responsabilidades históricas y trazabilidad. **No es una cola actual de tareas ni exige lectura completa al empezar.** Si una tarea toca una frontera no resumida aquí, consulta su sección antes de editar. Las instrucciones explícitas más recientes de Javier y del issue prevalecen sobre estados personales históricos del registro.

## Ruta corta: rol → lectura → tarea → entrega

| Rol | Lee para la tarea | Cola y entrega |
|---|---|---|
| Arquitecto / coordinación | `main`, issue/PR dependientes, fuentes del área | Define alcance, dependencias y aceptación en GitHub; no programa ni publica por defecto. |
| Historiador — Vintage Telnet | Canon del tema; `vintage-telnet/WORLD.md` como índice | Cola #282 y regla de entrega directa a GitHub #276; PR/documento e indicación del consumidor siguiente. Drive no es su carril normal. |
| Narrador — Vintage Telnet | Canon físico y sección relevante de `NARRATIVE.md` | Cola #284; entrega narrativa en rama/PR, enlazando dependencias. |
| Jugabilidad — Vintage Telnet | Sección pertinente de `GAMEPLAY.md` e inputs de Historia/Narrativa | Cola #285; entrega mecánicas/criterios con handoff a Desarrollo. |
| Dirección de Arte / artistas | `vintage-telnet/ART_WORLD_GUIDE.md`, issue, brief, assets existentes | Trabajo de arte en issue y bandeja de aprobación; operador publica asset aprobado en rama/PR. |
| Desarrollo pesado — Vintage Telnet | Issue, PRs dependientes, módulos y pruebas afectadas | Cola #278; rama y PR con HEAD base, pruebas y pendientes. |
| Junior 1 — backend ligero/QA | Issue y código/pruebas afectados | Cola #269; PR pequeña, sin invadir backend pesado ni canon. |
| Junior 2 — HTML/UI | Issue, `server/templates/`, contrato del servidor y pruebas | Cola #270; PR pequeña de interfaz. |
| Integrador / revisor | PR, dependencia, diff contra `main`, CI, handoff pertinente | Cola #254 cuando corresponda; no merge/deploy sin autorización de Javier. |
| Raspberry / operaciones | `vintage-telnet/ops/`, PR y plan de despliegue | Registra pruebas/logs en issue/PR; conserva estado persistente vivo. |
| Senku (desarrollo y Pixel Art) | Issue, `senku/`, assets y secciones de la guía extensa del rol | Rama/PR o asset según tarea; no usar copias viejas de `senku.html`. |

Entrada ampliada de Vintage Telnet: [vintage-telnet/README.md](vintage-telnet/README.md). La **cola** es el issue y sus comentarios, no un `HANDOFF.md` acumulado. WIP=1 donde lo indique el rol/issue; una PR abierta significa trabajo pendiente, no tarea libre.

## Reglas comunes de entrega

1. Registra HEAD base y tarea. Trabaja en rama identificable; guarda cambios y pruebas allí. Enlaza issue y PR e informa archivos, resultados, riesgos, trabajo previo afectado y próximo consumidor.
2. No hagas push directo ni merge a `main`, despliegue a Raspberry o publicación final salvo autorización explícita de Javier para esa acción. Una rama subida o prueba en Raspberry no equivale a integración.
3. Si `main` cambió desde la base, compara antes de integrar. No sobrescribas cambios de otro agente ni conviertas una tarea pequeña en refactorización extensa.
4. El servidor gobierna estado, reglas y acciones de Vintage Telnet; el navegador presenta. La Raspberry conserva cuentas, posiciones, inventarios y progreso vivos. Una actualización de código no debe sobrescribir esos datos.
5. Canon físico/cultural: Historiador; escenas y experiencia: Narrador; mecánicas/números: Jugabilidad; realización visual: Arte. Javier/Matías conservan dirección creativa. Si falta información, marca el bloqueo al responsable.
6. Para trabajo visual de Vintage Telnet, empieza por `ART_WORLD_GUIDE.md`, que indica lecturas por especie, pueblo, criatura, mapa o escena. Una imagen previa no reemplaza canon escrito.
7. Arte no cambia HTML/JS/CSS/lógica por defecto; Desarrollo no declara aprobado un asset. No reemplaces rutas estables ni un asset existente sin tarea explícita. El juego consume sólo assets publicados en GitHub.
8. Para solicitudes Pixel Art de ambos juegos usa `PIXEL_ART_REQUESTS.md`; verifica primero si el asset existe. Para binarios de arte de Vintage Telnet, la bandeja Drive recibe candidatos, Dirección de Arte aprueba y el Publicador/Integrador lleva lo aprobado a GitHub. GitHub conserva el asset consumible.
9. Cada cambio de código necesita pruebas pertinentes. El integrador revisa la versión exacta de la PR y el `main` actual; Javier no transporta parches o archivos manualmente entre agentes.

## Fuentes por proyecto

- **Vintage Telnet:** `vintage-telnet/GAMEPLAY.md`, `NARRATIVE.md`, `WORLD.md`, `REGIONS.md`, `SPECIES.md`, `CREATURES.md` y demás canon pertinente. Consulta por sección/tarea. `server/README.md` y `ops/` para contratos técnicos. `ARCHITECTURE_STATUS.md` y `TECHNICAL_RESEARCH_STATUS.md` son estados históricos; `HANDOFF.md` y `server/HANDOFF.md` contienen registros acumulados.
- **Senku:** juego actual en `senku/`; arte en `assets/`. Consulta `SENKU_GROWTH_RESEARCH.md` cuando una tarea afecte estructura de escenas o crecimiento técnico. No incrustes grandes imágenes Base64 ni reemplaces un HTML completo para un ajuste localizado.
- **Ambos:** GitHub `main` y el issue/PR vigente resuelven estado operativo. Si una regla resumida aquí no cubre un contrato de asset, despliegue, seguridad o publicación, consulta la sección específica del [archivo completo](docs/archive/AGENTS_FULL_2026-09-27.md) y anota cualquier contradicción antes de ejecutar.
