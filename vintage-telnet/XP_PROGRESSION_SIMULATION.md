# Vintage Telnet — Simulación de XP, cooperación y antifarmeo v1

**Fecha:** 2026-09-23  
**Estado:** EVIDENCIA DE BALANCE PARA `GAMEPLAY.md` SECCIÓN 22  
**Fuente normativa:** `vintage-telnet/GAMEPLAY.md`

## 1. Curva de XP aprobada

`XP_siguiente(L) = redondear(100 + 18×(L-1) + 0.25×(L-1)^2)`

Referencias:

| Nivel alcanzado | XP acumulada aproximada |
| ---: | ---: |
| 2 | 100 |
| 5 | 511 |
| 10 | 1,598 |
| 25 | 8,446 |
| 50 | 35,568 |
| 75 | 89,096 |
| 100 | 176,843 |

XP para subir desde niveles representativos:

| Nivel actual | XP siguiente |
| ---: | ---: |
| 1 | 100 |
| 5 | 176 |
| 10 | 282 |
| 25 | 676 |
| 50 | 1,582 |
| 75 | 2,801 |
| 99 | 4,265 |

La curva acelera de forma gradual sin introducir saltos artificiales.

## 2. Recompensa por categoría personal

| Categoría | % de XP de referencia |
| --- | ---: |
| Trivial | 2% |
| Favorable | 7% |
| Comparable | 12% |
| Peligroso | 20% |
| Abrumador | 25% |

La recompensa usa el nivel de referencia del enemigo y se limita al 25% del XP que el jugador necesita para subir.

Ejemplos sin grupo ni repetición:

| Caso | XP siguiente jugador | XP obtenida | % del nivel |
| --- | ---: | ---: | ---: |
| nivel 10 vs referencia 10 Comparable | 282 | 34 | 12.1% |
| nivel 50 vs referencia 50 Comparable | 1,582 | 190 | 12.0% |
| nivel 99 vs referencia 1 Trivial | 4,265 | 2 | ~0.05% |

Esto mantiene aproximadamente constante el número de encuentros apropiados por nivel y destruye el incentivo a farmear criaturas iniciales con un personaje veterano.

## 3. Prueba de power-leveling

Caso extremo:

- jugador nivel 1;
- enemigo referencia nivel 99;
- categoría Abrumador;
- dos participantes;
- el jugador bajo participa de forma significativa.

La recompensa se limita primero al 25% de su propio nivel y luego recibe el factor de grupo de 80%.

Resultado: **20 XP = 20% del nivel**, no varios niveles de una sola vez.

La v1 permite que jugar con alguien fuerte ayude, pero evita saltos masivos.

## 4. Cooperación

Con un encuentro Comparable, antes de repetición:

| Participantes | XP por jugador como % aproximado del nivel | XP total generado por el grupo |
| ---: | ---: | ---: |
| 1 | 12.0% | 12.0% |
| 2 | 9.6% | 19.2% |
| 3 | 8.4% | 25.2% |
| 4 | 7.2% | 28.8% |

Interpretación:

- cada individuo obtiene menos XP por una misma victoria;
- el grupo produce más progreso total;
- a cambio recibe seguridad, capacidad de afrontar retos mayores y velocidad de resolución;
- estar presente sin contribuir no otorga XP.

## 5. Antifarmeo

Ventana de repetición: últimas 10 victorias PvE.

| Veces que aparece la misma familia | Multiplicador |
| ---: | ---: |
| 1–3 | 100% |
| 4–5 | 60% |
| 6+ | 25% |

Simulación de un jugador matando únicamente enemigos Comparables de la misma familia:

- 3 primeras victorias: ~36% de nivel;
- 5 victorias: ~50% acumulado;
- 10 victorias: ~65%;
- 20 victorias seguidas: ~95%.

Por tanto, el jugador **puede** seguir progresando de esa forma, pero tarda mucho más que quien varía actividades.

Con respawns comunes alrededor de 5 minutos, veinte repeticiones idénticas no son una ruta óptima.

## 6. Ruta mixta

Ejemplo ilustrativo de una salida variada:

- 4 victorias Comparables: ~48%;
- 2 descubrimientos mayores: ~20%;
- 1 victoria Peligrosa: ~20%;
- 1 hito narrativo importante: ~15%.

Total orientativo: **~103% de un nivel**.

No significa que toda salida deba contener exactamente estas actividades. Demuestra que exploración + combate + narrativa pueden competir con el grind puro.

## 7. Especialistas y casuales

La recompensa se calcula según la dificultad **personal** del encuentro.

Consecuencia buscada:

- si una build especializada vuelve sencillo un enemigo, ese enemigo puede pasar a Favorable y aportar menos XP;
- un personaje casual para quien el mismo enemigo sigue siendo Comparable recibe la recompensa Comparable;
- el sistema no castiga al especialista, sino que lo empuja naturalmente hacia retos mayores apropiados a su potencia.

Esto es compatible con la regla previa de que una build casual no debe quedar inutilizada.

## 8. Evaluar peligro

La acción `evaluar <objetivo>` devuelve únicamente una categoría cualitativa.

Debe poder enriquecerse con señales, Percepción y conocimiento legítimo, pero no mostrar porcentajes de victoria ni estadísticas ocultas.

La clasificación sirve tanto para:
- ayudar al jugador a decidir;
- calcular el coeficiente de XP correspondiente.

La implementación puede afinar umbrales sin alterar las cinco categorías.

## 9. Resultado

La simulación satisface los casos pedidos por Issue #44:

- jugador casual solo: puede progresar con contenido Comparable;
- especialista solo: debe buscar retos más altos cuando trivializa contenido;
- dos principiantes: cooperación viable sin duplicar XP completo;
- jugador fuerte ayudando a débil: el tope evita saltos masivos;
- repetición de una criatura: sigue siendo posible pero ineficiente;
- explorador: puede obtener una parte importante de progreso sin matar.

El siguiente balance deberá hacerse con partidas reales y tiempos reales de combate/exploración.
