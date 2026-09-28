# Handoff del servidor — índice

El registro completo anterior está preservado sin cambios en [docs/archive/VT_SERVER_HANDOFF_FULL_2026-09-27.md](../../docs/archive/VT_SERVER_HANDOFF_FULL_2026-09-27.md). Este índice señala entregas registradas, **no su aprobación, integración o despliegue**. Comprueba el issue, PR y `main` antes de implementar o instalar.

| # | Entrega registrada |
|---:|---|
| — | En revisión: proveedor Ollama runtime opt-in después de #245 — rama `codex/vt-ollama-dialogue-runtime`, base `a03cfe4`; 23 pruebas de diálogo y suite de 420 pasan. Prueba sintética real con `llama3.2:3b` excedió 60 s sin respuesta; modelo descargado de memoria. Runtime no habilitado ni desplegado — 2026-09-28 |
| 1 | Entrega lista para revisión: HOME-CORE — hogar personal persistente mínimo (#280) — 2026-09-27 |
| 2 | Entrega lista para revisión: Acciones estructuradas derivadas del diálogo con gate autoritativo (#247) — 2026-09-27 |
| 3 | Entrega lista para revisión: Memoria conversacional acotada por jugador y NPC (#246) — 2026-09-27 |
| 4 | Entrega lista para revisión: Contrato seguro de conversación dinámica con NPC (#245) — 2026-09-27 |
| 5 | Entrega lista para revisión: Uñapiedra v1 para Hoshai / Khariel — Bloque A (#229) — 2026-09-27 |
| 6 | Subentrega de #213 / DEATH-01 — Regresión del motor de muerte y respawn — 2026-09-26 |
| 7 | Entrega limpia de Issues #209 y #211 — Portada pública y lectores canónicos — 2026-09-26 |
| 8 | Relevo de #207 — EDRAN-01 — 2026-09-26 |
| 9 | Entrega histórica — Issue #57 (conservada) |

La entrada histórica #57 continúa con apartados «Contexto», «Objetivo», «Cambios», «Pruebas», «Trabajo previo afectado», «Pendiente» y «Riesgos» en el registro íntegro. No se descartó.

Para nuevas entregas: documenta primero en el issue/PR la rama, HEAD base, cambios, pruebas, pendientes y consumidor. Consulta [server/README.md](README.md) para contratos actuales y `vintage-telnet/ops/` para operación. La Raspberry conserva el estado vivo; no inferir estado de producción de este índice.
