# Vintage Telnet — Preparación de base de datos y primer vertical slice jugable

**Fecha:** 2026-09-21  
**Preparado por:** Integrador y Publicador HTML — Vintage Telnet  
**Objetivo:** preparar la transición de la demo local del cliente HTML a una primera experiencia realmente persistente y autoritativa.

## Principio

El navegador no guarda el mundo vivo.

La arquitectura objetivo sigue siendo:

```text
Teléfono / iPad / computadora
        ↓
cliente HTML
        ↓
servidor Vintage Telnet
        ↓
SQLite persistente
        ↓
Raspberry Pi
```

El cliente envía intenciones. El servidor decide y guarda el resultado.

## Hallazgo importante

Existe una entrega preparada en:

`claude/vintage-telnet-server-v2`

Commit revisado:

`ca7be621cc7862cf4cbb7a34eaea0a787820cf63`

La entrega ya implementa una base real en Python + Flask/Waitress + SQLite y reporta:

- esquema SQLite versionado;
- cuentas y sesiones;
- contraseñas hasheadas;
- aprobación/rechazo/eliminación por Dungeon Master;
- elección de una de las cinco especies confirmadas;
- pueblo inicial según especie;
- ubicación persistente;
- movimiento N/S/E/O;
- chat local por sala;
- presencia básica de otros jugadores;
- API estructurada para identidad y sala;
- 19 pruebas reportadas como correctas;
- persistencia que sobrevive reinicio de proceso.

La rama no debe integrarse automáticamente: actualmente está divergida respecto a `main` porque `main` avanzó con arte/documentación. Debe revisarse y actualizarse contra el HEAD vigente antes de publicar.

## Primer vertical slice jugable real

No necesitamos esperar combate para dejar de ser una demo.

La primera versión real debe permitir este recorrido completo:

1. El jugador abre Vintage Telnet.
2. Crea una cuenta.
3. La cuenta queda pendiente.
4. El Dungeon Master la aprueba.
5. El jugador vuelve a entrar.
6. Elige una especie confirmada.
7. El servidor asigna su pueblo inicial.
8. El cliente muestra la sala actual recibida del servidor.
9. El jugador se mueve N/S/E/O.
10. El servidor valida el movimiento y guarda la nueva ubicación.
11. Dos jugadores en la misma sala pueden verse y hablar por chat local.
12. El jugador cierra el navegador.
13. Al volver a entrar, conserva identidad, especie y ubicación.

Esto será considerado **jugabilidad real** porque el estado deja de depender de JavaScript local y pasa a persistencia autoritativa.

## Datos mínimos que sí deben ser persistentes desde esta etapa

### Jugador

Como mínimo:

- identificador estable;
- nombre/login;
- hash de contraseña;
- estado de cuenta: pendiente/aprobada/rechazada/eliminada;
- especie elegida;
- sala/ubicación actual;
- fecha de creación;
- metadatos de sesión necesarios.

### Sesiones

- sesión revocable;
- vencimiento;
- jugador asociado;
- revocación inmediata al retirar acceso.

### Mundo inmediato

El contenido canónico del mundo no debe duplicarse innecesariamente en SQLite si puede estar versionado como datos/código del servidor.

La base sí debe guardar el **estado vivo** que cambia durante el juego.

### Chat local inicial

- sala;
- jugador;
- mensaje;
- fecha/hora;
- cantidad reciente limitada para no crecer sin control.

## Datos que deben prepararse conceptualmente pero NO inventarse todavía

El esquema deberá poder crecer posteriormente para:

- inventario;
- equipo;
- progreso;
- atributos;
- clases/especializaciones;
- poderes y recursos de poderes;
- descubrimientos del mapa;
- Arcanes;
- monstruos persistentes;
- derrotas de monstruos únicos;
- PvP;
- objetos físicos/Forja;
- eventos persistentes del mundo.

No deben crearse reglas o columnas definitivas para estos sistemas hasta que Jugabilidad/Historiador definan su significado.

## Regla de diseño de base de datos

Evitar una tabla `players` gigantesca con una columna por cada sistema futuro.

Preferir separar por dominio conforme esos sistemas aparezcan, por ejemplo:

```text
players
sessions
room_messages

# futuros, cuando exista definición aprobada:
player_progress
player_inventory
player_equipment
player_discoveries
player_arcanes
world_entities
world_events
forge_validations
```

