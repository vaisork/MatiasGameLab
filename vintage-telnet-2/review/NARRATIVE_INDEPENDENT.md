# Revisión lectora independiente de la narración nueva

Revisión de los catálogos nuevos `content/regions/{veyra,hoshai,korven,lethra,nhal}.json`, sin imágenes ni reutilización de la prosa del juego anterior. No se han editado estos catálogos. Fecha: 5 de octubre de 2026.

La evaluación se refiere a identidad espacial, continuidad, ritmo, causalidad y cambios perceptibles de noche/lluvia. No se acepta la experiencia por longitud del texto ni por contar habitaciones.

## Recorrido y límites de evidencia

Se leyó un recorrido conectado mediante las salidas existentes: hogar Felaryn → Khariel → diez tramos del Camino Alto → rampa de Veyra → plaza de las rutas → patio de cargas → nueve tramos hacia Brumak → regreso por el mismo camino a Vaisgard → toldos y desagües → diez tramos de Lethra → Narevia → mercado, muelle y patio → relevo de raíces → ribera de Nhal → Velmora → patio del relato → umbral de Elin. También se leyeron los ramales del mirador/caseta de Hoshai, registro del cauce de Korven, archivo de Veyra y taller/banco de Lethra.

Ejecución real mediante `/tmp/new-reader-journey.py`: **65 movimientos autenticados**, en una base temporal, después de registrar una cuenta, crear el personaje y aprobarlo mediante los endpoints correspondientes. Se alcanzaron Hoshai, Veyra, Korven, Lethra y Nhal y se volvió por conexiones realmente ofrecidas. No se modificaron posición, conocimiento ni flags directamente. Los resultados completos, incluidas escenas, posibilidades y recuerdos, están en `/tmp/vt-new-narrative-walk.json`.

El recorrido API verifica continuidad y entrega del texto, pero no constituye prueba de navegador ni sesión humana de 20–30 minutos. La lectura independiente de ramales y variantes de noche/lluvia sigue siendo una inspección authored; no se afirma haber ejecutado todavía esas decisiones bajo todas las condiciones. El bloqueo inicial del catálogo de fauna quedó resuelto antes de ejecutar este recorrido.

## Lo que ya produce identidad propia

| Región | Diferencia que se reconoce sin depender del nombre | Continuidad y ritmo observados |
|---|---|---|
| Veyra | Empedrado, pendientes, muros antiguos reutilizados, canales pequeños, cargas con procedencias distintas y espacios públicos organizados por uso. | De mercado a plaza y patio se pasa de intercambio material a distribución de viajes y noticias. Archivar y corregir una demora tiene consecuencias sociales concretas. |
| Hoshai | Cambios de nivel, apoyos distintos para pie y rueda, ventanas lejanas que engañan sobre la distancia, agua fría y descansos donde reorganizar cargas. | La montaña comienza con grava y raíces, no con una pared extrema. La vuelta del cruce de agua cambia la perspectiva. Mirador → observación del nudo → comunicación → recomendación forma una cadena comprensible. |
| Korven | Juntas, cascajo, polvo retenido, pasos estrechos, sombra de paredes, puertas adultas bajas y maniobra de cargas. | La loma oculta gradualmente la ciudad; cauce y meseta alternan cierre y apertura. Brumak expresa una cultura mediante dimensiones y usos, sin copiar una fortaleza genérica. |
| Lethra | Suelo firme que se interrumpe, raíces, primeras tablas, agua con movimientos diferentes, pasarela curva y plataformas a distintas alturas. | El ave permite imaginar el ancho oculto del cauce. El parentesco de Mira/Sola y la invitación producen una razón humana para recorrer lugares sin combate. |
| Nhal | Hojas de distintas edades, huella fragmentada, referencias próximas, musgo pisado, sonido de trabajo antes de ver el asentamiento y luz dirigida a tareas. | El dosel se cierra progresivamente. Elin y la comida fría dan humor y un recuerdo doméstico preciso; ampliar un relato puede importar sin convertirlo en revelación cósmica. |

