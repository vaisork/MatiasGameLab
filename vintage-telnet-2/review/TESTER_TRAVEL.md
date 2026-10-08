# Traslados de prueba por personaje

Implementación: permiso explícito `state.tester_enabled === true`, otorgado/revocado por Director. No se concede por nombre, especie ni cuenta. No se habilitó ninguna partida de producción desde esta revisión.

Director: POST `/api/master/tester` con `character_id` entero y `enabled` booleano, sesión DM y CSRF. Sólo personajes aprobados. Cada habilitación/revocación queda en audit.

Jugador: Personaje → «Pruebas: cambiar de lugar». Destinos actuales: hogar propio; Valdren, Khariel, Brumak, Narevia, Velmora, Vaisgard; todos los mercados, fragua, comedor y casas de cuidados canónicos; Entrada del canal cubierto; Puerta del almacén viejo. POST `/api/character/tester/travel` con `destination` y `recover` booleano, sesión propietaria seleccionada, aprobado y permiso habilitado. No acepta destino arbitrario ni identidad ajena.

El salto añade sólo el destino a visited/known y contabiliza la visita; NO añade ruta entre origen y destino. No revela caminos intermedios. No concede experiencia, sellos, equipo, bestiario ni progreso de encargos. La recuperación opcional restaura HP, fatiga y herida, sin inmunidad en combates posteriores. El traslado abandona el combate de este personaje sin borrar el encuentro compartido que puede pertenecer también a otros jugadores. Cada salto queda en audit; la presencia cambia de habitación. Al terminar, vuelve a Aventura y muestra la descripción del destino.

Validación: 28 pruebas test_engine, incluidas autorización, revocación, CSRF, aislamiento de otro personaje, rechazo de habitación secreta, descubrimiento limitado, invariantes de recompensas, recuperación y encuentro compartido retenido. Chrome con API real y base temporal: 320, 393 y 1440 px; traslados entre plaza, fragua, mercado y dos entradas de mazmorra; opciones de compra y NPC presentes; 0 rutas falsas; sin errores JavaScript; regreso a Aventura. No se usó DB producción.

## Habilitación de producción

2026-10-07: la única partida existente era Vaison, cuenta vaison, id1. El usuario pidió convertir a «Bison» en tester; se explicitó la interpretación de transcripción Vaison antes de aplicar el cambio. Con respaldo consistente previo y servidor detenido, se modificó únicamente `tester_enabled=true` y se registró `tester_enable` en audit. Se conservaron ubicación, vitalidad, progreso, bestiario, inventario y rutas. No hubo traslado automático. Servidor reiniciado PID298516; HTTP200 local y Tailscale. Diez imágenes de criaturas ya descubiertas comprobadas HTTP200 por Tailscale.
