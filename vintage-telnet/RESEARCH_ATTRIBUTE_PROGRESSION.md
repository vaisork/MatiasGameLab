# VT-RES-003 — Progresión matemática de atributos y especialización

**Fecha:** 2026-09-21  
**Estado:** INVESTIGADO — NO ES BALANCE APROBADO  
**Solicitante:** Diseñador de Jugabilidad — Vintage Telnet  
**Consumidor:** Jugabilidad con Javier/Matías  
**Alcance:** comparar modelos matemáticos; no fijar números definitivos.

## PROBLEMA

Vintage Telnet tendrá una primera etapa de niveles 1–100, ocho atributos base y Puntos de Atributo (PA) que el jugador distribuye. Los Puntos de Poder (PP), obtenidos mediante otra progresión, son un sistema separado.

Falta decidir cómo convertir PA en crecimiento de atributos sin:
- hacer dominante invertir todo en una sola estadística;
- volver inútil la especialización;
- inflar números durante 100 niveles;
- hacer irrelevantes los PA de niveles altos;
- impedir una expansión posterior a nivel 100;
- mezclar atributos, equipo y poderes en una misma moneda.

## ESTADO ACTUAL CONFIRMADO

- niveles iniciales: 1–100;
- atributos: Fuerza, Resistencia, Agilidad, Percepción, Intelecto, Voluntad, Destreza y Presencia;
- rasgos de especie separados;
- PA distribuidos por decisión del jugador;
- PP separados de PA;
- hitos de poderes cada 5 niveles;
- poderes concretos pertenecen al contenido, no a esta investigación;
- valores iniciales, PA por nivel, costes, máximos y curvas todavía abiertos.

## DISTINCIÓN MATEMÁTICA IMPORTANTE

Hay tres palancas diferentes que pueden confundirse:

1. **Coste de comprar atributo:** cuántos PA cuesta subir el valor mostrado.
2. **Efecto del atributo:** cuánto cambia daño, vida, precisión, etc. al aumentar el atributo.
3. **Velocidad de obtención de PA:** cuántos PA recibe el jugador y cuándo.

Un sistema puede tener coste lineal pero efecto decreciente, o coste creciente pero efecto lineal. No es necesario resolver los tres problemas con una sola fórmula.

## EJEMPLOS DOCUMENTADOS

### BatMUD — costes crecientes y máximos ligados a progresión

BatMUD es especialmente relevante porque sigue siendo un MUD activo.

Su ayuda oficial indica que:
- a partir de cierto nivel se obtienen training points que pueden gastarse en estadísticas;
- habilidades/hechizos se entrenan por porcentajes;
- el coste de entrenamiento aumenta al subir el porcentaje;
- el nivel de guild determina máximos de entrenamiento;
- en determinados casos se puede entrenar por encima del máximo racial con coste fuertemente incrementado.

Esto combina **coste creciente + límites/umbrales + fuentes separadas de progreso**.

Lección adaptable: especializarse puede seguir siendo posible sin que el punto 90→91 tenga necesariamente el mismo precio que 10→11.

### Dungeons & Dragons — point buy creciente + hard cap

El point buy de D&D 5e 2014 usa coste creciente en creación: 8 cuesta 0; 9=1; 10=2; 11=3; 12=4; 13=5; 14=7; 15=9. Los dos últimos incrementos cuestan más.

Durante progresión, Ability Score Improvement permite repartir incrementos, pero normalmente no puede superar 20.

El Basic Rules 2024 también define 20 como máximo normal del aventurero salvo excepción específica.

Lección: **coste creciente temprano y hard cap** controlan extremos con reglas fáciles de explicar. Desventaja para un juego de 100 niveles: un hard cap cercano puede hacer que los PA dejen de interesar demasiado pronto si no existen otros destinos.

### Guild Wars 2 — capas separadas y tiers

GW2 separa varias fuentes de poder:
- atributos base crecen con nivel;
- equipo aporta combinaciones de atributos;
- traits/specializations son otra capa;
- las especializaciones se desbloquean con Hero Points;
- los costes dentro de una especialización aumentan por tiers;
- solo un número limitado de especializaciones puede estar equipado simultáneamente.

