# Vintage Telnet — servidor, entrega 0.1.0

La Raspberry Pi ejecutará el servidor autoritativo y conservará el estado vivo.
GitHub conserva código y documentación. Senku permanece independiente.

Esta entrega permite registrar una cuenta, iniciar/cerrar sesión, recuperar un ID
estable y un número de jugador y consultar accesos desde la máquina. Tras entrar
se muestra que el mundo está en construcción. La página necesita el servidor:
no guarda partidas ni identidad autoritativa en el dispositivo y no funciona como
juego HTML autónomo. No implementa el protocolo Telnet TCP.

- Arquitectura y decisiones para revisión: [ARCHITECTURE.md](ARCHITECTURE.md).
- Instalación y operación física: [ops/RASPBERRY_HANDOFF.md](ops/RASPBERRY_HANDOFF.md).
- Respuesta del operador: [ops/RASPBERRY_REPORT.md](ops/RASPBERRY_REPORT.md).
- Validación de esta entrega: [VALIDATION.md](VALIDATION.md).
- Reglas y contenido: [GAMEPLAY.md](GAMEPLAY.md), [WORLD.md](WORLD.md).

## Desarrollo local

Python 3.11 o superior. Desde `vintage-telnet/`:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
export VT_DATA_DIR="$(pwd)/data"
export VT_SECRET_KEY="$(.venv/bin/python -c 'import secrets; print(secrets.token_hex(32))')"
export VT_ALLOW_HTTP=1
.venv/bin/python -m server
```

Abrir `http://127.0.0.1:8080`; detener con Ctrl+C. En Windows usar
`.venv\Scripts\python.exe` y variables `$env:VT_...` en PowerShell.
Conservar la clave en configuración privada entre reinicios si se desea mantener
sesiones: cambiarla invalida cookies, pero nunca borra jugadores.

No subir bases, contraseñas, cookies, claves ni respaldos a Git. No servir el
directorio del repositorio mediante un servidor estático.
