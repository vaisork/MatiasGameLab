# Especificación — Publicador automático de Assets por Lote

**Fecha:** 2026-09-22  
**Estado:** PROPUESTA DE ARQUITECTURA PARA IMPLEMENTAR  
**Solicitante:** Javier  
**Destinatario principal:** Arquitecto de MatiasGameLab  
**Consumidores posteriores:** Chats de Arte, Pixel Art, Arte HTML, Desarrollo, Integrador

## PROBLEMA

Actualmente generar arte con IA no es el principal cuello de botella. El problema es transportar y subir imágenes una por una al repositorio.

Javier no quiere funcionar como intermediario manual descargando imágenes de una IA y volviéndolas a subir a GitHub.

El repositorio ya establece correctamente que:
- los chats de arte crean/preparan/suben imágenes;
- su frontera normal es `assets/`;
- el arte debe vivir como archivo real en el repositorio;
- desarrollo consume las rutas del repositorio;
- no deben transportarse ZIP/Base64 manualmente entre agentes cuando el repositorio puede ser la fuente común.

Falta una herramienta común y determinista para que los agentes de arte puedan entregar **una imagen o un lote completo** con una sola operación lógica.

## PROPUESTA

Crear un componente del proyecto llamado conceptualmente:

# Publicador de Assets por Lote

Nombre técnico sugerido, a decidir por Arquitecto:
- `tools/publish-assets.py`; o
- `scripts/publish-assets.py`.

No debe ser otro agente que razona. Debe ser preferentemente un **script determinista**, barato y repetible.

Su misión:

> recibir archivos de imagen preparados por un agente, validarlos, colocarlos en rutas permitidas, preparar metadatos y publicar el lote de forma atómica o casi atómica en GitHub.

## PRINCIPIO

**El artista produce; el publicador transporta y valida; GitHub conserva; Desarrollo consume.**

Javier no debe participar en el transporte normal.

## FLUJO DESEADO

```
Agente de Arte
    ↓
genera / recorta / transparenta / nombra
    ↓
carpeta temporal o paquete de entrega
    ↓
Publicador de Assets
    ↓
validación automática
    ↓
previsualización / dry-run del lote
    ↓
una publicación lógica
    ↓
rama/commit de assets
    ↓
verificación
    ↓
repo disponible para Desarrollo
```

## CASO A — UNA SOLA IMAGEN

Para un único PNG/WebP/SVG:
1. validar archivo;
2. validar ruta;
3. comprobar si la ruta ya existe;
4. calcular metadatos;
5. subir;
6. confirmar commit/ruta.

La GitHub Contents API es suficiente para este caso.

## CASO B — LOTE DE IMÁGENES

Ejemplo:
- 8 frames de caminar;
- 12 iconos;
- 20 assets de una población;
- una familia completa de botones.

No deben realizarse 8/12/20 flujos manuales independientes.

El publicador debe:
1. leer todo el lote;
2. validar todo antes de escribir;
3. crear los objetos/blobs necesarios;
4. construir el árbol final;
5. crear **un solo commit de entrega** cuando técnicamente sea posible;
6. verificar que el commit contiene exactamente los archivos esperados.

La Git Data API de GitHub permite el patrón blob → tree → commit → actualización de referencia. Arquitecto/Desarrollo debe decidir si esta implementación se usa directamente o mediante Git local, según el entorno donde viva la herramienta.

## INPUT DEL PUBLICADOR

El publicador debería aceptar:

### Opción 1 — carpeta
```
publish-assets <carpeta> --target assets/senku/gato/
```

### Opción 2 — manifiesto
Un archivo de entrega, por ejemplo:

```json
{
  "project": "senku",
  "target": "assets/senku/gato/",
  "replace": false,
  "files": [
    {"source": "walk_01.png", "name": "walk_01.png"},
    {"source": "walk_02.png", "name": "walk_02.png"}
  ]
}
```

El formato exacto lo decide Arquitecto.

Para lotes complejos se recomienda manifiesto porque hace explícito qué se pretende publicar.

