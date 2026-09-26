# Wark — ficha piloto de recorrido: Valdren ↔ Narevia

**Fecha/base:** 2026-09-26; `main` 271a92e; contraste con `historia/vt-malla-regional-212` b30377e.  
**Clasificación:** PROPUESTA PENDIENTE para Historiador, Narrador y Jugabilidad.  
**Objeto:** Camino de la Tierra Húmeda, conexión periférica propuesta en #212. No es la ruta radial Valdren–Vaisgard ni Narevia–Vaisgard.

## Promesa del trayecto

El jugador sale de suelo que conoce por surcos y cercas y llega a un paisaje donde el agua obliga a leer la superficie antes de pisar. El cambio debe hacerse perceptible en varias señales, no en una puerta que anuncia “ahora estás en Lethra”. Puede viajar en ambos sentidos y entender el proceso inverso.

La rama histórica ya nombra **Campos Bajos**, **Puente de Madera Ancha**, **Los Primeros Juncos**, **La Orilla Partida**, **Vado de Juncos**, y los ramales **Molino Hundido** y **Sendero de los Charcos Negros**. Esta ficha ordena funciones de experiencia alrededor de esos elementos; sus nombres y hechos siguen pendientes de incorporación a `main`.

## Secuencia funcional, sin fijar número de habitaciones

| Etapa | Lo que se ve/oye | Decisión legible | Regreso y lectura |
| --- | --- | --- | --- |
| 1. Salida de Edran | Tierra firme, cultivos y huellas de carro reconocibles | Elegir entre ruta principal y señales locales de trabajo, sin salida falsa obligatoria | El terreno seco y el camino ancho indican la dirección de Valdren |
| 2. Campos Bajos | Zanjas y vegetación más alta; marcas de agua en objetos ordinarios | Observar si el suelo sigue siendo firme antes de tomar una huella lateral | Las zanjas vuelven a dar paso a parcelas más elevadas |
| 3. Puente de Madera Ancha | Cruce practicable y reparaciones de épocas distintas, sin atribuir causa histórica nueva | Cruzar o detenerse a mirar el cauce; un desvío hacia el Molino Hundido puede anunciarse desde aquí | El puente es un hito doble: se reconoce desde ambos lados |
| 4. Vado de Juncos | Pequeño asentamiento/refugio propuesto por Historia, entre tierra y pasarela | Buscar orientación sobre la siguiente transición; no asumir tienda, curación, guardado ni NPC fijo | Punto al que regresar antes de investigar desvíos |
| 5. Primeros Juncos | Vegetación acuática continua y menos huellas de carros | Reconocer que la pista de orientación ahora son bordes de agua y pasarela | Los primeros juncos dejan de ser continuos al volver hacia el vado |
| 6. Orilla Partida | Un camino firme y una pasarela bordean el agua y se relacionan más adelante, según confirme Historia | Elegir mirando señales de uso y estado del suelo; ninguna opción debe anunciarse como «la correcta» sin fundamento | Hacer reconocible el punto donde ambas variantes vuelven a unirse |
| 7. Aproximación a Narevia | Canales, pequeñas islas y organización cotidiana Marevyn ya establecida en `SETTLEMENTS.md` | Continuar al pueblo o volver a investigar un ramal pendiente | Agua y pasarelas más integradas en la vida diaria indican que se llegó |

Estas etapas pueden corresponder a una o varias salas. La escala física, acciones y costos no se deducen de la longitud del texto.

## Dos desvíos con promesas diferentes

**Molino Hundido — investigación visible.** Historia propone restos de una instalación de agua fuera de uso, parcialmente visibles. Desde la ruta se pueden advertir restos sobre el cauce; investigar debe poder devolver información observada aun sin premio material. No fijar quién lo construyó, por qué se abandonó ni qué hay debajo. Narrador decide pistas y escena. Historiador decide verdad histórica.

**Sendero de los Charcos Negros — incertidumbre y riesgo anunciado.** La rama histórica lo describe como desvío de suelo saturado conocido como mala ruta en ciertas épocas. Su entrada debe distinguirse de la ruta principal mediante agua estancada, huellas que se pierden y alguna señal comprensible antes del riesgo. “Mala ruta” no implica daño automático, trampa, jefe ni arma perdida. Jugabilidad decide accesibilidad y consecuencias; Historia define lo que existe al fondo.

Ambos ramales deben permitir volver al camino. Si un futuro diseño crea una mazmorra o jefe, requerirá un encargo de Historia, Narrativa y Jugabilidad independiente.

## Fauna: material disponible y frontera pendiente

`CREATURES.md` contiene Mordelinde y Espinajo en Edran; Pinzajunco y Saltalodo en Lethra, además de amenazas superiores regionales. La transición puede usar rastros que cambian de carácter, pero esta ficha **no asigna especies a salas**, no mezcla automáticamente hábitats ni crea criaturas nuevas. Historia valida compatibilidad ecológica; Narrador redacta señales concretas; Jugabilidad regula encuentros y riesgo.

## Prueba de mesa del recorrido

Dar al lector descripciones breves de las etapas 2, 4 y 6 sin mostrar un mapa completo. Pedirle elegir hacia dónde volvería y qué pista seguiría para investigar el molino. Si no puede justificar la dirección con dos referencias distintas, la orientación necesita mejores señales. En una segunda pasada en sentido Narevia → Valdren, comprobar que el cambio de pasarela a suelo firme cuenta una experiencia coherente.

Medir por separado: tiempo de primera lectura, decisiones, vueltas voluntarias, encuentros, descansos y relectura. El objetivo conversado de seis a ocho horas corresponde al mundo recorrido con retos y retornos; esta ficha no reclama una duración específica.

## Handoff

- **Historiador:** confirmar el corredor #212 en `main`, su relación con Vado de Juncos y la geometría de la bifurcación; resolver solo los hechos que Narrador necesite.
- **Narrador:** escribir escenas breves de ida y vuelta, señales observables antes de ambos desvíos y un descubrimiento que recompense atención sin misión artificial.
- **Jugabilidad:** decidir si los dos trazados de Orilla Partida son transitables desde el inicio, qué significa descansar en el vado, qué se registra en el mapa, consecuencias de desviarse y si algún hallazgo merece XP.
- **Arquitecto:** coordinar orden de integración de canon, escenas y futura implementación sin tomar esta ficha como especificación de código.
- **Wark siguiente ciclo:** revisar cambios nuevos de estas ramas y preparar una ficha equivalente para un corredor distinto o refinar esta según validación; registrar las diferencias.

**No contiene material de `SECRETS.md` ni `NARRATIVE_RESERVED.md`.**
