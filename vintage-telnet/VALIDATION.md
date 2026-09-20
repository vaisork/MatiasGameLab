# Validación de la entrega 0.1.0

Fecha: 2026-09-20. Entorno real de estas pruebas: **Windows AMD64 local**, Python
3.12.14, SQLite 3.53.1. No Raspberry Pi, Linux/systemd, iPad ni acceso remoto.

Desde `vintage-telnet/`:

```text
.venv\Scripts\python.exe -m unittest discover -s tests -v
Ran 9 tests in 12.727s
OK

.venv\Scripts\python.exe -m pip check
No broken requirements found.
```

Cobertura comprobada:

- Registro con hash scrypt; UUID/número estables al recrear aplicación y cambiar
  de cliente; creación intacta y último acceso actualizado solo tras autenticación.
- Duplicados normalizados y contraseña incorrecta sin eventos exitosos adicionales.
- CSRF, logout con revocación incluso al reproducir la cookie anterior, caducidad.
- Validación, escape HTML, restricción de Host y ausencia de rutas que sirvan
  documentos del repositorio/base; health sin refrescar cookies de sesión.
- Límite de autenticación persistente al reiniciar y liberación al vencer ventana.
- Cuatro registros simultáneos del mismo usuario: una sola cuenta, sesión y evento.
- Herramienta local de inspección sin hashes, integridad y backup recuperable;
  negativa a sobrescribir otro backup.
- Configuración incompleta/ruta relativa/esquema desconocido rechazados.
- Proceso **Waitress HTTP real** en loopback: cliente con cookie registra, ve
  `Jugador #0001`, proceso termina; nuevo proceso y cliente hacen login y recuperan
  el mismo UUID desde la base conservada. Prueba usa directorio temporal propio.

La primera corrida detectó que Flask renovaba cookies en health; se desactivó la
renovación automática y la suite completa pasó después del ajuste.

`git fetch origin` confirmó al terminar la implementación que `origin/main`
seguía en `bb2fef58ee1607d216e3bbc77b3d623489d24e9b`. La entrega agrega el registro
propio en `AGENTS.md` y archivos bajo `vintage-telnet/`. No modifica Senku,
documentación narrativa/jugabilidad existente ni funciones/firmas ajenas.

## Pendiente para poder declarar operación real

- Publicación/integración por el integrador y comunicación del SHA instalable.
- Instalación de dependencias sobre arquitectura/SO reales de Raspberry.
- Arranque, parada y reinicio con systemd, permisos y disco real.
- Registro/login desde iPad/teléfono en LAN y recuperación tras desconexión.
- Respaldo y restauración aislada en Raspberry; reinicio físico cuando Javier lo acuerde.
- Revisión del Arquitecto para futura exposición remota y evolución del mundo.

Seguir `ops/RASPBERRY_HANDOFF.md`; devolver `ops/RASPBERRY_REPORT.md` completado.
