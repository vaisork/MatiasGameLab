# Vintage Telnet — Estado arquitectónico heredado

**Fecha de auditoría:** 2026-09-21  
**Arquitecto:** Arquitecto de Vintage Telnet y Raspberry Pi  
**Base auditada:** `main` en `956f23285c9314cff2e06ebd58b628f45aa4e7cb`

Este documento conserva el resultado de la primera herencia arquitectónica. No sustituye `GAMEPLAY.md`, `WORLD.md` ni la autoridad creativa de Javier/Matías y sus especialistas.

## Arquitectura vigente

Dirección heredada y conservada:

```text
teléfono / iPad / computadora
        ↓
cliente web
        ↓
servidor autoritativo Vintage Telnet
        ↓
persistencia / mundo compartido
        ↓
Raspberry Pi como entorno real
```

Principios obligatorios:

- el navegador envía intenciones; no es autoridad de personaje, ubicación, inventario, progreso ni mundo;
- código y estado vivo son cosas distintas;
- los datos persistentes viven fuera del checkout y nunca se reemplazan por un deploy;
- GitHub conserva código, documentación, investigaciones, decisiones, pruebas y handoffs;
- Raspberry no es el entorno rutinario de desarrollo.

## Estado real de `main`

### Implementado

- `vintage-telnet.html`: cliente móvil V2 publicado.
- terminal negra/verde separada visualmente de la carcasa HTML café;
- controles táctiles, comando escrito y botones unificados en una función local;
- mapa/paneles de demostración;
- responsive móvil/tablet/escritorio;
- interfaz explícitamente marcada como demo local sin persistencia.

El cliente actual es una **demostración local**. No tiene conexión con un servidor y no representa autoridad persistente.

### Diseñado/documentado, no implementado en `main`

- servidor autoritativo;
- cuentas/sesiones reales;
- persistencia de personajes, posición, inventario, progreso y descubrimientos;
- contrato cliente-servidor;
- chat/presencia;
- combate autoritativo;
- migraciones reales;
- backups operativos;
- servicio Raspberry;
- despliegue real;
- acceso seguro desde Internet;
- automatización CI.

## Entrega histórica de servidor

La rama `codex/vintage-telnet-server` y la PR #1 contienen una implementación 0.1.0 no integrada:

- Python + Flask + Waitress;
- SQLite local fuera del checkout;
- WAL y claves foráneas;
- cuentas con UUID/número y contraseña hasheada con scrypt;
- sesiones revocables y CSRF;
- límite básico de autenticación;
- inspección y backup SQLite;
- unidad systemd endurecida;
- 9 pruebas locales documentadas, incluido reinicio de proceso HTTP.

La rama parte de un `main` antiguo y está muy divergida. **No debe mergearse directamente.**

`ops/RASPBERRY_REPORT.md` continúa como plantilla pendiente. Por tanto, no existe evidencia registrada de despliegue o validación física de esa entrega en Raspberry.

## Decisiones arquitectónicas tras la herencia

### 1. Rescatar, no mergear, la entrega de servidor

Se conservará el diseño útil del prototipo, pero un implementador deberá trasladarlo a una rama nueva nacida del HEAD vigente de `main`, revisar compatibilidad y ejecutar otra vez sus pruebas.

No se trasladarán copias obsoletas de `AGENTS.md`, `HANDOFF.md` ni documentación que contradiga el estado actual.

### 2. Python + Flask/Waitress + SQLite es una base válida para la primera etapa

La combinación ya implementada es suficientemente simple para el tamaño inicial previsto y evita infraestructura innecesaria.

Esto no significa comprometer el proyecto para siempre. Se reevaluará SQLite antes de introducir necesidades que excedan razonablemente un único servidor/escritor o una simulación concurrente mucho mayor.

### 3. HTTP primero; tiempo real solo cuando aporte valor

Registro, login, bootstrap, salud y operaciones no continuas pueden usar HTTP.

WebSocket se añadirá cuando una capacidad real lo necesite —por ejemplo chat/presencia/eventos multijugador en tiempo real—, no por anticipación. No se implementará un protocolo Telnet TCP solo por el nombre del juego.

### 4. Cliente y servidor necesitan un contrato explícito

Botones y comandos escritos deberán convertirse en la misma intención canónica antes de llegar a las reglas del servidor.

La respuesta del servidor será estructurada y podrá incluir texto narrativo más estado permitido para la interfaz. El cliente no inferirá estado autoritativo leyendo texto.

