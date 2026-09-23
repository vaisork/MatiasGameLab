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
