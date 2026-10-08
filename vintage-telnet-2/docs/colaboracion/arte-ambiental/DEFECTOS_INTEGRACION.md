# Defectos identificados sin tocar integración

## Miniatura de fragua

`placeArt` en `client/ui-data.js` deriva `valdren-fragua-thumb-v1.webp` desde la ilustración, pero ese archivo no existe. El asset existente se llama `valdren-fragua-anime-v1-thumb.webp`. Clasificación de referencia de miniatura: técnicamente defectuosa. La ilustración completa aprobada existe y se conserva.

Propuesta para Codex principal: asignar `thumbnail` explícito a la entrada `valdren_fragua`, apuntando al archivo actual. No requiere generar ni sustituir la ilustración. No se aplicó parche.

Todas las nuevas entradas propuestas incluyen miniatura explícita para evitar depender de sustituciones de nombre.
