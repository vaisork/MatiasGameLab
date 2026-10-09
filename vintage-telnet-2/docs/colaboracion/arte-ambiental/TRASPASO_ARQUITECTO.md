# Traspaso al arquitecto — arte ambiental

Estado vigente: 8 octubre 2026. Cobertura ambiental del canon auditado completa y revisada por el agente. Integración en el juego pendiente y fuera del alcance autorizado. No hay generación en curso ni trabajo simulado en segundo plano.

183 habitaciones públicas auditadas: 175 vistas nuevas y 8 vistas específicas aprobadas conservadas. Además, 3 variantes de objetos de misión: 178 imágenes nuevas seleccionadas, cada una con PNG, WebP y miniatura. Los derivados y descartes no aumentan el número de escenas. Cinco plantillas privadas de hogar existentes se documentan aparte. Las 16 criaturas/encuentros canónicos ya tienen imagen referenciada existente; no se generó bestiario redundante.

## Dónde está cada cosa

Entrega en Ubuntu: `/home/jdiaz/Escritorio/Vintage Telnet - Arte - Entrega/`.

- `originales/`: 178 PNG seleccionados.
- `webp/`: 178 WebP 1200 × 800, calidad 85, método 4.
- `miniaturas/`: 178 WebP 300 × 200, calidad 80.
- `referencias/`: 13 imágenes aprobadas para comparación; no sustituciones.
- `hojas-contacto/`: comparaciones por lote y seis regiones completas, revisadas.
- `recorridos/`: ocho rutas entre asentamientos completas y revisadas, además de ramales y recorridos locales comprobados en el grafo.
- `Obsidian/`: notas por habitación, región, hogar y ruta. Abrir TODA la entrega como vault para resolver los embeds a `webp/`; entrar a `Obsidian/Indice.md`. No se verificó renderizado dentro de la aplicación.
- `proceso/descartes/`: resultados rechazados, NO integrar. Registros intermedios históricos no sustituyen evaluaciones vigentes.

Repo principal leído: `/home/jdiaz/proyectos/vintage-telnet-2-nuevo`. No copié estos assets ni cambié motor, narración, mecánicas, partidas ni integración allí. No hubo commit, push, GitHub ni despliegue Raspberry.

Mi worktree aislado: `/home/jdiaz/proyectos/vintage-telnet-2-arte`, base detached `ec37879`. Contiene este informe como `TRASPASO_ARTE.md` y scripts locales `auditar_arte.py`, `registrar_lote.py`, `registrar_imagen.py`, `actualizar_entrega.py`, `crear_recorridos.py`. NO volver a ejecutar los dos primeros: pueden restablecer auditoría/estados. `actualizar_entrega.py` regenera derivados documentales pero su estado general conserva texto histórico «incompleta»: consultar el estado final vigente y no usarlo para cerrar misión sin revisión.

## Convención de nombres

La clave es el identificador canónico de habitación, con guiones bajos intactos, sin inventar slug del nombre visible.

- Base: `{id}-anime-v1.png`, `{id}-anime-v1.webp`, `{id}-anime-v1-thumb.webp`.
- Destino propuesto: `client/art/places/{id}-anime-v1.webp` y su miniatura en el mismo directorio.
- Nota: `Obsidian/{id}.md`.
- Variante: `{id}-anime-v1-{estado}.png/.webp` y `{id}-anime-v1-{estado}-thumb.webp`.
- Estados seleccionados: `sin-polea`, `sin-placa`, `placa-devuelta`.
- Recorridos mayores: `{inicio}-{fin}-completo.jpg`; ramales con nombre descriptivo y JSON de ids.
- Lotes: `lote-{numero}-{tema}.jpg`.

Ejemplo: `nhal_raices_altas-anime-v1.webp`. `v1` es la selección revisada; sus correcciones previas son descartes, no variantes de juego. Las imágenes aprobadas antiguas conservan sus nombres originales.

