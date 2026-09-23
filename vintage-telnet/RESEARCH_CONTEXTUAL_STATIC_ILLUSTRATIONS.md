# Investigación técnica — Ilustraciones contextuales estáticas en Vintage Telnet

**Fecha:** 2026-09-23  
**Estado:** INVESTIGADO — NO ASIGNA RESPONSABLE ARTÍSTICO  
**Autor:** Investigador Técnico y de Implementación — Vintage Telnet  
**Destinatarios:** Arquitecto, Director de Arte, Diseño/Arte HTML y quien reciba posteriormente la producción visual

## PROBLEMA

Javier aclaró una necesidad visual concreta para Vintage Telnet.

No se busca:
- convertir el juego en un juego gráfico;
- poner una ilustración como fondo general de la terminal;
- animar escenarios;
- representar gráficamente cada acción o cada habitación.

Vintage Telnet sigue siendo principalmente un juego de texto.

La necesidad es poder mostrar **una imagen estática contextual en una ventana de la interfaz**, por ejemplo:
- una vista representativa del pueblo donde se encuentra el jugador;
- una vista representativa de una ciudad/región;
- una imagen del mapa cuando corresponda.

La imagen acompaña al texto. No lo sustituye.

## ESTADO ACTUAL DEL HTML

En el HTML actual:
- la terminal textual ocupa la zona principal;
- en escritorio existe una columna lateral;
- esa columna contiene actualmente un mapa esquemático construido en HTML;
- en pantallas menores la columna lateral desaparece;
- el botón `Mapa` abre un diálogo;
- la terminal sigue siendo el elemento central.

Por tanto, ya existe conceptualmente espacio de interfaz donde en el futuro puede presentarse contenido visual contextual sin convertir la terminal en una escena gráfica.

Esta investigación **no decide** cómo debe rediseñarse esa zona. Solo confirma que la arquitectura HTML actual permite incorporar imágenes estáticas.

## DEFINICIÓN TÉCNICA PROPUESTA

Para evitar confusión con “background”, “sprite” o “mapa interactivo”, se recomienda llamar a este tipo de recurso:

# Ilustración contextual estática

Definición:

> Imagen no animada que acompaña la narración textual y representa visualmente un lugar, región, población o vista de mapa sin convertirse en la fuente autoritativa del estado del juego.

## PRINCIPIO FUNDAMENTAL

**El texto conserva la precisión narrativa; la ilustración aporta contexto visual.**

Una ilustración de Valdren no necesita cambiar cada vez que el jugador pasa de la plaza a un camino o a una zona de talleres.

Puede representar Valdren de manera general mientras la terminal explica exactamente dónde está el jugador.

Esto evita necesitar cientos de imágenes y protege la naturaleza Telnet del juego.

## FORMATO RECOMENDADO PARA ILUSTRACIONES

### WebP — formato principal recomendado

Para ilustraciones completas de:
- pueblos;
- ciudades;
- paisajes;
- regiones;
- vistas ambientales;
- mapas ilustrados rasterizados;

se recomienda **WebP** como formato web de entrega inicial.

Razones:
- apropiado para imágenes pictóricas;
- buena compresión para web;
- soportado ampliamente por navegadores modernos;
- permite reducir transferencia frente a PNG en ilustraciones complejas;
- puede conservar transparencia si alguna ilustración la necesita.

### PNG

PNG sigue siendo válido como:
- archivo maestro cuando el flujo artístico lo requiera;
- recurso con transparencia particular;
- Pixel Art;
- caso donde la compresión sin pérdida sea importante.

No es necesario obligar a que toda ilustración grande del HTML se publique como PNG.

### SVG

SVG sigue siendo apropiado para:
- iconos;
- marcos;
- separadores;
- geometría;
- ornamentación escalable;
- mapas realmente vectoriales cuando se diseñen como tales.

No se recomienda convertir automáticamente una ilustración pictórica compleja de un pueblo a SVG.

### AVIF

AVIF puede ofrecer compresión muy eficiente, pero no se propone como requisito inicial.

WebP es una opción simple y suficientemente moderna para comenzar. Arquitecto puede evaluar AVIF posteriormente si el peso real de las ilustraciones lo justifica.

## FLUJO DE PRODUCCIÓN RECOMENDADO

El artista no debe preocuparse necesariamente por producir directamente el formato final optimizado.

Flujo posible:

```
imagen generada/editada
        ↓
máster de trabajo (PNG u otro formato autorizado)
        ↓
validación
        ↓
conversión automática
        ↓
WebP optimizado para el juego
        ↓
publicador de assets
        ↓
repositorio
```

La conversión es trabajo determinista y debería integrarse al futuro **Publicador de Assets por Lote**, no hacerse manualmente por Javier.

## NO OBLIGAR AL ARTISTA A OPTIMIZAR A MANO

El agente artístico debe concentrarse en:
- composición;
- coherencia visual;
- canon;
- legibilidad;
- intención de la imagen.

Un script puede encargarse de:
- conversión;
- dimensiones;
- compresión;
- peso;
- nombres;
- validación;
- publicación.

## ORGANIZACIÓN DE ASSETS

La estructura exacta debe decidirla Arquitecto.

Conceptualmente conviene distinguir ilustraciones contextuales de mapas.

Ejemplo NO vinculante:

```
vintage-telnet/assets/
  locations/
    <poblacion>.webp
    <region>.webp
  maps/
    <mapa>.webp
```

No crear todavía todos esos archivos ni carpetas vacías solo por anticipación.

## RESOLUCIÓN

No se recomienda generar/publicar una imagen gigantesca simplemente porque la IA puede producirla.

