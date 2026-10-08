# Integración de arte ambiental, tanda b — 2026-10-08

Se integran 16 vistas nuevas con sus miniaturas, desde `Vintage Telnet - Arte - Entrega`. Según `ESTADO.json`, la entrega tiene 108 vistas nuevas aprobadas por el agente, sin revisión humana; las 92 restantes ya estaban integradas y son idénticas byte a byte.

- IDs: valdren_cobertizo, valdren_comedor, valdren_casa_semillas, valdren_cuidado, edran_canal_entrada, edran_canal_bifurcacion, edran_canal_compuerta, edran_canal_herramientas, edran_canal_refugio, edran_canal_repisa, veyra_archivo_cargas, nhal_umbral_elin, nhal_senda_recipiente, nhal_taller_cortezas, nhal_secadero_sombra, nhal_cocina_raices.
- Se mapean en `client/ui-data.js` con un bloque `Object.assign(placeIllustrations, …)` y miniatura explícita. Ahora hay 115 entradas.
- Verificación:
  - Los 32 archivos copiados coinciden por SHA256 con la entrega y con `sha256_webp` de `evaluaciones.json`.
  - Las ilustraciones miden 1200×800 y las miniaturas 300×200, y todas se decodifican.
  - Los 210 archivos que ya había en `client/art/places` no cambian.
  - `placeArt` resuelve las 16 entradas y los dos archivos de cada una existen.
- Hoja de contacto revisada por Claude: los interiores del canal, Valdren y los talleres de Nhal coinciden con sus descripciones.
- No se copian `proceso/descartes/` ni salidas del generador no aprobadas.
- `docs/colaboracion/arte-ambiental/` se actualiza con las versiones vigentes de la entrega.
- El generador sigue activo (67 salas pendientes): las nuevas vistas se integrarán en otra tanda con este mismo procedimiento.
