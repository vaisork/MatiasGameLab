# Vintage Telnet — Contenido canónico para cerrar el primer loop jugable

**Responsable:** Historiador y Constructor del Mundo  
**Origen:** #409, #410, #482  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Objetivo:** llenar tres huecos P0 del ciclo temprano sin añadir sistemas paralelos ni ampliar mapa.

Este documento define contenido y plausibilidad del mundo.  
No fija precios, porcentajes, cantidades, HP recuperado, fatiga, cooldowns ni antifarmeo.

---

# 1. #409 — primeros encargos pagados de Valdren

Valdren tiene trabajo cotidiano suficiente para pagar pequeños encargos sin convertir cada ayuda en misión épica.

La institución canónica usada en v1 es:

## Puesto de encargos del Mercado de Valdren

No es un gremio nuevo ni una facción.

Es una función práctica del mercado:
- comerciantes;
- familias;
- talleres;
- encargados de camino;
- viajeros;

dejan o transmiten pequeñas necesidades de trabajo.

No requiere un NPC nombrado para existir.

Superficie autorizada:
- `valdren_mercado`

El pago se hace en sellos porque el mercado ya participa del intercambio común de ruta.

## Tres encargos

| id de contenido | tipo | giver/institución | inicio | condición estructurada de finalización | repetición | por qué se paga |
| --- | --- | --- | --- | --- | --- | --- |
| `valdren_recado_forja` | local / micro | Puesto de encargos del Mercado de Valdren | `valdren_mercado` | aceptar paquete/recado → llegar a `valdren_forja` → registrar entrega con Daro → volver a `valdren_mercado` | repetible con cadencia de Jugabilidad | transportar recados pequeños entre mercado y taller evita que cada comerciante abandone su puesto |
| `valdren_revision_cobertizos` | ruta corta | Puesto de encargos del Mercado de Valdren | `valdren_mercado` | aceptar encargo → llegar a `valdren_cobertizos_viejos` → registrar inspección/presencia → volver a `valdren_mercado` | repetible con cadencia de Jugabilidad | los cobertizos sirven a viajeros y cargas; conviene confirmar que siguen utilizables y reportar daños o faltantes |
| `valdren_estado_vado` | recorrido mayor / riesgo | Puesto de encargos del Mercado de Valdren | `valdren_mercado` | aceptar encargo → llegar a `valdren_vado_menor` → registrar estado del paso → regresar a `valdren_mercado` | repetible con cadencia de Jugabilidad | el vado es parte de una ruta usada; cambios de agua, piedras movidas o daños importan a quienes transportan bienes |

## Límites

- Ningún encargo exige matar fauna.
- Un combate puede ocurrir durante el viaje, pero no es la condición de cobro.
- No dar sellos por cada criatura vencida dentro del encargo.
- No crear “daily quest”.
- No crear rango, reputación o gremio.
- El primer recado puede completarse enteramente dentro de Valdren y por tanto garantiza una vía de ingreso sin viaje peligroso.
- La repetición y reducción de payout pertenecen a Jugabilidad.

## Texto base de cobro

Narrativa puede variar el texto, pero la intención es breve:

> “Trabajo hecho. Aquí están tus sellos.”

No convertir el cobro en ceremonia ni exposición.

---

# 2. #410 — provisión y recuperación segura de Valdren

La primera recuperación comprable debe existir dentro del pueblo.

Superficie autorizada:
- `valdren_mercado`

No hace falta restaurante nuevo.

## Provisión básica

**Nombre:** Ración de camino de Valdren  
**Tipo:** provisión portátil ordinaria.

Presentación:
- pan firme o pieza horneada sencilla;
- acompañamiento salado/conservado de mercado;
- envuelto para viajar;
- pensado para comerse durante una pausa.

No es:
- poción;
- objeto mágico;
- medicina;
- comida de lujo;
- sistema de hambre.

Su función narrativa es permitir que un viajero recupere fuerzas con alimento común.

Jugabilidad decide:
- precio dentro de su banda;
- HP/fatiga;
- uso;
- relación con field-rest budget;
- si requiere estar fuera de combate.

## Servicio de recuperación segura

**Nombre:** Comida caliente del mercado  
**Lugar:** `valdren_mercado`  
**Proveedor:** puestos de comida del propio mercado, sin NPC nombrado obligatorio.

Es una comida servida en un lugar seguro donde el personaje puede sentarse, comer y descansar antes de volver a salir.

No crea:
- posada nueva;
- cama;
- teleport;
- curación mágica;
- respawn especial.

