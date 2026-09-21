# Vintage Telnet — Primer slice jugable real

**Fecha:** 2026-09-21  
**Prioridad de Javier:** ENTRAR → ELEGIR ESPECIE → MOVERSE POR EL PUEBLO  
**Estado:** LISTO PARA IMPLEMENTACIÓN COORDINADA

## Objetivo

La siguiente versión jugable de Vintage Telnet debe concentrarse únicamente en tres capacidades reales y persistentes:

1. Entrar al juego con una cuenta válida.
2. Elegir una especie jugable confirmada.
3. Aparecer en el pueblo inicial correspondiente y moverse dentro de ese pueblo.

Todo lo demás queda fuera de este primer slice salvo lo estrictamente necesario para sostener estas tres funciones.

## Alcance funcional

### 1. Entrada

El jugador debe poder:

- crear una cuenta;
- iniciar sesión;
- conservar una sesión válida;
- volver a entrar sin crear un personaje nuevo;
- recibir claramente el estado de su cuenta si todavía requiere aprobación del Dungeon Master.

La identidad y sesión pertenecen al servidor.

### 2. Elección de especie

Después de estar habilitado para jugar, el jugador debe elegir una sola especie entre las cinco confirmadas:

- Humanos;
- Felaryn;
- Dravak;
- Marevyn;
- Vesperi.

La selección debe presentar únicamente información canónica de `SPECIES.md` y `CONFIRMED_IDEAS.md`.

No mostrar al jugador las referencias internas de diseño usadas para crear cada especie.

La selección debe guardarse en la base de datos y no repetirse en cada conexión.

Pueblos iniciales confirmados:

- Humano → Valdren
- Felaryn → Khariel
- Dravak → Brumak
- Marevyn → Narevia
- Vesperi → Velmora

### 3. Movimiento dentro del pueblo

Después de elegir especie:

- el jugador aparece en una sala inicial de su pueblo;
- puede desplazarse con Norte / Sur / Este / Oeste;
- botones y comandos escritos deben enviar la misma intención;
- el servidor valida si existe salida;
- el servidor actualiza la ubicación persistente;
- al cerrar y volver a entrar, el jugador continúa en su última sala.

## Pueblo mínimo para la primera prueba

Cada pueblo inicial necesita únicamente una microzona suficiente para probar navegación real.

La estructura mínima debe reflejar solo elementos ya confirmados:

- un punto central/comunitario;
- acceso a una forja o taller;
- acceso a un lugar de alimentos/comercio;
- caminos internos suficientes para probar N/S/E/O.

No crear todavía una ciudad completa.

La geometría exacta y los textos definitivos pertenecen al Historiador. Si todavía no existen descripciones canónicas suficientes, el servidor puede usar identificadores técnicos claramente marcados como provisionales para pruebas, pero la interfaz publicada para jugadores no debe presentar geografía provisional como canon definitivo.

## Persistencia mínima requerida

La base de datos debe conservar como mínimo:

- ID estable del jugador;
- credenciales seguras;
- estado de cuenta;
- especie;
- pueblo inicial derivado de la especie;
- sala actual;
- sesión revocable;
- timestamps necesarios para operación.

No guardar este estado como autoridad en `localStorage`.

## Contrato mínimo cliente-servidor

El HTML necesita un contrato estable para:

### Identidad
`GET /api/me`

Debe permitir distinguir como mínimo:

- sin sesión;
- pendiente de aprobación;
- aprobado sin especie;
- aprobado con especie;
- ubicación actual.

### Selección de especie
Una acción autoritativa del servidor para elegir especie exactamente una vez.

Debe responder con:

- especie confirmada;
- pueblo inicial;
- sala inicial;
- estado actualizado del jugador.

### Movimiento
Una acción autoritativa para:

- norte;
- sur;
- este;
- oeste.

Debe responder estructuradamente con:

- acción aceptada o rechazada;
- sala anterior;
- sala actual;
- nombre/descripción permitida;
- salidas disponibles.

El cliente no debe deducir la ubicación interpretando texto narrativo.

## Interfaz HTML

El cliente móvil actual debe conservar:

- terminal negro + verde;
- carcasa HTML;
- controles táctiles;
- entrada por comando;
- diseño responsive;
- arte HTML modular cuando se integre.

Para este slice:

- la cruceta N/S/E/O debe dejar de mover una demo JavaScript local;
- debe enviar la intención al servidor;
- la terminal debe mostrar el resultado devuelto por el servidor;
- al recargar, debe reconstruir pantalla desde el estado del servidor.

## Fuera de alcance

No bloquear este primer slice esperando:

- combate;
- PvP;
- clases;
- estadísticas;
- niveles/experiencia;
- inventario;
- equipo;
- Arcanes;
- poderes;
- chat;
- economía;
- monstruos;
- secretos;
- mapa completo.

Esos sistemas vendrán después.

## Prueba de aceptación

El slice está aprobado cuando Javier/Matías puedan hacer desde teléfono:

```text
abrir Vintage Telnet
→ iniciar sesión
→ elegir especie
→ aparecer en su pueblo
→ moverse N/S/E/O por varias salas
→ cerrar el navegador
→ volver a entrar
→ aparecer exactamente en la última sala guardada
```

Debe comprobarse con al menos dos especies distintas para confirmar que cada una inicia en su pueblo correspondiente.

## Responsabilidades

### Desarrollador de Servidor
- actualizar/rebasar su entrega V2 sobre el `main` vigente sin perder trabajo reciente;
- conservar SQLite versionado y migraciones;
- cerrar endpoints/contrato para identidad, especie y movimiento;
- garantizar persistencia real.

### Historiador
- proporcionar o validar las microzonas iniciales de los cinco pueblos si faltan detalles narrativos;
- no definir mecánicas.

### Integrador HTML
- conectar el cliente al contrato aprobado;
- retirar la simulación local de identidad/especie/ubicación/movimiento;
- conservar una sola acción lógica para botón y comando;
- publicar solo con autorización de Javier.

### Arquitecto
- validar el contrato cliente-servidor;
- evitar duplicación de estado y mantener servidor como autoridad.

## Prioridad

**P0 — primer objetivo jugable real de Vintage Telnet.**

Hasta completar este flujo, no ampliar el alcance con sistemas secundarios que retrasen la prueba de persistencia y movimiento.
