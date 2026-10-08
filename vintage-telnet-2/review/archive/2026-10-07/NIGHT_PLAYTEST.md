# Partida técnica nocturna — primer corte

Prueba realizada en Chromium real, 393×750, contra servidor aislado en 8099 y base temporal. Cuenta sintética Felaryn/Sombra, aprobación real por API del director, salida del hogar, movimiento por el botón sur de Khariel. No se leyó ni alteró la partida real. Esto no equivale a una sesión humana de 20–30 minutos ni a Android físico.

Prompt maestro revisado: economía integrada (líneas 423–429 de la extracción autorizada), interfaz móvil centrada en jugar (432–441), y caminar→encontrar algo útil→vender/descansar/reparar/mejorar (329). La instrucción posterior del usuario autoriza cambios de mapa y arte anime en fichas.

## Cinco problemas priorizados reproducibles

1. **Lectura atrasada durante marcha.** Completar texto en Khariel y pulsar sur. A los 150 ms el encabezado dice Escalones al sol pero el lector conserva tres párrafos de plaza; la llegada nueva está al final y entorno/peligro siguen ocultos. Evidencia: `night-playtest/initial-rapid-step.png` y `initial-report.json`. Conservar historial consultable, presentar llegada y escena actual primero y cerrar animaciones pendientes al avanzar.
2. **Acciones demasiado altas en móvil.** Buscar alrededor incluye siete líneas de explicación dentro de una celda de tres columnas. La celda mide aproximadamente 105 px; el dock tapa acciones inferiores en la captura inicial. Las razones necesarias deben quedar breves o expandibles y las filas compactas.
3. **Hallazgos sin destino económico.** Los seis materiales regionales (semillas_camino, cuerda_recuperada, resina_pino, piedra_veteada, fibra_junco, rama_flexible) no tienen sell_price ni effect. En contraste, piel_mordelinde/fibra_espinajo sí tienen precios 3/4 y comprador. Buscar puede llenar mochila sin utilidad posterior. Fuente: catálogo vigente y acciones vender del motor.
4. **Comercio distante del inicio Felaryn.** Sólo dos de 162 cuartos tienen shop: fragua y comedor de Valdren. Mercado de Khariel no ofrece compras; hablar de mercancía no desemboca en adquirirla. Se necesita comercio regional con precios y efectos respaldados, sin fabricar monedas de monstruos.
5. **Aventura humana y acceso comunitario ausentes.** No hay señales de enemigos humanos/forajidos ni interacción explícita de permiso de entrada en poblaciones en el catálogo inicial. Son ampliaciones solicitadas por el usuario; deben probarse como diálogo→permiso→entrada y peligro→combate→consecuencia, no sólo añadir texto.

## Límites

La auditoría de contenido es estática; los puntos 1 y 2 sí se observaron en navegador. Los cortes económicos/forajidos deben volver a jugarse después de integrar cambios. No se afirman equilibrio independiente de cada criatura ni aprobación completa del prompt.

## Segundo corte integrado: circuito jugable API

`python3 scripts/night-world-journey.py` PASS. Base temporal propia, reloj de mediodía y azar determinista; se recorrieron conexiones reales y se pidieron permisos contextuales cuando una salida estaba bloqueada. Sin teleportación ni edición de inventario/partidas.

- Felaryn/Sombra sale de Khariel, busca resina de pino y la vende en su mercado por 2 sellos. Compra una provisión por 8: saldo real 14 desde los 20 iniciales.
- Viaja hasta el canal de Edran, conversa con Nela, obtiene la pista de Oren y se enfrenta al forajido de la compuerta. Tras avanzar 24 segundos de reloj, vence vivo; el humano no se registra en el bestiario.
- Recupera la caja en la repisa y la devuelve a Nela. La caja desaparece de la mochila y recibe exactamente una provisión adicional.
- Evidencia estructurada en `night-playtest/integration-report.json`. Estas comprobaciones no sustituyen una revisión visual del circuito ni equilibrio prolongado.

