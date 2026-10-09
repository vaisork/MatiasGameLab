# Integración: bestiario de riesgo de Lethra y Nhal (PR #669)

Una sola integración de las 20 especies del historiador: catálogo, combate, encuentros, narrativa, aprovechables y encargos de arte.

## Especies nuevas (16), en tres niveles de riesgo

| Región | Presa defensiva (favorable, nv 1) | Rival común (comparable, nv 2) | Depredador peligroso (peligroso, nv 4) |
|---|---|---|---|
| Lethra | Mordijunco | Cienfango, Raizacapa, Aguaculebra, Cortacorriente | Faucecieno, Tragacharco, Sombranutria (nocturna) |
| Nhal | Velomembrana (nocturna), Roecorteza | Quebracáscara, Escarbaraíz, Clavaespina | Mordesombra, Garfarrama, Tronchacolmillo |

Las fases de narrativa que pide la ficha se cubren así:

| Fase | Dónde está |
|---|---|
| Presagio y rastro | `presagio`, que también se añade a los rastros de buscar de su región |
| Primer avistamiento | Entradas de `wildlife_pool`; algunas varían con la hora o la lluvia (`requires_time`, `requires_weather`) |
| Advertencia | `warning` |
| Inicio | `combat_intro` |
| Maniobra característica | `MINOR_INTENTIONS`, con aviso legible e interrumpible o no según la especie |
| Defensa y ataque | `CREATURE_PROSE` |
| Huida o derrota | `defeat_text`, que ahora también se muestra al vencer a un animal |
| Aprovechamiento | `loot`, con texto propio en cada objeto |

- **Depredadores:** usan el mismo flujo que la fauna mayor. Primero «Observar de cerca», que muestra la advertencia; después «Insistir en enfrentarte» o «Retirarte», con retirada pacífica propia de cada especie.
- **Niveles:** las tres categorías escalan con la distancia al pueblo (`m.SCALED_CATEGORIES`). La fauna mayor no cambia.
- **Aparición:** las presas y los rivales comunes pesan ×3; los depredadores, ×2.
- **Hábitats:** juncales, raíces, charcos, pasos de agua y muelles en Lethra; suelo, raíces y redes, helechos, ramas y claros en Nhal.
- **Sin saturar:** se retiran los salteadores automáticos de las zonas habitadas de Lethra y Nhal. Se conservan los salteadores escritos a mano en los caminos.

## Especies existentes (4)

Pinzajunco, Saltalodo, Rondamusgo e Hilaria de niebla **siguen sin combate**, tal como están implementadas (`test_pinzajunco_can_be_examined_without_combat`).
- Se enriquecen con advertencias, avistamientos en sus hábitats y presagios.
- Ganan aprovechables que se recogen **sin matarlas**: caparazón y piel mudados, un mechón y hilos de una red abandonada.
- Hilaria no se convierte en combatiente, como exige el contrato.
- **Decisión pendiente:** la ficha propone combate defensivo para Pinzajunco, Saltalodo y Rondamusgo («pinzazo y repliegue», «salto evasivo», «empujón y huida»). Activarlo cambia una decisión anterior; queda a criterio del usuario.

## Economía

- **35 materiales nuevos**, con precio según el nivel de riesgo: presas 4, rivales 5-7, depredadores 9-13, recogidas sin combate 3-5. Es la escala del ciclo MUD vigente.
- Los compradores regionales los aceptan; Vaisgard compra todo.

## Dificultad (personaje de nivel 1, 300 duelos)

| Depredador | Sin equipo | Reforzado y 1 poción | Reforzado y 2 pociones |
|---|---|---|---|
| Faucecieno | 17 % | 91 % | 97 % |
| Tragacharco | 35 % | 96 % | 100 % |
| Sombranutria | 16 % | 89 % | 97 % |
| Mordesombra | 33 % | 93 % | 97 % |
| Garfarrama | 28 % | 91 % | 99 % |
| Tronchacolmillo | 27 % | 90 % | 98 % |

Presas y rivales comunes: se ganan siempre a su nivel base.
Viajes simulados por Lethra y Nhal: 1 a 4 peleas en tramos cortos, con botín regional propio.

## Arte

`docs/colaboracion/arte-criaturas/SOLICITUDES_CRIATURAS.json` contiene 36 encargos de tipo `creature`:
- 16 fichas para las especies nuevas;
- 20 imágenes de ambiente, una por especie;
- Las 4 especies existentes conservan su ficha.

No se generaron imágenes. El juego funciona sin ellas.

## Pruebas

168 tests OK, incluido `tests/test_fauna_lethra_nhal.py`. QA del cliente OK y recorridos narrativos A y B sin errores.
