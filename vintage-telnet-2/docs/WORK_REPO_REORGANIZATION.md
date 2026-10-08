# WORK HANDOFF — Ordenamiento de MatiasGameLab, Vintage Telnet 2 y Senku v2

**Responsable:** Work / Arquitectura operativa  
**Repositorio:** `vaisork/MatiasGameLab`  
**Estado:** ACTIVO  
**Objetivo:** ordenar la repo sin romper Vintage Telnet 2, separar completamente Senku y preparar ambas líneas para desarrollo independiente.

## Punto de partida

La repo contiene dos proyectos distintos que crecieron mezclados:

- **Vintage Telnet 2**: implementación nueva y activa en `vintage-telnet-2/`.
- **Vintage Telnet anterior**: permanece en `vintage-telnet/` como referencia/rollback hasta el cutover formal.
- **Senku**: versión anterior distribuida entre archivos de raíz y `senku/`; Javier construirá una nueva versión de Senku.

No volver a mezclar ambos juegos en la raíz operativa.

## Principio de trabajo

No hacer una limpieza cosmética.

El objetivo es que un agente pueda entrar a la repo y saber inmediatamente:

1. qué proyecto está tocando;
2. qué código está activo;
3. qué documentación manda;
4. qué material es histórico;
5. qué pruebas corresponden;
6. qué operaciones/deploy pertenecen a cada juego.

## Fuentes actuales de verdad

### Vintage Telnet 2
- `vintage-telnet-2/README.md`
- `vintage-telnet-2/CONTENT_CONTRACT.md`
- `vintage-telnet-2/content/world.json`
- `vintage-telnet-2/server/`
- `vintage-telnet-2/client/`
- `vintage-telnet-2/docs/ARCHITECTURE.md`
- `vintage-telnet-2/docs/CONTEXTO_CONTINUIDAD.md`

VT2 se construyó desde cero y no debe volver a depender del motor anterior.

### Vintage Telnet anterior
- `vintage-telnet/`

Tratarlo como **LEGACY / ROLLBACK** cuando VT2 sea validado oficialmente. No añadir trabajo nuevo allí después del corte.

### Senku
- identificar todos los archivos actuales de Senku;
- separar la versión existente como legado recuperable;
- preparar una ubicación limpia para **Senku v2**.

## Trabajo inmediato para Work

### 1. Auditar toda la raíz

Clasificar cada archivo/directorio de raíz como:

- `VT2`
- `VT1_LEGACY`
- `SENKU`
- `SHARED`
- `HISTORICAL`
- `TEMPORARY`
- `UNKNOWN_REVIEW`

Prestar especial atención a:

- HTML sueltos;
- manifests;
- scripts;
- arte;
- herramientas;
- documentación;
- handoffs;
- planes de implementación;
- workflows;
- tests;
- launchers;
- archivos huérfanos.

No mover nada antes de comprobar referencias.

### 2. Separar físicamente los proyectos

Objetivo recomendado:

```text
MatiasGameLab/
├── AGENTS.md
├── README.md
├── .github/
├── docs/
│   ├── shared/
│   └── archive/
├── tools/
├── scripts/
├── vintage-telnet-2/
├── vintage-telnet/          # legacy temporal hasta cutover
└── senku/
    ├── legacy/
    └── v2/
```

No imponer esta forma si una variante más segura preserva mejor imports/workflows, pero mantener la separación conceptual.

### 3. No romper VT2

Antes y después de cualquier movimiento:

- revisar imports;
- rutas de assets;
- rutas del cliente;
- scripts;
- tests;
- systemd;
- operaciones Raspberry;
- GitHub Actions;
- referencias en documentación;
- URLs internas.

VT2 actualmente usa:

- Python server;
- SQLite;
- `client/`;
- `content/`;
- `ops/`;
- `tests/`;
- `review/`.

No hacer cambios de estructura que alteren el deploy sin verificar `ops/RASPBERRY_HANDOFF.md`.

### 4. Limpiar `vintage-telnet-2/review/`

Esta carpeta ya concentra una gran cantidad de evidencia de iteraciones.

Ordenarla por función sin perder trazabilidad. Estructura sugerida:

```text
review/
├── current/
├── narrative/
├── combat/
├── map/
├── ui/
├── 3d/
├── browser/
├── qa/
└── archive/
```

Reglas:
- resultados vigentes/finales en `current/`;
- evidencia histórica por ciclo en `archive/`;
- no borrar pruebas reproducibles;
- conservar referencias usadas por documentación;
- actualizar cualquier ruta rota.

