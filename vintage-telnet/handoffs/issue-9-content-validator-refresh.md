# Handoff — Issue #9: infraestructura de contenido narrativo (refresh)

**Responsable:** Desarrollador Junior de Vintage Telnet  
**Issue:** #9  
**Base main:** `8faeab8618113806489b77c6769bb853d50d28c1`  
**Rama:** `junior/issue-9-content-validator-refresh`

## Motivo del refresh

PR #10 contenía una entrega funcional, pero quedó muy divergida del `main` vigente y GitHub ya no la consideraba mergeable. Los archivos de #9 nunca entraron a `main`.

Esta rama reconstruye la entrega **desde HEAD actual de main** y reutiliza exactamente los blobs finales ya revisados de PR #10 para:

- `scripts/validate-vintage-content.py`
- `vintage-telnet/content/README.md`
- `vintage-telnet/content/manifest.json`
- `vintage-telnet/tests/test_validate_vintage_content.py`

No se reescribió la lógica ni se añadió canon.

## Alcance

El validador determinista:
- no importa Flask ni arranca servidor;
- valida JSON/manifest;
- detecta IDs duplicados;
- exige campos obligatorios no vacíos;
- valida `description` inline;
- limita salidas v1 a north/south/east/west;
- detecta salidas/narrativa a salas inexistentes;
- valida relaciones especie/pueblo/sala inicial;
- rechaza referencias públicas a `private-content`;
- devuelve código distinto de cero ante errores.

El manifest inicial permanece vacío y no crea geografía/narrativa real.

## Evidencia heredada de PR #10

La versión exacta portada aquí tenía evidencia final registrada en PR #10:

```
Vintage Telnet content validation OK
Ran 15 tests in 1.393s
OK
```

Incluía explícitamente:
- `test_missing_description_is_reported`
- `test_empty_description_is_reported`
- `test_unsupported_exit_direction_is_reported`

## Evidencia de esta sesión

El entorno actual no puede resolver `github.com` desde el runner local, por lo que no se declara una nueva ejecución de suite. La reconstrucción se hizo copiando los blobs finales directamente desde la rama antigua mediante GitHub.

## Límites respetados

No se modificó:
- `vintage-telnet/server/`;
- `vintage-telnet/ops/`;
- Raspberry;
- SQLite viva;
- canon/narrativa/secretos;
- Senku.

## Estado

**LISTO PARA REVISIÓN:** sí.  
La PR vieja #10 debe cerrarse como superseded si esta entrega nueva queda aceptada.
