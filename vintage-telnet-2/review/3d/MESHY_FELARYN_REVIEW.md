# Felaryn Meshy — revisión de integración

## Contrato implementado

`mountFigure3D` carga `/client/models/species/felaryn.glb` sólo para la figura de especie Felaryn. El mapa conserva su avatar procedural ligero. GLTFLoader y BufferGeometryUtils proceden de la misma dependencia Three r160 local, cubierta por LICENSE-three.txt. No se reutilizó arquitectura anterior.

La figura procedural permanece durante la carga y ante error. El modelo recibido conserva sus materiales y texturas; no recibe el contorno ni material toon de las miniaturas procedurales. Se normaliza por altura y bbox, conserva controles de giro y ajusta el encuadre al ancho móvil. Al cargar este modelo no se superpone equipo procedural sobre su vestimenta fija. La UI lo identifica como representación de especie y aclara que su mochila y ropa no indican inventario. `dispose` libera geometrías, materiales y texturas, cierra ImageBitmap cuando procede y libera recursos de una carga que termine después del cierre. El loader revoca sus URL blob después de decodificar imágenes. El archivo no contiene clips: no se ofrece animación.

## Revisión real del original

Arnés aislado en 8107: el archivo original se interceptó desde su ubicación de Escritorio, sin copiarlo al producto. Chromium renderizó frente y espalda a 320, 393 y 1100 píxeles. Se inspeccionaron las capturas móviles: figura completa, orejas, cola y pies visibles, texturas y ropa reconocibles. Giro y cierre funcionan, cero canvas después de dispose, y una carga tardía no vuelve a montar la vista. Sin errores JS. Evidencias: `meshy-felaryn-original/report.json` y seis capturas. Prueba adicional de archivo ausente: queda un canvas procedural; después del cierre, cero.

Canon maestro, página 13, LAS ESPECIES JUGABLES / Felaryn: humanoides felinos aproximadamente de altura humana; piernas potentes, pies digitígrados, cola felina, orejas felinas sin orejas humanas, equilibrio y salto. El modelo muestra esos rasgos externos. El canon no exige rostro humano para Felaryn; la cautela inicial sobre hocico y patas se corrigió tras leer la sección exacta.

## Límites y revisión pendiente

El modelo trae camisa, pantalón, mochila y correas incorporados. Son vestimenta de la representación, no evidencia de objetos poseídos por el personaje. No se validó articulación ni animación: no hay skins ni clips. La textura y silueta visibles son aceptables como representación de especie; la cifra alta de polígonos del original impide adoptar ese archivo directamente para móvil. La versión optimizada se revisó después por separado: se conserva la silueta y el detalle reconocible de cara, orejas, cola, pies y vestimenta; los pliegues muestran simplificación leve. A escala móvil la comparación resulta favorable.

La integración usa GLB estándar, sin decoder Draco/Meshopt/KTX2. CSP y allowlist los mantiene root: imágenes embebidas requieren blob en img-src y connect-src. El fallo de red no bloquea juego ni muestra una figura vacía.

## Rejugar con la versión optimizada

Archivo de producto: 1.732.520 bytes, 32.225 vértices y 40.746 triángulos; el original permanece intacto fuera del producto. La procedencia, métricas, hash y comandos de optimización están en `MESHY_FELARYN_OPTIMIZATION.json`, mantenido por root.

`meshy-felaryn-optimized/report.json`: Chromium a 320/393/1100, frente y espalda, giro, cierre, carga tardía y error 404 con fallback; sin errores JS. Se inspeccionaron las capturas móviles frontal y posterior junto a las del original.

`meshy-felaryn-backend/report.json`: la misma prueba sobre el backend aislado 8099 reiniciado con CSP y allowlist actuales. El GLB se descarga por la ruta de producto, sin interceptar el archivo exitoso; la prueba de fallback sí fuerza un 404.

`meshy-felaryn-ui/report.json`: tres cuentas temporales Felaryn creadas y aprobadas, vista Personaje → ilustración → representación 3D. A 320/393/1100 carga el modelo, muestra etiqueta y aviso de equipo, gira y libera canvas al cerrar. Sin errores de JavaScript ni violaciones CSP. Se inspeccionó `320-species.png`: figura completa, controles legibles y aviso visible.

Checks de sintaxis para app.js, world3d.js, model-assets.js y arnés pasan; QA passive conserva sus cuatro casos. La validación demuestra carga, apariencia y limpieza DOM; no cuantifica FPS, batería ni ausencia total de fugas del driver. El original de más de un millón de triángulos no se descarga en la aplicación.
