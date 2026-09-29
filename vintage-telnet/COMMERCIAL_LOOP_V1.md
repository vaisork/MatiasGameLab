# Circuito comercial de los cinco pueblos — v1

Esta entrega conecta las salas ya presentes en `world.py`. Conserva las identidades
regionales y las primeras obtenciones de armas regionales; no crea gremios, NPC
nombrados ni mercados entre jugadores.

| Sala | Servicio visible | Regla |
| --- | --- | --- |
| `valdren_mercado` | Provisiones, comida caliente, acopio, Puesto de encargos | Los tres encargos de #409 comienzan y se cobran aquí. |
| `khariel_mercado`, `brumak_mercado`, `narevia_mercado`, `velmora_mercado` | Provisiones locales, comida caliente, acopio | Abastecimiento cotidiano; no replican los encargos de Valdren. |
| `valdren_forja` | Taller de Daro, compra/reventa común, entrega del recado | Conversar no ejecuta comercio. |
| Las otras cuatro salas `_forja` | Compra/reventa de armas comunes | Sus escenas locales siguen separadas de la tienda. |

Los talleres comparten únicamente el catálogo común que ya circula entre pueblos:
Varita de aprendiz (40), Puñal de camino (50), Arco de ruta (65) y Espada de
juramento (85). Recompran esas mismas armas al 35% redondeado hacia abajo.
Hoja de Hoshai, Martillo de Korven y equipo regional o singular conservan su
forma de obtención y no se venden en estas tiendas. Las raciones se nombran
por pueblo; cuestan 8 sellos y tienen el efecto aprobado de la ración de
Valdren. La comida caliente cuesta 18 y conserva el efecto aprobado del
servicio. Ninguna comida se cobra si no produce beneficio. El acopio compra
los materiales C1 ya aprobados, con el mismo precio por pieza en cualquiera
de los cinco mercados.

Presentación breve reusable: «Aquí puedes preparar el camino, vender lo que
aprovechaste y regresar con noticias». En cada forja: «Hay armas comunes de
viaje; las piezas propias de otra región no forman parte del mostrador».
En Valdren, el puesto explica: «Acepta el recado, registra el trabajo en su
destino y vuelve aquí para cobrar». Los precios y estados los muestra siempre
el servidor. Un viaje al taller no concede sellos por sí solo.

Estas salas son puestos cotidianos, no promesas de todos los servicios futuros.
La reparación excepcional de #535 y los catálogos regionales únicos siguen
siendo entregas independientes.