## VALIDACIONES OBLIGATORIAS ANTES DE SUBIR

### Seguridad de ruta
Por defecto solo permitir rutas autorizadas de assets.

Un chat de arte no debe poder usar esta herramienta para escribir:
- HTML;
- JavaScript;
- CSS;
- secretos;
- configuración de servidor;
- documentación ajena.

La frontera de `AGENTS.md` debe seguir vigente.

### Existencia
Si el destino ya existe:
- **rechazar por defecto**;
- permitir reemplazo únicamente con una bandera explícita y una tarea que lo autorice.

Nunca sobrescribir silenciosamente un asset que ya usa el juego.

### Formato
Inicialmente permitir únicamente formatos aprobados, por ejemplo:
- PNG;
- WebP;
- SVG cuando corresponda;
- quizá JPG/JPEG para fondos sin transparencia.

La lista definitiva corresponde al Arquitecto.

### Integridad
Verificar:
- archivo legible;
- extensión compatible con contenido;
- tamaño > 0;
- dimensiones válidas en formatos raster;
- transparencia cuando la tarea la requiera;
- nombres seguros;
- ausencia de nombres duplicados en el lote.

### Peso
Advertir/rechazar imágenes excesivamente pesadas según límites definidos por proyecto.

No introducir Git LFS como requisito para sprites normales.

Si en el futuro existen PSD, TIFF, modelos o fuentes de trabajo enormes, tratarlos como otro problema.

## VALIDACIONES ESPECÍFICAS PARA SPRITES

Cuando el manifiesto declare una animación:
- cantidad de frames;
- dimensiones consistentes cuando deban serlo;
- orden explícito;
- nombres secuenciales;
- transparencia esperada;
- ausencia de frames faltantes.

Ejemplo:
```
senku_walk_01.png
senku_walk_02.png
...
senku_walk_08.png
```

El publicador no decide si el dibujo es bonito. Solo valida coherencia técnica.

## MANIFEST DE ASSETS

El proyecto ya utiliza/prevé manifiestos de contenido en distintas áreas. Para arte conviene que el Arquitecto decida si se mantiene un manifiesto global, uno por carpeta o metadatos de entrega.

Como mínimo, la salida del publicador debe poder informar:
- ruta;
- nombre;
- formato;
- dimensiones;
- bytes;
- transparencia si puede detectarse;
- hash/checksum;
- lote/commit;
- orden de frame cuando aplique.

No es obligatorio convertir toda esa información en un archivo permanente si añade mantenimiento innecesario. Arquitecto debe escoger el mínimo útil.

## DRY RUN

Requisito recomendado:

```
publish-assets ... --dry-run
```

Debe mostrar:
- qué archivos se añadirían;
- qué rutas usarían;
- cuáles fallan;
- cuáles ya existen;
- peso total;
- advertencias.

Sin modificar GitHub.

Esto permite que un agente detecte un error antes de crear 20 archivos incorrectos.

## RESULTADO ESPERADO

Una publicación exitosa debe devolver algo parecido a:

```
ASSET BATCH: OK
files: 8
target: assets/senku/gato/
added: 8
replaced: 0
commit: <sha>
warnings: 0
```

Y para cada archivo, si se necesita:
```
walk_01.png — 24x24 — PNG — alpha
...
```

El agente puede copiar ese resumen a su handoff sin que Javier transporte archivos.

## PUBLICACIÓN: MAIN VS RAMA

El Arquitecto debe conservar las reglas actuales del repositorio.

La herramienta debe soportar publicar sobre una **rama de entrega de assets** cuando el flujo requiera revisión.

No debe convertir “automatizar la subida” en “cualquier agente puede sobrescribir main”.

Recomendación:
- lotes nuevos y claramente delimitados pueden seguir el protocolo que Arquitecto defina para Arte;
- reemplazos de assets usados por el juego merecen revisión;
- el publicador recibe la rama/ref destino como parámetro y no decide permisos por sí mismo.

## ZIP