La noche cambia visibilidad y trabajo: tablillas guardadas, luz localizada en apoyos, agua que se oye más de lo que se ve, talleres que dejan de hacer ruido. La lluvia modifica superficies y posiciones: cargas separadas de herramientas, recipientes retirados, bancos desplazados, canalillos que recogen agua y hojas que se adhieren. Son diferencias físicas, no sólo etiquetas.

## Tres problemas prioritarios

### 1. La voz del documento de diseño invade la voz del mundo

La prosa explica repetidamente qué tropo, secreto o recompensa **no** se está creando. Ejemplos:

- `hoshai_caseta_revision.actions[hoshai_acordar_revision].text` habla de “sin inventar una caída ni convertirte en especialista de montaña”. Es una explicación del autor, no una respuesta vivida del mundo.
- `nhal_piedras_musgo.night` comenta que perseguir al animal no es necesario “para que la escena tenga un final”. Nombra la escena como artefacto.
- `nhal_claro_silencio.return` contrapone la pausa a “el desbloqueo obligatorio de un secreto”. Introduce una lógica de diseño en una experiencia de descanso.
- `hoshai_taller_apoyos.description` explica que el lugar no trabaja para hacer héroes; `korven_meseta_baja.description` aclara que dos piedras no son puerta ni altar. Esta estructura de negación se repite aun cuando nada observado planteó esa posibilidad.

El efecto conjunto es una voz docente bastante uniforme. En varias regiones las historias vuelven a la misma operación de localizar, atribuir, comparar y registrar. Esa coherencia da rigor, pero reduce la diversidad emocional de personas y situaciones.

**Propuesta concreta:** conservar las restricciones en documentación de autor y expresarlas dentro del juego mediante hechos. En la caseta, mostrar a Iria corrigiendo una nota y separando la tira gastada; no explicar que el juego evita una caída inventada. En el claro, dejar el asiento disponible, el sonido que continúa y una pausa familiar; no mencionar desbloqueos. Mantener el rigor de Nera/Oma, pero permitir que el humor de Elin, el vínculo de Mira/Sola y otras actividades no argumentativas sostengan cadencias distintas. No se necesita nuevo balance ni premios para lograrlo.

**Aceptación:** leer ocho a doce movimientos seguidos sin encontrar comentarios sobre escenas, recompensas, secretos obligatorios o decisiones del autor. Distinguir dos voces de personas por sus palabras y su motivo, sin encabezado con nombre.

### 2. Noche y lluvia cambian la descripción, pero algunas decisiones desmienten ese cambio

- `hoshai_mirador_nudo.night` afirma que el nudo ya no se distingue y que se guarda la revisión. La acción `hoshai_observar_nudo` sólo exige flags y aun así entrega una comparación precisa del desgaste.
- `hoshai_caseta_revision.night` presenta puerta cerrada y luz apagada; Iria no tiene un horario que retire su presencia, y las acciones de comunicar/acordar revisión mantienen su respuesta habitual.
- `korven_cauce_observacion.night` afirma que no se distingue cara limpia de polvo viejo. En lluvia, el polvo se borra y la comparación es menos clara. `korven_atribuir_cambio` permite registrar justamente el apoyo anterior visible en ese polvo, sin condición de iluminación o suelo.

Las variantes descriptivas son buenas; la contradicción aparece al elegir. En una aventura apoyada en interpretar señales, poder obtener información que la propia escena declara ilegible debilita la confianza en la lectura.

**Propuesta concreta:** conectar condiciones de observación/atención a disponibilidad y resultado authored. Decidir para cada caso entre posponer, ofrecer otra comparación realmente visible o recibir una observación anterior sin afirmar que acaba de verse ahora. Una caseta cerrada puede ofrecer dejar una nota si eso se escribe y autoriza; no debe tratarse automáticamente como la misma conversación presencial. El cliente debe representar el resultado del servidor, no esconder botones por interpretar una frase.

