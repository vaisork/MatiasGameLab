# Vintage Telnet 2 — arte ambiental

Estado: **producción en curso, misión incompleta**. No se ha modificado ni desplegado el juego.

## Ubicaciones

- Proyecto leído: `/home/jdiaz/proyectos/vintage-telnet-2-nuevo`.
- Worktree aislado: `/home/jdiaz/proyectos/vintage-telnet-2-arte`, snapshot `ec37879`.
- Entrega: esta carpeta.
- Generador: herramienta image_gen integrada, comprobada mediante generación real. No se activó API ni se descargaron modelos.

## Integración para el Codex principal

`evaluaciones.json` contiene ids, nombres, regiones, archivos, rutas propuestas, crítica y puntuaciones. `prompts.json` guarda instrucciones de generación y corrección. Copiar sólo los WebP aprobados a las rutas allí indicadas y las miniaturas correspondientes. Añadir una entrada explícita por id a `placeIllustrations` en `client/ui-data.js`, con `illustration` y `thumbnail`. Las rutas deben empezar por `/client/art/places/` al servirlas. Estas entradas evitarán el fallback regional genérico. No sustituir las seis vistas de pueblo aprobadas.

Las imágenes no incluyen estado temporal jugable. `placeArt` resuelve una única vista fija; la lectura describe hora, clima y consecuencias. Las variantes se proponen en `DIRECCION_VISUAL.md`, sin parche de motor.

## Auditoría y evidencia

- 183 habitaciones públicas canónicas, cruzadas con salidas reales y referencias del cliente.
- Cinco plantillas privadas de hogar con arte existente, documentadas aparte. No se exportaron partidas ni ids privados.
- Estado inicial: 153 sin imagen, 22 con imagen regional compartida, 8 con vista específica existente.
- `inventario-escenarios.csv` y JSON: cola ordenada, canon, vecinos, referencia actual y ruta propuesta.
- `assets-audit.json`: 57 assets existentes decodificados, tamaños y SHA-256.
- `canon-snapshot.json`: geografía y descripciones públicas usadas para producir; volver a contrastar si el Codex narrativo cambia el canon después del snapshot.
- `ANOTACIONES_NARRATIVAS.md`: propuestas autorizadas para diferenciar 22 calles o plazas; no modifica narración.
- `Obsidian/`: notas enlazadas por id, región, hogar y recorrido. Abrir la carpeta completa de entrega como vault y entrar a `Obsidian/Indice`; así también funcionan los embeds de WebP. No se verificó en la aplicación Obsidian.
- `hojas-contacto/`: referencias por región y comparación de lotes.
- `recorridos/`: ocho rutas canónicas verificadas en grafo; cobertura y revisión actual de cada una en rutas-canonicas.json. Las secuencias cortas se revisan por separado.

## Lote 1

Cuatro vistas específicas de Vaisgard: plaza de las rutas, calle de almacenes, calle de toldos y patio del agua. Cada una tiene PNG original de generación, WebP 1200×800 y miniatura. Evaluación artística del agente; no se atribuye aprobación humana.

Se compararon hoja de contacto y tres secuencias reales: almacenes–mercado–plaza; plaza–mercado–agua; almacenes–mercado–toldos. Piedra, madera, telas y luz comparten lenguaje; cambia circulación, actividad y escala. El mercado aprobado conserva relieve más intenso al fondo: se registró la discrepancia sin sustituirlo. Nuevas vistas no propagan montañas inmediatas a Veyra.

La plaza necesitó corrección: primera versión demasiado comercial y con sierra demasiado cercana. Su PNG entregado es la versión corregida. No se incluye el descarte como imagen aprobada.

## Pendientes

Cobertura restante de calles, entradas, caminos, regiones, interiores y lugares especiales. No se inicia bestiario mientras exista cobertura ambiental prioritaria resoluble. Las rutas largas no están aprobadas visualmente sólo por tener el grafo documentado.

No hay trabajo simulado en segundo plano. Los registros describen únicamente archivos realmente producidos y revisados.

## Estado actualizado

Consultar `ESTADO.json` para conteos actuales, y `DEFECTOS_INTEGRACION.md` para referencias rotas detectadas. La cola incluye entradas, salidas, cruces y habitaciones de encargos tras cruzar los catálogos de misiones.

## Cobertura actual automatizada

113 vistas nuevas revisadas por el agente; 62 habitaciones pendientes de vista específica. Las 22 calles y patios con fondo compartido inicial ya tienen arte propio y anotaciones narrativas. Misión incompleta.

Recorridos completos: consultar `recorridos/rutas-canonicas.json` y `REVISION_RECORRIDOS.md`; los demás continúan pendientes. Sólo los archivos listados en `evaluaciones.json` están propuestos para integrar. Los descartes no se integran.
