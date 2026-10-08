# Estructura de MatiasGameLab

## Proyectos y fuentes de verdad

| Proyecto | Estado | Entrada | Fuentes |
|---|---|---|---|
| `vintage-telnet-2/` | Base actual | `README.md`, `AGENTS.md`, `docs/DECISIONES_VIGENTES.md` | `CONTENT_CONTRACT.md`, `CANON_EXPANSION.md`, `content/`, `server/`, `client/` |
| `vintage-telnet/` | Legacy/rollback | `AGENTS.md` | Código/canon anterior, consultados sólo con propósito explícito |
| `senku/legacy/` | Anterior recuperable | `AGENTS.md`, `index.html`, `juego.html` | Código, manifiesto y documentos legacy |
| `senku/v2/` | Preparado, sin construir | `README.md`, `AGENTS.md` | Futuro encargo de Javier; carpetas independientes |

## Raíz y compatibilidad

`README.md`, `AGENTS.md`, este mapa y `MIGRATION_REPORT.md` orientan. `index.html` y `matiasgamelab.webmanifest` son el portal. `.github/` conserva workflows; `docs/shared/` contiene investigación compartida e inventarios, `docs/archive/` los handoffs/contratos históricos. `VINTAGE_TELNET_2.md` es un acceso documental compatible.

La separación física de código Senku está completa. Se conserva una excepción deliberada para URLs y herramientas existentes: `assets/`, `art-masters/`, `tools/`, `scripts/`, los cuatro launchers de arte y HTML antiguos. Sus propietarios y límites están en `docs/shared/TOOLS.md`; no representan dependencias nuevas entre los juegos. Moverlos por estética rompería accesos/workflows y rollback. No usar los HTML antiguos como cliente de VT2.

## Documentación y evidencia

Visión VT2 versionada en `vintage-telnet-2/docs/PROMPT_MAESTRO_2026-10-08.md`. Agentes y autoridad se definen en cada proyecto. Revisión agrupada en `vintage-telnet-2/review/`; `review/current/` contiene índices, no una certificación nueva.

Inventario completo de raíz, movimientos y hashes de evidencia: `docs/shared/REORGANIZATION_INVENTORY.json`. Colas abiertas: `vintage-telnet-2/docs/QUEUE_MIGRATION_2026-10-08.md`.
