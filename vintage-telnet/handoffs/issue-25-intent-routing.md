# Handoff — Issue #25: intenciones de terminal y primer playtest narrativo

**Responsable:** Desarrollador Junior / desarrollador disponible de Vintage Telnet  
**Base main:** `77f0e04e2cee4148dd0fc3f7b91fab5a1c7607e9`  
**Rama:** `junior/issue-25-intent-routing`

## Cambios

### 1. Chat deja de ser fallback
`/command` ya no publica cualquier texto desconocido como chat.

Chat explícito:
- `decir <texto>`
- `say <texto>`

Un comando desconocido devuelve error y no crea mensaje de sala.

### 2. Parser único de intención

Se añadió `parse_intent()` con tipos:
- `move`
- `look`
- `inspect`
- `say`
- `talk_npc`
- `unknown/invalid`

Movimiento y comando escrito siguen convergiendo a la misma lógica autoritativa.

### 3. Inspección

`observar` y `examinar` se reconocen como intención estructurada.

Ejemplos:
- `observar`
- `observar huellas`
- `examinar puerta`

Mientras no exista contenido canónico específico, la respuesta es segura:
`detail=null` / “No hay detalle adicional autorizado todavía.”

No se inventa contenido narrativo.

### 4. Conversación NPC

`hablar <npc>` queda clasificado separadamente de chat.

Todavía no genera diálogo. Devuelve contrato técnico explícito indicando que no hay NPC activo para conversación.

### 5. API estructurada

Nuevo endpoint:

`POST /api/intent`

Usa el mismo parser que `/command` y devuelve intención estructurada para:
- movimiento;
- mirar;
- inspección;
- chat explícito;
- hablar con NPC;
- comandos desconocidos.

### 6. UI

El texto de ayuda del campo de comandos ya no afirma que cualquier texto se publique.

Ahora explica:
- movimiento;
- mirar;
- observar/examinar;
- `decir <texto>`;
- `hablar <npc>`.

## Pruebas añadidas/actualizadas

En `vintage-telnet/tests/test_gameplay.py`:
- comando desconocido no se vuelve chat;
- `examinar huellas` no se vuelve chat;
- chat requiere `decir`;
- `/api/intent` diferencia inspect / talk_npc / say / move;
- movimiento sigue funcionando;
- prueba antigua de chat implícito actualizada a chat explícito.

## Límites respetados

No se modificó:
- Raspberry;
- systemd;
- SQLite viva;
- contenido canónico;
- diálogos NPC;
- NPCs definitivos;
- Ollama.

## Evidencia

La sesión no dispone de un runner CI asociado a esta rama ni de checkout local completo del repo, así que no se afirma una ejecución completa de la suite.

La revisión estática confirmó:
- `/command` ya no contiene fallback `store.add_message(...raw...)`;
- chat solo entra por intención `say`;
- inspección y hablar NPC no llaman `store.add_message`;
- `/api/intent` comparte `parse_intent()`;
- la expectativa antigua de chat implícito fue actualizada.

**LISTO PARA REVISIÓN TÉCNICA:** SÍ