Un ZIP puede ser cómodo como **input temporal** cuando una IA entrega ocho imágenes juntas.

Pero el ZIP NO debe ser el resultado final que consume el juego.

Flujo:
```
ZIP de entrega
→ extraer en temporal
→ validar
→ publicar PNG/WebP/SVG individuales
→ opcionalmente descartar ZIP
```

Así Desarrollo puede referenciar cada asset directamente.

## BASE64

Base64 es un mecanismo de transporte para APIs, no un formato de trabajo humano.

El agente/publicador puede codificar binarios internamente cuando la API lo necesite.

Javier nunca debería:
- copiar Base64;
- pegar Base64;
- transportar Base64 entre chats.

Y el juego no debe incrustar grandes imágenes Base64 en HTML, coherente con `AGENTS.md`.

## GIT LFS

No se recomienda Git LFS para sprites/PNG normales del juego.

Razones:
- añade configuración y dependencias;
- complica clientes/agentes;
- GitHub Pages y consumidores necesitan considerar punteros LFS;
- no resuelve el problema real de Javier, que es automatizar la entrega.

Reevaluar LFS solo si el repositorio empieza a almacenar archivos fuente realmente grandes.

## ERRORES Y ATOMICIDAD

Idealmente un lote debe ser **todo o nada**.

Si el frame 7 de 8 es inválido:
- no publicar los primeros seis;
- fallar el lote;
- informar exactamente el problema.

Esto evita animaciones incompletas visibles en el repo.

Si se usa Git local, validar antes del commit.
Si se usa Git Data API, construir todos los blobs/tree antes de mover la referencia destino.

## CONCURRENCIA

Antes de publicar:
1. registrar HEAD/ref esperado;
2. validar lote;
3. comprobar que la referencia no cambió si la operación depende de ese HEAD;
4. si cambió, revalidar/reintentar de forma segura.

No sobrescribir trabajo concurrente.

Para rutas nuevas y diferentes el riesgo es pequeño, pero debe existir protección.

## AUTENTICACIÓN

Nunca guardar token GitHub dentro del repositorio.

El publicador debe recibir credenciales desde:
- conexión autorizada del agente;
- variable de entorno/secret store;
- GitHub App;
- o mecanismo que Arquitecto apruebe.

Principio de mínimo privilegio.

## IMPLEMENTACIÓN POSIBLE

### Variante A — Git local

Buena si el agente trabaja en un entorno con checkout del repo:
1. copiar lote;
2. validar;
3. `git add`;
4. un commit;
5. push a rama autorizada.

Ventajas:
- simple;
- Git maneja binarios;
- fácil inspección local.

### Variante B — GitHub API

Buena si el agente no tiene checkout pero sí API:
- una imagen: Contents API;
- lote: Git Data API (blobs/tree/commit/ref).

Ventajas:
- no necesita checkout completo;
- apropiada para agentes cloud.

### Recomendación de arquitectura

Crear **una interfaz única de publicador** y ocultar el backend.

El agente de arte no debería saber si por debajo se usó Git local o API.

Conceptualmente:
```
publish_batch(files, target, branch, replace=false)
```

Luego el backend puede ser:
- local Git;
- GitHub API;
- otro mecanismo futuro.

## NO USAR IA PARA LO DETERMINISTA

No gastar contexto/tokens de un modelo en:
- Base64;
- calcular dimensiones;
- comprobar extensiones;
- ordenar nombres;
- detectar duplicados;
- construir commits;
- generar checksums.

Todo eso debe hacerlo el script.

La IA se usa para:
- crear arte;
- decidir cómo recortar;
- interpretar una petición visual;
- escoger qué assets pertenecen a una entrega.

## INTEGRACIÓN CON LOS AGENTES DE ARTE

Agregar al protocolo de Arte algo equivalente a:

> Cuando entregues más de un asset, utiliza el Publicador de Assets por Lote. No solicites a Javier que descargue y vuelva a subir archivos. Prepara los archivos, ejecuta validación/dry-run, publica el lote en la rama/ruta autorizada y devuelve únicamente el resumen, rutas y commit.

