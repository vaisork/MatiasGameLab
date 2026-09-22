# Prueba en Raspberry Pi — puente NPC ↔ Ollama

Reporta el Agente que opera la Raspberry Pi de Vintage Telnet. Referencia:
`vintage-telnet/NPC_OLLAMA_BRIDGE.md` y la rama `arch/npc-ollama-personality-bridge`
(no mergeada a `main` todavía — este reporte alimenta esa revisión, no confirma
que esté lista para publicar).

## Estado y hardware

- Fecha UTC: 2026-09-22 ~15:10.
- Raspberry Pi 5, Debian 13, 7.9 GiB RAM (con `ollama.service` corriendo,
  ~4.9 GiB en uso al momento de la prueba), 4 núcleos, sin GPU.
- `ollama.service`: `active (running)`, escuchando en `127.0.0.1:11434`
  (no expuesto fuera de loopback).
- Modelos instalados: `llama3.2:3b`, `qwen3:4b`, `ojo-de-agua:latest`
  (este último es un fine-tune sobre `llama3.2:3b`, de otro proyecto en esta
  misma máquina). Ninguno configurado como `VT_OLLAMA_NPC_MODEL` por defecto
  — con 3 modelos instalados, la auto-detección del puente falla a propósito
  (documentado así en `NPC_OLLAMA_BRIDGE.md`) y exige elegir uno explícito.

## Pruebas unitarias (aisladas, sin Ollama real)

`tests/test_npc_personality.py`: **6/6 OK** en un venv aislado (checkout
temporal fuera del repo, sin tocar el checkout de trabajo). Cubren: campos
autoritativos sin cambios, generación única con lock, cero llamadas a Ollama
si ya está `personality_locked`, rechazo de campos extra que Ollama intente
colar, y rechazo de sobrescribir personalidad ya existente sin lock. El código
del puente (`server/npc_personality.py`, `server/npc_personality_cli.py`) está
bien diseñado: valida estrictamente, es idempotente y no permite que Ollama
toque campos autoritativos.

## Prueba real contra Ollama en esta Raspberry

Ficha de prueba (NPC ficticio, sin dato narrativo real): tabernero humano en
Valdren. Corrida vía `server.npc_personality_cli` contra el Ollama real de
esta máquina, en un checkout aislado (no la instalación de producción).

**Ningún modelo instalado completó el contrato exitosamente:**

| Modelo | Resultado | Tiempo |
|---|---|---|
| `llama3.2:3b` | Rechazado: falta `expressive_reactions` (reproducible, 2/2 intentos) | ~25-31s |
| `ojo-de-agua:latest` | Rechazado: falta `expressive_reactions` (mismo patrón; hereda de `llama3.2:3b`) | ~24s |
| `qwen3:4b` | Rechazado: Ollama no devolvió el campo `response` esperado (probablemente su modo "thinking" interfiere con `format: json`) | ~88s |

La primera llamada a `llama3.2:3b` además dio timeout a los 45s (default del
cliente) — con `--timeout 180` sí respondió en ~25-31s, así que 45s puede
quedar corto para la primera carga del modelo en este hardware.

La **validación funcionó correctamente en los tres casos**: el puente falló
cerrado sin persistir nada inválido, tal como está diseñado. No es un fallo
de seguridad ni de integridad — es que, con los modelos actualmente
instalados, ningún NPC real podría enriquecerse todavía sin intervención.

## No hice yo

No modifiqué el prompt, el contrato de campos ni la lógica de validación en
`npc_personality.py` — eso es una decisión del desarrollador/Arquitecto de
esta rama, no del operador. Tampoco instalé un modelo nuevo ni cambié la
configuración de Ollama en esta máquina (es compartido con otro proyecto,
Ojo de Agua).

## Pendiente / devuelto al desarrollador

1. Ajustar el prompt o el contrato para que modelos pequeños tipo
   `llama3.2:3b` incluyan `expressive_reactions` de forma consistente (podría
   ser tan simple como repetir la lista completa de campos con un ejemplo, o
   bajar el número mínimo de items).
2. Decidir si `qwen3:4b` (modo thinking) es compatible en absoluto con
   `format: "json"` de Ollama, o si debe excluirse/instruirse para desactivar
   thinking.
3. Subir el timeout por defecto del cliente (45s) o documentar que la primera
   llamada puede tardar más en hardware ARM sin GPU.
4. Cuando el desarrollador tenga un prompt/modelo que sí cumpla el contrato,
   el operador puede volver a correr esta misma prueba contra Ollama real
   para confirmar antes de integrarlo al flujo de creación de NPCs.

No se generó ni persistió ningún NPC real durante esta prueba; el archivo de
prueba y sus intentos de salida se descartaron al terminar.
