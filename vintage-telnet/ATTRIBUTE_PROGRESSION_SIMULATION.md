# Estudio experimental — Simulación de progresión de atributos

**Fecha:** 2026-09-21  
**Estado:** SIMULACIÓN EXPLORATORIA — NÚMEROS NO APROBADOS  
**Deriva de:** `RESEARCH_ATTRIBUTE_PROGRESSION.md`  
**Consumidor:** Diseñador de Jugabilidad con Javier/Matías

## OBJETIVO

Pasar de la comparación teórica a números de prueba para descubrir fallos antes de que Jugabilidad elija una curva.

Nada de este documento fija reglas. Los valores se eligieron para tensionar los modelos y poder compararlos.

## HIPÓTESIS COMÚN DE LABORATORIO

Para poder comparar usamos temporalmente:
- 8 atributos;
- todos comienzan en 10;
- 2 PA por subida de nivel;
- niveles observados: 10, 25, 50, 75 y 100;
- por tanto, PA acumulados desde nivel 1: 18, 48, 98, 148 y 198.

**2 PA/nivel NO es una recomendación.** Es una hipótesis de trabajo.

Builds conceptuales:
1. **Especialista puro:** prioriza casi exclusivamente un atributo.
2. **Doble especialista:** reparte prioridad entre dos.
3. **Equilibrado:** intenta mantener ocho atributos próximos.
4. **Irregular:** prioriza aproximadamente cuatro atributos con intensidades distintas y deja otros bajos.

## PRUEBA 1 — COSTE LINEAL PURO

Supuesto:
- cada +1 cuesta 1 PA;
- sin soft cap;
- sin hard cap alcanzable.

Un especialista que empezara en 10 y destinara todo a un atributo podría llegar teóricamente a:
- nivel 10: 28;
- nivel 25: 58;
- nivel 50: 108;
- nivel 75: 158;
- nivel 100: 208.

El equilibrado, distribuyendo 198 PA entre ocho atributos, termina alrededor de 34–35 cada uno.

### Hallazgo

La diferencia de identidad es enorme, pero también lo es el riesgo de **god stat**.

Si el atributo principal escala linealmente una función importante, el especialista de nivel 100 tendría aproximadamente seis veces el valor bruto del equilibrado en esa estadística.

No significa automáticamente seis veces más poder —depende de las fórmulas—, pero obliga a que todas las fórmulas derivadas absorban una amplitud gigantesca.

### Diagnóstico

**Falla como modelo autónomo.**

Podría funcionar si:
- los efectos derivados tienen soft caps fuertes;
- existe cap por nivel;
- o el atributo mostrado no entra linealmente en las fórmulas.

Pero entonces la simplicidad aparente del coste lineal se traslada a fórmulas más difíciles de explicar.

## PRUEBA 2 — COSTE CRECIENTE POR TRAMOS

Hipótesis experimental:

| Valor actual antes de subir | Coste del siguiente +1 |
|---|---:|
| 10–19 | 1 PA |
| 20–34 | 2 PA |
| 35–49 | 3 PA |
| 50+ | 4 PA |

No es propuesta final; se usa para observar comportamiento.

Coste acumulado desde 10:
- llegar a 20 = 10 PA;
- 25 = 20 PA;
- 30 = 30 PA;
- 35 = 40 PA;
- 40 = 55 PA;
- 50 = 85 PA;
- 60 = 125 PA;
- 70 = 165 PA;
- 80 = 205 PA.

### Especialista puro

Con 198 PA, no puede llegar a 80; termina aproximadamente en 78 si prácticamente todo se destina al atributo principal.

### Equilibrado

Con los mismos 198 PA, puede elevar los ocho atributos mucho más en suma total porque compra muchos incrementos baratos.

Si distribuye uniformemente, cada atributo puede situarse aproximadamente en la zona media de 20s/30s, dependiendo de cómo se gasten residuos.

### Interpretación

El especialista:
- conserva una cifra claramente extraordinaria;
- sacrifica muchísima suma total de atributos;
- sigue teniendo una meta incluso en nivel 100;
- no alcanza un techo artificial.

El equilibrado:
- tiene mayor suma de atributos;
- obtiene versatilidad;
- nunca alcanza el extremo del especialista.

### Riesgo

El salto exacto de 19→20 o 34→35 crea **breakpoints**. Un jugador experto puede optimizar quedándose justo antes de un tramo caro y repartiendo el resto.

Mitigaciones posibles:
- aceptar los breakpoints porque son fáciles de entender;
- suavizar la curva;
- usar tramos suficientemente amplios;
- mostrar siempre el coste del siguiente punto.

### Diagnóstico

**Buen candidato para simulación seria.**

Es fácil de explicar y mantiene diferencia entre especialista/generalista.

## PRUEBA 3 — LINEAL + SOFT CAP DE EFECTO

Hipótesis experimental:
- comprar atributo cuesta siempre 1 PA;
- valor mostrado puede crecer libremente;
- para una estadística derivada genérica:
  - primeros valores aportan efecto completo;
  - después de un umbral aportan ~50%;
  - después de otro, ~25%.

