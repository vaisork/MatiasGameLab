# Vintage Telnet — Contexto visual persistente por zona

**Responsable:** Historiador y Constructor del Mundo — Vintage Telnet  
**Origen:** Issues #87 y #92  
**Consumidor principal:** #89

Este documento define un contrato de **presentación canónica**, no una mecánica ni una topología nueva. Su objetivo es permitir que la interfaz conserve una identidad visual estable mientras el jugador permanece dentro de una misma macro-zona, sin deducir contexto leyendo prosa o prefijos de IDs.

## Principios

- `visual_context_id` debe llegar como dato estructurado/autoritativo; Frontend no debe inferirlo a partir del nombre o descripción de una sala.
- Compartir contexto visual significa únicamente que varias salas pertenecen a una misma identidad territorial/presentacional. No vuelve equivalentes las salas ni modifica salidas, encuentros o descubrimientos.
- Un asset solo puede mostrarse si ya está aprobado por el flujo de Arte. Este documento no aprueba imágenes nuevas.
- Una ilustración de pueblo puede acompañar sus micro-salas internas como identidad persistente del asentamiento aunque la escena concreta sea mercado, taller o sendero interno; no debe interpretarse como representación literal de cada objeto visible en esa sala.
- Al abandonar claramente un asentamiento hacia campo/camino, debe cambiar el contexto aunque todavía se esté en la misma región cultural.
- No mostrar mediante imagen, nombre o texto un destino, criatura, ruina o ruta que el personaje todavía no haya descubierto.

## Contextos actuales

| visual_context_id | nombre visible aprobado | alcance canónico | asset canónico permitido actualmente |
| --- | --- | --- | --- |
| `zone.vaisgard` | **Vaisgard** | Ciudad de Vaisgard y sus salas urbanas presentes/futuras mientras sigan dentro de la ciudad | `assets/vintage-telnet/locations/vaisgard.webp` |
| `zone.valdren` | **Valdren** | Centro y micro-salas internas del pueblo de Valdren | `assets/vintage-telnet/locations/valdren.webp` |
| `zone.edran.valdren_outskirts` | **Alrededores de Valdren** | Salida del pueblo, parcelas, cercas y camino inmediato de la microaventura *El lindero roto* dentro de los Llanos de Edran | ninguno aprobado todavía |
| `zone.veyra.road` | **Caminos de la Cuenca de Veyra** | Tramos técnicos actuales de camino entre asentamientos que no están dentro de un pueblo ni forman parte de la salida inmediata de Valdren | ninguno aprobado todavía |
| `zone.khariel` | **Khariel** | Centro y micro-salas internas de Khariel | ninguno aprobado en runtime todavía |
| `zone.brumak` | **Brumak** | Centro y micro-salas internas de Brumak | ninguno aprobado en runtime todavía |
| `zone.narevia` | **Narevia** | Centro y micro-salas internas de Narevia | ninguno aprobado en runtime todavía |
| `zone.velmora` | **Velmora** | Centro y micro-salas internas de Velmora | ninguno aprobado en runtime todavía |

Los últimos cuatro IDs quedan definidos para que el contrato no tenga que cambiar cuando sus assets aprobados entren al runtime. Mientras no exista asset aprobado, la interfaz debe funcionar sin imagen o con un tratamiento neutro que no invente cultura visual.

## Mapeo de las salas actuales

| room_id | visual_context_id | nombre visible | asset permitido |
| --- | --- | --- | --- |
| `vaisgard` | `zone.vaisgard` | Vaisgard | `vaisgard.webp` |
| `valdren_centro` | `zone.valdren` | Valdren | `valdren.webp` |
| `valdren_forja` | `zone.valdren` | Valdren | `valdren.webp` |
| `valdren_mercado` | `zone.valdren` | Valdren | `valdren.webp` |
| `valdren_sendero` | `zone.edran.valdren_outskirts` | Alrededores de Valdren | ninguno |
| `valdren_camino_parcela` | `zone.edran.valdren_outskirts` | Alrededores de Valdren | ninguno |
| `valdren_camino_cerca` | `zone.edran.valdren_outskirts` | Alrededores de Valdren | ninguno |
| `valdren_camino_lindero` | `zone.edran.valdren_outskirts` | Alrededores de Valdren | ninguno |
| `road_north` | `zone.veyra.road` | Caminos de la Cuenca de Veyra | ninguno |
| `road_west` | `zone.veyra.road` | Caminos de la Cuenca de Veyra | ninguno |
| `khariel_centro` | `zone.khariel` | Khariel | ninguno en runtime |
| `khariel_forja` | `zone.khariel` | Khariel | ninguno en runtime |
| `khariel_mercado` | `zone.khariel` | Khariel | ninguno en runtime |
| `khariel_sendero` | `zone.khariel` | Khariel | ninguno en runtime |
| `brumak_centro` | `zone.brumak` | Brumak | ninguno en runtime |
| `brumak_forja` | `zone.brumak` | Brumak | ninguno en runtime |
| `brumak_mercado` | `zone.brumak` | Brumak | ninguno en runtime |
| `brumak_sendero` | `zone.brumak` | Brumak | ninguno en runtime |
| `narevia_centro` | `zone.narevia` | Narevia | ninguno en runtime |
| `narevia_forja` | `zone.narevia` | Narevia | ninguno en runtime |
| `narevia_mercado` | `zone.narevia` | Narevia | ninguno en runtime |
| `velmora_centro` | `zone.velmora` | Velmora | ninguno en runtime |
| `velmora_forja` | `zone.velmora` | Velmora | ninguno en runtime |
| `velmora_mercado` | `zone.velmora` | Velmora | ninguno en runtime |
| `velmora_sendero` | `zone.velmora` | Velmora | ninguno en runtime |

