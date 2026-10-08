# Mecánicas nocturnas — 6 octubre 2026

Implementación de las extensiones autorizadas por Javier: no se presenta como una regla numérica transcrita del PDF. Se reutilizan las transacciones/idempotencia existentes y el perfil inicial asequible; no hay validación ficticia de Forja.

- `afinar`: sólo con el forjador presente, pieza activada/intacta, una vez por instancia, confirmación explícita, 12 sellos y una unidad de `room.honing_material`. Aumenta +1 el daño base que consume la ronda real. No equipar automáticamente ni activar Forja. Daro pide fibra de Espinajo; Beran pide piedra veteada. Taren conserva su alfarería.
- Venta de materiales nuevos por 2 sellos, y materiales anteriores por 3/4. Tiendas y compradores deben estar presentes físicamente. Armas conservan bloqueo de venta del equipo activo/última pieza utilizable y confirmación.
- `exit_requirements:{dirección:{requires_flags:[...],text:...}}`: salida deshabilitada hasta autorización narrativa. Regreso a un destino ya visitado y entrada al pueblo de origen quedan libres, conservando recuperación y retirada.
- Acciones/temas admiten `requires_items`, `consume_items`, `give_items` como mapas catálogo→cantidad. Las entregas validan existencias antes de consumir. Recompensas de objetos acotadas a 1–3 unidades por entrada. Acciones únicas requieren `forbids_flags` y `set_flags` correspondientes.
- `combatant_kind:'human'`: el forajido se examina/evalúa/combate, pero nunca entra al bestiario animal. Usa el perfil inicial 28 PV/5 daño; XP con los límites/antifarm existentes, sin monedas por matar. `victory_flags` activa consecuencias narrativas y evaluación de encargos al terminar. Snapshot combate incluye tipo para presentación.
- Encargos nuevos utilizan su sala autorizada y pago entero 0–24, sin lista fija de IDs. Son únicos por defecto; `repeatable:true` opta por repetición. Los tres encargos originales mantienen repetición. Los tres repetibles de Valdren comparten su presupuesto decreciente por hora. Los encargos regionales únicos pagan el importe anunciado y no pueden repetirse. La familia heredada `valdren_paid_errands` se conserva para los repetibles originales.

Prueba nueva `tests/test_night_mechanics.py`: afinado/material/coste/daño real, puertas y retorno, humano sin bestiario, entrega única, validación antes de consumir, y recorrido API real hasta combate/forja con request repetido y reconexión. 5 pruebas PASS (2.296 s). Suite integrada: 56 pruebas PASS en 30.688 s con contenido nuevo. La revisión visual y recorridos adicionales corresponden al resto del equipo.

El agente mecánico no modificó ninguna partida real. La raíz integra los cambios y reinicia el servidor sólo después de verificarlos, conservando runtime y partidas.

## Segunda iteración: progresión y recuperación

Hallazgo causal en la regla existente: el respawn conservaba un `rest_budget` agotado. §24.8 de GAMEPLAY declara explícitamente que morir reinicia ese presupuesto para evitar quedar atrapado. Corregido: tras respawn a 60% PV/40 fatiga, vuelve a permitir descanso 60→70→72; repetir no cura más y no cambia XP/sellos. Provisión continúa sin reiniciar presupuesto, como exige su contrato; servicio pagado sí lo reinicia. No se añadieron PP ficticios ni cambios arbitrarios de daño en fauna ambiental.

Cobrar añade `encargo_pagado:<id>` para memoria persistente de NPC. Toda victoria añade `victoria:<room_id>:<combatant_id>` para consecuencias **locales**: vencer al mismo forajido en otro lugar no abre el premio de este campamento. La marca no crea moneda ni botín extra por sí sola. Los botones de quitar equipo usan Guardar arma / Quitar armadura / Guardar escudo.

Regresiones específicas: 7 pruebas PASS (1.641 s), incluyendo descanso tras muerte y nuevo encargo único con memoria de pago. La partida del jugador permanece intacta.

## Correcciones de contrato tras recorrido independiente

Los encargos regionales únicos pagan el importe anunciado completo; no se les aplica el contador repetible de Valdren. El ledger respeta `quest.family`. La familia repetible original conserva sus multiplicadores 100%/60%/30%. Cuatro encargos únicos de 8 sellos pagan 32 aunque existan cinco cobros previos de Valdren, y cada instancia cobra una sola vez. Encargos únicos ya pagados desaparecen de acciones; aceptados muestran una explicación de tarea en marcha.

