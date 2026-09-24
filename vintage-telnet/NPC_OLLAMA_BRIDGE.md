# Puente Generador de NPCs ↔ Ollama — personalidad de una sola generación

## Decisión

El **Generador de NPCs** es la autoridad. Ollama no crea el NPC ni decide hechos del
mundo: únicamente añade personalidad y voz **una vez**, después de que la ficha
autoritativa ya existe.

Flujo:

```text
Generador de NPCs
      ↓ ficha JSON autoritativa
npc_personality.enrich_personality_once()
      ↓ una sola llamada local
Ollama
      ↓ JSON de personalidad estrictamente validado
NPC con personality + provenance + personality_locked=true
      ↓
contenido persistido
```

Después de `personality_locked=true`, volver a pasar el NPC por el puente no llama a
Ollama. Reinicios, cambios de modelo y actualizaciones de Ollama no modifican el NPC.

## Qué puede crear Ollama

Solo estos campos:

- `temperament`
- `speech_style`
- `formality`
- `humor`
- `sociability`
- `response_length`
- `expressive_reactions`
- `traits`
- `example_phrases`

Las frases de ejemplo existen para fijar la voz del personaje. No pueden añadir hechos
nuevos, relaciones, objetos, poderes, eventos o secretos.

## Qué sigue perteneciendo al generador

Todo lo demás. Entre otros: identidad, nombre, especie, pueblo, oficio, relaciones,
conocimiento permitido/prohibido, historia, capacidades, objetos, función narrativa y
cualquier dato que afecte canon, mecánicas o estado.

El puente copia esos datos sin modificarlos y rechaza una respuesta de Ollama que intente
devolver campos fuera del contrato de personalidad.

## Configuración local de Ollama

Por defecto:

- URL: `http://127.0.0.1:11434`
- modelo: `VT_OLLAMA_NPC_MODEL`

Si no se configura un modelo, el puente consulta `/api/tags`. Solo autodetecta cuando
hay exactamente un modelo instalado; si hay varios, falla de forma explícita para no
elegir uno arbitrariamente.

Opcional:

```text
VT_OLLAMA_URL=http://127.0.0.1:11434
VT_OLLAMA_NPC_MODEL=<modelo-instalado>
```

No hay credenciales de Ollama en Git y Ollama no se expone como ruta HTTP del juego.

## Uso desde el generador

En Python:

```python
from server.npc_personality import OllamaPersonalityClient, enrich_personality_once

npc = generador.crear_npc(...)
npc = enrich_personality_once(npc, OllamaPersonalityClient())
guardar_npc(npc)
```

O mediante CLI, desde `vintage-telnet/`:

```bash
.venv/bin/python -m server.npc_personality_cli npc.json --in-place
```

También puede escribirse en un archivo distinto:

```bash
.venv/bin/python -m server.npc_personality_cli npc.json --output npc-ready.json
```

## Datos guardados

Además de `personality`, se añaden:

```json
{
  "personality_locked": true,
  "personality_provenance": {
    "ollama_model": "...",
    "personality_prompt_version": "vt-npc-personality-v1",
    "personality_generated_at": "..."
  }
}
```

## Fallos

Si Ollama está apagado, no tiene modelo, tarda demasiado o devuelve JSON fuera del
contrato, la creación de personalidad falla sin modificar la ficha original.

Esto **no afecta al juego en ejecución**: Ollama no forma parte de login, movimiento,
chat, combate ni ninguna petición crítica del jugador.

## Regeneración

No existe regeneración automática en v1. Si en el futuro se necesita una acción
administrativa explícita de regeneración, deberá diseñarse separadamente y quedar
auditada; actualizar Ollama o cambiar de modelo nunca basta para reescribir personajes.

## Prueba mínima de aceptación

1. Crear ficha autoritativa.
2. Enriquecerla: una llamada a Ollama.
3. Persistir JSON.
4. Volver a cargar y enriquecer: cero llamadas a Ollama.
5. Reiniciar servicio/Raspberry y confirmar que la personalidad sigue idéntica.
