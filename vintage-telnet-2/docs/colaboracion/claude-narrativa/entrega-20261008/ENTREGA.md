# Entrega narrativa — bloques 1 a 3

Autor: Claude (autor y revisor narrativo). Fecha: 2026-10-08. Solo se escribió en esta carpeta. No se tocaron `content/`, `server/` ni `client/`. No hubo commit ni despliegue.

## Resumen

Los 10 encargos ahora tienen una historia completa: una petición en la voz del NPC, un resumen para el diario, un aviso de «listo» que dice adónde volver, y una entrega con una consecuencia que se ve y una frase final del NPC. Además:

- Se corrigieron las contradicciones que impedían que cada encargo tuviera sentido: medida inexistente, exámenes que no respondían a la pregunta, recipiente con dueños cruzados, opciones de la taza que no se oponían.
- Se arreglaron 13 respuestas de NPC que imprimían narración como si fuera voz.
- El Salteador de cargas tiene voz, motivo, entrada al combate y derrota sin muerte.
- La fauna de Edran tiene un texto propio por lugar.

## Archivos de esta carpeta

| Archivo | Contenido |
|---|---|
| `TEXTOS.md` | 245 bloques por ID y campo: archivo, condiciones, texto actual, texto propuesto y por qué. |
| `propuestas.json` | Los mismos 245 bloques como `{archivo, tabla, id, campo, condiciones, texto, requiere_codigo}`. Es material de integración, no un parche automático. |
| `REVISION.md` | Problemas encontrados, las cuatro pasadas con ejemplos antes/después, y lo que falta verificar. |
| `generar.py` | Única fuente de las propuestas. Regenera `TEXTOS.md` y `propuestas.json` leyendo el texto actual de `content/`. Comprueba que ningún texto quede vacío. |

### Sintaxis de `campo`

- Un punto entra en un objeto: `topics.rueda`.
- `[n]` es un índice: `states[0]`.
- `[clave=valor]` selecciona un elemento de una lista: `actions[id=…]`, `wildlife_pool[creature=…]`.
- Si el tema actual es un objeto, el campo es `topics.X.text`. Hay que cambiar solo el texto y conservar los flags.

## Archivos consultados

- `docs/CONTEXTO_CONTINUIDAD.md`, `CONTENT_CONTRACT.md`, `CANON_EXPANSION.md`, `docs/ARCHITECTURE.md`
- `content/world.json`, `content/regions/*.json`
- `server/engine.py`, en lectura: aceptar, cobrar, hablar, hablar_adversario, victoria, people, update_quests
- `server/mechanics.py`: perfiles y observaciones
- `review/GOAL_HANDOFF_20261007.md`, por encima
- `tests/test_narrative_results.py`, para comprobar que los campos nuevos ya están cubiertos por fixtures
- Las secciones de narración del prompt maestro (extracto `/tmp/vt-authoritative-reread.txt`). No se copió nada de él aquí.

## IDs cubiertos

- **Encargos** (`accept_dialogue`, `accept_text`, `ready_text`, `delivery_text`, `payment_dialogue`):
  - valdren_recado_forja, valdren_revision_cobertizos, valdren_estado_vado
  - khariel_polea, khariel_cornisa
  - velmora_recipiente
  - narevia_preparativos
  - vaisgard_aviso_carga, vaisgard_toldo
  - brumak_taza
- **NPC**:
  - edran_bren, edran_nela, edran_oren
  - hoshai_seran, hoshai_luma
  - nhal_varo, nhal_elin, nhal_desi
  - lethra_nima
  - veyra_tov, veyra_nera
  - korven_taren
- **Salas**:
  - valdren_cobertizo, valdren_graneros, edran_cobertizo_campo, edran_puente_juncos, edran_hito_campos
  - hoshai_campamento_lona, hoshai_taller_apoyos, hoshai_balcon_valle
  - nhal_umbral_elin
  - lethra_plataforma_secado
  - veyra_calle_toldos
  - korven_horno_reposo
  - 12 salas de Edran con fauna
