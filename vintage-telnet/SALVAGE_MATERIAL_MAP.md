# Vintage Telnet — Mapping final de materiales de salvage C1

**Origen:** #500 / #482  
**Responsable:** Historiador y Constructor del Mundo  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Objetivo:** convertir las alternativas plausibles de #482 en exactamente un material v1 por familia C1, con clave estable consumible por Desarrollo.

No cambia:
- frecuencia de drop;
- cantidad;
- valor por referencia;
- antifarmeo;
- venta;
- economía;
- crafting.

Jugabilidad ya fija ref1 = 3 sellos y ref2 = 4 sellos.

| family | item_key | material_label | referencia | compatibilidad canónica |
| --- | --- | --- | ---: | --- |
| `mordelinde` | `salvage_mordelinde_piel` | Retazo de piel de Mordelinde | 1 | Selecciona la opción de piel curtible ya aprobada; no usa diente como drop v1. |
| `espinajo_rastrojo` | `salvage_espinajo_pua` | Púa rígida de Espinajo | 2 | Selecciona las púas aprovechables ya aprobadas; evita convertirlo en fuente genérica de cuero. |
| `unapiedra` | `salvage_unapiedra_escama` | Escama gruesa de Uñapiedra | 1 | Usa escamas recuperables ya aprobadas; no crea cristal/mineral. |
| `saltacresta` | `salvage_saltacresta_fibra` | Fibra resistente de Saltacresta | 2 | Usa pelo/fibra resistente ya aprobado; no añade escamas ni caparazón. |
| `cascapedernal` | `salvage_cascapedernal_caparazon` | Fragmento de caparazón de Cascapedernal | 1 | Material orgánico duro ya aprobado; no piedra, metal ni gema. |
| `colagrieta` | `salvage_colagrieta_piel` | Retazo de piel de Colagrieta | 2 | Selecciona la piel flexible ya aprobada; no usa placa mineral. |
| `pinzajunco` | `salvage_pinzajunco_caparazon` | Segmento de caparazón de Pinzajunco | 1 | Usa caparazón limpio ya aprobado; no piel ni gema. |
| `saltalodo` | `salvage_saltalodo_membrana` | Membrana resistente de Saltalodo | 2 | Usa membrana/piel resistente ya aprobada; etiqueta v1 evita tratarlo como cuero común. |
| `rondamusgo` | `salvage_rondamusgo_fibra` | Fibra áspera de Rondamusgo | 1 | Usa pelo/fibra limpia; semillas/hojas adheridas no son loot. |
| `hilaria_niebla` | `salvage_hilaria_seda` | Seda de Hilaria de niebla | 2 | Usa seda recuperable de red ya aprobada; no veneno automático. |
| `garralaja` | `salvage_garralaja_piel` | Tira de piel escamada de Garralaja | 1 | Selecciona piel escamada ya aprobada; no piedra/cristal/metal. |
| `cavapolvo` | `salvage_cavapolvo_placa` | Placa dérmica de Cavapolvo | 2 | Usa placa dérmica menor ya aprobada; no mineral extraído del cuerpo. |
| `remojunco` | `salvage_remojunco_placa` | Placa córnea de Remojunco | 1 | Usa únicamente tegumento/placa propia del animal; los juncos del refugio no cuentan como loot. |
| `velacauce` | `salvage_velacauce_membrana` | Membrana flexible de Velacauce | 2 | Usa piel/membrana flexible ya aprobada; no cuerno ni metal. |
| `silbarisco` | `salvage_silbarisco_fibra` | Fibra superficial de Silbarisco | 1 | Elige la opción neutra ya permitida; no presupone plumas definitivas ni crea objeto sonoro mágico. |

## Regla v1

Cada familia C1 usa **un solo item_key** de salvage.

No se elige aleatoriamente entre materiales alternativos.

La variedad futura de materiales requiere un contrato posterior y no debe aparecer por inferencia en Desarrollo.

## Compra

El comprador v1 sigue siendo:

**Puesto de acopio del Mercado de Valdren**  
room_id: `valdren_mercado`

Daro no compra estos materiales como regla general.

## Estado

**HISTORIA #500 COMPLETA.**

La tabla ya es inequívoca para implementación.
