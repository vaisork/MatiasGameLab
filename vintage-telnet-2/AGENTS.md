# Agentes de Vintage Telnet 2

Lee `README.md`, `docs/DECISIONES_VIGENTES.md`, `CONTENT_CONTRACT.md` y sólo el canon necesario. Para continuidad: `docs/CONTEXTO_CONTINUIDAD.md`; para arquitectura: `docs/ARCHITECTURE.md`.

Este proyecto no importa el motor VT1. No leer Senku como contexto operativo ni copiar narración descartada. Servidor Python y SQLite gobiernan estado/reglas; cliente, mapa, personaje y bestiario muestran ese mismo estado. No crear canon ni estado 3D paralelo.

## Alcance autorizado

Reorganización operativa #649 autorizada el 8 de octubre de 2026. La profundización narrativa y desarrollo general continúan en pausa. No reactivar las antiguas colas al migrar agentes. Antes de programar, debe existir encargo vigente explícito para VT2.

## Fronteras

| Función | Producto y límite |
|---|---|
| Arquitectura/Work | Alcance, dependencias, prioridades, estructura y aceptación; no decidir tensiones creativas pendientes. |
| Historia | Canon físico/cultural/ecológico, IDs reales; no números de combate/economía. |
| Narrativa | Textos, escenas, señales y ritmo sobre salas/estados reales; no reglas ni recompensas nuevas. |
| Jugabilidad | Contrato cerrado con números, estados, casos límite, persistencia y aceptación; no canon nuevo. |
| NPCs | Presencia, motivos, diálogo y servicios compatibles con canon y motor; no inventar mecanismos. |
| Arte | Brief, realización y aprobación con asset_id, archivo, hash, dimensiones y mapping real; no publicar runtime. |
| Integración de contenido | Ensamblar contratos cerrados sin decidir contenido; explicitar bloqueos. |
| Desarrollo | Implementar contrato vigente en su capa; conservar servidor autoritativo y progresión. |
| Revisión/Codex | Verificar, reparar y reconciliar entregas autorizadas; no rediseñar canon ni desplegar. |
| Operación Raspberry | Sólo ejecución autorizada; verificar SHA, salud, persistencia, acceso y rollback real. |

Las funciones se conservan, las asignaciones antiguas no se trasladan por inercia. Ver `docs/CUTOVER_REPORT.md` y el inventario de colas antes de consumir trabajo heredado.

## Fuentes y comprobación

`content/world.json`, `content/regions/`, `CONTENT_CONTRACT.md`, `CANON_EXPANSION.md` y contratos vigentes definen contenido. `server/` implementa; `client/` presenta; `tests/` usa datos aislados. Ejecuta pruebas focales y QA cliente pertinente. Nunca confundir fixtures/API con sesión humana en Raspberry.

Evidencia en `review/README.md`; índices en `review/current/`. Los archivos históricos no certifican estado actual. Mantener scripts dentro del cwd de este proyecto; no usar DB de producción.

Credenciales/partidas se quedan en `runtime/`, fuera de Git. `ops/RASPBERRY_HANDOFF.md` define operación. No cambiar rutas físicas de producción por estética. Bestiario 3D/animaciones no están autorizados actualmente; las tensiones visuales figuran en el Prompt Maestro público.
