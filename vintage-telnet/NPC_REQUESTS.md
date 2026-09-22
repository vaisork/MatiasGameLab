# Vintage Telnet — Solicitudes de NPCs

## VT-NPC-001 — Población mínima para primera prueba jugable

**Solicitante:** Narrador de Aventuras  
**Prioridad:** ALTA  
**Fuente:** `vintage-telnet/NARRATIVE.md`  
**Estado:** EN TRABAJO

### Pedido
Población mínima para Valdren, Khariel, Brumak, Narevia y Velmora, priorizando pocos personajes memorables sobre volumen.

### Entrega inicial
- clasificación entre imprescindibles, útiles y todavía innecesarios;
- cinco NPCs ancla en BORRADOR, uno por pueblo;
- cada ancla permite conversación inicial, seguimiento y reacción al regreso.

### Pendiente
- validación del Historiador cuando corresponda;
- selección del primer NPC de implementación por Narrador;
- segunda capa hasta aproximarse al objetivo de 15–20 solo después de probar el P0.

---

## VT-PSY-003 — NPC conversable para playtest infantil

**Solicitante:** Psicopedagogía y Experiencia Infantil  
**Prioridad:** P0 para playtest narrativo  
**Fuente:** `vintage-telnet/RESEARCH_REQUESTS.md` / `PSYCHOPEDAGOGY.md`  
**Estado:** RESPUESTA P0 PREPARADA — TAREN SELECCIONADO

### Requisitos asumidos
- respuesta inicial breve;
- conversación por capas;
- seguimiento;
- separación entre saber, creer y desconocer;
- reacción al regreso con una observación del jugador;
- ningún NPC resuelve automáticamente el misterio.

### Dependencia técnica
El servidor todavía debe distinguir de forma inequívoca órdenes, conversación con NPC y chat entre jugadores.


---

## VT-NPC-PLAYTEST-001 — Taren como primer NPC conversable

**Estado:** LISTO PARA VALIDACIÓN

Se selecciona a Taren (Khariel) para la primera prueba porque la prueba técnica real más reciente ya dejó un personaje Felaryn en Khariel.

La especificación completa está en `NPCS.md` e incluye:
- primer encuentro;
- preguntas de seguimiento;
- respuesta “no sé”;
- negativa;
- señales comunes;
- combinación de señales;
- reacción al regreso;
- límites de Presencia;
- memoria mínima esperada;
- criterio de aceptación infantil.

**NECESIDAD DEL HISTORIADOR:** validar que el rol cotidiano de Taren no introduzca una institución o jerarquía no definida.

**NECESIDAD DEL NARRADOR:** validar que el grado de información de la conversación encaje con VT-NAR-001/002B y elegir la escena concreta de introducción.

**NECESIDAD TÉCNICA:** implementar después de cerrar la separación entre comando, NPC y chat local.
