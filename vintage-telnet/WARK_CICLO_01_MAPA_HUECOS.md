# Wark — ciclo 01: huecos de recorrido de la primera región

**Fecha:** 2026-09-26  
**Base leída:** `main` 271a92eba6f0e3b554328d57ed1c66a61a7624f0.  
**Estado:** análisis y propuesta pendiente; no es canon, diseño narrativo aprobado ni contenido implementable.  
**Autor:** agente Wark.

## Hallazgo principal

La expansión no empieza desde cero. `REGIONS.md` fija cinco rutas radiales; `server/world.py` ya implementa cadenas de aproximadamente 18 pasos desde cada pueblo hacia Vaisgard y un pequeño ramal en Edran. La ruta A contiene una microaventura y algunos hábitats dinámicos. `CREATURES.md` define dos criaturas menores y una amenaza superior para cada región de inicio. El servidor indica explícitamente que su topología cardinal v1 no es el mapa canónico completo.

Existe trabajo activo fuera de `main`: `narrador/routes-doc-main-sync` contiene `NARRATIVE_ROUTES.md` con seis cinturones narrativos, 17–18 estaciones por ruta y bifurcaciones B7/C6/E5 previstas; `historia/vt-malla-regional-212` contiene `REGIONAL_CONNECTIONS.md`, cinco corredores periféricos, diez ramales candidatos y cinco asentamientos secundarios en `SETTLEMENTS.md`. Sus HEAD observados fueron a5af232 y b30377e. Estas ramas son insumos de coordinación, no se elevan aquí a canon de `main` ni se les reescribe el contenido.

El hueco real es **convertir la malla periférica en recorridos interesantes y comprobables**, y distinguirla de los corredores radiales ya escritos. Más habitaciones idénticas no producen por sí mismas seis a ocho horas de juego.

## Mapa de trabajo (topología conceptual, no mapa del jugador)

```text
                         Khariel
                   Lajas /     \ Dosel Alto
                     /             \
                 Brumak           Velmora
                 /                   \
          Viento Bajo            Ribera Sombría
               /                       \
          Valdren — Tierra Húmeda — Narevia

                  Vaisgard: nodo central
          cinco caminos radiales ya representados
```

La malla periférica de la rama del Historiador enlaza pueblos vecinos sin obligar al regreso por Vaisgard. No presupone que todas las conexiones sean conocidas por un personaje nuevo: `GAMEPLAY.md` §23 distingue conocimiento, visita y recorrido, y niega viaje rápido en v1.

## Matriz de huecos a llenar

| Tramo | Ya disponible en rama histórica | Entrega que falta | Lectura que debería pedir al jugador | Responsable de validación |
| --- | --- | --- | --- | --- |
| Khariel ↔ Brumak, Paso de las Lajas | Cuatro hitos, Grieta del Eco Seco, Cornisa Ciega, Refugio de Lajas | Secuencia de transición altura → roca; bifurcación legible; retorno al refugio | Distinguir referencias de altura de marcas de piedra; advertir que una grieta lateral no es atajo obligatorio | Historiador para hechos; Narrador para escenas |
| Brumak ↔ Valdren, Viento Bajo | Cuatro hitos, Cantera Abandonada, Zanja de la Piedra Hundida, Parada de los Cardos | Secuencia que abre progresivamente el horizonte y separa camino de cantera | Usar viento, suelo y visibilidad para orientarse cuando los montones de piedra dejan de servir | Historiador; Narrador |
| Valdren ↔ Narevia, Tierra Húmeda | Cuatro hitos, Molino Hundido, Charcos Negros, Vado de Juncos | Pasos de humedad creciente, elección de ruta firme/pasarela y señal previa de riesgo | Reconocer que los indicios de suelo cambian antes de que se vea agua abierta | Historiador; Narrador; Jugabilidad si afecta acceso |
| Narevia ↔ Velmora, Ribera Sombría | Cuatro hitos, Canal Quieto, Sendero sin Marca, Orilla Velada | Transición de agua abierta a dosel; ruta legible de ida y vuelta | Distinguir silencio normal, pérdida de marcas y señal concreta de peligro | Historiador; Narrador |
| Velmora ↔ Khariel, Dosel Alto | Corredor nombrado y ramales definidos en la rama histórica | Verificar hitos y ramales completos; graduar cambio de dosel a altura sin repetir Camino Alto | Comparar orientación por señales discretas con líneas de visión abiertas | Historiador; Narrador |

