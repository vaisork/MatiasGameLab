# Contratos de agentes

Esta carpeta contiene un archivo por función/agente registrado.

## Lectura esperada

Un agente nuevo no necesita leer todos estos archivos. Debe leer:

1. `AGENTS.md`;
2. su propio contrato;
3. únicamente contratos ajenos necesarios para resolver una frontera concreta.

## Metadatos mínimos

Cada contrato debe identificar:

- identificador estable;
- proyecto;
- estado;
- quién asignó la función y fecha registrada;
- ramas autorizadas según las reglas comunes;
- forma de entrega;
- contrato y firma.

Mover un contrato desde `AGENTS.md` a esta carpeta no cambia su autoridad ni permite reescribir su firma.

## Cambios de función

Una función no se autoedita. Cuando Javier cambie un alcance:

- conservar la trazabilidad del alcance anterior;
- actualizar el archivo individual;
- actualizar la fila correspondiente de `AGENTS.md`;
- si el cambio afecta trabajo en curso, actualizar también `RAMAS_ACTIVAS.md`.

Los agentes inactivos pueden conservar su archivo para historial, marcados claramente como INACTIVOS.
