# Vintage Telnet — Requisitos de interfaz derivados de Jugabilidad

**Responsable de criterios:** Diseñador de Jugabilidad — Vintage Telnet  
**Estado:** REQUISITOS PARA EVOLUCIÓN DE INTERFAZ  
**Fuente normativa principal:** `vintage-telnet/GAMEPLAY.md`  
**Interfaz real revisada:** `vintage-telnet/server/templates/entry.html`

Este documento no diseña HTML ni arquitectura. Define qué información y acciones necesita poder expresar la interfaz para que la Jugabilidad v1 sea realmente jugable en teléfono, iPad/tablet y computadora.

## 1. Principio rector

La terminal textual sigue siendo el centro de la experiencia.

HTML debe:
- reducir fricción;
- mostrar estado importante sin enterrarlo en el log;
- facilitar acciones frecuentes;
- organizar información compleja;
- no resolver decisiones;
- no revelar secretos, enemigos ocultos, salidas ocultas, pistas o NPCs que el personaje todavía no percibió.

**Una acción del juego puede tener botón y comando, pero ambos deben terminar en la misma intención autoritativa del servidor.**

## 2. Lo que la interfaz actual ya resuelve bien

La versión real ya dispone de:
- login/registro;
- selección de especie;
- terminal negra/verde;
- movimiento N/S/E/O;
- `mirar`;
- caja de comandos;
- separación explícita entre chat mediante `decir <texto>` y comandos;
- intención separada para `observar/examinar`;
- intención separada para `hablar <npc>`;
- botones/paneles preparados para Personaje, Inventario, Poderes y Ayuda;
- Atacar/Huir visibles pero correctamente desactivados mientras no exista combate.

No reemplazar esta base por una interfaz gráfica convencional.

## 3. Corrección inmediata P0 — Ayuda y lenguaje de comandos

El modal de Ayuda visible en `entry.html` todavía afirma que escribir cualquier texto sirve para hablar con personas de la sala. Eso contradice el comportamiento actual del servidor y el criterio psicopedagógico aprobado.

La ayuda debe enseñar de forma coherente:
- `norte/sur/este/oeste` = movimiento;
- `mirar` = volver a leer la situación general;
- `observar <objetivo>` / `examinar <objetivo>` = inspección;
- `hablar <npc>` = conversación con NPC;
- `decir <texto>` = chat con jugadores;
- un comando desconocido **no se publica como chat**.

Este ajuste es P0 antes del playtest narrativo con niños.

## 4. Estado persistente del personaje — panel Personaje

Cuando el backend implemente Jugabilidad v1, el panel Personaje debe poder mostrar como mínimo:

- nombre;
- especie;
- nivel;
- XP/progreso al siguiente nivel cuando exista la regla final;
- PA disponibles;
- ocho atributos;
- HP actual / HP máximo;
- estado narrativo de condición;
- fatiga 0–100 y estado operativo/cansado/agotado;
- máximo una herida persistente relevante tras respawn según v1;
- clase/camino cuando el contenido correspondiente esté implementado.

La **competencia general (CG)** puede permanecer interna y no necesita mostrarse como atributo separado.

En móvil, este panel debe abrirse bajo demanda y no quitar espacio permanente a la terminal.

## 5. Estado esencial visible durante peligro/combate

Durante combate el jugador no debería necesitar abrir Personaje para conocer:
- HP actual/máximo;
- fatiga;
- herida relevante;
- enemigo/amenaza activa;
- si una capacidad está disponible o en recarga.

La forma visual concreta corresponde al Integrador/Arte HTML, pero debe ser compacta.

Fuera de combate puede reducirse u ocultarse parcialmente para devolver protagonismo al texto.

## 6. Acciones de combate

Cuando combate exista, la interfaz debe contemplar:

### Acciones frecuentes
- Atacar;
- Huir;
- Poderes.

### Defensa contextual
Las respuestas:
- Esquivar;
- Bloquear/desviar;
- Resistir

**no deben convertirse en tres botones permanentes equivalentes.**

Deben aparecer cuando el contexto permita una decisión defensiva y respetar:
- equipo;
- posición;
- tipo de ataque;
- información que el personaje realmente percibió.

La interfaz no debe señalar automáticamente cuál es “la mejor”.

### Poderes
El panel debe poder mostrar:
- poder;
- disponible / en recarga;
- categoría/recarga cuando corresponda;
- coste o requisito que el servidor autorice mostrar.

No inventar poderes desde la interfaz.

## 7. Descanso y recuperación

Jugabilidad v1 incluye una acción explícita de descanso.

