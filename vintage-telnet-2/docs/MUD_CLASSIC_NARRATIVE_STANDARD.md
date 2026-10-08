# VT2 — Estándar de narrativa MUD clásica

**Objetivo:** conseguir que Vintage Telnet 2 se lea como un MUD clásico en español de los años noventa, enriquecido con un mundo dinámico y reconocible.

## Reglas editoriales

- Cada habitación debe comunicar dónde está el jugador, qué distingue al lugar y qué puede observar.
- Usar lenguaje concreto, evocador y natural. Evitar prosa ornamental, redundancias y explicaciones innecesarias.
- Descripción base orientativa: 30–65 palabras. Permitir excepciones justificadas.
- No repetir información entre descripción, ambiente, acontecimientos y mensajes de navegación.
- Separar texto permanente de información dinámica: hora, clima, NPCs, criaturas, objetos y sucesos.
- No inventar cambios de estado del mundo mediante la narración.
- Mantener salidas y acciones disponibles claramente identificables.
- Usar descripciones más extensas sólo cuando el descubrimiento lo justifique.
- Permitir que `mirar` revele detalles adicionales sin saturar la navegación habitual.
- Conservar todos los hechos importantes, pistas, relaciones espaciales y elementos del canon.

## Implementación

1. Auditar una región existente e identificar duplicaciones.
2. Crear ejemplos de antes y después.
3. Separar los bloques narrativos de los datos de estado.
4. Proponer ajustes mínimos al renderizador.
5. Probar navegación, exploración, combate y regreso a habitaciones.
6. Medir reducción de texto repetido y verificar que no se pierda información.

## Restricciones

- No modificar masivamente el mundo.
- No alterar canon ni mecánicas.
- No desplegar en Raspberry sin autorización.
- Preparar primero una propuesta y una prueba acotada.

## Criterio de éxito

El jugador debe reconocer cada lugar en pocos segundos, percibir un mundo vivo y querer seguir explorando.
