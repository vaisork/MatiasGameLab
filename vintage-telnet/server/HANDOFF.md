# Handoff del servidor — índice

El registro completo anterior está preservado sin cambios en [docs/archive/VT_SERVER_HANDOFF_FULL_2026-09-27.md](../../docs/archive/VT_SERVER_HANDOFF_FULL_2026-09-27.md). Este índice señala entregas registradas, **no su aprobación, integración o despliegue**. Comprueba el issue, PR y `main` antes de implementar o instalar.

| # | Entrega registrada |
|---:|---|
| — | REST-01 (#377): migración v13 tolera columnas existentes/parciales de presupuesto de descanso; PR #383, rama `junior/377-rest-budget`, base integrada `fe3b402`. 434 pruebas pasan en Linux/Python 3.13 con `python -m unittest discover -s tests -q`; workflow temporal de la rama retirado. Entrega para revisión/integración; sin Raspberry ni deploy — 2026-09-28 |
| — | Proveedor Ollama runtime opt-in (#382) — PR #386, rama `codex/vt-ollama-dialogue-runtime`, base `a03cfe4`; decisión explícita de Javier: permite Ollama para conversación de Vintage Telnet, nunca `ojo-de-agua:latest`. 23 pruebas de diálogo y suite de 420 pasan. Sonda sintética con `llama3.2:3b`: primera llamada excedió 60 s; segunda respondió en ~58 s con errores gramaticales y un detalle no confirmado. `qwen3:4b` queda sin probar. Servicio sigue en `fixed`; no desplegado — 2026-09-28 |
| — | Saltacresta v1 (#274): perfil y encuentro autorizado en `alto_terraza_abandonada`; PR #277, rama `antigravity/vt-274-saltacresta`, rebased sobre `67b851d`. Saltacresta 12/12, Uñapiedra 13/13 y rutas 9/9; suite de integración combinada con #294: 490/490 OK. Incluye playtest simulado de 160 combates. Sin cambios de arte ni deploy — 2026-09-28 |
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
