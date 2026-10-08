# Biblioteca de mecánicas históricas MUD para VT2

**Fecha:** 2026-10-08. **Estado:** investigación / instrucciones de análisis, no contrato numérico aprobado ni código desplegado.

## Propósito
Entregar al Arquitecto, Jugabilidad y Programador fuentes primarias y secundarias para **reimplementar con código original** mecánicas probadas de MUD clásicos. No importar motores C ni copiar mundos, nombres propios, prosa o licencias sin revisión.

## Fuentes históricas — consultar antes de diseñar

| Sistema | Documentación / código para estudio | Qué aporta | Licencia / precaución |
|---|---|---|---|
| DikuMUD | https://dikumud.com/dikumud-license/ | Origen, THAC0, AC, combate, áreas | Autores anunciaron LGPL en 2020; derivados NO automáticamente relicenciados |
| CircleMUD | https://www.circlemud.org/ ; https://www.circlemud.org/license.html | Referencia de mecánicas Diku, comandos, habilidades y progresión | Sitio declara LGPL desde 2020; revisar archivos concretos |
| CircleMUD Builder's Manual | https://www.circlemud.org/pub/jelson/CircleMUD/3.x/uncompressed/current/doc/building.pdf | Tablas de mobs: nivel, THAC0, AC, HP, dados de daño, oro, XP | Documento externo: enlazar, no republicar íntegro |
| CircleMUD ayuda AC | https://github.com/Yuffster/CircleMUD/blob/master/lib/text/help/info.hlp | AC y representación de estadísticas para jugadores | Fuente comunitaria, confirmar versión |
| Merc 2.2 | https://github.com/benjamin-small/Merc | Fuente histórica C, documentación, equipo, economía, combate | Condiciones Merc/Diku y componentes múltiples: NO copiar fuente |
| Merc C++ / documentación de clase | https://github.com/DikuMUDOmnibus/Merc-Cpp | THAC0 interpolado, HP por clase, tablas de habilidades | Derivado y licencia propia; referencia, no dependencia |
| ROM 2.4 | https://github.com/MUDOmnibus/Rom24b6 | Clases, habilidades, armas, armadura y tipos de daño | Ver `doc/rom.license` y otras licencias heredadas |
| ROM 2.4 documentación de construcción | https://github.com/avinson/rom24-quickmud/blob/master/doc/Rom2.4.doc | Cuatro AC: perforante, contundente, cortante, mágico; resistencias y vulnerabilidades | Documentación externa, no incorporar íntegra |

### Política de incorporación
- Los enlaces externos **no son copias descargadas ni archivos vendorizados**. Esta carpeta conserva resúmenes originales, índice y guías de implementación, evitando republicar material cuya licencia no esté comprobada.
- Matemáticas, procedimientos y estructuras abstractas pueden estudiarse y reimplementarse de forma independiente; **no copiar líneas de C** a Python, ni archivos de área, arte, diálogos o tablas expresivas completas sin revisión de licencia y atribución.
- Las condiciones de cada versión y distribución importan; la licencia nueva de DikuMUD no relicencia Merc/ROM automáticamente. No interpretar este informe como dictamen jurídico.
- Documentar para cada fórmula: motor y versión, ruta exacta y función original, interpretación, pseudocódigo propio, ejemplo de cálculo, diferencias VT2, pruebas y licencia comprobada.

## Orden de lectura
1. [Inventario de mecánicas](MECHANICS_CATALOG.md).
2. [Modelos matemáticos explicados](FORMULAS_AND_EXAMPLES.md).
3. [Handoff al Arquitecto y Programador](ARCHITECT_PROGRAMMER_HANDOFF.md).
4. Abrir fuentes originales para verificar cada algoritmo antes de decidir.

## Restricciones del proyecto
Leer `AGENTS.md`, `vintage-telnet-2/AGENTS.md`, `CONTENT_CONTRACT.md`, `docs/DECISIONES_VIGENTES.md`, `docs/ARCHITECTURE.md` y `review/current/KNOWN_LIMITS.md`. `server/mechanics.py` es la autoridad de matemáticas; `server/engine.py` resuelve acciones; Python/SQLite gobiernan estado. No desplegar Raspberry, tocar partidas, activar Forja canónica ni alterar economía sin contrato aprobado.

**Alcance de esta entrega:** investigación y plan de trabajo, no implementación. Issue de referencia: #655.
