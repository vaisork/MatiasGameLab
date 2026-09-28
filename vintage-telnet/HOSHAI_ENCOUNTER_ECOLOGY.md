# Vintage Telnet — Mapping ecológico Hoshai / Camino Alto

**Responsable:** Historiador y Constructor del Mundo  
**Origen:** Issue #289 / #166  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Alcance:** compatibilidad ecológica de Uñapiedra y Saltacresta sobre las salas vigentes del Camino Alto.

No fija porcentajes, pesos, dificultad, XP ni balance.

| room_id | Uñapiedra | Saltacresta | regional_habitat | microhábitat | restricción ecológica |
| --- | --- | --- | --- | --- | --- |
| `alto_terrazas` | no | no | no | borde habitado / terrazas de Khariel | Espacio cotidiano inmediato del pueblo; aunque exista roca y vegetación, no usar pool silvestre ordinario. |
| `alto_mirador` | no | no | no | mirador mantenido / hito de orientación | Punto de observación conocido y transitado; conservar como pausa sin fauna ordinaria. |
| `alto_anclajes` | sí | no | sí | roca trabajada, huecos y bordes pétreos | Uñapiedra puede aprovechar roca y anclajes abandonados; falta alimento/cobertura vegetal suficiente para Saltacresta. |
| `alto_escalones` | sí | sí | sí | escalones de roca / sendero serrano | Uñapiedra usa salientes; Saltacresta solo donde haya brotes laterales y espacio real de salto/escape. |
| `alto_terraza_abandonada` | sí | sí | sí | terraza mixta abandonada | La pérdida de uso cotidiano permite refugio y brotes; ambas son compatibles sin volver la terraza una guarida fija. |
| `alto_garganta` | sí | no | sí | garganta / roca / grieta | Contexto prioritario de Uñapiedra. Saltacresta no encaja en el paso estrecho por falta de vegetación y escape lateral suficiente. |
| `alto_cruce_alturas` | sí | sí | sí | cruce de alturas / sendero serrano | Ambas compatibles si existen roca de refugio y bordes vegetados; no asumir grupo de Saltacrestas. |
| `alto_puente_viento` | no | no | no | puente expuesto / estructura de tránsito | Exposición y tránsito alto; además Narrativa lo reserva como landmark limpio. |
| `alto_pinar` | no | sí | sí | vegetación de montaña / suelo blando | Favorece Saltacresta por alimento, cobertura y salto. Uñapiedra queda fuera si la roca expuesta deja de dominar. |
| `alto_descenso` | sí | sí | sí | ladera mixta / roca y vegetación dispersa | Ambas compatibles; Uñapiedra en piedra y Saltacresta en bordes vegetados, sin mezclar hábitats de forma artificial. |
| `alto_agua_fria` | no | no | no | corriente fría / pausa de viajeros | El agua cercana podría admitir Saltacresta en otro contexto, pero esta sala queda deliberadamente sin fauna ordinaria por función de respiro. |
| `alto_ultimo_risco` | sí | sí | sí | risco / repisa / vegetación dispersa | Uñapiedra favorecida por roca; Saltacresta solo en sectores con brotes y salida por salto. |
| `alto_camino_falda` | sí | sí | sí | sendero serrano de transición | Ambas pueden aparecer de forma ocasional mientras aún exista roca/refugio y vegetación de altura; la presión debe bajar al acercarse a Veyra. |

## Reglas de consumo

- `regional_habitat=no` implica **0%** de pool regional ordinario.
- Rasgacumbres permanece **fuera de todos los pools ordinarios**.
- Si Narrativa reserva una sala como pausa deliberada, esa reserva prevalece aunque el entorno físico pudiera sostener fauna.
- La compatibilidad de Saltacresta presupone espacio real de salto/escape y algo de vegetación; no aparece en roca desnuda o pasos cerrados.
- La compatibilidad de Uñapiedra presupone roca/refugio inmediato; no se traslada a suelo blando o vegetación dominante solo porque siga dentro de Hoshai.

## Handoff directo a Jugabilidad

Con esta tabla, HOSHAI-01 puede consumir las reglas ya fijadas en #289:
- solo Uñapiedra → 100/0;
- solo Saltacresta → 0/100;
- ambas en roca/grieta/repisa/garganta → 75/25;
- ambas en terraza mixta/sendero/cruce → 50/50;
- ambas en vegetación/agua/espacio claro de salto → 30/70.

Historia no añade ni modifica porcentajes.

## Estado

**HISTORIA DE #289 COMPLETA.**