**Aceptación:** repetir los mismos tres casos de día seco, noche y lluvia. El texto leído antes de elegir, la posibilidad ofrecida y el hecho anotado después deben ser compatibles. No hacen falta nuevas penalizaciones numéricas.

### 3. Una indicación espacial promete una conexión que el recorrido no ofrece

En `veyra_patio_senales.description` aparece un corredor al norte hacia los hitos del Camino Alto. El objeto `exits` sólo permite oeste hacia la plaza y este hacia el archivo. Si el lector trata las direcciones como información útil, puede intentar una salida expresamente descrita y recibir un rechazo.

También conviene revisar frases que atribuyen una experiencia no asegurada por el estado. `veyra_puerta_alta.return` recuerda cómo se reorganizó la carga, aunque el paso no exige ni registra esa preparación; el retorno debería distinguir haber visto un lugar de haber ejecutado una tarea.

**Propuesta concreta:** contrastar toda instrucción cardinal de una descripción con salidas y conexiones existentes. En el patio, corregir la referencia si se trata de una vista o un camino alcanzable por la plaza, o autorizar la conexión si debe recorrerse directamente. En los retornos, basar reconocimiento en hechos registrados: reconocer la plataforma no implica haber ajustado allí una carga.

**Aceptación:** un lector puede seguir indicaciones cardinales sin probar salidas contradictorias. Al volver sin realizar una preparación opcional, el texto reconoce su visita y no le atribuye la acción que omitió.

## Integración de lectura y decisiones

El cliente nuevo muestra la `scene` actual y conserva `narrative` como respuesta de la última acción, eliminando espejos idénticos por tipo y texto. Una respuesta breve no sustituye toda la identidad del lugar. Las acciones authored siguen el orden del servidor y no quedan detrás de mirar/observar por una prioridad local fija. El historial permite releer hechos, y las decisiones escritas se resuelven por el servidor.

No se han ocultado contradicciones temporales ni inventado conexiones en el frontend. La corrección debe conservar la relación entre contenido, estado y posibilidades. No hay evidencia de navegador ni imágenes en esta revisión.

## Segunda revisión después de las correcciones

Se repitió el recorrido original de **65 movimientos API** con los catálogos corregidos. La continuidad sigue pasando. Después se ejecutó otro recorrido de **72 acciones reales**, que entra en los ramales del mirador/caseta de Hoshai, cauce de Korven, taller/plataforma/banco/cocina de Lethra y umbral de Elin. Los caminos se seleccionaron con el catálogo para esta prueba técnica; cada movimiento se envió mediante una acción disponible. No representa descubrimiento espontáneo de una persona. No se modificaron ubicación, flags o recuerdos por SQL.

`/tmp/vt-new-reader-branches.json` conserva respuestas completas y siete casos temporales controlados: nudo invisible de noche/reconocible de día; Iria ausente de noche/presente de día; polvo no interpretable en lluvia ni de noche, interpretable con día despejado. Cada acción vedada se intentó realmente y recibió rechazo HTTP, además de desaparecer de las posibilidades. El reloj era una dependencia de prueba aislada, no el reloj de producción.

**Acepto la corrección temporal:** la restricción es efectiva en el servidor, no una frase ni un botón oculto por el cliente. Las consecuencias de observar el nudo, comunicarlo y acordar la revisión se ejecutaron de día. También se ejecutó la atribución del cauce bajo condiciones compatibles.

**Acepto las correcciones de dirección y recuerdos:** el patio dirige a la plaza para alcanzar el Camino Alto y los retornos ya reconocen una visita sin atribuir preparación omitida. **Acepto la retirada de los metacomentarios señalados**, comprobada en las fuentes actuales. Se conserva el informe inicial arriba como evidencia de qué se corrigió, no como lista de defectos todavía vigentes.

