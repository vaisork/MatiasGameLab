# Ciclo 4: materialización tridimensional del estado conocido

Módulo nuevo `client/world3d.js`: `mountWorld3D(container, options)` y `mountFigure3D(container, options)` devuelven una función dispose. Three local MIT y licencia son la única reutilización del proyecto anterior. No se reutilizan modelos rechazados, motor anterior, prosa anterior ni estado paralelo. La integración de app y degradación corresponde al coordinador.

Mapa: nodos recibidos y rutas aprendidas, posiciones esquemáticas ya calculadas por ui-data, caminos ortogonales `discoveredPaths`, frontera punteada, elevación y materiales regionales, marca dorada del lugar actual, etiquetas DOM seleccionables. Seleccionar nunca llama acciones de viaje. Pan táctil, pinch, rueda, botones de zoom/rotación/centrado. Fit responsive basado en extensión proyectada; etiquetas con prioridad actual/selección/pueblos y ocultación por colisión, más detalle al acercar. Rendering bajo demanda, DPR limitado a 1.5, ResizeObserver y limpieza de geometrías/materiales/contexto al desmontar.

Figuras: cinco especies proporcionadas desde canon: Dravak 70% altura humana, Marevyn 110%, Felaryn cola/orejas felinas/apoyo digitígrado, Vesperi ojos/orejas especializados y brazos largos; sin alas, branquias, cola de pez o clichés dracónicos. Equipo sólo si el objeto equipado se resuelve en inventory. Fauna distingue arácnido de ocho patas, crustáceo con pinza mayor, anfibio dorsal largo, Espinajo con espinas, caparazón de placas, cuadrúpedo con musgo, Uñapiedra bajo, Cornalomo voluminoso y piel irregular Rasgacorteza. Son miniaturas procedurales, no arte anime final ni fauna animada.

Seis pueblos explícitos: Valdren surcos/acequia/banco/carro; Khariel dos niveles/rampa; Brumak puertas bajas/roca; Narevia agua/pasarela/barca/juncos; Velmora árboles/raíces/claros; Vaisgard empedrado/patio/desagüe. Cruce inundable `edran_puente_juncos` y refugios conocidos tienen forma de puente/apoyos/cubierta. El módulo no descubre estos lugares por su cuenta.

## Inspección y correcciones

Chromium real en servidor estático aislado 8107, snapshot creado por API con base temporal; desktop 1100px y móvil 393px. Capturas inspeccionadas en `review/depth-cycle4/`. Primera crítica: etiquetas masivas tapaban el terreno y había demasiado aire en encuadre. Se implementó colisión/prioridades, fit por aspect y caminos existentes; se volvió a capturar y comparar. Resultado final: geología visible, contraste de agua/bosque/piedra/cultivo, cuatro etiquetas principales en overview de esta ruta, controles usables y figuras completas. Inspección independiente del agente regional confirmó mapa de 81 nodos en 320px, interacción y fallback 2D del cliente.

Prueba `scripts/depth-cycle4-world3d.mjs`: carga mapa, zoom/rotación, render de cinco especies, diez criaturas y ocho hitos, móvil y desmontaje. Sin errores JS; cero canvas después de dispose. `node --check client/world3d.js` pasa. Evidencia JSON `review/depth-cycle4/report.json`.

## Autocrítica y límites

Los modelos son deliberadamente esquemáticos y no alcanzan el detalle del arte anime 2D conservado. Algunas especies de fauna siguen compartiendo base cuadrúpeda; espinas/caparazón/musgo/longitud/altura sí se ven distintos, pero todavía faltan articulación, gestos y estudio de anatomía para representación final más rica. En overview grande, el terreno se lee como memoria de rutas con señales de región; la arquitectura requiere zoom. Las posiciones son el esquema de conocimiento existente, no geografía precisa. No se afirma rendimiento en un móvil físico: el navegador emula ancho táctil. El módulo lanza error si WebGL no se puede crear; el cliente conserva representación 2D. Hora/clima cambian luz y fondo, sin lluvia simulada ni efectos que obstaculicen la lectura.

## Revisión visual final y rejuego comparativo

La crítica adicional del coordinador señaló modelos capsulados y diferencia con anime. Se corrigieron material toon, contorno fino, ojos con iris/esclerótica/luz, nariz/boca/cabello y piel humana cálida Dravak con zonas pétreas limitadas. Se inspeccionaron los retratos reales Dravak y Marevyn antes de ajustar; Marevyn mantiene la piel turquesa del retrato y la fisonomía humanoide, sin branquias. Una nueva captura mostró que Marevyn alto se recortaba arriba: la cámara ahora centra el bounding box de cada figura. Las capturas finales de especies y seis pueblos fueron vueltas a renderizar e inspeccionar, no se reutilizó evidencia anterior como si fuera la nueva. El salto visual mejora rostro y silueta sin igualar una figura anime terminada.

Se añadió evento `visual3dfailed` y callback onError para pérdida de contexto gráfica. El coordinador integra la vuelta a 2D; el módulo libera recursos y contexto al desmontar, con listener removido antes de provocar la liberación normal. La prueba de selección verifica una llamada onSelect y cuenta exacta de botones derivados de nodos conocidos más cuatro controles, sin nodos añadidos.
