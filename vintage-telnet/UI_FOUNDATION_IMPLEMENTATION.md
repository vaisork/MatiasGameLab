# VT UI Foundation — implementación Junior

**Rama:** `junior/issue-72-ui-foundation`  
**HEAD base:** `44e89d9c8ab5195c1b60eba7440dd9233d14bfe4`  
**Tareas:** #72 + continuidad coordinada con #74  
**Contrato visual consumido:** #75, comentario `5802236381`

Este archivo fija decisiones de implementación ya autorizadas para evitar reinterpretar la dirección visual mientras #76 (texto canónico) y #77 (matriz de acciones) siguen pendientes. No añade canon ni mecánicas.

## Jerarquía DOM/CSS a preservar

1. Terminal/narración como superficie principal.
2. Estado urgente cuando el servidor lo entregue.
3. Acciones contextuales autorizadas por servidor.
4. Entrada de comando/chat.
5. Ilustración contextual.
6. Paneles secundarios: Personaje, Ayuda, Mapa; Inventario solo cuando #57 esté implementado.

En móvil la ilustración queda en flujo normal, nunca sticky. En escritorio/tablet horizontal puede convivir en lateral, sin crear una tercera columna.

## Tokens y comportamiento visual

- fondo casi negro con matiz verde/azul oscuro;
- terminal verde legible y acento dorado apagado;
- bordes finos y superficies discretas;
- sin glassmorphism, gradientes llamativos, marcos medievales pesados ni iconografía cultural inventada;
- touch targets mínimos de 44 px;
- `:focus-visible` de alto contraste;
- `prefers-reduced-motion` respetado;
- botones disabled con contraste reducido; la razón textual solo se mostrará si el contrato del servidor/Jugabilidad la entrega.

## Ilustración contextual

- se resuelve únicamente desde `room.art`/ID estructurado del servidor;
- nunca inferir ubicación leyendo narración;
- proporción visual aproximada 3:2 con `object-fit: cover`;
- escritorio 180–240 px, tablet 150–210 px, móvil 120–170 px;
- alt y fallback obligatorios;
- sin texto, enemigos, salidas, brújula ni badges superpuestos;
- si falta asset, fallback sobrio; nunca reciclar otra ciudad.

## Componentes técnicos autorizados antes de #76/#77

### Paneles
Usar `dialog`/drawer reusable para Personaje, Ayuda y Mapa. Apertura/cierre accesible por botón, Escape nativo y cierre explícito. No activar Inventario/Poderes.

### Ayuda
Preparar contenedor de tarjetas/bloques escaneables. El contenido final y número exacto de acciones se consume de #77; textos de mundo de #76. No duplicar ahora párrafos inventados.

### Acciones contextuales
Preparar un contenedor único para acciones autorizadas. No crear controles permanentes para capacidades futuras. `Atacar`, `Huir` y `Evaluar` conservan comportamiento existente hasta consumir #77/#73.

### Descansar
La UI podrá enviar la intención `descansar` por la misma ruta autoritativa que el comando. No calcular recuperación en JavaScript. La visibilidad final se ajustará a #77.

### Mapa progresivo
El panel consume `/api/map`; solo renderiza nodos/rutas devueltos por servidor. No calcula adyacencias, no completa topografía y no revela nodos ausentes. Estado de carga, vacío y error deben ser utilizables sin bloquear terminal.

## Responsive

- móvil: una columna; terminal primero; arte no sticky; paneles secundarios modales;
- tablet: máximo dos zonas flexibles;
- escritorio: máximo terminal + lateral contextual/estado;
- no usar ancho extra para agregar widgets no autorizados.

## Dependencias todavía abiertas

- #76: `context_id → texto visible aprobado`; no reemplazar textos canónicos antes de recibirlo.
- #77: matriz de acciones y estructura final de Ayuda; no inventar botones.
- #73: `available_actions` y defensas contextuales; consumir cuando esté disponible.
- #57: inventario/equipamiento; no mostrar slot activo antes de backend real.

## Criterio de pruebas para la implementación

Cuando se modifique `entry.html`, cubrir al menos:
- terminal antes que arte en orden de lectura móvil;
- controles táctiles >= 44 px;
- no existen botones Inventario/Poderes sin capacidad real;
- Mapa solo representa respuesta de `/api/map`;
- fallo de arte o mapa no impide jugar;
- Descansar termina en intención de servidor, no en lógica cliente;
- foco visible y cierre accesible de paneles;
- regresión de login, especie, movimiento, comando y combate existente.

Este contrato es preparación técnica; no autoriza merge, publicación ni despliegue.