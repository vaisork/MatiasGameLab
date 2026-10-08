# MatiasGameLab — reglas comunes

Antes de trabajar identifica proyecto, tarea vigente y HEAD de `main`. Lee el `AGENTS.md` del proyecto. No uses colas históricas como órdenes actuales.

- WIP=1 por agente. Comprueba ramas, PRs y entregas antes de duplicar trabajo.
- Javier y Matías conservan la dirección creativa. No inventar decisiones de otra especialidad ni ampliar alcance.
- VT2 es la base actual de Vintage Telnet. VT1 se conserva para rollback; no recibe desarrollo nuevo.
- Senku es independiente. `senku/legacy/` conserva el anterior; `senku/v2/` sólo prepara espacio, no autoriza construirlo.
- Las instrucciones explícitas recientes prevalecen sobre documentación histórica.
- No usar partidas reales como fixtures ni publicar credenciales, bases, fotografías originales o runtime.
- No desplegar, reiniciar servicios o cambiar túneles Raspberry sin autorización explícita para esa ejecución.
- Entregas: hecho/no hecho, archivos, pruebas, riesgos, dependencias y próximo consumidor.

## Pruebas

Ejecuta pruebas de la función y módulos afectados más `git diff --check`. No ejecutes suite completa tras cada entrega. Suite completa sólo al tocar persistencia/esquema, transacciones compartidas, combate central, autenticación/sesiones o infraestructura común de alto impacto; máximo una ejecución por PR salvo corrección tras fallo. En cadenas dependientes, ejecuta la definitiva sobre el candidato reconciliado. Salida compacta; distingue pruebas aisladas de validación de producción.

## Entradas

- [Mapa del repositorio](REPO_STRUCTURE.md).
- [VT2](vintage-telnet-2/AGENTS.md).
- [VT1 legacy](vintage-telnet/AGENTS.md).
- [Senku legacy](senku/legacy/AGENTS.md).
- [Senku v2](senku/v2/AGENTS.md).

Contratos anteriores: `docs/archive/AGENTS_PRE_CUTOVER_20261008.md`. Son referencia histórica, no cola vigente.
