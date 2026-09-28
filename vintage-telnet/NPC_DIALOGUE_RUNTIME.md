# Proveedor de conversación de NPC en runtime

El contrato de `server/npc_dialogue.py` puede usar un proveedor fijo de prueba o
un Ollama local. El proveedor real se selecciona explícitamente al arrancar el
servidor; no se consulta ni descarga la lista de modelos y la selección no hace
ninguna petición durante el inicio.

## Activación explícita

En el `server.env` local del servicio:

```ini
VT_NPC_DIALOGUE_PROVIDER=ollama
VT_OLLAMA_DIALOGUE_URL=http://127.0.0.1:11434
VT_OLLAMA_DIALOGUE_MODEL=<modelo aprobado para Vintage Telnet>
VT_OLLAMA_DIALOGUE_TIMEOUT=120
```

`VT_NPC_DIALOGUE_PROVIDER=fixed` conserva el stub determinista. Ollama de runtime
solo acepta HTTP en `localhost`/loopback. El modelo debe seleccionarse
explícitamente; no se consulta ni se escoge uno entre los modelos instalados.
Usa un modelo general aprobado para Vintage Telnet (por ejemplo,
`llama3.2:3b`), nunca el fine-tune `ojo-de-agua:latest`. Una configuración
`ollama` incompleta mantiene el servidor arriba, registra el problema y hace
que cada intento de diálogo degrade al `fallback_dialogue` canónico del NPC.

## Datos y límites

- El proveedor recibe el prompt ya filtrado por `build_dialogue_prompt`: voz y
  personalidad del NPC, memoria reciente y solo `knowledge_allowed`.
- El mensaje actual del jugador se envía como mensaje `user`; nunca se mezcla
  dentro de las instrucciones `system`.
- Se usa el endpoint [`/api/chat` de Ollama](https://docs.ollama.com/api/chat),
  sin streaming, tools ni llamadas a acciones del juego.
- Solo se consume `message.content` como texto. La autoridad, presencia,
  historial y gate de acciones siguen en Vintage Telnet.
- Se atiende una sola inferencia a la vez por proceso; solicitudes concurrentes
  degradan al fallback en vez de acumular carga de modelo en la Raspberry.
- Timeout, error HTTP, JSON inválido o contenido vacío degradan al fallback
  canónico sin afectar estado del jugador o del mundo.
- El mensaje del jugador se limita a 500 caracteres, el cuerpo de la respuesta
  a 64 KiB y el tiempo de espera a 1–180 segundos (120 por defecto).
- No requiere paquetes Python adicionales; usa la biblioteca estándar.

## Estado de verificación

Las pruebas automatizadas del proveedor simulan la respuesta HTTP y no contactan
a ningún servidor Ollama. Esto verifica el protocolo, selección de proveedor,
filtrado de conocimiento y fallback, pero no demuestra por sí solo que un modelo
concreto responda bien o con latencia aceptable.

Sondas manuales locales del 2026-09-28: la primera llamada con
`llama3.2:3b` superó 60 segundos sin terminar; el modelo se descargó de memoria.
Con el límite ampliado a 120 segundos, una segunda llamada sintética por el
adaptador respondió en aproximadamente 58 segundos:

> La forja se está moviendo. Acabo de terminar una pieza de clavos para la cosecha de esta semana. La calidad de la acero es buena y espero que no haya problemas con los aperos.

La respuesta sí es contextual, pero contiene una construcción gramatical
incorrecta y un detalle de trabajo no confirmado por el contexto autorizado.
Esto confirma que la integración local funciona y que el límite ampliado permite
obtener texto; no valida todavía calidad narrativa ni elimina alucinaciones. No
se probó `qwen3:4b`. La decisión de Javier permite probar Ollama de runtime en
Vintage Telnet aunque la latencia sea mayor; sigue prohibido usar el modelo
`ojo-de-agua:latest`. El proveedor del servicio continúa en `fixed` y no se ha
desplegado.

El flujo de generación única de personalidad de
[`NPC_OLLAMA_BRIDGE.md`](NPC_OLLAMA_BRIDGE.md) es una función distinta y no
activa ni configura por sí misma las conversaciones en runtime.
