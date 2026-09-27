# Wark — cierre del paquete documental del issue #212

**Fecha:** 2026-09-27.  
**HEAD de `main` revisado:** `4d8b36c7c5dff10b8c4faa2d4053fa6613271d53`.  
**Rama:** `work/wark-continuidad-vintage-telnet`.  
**Alcance:** registro de agotamiento del encargo documental vigente; no es canon, narrativa aprobada ni regla de jugabilidad.

## Verificación realizada

Se revisaron:

- `AGENTS.md` vigente;
- issue #212 y sus nueve comentarios;
- PR #218 del Historiador y su definición de cinco corredores, diez ramales y cinco asentamientos de apoyo;
- ramas relacionadas del Narrador localizadas;
- entregas WARK 01–06 de esta rama;
- cambios recientes de `main`.

No apareció una nueva conexión autorizada, un nuevo ramal definido por Historia ni una ampliación del alcance de Javier que permita crear otra ficha sin inventar geografía o sustituir a Narrativa/Jugabilidad.

## Cobertura entregada

| Corredor del PR #218 | Ficha Wark | Cobertura documental |
| --- | --- | --- |
| Valdren ↔ Narevia — Camino de la Tierra Húmeda | `WARK_CICLO_01_TIERRA_HUMEDA.md` | Ida/vuelta, transición de suelo y agua, Molino Hundido, Charcos Negros, retorno y dependencias |
| Khariel ↔ Brumak — Paso de las Lajas | `WARK_CICLO_03_PASO_LAJAS.md` | Ida/vuelta, lectura de altura/roca, Grieta del Eco Seco, Cornisa Ciega, retorno y dependencias |
| Brumak ↔ Valdren — Senda del Viento Bajo | `WARK_CICLO_04_VIENTO_BAJO.md` | Ida/vuelta, horizonte/viento/tránsito, Cantera, Zanja, retorno y dependencias |
| Narevia ↔ Velmora — Ribera Sombría | `WARK_CICLO_05_RIBERA_SOMBRIA.md` | Ida/vuelta, luz/orilla/marcas, Canal Quieto, Sendero sin Marca, retorno y dependencias |
| Velmora ↔ Khariel — Paso del Dosel Alto | `WARK_CICLO_06_DOSEL_ALTO.md` | Ida/vuelta, dosel/pendiente/aire, Boca de la Montaña, Sendero de las Copas, retorno y dependencias |

`WARK_CICLO_01_MAPA_HUECOS.md` y `WARK_CICLO_02_ESCALA_RETORNO.md` aportan el mapa general y el criterio transversal de reconocimiento, preparación y nueva expedición.

## Motivo del cierre

Continuar con otra ficha bajo el mismo contrato obligaría a una de estas acciones no autorizadas:

- abrir una de las conexiones diagonales que PR #218 reserva explícitamente para el futuro;
- definir interiores de mazmorra o jefes que Historia y Jugabilidad dejaron pendientes;
- escribir escenas que corresponden al Narrador;
- fijar obstáculos, requisitos, costes o recompensas que corresponden a Jugabilidad;
- repetir la misma estructura con nombres distintos sin añadir un hueco real.

Por instrucción de Javier, no se genera relleno.

## Dependencias pendientes

- **Historiador:** confirmar o integrar la geografía del PR #218 y resolver las relaciones espaciales señaladas en cada ficha.
- **Narrador:** convertir funciones de orientación y retorno en escenas y secuencias jugables.
- **Jugabilidad:** definir presión, acceso, mapa, riesgos, descanso, requisitos y recompensas.
- **Arquitectura/Desarrollo:** consumir únicamente material aprobado y coordinado.

## Estado final

**PAQUETE DOCUMENTAL WARK PARA LOS CINCO CORREDORES: COMPLETO DENTRO DEL ALCANCE ASIGNADO.**

El issue #212 permanece abierto bajo liderazgo del Narrador. Wark no lo cierra, no cambia prioridades y no abre otro frente. Un nuevo ciclo solo tendría sentido si Javier amplía el encargo o si Historia/Narrativa/Jugabilidad dejan un hueco concreto nuevo en GitHub.