## Tercer corte: lector y mapa en Chromium

PASS real, viewport 393×750. Tras salir de Khariel se realizaron seis movimientos por botones (norte/sur), con 100 ms de espera por paso. En cada respuesta, el primer evento accesible de la terminal corresponde al lugar actual. El historial conserva las ocho visitas en «Releer lo vivido». Mirar mantuvo scrollTop 30→30. Sin desbordamiento horizontal a 320, 393 y 1440 px. Mapa sin tarjeta «Dónde estás», cuatro salidas punteadas sin nombres de destinos ocultos. Capturas `walking-*.png`, `map-dashed.png` y `client-report.json`.

La explicación larga de Buscar ya no infla la celda; el corte visual mejora la densidad. Detectado detalle pendiente: «Dejar de usar weapon» expone nombre interno de ranura; comunicado para traducir. La leyenda ↑N orienta el mapa, aunque las conexiones ya no llevan letras. No se probó todavía un gesto táctil físico.

## Cuarto corte: encargos cercanos de Khariel

El reproductor API agregó dos encargos completos con desplazamiento real: Luma recibe una recomendación de cornisa tras inspección/decisión y paga 6 sellos; Seran explica su cuenta, acuerda devolver la polea, se recoge y entrega a Daren, que paga 8 sellos. El objeto prestado desaparece al devolverlo. Total: 19 comprobaciones de recorrido/interacción en el informe integrado. No fue necesario combatir ni insertar objetos para esos encargos.

## Quinto corte: forja y mazmorra en navegador

PASS Chromium sobre servidor aislado nuevo. Humano/Juramentado gana 6 sellos con el recado real de Daro/Bren, combate al Espinajo por una fibra real y vuelve a la fragua. En Mochila, confirma el afinado mediante diálogo del navegador: daño base 10→11, saldo 26→14, fibra consumida y afinado retirado de acciones. Repetir exactamente el request_id de esa compra no vuelve a cobrar. Cerrar sesión y entrar conserva la pieza mejorada.

La pantalla muestra «Daño base: 11» y «Afinada · +1 daño». Capturas `forge-before.png`, `forge-after.png`; resultado `forge-report.json`. Después se verificó aviso del forajido en el canal, retirada resuelta y ruta pacífica «Pasar por el borde sin provocarlo» hasta la repisa, sin combate activo.

El primer intento técnico esperó sólo 17 segundos contra Espinajo de 40 HP y no alcanzó a resolver la lucha. El reproductor usa 27 segundos y servidor/base nuevos para no heredar encuentros compartidos de otro intento. Un segundo fallo fue una carrera del propio test al consultar antes de terminar login; se corrigió esperando la región de lectura.

## Sexto corte: pagos y capacidades corregidos

Rerun final PASS: los cuatro encargos únicos pagan completos 6/8/8/6 sellos, respetando el precio anunciado, y permanecen cerrados tras reconexión; intentos de volver a cobrar son rechazados sin aumentar saldo. La entrega individual de Elin usa una marca diferente del cuenco comunitario previo. El informe contiene 36 etapas documentadas de recorrido e interacción.

Comparativa real de rondas contra Espinajo preparado, basada en GAMEPLAY §§20.5 y 36.4–36.7 y la reconciliación canónica de firmas: Guardia reduce el golpe 8→6; Sombra baja precisión 60→35 y, al fallar el rival, permite acertar con una tirada que el ataque normal pierde; Artífice sacrifica daño por interrupción. Detectado y corregido Arcano: antes mantenía parte del bono de la carga (50%); ahora cancela y responde desde precisión básica menos 10 puntos (40%). `night-power-audit.py` verifica esa diferencia y registra `power-audit.json`.

