# Informe de reorganización — 2026-10-08

## Resultado

VT2 queda como base actual; VT1 queda identificado como legacy/rollback. Senku anterior vive en `senku/legacy/` y Senku v2 tiene agentes, assets, documentos y tests independientes, sin implementación nueva. La raíz tiene una entrada común y documentación por proyecto.

Base auditada: `e50be1f9c8dfcc6ad6e1507e40dec1189433a7bd`. Encargo: #649 y `vintage-telnet-2/docs/WORK_REPO_REORGANIZATION.md`. Javier confirmó VT2 desplegado y autorizó comenzar el 8 de octubre de 2026. La pausa narrativa no se levanta con este encargo.

## Movimientos e inventarios

672 archivos trasladados, sin borrar evidencia. Se agrupan revisiones por función y ciclos históricos en `review/archive/2026-10-07/`. Los documentos VT1 de raíz pasan a `vintage-telnet/docs/archive/`; handoffs transversales e instrucciones anteriores pasan a `docs/archive/`; investigación compartida pasa a `docs/shared/`; investigación Senku pasa a `senku/legacy/docs/`.

`docs/shared/REORGANIZATION_INVENTORY.json` clasifica las 37 entradas originales de raíz y contiene cada movimiento y hashes originales de evidencia. El archivo vacío `To` se conserva como huérfano en archivo; no contiene una tarea pendiente. Las referencias Markdown y rutas de salida de scripts se actualizan; Python relativo conserva la raíz VT2 tras su traslado.

## Agentes, colas y automatización

`AGENTS.md` contiene reglas comunes; cada proyecto tiene contrato propio. Se conservan las fronteras de Arquitectura, Historia, Narrativa, Jugabilidad, NPCs, Arte, Integración, Desarrollo, Revisión y Operación. No se asigna trabajo nuevo a VT1 ni se trasladan sus colas como órdenes actuales.

Se clasifican 156 entradas abiertas (139 issues y 17 PRs) en `vintage-telnet-2/docs/QUEUE_MIGRATION_2026-10-08.md`: 1 MIGRAR, 57 SUPERSEDED, 86 CONTENIDO VÁLIDO potencialmente recuperable y 12 ARCHIVAR. No se declara YA RESUELTO EN VT2 por semejanza de título. No se cierran issues ni se mergean PRs antiguas en lote; se preservan sus contratos y ramas. Reutilizar contenido requiere tarea VT2 vigente y revisión de canon/IDs.

Se congelan eventos automáticos de generación/publicación/revisión/limpieza de arte VT1. Los workflows manuales conservan sus rutas y exigen `legacy_ack=true`. No se elimina código ni se ejecuta generación con coste API. CI VT1 de pruebas/assets permanece; se añade CI VT2 para Python, mapa/lectura y estructura.

## Prompt Maestro

`vintage-telnet-2/docs/PROMPT_MAESTRO_2026-10-08.md` versiona transcripción pública del PDF entregado por Javier, con fecha, procedencia y SHA-256 del original. Se omiten portada y datos de acceso; no se publica el PDF sensible. Instrucciones posteriores, pausa narrativa y límites actuales prevalecen sobre aspiraciones del prompt. Las tensiones UI/3D y móvil/escritorio quedan explícitas, sin resolverlas silenciosamente.

## Compatibilidad preservada

- `senku/` y `senku/juego.html` redirigen a legacy; `senku.html` y el manifiesto antiguo siguen funcionando. Se conservan origen y claves localStorage `senku_*`.
- Senku tiene manifiesto propio junto a su implementación. Sus assets históricos conservan URLs de raíz para evitar romper enlaces/cachés.
- Portal enlaza al VT2 desplegado. HTML VT1 y previews quedan recuperables; no son clientes VT2.
- `assets/`, `art-masters/`, herramientas, tests de publicación y launchers históricos mantienen rutas como excepción deliberada. Propiedad detallada en `docs/shared/TOOLS.md`. No constituyen dependencia de VT2 ni de Senku v2.
- No se modifica código de servidor, cliente, contenido, tests existentes ni instaladores/launchers de VT2. Sólo se actualiza documentación operativa y scripts de revisión.
- No se despliega, reinicia ni cambia configuración/DB/túneles Raspberry.

## Validación

- `python -m unittest discover -s tests -q`, desde VT2: **132 PASS**, DBs temporales, 26,622 s.
- `node client/qa-map.mjs`: **15 comprobaciones PASS**.
- `node client/qa-map-paths.mjs`: **PASS**.
- `node client/qa-printing.mjs`: **34 comprobaciones PASS**.
- `python scripts/check_repo_structure.py`: movimientos, hashes, links Markdown, agentes y manifiestos; **PASS: 672 movimientos y 527 hashes**, enlaces y manifiestos válidos.
- 9 workflows YAML, 11 scripts Python y 32 scripts JavaScript trasladados: **PASS de sintaxis**; shell y JavaScript Senku: **PASS**. Se corrige indentación YAML inválida preexistente en el mensaje de commit del publicador VT1.
- 8 rutas HTTP estáticas de portal/Senku/assets: **200 OK**.
- Publicador de assets preservado: **17 tests PASS** (casos negativos intencionales incluidos); no se ejecuta publicación/generación real.
- `git diff --check`: comprobado sobre candidato final.

Las pruebas locales no certifican sesión humana de producción, reinicio físico, SHA Raspberry ni diversión. Muchos scripts de navegador conservan dependencias locales históricas; su traslado no instala Playwright/Chrome/fixtures de Ubuntu.

## Riesgos y trabajo pendiente real

Mantener nombres de rutas de producción y código narrativo preservado que aún no se ha desplegado. No sustituir SQLite Raspberry por Ubuntu. Antes de cerrar #649 definitivamente registrar SHA productivo y comprobación autenticada de sus criterios restantes; el informe de despliegue previo declara límites de sesión humana y reinicio físico.

La clasificación de contenido es un inventario, no aprobación automática de cada contrato. La separación de assets antiguos conserva rutas de compatibilidad; retirarlas requerirá una migración específica que considere el hosting y cachés.

## Rollback

Repositorio: revertir el commit/PR de reorganización mediante `git revert`, conservando cambios posteriores. El inventario permite reconstruir rutas anteriores; no borrar ramas para revertir.

Producción: no necesita reversión porque esta entrega no la toca. Para rollback del juego, usar el procedimiento documentado en `vintage-telnet-2/review/qa/raspberry-deploy/DEPLOYMENT.md`: servicio antiguo y respaldo conservados, origen Funnel anterior 8080, detener nuevo si corresponde. Requiere autorización de operación; nunca restaurar DB antigua encima de una partida activa ni mezclar schemas.