### Valoración lectora del §6 del prompt

Escala 1–5. Es una revisión técnica y de lectura authored, no aprobación humana de una sesión ni de la interfaz renderizada. Un 4 indica que hay evidencia suficiente de esa capacidad en el alcance leído; no perfección.

| Categoría | Puntuación | Evidencia y límite |
|---|---:|---|
| Identidad espacial | 4 | Agua rápida/lenta y plataformas de Lethra; juntas, altura de puertas y maniobra en Korven; pendientes y ventanas engañosas de Hoshai. |
| Continuidad | 4 | 65 movimientos conectados, vuelta por el mismo camino y otros 72 actos hacia ramales. Las direcciones señaladas se corrigieron. |
| Ritmo | **3** | Alternancia de panoramas, trabajo y pausa, pero sucesión repetida de interpretación, comparación y registro en Hoshai/Korven. La prosa ya evita explicar al lector el diseño; falta mayor variación en el tipo de escena. |
| Vida ambiental | 4 | Trabajo, comida, recipientes, cargas, luces localizadas y NPC con presencia diurna real. Falta sesión humana para valorar cuánto se percibe sin buscarlo. |
| Densidad sensorial | 4 | Sonido de agua y tareas antes de ver su origen, polvo retenido, hojas adheridas y frío de agua; detalles que orientan, no sólo adornan. |
| Identidad regional | 4 | Las cinco regiones difieren mediante suelo, apoyo, usos y formas de ocupar el espacio. No se califica Edran en esta muestra. |
| Tiempo y clima | 4 | Siete controles API: escena, posibilidades y rechazo concuerdan en noche, lluvia y día despejado. No se han recorrido todos los sitios en todas las variantes. |
| Exploración | 4 | Ramales útiles sin combate obligatorio; conversar, reparar costura y seguir un relato cambian razones para volver. Recorrido técnico guiado por fuente, no descubrimiento humano. |
| Encuentros | **3** | Iria, Taren, Mira/Sola y Elin ofrecen actividad y motivo propios; abundan encuentros orientados a explicar o verificar información. Esta prueba no permite aprobar ritmo o legibilidad de combates. |
| Memoria | 4 | Acciones y retorno registran visita/hechos; nuevas variantes físicas tras costura/recipiente. Se evita atribuir automáticamente una preparación omitida. |
| Color semántico | **Sin nota visual** | Categorías del servidor llegan a `narrativeNode` y estilos de lectura en CSS. Contrato e inspección de código presentes; contraste, legibilidad y diferenciación reales pendientes de navegador. No se infiere un 4 desde CSS. |
| Curiosidad | 4 | Sonidos antes de asentamiento, distancia aparente frente a trayecto y vínculos entre taller, banco y cocina sugieren continuar sin exigir una recompensa. Requiere lector nuevo para verificar deseo real de seguir. |

### Prioridades que todavía impiden aprobar todo con 4

1. **Variar el ritmo de Hoshai/Korven:** conservar sus culturas de atención material, pero intercalar una escena con urgencia cotidiana o una actividad interrumpida donde la decisión sea ayudar, esperar o dejar espacio. Su consecuencia debe ser observable y pequeña; no añadir otra cadena de observar → atribuir → registrar. Esto requiere escritura original, no más párrafos del mismo patrón.
2. **Diversificar los encuentros:** mantener a las personas rigurosas, pero dar al menos una interacción sin función de tutor o registrador: una persona que esté terminando una tarea, solicite una intervención concreta o tenga una limitación práctica. La decisión debe alterar gesto, disponibilidad o conversación de retorno. Elin y el vínculo Mira/Sola ofrecen un comienzo que conviene extender sin repetirlo en todas partes.
3. **Cerrar evidencia pendiente:** revisión visual del color semántico y lectura humana de 20–30 minutos, además del encargo/cobro y relogin del plan. Las pruebas API y la ausencia de excepciones no autorizan una nota visual ni una nota de combate.