La resolución final debe derivarse del tamaño máximo real de la ventana HTML y de pantallas HiDPI.

Arquitecto/HTML debe definir primero el espacio de presentación y después fijar:
- relación de aspecto;
- ancho máximo útil;
- variantes si realmente hacen falta;
- objetivo de peso.

Evitar almacenar varias resoluciones si una sola versión optimizada satisface móvil/tablet/escritorio.

## CARGA WEB

Las ilustraciones contextuales no deberían bloquear el inicio de la terminal.

Recomendaciones para implementación posterior:
- terminal y estado textual primero;
- imágenes secundarias con carga diferida cuando corresponda;
- dimensiones/aspect-ratio conocidos para evitar saltos de layout;
- fallback visual si la imagen no carga;
- no codificar imágenes grandes como Base64 dentro del HTML.

## RELACIÓN CON EL ESTADO DEL JUEGO

Cuando exista servidor, la imagen mostrada debe derivarse de un **identificador de contexto** autorizado por el estado del juego.

Ejemplo conceptual:

```
location_context = "valdren"
visual_asset = "valdren.webp"
```

La interfaz no debe intentar deducir el lugar analizando frases de la narración.

El servidor/estado estructurado debe poder indicar el contexto y el cliente elegir el asset correspondiente.

Esto mantiene separadas:
- narración;
- estado;
- presentación.

## NO REVELAR INFORMACIÓN NO DESCUBIERTA

Una ilustración no debe romper el diseño textual revelando:
- caminos secretos;
- criaturas ocultas;
- identidades desconocidas;
- interiores no visitados;
- elementos narrativos que el personaje todavía no conoce;
- detalles de canon que Historia no haya establecido.

La ilustración contextual debe representar solo aquello que su nivel de contexto permite mostrar.

Para Vintage Telnet, cualquier producción visual debe seguir la autoridad ya definida en el repositorio:
- Historiador: qué existe y cómo es;
- Narrador: qué experiencia/momento se representa;
- Arte: cómo se vuelve visible sin cambiar canon.

## MAPA E ILUSTRACIÓN DE LUGAR SON RECURSOS DIFERENTES

No conviene tratar ambos como el mismo concepto.

### Ilustración de lugar
Comunica:
- apariencia;
- ambiente;
- arquitectura;
- identidad visual.

### Mapa
Comunica:
- orientación;
- relaciones espaciales;
- información descubierta.

Por tanto, pueden compartir una ventana de presentación en la interfaz, pero tienen requisitos distintos.

Especialmente el mapa debe respetar descubrimiento y ocultamiento de información.

## QUÉ NO DEBE HACER ESTA IMAGEN

No debe convertirse en:
- mapa clicable por defecto;
- sistema de movimiento;
- reemplazo del texto;
- fuente de verdad de salidas;
- animación;
- escenario que deba actualizarse por cada comando;
- requisito para comprender la narración.

El juego debe seguir siendo funcional y comprensible mediante texto.

## ACCESIBILIDAD

La imagen es complementaria.

La implementación HTML debe proporcionar texto alternativo apropiado o descripción accesible cuando corresponda, sin duplicar innecesariamente toda la narración.

Un jugador que no vea/cargue la ilustración no debería perder información mecánica necesaria.

## RELACIÓN CON EL PUBLICADOR AUTOMÁTICO

Esta necesidad refuerza `ASSET_BATCH_PUBLISHER_SPEC.md`.

El publicador debería poder, en una fase posterior:
1. recibir un máster;
2. identificar que es una ilustración contextual;
3. convertir a WebP según perfil aprobado;
4. comprobar dimensiones/peso;
5. publicar el recurso;
6. devolver ruta, dimensiones y peso final.

Ejemplo conceptual:

```
publish-assets valdren.png \
  --profile vintage-location \
  --target <ruta-autorizada>
```

El nombre real del comando/perfil lo decide Arquitecto.

## PRUEBA TÉCNICA PROPUESTA

Cuando exista una primera ilustración aprobada:

1. tomar una única imagen de una población ya definida;
2. conservar el máster fuera o dentro del repo según política que decida Arquitecto;
3. producir WebP optimizado;
4. cargarlo en la ventana HTML de prueba;
5. comprobar teléfono, tablet y escritorio;
6. medir peso y tiempo de carga;
7. comprobar que la terminal sigue siendo protagonista;
8. comprobar que sin imagen el juego continúa funcionando;
9. verificar que la imagen no revela información fuera de canon.

Una sola imagen basta para validar el sistema antes de producir una biblioteca completa.

## DECISIONES QUE ESTA INVESTIGACIÓN NO TOMA

Este documento NO decide:
- quién crea las ilustraciones;
- si la tarea corresponde a Artista, Director de Arte, Arte HTML u otro rol;
- composición artística;
- estilo definitivo;
- qué población se ilustra primero;
- relación de aspecto definitiva;
- ubicación final de la ventana;
- cuándo cambia la imagen;
- qué mapas se muestran;
- reglas de descubrimiento.

Esas decisiones corresponden a los roles de coordinación, arte, jugabilidad y canon apropiados.

## RECOMENDACIÓN TÉCNICA

Para esta necesidad concreta:

**tratar las imágenes como ilustraciones contextuales estáticas y usar WebP como formato web principal para escenas pictóricas, manteniendo la terminal textual como fuente principal de experiencia y la imagen como complemento.**

El flujo artístico puede producir un máster PNG u otro formato aprobado; la conversión/optimización debería automatizarse antes de publicación.

No es necesario diseñar un sistema gráfico complejo para conseguir esta mejora.
