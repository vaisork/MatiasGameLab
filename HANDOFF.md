# HANDOFF — Entrega técnica

## ENTREGA — Reloj global de hora del día conectado a `world.get_ambient()` (Issue #138)

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `8336f915cb7d0e48425916d517a1ca7f84643e6a` (origin/main)
**TAREA ASIGNADA:** revisión automática recurrente (Issue #47) sobre el Issue #138. Jugabilidad ya dejó el contrato v1 como comentario en el issue (2026-09-25T02:07): reloj de juego **global y compartido**, amanecer → día → atardecer → noche, ciclo de 4h reales/60 min reales por estado, sin efecto mecánico en v1, y cerró con "Handoff a Servidor: conectar `world.get_ambient()` con este reloj compartido". El Narrador entregó las etiquetas visibles el mismo día.
**RAMA:** `claude/vintage-telnet-server-ambient-clock`

### CAMBIOS (solo `server/world.py` + pruebas; sin esquema, UI nueva, arte ni canon)
- `world._current_time_of_day(now=None)`: función pura de `time.time()` (inyectable) que da amanecer/día/atardecer/noche según el ciclo de 4h/60 min por estado que definió Jugabilidad. Al ser función del tiempo real y no un contador persistente, reiniciar el servidor no reinicia el día de forma arbitraria (lo que pedía el criterio de aceptación del issue).
- `world.get_ambient(room_id, now=None)`: ahora devuelve `time_of_day` con ese reloj; `weather` **sigue en `None`** — el Narrador dejó explícito en el mismo issue que no puede asignar distribución regional de clima sin el canon del Historiador, que todavía no llegó. No se inventa.
- Iconos usados (ya existían en `AMBIENT_ICONS`): amanecer→`amanecer`, día→`sol`, atardecer→`atardecer`, noche→`luna`.

### PENDIENTE, NO INVENTADO
- **NECESIDAD DE HISTORIADOR** (ya registrada por Narrador en el propio Issue #138): canon de clima plausible por región (Edran, Hoshai, Korven, Lethra, Nhal, Vaisgard) antes de que `weather` deje de ser `None`.
- **Registro formal en `GAMEPLAY.md`:** al momento de esta entrega, el contrato de Jugabilidad para #138 solo existe como comentario del issue — la rama `gameplay/issue-138-time-weather-contract` no lo contiene (confirmado con `git diff` contra `main`, sigue igual que cuando Javier lo señaló el 2026-09-24). No me corresponde escribir `GAMEPLAY.md`; lo dejo señalado para Jugabilidad, que ya autorizó explícitamente implementar el reloj sin esperar ese paso ("Desarrollo puede implementar ya el reloj compartido").
- Efectos mecánicos de hora/clima (Percepción con niebla, criaturas nocturnas, Vesperi en baja luz, etc.) siguen fuera de alcance: Jugabilidad dijo expresamente que v1 es solo ambiental/presentacional.

### PRUEBAS
- Suite completa **263/263 OK** (`.venv/bin/python -m unittest discover -s tests`).
- `tests/test_entry.py`: reescribí `test_ambient_slot_is_empty_until_gameplay_and_narrative_define_it` → `test_ambient_shows_shared_time_of_day_but_no_weather_yet` (ya no puede esperar `ambient == {None, None}`; ahora comprueba que `time_of_day` viene poblado, `weather` sigue `None`, y que la barra muestra el chip). Añadí `AmbientClockTests` (5 pruebas nuevas): límites del ciclo/orden, reproducibilidad con la misma `now`, que no depende de un contador (equivalente a sobrevivir un reinicio), `get_ambient` usa el reloj y dejando `weather` sin definir, y que cada estado usa un icono conocido de `AMBIENT_ICONS`.
- `py_compile` limpio en los dos archivos tocados.

**LISTO PARA PUBLICAR:** falta autorización de Javier ("sube"). Sin migración: el esquema sigue igual.

---

## ENTREGA — Sin parpadeo: las acciones del juego ya no recargan la página + barra del enemigo abajo

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `2eb110b` (origin/main)
**TAREA ASIGNADA:** Javier (2026-09-25): "durante la pelea flashea la página; la barra de daño del enemigo se queda arriba, debería verse abajo para que parezca que solo crece la narración".
**RAMA:** `claude/vt-no-flash`

### CAMBIOS (solo `server/templates/entry.html` + pruebas; el servidor no cambia)
- **Sin recarga.** Un listener `submit` delegado intercepta **solo los formularios dentro de `.game-shell`**: cruz, acciones de combate y exploración, cuadro de comando y "mirar". Login, logout, especie, clase y DM siguen normales. Hace el mismo POST/GET (mismas rutas, mismo CSRF, mismas reglas) con `fetch`, parsea la respuesta y **reemplaza solo las regiones `[data-swap]`**: place, art, terminal, controls y side. También actualiza la clase del `.game-shell`.
  - La imagen **no se reemplaza** si su `src` es el mismo; así no parpadea al caminar dentro de un pueblo.
  - Si la respuesta no es una pantalla de juego (sesión vencida, 403, etc.) o falla la red, hace una navegación normal a `/`.
  - Evita dobles envíos mientras hay una acción en curso. El cuadro de comando se limpia después de enviar.
  - `afterRender()` (scroll al último resultado y revelado del texto) corre al cargar y después de cada acción. "Examinar" y el fallback de la imagen usan delegación para seguir funcionando tras el reemplazo.
- **Barra del enemigo abajo.** Nombre y banda de condición en `.enemy-status`, una franja fija entre el relato y la pista. El comportamiento de la criatura queda como primera línea del relato.

### PRUEBAS
- Suite **258/258 OK**, con 2 nuevas en `NoFlashTests` (la clase también hereda las 3 de estabilidad).
- En Chromium a 390 px, con una marca en `window` y un contador de navegaciones: se caminó con botón, flecha ← y comando escrito, y se peleó con Mordelinde 4 turnos hasta la victoria. **0 recargas** (la marca sobrevivió), posiciones de imagen, terminal, botones, comando y barra del enemigo **idénticas** turno a turno, sin errores de JS.

**LISTO PARA PUBLICAR:** falta la autorización de Javier ("sube"). Sin migración: el esquema sigue en 10.

---

## ENTREGA — Relato de la pelea (historial de combate) + la pantalla siempre cabe en el celular

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `5d4a31d` (origin/main)
**TAREA ASIGNADA:** Javier (2026-09-25): "sí, hazlo" — guardar el historial de la pelea para leerla turno por turno.
**RAMA:** `claude/vt-combat-log`

### CAMBIOS
- **Esquema v9 → v10.** Nueva tabla `combat_log` (id, player_id, room_id, action, text, created_at) con índice. Es aditiva: no toca datos existentes.
- `store.append_combat_log` / `get_combat_log` (últimas 20 líneas) con **poda a 30 líneas** por encuentro. `start_encounter` borra el relato viejo si el encuentro es nuevo y `clear_encounter` lo borra al terminar la pelea: victoria, huida o derrota. **Nunca crece.** Una pelea ocupa unos 2 KB.
- `app.py`: `_record_combat` envuelve atacar, huir, esquivar, resistir y bloquear, y hay un envoltorio para evaluar. Registra la acción venga de un botón, de un comando escrito o de `/api/intent`. No registra nada si no hay criatura (`no_target`) ni si la pelea ya terminó.
- `room_view` expone `combat_log` en combate. `entry.html` lo muestra como relato (`> acción` + texto), con la última línea destacada. En combate, el cuadro de lectura siempre se desplaza hasta lo más reciente.
- **Layout en teléfono** (arregla un recorte real): `.app` y `.layout` pasan a columna flex, y el terminal toma **exactamente el espacio que sobra**. Antes el cuadro se aplastaba y la última línea quedaba oculta, y además sobraban ~220 px abajo. En pantallas bajas (≤720 px de alto, como el iPhone SE) la imagen mide 120 px.

### PRUEBAS
- Suite **253/253 OK**, con 3 nuevas en `CombatLogTests`: relato por turnos también por comando, poda a 30, sin criatura no se registra y se borra al terminar. Las simulaciones de bases v7/v8 ahora tampoco tienen `combat_log`.
- Migración real de una base **v9 con 3 jugadores** → v10: jugadores intactos y `integrity_check ok`.
- En Chromium a 390×844, 375×667 y 820×1180, en exploración y en combate de 4 turnos:
  - las posiciones de imagen, terminal, comando y barra son **idénticas** turno a turno;
  - el terminal nunca queda bajo los controles;
  - la última línea siempre está a la vista;
  - la página no desborda.

### DEPLOY
`sudo vt-deploy latest` aplica la migración v9 → v10 con respaldo y ensayo previo, como hizo con la v9.

**LISTO PARA PUBLICAR:** falta la autorización de Javier ("sube").

---

## ENTREGA — Pantalla estable: la imagen y los controles ya no se mueven

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `b8b749b` (origin/main)
**TAREA ASIGNADA:** Javier (2026-09-25), después de probar en su celular: "la zona de imágenes se va y regresa, debe quedarse quieta" y "la pantalla se ajusta a cada rato".
**RAMA:** `claude/vt-art-stable`

### CAUSAS ENCONTRADAS
1. Todo se servía con `Cache-Control: no-store`, **incluida la ilustración** (~425 KB). En cada acción el celular volvía a descargarla y el marco quedaba vacío hasta que llegaba.
2. **21 de 25 salas no tienen arte aprobado**: el marco desaparecía y todo saltaba hacia arriba.
3. El texto de la sala aparecía letra por letra **haciendo crecer el terminal**, y la cruz y los botones bajaban mientras tanto.
4. El terminal cambiaba de alto según el largo del texto de cada sala, y en el teléfono usaba `dvh`, que cambia cuando el navegador muestra u oculta su barra.

### CAMBIOS
- `server/app.py`: iconos, arte, mapas y UI (`app_icon`, `html_ui_assets`, `location_assets`, `map_assets`) → `Cache-Control: public, max-age=86400`. Páginas y API siguen con `no-store`.
- `entry.html`:
  - El marco de arte **siempre existe** con alto fijo. Sin arte aprobado muestra un marco sobrio con ícono y nombre del lugar (rojizo en combate); no se inventa ninguna imagen. La imagen ya no usa `loading="lazy"` sino `fetchpriority="high"`.
  - El texto completo **ocupa su lugar desde el inicio**; la parte no revelada es invisible (`visibility:hidden`).
  - Terminal de **alto fijo** (`30svh` exploración / `42svh` combate, con `dvh` de respaldo) que se desplaza por dentro, y `.app` en `100svh`.

### PRUEBAS
- Suite **242/242 OK**, con 3 nuevas en `tests/test_screen_stability.py`.
- Medición en Chromium a 390 px: posición vertical de arte, terminal, cruz, comando y barra al cargar, a los 0.4 s y a los 3 s, en Valdren (con arte) → Sendero (sin arte) → Valdren → Mercado (con arte). **Idéntica al píxel en los 12 puntos.**

### SEGUNDA RONDA (Javier, 2026-09-25)
Pidió que el marco de imagen siga esta regla: pueblo → su imagen fija; camino → imagen de camino; pelea → el animal; sin nada que mostrar → vacío y quieto. También pidió botones ~20 % más chicos, letra ~10 % más chica, más espacio de lectura, y las imágenes de las especies en la pantalla de elegir especie.
- **Pueblos:** Khariel, Brumak, Narevia y Velmora ya tenían arte **aprobado y publicado desde el 2026-09-23** (commits `6de5885`, `0f07a28`, `81ed307`, `c5af42b`), pero nunca se había conectado. Ya están en `VISUAL_CONTEXT_ART`, así que los 6 asentamientos muestran su imagen.
- **Caminos** (`zone.veyra.road`, `zone.edran.valdren_outskirts`): el marco queda vacío hasta que Arte publique la imagen; después basta agregar la fila en `VISUAL_CONTEXT_ART`.
- **Combate:** `creatures.CREATURE_ART` (vacío por ahora) y la ruta `/assets/creatures/<archivo>` (cacheable). En combate el marco muestra la criatura o queda vacío; nunca el paisaje. Solicitud de arte registrada en una issue para el Director de Arte.
- **Marco vacío:** sin texto ni ícono, solo el marco, como pidió Javier.
- **Especies:** la ruta `/assets/species/<archivo>` sirve las 5 fichas aprobadas (`assets/vintage-telnet/species/`). Cada tarjeta muestra la ficha **completa** (Javier: "me gusta cómo se ve") y el enlace "Ver ficha completa" para abrirla grande. Se quitó "Retrato pendiente de asset aprobado".
- **Tamaños:** bloque "Compacto" al final del CSS. Botones ~20 % más bajos (acción 46→37 px; en teléfono 44→36, cruz 40×37, barra inferior 54→44) y letra del terminal ~10 % menor (15→13.5 px en teléfono). Terminal más alto: 36svh exploración / 46svh combate / hasta 40svh en escritorio. El cuadro de comando conserva 16 px de letra por el zoom de iOS.
- **Pruebas:** 242/242 OK. En Chromium a 390 px, Khariel → Sendero → Khariel → Vaisgard → Camino del Norte: arte, terminal, cruz, comando y barra en la **misma posición** al cargar y a los 3 s. También revisado a 820×1180 (iPad).

### TERCERA RONDA (Javier, 2026-09-25): "cuando hay pelea no es necesario saber cómo se ve el lugar, solo leer cómo sucede la pelea"
- En combate, el cuadro de lectura **no muestra la descripción del lugar ni las salidas**: solo la criatura, su banda de condición, su comportamiento y el resultado de cada acción.
- **Dentro del juego, el resultado de cada acción** (combate, examinar, descansar, equipar…) se escribe **en el cuadro de lectura** (`.result-entry`, rojizo en combate) y ya no en el aviso de arriba (`alert-note`), que empujaba toda la pantalla. El aviso de arriba queda solo fuera del juego: login, especie y clase.
- El cuadro de lectura se desplaza solo para que el último resultado quede a la vista.
- Pruebas: **247/247 OK**, con 2 nuevas en `test_screen_stability.py`. En Chromium a 390 px, las posiciones antes y después de atacar son **idénticas**.
- Pendiente sugerido, fuera de esta entrega: hoy solo se ve el resultado de la **última** acción. Un historial de la pelea (varios turnos seguidos) requeriría guardar el registro de combate en el servidor.

**LISTO PARA PUBLICAR:** falta la autorización de Javier ("sube"). Luego se despliega con `sudo vt-deploy latest`.

---

## ENTREGA — Seguridad: panel del DM solo desde la red privada (no desde internet)

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `bbc5b1c` (origin/main)
**TAREA ASIGNADA:** Javier (2026-09-25): entendía que el panel del DM solo funcionaba desde la Raspberry. Verifiqué que **no era así**: `https://raspberrypi.tail3d212e.ts.net/dm` respondía 200 desde internet y mostraba el formulario de contraseña.
**RAMA:** `claude/vt-dm-private`

### CAMBIOS (`server/app.py` + pruebas)
- Nuevo `before_request` `dm_panel_is_private`, que corre **antes** que CSRF y el login. Si la petición trae `Tailscale-Funnel-Request` (lo agrega Tailscale Funnel a todo lo que llega desde internet), `/dm` y `/dm/*` responden **404**, como si no existieran.
- Una sesión de DM abierta desde la red privada **no da poderes de DM** si la petición llega por internet: `g.dm` es falso en ese caso.
- Los jugadores no cambian nada: `/`, `/healthz` y todo el juego siguen públicos por Funnel.
- El DM entra igual que antes desde la red Tailscale (celular o compu con Tailscale) o en la Raspberry misma (`http://127.0.0.1:8080/dm`).

### PRUEBAS
- Suite completa **239/239 OK**, con 4 pruebas nuevas en `tests/test_dm_private.py`:
  - desde Funnel todas las rutas del DM dan 404;
  - desde la red privada funciona;
  - una sesión de DM no sirve por Funnel;
  - los jugadores no se ven afectados.

### VERIFICACIÓN PENDIENTE EN PRODUCCIÓN (la puede hacer cualquiera desde fuera)
- Después de `sudo vt-deploy latest`: `curl -s -o /dev/null -w "%{http_code}" https://raspberrypi.tail3d212e.ts.net/dm` debe dar **404**. Desde la red Tailscale debe seguir dando 200.
- Si diera 200, Funnel no está enviando la marca en esa versión de Tailscale. No se rompe nada, pero el panel seguiría público: reportarlo y usar la alternativa de apagar Funnel para `/dm`.

### RECOMENDACIÓN
- Usar una contraseña del DM (`VT_DM_PASSWORD` en `/etc/vintage-telnet/server.env`) larga, de 16 caracteres o más.

**LISTO PARA PUBLICAR:** falta la autorización de Javier ("sube"). Lo ideal es que el Arquitecto de Vintage Telnet lo revise, por ser un cambio de seguridad.

---

## ENTREGA — Vintage Telnet: navegación (minimapa, salidas con nombre, flechas del teclado)

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `ca101d4` (origin/main)
**TAREA ASIGNADA:** Javier (sesión directa, 2026-09-24): seguir mejorando la navegación y las pantallas en la línea de la maqueta que aprobó (#135, panel "Mapa y orientación").
**RAMA:** `claude/vintage-telnet-ui-navigation`

### CAMBIOS
- **Minimapa real en Mapa general.**
  - Dibuja en SVG solo lo que el personaje conoce: lugares visitados con su nombre, tu ubicación (dorada), rutas recorridas y las salidas sin explorar de cada lugar visitado (línea punteada, sin nombre ni destino).
  - La leyenda es la de la maqueta: Tu ubicación / Lugar conocido / Ruta recorrida / Salida sin explorar.
  - Si el mapa es poco más ancho que la pantalla se reduce para verse completo; si es mucho más grande se desplaza con el dedo, centrado en tu ubicación.
  - El mapa regional ilustrado queda debajo, como "Región inicial".
- **Servidor, `world.map_layout()`:** coordenadas de rejilla calculadas solo con las salidas reales (norte = arriba, etc.), una vez para todo el mundo, así la posición de una sala no cambia según lo descubierto. Si dos salas caen en la misma celda, la segunda se desplaza a la siguiente celda libre en su dirección; hoy no hay colisiones en las 25 salas.
- **`/api/map`** agrega `current_room`, `places` [{id, name, x, y, current}] y `unexplored_exits` [{from, direction}]. Las claves anteriores (`visited_rooms`, `traversed_routes`, `current_heading`) siguen igual.
- **La lista de lugares y rutas** usa nombres reales ("Mercado de Valdren") en vez de ids ("valdren mercado") y marca "estás aquí".
- **Línea "Salidas"** en el terminal fuera de combate, por ejemplo: `Salidas: sur (Camino del Norte) · norte · este`.
  - El nombre del destino aparece **solo si ya lo visitaste**, porque el mapa es progresivo (GAMEPLAY §23); una salida nueva muestra solo la dirección.
  - Lo mismo en el título y la etiqueta accesible de los botones de la cruz.
  - `room.exits[].known_name` también sale en `/api/room`.
- **Flechas del teclado** (↑↓←→) para moverse en computadora. Pulsan el mismo botón de la cruz, así que aplican las mismas reglas del servidor. No actúan mientras se escribe ni con un panel abierto.

### PRUEBAS
- Suite completa: **232/232 OK**, con 4 pruebas nuevas en `tests/test_navigation.py`:
  - la rejilla cubre todas las salas sin colisiones y es estable;
  - el minimapa solo expone lo conocido;
  - los nombres de salida aparecen solo después de visitar;
  - el panel y el teclado están cableados.
- En Chromium a 390 px contra el servidor real, caminando por Valdren y luego Valdren → Vaisgard → Khariel/Narevia:
  - la flecha → mueve igual que el botón;
  - el minimapa se lee con halo oscuro bajo los nombres;
  - no hay scroll horizontal de página ni errores de JS.

### NO CAMBIA
Movimiento, reglas, combate, persistencia, esquema (sigue en v9) y canon. La rejilla es una representación esquemática derivada de las salidas existentes; no inventa geografía.
## ENTREGA — vt-deploy: prueba completa en Raspberry simulada + reintento después de rollback

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `ab61e88` (rama `vt-ops/fix-vt-deploy-uuid-ids`, corrección de IDs UUID del Operador de Raspberry) sobre `main` @ `ca101d4`
**TAREA ASIGNADA:** Javier (2026-09-24) pidió revisar si el programa de despliegue del Arquitecto (`vt-deploy`, PR #142, Issue #141) realmente sirve.
**RAMA:** `claude/vt-deploy-retry-after-rollback`. Incluye el commit de la corrección UUID.

### PRUEBA REAL (Raspberry simulada en la nube)
- Monté las mismas rutas en una carpeta aislada:
  - release anterior `0ffcc36` (esquema 7) como `current`;
  - base con 3 jugadores creada con esa versión (uno en combate, uno con espada equipada, un Vesperi);
  - `systemctl` y `ss` de prueba que arrancan y detienen el servidor real y corren el `backup.sh` real.
- Usé una copia de `vt_deploy.py` con solo las rutas cambiadas; la lógica es idéntica.
- **Deploy normal:** `vt-deploy latest` pasó de 7 a **9** en ~1 min. Tests OK, backup verificado, migración ensayada en copia, `healthz` OK, **3 jugadores preservados** y preflight 6/6. ✅
- **Rollback:** forcé una falla después del cambio (preflight ve el puerto 8080 expuesto). El rollback regresó `current` al release anterior, restauró la base y el servicio siguió sano. ✅
- **Bug encontrado:** tras ese rollback, el siguiente `vt-deploy latest` del mismo SHA se negaba a correr ("El release … ya existe pero no es current"). Había que borrar a mano con sudo en la Raspberry. ❌

### CAMBIOS
- `ops/vt_deploy.py`:
  - `quarantine_failed_release()`: tras un rollback, o si falla entre crear el release y activarlo, el release fallido se **aparta** a `releases/.failed-<sha>-<UTC>`. Nunca se borra; queda como evidencia. Nunca aparta el release `current`.
  - Timeout de la suite en el deploy: 300 s → **1200 s**. En la nube tarda ~50 s y en una Raspberry puede tardar varias veces más; así no se aborta un deploy sano por lentitud.
- `ops/install_vt_deploy_command.sh`: corrige el `\n` literal en el mensaje final que reportó el Operador en #141. Es solo cosmético.
- `tests/test_vt_deploy.py`: 3 pruebas del apartado.
- **Verificado de nuevo en la simulación:** falla → rollback → release apartado → corregir → `vt-deploy latest` del mismo SHA → **DESPLIEGUE OK**.

### PRUEBAS
- Suite completa **231/231 OK**. `sh -n` y `py_compile` OK.

### PENDIENTE
- Primera instalación y deploy **en la Raspberry física**, que es el criterio de cierre de #141.
- Nota para quien instale: si hay una copia vieja de `vt_deploy.py` ya instalada en `/usr/local/lib/vintage-telnet/`, hay que volver a correr el instalador después de integrar esta rama.

**LISTO PARA PUBLICAR:** falta la autorización de Javier ("sube").

---

## ENTREGA — Vintage Telnet Issue #112: elección de clase inicial + arma inicial por clase

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `0ffcc36` (origin/main)
**TAREA ASIGNADA:** Issue #112. Javier la asignó en sesión directa (2026-09-24) al pedirme que revisara el trabajo pendiente y lo resolviera según sus peticiones. Era la única entrada abierta que se podía programar sin inventar decisiones: #83 y #19 solo esperan prueba física, y #114/#115 dependen de decisiones abiertas de Arquitectura, Narrativa y Jugabilidad.
**RAMA:** `claude/vintage-telnet-server-issue-112-class`

### CAMBIOS
- **Flujo:** crear/entrar → elegir especie → **elegir clase** → mundo. Mientras falte la clase, el mundo no avanza. Las rutas HTML devuelven 403 y las API `/api/room`, `/api/intent` y `/api/move` devuelven `409 class_required`, igual que ya pasaba con `species_required`. Las consultas de solo lectura (`/api/character`, `/api/inventory`, `/api/map`) siguen abiertas.
- **Clases:** Arcano, Juramentado, Sombra y Artífice (`world.CLASSES`), con la orientación copiada de `CONFIRMED_IDEAS.md`. No incluyen poderes, bonos ni números nuevos. El texto de la pantalla repite `GAMEPLAY.md` §2: la clase orienta, pero no encierra.
- **Arma inicial:** `items.STARTER_WEAPON_BY_CLASS` asigna Varita de aprendiz, Espada de juramento, Puñal de camino y Arco de ruta. Sale de la "Obtención narrativa" de `WEAPON_CATALOG.md` y reemplaza el perfil técnico `BaseArma=10` de §24.10. Se entrega como entrega autoritativa (§32.5), en la **misma transacción** en que se guarda la clase, y queda equipada solo si el personaje no tenía otra arma activa.
- **Persistencia:** migración de esquema **v8 → v9** (originalmente v7→v8; ver reconciliación), que agrega la columna `players.player_class` con un `CHECK` de las 4 clases. `store.set_player_class` solo tiene efecto una vez y exige especie previa. Usa `BEGIN IMMEDIATE` y `rowcount`, así que si llegan dos elecciones al mismo tiempo gana una y se entrega una sola arma.
- **Rutas:** `POST /class` (formulario) y `POST /api/class` (JSON, responde con `player_class`, `starter_weapon` y `player`). `/api/character` ahora también expone `species` y `player_class`.
- **`entry.html`:** agregué el paso de clase, que reutiliza las tarjetas de especie: 2 columnas en tableta y 1 en celular. La clase también aparece en "Estado visible" y en el panel Personaje.

### PRUEBAS
- Suite completa: **206/206 OK**, con 10 pruebas nuevas en `tests/test_class_choice.py`:
  - el paso de clase aparece después de la especie y bloquea el mundo;
  - no se puede elegir clase sin especie;
  - cada clase recibe su arma del catálogo, equipada;
  - se elige una sola vez y una clase desconocida se rechaza;
  - contrato de `/api/class`;
  - concurrencia: una sola clase y una sola arma;
  - el arma inicial no reemplaza un arma ya equipada;
  - un personaje v7 con progreso migra a v8 conservando especie, sala y XP, y elige clase al volver.
- En las pruebas existentes de combate, inventario y piloto, la clase se asigna **sin arma inicial** para conservar el perfil base con el que fueron escritas. Las de gameplay y entrada usan el flujo real `/class`. Además actualicé `schema_version` 7→8 y el inventario esperado de una prueba de UI (ahora incluye el puñal de Sombra).
- Probé a mano contra el servidor real (waitress) con Chromium a 390 px y 1280 px: la pantalla de clase se lee bien. Elegir Juramentado entra a Valdren con la Espada de juramento equipada (`/api/inventory`) y la página no tiene scroll horizontal.

### TRABAJO PREVIO AFECTADO
- Los personajes que ya existen en la Raspberry verán la pantalla de clase la próxima vez que entren, **sin perder** especie, sala, XP ni inventario.
- `combat.py`, `creatures.py`, las criaturas, la narrativa y el canon no cambiaron.
- No hay otro cliente que consuma `species_required` (revisé con grep), así que ningún cliente externo se rompe con `class_required`.

### RECONCILIACIÓN CON #132/#134 (2026-09-24)
- #132 (PP y fatiga) entró a `main` junto con #134 y ocupó el esquema **v8**. La migración de clase pasa a **v8 → v9** (`store.SCHEMA_VERSION = 9`).
- `POST /api/character/attributes` (#132) también exige clase (`409 class_required`), igual que el resto de rutas de juego.
- `tests/test_progression.py`:
  - su base v7 simulada ahora tampoco tiene `player_class`;
  - sus personajes eligen clase sin arma inicial, para no alterar las pruebas de progresión.
- Suite completa tras el merge: **226/226 OK**. En navegador a 390 px: especie → pantalla de clase → Arcano → gasto de PA desde Personaje, sin errores de JS.

### PENDIENTES / DECISIONES PARA OTROS ROLES
- **NECESIDAD DE JUGABILIDAD:** confirmar que el arma inicial se entrega y queda equipada al elegir la clase, y con qué arma por clase. Si cambia, solo cambia `STARTER_WEAPON_BY_CLASS`.
- Siguen fuera de alcance: poderes por clase, sobrecoste fuera de clase (§20.12), cambio de clase y arte de las clases.
- **Raspberry:** el despliegue aplica la migración a v9 (desde v7 o v8). Conviene hacer respaldo antes, como en migraciones anteriores.
- **Observación para Frontend (no es de esta entrega):** a 390 px, el marco del terminal y los botones se ven cortados unos px en el borde derecho. Pasa igual en `main`, aunque la página no hace scroll horizontal.

**LISTO PARA PUBLICAR:** NO. Queda para revisión del Arquitecto de Vintage Telnet / Integrador y autorización de Javier ("sube").
## ENTREGA — Vintage Telnet Issue #135: pantalla principal según la maqueta del Director de Arte

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `fdc726b` (origin/main)
**TAREA ASIGNADA:** Issue #135. Javier (2026-09-24) aprobó la maqueta de 3 pantallas del Director de Arte y la asignó con prioridad ALTA. Las decisiones de contenido (hora del día, HP del enemigo) quedan para Jugabilidad/Narrador.
**RAMA:** `claude/vintage-telnet-ui-main-screen`

### CAMBIOS (solo `server/templates/entry.html` + pruebas)
- **Barra de lugar** con ícono de ubicación y nombre de la sala. En combate se pone roja, con espadas y la etiqueta **¡COMBATE!**.
- **Ilustración enmarcada** (`room.art`) arriba del terminal; se conserva el fallback si falta la imagen.
- **Terminal verde:** conserva el revelado progresivo, la pista y el chat.
- **Exploración:**
  - cruz N/O/●/E/S en verde con flechas; las salidas que no existen se ven apagadas;
  - a la derecha, Mirar, Examinar y Descansar con ícono. Descansar solo aparece si `available_actions` lo autoriza;
  - **Examinar** solo escribe "examinar " en el cuadro de comando y lo enfoca: no ejecuta nada ni aplica reglas.
- **Combate:**
  - **Atacar** grande y rojo; debajo Huir (azul) y Evaluar (dorado), y luego Esquivar/Resistir/Bloquear según `available_actions`;
  - banda de **condición cualitativa** del enemigo: 4 segmentos que salen de la etiqueta de `enemy_condition` (entero/herido/malherido/al borde). **Nunca muestra HP numérico** (GAMEPLAY §31);
  - la cruz de movimiento no se muestra en combate, igual que en la maqueta. Moverse escribiendo el comando sigue funcionando igual que antes.
- **Barra inferior:** Personaje, Inventario, Mapa y Ayuda. En teléfono el ícono va arriba del texto.
- **Mapa:** debajo del mapa regional se muestran "Estás en: <sala>" y una tarjeta "Dirección actual" con brújula y "Caminando hacia: <rumbo>" (`current_heading`). La pestaña "Dirección actual" se conserva.
- **Corrección de desborde en teléfonos (ya existía en `main`):** la columna implícita de `.app` y la de `.layout` crecían hasta el ancho de la pista de una sola línea, y el marco se cortaba unos px a la derecha. Ahora son `minmax(0,1fr)`.
- Todo con HTML/CSS/SVG (frontera #109). Agregué 4 íconos SVG: ubicación, lupa, cama y correr.

### PRUEBAS
- Suite completa: **217/217 OK**.
  - Nueva prueba del estado de exploración y de combate: barra de lugar, controles, banda de condición y que no aparece "HP n/n".
  - El placeholder del comando cambió a "> norte, mirar, examinar…", como en la maqueta; ajusté la prueba que lo fijaba.
- Chromium a 390 px contra el servidor real (waitress), en exploración en Valdren, combate con Mordelinde y el panel Mapa:
  - `scrollWidth == innerWidth` y **ningún elemento pasa del borde derecho**;
  - sin errores de JS;
  - Examinar rellena el cuadro.
- Revisé también a 1280 px: el panel lateral "Estado visible" se conserva.

### SEGUNDA RONDA (petición de Javier, 2026-09-24)
- **Espacio para hora del día y clima.** El servidor expone `ambient: {time_of_day, weather}` en cada sala mediante `world.get_ambient(room_id)`, que hoy siempre devuelve vacío.
  - La barra de lugar muestra hasta 2 etiquetas con ícono. Íconos SVG disponibles: sol, luna, amanecer, atardecer, nube, lluvia, niebla, nieve, tormenta, viento.
  - Qué estados existen y cómo cambian lo definen **Jugabilidad y Narrador en la Issue #138**, por petición expresa de Javier. No se inventó ningún estado; sin datos no se muestra nada.
- **Letra un poco más pequeña** para que quepa mejor:
  - terminal a 15 px en teléfono (antes 17) y clamp(.95–1.02rem) en escritorio;
  - botones de acción a .8rem;
  - Atacar a 56 px de alto.
  - El cuadro de comando se queda en **16 px** a propósito: con menos, iPhone hace zoom al escribir.
- Pruebas: **218/218 OK**, con una nueva que comprueba que el ambiente está vacío por defecto y se muestra con datos. Un ícono desconocido aparece solo como texto.
- Captura a 390 px con un ambiente de ejemplo inyectado solo en la prueba: la barra muestra "☀ Mañana · ☁ Despejado" sin desbordar.

### NO IMPLEMENTADO (lo decide Jugabilidad/Narrador; registrado en #135 y #138)
- Estados concretos de hora del día y clima (#138).
- Barra de HP numérica del enemigo; se usa la banda de condición.
- El contenido de ejemplo de la maqueta (jabalí salvaje, etc.) no se copió.
- Marcadores o leyenda sobre la imagen del mapa: la imagen es estática y no dibujamos marcadores.

### AVISO DE INTEGRACIÓN
- #133 (clase) también toca `entry.html`, pero en zonas distintas: pantalla de clase y panel Personaje. `git merge-tree` confirma que el código se combina sin conflicto. El único conflicto es de texto en `HANDOFF.md`, porque ambas entregas agregan su entrada arriba: se conservan las dos.

**LISTO PARA PUBLICAR:** NO. Queda para revisión del Integrador/Director de Arte y autorización de Javier ("sube").

---

## ENTREGA — Vintage Telnet: pantalla para gastar PA en el panel Personaje

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `e122c56`, rama `claude/vintage-telnet-server-progression-fatigue` (PR #132, otra sesión), sobre `main` @ `8ba4d1d`
**TAREA ASIGNADA:** Javier autorizó en sesión directa (2026-09-24) que yo hiciera el frontend pendiente de la PR #132. Lo avisé en la PR #132.
**RAMA:** `claude/vintage-telnet-server-pa-screen`. **Depende de #132**: se integra después de ella o junto con ella.

### CAMBIOS (solo `server/templates/entry.html` + una prueba)
- El panel **Personaje** tiene ahora la sección "Mejorar atributos". Al abrirse:
  - lee `GET /api/character` (`attributes`, `attribute_costs`, `pa_unspent`, `pp_unspent`, `in_combat`);
  - muestra cada atributo con su valor, el coste del siguiente +1 y un botón "+1 <atributo>".
- **Confirmación explícita (§25.5):** antes de gastar aparece "Fuerza: 10 → 11. Cuesta 1 PA y te quedarán 5 PA. Después de confirmar no se puede deshacer.", con los botones Cancelar y Confirmar. Cancelar no gasta nada.
- Al confirmar se envía `POST /api/character/attributes` con `current_value` = el valor que el jugador vio. Si cambió, el servidor responde `stale_confirmation`, el panel recarga los datos y muestra el mensaje del servidor.
- Los botones quedan deshabilitados sin PA suficientes o en combate (`in_combat`). **El cliente no calcula costes ni reglas**: todo sale del servidor.
- Después de un gasto, los bloques Estado, Progreso y Atributos se actualizan al instante. Al cerrar el panel, la página se recarga para refrescar también "Estado visible".
- Sin JavaScript, el panel queda informativo y los PA siguen guardados.

### PRUEBAS
- Suite completa sobre la rama: **216/216 OK**, incluida una prueba nueva en `test_entry.py` sobre el cableado del panel: contrato, confirmación, `current_value` y que el cliente no calcula costes.
- Probé de punta a punta contra el servidor real (waitress) con Chromium a 390 px:
  - con 6 PA, "+1 Fuerza" → Confirmar deja Fuerza en 11 y 5 PA (verificado con `/api/character`);
  - Cancelar no gasta nada;
  - la confirmación de un atributo de abajo aparece a la vista;
  - no hay scroll horizontal ni errores de JS en consola.

### PENDIENTES
- PP: se muestra el saldo, pero no hay gasto porque los poderes no existen todavía (§25.8).
- Integración: depende de #132. Con #133 (clase) no hay conflicto de código en `entry.html`: tocan zonas distintas del mismo archivo, pero conviene integrarlas en orden, #132 → esta → #133 (reconciliada a esquema v9).

**LISTO PARA PUBLICAR:** NO. Queda para revisión del Integrador y autorización de Javier ("sube").

---

## ENTREGA — Vintage Telnet Issue #125: `visual_context_id` server-side, arte por contexto no por `room_id`

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `200e24c543cba1699821022d594f5d955916df62` (origin/main)
**TAREA ASIGNADA:** Issue #125 — "VT-SERVER/UI: contexto visual persistente
por zona sin inferir narrativa" (Historiador, P1, `ROLE: developer-vt`).
**RAMA:** `claude/vintage-telnet-server-visual-context`

### ORIGEN
`describe_room()` en `world.py` resolvía `room.art` por `LOCATION_ART.get(room_id)`
exacto: solo `valdren_centro` y `vaisgard` tenían imagen, así que la
ilustración desaparecía al entrar a la forja/mercado de Valdren aunque
seguían siendo el mismo pueblo — justo el bug que reportó Javier y que
`vintage-telnet/VISUAL_CONTEXT_CANON.md` (Historiador, issues #87/#92)
documenta como contrato pendiente de implementar en servidor.

### CAMBIOS (solo `vintage-telnet/server/world.py`)
- `LOCATION_ART` (por `room_id`) → `VISUAL_CONTEXT_ART` (por
  `visual_context_id`), mismo contenido de los dos assets ya aprobados
  (`zone.valdren`, `zone.vaisgard`), ningún asset nuevo inventado.
- `ROOM_VISUAL_CONTEXT_OVERRIDES`: excepciones explícitas del canon —
  `vaisgard`, `road_north`/`road_west` (`zone.veyra.road`) y las 4 salas de
  "Alrededores de Valdren" (`zone.edran.valdren_outskirts`).
- `get_visual_context_id(room_id)`: nueva función pública. Devuelve la
  excepción si existe; si no, cualquier sala cuyo `room_id` empiece con el
  prefijo de uno de los 5 pueblos hereda `zone.<pueblo>` — exactamente lo
  que el canon autoriza para "cualquier nueva micro-sala claramente interna"
  sin que yo tenga que tocar este archivo de nuevo cuando aparezcan más.
  Sin asset aprobado → `None` (fallback sobrio, ninguna imagen inventada).
- `describe_room()` ahora expone `visual_context_id` (dato estructurado,
  como pide el canon para que el frontend no tenga que inferir nada) y
  resuelve `art` desde `VISUAL_CONTEXT_ART.get(visual_context_id)` en vez
  de por `room_id`.
- No toqué `entry.html`: ya consume `room.art.src/alt/width/height` tal
  cual, así que el fix es transparente para el cliente actual. No cambié
  gameplay, persistencia, salidas ni texto narrativo de ninguna sala.

### PRUEBAS
- Suite completa: **194/194** (`.venv/bin/python -m unittest discover -s
  tests -v`), incluida la prueba preexistente de arte de Valdren sin
  modificar.
- 4 pruebas nuevas en `vintage-telnet/tests/test_entry.py`:
  - forja/mercado de Valdren comparten `visual_context_id` y `art` con el
    centro (el bug reportado, ahora corregido);
  - el sendero/lindero de Valdren cambian de contexto a "Alrededores de
    Valdren" aunque compartan prefijo `room_id` (frontera del canon);
  - un contexto sin asset aprobado (ej. Khariel) devuelve `art: None`, no
    inventa imagen;
  - las ~25 salas reales de `world.ROOMS` resuelven `visual_context_id` de
    forma consistente entre `describe_room()` y `get_visual_context_id()`.
- Verificado a mano con un script que imprime `visual_context_id`/`art`
  para cada sala de `world.ROOMS` y lo comparé fila por fila contra la
  tabla "Mapeo de las salas actuales" de `VISUAL_CONTEXT_CANON.md`: coincide
  exactamente.

### TRABAJO PREVIO AFECTADO
Solo `vintage-telnet/server/world.py` (dato de mundo) y el archivo de
pruebas. No toqué `combat.py`, `app.py`, `store.py`, `creatures.py`,
`entry.html`/`vintage-telnet.html` ni ningún archivo de Senku. No hay
`LOCATION_ART` residual: era interno a `world.py`, sin otras referencias en
el repo (confirmado por grep antes de renombrar).

### PENDIENTES (fuera de esta entrega)
- Los 5 contextos que aún no tienen asset aprobado en runtime
  (`zone.khariel`, `zone.brumak`, `zone.narevia`, `zone.velmora`,
  `zone.edran.valdren_outskirts`, `zone.veyra.road`) siguen mostrando sin
  imagen — correcto según el canon ("ninguno aprobado todavía"), no es un
  defecto de esta entrega. En cuanto Arte/Dirección de Arte aprueben esos
  assets y el Publicador los suba a `assets/vintage-telnet/locations/`,
  agregar la fila correspondiente a `VISUAL_CONTEXT_ART` es el único cambio
  necesario — no requiere tocar `describe_room()` de nuevo.
- El Issue #125 también menciona el cierre visual de #106/PR #123 (mapa +
  heading); esta entrega es solo la parte de servidor que #125 pide
  explícitamente, no reabre ni modifica esa PR ya mergeada.

**LISTO PARA PUBLICAR:** NO — pendiente de revisión del Arquitecto de
Vintage Telnet y Raspberry Pi / Integrador según el flujo normal de
`AGENTS.md`. Cambio de bajo riesgo y acotado a un solo archivo de datos de
mundo más pruebas.

---

## ENTREGA — Fixes puntuales de `entry.html` reportados por Javier jugando en celular real

**Desarrollador:** Claude — Desarrollador de Servidor de Vintage Telnet

**Estado:** LISTO PARA REVISIÓN

**Rama:** `claude/vintage-telnet-server-entry-ui-fixes`

### Origen
Javier probó "El lindero roto" en su celular contra la Raspberry real (después de fusionar PR #79 + #85) y reportó: caja de comando ilegible/diminuta, botón Enviar desproporcionado, Atacar sin arte junto a un Huir muy vistoso, y texto de sala apareciendo todo de golpe. Antes de tocar nada confirmé que no había ninguna PR abierta modificando `entry.html` en paralelo (PR #79 ya se había fusionado y reconciliado).

### Bug real encontrado (no solo preferencia visual)
`.btn{width:100%}` dentro del `.commandbar` (flex row) le robaba casi todo el ancho al input de texto: medía **26px de ancho real** en el navegador (prácticamente inusable para escribir), mientras el botón Enviar ocupaba 318px. Verificado con `getBoundingClientRect()` contra el servidor real corriendo localmente, no solo leyendo CSS.

### Cambios (solo `entry.html` + 1 línea de `app.py`)
- `.commandbar .btn{width:auto;flex:0 0 auto;min-width:96px}` — el input ahora mide ~248px (usable), el botón Enviar ~96px (proporcionado a su contenido).
- Atacar ya no usa `.btn.primary` genérico: nueva clase `.btn.combat-attack` (tono de peligro, ícono ⚔ de texto) para no verse "sin arte" al lado de Huir. Mismo ancho que Huir ahora (196px vs 196px, antes muy distintos). La altura difiere ~19px porque `.btn-art` fija `aspect-ratio:3/1` para no deformar el arte de Huir — aceptable hasta que exista ícono real de Atacar (Issue #75).
- Texto de sala (`> mirar`) ahora se revela progresivamente (~2 caracteres/18ms) en vez de aparecer todo de golpe; respeta `prefers-reduced-motion`; un toque/clic en el log revela todo de inmediato (no bloquea si alguien quiere leer rápido).
- Tamaño de fuente del texto de sala subido ligeramente (16px→17px en móvil, clamp ajustado en escritorio) para legibilidad.
- `app.py`: agregado `connect-src 'self'` al CSP — sin esto, el panel **Mapa** que agregó PR #79 (usa `fetch("/api/map")`) queda bloqueado silenciosamente por `default-src 'none'` y nunca carga. Bug real, no relacionado con el reporte de Javier pero encontrado en la misma verificación.

### Pruebas
112/112 (`python -m unittest discover -s tests -v`), incluyendo una prueba nueva que verifica `connect-src 'self'` en el CSP. Verificado además a mano contra el servidor real corriendo (login, encuentro con Mordelinde, medidas reales de los botones vía `getBoundingClientRect()`).

### Pendiente para otros roles (no lo hago yo)
- Ícono real de Atacar y arte de Huir/Atacar equivalente — Issue #75 (Arte + Integrador).
- Javier reportó que las tarjetas de arte de las 5 especies ya existen ("subidas a la repo") pero no las encontré en `main` ni en las ramas abiertas de Arte — dejé pregunta en Issue #75 para que confirme ubicación (¿Drive vs. repo?) antes de que alguien las conecte a la pantalla de selección de especie.

**LISTO PARA PUBLICAR:** NO — pendiente de revisión como el resto de mis entregas. Cambio de bajo riesgo (solo `entry.html` + 1 línea de CSP), sin tocar lógica de combate/servidor ya revisada en PRs anteriores.

---

## ENTREGA — Vintage Telnet Issue #73: Esquivar/Bloquear/Resistir + `available_actions`

**DESARROLLADOR:** Claude — Desarrollador de Servidor de Vintage Telnet
**HEAD BASE:** `f594565e5d6a8a3e18526248799f83972785c120` (origin/main)
**TAREA ASIGNADA:** Issue #73 — implementar las intenciones de combate que
faltaban (`esquivar`, `bloquear`, `resistir`) conforme a `GAMEPLAY.md` 20.5/
24.2/24.3 y al contrato normativo que Jugabilidad cerró en el comentario del
Issue y en `vintage-telnet/UI_ACTIONS_CONTRACT.md` (rama
`gameplay/issue-77-ui-actions-contract`, aún no mergeada a `main` — la leí
directamente de esa rama porque es la fuente normativa citada en el Issue).
**RAMA:** `claude/vintage-telnet-server-issue-73`

### CAMBIOS
- `vintage-telnet/server/combat.py`: `FATIGUE_BASE_COST` ahora incluye
  `resistir` (3), `bloquear` (5) y `esquivar` (6), tal como cerró
  Jugabilidad en 24.3. Tres funciones puras nuevas, sin Flask/DB:
  `resolve_dodged_attack_roll` (reduce % de impacto según
  Agilidad/Percepción, nunca reduce daño), `resolve_resisted_attack_roll`
  (no cambia % de impacto, reduce daño según Resistencia, tope 38%) y
  `resolve_blocked_attack_roll` (no cambia % de impacto, reduce daño según
  Destreza, tope 32%) — las tres fórmulas literales de GAMEPLAY.md 20.5.
- `vintage-telnet/server/app.py`:
  - `_can_block()` (nivel de módulo, no closure, para poder parchearla en
    pruebas): **siempre devuelve `False`** porque Bloquear exige equipo
    (arma/escudo/objeto) y el Issue #57 (inventario/equipo) todavía no está
    integrado. Issue #73 pide explícitamente no inventar inventario aquí,
    así que en vez de simular equipo, `bloquear` nunca aparece en
    `available_actions` y la intención se rechaza con un mensaje honesto
    ("Todavía no tienes equipo adecuado para bloquear."). El resto de la
    resolución de Bloquear (daño/fatiga) ya está implementado y probado
    (parcheando `_can_block` a `True`), lista para conectarse a equipo real
    en cuanto #57 exista — no hay que tocar nada más.
  - `attempt_dodge`, `attempt_resist`, `attempt_block`: mismo patrón que
    `attempt_flee` ya existente (sustituyen el ataque básico del jugador de
    esa ronda por la intervención elegida; aplican coste de fatiga de 24.3,
    penalización de fatiga/herida del propio defensor sobre su esquiva
    —24.4/24.6, `combined_accuracy_penalty` ya documentaba que aplica a
    "esquiva"—, y el mismo flujo de derrota/reaparición que atacar/huir).
  - Nuevas intenciones `esquivar`/`bloquear`/`resistir` reconocidas por
    `parse_intent` y despachadas tanto en `/command` (HTML) como en
    `/api/intent` (JSON), igual que `huir`/`descansar`.
  - Rutas dedicadas `POST /dodge`, `POST /resist`, `POST /block` (mismo
    patrón que `/attack`, `/flee`, `/evaluate` ya existentes) para que un
    botón de interfaz llegue a la misma intención autoritativa que el
    comando escrito.
  - `room_view()` ahora expone `available_actions`: con criatura presente,
    `[atacar, evaluar, huir, esquivar, resistir]` (+ `bloquear` solo si
    `_can_block()` autoriza); sin criatura, `[descansar]`. Es la "forma
    mínima recomendada" de `UI_ACTIONS_CONTRACT.md`. **Alcance explícito de
    esta entrega:** solo acciones de combate/descanso, que es lo que pide
    el Issue #73 ("esto desbloquea los botones de combate correctos para
    #43"); movimiento, mirar, observar/examinar y hablar ya tienen su
    propia autorización por otras vías (salidas de sala, texto de
    examinar, NPC activo) y quedan fuera de `available_actions` por ahora
    — no es una omisión, es alcance del Issue.
- `vintage-telnet/server/README.md`: actualizado para reflejar que
  Esquivar/Bloquear/Resistir ya están implementados (ya no aparecen como
  "diferidos al Issue #43" — eso sigue aplicando solo a las rondas
  semi-automáticas de 24.1) y documentado el bloqueo de Bloquear por falta
  de equipo (#57).
- `vintage-telnet/server/combat.py` (docstring del módulo): actualizado en
  el mismo sentido.
- `vintage-telnet/tests/test_combat_actions.py` (nuevo): 24 pruebas nuevas
  — 9 puras sobre las fórmulas de `combat.py` (sin Flask/DB) y 15 de
  integración contra el servidor real (Flask + SQLite), cubriendo: no-op
  honesto sin criatura, esquivar evitando un golpe que conectaría con
  Agilidad alta, resistir reduciendo daño con Resistencia alta, coste de
  fatiga de las tres acciones, bloquear rechazado sin equipo y resuelto
  correctamente una vez autorizado (equipo simulado vía parche de
  `_can_block` para la prueba, no en el código de producción), paridad
  botón/comando para las tres acciones nuevas, y la forma de
  `available_actions` dentro/fuera de combate.

### PRUEBAS
- Suite completa: **110/110 pruebas pasan**
  (`.venv/bin/python -m unittest discover -s tests -v`), incluidas las 86
  heredadas sin cambios de comportamiento y las 24 nuevas de este archivo.
- No se modificó ningún test existente.

### TRABAJO PREVIO AFECTADO
Solo se tocó `vintage-telnet/server/combat.py`, `app.py` y `README.md`
(server), más el nuevo archivo de pruebas. No se tocó
`vintage-telnet/server/store.py`, `world.py`, `creatures.py`,
`vintage-telnet.html` ni ningún archivo de Senku. `atacar`/`huir`/
`evaluar`/`descansar` se conservan exactamente como estaban (ninguna de sus
funciones ni rutas fue modificada), conforme pedía el Issue.

### PENDIENTES
- **NECESIDAD DEL SERVIDOR (autogenerada, no bloqueante):** en cuanto el
  Issue #57 (inventario/equipo) esté integrado, cambiar `_can_block()` en
  `server/app.py` para que consulte equipo real en vez de devolver `False`
  siempre. Es el único cambio necesario; la resolución de golpe/daño/fatiga
  de Bloquear ya existe y está probada.
- Integración de botones reales en la interfaz (`/dodge`, `/resist`,
  `/block`, y renderizar `available_actions`) corresponde al Desarrollador
  Junior en el Issue #72/#43, no a esta entrega — el Issue #73 así lo
  delimita explícitamente ("esto desbloquea los botones de combate
  correctos para #43"). No toqué `entry.html`.
- Rondas semi-automáticas con ataque básico continuo (GAMEPLAY.md 24.1)
  siguen diferidas al Issue #43 por decisión del Arquitecto; esta entrega
  no las implementa, sigue siendo un intercambio simple por comando/botón.

### AVISO PARA EL ARQUITECTO DE VINTAGE TELNET Y RASPBERRY PI
Esta entrega implementa exactamente lo que pidió el Issue #73 y el
contrato normativo de Jugabilidad, dentro del modelo de combate síncrono
por request que ya existía (sin rondas automáticas). Si algo de esto no
encaja con una decisión arquitectónica que yo no haya visto, avisame y lo
ajusto.

### AVISO PARA EL INTEGRADOR/PUBLICADOR
No publicar hasta autorización expresa de Javier. Comparar esta rama
contra el HEAD vigente de `main` antes de integrar — solo toca
`vintage-telnet/server/{app.py,combat.py,README.md}` y agrega
`vintage-telnet/tests/test_combat_actions.py`, así que no debería haber
conflicto con otras entregas de Vintage Telnet en curso (UI, arte, NPCs),
pero conviene confirmarlo contra el `main` real al momento de integrar.

**LISTO PARA REVISIÓN:** SÍ
**LISTO PARA PUBLICAR:** NO — falta revisión del Arquitecto de Vintage
Telnet/Jugabilidad y autorización de Javier ("sube").

---

## ENTREGA — Senku: portada narrativa antes del juego

**DESARROLLADOR:** Desarrollador Junior de Senku — segundo desarrollador  
**HEAD BASE:** `a38a2125ff1a250a030934edb77548f07663bd5a`  
**TAREA ASIGNADA:** crear una portada propia de Senku con una explicación breve de la aventura y mover el juego un nivel abajo para que MatiasGameLab no entre directamente a DESPERTAR.  
**RAMA:** `junior/senku-portada-intro`

### CAMBIOS
- Nueva portada: `senku/index.html`.
- Juego movido a: `senku/juego.html`.
- `index.html` del portal ahora entra a `senku/`.
- El antiguo `senku.html` redirige a la nueva portada para conservar enlaces guardados.
- `senku.webmanifest` abre la portada de Senku al iniciar como app.
- El botón de casa dentro del juego vuelve a la portada de Senku.
- Se ajustaron rutas de assets del juego a `../assets/`.

### PRUEBAS
- JavaScript de `senku/juego.html`: parseo OK.
- DESPERTAR: handler presente; entra a Casa con almacenamiento normal.
- DESPERTAR: handler presente; entra a Casa con `localStorage` bloqueado.
- Rutas verificadas: portal → portada Senku → juego; portada → MatiasGameLab; juego → portada.
- No quedan referencias de assets con ruta raíz incorrecta dentro del juego movido.

### TRABAJO PREVIO AFECTADO
Se conserva íntegra la lógica de Senku v0.5.9. La tarea reorganiza únicamente su entrada/navegación y rutas relativas.

### PENDIENTES
Prueba visual final en teléfono/iPad/escritorio después de publicar.

### AVISO PARA EL OTRO DESARROLLADOR
La entrada canónica de Senku pasa a ser `senku/`; la experiencia jugable vive en `senku/juego.html`. No volver a enlazar el portal directamente al HTML jugable salvo instrucción explícita.

**LISTO PARA REVISIÓN:** SÍ

---

## ENTREGA — Senku Issue #81: DESPERTAR resistente a almacenamiento bloqueado

**DESARROLLADOR:** Desarrollador Junior de Senku — segundo desarrollador

**HEAD BASE:** `8faeab8618113806489b77c6769bb853d50d28c1`

**TAREA ASIGNADA:** Issue #81 — corregir la versión pública de Senku cuando la portada carga pero el botón **DESPERTAR** no inicia el juego.

**RAMA:** `junior/senku-fix-despertar-81`

### PROBLEMA ENCONTRADO
`senku.html` ejecutaba `localStorage.getItem('senku_skin')` durante la inicialización global y antes de registrar `#start.onclick`. En navegadores donde el almacenamiento está bloqueado y ese acceso lanza `SecurityError`, el script se aborta: la portada permanece visible, pero DESPERTAR queda sin handler.

### CORRECCIÓN REALIZADA
- Se añadieron `storageGet()` y `storageSet()` con `try/catch`.
- Si el almacenamiento falla, Senku continúa sin persistencia durante esa sesión en vez de abortar el juego.
- `save()` usa el wrapper seguro, de modo que una falla posterior al guardar tampoco detiene el juego.
- Se actualizó la identificación visible a **v0.5.9 · arranque resistente**.
- No se modificó `index.html`.

### PRUEBAS
Prueba automatizada del JavaScript exacto de la rama con DOM mínimo simulado y `requestAnimationFrame` controlado:
- Parseo JavaScript: **OK**.
- Almacenamiento normal: `#start.onclick` registrado, pulsar DESPERTAR oculta portada y deja zona **Casa**.
- `localStorage` bloqueado lanzando `SecurityError`: inicialización completa sin excepción no controlada, `#start.onclick` registrado, pulsar DESPERTAR oculta portada y deja zona **Casa**.
- En el escenario bloqueado se registra una advertencia controlada y la ejecución continúa.

La URL pública no pudo abrirse desde el navegador de verificación disponible en esta sesión, por lo que la comprobación final física en teléfono/iPad queda para después de integración/publicación.

### TRABAJO PREVIO AFECTADO
Solo la inicialización/persistencia de `senku.html`. No se cambiaron escenas, controles, arte, portal ni Vintage Telnet.

### PENDIENTES
- Integrador: comparar la rama contra el `main` vigente, integrar únicamente con autorización de Javier y verificar GitHub Pages.
- Javier/Matías: prueba física final **Portal → Senku → DESPERTAR → Casa → controles** en el dispositivo donde se reprodujo el fallo.

### AVISO PARA EL OTRO DESARROLLADOR
El acceso directo a Web Storage debe mantenerse detrás de los wrappers seguros; no reintroducir lecturas/escrituras directas de `localStorage` durante bootstrap.

**LISTO PARA REVISIÓN:** SÍ  
**LISTO PARA PUBLICAR:** NO — requiere flujo de integración vigente.

---

## ENTREGA — Binding narrativo explícito de Issue #46 en PR #49 (tercera vuelta del Arquitecto)

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN (tercera vuelta)

**Rama:** `claude/vintage-telnet-server-lindero-roto` (misma rama del PR #49, HEAD base sin cambios: `b8734f5ef0f518af9ad85696518ed69d719dc495`)

### Objetivo
El Arquitecto de Vintage Telnet y Raspberry Pi pidió una tercera vuelta en PR #49 (comentario 2026-09-23T10:55:48Z) una vez que Issue #46 quedó resuelto (Narrador: `valdren_centro`, confirmado compatible con canon por el Historiador, conforme de Jugabilidad): sustituir el marcador provisional por el binding canónico explícito, añadir una prueba que lo demuestre, no ampliar el alcance hacia #43/24.7, y reejecutar la suite completa.

### Qué se cambió
- `server/app.py`: `PENDING_SAFE_ROOM_ID` → `SAFE_ROOM_ID = "valdren_centro"`, con el comentario actualizado citando la resolución de Issue #46 en vez de describirlo como pendiente. `attempt_rest` ahora distingue: dentro de `SAFE_ROOM_ID` aplica `combat.safe_recovery_result` (GAMEPLAY.md 24.9, cura 100% HP, fatiga a 0, mejora la herida un grado) en vez del descanso de campo v1; fuera de esa sala sigue usando `combat.rest_result` sin cambios. Los mensajes de respawn y de recuperación segura usan el texto que el Narrador propuso textualmente en Issue #46 (`RESPAWN_MESSAGE`/`SAFE_RECOVERY_MESSAGE`) en vez de la frase genérica anterior — no es redacción inventada por Desarrollo.
- `server/README.md`: la nota de "NECESIDAD NARRATIVA pendiente (Issue #46)" se reemplazó por la descripción del binding ya resuelto.
- `tests/test_pilot_lindero_roto.py`: `test_resting_outside_combat_heals_and_reduces_fatigue` ahora se mueve fuera de `valdren_centro` antes de descansar (para seguir probando el descanso de campo v1, que dejó de aplicar en la sala segura); nueva `test_resting_in_valdren_centro_uses_full_safe_recovery` demuestra que `descansar` en `valdren_centro` resuelve a recuperación segura completa (HP 100%, fatiga 0, herida mejorada un grado). `test_defeat_respawns_in_valdren_with_60_percent_hp` (ya existente) sigue demostrando que la muerte resuelve a `valdren_centro`.
- No toqué `entry.html`, Issue #43/P1, ni la recuperación pasiva de fatiga (24.7): siguen fuera de esta entrega, tal como pidió el Arquitecto.

### Pruebas
`.venv/bin/python -m unittest discover -s tests -v` → **77/77 OK** (76 previas + 1 nueva).

### Pendiente (sin cambios respecto a la vuelta anterior, no bloqueante)
- Recuperación pasiva de fatiga fuera de combate (24.7, ~1 fatiga/10s): sigue sin implementar, documentado en `server/README.md`.

**LISTO PARA PUBLICAR: NO** — pendiente de que el Arquitecto confirme esta tercera vuelta antes de tocar `main`.

---

## ENTREGA — Respuesta a revisión arquitectónica de PR #49 (fatiga/heridas/recuperación §24, cooldown de monstruos)

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN (segunda vuelta)

**Rama:** `claude/vintage-telnet-server-lindero-roto` (misma rama del PR #49, HEAD base sin cambios: `b8734f5ef0f518af9ad85696518ed69d719dc495`)

### Objetivo
El Arquitecto de Vintage Telnet y Raspberry Pi revisó PR #49 y pidió cuatro cambios antes de integrar (comentario en el PR, 2026-09-23). Esta entrega responde a los cuatro:

1. **Respawn/recuperación segura no debe fijarse por implementación** (Issue #46 sigue abierto). No inventé el punto narrativo: extraje el literal `"valdren_centro"` a `app.PENDING_SAFE_ROOM_ID`, documentado como marcador técnico operativo pendiente de Issue #46 — sustituir esa única constante cuando el Narrador entregue el ID real. La recuperación segura completa de GAMEPLAY.md 24.9 (`combat.safe_recovery_result`, probada) está implementada pero **no atada a ninguna sala todavía**, para no decidir por Narrativa.
2. **Sincronizar con GAMEPLAY.md vigente** (commit `6c764442206d7aeb31ac9daf6e7a084c27ee80c6`, sección 24, ya en el HEAD base de PR #49): implementé costes de fatiga por acción (24.3), penalizaciones de fatiga cansado/agotado (24.4), disparador de heridas por golpe recibido (24.5), efectos de herida sobre precisión/daño/tope de descanso (24.6), acción `descansar` (24.8) y la función pura de recuperación segura (24.9, ver punto 1). Actualicé `server/combat.py`, `server/app.py`, `server/README.md` y las pruebas para dejar de declarar estas reglas como "pendiente de Jugabilidad" — ya no lo están.
3. **Respawn de monstruos con cooldown** (20.14): agregué tabla `creature_cooldowns` (esquema v4) y `store.creature_available`/`start_creature_cooldown`; al derrotar una criatura queda un cooldown de referencia ~5 minutos antes de que esa sala vuelva a generarle una nueva a ese jugador, en vez de reaparición llena instantánea.
4. **No ampliar P1 de UI en este PR**: no toqué `entry.html` ni agregué botones nuevos. `descansar` solo se agregó como intención de texto (`parse_intent`/`/command`/`/api/intent`), igual que otros comandos existentes; rondas semi-automáticas y defensa contextual (24.1-24.2) siguen explícitamente diferidas al Issue #43, ahora documentado así en `server/README.md` en vez de listarlas como huecos de Jugabilidad.

### Qué se agregó/cambió
- `server/combat.py`: `FATIGUE_BASE_COST`, `fatigue_state`, `fatigue_modifier`, `fatigue_gained`, `combined_accuracy_penalty`, `combined_damage_multiplier`, `wound_from_hit`, `worse_wound`, `rest_result`, `safe_recovery_result`; `resolve_attack_roll` acepta `accuracy_penalty`/`damage_multiplier` opcionales.
- `server/store.py`: esquema v4 (tabla `creature_cooldowns`), `update_combat_state` acepta `fatigue`, `creature_available`/`start_creature_cooldown`.
- `server/app.py`: `PENDING_SAFE_ROOM_ID`; `attempt_attack`/`attempt_flee` aplican coste de fatiga y disparan heridas reales; `attempt_move` respeta el cooldown de criaturas; nueva `attempt_rest` + intención `descansar` en `/command` y `/api/intent`.
- `server/README.md`: reescrito el bloque de la microaventura piloto para reflejar 20-24 cerrado, con las tres notas explícitas (NECESIDAD NARRATIVA #46, diferido a #43, pendiente técnico no bloqueante de recuperación pasiva 24.7).
- `tests/test_entry.py`: dos pruebas ajustadas al nuevo `schema_version=4` (la prueba de esquema no soportado ahora usa `5` en vez de `4`, que ya es válido).
- `tests/test_pilot_lindero_roto.py`: 13 pruebas nuevas (fórmulas puras de fatiga/heridas/descanso/recuperación segura, coste de fatiga real por HTTP, herida por golpe recibido, `descansar` dentro y fuera de combate, cooldown de criatura tras derrota y su expiración).

### Pruebas
`.venv/bin/python -m unittest discover -s tests -v` → **76/76 OK** (63 previas + 13 nuevas; 2 ajustadas por el cambio de versión de esquema, sin cambiar lo que verifican).

### Pendiente (no bloqueante, documentado explícitamente en `server/README.md` para no darlo por cerrado en silencio)
- Recuperación pasiva de fatiga fuera de combate (24.7, ~1 fatiga/10s): no implementada. El criterio de aceptación del Issue #45 no depende de ella.
- Recuperación segura (24.9) sigue sin sala asignada — depende de Issue #46.

**LISTO PARA PUBLICAR: NO** — pendiente de una nueva revisión del Arquitecto sobre estos cuatro puntos antes de tocar `main`.

---

## ENTREGA — Microaventura piloto jugable "El lindero roto" (Issue #45)

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN

**Rama:** `claude/vintage-telnet-server-lindero-roto`

### Objetivo
Issue #45 pedía a "Arquitecto + Desarrollo de servidor/contenido + Integrador HTML" convertir VT-NAR-003 (`NARRATIVE.md`) en el primer tramo narrativo jugable real, con los bindings mecánicos que Jugabilidad ya aprobó en `GAMEPLAY.md` §20-23. Implementé la parte de servidor completa: nada de esto inventa mecánica nueva, cada fórmula/decisión cita la sección de `GAMEPLAY.md`, `NARRATIVE.md` o `CREATURES.md` de la que sale.

### Qué se agregó
- **`server/combat.py`** (nuevo, puro, sin Flask/DB): atributos, CG, HP máximo, precisión/daño, categorías de encuentro (Trivial…Abrumador), XP de combate con tope del 25%/antifarmeo/bono de primera familia, XP de descubrimiento, curva de nivel, huida, reaparición. Cada función documenta la sección exacta de GAMEPLAY.md.
- **`server/creatures.py`** (nuevo): estadísticas de combate de Mordelinde y Espinajo de rastrojo, calibradas para caer en la banda Favorable/Comparable y Comparable/Peligroso que pidió el Issue #45 contra un personaje nivel 1 recién creado — marcadas explícitamente como calibración inicial afinable (GAMEPLAY.md 20.15), no balance definitivo. Cornalomo no tiene stats a propósito (NARRATIVE.md pide pedir su tabla a Jugabilidad antes de combate real; no aparece como encuentro en este piloto).
- **`server/world.py`**: nuevo camino `valdren_sendero → valdren_camino_parcela → valdren_camino_cerca → valdren_camino_lindero`, con los textos de `NARRATIVE.md` citados literalmente, objetivos de `examinar`, encuentros de Mordelinde/Espinajo y las tres definiciones de descubrimiento. Ningún otro pueblo cambia.
- **`server/store.py`**: esquema v3 (migración desde v2, fail-closed sobre versiones desconocidas): atributos/nivel/XP/HP/fatiga/herida/PA por jugador, y tablas de descubrimientos, salas visitadas, rutas recorridas, victorias PvE (para antifarmeo/primera familia) y encuentros activos por sala.
- **`server/app.py`**: nuevos intents `evaluar`/`atacar`/`huir` (botón y comando escrito ejecutan la misma función autoritativa, como el resto del servidor); `examinar`/`observar` ahora devuelve texto real y otorga descubrimientos una sola vez; movimiento actualiza mapa progresivo y coloca encuentros; `GET /api/character`, `GET /api/map`.
- **`server/templates/entry.html`**: corregido el bug P0 que señaló el Issue #43 (el modal de Ayuda decía que cualquier texto era chat; ahora explica el parser real). Panel Personaje con nivel/XP/HP/fatiga/herida/atributos reales. Botones Atacar/Huir/Evaluar habilitados solo cuando hay una criatura visible en la sala.

### Pruebas (63 en total, 32 nuevas en `tests/test_pilot_lindero_roto.py`)
Fórmulas puras contra la tabla de referencia de GAMEPLAY.md 22.1, calibración de las dos criaturas, conectividad/contenido del camino nuevo, y flujo HTTP completo: descubrimiento único por examinar, hito de regreso, `evaluar` sin revelar números, victoria con XP/bono de primera familia (verificado con RNG determinista via `unittest.mock.patch`), muerte/reaparición al 60% HP, huida exitosa, mapa persistente tras reiniciar el proceso. Verificado además a mano contra el servidor real corriendo en un navegador (registro → aprobación DM → especie → caminar → Mordelinde aparece → evaluar → examinar (+5 XP) → combate real con golpes/fallos → victoria (+12 XP, bono de familia) → estado confirmado en `/api/character`).

### Hallazgo durante el trabajo: PR #28 quedó redundante
Al preparar esta entrega encontré que mi PR #28 (fix del log de esquema + `backup.sh`, abierto antes de esta tarea) quedó completamente redundante: `main` ya tiene el mismo fix y una versión de `backup.sh` más madura, corregida dos veces para bugs reales que mi rama no tenía resueltos (`ff587d0`, `f21a01c`), aparentemente por el cierre del Issue #32 por otra vía. Cerré el PR #28 con una nota explicando por qué, para no reintroducir código más viejo.

### Pendiente (documentado como NECESIDAD DE JUGABILIDAD, no soy quien decide)
- Tabla de coste de fatiga por acción (20.7 la deja abierta a propósito).
- Disparador de heridas durante combate v1 (20.8 define los grados pero no cuándo se asignan).
- Defensa contextual (Esquivar/Bloquear/Resistir) y el resto del panel P1 que pide el Issue #43 — ese trabajo de interfaz corresponde a Arquitectura/Integrador, no a mí.
- Respawn de criaturas con temporizador (20.14): por ahora la criatura reaparece llena en la próxima visita a la sala, sin cooldown.

**LISTO PARA PUBLICAR:** NO — pendiente de revisión del Arquitecto/Jugabilidad antes de tocar `main`.

---

## ENTREGA — Ajustes tras la instalación real en Raspberry Pi

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN

**Rama:** `claude/vintage-telnet-server-v2`

### Contexto
El operador de Raspberry Pi instaló esta rama como servicio `systemd` real (reemplazando el despliegue viejo de `codex/vintage-telnet-server`/PR #1, sin borrar sus datos), corrió las 28 pruebas ahí mismo (28/28 OK, Raspberry Pi 5, Debian 13, Python 3.13.5), probó el flujo completo desde un navegador real, y confirmó que el servicio sobrevive un reinicio físico de la Raspberry con los datos intactos. Reporte completo en `vintage-telnet/ops/RASPBERRY_REPORT.md`.

Dejó dos pendientes concretos en ese reporte; los resuelvo acá.

### 1. Mensaje de log desactualizado
`server/__main__.py` tenía hardcodeado `"esquema 1"` en el log de arranque, aunque el esquema real ya es la versión 2. No era un fallo funcional, solo una observación del operador. Corregido para que lea `PRAGMA user_version` real de la base al arrancar — no se puede volver a desactualizar sola en el próximo cambio de esquema.

### 2. Sin política de respaldo
El operador señaló explícitamente que no había decisión de backup antes de la primera instalación real con datos. Agregué:
- `vintage-telnet/ops/backup.sh`: llama a `server.admin backup` (que ya verifica integridad de la copia) y poda backups de más de 14 días.
- `vintage-telnet/ops/vintage-telnet-backup.service` + `.timer`: unidad `systemd` endurecida (mismo estilo que el servicio principal) que corre el respaldo una vez al día.
- Documentado en `server/README.md` cómo activarlo (`systemctl enable --now vintage-telnet-backup.timer`).

No reemplaza una copia fuera del equipo (disco externo/otra máquina) — eso sigue siendo una decisión operativa aparte, señalada como tal en el README.

### Pruebas
28/28 siguen pasando sin cambios (el fix de `__main__.py` no tiene lógica nueva que probar aparte de lo que ya cubre `test_http.py`; verifiqué manualmente que el log ahora dice "esquema 2").

### Riesgo
Los archivos nuevos de `ops/` no se instalan solos — el operador de Raspberry debe habilitar el timer manualmente la próxima vez que sincronice esta rama. No pasa nada si no lo hace todavía; el servicio principal sigue funcionando igual.

**LISTO PARA PUBLICAR:** NO — como el resto de esta rama, sigue esperando revisión del Arquitecto antes de tocar `main`.

---

## ENTREGA — Segunda respuesta a la revisión del Arquitecto (PR #6, rondas 3 y 4)

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN

**Rama:** `claude/vintage-telnet-server-v2`

### Objetivo
El Arquitecto dejó dos revisiones más en el PR #6 después de la respuesta anterior (rondas 3 y 4), validando lo ya corregido y encontrando 6 puntos nuevos: 2 operativos y 4 de seguridad/contrato API.

### 1-2. Puntos operativos (ronda 3)
- `vintage-telnet/ops/server.env.example` no incluía `VT_DM_PASSWORD` → sin ella, cualquiera que copie ese archivo tal cual deja `/dm` deshabilitado y no puede completar el recorrido P0. Agregado como placeholder no secreto, con comentario explicando por qué es obligatoria.
- `vintage-telnet/server/README.md` estaba desfasado (decía 19 pruebas, describía todo como formularios HTML clásicos). Reescrito: 28 pruebas, `/command`, `POST /api/species`, `POST /api/move`, contrato de errores JSON, CSP con nonce, microzonas por pueblo, privacidad del chat, y una nota sobre `PR #8`/`CONTENT_RUNTIME_ARCHITECTURE.md` (la geografía se migrará a contenido versionado más adelante, no en este servidor).

### 3-6. Puntos de seguridad/contrato (ronda 4)
- **`POST /api/species` incompleto:** ahora responde también `town` (nombre del pueblo, tomado del `name` de la sala central) y `player` (estado completo actualizado, releído de la base después de escribir), no solo `accepted`/`species`/`room`.
- **Errores HTML en rutas API:** `/api/room`, `/api/species` y `/api/move` ya no usan `require_approved_player()` (que hace `abort()`, HTML). Nuevo helper `api_player_state()` devuelve `{"error": "unauthenticated"}` (401), `{"error": "not_approved", "status": ...}` (403) o `{"error": "species_required"}` (409) en JSON. Las rutas de formulario (`/move`, `/species`, `/command`, `/room/say`) siguen devolviendo HTML sin cambios.
- **Username filtrándose en el chat:** `store.recent_messages()` seleccionaba `p.username` además de `p.name` y `/api/room` lo exponía en cada mensaje. Quitado por completo de la consulta — el chat solo expone `name` (identidad pública), nunca la credencial de login de otro jugador.
- **Elección de especie no era atómica de verdad:** `set_species()` hacía el `UPDATE ... WHERE species IS NULL` pero no comprobaba si realmente escribió; dos POST casi simultáneos podían terminar ambos con `accepted=True` con datos distintos (uno de los dos se pisaba silenciosamente). Corregido usando `cursor.rowcount`: la función ahora devuelve si *esta* llamada fue la que efectivamente escribió, y `attempt_choose_species()` usa ese resultado en vez de una lectura previa de `player["species"]`.

### Pruebas agregadas (3 nuevas, 28 en total)
- Contrato de errores JSON para `/api/room` y `/api/move`: no autenticado, pendiente de aprobación, y aprobado-sin-especie, verificando el `error` exacto en cada caso.
- El chat nunca expone el `username` de otro jugador (registra una cuenta con username distinto a su nombre público y confirma que el username no aparece en ningún lado de `/api/room`).
- Elección de especie concurrente con `ThreadPoolExecutor` (4 hilos, 4 especies distintas) contra `store.set_species` directamente: exactamente una escritura tiene efecto, y el estado final en la base es consistente (especie y sala coinciden).

### Rebase
`main` avanzó de nuevo (contenido narrativo, atributos, nuevo especialista de Psicopedagogía infantil). Mergeado sin problema: único conflicto real fue `AGENTS.md` (dos secciones nuevas en paralelo), resuelto conservando ambas. Nada de esto toca `vintage-telnet/server/`.

### Riesgos/nota para el Arquitecto
La extracción de `world.py` hacia `vintage-telnet/content/` (PR #8) sigue sin hacerse aquí — el Arquitecto ya la dejó explícitamente como entrega separada posterior, no bloqueante para este PR.

**LISTO PARA PUBLICAR:** NO — vuelve a quedar para revisión.

---

## ENTREGA — Respuesta a la revisión del Arquitecto (PR #6)

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN

**Rama:** `claude/vintage-telnet-server-v2`

### Objetivo
Responder punto por punto a la revisión del Arquitecto en el PR #6 (`REVISIÓN DEL ARQUITECTO — NO LISTA PARA INTEGRAR TODAVÍA`).

### 1. Rebase/actualización contra `main`
Mergeado `origin/main` (traía la integración de arte, `DATABASE_GAMEPLAY_PREP.md` y `FIRST_PLAYABLE_SLICE.md`, el documento de prioridad P0 de Javier). Conflicto real solo en `AGENTS.md` (dos secciones nuevas en paralelo), resuelto conservando ambas. `HANDOFF.md` mergeó solo. 25/25 pruebas pasan después del merge.

### 2. CSP para assets — bug real confirmado y corregido
Verifiqué en consola del navegador **antes** de tocar nada: la política `default-src 'none'` sin `img-src` bloqueaba de verdad las 4 imágenes de fondo/botones (`net::ERR_BLOCKED_BY_RESPONSE` / CSP violation) — se veían en mis pruebas anteriores porque las había probado sobre `vintage-telnet.html` (PR #7, sin CSP) o sin fijarme en la consola de esta página en particular. También descubrí que el `<script>` inline de los diálogos (Personaje/Inventario/Poderes/Ayuda) estaba bloqueado por la misma razón — nunca abrían en el servidor real.
- Agregué `img-src 'self'`.
- Para el script, en vez de `'unsafe-inline'` (que debilita CSP para todo el sitio), implementé un **nonce por request** (`g.csp_nonce`, inyectado en la plantilla vía `context_processor`) y `script-src 'nonce-...'`.
- Verificado en consola: cero violaciones CSP después del cambio; los 4 diálogos abren correctamente.

### 3. Microzona interna por pueblo (P0)
`world.py` reescrito: cada uno de los 5 pueblos de inicio ahora es una microzona de 3-4 salas (`_centro`, `_forja`, `_mercado`, y `_sendero` cuando queda una cuarta dirección libre), no una sala única. El punto central conserva exactamente las mismas conexiones externas que ya existían hacia Vaisgard/caminos. Narevia (que ya usaba 2 direcciones para caminos externos) solo tiene forja+mercado, sin sendero adicional — sus 4 direcciones ya prueban N/S/E/O igualmente. Verificado con un BFS que las 22 salas resultantes son alcanzables desde Vaisgard y no hay salidas colgantes. Todo sigue marcado `[PLACEHOLDER]` explícitamente: no se presenta como canon.

### 4. Botón y comando = misma acción
Extraje la lógica de movimiento a una función única `attempt_move()`, usada por el botón (`/move`), el contrato JSON (`/api/move`) y el nuevo cuadro de texto. El cuadro de texto ahora postea a `/command`: si el texto es norte/sur/este/oeste (o n/s/e/o), ejecuta exactamente la misma acción autoritativa que el botón correspondiente; si es "mirar", refresca; cualquier otro texto sigue funcionando como chat local (fuera de alcance P0 según `FIRST_PLAYABLE_SLICE.md`, pero se conserva porque ya funcionaba y no cuesta nada mantenerlo).

### 5. Contrato estructurado de movimiento/especie
Agregué `POST /api/species` y `POST /api/move` (JSON in/out), compartiendo la misma lógica autoritativa que las rutas HTML (`attempt_choose_species`, `attempt_move`). `/api/move` responde `{accepted, previous_room, current_room: {id, name, description, exits, ...}, reason}` tal como pide `FIRST_PLAYABLE_SLICE.md`. Las rutas HTML (`/move`, `/species`) se conservan como fallback funcional para la plantilla actual, tal como el Arquitecto autorizó explícitamente. Para que un cliente JSON pueda enviar el CSRF sin parsear HTML, `GET /api/me` ahora también devuelve el token `csrf` vigente.

### 6. Pruebas agregadas (6 nuevas, 25 en total)
- CSP: `img-src 'self'` y `script-src 'nonce-...'` presentes en la respuesta, y el nonce del header coincide con el del `<script>` renderizado.
- Segunda especie (`marevyn`) confirmando que cada una llega a su propio pueblo (`narevia_centro`).
- Persistencia de especie **y sala** (no solo sesión) tras recrear la app con un dispositivo nuevo.
- Comando escrito ("norte", alias "s", "mirar", y texto libre) produciendo exactamente el mismo resultado que los botones/chat.
- Contrato estructurado `/api/species` + `/api/move` (aceptado y rechazado).
- Rate limit propio de `/dm/login` (clave separada de `/register`/`/login`, no comparten cupo).

### Bug real encontrado y corregido durante esta entrega
Al extraer `attempt_choose_species()`, el caso "ya tenías especie elegida" pasó de ser un redirect silencioso a tratarse como error renderizando la plantilla sin pasarle `room` — como en ese punto el jugador ya tenía especie, la plantilla intentaba la vista de mundo y fallaba con `UndefinedError`. Corregido separando "ya elegida" (no-op, redirect) de "especie inválida" (error real, sin necesitar `room` porque el jugador sigue sin especie en ese caso). Detectado por la propia suite de pruebas, no en manual.

### Riesgo/nota para el Arquitecto
El mínimo de contraseña de 8 caracteres sigue igual (decisión explícita de Javier, ya registrada en la entrega anterior) — no es parte de esta respuesta a la revisión.

**LISTO PARA PUBLICAR:** NO — vuelve a quedar para revisión del Arquitecto según pidió ("cuando la rama se actualice con estos puntos, volver a revisión").

---

## ENTREGA — Login real + arte integrado en el servidor (mismo origen)

**Desarrollador:** Claude (Desarrollador de Servidor de Vintage Telnet)

**Estado:** LISTO PARA REVISIÓN

**Rama:** `claude/vintage-telnet-server-v2` (mismo commit base que la entrega anterior de esta rama)

### Objetivo
Javier pidió una pantalla de login real antes de entrar al mundo — no la demo local de `vintage-telnet.html` (PR #7), sino el servidor real (PR #6) con la misma identidad visual. Esto reemplaza `server/templates/entry.html` por una versión que reutiliza el arte de `vintage-telnet/assets/html-ui/` (mismo origen, sin CORS) y conecta login/registro/mundo/movimiento/chat a las rutas reales que ya existían.

### Archivos nuevos
- `vintage-telnet/assets/html-ui/` — traída desde `origin/main` (ya estaba fusionada ahí vía el PR de Arte HTML); esta rama no la tenía porque nació de un commit de `main` anterior a esa fusión.

### Archivos modificados
- `vintage-telnet/server/app.py`:
  - Nueva ruta `GET /assets/html-ui/<path:filename>` (vía `send_from_directory`, con `before_request` saltando la verificación de sesión/CSRF para esa ruta) — el servidor no tenía carpeta estática habilitada (`static_folder=None` deliberado, ver pruebas de seguridad existentes), así que agregué exactamente esta carpeta, no una carpeta estática general.
  - **Cambio de política de contraseña, a pedido explícito de Javier**: el mínimo bajó de 12 a **8 caracteres**. Se lo señalé como una reducción real de seguridad antes de hacerlo; Javier lo confirmó explícitamente sabiendo el trade-off.
- `vintage-telnet/server/templates/entry.html` — reescrito completo:
  - Login/registro real con el arte nuevo (pizarra azul + bronce + marfil), mismas rutas/campos de siempre (`/login`, `/register`, csrf).
  - Vista de mundo real: sala/descripción/salidas vienen de `GET` a `/` con los datos reales del jugador (ya no hay `rooms` simulado en JavaScript). Los botones N/S/E/O son formularios reales a `/move`; se deshabilitan cuando esa dirección no es una salida real de la sala actual.
  - Chat real: formulario a `/room/say`, mensajes mostrados vienen de `room.messages`.
  - Atacar/Huir quedan visiblemente deshabilitados con `title="Combate todavía no implementado"` — no se simula combate que no existe.
  - Personaje/Inventario/Poderes/Ayuda siguen como diálogos informativos honestos (igual que en la demo), sin JavaScript de simulación de mundo.

### Cuenta real creada
Registré la cuenta `vaisork` a través del formulario real del navegador (no por comando, para no dejar la contraseña en ningún archivo ni historial de shell) y la aprobé desde `/dm`. Contraseña con hash `scrypt` vía `werkzeug`, nunca almacenada ni mostrada en texto plano en ningún archivo de este repositorio.

### Pruebas realizadas
- Suite completa: **19/19 pruebas siguen pasando** sin modificarlas (el cambio de mínimo de contraseña no rompe ninguna, ya usaban contraseñas de prueba más largas).
- Prueba real de punta a punta en el navegador, con la cuenta `vaisork` real: registro → visible en `/dm` → aprobar → elegir especie (Dravak) → aparece en Brumak con solo la salida norte habilitada → mover al norte → llega a Vaisgard con las 4 salidas habilitadas → confirmado en `/dm` que quedó `especie=dravak`, `sala=vaisgard`.
- Verifiqué (renderizando la plantilla directo con Jinja2, con datos de Brumak) que los botones de dirección sin salida real quedan con el atributo `disabled` — al principio pensé que había un bug porque los 4 botones aparecían habilitados, pero era porque el jugador ya se había movido a Vaisgard (que sí tiene las 4 salidas) mientras yo revisaba otra pestaña.

### Qué sigue sin existir (a propósito)
Combate, inventario, personaje, poderes reales — solo quedan como paneles honestos que dicen que no existen todavía. Mapa lateral con nodos visuales (el de la demo) no se replicó; el panel lateral ahora muestra datos reales (jugador, especie, sala) en vez del mapa ficticio.

### Riesgos/conflictos
Ninguno nuevo: esta entrega solo toca archivos ya propios de esta rama (`app.py`, `entry.html`) más la carpeta de arte que ya es idéntica a la de `main`, así que al fusionar no debería haber conflicto contra la integración de arte ya publicada.

### Aviso
El mínimo de contraseña de 8 caracteres es más bajo que el estándar recomendado (12+). Fue una decisión explícita de Javier después de que se lo señalé; si más adelante se agrega más gente al servidor, vale la pena reconsiderarlo.

**LISTO PARA PUBLICAR:** NO — sigue pendiente la revisión del Arquitecto de Vintage Telnet y autorización de Javier para `main`. El servidor de prueba con la cuenta real de Javier quedó corriendo localmente para que pueda seguir jugando; no es la Raspberry Pi ni un despliegue público.

---

## ENTREGA — Claude, Desarrollador de Servidor de Vintage Telnet

**Estado:** ENTREGA PREPARADA EN RAMA, PENDIENTE DE REVISIÓN

### Desarrollador
Claude — Desarrollador de Servidor de Vintage Telnet

### Estado base
Commit/HEAD de `main` sobre el que se trabajó:
`fffc5e6ab1e295f02b76c2b6809dc07622f28b38`

### Rama
`claude/vintage-telnet-server-v2`

### Objetivo
Javier decidió adoptar la base técnica ya elegida por el Arquitecto de Vintage Telnet y Raspberry Pi (Python + Flask/Waitress + SQLite, rescatando el diseño de `codex/vintage-telnet-server` / PR #1) y pidió explícitamente sumarle encima la parte jugable que yo ya había explorado en una implementación previa en Node.js (nunca publicada): aprobación de cuentas por el Dungeon Master, especies, mundo/movimiento y chat.

### Qué se rescató de PR #1 (sin cambios de lógica)
- `vintage-telnet/server/__init__.py`, `__main__.py`
- Capa de cuentas/sesión/CSRF/rate-limit de `app.py` y `store.py` (login, registro, logout, `/api/me`, `/healthz`)
- `vintage-telnet/tests/test_entry.py`, `test_http.py` (con 2 aserciones actualizadas por el cambio de esquema, ver abajo)
- `vintage-telnet/requirements.txt`, `.gitignore`
- `vintage-telnet/ops/server.env.example`, `vintage-telnet/ops/vintage-telnet.service`, `vintage-telnet/ops/RASPBERRY_REPORT.md`

No se rescató `AGENTS.md`/`HANDOFF.md` de esa rama vieja (documentación de coordinación obsoleta) ni `vintage-telnet/ops/RASPBERRY_HANDOFF.md` (referenciaba una rama/commit ya inexistente).

### Archivos nuevos
- `vintage-telnet/server/world.py` — especies y salas (placeholder de geografía, marcado explícitamente)
- `vintage-telnet/server/dm_auth.py` — verificación del secreto del Dungeon Master (`VT_DM_PASSWORD`)
- `vintage-telnet/server/templates/dm.html` — panel del Dungeon Master
- `vintage-telnet/server/README.md` — documentación técnica del servidor
- `vintage-telnet/tests/test_gameplay.py` — 10 pruebas nuevas

### Archivos modificados
- `vintage-telnet/server/store.py` — esquema versión 2: columnas `status`/`species`/`room` en `players`, tabla `room_messages`; funciones nuevas (`set_status`, `set_species`, `move_player`, `players_in_room`, `add_message`, `recent_messages`, `list_by_status`)
- `vintage-telnet/server/app.py` — rutas nuevas: `/species`, `/move`, `/room/say`, `/api/room`, `/dm`, `/dm/login`, `/dm/logout`, `/dm/approve`, `/dm/reject`, `/dm/remove`
- `vintage-telnet/server/templates/entry.html` — estados nuevos: pendiente, rechazado/eliminado, elegir especie, vista de mundo con movimiento y chat
- `vintage-telnet/server/admin.py` — el comando `players` ahora incluye `status`/`species`/`room` (sigue sin exponer `password_hash`)
- `vintage-telnet/tests/test_entry.py` — 2 aserciones actualizadas: `schema_version` esperado pasa de 1 a 2; la prueba de "versión de esquema desconocida" ahora usa 3 en vez de 2 (porque 2 ya es una versión válida)
- `AGENTS.md` — reactivé mi firma como "Desarrollador de Servidor — Vintage Telnet", explícitamente subordinada a la autoridad arquitectónica del Arquitecto de Vintage Telnet y Raspberry Pi

### Cambios realizados
- **Cuentas y aprobación:** el registro ahora deja la cuenta en `status = pending` (antes cualquiera que se registraba ya podía jugar; ahora nadie juega sin aprobación). El Dungeon Master aprueba/rechaza desde `/dm`. Eliminar una cuenta aprobada la marca `removed` (no se borra el registro) y **revoca sus sesiones activas en la base de datos**, así que el efecto es inmediato aunque la persona no esté conectada en ese momento — no hace falta un socket en vivo para lograrlo, a diferencia de mi prototipo anterior en Node.js.
- **Especies y mundo:** al aprobar, la cuenta elige una de las 5 especies confirmadas y aparece en su pueblo de inicio confirmado (`CONFIRMED_IDEAS.md`). Movimiento N/S/E/O sobre un grafo de salas placeholder (Vaisgard + 5 pueblos), igual en espíritu al que ya había probado en Node.js pero reescrito en Python/SQLite.
- **Chat:** local por sala, visible para quien esté en la misma sala, con lista de "quién más está aquí".
- **Contrato explícito:** `GET /api/room` devuelve JSON estructurado (no texto libre) pensando en que `vintage-telnet.html` pueda consumirlo en el futuro, siguiendo el principio de `ARCHITECTURE_STATUS.md` de que el cliente no debe inferir estado autoritativo leyendo texto.
- Deliberadamente NO se implementó: combate, PvP, clases/estadísticas, reaparición de monstruos, chat global, recuperación de contraseña — sigue abierto en `GAMEPLAY.md` o es endurecimiento de seguridad para después.

### Pruebas realizadas
- Suite completa: **19/19 pruebas pasan** (`python -m unittest discover -s tests -v`), incluidas las 9 heredadas sin cambios de comportamiento y las 10 nuevas de aprobación/especies/movimiento/chat.
- Prueba manual end-to-end con el servidor real (Waitress, no el cliente de test de Flask) vía `curl`: registro → pendiente → login del DM → aprobar → elegir especie (Felaryn → Khariel) → moverse al oeste (→ Vaisgard) → chat local → eliminar desde el DM → `/api/me` devuelve 401 inmediatamente después.
- Verifiqué que un jugador removido no puede volver a entrar con las mismas credenciales (queda en `status = removed`).

### Qué es funcional
- Todo lo descrito arriba, corriendo de verdad (no es una demo): cuentas, aprobación, especies, mundo, movimiento, chat, persistencia en SQLite que sobrevive a reinicio del proceso.

### Qué sigue siendo pendiente
- Geografía y descripciones reales del mundo (reemplazar el placeholder de `world.py`) — corresponde al Historiador.
- Todo combate/clases/progresión — corresponde a Jugabilidad, junto con Javier.
- Conectar `vintage-telnet.html` (cliente móvil actual, sigue siendo demo local) contra esta API real — requiere que el Arquitecto de Vintage Telnet y Raspberry Pi defina el contrato cliente-servidor en detalle antes de tocar ese HTML.
- Despliegue real en Raspberry Pi — corresponde al agente de Raspberry Pi, siguiendo la secuencia de `ARCHITECTURE_STATUS.md` (esta rama ya pasó "fuera de Raspberry": sintaxis, unit tests, integración HTTP local; falta systemd real, puertos/firewall, backup/restauración probada en el equipo real).
- Recuperación de contraseña, verificación de correo, HTTPS si sale de la red local.

### NECESIDAD DE JUGABILIDAD
- Sin cambios: fórmulas de combate, esfuerzo para cambiar de clase, tiempos de reaparición de monstruos, mecanismo de habilidades limitadas, fórmula de huida, protección ante diferencias extremas de poder — todo sigue "abierto" en `GAMEPLAY.md`.

### Riesgos/conflictos
- Ninguno detectado contra `main`: esta rama nació de `origin/main` vigente (no de la rama vieja divergida de PR #1), así que no hereda su desactualización.
- `vintage-telnet.html` no se tocó; sigue siendo la demo local del Desarrollador Junior, sin relación funcional con este servidor todavía.

### Aviso para el Arquitecto de Vintage Telnet y Raspberry Pi
Esta entrega implementa dentro del stack y la secuencia que ya publicaste en `ARCHITECTURE_STATUS.md` (rescatar PR #1, HTTP primero, contrato estructurado). Si algo de lo que agregué (esquema de `players`, rutas de aprobación/mundo/chat) no encaja con una decisión tuya que yo no haya visto, avisame y lo ajusto — no pretendo sustituir tu autoridad arquitectónica, solo ejecuté la siguiente pieza dentro de lo ya decidido.

### Aviso para el Integrador/Publicador
No publicar hasta autorización expresa de Javier. Comparar esta rama contra el HEAD vigente de `main` antes de integrar (mi rama y `vintage-telnet.html` no tocan los mismos archivos, pero `main` puede haber avanzado desde que la creé).

**LISTO PARA REVISIÓN:** SÍ
**LISTO PARA PUBLICAR:** NO — falta revisión del Arquitecto de Vintage Telnet y del Integrador, y autorización de Javier ("sube").

---

## ENTREGA PARA CHATGPT (histórico — publicada)

**Estado:** PUBLICADA EN `main`

### Desarrollador
Desarrollador Junior de Vintage Telnet

### Estado base
Commit/HEAD de `main`:
`4f015d48a7cfbc7cdf0fbac0e1fd7afe70876270`

### Rama
`junior/vintage-telnet-mobile-v2`

### Objetivo
Aplicar la investigación `VT-RES-002` para optimizar la interfaz HTML de Vintage Telnet en celular y separar visualmente la carcasa HTML café de la terminal Telnet negra/verde.

### Archivos modificados
- `vintage-telnet.html`
- `HANDOFF.md`

### Investigación consumida
- `vintage-telnet/RESEARCH_MOBILE_TELNET_UI.md`

### Cambios realizados
- Terminal Telnet convertida en una zona visual inequívoca: negro casi puro, texto verde y tipografía monoespaciada.
- Carcasa HTML conservada en tonos café/ocre para distinguir herramientas web de la sesión Telnet.
- Layout móvil rehecho como shell de alto visible con terminal flexible y scroll interno.
- En teléfono, mapa/estado dejan de ocupar espacio permanente; mapa/personaje/inventario/ayuda se abren en dialogs.
- Controles principales compactados sin reducirlos por debajo de objetivos táctiles prácticos.
- Cruceta N/O/Mirar/E/S mantenida con relación espacial clara.
- Atacar y Huir permanecen visibles como acciones principales de demo.
- Entrada de comandos conserva 16 px, añade `enterkeyhint="send"` y permanece próxima a la terminal.
- Safe areas incorporadas para notch/home indicator.
- Se eliminó `scrollIntoView` del documento: ahora solo se desplaza el log interno de terminal.
- Añadido soporte `prefers-reduced-motion`.
- Responsive reorganizado: compacto <=640 px, intermedio hasta 959 px, lateral persistente desde 960 px.
- No se añadieron frameworks ni lógica paralela de botones.

### Qué es funcional
- Navegación local de demo por N/S/E/O.
- Mirar.
- Entrada escrita de comandos y alias n/s/e/o.
- Botones y comandos siguen entrando por la misma función `perform()`.
- Mapa/personaje/inventario/ayuda mediante dialogs.
- Scroll interno de terminal.
- Layout compacto para teléfono y dos columnas en escritorio.
- Indicadores locales de última acción y combate.

### Qué sigue siendo demostración
- Ubicación y conectividad de la microzona.
- Mapa mostrado.
- Estado de sesión.
- Combate.
- Inventario/personaje.
- Todo continúa sin Raspberry Pi ni persistencia real.

### NECESIDAD DEL SERVIDOR
- Sin cambios respecto a la entrega anterior: contrato de acciones, estado persistente, ubicación real, inventario, combate, descubrimiento y resincronización.

### NECESIDAD DE JUGABILIDAD
- Sin cambios respecto a la entrega anterior: objetivo de ataque, huida, vocabulario definitivo y datos exactos de combate/personaje/mapa.

### Pruebas realizadas
- Comprobación estructural de terminal negra/verde.
- Comprobación de media query móvil <=640 px.
- Comprobación de terminal con scroll interno.
- Comprobación de targets táctiles de 44–46 px o mayores.
- Comprobación de safe areas superior e inferior.
- Comprobación de dialogs para mapa/personaje/inventario/ayuda.
- Comprobación de `enterkeyhint="send"`.
- Comprobación de ruta única `perform()` para botón y comando.
- Comprobación de ausencia de `scrollIntoView`.
- Comprobación de `prefers-reduced-motion`.
- Confirmación de que no se añadió framework externo.

### Prueba visual que Javier/Matías deben hacer
1. Abrir en teléfono vertical.
2. Confirmar que se percibe inmediatamente la separación: café = cliente HTML; negro/verde = Telnet.
3. Revisar cuántas líneas de texto caben sin scroll de página.
4. Moverse con una mano usando N/S/E/O.
5. Probar Mirar, Atacar y Huir.
6. Escribir 5–10 comandos seguidos con el teclado abierto.
7. Abrir/cerrar mapa, personaje, inventario y ayuda.
8. Girar teléfono a horizontal y regresar.
9. Probar en iPad vertical/horizontal.
10. Decidir si los controles siguen ocupando demasiado o si la proporción ya se siente correcta.

### Riesgos/conflictos
- Validación visual final requiere teléfono/iPad real.
- La terminal usa scroll interno en móvil; Javier/Matías deben confirmar que esta interacción resulta natural.
- Si `main` cambia antes de integrar, el Integrador debe volver a comparar la rama.

### Aviso para el Integrador/Publicador
No publicar hasta autorización expresa de Javier. Comparar esta rama contra el HEAD vigente de `main` antes de integrar.

**LISTO PARA REVISIÓN:** SÍ  
**PUBLICADA EN `main`:** SÍ — autorización “Sube” recibida el 2026-09-21  
**MERGE COMMIT:** `c156fce377203534f7d9cb14632ef4f36815310c`


## INTEGRACIÓN DE ARTE HTML — Vintage Telnet

**Fecha:** 2026-09-21  
**Estado:** INTEGRADO EN `main`

### Origen de la entrega
- Rama: `art/vintage-telnet-html-assets`
- Commit de arte revisado: `886314bfd9be648938cc7668e2527a079050d231`
- Estado antes de integrar: rama 1 commit adelante de `main` y 0 atrás.

### Qué se integró
Biblioteca modular de arte para la carcasa HTML de Vintage Telnet en:
`vintage-telnet/assets/html-ui/`

Incluye:
- botones para Inventario, Mapa, Huir y Poderes;
- ornamento de esquina;
- divisor horizontal dorado;
- textura azul/pizarra repetible;
- preview móvil de referencia;
- `README.md` y `ASSET_MANIFEST.md` con instrucciones de uso, tamaños y alcance.

### Criterio de revisión aplicado
- Los PNG son assets modulares; no sustituyen controles HTML reales.
- La terminal Telnet negro/verde debe mantenerse separada de la carcasa visual exterior.
- El arte sigue una dirección más juvenil/mobile-first y menos recargada.
- El botón `Poderes` queda como categoría visual; no define mecánicas ni poderes concretos.
- No se modificó `vintage-telnet.html` durante esta integración.
- No se modificó Senku.

### Pendiente
La siguiente tarea separada será adaptar `vintage-telnet.html` para consumir estos assets sin romper la lógica existente ni la ruta única de acciones del cliente.

### Resultado
- Arte integrado a `main`: SÍ.
- HTML actualizado para usar el arte: NO, pendiente de una tarea posterior.
- Publicación/servidor Raspberry: sin cambios por esta integración.


## PREPARACIÓN DE BASE DE DATOS Y JUGABILIDAD REAL — Vintage Telnet

**Fecha:** 2026-09-21  
**Estado:** PREPARACIÓN DOCUMENTADA; SERVIDOR V2 NO INTEGRADO

### Trabajo realizado
- Revisada la rama `claude/vintage-telnet-server-v2`.
- Commit revisado: `ca7be621cc7862cf4cbb7a34eaea0a787820cf63`.
- La entrega reporta SQLite real, cuentas/sesiones, aprobación del Dungeon Master, especies, ubicación persistente, movimiento N/S/E/O, chat local y API estructurada.
- La rama está divergida respecto a `main`; no se integró automáticamente.
- Se creó `vintage-telnet/DATABASE_GAMEPLAY_PREP.md` con el primer vertical slice jugable real, requisitos mínimos de persistencia, contrato cliente-servidor necesario, seguridad, pruebas y secuencia recomendada.

### Primer hito jugable acordado para preparación
`Abrir → entrar → aprobar cuenta → elegir especie → aparecer en pueblo → moverse → ver otro jugador → hablar → cerrar → volver → conservar ubicación.`

### Importante
- No se implementó ni inventó combate.
- No se modificó `vintage-telnet.html`.
- No se desplegó nada a Raspberry Pi.
- No se integró la rama de servidor V2.
- La siguiente acción técnica corresponde a revisión/actualización del servidor V2 contra el `main` vigente y cierre del contrato cliente-servidor.


## PRIORIDAD P0 — PRIMER SLICE JUGABLE REAL

Javier fijó la prioridad del siguiente hito:

**ENTRAR → ELEGIR ESPECIE → MOVERSE POR EL PUEBLO**

Se creó `vintage-telnet/FIRST_PLAYABLE_SLICE.md` con el alcance completo, contrato mínimo requerido, persistencia, responsabilidades y prueba de aceptación.

Por decisión de alcance, quedan fuera de este primer slice: chat, combate, PvP, clases, estadísticas, inventario, Arcanes, poderes, economía, monstruos, secretos y mapa completo.

El objetivo es llegar antes a una versión realmente persistente y jugable en teléfono.


## VT-SERVER: mapa regional servido + rumbo autoritativo (Issue #120)

**Desarrollador:** Claude — Desarrollador de Servidor de Vintage Telnet
**Estado:** LISTO PARA REVISIÓN
**HEAD base:** `9c5af20d132c09914c3d73e0b7c574438691ce0f` (`origin/main`)
**Rama/commit de entrega:** `claude/vintage-telnet-server-map-heading`
**Tarea asignada:** Issue #120 (`VT-SERVER: exponer mapa regional y rumbo autoritativo para Mapa y orientación`), dependencia no bloqueante detectada por Frontend en PR #119/#106.

### Cambios
- Nueva ruta `GET /assets/maps/<filename>` que sirve únicamente
  `assets/vintage-telnet/maps/` (donde ya vive `region-inicial.webp`,
  publicado por PR #99), con `mimetype="image/webp"` explícito igual que
  `/assets/locations/`. `send_from_directory` rechaza cualquier intento de
  salir de esa carpeta (traversal) con 404; no se expone el árbol completo
  de `assets/`.
- `/api/map` ahora incluye `current_heading` (`"north" | "south" | "east" |
  "west" | null`) además de `visited_rooms`/`traversed_routes`, que se
  conservan sin cambios.
- Nueva columna persistente `players.heading` (migración de esquema v6→v7
  en `store.py`, `ALTER TABLE` + `CHECK` de las cuatro direcciones
  cardinales). El servidor la fija en `store.move_player()` cada vez que
  `attempt_move()` acepta un movimiento, usando la misma dirección
  canónica ya resuelta por `DIRECTION_ALIASES` (nunca inferida de
  narrativa, nombre de sala ni imagen). Antes del primer movimiento queda
  `NULL` → `current_heading: null`, tal como permite la Issue.
- No se tocó `available_actions` (#73), narrativa, canon ni
  `vintage-telnet.html`.

### Pruebas
`cd vintage-telnet && .venv/bin/python -m unittest discover -s tests -v` → **171 tests, OK** (incluye 4 pruebas nuevas/actualizadas en `test_entry.py`: mapa servido con MIME correcto, ruta de mapas rechaza traversal/archivo inexistente, `current_heading` null→`"west"` tras moverse; y `schema_version`/`PRAGMA user_version` actualizados de 6→7 en `test_entry.py` y `test_inventory.py`, con el test de "esquema futuro desconocido falla cerrado" reapuntado a la versión 8).

### Trabajo previo afectado
Ninguna lógica de movimiento, combate, inventario ni mapa progresivo existente cambió de comportamiento; solo se agrega una columna y una clave nueva en la respuesta JSON. Los tests que fijaban `schema_version`/`user_version` en 6 se actualizaron a 7 porque ahora reflejan el esquema real tras la migración.

### Pendiente
- Ninguno dentro del alcance de esta Issue. Los criterios de aceptación 1–4 quedan cubiertos por el servidor; el criterio 5 ("Frontend #106 puede sustituir sus estados neutrales sin lógica inferida") depende de que Frontend consuma esta rama.

### Aviso para el otro desarrollador / Integrador
- No se hizo push a `main`; solo commits en `claude/vintage-telnet-server-map-heading`.
- No se desplegó ni tocó la Raspberry Pi.
- Cuando esta rama se integre, Frontend (#106/PR #119) puede reemplazar sus estados neutrales de mapa/rumbo consumiendo `/assets/maps/region-inicial.webp` y `current_heading` de `/api/map` directamente.


## VT-SERVER: gasto de PA, PP, subida de nivel sin curación total y fatiga pasiva (PLAYABILITY_READINESS P1 #5/#6)

**Desarrollador:** Claude — Desarrollador de Servidor de Vintage Telnet
**Estado:** LISTO PARA REVISIÓN
**HEAD base:** `8ba4d1d08d0474e0fdd402b6ae26c32b48e48831` (`origin/main`)
**Rama de entrega:** `claude/vintage-telnet-server-progression-fatigue`
**Origen:** encargo directo de Javier (2026-09-24): revisar el juego y adelantar lo más atrasado. `PLAYABILITY_READINESS.md` marca como P1 pendientes el gasto de PA (§25.4) y la recuperación pasiva de fatiga (§24.7). Las reglas ya estaban **APROBADAS PARA IMPLEMENTACIÓN** en `GAMEPLAY.md` y solo faltaba el servidor. No se inventó ninguna mecánica.

### Cambios
- **Bug corregido (§25.6):** `store.award_xp` curaba al 100% en cada subida de nivel. Ahora el HP actual sube solo por la diferencia del nuevo máximo (`combat.hp_after_max_change`).
- **PP (§25.1/§25.8):** nueva columna `players.pp_unspent`. Se da 1 PP por cada nivel múltiplo de 5. Antes no se registraban.
- **Aviso de subida (§25.9):** el mensaje de victoria o descubrimiento dice ahora nivel, PA y PP obtenidos. Antes, subir de nivel por un descubrimiento no avisaba nada.
- **Gasto de PA (§19/§25.4/§25.5/§25.7):**
  - `GET /api/character` agrega `attribute_costs`, `pp_unspent` e `in_combat`.
  - Nuevo `POST /api/character/attributes` con `{attribute, current_value, csrf}`. `current_value` es la confirmación: si ya no coincide con el valor real, responde `409 stale_confirmation` y no gasta nada.
  - Solo fuera de combate, sin PA negativos, atómico y sin deshacer. Subir Resistencia o Voluntad recalcula el HP máximo con la regla de diferencia.
- **Fatiga pasiva (§24.7):**
  - Se recupera 1 punto cada 10 s fuera de combate, calculado por tiempo en servidor al leer el personaje. No hay proceso de fondo.
  - Cualquier cambio explícito de fatiga reinicia el reloj. En combate no se recupera. No toca HP ni heridas.
- **Esquema v7→v8:** columnas `pp_unspent` y `fatigue_updated_at`. Los personajes existentes reciben los PP de los niveles múltiplo de 5 que ya alcanzaron. Se agregó la constante `store.SCHEMA_VERSION`.
- **`ops/inventory_migration_probe.py`:** seguía esperando el esquema v6 (ya estaba desfasado frente a la v7). Ahora valida contra `store.SCHEMA_VERSION` y las columnas de v7/v8, y cierra sus conexiones SQLite (antes fallaba en Windows al borrar el temporal).

### Pruebas
- `cd vintage-telnet && .venv/bin/python -m unittest discover -s tests -v` → **215 tests, OK**.
  - 19 son nuevas, en `tests/test_progression.py`.
  - En `test_entry.py`/`test_inventory.py` se actualizaron las aserciones de esquema 7→8. El caso de "esquema futuro desconocido" ahora apunta a la versión 9.
- `ops/inventory_migration_probe.py` sobre una base v7 simulada con un jugador: 7→8, jugadores preservados, 11/11 OK.

### NECESIDAD DE FRONTEND (no la hice: `vintage-telnet.html` no es de mi área)
El panel Personaje debe:
- mostrar los PA y PP disponibles y el coste del siguiente +1;
- pedir confirmación (atributo, valor actual → nuevo valor, coste);
- enviar `POST /api/character/attributes` con el `current_value` que vio el jugador;
- deshabilitar el gasto cuando `in_combat` sea verdadero.

No debe ofrecer poderes con PP (§25.8: todavía no hay contenido de poder validado).

### Riesgos
- **Migración:** es aditiva (dos `ALTER TABLE ADD COLUMN` y un backfill de PP). No borra ni reescribe estado vivo. Antes de desplegar, el Operador de Raspberry puede correr `ops/inventory_migration_probe.py` sobre la base viva, en solo lectura.
- **Cambio de comportamiento:** subir de nivel ya no cura por completo. Es lo que exige §25.6, pero los jugadores lo notarán.

### Aviso para el Integrador / Operador de Raspberry
- No se hizo push a `main`.
- No se tocó la Raspberry.