Los nombres anteriores son una guía estructural, no una orden de implementación inmediata.

## Contrato mínimo que necesita el cliente HTML

### Identidad

`GET /api/me`

Debe permitir al cliente conocer, como mínimo:

- si hay sesión;
- estado de cuenta;
- identidad;
- especie;
- ubicación actual.

### Sala actual

`GET /api/room`

Debe devolver estado estructurado, no obligar al cliente a interpretar texto narrativo para descubrir:

- id de sala;
- nombre;
- descripción permitida;
- salidas disponibles;
- otros jugadores presentes;
- mensajes recientes permitidos.

### Acciones

El cliente deberá enviar intenciones canónicas al servidor.

Ejemplos:

```text
norte
sur
este
oeste
mirar
decir
```

Un botón y un comando escrito deben terminar en la misma intención de servidor.

## NECESIDAD DEL SERVIDOR

Para conectar el cliente móvil actual se necesita cerrar un contrato estable para:

- autenticación desde el cliente;
- CSRF/sesión;
- bootstrap inicial;
- movimiento;
- refresco de sala;
- chat local;
- errores estructurados;
- resincronización después de reconexión.

No debe conectarse `vintage-telnet.html` directamente a endpoints improvisados antes de que ese contrato quede claro.

## NECESIDAD DE JUGABILIDAD

Para este primer vertical slice NO hace falta definir todavía combate, daño, experiencia o economía.

Sí hace falta respetar lo ya confirmado:

- mundo persistente;
- movimiento cardinal;
- especie inicial;
- pueblos confirmados;
- información descubierta limitada a lo que corresponda;
- mismo comportamiento para botón y comando.

## Requisitos de seguridad y persistencia antes de Raspberry

Antes de considerar la base lista para el mundo vivo:

- migración de esquema versionada;
- backup antes de migraciones;
- restauración probada;
- datos fuera del checkout;
- SQLite con integridad verificada;
- sesiones revocables;
- secretos fuera del repositorio;
- pruebas HTTP reales;
- prueba de reinicio del proceso;
- prueba de dos jugadores;
- prueba de reconexión conservando ubicación.

## Secuencia recomendada de trabajo

### Fase 1 — revisar servidor V2
Responsable: Desarrollador de Servidor + Arquitecto.

- actualizar la rama contra el `main` vigente;
- verificar que los cambios recientes de arte/documentación no se pierdan;
- ejecutar nuevamente las 19 pruebas;
- revisar esquema y migración v1 → v2;
- revisar backup/restauración.

### Fase 2 — aprobar el contrato cliente-servidor
Responsables: Arquitecto + Servidor + Integrador HTML.

Congelar el contrato mínimo para:

- login/registro;
- estado pendiente/aprobado;
- especie;
- sala;
- movimiento;
- chat.

### Fase 3 — conectar el HTML
Responsable: Integrador/Desarrollador HTML.

Retirar de la ruta principal la simulación local de:

- ubicación;
- movimiento;
- presencia;
- chat.

Reemplazarla por respuestas del servidor manteniendo:

- terminal negra/verde;
- controles táctiles;
- entrada por comando;
- misma acción para botón/comando;
- diseño responsive actual.

### Fase 4 — prueba real
Primero fuera de Raspberry:

```text
crear cuenta
→ aprobar
→ elegir especie
→ aparecer en pueblo
→ moverse
→ otro jugador aparece
→ hablar
→ cerrar
→ volver
→ conservar ubicación
```

Después repetir el mismo recorrido en Raspberry.

## Qué NO debe hacerse todavía

- No implementar combate con números inventados.
- No crear experiencia/niveles sin criterios aprobados.
- No poblar masivamente el mundo antes de asegurar backup/restauración.
- No guardar estado autoritativo en localStorage.
- No exponer la Raspberry a Internet sin resolver HTTPS y acceso seguro.
- No convertir la geografía placeholder de pruebas en canon.

## Criterio de aceptación del primer hito jugable

El hito estará cumplido cuando Javier/Matías puedan realizar desde un teléfono:

**Abrir → entrar → aparecer en el lugar persistente → moverse → ver a otro jugador → enviar un mensaje → cerrar → volver a entrar → continuar donde quedaron.**

Ese será el primer momento en que Vintage Telnet deje de ser solamente una demostración de interfaz y empiece a funcionar como mundo persistente real.
