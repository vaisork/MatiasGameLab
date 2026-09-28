# KORVEN-01 — Mapping ecológico del Camino de Piedra

**Origen:** #304 / #166 / PR #281
**Capa:** Historiador y Constructor del Mundo
**Región:** Pedrales de Korven — Brumak → Veyra
**Criaturas evaluadas:** Cascapedernal / Colagrieta

Este documento resuelve únicamente la capa de Historia pedida en #304.

No fija:
- porcentajes;
- pesos;
- densidad;
- dificultad;
- encuentros scripted;
- señales narrativas;
- números de criatura.

La capa narrativa complementaria está en PR #316.

---

## Criterio ecológico

### Cascapedernal

Puede aparecer donde existan:
- piedra expuesta;
- superficies cálidas;
- líquenes o restos vegetales;
- hendiduras pequeñas para refugio.

Tolera mejor los espacios abiertos que Colagrieta, siempre que siga habiendo piedra y refugios pequeños.

### Colagrieta

Requiere con más claridad:
- fisuras;
- grietas;
- paredes fracturadas;
- cavidades;
- cobertura inmediata para retirarse.

No debe poblar de forma ordinaria:
- patios mantenidos;
- mesetas muy abiertas;
- tramos ya claramente fuera de Korven;
- espacios donde no haya una retirada plausible hacia roca.

### Quebrarrocas

**EXCLUIDO de todo pool ordinario KORVEN-01.**

Sigue siendo amenaza superior regional.

---

# Mapping por room_id

| room_id | Cascapedernal | Colagrieta | lectura regional | incompatibilidad / nota ecológica |
|---|---:|---:|---|---|
| `piedra_patio_exterior` | no | no | Korven — borde habitado de Brumak | Patio preparado para visitantes y tránsito cotidiano; no se usa como hábitat silvestre ordinario. |
| `piedra_pared_anclajes` | sí | no | Korven | Roca expuesta compatible con Cascapedernal; no hay fisura/cavidad suficiente descrita para justificar Colagrieta. |
| `piedra_paso_corto` | sí | sí | Korven | Paso entre paredes de piedra: refugio y bordes compatibles con ambas especies. |
| `piedra_patio_abierto` | sí | no | Korven | Sigue siendo terreno pétreo, pero el espacio abierto reduce la cobertura que necesita Colagrieta. |
| `piedra_primer_monton` | sí | no | Korven | Los montones y piedra expuesta permiten Cascapedernal; Colagrieta no tiene una fisura natural claramente establecida. |
| `piedra_hendiduras` | sí | sí | Korven profundo | Hábitat ejemplar para ambas; las hendiduras favorecen especialmente a Colagrieta. |
| `piedra_pared_partida` | sí | sí | Korven | La pared fracturada ofrece superficie para Cascapedernal y retirada inmediata para Colagrieta. |
| `piedra_abrigo_viento` | sí | no | Korven | Hondonada rocosa compatible con Cascapedernal; el uso frecuente como pausa de viajeros hace poco apropiado convertirla en hábitat ordinario de Colagrieta. |
| `piedra_meseta_baja` | sí | no | Korven | Meseta rocosa abierta: Cascapedernal sí; falta cobertura inmediata para Colagrieta. |
| `piedra_cruce_montones` | sí | no | Korven | Piedra y pequeños huecos permiten Cascapedernal; el cruce transitado y abierto no favorece Colagrieta. |
| `piedra_cavidades` | sí | sí | Korven | Cavidades superficiales constituyen hábitat directo para ambas especies, especialmente Colagrieta. |
| `piedra_clara` | sí | no | Korven | El cambio de color no cambia por sí solo el sustrato rocoso; Cascapedernal sigue siendo plausible. No se establece fisura suficiente para Colagrieta. |
| `piedra_ultimo_corredor` | sí | sí | Korven — borde de salida | Las paredes todavía forman corredor y refugio. Ambas siguen siendo plausibles antes de abandonar los Pedrales. |
| `piedra_suelo_quebrado` | sí | no | **transición Korven → Veyra** | Última franja de piedra rota compatible con Cascapedernal; el terreno ya se abre demasiado para la ecología ordinaria de Colagrieta. |

---

# Lectura regional

## Korven pleno

Se consideran todavía parte clara de los Pedrales de Korven:

- `piedra_patio_exterior`
- `piedra_pared_anclajes`
- `piedra_paso_corto`
- `piedra_patio_abierto`
- `piedra_primer_monton`
- `piedra_hendiduras`
- `piedra_pared_partida`
- `piedra_abrigo_viento`
- `piedra_meseta_baja`
- `piedra_cruce_montones`
- `piedra_cavidades`
- `piedra_clara`

## Borde de salida de Korven

`piedra_ultimo_corredor` sigue siendo Korven, pero funciona como el último corredor rocoso reconocible antes de que el terreno cambie.

## Transición a Veyra

`piedra_suelo_quebrado` es la primera sala de la lista que debe leerse ya como transición.

La piedra fracturada todavía permite una presencia marginal de Cascapedernal, pero no debe introducir fauna nueva de Veyra dentro de KORVEN-01 sin contrato separado.

---

# Compatibilidad con la capa del Narrador — PR #316

Historia revisó la tabla narrativa ya entregada.

No hay contradicción.

Las cuatro salas que Narrativa reserva como tranquilas/excluidas pueden permanecer fuera del pool aunque el hábitat físico permitiría fauna en algunas de ellas:

- `piedra_patio_exterior` — Historia también la excluye.
- `piedra_primer_monton` — ecológicamente Cascapedernal sería posible, pero Narrativa la reserva como hito de orientación.
- `piedra_abrigo_viento` — ecológicamente Cascapedernal sería posible, pero Narrativa la reserva como pausa.
- `piedra_clara` — ecológicamente Cascapedernal sería posible, pero Narrativa la reserva como marcador de progreso.

Por tanto, Jugabilidad debe tomar la **intersección**:
1. especie ecológicamente admitida por Historia;
2. sala no reservada/excluida por Narrativa;
3. densidad/peso definido por Jugabilidad.

---

# Salas de mayor afinidad ecológica

Sin fijar peso mecánico, Historia identifica como ejemplos más fuertes del hábitat:

### Cascapedernal
- `piedra_hendiduras`
- `piedra_pared_partida`
- `piedra_cavidades`
- `piedra_meseta_baja`

### Colagrieta
- `piedra_hendiduras`
- `piedra_pared_partida`
- `piedra_cavidades`
- `piedra_ultimo_corredor`

Esto **no es una tabla de pesos**. Solo indica compatibilidad ecológica especialmente clara.

---

# Exclusiones obligatorias

No usar en KORVEN-01 ordinario:
- `brumak_centro`;
- forja, mercado, interiores o salas comunitarias de Brumak;
- cualquier sala de otra región;
- Quebrarrocas;
- fauna de Hoshai, Edran, Lethra o Nhal por conveniencia técnica.

---

# Handoff a Jugabilidad

Historia da por cerrada su parte de #304.

Jugabilidad puede combinar esta tabla con PR #316 para decidir:
- salas realmente elegibles;
- densidad;
- pesos Cascapedernal/Colagrieta;
- exclusiones finales;
- tests de KORVEN-01.

**ESTADO: LISTO PARA KORVEN-01.**
