# Vintage Telnet — Servidor autoritativo

Servidor Python (Flask + Waitress + SQLite) para Vintage Telnet: cuentas con
aprobación del Dungeon Master, mundo con movimiento N/S/E/O, chat local por
sala, y ahora combate/XP/descubrimientos/mapa progresivo v1 según
[`../GAMEPLAY.md`](../GAMEPLAY.md) (secciones 20-23) para la microaventura
piloto VT-NAR-003 "El lindero roto". Lo que ese documento sigue dejando
abierto (PvP, poderes/Arcanes, clases, tabla de Cornalomo) no se inventa
aquí.

Esta base nace de la entrega histórica `codex/vintage-telnet-server` (PR #1),
rescatada sobre el `main` vigente según la decisión del Arquitecto de
Vintage Telnet y Raspberry Pi en
[`../ARCHITECTURE_STATUS.md`](../ARCHITECTURE_STATUS.md). La capa de
cuentas/sesión/CSRF/rate-limit es la original de esa entrega; species,
mundo, movimiento, chat y aprobación del Dungeon Master son nuevos.

Cumple el alcance mínimo de
[`../FIRST_PLAYABLE_SLICE.md`](../FIRST_PLAYABLE_SLICE.md) (P0): entrar,
elegir especie y moverse por el pueblo, con persistencia real.

## Cómo correrlo

```bash
cd vintage-telnet
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # en Windows: .venv\Scripts\pip
VT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))') \
VT_DATA_DIR=/tmp/vintage-telnet-data \
VT_DM_PASSWORD=elegí-una-contraseña \
VT_ALLOW_HTTP=1 \
.venv/bin/python -m server
```

Por defecto escucha en `127.0.0.1:8080` (`VT_HOST`/`VT_PORT`). `VT_DATA_DIR`
debe ser una ruta absoluta fuera del checkout — ahí vive `vintage.sqlite3`,
nunca versionado en git. `VT_SECRET_KEY` debe tener 32+ caracteres
aleatorios. `VT_ALLOW_HTTP=1` solo sirve para pruebas locales/LAN sin HTTPS;
en producción real debe ir detrás de HTTPS y esta variable debe quedar sin
definir (por defecto exige cookies seguras).

`VT_DM_PASSWORD` habilita `/dm`, el panel del Dungeon Master, y es
**obligatoria** para completar el recorrido P0 (sin ella nadie puede
aprobarse y nadie puede jugar). Si no está definida, el panel queda
deshabilitado (falla cerrado), nunca acepta cualquier contraseña por
defecto. Ver [`../ops/server.env.example`](../ops/server.env.example).

## Correr las pruebas

```bash
cd vintage-telnet
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

63 pruebas: 9 heredadas de la entrega original + 19 de especies/movimiento/API
del primer slice jugable + 3 de enrutamiento de intención (Issue #25) +
32 de la microaventura piloto (`test_pilot_lindero_roto.py`): fórmulas de
combate/XP puras contra la tabla de referencia de `GAMEPLAY.md`,
calibración de Mordelinde/Espinajo de rastrojo en la banda de peligro que
pidió Jugabilidad, contenido/conectividad del camino nuevo, y flujo
completo por HTTP (examinar → descubrimiento → XP, evaluar sin revelar
números, atacar hasta la victoria con antifarmeo/bono de primera familia,
huir, muerte/reaparición al 60% de HP, persistencia del mapa tras
reiniciar el proceso).

## Qué existe hoy

### Cuentas y aprobación
- Registro en `/` (formulario) → cuenta con `status = pending`.
- El Dungeon Master (`/dm`, protegido por `VT_DM_PASSWORD`, con su propio
  límite de intentos) ve las cuentas pendientes y puede **Aceptar** o
  **Rechazar**.
- Solo cuentas `approved` pueden elegir especie y jugar.
- El Dungeon Master puede **Eliminar** una cuenta aprobada: queda marcada
  `removed` (no se borra el registro) y sus sesiones activas se revocan al
  instante — el próximo request de esa persona ya devuelve 401/estado no
  habilitado, sin depender de que esté conectada en ese momento.
- Contraseñas con `werkzeug.security` (scrypt), nunca en texto plano.
  Comparación de login contra un hash señuelo cuando el usuario no existe,
  para no filtrar por tiempo qué cuentas son reales.

### Mundo
- Primera vez que una cuenta aprobada elige especie (`POST /species` o
  `POST /api/species`): una de las cinco confirmadas (Humano, Felaryn,
  Dravak, Marevyn, Vesperi), aparece en el punto central de su pueblo de
  inicio confirmado (`../CONFIRMED_IDEAS.md`). La elección solo aplica una
  vez — es atómica de verdad (`store.set_species` usa `rowcount`, no una
  lectura previa), así que dos intentos casi simultáneos no pueden
  aceptarse los dos.
- Cada pueblo de inicio es una **microzona** de 3-4 salas (punto
  central/comunitario + forja/taller + mercado/alimentos + sendero cuando
  queda una cuarta dirección libre), suficiente para probar movimiento
  real N/S/E/O dentro del pueblo, no solo salir hacia Vaisgard. Ver
  `world.py` — sigue siendo **placeholder de geografía**, marcado
  explícitamente; no es canon.
- Movimiento norte/sur/este/oeste (`POST /move`, `POST /api/move`, o
  escribiendo el comando) validado contra las salidas reales de la sala
  actual.
- Estado persistente real en SQLite: la sala/especie del jugador sobrevive
  a reinicios del proceso y a cambiar de dispositivo.
- Chat local por sala (visible en `GET /api/room` y en la página
  principal) y lista de quién más está en la sala. Solo se expone el
  nombre para mostrar (`name`); el usuario de login de otro jugador nunca
  sale en el chat ni en la lista de presentes.

### Botón y comando escrito son la misma acción
El cuadro de texto de la terminal postea a `POST /command`: si el texto es
norte/sur/este/oeste (o n/s/e/o), ejecuta exactamente la misma función
autoritativa (`attempt_move`) que los botones de la cruceta; "mirar"
refresca; cualquier otro texto se trata como chat local (fuera de alcance
P0 según `FIRST_PLAYABLE_SLICE.md`, pero se conserva porque ya funciona).

### Contrato API estructurado para un cliente enriquecido
- `GET /api/me` — identidad, estado, especie, sala, y el token `csrf`
  vigente (para que un cliente JSON pueda operar sin parsear HTML).
- `GET /api/room` — sala actual estructurada (id, nombre, descripción,
  salidas, quién está presente, mensajes recientes).
- `POST /api/species` — especie confirmada + **pueblo inicial** (`town`) +
  sala inicial + estado actualizado del jugador (`player`).
- `POST /api/move` — aceptada/rechazada, sala anterior, sala actual
  estructurada y motivo de rechazo si aplica. El cliente no necesita
  interpretar texto narrativo para saber dónde quedó.
- **Errores en JSON, no HTML:** las rutas `/api/*` devuelven
  `{"error": "unauthenticated"}` (401), `{"error": "not_approved", "status": ...}`
  (403) o `{"error": "species_required"}` (409) en vez de una página HTML de
  error — las rutas de formulario (`/move`, `/species`, `/command`) siguen
  devolviendo la plantilla con `error` para el humano.
- Pensado para que `vintage-telnet.html` (o su sucesor) deje de ser una
  demo local y hable con este servidor cuando el Arquitecto decida
  conectarlos; las rutas de formulario siguen funcionando como fallback.

### Microaventura piloto "El lindero roto" (VT-NAR-003)

Camino nuevo desde Valdren (`valdren_sendero` se extiende hacia el oeste con
`valdren_camino_parcela` → `valdren_camino_cerca` → `valdren_camino_lindero`,
textos citados de `../NARRATIVE.md`), implementando GAMEPLAY.md 20-22 tal
como los pidió Jugabilidad en el Issue #45:

- **Personaje real:** ocho atributos (base 10), nivel, XP, HP, fatiga
  (campo listo, sin tabla de coste por acción todavía — ver Pendiente),
  herida (campo listo, sin disparador de combate todavía — ver Pendiente),
  PA sin gastar acumulados por nivel. `GET /api/character`.
- **Combate real** (`atacar`/`huir`, botones o comando, misma acción
  autoritativa): precisión/daño/HP exactos de GAMEPLAY.md 20.4/20.3, muerte
  y reaparición al 60% HP en `valdren_centro` (20.9), huida con fórmula
  20.10. Mordelinde y Espinajo de rastrojo (`server/creatures.py`) tienen
  las estadísticas de calibración inicial que pidió el Issue #45 para caer
  en la banda Favorable/Comparable y Comparable/Peligroso respectivamente
  contra un personaje nuevo — **afinable de balance, no definitivo**
  (GAMEPLAY.md 20.15). Cornalomo no tiene stats: se pide su tabla a
  Jugabilidad cuando exista combate real contra él.
- **`evaluar <criatura>`** (GAMEPLAY.md 22.11): categoría cualitativa
  (Trivial/Favorable/Comparable/Peligroso/Abrumador) sin revelar HP, daño
  ni porcentajes.
- **XP y antifarmeo** (22.4-22.8): coeficiente por categoría, tope del 25%
  del siguiente nivel, bono de primera victoria por familia, reducción por
  repetición en las últimas 10 victorias PvE.
- **Descubrimientos** (22.7): señales de Mordelinde (`examinar
  tallos/monticulos`), el lindero roto (`examinar cerca/huellas`) y el
  regreso a Valdren con el hallazgo — cada uno una sola vez por personaje.
- **Mapa progresivo** (23): `GET /api/map` devuelve solo las salas
  visitadas y rutas recorridas por ese personaje, persistente en SQLite.

Contrato completo en `server/combat.py` (fórmulas puras, sin Flask/DB —
cada función cita la sección de GAMEPLAY.md de la que sale).

**NECESIDAD DE JUGABILIDAD pendiente** (no implementado a propósito, para
no inventar mecánica que el documento deja abierta):
- Tabla de coste de fatiga por acción (20.7 la deja explícitamente para
  "la tabla de acciones/poderes", que todavía no existe).
- Disparador de heridas en combate v1 (20.8 define los tres grados y el
  downgrade al reaparecer, pero no cuándo se asigna una herida durante la
  pelea).
- Defensa contextual (Esquivar/Bloquear/Resistir): en este piloto el
  combate es un intercambio simple sin elección activa de defensa; el
  Issue #43 (P1) es quien pide ese panel contextual.

## Qué NO existe todavía (a propósito)

- PvP, protección ante diferencias de poder, poderes/PP, Arcanes.
- Clases y fórmulas de progresión más allá de lo ya implementado en 20-22.
- Persistencia/reaparición de monstruos por temporizador (respawn de
  criaturas comunes: referencia 20.14, no implementado — la criatura
  reaparece llena la próxima vez que se visita la sala, sin cooldown).
- Chat global (solo hay chat local por sala).
- Geografía y descripciones **definitivas** del mundo: sigue siendo
  placeholder en `world.py`. El Arquitecto ya definió (ver PR #8,
  `../CONTENT_RUNTIME_ARCHITECTURE.md`) que el contenido narrativo del
  Historiador se cargará como contenido versionado desde
  `vintage-telnet/content/` con sincronización automática a Raspberry
  cada 10 horas (staging → validación → release por SHA → symlink
  atómico → health check → rollback). Migrar `world.py` a ese mecanismo
  es una entrega separada posterior, no parte de este servidor todavía.
- Recuperación de contraseña, verificación de correo.
- Integración real con `vintage-telnet.html`: ese cliente sigue siendo una
  demo local sin backend; conectar ambos es una decisión de contrato que
  corresponde al Arquitecto de Vintage Telnet y Raspberry Pi.

## Estructura

```
vintage-telnet/
├── requirements.txt
├── ops/                        systemd, env de ejemplo (incluye VT_DM_PASSWORD), plantilla de reporte de Raspberry
├── server/
│   ├── __main__.py             arranque con waitress
│   ├── app.py                  rutas Flask (cuentas, DM, mundo, movimiento, comando, combate, chat, API JSON)
│   ├── store.py                SQLite: esquema versionado, cuentas, sesiones, salas, mensajes, personaje, mapa, encuentros
│   ├── world.py                especies, microzonas de los 5 pueblos y la microaventura piloto (placeholder de geografía)
│   ├── combat.py                fórmulas puras de combate/XP (GAMEPLAY.md 20-22), sin Flask ni DB
│   ├── creatures.py             estadísticas de combate de Mordelinde/Espinajo de rastrojo
│   ├── dm_auth.py               verificación del secreto del Dungeon Master
│   ├── admin.py                 CLI de operación: listar, backup verificado, integrity check
│   └── templates/
│       ├── entry.html           login/registro/estado/especie/mundo/combate/chat/comando
│       └── dm.html               panel del Dungeon Master
└── tests/
    ├── test_entry.py            pruebas heredadas de cuentas/sesión/CSRF/etc.
    ├── test_http.py              prueba de proceso HTTP real con reinicio
    ├── test_gameplay.py          aprobación, especies, movimiento, comando/botón, API, CSP, privacidad
    └── test_pilot_lindero_roto.py  combate/XP/descubrimientos/mapa de VT-NAR-003
```

## Despliegue en Raspberry Pi

Ver [`../ops/server.env.example`](../ops/server.env.example) (incluye
`VT_DM_PASSWORD`, obligatoria para el flujo P0) y
[`../ops/vintage-telnet.service`](../ops/vintage-telnet.service) (unidad
systemd ya endurecida: usuario dedicado, `ProtectSystem=strict`,
`NoNewPrivileges`, `PrivateTmp`, directorio de estado separado). No
desplegar sin haber corrido la suite completa fuera de la Raspberry
primero, según la secuencia técnica de `../ARCHITECTURE_STATUS.md`.

### Respaldo periódico

[`../ops/backup.sh`](../ops/backup.sh) +
[`../ops/vintage-telnet-backup.service`](../ops/vintage-telnet-backup.service) +
[`../ops/vintage-telnet-backup.timer`](../ops/vintage-telnet-backup.timer):
respaldo diario de `vintage.sqlite3` vía `server.admin backup` (que ya
verifica integridad de la copia), con poda automática de backups de más de
14 días (`VT_BACKUP_KEEP_DAYS`). Activar junto con el servicio principal:

```bash
sudo systemctl enable --now vintage-telnet-backup.timer
```

Esto responde al pendiente que el operador de Raspberry dejó explícito en
`../ops/RASPBERRY_REPORT.md`: no había política de respaldo antes de la
primera instalación real. El script no reemplaza una copia fuera del
equipo (disco externo, otra máquina); eso sigue siendo una decisión
operativa aparte.
