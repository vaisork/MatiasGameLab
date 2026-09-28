# COMBAT-SALVAGE-01 — presentación narrativa breve

Issue: #482
Fuentes: Historia PR #491 + Jugabilidad GAMEPLAY §42.
Superficie de venta autorizada: valdren_mercado, Puesto de acopio del Mercado de Valdren.

## Regla de presentación

La obtención de material no se convierte en una escena larga. Después de una victoria C1, el resultado debe resolverse en una sola línea.

### Si hay material aprovechable

Texto base:
“Entre los restos queda algo aprovechable: {material_label}.”

Variante cuando convenga subrayar que no es automático:
“Esta vez queda material en buen estado: {material_label}.”

### Si no hay material aprovechable

Texto base:
“No queda nada aprovechable que valga la pena cargar.”

Variante:
“Los restos no dejan material útil para el mercado.”

No usar “loot”, “drop”, “premio” ni lenguaje de videojuego dentro del relato.

## Venta en el Puesto de acopio

Antes de vender, la interfaz debe mostrar material y valor fijado por Jugabilidad.

Presentación:
“El puesto de acopio compra materiales comunes de fauna para revenderlos a talleres y viajeros.”

Confirmación:
“Entregas {material_label}. Recibes {valor} sellos.”

Si el jugador no vende:
“Guardas el material.”

Daro no participa en este flujo como comprador genérico.

## Familias C1

Los mensajes usan el nombre visible del material que Integración derive de la tabla canónica de Historia. Narrativa no inventa órganos, venenos, cristales, metales ni propiedades especiales.

Familias cubiertas:
- Mordelinde
- Espinajo de rastrojo
- Uñapiedra
- Saltacresta
- Cascapedernal
- Colagrieta
- Pinzajunco
- Saltalodo
- Rondamusgo
- Hilaria de niebla
- Garralaja
- Cavapolvo
- Remojunco
- Velacauce
- Silbarisco

## Límites

- no sellos directos por muerte;
- no crafting obligatorio;
- no escena de despiece;
- no gore;
- no material garantizado;
- no duplicación por jugador en combate multijugador;
- no mensaje de venta antes de confirmar la operación autoritativa;
- reconexión no repite la obtención ya resuelta.

## Handoff

Narrativa #482: CERRADA.

Integración/Desarrollo puede consumir estos textos junto con:
- material/item_key final;
- frecuencia/cantidad;
- valor de venta;
- resolución atómica;
- antifarmeo;
todo definido fuera de Narrativa.
