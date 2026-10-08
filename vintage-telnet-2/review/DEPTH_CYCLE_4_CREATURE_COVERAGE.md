# Corrección posterior: cobertura semántica del bestiario 3D

El coordinador detectó un defecto real del módulo inicial: Rasgacumbres y Quebrarrocas no tenían rama ni paleta propia y caían en el mismo cuadrúpedo gris. Mi prueba inicial de diez criaturas no cubría ese hueco. Se corrige la implementación y la prueba, sin revertir brújula ni avatar propio añadidos por el coordinador.

La prueba ahora obtiene todos los IDs de `content/world.json`, compara exactamente el catálogo de 16 con `supportedCreatureIds`, renderiza 15 fauna y el combatiente humano y guarda las 16 capturas. Los IDs no soportados producen una excepción antes de crear canvas para permitir fallback, en lugar de una criatura genérica silenciosa. Esto no agrega entradas al bestiario de jugadores: la integración sigue montando únicamente entradas descubiertas.

`node scripts/depth-cycle4-world3d.mjs` en servidor actual 8099: PASS, sin errores JS, catálogo16 coincidente, fauna15, selección única y cero canvas tras dispose. Las 16 capturas nuevas fueron abiertas con view_image; no se deduce calidad visual por nombre de archivo. Evidencia: `review/depth-cycle4/report.json` y PNG por ID.

| ID | Forma examinada | Relación con entrada canónica |
| --- | --- | --- |
| mordelinde | Bajo alargado, hocico, cola corta | Aparta semillas y busca salida; pelo todavía esquemático |
| espinajo_rastrojo | Compacto con espinas | Lomo de espinas visible |
| cornalomo | Masa alta, apoyo ancho | Peso/huellas/lomo por encima de hierba |
| saltacresta | Rodillas posteriores dobladas y cuerpo en salto | Desnivel y saltos; postura distinta del cuadrúpedo de base |
| unapiedra | Cuerpo muy bajo, apoyos abiertos, uñas delanteras | Pegado a pendiente y agarre en roca |
| rasgacumbres | Cuadrúpedo de hombros elevados, delanteras robustas, garras, mechones | Depredador de montaña con pelaje grueso y patas delanteras fuertes |
| quebrarrocas | Bajo muy ancho, antebrazos pala y placas acorazadas | Excavador que empuja bloques; figura animal, no gólem |
| cascapedernal | Caparazón oscuro con seis patas articuladas | Artrópodo de fisuras/piedra cálida |
| colagrieta | Alargado con cola gruesa de apoyo | Reptil de fisuras |
| pinzajunco | Desplazamiento lateral, pinzas de tamaño desigual | Crustáceo de raíces/juncos |
| saltalodo | Anfibio plano, manchas dorsales, bolsa de cuello | Piel moteada y llamada inflando bolsa |
| dorsalodo | Largo pesado, espalda rugosa | Depredador anfibio entre barro/vegetación |
| rondamusgo | Cuatro patas cortas, musgo/semillas sobre el cuerpo | Fauna que busca hongos/frutos; pelo aún poco desarrollado |
| hilaria_niebla | Ocho patas y abdomen opaco | Arácnido de red baja |
| rasgacorteza | Masa alta de piel irregular | Camuflaje de corteza, tamaño y territorio |
| forajido_camino | Humano vestido | Combatiente humano, no criatura añadida al bestiario |

Autocrítica: comparar nombres y comprobar render no basta. Por eso se inspeccionaron las imágenes y se corrigieron además seis patas de Cascapedernal, uñas de Uñapiedra, manchas de Saltalodo y postura posterior de Saltacresta. Algunas miniaturas mantienen cuerpos elipsoidales y extremidades de primitivas compartidas; hay rasgos diferenciados, pero no se afirma una calidad anatómica final de quince modelos de producción ni equivalencia con anime.

Coherencia pendiente del arte 2D: `CREATURES.md:751`, «Amenaza superior: Rasgacumbres», fija cuadrúpedo de pelaje grueso/patas delanteras fuertes. El retrato anime anterior inspeccionado muestra piel reptiliana azul y placas/cuernos, sin pelaje visible. El modelo nuevo conserva referencia cromática pero sigue el pelaje del canon, no reproduce esos rasgos incompatibles. El coordinador recibió esta discrepancia para corregir también el retrato. Quebrarrocas anime conserva cuerpo animal y placas coherentes con la bestia acorazada, sin contradicción equivalente detectada.
