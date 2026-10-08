# Rasgacumbres — corrección anatómica del arte anime

Se generó una ilustración nueva con la herramienta integrada `image_gen.imagegen`; no se usó CLI/API externa ni se modificó el modelo 3D. La versión 1 permanece intacta.

## Canon y decisión

Fuente anatómica autorizada: `/home/jdiaz/proyectos/vintage-telnet-2/vintage-telnet/CREATURES.md`, apartado «Amenaza superior: Rasgacumbres», líneas 751–769. Describe un gran cuadrúpedo de pelaje grueso, patas delanteras muy fuertes, depredador de montaña en terreno escarpado, con marcas profundas de garras y cornisas. El prompt maestro actualizado, `/home/jdiaz/Descargas/Vintage_Telnet_Prompt_Actualizado.pdf`, enumera Rasgacumbres en Hoshai; su extracción local, línea 859, confirma criatura/región sin anatomía adicional. No se imprimieron credenciales de ese documento.

La inspección de `rasgacumbres-anime-v1.webp` mostró un reptil azul con cuernos y placas dorsales, incompatible con esa anatomía. La nueva imagen muestra un animal mamífero de pelaje espeso, cuatro patas, hombros y patas delanteras robustos y garras naturales sobre una cornisa. Color del pelaje, expresión, cola y dibujo facial son interpretación artística, no nuevos hechos canónicos. No se añadieron poderes, armadura ni habilidades.

## Generación e integración

Prompt EXACTO enviado: `review/qa/rasgacumbres-v2/PROMPT.txt`.

Salida real de la herramienta:

`/home/jdiaz/.codex/generated_images/01a11185-c2b0-7893-8626-66b9cec4ca60/exec-8d55282e-17a1-4df9-98e1-2a187d2d6897.png`

Asset final: `client/art/bestiary/rasgacumbres-anime-v2.webp`, 1536×1024, 459936 bytes. Única transformación posterior: conversión de formato/ajuste máximo de tamaño mediante ImageMagick; no se pintó, compuso ni alteró anatomía con scripts.

Comando aplicado:

```sh
magick /home/jdiaz/.codex/generated_images/01a11185-c2b0-7893-8626-66b9cec4ca60/exec-8d55282e-17a1-4df9-98e1-2a187d2d6897.png -resize '1536x1024>' -quality 88 client/art/bestiary/rasgacumbres-anime-v2.webp
```

`content/world.json`, criatura `rasgacumbres`, apunta a `/client/art/bestiary/rasgacumbres-anime-v2.webp`. No se editaron regiones ni referencias 3D en esta tarea.

SHA-256:

- Original preservado v1: `f79059b6196d2150e3cea1bcc7274d4dc50a869254c1ae10931cae01d9499c91`.
- Nuevo v2: `4e2765107f629383a4e47d2bcca82771f1e9be4e9558260447e002a7e2ba83c2`.

## Inspección y comprobación real

Inspección visual de agente, no aprobación humana: silueta cuadrúpeda completa, pelaje grueso sobre cuerpo y extremidades, antebrazos fuertes, garras sin sangre, montaña y pinos. No hay cuernos, placas reptilianas, alas, cadáveres, presas ni ataque al espectador. La línea y el sombreado mantienen una ilustración anime marcada, apta para exploración infantil; el depredador conserva presencia imponente.

`scripts/review-rasgacumbres-snapshot.py` registró/aprobó una cuenta nueva en una base temporal, salió de Khariel y descubrió Rasgacumbres mediante un encuentro real con RNG=0.4. La API entregó el asset v2; no se inyectó bestiario ni se inició combate. La base se destruyó al acabar. El snapshot conserva únicamente la entrada descubierta para centrar la comprobación de lectura; esta selección no fabrica descubrimientos.

Después `scripts/browser-review-bestiary.mjs` abrió la interfaz contra el servidor aislado localhost:8099 con ese snapshot. Chromium móvil 393×750 decodificó el WebP, comprobó miniatura ≤56px, abrió/cerró el modal y verificó ausencia de errores JavaScript y desbordamiento horizontal. Se inspeccionaron ambas capturas: la miniatura identifica pelo/cabeza; el modal permite ver las cuatro patas y garras sin recorte del cuerpo.

Evidencia:

- `review/qa/rasgacumbres-v2/api-state.json`.
- `review/qa/rasgacumbres-v2/browser/bestiary-list.png`.
- `review/qa/rasgacumbres-v2/browser/rasgacumbres-expanded.png`.
- `review/qa/rasgacumbres-v2/browser/report.json`: PASS, una criatura.

Límites: móvil emulado, no dispositivo Android físico; snapshot de API interceptado sólo para mostrar el resultado, sin acciones sobre cuentas reales. No se evaluó ni modificó la miniatura 3D existente.
