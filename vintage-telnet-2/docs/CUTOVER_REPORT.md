# Relevo operativo VT2 / VT1 — 2026-10-08

VT2 es la base actual de trabajo por confirmación de Javier. VT1 se conserva como legacy/rollback y no recibe tareas nuevas. Esta entrega ordena repositorio y contratos; no despliega ni vuelve a ejecutar migración de servicio/datos.

Evidencia de sustitución: [DEPLOYMENT.md](../review/qa/raspberry-deploy/DEPLOYMENT.md). Servicio antiguo detenido/deshabilitado, nuevo servicio de usuario y Funnel a 8083 documentados. Confirmación de Javier: «ya está desplegado vt2 así que comienza», 8 de octubre de 2026.

Agentes migrados: Arquitectura/Work, Historia, Narrativa, Jugabilidad, NPCs, Arte, Integración, Desarrollo, Revisión y Operación, con fronteras en [AGENTS.md](../AGENTS.md). Migración de funciones no reactiva colas ni redacción pausadas.

Inventario de 156 entradas abiertas: [QUEUE_MIGRATION_2026-10-08.md](QUEUE_MIGRATION_2026-10-08.md). Código del motor VT1 no se traslada; arte/canon potencialmente útil requiere reconciliación específica. Se conservan ramas, PRs, releases y documentos recuperables.

Visión versionada: [Prompt Maestro público](PROMPT_MAESTRO_2026-10-08.md). Se registran tensiones visuales y prevalencia de decisiones posteriores; se excluyen datos de acceso.

Cierre estructural, pruebas, compatibilidad y rollback: [MIGRATION_REPORT.md](../../MIGRATION_REPORT.md).

## Límite de cierre #649

La reorganización está lista para revisión/integración. No se certifica SHA actual de Raspberry, sesión humana autenticada prolongada ni reinicio físico desde este entorno. El informe de despliegue anterior distingue estos límites. Antes de cerrar #649 como cutover validado, registrar evidencia productiva de sus criterios pendientes mediante una tarea de operación autorizada. La pausa de desarrollo narrativo sigue vigente.
