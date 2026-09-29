# Vintage Telnet — entrada rápida para agentes

Dirección de Arte: el flujo local de generación/versionado de borradores por OpenAI Image API está documentado en [ART_IMAGE_PIPELINE.md](ART_IMAGE_PIPELINE.md); la herramienta CLI vive en `tools/vt_art/` y nunca publica imágenes al runtime.

Este índice orienta la lectura; no sustituye `AGENTS.md`, el canon ni las instrucciones del issue. Comprueba `main` y la PR relacionada antes de actuar. Lee sólo las secciones necesarias para tu tarea; si hay divergencia entre issue antiguo y código/canon vigente, documenta la diferencia.

| Pregunta | Ruta |
|---|---|
| ¿Qué soy? | `AGENTS.md`, sección de tu rol y reglas comunes. Historiador: regla operativa de [#276](https://github.com/vaisork/MatiasGameLab/issues/276). |
| ¿Qué debo leer? | Issue asignado, comentarios y PRs dependientes. Después, las fuentes por rol de la tabla inferior. |
| ¿Qué trabajo tengo? | Cola específica de rol o issue asignado; comprueba si ya existe PR/rama. Una PR abierta sigue pendiente de integración. |
| ¿Dónde entrego? | Rama y PR vinculadas al issue para texto/código; arte por el carril de aprobación y publicación descrito en `AGENTS.md`. Registra pruebas, HEAD base, dependencias y consumidor siguiente. No hagas merge/deploy sin autorización de Javier. |

## Lectura según función

| Función | Entrada mínima después del issue |
|---|---|
| Historiador | `WORLD.md` como índice y sólo el archivo canónico del tema (`REGIONS.md`, `CREATURES.md`, `SPECIES.md`, etc.); `HISTORIAN_STATUS.md` contiene estado histórico, no la cola actual. Entrega directa en GitHub según #276. |
| Narrador | `NARRATIVE.md` por sección, canon físico correspondiente y PR de Historia de la que dependa; consulta `NARRATIVE_REGIONAL_ROUTES.md` si trabaja rutas. |
| Jugabilidad | `GAMEPLAY.md` por sección, issue y entregas de Historia/Narrativa pertinentes; números y reglas de encuentro requieren verificar el código de `server/`. |
| Arte | `ART_WORLD_GUIDE.md` (incluye orden de lectura por tipo de imagen), brief/issue y assets existentes; luego proceso de aprobación de `AGENTS.md`. |
| Desarrollo backend y QA | Issue/PR, módulos afectados en `server/`, pruebas relacionadas y `server/README.md` para operación. `server/HANDOFF.md` es historial de entregas, no una lectura inicial completa. |
| Desarrollo HTML | Issue/PR, plantillas afectadas en `server/templates/`, contrato del servidor y pruebas de UI. |
| Integración y Raspberry | PR y dependencias, HEAD de `main`, pruebas/CI, `ops/` y reporte de despliegue pertinente. La Raspberry conserva el estado vivo. |

## Autoridad y estados

- `main` es el código integrado; las PRs abiertas son entregas pendientes, algunas apiladas. No se debe tratar una rama como integrada sólo por su nombre.
- `AGENTS.md` contiene reglas comunes y fronteras. Para arte, `ART_WORLD_GUIDE.md` dirige hacia el canon visual. `GAMEPLAY.md` define mecánicas y los archivos de Historia/Narrativa definen sus respectivas áreas.
- `ARCHITECTURE_STATUS.md` y `TECHNICAL_RESEARCH_STATUS.md` describen etapas anteriores. No son un reporte actual del servidor.
- Los handoffs y reportes largos conservan evidencia histórica. Busca primero el issue/PR y la sección relevante, en vez de leerlos enteros.
- El Historiador entrega directamente en GitHub (#276). Drive sirve de bandeja para binarios de arte según `AGENTS.md`; un asset sólo es consumible cuando se publica en la ruta estable de GitHub.
