# Ciclo 6 — implementar, rejugar y comparar memoria causal

Evaluación de agente por API real; no evaluación humana ni visual. BEFORE y AFTER usan `scripts/depth-cycle6-history.py`, dos cuentas en la misma base temporal y la misma secuencia exacta. Evidencias: `review/archive/2026-10-07/depth-cycle6-before.json` y `review/archive/2026-10-07/depth-cycle6-after.json`. No hubo escritura en usuarios/base reales ni edición de motor/mecánicas/world/client.

## Cambio y alcance

Se añadieron variantes personales de descripción/day/night/return/examine usando flags EXISTENTES: caja, placa, polea y recipiente retirados/entregados; notas de cornisa; preparación de paño/cubierta; aviso preciso/comprobación; amarre/perchas; recomendación base/aro; entrega de noticias en los tres encargos originales de Valdren. Se sustituyeron recuerdos contables de diez encargos por hechos propios de cada entrega. Nela y Ruma dan información espacial neutral que no contradice lo que recuerdan después. Nima comunica la elección sin imponer cocina cubierta cuando se escogió paño. Oren describe dónde colocó la caja en pasado y localiza la repisa, evitando asegurar que la caja sigue allí.

Las descripciones base de compuerta/cruce del almacén dejaron de imponer un hombre siempre presente. Las señales existentes siguen estableciendo presencia y peligro. Las variantes de victoria/rodeo recuerdan el lugar del encuentro sin prometer despoblación permanente ni cambiar el estado de otro jugador.

Se conservaron scopes y reglas de todas las acciones y conversaciones, objetos/cantidades, pagos, perfiles, requisitos y opciones de movimiento. Las reparaciones de mundo previas siguen compartidas. Recibir pago por una observación en Valdren no arregla una rueda, vacía un granero ni cambia el nivel del vado.

## Resultado reproducible

| Resultado de la sesión completa | Antes | Después |
|---|---:|---:|
| Movimientos reales | 687 | 687 |
| Checkpoints pareados dueño/observador | 20 | 20 |
| Encargos entregados y pagados | 10 | 10 |
| Recuperaciones interiores caja/placa | 2 | 2 |
| Sellos finales | 80 | 80 |
| HP finales | 55.9 | 55.9 |
| Regreso final | Hogar | Hogar |

Las listas completas de `(action,target)` son idénticas. Los diez flags de pago permanecen sólo en el protagonista; el observador no recibió ninguno. Caja/placa y sus flags personales permanecen aislados. La acequia se reparó usando la acción `edran_despejar_acequia`, de alcance mundo: ambos personajes ven la misma abertura limpia y corriente repartida. El script afirma esas relaciones mediante lecturas de la base temporal, sin mutarlas.

Pruebas complementarias: 14 casos de `test_real_content.py` pasan. `test_depth_history.HistoryBranchTests` añade una regresión significativa por API real: juega y entrega decisiones alternativas de revisión de cornisa, paño, perchas, comprobación del aviso y aro; sus escenas muestran la rama escogida y no la de base más ancha/cocina cubierta. No se inyectan flags para pasar la prueba.

## Comparación de experiencia y muestras sin nombres

Antes, Nela mandaba a comprobar una caja al fondo y acto seguido levantaba la que ya habías devuelto. Después sitúa la repisa y la salida; el recuerdo y la actividad muestran el resultado:

> Nela separa una cuña de la caja que devolviste y la compara con la toma de agua. El resto queda envuelto junto a su tablilla.

Al volver al fondo:

> La repisa quedó vacía donde recogiste la caja de cuñas; una marca rectangular conserva el borde seco.

El observador nuevo todavía ve su caja sobre la repisa: no se le atribuye una recogida ajena.

Antes, Ruma decía que faltaba una placa y luego mostraba la balanza montada, mientras el fondo conservaba esa misma placa. Después el dueño ve el hueco y los dos brazos completos:

> Los dos brazos de madera tienen sus placas sobre la mesa baja. Ruma encajó la que trajiste por las tres muescas del borde.

En el taller de la polea:

> Daren encaja la polea que trajiste en un apoyo del banco bajo. La tablilla de Seran queda junto al dibujo de los escalones; todavía compara las dos cuentas.

La recuperación devuelve un uso concreto; no resuelve automáticamente una disputa de cuentas.

En el secadero:

> El aro del recipiente quedó libre cuando recogiste la pieza de Elin. La tabla sigue sosteniendo el juguete en la franja de luz.

La entrega del recipiente pequeño no vacía por error el apoyo del recipiente histórico del relato: son objetos distintos. La versión compartida anterior del relato sigue utilizando sus propios flags.

