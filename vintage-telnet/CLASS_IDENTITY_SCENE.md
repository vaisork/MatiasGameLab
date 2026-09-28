# Vintage Telnet — Escena temprana de identidad de clase

**Origen:** #279 / continuación de #208  
**Responsable:** Narrador  
**Estado:** entrega narrativa para implementación

## Propósito

La primera capacidad de cada clase debe sentirse diferente antes de que el jugador estudie números o árboles de habilidades. La escena usa al **Espinajo de rastrojo** y una intención enemiga anunciada: la embestida territorial.

No es un tutorial obligatorio. Es una oportunidad contextual dentro de un combate normal.

## Intención enemiga

Texto base recomendado:

> El Espinajo baja el cuerpo y afirma las patas contra el suelo. Mantiene la cabeza dirigida hacia ti. Está preparando una embestida.

Variantes para repeticiones:

- El Espinajo raspa el terreno y vuelve a cuadrar el cuerpo frente a ti. La carga está por venir.
- El animal se planta, tensa el lomo y deja de tantear el terreno. Su siguiente movimiento apunta directamente hacia ti.
- El Espinajo retrocede apenas lo necesario para ganar impulso. No está huyendo.

La intención debe aparecer **antes** de resolverse. No ocultar una acción que precisamente sirve para enseñar lectura del combate.

## Juramentado — Guardia Comprometida

Disponibilidad contextual:

> Puedes comprometer tu guardia y recibir la carga de frente.

Éxito narrativo:

> Te afirmas antes del impacto. La embestida encuentra una guardia preparada y pierde su avance contra tu posición.

Fallo narrativo:

> Plantas la guardia, pero el impacto rompe tu postura antes de que logres asentarte por completo.

La identidad es **sostener el intercambio**, no producir un golpe de espada adicional.

## Arcano — Impulso Arcano

Disponibilidad contextual:

> La carga todavía no comienza. Puedes liberar un impulso arcano contra su preparación.

Éxito:

> El impulso alcanza al Espinajo cuando empieza a lanzarse. Una fuerza invisible altera su movimiento y descompone la carga.

Fallo:

> Liberas el impulso, pero no consigues desviar la masa que ya viene sobre ti.

Debe sentirse sobrenatural incluso si la resolución mecánica es pequeña. No describirlo como proyectil elemental salvo que Historia lo autorice.

## Sombra — Borrar el Foco

Disponibilidad contextual:

> El Espinajo te tiene fijado como objetivo. Puedes intentar romper esa atención antes de la carga.

Éxito:

> Rompes su lectura en el instante previo. El Espinajo arranca sin una referencia limpia y su embestida pierde la línea que buscaba.

Fallo:

> Intentas salir de su lectura, pero el Espinajo conserva tu posición y completa la carga.

La capacidad manipula **atención y oportunidad**. No implica invisibilidad ni teleportación.

## Artífice — Tiro de Interrupción

Disponibilidad contextual:

> La postura del Espinajo deja un instante para un tiro técnico antes de que cargue.

Éxito:

> Disparas durante la preparación. El impacto obliga al Espinajo a corregir el apoyo y corta el ritmo de la embestida.

Fallo:

> El tiro no consigue romper su preparación. El Espinajo mantiene el apoyo y se lanza.

La identidad es usar distancia, lectura y herramienta. No convertir el tiro en magia ni asumir fabricación todavía.

## Si el jugador ignora la oportunidad

No castigar con texto tutorial. Resolver mediante las reglas normales.

Texto sugerido:

> El Espinajo termina de afirmarse y se lanza.

El jugador sigue pudiendo atacar normalmente, defender según las reglas existentes o intentar huir. La capacidad de clase es una opción, no una pregunta de examen.

## Repetición

Para evitar sensación de escena guionizada:

- alternar una de las variantes de intención;
- mostrar la capacidad de forma contextual y breve;
- no repetir explicación pedagógica después de la primera aparición;
- conservar el nombre de la capacidad para que el jugador aprenda a reconocerla;
- los resultados pueden alternar frases equivalentes sin cambiar significado mecánico.

No se requiere RNG narrativo específico: Desarrollo puede seleccionar una frase estable en V1 y ampliar variantes después.

## Presentación en HTML/terminal

La intención enemiga debe ser visible como estado inmediato del combate, no enterrada en un párrafo anterior.

Cuando exista una intención preparada:
- terminal: una línea breve de aviso;
- HTML: acción contextual de la capacidad de la clase, junto a las acciones de combate pertinentes;
- nunca mostrar al jugador botones de capacidades de otras clases;
- el servidor sigue siendo autoritativo.

No introducir un panel nuevo si la UI actual puede presentar una acción contextual.

## Prueba humana mínima

Crear dos personajes de clases distintas y enfrentar el mismo patrón de embestida. La prueba pasa si, sin consultar documentación, el jugador puede explicar que tomó **dos tipos distintos de decisión** y no únicamente “usé otra arma”.

## Fuera de alcance

No fija daño, porcentajes, coste, cooldown, atributos, balance ni desbloqueo. No implementa las segundas capacidades de clase. No cambia canon del Espinajo.