Cuando esté implementada:
- debe ser accesible sin memorizar un comando raro;
- puede ser botón contextual fuera de peligro;
- debe desaparecer/deshabilitarse cuando el servidor indique que no es válida;
- la interfaz debe comunicar interrupción o recuperación mediante texto y estado, no solo una barra.

## 8. Mirar, observar y examinar

Mantener tres niveles claros:

- **Mirar:** situación general.
- **Observar:** enfocar señales relevantes.
- **Examinar:** detalle de un elemento concreto.

No crear una lista global de objetivos que revele objetos/pistas ocultos.

Cuando el servidor ya haya revelado legítimamente un elemento, HTML puede ofrecerlo como objetivo tocable para observar/examinar, pero debe producir la misma acción canónica que escribir el comando.

## 9. NPCs y conversación

Cuando existan NPCs activos:
- un NPC visible puede presentarse entre los elementos/personas realmente percibidos de la sala;
- tocarlo puede ofrecer **Hablar**, equivalente a `hablar <npc>`;
- chat de jugadores y conversación con NPC deben distinguirse visualmente;
- respuestas de NPC siguen apareciendo principalmente como texto;
- memoria, conocimiento y estado conversacional pertenecen al servidor, no al navegador;
- Presencia puede modificar la recepción según `GAMEPLAY.md`, pero la interfaz no muestra una probabilidad de “persuasión” que sustituya leer la conversación.

## 10. Jugadores presentes y chat

La interfaz puede hacer visible quién está en la misma zona cuando el servidor lo autorice.

Debe quedar inequívoco:
- quién es un jugador;
- quién es un NPC;
- cuándo se está enviando chat;
- cuándo se está ejecutando un comando.

No convertir un error de comando en publicación pública.

Chat global, grupo, comercio y demás acciones sociales siguen pendientes o por fases; no inventarlos desde HTML.

## 11. Arcanes

La interfaz deberá poder evolucionar para soportar la sección 21 de `GAMEPLAY.md`.

Después de que un jugador tenga al menos un Arcane vinculado, debe poder consultar:
- nombre elegido por el jugador;
- descripción/identidad autorizada;
- poder fijo;
- cuál está activo;
- cuáles permanecen en casa.

Reglas:
- máximo 3 vinculados;
- solo 1 acompañante activo;
- solo el activo aporta su poder;
- no mostrar niveles, XP, PA/PP ni árbol de habilidades del Arcane porque no existen;
- el nombre se pide **solo después de establecer el vínculo**;
- antes del vínculo no mostrar un nombre individual inventado.

No es necesario mostrar un botón permanente “Arcanes” a un jugador que todavía no ha desbloqueado esa parte si Arquitectura/Narrativa consideran que adelanta información innecesaria.

## 12. Mapa y descubrimiento

La interfaz necesita un acceso claro a mapa cuando el sistema correspondiente esté listo.

El mapa:
- puede ser más legible que un mapa Telnet clásico;
- solo muestra conocimiento autorizado por el servidor;
- no revela salidas secretas mediante botones deshabilitados, huecos obvios o iconos;
- diferencia lugar conocido de lugar explorado cuando Jugabilidad/Narrativa así lo indiquen;
- puede incorporar información compartida en el futuro sin convertirla automáticamente en descubrimiento personal.

La imagen contextual de Issue #42 es complementaria al mapa y terminal. No sustituye ninguna de las dos.

## 13. Ilustración contextual

Se apoya el piloto de Issue #42 con estas condiciones de Jugabilidad:

- ilustración complementaria, nunca fondo que vuelva ilegible la terminal;
- el juego sigue funcionando si no carga;
- el servidor entrega contexto estructurado; el cliente no deduce ubicación leyendo narración;
- una ilustración no puede revelar enemigo, NPC, ruta, puerta, pista o estado que todavía no fue legítimamente descubierto;
- en móvil debe poder consultarse sin reducir de forma permanente la terminal a un área mínima.

## 14. Diseño responsive con crecimiento de sistemas

La interfaz ya no puede asumir que siempre habrá únicamente movimiento + dos acciones de combate.

A medida que se incorporen sistemas, priorizar **acciones contextuales** sobre añadir filas permanentes de botones.

Prioridad de pantalla en móvil:

1. texto/terminal;
2. estado urgente;
3. acciones inmediatas del contexto;
4. entrada de comando/chat;
5. paneles secundarios bajo demanda.

Personaje, Inventario, Poderes, Mapa, Arcanes y Ayuda deben ser paneles/modales/drawers equivalentes, no competir todos permanentemente por alto de pantalla.

## 15. Contratos que el backend deberá entregar progresivamente

La interfaz no debe calcular reglas de Jugabilidad por su cuenta.

