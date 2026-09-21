# Vintage Telnet — Servidor autoritativo

Servidor Python (Flask + Waitress + SQLite) para Vintage Telnet: cuentas con
aprobación del Dungeon Master, mundo con movimiento N/S/E/O y chat local por
sala. No implementa combate, clases, progresión ni PvP: esas decisiones
siguen abiertas en [`../GAMEPLAY.md`](../GAMEPLAY.md) y no se inventaron aquí.

Esta base nace de la entrega histórica `codex/vintage-telnet-server` (PR #1),
rescatada sobre el `main` vigente según la decisión del Arquitecto de
Vintage Telnet y Raspberry Pi en
[`../ARCHITECTURE_STATUS.md`](../ARCHITECTURE_STATUS.md). La capa de
cuentas/sesión/CSRF/rate-limit es la original de esa entrega; species,
mundo, movimiento, chat y aprobación del Dungeon Master son nuevos.

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

`VT_DM_PASSWORD` habilita `/dm`, el panel del Dungeon Master. Si no está
definida, el panel queda deshabilitado (falla cerrado), nunca acepta
cualquier contraseña por defecto.

## Correr las pruebas

```bash
cd vintage-telnet
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

19 pruebas: 9 heredadas de la entrega original (cuentas, sesiones, CSRF,
rate limit, concurrencia, backup/inspección, fail-closed, reinicio de
proceso) + 10 nuevas (aprobación del DM, especies, movimiento, chat).

## Qué existe hoy

### Cuentas y aprobación
- Registro en `/` (formulario) → cuenta con `status = pending`.
- El Dungeon Master (`/dm`, protegido por `VT_DM_PASSWORD`) ve las cuentas
  pendientes y puede **Aceptar** o **Rechazar**.
- Solo cuentas `approved` pueden elegir especie y jugar.
- El Dungeon Master puede **Eliminar** una cuenta aprobada: queda marcada
  `removed` (no se borra el registro) y sus sesiones activas se revocan al
  instante — el próximo request de esa persona ya devuelve 401/estado no
  habilitado, sin depender de que esté conectada en ese momento.
- Contraseñas con `werkzeug.security` (scrypt), nunca en texto plano.
  Comparación de login contra un hash señuelo cuando el usuario no existe,
  para no filtrar por tiempo qué cuentas son reales.

### Mundo
- Primera vez que una cuenta aprobada elige especie (`POST /species`):
  una de las cinco confirmadas (Humano, Felaryn, Dravak, Marevyn, Vesperi),
  aparece en su pueblo de inicio confirmado
  (`../CONFIRMED_IDEAS.md`). La elección solo aplica una vez.
- Movimiento norte/sur/este/oeste (`POST /move`) sobre un grafo de salas
  **placeholder** (marcado explícitamente en `world.py`): Vaisgard + los
  cinco pueblos de inicio, conectividad mínima solo para probar
  movimiento. No es geografía canónica; el Historiador debe reemplazarla.
- Estado persistente real en SQLite: la sala/especie del jugador sobrevive
  a reinicios del proceso y a cambiar de dispositivo (mismo modelo que ya
  probaban las pruebas heredadas para la sesión).
- Chat local por sala (`POST /room/say`, visible en `GET /api/room` y en
  la página principal) y lista de quién más está en la sala.

### Contrato API para un futuro cliente enriquecido
- `GET /api/me` — identidad, estado, especie, sala.
- `GET /api/room` — sala actual estructurada (id, nombre, descripción,
  salidas, quién está presente, mensajes recientes). Pensado para que
  `vintage-telnet.html` (o su sucesor) deje de ser una demo local y hable
  con este servidor cuando el Arquitecto decida ese contrato en detalle.
- Las rutas de acción (`/species`, `/move`, `/room/say`) hoy son formularios
  HTML clásicos (POST + redirect 303), consistente con el resto del
  servidor; no hay WebSocket ni tiempo real todavía, siguiendo la decisión
  de "HTTP primero" en `../ARCHITECTURE_STATUS.md`.

## Qué NO existe todavía (a propósito)

- Combate, PvP, huida, protección ante diferencias de poder.
- Clases, estadísticas, fórmulas de progresión.
- Persistencia/reaparición de monstruos, pérdida de armas, forja física.
- Chat global (solo hay chat local por sala).
- Geografía y descripciones reales del mundo (`world.py` es un
  placeholder explícito para el Historiador).
- Recuperación de contraseña, verificación de correo.
- Integración real con `vintage-telnet.html`: ese cliente sigue siendo una
  demo local sin backend; conectar ambos es una decisión de contrato que
  corresponde al Arquitecto de Vintage Telnet y Raspberry Pi.

## Estructura

```
vintage-telnet/
├── requirements.txt
├── ops/                        systemd, env de ejemplo, plantilla de reporte de Raspberry
├── server/
│   ├── __main__.py             arranque con waitress
│   ├── app.py                  rutas Flask (cuentas, DM, mundo, movimiento, chat)
│   ├── store.py                SQLite: esquema versionado, cuentas, sesiones, salas, mensajes
│   ├── world.py                especies y salas (placeholder de geografía)
│   ├── dm_auth.py               verificación del secreto del Dungeon Master
│   ├── admin.py                 CLI de operación: listar, backup verificado, integrity check
│   └── templates/
│       ├── entry.html           login/registro/estado/especie/mundo/chat
│       └── dm.html               panel del Dungeon Master
└── tests/
    ├── test_entry.py            pruebas heredadas de cuentas/sesión/CSRF/etc.
    ├── test_http.py              prueba de proceso HTTP real con reinicio
    └── test_gameplay.py          pruebas nuevas: aprobación, especies, movimiento, chat
```

## Despliegue en Raspberry Pi

Ver [`../ops/server.env.example`](../ops/server.env.example) y
[`../ops/vintage-telnet.service`](../ops/vintage-telnet.service) (unidad
systemd ya endurecida: usuario dedicado, `ProtectSystem=strict`,
`NoNewPrivileges`, `PrivateTmp`, directorio de estado separado). No
desplegar sin haber corrido la suite completa fuera de la Raspberry
primero, según la secuencia técnica de `../ARCHITECTURE_STATUS.md`.
