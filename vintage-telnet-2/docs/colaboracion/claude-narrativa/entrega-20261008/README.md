# Encargo para Claude: narrativa de Vintage Telnet 2

## Entorno y proyecto

Trabajas junto al Codex principal en Ubuntu. Proyecto activo: `/home/jdiaz/proyectos/vintage-telnet-2-nuevo`. Publicación: `https://github.com/vaisork/MatiasGameLab`, carpeta `vintage-telnet-2` en main. La carpeta Ubuntu tiene su propio historial: no hacer push de su raíz sobre el main del monorepo.

Tu función es autoría y revisión narrativa. Codex integra textos y código, prueba el juego y publica entregas completas. No cambies los archivos de trabajo de Codex ni hagas commits, push o despliegues. Escribe únicamente en esta carpeta de colaboración. No uses partidas reales para pruebas. El estado general de pausa/reanudación lo decide Javier; este documento no reanuda automáticamente a otros agentes.

## Leer en este orden

1. `docs/CONTEXTO_CONTINUIDAD.md`: decisiones de Javier, canon resumido, estado y límites.
2. `CONTENT_CONTRACT.md` y `CANON_EXPANSION.md`: campos narrativos, estados y consecuencias válidas.
3. `docs/ARCHITECTURE.md`: cómo llega contenido al jugador.
4. `content/world.json` y `content/regions/*.json`: NPC, encargos, criaturas, lugares y estados existentes. Trabajar sobre sus IDs exactos.
5. `server/engine.py` en modo lectura: aceptación, entrega, conversación, comercio, encuentros y composición narrativa. Hay un parche reciente de narrativa guardado pero no desplegado.
6. `review/GOAL_HANDOFF_20261007.md` y los informes específicos del recorrido que revises: distinguir pruebas reales de fixtures y cambios históricos.

Prompt maestro de Javier: `/home/jdiaz/Descargas/Vintage_Telnet_Prompt_Actualizado.pdf`. Usar las secciones de canon/narración pertinentes. No copiar el documento completo a esta carpeta ni publicar sus datos sensibles iniciales. No reutilizar la historia ni la narración descartada del juego anterior. Conservar su canon autorizado y las decisiones más recientes de Javier.

## Objetivo

Texto para niños que están entendiendo una historia. NPC con motivos, conversación concreta y una petición comprensible: quién, qué necesita, por qué importa, dónde y a quién acudir, cómo reconocer que se cumplió. Entregar el encargo debe mostrar una consecuencia coherente, no sólo un número. Evitar palabras rimbombantes y relleno.

Encuentros humanos con diálogo y contexto; fauna con movimiento y reacción en su entorno. No inventar economía, poderes, recompensas, salidas, objetos, estados de combate o ausencias. Diferenciar narración de voz del personaje. No prometer una elección que no existe: etiquetar cualquier propuesta que requiera implementación como tal. No afirmar que un animal desaparece si el motor permite seguir interactuando con él. No atribuir frases a un NPC ausente ni amenazas vivas a enemigos vencidos.

Conservar contraste: viaje tranquilo puede ser breve; petición, encuentro y decisión importante merecen una escena. Hacer tres o cuatro pasadas de lectura/crítica/corrección con ejemplos antes/después y recorrer mentalmente secuencias completas. Los conteos no prueban que un niño disfrutará la historia.

## Entrega dentro de esta carpeta

- `ENTREGA.md`: resumen, alcance, archivos consultados, IDs cubiertos, lo listo para integrar y las dependencias reales de código.
- `TEXTOS.md`: bloques por ID existente y campo. En cada bloque: archivo de origen, ID, campo, condiciones de aparición, texto actual de referencia breve, texto propuesto y explicación de coherencia. Incluir aceptación, desarrollo, entrega y regreso cuando correspondan; no sólo primera visita.
- `REVISION.md`: problemas detectados, repetición, contradicciones, pasadas realizadas y escenas todavía no verificadas en juego.
- Opcional: `propuestas.json` con una lista de `{archivo, tabla, id, campo, condiciones, texto, requiere_codigo}`. Es material de integración, no un parche para aplicar automáticamente.

No mezclar propuestas no respaldadas por mecánicas con texto ya integrable. No incluir contraseñas, tokens, fotos familiares originales, partidas o PDF completo. No crear otro motor ni otra copia editable del contenido principal.

## Coordinación y GitHub

Mientras Codex desarrolla, no editar `content/`, `server/`, `client/` ni archivos de otros colaboradores. Todos los entregables de esta carpeta forman parte del repositorio de desarrollo y se publicarán con la siguiente entrega completa revisada, dentro de `vintage-telnet-2/docs/colaboracion/claude-narrativa/`. Codex es responsable de integración, revisión, pruebas y publicación en MatiasGameLab. Javier decidió trabajar en bloques largos en Ubuntu y subir al terminar, no publicar cada borrador.
