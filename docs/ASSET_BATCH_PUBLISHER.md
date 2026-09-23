# Publicador de Assets por Lote — Vintage Telnet

Implementación técnica de Issue #52 y de la arquitectura definida en PR #51.

## Alcance v1

Rutas permitidas:

- `assets/vintage-telnet/locations/`
- `assets/vintage-telnet/species/`
- `assets/vintage-telnet/maps/`

Formatos raster:

- PNG
- WebP
- JPG/JPEG

Límites iniciales conservadores:

- máximo 8 MiB por archivo;
- dimensiones entre 1×1 y 8192×8192;
- nombres en minúsculas con letras, números, `.`, `-` y `_`;
- ZIP/Base64 no son assets finales.

Estos límites son de transporte/validación, no decisiones artísticas.


## Flujo oficial desde Google Drive: máster aprobado → derivado runtime

Para Vintage Telnet, Google Drive funciona como **archivo artístico y carril de aprobación**; GitHub conserva el **asset técnico que consume el juego**.

Carpeta de entrada autorizada para el Publicador:

`MatiasGameLab - Arte/02_APROBADO/Vintage-Telnet`

El Publicador **NO debe tomar archivos desde `01_ENTREGAS` ni `03_RECHAZADO`**.

Secuencia obligatoria:

1. localizar en `02_APROBADO/Vintage-Telnet` el archivo exacto aprobado por Dirección de Arte;
2. registrar Drive file ID, nombre, dimensiones, bytes y SHA-256 del máster;
3. descargar el archivo sin modificarlo;
4. recalcular SHA-256 después de descargar y exigir coincidencia exacta con el hash aprobado;
5. conservar ese archivo como **máster artístico**; no recomprimirlo ni reemplazarlo;
6. generar a partir de él el **derivado runtime** apropiado para web;
7. calcular y registrar un SHA-256 nuevo para el derivado;
8. ejecutar `publish-assets.py --dry-run` sobre el derivado;
9. si pasa, ejecutar la publicación normal a una rama de entrega;
10. dejar GitHub Actions como segunda validación técnica antes de integración.

### Regla de hashes

El hash aprobado por Dirección de Arte identifica el **máster de Drive**.

Ejemplo:

`valdren.png` en Drive:
`sha256:4f2a03c3512757540f4d96b5bc48aabfe9f88e35cbc3d84646216c718eb5ea9c`

El WebP generado para el juego tendrá necesariamente otro hash. Eso es correcto.

Nunca se debe:
- alterar el PNG y seguir presentándolo como si conservara el hash aprobado;
- exigir que el WebP tenga el mismo hash que el PNG;
- recomprimir manualmente el máster para superar un problema de transporte;
- sustituir silenciosamente el archivo de `02_APROBADO`.

La trazabilidad correcta es:

`hash máster aprobado → conversión determinista → hash derivado runtime → commit Git`.

## Perfil inicial de conversión para ilustraciones contextuales

Para ilustraciones raster grandes de localizaciones/escenas de Vintage Telnet, mientras no exista un perfil específico distinto aprobado:

- fuente: PNG máster aprobado;
- salida runtime: **WebP**;
- espacio/color de trabajo: RGB;
- conservar las dimensiones originales salvo instrucción técnica explícita de redimensionado;
- calidad WebP inicial: **82**;
- esfuerzo/método del encoder: **6** cuando el encoder usado lo soporte;
- no eliminar transparencia cuando el asset la requiera;
- verificar visualmente el resultado antes de publicar;
- registrar dimensiones, bytes y SHA-256 del WebP generado.

Este perfil parte del piloto técnico de Vaisgard y funciona como **baseline v1**, no como regla eterna. Si las pruebas en móvil/tablet/escritorio demuestran que otro nivel de calidad o tamaño es mejor, se cambia el perfil de publicación; el PNG máster permite regenerar el derivado sin pérdida acumulativa.

### Excepciones

No aplicar automáticamente esta conversión a:
- pixel art que deba mantenerse exacto;
- imágenes cuyo destino final aprobado siga siendo PNG;
- assets que necesiten transparencia o fidelidad especial y tengan un perfil específico;
- cualquier archivo para el que Dirección de Arte o Arquitectura haya dejado instrucciones técnicas distintas.

En esos casos manda el perfil específico del asset.

### Responsabilidad del operador

La **conversión de calidad forma parte del trabajo del Publicador/operador técnico antes de subir el asset a GitHub**.

El Artista entrega y conserva el máster de máxima calidad.  
Dirección de Arte aprueba el máster.  
El Publicador prepara el derivado web y lo publica.

Por tanto, ante un PNG aprobado demasiado grande para el transporte directo por API, la respuesta correcta no es degradar el máster ni declarar bloqueo definitivo si el destino runtime previsto es WebP. La respuesta correcta es generar localmente el derivado WebP autorizado, verificarlo, registrarlo y publicar ese derivado.

## Dry-run obligatorio antes de publicar

Carpeta:

```bash
python tools/publish-assets.py /ruta/al/lote \
  --target assets/vintage-telnet/locations/ \
  --dry-run
```

Manifiesto:

```json
{
  "target": "assets/vintage-telnet/locations/",
  "replace": false,
  "files": [
    {"source": "vaisgard.webp", "name": "vaisgard.webp"}
  ]
}
```

```bash
python tools/publish-assets.py batch.json --dry-run
```

## Publicación local

Después de revisar el dry-run, ejecutar el mismo comando sin `--dry-run`.

Requisitos:
- checkout Git local;
- estar en una rama distinta de `main`/`master`;
- árbol de archivos rastreados limpio.

El script:
1. valida todo el lote;
2. no escribe nada si un archivo falla;
3. copia el lote;
4. hace `git add`;
5. crea un único commit local;
6. imprime rutas, dimensiones, bytes, hashes, hash de lote y SHA de commit.

No hace `git push`, no crea PR, no mergea y no despliega.

## Reemplazos

Un destino existente se rechaza por defecto.

`--replace` (o `"replace": true` en el manifiesto) habilita reemplazo **solo localmente** cuando exista autorización explícita.

En v1, GitHub Actions rechaza modificaciones/eliminaciones de assets existentes. Esto mantiene el piloto seguro; un flujo verificable de autorización de reemplazos debe diseñarse antes de permitirlos en PR automáticamente.

## GitHub Actions

`.github/workflows/asset-validation.yml` se ejecuta en Pull Requests que toquen assets o el propio publicador.

Revalida:
- allowlist;
- formatos;
- legibilidad;
- dimensiones;
- peso;
- nombres;
- prohibición de ZIP/Base64;
- que el PR de assets solo añada archivos nuevos;
- que una entrega de assets no mezcle cambios fuera de la superficie técnica autorizada.

También ejecuta la suite sintética del publicador.

El workflow usa solo `contents: read`. No necesita secretos ni acceso a Raspberry.

## Piloto Vaisgard

Después de que esta implementación y sus pruebas queden verdes, el primer asset real debe ser:

`assets/vintage-telnet/locations/vaisgard.webp`

No publicar todavía el resto del lote artístico. Primero deben completarse publicación, Actions, integración HTML y prueba en teléfono/tablet/escritorio.

## Lo que esta herramienta NO hace

- no genera imágenes;
- no decide canon ni calidad artística;
- no escribe HTML/JS/CSS;
- no toca servidor, SQLite, Ollama, systemd o Raspberry;
- no publica directamente a `main`;
- no guarda tokens.
