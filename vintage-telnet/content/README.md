# Vintage Telnet — contenido público versionado

Esta carpeta es el carril técnico para contenido **público y versionado** de Vintage Telnet. No contiene todavía geografía, narrativa ni canon real: Historiador y Narrador lo poblarán después.

## Principios

- GitHub conserva únicamente contenido que puede ser público.
- El servidor carga e interpreta este contenido; el HTML no descarga la historia completa.
- Estado vivo, SQLite, secretos operativos y contenido realmente reservado viven fuera de esta carpeta.
- Los IDs técnicos deben ser estables, no traducidos y no reutilizados.
- Antes de integrar contenido se ejecuta: `python scripts/validate-vintage-content.py`.

## manifest.json

Formato mínimo:

```json
{
  "schema_version": 1,
  "content_version": "0.0.0",
  "files": []
}
```

`files` contiene rutas JSON relativas a esta carpeta, por ejemplo `settlements/test-settlement.json`. El validador exige que la lista coincida exactamente con los JSON públicos presentes, excepto `manifest.json` y archivos bajo `schema/`.

`content_version` usa formato `MAJOR.MINOR.PATCH`.

## Formatos soportados por el validador

Los ejemplos siguientes son **estructurales**. Los IDs son ficticios y no representan canon.

### Pueblo / asentamiento

Archivo bajo `settlements/*.json`:

```json
{
  "id": "test_settlement",
  "name": "Test Settlement",
  "starting_room": "test_room_a",
  "rooms": [
    {
      "id": "test_room_a",
      "settlement": "test_settlement",
      "name": "Test Room A",
      "description": "Synthetic room description.",
      "exits": {"north": "test_room_b"},
      "tags": []
    }
  ]
}
```

### Especies

`species.json`:

```json
{
  "species": [
    {
      "id": "test_species",
      "name": "Test Species",
      "starting_settlement": "test_settlement",
      "starting_room": "test_room_a"
    }
  ]
}
```

La relación especie → pueblo/sala inicial es técnica; este ejemplo no define ninguna especie real ni asignación canónica.

### Narrativa

Archivo bajo `narrative/*.json`:

```json
{
  "narrative": [
    {
      "id": "test_narrative_event",
      "room": "test_room_a",
      "trigger": "first_entry",
      "once_per_player": true,
      "text": "Synthetic test text.",
      "requires": [],
      "sets": []
    }
  ]
}
```

El Narrador decide textos y necesidades narrativas. El servidor decidirá cómo interpretar triggers cuando esa capacidad exista.

## Qué valida la herramienta

- JSON válido;
- manifest presente y coherente;
- versión de esquema soportada y `content_version` válida;
- rutas del manifest seguras, existentes, únicas y completas;
- campos obligatorios no vacíos;
- IDs únicos entre entidades públicas cargadas;
- salidas hacia salas existentes;
- direcciones de salida limitadas a `north`, `south`, `east`, `west` en schema v1;
- narrativa hacia salas existentes;
- sala inicial de cada pueblo existente y perteneciente a ese pueblo;
- pueblo/sala inicial de cada especie existente cuando `species.json` exista;
- ausencia de referencias explícitas a `private-content` desde archivos públicos.

## Ejecución

Desde la raíz del repositorio:

```bash
python scripts/validate-vintage-content.py
```

Para pruebas o staging:

```bash
python scripts/validate-vintage-content.py --content-dir /ruta/al/content
```

Código de salida `0` significa contenido válido; cualquier error devuelve un código distinto de cero.


## Contrato v1 relevante

Para `schema_version: 1`:

- la descripción pública básica de una sala vive inline en `description`;
- no se usa `description_id` en P0;
- las únicas direcciones de `exits` válidas son `north`, `south`, `east`, `west`.

Esto sigue la arquitectura vigente de PR #8.