Impulso Arcano sobre una preparación usa la precisión básica del rival menos 10 puntos, según §36.5: Espinajo pasa de preparación 60 a respuesta básica 50−10=40. Antes dejaba 50 al restar del valor preparado. Se mantiene el efecto no preparado de −20 y todas las recargas existentes. Regresión comprueba el valor exacto de 40.

## Encargos visibles y defensas honestas

Snapshot `quests` contiene únicamente instancias del jugador: `id`, `name`, `status`, `reward` base, `reward_current` calculado con el mismo método del cobro, `summary`; `return_room_name` sólo cuando esa sala ya fue visitada y `paid_amount` sólo para pagos registrados. No expone requisitos, flags, salas objetivo ni encargos no aceptados. Las defensas explican su efecto calculado con atributos/estado actuales: al comenzar, esquivar y resistir no prometen una ventaja inexistente; bloquear conserva su reducción base del 10%. No se cambiaron fórmulas.

`room.buy_items` permite que un comprador acepte sólo materiales de su oficio; ausencia conserva el comportamiento anterior. La restricción autoriza tanto el botón como el POST real y no sustituye la presencia obligatoria del NPC.

## Cooperación y preparación declarada

Reproducción de defecto actual: Sombra secundaria usaba Borrar el Foco, la respuesta del enemigo fallaba, pero `opening` seguía ausente. Corregido: esa respuesta fallida concede Apertura a las Sombras participantes que usaron su capacidad en esa ronda; cada personaje conserva y consume sólo su propia apertura. Prueba API de dos cuentas comprueba una tirada del 60% que sólo conecta gracias al +15 del Sombra secundario, mientras el principal no recibe ese bono.

Espinajo declara `prepared_action` con embestida frontal, interruptible y precisión 60; perfiles/partidas anteriores mantienen compatibilidad con `prepared` booleano. Guardia requiere preparación frontal; Arcano requiere preparación interruptible para cancelarla; un disparo del Artífice puede causar su daño normal de capacidad sin interrumpir una preparación no interruptible. No se inventó una criatura nueva ni se cambiaron cifras del Espinajo. El snapshot muestra la preparación actual para comunicar la decisión.

## Búsqueda: variedad realmente alcanzable

Auditoría con tiradas .75/.76/.80/.90/.99 confirmó que el primer texto de búsqueda vacía nunca podía aparecer: el código multiplicaba directamente una tirada siempre ≥.75 por una tabla de dos textos, eligiendo siempre índice 1. Corregido normalizando la tirada dentro del intervalo de cada resultado; también las huellas distribuyen sus variantes dentro de su intervalo. Se conservan 40% de hallazgo, umbral 75% de huella, stock compartido 30 minutos, descanso de búsqueda 60 segundos y el número de llamadas RNG. Regresión verifica ambos textos de vacío y ambas huellas mediante sus tiradas concretas.

Lectura de acceso económico: los seis orígenes tienen comprador/provisión a 0–3 pasos y búsqueda a 1–2. Se notificó al autor del mundo la ausencia de recuperación pagada fuera de Valdren, para permitir nuevos intentos locales sin viajar lejos ni usar la muerte como reinicio.

## Atención local y acciones pagadas

`recovery_npc` requiere que el cuidador esté presente y visible según sus condiciones y horario. Las salas anteriores sin ese campo mantienen compatibilidad. Recuperación sin beneficio se deshabilita con «No necesitas atención ahora». Compra, afinado, reparación y recuperación exponen coste y deshabilitan saldo insuficiente con la cantidad exacta que falta. Los POST siguen protegidos por la validación de acciones y los guardas de saldo/efecto. Reparar menciona al herrero realmente presente, no a Daro por defecto.

## Encuentros compartidos y conocimiento personal

Defecto reproducido por el recorrido independiente: un jugador que conocía el rodeo de Nhal/Lethra podía filtrar al forajido antes de la tirada y almacenar otro animal en el caché compartido, privando del encuentro a otro jugador sin esa marca. Corregido: selección global sólo depende de presencia física/respawn y hora/clima; las condiciones personales filtran después señales y acciones para cada jugador. No se modifican probabilidades ni los 5 minutos de caché. Los pools actuales sólo usan dos `forbids_flags` personales; no existe una condición de flags públicos que requiera ampliar el contrato ahora. Si se autoriza una futura condición global de aparición, deberá declararse de forma explícita, sin mezclarla con conocimientos personales.

Regresión comprueba dos personajes con marcas distintas, expiración de 5 minutos, reaparición y tres snapshots que no tiran RNG ni alteran caché. Pruebas específicas actuales: 16 PASS en 1.797 s. Ninguna prueba toca la partida real.