A nivel 1 con atributos 10, Esquivar y Resistir aún no añaden mitigación según sus fórmulas aprobadas. Se informó para explicar el efecto actual en botones; no se modificaron números ni se presenta esto como equilibrio completo.

## Séptimo corte: cooperación y seguimiento

Tres cuentas temporales recorrieron el mundo y aceptaron la polea. Dos atacaron al mismo salteador: HP enemigo compartido 28→9 y una sola respuesta (principal 95 PV; compañero 100). El principal huyó antes de la victoria. Sólo el compañero que permaneció y venció obtuvo XP y la acción local de recuperar la polea; retirada y observador conservaron XP 0 y no pudieron cobrar ese encargo. Sólo después de recuperar/devolver la polea recibió 8 sellos. Ninguna moneda ni entrada animal por vencer al humano. `coop-report.json`.

Tracker de encargos jugado en Chromium: aceptar Cornisa, estado En marcha y 6 sellos, ruta de entrega conocida, recorrido/inspección/decisión/conversación, estado Listo para entregar, cobro desde Recuerdos y detalle Entregado/Recibiste 6. Reconexión conserva el resultado. `tracker-report.json`, `quest-ready.png` y `quest-paid.png`.

Regresión pasiva reproducida con efectos reducidos: lector desplazado 55 px y decisión escrita, muerte real por Cornalomo, regreso a Brumak con 60 PV. El nuevo lugar aparece pero se restaura scroll viejo 55 en vez de 0. Con animación normal parecía correcto porque el DOM recién creado tenía altura insuficiente y el navegador recortaba el scroll a 0. Evidencia previa al arreglo: `passive-regression/before-fix.json` y `.png`. Comunicado al responsable del cliente.

Reproducción aislada: `python3 scripts/night-test-server.py --fixed-clock` para el test de muerte; `VT_REVIEW_PLAYWRIGHT=/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs node scripts/night-passive-death.mjs`. El servidor sólo abre localhost:8099, crea base temporal y mantiene CSRF en la ruta de avance de reloj. Para el test de forja use el servidor sin `--fixed-clock`, porque espera rondas de tiempo real.

Regresión pasiva corregida y repetida en Chromium con efectos reducidos y servidor/base nuevos: lector 55→0, encabezado «Patio de Brumak», primer evento «Llegas a Patio de Brumak», PV 60 y combate terminado. Conserva foco/campo de decisión y «mirar después». Evidencia final `passive-regression/after-fix.json` y `.png`. El avance de reloj es del servidor aislado y se enviaba con CSRF; no se alteró la base real.

## Octavo corte: vistas opcionales y otros tres encargos

Chromium PASS: los seis WebP de pueblos responden 200; la página no solicita automáticamente arte de pueblos antes de tocar el icono y no inserta imágenes en la lectura. Khariel se abre desde el lugar actual y desde el mapa conocido; cierra por Escape, botón y fondo. Sin desbordamiento en 320/393/1440 px. Un nodo canónico descubierto pero no visitado, añadido únicamente a la respuesta aislada del navegador como fixture, no ofrece arte; no se escribió en la base. `town-art-report.json` y `khariel-modal.png`.

Recorrido API ampliado a siete encargos únicos: aviso de Tov/Nera/Arel paga 6, toldo de Seli paga 6 y taza de Taren paga 8; reconexión conserva los siete pagos y rechaza recobros. Intentar sujetar el toldo sin material se rechaza sin modificar inventario. Bela presta una unidad real de junco: no se vende, se consume una sola vez al usarlo y repetir el mismo request no duplica consumo.

Una segunda cuenta recorre la alternativa pacífica: prepara perchas sin consumir el haz, devuelve exactamente una unidad no usada a Bela y cobra el trabajo una sola vez. Repetir devolución es rechazado sin crear material. El informe integrado registra 58 etapas de recorrido/interacción. Esto continúa siendo una prueba automatizada, no una aprobación humana del prompt completo.
