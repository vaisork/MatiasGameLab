# HANDOFF — Entrega técnica

## ENTREGA PARA CHATGPT

**Estado:** ENTREGA PREPARADA EN RAMA — NO PUBLICADA

### Desarrollador
Desarrollador Junior de Vintage Telnet

### Estado base
Commit/HEAD de `main` sobre el que se trabajó:
`461446cae98e2d9b58a02c19fa8181e404a07ae4`

### Rama
`junior/vintage-telnet-vertical-slice`

### Objetivo
Construir el primer vertical slice visible y navegable del cliente web de Vintage Telnet sin inventar persistencia, reglas abiertas ni secretos.

### Archivos modificados
- `vintage-telnet.html`
- `AGENTS.md`
- `HANDOFF.md`

### Cambios realizados
- Sustituida la pantalla “en construcción” por un cliente responsive de demostración.
- Texto como área protagonista, con ubicación actual, narración, mensajes importantes y registro de acciones.
- Controles táctiles Norte/Sur/Este/Oeste, Mirar, Atacar y Huir.
- Línea de comandos con Enviar y alias básicos de demostración.
- Botones y comandos pasan por una única función de acción del cliente.
- Mapa HTML de microzona temporal, sin revelar secretos.
- Paneles de Personaje e Inventario sin estadísticas u objetos ficticios.
- Diseño adaptativo para teléfono, iPad/tablet y escritorio; paneles secundarios colapsables en móvil.
- Aviso permanente de “DEMO LOCAL”: no conecta con Raspberry Pi ni guarda progreso.
- Escenario de muestra basado únicamente en elementos públicos existentes de Valdren; la distribución de habitaciones se marca explícitamente como no canónica.
- Función del Desarrollador Junior de Vintage Telnet registrada y firmada en `AGENTS.md`.

### Qué es funcional
- Navegación local dentro de la microzona de demostración.
- Mismo despachador de acción para botones y comandos.
- Entrada de comandos y alias n/s/e/o.
- Mirar, ayuda y apertura/cierre de mapa/personaje/inventario.
- Mensajes visibles ante acciones todavía no resolubles.
- Adaptación CSS a pantallas pequeñas.

### Qué es solamente demostración
- La microzona y su conectividad local.
- Estado de ubicación en memoria del navegador.
- Contenido del mapa mostrado.
- Registro de acciones de la sesión.
Nada de esto representa persistencia real.

### NECESIDAD DEL SERVIDOR
- Contrato cliente-servidor para acciones canónicas y respuestas estructuradas.
- Autoridad de ubicación, personaje, inventario, combate, mapa descubierto y estado persistente.
- Reconexión/resincronización desde Raspberry Pi.
- Resolución real de ATACAR/HUIR y errores autorizados.

### NECESIDAD DE JUGABILIDAD
- Vocabulario/alias oficiales definitivos.
- Regla de selección de objetivo al ATACAR.
- Resultado y condiciones exactas de HUIR.
- Información exacta que personaje/estado de combate debe mostrar.
- Criterios definitivos de qué descubre y enseña el mapa.

### NECESIDAD NARRATIVA
- Cuando se construya la primera microzona real, definir las descripciones jugables concretas que deban aparecer por habitación/estado, sin utilizar material reservado.

### Pruebas realizadas
- Revisión del HEAD actual de `main` antes de trabajar.
- Verificación de que Senku no fue modificado.
- Revisión del flujo de acciones: botones y comandos llaman al mismo despachador.
- Revisión de controles con altura táctil aproximada de 50–56 px.
- Revisión de media queries para ≤900 px y ≤620 px.
- Verificación de que los paneles secundarios pueden abrirse/cerrarse en móvil y los diálogos cerrarse.
- Verificación de que el HTML no incluye contenido de `SECRETS.md` ni `NARRATIVE_RESERVED.md`.

### Prueba visual para Javier/Matías
1. Abrir la rama/preview de `vintage-telnet.html` en teléfono o iPad.
2. Probar botones N/S/E/O y repetir las mismas acciones escribiendo `norte`, `sur`, etc.
3. Pulsar Mirar, Atacar y Huir y comprobar que la respuesta es comprensible.
4. Abrir/cerrar Mapa, Personaje e Inventario.
5. En teléfono, comprobar que el texto sigue siendo protagonista y que los botones se pulsan cómodamente.
6. Decidir si la estética se siente como “un mundo de texto antiguo usando una pantalla moderna”.

### Riesgos/conflictos
- La rama parte de `461446cae98e2d9b58a02c19fa8181e404a07ae4`. El Integrador debe comparar contra el HEAD de `main` vigente antes de integrar.
- No existe todavía backend real conectado; no presentar la demo como juego persistente.

### Aviso para el Integrador/Publicador
No publicar hasta que Javier diga **“sube”**. Antes de integrar, volver a leer `main`, comparar esta rama y verificar que no haya cambios concurrentes en `vintage-telnet.html`, `AGENTS.md` o `HANDOFF.md`.

**LISTO PARA REVISIÓN:** SÍ  
**LISTO PARA PUBLICAR:** SOLO TRAS AUTORIZACIÓN “sube”
