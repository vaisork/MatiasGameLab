# Vintage Telnet — Contrato de acciones de interfaz v1

**Responsable:** Diseñador de Jugabilidad — Vintage Telnet  
**Estado:** APROBADO PARA IMPLEMENTACIÓN de #72/#73  
**Fuentes normativas:** `GAMEPLAY.md` §§15, 20, 22–24, 32; `INTERFACE_GAMEPLAY_REQUIREMENTS.md`  
**Alcance:** qué acciones puede ofrecer la interfaz y cuándo. No define HTML, estética, endpoints ni canon.

## Principio obligatorio

El servidor es autoridad. La interfaz **renderiza únicamente posibilidades autorizadas**; no deduce acciones desde texto narrativo, no calcula si una defensa conviene y no deja controles muertos para capacidades no disponibles.

Un botón y su comando escrito terminan en la **misma intención autoritativa**. Una acción no autorizada puede existir en Ayuda como enseñanza general, pero no como botón contextual de la escena actual.

Para #73, `available_actions` debe ser la fuente estructurada de acciones inmediatas. Cada entrada debe identificar al menos una `action` canónica y, cuando aplique, objetivos autorizados. El servidor puede incluir un `reason` para explicar por qué una acción esperable no está disponible, pero ese motivo **no obliga a renderizar un botón deshabilitado** si hacerlo revela equipo, rutas, enemigos, pistas o capacidades no descubiertas.

## Matriz v1

| Acción UI | Comando/intención equivalente | Visible cuando | Habilitada cuando | Autoridad/dato de servidor | Feedback mínimo |
| --- | --- | --- | --- | --- | --- |
| N/S/E/O | `norte/sur/este/oeste` | existe una salida **ya legítimamente disponible** en esa dirección | servidor permite movimiento ahora | salidas disponibles / `available_actions` | resultado textual del movimiento o motivo seguro de rechazo |
| Mirar | `mirar` | durante juego normal | servidor acepta la intención | `available_actions` o capacidad base de sala | vuelve a presentar situación general |
| Observar | `observar <objetivo>` | existe objetivo ya percibido/autorizado | objetivo sigue observable | `visible_targets` + acción/targets autorizados | señales relevantes sin resolver la deducción |
| Examinar | `examinar <objetivo>` | existe elemento concreto ya revelado/autorizado | objetivo sigue examinable | `visible_targets` + acción/targets autorizados | detalle legítimo del elemento |
| Evaluar | `evaluar <criatura>` | criatura legítimamente visible | servidor puede evaluarla | criatura visible + acción/target autorizado | categoría cualitativa; nunca HP, daño o % victoria ocultos |
| Atacar | `atacar <objetivo>` | existe objetivo atacable autorizado | servidor permite iniciar/continuar ataque | `available_actions` + targets atacables | confirmación/resultado textual; en combate el ataque básico continúa automáticamente si no se interviene |
| Huir | `huir` | personaje está en combate y huida es una posibilidad real | servidor acepta intento en esa ronda | `available_actions` | éxito o fallo comprensible; no mostrar % exacto salvo decisión futura |
| Esquivar | `esquivar` | existe ventana defensiva y el servidor la ofrece | acción incluida para la siguiente resolución | `available_actions`; ataque/contexto ya percibido | confirma que sustituye el ataque básico de esa ronda y narra resultado |
| Bloquear/desviar | `bloquear` | **solo** si ataque, posición y equipo apropiado permiten bloqueo | servidor lo incluye para esa resolución | `available_actions`; validación autoritativa de equipo/posición/ataque | confirma defensa elegida y narra bloqueo/desvío/impacto; no revelar equipo oculto |
| Resistir | `resistir` | existe ventana defensiva donde aceptar/mitigar impacto tiene sentido | servidor la incluye para esa resolución | `available_actions` | confirma defensa y narra consecuencia; no fingir que evita ser golpeado |
| Descansar | `descansar` | fuera de combate y contexto potencialmente seguro | servidor autoriza descanso en ese momento | `available_actions` / estado de peligro | recuperación o rechazo/interrupción explicado por texto/estado |
| Personaje | consulta de estado, no comando de combate obligatorio | jugador autenticado con personaje | estado disponible | `player_state` | panel con estado autoritativo; no calcula reglas |
| Mapa | consulta `/api/map` o contrato equivalente | sistema de mapa disponible para el personaje | datos cartográficos disponibles | estados conocidos/visitados y rutas conocidas/recorridas | solo conocimiento legítimo; nunca huecos de secretos |
| Inventario/Equipo | `equipar <objeto>` / `desequipar <objeto>` cuando #57 esté integrado | **solo después de existir el sistema real** | servidor autoriza acción; equipar/desequipar fuera de combate según §32 | inventario/equipo autoritativo + `available_actions` | poseído vs equipado, efecto/estado de Forja autorizado |
| Poderes | intención concreta del poder | solo si el personaje posee contenido real aplicable | poder disponible y requisitos/cooldown cumplidos | poderes poseídos + cooldowns + `available_actions` | nombre/estado/coste autorizado; nunca poder inventado |
| Hablar | `hablar <npc>` | NPC activo y legítimamente percibido | servidor autoriza conversación con ese NPC | `visible_npcs` + target autorizado | entrada/respuesta textual de conversación |
| Chat local | `decir <texto>` | función de chat local disponible | texto válido y servidor acepta envío | capacidad de chat/sala | distinguir inequívocamente chat de comando |