Jugabilidad decide si corresponde a recuperación media o completa segura y su coste exacto.

## Límite regional

En v1:
- la Ración de camino se compra en Valdren;
- la Comida caliente del mercado se consume en Valdren;
- `campos_almacen` NO se convierte todavía en tienda ni punto de curación.

Eso puede ampliarse después.

---

# 3. #482 — materiales vendibles de fauna común

La fauna común no deja sellos.

Parte de una criatura puede ser aprovechable **si el ejemplar y el estado del material lo permiten**.

No toda victoria produce material útil.

Jugabilidad define frecuencia/cantidad.

## Comprador autorizado v1

**Puesto de acopio del Mercado de Valdren**  
Superficie:
- `valdren_mercado`

No es un gremio ni un NPC obligatorio.

Es una función de compra/reventa de materiales comunes:
- cuero;
- fibras;
- caparazón;
- púas;
- seda;
- escamas;
- piezas naturales útiles.

El puesto puede pagar sellos porque revende esos materiales a talleres y viajeros.

### Daro

Daro **NO es comprador genérico de materiales de fauna**.

Puede reconocer materiales duros si una escena futura lo necesita, pero la economía v1 no debe asumir que el herrero compra pieles, seda o caparazones.

---

# 4. Tabla de materiales plausibles por familia C1

| familia | material plausible | no tendría sentido | puede no producir nada |
| --- | --- | --- | ---: |
| Mordelinde | retazo de piel curtible; diente pequeño íntegro | cuerno, placa mineral, seda | sí |
| Espinajo de rastrojo | púas rígidas aprovechables; retazo de piel | caparazón completo, pluma, mineral | sí |
| Uñapiedra | escamas gruesas desprendidas/recuperables; uña curva íntegra | cuero abundante, cuerno, cristal | sí |
| Saltacresta | mechón de fibra/pelo resistente; pequeña pieza de cuero | escama mineral, caparazón, seda | sí |
| Cascapedernal | fragmento de caparazón orgánico duro | piedra “mágica”, metal, gema | sí |
| Colagrieta | retazo de piel flexible; diente pequeño | placa mineral, caparazón pesado, seda | sí |
| Pinzajunco | segmento de caparazón limpio; pinza menor intacta | piel curtible, pluma, gema | sí |
| Saltalodo | membrana/piel resistente en buen estado | caparazón, cuerno, seda | sí |
| Rondamusgo | fibra de pelo áspero limpia; semillas/hojas adheridas NO cuentan como loot propio | “musgo mágico”, cuero pesado, mineral | sí |
| Hilaria de niebla | seda recuperable de red; pequeña pieza de quitina | veneno comercial automático, gema, cuero | sí |
| Garralaja | tira de piel escamada; uña pequeña | piedra, cristal, metal | sí |
| Cavapolvo | placa dérmica/caparazón menor; uña excavadora pequeña | mineral extraído del cuerpo, gema | sí |
| Remojunco | fibra vegetal compactada del refugio NO; únicamente pequeñas placas córneas/tegumento si quedan íntegras | “junco loot” automático, gema | sí |
| Velacauce | piel/membrana flexible en buen estado | escama mineral, cuerno, metal | sí |
| Silbarisco | fibra/pluma-filamento corporal si su ficha final la conserva; si no, retazo de piel/fibra superficial | objeto sonoro mágico, gema | sí |

## Regla de prudencia

Para familias cuya anatomía visual/final cambie posteriormente:
- conservar la categoría material general;
- no inventar órganos, venenos o sustancias especiales;
- si la ficha final contradice el material, Historia debe corregir esa fila antes de implementación.

## Sin crafting obligatorio

Estos materiales tienen valor por intercambio.

El jugador no necesita fabricar nada con ellos para que sean útiles.

Un sistema de crafting futuro puede consumirlos solo mediante contrato nuevo.

---

# 5. Handoff

## Jugabilidad
Debe fijar:
- payout exacto de los tres encargos;
- frecuencia/cadencia;
- precio/efecto de Ración de camino;
- precio/efecto de Comida caliente;
- frecuencia/cantidad/precio de materiales;
- límites antifarmeo.

## Narrativa
Puede:
- escribir aceptación/cobro de encargos;
- presentar compra/uso de provisión;
- presentar obtención o ausencia de material en una línea breve.

## Desarrollo
No debe implementar hasta recibir los números cerrados de Jugabilidad.

---

# Estado

**Historia #409: COMPLETA.**  
**Historia #410: COMPLETA.**  
**Historia #482: COMPLETA PARA LAS FAMILIAS C1 LISTADAS.**