## Tercera lectura: encuentros y pausas nuevos

Se repitieron las 72 acciones y siete condiciones temporales, y se amplió el recorrido hasta **158 acciones públicas reales** para ejecutar las cuatro intervenciones nuevas. Evidencia: `/tmp/vt-new-lived-encounters.json`. En cada sitio se comprobó la disponibilidad, se eligió, se salió y se volvió mediante conexiones reales. La acción ya cumplida no volvió a ofrecerse; el retorno mostró una variante física. No se insertaron flags.

Las cuatro respuestas se distinguen por actividad y relación: Yesa libera la cinta del dedo y retoma su camino; Taren cambia el destinatario de una taza con humor; Nima ofrece caldo a su padre y reserva para sí una hoja; Desi termina un regalo que el niño interpreta a su manera. Las decisiones son sostener, hacer sitio y servir, en lugar de cuatro variantes de registrar información. El resultado no necesita entregar un objeto al jugador. Esto sí corrige la causa señalada para **encuentros: 4/5** y, combinado con las pausas breves nuevas, **ritmo: 4/5 en la muestra authored/API**. No se atribuye una nota humana de disfrute ni una revisión de combate.

Persisten dos ajustes de integración de texto observados en respuestas reales: el retorno de Yesa recuerda una «pausa que compartiste» después de elegir sostener el paquete, sin haber elegido sentarse; conviene nombrar la ayuda o distinguir las dos decisiones. El entrante de Taren conserva una capa de «la alfarera» con «su aprendiz» y una explicación de no convertirlo en escuela; debe mostrar a Taren y su trabajo después de la taza, sin voz del documento de diseño. Estos residuos están comunicados al autor y no se ocultaron en el cliente.

La nota de color semántico sigue pendiente de navegador. También quedan lectura humana, cobro/relogin observado y revisión efectiva de los encuentros de combate; esta ampliación no elimina sus límites.

## Muestra final independiente: Dravak y ramales no ajustados

Se ejecutó una cuenta/personaje Dravak nuevo en base temporal: Brumak → roca del Cascapedernal → meseta de relevo → garganta occidental de Hoshai → hombro/aprisco/collado → estación de cuerda → relevo alto de Nhal → roca, hogares, cocina y secadero → ribera de Lethra → barcas, orilla y raíces → retorno a la orilla. **86 acciones API**, **19 puntos de lectura**, amanecer/día/atardecer/noche presentes. Script reproducible: `review/api-reader-final.py`; respuestas y hashes: `review/API_READER_FINAL.json`. Datos de CSRF, cuenta y cookies no forman parte de la evidencia guardada. La selección del trayecto usa la topología authored como guía técnica; no se afirma descubrimiento espontáneo ni sesión humana.

Correcciones previas reejecutadas y conservadas en `API_CORRECTIONS_RECHECK.json`: Yesa reconoce sostener el paquete y ya no haber elegido sentarse. Taren cambia descripción personal al completar la taza; queda una capa de escena con alfarera/aprendiz que todavía no cambia junto a él. Las otras intervenciones mantienen consecuencias y acciones cumplidas retiradas.

### Calificación final del alcance leído

La tercera revisión había puntuado los cuatro encuentros nuevos. Esta muestra final amplía el alcance a ramales no ajustados y vuelve a encontrar las causas iniciales. Por eso no se generalizan aquellos 4/5 a todo el mundo.

