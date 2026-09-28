# C0 — motor aislado de fauna ambiental (#379)

DESARROLLADOR: Codex desktop. Fecha: 2026-09-27.
HEAD BASE: `fe3b402e404e552a980cddfe45535b278ba48c91`.
RAMA: `codex/vt-379-ambient-c0`.
Consumidor: Codex Raspberry / integrador, por instrucción de Javier.
Estado de este tramo: **LISTO PARA REVISIÓN**.

## Alcance entregado

`server/ambient.py` implementa selección pura y control de presentación C0 de
GAMEPLAY §39.1–39.5. `tests/test_ambient.py` usa exclusivamente fixtures sintéticos.
No modifica app.py, templates, combate, movimiento, SQLite, dependencias ni deploy.
No activa fauna productiva: `CATALOG = ()`.

Esta entrega es un tramo integrable de #379, **no cierra el issue completo**:
el motor aún no está conectado a HTTP, a la terminal ni al comando atacar.
La prueba de retirada verifica la API del motor, no un ataque HTTP.
La conexión del adaptador y las pruebas end-to-end siguen pendientes; la activación
productiva además espera catálogo y mapping canónico de Historia #333.

## Contrato de uso

- `Habitat(room_id, habitat_id, region, tags, profile)`: contexto autoritativo de
  sala. Perfiles `ambient_none/sparse/normal/rich` = 0/15/30/45%.
- Registros C0: exactamente `ambient_id`, `name`, `regions`, `habitat_tags`,
  `behavior_text`, `exclusions`. Las dos allowlists deben ser no vacías.
- Compatibilidad: región incluida y al menos un tag de hábitat compartido.
  Exclusiones vetan coincidencias con room_id, habitat_id, región o tags.
  Esta es la semántica técnica del adaptador; si la tabla canónica necesita otra
  semántica, reconciliar antes de activarla, sin reinterpretar contenido silenciosamente.
- `select_presence(habitat, catalog=..., now=..., hash_fn=...,
  combat_active=..., scripted=..., encounter=...)`: devuelve una `Presence` o None.
  Las prioridades deben venir del servidor, nunca del cliente. En combate,
  scripted o C1+ devuelve None sin tirar C0.
- Fase `floor(unix_time / 600)`. SHA-256 estable sobre JSON de dominio + fase +
  sala + hábitat. Un roll de presencia y, si procede, una selección equiprobable
  entre registros compatibles ordenados por ID. No hay pesos de rareza inventados;
  añadir registros no incrementa la chance de presencia.
- `observe(presence, session_state, explicit=False)`: emite solo una vez por
  sesión/sala/fase. Observación explícita puede repetir; ida/vuelta no reinicia
  el control. Reasigna la clave `ambient_c0` para soportar sesiones Flask.
- `withdraw(presence, session_state)`: resultado estructurado `ambient_withdrawn`
  con ID/nombre; retira solo la presentación de esa sesión hasta nueva fase.
  El adaptador debe producir la respuesta legible y terminar la acción sin entrar
  al motor de combate. No concede XP/loot ni altera la observación de otros jugadores.
- Pasar siempre una presencia recién seleccionada; no almacenar objetos Presence
  como identidades persistentes. La sesión conserva solo fase y estados por sala;
  la siguiente fase descarta los anteriores. Una sesión nueva vuelve a observar.

## Próximo adaptador (pendiente, fuera de este tramo)

1. Recibir catálogo/mapping autorizados; impedir mezclar IDs C1+ con C0.
2. En lectura de sala, seleccionar usando estado real de combate/encuentros y
   aplicar observe solo cuando se vaya a presentar, evitando que un polling
   invisible consuma el evento antes que la terminal.
3. Conectar mirar explícito y retirada por intento de ataque C0 sin tocar
   encuentros combatibles. No usar withdraw para interceptar ataques C1/scripted.
4. Añadir pruebas HTTP de prioridad, movimiento, no XP/combate y sesión/reconnect.
5. Coordinar cambios de app.py con #380 y #381, que tienen ramas de Antigravity.

## Pruebas locales ejecutadas

Windows / Python 3.12.14, desde `vintage-telnet/`:

```text
.venv/Scripts/python.exe -m unittest discover -s tests -p test_ambient.py -v
25 tests — OK
.venv/Scripts/python.exe -m unittest discover -s tests -p test_random_encounters.py -v
17 tests — OK
```

Incluyen densidades con 5.000 fases por perfil, frontera temporal exacta,
reproducibilidad entre procesos con distinto PYTHONHASHSEED, máximo uno,
catálogo vacío/inválido, compatibilidad/exclusión, prioridad, anti-spam,
observación explícita y retirada local sin estado persistente.

No se ejecutó la suite completa ni pruebas físicas en Raspberry en este tramo;
no se presentan estas 42 pruebas como suite completa. El código nuevo no está
importado por rutas de producción. No se hicieron merge ni deploy.

## Entrega al integrador

Revisar diff y repetir las dos suites sobre el SHA exacto de la PR. Javier pidió
que Codex Raspberry sea quien integre a main tras revisar; esta entrega no pide
desplegar ni usar datos vivos. Registrar resultado en la PR. Mantener #379 abierto
con los pendientes del adaptador y #333, incluso si este tramo se integra.
