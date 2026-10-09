# Ciclo MUD: pelear, recoger, vender, comprar, mejorar (2026-10-08)

Partida de prueba del usuario: de Valdren a Vaisgard hubo sólo dos peleas, un Cornalomo de nivel 8 lo mató al primer golpe, no había nada que vender ni comprar, y las salas sin salida no daban ninguna razón para entrar.

## Diagnóstico (medido en el contenido)
- Sólo 23 de 183 salas tenían un rival comparable. Los niveles saltaban de 1-2 a 8, sin nada intermedio.
- Las criaturas no dejaban nada (los salteadores, 4 sellos). Los materiales se vendían a 2-4 sellos.
- Había 4 armas casi iguales (7-10 de daño), ninguna armadura ni accesorio a la venta, y sólo la provisión básica.
- Los 34 callejones sin salida no tenían nada propio que encontrar.

## Cambios
- **Equipo por partes del cuerpo:** cabeza, torso, brazos, piernas y pies (`kind: armor`, `slot`), más anillo y amuleto (`kind: accessory`, `bonus`).
  - La protección se suma hasta un máximo del 50 % (`m.armor_total`).
  - Las bonificaciones de `vida`, `precision`, `dano` y `esquiva` se aplican en `hp_max` y `resolve_round`.
  - La antigua ranura `armor` sigue valiendo como torso.
- **Armas:** 8 nuevas en dos calidades más, una por familia, cada una con su rasgo (bloqueo, precisión, foco con vida extra, distancia).
- **Armadura:** 15 piezas, 5 partes del cuerpo × 3 calidades (cuero, reforzada, Vaisgard). **Accesorios:** 6 anillos y amuletos.
- **Pociones:** menor, de vida, tónico y ungüento. Se pueden usar también en combate, gastando la ronda (el rival responde).
- **Botín:** cada rival tiene tabla de botín (`creatures.<id>.loot`). La fauna mayor deja trofeos de 40-45 sellos. El nivel del rival aumenta la probabilidad de botín y los sellos del salteador.
- **Tiendas:**
  - Vaisgard vende todas las calidades y compra cualquier botín y equipo.
  - Cada región vende cuero, parte de lo reforzado, pociones y armas de su estilo.
  - Los compradores aceptan los materiales nuevos (tope de venta: 60).
- **Niveles de rival:** cada rival comparable aparece con nivel 1-6 según su distancia al pueblo más cercano (un nivel cada 3 pasos, ±1 al azar). Por nivel: +20 % de vida, +12 % de daño y +2 de precisión (`m.scaled`). El nivel se ve en el botón de combate y en el nombre del rival.
- **Más encuentros:**
  - La probabilidad de aparición sube de 45 % a 70 %, y los rivales comparables pesan el triple que la fauna mayor.
  - Todo camino, zona salvaje o lugar señalado sin rival comparable recibe uno o dos de su región, con varias versiones de texto: Espinajo, Cascapedernal o salteador. El Mordelinde sigue siendo un animal que huye.
- **Buscar:**
  - Cada región tiene 5 hallazgos más, y la probabilidad de hallazgo sube del 40 % al 50 %.
  - Cada sala puede tener `hallazgos` propios: los únicos, una vez por jugador; los demás se reponen a los 30 minutos.
  - Buscar se habilita en cualquier sala que tenga hallazgos propios.
- **Callejones sin salida:** 17 salas con hallazgo propio, la mayoría con premio único (amuletos, anillos, pociones, cristal, un puñal, botas).
- **Pasajes secretos:** 7, que aparecen después de buscar en el callejón, con su camino de vuelta. Entre ellos, el conducto viejo entre la Repisa de las cuñas y la Zanja seca.

## Medición (`simular_viaje.py`, Valdren → Vaisgard con desvíos de un paso)
| | Antes | Ahora |
|---|---|---|
| Peleas por viaje | 2-4 | 8-13 |
| Victorias | 1-3 | 6-11 |
| Sellos + botín vendible | ~20 | ~100-125 |
| Nivel máximo de rival | 1-2 o 8 | 3-4 |

Pruebas: 161 tests OK (incluye `tests/test_ciclo_mud.py`); QA del cliente OK; recorridos narrativos A y B sin errores.

## Pendiente
- Lethra y Nhal sólo tienen salteadores como rivales comparables. Hace falta fauna menor canónica peleable: pedírsela al historiador.
- Las piezas de armadura no tienen todavía arte ni se ven en la figura.
- Pociones de efecto especial y equipo único de jefes, más adelante.
