# Handoffs — índice de entregas

El registro íntegro anterior está en [docs/archive/HANDOFF_FULL_2026-09-27.md](HANDOFF_FULL_2026-09-27.md), conservado sin modificación. Este archivo es un índice para localizar una entrega; **no certifica que esté integrada, desplegada o aún pendiente**.

Para trabajar: lee `main`, tu issue y la PR/branch vinculada. Si un handoff menciona un pendiente, verifica su estado en issue/PR y código actual. No ejecutes instrucciones históricas sólo por aparecer aquí. Las nuevas entregas deben quedar primero en el issue/PR con HEAD base, pruebas y consumidor; añade aquí un enlace breve únicamente si sirve como índice transversal.

| # | Entrega registrada (orden del documento completo) |
|---:|---|
| 1 | ENTREGA — Reloj global de hora del día conectado a `world.get_ambient()` (Issue #138) |
| 2 | ENTREGA — Arte aprobado en el juego: Mordelinde, Espinajo de rastrojo y camino de Veyra (#151) |
| 3 | ENTREGA — Las Cinco Rutas completas con la geografía de REGIONS.md |
| 4 | ENTREGA — Camino de los Campos, bloque 1 (A1–A10) + minimapa sin nombres encimados |
| 5 | ENTREGA — Cuentas con varios personajes (hasta 5) + nombres de personaje únicos + registro más claro |
| 6 | ENTREGA — Ajuste tras revisión de Jugabilidad en PR #165 (GAMEPLAY §33) |
| 7 | ENTREGA — Motor de encuentros aleatorios (Issue #160) |
| 8 | ENTREGA — Sin parpadeo: las acciones del juego ya no recargan la página + barra del enemigo abajo |
| 9 | ENTREGA — Relato de la pelea (historial de combate) + la pantalla siempre cabe en el celular |
| 10 | ENTREGA — Pantalla estable: la imagen y los controles ya no se mueven |
| 11 | ENTREGA — Seguridad: panel del DM solo desde la red privada (no desde internet) |
| 12 | ENTREGA — Vintage Telnet: navegación (minimapa, salidas con nombre, flechas del teclado) |
| 13 | ENTREGA — vt-deploy: prueba completa en Raspberry simulada + reintento después de rollback |
| 14 | ENTREGA — Vintage Telnet Issue #112: elección de clase inicial + arma inicial por clase |
| 15 | ENTREGA — Vintage Telnet Issue #135: pantalla principal según la maqueta del Director de Arte |
| 16 | ENTREGA — Vintage Telnet: pantalla para gastar PA en el panel Personaje |
| 17 | ENTREGA — Vintage Telnet Issue #125: `visual_context_id` server-side, arte por contexto no por `room_id` |
| 18 | ENTREGA — Fixes puntuales de `entry.html` reportados por Javier jugando en celular real |
| 19 | ENTREGA — Vintage Telnet Issue #73: Esquivar/Bloquear/Resistir + `available_actions` |
| 20 | ENTREGA — Senku: portada narrativa antes del juego |
| 21 | ENTREGA — Senku Issue #81: DESPERTAR resistente a almacenamiento bloqueado |
| 22 | ENTREGA — Binding narrativo explícito de Issue #46 en PR #49 (tercera vuelta del Arquitecto) |
| 23 | ENTREGA — Respuesta a revisión arquitectónica de PR #49 (fatiga/heridas/recuperación §24, cooldown de monstruos) |
| 24 | ENTREGA — Microaventura piloto jugable "El lindero roto" (Issue #45) |
| 25 | ENTREGA — Ajustes tras la instalación real en Raspberry Pi |
| 26 | ENTREGA — Segunda respuesta a la revisión del Arquitecto (PR #6, rondas 3 y 4) |
| 27 | ENTREGA — Respuesta a la revisión del Arquitecto (PR #6) |
| 28 | ENTREGA — Login real + arte integrado en el servidor (mismo origen) |
| 29 | ENTREGA — Claude, Desarrollador de Servidor de Vintage Telnet |
| 30 | ENTREGA PARA CHATGPT (histórico — publicada) |
| 31 | INTEGRACIÓN DE ARTE HTML — Vintage Telnet |
| 32 | PREPARACIÓN DE BASE DE DATOS Y JUGABILIDAD REAL — Vintage Telnet |
| 33 | PRIORIDAD P0 — PRIMER SLICE JUGABLE REAL |
| 34 | VT-SERVER: mapa regional servido + rumbo autoritativo (Issue #120) |
| 35 | VT-SERVER: gasto de PA, PP, subida de nivel sin curación total y fatiga pasiva (PLAYABILITY_READINESS P1 #5/#6) |

Las entradas de Senku y Vintage Telnet están mezcladas en el registro histórico. Para el backend de Vintage Telnet, usa también [vintage-telnet/server/HANDOFF.md](../../vintage-telnet/server/HANDOFF.md). Los resultados de despliegue están en `vintage-telnet/ops/RASPBERRY_REPORT.md`, que puede contener estado antiguo; comprueba el estado vivo antes de operar.
