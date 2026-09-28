# Vintage Telnet — PROGRESSION-FEEL-01 / corte inicial de balance nivel 1–5

**Issue:** #483  
**Origen:** playtest humano de Javier, niveles 3–4  
**Objetivo:** separar falta de progresión real de falta de recuperación entre expediciones.

## 1. Fórmula vigente

HP máximo:

`100 + 1.25*(nivel-1) + 2.5*(Resistencia-10) + 0.5*(Voluntad-10)`

Competencia general:

`8*(nivel-1)/99`

PA:
- +2 por nivel;
- gastar PA en Resistencia aumenta HP;
- gastar PA en otros atributos no debe otorgar HP oculto.

## 2. Hallazgo principal

El crecimiento de HP por nivel **sin gastar PA en Resistencia** es pequeño:

| Nivel | HP base |
|---|---:|
| 1 | 100 |
| 2 | 101.25 |
| 3 | 102.50 |
| 4 | 103.75 |
| 5 | 105.00 |

Esto es deliberadamente menor que el efecto de especializar Resistencia.

Ejemplo de gasto balanceado aproximado, repartiendo PA entre Resistencia y Fuerza:

| Nivel | Resistencia | Fuerza | HP aprox. |
|---|---:|---:|---:|
| 1 | 10 | 10 | 100.0 |
| 2 | 11 | 11 | 103.75 |
| 3 | 12 | 12 | 107.50 |
| 4 | 13 | 13 | 111.25 |
| 5 | 14 | 14 | 115.00 |

Por tanto el nivel puede sentirse poco si el jugador invierte sus PA en atributos de identidad de clase y no en Resistencia. Eso no es automáticamente un bug: la identidad de clase debe venir también de #216.

## 3. Simulación de referencia

Modelo deliberadamente simple:
- intercambio básico;
- jugador ataca primero;
- criatura responde mientras siga viva;
- precisión/daño reales de C1 en `server/creatures.py`;
- arma Arcano = Varita base7;
- sin capacidad firma;
- sin defensa activa;
- sin provisión;
- sin herida/fatiga avanzada;
- fauna C1 menor disponible: Mordelinde, Uñapiedra, Rondamusgo, Garralaja, Silbarisco, Pinzajunco, Remojunco y Cascapedernal.

No sustituye playtest humano. Sirve para detectar cuál variable domina.

### Desde HP completo

Con PA balanceados Resistencia/Fuerza, el modelo no muestra una muerte matemática habitual tras solo tres C1.

Lectura:
- el combate C1 aislado no justifica por sí solo bajar fauna;
- la progresión por PA sí modifica supervivencia/tiempo de combate;
- falta incluir firma de clase #216 antes de cambiar crecimiento global.

### Desde respawn al 60%

El resultado cambia materialmente.

Referencia Monte Carlo de tres C1 aleatorios con Varita base7:

| Nivel | Inicio | Riesgo aproximado de morir antes de completar 3 |
|---|---:|---:|
| 1 | 60% HP | ~23% |
| 2 | 60% HP | ~12% |
| 3 | 60% HP | ~8% |
| 4 | 60% HP | ~4% |
| 5 | 60% HP | ~3% |

Para cuatro C1 desde 60%, el riesgo aumenta con fuerza y el HP restante típico cae a una banda que hace peligroso continuar.

El playtest real puede ser más duro que este modelo por:
- heridas;
- fatiga;
- composición concreta de fauna;
- decisiones defensivas fallidas;
- comenzar una nueva salida sin recuperación plena;
- arma/clase/PA reales.

## 4. Diagnóstico

El hueco prioritario NO es todavía “más HP por nivel”.

El bucle actual concatena:

`morir -> reaparecer ~60% -> descanso parcial -> no existe provisión/servicio -> salir otra vez incompleto -> acumular daño -> volver a morir`

Eso hace que la muerte funcione como comienzo de una expedición degradada en vez de como reinicio jugable razonable.

## 5. Veredicto provisional de Jugabilidad

**No modificar todavía la fórmula global de HP ni bajar C1.**

Primero integrar:
1. #410 recuperación pagada;
2. #409 ingreso real;
3. #216 capacidades firma;
4. #370 feedback visible de nivel.

Después repetir nivel1–5.

Cambiar HP antes de esas cuatro piezas corre riesgo de doble compensación.

## 6. Targets para el siguiente playtest

No son garantía por combate individual; son criterios de salud del bucle.

### Nivel 1
Desde preparación completa:
- dos C1 ordinarios deben ser una expedición razonable;
- el jugador debe poder decidir regresar después sin quedar matemáticamente condenado.

### Nivel 3–4
Desde servicio seguro (>=90% HP, fatiga0):
- tres C1 ordinarios deben ser sostenibles la gran mayoría de las veces;
- una provisión debe permitir extender razonablemente hacia un cuarto encuentro o asegurar regreso;
- seguir después debe ser decisión, no obligación.

### Nivel 5
Debe sentirse una mejora visible respecto a nivel1:
- más margen de HP si invirtió en Resistencia;
- mejor ejecución por PA;
- PP/capacidades ya empiezan a ampliar opciones;
- no se exige invulnerabilidad.

## 7. Trigger para recalibrar HP

Reabrir fórmula de HP/CG solo si, con #410 + #216 activos y preparación >=90%:

- nivel3–4 sigue muriendo habitualmente antes de completar 3 C1 ordinarios;
- o gastar PA razonablemente no produce diferencia perceptible;
- o un personaje de nivel4 preparado no llega apreciablemente más lejos que nivel1.

En ese caso evaluar primero:
1. coeficiente HP por nivel;
2. valor de Resistencia;
3. CG;
4. recién después números de C1.

## 8. Principio

**El nivel debe permitir llegar más lejos; la recuperación debe permitir volver a intentarlo; la fauna no debe ser debilitada para compensar la ausencia de ambos sistemas.**
