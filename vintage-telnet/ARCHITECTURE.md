# Arquitectura técnica — entrada 0.1.0

Estado: implementada para prueba local; despliegue físico pendiente. HEAD de partida:
`bb2fef58ee1607d216e3bbc77b3d623489d24e9b` (2026-09-20).

## Autoridad y componentes

Dispositivo → formularios HTTP → Flask/Waitress en Raspberry → SQLite local.
Una instalación, un mundo compartido y una base persistente fuera del checkout.
No usar bases distintas por dispositivo. No guardar estado del mundo en cookies,
localStorage ni Git. No servir documentación narrativa ni secretos al navegador.

`server/app.py` adapta HTTP y valida entradas. `server/store.py` posee las
transacciones de identidad/acceso. `server/admin.py` permite inspección y respaldo
locales. `server/templates/entry.html` es una vista renderizada por el servidor.
Waitress ejecuta un proceso con cuatro hilos; cada operación abre su conexión
SQLite, activa claves foráneas y espera hasta diez segundos por bloqueos.

## Identidad persistente

`players` almacena UUID inmutable, `player_number` creciente (AUTOINCREMENT),
usuario único normalizado a minúsculas, nombre visible, hash scrypt con sal,
fecha de creación y último acceso en UTC. El número se muestra como `#0002`;
el ancho mínimo de cuatro dígitos no limita el total ni promete números sin huecos.
El usuario es la identificación mínima: no se piden correo, teléfono, edad ni
nombre legal. Un nombre visible no demuestra identidad; se exige contraseña.

`access_events` conserva cada registro e inicio de sesión exitoso, tipo, jugador
y fecha. Registro, número, sesión, último acceso y evento se confirman en una sola
transacción. Un login fallido no actualiza último acceso. Recargar la página no
equivale a un nuevo login. No se registra un cierre de navegador como desconexión:
esa señal no es confiable y esta entrega no implementa presencia en línea.

`sessions` conserva hash de token aleatorio, jugador y caducidad absoluta de 12 h.
La cookie firmada contiene token y CSRF; no contiene personaje ni ubicación.
Cerrar sesión revoca ese token en la base. Se permiten varias sesiones del mismo
jugador sin duplicar su cuenta. La caducidad de sesión no borra al jugador.

`auth_limits` limita registro y login a veinte envíos por IP/minuto, incluso tras
reiniciar. Guarda SHA-256 de IP, no una lista de direcciones en el historial; se
limpia al recibir posteriores intentos. Una familia tras NAT comparte el límite.
Esto es una defensa básica para prueba local, no protección suficiente para
publicación en Internet. No se confía en X-Forwarded-For.

## Evolución sin reemplazar las cuentas

Esquema versionado con `PRAGMA user_version=1`; creación transaccional. El servidor
rechaza versiones desconocidas. Las siguientes entregas deben incluir migración
ordenada, respaldo previo y pruebas de actualización de datos reales anonimizados.
No se reinicializa ni reemplaza una base para desplegar código.

Diseño previsto, **sin crear todavía tablas ni contenido jugable**:

| Entidad futura | Relación y responsabilidad |
| --- | --- |
| Personajes | FK a `players.id`; especie y clase referencian contenido aprobado. La cantidad de personajes por cuenta está pendiente. |
| Lugares | ID estable de lugar; región, asentamiento y descripción definidos por contenido. |
| Posición | FK personaje → lugar; la guarda el servidor dentro de la transacción de movimiento. Al volver se lee esa misma fila. |
| Inventario/progreso | FK al personaje; derechos y cambios validados por servidor, nunca aceptados como estado enviado por el cliente. |
| Entidades y acontecimientos | Tablas del único mundo; transacciones para evitar adjudicar dos veces un objeto o una derrota única. |
| Presencia y comunicación | Sesiones/conexiones separadas de la posición persistente; cerrar iPad no elimina al personaje. |

La API futura recibirá intenciones/comandos, comprobará reglas y confirmará cambios
atómicos antes de responder. SQLite permite un escritor a la vez; para esta fase
es suficiente. Revisar carga y coordinación antes de introducir simulación,
varios procesos, colas o un tick de mundo. No montar SQLite en un disco de red ni
desplegar réplicas escritoras independientes.

## Contrato HTTP actual

| Ruta | Resultado |
| --- | --- |
| GET `/` | Formularios o bienvenida con número de jugador. |
| POST `/register` | `username`, `name`, `password`, `csrf`; 303 al confirmar, 400 inválido, 409 duplicado. |
| POST `/login` | `username`, `password`, `csrf`; 303 al entrar, 401 credenciales incorrectas. |
| POST `/logout` | `csrf`; revoca sesión, 303 al inicio. |
| GET `/api/me` | Datos de la propia cuenta y `world_status`; 401 sin sesión. |
| GET `/healthz` | Lectura de tabla y versión del esquema; 200 si disponible. No prueba disco escribible ni conectividad del iPad. |

Los POST necesitan CSRF de la página previa y su cookie. Registro/login devuelven
429 si exceden el límite. No existe API pública para enumerar jugadores.
Tamaño de petición limitado; SQL parametrizado; autoescape HTML; cookies HttpOnly
y SameSite=Lax; hosts permitidos explícitos y cabeceras contra embebido/inyección.

## Decisiones importantes para Javier y el Arquitecto

1. Python + Flask/Waitress y SQLite local constituyen la base implementada. Revisar
   esta elección antes de ampliar la simulación multijugador; no presupone escala masiva.
2. Entrada web adaptable al iPad, sin Telnet en texto plano. El nombre Vintage Telnet
   no obliga a ese protocolo. Revisar si habrá también clientes terminales.
3. Identidad por usuario/contraseña; no se implementan recuperación, roles de DM,
   administración remota, borrado de cuentas ni invitaciones. Definirlos antes de
   ampliar la audiencia; no improvisar recuperación modificando hashes a mano.
4. Acceso remoto pendiente: decidir red privada/túnel/HTTPS, autenticación de entrada,
   confianza de proxies, registros/invitaciones, protección de fuerza bruta y operación
   de respaldos. No se abre router, túnel ni DNS en esta entrega. HTTP solo para prueba
   explícita en LAN confiable con cuentas de prueba y contraseñas no reutilizadas.
5. Lugar inicial, creación de personaje, selección de especie/clase y reglas de
   presencia/combate desconectado dependen de Jugabilidad/Historiador. No se asigna
   Valdren ni otra ubicación por defecto a todas las cuentas.

Referencias técnicas consultadas: [despliegue Flask](https://flask.palletsprojects.com/en/stable/deploying/),
[Waitress](https://flask.palletsprojects.com/en/stable/deploying/waitress/),
[seguridad web](https://flask.palletsprojects.com/en/stable/web-security/),
[hashes Werkzeug](https://werkzeug.palletsprojects.com/en/stable/utils/).