### 5. Preferencia por mismo origen en el entorno real

El cliente publicado en GitHub Pages puede seguir sirviendo como prototipo/portal mientras no exista backend.

Para la versión autenticada real se prefiere servir cliente y API desde el mismo origen HTTPS del entorno Vintage Telnet. Esto reduce complejidad y riesgo de CORS, cookies, CSRF y contenido mixto. La forma concreta de acceso remoto se decidirá antes de exponer la Raspberry a Internet.

### 6. Persistencia antes que contenido masivo

Antes de guardar mundo valioso deben existir:

- esquema versionado;
- migración incremental;
- backup previo a migrar;
- restauración probada;
- directorio de datos separado;
- política de rollback compatible;
- pruebas con datos temporales/anonimizados.

### 7. Raspberry es validación final de entorno, no banco de desarrollo

Primero deben pasar fuera de Raspberry:

- sintaxis/imports;
- unit tests;
- integración HTTP;
- autenticación/sesiones;
- persistencia temporal;
- concurrencia razonable;
- migraciones;
- backup/restauración;
- contratos cliente-servidor;
- regresiones.

Raspberry se reserva para:

- arquitectura ARM/SO/dependencias reales;
- systemd;
- usuario/permisos;
- rutas y almacenamiento;
- puertos/firewall/red;
- conexión desde dispositivos reales;
- reboot y recuperación;
- logs reales;
- rendimiento, memoria, disco y comportamiento del hardware.

## Automatización prevista

Cuando el servidor sea rescatado sobre `main`, crear CI específico para Vintage Telnet:

- ejecución en Pull Requests;
- filtros por rutas de Vintage Telnet;
- suite Python/unittest;
- comprobación de imports/sintaxis;
- integración HTTP local;
- migración y backup/restauración;
- sin desplegar automáticamente a Raspberry.

Se medirá duración y utilidad antes de aumentar frecuencia. No se copiarán workflows de Senku por defecto.

## Huecos de responsabilidad

En `main` sí están registrados y firmados:

- Arquitecto de Vintage Telnet y Raspberry Pi;
- Diseñador de Jugabilidad;
- Historiador y Constructor del Mundo;
- Narrador de Aventuras;
- Psicopedagogía y Experiencia Infantil;
- Investigador Técnico y de Implementación;
- Integrador y Publicador HTML;
- Desarrollador Junior de Vintage Telnet.

No están registrados actualmente en `main`:

- **Desarrollador de Servidor — Vintage Telnet**: existe una firma histórica solo dentro de la rama/PR antigua.
- **Operador Raspberry Pi dedicado**: no existe un agente firmado con esa función.

Por tanto, la siguiente implementación de backend requiere asignar explícitamente un implementador de servidor. La operación Raspberry puede mantenerse separada y solo activarse cuando haya una entrega que realmente necesite hardware.

## Riesgos prioritarios

1. Integrar la PR #1 directamente y reintroducir documentación/arquitectura antigua.
2. Conectar el cliente actual al backend sin definir contrato y autoridad.
3. Empezar a almacenar personajes/mundo antes de tener migraciones y restauración probada.
4. Hacer de Raspberry el lugar donde se descubren errores que podían detectarse localmente.
5. Exponer HTTP/puertos de la Raspberry a Internet antes de resolver TLS, origen, proxy/túnel, registro y protección de autenticación.
6. Mantener backups solo en la misma tarjeta/disco que el mundo vivo.
7. Considerar “servicio activo” equivalente a “juego recuperable después de fallo/reboot”.
8. Permitir que documentación técnica obsoleta sea confundida con `main`.

## Próxima secuencia técnica

1. Asignar un implementador de servidor.
2. Crear rama fresca desde `main`.
3. Rescatar la base Flask/Waitress/SQLite de PR #1 sin sus archivos de coordinación obsoletos.
4. Revalidar las 9 pruebas y actualizar dependencias/documentación.
5. Añadir migración/backup/restore como requisito antes de estado jugable.
6. Definir contrato mínimo cliente-servidor para autenticación + identidad + una acción de prueba.
7. Integrar CI de Pull Request.
8. Solo entonces preparar una entrega instalable para Raspberry y ejecutar pruebas físicas.
9. Investigar acceso seguro remoto antes de cualquier exposición a Internet.

---

**Estado:** herencia arquitectónica completada; no se ha reconstruido el juego ni desplegado servidor.
