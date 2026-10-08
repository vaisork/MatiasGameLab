# VT2 — Referencia de narrativa MUD clásica (propuesta editorial)

**Estado:** material de referencia y ejemplos originales, **NO** contenido integrado ni despliegue. **Fecha:** 2026-10-08.

## Procedencia y límites

- Merc/Diku: [documentación histórica de áreas](https://github.com/alexmchale/merc-mud/blob/master/doc/area.txt) y [Midgaard](https://github.com/alexmchale/merc-mud/blob/master/area/midgaard.are). Su arquitectura separa `#ROOMS`, descripciones de salida `D`, descripciones adicionales `E`, `#MOBILES`, `#OBJECTS` y `#SHOPS`.
- **Ninguno de los ejemplos siguientes es una transcripción de Killer Instincts ni una traducción literal de Midgaard.** Son textos originales escritos como demostración de ritmo y presentación; los nombres de VT2 son contextuales y deben contrastarse con IDs y canon reales antes de integrarlos.
- No se incorpora código ni texto protegido de terceros. Antes de reutilizar archivos históricos completos, revisar licencias y atribuciones.

## Contrato de lectura propuesto

1. **Título + base estable**: 25–65 palabras por defecto, con excepciones justificadas; topografía, rasgo singular y orientación sin repetición.
2. **Presencia**: listar NPC/objetos sólo cuando el servidor confirma presencia. No incrustar NPC móviles ni clima mutable en la base.
3. **Eventos**: máximo una o dos señales relevantes por pantalla; hora, clima, amenaza y memoria son capas priorizadas, no concatenadas por obligación.
4. **Salidas**: derivar exclusivamente del grafo real, nunca de estos ejemplos.
5. **Mirar / examinar**: texto adicional ligado a objetivo real, sin otorgar información secreta por mera prosa.
6. **Reentrada**: vista corta opcional para desplazamiento repetido; `mirar` restaura descripción completa; nunca ocultar peligro o información funcional.
7. **Sin invención de estado**: combate, botín, comercio, encargos y NPCs son del servidor Python/SQLite.
8. **Variación con propósito**: alternar calle, interior, cruce, transición, amenaza, silencio y descubrimiento; no añadir clima o fauna en cada paso.

### Formato de ejemplo

Cada ficha presenta **base**, **capa dinámica hipotética** (NO mostrar sin condición real), **examen** y **salidas ilustrativas** (NO usar sin mapear IDs). Los ejemplos son *propuestas no canónicas*.

### 01. Plaza urbana — La plaza del mercado

**Base:** Los puestos rodean una fuente baja. Una calle empedrada conduce al norte; hacia el este se oyen los pregones de los vendedores.

**Capa condicional:** Un mercader acomoda sus telas.

**Interacción `examinar fuente`:** El borde de piedra está gastado por años de uso.

**Salidas de muestra (no canónicas):** norte, este, sur.

### 02. Calle de ciudad — Calle de los curtidores

**Base:** Las casas estrechan la calle. Bajo los aleros cuelgan tiras de cuero y un canal lleva agua turbia hacia el sur.

**Capa condicional:** Un aprendiz cruza con un haz de correas.

**Interacción `mirar canal`:** El agua corre bajo una rejilla de hierro.

**Salidas de muestra (no canónicas):** norte, sur.

### 03. Taberna — La mesa junto al hogar

**Base:** Un hogar de piedra calienta la sala. Las mesas están marcadas por vasos y cuchillos; una escalera sube a los cuartos.

**Capa condicional:** La tabernera recoge una jarra vacía.

**Interacción `examinar mesa`:** Hay nombres tallados en la madera.

**Salidas de muestra (no canónicas):** este, arriba.

### 04. Comercio — Tienda de herramientas

**Base:** Azadas, cuerdas y clavos ocupan los estantes. Un mostrador separa la entrada de la trastienda.

**Capa condicional:** Un comerciante espera detrás del mostrador.

**Interacción `examinar estantes`:** Las herramientas están agrupadas por oficio.

**Salidas de muestra (no canónicas):** oeste.

### 05. Forja — Umbral de la forja

**Base:** La piedra del umbral está ennegrecida. Dentro se ven un yunque, tenazas y un horno encendido.

**Capa condicional:** Daro trabaja el metal si está presente según el estado del servidor.

**Interacción `mirar yunque`:** La superficie muestra pequeñas marcas de golpes antiguos.

**Salidas de muestra (no canónicas):** sur, este.

### 06. Camino — Camino de piedra

**Base:** El sendero desciende entre rocas oscuras. Más adelante se distingue el humo de las casas de Valdren.

**Capa condicional:** Una carreta pasa sólo si existe el evento correspondiente.

**Interacción `mirar humo`:** La columna asciende desde el poblado.

**Salidas de muestra (no canónicas):** norte, sur.

### 07. Cruce — Cruce de senderos

**Base:** Dos caminos se encuentran junto a un poste torcido. El terreno se vuelve pedregoso hacia el oeste; al este crece hierba alta.

**Capa condicional:** El viento mueve la cuerda del poste.

**Interacción `examinar poste`:** Las letras están descoloridas, pero una flecha sigue apuntando al este.

**Salidas de muestra (no canónicas):** norte, este, oeste.

### 08. Bosque — Bajo los abedules

**Base:** Los troncos blancos dejan pasar una luz desigual. Las raíces levantan la tierra del sendero y una rama caída obliga a rodearla.

**Capa condicional:** Se oye un pájaro entre las hojas, si corresponde al lugar.

**Interacción `examinar rama`:** La corteza está recién partida.

**Salidas de muestra (no canónicas):** sur, oeste.

### 09. Ribera — Orilla del arroyo

**Base:** El agua corre entre piedras redondas. La orilla opuesta queda oculta tras los juncos; el camino continúa junto a la corriente.

**Capa condicional:** Un insecto se posa sobre el agua.

**Interacción `mirar juncos`:** Entre los tallos se ve una franja de barro húmedo.

**Salidas de muestra (no canónicas):** norte, sur.

### 10. Montaña — Cornisa de Hoshai

**Base:** El paso apenas admite a dos viajeros. A un lado se alza la pared de roca; al otro, la ladera cae hacia una quebrada.

**Capa condicional:** Una piedra rueda cuesta abajo si se dispara ese evento.

**Interacción `mirar quebrada`:** La niebla impide distinguir el fondo.

**Salidas de muestra (no canónicas):** este, oeste.

### 11. Ruinas — Patio derrumbado

**Base:** Tres columnas siguen en pie. El resto del techo yace sobre losas rotas, cubiertas de polvo y pequeñas plantas.

**Capa condicional:** Un golpe seco resuena a lo lejos sólo si hay un origen real.

**Interacción `examinar columnas`:** En la base sobreviven marcas de herramientas.

**Salidas de muestra (no canónicas):** norte, abajo.

### 12. Mazmorra — Galería de las grietas

**Base:** La galería gira hacia el este. Una fisura recorre el techo y el suelo está cubierto de grava suelta.

**Capa condicional:** Se escucha un roce detrás de la pared cuando existe la amenaza.

**Interacción `examinar fisura`:** La grieta se estrecha antes de perderse en la oscuridad.

**Salidas de muestra (no canónicas):** este, oeste.

### 13. Peligro anticipado — Paso de las huellas

**Base:** El sendero atraviesa un claro sin árboles. Hay surcos recientes en la tierra y varias ramas están quebradas a poca altura.

**Capa condicional:** Un gruñido lejano sólo aparece si el servidor confirma la criatura.

**Interacción `examinar surcos`:** Las marcas se internan hacia el norte.

**Salidas de muestra (no canónicas):** norte, sur.

### 14. Hallazgo — Rincón del molino

**Base:** El viejo molino está inmóvil. Bajo la rueda quedan hojas atrapadas y el canal se ha llenado de arena.

**Capa condicional:** Un objeto visible se lista aquí sólo si realmente existe.

**Interacción `examinar rueda`:** Una de las paletas está partida.

**Salidas de muestra (no canónicas):** este, sur.

### 15. Regreso — Entrada de Valdren

**Base:** Las primeras casas rodean el camino. Desde la calle se ve la chimenea de la forja y un abrevadero de piedra.

**Capa condicional:** Una puerta se cierra a lo lejos si el evento está activo.

**Interacción `mirar abrevadero`:** El agua deja una línea oscura en la piedra.

**Salidas de muestra (no canónicas):** norte, oeste.

### 16. Combate y consecuencia — Borde del matorral

**Base:** El camino pasa junto a un matorral espeso. La tierra conserva marcas de pisadas y el sendero sigue hacia el norte.

**Capa condicional:** Una criatura emerge sólo tras validación del servidor; heridas, botín y retirada se presentan en bloques separados.

**Interacción `examinar pisadas`:** Algunas marcas son recientes; no revelan por sí solas qué criatura las dejó.

**Salidas de muestra (no canónicas):** norte, sur.

## Sesión extendida: una exploración en pantalla (texto ORIGINAL)

```text
> mirar
Camino de piedra
El sendero desciende entre rocas oscuras. Más adelante se distingue
el humo de las casas de Valdren.

Salidas: norte, sur.

> sur
Entrada de Valdren
Las primeras casas rodean el camino. Desde la calle se ve la chimenea
de la forja y un abrevadero de piedra.

Salidas: norte, oeste.

> examinar abrevadero
El agua deja una línea oscura en la piedra.

> oeste
Umbral de la forja
La piedra del umbral está ennegrecida. Dentro se ven un yunque,
tenazas y un horno encendido.

Daro trabaja junto al yunque.
Salidas: sur, este.

> hablar daro
[El servidor debe obtener el diálogo real del NPC; no generar
un servicio, encargo o recompensa inexistentes.]

> este
Entrada de Valdren
Reconoces las primeras casas y el abrevadero de piedra.
Salidas: norte, oeste.

> mirar
Entrada de Valdren
Las primeras casas rodean el camino. Desde la calle se ve la chimenea
de la forja y un abrevadero de piedra.
Salidas: norte, oeste.
```

**Nota:** Esta sesión es una demostración editorial; las direcciones, conexiones, presencia de Daro y comandos no prueban que el motor actual soporte exactamente esta secuencia. El implementador debe contrastar el grafo y la API reales.

## Anti-ejemplo y corrección

**Redundante (inventado):** «El oscuro camino está oscuro por la noche. La oscuridad de la noche cubre el camino y todo se ve oscuro. Sopla el viento nocturno. Es de noche.»

**Corregido:** Base: «El camino atraviesa un tramo de roca desnuda. Una cerca rota marca el desvío hacia el poblado». Capa nocturna, sólo cuando aplica: «La cerca apenas se distingue bajo la luz de la luna».

## Integración sugerida, no autorizada automáticamente

- World Writer: seleccionar 3–5 salas **existentes** por ID y redactar propuesta de antes/después sin perder pistas.
- Dungeon Master: verificar presagios y exploración sin introducir encuentros ni recompensas nuevos.
- Desarrollo: auditar composición existente (`description`, `arrivals`, `day/night`, `rain/clear`, `return`, `examine`, `focus`, `max_layers`), identificar duplicaciones y presentar diff mínimo; no tocar producción.
- QA: comparar primera entrada, reentrada, `mirar`, `examinar`, cambios de hora/clima, presencia de NPC y accesibilidad de pistas; preservar mapa y persistencia.

**Aprobación requerida** antes de sustituir textos canónicos o cambiar renderizador. No despliegue Raspberry.
