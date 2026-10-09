# Comprobación visual del combate — versión 42846e8

Se extrajo exactamente42846e8 con git archive en carpeta temporal, sin cambiar el checkout de otro programador. Se creó una cuenta/personaje propios en SQLite temporal, se aprobó por API y se inició combatir:espinajo_rastrojo por el motor real. Nivel8/atributos20 son sólo fixture para obtener el encuentro, no balance certificado. No se leyeron ni modificaron partidas de Raspberry.

Chrome real a320,393,768,1440px: ambas barras están en la misma línea, altura4px, con ancho visible y límites dentro de pantalla. Dos meters accesibles, sin overflow horizontal ni errores JavaScript. Se inspeccionaron visualmente las capturas393 y1440: cabecera compacta, nombre completo del enemigo en título, etiquetas abreviadas junto a barras, ronda bajo ellas. Esto cumple el diseño de una línea fina de dos barras; no significa que toda la tarjeta de combate mida4px.

Sin cambios al código del juego ni nuevo despliegue. El navegador usa emulación de viewport; no acredita una sesión móvil física. Se comprobó composición en un encuentro real inicial, no todos los turnos/clases/adversarios ni balance. Los saltos de línea dentro de algunos nombres de botones son visibles y pertenecen a la disposición de acciones, fuera de esta comprobación de barras.

browser.json registra medidas y errores; PNGs contienen capturas. serve-fixture.py documenta el fixture con rutas locales explícitas. Requiere archivo exacto de esa versión, dependencias Python existentes y Node Playwright/Chrome en rutas del script; no ejecutarlo sobre runtime real. Informe local preparado para la repo, sin push en esta operación.
