# WORLD-POPULATION-01 — voz de NPCs ambientales

Origen: #334. Capa Narrador.
Este documento entrega barks reusables. Historia asigna los role_id definitivos, regiones y restricciones; Jugabilidad ya cerró densidad y persistencia.

## Habitante

Barks:
- "Buen camino."
- "Hoy hay más movimiento de lo normal."
- "Si buscas pasar, deja libre el centro."
- "Todavía queda día para ir y volver."

Respuesta fija a hablar:
> "No necesito nada, gracias. Solo estoy siguiendo con mi día."

## Trabajador

Barks:
- "Un momento; termino esto y dejo libre el paso."
- "Siempre aparece algo que reparar."
- "Mejor hacerlo bien una vez."
- "Por aquí pasa más gente de la que parece."

Respuesta fija:
> "Estoy trabajando. Puedes pasar, solo ten cuidado por dónde pisas."

## Cargador

Barks:
- "Despacio. Esto pesa más de lo que parece."
- "Déjame sitio y en un momento queda libre."
- "Lo difícil no es cargarlo; es llevarlo sin estorbar a todos."
- "Ya casi llego."

Respuesta fija:
> "Voy de paso con la carga. No hay ningún encargo."

## Viajero

Barks:
- "Aún me queda camino."
- "Vengo de más lejos de lo que parece."
- "Conviene mirar bien antes de dejar atrás un cruce."
- "Hoy prefiero avanzar mientras haya buena visibilidad."
- "Nos veremos en otro tramo, quizá."

Respuesta fija:
> "Solo estoy de camino. Que tengas buen viaje."

## Recolector

Barks:
- "Aquí todavía se encuentra algo si sabes mirar."
- "No hace falta llevarse todo lo que uno ve."
- "Estoy terminando por esta zona."
- "El terreno cambia mucho de un tramo a otro."

Respuesta fija:
> "Solo recojo lo habitual de la zona. No estoy buscando ayuda."

## Reglas narrativas N0

- Una frase debe poder aparecer sin implicar una misión.
- No mencionar recompensas, tiendas, precios, secretos ni amenazas no visibles.
- No prometer que el NPC estará en el mismo sitio después.
- No atribuir nombre, parentesco, oficio especializado o historia personal a una presencia efímera.
- Evitar frases que obliguen a una región concreta hasta que Historia asigne compatibilidad.
- Si una sala tiene NPC scripted, su diálogo tiene prioridad y estos barks no lo sustituyen.

## N5-lite — Loren

Primer viajero canónico:
- npc_id: `viajero_loren`
- route_id: `valdren_camino_corto_01`
- movimiento: Valdren → Árbol del descanso → regreso
- no comerciante, no quest giver, no autoridad

Barks específicos:
- "Voy hasta el árbol del descanso y luego regreso a Valdren."
- "Este camino cambia poco de nombre y mucho de aspecto."
- "Los cobertizos sirven para medir cuánto te has alejado."
- "Si el cruce queda a tu espalda, conviene recordar por dónde volver."
- "Llevo noticias pequeñas. Las importantes suelen viajar con más gente."

Respuesta fija a hablar:
> "Soy Loren. Voy y vuelvo por este camino. Si necesitas una misión o mercancía, tendrás que buscar a otra persona."

Reglas:
- las frases no cambian su ruta;
- conversación no ordena movimiento;
- no promete entrega de objetos;
- no revela amenazas ni rutas secretas;
- no crea servicio postal formal.

## Criterio de experiencia

La población debe hacer que un pueblo o camino parezca usado sin convertir cada figura en contenido que el jugador deba resolver. Hablar con un N0 confirma que es una persona del mundo, no una quest escondida.
