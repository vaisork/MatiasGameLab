# Ciclo 6 — jugar y criticar historial después de misiones

Evaluación de agente mediante API real, dos cuentas en una misma base temporal, sin editar inventarios/flags/base real. `scripts/depth-cycle6-history.py` extiende la sesión larga para completar las siete misiones regionales, las tres originales de Valdren y las recuperaciones de caja y placa en ambos interiores. Luego vuelve con el protagonista y un observador nuevo a los mismos puntos; el observador no realiza entregas. La acequia se repara mediante su acción autorizada de alcance mundo y se comprueba con ambas cuentas. Así se distingue conocimiento personal de reparación compartida.

La primera pasada focal, 680 movimientos, expuso el defecto. La pasada reproducible final incorpora además el control de acequia compartida y conserva sus propios eventos en `review/depth-cycle6-before.json`; esa es la referencia exacta para AFTER. No se afirma evaluación humana ni que un guion dirigido sea juego espontáneo.

## Lo mejor y lo más débil

Las acciones consumen caja/placa/polea y los NPC ya tienen algunas memorias correctas. El defecto ocurre después: la habitación conserva el objeto en su posición original y el diálogo base pide buscarlo mientras la memoria confirma que ya lo devolviste. El historial económico funciona; el mundo leído contradice esa causalidad.

Casos jugados, no supuestos:

- Nela describe la caja al fondo del ramal y a continuación levanta «la caja que devolviste».
- Ruma dice «Ahora falta la placa» y después muestra la balanza montada. La cámara de balanzas conserva un brazo vacío y el depósito todavía muestra la placa contra el saco.
- El propietario vuelve a las cajas de Seran: la polea entregada sigue «encajada entre dos cajas».
- El secadero conserva juguete y recipiente aunque el personaje ya separó el recipiente y lo entregó a Elin.
- Los siete encargos regionales terminan; salvo recuerdos NPC, las escenas siguen casi iguales. En las tres misiones originales de Valdren ni el punto de entrega distingue las noticias recibidas.

El observador nuevo comparte esas escenas base. No es correcto arreglarlo poniendo los flags personales en el mundo: se daría por hecha la misión de otra cuenta. Las reparaciones auténticamente compartidas, como acequia o caldo servido, requieren conservar el alcance ya definido.

## Aburrimiento, plantilla y mundo

Tras pagar, varios NPC sustituyen su recuerdo concreto por el último mensaje genérico: «El trabajo que acordaste está terminado y pagado...». La repetición interrumpe la conversación para explicar cierre contable. Una referencia a la polea/nota/cuencos comunica historia de forma más breve y situada.

El hombre estático en la descripción de compuerta no depende de señales reales ni de recuperación del encuentro. La descripción neutral debe enseñar franja de paso y madera; la señal real establece si hay amenaza. Una memoria de enfrentamiento puede reconocer el lugar sin prometer que jamás volverá otra persona.

Los interiores del canal y almacén son buenos lugares para silencio y tensión, pero la memoria genérica de apoyos pierde caja, placa, crecida, cordel y brazo de balanza. El canon hidráulico y las adaptaciones del almacén existen como elementos; necesitan continuidad causal para percibirse como mundo trabajado.

## Sistema infrautilizado y cambio concreto

Se usará `states` con flags personales existentes para descripción/day/night/return/examine; no se cambiarán reglas, cuantías ni scopes. Los estados compartidos anteriores se conservan y no se convertirán en recuerdos privados. Las tres misiones originales sólo certifican observaciones: pagar por medir una abrazadera no repara una rueda, y traer noticias de un vado no drena el agua.

Dos prioridades: objetos retirados/entregados que siguen visibles y recuerdos NPC contables que desplazan su hecho concreto. Tercera: rama elegida debe seguir siendo visible (paño/cubierta, base/aro, amarre/perchas, aviso/comprobación), sin simular una reparación adicional ni resolver misterios históricos.

## Valoración inicial

Identidad/continuidad espacial 4/5; memoria causal 2/5; vida ambiental 3/5; ritmo 3/5; curiosidad al regresar 3/5. La pérdida de consecuencia es más grave que un texto repetido: leer dos afirmaciones incompatibles obliga a interpretar el motor desde fuera del mundo. No se declara suficiente el 3/5 de vida o ritmo; este ciclo no promete convertir todo el catálogo en simulación dinámica.