- **Criaturas**: forajido_camino (dialogue, description, combat_intro, defeat_text). Espinajo, Mordelinde y Cornalomo mediante señales de sala.

## Listo para integrar (sin código)

Son los 121 bloques con `requiere_codigo: false`. Todos usan campos que el motor ya lee:

- Del parche narrativo guardado: `accept_dialogue`, `delivery_text`, `payment_dialogue`, `dialogue`, `defeat_text`.
- Ya existentes: `ready_text`, `topics`, `examine`, `actions[].text/label`, `signals[].text`, `wildlife_pool[].text`, `description`, `combat_intro`.

Notas para integrar:
- Al reemplazar `topics.X.text`, conservar `set_flags`, `requires_flags` y `forbids_flags`.
- El renombrado de claves de Nera (`topics (claves)`) es opcional. Ningún encargo depende de esas claves, pero conviene revisar los tests.
- Las claves del diálogo del salteador llevan espacios y acentos («qué quieres»). Comprobar el botón en el cliente; si da problemas, usar `que_quieres` con etiqueta.
- Los tests existentes usan fixtures propias para estos campos, no el texto del contenido. No se encontraron aserciones sobre los textos reemplazados.

## Dependencias de código (no integrables solo con texto)

| # | Necesidad | Por qué | Qué cambiaría |
|---|---|---|---|
| D1 | Nombre y diálogo de adversario **por señal** (`signals[].name`, `signals[].dialogue`, que el motor prefiera a los de la criatura). | En el campamento de Hoshai, Seran y el «Salteador de cargas» son la misma persona y hoy hablan con dos voces. El diálogo propuesto para Seran está en TEXTOS (`requiere_codigo: sí`). | `actions()`, `hablar_adversario` y el título del combate leen la señal de la sala. |
| D2 | Exigir que el NPC esté presente para `aceptar` y `cobrar`, o dar una explicación cuando no está. | Hoy se puede cobrar de noche ante el rincón vacío de Taren («Recibes 8 sellos» de nadie). Lo mismo con cualquier NPC que tenga horario. | Desactivar con la razón «Taren vuelve de día», o pago diferido. |
| D3 | `required_actions` atadas a la sala del encargo. | `examinar losa` cuenta en 3 salas, `apoyos` en 8, `recipiente` en 5 y `costura` en 2. En Bren se puede examinar la losa de la acequia, pasar por el hito sin mirar y el encargo se completa. | Guardar la sala en `instance.actions` y comparar con `room` opcional en la acción requerida. |
| D4 | (Propuesta) Variantes por repetición en los encargos repetibles de Valdren. | La misma historia se repite tal cual. | Por ejemplo, `accept_dialogue` como lista indexada por número de entregas. |
| D5 | (Cadena del motor) «recuperas N sellos» al vencer a un humano. | Si no te había quitado nada, «recuperar» es falso. | «ganas» o «el salteador deja caer N sellos». |

## Bloque 4: estándar MUD clásico (carpeta `estandar_mud/`)

Auditoría de Edran, propuesta de texto para las 183 salas de las seis regiones, parches mínimos de motor y cliente, y una prueba reproducible. En un recorrido por las 183 salas: −51 % de palabras leídas y −63 % de texto repetido; 141 tests OK y QA del cliente PASS con los parches. Detalle en `estandar_mud/ESTANDAR_MUD.md`. No se ha integrado ni desplegado.

Ampliado después:
- Las 183 descripciones en versión larga y sensorial: +22 % de texto nuevo en el recorrido.
- Escenas que avanzan al volver en 11 lugares.
- Combate narrado según el arma, la intensidad del golpe y el ataque de cada criatura (`combate.patch` y `combate_motor.patch`). Entran en la base desplegada `vt2-mud-piloto` con 145 tests OK.

## Estado de las dependencias (comprobado en el diff local de Codex, 2026-10-08)

