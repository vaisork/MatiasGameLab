# Vintage Telnet 2 — arte ambiental disponible

Cobertura preparada y revisada: **183 habitaciones públicas**, con **175 vistas nuevas + 8 aprobadas conservadas**, además de **3 variantes de estado**. Total seleccionado nuevo: **178 imágenes**, con PNG, WebP y miniaturas. Integración en el juego pendiente; no hubo modificación de motor, narración, partidas, publicación ni despliegue.

Para verlas, abrir `VER_ESCENARIOS.html` en navegador local o las seis hojas `hojas-contacto/{region}-cobertura-actual.jpg`. Las secuencias de viaje están en `recorridos/`; ocho rutas entre asentamientos tienen cobertura y revisión completa. Las 22 calles/patios originalmente compartidos tienen vistas propias y anotaciones autorizadas.

Leer primero `TRASPASO_ARQUITECTO.md`: explica aislamiento, convenciones, herramientas, canon, selección, límites y recepción. El worktree está en `/home/jdiaz/proyectos/vintage-telnet-2-arte`; el proyecto principal leído es `/home/jdiaz/proyectos/vintage-telnet-2-nuevo`. Assets sólo en esta entrega, no copiados a la repo principal.

## Archivos de integración

- `evaluaciones.json`: 175 escenas base, con id, nombre, región, rutas, prompt, crítica, puntuaciones y hashes.
- `integracion-propuesta.json`: correspondencia por id para vistas/miniaturas; no aplicada.
- `variantes-evaluadas.json`: tres variantes, flags y rutas. Requieren selector; ver `VARIANTES_INTEGRACION.md`.
- `originales/`: PNG seleccionados; `webp/`: 1200 × 800, calidad 85; `miniaturas/`: 300 × 200, calidad 80.
- `inventario-escenarios.csv/json`, `canon-snapshot.json`, `canon-recontraste-final.json`: auditoría y canon vigente contrastado.
- `VERIFICACION_FINAL.json`: 534 archivos decodificados y comprobados; cero problemas técnicos detectados. Los 13 originales ambientales permanecen iguales por hash en la repo principal.
- `REVISION_RECORRIDOS.md`, `REVISION_GLOBAL.md`, `lotes.json`: pruebas visuales, coherencia y límites.
- `ANOTACIONES_NARRATIVAS.md`, `DIRECCION_VISUAL.md`, `DEFECTOS_INTEGRACION.md`: notas para narrador/arquitecto, sin cambios al juego.
- `bestiario-cobertura-verificada.json`: 16 criaturas/encuentros con imagen existente; no faltantes por referencia.
- `Obsidian/`: notas enlazadas; abrir toda la entrega como vault para resolver embeds de `webp/`. Renderizado en Obsidian no probado.

No copiar `proceso/descartes/` ni salidas intermedias. Sólo las selecciones en evaluaciones y variantes están propuestas. Las aprobaciones son del agente, no revisión humana. La lectura mantiene autoridad sobre hora, clima y consecuencias; vistas fijas no sincronizadas. Cuatro prompts del lote 22 interrumpido son resúmenes declarados, no reproducción exacta.

No hay escenarios públicos sin vista específica en el canon contrastado. No hay generación en curso ni trabajo simulado después de esta sesión. Integración, prueba en cliente y revisión humana quedan para el responsable del proyecto, fuera del alcance de este agente.