No se fija una fórmula definitiva.

### Ejemplo extremo

El especialista puede mostrar Fuerza 208 a nivel 100, pero la fórmula de daño no trata 208 como 208 unidades lineales de poder.

### Ventaja

La fantasía del especialista permanece:
“mi Fuerza es enorme”.

### Problema observado

A un jugador le resulta difícil valorar un PA:
- de 20→21 puede valer una unidad efectiva;
- de 60→61 quizá media;
- de 150→151 quizá una fracción.

Si la UI muestra solo el atributo bruto, el jugador no sabe cuánto compró realmente.

Si la UI muestra atributo bruto + valor efectivo, el sistema se vuelve más técnico.

### Diagnóstico

**Matemáticamente potente, pedagógicamente más difícil.**

Puede ser excelente para estadísticas derivadas con límites naturales —probabilidad de esquivar, crítico, mitigación— pero usarlo universalmente en los ocho atributos puede ser innecesariamente opaco.

## PRUEBA 4 — HARD CAP PURO

Hipótesis experimental:
- coste 1;
- cap de atributo 50.

Un especialista necesita solo 40 PA para llevar su atributo 10→50.

Con 2 PA/nivel lo logra aproximadamente alrededor del nivel 21 si invierte todo.

Después quedan ~158 PA hasta nivel 100 que necesariamente debe poner en otros atributos.

### Hallazgo

El sistema empieza especializado pero **converge**.

Con 198 PA totales y ocho atributos de 10→50, el coste de capear todos sería 320 PA. No llega a capearlos todos, pero el especialista pasa casi cuatro quintas partes de la campaña desarrollando cosas que no eran su prioridad original.

Si el cap fuera menor, convergencia empeora; si fuera mucho mayor, el cap deja de controlar el extremo.

### Diagnóstico

**No recomendable como mecanismo principal** para 100 niveles.

Sí conviene un hard cap técnico lejano como protección del motor/balance.

## PRUEBA 5 — HÍBRIDO SUAVE

Hipótesis:
- coste por tramos como en Prueba 2;
- atributo bruto conserva significado sencillo;
- soft caps NO universales;
- solo estadísticas derivadas que los necesiten usan rendimientos decrecientes;
- hard cap técnico queda fuera del rango normal de la primera etapa.

Ejemplo conceptual:
- Fuerza puede seguir dando capacidad física de forma entendible;
- una probabilidad derivada que no puede crecer indefinidamente sí usa curva/techo;
- equipo y poderes permanecen en sus capas separadas.

### Hallazgo

Evita el “doble castigo” si se usa con disciplina:
- el coste creciente ya controla el atributo;
- soft cap solo controla fórmulas que matemáticamente lo necesitan.

No se aplica coste creciente **y además** rendimiento decreciente a todo.

### Diagnóstico

**Es el candidato más flexible**, pero requiere más trabajo de diseño por atributo.

## PRUEBA 6 — CAP POR ETAPA

Hipótesis experimental:
- coste sencillo;
- el máximo permitido se abre en grandes hitos de nivel.

Ejemplo solo para estudiar comportamiento:
- niveles bajos: cap bajo;
- niveles medios: cap se amplía;
- niveles altos: cap vuelve a ampliarse.

### Ventaja

Evita que un personaje de nivel bajo vuelque absolutamente todo y obtenga una estadística desproporcionada.

### Problema

Si el jugador recibe PA que no puede gastar donde quiere:
- puede sentirse castigado;
- puede guardar PA;
- puede verse obligado a diversificar.

Entonces debemos decidir explícitamente si guardar PA está permitido. Esa decisión altera mucho el modelo.

### Diagnóstico

**Útil como barrera de seguridad secundaria**, menos atractivo como corazón del sistema.

## COMPARACIÓN EN NIVEL 100 BAJO LA HIPÓTESIS DE 198 PA

| Modelo | Especialista extremo | Generalista | PA altos siguen útiles | Claridad |
|---|---|---|---|---|
| Lineal puro | Excesivo | Mucha distancia | Sí | Excelente |
| Coste por tramos | Fuerte pero caro | Muy competitivo en suma | Sí | Alta |
| Lineal + soft cap | Bruto extremo, efectivo controlado | Competitivo | Sí | Media |
| Hard cap puro | Se frena pronto | Convergencia | Riesgo | Excelente |
| Híbrido suave | Fuerte/controlable | Versátil | Sí | Alta-media |
| Cap por etapa | Controlado artificialmente | Favorecido | Depende de banking | Alta |

## PRUEBA DE “¿SIGUE IMPORTANDO UN PA EN NIVEL 90?”

### Lineal
Sí, pero puede aumentar una estadística ya descontrolada.

### Coste creciente
Sí. Puede:
- ahorrar para el siguiente punto caro del atributo principal;
- comprar un punto barato secundario;
- completar un tramo.

Esto crea decisiones.

### Soft cap
Sí numéricamente, pero el beneficio marginal puede sentirse pequeño.

### Hard cap
Puede dejar de importar para la identidad principal si ya llegó al cap.

