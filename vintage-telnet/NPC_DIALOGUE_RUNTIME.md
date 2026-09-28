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

Sonda manual local del 2026-09-28: `llama3.2:3b` recibió un prompt sintético de
Daro por `/api/chat`, pero no terminó dentro del timeout de 60 segundos usado
en la prueba. La configuración predeterminada de runtime se subió a 120 segundos
para dejar margen al arranque en frío. La petición expiró; descargué el modelo
de memoria y no obtuve una respuesta usable. No hice una segunda llamada. Este resultado no demuestra que todos
los modelos o prompts fallen, pero ese modelo/configuración no está listo para
activar en el juego.

El flujo de generación única de personalidad de
[`NPC_OLLAMA_BRIDGE.md`](NPC_OLLAMA_BRIDGE.md) es una función distinta y no
activa ni configura por sí misma las conversaciones en runtime.
