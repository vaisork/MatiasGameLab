# Handoff — Issue #22: Generador de NPCs ↔ personalidad Ollama

**Responsable:** Desarrollador Junior de Vintage Telnet / desarrollador disponible  
**Base main:** `059a448cfac4fd84fb49c88d38093640b95e04b5`  
**Rama:** `junior/npc-generator-ollama-adapter`

## Alcance

Se preparó el lado del Generador de NPCs sin tocar Raspberry ni Ollama real.

Archivos:
- `vintage-telnet/npc_generator_adapter.py`
- `vintage-telnet/tests/test_npc_generator_adapter.py`
- `vintage-telnet/NPC_GENERATOR_OLLAMA_ADAPTER.md`

## Contrato autoritativo

La ficha normalizada exige:
- id, name, species;
- settlement, location, role;
- relationships;
- knowledge_allowed;
- knowledge_forbidden;
- beliefs_uncertain;
- initial_talk;
- conditional_knowledge;
- narrative_function;
- gameplay_function;
- memory_hooks.

Se permiten campos adicionales del generador y se conservan sin cambios.

El generador no puede pre-poblar:
- personality;
- personality_locked;
- personality_provenance.

## Integración con PR #20

El adaptador no duplica el cliente Ollama.

Cuando PR #20 esté integrado, importa perezosamente:
`server.npc_personality.enrich_personality_once`.

Para desarrollo local se puede inyectar `enrich_fn` falso.

## Lotes

`enrich_generated_batch()` procesa varias fichas ya existentes:
- no crea NPCs;
- no decide canon;
- rechaza IDs duplicados;
- aplica el mismo contrato a cada ficha.

## Pruebas

Se ejecutaron pruebas locales con un fake sin conexión a Ollama real.

Comando equivalente:
`python -m unittest discover -s vintage-telnet/tests -p 'test_npc_generator_adapter.py' -v`

Resultado:
```text
Ran 9 tests in 0.001s
OK
```

Cobertura:
1. normalización del contrato;
2. rechazo de campo autoritativo faltante;
3. rechazo de personalidad precreada por el generador;
4. flujo end-to-end con personalidad falsa y lock;
5. segunda pasada sin nueva generación;
6. campos autoritativos intactos;
7. detección de mutación autoritativa por el puente;
8. procesamiento por lote;
9. rechazo de IDs duplicados en lote.

Durante pruebas se detectaron y corrigieron dos problemas:
- el adaptador inicialmente rechazaba una segunda pasada sobre una ficha ya bloqueada;
- el fake inicialmente contaba una llamada antes de revisar el lock y no representaba fielmente PR #20.

## Límites respetados

No se tocó:
- Raspberry;
- Ollama real;
- systemd;
- /etc/vintage-telnet;
- SQLite viva;
- PR #20;
- servidor productivo;
- canon o tanda definitiva de NPCs.

## Dependencia

La integración real queda pendiente de que Issue #21 marque **OLLAMA REAL VALIDADO** y de que PR #20 esté disponible para importar su `enrich_personality_once()`.

**LISTO PARA REVISIÓN:** SÍ


## Revisión cruzada posterior con PR #20 / Issue #19

Se inspeccionó la implementación real de PR #20 y se confirmó compatibilidad con la firma
`enrich_personality_once(npc, client)`.

La revisión detectó un hueco en nuestro contrato: Issue #19 enumera **capacidades y límites**
como autoridad explícita del generador. Se añadieron los campos obligatorios:

- `capabilities`
- `limits`

También se añadieron pruebas específicas para rechazar fichas que omitan cualquiera de esos campos.


## Fixture compartido para prueba física posterior

Se añadió:

`vintage-telnet/tests/fixtures/npc-authoritative-synthetic.json`

Es una ficha explícitamente **NO CANÓNICA**, con IDs `test_*`, preparada para:
- validar el contrato del adaptador;
- servir como entrada reproducible a la prueba física de PR #20 / Issue #21;
- evitar inventar una ficha distinta en cada ejecución.

La suite del adaptador incluye una prueba que carga y valida este fixture.
