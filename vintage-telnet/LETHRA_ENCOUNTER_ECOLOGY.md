# LETHRA-01 — Mapping ecológico del Camino de los Juncos

**Origen:** #305 / #166 / PR #281
**Capa:** Historiador y Constructor del Mundo
**Región:** Aguas de Lethra — Narevia → Veyra
**Criaturas evaluadas:** Pinzajunco / Saltalodo

Este documento usa los `room_id` autoritativos de `server/world.py` en `main`.

El cuerpo original de #305 contiene varios IDs desactualizados. Historia no los reutiliza ni los recrea.

No fija:
- porcentajes;
- pesos;
- densidad;
- dificultad;
- mecánicas acuáticas;
- señales narrativas;
- encuentros scripted.

La capa narrativa complementaria está en PR #320.

---

# Criterio ecológico

## Pinzajunco

Necesita:
- agua dulce poco profunda;
- orilla;
- barro;
- raíces o juncos;
- refugio cercano.

No debe aparecer en:
- pasarelas secas sin borde accesible;
- suelo firme lejos del agua;
- canales claramente profundos sin orilla útil;
- espacios comunitarios de Narevia.

## Saltalodo

Tolera mejor:
- charcas;
- barro;
- hojas flotantes;
- bordes de canal;
- zonas húmedas con insectos;
- agua somera o ribera utilizable.

No debe aparecer de forma ordinaria en:
- suelo seco;
- pasarelas sin acceso inmediato al agua;
- zonas urbanizadas;
- transición ya dominada por Veyra.

## Dorsalodo

**EXCLUIDO de todo pool ordinario LETHRA-01.**

Sigue siendo amenaza superior regional.

---

# Mapping por room_id

| room_id | Pinzajunco | Saltalodo | tipo de hábitat | lectura regional | incompatibilidad / nota |
|---|---:|---:|---|---|---|
| `juncos_plataformas` | no | no | plataforma habitada / borde de agua | Lethra — borde de Narevia | Espacio todavía ligado a uso cotidiano del pueblo; no se usa como hábitat silvestre ordinario. |
| `juncos_postes` | sí | no | orilla / agua somera señalizada | Lethra | El borde acuático permite Pinzajunco; no hay barro/charca suficiente descrito para Saltalodo. |
| `juncos_pasarela_antigua` | no | no | pasarela / estructura histórica | Lethra | La función principal es lectura histórica del camino; la propia pasarela no constituye hábitat. |
| `juncos_isla_refugio` | no | no | isla-refugio | Lethra | Espacio de refugio y uso humano estacional; se preserva fuera del pool ordinario. |
| `juncos_juncal` | sí | sí | juncal / orilla / barro | Lethra profundo | Hábitat directo para ambas especies. |
| `juncos_paso_raices` | sí | sí | raíces / barro / sendero elevado | Lethra profundo | Raíces, vegetación y barro ofrecen refugio y territorio para ambas. |
| `juncos_embarcadero` | no | no | embarcadero / orilla intervenida | Lethra | Landmark de tránsito; no se usa como hábitat ordinario aunque exista agua alrededor. |
| `juncos_agua_entre_caminos` | sí | sí | canal somero / barro / interrupción de camino | Lethra profundo | El agua invade el tránsito terrestre; ambas especies son compatibles. |
| `juncos_pasarela_larga` | no | sí | pasarela sobre agua | Lethra profundo | Falta orilla/raíz/junco cercano para Pinzajunco; Saltalodo puede aparecer desde el agua y retirarse a ella. |
| `juncos_islas_bajas` | sí | sí | islas bajas / orillas / barro | Lethra profundo | Múltiples bordes de agua y terreno húmedo: hábitat fuerte para ambas. |
| `juncos_canal_ancho` | sí | sí | canal con borde transitable | Lethra profundo | El jugador bordea el canal: sus márgenes siguen siendo utilizables por ambas especies. |
| `juncos_ultimos` | sí | sí | juncal denso / humedal | Lethra — borde de salida | Sigue siendo hábitat pleno aunque marque el final del corazón de Lethra. |
| `juncos_suelo_firme` | no | no | seco / camino de tierra | **transición Lethra → Veyra** | Primera ruptura clara con el humedal; no mantener fauna acuática por inercia. |
| `juncos_corrientes` | sí | no | pequeños canales junto a camino firme | transición Lethra → Veyra | Pinzajunco aún es marginalmente plausible en bordes someros; Saltalodo ya pierde el hábitat continuo que necesita. |
| `juncos_entrada_veyra` | no | no | camino abierto / huellas de viajeros | Veyra | La ruta ya entra en Veyra; LETHRA-01 no debe seguir poblando aquí. |

---

# Lectura regional

## Lethra claro

Se mantienen como Lethra:
- `juncos_plataformas`
- `juncos_postes`
- `juncos_pasarela_antigua`
- `juncos_isla_refugio`
- `juncos_juncal`
- `juncos_paso_raices`
- `juncos_embarcadero`
- `juncos_agua_entre_caminos`
- `juncos_pasarela_larga`
- `juncos_islas_bajas`
- `juncos_canal_ancho`
- `juncos_ultimos`

## Transición Lethra → Veyra

- `juncos_suelo_firme` — comienzo claro de transición.
- `juncos_corrientes` — transición todavía influida por pequeños canales.
- `juncos_entrada_veyra` — Veyra.

No introducir fauna nueva de Veyra dentro de LETHRA-01 sin contrato separado.

---

# Compatibilidad con Narrativa — PR #320

Historia revisó la capa narrativa y no detecta contradicción.

Las salas que Narrativa reserva como tranquilas/excluidas deben permanecer fuera del pool aunque físicamente tengan agua cerca:

- `juncos_plataformas`
- `juncos_pasarela_antigua`
- `juncos_isla_refugio`
- `juncos_embarcadero`
- `juncos_suelo_firme`
- `juncos_entrada_veyra`

Jugabilidad debe usar la intersección:

1. especie admitida por Historia;
2. sala no excluida por Narrativa;
3. densidad/peso definido por Jugabilidad.

---

# Mayor afinidad ecológica

Sin fijar pesos:

## Pinzajunco
- `juncos_juncal`
- `juncos_paso_raices`
- `juncos_agua_entre_caminos`
- `juncos_islas_bajas`
- `juncos_canal_ancho`

## Saltalodo
- `juncos_juncal`
- `juncos_paso_raices`
- `juncos_agua_entre_caminos`
- `juncos_islas_bajas`
- `juncos_ultimos`

Esto expresa afinidad de hábitat, no peso mecánico.

---

# Exclusiones obligatorias

No usar en LETHRA-01 ordinario:
- `narevia_centro`;
- plataformas interiores/comunitarias;
- mercado, forja o espacios residenciales;
- Dorsalodo;
- fauna de Edran, Hoshai, Korven o Nhal por conveniencia técnica;
- salas ya plenamente de Veyra.

---

# Handoff a Jugabilidad

Historia considera cerrada su capa de #305.

Jugabilidad puede combinar este documento con PR #320 para cerrar:
- salas elegibles;
- densidad;
- pesos Pinzajunco/Saltalodo;
- exclusiones;
- tests de LETHRA-01.

**ESTADO: LISTO PARA LETHRA-01.**
