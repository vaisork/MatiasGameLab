# NHAL-01 — Mapping ecológico del Camino de la Sombra Verde

**Origen:** #306 / #166 / PR #281  
**Capa:** Historiador y Constructor del Mundo  
**Región:** Bosque de Nhal — Velmora → Veyra  
**Criaturas evaluadas:** Rondamusgo / Hilaria de niebla

Este documento usa los `room_id` autoritativos actuales de `server/world.py`.

El cuerpo original de #306 contiene varios nombres que ya no coinciden con `main`. Historia no inventa esos IDs ni los fuerza sobre la ruta vigente.

No fija:
- porcentajes;
- pesos;
- densidad;
- dificultad;
- inmovilización por red;
- señales narrativas;
- encuentros scripted.

---

# Criterio ecológico

## Rondamusgo

Necesita:
- hojarasca;
- raíces;
- hongos;
- frutos caídos;
- cobertura vegetal;
- huecos de refugio.

Tolera claros pequeños y bosque menos cerrado mientras conserve cobertura cercana.

No debe aparecer como fauna ordinaria:
- dentro de Velmora;
- en terreno abierto de Veyra;
- en pasos sin vegetación/refugio.

## Hilaria de niebla

Necesita:
- raíces;
- arbustos;
- troncos caídos;
- puntos de anclaje próximos;
- cobertura;
- humedad suficiente para sostener su ambiente de bosque.

No debe poblar:
- claros demasiado abiertos;
- tramos ya muy transitados/mantenidos;
- zonas donde el dosel y los puntos de anclaje desaparecen;
- Veyra abierta.

## Rasgacorteza

**EXCLUIDO de todo pool ordinario NHAL-01.**

Sigue siendo amenaza superior regional.

---

# Mapping por room_id

| room_id | Rondamusgo | Hilaria | cobertura / red viable | lectura regional | incompatibilidad / nota |
|---|---:|---:|---|---|---|
| `sombra_borde` | no | no | cobertura sí, pero borde habitado | Nhal — borde de Velmora | Casas y referencias mantenidas; no se usa como hábitat silvestre ordinario. |
| `sombra_tronco` | no | no | tronco disponible, pero señal mantenida | Nhal | El tronco es un hito cuidado de ruta; se reserva fuera del pool ordinario. |
| `sombra_raices_cruzadas` | sí | sí | raíces abundantes / red viable | Nhal | Hábitat fuerte para ambas especies. |
| `sombra_claro_pequeno` | sí | no | cobertura periférica / red débil en el centro | Nhal | Rondamusgo puede usar bordes del claro; Hilaria pierde continuidad de anclajes. |
| `sombra_sendero_doble` | sí | sí | vegetación espesa / red viable | Nhal profundo | Dos huellas entre vegetación crean refugio y anclajes. |
| `sombra_niebla_baja` | sí | sí | humedad + cobertura / red viable | Nhal profundo | Hábitat ejemplar para ambas, especialmente Hilaria. |
| `sombra_arbol_caido` | sí | sí | tronco + raíces / red muy viable | Nhal profundo | Tronco caído y entorno adaptado ofrecen refugio fuerte y puntos de red. |
| `sombra_tres_marcas` | sí | no | cobertura existe, pero ruta señalizada | Nhal | Rondamusgo sigue siendo plausible; Hilaria no debe convertir un hito mantenido en red territorial ordinaria. |
| `sombra_claro_escucha` | sí | no | claro / cobertura periférica | Nhal | Rondamusgo puede cruzar o alimentarse en bordes; Hilaria carece de densidad de anclaje suficiente en el claro. |
| `sombra_raiz_alta` | sí | sí | raíz dominante / red viable | Nhal profundo | Hábitat fuerte para ambas especies. |
| `sombra_bosque_abierto` | sí | no | cobertura decreciente | Nhal — borde de salida | Rondamusgo aún puede usar el sotobosque; Hilaria pierde la densidad de anclajes característica. |
| `sombra_hojas_claras` | sí | no | hojarasca / cobertura decreciente | **transición Nhal → Veyra** | Rondamusgo todavía es marginalmente plausible; Hilaria deja de ser apropiada para pool ordinario. |
| `sombra_ultimas_senales` | sí | no | cobertura residual / red no fiable | transición Nhal → Veyra | Última franja donde Rondamusgo puede aparecer de forma marginal. |
| `sombra_entrada_veyra` | no | no | terreno abierto | Veyra | NHAL-01 termina aquí. |

---

# Lectura regional

## Nhal claro

Se consideran todavía parte de Nhal:
- `sombra_borde`
- `sombra_tronco`
- `sombra_raices_cruzadas`
- `sombra_claro_pequeno`
- `sombra_sendero_doble`
- `sombra_niebla_baja`
- `sombra_arbol_caido`
- `sombra_tres_marcas`
- `sombra_claro_escucha`
- `sombra_raiz_alta`

## Borde de salida

`sombra_bosque_abierto` sigue siendo Nhal, pero ya anuncia pérdida de cobertura.

## Transición Nhal → Veyra

- `sombra_hojas_claras` — comienzo claro de transición.
- `sombra_ultimas_senales` — última franja de influencia de Nhal.
- `sombra_entrada_veyra` — Veyra.

No introducir fauna de Veyra dentro de NHAL-01 sin contrato separado.

---

# Mayor afinidad ecológica

Sin fijar pesos:

## Rondamusgo
- `sombra_raices_cruzadas`
- `sombra_sendero_doble`
- `sombra_niebla_baja`
- `sombra_arbol_caido`
- `sombra_raiz_alta`

## Hilaria de niebla
- `sombra_raices_cruzadas`
- `sombra_sendero_doble`
- `sombra_niebla_baja`
- `sombra_arbol_caido`
- `sombra_raiz_alta`

Esto expresa afinidad de hábitat, no peso mecánico.

---

# Regla especial de Hilaria

La Hilaria no debe aparecer simplemente porque una sala sea "oscura".

Su presencia requiere **estructura física para red**.

Por tanto:
- niebla sola no basta;
- baja luz sola no basta;
- nombre de región Nhal solo no basta.

Debe existir combinación de raíces, troncos, arbustos u otros puntos de anclaje compatibles.

---

# Exclusiones obligatorias

No usar en NHAL-01 ordinario:
- `velmora_centro`;
- casas, espacios comunitarios y rutas internas del pueblo;
- Rasgacorteza;
- fauna de Edran, Hoshai, Korven o Lethra por conveniencia técnica;
- `sombra_entrada_veyra` y salas posteriores de Veyra.

---

# Handoff a Narrativa

Narrativa todavía debe marcar sobre los IDs vigentes:
- tranquila / presencia / territorial;
- reservas scripted;
- señales de red o presencia;
- pausas deliberadas.

Historia no fija esa capa.

---

# Handoff a Jugabilidad

Una vez exista la capa narrativa de #306, Jugabilidad puede usar la intersección:

1. especie ecológicamente admitida aquí;
2. sala no excluida por Narrativa;
3. densidad/peso definido por Jugabilidad.

Historia considera cerrada su parte de #306.

**ESTADO: HISTORIA LISTA / PENDIENTE CAPA NARRATIVA PARA NHAL-01.**