Históricamente también condensó trait points para que cada punto individual tuviera más significado.

Lección: no todo crecimiento debe pasar por el atributo. Separar atributos, equipo y capacidades especiales permite que el personaje progrese durante mucho tiempo sin hacer que una sola cifra absorba todo el poder.

### RuneScape / Old School RuneScape — crecimiento geométrico del coste de progreso

En RuneScape la experiencia necesaria para subir skills crece geométricamente. La documentación de RuneScape indica aproximadamente +10.4% en la separación de experiencia por nivel y que el total aproximadamente se duplica cada siete niveles; OSRS conserva la conocida consecuencia de que nivel 92 está aproximadamente a mitad del XP total hacia 99.

Lección: una campaña de ~100 niveles puede hacer que los niveles altos representen mucha más inversión sin necesitar que el poder obtenido por cada nivel crezca al mismo ritmo.

Esto es una curva de **coste de adquisición del nivel/skill**, no exactamente una moneda PA, pero demuestra por qué conviene separar “tiempo/esfuerzo para conseguir progreso” de “magnitud de poder entregada”.

### EverQuest clásico / Project 1999 — soft caps en estadísticas derivadas

La documentación comunitaria técnica de Project 1999 describe, por ejemplo, un soft cap de Armor Class ligado al nivel para parte de la mitigación. Más allá del soft cap el sistema puede seguir aceptando inversión/equipo, pero su tratamiento efectivo cambia.

Lección conceptual: un soft cap permite que una cifra continúe creciendo sin permitir que su beneficio efectivo conserve siempre la misma pendiente.

## MODELO 1 — COSTE LINEAL

Ejemplo conceptual:
- cada +1 de atributo cuesta 1 PA.

### Ventajas
- extremadamente fácil de entender;
- cada nivel y cada PA se sienten previsibles;
- UI simple;
- respec/reembolso sencillo;
- favorece libertad de construcción.

### Problemas
- si el beneficio también es lineal, maximizar la estadística que más multiplica la función principal del personaje suele ser atractivo;
- ocho atributos no garantizan diversidad si uno produce más poder marginal;
- para 100 niveles puede generar cifras muy altas;
- obliga a controlar especialización mediante caps, requisitos o fórmulas de efecto.

### Especializado vs equilibrado
El especialista paga exactamente lo mismo por su punto 50 que otro personaje por llevar un atributo secundario de 10 a 11. No existe fricción matemática contra extremos.

### Largo plazo
Es viable si el **efecto** tiene soft caps o si existen hard caps por tramo/nivel. Sin esas defensas, es el modelo con mayor riesgo de inflación/min-maxing.

## MODELO 2 — COSTE CRECIENTE

Ejemplo conceptual, sin números propuestos:
- tramo bajo: coste A;
- tramo medio: coste B > A;
- tramo alto: coste C > B.

O una función continua creciente.

### Ventajas
- especializar sigue siendo posible, pero tiene coste de oportunidad real;
- hace atractivos atributos secundarios cuando el principal ya está alto;
- controla inflación del valor mostrado;
- puede extenderse más allá de nivel 100 añadiendo tramos.

### Problemas
- si la curva es demasiado agresiva, el juego castiga al jugador por querer ser especialista;
- puede sentirse como “impuesto” oculto si no se muestra claramente;
- una fórmula compleja dificulta prever cuánto falta para una meta;
- guardar PA puede convertirse en estrategia óptima si el diseño de costes/umbrales lo incentiva.

### Especializado vs equilibrado
El especialista puede existir, pero sacrifica muchos incrementos baratos en otros atributos por pocos incrementos caros en su principal.

### Largo plazo
Muy adecuado para 100 niveles si los tramos son visibles y pocos.

## MODELO 3 — SOFT CAP / RENDIMIENTOS DECRECIENTES

Aquí el coste de +1 puede seguir siendo constante, pero el **poder efectivo** obtenido cambia después de ciertos umbrales.

Ejemplo conceptual:
- atributo mostrado 1–X: 100% de efecto marginal;
- X–Y: menor efecto marginal;
- Y+: aún menor.