En los encargos originales, Daro conserva la medida junto a la tiza; Elva archiva noticias de los dos espacios; Bren sitúa los dos cruces en su tablilla. El pago se expresa con un hecho recordado y el siguiente gesto, sin convertir cada diálogo en instrucciones sobre cómo funciona una quest.

## Auditoría de los diez encargos y dos interiores

| Encargo/sistema | Continuidad después de resolver |
|---|---|
| Polea | Hueco en cajas, pieza en taller, tablilla de cuenta conservada |
| Cornisa | Nota refleja revisión o cargas pequeñas; no inventa apoyos invisibles |
| Recipiente | Aro libre en secadero, tabla bajo juguete, pieza pequeña en Elin |
| Cuencos | Paño/cubierta reconocibles; estado de caldo servido conserva prioridad propia |
| Aviso | Preciso/comprobación conservan distinta certeza, carga sigue pendiente |
| Toldo | Amarre/perchas distintos, salida del agua y borde recordado |
| Taza | Base/aro quedan como marcas para prueba; no se entrega una pieza nueva |
| Medida del carro | Marca de tiza recuerda noticia; no repara automáticamente rueda |
| Espacios de reserva | Lista registra dos comprobaciones; no mueve cargas inventadas |
| Cruce de agua | Dos noticias atribuidas; no baja agua ni elimina fauna |
| Canal | Caja retirada y vuelta a Nela; compuerta geométrica y memoria de encuentro |
| Almacén | Placa retirada, brazo restaurado para protagonista, rutas conservadas |

El canon hidráulico y los ajustes de escalas Dravak se perciben ahora en consecuencias: cuñas comparadas con toma, placa ajustada por tres muescas, pequeñas cargas en mesa baja. No se identifica quién construyó Vaisgard ni se resuelve por texto una causa desconocida del horno.

## Autocrítica y problema nuevo antes de detenerse

**Lo mejor:** las entregas dejan rastros materiales y actividades propias. El regreso ya no contradice inventario e historial; la segunda cuenta prueba que recordar una misión personal no la da por resuelta para terceros. Las decisiones alternativas conservan incertidumbre en lugar de convertir todo aviso en una verdad confirmada.

**Lo débil:** las nuevas actividades son variantes persistentes. Daren seguirá encajando la misma polea y Nela seguirá separando una cuña en cada visita si no ocurre otra transición. La causalidad mejoró; la vida autónoma no quedó demostrada. En jornadas largas, el conjunto de descripciones de inventario visible puede ser excesivo aunque cada frase sea correcta.

**Aburrimiento/plantilla:** el texto contable dejó paso a objetos/gestos, pero algunos retornos se imprimen junto a una actividad que menciona el mismo objeto. No conviene resolverlo acumulando más capas. Los mejores momentos son los que alternan un reconocimiento pequeño con un uso, una voz o una pausa.

**Crítica importante nueva:** el presupuesto de tres capas todavía puede enfrentar memoria causal y clima. En las balanzas, la primera llegada del protagonista muestra la lluvia y el uso recuperado; en la entrada, el retorno de placa ocupa espacio mientras lluvia expulsa el gesto de Ruma. Son dos decisiones defendibles, pero la selección no siempre pone en primer plano la consecuencia que hizo valioso regresar. El contenido ya tiene el hecho; el selector necesita una prueba focal de clima/primera llegada/postmisión antes de otra corrección. Esta es una limitación observada en eventos, no una razón para elevar vida/ritmo a 4 por tener más prosa.

**Sistema infrautilizado:** `states` ahora expresa historia sin nueva arquitectura. `focus` y prioridades por situación pueden ayudar a seleccionarla; la futura intervención debe medir si mejora la lectura y conserva el clima. No se modificaron aquí para esconder la tensión de presupuesto.

**Canon aún invisible:** el interior hidráulico muestra uso/adaptación, pero la ciudad antigua en conjunto todavía no cuenta sus sucesivas reparaciones en el paseo de mercado. Una prueba de historia urbana y una sesión temporal completa siguen pendientes. La sesión dirigida de 687 movimientos no las sustituye.

| Criterio | Antes | Después |
|---|---:|---:|
| Identidad espacial | 4 | 4 |
| Continuidad espacial | 4 | 4 |
| Memoria causal | 2 | 4 |
| Vida ambiental | 3 | 3 |
| Ritmo | 3 | 3 |
| Curiosidad al regresar | 3 | 4 |

No se declara terminada la calidad narrativa. Vida ambiental y ritmo permanecen por debajo del umbral canónico; la siguiente prueba debe atacar selección de capas y variación temporal con evidencia, además de la ruta final ciega del catálogo completo.
