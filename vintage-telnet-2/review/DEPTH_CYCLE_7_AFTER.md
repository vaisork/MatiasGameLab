# Ciclo 7: amenazas regionales y decisiones de formación — después

Implementación en mechanics.py con una matriz declarativa de cuatro intenciones, preparada sólo al comenzar el contacto. No cambia HP, daño, precisión ordinaria, reducción, nivel, XP ni loot. El coordinador integra el aviso antes de la intervención en Engine; prepared_action ya llega al cliente. No se altera el pool de criaturas, la presencia regional ni las rutas.

| Criatura | Preparación | Guardia frontal | Interrupción Arcano |
| --- | --- | --- | --- |
| Rasgacumbres | Zarpazo lateral | No disponible | Disponible |
| Quebrarrocas | Empuje anclado frontal | Disponible | No disponible |
| Dorsalodo | Barrido pesado lateral | No disponible | No disponible |
| Rasgacorteza | Golpe desde tronco frontal | Disponible | Disponible |

Sombra conserva reducción de precisión y apertura si la respuesta falla; Artífice necesita acertar y sólo interrumpe preparaciones interrumpibles. Interrumpir no elimina toda respuesta del rival: éste conserva una respuesta ordinaria, conforme al contrato de Jugabilidad. Los mensajes nombran la acción concreta y las limitaciones; guardia forzada contra ataque lateral informa que no reduce daño. `capability_hint` explicita qué significa elegir el disparo antes de decidir.

Rejuego comparable REAL: `VT_DEPTH7_OUTPUT=review/depth-cycle7-after.json python3 scripts/depth-cycle7-combat.py`. 160 movimientos, cuatro clases por cada región, 16 encuentros. Mismas cuentas aisladas/aprobación DM/nivel8/atributos20/equipo/RNG que el baseline reconstruido; cambios sólo en primera preparación. Se confirmó aviso de dos eventos antes de una intervención y nombres/ángulos/interrumpibilidad visibles. Los 16 jugadores observaron, se retiraron antes del contacto, provocaron voluntariamente y huyeron después de una ronda; todos sobrevivieron.

Antes las 16 capacidades estaban disponibles contra el perfil clonado. Después Juramentado deja de ofrecer guardia en dos ataques laterales y Arcano deja de ofrecer interrupción en dos acciones ancladas. Cambian las decisiones válidas, no sólo el nombre de la criatura. En el ensayo controlado: Juramentado frontal conserva 13 daño; lateral elige esquivar y recibe 0. Arcano interrumpe donde corresponde; en los otros dos casos esquiva. Estos resultados dependen del roll .6 y los atributos20; no son garantías de esquiva/victoria.

Artífice expuso un límite real: antes el rival ordinario perdía 15 de precisión al acertar; ahora una preparación interrumpida vuelve a precisión ordinaria65, y recibe20 daño en este roll. No se inventó un bono para esconderlo. Segunda vuelta adaptativa REAL (`VT_DEPTH7_ADAPT=1`, evidencia `depth-cycle7-adaptive.json`): 40 movimientos/cuatro regiones. En Quebrarrocas y Dorsalodo el texto permite reconocer que el disparo sólo dañaría y elegir esquiva: daño20→0. En los otros dos el disparo interrumpe y mantiene una respuesta ordinaria; la elección sigue teniendo coste real. El jugador puede preferir defensa o fuga.

Pruebas: 25 pruebas tácticas, poderes y mecánicas PASS; 38 pruebas de contenido real, motor y multijugador PASS. Tras añadir hints exactos, siete pruebas focales PASS. Cubren matriz de disponibilidad, conservación numérica, avisos físicos, guardia lateral y mensaje Artífice no interrumpible. Toda ejecución usa DB temporal.

Autocrítica: cuatro animales aún comparten la escala de peligro numérica, de manera intencional. Se diferencian en la primera decisión preparada; rondas posteriores vuelven al combate ordinario, sin rearmar ataques ocultos. La matriz no es una simulación de ecología ni reemplaza comportamiento fuera del combate. La observación estática inicial falló al omitir pools dinámicos: se corrigió y se descartó el ensayo artificial. El baseline numérico está reconstruido en el proceso de prueba, no se disfraza de versión anterior desplegada. Falta una pasada de cooperación donde interrumpir un ataque lateral permita que otra formación responda sobre el rival ya desviado; la suite multijugador existente pasa, pero no se afirma esa experiencia específica como jugada.