**Nota:** los nombres de hitos y ramales anteriores proceden de la rama histórica #212. Antes de redactar escenas definitivas, comprobar si esa rama fue integrada o revisada.

## Unidad de diseño para cada tramo periférico

Propongo una ficha de **recorrido**, no una cantidad fija de salas:

1. **Salida reconocible:** qué hábito del pueblo aún se ve y qué cambia primero.
2. **Dos referencias distintas:** una para avanzar y otra para reconocer el regreso.
3. **Cambio ecológico gradual:** dónde cesan los indicios de la primera región y dónde aparecen los de la segunda.
4. **Desvío opcional:** qué se ve desde el camino, por qué alguien lo investigaría y cómo vuelve a la ruta. No prometer una mazmorra ya construida.
5. **Advertencia justa:** rastro observable antes del peligro; la amenaza superior común no se convierte por ello en jefe.
6. **Pausa con sentido:** refugio/asentamiento secundario existente en la rama, con función de orientación y regreso; descanso mecánico, comercio y reaparición requieren decisión de Jugabilidad.
7. **Descubrimiento:** algo que el jugador pueda deducir al comparar dos señales; Historiador decide la verdad, Narrador la escena y Jugabilidad si amerita XP.
8. **Prueba de retorno:** al volver, el jugador debe reconocer al menos dos referencias sin depender exclusivamente del mapa.

La ficha se puede repetir cinco veces sin clonar escenas. La primera ficha prioritaria debería ser **Valdren ↔ Narevia**: ofrece un cambio físico muy legible (suelo firme a pasarela), conecta dos pueblos con identidad distinta y aprovecha criaturas ya definidas en Edran y Lethra. No asigno fauna a salas ni mezclo pools sin validación.

## Restricciones que protegen el juego

- La meta conversada de seis a ocho horas para recorrer el mundo es un objetivo de experiencia pendiente de medición, no un tiempo canónico ni una fórmula de 18 pasos = cierta duración.
- Un camino extenso necesita decisiones, retorno y descubrimientos; medir tiempo de lectura, movimiento, pausas y desvíos por separado durante un playtest.
- `GAMEPLAY.md` §23 impide revelar automáticamente rutas o secretos en el mapa; tampoco hay viaje rápido v1.
- `GAMEPLAY.md` §96 reserva pérdida de arma PvE para jefes explícitos y aun entonces depende de regla concreta. Ninguna amenaza regional ni acceso futuro de esta ficha se etiqueta como jefe por defecto.
- No poblar `vintage-telnet/content/` ni `server/world.py` desde este documento. Requieren una entrega aprobada y trabajo técnico posterior.
- El material de `SECRETS.md` y `NARRATIVE_RESERVED.md` no se traslada a fichas públicas ni a conversaciones normales con Javier jugador.

## Estado de entrega

La ficha piloto de **Tierra Húmeda** ya se entregó en `WARK_CICLO_01_TIERRA_HUMEDA.md`. El Historiador debe validar qué hechos del corredor #212 se vuelven canon en `main`; Narrador convierte funciones en prosa y escenas; Jugabilidad decide cualquier costo, descanso, acceso, encuentros o recompensa; Arquitecto coordina implementación posterior. Wark espera un nuevo encargo directo de Javier antes de abrir otro frente.

**Criterio de aceptación del piloto:** un lector puede explicar dónde está, cómo volver, qué pista justifica investigar un ramal y por qué el otro camino sigue hacia Narevia, sin revelar secretos ni recurrir a combate obligatorio.
