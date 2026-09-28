# Vintage Telnet — KORVEN-WEAPON-01

Origen: #288
Responsable: Narrador

## Escena: La carga que no asienta

En un espacio cotidiano de trabajo de Brumak, una carga quedó mal asentada sobre su apoyo. No es una emergencia: ocupa el paso y necesita dos personas para corregirse.

Presentación:
> Una carga descansa torcida sobre su apoyo. No parece a punto de caer, pero ocupa más espacio del debido.

Petición:
> —Sostén ese extremo. Yo corrijo el apoyo. Si queda firme, podremos moverla.

Cualquier especie y clase puede colaborar. No requiere capacidad racial.

## Hito

`korven_trabajo_ayudado`

Se completa cuando el jugador acepta ayudar y deja la carga estable y el tránsito libre. No requiere combate ni puzzle.

Resolución:
> El apoyo vuelve a quedar bajo el peso correcto. La carga queda estable y el paso vuelve a estar libre.

Reconocimiento:
> —Así está bien. Una herramienta sirve más cuando quien la lleva sabe cuándo hacer fuerza y cuándo sostener.

## Recompensa

Hito once-per-character:

`korven_martillo_recibido`

Texto:
> Te entregan un Martillo de Korven. La pieza es tuya, pero todavía necesita validación de Forja antes de poder equiparse.

La pieza entra al inventario, no se autoequipa y conserva `forge_validated=false` según #288.

En revisitas no se entrega otra copia.

## Límites

Sin tienda, dinero, crafting, drop de fauna, requisito Dravak, requisito de clase o nivel, propiedades nuevas ni auto-validación de Forja.

La escena ocurre en `brumak_forja`, sala existente de Brumak dedicada a fabricar y reparar armas y herramientas. El actor funcional queda vinculado a `brumak_taller_korven_01` (Karn), ya usado por la implementación de PR #441. La ficha de NPC debe conservar el contrato del Creador de NPCs; Narrativa no añade biografía ni canon fuera de esta función.

Estados persistentes:
- `korven_trabajo_ayudado`
- `korven_martillo_recibido`

La implementación pesada respeta el orden indicado en #288 respecto de HOSHAI-WEAPON-01.

## Contrato final de integración

- room_id: `brumak_forja`
- actor: `brumak_taller_korven_01` (Karn)
- ayuda completada: `korven_trabajo_ayudado`
- recompensa: `korven_martillo_recibido`
- item: `martillo_korven`
- estado inicial: `forge_validated=false`

El nombre `korven_carga_asentada` de la primera versión narrativa queda retirado. Jugabilidad fijó `korven_trabajo_ayudado` como identificador autoritativo.
