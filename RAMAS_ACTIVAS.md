# Índice de ramas — MatiasGameLab

**Última auditoría contra Git:** 2026-09-21  
**Base observada:** `main@fffc5e6ab1e295f02b76c2b6809dc07622f28b38`

Este archivo evita que una rama antigua parezca trabajo pendiente por el solo hecho de existir.

## Regla de mantenimiento

- El estado real de Git prevalece sobre este archivo.
- Después de cada fusión a `main`, el arquitecto responsable revisa inmediatamente las filas de su proyecto.
- Una rama ya absorbida no permanece en la tabla activa.
- Una rama semánticamente reemplazada por otra solución se marca **SUPERADA** hasta cierre o rescate.
- El Arquitecto de Senku mantiene Senku y recursos compartidos bajo su alcance.
- El Arquitecto de Vintage Telnet y Raspberry Pi mantiene Vintage Telnet.
- `python scripts/audit-branches.py --fetch` calcula la parte determinista: ahead/behind contra `origin/main`.

## Ramas activas o con entrega pendiente

| Rama | Proyecto | Estado operativo | Git vs main | Objetivo / coordinación | Responsable de mantener la fila |
|---|---|---|---|---|---|
| `arch/workflow-agents-index` | Compartido | **EN PREPARACIÓN** | ahead 16 / behind 0 al momento de crear este índice | Separar contratos, compactar AGENTS, índice de ramas y auditoría determinista. Cambio compartido: no altera autoridad de Senku ni Vintage Telnet. | Arquitecto Vintage Telnet durante esta entrega; revisión compartida antes de integrar |
| `art/vintage-telnet-html-assets` | Vintage Telnet | **LISTA PARA REVISIÓN/INTEGRACIÓN** | ahead 1 / behind 0 | Biblioteca modular HTML juvenil/mobile-first en `vintage-telnet/assets/html-ui/`; el commit declara pendiente de revisión/integración. | Arquitecto Vintage Telnet |
| `junior/vintage-telnet-help-character` | Vintage Telnet | **ACTIVA — NECESITA REVISIÓN SOBRE MAIN ACTUAL** | ahead 2 / behind 3 | Ayuda fullscreen + placeholder de imagen 3D de personaje. Handoff declara entrega preparada, no publicada y dependencia de asset. | Arquitecto Vintage Telnet |
| `claude/senku-revision-inicial` | Senku | **PR #2 ABIERTA — CLASIFICACIÓN/ACTUALIZACIÓN CORRESPONDE A SENKU** | ahead 5 / behind 99 | Fix HUD, churus no duplicables y taza en Casa; PR abierta. No evaluar ni integrar desde Vintage Telnet. | Arquitecto Senku / coordinación general |

## Ramas no activas o que no deben confundirse con una entrega lista

| Rama | Proyecto | Clasificación | Git vs main | Motivo |
|---|---|---|---|---|
| `codex/vintage-telnet-server` | Vintage Telnet | **SUPERADA COMO RAMA DE MERGE / RESCATE PARCIAL** | ahead 3 / behind 100 | PR #1 conserva una base útil de servidor, pero el Arquitecto ya decidió no mergearla directamente; se rescatará sobre rama fresca. |
| `junior/vintage-telnet-mobile-v2` | Vintage Telnet | **ABSORBIDA** | ahead 0 / behind 9 | Sus cambios ya están contenidos en `main`. |
| `junior/vintage-telnet-vertical-slice` | Vintage Telnet | **ABSORBIDA** | ahead 0 / behind 16 | Sus cambios ya están contenidos en `main`. |
| `claude/pixel-art-requests-dog-rat` | MatiasGameLab / Senku | **PENDIENTE DE CLASIFICACIÓN POR SU RESPONSABLE** | ahead 1 / behind 69 | Rama vieja sin PR; no corresponde al Arquitecto de Vintage Telnet decidir si se cierra o rescata. |
| `junior/senku-registro-20260920` | Senku | **PENDIENTE DE CLASIFICACIÓN POR SENKU** | ahead 1 / behind 61 | Rama de registro antigua; no asumir que sigue pendiente. |
| `junior/senku-registro-segundo-desarrollador` | Senku | **PENDIENTE DE CLASIFICACIÓN POR SENKU** | ahead 1 / behind 61 | Rama de registro antigua; no asumir que sigue pendiente. |
| `portal/registrar-disenador-matiasgamelab` | Recurso compartido / portal | **PENDIENTE DE CLASIFICACIÓN POR COORDINACIÓN GENERAL** | ahead 1 / behind 93 | Rama antigua de registro; no inferir integración desde Vintage Telnet. |

## Cómo usar este archivo

Antes de asignar una tarea:

1. ejecutar `python scripts/audit-branches.py --fetch`;
2. localizar ramas del mismo proyecto/objetivo;
3. leer únicamente el handoff/PR relevante;
4. si una rama ya resolvió el objetivo, reutilizarla o marcar la otra como SUPERADA;
5. actualizar este índice cuando cambie la clasificación semántica.

Los números ahead/behind son una instantánea y pueden cambiar. La clasificación operativa debe actualizarse después de fusiones, rescates o cierres.
