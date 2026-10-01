# Vintage Telnet — Mapping visual regional II

**Responsable:** Historiador y Constructor del Mundo  
**Origen:** #506 / #507  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Objetivo:** conectar dos assets aprobados a salas existentes sin crear geografía nueva.

---

# 1. Korven — hondonada de líquenes minerales

Asset aprobado:
`assets/vintage-telnet/locations/korven-hondonada-liquenes-minerales.webp`

## Mapping principal

### `piedra_abrigo_viento`
**Sí — principal.**

Razón:
- ya es una hondonada protegida del viento;
- funciona como pausa natural de viajeros;
- el asset representa exactamente terreno contenido, roca fracturada y superficies protegidas;
- líquenes apagados son compatibles con humedad/resguardo local sin volver Korven un bioma vegetal.

## Compatibilidad secundaria

### `piedra_hendiduras`
**Condicional.**

Puede utilizarse solo si el encuadre conserva la lectura de corredores paralelos.
No debe borrar la identidad de hendiduras.

### `piedra_cavidades`
**No.**

Las cavidades superficiales son el landmark principal; el asset no las garantiza.

### `piedra_meseta_baja`
**No.**

La meseta requiere horizonte más abierto y exposición al viento, lo contrario de la hondonada.

### `piedra_entrada_veyra` y posteriores
**No.**

Ya pertenecen a la transición hacia Veyra.

**Mapping recomendado v1:**  
`piedra_abrigo_viento`.

---

# 2. Velmora — pasarela protegida entre raíces

Asset aprobado:
`assets/vintage-telnet/locations/velmora-pasarela-protegida-raices.webp`

## Mapping principal

### `sombra_borde`
**Sí — principal.**

Razón:
- es el borde habitado de Velmora;
- las casas y circulación ya se funden con raíces/troncos;
- una pasarela corta y protegida es infraestructura cotidiana coherente en esta transición;
- no redefine el camino como puente largo ni arquitectura monumental.

## Compatibilidad secundaria

### `velmora_centro`
**Sí, como contexto visual secundario de asentamiento.**

La pasarela puede representar circulación interna de Velmora alrededor del centro, pero no debe sustituir una futura imagen específica de plaza/núcleo si existe.

### `sombra_raices_cruzadas`
**No por defecto.**

La sala dice que el camino ya parece natural; introducir una pasarela construida cambiaría su lectura.

### `sombra_sendero_doble`
**No.**

Su identidad es la bifurcación natural temporal que vuelve a unirse.

### `sombra_niebla_baja` y bosque profundo
**No.**

La infraestructura habitada debe quedar cerca de Velmora, no propagarse arbitrariamente por Nhal profundo.

**Mapping recomendado v1:**  
`sombra_borde`, con `velmora_centro` como contexto secundario permitido.

---

# Regla general

Los assets de arquitectura cotidiana pueden repetirse solo dentro de la zona habitada que representan.

No deben usarse para convertir rutas naturales profundas en infraestructura urbana continua.

---

# Estado

**#506: mapping histórico cerrado.**  
**#507: mapping histórico cerrado.**
