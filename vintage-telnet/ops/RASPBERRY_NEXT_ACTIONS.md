# Raspberry — siguiente ejecución mínima

Objetivo: que el Operador Raspberry/Cloud **no programe**. El código se prepara y prueba en GitHub; Raspberry solo valida hardware/servicio real.

## Comando de preflight

Desde el checkout desplegado:

```bash
cd /opt/vintage-telnet/current/vintage-telnet
.venv/bin/python ops/raspberry_preflight.py --tests
```

Opcionalmente, exigir un SHA:

```bash
.venv/bin/python ops/raspberry_preflight.py --tests --expected-head <SHA>
```

El script es **solo lectura**. No hace deploy, restart, sudo, cambios de configuración ni toca SQLite.

Comprueba:
- HEAD instalado;
- `vintage-telnet.service`;
- 8080 solo en loopback;
- `/healthz` local y por Funnel;
- manifest Android de Vintage Telnet;
- icono WebP y MIME correcto;
- estado/modelos Ollama como información;
- suite completa cuando se pasa `--tests`.

## Trabajo que debe quedar fuera de Raspberry

Antes de pedir una sesión de Cloud/Raspberry:
1. código mergeado en `main`;
2. suite verde en GitHub Actions;
3. migraciones/esquema cubiertos por pruebas;
4. frontend revisado;
5. SHA exacto elegido para deploy.

## Trabajo mínimo que sí requiere Raspberry

1. backup previo si el deploy cambia servidor/SQLite;
2. actualizar al SHA autorizado;
3. ejecutar el preflight;
4. confirmar login/registro/aprobación/especie/juego en navegador real cuando aplique;
5. probar funciones que dependan del hardware/servicio local (Ollama, systemd, Funnel);
6. registrar resultado, sin programar fixes allí.

Si algo falla, devolver el error exacto a GitHub. El arreglo se desarrolla fuera de la Raspberry y después se repite la validación.


## Probe seguro de migración de inventario

Antes de desplegar un HEAD con esquema v6, validar la base viva **sin modificarla**:

```bash
cd /opt/vintage-telnet/current/vintage-telnet
.venv/bin/python ops/inventory_migration_probe.py /var/lib/vintage-telnet/vintage-telnet.sqlite3
```

El script abre el origen en modo read-only, usa `sqlite3.backup()` hacia un temporal y ejecuta la migración solamente sobre esa copia. Comprueba versión v6, IDs/números/usernames preservados, tabla de inventario, columnas de equipo, `foreign_key_check` y `quick_check`.

Si la ruta real de SQLite difiere, usar la ruta de `VT_DB_PATH`/configuración vigente. No adivinar ni mover la base.