Para un ZIP generado en el chat:

> El ZIP es input del publicador, no entrega final del repositorio.

## CRITERIOS DE ACEPTACIÓN PARA EL ARQUITECTO

La tarea de implementación queda completa cuando pueda demostrarse:

### Prueba 1
Publicar un PNG nuevo.

### Prueba 2
Publicar 8 PNG de una animación en **un solo commit**.

### Prueba 3
Intentar subir un lote donde un archivo es inválido: no se publica ninguno.

### Prueba 4
Intentar sobrescribir una ruta existente sin autorización: rechazo.

### Prueba 5
Dry-run de un lote: muestra resultado sin modificar repo.

### Prueba 6
Intentar escribir fuera de rutas permitidas: rechazo.

### Prueba 7
Publicar lote con nombres/orden de frames y devolver resumen verificable.

### Prueba 8
Comprobar que un desarrollador puede consumir inmediatamente las rutas individuales desde HTML/JS después de integrar el lote.

## TAREA PROPUESTA PARA ARQUITECTO

Definir y asignar la implementación de un:

**Publicador de Assets por Lote — MatiasGameLab**

El Arquitecto debe decidir:
- nombre/ruta final del script;
- backend inicial (Git local o GitHub API);
- política de ramas para Arte;
- formatos permitidos;
- límites de peso;
- esquema mínimo de manifiesto;
- dónde vive la validación;
- cómo se autentica sin secretos en repo.

No debe convertirlo en un servicio complejo si un script pequeño resuelve el problema.

## RESULTADO BUSCADO PARA JAVIER

Flujo actual no deseado:
```
IA genera imagen
→ Javier descarga
→ Javier guarda
→ Javier vuelve a subir
→ agente procesa
→ repetir ×8
```

Flujo objetivo:
```
Javier pide arte
→ IA genera/prepara lote
→ publicador automático valida
→ un commit
→ Desarrollo lo encuentra en repo
```

**Javier sale completamente del transporte de archivos.**


---

## DECISIÓN DE ARQUITECTURA — EJECUCIÓN DEL PUBLICADOR + GITHUB ACTIONS

**Estado:** APROBADO PARA IMPLEMENTAR  
**Decisión:** el Publicador de Assets no depende de la Raspberry Pi.

### Dónde corre cada parte

El flujo se divide en dos capas:

1. **Publicación del lote — entorno del agente/artista**
   - El script `tools/publish-assets.py` (nombre final propuesto) vive en el repositorio.
   - Se ejecuta en el entorno de trabajo que tenga los archivos de imagen y acceso autorizado a GitHub: checkout local, entorno cloud de Claude/Codex/ChatGPT u otro agente compatible.
   - Valida primero en local, ejecuta `--dry-run` y después crea/actualiza una **rama de entrega de assets**.
   - No necesita acceso a Raspberry, SQLite viva, systemd, Ollama ni secretos del servidor.
   - No publica directamente a `main`.

2. **Validación automática — GitHub Actions**
   - Cada Pull Request que modifique rutas de assets autorizadas dispara un workflow de validación.
   - El workflow vuelve a ejecutar validaciones deterministas sobre los archivos ya presentes en la rama.
   - Si falla una validación, el PR queda rojo y no debe integrarse hasta corregir el lote.
   - GitHub Actions **no genera arte**, no decide canon, no selecciona qué imagen es mejor y no reemplaza al Director de Arte.
   - GitHub Actions no despliega automáticamente a Raspberry en esta fase.

### Flujo completo

```
Artista / Director de Arte
    ↓
prepara uno o varios assets
    ↓
entorno del agente ejecuta publish-assets.py --dry-run
    ↓
publish-assets.py publica el lote en rama de assets
    ↓
Pull Request
    ↓
GitHub Actions valida automáticamente
    ↓
revisión de Arte / Arquitectura / Integrador según corresponda
    ↓
merge autorizado a main
    ↓
despliegue normal del juego
    ↓
Raspberry recibe la versión integrada cuando toque desplegar
```

