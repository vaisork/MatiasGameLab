# Handoffs de Vintage Telnet

Esta carpeta evita usar `HANDOFF.md` raíz como buzón compartido entre ramas y juegos.

## Regla

Cada entrega nueva de Vintage Telnet deja un archivo propio:

`vintage-telnet/handoffs/<identificador-de-tarea>.md`

El nombre debe ser estable y reconocible, preferiblemente relacionado con la rama o tarea.

## Contenido mínimo

- HEAD base;
- agente/implementador responsable;
- objetivo y alcance;
- rama y commit de entrega;
- archivos modificados;
- pruebas realmente ejecutadas y resultado;
- pruebas pendientes;
- dependencias o bloqueos;
- riesgos/conflictos;
- qué debe revisar el siguiente agente;
- estado: preparado / revisado / integrado / superado.

## Después de integrar

El handoff se conserva como historial. `RAMAS_ACTIVAS.md` deja de tratar la rama como activa.

No guardar secretos, credenciales, bases de datos ni datos vivos en estos documentos.