### Nota sobre salas generadas

`world.py` genera micro-salas internas según direcciones libres; si una de las filas anteriores no existe en una versión concreta del runtime, simplemente se ignora. Cualquier nueva micro-sala **claramente interna** de uno de los cinco pueblos hereda el `zone.<pueblo>` correspondiente hasta que Historia defina una excepción.

## Frontera Valdren → alrededores

La frontera presentacional se fija al salir del núcleo cotidiano del pueblo hacia la apertura de *El lindero roto*:

- `valdren_centro`, forja y mercado siguen siendo **Valdren**;
- `valdren_sendero` ya describe las últimas casas a la espalda y el camino entre parcelas, por lo que pertenece a **Alrededores de Valdren**;
- parcela, cerca y lindero conservan ese mismo contexto visual: son una sola salida rural continua y no necesitan una imagen distinta por micro-sala;
- el contexto termina cuando una ruta futura abandone inequívocamente este entorno inmediato. Este documento no inventa todavía cuál será esa sala.

Esto evita dos errores: mantener la ilustración del pueblo cuando el texto ya sitúa al jugador fuera de sus últimas casas, o cambiar de imagen cuatro veces durante una misma salida rural.

## Textos consumibles

| context_id | texto visible aprobado |
| --- | --- |
| `visual.zone.vaisgard` | **Vaisgard** — Ciudad principal del mundo conocido, levantada en capas dentro de la Cuenca de Veyra. |
| `visual.zone.valdren` | **Valdren** — Pueblo abierto de caminos de tierra, madera, piedra y pequeñas parcelas en los Llanos de Edran. |
| `visual.zone.edran.valdren_outskirts` | **Alrededores de Valdren** — Parcelas, cercas bajas y caminos de tierra marcan la transición entre el pueblo y los Llanos de Edran. |
| `visual.zone.veyra.road` | **Caminos de la Cuenca de Veyra** — Rutas transitadas conectan Vaisgard con los asentamientos del territorio conocido. |
| `visual.zone.khariel` | **Khariel** — Asentamiento Felaryn entre terrazas naturales, roca y distintos niveles de la Sierra de Hoshai. |
| `visual.zone.brumak` | **Brumak** — Asentamiento Dravak compacto entre roca y espacios protegidos del viento en los Pedrales de Korven. |
| `visual.zone.narevia` | **Narevia** — Pueblo Marevyn organizado alrededor de agua dulce, canales, vegetación e islas pequeñas en las Aguas de Lethra. |
| `visual.zone.velmora` | **Velmora** — Pueblo Vesperi dentro del Bosque de Nhal, unido por senderos y señales discretas bajo luz reducida. |

## Límites de revelación

1. El `visual_context_id` activo describe **dónde está** el personaje, no hacia dónde conduce una salida no recorrida.
2. Un mapa o control no debe usar estos IDs para revelar contextos vecinos antes de que el servidor los marque como descubiertos.
3. `zone.edran.valdren_outskirts` no revela por sí mismo *El lindero roto*, Mordelindes, Espinajos ni ninguna criatura mayor.
4. `zone.veyra.road` es deliberadamente genérico para los tramos técnicos actuales. No debe utilizarse para afirmar que esos `room_id` representan fielmente la orientación geográfica definitiva de `REGIONS.md`; `world.py` declara que la topología cardinal v1 es técnica.
5. La ilustración de Valdren **no** debe reutilizarse como si representara literalmente el lindero, una parcela concreta o una criatura. Si Frontend necesita mantener continuidad visual fuera del pueblo antes de que exista arte de alrededores, debe usar tratamiento neutro/ambiental sin inventar un asset.
6. Cuando entren al runtime los assets aprobados de Khariel, Brumak, Narevia o Velmora, Arte/Frontend puede asociarlos al ID ya definido sin cambiar este canon, siempre que conserve el flujo de aprobación de assets.

## Handoff

- **#89 / Frontend:** consumir `visual_context_id` estructurado y mantener el contexto mientras no cambie de macro-zona; no parsear `room_id` ni narración.
- **Servidor:** si decide exponer este contrato, el mapeo anterior es la fuente de presentación; Historia no solicita aquí cambios de backend mientras siga congelado por #89.
- **Director de Arte:** los contextos sin asset son necesidades visuales posibles, no solicitudes automáticas ni autorización para producir arte.

**Estado:** ENTREGA CANÓNICA CONSUMIBLE — Issues #87/#92.
