# Vintage Telnet — Principios de Jugabilidad

Este documento es la **fuente de verdad de las reglas de jugabilidad de Vintage Telnet** dentro de MatiasGameLab.

## Autoridad sobre las reglas de juego

Las reglas de jugabilidad se definen en el trabajo conjunto entre Javier/Matías y el **Diseñador de Jugabilidad de Vintage Telnet**.

Los demás agentes pueden implementar reglas aprobadas, analizarlas técnicamente, señalar problemas o proponer ideas, pero **no deben crear, cambiar, eliminar ni reinterpretar reglas de jugabilidad por su cuenta**.

Si una implementación necesita una regla que todavía no existe, debe marcarla como **decisión pendiente de jugabilidad** y devolverla al Diseñador de Jugabilidad. No debe inventarla para poder continuar.

El Arquitecto de MatiasGameLab coordina arquitectura, responsabilidades y límites entre agentes. El Diseñador de Jugabilidad es responsable de mantener coherentes las reglas de cómo se juega Vintage Telnet. Javier y Matías conservan la dirección creativa y las decisiones finales sobre qué juego quieren.

## Método de diseño

Vintage Telnet no se diseñará completo de una sola vez.

El proceso es:

1. Recuperar mediante preguntas la experiencia que Javier quiere conservar o reconstruir.
2. Identificar el núcleo de jugabilidad.
3. Convertir decisiones aprobadas en reglas claras y comprobables.
4. Mantener separadas las reglas confirmadas, las ideas en exploración y las decisiones pendientes.
5. Sólo después entregar reglas suficientemente definidas para implementación.

La historia, narrativa concreta y contenido de aventuras no sustituyen las reglas de jugabilidad.

## Principios confirmados hasta ahora

### 1. Progresión RPG
Vintage Telnet será un RPG de progresión. El personaje comienza con capacidades limitadas y aumenta su poder y posibilidades mediante el juego.

### 2. Combate y crecimiento
El combate forma parte de la progresión. El jugador comenzará enfrentándose a enemigos débiles y podrá enfrentarse a amenazas mayores conforme su personaje mejore.

Los números exactos, fórmulas, estadísticas, ritmo de progresión y balance todavía no están definidos.

### 3. Caminos o clases de personaje
Existirán diferentes formas de desarrollar al personaje, incluyendo conceptos como guerrero o mago.

Todavía está pendiente decidir cómo se obtiene o elige una clase y qué otras clases existirán.

### 4. Equipamiento
El equipamiento será una parte importante de la mejora del personaje. No todo objeto del juego necesitará una representación física.

### 5. Piezas físicas
Determinadas mejoras importantes tendrán una pieza física imprimible en 3D que pueda aplicarse a la figura base del jugador.

El diseño debe favorecer piezas prácticas y reutilizables —por ejemplo armas, báculos, prendas o accesorios— en lugar de exigir imprimir una figura completa cada vez que el personaje mejora.

Las piezas pueden imprimirse en un solo color. Pintarlas posteriormente es opcional y no debe ser requisito de jugabilidad salvo que una regla futura establezca lo contrario.

### 6. Ganar una pieza no equivale a poder usarla
Cuando un jugador consigue dentro del juego una mejora que requiere pieza física, obtener la recompensa digital no basta para activarla.

Debe existir un proceso de activación física.

### 7. Ciclo de activación física
El principio actualmente acordado es:

**Ganar la mejora → fabricar/recibir la pieza → colocarla físicamente en la figura del jugador → enviar evidencia fotográfica → validar la evidencia → habilitar el uso dentro del juego.**

La entrega de la pieza por parte del Maestro de Forja **no activa por sí sola** la mejora.

### 8. Evidencia del jugador
Es responsabilidad del jugador demostrar que aplicó la pieza a su personaje físico mediante una imagen.

Hasta que esa evidencia sea validada, la mejora correspondiente no puede utilizarse dentro del juego.

### 9. Maestro de Forja
Javier Díaz es el **Maestro de Forja**. Puede además participar como jugador y ejercer funciones de Maestro del Juego.

El hecho de que Javier fabrique o entregue una pieza no sustituye el requisito de evidencia del jugador.

### 10. Validador de Forja
Se prevé un agente/chat separado encargado de validar el cumplimiento del proceso de forja a partir de la evidencia correspondiente.

Ese agente **no define las reglas de la forja**. Aplica las reglas documentadas aquí y registra/verifica su cumplimiento.

## Decisiones de jugabilidad todavía abiertas

Entre otras, aún deben definirse:

- núcleo exacto de acciones que el jugador repetirá;
- objetivo o estructura de una sesión;
- creación inicial del personaje;
- elección u obtención de clases;
- atributos y estadísticas;
- sistema exacto de combate;
- exploración;
- comandos e interfaz Telnet;
- inventario;
- economía;
- experiencia y niveles;
- muerte y consecuencias;
- cooperación y competencia;
- frecuencia y rareza de recompensas físicas;
- reglas exactas de validación;
- qué ocurre con una pieza perdida, retirada o rota;
- balance entre recompensas exclusivamente digitales y recompensas físicas.

Que algo aparezca en esta lista significa que **ningún agente debe asumir una respuesta todavía**.

## Regla para implementación

Antes de implementar una mecánica de Vintage Telnet, el agente responsable debe comprobar este documento.

- Si la regla está confirmada: puede implementarse respetando su intención.
- Si está pendiente: no debe inventarse.
- Si la implementación revela una contradicción: debe señalarse.
- Si se propone una mejora: se presenta como propuesta, no como regla existente.
- Si Javier/Matías y el Diseñador de Jugabilidad aprueban una nueva regla, este documento debe actualizarse para mantener una única fuente de verdad.

## Responsabilidad del Diseñador de Jugabilidad

El Diseñador de Jugabilidad mantiene este documento como contrato de cómo funciona el juego.

Su trabajo incluye entrevistar, estructurar, probar conceptualmente y documentar reglas. No le corresponde convertir por iniciativa propia esas reglas en historia, código, arte o arquitectura técnica.

---

**Estado:** diseño inicial en curso.  
**Juego:** Vintage Telnet  
**Repositorio:** MatiasGameLab
