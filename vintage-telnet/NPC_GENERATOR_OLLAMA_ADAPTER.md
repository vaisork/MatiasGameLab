# Generador de NPCs → personalidad Ollama: contrato de integración

## Objetivo

Esta capa prepara la salida autoritativa del Generador de NPCs para PR #20 sin
llamar al Ollama real durante desarrollo local.

El Generador sigue siendo dueño de todos los hechos del NPC. El puente de PR #20
solo añade personalidad/voz una vez.

## Ficha autoritativa normalizada

Campos mínimos:

- `id`
- `name`
- `species`
- `settlement`
- `location`
- `role`
- `relationships`
- `knowledge_allowed`
- `knowledge_forbidden`
- `beliefs_uncertain`
- `initial_talk`
- `conditional_knowledge`
- `narrative_function`
- `gameplay_function`
- `memory_hooks`

Se permiten campos adicionales del generador, pero siguen siendo autoritativos e
inmutables durante el enriquecimiento.

El generador **no** puede producir `personality`, `personality_locked` ni
`personality_provenance`; esos campos pertenecen exclusivamente al puente de
personalidad.

## Flujo

```text
Generador
  ↓
normalize_authoritative_npc()
  ↓
enrich_generated_npc()
  ↓
PR #20 enrich_personality_once()
  ↓
personality + provenance + personality_locked=true
```

En desarrollo local se inyecta un fake mediante `enrich_fn`; no se llama Ollama.

## Lotes

`enrich_generated_batch()` procesa varias fichas ya creadas y rechaza IDs duplicados.
No genera NPCs nuevos ni decide canon.

## Integración posterior

Cuando PR #20 esté disponible en la rama integrada, el adaptador importa de forma
perezosa:

`server.npc_personality.enrich_personality_once`

No se duplica el cliente Ollama ni su validación.