### Ventajas
- el jugador puede decir “mi personaje tiene Fuerza altísima”;
- no bloquea fantasías de especialización;
- controla daño/defensa/precisión efectivos;
- permite equipo futuro sin romper inmediatamente el cap visible.

### Problemas
- el jugador puede sentir que le “roban” puntos si no entiende la conversión;
- requiere UI que explique valor bruto vs efecto;
- distintos atributos probablemente necesiten funciones distintas;
- soft caps demasiado fuertes crean un hard cap disfrazado.

### Especializado vs equilibrado
Permite extremos de identidad, pero reduce el rendimiento mecánico de seguir apilando la misma estadística.

### Largo plazo
Excelente como válvula de seguridad, especialmente para equipo y expansiones, pero no necesariamente ideal como único control de PA.

## MODELO 4 — HARD CAP

Un atributo no puede superar cierto valor, ya sea global o condicionado por nivel.

### Ventajas
- muy claro;
- balancea el espacio de estados;
- impide cifras absurdas;
- facilita diseñar contenido contra máximos conocidos.

### Problemas
- cuando el jugador alcanza su atributo favorito, PA posteriores pueden sentirse obligatoriamente desviados;
- muchos personajes convergen al final si hay PA suficientes para capear todo;
- expansión posterior requiere subir caps o crear otra progresión;
- un cap demasiado temprano mata especialización.

### Especializado vs equilibrado
El especialista llega antes al máximo y luego necesariamente diversifica.

### Largo plazo
Útil como **techo de seguridad**, pero arriesgado como mecanismo principal de una campaña de 100 niveles.

## MODELO 5 — HÍBRIDO POR TRAMOS

Combina:
- coste bajo/lineal en rango inicial;
- coste creciente en rango de especialización;
- posible soft cap en la conversión a estadísticas derivadas;
- hard cap lejano como seguridad;
- límites o accesos por nivel si fueran necesarios.

### Ventajas
- fácil de explicar si hay pocos tramos;
- el comienzo permite experimentar;
- el medio permite especializar;
- el final evita explosión;
- puede reservar espacio después de 100;
- separa identidad (“tengo 70 Fuerza”) de impacto real si una fórmula derivada necesita soft cap.

### Problemas
- más reglas que un modelo puro;
- requiere simulación para encontrar breakpoints;
- una mala combinación de coste creciente + soft cap puede castigar dos veces al especialista.

### Especializado vs equilibrado
Puede calibrarse para que ambos sean viables: el especialista compra puntos más caros pero conserva ventajas reales; el equilibrado obtiene más suma total de atributos y versatilidad.

## COMPARACIÓN DIRECTA

| Modelo | Comprensión | Especialización | Control inflación | Nivel 100 | Expansión >100 |
|---|---|---|---|---|---|
| Lineal puro | Muy alta | Muy alta / riesgo de dominante | Bajo sin otras reglas | Riesgoso | Fácil matemáticamente, riesgoso en poder |
| Coste creciente | Alta si es por tramos | Permitida con coste | Alto | Bueno | Bueno |
| Soft cap | Media | Identidad alta, poder controlado | Alto | Bueno | Muy bueno |
| Hard cap | Muy alta | Se detiene al cap | Muy alto | Puede converger | Requiere mover cap/otra capa |
| Híbrido | Media-alta | Ajustable | Muy alto | Muy bueno | Muy bueno si deja headroom |

## CÓMO EVITAR QUE UN SOLO ATRIBUTO SEA DOMINANTE

La curva de costes no puede arreglar por sí sola un atributo que hace demasiadas cosas.

BatMUD muestra que sus estadísticas afectan conjuntos distintos de capacidades, aunque algunas sean importantes para muchos personajes. D&D también distribuye checks, ataques y salvaciones entre distintas abilities.

Para Vintage Telnet, Jugabilidad debería comprobar posteriormente:
1. cuántas fórmulas usa cada atributo;
2. si un atributo mejora simultáneamente ataque, defensa y recursos;
3. si existen situaciones frecuentes donde atributos secundarios importan;
4. si dos atributos diferentes pueden resolver problemas similares de maneras distintas;
5. poder marginal de +1 en cada atributo a valores bajos, medios y altos.

