# Senku — Investigación técnica para crecer más rápido

**Autor:** Investigador Técnico y de Implementación — Senku  
**Fecha:** 2026-09-20  
**Estado base investigado:** `c2ad5e920cbf7b584db8b1fb7272f8cf03c93051`  
**Objetivo:** ayudar al Arquitecto a hacer que Senku pueda crecer país por país con iteraciones más rápidas, sin reconstruir innecesariamente el juego existente.

## PROBLEMA

Senku debe crecer y mejorar conforme avanzan los niveles y países. El reto es permitir que cada nueva iteración añada contenido y, cuando corresponda, capacidades técnicas nuevas sin que cada escena obligue a editar muchas partes distintas del juego o a reconstruir lo anterior.

La prioridad no es crear un motor sofisticado. La prioridad es que una idea nueva pueda convertirse rápidamente en una escena jugable, probarse en teléfono/iPad y mejorarse sin romper escenas anteriores.

## ESTADO ACTUAL

Senku sigue siendo una arquitectura HTML/Canvas ligera y apropiada para su tamaño actual.

Hoy `senku.html` concentra:
- HTML de interfaz y menús;
- CSS responsive;
- entrada táctil y teclado;
- bucle `requestAnimationFrame`;
- movimiento, salto, gravedad y colisiones;
- estado del jugador;
- escenas;
- plataformas;
- coleccionables;
- detección de interacciones;
- acciones narrativas;
- render de fondos/objetos;
- carga de sprites;
- guardar algunos datos en `localStorage`.

Las cuatro escenas actuales son `house`, `street`, `bus` y `taco`.

Para añadir o cambiar una escena hoy suele ser necesario tocar varias zonas diferentes:
1. `info` para nombre/objetivo;
2. `setScene()` para spawn y objetos;
3. `platforms()` para geometría;
4. `interaction()` para detectar puntos interactivos;
5. `act()` para decidir qué ocurre;
6. una función de dibujo;
7. `draw()` para llamar a esa función.

Esto es sencillo con pocas escenas, pero crecerá mal si cada país añade muchas escenas.

### Cosas que ya están bien y conviene conservar

- Canvas y controles compartidos.
- Físicas pequeñas y comprensibles.
- Assets externos en `assets/` en vez de grandes Base64.
- Spritesheets donde ya aportan utilidad.
- GitHub/`main` como fuente de verdad.
- Pixel Art separado del código.
- Posibilidad de usar formas simples de Canvas mientras llega el arte definitivo.
- Filosofía de que los países posteriores puedan mostrar una evolución técnica visible.

## OPCIONES INVESTIGADAS

### Opción A — Seguir añadiendo `if(scene===...)` al HTML

**Ventajas**
- Cero trabajo inicial.
- Muy fácil de entender ahora.
- Adecuado para pequeños ajustes en México.

**Desventajas**
- Cada escena nueva exige editar muchos lugares.
- Mayor riesgo de olvidar una parte.
- Más conflictos cuando varios desarrolladores trabajan.
- Cada nivel tarda progresivamente más en integrar y probar.

**Conclusión**
Conservar para mantenimiento de México, pero no usar como patrón indefinido para todos los países.

### Opción B — Reescribir Senku con un motor/framework

**Ventajas**
- Muchos sistemas preparados.
- Escalabilidad técnica alta en teoría.

**Desventajas**
- Reescritura costosa.
- Puede romper controles, sensación y compatibilidad actuales.
- Introduce complejidad que todavía no necesitamos.
- Dificulta ver la evolución progresiva del propio proyecto.

**Conclusión**
No recomendado ahora.

### Opción C — Crear un pequeño “núcleo Senku” y convertir los niveles futuros en datos/configuración

**Ventajas**
- Conserva Canvas y el juego actual.
- Reduce la cantidad de código nuevo por escena.
- Permite reutilizar movimiento, colisiones, interacción, HUD y coleccionables.
- Hace más fácil que un país nuevo tenga mejoras propias.
- Permite migración gradual, no una reescritura.

**Desventajas**
- Requiere definir un contrato simple para escenas.
- Algunas mecánicas especiales seguirán necesitando código propio.

**Conclusión**
Es la dirección recomendada.

## RECOMENDACIÓN TÉCNICA PARA EL ARQUITECTO

### 1. Separar mentalmente MOTOR y CONTENIDO antes de separar archivos

Primero establecer dos categorías:

**NÚCLEO REUTILIZABLE**
- loop;
- input;
- movimiento;
- salto/gravedad;
- colisión base;
- cámara cuando exista;
- HUD;
- modal;
- carga de assets;
- sistema básico de interacción;
- coleccionables;
- guardado.

**CONTENIDO DEL NIVEL**
- nombre y objetivo;
- spawn;
- plataformas;
- objetos;
- NPCs;
- zonas de interacción;
- texto;
- transición a otra escena;
- dibujo/fondo específico;
- mecánica especial del lugar.

No hace falta separar inmediatamente todo en archivos diferentes. Primero hay que separar responsabilidades.

