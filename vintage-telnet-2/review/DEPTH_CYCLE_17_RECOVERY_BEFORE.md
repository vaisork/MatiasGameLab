# C17 — derrota, cuidados y regreso antes de cambiar

Juego por HTTP real en 8117 con DB temporal nueva, RNG cero y reloj controlado desde 43200. Dos personajes nuevos de nivel 1: Felaryn Sombra y Humano Arcano. Ninguna inyección de HP, heridas, flags, sellos, equipo o ubicación. 96 movimientos y 122 acciones. Evidencia completa: `depth-cycle17-recovery-before.json`.

## Muerte real y vuelta al camino

La Felaryn hace una ruta larga por Hoshai, Veyra, Lethra y Nhal, recoge resina/junco y observa Cornalomo en Edran. Tras la advertencia de criatura abrumadora insiste en combatir. El reloj avanza 40 segundos y el combate real la derrota. Recupera el conocimiento en Brumak, a seis tramos reales del Prado de las Marcas Anchas, con 60 HP y 40 fatiga. Sellos, inventario y progreso se conservan; no aparece una arista de mapa falsa para el traslado. Brumak es más cercano por las rutas existentes que su hogar en Khariel.

Descansa dos veces: 60 → 70 → 72 HP; 40 → 15 → 0 fatiga. Encuentra cuidados a dos pasos por la calle de las fachadas, cuyo texto indica la puerta oriental. Neru explica el servicio; pagar 18 deja 90 HP, fatiga cero y renueva margen de descanso. Otra pausa deja 93 HP. Vuelve caminando al prado, observa y se retira antes de pelear otra vez. Este caso suma 70 movimientos. No hubo softlock de regreso o de dinero; 20 sellos iniciales permiten el servicio y quedan dos.

## Canal y venta después del combate

El Arcano recoge semillas en camino, pregunta a Nela/Oren, entra al canal y combate con el salteador de cargas. Tras 32 segundos vence con 12 XP, sin sellos de combate ni entrada de humano en bestiario. Recupera y devuelve la caja; la provisión entregada por Nela es un recurso real. Sale caminando, vende semillas por dos sellos, usa la provisión y vuelve al hogar con 100 HP. Este caso suma 26 movimientos. No se inventó botín animal para el humano ni se simuló curación.

## Defecto prioritario reproducido

El tercer descanso de Brumak sigue habilitado aunque el margen de recuperación esté agotado y la fatiga sea cero. Conserva 72/100 HP y 0 fatiga, pero anuncia: «Descansas. Recuperas 0 de vida y aflojas la fatiga acumulada.» La frase promete una reducción que no ocurre; la acción tampoco explica por qué aún faltan 28 HP y dormir de nuevo no sirve. El estado público no comunica ese margen mediante la acción.

Causa: `Engine.actions` ofrece descanso por seguridad del lugar, sin considerar el efecto real de `mechanics.rest`; el mensaje siempre usa la misma promesa de fatiga. Cambio propuesto, pendiente de coordinación: disponibilidad y razón según recuperación posible/fatiga, manteniendo todos los números del descanso; cuando no cure pero sí reduzca fatiga, describir sólo ese efecto. Cuando no tenga efecto, indicar que la vida restante requiere provisión o cuidados, sin regalar una ruta desconocida ni forzar a gastar.

La recuperación por derrota y los cuidados sí cumplieron sus promesas observadas. No se detectó un softlock duro: el defecto es orientación y falsa expectativa al repetir descanso. No se propone aumentar curación ni cambiar precio/penalización. El canon maestro pide muerte posible sin destruir horas y un ciclo de regresar, descansar, vender y volver a salir (páginas 5–6); el comportamiento exitoso respeta ese objetivo.

## Autocrítica

RNG cero asegura respuestas acertadas y no representa una frecuencia natural; la muerte fue elegida después de advertencia, no presentada como emboscada inevitable. No se probó muerte con herida grave: los golpes canónicos observados producen herida leve y la recuperación por derrota reduce un grado. Se corrigió un ID de sala del arnés y se repitió la sesión en DB nueva; ese error no se atribuye al producto. La búsqueda de cuidados sigue un recorrido planificado, aunque las dos direcciones están apoyadas por texto real del pueblo. No se midió UX humana ni rendimiento visual.
