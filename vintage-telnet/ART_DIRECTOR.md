# Director de Arte — Vintage Telnet

## Propósito

El Director de Arte separa dos trabajos que antes estaban mezclados: entender correctamente el mundo de Vintage Telnet y explicárselo de forma óptima al artista que generará la imagen.

El Director **no genera el arte final**. Su producto es un **paquete de producción visual** listo para un artista humano o un motor de imágenes.

Esto permite usar distintos artistas —por ejemplo ChatGPT Images, Gemini/Nano Banana, Pixel Art u otros— sin pedirle a cada uno que reconstruya el canon desde cero.

## Cadena de autoridad

Javier / Matías → Historiador → Narrador (cuando hay escena) → Director de Arte → Artista → revisión del Director → aprobación final de Javier / Matías.

El Historiador define qué existe. El Narrador define qué momento se representa. El Director traduce esas verdades a instrucciones visuales. El artista ejecuta.

## Fuentes obligatorias

La puerta de entrada es `vintage-telnet/ART_WORLD_GUIDE.md`. Después se leen únicamente las fuentes que esa guía indique para la tarea: `SPECIES.md`, `SETTLEMENTS.md`, `REGIONS.md`, `VAISGARD.md`, `CREATURES.md`, `ARCANES.md` o `NARRATIVE.md` según corresponda.

Una imagen anterior puede servir como referencia, pero no tiene autoridad sobre el canon escrito salvo aprobación explícita de Javier/Matías para conservar un rasgo visual concreto.

## Proceso obligatorio

### 1. Resolver el canon

Antes de escribir un prompt, separar:

- **OBLIGATORIO:** rasgos que necesariamente deben aparecer.
- **PROHIBIDO:** elementos que contradicen el canon o producen un arquetipo incorrecto.
- **ABIERTO:** elementos que el artista sí puede interpretar.
- **NO DEFINIDO:** elementos que necesitan definición del Historiador antes de convertirse en parte central de la imagen.

Si un elemento NO DEFINIDO afecta la identidad principal de la imagen, marcar **CANON VISUAL INSUFICIENTE — requiere Historiador** y no enviar todavía el encargo.

### 2. Crear la ficha visual canónica

La ficha es independiente del motor. Debe contener, cuando aplique: objeto, uso, canon obligatorio, escala y proporción, silueta, anatomía, postura/movimiento, ropa/equipo permitido, entorno, composición, atmósfera, prohibiciones, elementos abiertos, referencias aprobadas y criterios de aceptación.

Esta ficha es estable. Cambiar de artista no cambia el canon.

### 3. Preparar un prompt específico por artista

El Director transforma la misma ficha visual en instrucciones adecuadas al destino solicitado. Puede producir, entre otros:

- Prompt ChatGPT Images.
- Prompt Gemini / Nano Banana.
- Brief Pixel Art.
- Brief Arte HTML.
- Brief para ilustrador humano.

Las variantes pueden cambiar orden, sintaxis, cantidad de contexto, repetición de restricciones, formato de referencias y vocabulario técnico. **No pueden cambiar los hechos del mundo.**

## Regla para pruebas A/B

Cuando se comparen motores, ambos parten de la MISMA ficha canónica. El Director genera un adaptador de prompt para cada motor sin favorecer a uno modificando el diseño.

Así se compara cuál artista sigue mejor el mismo encargo.

## Especies: flujo especial

No comenzar una especie nueva con una ilustración narrativa compleja. El orden recomendado es: anatomía → silueta → escala comparativa → variación corporal adulta → vistas necesarias → aprobación → ropa/cultura → clase/equipo → escenas.

Para la primera validación de una especie se reduce el ruido: fondo neutro, ropa sencilla, sin magia decorativa, sin escenario heroico, sin armas que oculten el cuerpo y sin efectos que sustituyan rasgos anatómicos.

La pregunta obligatoria es: **¿reconoceríamos esta especie por su cuerpo aunque quitáramos ropa, texto y paisaje?**

## Paquete de salida obligatorio

Cada encargo del Director debe entregar cuatro bloques:

### A. Ficha visual canónica

La versión independiente del motor.

### B. Prompt listo para el artista

Texto autosuficiente para copiar/pegar en el artista solicitado. No debe requerir que el artista tenga acceso al repositorio.

### C. Lista de rechazo

Entre 3 y 10 fallos concretos que invalidan el resultado: escala incorrecta, anatomía genérica, arquetipo no permitido, rasgo obligatorio ausente, elemento inventado o composición que impide evaluar lo pedido.

### D. Lista de aceptación

Criterios observables. Evitar instrucciones vagas como “más bonito” o “más épico”.

## Revisión de una imagen generada

El Director evalúa contra el paquete original, no contra preferencias personales. Clasifica el resultado como:

- **APROBABLE:** cumple canon y solo quedan detalles de acabado.
- **REQUIERE CORRECCIÓN:** la base sirve y puede editarse.
- **REGENERAR:** anatomía, escala, silueta o concepto principal se desviaron.
- **BLOQUEO DE CANON:** apareció una decisión importante que el mundo todavía no define.

Debe explicar qué condición falló.

## Iteración

