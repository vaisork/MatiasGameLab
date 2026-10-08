# Integración de entregas — piloto MUD clásico

Base auditada: main e320b77; main incorporó después el estándar editorial 81220ff.

## Entregas incorporadas

- Otro Codex: 47 vistas ambientales WebP y sus 47 miniaturas. Se conserva su correspondencia con IDs y nombres existentes y su documentación en `docs/colaboracion/arte-ambiental/`. Se revisaron las hojas de las seis regiones; no se incorporan originales PNG ni descartes. El arte representa el lugar, no sustituye la hora, presencia o clima autorizados por el servidor.
- Claude: entrega original preservada en `docs/colaboracion/claude-narrativa/estandar_mud/`. Se adaptan cuatro resúmenes y el concepto de lectura breve al regresar; se añaden dos resúmenes canónicos para completar el piloto de seis salas. No se aplica su parche automáticamente: la descripción permanente, pistas y salidas se conservan intactas. No se introduce un motivo nuevo para la piedra del banco ni capas que puedan desplazar peligros.
- Referencias editoriales e investigación histórica de mecánicas incorporadas como documentación. Sus ejemplos numéricos no alteran el combate actual.

## Comportamiento resultante

Primera visita: descripción completa. Regreso: resumen breve cuando está disponible. Mirar: descripción completa y deliberada, visible aunque la escena ya estuviera registrada. Observar sigue mostrando condiciones, presencias y pistas. Una descripción condicionada o cambiada por ausencia de criatura invalida un resumen obsoleto.

Se elimina la repetición de ubicación en el cuerpo de lectura; el encabezado y el historial conservan esa información. Se corrige `placeArt`: la miniatura explícita tiene prioridad sobre el nombre derivado. Esto evita rutas inexistentes para las vistas nuevas y la fragua.

Ejemplo, plaza: la descripción completa de 42 palabras conserva fragua al norte, huertos al este, pozo al sur y cobertizo al oeste. El retorno usa «La plaza de Valdren, con su banco largo partido por una piedra.» Mirar recupera el texto completo. Las acciones y la brújula siguen procediendo del servidor.

## Validación propia

- 45 pruebas Python: piloto, narrativa, resultados, catálogo real, posvictoria y mundo nocturno.
- Cliente: sintaxis; contratos de diario (22), actualización pasiva (4 casos) e impresión progresiva (34).
- Chrome real con base temporal y jugadores de prueba: 320, 393 y 1440 px. Primera visita, regreso, mirar, ausencia de repetición pasiva, imagen nueva a 1200 px y ausencia de desbordamiento/errores de ejecución. Movimiento reducido para aislar contenido y distribución; no es una evaluación humana de velocidad de lectura.
- Recorrido real en memoria: 30 movimientos, 42 instantáneas; pistas, arreglo compartido del granero, conversación, combate y victoria, regreso, noche, lluvia y viento. Comparación contra la base: descripciones completas, acciones, salidas, combate y capas secundarias idénticos; estado mecánico final y mundo compartido idénticos. Sólo difieren los eventos de presentación previstos.
- Lectura de navegación: 2491 → 2268 palabras, reducción 8,95 %. Ocho bases de regreso abreviadas en la ruta. Esta cifra corresponde al piloto real; no se reutiliza la reducción del parche original de Claude.
- Revisión independiente sin ediciones: seis resúmenes, prioridad del peligro y 54 correspondencias de arte/miniaturas válidas.

La prueba de impresión se actualizó porque verificaba la antigua ubicación duplicada. El primer intento de navegador falló por un nombre de botón incorrecto en la prueba; se corrigió al nombre canónico. El recorrido comparó primero también los eventos de presentación dentro del estado; la comparación final separa éstos de los datos mecánicos.

No se modifican partidas, contraseñas, rutas geográficas, cifras de combate ni servicios. No se despliega en Raspberry. El trabajo anterior sin commit en la carpeta original de Ubuntu permanece conservado; esta integración se prepara en un worktree aislado para evitar mezclar cambios no revisados.

Evidencia: `metrics.json`, `browser.json`, seis capturas, `journey.py`, `baseline.json`, `candidate.json` y `browser.mjs`. Las bases de prueba se destruyen al finalizar.
