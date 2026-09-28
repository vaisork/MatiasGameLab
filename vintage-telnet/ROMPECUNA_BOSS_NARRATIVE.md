# #363 — Rompecuña: experiencia narrativa BOSS-LOSS-01

Fuente canónica: Historia PR #510 / FIRST_BOSS_CANON.md.

## Aproximación

El encuentro se construye desde el final ya conocido de Cantera Abandonada.

- CA-07 Frente quebrado: empiezan a aparecer bloques movidos y raspaduras bajas demasiado anchas para la fauna común.
- CA-08 Paso entre bloques: pueden sentirse vibraciones espaciadas y una disminución clara de fauna menor.
- CA-09 Cavidad tras el frente: último punto de retorno. Desde aquí pueden oírse respiración grave y desplazamientos de grava desde la cavidad posterior.

CA-09 sigue siendo un umbral seguro. Cruzarlo es una decisión explícita.

## Compromiso

Antes de entrar:
“Más allá del frente, el aire parece inmóvil. Algo pesado cambia de apoyo detrás de la roca y la grava responde bajo tus pies.”

Acciones legibles antes del compromiso:
- observar/evaluar;
- retroceder;
- cruzar el umbral.

Al cruzar:
“Entras en la cavidad. La masa baja de Rompecuña ocupa la continuidad del paso. No te persiguió hasta aquí: tú entraste en su espacio.”

## Fases narrativas

Las fases son de presentación. Jugabilidad fija triggers, números y prepared_actions.

### Fase I — Bloqueo

Rompecuña sostiene terreno y responde a aproximación directa con empuje frontal.

Lectura:
“Rompecuña baja el cráneo en cuña y carga el peso hacia delante. La piedra suelta cruje bajo sus patas.”

Objetivo narrativo: enseñar que el jefe controla espacio y que su amenaza está anunciada.

### Fase II — Cavidad en movimiento

Tras recibir presión suficiente, el combate desplaza grava y pequeños bloques ya fracturados. No se derrumba la cantera ni se cierra la salida.

Lectura:
“El choque desplaza grava y abre un corredor distinto dentro de la misma cavidad. Rompecuña gira el cuerpo ancho para volver a cortarte el paso.”

Objetivo narrativo: cambiar la lectura espacial sin inventar una mecánica de derrumbe.

### Fase III — Último empuje

Herido, Rompecuña no se vuelve mágico ni más inteligente. Reduce distancia y compromete su masa en ataques más directos.

Lectura:
“La respiración se vuelve áspera. Rompecuña deja de reservar espacio y empuja con todo el cuerpo, exponiendo por momentos los costados al corregir la dirección.”

Objetivo narrativo: hacer visible que el enfrentamiento entró en su tramo final.

## Derrota del jugador

Texto base:
“El impacto te saca de equilibrio. Tu arma se desprende de la mano y golpea la piedra cerca del borde de la cavidad. Rompecuña vuelve a ocupar el paso mientras el mundo se apaga alrededor.”

La transición posterior usa el sistema de muerte/respawn vigente. Narrativa no cambia HP, fatiga, heridas ni inventario adicional.

Mensaje posterior al despertar si hubo pérdida:
“Recuerdas dónde cayó tu arma: en la entrada de la cavidad de Rompecuña. No fue destruida ni se la llevó la criatura.”

## Ruta clara de recuperación

La recuperación no requiere matar al jefe ni comprar otra arma.

1. regresar por Cantera Abandonada hasta CA-09;
2. desde el umbral, observar la zona exterior de compromiso;
3. el arma perdida debe ser visible/identificable cerca del borde de la cavidad, fuera de la posición que obliga a iniciar de inmediato un nuevo intento;
4. usar una interacción explícita de recuperación que Jugabilidad/Desarrollo implementen;
5. después de recuperar el estado autoritativo del arma, el jugador decide si retrocede o vuelve a cruzar para otro intento.

Narrativa exige que esta ruta permanezca disponible mientras Rompecuña siga vivo. No se convierte en puzzle, crafting, compra ni quest genérica.

Si el contrato mecánico de Jugabilidad requiere un paso adicional para reactivar el derecho de uso, debe ocurrir dentro de esta misma recuperación explícita y ser comunicado claramente; no se inventa desde Narrativa.

## Victoria

Texto base:
“Rompecuña intenta sostener el paso una vez más. Las patas delanteras ceden y el cuerpo pesado queda inmóvil entre la grava. Las vibraciones que llenaban la cavidad se detienen.”

Después:
“Por primera vez, la continuidad detrás de la cámara deja de estar bloqueada por la criatura. Lo que exista más allá sigue sin estar definido.”

Estado narrativo consumido:
- rompecuna_defeated=true;
- no reaparece;
- cesan señales frescas de su presencia;
- no se revela origen de la cantera;
- no hay tesoro automático.

## Repetición y mundo persistente

- Si rompecuna_defeated=false: las señales y el encuentro pueden existir.
- Si rompecuna_defeated=true: no volver a reproducir respiración, vibraciones frescas ni encuentro.
- La fauna menor puede volver gradualmente cerca del umbral solo cuando el sistema posterior lo autorice.

## Handoff

Narrativa #363: CERRADA para experiencia, derrota/victoria y ruta de recuperación.

Pendientes fuera de Narrativa:
- Jugabilidad: perfil C5, triggers/fases, huida, recompensa y contrato exacto de weapon_loss/recovery.
- Arquitectura/Desarrollo: materializar la cavidad posterior de CA-09 y la interacción autoritativa de recuperación.
- No habilitar weapon_loss_on_defeat=true hasta probar que el arma se puede recuperar.