Si Fuerza produce 3 veces el valor marginal de Presencia, encarecer Fuerza solo oculta un problema semántico de atributos.

## ATRIBUTOS, EQUIPO Y PODERES

La evidencia comparada favorece **capas separadas**.

Vintage Telnet ya ha tomado una buena decisión estructural al separar PA y PP.

Una arquitectura de balance sana puede distinguir:
- **atributos:** capacidad general persistente;
- **equipo:** modificadores/propiedades reemplazables y situacionales;
- **poderes:** nuevas decisiones/capacidades, no simplemente +N al atributo;
- **rasgos de especie:** naturaleza del personaje, no comprada con PA.

Esto reduce presión para que cada nivel tenga que entregar una enorme subida numérica.

## PROBLEMA ESPECÍFICO DE 100 NIVELES

Con 99 subidas después de nivel 1, incluso 1 PA por nivel ya crea una reserva sustancial además de puntos iniciales. Si fueran varios PA por nivel, el espacio crece rápidamente.

Por eso el modelo debe probar:
- concentración máxima posible en 1 atributo;
- concentración en 2;
- reparto equilibrado en 8;
- cuánto cambia cada build a nivel 10, 25, 50, 75 y 100;
- qué porcentaje del máximo teórico se alcanza a cada hito;
- si sobran PA cuando los atributos relevantes llegan a caps;
- qué ocurre si equipo añade valores por encima del rango normal.

No se fijan aquí cantidades; son escenarios obligatorios para la simulación posterior.

## CÓMO DEJAR ESPACIO DESPUÉS DE NIVEL 100

No diseñar ahora niveles infinitos.

Sí conviene evitar fórmulas cuyo significado dependa de que “100 es el máximo eterno”.

Técnicas compatibles:
- hard cap técnico mayor que el máximo alcanzable en la primera etapa;
- tramos de coste parametrizados;
- funciones de efecto con soft cap que continúen definidas;
- equipo separado de PA;
- poderes separados de PA;
- guardar la curva de progresión como datos/configuración, no dispersa en código;
- versionar reglas si en el futuro cambia el balance.

RuneScape muestra una estrategia distinta: nivel 99 fue durante mucho tiempo un hito reconocible y algunos skills posteriormente obtuvieron contenido real hasta 120, sin que todos tuvieran que ampliarse de la misma manera.

## EXPLOITS / FALLOS A BUSCAR EN SIMULACIÓN

1. **Dump stat:** un atributo puede ignorarse sin coste real.
2. **God stat:** uno domina demasiadas fórmulas.
3. **Breakpoint gaming:** quedarse exactamente antes/después de un tramo siempre es óptimo.
4. **PA banking:** no gastar hasta alcanzar cierto nivel es matemáticamente superior.
5. **Cap convergence:** al 100 todos terminan casi iguales.
6. **Specialist trap:** especializar parece divertido pero produce peor personaje en todo.
7. **Generalist tax:** repartir siempre pierde contra maximizar una estadística.
8. **Gear bypass:** equipo permite saltarse el control de atributos.
9. **Double diminishing:** coste creciente + soft cap castigan excesivamente el mismo incremento.
10. **Dead high-level PA:** un PA al nivel 90 ya no compra nada interesante.

## 4 MODELOS CANDIDATOS PARA SIMULAR

Estos NO son recomendaciones definitivas ni incluyen números.

### Candidato A — Lineal + soft cap de efectos
- PA compra atributos a coste constante.
- Las fórmulas derivadas aplican rendimientos decrecientes después de umbrales.
- Hard cap técnico lejano.

**Pregunta de simulación:** ¿es suficientemente transparente para niños/jugadores nuevos cuando el valor mostrado y el poder efectivo divergen?

### Candidato B — Coste creciente por tramos
- El atributo compra +1 normalmente.
- El precio en PA aumenta en pocos tramos visibles.
- Efecto del atributo permanece lo más lineal posible.
- Hard cap técnico lejano.

**Pregunta:** ¿qué diferencia de coste permite especialistas reales sin hacerlos obviamente superiores o inferiores?