### 5. Crear fronteras de agentes

La raíz `AGENTS.md` debe contener sólo reglas comunes de MatiasGameLab.

Cada proyecto debe tener instrucciones propias:

- `vintage-telnet-2/AGENTS.md`
- `senku/v2/AGENTS.md`

Los agentes de VT2 no deben leer Senku como contexto operativo.
Los agentes de Senku v2 no deben usar canon, assets ni código de VT2 salvo herramientas declaradas explícitamente como compartidas.

### 6. Integrar el Prompt Maestro de Vintage Telnet 2

El Prompt Maestro actualizado de Javier pasa a documentación de visión de VT2.

Debe quedar versionado dentro de:

`vintage-telnet-2/docs/`

Principios obligatorios:

- **LA LECTURA ES EL MUNDO.**
- **EL 3D LO MATERIALIZA.**
- **EL SERVIDOR DECIDE QUÉ ES VERDAD.**
- **EL JUGADOR DESCUBRE EL RESTO.**
- terminal narrativa como protagonista;
- un único estado del mundo;
- mapa/personaje/bestiario derivados del estado del servidor;
- hora, clima, microvida, memoria y descubrimiento forman parte de la experiencia;
- no crear canon 3D paralelo;
- no degradar jugabilidad por añadir representación visual.

Registrar como pendiente explícito de Dirección/Arquitectura:
- armonizar UI moderna/colorida con 3D sobrio/contenido;
- armonizar layout mobile-first con uso adicional de espacio en escritorio.

No resolver esas tensiones silenciosamente.

### 7. Vintage Telnet anterior: preparar relevo

Relacionado con **Issue #649**.

Cuando Javier confirme que VT2 está arriba y validado:

- VT2 pasa a ser única base activa;
- `vintage-telnet/` queda marcado legacy/rollback;
- no asignar nuevas tareas a VT1;
- auditar issues/PRs pendientes;
- clasificar: MIGRAR / RESUELTO EN VT2 / SUPERSEDED / CONTENIDO VÁLIDO / ARCHIVAR;
- preservar rollback;
- no borrar datos de producción.

### 8. Senku v2

No construir Senku v2 todavía salvo instrucción explícita.

Preparar:
- ubicación limpia;
- separación de assets;
- separación de docs;
- separación de tests;
- separación de agentes;
- versión anterior recuperable.

No copiar automáticamente toda la implementación anterior a v2.

### 9. Documentación final obligatoria

Work debe dejar:

- `REPO_STRUCTURE.md`
- `MIGRATION_REPORT.md`
- mapa de proyectos;
- fuentes de verdad por proyecto;
- inventario de material histórico;
- inventario de archivos movidos;
- referencias actualizadas;
- riesgos pendientes;
- procedimiento de rollback.

## Restricciones

- No desplegar a Raspberry sin autorización explícita de Javier.
- No borrar bases de datos, runtime ni credenciales.
- No subir secretos.
- No mezclar VT2 y Senku.
- No migrar contenido por inercia.
- No declarar terminado sólo porque la estructura “se ve limpia”.
- No romper rutas de producción por estética.

## Validación

Antes de entregar:

1. ejecutar tests relevantes de VT2;
2. comprobar referencias internas;
3. comprobar workflows;
4. comprobar launch/start scripts;
5. comprobar que Senku legacy sigue localizable;
6. comprobar que ningún agente nuevo necesita leer documentación histórica para saber qué hacer;
7. comprobar que la raíz de la repo permite identificar ambos proyectos sin ambigüedad.

## Reentrada para Work

Al despertar en Work:

1. leer este archivo;
2. leer `vintage-telnet-2/docs/CONTEXTO_CONTINUIDAD.md`;
3. leer `vintage-telnet-2/README.md`;
4. revisar Issue #649;
5. inspeccionar HEAD actual de `main`;
6. continuar desde el último cambio confirmado, sin repetir auditorías ya documentadas;
7. trabajar de forma autónoma hasta encontrar una decisión realmente bloqueante.

## Criterio de terminado

La reorganización queda terminada cuando:

- VT2 está claramente aislado y sigue funcionando;
- VT1 está identificado como legacy/rollback tras el cutover;
- Senku está claramente separado;
- Senku v2 tiene espacio limpio para comenzar;
- la raíz tiene sólo elementos verdaderamente compartidos;
- documentación activa e histórica están separadas;
- agentes tienen fronteras claras;
- workflows/rutas/tests siguen funcionando;
- existe rollback documentado;
- Javier puede abrir MatiasGameLab y entender su estructura sin investigar el historial del proyecto.