## Cómo trabajé

Crucé mapa, habitaciones, rutas, encargos, canon, referencias en código y assets decodificados. Investigué cada lugar y vecinos, generé con image_gen conectado, inspeccioné, critiqué, corregí, exporté PNG/WebP/miniaturas y comparé contactos y recorridos. Caveman para comunicación concisa, Ponytail para proceso simple y Obsidian Markdown para notas. No instalé modelos enormes ni activé APIs externas de pago.

Anime fantástico serio, no tierno por defecto: Nhal interior y orillas de Lethra más sobrios; almacén viejo cerrado y oscuro; regiones habitadas conservan vida cotidiana. No inventé causas del abandono ni criaturas permanentes para explicar huellas. Las 22 calles/patios antes compartidos tienen vista propia y propuestas narrativas autorizadas en `ANOTACIONES_NARRATIVAS.md`, sin editar narración.

## Qué integrar y límites

`integracion-propuesta.json` mapea las 175 habitaciones nuevas a ilustración/miniatura. `evaluaciones.json` contiene nombre, región, PNG/WebP, hashes, justificación, prompt, crítica y diez puntuaciones. `variantes-evaluadas.json` contiene las 3 variantes, sus flags, rutas, prompts y evaluación. Copiar sólo los archivos seleccionados cuando el responsable integre; añadir entradas por id a `placeIllustrations` en `client/ui-data.js`. El agente no hizo esa modificación.

Las variantes requieren selector por flags: `hoshai_polea_recogida`, `korven_placa_recogida`, `korven_placa_devuelta`. No colocarlas como base estática: falsearían el estado previo. La UI actual muestra vistas fijas y no sincroniza hora, clima o flags; integración propuesta en `VARIANTES_INTEGRACION.md`. Hasta tener selector, la lectura conserva autoridad sobre cambios. Microtrazas de las variantes se leen mejor en texto que en miniaturas.

Las vistas representan cada lugar y no una reconstrucción topográfica exacta de cada ángulo. El mercado aprobado de Vaisgard mantiene relieve exagerado, documentado sin sustituir; las nuevas vistas exteriores usan cuenca baja. Peldaños originales de Brumak son roca seca: se retiró una reserva inicial incorrecta tras ampliarlos. La discrepancia de miniatura antigua de la fragua está documentada en `DEFECTOS_INTEGRACION.md`.

Cuatro prompts del lote 22 interrumpido se conservan como resúmenes, no como instrucciones exactas recuperadas: `prompt_exacto_recuperado:false` en el registro correspondiente. Las generaciones posteriores guardaron instrucciones antes de producir. No convertir esos resúmenes en una promesa de reproducción exacta.

## Verificación y recepción

`VERIFICACION_FINAL.json`: 534 archivos nuevos decodificados, tamaños de WebP/miniaturas y hashes comprobados, ids únicos, propuestas y notas presentes, sin problemas técnicos detectados. Los 13 originales ambientales de la repo coinciden por hash con auditoría inicial. `canon-recontraste-final.json`: 183 habitaciones, sin altas ni cambios en nombre, región, tipo, descripción, examen o salidas. Si el narrador cambia canon después, recontrastar.

Aprobaciones artísticas del agente, NO revisión humana ni prueba de assets dentro del cliente. Ocho rutas mayores y recorridos locales revisados: consultar `REVISION_RECORRIDOS.md`, `lotes.json` y `recorridos/rutas-canonicas.json`. Ver `REVISION_GLOBAL.md` para límites de continuidad y paletas.

Para recibir, leer este informe y `ENTREGA.md`, después `ESTADO.json`, `integracion-propuesta.json`, `evaluaciones.json`, `variantes-evaluadas.json`. Integración y publicación siguen pendientes del responsable del proyecto. La documentación histórica de pausas anteriores está en `proceso/TRASPASO_ARQUITECTO-historico.md`; no es estado vigente.