### Híbrido
Sí, siempre que los costes máximos no sean tan altos que hagan falta demasiados niveles para notar un cambio.

## PRUEBA DE ESPECIALIZACIÓN

Una meta de diseño razonable para Jugabilidad podría ser:

**un especialista de nivel 100 debe ser inequívocamente extraordinario en su atributo principal, pero no debe obtener suficiente poder total de ese atributo como para reemplazar las funciones de varios atributos.**

Esto no fija cuánto vale “extraordinario”. Define qué medir.

Ejemplo:
- Fuerza muy alta no debería automáticamente producir también máxima supervivencia, velocidad y percepción.
- Intelecto muy alto no debería automáticamente maximizar todas las capacidades mágicas si Voluntad/Percepción también tienen papeles reales.

La diversidad depende tanto de las fórmulas como de la curva de PA.

## PRUEBA DE DOBLE ESPECIALISTA

Con coste creciente, desarrollar dos atributos altos suele ser más barato que llevar uno a un extremo equivalente de gasto.

Eso crea una elección interesante:
- **pico:** una capacidad excepcional;
- **doble foco:** dos capacidades fuertes;
- **generalista:** muchas capacidades competentes.

Si las tres tienen usos reales en el mundo, aparecen builds distintas sin prohibiciones artificiales.

## PRUEBA DE EXPANSIÓN DESPUÉS DE 100

### Lineal
Se extiende trivialmente, pero la inflación empeora.

### Hard cap
Necesita mover el cap o crear otra progresión.

### Coste por tramos
Puede añadir un tramo posterior sin modificar los anteriores, siempre que el motor use tabla/configuración.

### Híbrido
Puede ampliar costes y ajustar fórmulas derivadas concretas.

**Resultado:** coste creciente/híbrido dejan más espacio estructural.

## SENSIBILIDAD A PA POR NIVEL

La hipótesis 2 PA/nivel no debe convertirse accidentalmente en regla.

Si fueran:
- 1 PA/nivel: 99 PA hasta nivel 100;
- 2 PA/nivel: 198;
- 3 PA/nivel: 297;
- 5 PA/nivel: 495.

Esto cambia radicalmente la curva.

Por ejemplo, con los tramos experimentales:
- llegar de 10 a 50 cuesta 85 PA;
- con 1 PA/nivel es una meta casi de campaña completa;
- con 5 PA/nivel puede alcanzarse relativamente temprano.

**Conclusión:** PA por nivel y coste de atributo deben balancearse juntos.

## NUEVA PREGUNTA: ¿DAR PA TODOS LOS NIVELES?

La decisión confirmada dice que cada subida entrega PA, pero no especifica cantidad.

Puede mantenerse esa satisfacción sin que cada nivel tenga idéntica cantidad:
- base constante;
- bonos en hitos;
- o cantidades que cambien por etapa.

No se recomienda nada todavía. Solo debe incluirse en simulación porque modifica la sensación de niveles 5/10/25/etc. y convive con PP cada 5 niveles.

## RIESGO DE DOS RECOMPENSAS EN NIVEL MÚLTIPLO DE 5

Como los poderes progresan cada 5 niveles y PA se obtienen al subir:
- nivel normal: PA;
- nivel múltiplo de 5: PA + progreso de poder.

Esto puede ser positivo: crea hitos fuertes.

Pero Jugabilidad debe evitar que el salto de poder de cada quinto nivel sea tan grande que los cuatro niveles intermedios parezcan relleno.

## RECOMENDACIÓN DEL ESTUDIO PARA LA SIGUIENTE RONDA

No elegir todavía números finales.

Descartar de la siguiente ronda como modelos autónomos:
- **lineal puro sin defensas**;
- **hard cap puro cercano**.

Mantener tres candidatos:

### A — Coste creciente por tramos
El más transparente.

### B — Híbrido suave
Coste creciente + soft caps solo en derivados que los necesiten.

### C — Lineal + soft caps
Mantener como control/comparación porque es simple de comprar aunque más opaco en efecto.

Y hacer la próxima simulación variando:
- PA/nivel = 1, 2 y 3;
- tres tablas de coste creciente (suave/media/fuerte);
- valores iniciales;
- especialista/doble/equilibrado;
- fórmulas reales de los ocho atributos cuando Jugabilidad defina qué hace cada uno.

## RESULTADO PRINCIPAL

La simulación preliminar favorece **no usar un único mecanismo para resolver todos los problemas**.

La opción que mejor preserva identidad de personaje y espacio hasta nivel 100 es estudiar seriamente:

**coste creciente visible para comprar valores altos + hard cap técnico lejano + soft caps únicamente en estadísticas derivadas que matemáticamente los necesiten.**

Esto sigue siendo una **hipótesis a validar**, no una regla aprobada.

El punto decisivo será la siguiente simulación: cuando Jugabilidad defina qué efectos produce Fuerza, Resistencia, Agilidad, Percepción, Intelecto, Voluntad, Destreza y Presencia, podremos medir poder marginal real y no solo números de atributo.