Conforme se implementen sistemas, necesita recibir estructuradamente:
- player_state;
- combat_state;
- available_actions;
- visible_targets;
- visible_npcs;
- players_present;
- cooldowns/powers;
- map/discovery state;
- active_arcane/owned_arcanes;
- contextual illustration id cuando corresponda.

Los nombres definitivos de endpoints/campos corresponden al Arquitecto. La necesidad es que **el servidor sea autoridad y la interfaz renderice posibilidades reales**.

## 16. Prioridades de evolución

### P0 — antes del playtest narrativo
1. Corregir Ayuda para reflejar separación chat/comando.
2. Sustituir placeholders de la ruta de prueba mediante el pipeline narrativo.
3. Integrar al menos una inspección real `observar/examinar`.
4. Integrar al menos un NPC conversable.
5. Mantener comando desconocido fuera del chat.

### P1 — primer bucle RPG real
1. Personaje: nivel, XP, PA, atributos.
2. HP + condición narrativa.
3. Fatiga + herida.
4. Atacar/Huir reales.
5. Defensa contextual.
6. Descanso.
7. Poderes/cooldowns cuando exista contenido.
8. Mapa mínimo progresivo.

### P2 — expansión
1. Inventario/equipo.
2. Arcanes y casa.
3. grupos/cooperación;
4. comercio;
5. sistemas sociales avanzados;
6. ilustraciones contextuales extendidas.

## 17. Regla para implementación

Integrador/Junior no deben inventar una regla para llenar un panel.

Si falta un dato:
- **NECESIDAD DE JUGABILIDAD** si es regla;
- **NECESIDAD DEL SERVIDOR** si la regla existe pero falta backend;
- **NECESIDAD NARRATIVA/HISTÓRICA** si falta contenido.

La interfaz debe poder crecer sin obligar a rehacer el flujo principal de terminal.


## 18. Actualización tras cierre de XP y mapa

Jugabilidad ya cerró las secciones 22 y 23 de `GAMEPLAY.md`.

La interfaz/backend deberá poder incorporar, cuando se implementen:

### Progreso
- nivel actual;
- XP actual;
- XP necesaria para el siguiente nivel;
- XP obtenida por una acción cuando sea relevante;
- aviso comprensible cuando la repetición de una misma familia de criatura reduzca la recompensa.

No mostrar al jugador el nivel de referencia interno del contenido si no existe razón de diseño para hacerlo.

### Evaluar
Para una criatura legítimamente visible:
- acción `evaluar <objetivo>` y equivalente táctil;
- resultado cualitativo: Trivial/Favorable/Comparable/Peligroso/Abrumador o texto narrativo equivalente;
- no mostrar porcentaje de victoria, HP exacto enemigo ni estadísticas ocultas.

### Mapa progresivo
El cliente necesita estados estructurados por personaje:
- lugar desconocido/conocido/visitado;
- ruta desconocida/conocida/recorrida.

Un elemento desconocido no debe renderizarse ni dejar una pista visual de que existe.

El mapa no ejecuta viaje rápido en la v1.

Chat de otro jugador no cambia por sí mismo el estado del mapa.


## 18. Actualización después del cierre §§24–28

Jugabilidad ya cerró dependencias que la interfaz no debe improvisar:

### Combate
- ronda objetivo ~4 s;
- ataque básico automático;
- una intervención sustituye el ataque básico de la siguiente ronda;
- defensas contextuales;
- Atacar/Huir/Esquivar/Bloquear/Resistir usan estado autoritativo de servidor.

### Estado
La interfaz ya puede prever campos reales para:
- nivel;
- XP actual / siguiente nivel;
- PA disponibles;
- PP disponibles;
- HP actual/máximo;
- fatiga 0–100;
- estado operativo/cansado/agotado;
- herida principal;
- cooldowns cuando existan.

### Subida de nivel
- XP sobrante se conserva;
- +2 PA por nivel;
- +1 PP cada 5 niveles;
- PA se gastan fuera de combate;
- el jugador confirma atributo/coste;
- subir nivel no cura por completo.

### Recuperación
Acción canónica:
- `descansar`

Debe ser contextual y usar resultado del servidor. No calcular curación/fatiga en cliente.

### Vocabulario canónico P0/P1
- movimiento: norte/sur/este/oeste;
- mirar;
- observar <objetivo>;
- examinar <objetivo>;
- evaluar <criatura>;
- atacar <objetivo>;
- huir;
- esquivar;
- bloquear;
- resistir;
- descansar;
- decir <texto>;
- hablar <npc>.

La Ayuda y los botones deben usar este vocabulario y no crear sinónimos con reglas propias.
