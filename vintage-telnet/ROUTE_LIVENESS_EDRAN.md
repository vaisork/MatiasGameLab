# WORLD-LIVENESS — Camino de los Campos / Edran → Veyra

Origen: cola Narrativa #284 / ola #558.

Objetivo: añadir micro-presencia opcional a salas existentes para que el viaje cambie ligeramente entre visitas sin crear NPC persistente, quest, loot ni mecánica.

Uso: como línea secundaria de `room_view` o `mirar`; máximo una por sala cuando no haya combate ni escena scripted.

| room_id | micro-presencia |
| --- | --- |
| `valdren_lindero_tres_piedras` | “Una huella reciente cruza el lindero sin seguir ninguna cerca. El camino sigue siendo el paso más usado.” |
| `valdren_camino_hundido` | “En el borde del camino queda una reparación reciente de tierra compactada y piedra menuda.” |
| `valdren_cobertizos_viejos` | “Uno de los cobertizos muestra una puerta abierta y señales de uso reciente, aunque nadie te llame desde dentro.” |
| `valdren_cruce_cercas` | “Las huellas se separan en más de una dirección y vuelven a concentrarse sobre la ruta principal.” |
| `valdren_campo_rastrojo` | “El rastrojo se mueve por franjas y deja ver pasos recientes entre zonas de tierra en descanso.” |
| `valdren_zanja_vieja` | “Alguien retiró ramas y tierra de un tramo corto de la zanja para que el agua siga pasando.” |
| `valdren_arbol_descanso` | “Hay tierra recién pisada bajo la sombra y una marca de carga apoyada contra el tronco.” |
| `valdren_campos_sin_cerca` | “Unas huellas de carro cortan el camino y se pierden hacia tierras abiertas sin formar una ruta nueva.” |
| `valdren_vado_menor` | “Varias piedras del paso están húmedas y una de ellas fue recolocada hace poco.” |
| `campos_loma` | “Desde la loma se distingue polvo levantado muy lejos por otro viajero, demasiado distante para reconocerlo.” |
| `campos_mojon` | “El borde del mojón tiene una reparación pequeña con piedra distinta a la original.” |
| `campos_camino_compartido` | “Las huellas ya no parecen venir de un solo pueblo: anchos, pasos y cargas distintos se superponen.” |
| `campos_colinas` | “En una curva reciente aparecen ramas cortadas para mantener visible el borde del camino.” |
| `campos_almacen` | “El almacén conserva señales de uso: una hoja barrida, una cuerda vieja retirada y un rincón despejado.” |
| `campos_vista_vaisgard` | “Otro viajero se detuvo aquí antes: las marcas de pies se concentran justo donde la ciudad se ve mejor.” |
| `campos_camino_exterior` | “Las reparaciones del camino se vuelven más frecuentes y de materiales distintos entre sí.” |
| `campos_acceso` | “La dirección del tránsito ya no necesita adivinarse: casi todas las huellas buscan la ciudad.” |
| `cuenca_aproximacion_sur` | “Dos corrientes de viajeros se mezclan en el acceso y vuelven a separarse al acercarse a Vaisgard.” |

## Reglas

- no nombrar personas;
- no prometer que la misma señal seguirá presente;
- no crear atajos, salidas ni rutas ocultas;
- no convertir mantenimiento de camino en quest;
- no añadir rewards, comercio ni fauna fija;
- si una sala tiene encuentro scripted o combate activo, esa escena tiene prioridad;
- clima/daypart pueden sustituir la línea, no acumular texto.

## Handoff

LISTO PARA INTEGRACIÓN: SÍ.
Estas líneas enriquecen únicamente salas ya existentes de Edran/Veyra.