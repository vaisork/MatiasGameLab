# Director de Arte — Vintage Telnet — Estado inicial

**Fecha:** 2026-09-22  
**HEAD base de `main`:** `a5f47e1ca3ee98bd1babf906fc70a246c8081fc7`  
**Rama:** `art-director/vintage-initial-audit`  
**PR de definición del rol consultada:** #29 — `arch/vintage-art-director` — abierta, no fusionada al momento de esta revisión.\n**Cambio concurrente revisado:** durante esta auditoría `main` avanzó a `a7b20511aeb39f4f54d164e4991396fdf7012c8f`; el cambio únicamente releva temporalmente a Arte HTML y no modifica el canon de especies. La rama conserva trazabilidad de su HEAD base original.

## Firma

**Firma: Director de Arte — Vintage Telnet — función leída, comprendida y aceptada — 2026-09-22.**

No se duplica en esta rama la definición del rol que ya existe en la PR #29. Este archivo registra únicamente la activación del agente y su primera revisión de canon.

## Fuentes leídas

- `AGENTS.md` completo desde el HEAD base y el delta posterior de `main` en `a7b20511aeb39f4f54d164e4991396fdf7012c8f`.
- `vintage-telnet/ART_WORLD_GUIDE.md`.
- `vintage-telnet/SPECIES.md`.
- `vintage-telnet/CONFIRMED_IDEAS.md`.
- `vintage-telnet/ART_DIRECTOR.md` desde la rama de la PR #29.

## Comprensión canónica de las cinco especies

### Humanos

Son la referencia corporal generalista: proporciones humanas normales, anatomía humana, sin adaptación física extraordinaria obligatoria.

**Estado para hoja anatómica:** suficiente.

### Felaryn

Humanoides propios con pelo visible, orejas claramente felinas y cola felina funcional. Su cuerpo debe comunicar agilidad, impulso, salto y equilibrio, sin convertirse en un humano al que solo se añadieron orejas ni en una caricatura animal.

**Estado para hoja anatómica:** requiere una definición adicional antes de fijar una referencia anatómica estable.

**CANON VISUAL INSUFICIENTE — requiere Historiador:** precisar el alcance de “pelo visible” y la morfología corporal que debe acompañar a orejas/cola, especialmente piernas/pies y rasgos faciales. La hoja anatómica no debe decidir por cuenta propia si son plantígrados o digitígrados, si poseen pelaje corporal extenso, hocico u otros rasgos felinos no canonizados.

### Dravak

Adultos de escala menor que un humano y constitución compacta, con zonas corporales endurecidas de aspecto mineral o pétreo. Pueden existir vetas/fisuras volcánicas sutiles, pero no lava expuesta. Deben comunicar dureza y estabilidad sin parecer niños, enanos clásicos, gnomos ni humanoides dracónicos.

**Estado para hoja anatómica:** requiere una definición adicional para fijar una referencia estable y repetible.

**CANON VISUAL INSUFICIENTE — requiere Historiador:** definir un rango proporcional adulto respecto del humano y aclarar si las placas/zonas minerales siguen ubicaciones anatómicas canónicas o si su distribución es variación individual. Sin esto, distintas generaciones pueden producir especies visualmente incompatibles.

### Marevyn

Altos, estilizados, de anatomía elegante y fluida, con escamas parciales integradas en la piel y rasgos de inspiración acuática/ictia. Siguen respirando aire y no tienen branquias confirmadas.

**Estado para hoja anatómica:** bloqueado parcialmente por rasgos centrales todavía no definidos.

**CANON VISUAL INSUFICIENTE — requiere Historiador:** `ART_WORLD_GUIDE.md` deja expresamente abiertos orejas, piel, manos y pies. Una hoja anatómica completa necesita esas decisiones o una instrucción explícita de mantener morfología humanoide normal en esos puntos.

### Vesperi

Especie adaptada a baja luz, con ojos muy grandes dominantes en el rostro y postura naturalmente algo encorvada o recogida. No vuela, no tiene ecolocalización confirmada y no debe convertirse en elfo oscuro ni humano murciélago.

**Estado para hoja anatómica:** requiere una definición adicional para que la silueta sea estable más allá de la pose.

**CANON VISUAL INSUFICIENTE — requiere Historiador:** definir los rasgos corporales principales todavía abiertos —en especial cabeza/orejas, proporciones generales, piel y extremidades— para evitar que el artista rellene el vacío con arquetipos élficos o de murciélago.

## Inconsistencia documental detectada

`CONFIRMED_IDEAS.md` conserva texto anterior que describe a Dravak como “muy pequeños” y mantiene como pendientes algunas apariencias que ya fueron precisadas posteriormente en `SPECIES.md` y `ART_WORLD_GUIDE.md`.

Para esta revisión se trata `SPECIES.md` como fuente especializada vigente de rasgos naturales y `ART_WORLD_GUIDE.md` como traducción visual obligatoria, coherente además con los commits recientes del Historiador. Conviene que el Historiador sincronice `CONFIRMED_IDEAS.md` para que futuros agentes no lean dos estados distintos del canon.

## Resultado de la primera tarea

La identidad principal de las cinco especies está comprendida. Humanos ya pueden pasar a hoja anatómica. Felaryn, Dravak, Marevyn y Vesperi tienen suficiente dirección para concept art exploratorio, pero todavía contienen decisiones anatómicas que no deben convertirse accidentalmente en canon mediante una hoja de referencia definitiva.

No se han preparado prompts ni generado imágenes en esta revisión.

**Estado:** DIRECTOR DE ARTE ACTIVO — canon leído, función firmada y listo para preparar prompts para artistas una vez resueltos los bloqueos anatómicos señalados.
