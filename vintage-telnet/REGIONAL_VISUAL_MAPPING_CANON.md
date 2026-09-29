# Vintage Telnet — Mapping canónico de paisajes regionales aprobados

**Responsable:** Historiador y Constructor del Mundo  
**Origen:** #203, #215, #487 / cola #374  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Objetivo:** cerrar tres huecos de mapping entre arte aprobado y salas ya existentes, sin crear geografía nueva.

Este documento valida **compatibilidad regional**. Desarrollo/Integración sigue siendo responsable de conectar los assets al runtime.

---

# 1. Hoshai — paso alto interior

Asset aprobado:
`assets/vintage-telnet/locations/hoshai-paso-alto.webp`

## Salas compatibles

### `alto_escalones`
**Sí.**

Razón:
- cambios de nivel;
- roca próxima;
- viento dominante;
- lectura de paso interior.

### `alto_garganta`
**Sí.**

Razón:
- paso estrecho entre paredes;
- horizonte reducido;
- roca cercana;
- lectura peatonal interior de sierra.

### `alto_cruce_alturas`
**Sí.**

Razón:
- desnivel;
- trazado que rodea roca;
- continuidad de paso alto;
- el asset puede funcionar como fondo persistente sin inventar estructura nueva.

## Salas que NO deben usarlo

- `alto_terrazas` — demasiado pegada a Khariel/habitable.
- `alto_mirador` — función panorámica distinta.
- `alto_puente_viento` — requiere puente protagonista.
- `alto_pinar` — vegetación domina más.
- `alto_agua_fria` — necesita corriente visible.
- `alto_cuenca_norte` y posteriores — ya son transición a Veyra.

**Mapping canónico recomendado:**  
`alto_escalones`, `alto_garganta`, `alto_cruce_alturas`.

---

# 2. Lethra — canal bajo entre islas

Asset aprobado:
`assets/vintage-telnet/locations/lethra-canal-bajo-islas.webp`

## Salas compatibles

### `juncos_agua_entre_caminos`
**Sí.**

Razón:
- agua interrumpe camino terrestre;
- navegación visual entre pasos;
- horizonte corto.

### `juncos_islas_bajas`
**Sí — principal.**

Razón:
- coincide directamente con islas pequeñas;
- agua dulce;
- lectura interior de Lethra;
- no requiere Narevia visible.

### `juncos_canal_ancho`
**Sí.**

Razón:
- agua protagonista;
- recorrido lateral alrededor de canal;
- compatible con raíces y vegetación anfibia.

## Compatibilidad condicional

### `juncos_paso_raices`
**Condicional.**

Puede usar el asset solo si el recorte mantiene legible el sendero elevado/raíces.  
No usarlo si la imagen hace parecer que el jugador debe nadar.

## Salas que NO deben usarlo

- `juncos_plataformas` — demasiado asociado a Narevia.
- `juncos_postes` — necesita postes/marcas de agua.
- `juncos_pasarela_antigua` — pasarela histórica es el foco.
- `juncos_embarcadero` — embarcadero debe ser legible.
- `juncos_pasarela_larga` — pasarela larga domina la escena.
- `juncos_suelo_firme` y posteriores — ya salieron del corazón acuático de Lethra.

**Mapping canónico recomendado:**  
`juncos_agua_entre_caminos`, `juncos_islas_bajas`, `juncos_canal_ancho`.

---

# 3. Veyra — terrazas de piedra

Asset aprobado:
`assets/vintage-telnet/locations/veyra-terrazas-piedra.webp`

## Sala principal compatible

### `campos_colinas` — Primeras colinas de Veyra
**Sí — mapping principal.**

Razón:
- primera pérdida clara del horizonte llano de Edran;
- ya es Veyra por `get_room_region()`;
- ladera baja y terrazas de piedra son compatibles con terreno ondulado;
- no requiere Vaisgard visible;
- no contradice el camino principal: el asset puede representar el entorno lateral de la sala.

## Compatibilidad secundaria

### `campos_mojon`
**No como mapping principal.**

Aunque el terreno empieza a ondular, el mojón es su hito narrativo. El asset no garantiza que ese mojón sea visible.

### `campos_camino_compartido`
**No.**

La identidad de la sala es tránsito de personas/materiales de varias regiones, que el asset no comunica.

### `campos_almacen`
**No.**

Existe un almacén de ruta concreto que debe permanecer visualmente distinguible.

### `campos_vista_vaisgard`
**No.**

La primera vista de Vaisgard debe conservarse.

### `alto_cuenca_norte`, `piedra_entrada_veyra`, `juncos_entrada_veyra`, `sombra_entrada_veyra`
**No por defecto.**

Aunque están en Veyra, cada una conserva una transición desde una región distinta; reutilizar el mismo asset borraría esa lectura.

**Mapping canónico recomendado:**  
solo `campos_colinas` para v1.

---

# 4. Regla de uso

El mismo asset regional puede repetirse en varias microsalas solo cuando:
- la geografía local es compatible;
- no elimina un landmark narrativo esencial;
- no contradice una estructura específica de la sala.

Un asset regional NO redefine el texto ni la topología.

---

# Estado

**Hueco #203 / Hoshai: CERRADO por Historia.**  
**Hueco #215 / Lethra: CERRADO por Historia.**  
**Hueco #487 / Veyra: CERRADO por Historia.**

Integración puede conectar estos mappings sin otra decisión creativa.