### 2. Introducir un registro de escenas para los niveles nuevos

En lugar de añadir cinco o seis `if(scene===...)`, los niveles futuros deberían poder describirse mediante una estructura similar a:

```js
SCENES.market = {
  country: 'mexico',
  title: 'Mercado',
  objective: 'Encuentra el puesto correcto',
  spawn: {x: 60, y: 430},
  platforms: [...],
  collectibles: [...],
  interactions: [...],
  draw: drawMarket
}
```

No es obligatorio migrar inmediatamente las cuatro escenas actuales.

La primera meta es que una escena futura pueda registrarse en un solo lugar y el núcleo lea automáticamente su título, spawn, plataformas, objetos e interacciones comunes.

### 3. Las mecánicas especiales deben ser “extensiones”, no copias del motor

Ejemplo actual: la taza tiene una pequeña lógica especial.

El patrón futuro puede ser:

- comportamiento genérico compartido;
- pequeño `update()` opcional por escena;
- pequeño `draw()` opcional;
- eventos opcionales `enter/exit/action`.

Así una escena con un objeto nuevo no obliga a modificar el loop principal permanentemente.

### 4. No reconstruir México sólo para que use la nueva estructura

México puede seguir mostrando cómo empezó Senku.

Cuando llegue el siguiente país o un bloque importante de escenas nuevas, ahí conviene probar el nuevo registro de escenas.

Después de comprobar que realmente acelera el trabajo, el Arquitecto podrá decidir si alguna pieza antigua merece migrarse. No hacerlo por uniformidad estética del código.

### 5. Crear una PLANTILLA DE NIVEL

Para cada escena nueva, el Arquitecto debería entregar a desarrollo una ficha corta:

```
ESCENA:
PAÍS:
OBJETIVO:
SPAWN:
SALIDA/TRANSICIÓN:
PLATAFORMAS:
COLECCIONABLES:
INTERACCIONES:
NPC/ENEMIGO:
MECÁNICA NUEVA:
ASSETS EXISTENTES:
ASSETS FALTANTES:
PRUEBA EN MÓVIL:
CRITERIO DE ACEPTACIÓN:
```

Esto reduce conversaciones repetidas y permite que Pixel Art y desarrollo trabajen en paralelo.

### 6. Utilizar placeholders funcionales antes del arte final

Senku ya dibuja muchos escenarios con formas de Canvas. Esto debe aprovecharse.

Flujo recomendado:
1. Arquitecto define escena.
2. Desarrollo crea geometría e interacción con bloques/colores temporales.
3. Javier/Matías prueban si la escena es divertida.
4. Sólo después se solicitan o terminan los assets definitivos.
5. Pixel Art reemplaza los placeholders mediante rutas estables.

Esto evita esperar a que todo el arte esté terminado antes de probar el nivel.

### 7. Crear “paquetes de assets” por función o por escena

Para nuevos países, evitar una secuencia de solicitudes PNG aisladas.

Una escena debería declarar de una vez qué necesita:
- personaje/NPC;
- poses o frames;
- objetos;
- fondo;
- interfaz especial.

Pixel Art puede preparar una entrega por lote. Las rutas deben conocerse antes de la integración final.

No reorganizar las rutas existentes de México sólo para cumplir esta estructura.

### 8. Para países nuevos, usar una carpeta propia de assets

Sin romper rutas actuales, una convención útil para contenido futuro sería:

```
assets/countries/<pais>/<escena>/...
```

o una estructura equivalente que el Arquitecto apruebe.

Esto reduce colisiones de nombres y permite saber rápidamente qué pertenece a un país.

Los assets globales de Senku, trajes reutilizables o iconos pueden continuar fuera de esa estructura.

### 9. Definir CAPACIDADES por país para mostrar evolución

No todos los países deben usar todas las técnicas.

Ejemplo conceptual:

- **México:** movimiento, salto, escenas fijas, interacciones básicas.
- **País siguiente:** puede estrenar scrolling/cámara.
- **Otro posterior:** NPCs con rutas o estados.
- **Posterior:** audio ambiental, partículas, clima, plataformas móviles, etc.

El Arquitecto debe tratar una tecnología nueva como una “capacidad” que se estrena cuando mejora realmente ese tramo del juego.

Una capacidad que nace en un país posterior no obliga automáticamente a rehacer los anteriores.

### 10. Crear una regla de “investigar sólo lo nuevo”

El Investigador no debe bloquear cada nivel.

Si el Arquitecto pide:
- otra plataforma;
- otro coleccionable;
- otra conversación;
- otra transición ya conocida;

desarrollo debería reutilizar el patrón existente directamente.

Consultar al Investigador cuando aparezca algo realmente nuevo:
- cámara;
- scrolling;
- mapas grandes;
- enemigo con IA;
- agua/física diferente;
- nueva forma de guardado;
- audio complejo;
- muchos sprites;
- rendimiento;
- nuevas necesidades offline/PWA.

### 11. Automatizar validaciones pequeñas antes que crear un build system