- **D1** hecho: `room.adversary_prose` con `creature_prose()`. El diálogo propuesto para Seran va en `hoshai_campamento_lona.adversary_prose.forajido_camino`, no en `signals[].dialogue`.
- **D2** hecho: aceptar y entregar quedan desactivados si el NPC no está, con su horario.
- **D3** a medias: `update_quests` guarda `room` en cada acción realizada. Falta poner `room` en las `required_actions` de `world.json` (`losa`, `apoyos`, `recipiente`, `costura`) para que cuenten sólo en su sala.
- **D5** hecho: «ganas N sellos».

## Bloque 2: fauna de Hoshai, Korven, Lethra y Nhal (grupos E–H)

91 textos `wildlife_pool[creature=…].text`, uno por sala y criatura, donde hoy se repetía la misma frase entre 4 y 12 veces. No se tocan las señales fijas ni los textos que ya eran propios de cada sala (Saltacresta, la mayoría del Cascapedernal, parte del Pinzajunco y del Rondamusgo). Corrige también la errata «Un Unapiedra» → «Uñapiedra». Todo se puede integrar sin código.

## Bloque 3: secretos para descubrir (grupo I)

Petición de Javier: que el niño sienta que la aventura crece cuanto más investiga, con easter eggs. Seis secretos, cada uno con el mismo esquema:

1. **Pista:** un examen condicionado. Las pistas también salen al azar al pulsar Observar.
2. **Revelación:** una acción con su entrada en el diario.
3. **Remate:** un tema nuevo con un personaje que ya existe.

| Secreto | Dónde | Cuándo o quién | Remate |
|---|---|---|---|
| Los Espinajos de Lio | Fragua, cobertizo de estacas, pozo (Valdren) | noche, segunda visita, día | Elva (y Daro tras el primero) |
| La repisa de las marcas | Paso entre paredes (Hoshai) | sólo **Felaryn** (Senku); los demás ven la pista | Luma |
| La barquita de Sola | Orilla del canal (Lethra) | sólo **Marevyn** (Alivision) la saca; después la ven todos | Sola y Mira, que se contradicen |
| La figura de corteza viaja | Rincón de semillas, claro, patio del relato (Nhal) | tras sostener la figura; día, atardecer y noche | Desi |
| Piedras para el muro antiguo | Patio de mensajes (Vaisgard) | segunda visita | Arel. No resuelve quién construyó el muro. |
| El dibujo que crece | Refugio de Lajas (Korven) | cambia en las visitas 3, 5 y 8 | el propio dibujo |

Sólo se usan guardas que ya existen: `requires_time`, `requires_visits`, `requires_species`, `requires_flags`, `forbids_flags`, `scope` y `journal`. No hay objetos, sellos ni XP.

Notas para integrar:
- `states[+]` significa añadir un estado nuevo al final de la lista. En el dibujo de Korven, colocar los estados en orden de visitas: gana el último que se cumpla.
- En las propuestas de `actions[id=…]`, `topics.X` y `examine.X` que no existen todavía, el texto es el objeto JSON completo que hay que añadir.
- Antes de dar por buenos los secretos por especie, comprobar en producción (sólo lectura) que los personajes de Senku y Alivision guardan `state.species` como `felaryn` y `marevyn`.

**Requiere código (I7):** una línea en el diario, «Secretos encontrados: N. El mundo guarda más.». Es lo que hace volver a mirar de noche o en la tercera visita.

## No hecho todavía

- Más secretos: ahora hay uno por región. Próximo: un segundo por región, y secretos que conecten dos regiones (un objeto o nombre que reaparece lejos).
- Encuentros humanos contextuales en las otras cuatro salas del salteador, usando `adversary_prose` (Edran canal, Korven almacén, Lethra ribera, Nhal sendero).
- Conversaciones de NPC sin encargo, salvo las corregidas por la voz.
- Una lectura en el juego real (ver el final de REVISION.md).