### Qué debe validar GitHub Actions

Como mínimo:

- rutas permitidas;
- extensiones/formato permitidos;
- archivo no vacío y legible;
- dimensiones de raster;
- límites de peso;
- nombres seguros;
- duplicados dentro del lote;
- ausencia de sobrescritura no autorizada;
- consistencia de frames cuando exista manifiesto de animación;
- manifiesto válido cuando se use;
- hash/checksum verificable;
- que no se hayan añadido accidentalmente ZIP/base64 como assets finales;
- que los archivos estén únicamente en áreas autorizadas por el rol.

Para Vintage Telnet, la primera familia de rutas autorizadas será:

```
assets/vintage-telnet/locations/
assets/vintage-telnet/species/
assets/vintage-telnet/maps/
```

La ampliación de rutas debe ser explícita; no usar un permiso genérico que permita escribir en cualquier parte del repositorio.

### Evento inicial de GitHub Actions

Primera implementación recomendada:

```yaml
on:
  pull_request:
    paths:
      - 'assets/**'
      - 'tools/publish-assets.py'
      - 'assets/**/manifest*.json'
```

El workflow debe ser de **validación**, no de publicación autónoma a `main`.

Más adelante puede añadirse `workflow_dispatch` para pruebas manuales, pero no es necesario para el piloto.

### Seguridad

- Usar `GITHUB_TOKEN` del workflow solo con los permisos mínimos necesarios.
- El workflow de validación debería operar con lectura del contenido y checks; no necesita permisos para hacer merge.
- No almacenar PAT/tokens de artistas en el repositorio.
- No compartir secretos de Raspberry con el workflow.
- No permitir que un PR de assets modifique al mismo tiempo código sensible y use el publicador como vía para saltarse revisión.
- El script debe rechazar rutas con `..`, rutas absolutas y destinos fuera de las allowlists.

### Política de ramas

Nombre sugerido para entregas:

```
art/<proyecto>-<lote>
assets/<proyecto>-<lote>
```

Una entrega de arte puede contener uno o muchos archivos, pero debe intentar producir **un solo commit lógico por lote** cuando sea razonable.

Reemplazar un archivo existente requiere autorización explícita y debe quedar visible en el PR. Añadir un archivo nuevo no autoriza a reemplazar otro silenciosamente.

### Papel de Raspberry

La Raspberry **no es el lugar normal donde se publica arte**.

Su responsabilidad empieza después de que una versión aprobada llegue a `main` y toque desplegar el juego. El mismo despliegue normal trae los assets junto con el código correspondiente.

Esto evita:
- dar acceso de producción a agentes de arte;
- mezclar secretos del juego con credenciales de GitHub;
- bloquear producción artística cuando la Raspberry esté apagada o inaccesible;
- convertir el servidor del juego en estación de trabajo.

### Primer piloto obligatorio — Vaisgard

Antes de procesar toda la biblioteca de Vintage Telnet:

1. publicar `vaisgard.webp` desde el entorno del agente usando el publicador;
2. ejecutar dry-run;
3. crear rama/PR;
4. GitHub Actions valida automáticamente;
5. Integrador consume la ruta estable;
6. probar carga/fallback en teléfono, tablet y escritorio;
7. medir peso/carga real;
8. solo después usar el mismo circuito para el lote restante aprobado.

El piloto no fija todavía parámetros definitivos para todas las imágenes; los límites podrán ajustarse con evidencia del primer uso real.

### Criterio de cierre de esta arquitectura

Se considera implementado correctamente cuando:

- un artista puede publicar un lote sin que Javier transporte archivos manualmente;
- el lote entra en una rama, no en `main`;
- GitHub Actions valida de forma automática y reproducible;
- un fallo invalida el PR sin publicar parcialmente;
- un lote válido deja rutas individuales consumibles por Desarrollo;
- la Raspberry no participa en la publicación;
- el despliegue posterior incluye los assets ya integrados sin un segundo proceso manual.