### Candidato C — Híbrido suave
- Primer tramo barato para permitir experimentar.
- Segundo/tercer tramo con coste creciente.
- Soft cap solo en estadísticas derivadas que realmente lo necesiten (por ejemplo porcentajes con límites naturales), no universal.
- Hard cap de seguridad lejano.

**Pregunta:** ¿podemos mantener una explicación sencilla evitando castigar dos veces la especialización?

### Candidato D — Cap de especialización por etapa
- Coste simple.
- El máximo invertible en un atributo depende de hitos amplios de nivel/progresión.
- Los caps se abren gradualmente.
- El jugador puede guardar PA o diversificar según la regla que Jugabilidad decida.

**Pregunta:** ¿los caps por etapa se sienten como progreso o como restricción artificial?

## QUÉ DEBE HACER JUGABILIDAD DESPUÉS

Antes de elegir:
1. fijar rangos candidatos de valor inicial;
2. fijar 2–3 hipótesis de PA por nivel;
3. simular A–D a niveles 10/25/50/75/100;
4. construir al menos cuatro builds: especialista puro, doble especialista, equilibrado y deliberadamente extraño;
5. comparar poder marginal, no solo suma de atributos;
6. probar con y sin equipo;
7. comprobar qué queda disponible después de 100;
8. recién entonces elegir costes/caps.

## FUENTES

- BatMUD — Levels: https://www.bat.org/help/help?htype=basic&str=levels
- BatMUD — Train: https://www.bat.org/help/help?htype=basic&str=train
- BatMUD — Getting Started: https://www.bat.org/help/help?str=getting_started
- BatMUD — Stats: https://www.bat.org/help/help?htype=basic&str=stats
- D&D Beyond — 2014 Basic Rules, Step-by-Step Characters / point buy: https://www.dndbeyond.com/sources/dnd/basic-rules-2014/step-by-step-characters
- D&D Beyond — 2024 Basic Rules, ability scores: https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game
- D&D Beyond — Ability Score Improvement: https://www.dndbeyond.com/feats/1789092-ability-score-improvement
- Guild Wars 2 Wiki — Attributes: https://wiki.guildwars2.com/wiki/Attribute
- Guild Wars 2 Wiki — Traits/Specializations: https://wiki.guildwars2.com/wiki/Trait
- RuneScape Wiki — Experience: https://runescape.wiki/w/Experience
- Old School RuneScape Wiki — Experience: https://oldschool.runescape.wiki/w/Experience
- Project 1999 Wiki — Statistics/AC soft cap: https://wiki.project1999.com/HP

## CONCLUSIÓN

La evidencia no apunta a una única fórmula universal.

Para una campaña de 100 niveles, **lineal puro sin ninguna otra defensa es el modelo que más depende de que los ocho atributos estén perfectamente equilibrados**. Hard cap puro controla bien el poder pero corre el riesgo de hacer converger personajes o matar el interés de PA.

Los modelos que más merece la pena simular son los que separan claramente:
- cuánto cuesta comprar atributo;
- cuánto poder efectivo produce;
- qué otras capas de progreso existen.

BatMUD aporta un precedente especialmente relevante de costes crecientes y máximos dentro de un MUD; D&D muestra point buy creciente y caps; GW2 muestra separación de capas y tiers; RuneScape muestra cómo una curva creciente sostiene progresión larga.

**Siguiente paso correcto: simulación, no decisión intuitiva.** Jugabilidad debe probar los cuatro candidatos con números hipotéticos antes de convertir alguno en regla.


## SIMULACIÓN POSTERIOR

La comparación numérica exploratoria solicitada por Javier fue realizada y está documentada en:

`vintage-telnet/ATTRIBUTE_PROGRESSION_SIMULATION.md`

La simulación usa valores deliberadamente hipotéticos y NO convierte 2 PA/nivel ni ninguna tabla de costes en regla.

Resultado preliminar: lineal puro y hard cap cercano presentan problemas claros a 100 niveles. La siguiente ronda debería concentrarse en coste creciente por tramos, híbrido suave y lineal + soft caps como control, variando PA/nivel y, sobre todo, incorporando los efectos mecánicos reales de los ocho atributos cuando Jugabilidad los defina.