| Categoría | Nota | Evidencia final |
|---|---:|---|
| Identidad espacial | 4 | Pedral→lajas→aprisco→árboles de altura→raíces/canal, con materiales y apoyos reconocibles. |
| Continuidad | **3** | Movimiento conectado pasa, pero tres descripciones indican conexiones cardinales inexistentes. |
| Ritmo | **3** | Pausas e intervenciones nuevas sí varían; ramales de relevo/roca/secadero vuelven a explicar, comparar, atribuir y registrar. |
| Vida ambiental | 4 | Rebaño retirado, faroles, tareas domésticas, barcas inclinadas y juguete en reparación; actividad material observable. |
| Densidad sensorial | 4 | Lajas reflejan farol, polvo en garganta, agua concentrada por dosel, sonidos y huellas de entrada ancha. |
| Identidad regional | 4 | Transición física entre Korven/Hoshai/Nhal/Lethra conserva diferencias sin corte instantáneo del paisaje. |
| Tiempo y clima | **3** | Siete guardas pasan y cuatro fases existen; en barcas se superpone revisión suspendida por lluvia con comparación diurna en curso. |
| Exploración | 4 | Ramales con observación, fauna y conversación disponibles; ninguna prueba necesitó combate para continuar. |
| Encuentros | **3** | Cuatro intervenciones vividas nuevas son buenas; en ramales intactos predomina cuidadora que explica/atribuye. No basta contar NPC o líneas. |
| Memoria | 4 | Corrección Yesa y estado físico de taza, caldo, figura; acción no reaparece al volver. |
| Color semántico | Pendiente visual | Contrato de categorías y CSS inspeccionados; no se ha visto el navegador. |
| Curiosidad | 4 | Fauna discreta entre roca, vista interrumpida y señales de presencia pesada permiten querer mirar sin exigir loot. Nota lectora, no prueba humana. |

### Tres causas pendientes, comprobables

1. **Promesa espacial contra salidas:** `nhal_secadero_sombra.description` ofrece senda al norte, pero sólo hay oeste; `nhal_calle_hogares.description` promete secadero al oeste, pero sólo sur/norte; `lethra_raices_observacion.description` dice regreso al norte, pero sólo este. Corregir perspectiva o conexión authored sin inferencia del cliente. Verificar cada frase orientadora con sus salidas reales.
2. **Voz de diseño y homogeneidad en ramales:** secadero explica que la paciencia no se premia con monedas; roca entre copas explica no celebrar un sentido sobre otro; relevo de altura declara reunir conocimientos/no eliminar viaje. Sustituir comentarios por acciones y voces propias, y romper al menos una secuencia de comparación/atribución con una actividad cotidiana que tenga una decisión distinta. Las cuatro intervenciones nuevas demuestran que se puede lograr.
3. **Capas incompatibles:** en barcas, lluvia suspende revisión sobre una superficie ya ilegible mientras la capa diurna muestra la unión y pide comparar la pérdida de agua. En el entrante, estado de Taren/taza todavía convive con aprendiz y otra operación de muestras. Seleccionar o escribir capas compatibles con clima/estado, sin ocultarlas localmente. Repetir respuesta completa de llegada y retorno, no sólo el fragmento cambiado.

Estos hallazgos se comunicaron al autor antes del cierre. La revisión técnica no aprueba visuales, combate, cobro ni sesión humana de 20–30 minutos. Quedan los límites documentados en `HUMAN_READING_SESSION.md`.

## Revisión de las correcciones globales y segunda muestra final

Se reejecutó el mismo recorrido Dravak de **86 acciones y 19 puntos de lectura**, con las cuatro fases, después de los cambios globales. Se revisaron individualmente las diez incompatibilidades del catálogo: **aceptadas**, con registro independiente de texto/exits/hashes en `SPATIAL_RECHECK.json`. No se inventaron nuevas conexiones. Las referencias a viviendas del secadero pasaron a ser vistas y las salidas reales quedaron explícitas. La lluvia en barcas muestra la unión cubierta y las herramientas recogidas; ya no superpone una comparación en curso. Al retirarse las capas `clear` antiguas, los estados no vuelven a recibir una actividad previa que los contradice.

