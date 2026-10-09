# Defectos identificados sin tocar integración

## Miniatura de fragua

`placeArt` en `client/ui-data.js` deriva `valdren-fragua-thumb-v1.webp` desde la ilustración, pero ese archivo no existe. El asset existente se llama `valdren-fragua-anime-v1-thumb.webp`. Clasificación de referencia de miniatura: técnicamente defectuosa. La ilustración completa aprobada existe y se conserva.

Propuesta para Codex principal: asignar `thumbnail` explícito a la entrada `valdren_fragua`, apuntando al archivo actual. No requiere generar ni sustituir la ilustración. No se aplicó parche.

Todas las nuevas entradas propuestas incluyen miniatura explícita para evitar depender de sustituciones de nombre.

Corrección de revisión: la ampliación de brumak-escalones-anime-v1.webp muestra roca seca y vegetación local. Se retira la clasificación previa de fondo alpino y la propuesta de sustitución basada en esa miniatura. No hay sustitución pendiente por ese motivo. La ruta Vaisgard–Brumak queda revisada sin esa reserva.

## Estado de la polea — hoshai_cajas_camino

La imagen base muestra el objeto antes de hoshai_polea_recogida. Después debe cambiar a hueco vacío con marca de apoyo, sin modificar arquitectura. No existe selector por flags en el cliente auditado; integración propuesta para Codex principal. No usar base después de recogerla como si reflejara el estado actualizado.

## Placa de balanza — estados del almacén

Fondo base contiene placa antes de korven_placa_recogida; pesaje base conserva un soporte vacío antes de korven_placa_devuelta. Posteriores propuestas: hueco con tres marcas en fondo y segunda placa encajada en pesaje. Requieren selector por flags en integración; no modificar motor desde esta entrega.