## Contrato específico de combate para #73

1. Al iniciar combate, **ataque básico automático** es el comportamiento por defecto. No hace falta que el jugador pulse Atacar cada ~4 s.
2. Antes de la siguiente ronda, el jugador puede enviar **una intervención**. Huir, Esquivar, Bloquear/desviar, Resistir, un poder u objeto válido sustituyen el ataque básico de esa ronda.
3. Esquivar/Bloquear/Resistir **no son tres botones permanentes equivalentes**. Solo aparecen cuando `available_actions` los autoriza para la resolución actual.
4. Bloquear requiere arma, escudo u objeto adecuado y además coherencia con ataque/posición. El cliente nunca infiere esto desde el inventario.
5. Fatiga base vigente antes de modificadores: ataque 4, Resistir 3, Bloquear 5, Esquivar 6, Huir 8. **El cliente no calcula ni descuenta estos valores**; el servidor aplica §20.7/§24.
6. Si la ventana defensiva expira o cambia el contexto, el servidor puede rechazar la acción; el cliente refresca estado y muestra el motivo seguro.
7. No existe una acción UI “mejor defensa”. La información percibida ayuda al jugador a elegir.

### Forma mínima recomendada de `available_actions`

Esto es un **contrato semántico**, no una imposición de nombres de endpoint:

```json
{
  "available_actions": [
    {"action": "huir"},
    {"action": "esquivar"},
    {"action": "bloquear"},
    {"action": "resistir"},
    {"action": "evaluar", "targets": ["<id-visible>"]}
  ]
}
```

Reglas:
- usar IDs/targets que el servidor ya haya autorizado; no reconstruirlos parseando narración;
- omitir una acción secreta/no disponible es preferible a enviar `enabled:false` si su mera existencia revela información;
- `reason` es apropiado solo cuando explicar indisponibilidad no filtra secretos, por ejemplo una acción visible que acaba de expirar;
- el servidor vuelve a validar siempre la intención aunque el cliente haya mostrado el botón.

## Ayuda visual — estructura de 5 bloques

La Ayuda debe ser corta, escaneable y orientada a **acción + ejemplo**, no a reglamento.

### 1. Muévete
- **N / S / E / O** — recorre salidas disponibles.
- **Mirar** — vuelve a leer dónde estás.

### 2. Investiga
- **Observar** — busca señales en algo que ya puedes percibir.
- **Examinar** — revisa de cerca un elemento concreto.
- **Evaluar** — estima cualitativamente el peligro de una criatura visible.

### 3. Combate
- El ataque básico continúa solo una vez iniciado el combate.
- **Huir** o una defensa disponible sustituye tu ataque de esa ronda.
- **Esquivar / Bloquear / Resistir** aparecen solo cuando tienen sentido; lee la situación antes de elegir.

### 4. Recupérate y consulta
- **Descansar** aparece cuando el lugar y el peligro lo permiten.
- **Personaje** muestra tu estado.
- **Mapa** recuerda únicamente lugares/rutas que tu personaje conoce.

### 5. Habla
- **Hablar** — conversa con un NPC disponible.
- **`decir <texto>`** — chat local con jugadores.
- Un comando desconocido no se convierte en chat.

Inventario/Equipo y Poderes **no se enseñan como controles activos** hasta que existan/desbloqueen realmente. Cuando aparezcan, la ayuda puede añadirlos dentro de un bloque existente antes de superar seis bloques.

## Criterios de aceptación para Junior/Servidor

- Ningún botón contextual depende de analizar texto narrativo.
- Ningún secreto se filtra por botón deshabilitado, hueco reservado o target no descubierto.
- Botón y comando llegan a la misma intención del servidor.
- Defensa ofrecida por UI coincide exactamente con `available_actions`.
- Bloquear no aparece sin autorización de servidor basada en equipo/contexto.
- Una intervención defensiva sustituye el ataque básico de esa ronda.
- Descansar no aparece durante combate y el servidor conserva autoridad para rechazar/interrumpir.
- Mapa no muestra desconocidos ni funciona como viaje rápido.
- Poderes/Inventario no aparecen como funciones reales antes de que exista contenido/sistema real.
- Ayuda usa máximo 4–6 bloques y ejemplos accionables.

## Handoff

- **Servidor #73:** implementar/normalizar intenciones y exponer `available_actions` conforme a este contrato; no inventar condiciones adicionales de Jugabilidad.
- **Junior #72:** renderizar acciones autorizadas y Ayuda; no crear controles permanentes para defensas contextuales.
- **Director de Arte #75:** puede diseñar lenguaje visual de estos estados sin cambiar cuándo existen las acciones ni cuál es la mejor.
