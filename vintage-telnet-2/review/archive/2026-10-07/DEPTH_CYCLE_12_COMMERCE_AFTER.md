# C12 — comercio después de implementar

## Cambio y comparación

El bloque de compras de `Engine.actions` conserva precios, objetos y disponibilidad, pero incorpora daño base, alcance, foco y bloqueo desde los datos reales de cada arma. Una compra asequible explica que el arma va a la mochila y debe equiparse, y compara su daño base con la pieza activa, incluido su afinado real. Las provisiones muestran recuperación máxima de vida según HP máximo actual y reducción de hasta 20 fatiga; la explicación conserva el límite y que no trata heridas. El label mantiene información esencial incluso cuando falta dinero y reason pasa a explicar los fondos.

Root añadió la presentación de reason en los botones de compra existentes. No se creó panel de comparación ni estadísticas nuevas. Las cifras de provisión son exactamente las del efecto `usar`, no un balance nuevo.

La misma sesión HTTP aislada se repitió desde cuenta nueva y DB temporal nueva en 8112: 110 movimientos, 131 acciones, mismo inventario final y 4 sellos al volver al hogar. Piedra encontrada y vendida, espada afinada 10 → 11, provisión comprada, visita a Lethra, Cascapedernal comparable vencido, provisión usada, conversación postcombate y regreso. La provisión restauró 90 → 100 HP y 12 → 0 fatiga antes y después: corresponde a los límites máximos anunciados de 18/20, no promete recuperar una cantidad que exceda lo perdido. No se alteraron recursos ni atributos en esta sesión.

| Oferta | BEFORE | AFTER |
|---|---|---|
| Provisión | Nombre y 8 sellos | Hasta 18 vida; reduce hasta 20 fatiga; no trata heridas |
| Puñal | Nombre y 50 sellos | Daño base 8 |
| Espada | Nombre y 85 sellos | Daño base 10; permite bloquear |

Evidencias autoritativas: `depth-cycle12-commerce-before.json` y `depth-cycle12-commerce-after.json`.

## Verificación focal y visual

`tests/test_commerce_preview.py` contiene dos regresiones de API sobre contenido real y DB temporal. La primera gana fibra, afina la espada y verifica 11 de daño; una fixture explícita de 100 sellos permite comprobar la rama asequible de referencia, comprar Puñal por 50, equipar su daño 8 y conservar la espada afinada. Esa fixture sólo pertenece al test, no a la sesión jugada ni a la economía del producto. La segunda usa fixtures de lesión/fatiga para verificar provisión por 8 sellos, cap de HP, reducción máxima de 20 fatiga y conservación de herida leve. Ambos casos pasan.

Browser real en 8112 con dos cuentas Dravak nuevas, 320 y 393 píxeles: compras muestran daño/efecto, compra legal de provisión funciona y no hay errores JS. `depth-cycle12-commerce-ui/report.json` y sus dos capturas. Se inspeccionó `320-offers.png`: daño actual y daño de Puñal visibles, explicación de recuperación y herida legibles, botones dentro del ancho móvil; las ofertas inferiores requieren scroll normal. Sintaxis pasa. Los 23 tests de engine, 14 de real_content y dos de commerce_preview pasaron; la primera invocación de real_content usó PYTHONPATH incompleto y se corrigió, sin atribuir ese fallo al producto.

## Autocrítica

La mejora es de decisión informada, no una expansión del comercio. No demuestra que una persona vaya a elegir mejor ni mide ritmo humano. El daño base compara armas sin simular todos los atributos o poderes de clase. No se presentó la retirada correcta de Mordelinde como victoria ni se inventó material del Cascapedernal. Los NPC conservan sus conversaciones de oficio y memoria de hallazgos, sin comentarios omniscientes sobre cada batalla. El recorrido sigue siendo un guion de agente con RNG controlado; la compra de un arma cara se cubre mediante la fixture declarada, no mediante ingresos naturales fingidos.
