# Handoff: Arquitecto → Jugabilidad → Programador (VT2)

## Encargo
El usuario quiere que VT2 aproveche la experiencia de jugabilidad de los MUD clásicos de los noventa: armas, protecciones del Juramentado, crecimiento, combate, economía, habilidades y recompensas. **No inventar una matemática nueva sin comparar las históricas.** La documentación de este directorio es material de consulta y no aprobación automática de cambios.

## Prompt para Arquitecto
> Lee `AGENTS.md`, `vintage-telnet-2/AGENTS.md`, `CONTENT_CONTRACT.md`, `docs/DECISIONES_VIGENTES.md`, `docs/ARCHITECTURE.md`, `review/current/KNOWN_LIMITS.md`, el issue #655 y los cuatro archivos de `docs/research/mud-classic-mechanics/`. Audita `server/mechanics.py`, `server/engine.py`, `server/content.py`, catálogos de ítems, equipamiento, persistencia y pruebas. Contrasta DikuMUD, CircleMUD, Merc 2.2 y ROM 2.4 usando URLs y rutas/funciones exactas. Entrega una tabla 'actual VT2 / histórico / adoptar-adaptar-descartar / motivo / riesgo / pruebas' para THAC0/AC, dados, hitroll/damroll, tipos de defensa, slots, clases, habilidades, progresión XP/HP, economía, tiendas, botín y muerte. **No modifiques el motor todavía.** Divide en contratos cerrados de Jugabilidad, con WIP=1 y aprobación creativa cuando haya cifras nuevas. No copiar fuente C ni licencias dudosas.

## Prompt para Jugabilidad
> A partir de la auditoría del Arquitecto, redacta un contrato cuantitativo completo y verificable para un piloto del Juramentado: piezas de protección, una progresión limitada de armas, comparación de equipo, efectos en combate, restricciones por nivel/clase, adquisición, venta y migración. Incluye fórmulas elegidas, ejemplos de cálculo, tablas de balance, topes, estados, persistencia, errores, riesgos para las otras cuatro clases y criterios de aceptación. Si hay tensiones de diseño, preséntalas para aprobación, no las decidas silenciosamente. No cambiar canon ni desplegar.

## Prompt para Programador (ejecutar SOLO con contrato aprobado)
> Implementa exclusivamente el contrato cerrado y aprobado de Jugabilidad. Mantén Python/SQLite como autoridad y compatibilidad con partidas. Edita la capa correcta (`server/mechanics.py`, `server/engine.py`, `server/content.py`, catálogo, interfaz y tests sólo según necesidad). No copies código de terceros: reimplementa algoritmos documentados. Cubre equipar/desequipar, cálculo de daño y protección, comparar objetos, compra/venta, límites de clase/nivel, doble solicitud, inventario por instancia y migración. Ejecuta pruebas focales, `git diff --check` y suite amplia sólo si los cambios afectan combate central/persistencia según AGENTS. Entrega PR, evidencia, riesgos y rollback. No hacer merge ni desplegar Raspberry sin autorización.

## Secuencia de entregables
1. **Auditoría de estado real** con IDs, funciones, tablas, tests, fuentes y brechas.
2. **Contrato Jugabilidad v1** con números aprobados y 10 casos de aceptación.
3. **PR piloto**: equipamiento defensivo limitado y comparación, sin reescribir todo el combate de una vez.
4. **Balance y pruebas**: combates simulados y lectura real de progreso, luego decidir expansión.

## Condiciones de parada
- Licencia de una fuente no clara → documentar, no copiar.
- Sistema de defensa incompatible con motor actual → propuesta de adaptación, no sustitución automática.
- Falta de aprobación de valores, canon o economía → detener implementación.
- Riesgo de pérdida de partidas o duplicación → pruebas de migración y transacción antes de merge.
- Sin autorización de operación → no tocar Raspberry.

**Hecho por esta entrega:** investigación y prompts versionados. **No hecho:** auditoría exhaustiva de código, contrato cuantitativo aprobado, programación, pruebas de motor, merge o despliegue.