Los cambios globales se ven también fuera de las cuatro intervenciones: el secadero responde mediante lado seco y juguete; el relevo muestra cómo dos cuidadoras orientan nota y cuerda; no hace falta una declaración del autor sobre premios para explicar la espera. Persisten formulaciones explicativas aisladas y algunas duplicaciones menores de dirección, pero no dominan la muestra como antes. Esto justifica revisar a **4/5** ritmo y encuentros en el alcance leído, sin convertirlo en 5 ni afirmar disfrute humano.

Se añadió un recorrido completamente distinto con personaje Humano: pozo → comedor → paños → cuidado → patio/carros y graneros → estanque → bajo húmedo → vuelta al estanque → sauces → puente → ramales de Lethra y vuelta. **66 acciones públicas reales, 19 puntos de lectura, cuatro fases**. Script: `api-reader-edran.py`; evidencia saneada y hashes: `API_READER_EDRAN.json`. La prosa de Edran permite alternar mesa con sitios reservados, pinzas vacías, luz sobre asiento, tronco/reflejo, ave y silencios largos. No se exige solucionar un problema o registrar una atribución en cada pausa. El retorno al estanque conserva la corriente y nivel observados; consultar, conversar y observar no transporta al personaje fuera de las salidas ofrecidas.

### Valoración lectora vigente después de cambios globales

| Categoría | Nota | Evidencia |
|---|---:|---|
| Identidad espacial | 4 | Sala de cuidados, paños, dos graneros, estanque partido por tronco y transición a plataformas húmedas. |
| Continuidad | 4 | Diez indicaciones corregidas, 86 + 66 acciones conectadas y retornos reales. |
| Ritmo | 4 | Intervenciones variadas y quietud breve de sauces/estanque; la interpretación de noticias ya no monopoliza estas muestras. |
| Vida ambiental | 4 | Cena tardía conserva lugares, rebaño recogido, herramientas cubiertas, aves con intervalos de silencio. |
| Densidad sensorial | 4 | Pinzas golpean, reflejo dividido, agua que sigue fuera de zona quieta, lámpara orientada y viento previo a las tablas. |
| Identidad regional | 4 | Edran llega a Lethra cambiando suelo, apoyo y circulación; el recorrido anterior preserva pedral, altura y dosel. |
| Tiempo y clima | 4 | Cuatro fases y siete guardas; capas de lluvia/estado compatibles en el caso problemático reejecutado. |
| Exploración | 4 | Ramales visitables, observar fauna y retirarse, conversaciones y regreso sin combate obligatorio. |
| Encuentros | 4 | Personas con tarea y vínculos, cuatro ayudas domésticas con cambios concretos; valoración de encuentros sociales, no aprobación de combate. |
| Memoria | 4 | Yesa distingue ayuda, taza/figura/caldo cambian estado y posibilidad; retorno al estanque mantiene lectura del sitio. |
| Color semántico | Pendiente visual | Sólo contrato y código inspeccionados. |
| Curiosidad | 4 | Borde firme frente a bajo húmedo, aves en hueco, marcas de presencia pesada y conexiones regionales dan razones para mirar. |

Esta valoración sustituye las notas lectoras previas para el contenido corregido, no borra los hallazgos ni amplía la evidencia a lo que no se hizo. El catálogo restante no recibió una sesión humana completa: la auditoría global espacial fue de fuentes, los recorridos son técnicos. Siguen pendientes navegador/color, lectura humana de 20–30 minutos, cobro/relogin observado en esa sesión y legibilidad de combate. No se declara perfección ni cierre visual.


Actualización por la petición de lenguaje claro: se reescribieron162 descripciones, se simplificaron141 nombres y se aclararon resultados y variantes. Las puntuaciones4/5 anteriores pertenecen al catálogo anterior y no se transfieren automáticamente. La revisión de prosa directa y sus hashes están en PLAIN_PROSE.md; no constituye aprobación visual ni una nueva sesión humana.
