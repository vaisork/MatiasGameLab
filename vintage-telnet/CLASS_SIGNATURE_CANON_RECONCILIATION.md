# Vintage Telnet — Reconciliación canónica de capacidades firma

**Responsable:** Historiador y Constructor del Mundo — Vintage Telnet  
**Origen:** Issue #208 / Issue #216 / GAMEPLAY §36  
**Clasificación:** VALIDACIÓN DE CANON  
**Objetivo:** comprobar que la implementación mecánica propuesta para las cuatro capacidades firma conserva la identidad histórica/narrativa definida por Historia.

Este documento no cambia números, recargas, fatiga, fórmulas ni efectos mecánicos. Solo valida la coherencia de ficción y fija límites de interpretación para Desarrollo/Narrativa.

---

# Dictamen general

Las cuatro capacidades firma de GAMEPLAY §36 son **COMPATIBLES CON EL CANON DE CLASES** definido por Historia.

La implementación debe conservar esta lectura:

- **Juramentado:** sostener el peligro frontal.
- **Arcano:** alterar sobrenaturalmente la acción inmediata.
- **Sombra:** romper atención y convertir el error del enemigo en oportunidad.
- **Artífice:** intervenir a distancia mediante lectura, herramienta y precisión.

Ninguna debe representarse simplemente como “ataque especial con otro nombre”.

---

# 1. Juramentado — Guardia Comprometida

## Compatibilidad

GAMEPLAY §36.4 es compatible con la intención canónica de Guardia Comprometida:
- postura deliberada;
- compromiso frontal;
- interposición;
- reducción de consecuencia;
- control del intercambio.

## Aclaración de Historia

La versión original de CLASSES.md menciona que, en ficción, un Juramentado puede llegar a interponerse por otra persona si posición y espacio lo permiten.

Para la fase v1 de #216:
- esa posibilidad **permanece como potencial canónico futuro**;
- NO obliga a implementar protección de aliados;
- no debe simularse de forma falsa mientras no exista selección de objetivo suficiente.

La capacidad v1 protege al propio Juramentado.

## No representar como

- escudo mágico;
- aura;
- invulnerabilidad;
- reducción inexplicable sin postura;
- provocación sobrenatural del enemigo.

La lectura debe seguir siendo física y disciplinaria.

---

# 2. Arcano — Impulso Arcano

## Compatibilidad

GAMEPLAY §36.5 conserva el núcleo canónico:
- fuerza sobrenatural;
- alteración de trayectoria/ritmo;
- interrupción;
- no depende de daño directo;
- requiere foco.

## Aclaración de Historia

El texto canónico permite que Impulso Arcano produzca un efecto visible de fuerza.

Sin embargo:

**“interrumpir” no significa siempre “desplazar físicamente”.**

Según tamaño, postura y contexto, el resultado visible puede ser:
- vacilación;
- pérdida de línea;
- torsión del cuerpo;
- desviación;
- paso involuntario;
- golpe de aire;
- desplazamiento pequeño.

Contra una criatura enorme, el efecto puede alterar el ataque sin mover significativamente su posición.

Esto coincide con GAMEPLAY §36.5.

## No representar como

- proyectil elemental;
- bola de energía genérica;
- telequinesis libre;
- explosión;
- daño mágico obligatorio;
- empuje garantizado de cualquier enemigo.

---

# 3. Sombra — Borrar el Foco

## Compatibilidad

GAMEPLAY §36.6 conserva la identidad canónica:
- manipular atención;
- usar posición/contexto;
- no volverse invisible;
- aprovechar un fallo;
- crear una apertura.

## Aclaración de Historia

`focus_break_possible` debe leerse como **condición del entorno y de la percepción del enemigo**, no como poder sobrenatural del Sombra.

Contextos compatibles pueden incluir:
- cobertura;
- cambio de ángulo;
- terreno irregular;
- distracción;
- ruido;
- movimiento cruzado;
- obstáculos parciales.

No es necesario que siempre exista una pared o un objeto grande; basta con que la escena haga plausible perder la lectura limpia del movimiento.

## No representar como

- invisibilidad;
- teletransporte;
- duplicado ilusorio;
- desaparición total;
- pérdida automática de memoria del enemigo.

“Apertura” es oportunidad táctica, no efecto mágico visible.

---

# 4. Artífice — Tiro de Interrupción

## Compatibilidad

GAMEPLAY §36.7 es compatible con Historia:
- tiro deliberado;
- lectura del movimiento;
- intervención a distancia;
- interrupción de una acción;
- resultado dependiente de impacto.

## Aclaración de Historia

El Artífice no necesita que cada Tiro de Interrupción impacte una parte anatómica específica.

La ficción puede expresarse como:
- disparo al suelo inmediato;
- golpe a una extremidad expuesta;
- flecha que obliga a variar trayectoria;
- impacto contra una pieza/equipo cuando exista;
- tiro al punto donde el enemigo necesita apoyar el movimiento.

El resultado mecánico manda, pero la narración debe adaptarse al objetivo.

## No representar como

- flecha mágica;
- tiro que inmoviliza siempre;
- perforación garantizada;
- disparo imposible a través de obstáculos;
- “tiro crítico” renombrado.

---

# 5. Intención enemiga visible

Historia valida el uso de una intención enemiga visible porque permite que la identidad de clase se lea como **decisión** y no solo como estadística.

## Principio canónico

Una criatura puede mostrar que está a punto de actuar mediante:
- postura;
- cambio de respiración;
- tensión corporal;
- desplazamiento;
- sonido;
- erizamiento;
- fijación de mirada;
- preparación de carga.

La señal concreta debe respetar la biología de cada criatura.

No todas las criaturas deben usar la misma señal.

## Espinajo de rastrojo

El Espinajo es un caso adecuado para #216 porque su conducta territorial ya permite una advertencia corporal antes de una acción comprometida.

La intención visible no debe convertirlo en criatura inteligente que “anuncia un ataque”.

Debe seguir siendo lenguaje corporal animal.

---

# 6. Estado de las segundas capacidades

Historia confirma que las segundas capacidades siguen siendo válidas como siguiente escalón:

- Juramentado — **Paso de Ruptura**
- Arcano — **Velo de Contención**
- Sombra — **Finta de Vacío**
- Artífice — **Traba de Campo**

Pero **NO deben entrar en #216**.

Su existencia en canon no significa implementación inmediata.

La secuencia correcta es:

1. implementar capacidades firma;
2. playtest;
3. comprobar que las cuatro clases ya se reconocen por su decisión;
4. solo después abrir segundo escalón.

Esto coincide con GAMEPLAY §36.9 y #290.

---

# 7. Criterio de Historia para playtest

Además de los criterios mecánicos de Jugabilidad, Historia considera que la separación funciona si un observador puede leer un fragmento breve de combate sin ver el nombre de clase y deducir razonablemente cuál camino está actuando:

- sostiene la carga → Juramentado;
- altera sobrenaturalmente la carga → Arcano;
- rompe la atención → Sombra;
- interrumpe con tiro calculado → Artífice.

Si los cuatro relatos terminan siendo equivalentes a:

> “usa su poder y golpea al enemigo”

la implementación no está conservando la identidad canónica aunque los números sean correctos.

---

# Estado

**DICTAMEN: CANON COMPATIBLE / LISTO PARA DESARROLLO Y PLAYTEST.**

No se requieren cambios históricos para comenzar #216.

Las segundas capacidades permanecen reservadas para fase posterior.
