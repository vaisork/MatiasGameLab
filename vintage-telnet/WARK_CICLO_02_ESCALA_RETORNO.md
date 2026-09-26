# Wark — ciclo 02: escala, retorno y preparación en la malla periférica

**Fecha:** 2026-09-26. **Base revisada:** `main` 271a92eba6f0e3b554328d57ed1c66a61a7624f0.  
**Encargo vigente de Javier:** llenar los huecos de recorrido del mundo conocido sin programar.  
**Fuentes concurrentes:** issue #212 y sus tres comentarios; PR #218 abierto, sin merge (`historia/vt-malla-regional-212` b30377e); `narrador/routes-doc-main-sync` a5af232; `REGIONS.md`, `GAMEPLAY.md`, `CREATURES.md`, `NARRATIVE.md` y `server/world.py` de `main`.  
**Estado:** propuesta operativa para revisión. No es canon ni reglamento de jugabilidad.

## Corrección de escala tras leer #212

Javier ya fijó en los comentarios del issue que conocer/recorrer el mundo jugable debe rondar **6–8 horas de experiencia efectiva**, principalmente por retos, preparación, progresión, retornos y reintentos, no por seis horas de texto lineal. Narrativa propuso 20–30 segundos por sala solo como hipótesis de medición, no como velocidad aprobada. La cifra de «varios cientos de ubicaciones» es horizonte de crecimiento, no cuota para esta entrega.

La ficha de Tierra Húmeda del ciclo 01 sirve como estructura de orientación, pero todavía necesita un diseño explícito de **por qué el jugador querría o necesitaría volver**. Este documento llena ese hueco sin imponer costos ni resultados de combate.

## Una unidad de progreso que vale el regreso

Cada corredor puede sostener tres visitas con propósitos distintos:

| Visita | Pregunta del jugador | Resultado narrativo mínimo | Dependencia mecánica |
| --- | --- | --- | --- |
| Reconocimiento | «¿Hasta dónde llego y qué señales entiendo?» | Dos hitos recordables, una bifurcación visible y advertencia antes del peligro; regreso posible con información | Mapa conocido/visitado según `GAMEPLAY.md` §23 |
| Preparación | «¿Qué me faltó y a dónde vuelvo?» | El jugador reconoce el mismo lugar, ahora con una razón concreta para reintentar | Jugabilidad define fatiga, equipo, descanso, compra, muerte y respawn; no asumir hambre/comercio implementados |
| Expedición | «¿Qué cambió cuando pude continuar?» | Acceso a otro tramo, pueblo o ramal; hallazgo distinto de una recompensa repetible por caminar | Encuentros y XP de descubrimiento solo si Jugabilidad lo aprueba |

Esto es una **secuencia de experiencias posibles**, no un bloqueo obligatorio a todo jugador ni un requisito de nivel. Un jugador hábil o bien acompañado podría avanzar de otro modo si Jugabilidad lo permite.

## Matriz de presión y retorno para los cinco corredores del PR #218

| Corredor | Hito seguro de orientación propuesto por Historia | Presión perceptible que justifica decidir | Retorno con conocimiento, sin premio inventado | Ramales a reservar |
| --- | --- | --- | --- | --- |
| Paso de las Lajas (Khariel–Brumak) | Mirador de las Dos Piedras / Piedra de Resguardo; Refugio de Lajas | Visibilidad que disminuye al entrar en corredores de roca y caída lateral advertida | Saber distinguir la ruta principal de la cornisa al volver desde el lado mineral | Grieta del Eco Seco; Cornisa Ciega |
| Viento Bajo (Brumak–Valdren) | Las Tres Marcas / Cruce del Carro Viejo; Parada de los Cardos | Cambio de viento encauzado a horizonte abierto; desvío hacia excavación y surco bajo roca | Reconocer que los montones de piedra dejan de ser la única referencia | Cantera Abandonada; Zanja de la Piedra Hundida |
| Tierra Húmeda (Valdren–Narevia) | Puente de Madera Ancha; Vado de Juncos | Suelo saturado, pasarela y sendero de agua oscura anunciados antes de entrar | Volver con la localización del molino y comprender dónde recupera firmeza la tierra | Molino Hundido; Charcos Negros |
| Ribera Sombría (Narevia–Velmora) | Embarcadero del Último Claro; Orilla Velada | Se pierden gradualmente horizonte y marcas de agua al entrar bajo dosel | Reconocer el último punto de agua abierta y la primera marca confiable de Nhal | Canal Quieto; Sendero sin Marca |
| Dosel Alto (Velmora–Khariel) | Hitos y refugio de Alto de las Raíces según PR #218 | Cambio de señales discretas a terreno elevado: confirmar detalle canónico antes de escribir | Volver identificando el punto en que reaparecen señales de bosque | Ramales exactos a contrastar en `REGIONAL_CONNECTIONS.md` antes de ficharlos |

**Frente de responsabilidad:** Wark documenta la función de cada presión. Narrador decide la escena y cómo se comunica; Historia decide qué existe; Jugabilidad decide si hay obstáculo, costo, recuperación, nivel o consecuencia. Una amenaza superior de `CREATURES.md` no se convierte automáticamente en jefe ni activa pérdida de arma (`GAMEPLAY.md` §96).

## Prioridad dentro de la asignación actual

1. Completar la ficha piloto Tierra Húmeda con una tabla de **tres visitas**: primera lectura, retorno voluntario, segunda expedición. Distinguir lo observable de sistemas aún no aprobados.
2. Revisar el texto vigente de PR #218 antes de elaborar cada ficha nueva; si se integra a `main`, usar esa versión.
3. Extender el mismo instrumento de análisis a los otros cuatro corredores, uno por ciclo, sin copiar nombres, escenas o retos de uno a otro.
4. Registrar en cada ciclo cuántos tramos tienen orientación, vuelta, presión, desvío y cierre; reportar huecos reales, no acumular páginas de descripción.

Este orden organiza **el encargo ya asignado por Javier**; no abre issues ni asigna trabajo a otros.

## Prueba de valor para el lector

En una lectura de mesa, preguntar después de la primera incursión:
- ¿Dónde pararías o regresarías y qué señal te hizo decidir?
- ¿Qué recordarías para volver sin que el mapa te teletransporte?
- ¿Qué intentarías preparar para una segunda visita y cuál de esas opciones existe realmente en el juego hoy?

Si la tercera respuesta depende de comprar comida, vender botín o mejorar equipo sin que esos sistemas estén aprobados/implementados, la ficha se marca como dependencia futura y debe ofrecer un motivo de retorno basado en información, descanso o exploración que sí sea válido.

**Handoff:** Historiador mantiene el PR #218; Narrador lidera #212; Jugabilidad decide las consecuencias. Esta propuesta queda en la rama de Wark para que puedan consumirla sin que Javier transporte texto entre chats.
