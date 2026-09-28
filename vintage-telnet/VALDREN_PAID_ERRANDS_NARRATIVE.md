# ECONOMY-INCOME-01 — presentación narrativa de encargos de Valdren

Issue: #409
Fuente histórica: PR #491.
Lugar de inicio y cobro: valdren_mercado.
Giver: Puesto de encargos del Mercado de Valdren, sin NPC nombrado obligatorio.

## 1. valdren_recado_forja

Tipo: local / micro.

Inicio:
“En el puesto de encargos hay un recado sencillo para la forja. No hace falta salir de Valdren: basta llevarlo, confirmar la entrega y regresar.”

Aceptación:
“Tomas el recado y lo guardas para entregarlo en la forja.”

Condición estructurada:
aceptar en valdren_mercado → llegar a valdren_forja → registrar entrega con Daro → volver a valdren_mercado.

Al entregar en la forja:
“Daro recibe el recado, lo revisa por encima y deja constancia de que llegó.”

Al volver a cobrar:
“Recado entregado y regreso confirmado. Trabajo hecho. Aquí están tus sellos.”

Repetición:
repetible con la cadencia que fije Jugabilidad.

## 2. valdren_revision_cobertizos

Tipo: ruta corta.

Inicio:
“Piden comprobar el estado de los cobertizos viejos del camino y volver con una respuesta clara. No hace falta reparar nada: solo llegar, observar el lugar y reportar.”

Aceptación:
“Queda anotado el encargo: revisar los cobertizos viejos y regresar al mercado.”

Condición estructurada:
aceptar en valdren_mercado → llegar a valdren_cobertizos_viejos → registrar inspección/presencia → volver a valdren_mercado.

Al registrar la inspección:
“Te detienes lo suficiente para comprobar el estado general de los cobertizos y recordar qué debes reportar.”

Al volver a cobrar:
“Con el estado de los cobertizos confirmado, el puesto da el encargo por cumplido. Aquí están tus sellos.”

Repetición:
repetible con la cadencia que fije Jugabilidad.

## 3. valdren_estado_vado

Tipo: recorrido mayor / riesgo.

Inicio:
“Necesitan noticias del Vado menor: agua, piedras y estado del paso. El trabajo es ir, comprobarlo y regresar; no buscar pelea.”

Aceptación:
“Queda anotado el recorrido al Vado menor. El pago espera a tu regreso con el estado del paso.”

Condición estructurada:
aceptar en valdren_mercado → llegar a valdren_vado_menor → registrar estado del paso → volver a valdren_mercado.

Al registrar el estado:
“Observas el paso, las piedras y el agua con suficiente calma para poder describir cómo se encuentra.”

Al volver a cobrar:
“Tu reporte basta para saber cómo está el vado. Trabajo hecho. Aquí están tus sellos.”

Repetición:
repetible con la cadencia que fije Jugabilidad.

## Reglas comunes

- Ningún encargo exige matar fauna.
- Un combate durante el recorrido no sustituye la condición del encargo.
- No se pagan sellos por criatura vencida.
- No hay gremio, rango, reputación ni daily reward.
- El primer encargo garantiza una vía de ingreso sin abandonar Valdren.
- El texto de cobro no fija una cantidad; la cifra visible la aporta Jugabilidad.
- Doble submit, reconexión o volver a pasar por la sala no debe cobrar dos veces la misma finalización.

## Handoff

Narrativa #409: CERRADA.

Integración puede usar los tres content_id, el Puesto de encargos del Mercado de Valdren, las condiciones estructuradas de Historia y estos textos de aceptación/progreso/cobro. Payout, flags técnicos y antifarmeo pertenecen a Jugabilidad/Integración.
