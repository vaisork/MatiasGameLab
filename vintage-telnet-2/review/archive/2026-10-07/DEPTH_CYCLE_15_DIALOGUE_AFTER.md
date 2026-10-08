# C15 — respuestas después de hechos resueltos

## Implementación acotada

Sólo se añadieron `states.overrides.topics` en 10 NPC de Edran, Hoshai, Korven y Veyra, con flags existentes. El motor y cliente no se modificaron. Daro reconoce la medida pagada; Daren conserva la polea devuelta y la cuenta todavía pendiente; Taren distingue recomendación de base o aro sin declarar terminada una taza que aún debe probar; Ruma reconoce la placa colocada. Seli diferencia atadura de junco de perchas preparadas: preparar perchas no significa que el toldo ya esté reparado. Tov y Nera responden según aviso preciso o solicitud de comprobación. Luma distingue cargas pequeñas de revisión previa.

Bren e Iria usan dos hechos físicos mundiales (cuña sujeta y cuenta aclarada), con respuestas descriptivas que no atribuyen al interlocutor trabajo ajeno. Las entregas y recomendaciones privadas exigen sus flags personales. No se añadieron misiones, flags, recompensas, rutas ni efectos. La primera conversación mantiene sus acciones y condiciones; el override aparece después de producirse el hecho.

## Rejugar y comparar

`depth-cycle15-dialogue-before.json` → `depth-cycle15-dialogue-after.json`: API HTTP real, servidor aislado 8115, cuenta nueva y DB temporal nueva. Ambos recorren 248 movimientos y 311 acciones, con 36 comprobaciones y seis encargos pagados; final idéntico de 60 sellos, inventario, equipo, HP, fatiga, XP y atributos.

`depth-cycle15-dialogue-comparison.json`, generado por `scripts/depth-cycle15-compare.py`, verifica 11 topics resueltos modificados, todas las respuestas iniciales/primeras entregas preservadas, nueve respuestas del observador privadas o de control idénticas al BEFORE, y las dos respuestas físicas mundiales iguales para actor y observador. No hay crédito privado filtrado al observador. Arel sirve de control: su máxima sigue siendo verdadera y su memoria ya era adecuada. Seran sigue teniendo una cuenta pendiente: no se inventó que devolver la polea fuera pagarla.

`depth-cycle15-dialogue-alternatives.json`: otra cuenta real sin fixtures recorre 89 movimientos y diez comprobaciones. Revisión de cornisa, aro de taza, atadura con junco prestado y aviso para comprobar producen sus cinco respuestas específicas. Se verificó consumo del préstamo y se cobraron únicamente los encargos existentes. No se usó un flag editado para simular estas variantes.

Los 14 tests de contenido real pasan; el comparador de las sesiones guardadas y las cinco aserciones de alternativas pasan. La prueba no depende de una imagen ni de un checklist: reproduce las órdenes contradictorias y observa su reemplazo con las mismas consecuencias mecánicas.

## Autocrítica y límites

La auditoría cubrió los 27 NPC de las cuatro regiones por lectura y jugó los temas que dependían de hechos ya resueltos. No prueba todos los horarios, especies o conversaciones. La memoria añadida después de la respuesta puede repetir un hecho, pero ya no contradice la instrucción principal. El recado de Daro es repetible: su respuesta recuerda una medida anterior y las instrucciones de aceptar otra vuelta siguen en la acción de encargo; no se pretendió añadir estados de misión nuevos para cada repetición. Los trabajos privados mantienen el modelo de progreso personal existente, mientras los cambios físicos compartidos se describen como visibles para todos.