Antes de introducir herramientas grandes, sería útil que desarrollo dispusiera de una prueba simple capaz de detectar:

- ruta de asset inexistente;
- ID duplicado de coleccionable;
- escena de destino inexistente;
- sprite con datos incoherentes;
- referencias rotas;
- errores JavaScript básicos.

Esto puede ser un script de validación aislado y no necesita convertirse en parte del juego.

### 12. Modularizar archivos sólo cuando el crecimiento lo justifique

No recomiendo partir `senku.html` inmediatamente.

Señales para hacerlo:
- varios países activos;
- conflictos frecuentes en el mismo archivo;
- funciones de escenas dominando el HTML;
- dificultad real para revisar cambios.

Cuando llegue ese punto, una división pequeña sería suficiente:

```
senku.html
js/senku-core.js
js/senku-scenes.js
```

y sólo después, si sigue creciendo:

```
js/countries/mexico.js
js/countries/<siguiente-pais>.js
```

No introducir bundler/framework por defecto.

## PROPUESTA DE FLUJO PARA ITERACIONES MÁS RÁPIDAS

```
Javier/Matías
    ↓ idea
Arquitecto
    ↓ ficha de escena + criterio de aceptación
    ├── mecánica conocida → Desarrollo directamente
    ├── mecánica nueva/difícil → Investigador Técnico
    └── arte faltante → PIXEL_ART_REQUESTS.md
          ↓
Desarrollo crea primero versión jugable con placeholders
          ↓
Javier/Matías prueban diversión y sensación
          ↓
Pixel Art entrega assets en lote
          ↓
Desarrollo conecta rutas finales
          ↓
Integrador revisa y publica
```

La clave es que programación y arte puedan avanzar en paralelo y que el arte definitivo no bloquee una prueba jugable.

## IMPACTO

La primera etapa no necesita reescribir `senku.html`.

Los cambios futuros probablemente afectarán:
- definición de escenas;
- sistema de interacción;
- organización de assets futuros;
- documentación de nivel;
- eventualmente uno o dos archivos JavaScript externos si el tamaño lo justifica.

## RIESGOS

### Abstraer demasiado pronto
Crear un sistema genérico para problemas que aún no existen puede ralentizar el proyecto.

**Mitigación:** extraer una abstracción sólo después de ver al menos dos usos claros.

### Obligar a México a usar toda tecnología nueva
Eliminaría parte de la evolución visible y consumiría tiempo sin añadir diversión.

**Mitigación:** compatibilidad hacia adelante, no homogeneización hacia atrás.

### Hacer que la configuración sea más difícil que el código
Un formato demasiado sofisticado puede ser peor que unos pocos `if`.

**Mitigación:** objetos JavaScript simples; nada de DSL ni editor de niveles complejo por ahora.

### Bloqueo entre arte y programación
Esperar el asset final antes de probar una escena alarga cada ciclo.

**Mitigación:** placeholders + contrato de asset + sustitución posterior.

## PRUEBA PROPUESTA

Usar una próxima escena o país como piloto.

Medir:
1. cuántos lugares del código hay que tocar para añadirla;
2. cuántos cambios requieren al Arquitecto volver a explicar información;
3. cuánto trabajo puede hacerse antes de recibir arte final;
4. cuántos fallos aparecen por rutas/assets;
5. cuánto tarda una segunda escena parecida después de crear el patrón.

Si la segunda escena puede construirse principalmente declarando datos y reutilizando comportamiento, el sistema está cumpliendo su objetivo.

## IMPLEMENTACIÓN PARA DESARROLLO

Cuando el Arquitecto decida comenzar esta evolución, no pedir una “refactorización de Senku”.

Pedir primero una tarea pequeña:

> Crear un registro mínimo para una nueva escena que permita declarar título, objetivo, spawn, plataformas, coleccionables e interacciones comunes sin modificar múltiples `if(scene===...)`. Mantener las escenas actuales funcionando y no migrarlas salvo que sea estrictamente necesario. Permitir además hooks opcionales de entrada, actualización, dibujo y acción para mecánicas especiales. Probarlo con una sola escena nueva o prototipo aislado.

La decisión de implementarlo debe coincidir con una necesidad real de contenido nuevo.

## MENSAJE PARA EL ARQUITECTO

La estrategia para acelerar Senku no es programar más deprisa dentro del mismo patrón, sino hacer que **cada cosa ya resuelta se convierta en una pieza reutilizable**.

Preservar:
- el juego pequeño;
- Canvas;
- controles actuales;
- assets externos;
- posibilidad de experimentar.

Cambiar progresivamente:
- escenas definidas en muchos sitios → escenas registradas en un solo contrato;
- solicitudes de arte aisladas → paquetes por escena;
- esperar al arte → prototipo jugable primero;
- investigar cada detalle → investigar sólo capacidades nuevas;
- rehacer niveles viejos → estrenar mejoras en niveles nuevos cuando tenga sentido.

Con este enfoque, cada país puede ser técnicamente más rico que el anterior sin que el costo de desarrollar cada nueva escena crezca al mismo ritmo.