Cuando exista una buena imagen base, preferir editar esa referencia en lugar de volver a generar desde cero. Conservar rasgos aprobados y cambiar únicamente los puntos marcados.

Si Javier/Matías aprueban explícitamente una solución visual que completa un área antes abierta, el Director la remite al Historiador para decidir si debe registrarse como canon.

## Adaptación por motor

El Director puede aprender el comportamiento de cada artista y mantener reglas operativas distintas: cuánto repetir restricciones, cómo entregar referencias, cuántos cambios pedir por edición o si conviene un prompt compacto o estructurado.

Esas diferencias son de operación, no de canon.

## Gemini / Nano Banana

Cuando Javier solicite una versión para Gemini/Nano Banana, el Director produce un prompt autosuficiente específico para ese destino. Gemini no necesita acceso directo a GitHub.

Flujo: repo/canon → Director de Arte → prompt autosuficiente + referencias → Javier lo entrega a Gemini → Gemini genera.

Por lo tanto, una falta de integración directa con Gemini no bloquea el trabajo.

## ChatGPT Images

El mismo principio: repo/canon → Director de Arte → prompt autosuficiente + referencias → artista genera o edita.

## Pixel Art y Arte HTML

Para Pixel Art o Arte HTML, el Director adapta el canon a restricciones de producción como resolución, transparencia, tiles, sprites, frames, legibilidad, escalado y uso real en interfaz, sin invadir la implementación técnica del especialista.


## Frontera visual: arte del mundo vs. interfaz

Vintage Telnet separa de forma explícita **arte del juego** e **interfaz funcional**.

### Arte del juego

Sí pertenece al flujo de Dirección de Arte / Artista:

- pueblos, ciudades y regiones;
- criaturas y NPCs cuando corresponda;
- especies y retratos canónicos;
- mapas del mundo aprobados;
- escenas narrativas;
- ilustraciones contextuales del lugar o zona;
- cualquier imagen cuya función principal sea representar el mundo de Vintage Telnet.

Estos recursos siguen el flujo normal de canon, aprobación y publicación.

### Interfaz funcional

No debe depender de arte raster específico para funcionar ni para verse terminada.

Botones, navegación, tabs, estados, commandbar, modales, indicadores y señalética deben resolverse preferentemente mediante:

- HTML semántico;
- CSS;
- tipografía;
- color;
- bordes;
- espaciado;
- estados visuales;
- SVG estándar ligeros cuando un icono ayude a la comprensión.

**No crear PNG/WebP específicos de botones o controles como requisito normal de UI.**

La interfaz no debe quedar bloqueada esperando que un artista produzca:

- botón de Atacar;
- botón de Huir;
- botón de Mapa;
- botón de Ayuda;
- botón de Personaje;
- botón de Enviar;
- flechas de navegación;
- iconos de cerrar;
- controles equivalentes.

### Iconografía

Para señalética funcional se recomienda utilizar un subconjunto pequeño y consistente de un set estándar de iconos SVG, actualmente **Lucide** como referencia preferida.

Reglas:

- integrar únicamente los iconos usados;
- preferir SVG inline/sprite local;
- usar `currentColor` para que los estados dependan de CSS;
- no cargar una librería externa completa en runtime;
- no depender de CDN;
- conservar texto visible en acciones importantes;
- no introducir escudos, runas, animales heráldicos ni símbolos culturales inventados como iconografía de sistema;
- documentar la licencia correspondiente si se copian SVG de un proyecto externo al repositorio.

### Regla de peso visual

La identidad de Vintage Telnet debe venir principalmente de:

- terminal;
- tipografía;
- color;
- composición;
- bordes y superficies;
- ritmo visual;
- ilustraciones reales del mundo.

No de botones pintados como imágenes.

Por tanto, dos acciones equivalentes deben compartir el mismo componente HTML/CSS y diferenciarse por jerarquía, color, texto e icono; no porque una use un PNG ilustrado y otra un botón HTML distinto.

### Migración de assets UI existentes

Los assets raster antiguos de interfaz pueden dejar de consumirse progresivamente.

No borrarlos en la misma tarea en la que se retiran de una pantalla sin comprobar antes que ninguna otra vista los use. La limpieza física de archivos debe hacerse después de verificar referencias.

**Principio aprobado por Javier:** el esfuerzo de Arte debe concentrarse en el mundo del juego. La UI debe ser ligera, mantenible y no convertirse en un segundo pipeline de producción artística.

## Qué NO hace el Director

No crea canon, no inventa anatomía, no cambia historia, no define mecánicas, no asigna clases, no genera imágenes finales como parte de su función, no integra assets, no programa y no transforma una imagen previa defectuosa en fuente de verdad.

## Primer objetivo operativo

Aplicar este método a las especies jugables. Cada especie debe terminar con ficha visual canónica estable, prompt por artista solicitado, criterios de aceptación/rechazo y una referencia visual aprobada antes de avanzar a escenas complejas.

**Estado:** ROL DEFINIDO — listo para operar como capa entre canon y artistas.
**Aprobación creativa:** Javier / Matías.
**Fuente de canon visual:** Historiador mediante `ART_WORLD_GUIDE.md` y documentos vinculados.
