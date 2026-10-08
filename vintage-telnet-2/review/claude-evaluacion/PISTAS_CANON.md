# Pistas de «buscar»: resolución canónica (revisión del historiador, 2026-10-08)

Regla: no todas las pistas llevan a monstruos. El mundo da pistas, no soluciones. La fauna mayor (Cargallanura, Rompecimas, Hundepedral, Tragacauce, Quebradosel) se anticipa por rastros, sin convertirse todavía en encuentro, y sin nombrarla hasta que varias señales permitan deducirla.

| Región | Pista | Es en realidad | Se resuelve en |
|---|---|---|---|
| Edran | Huella partida, más honda que las de Cornalomo | Cargallanura (pezuña ancha de dos lóbulos; **no** tiene cuatro dedos) | Prado de las Marcas Anchas, comparando con los rastros de Cornalomo |
| Edran | Postes empujados desde el campo | Paso de Cargallanura: madera empujada, no mordida | Campos exteriores; nunca junto al centro de Valdren |
| Edran | Línea de tierra hundida y recta | Antigua conducción de agua | Zanja seca → Entrada del canal cubierto, con Nela |
| Hoshai | Roca rodada con marcas en la cresta | Rompecimas | Paso entre paredes, Escalones al sol |
| Hoshai | Arañazos de tres en tres, muy altos | Rompecimas (tres garras que tocaron la roca; no es una ficha anatómica) | Ídem; Iria descarta que sean marcas de mantenimiento |
| Korven | Losa con fractura vieja reabierta | Primera señal de Hundepedral | Cauce de piedras movidas → Plataforma de escucha → registro de Oma |
| Korven | Suelo hueco | Corredor alterado por Hundepedral; no prueba que esté debajo | Plataforma de escucha → Registro del cauce, con Oma |
| Korven | Herramienta Dravak oxidada | Trabajo Dravak anterior a las reparaciones de Brumak; no es una civilización perdida | Horno viejo / Rincón de las muestras, con Taren («Una pieza no es todo el pasado») |
| Lethra | Juncos aplastados por algo largo | Dorsalodo | Orilla del canal, raíces cercanas |
| Lethra | Poste de amarre doblado | Una barca que tiró del amarre con la corriente | Patio de las barcas, con Sola |
| Lethra | Cuerda deshilachada | Desgaste por tensión, no un corte ni un sabotaje | Ídem, con Sola |
| Lethra | Algo pequeño con forma de barca bajo el agua | La barquita de juguete de Sola (secreto `lethra_secreto_barquita`) | Orilla del canal |
| Nhal | Árbol joven doblado sin romper la copa | Quebradosel comiendo brotes altos | Raíz marcada, corredores profundos |
| Nhal | Franja donde callan los pájaros | Fauna menor ante una amenaza grande (Rasgacorteza); no detecta monstruos por sí sola | Raíz marcada; después, observar a Rasgacorteza |
| Nhal | Talla de dos líneas y un círculo | Señal de ruta Vesperi antigua; no es runa ni magia | Primer árbol del bosque, Alto de las Raíces; Arel (Patio de mensajes) |
| Veyra | Canal antiguo bajo las piedras | Conducciones antiguas de Vaisgard, de constructor desconocido | Patio del agua, Cruce de canales, Camino sobre la acequia; Nera |
| Veyra | Piedra cortada en otra época | Piedra antigua reutilizada | Cantera vieja, Plaza de las Cinco Rutas; Nera: «las piedras no nos han contado quién las puso» |
| Veyra | Disco de metal desconocido | Función desconocida; **no** afirmar moneda ni economía antigua | Archivo de cargas, con Nera: no coincide con los sellos actuales; el origen queda sin resolver |

Aplicado: huella de Edran (sin «cuatro dedos»), tierra hundida que apunta al canal, losa con fractura vieja reabierta, barquita en lugar de barca grande y disco de metal en lugar de moneda.
Iteración 5 (aplicado):
- Las 16 pistas con bandera (`{"text","flag"}` en `search.traces`) guardan que el jugador las vio.
- 6 acciones de investigación, cada una con su secreto (`world.secrets`): Prado (comparar huellas), Zanja seca (seguir la línea), Paso entre paredes (mirar a la cresta), Cauce de piedras movidas (comparar la grieta), Orilla del canal (seguir los juncos) y Raíz marcada (altura del daño).
- 8 respuestas de personajes que sólo aparecen tras ver la pista: Nela (línea), Iria de Khariel (marcas), Oma (grieta), Taren (herramienta), Sola (amarre), Arel (talla) y Nera (disco y piedras).
- Ninguna nombra a la fauna mayor: el jugador la deduce comparando.

Pendiente: la franja donde callan los pájaros no tiene resolución propia (Raíz marcada ya trata el silencio); la barquita sigue reservada a los Marevyn, como en su secreto original.
