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


---

## VT-NPC-002 — Profundización de personalidad + segunda tanda

**Solicitante:** Javier  
**Estado:** ENTREGADO EN BORRADOR  
**Objetivo:** hacer que los NPCs se sientan más humanos y preparar una segunda tanda sin llenar los pueblos artificialmente.

### Mejoras aplicadas a los cinco ancla
Cada uno recibe:
- manías;
- irritaciones;
- humor;
- contradicción personal;
- error típico;
- comportamiento al ganar confianza;
- forma de enfadarse;
- relaciones iniciales;
- una regla de voz que no debe perderse.

### Segunda tanda añadida
Se añaden diez NPCs:
- Valdren: Oren, Ilya;
- Khariel: Vael, Isen;
- Brumak: Tovo, Piri;
- Narevia: Sela, Orin;
- Velmora: Mirel, Dovar.

Total inicial documentado: **15 NPCs**.

### Diseño social
Cada pueblo queda con tres perspectivas distintas y relaciones cruzadas para que:
- un NPC pueda opinar sobre otro;
- existan desacuerdos plausibles;
- rumores y observaciones no sean una sola voz;
- volver al pueblo pueda cambiar varias conversaciones.

### Regla para generación dinámica
La futura capa Ollama puede variar lenguaje, pero no identidad, memoria, conocimiento permitido ni relaciones.
