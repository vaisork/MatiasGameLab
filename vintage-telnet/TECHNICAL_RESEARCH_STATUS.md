# Vintage Telnet — Estado técnico inicial para Investigación

**Revisión:** 2026-09-20
**HEAD revisado al iniciar la función:** 2f42afd48c183356e200a208ecef8a36b872994d

## COMPONENTES QUE YA EXISTEN

1. **Cliente web público:** vintage-telnet.html existe como pantalla inicial “En construcción”. Está preparado visualmente como puerta de entrada, pero declara expresamente que todavía no conecta con la Raspberry Pi.
2. **Documentación de jugabilidad:** GAMEPLAY.md contiene criterios mecánicos ya confirmados.
3. **Documentación de mundo/narrativa:** WORLD.md y sus documentos asociados contienen canon, regiones, asentamientos, historia y coordinación narrativa.
4. **Cola de investigación:** RESEARCH_REQUESTS.md permite que especialistas pidan investigación directamente.
5. **Arquitectura conceptual acordada:** teléfono/iPad/computadora → cliente web → servidor Vintage Telnet → Raspberry Pi → estado persistente.
6. **Flujo de desarrollo acordado:** ramas de entrega para servidor; prueba real posterior en Raspberry; integración a main solo mediante el flujo autorizado.

## COMPONENTES TÉCNICOS QUE NO APARECEN TODAVÍA EN EL REPOSITORIO

En la revisión actual no aparece código de servidor de Vintage Telnet, esquema de base de datos, protocolo cliente-servidor, autenticación, servicio Linux, scripts de despliegue, configuración de Raspberry, pruebas de servidor ni documentación técnica específica adicional. Por tanto, no debe asumirse que alguna tecnología concreta de backend ya está implementada.

## DECISIONES TÉCNICAS YA TOMADAS

- El navegador no será autoridad del personaje ni del mundo.
- El mundo debe ser persistente.
- La Raspberry Pi ejecutará el servidor/estado vivo previsto.
- El cliente debe poder utilizarse desde teléfono, iPad/tablet y computadora.
- GitHub es fuente de verdad del código/documentación, no del estado vivo.
- Los cambios de servidor se prueban realmente en Raspberry antes de afirmar compatibilidad.
- No se deben exponer secretos ni abrir servicios domésticos indiscriminadamente.

## PREGUNTAS TÉCNICAS ABIERTAS

- Lenguaje/runtime del servidor.
- HTTP, WebSocket o combinación y formato del protocolo.
- Modelo de conexión/reconexión.
- Identidad, autenticación y sesiones.
- Modelo de datos persistente y elección de base de datos.
- Transacciones/concurrencia para varios jugadores y eventos únicos.
- Modelo de habitaciones, criaturas, inventario, descubrimientos y estado global.
- Logs, backups, restauración y recuperación tras fallo.
- Servicio Linux y estrategia de despliegue/actualización.
- Acceso seguro desde Internet sin comprometer la red doméstica.
- Pruebas automáticas y simulación de varios clientes.
- Límites iniciales de rendimiento de la Raspberry real.

## MAPA CORTO DE INVESTIGACIONES PRÓXIMAS

**Prioridad A — antes del primer servidor jugable**
1. Elegir la arquitectura mínima del servidor y comparar runtimes apropiados para la Raspberry.
2. Definir protocolo mínimo cliente-servidor y reconexión.
3. Diseñar persistencia mínima: jugador, posición, inventario y estado compartido.
4. Investigar autenticación/identificación segura para los primeros jugadores.
5. Definir modelo de habitaciones/eventos que soporte contenido del Historiador y Narrador sin hardcode excesivo.

**Prioridad B — antes de exponerlo a Internet**
6. Investigar acceso seguro desde Internet, TLS/reverse proxy o alternativa adecuada.
7. Servicio Linux, logs, backups y restauración.
8. Pruebas de concurrencia y fallos.

**Prioridad C — conforme crezca el mundo**
9. Eventos persistentes y monstruos únicos.
10. Herramientas de administración/Dungeon Master.
11. Estrategia de migraciones de datos y evolución del contenido.

## ESTADO

Este documento es un mapa de investigación, no una decisión de arquitectura. No se ha implementado ni probado servidor alguno en Raspberry como parte de esta revisión.
