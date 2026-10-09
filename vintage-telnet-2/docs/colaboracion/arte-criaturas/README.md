# Encargos de arte: fauna menor de Lethra y Nhal

Origen: bestiario del historiador (PR #669), ya integrado en el juego.

`SOLICITUDES_CRIATURAS.json` tiene 36 encargos de tipo `creature`, generados a partir de los datos reales del juego:
- **16 fichas de bestiario** para las especies nuevas, en `client/art/bestiary/{id}-anime-v1.webp` (1536×1024).
- **20 imágenes de ambiente** (encuentro en su hábitat), una por especie, en `client/art/encounters/{id}-anime-v1.webp` (1536×1024).

Cada encargo incluye anatomía y conducta, presagio, escala, materiales visibles, salas de referencia, paleta regional, restricciones y un borrador de prompt en el formato de `prompts.json`.

Reglas:
- Pinzajunco, Saltalodo, Rondamusgo e Hilaria de niebla conservan su ficha aprobada (`conservar_ficha`) y sólo piden ambiente.
- No se generaron imágenes en esta integración.
- El juego funciona sin ellas: las especies nuevas aparecen en el bestiario sin ilustración hasta que se entreguen. Para integrarlas, añadir `illustration` a la criatura en `content/world.json`, como en las fichas existentes.
- Dorsalodo y Rasgacorteza (fauna mayor) quedan fuera de este encargo.
