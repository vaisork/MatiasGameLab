# Handoff — Issue #9: infraestructura de contenido narrativo

**Responsable:** Desarrollador Junior de Vintage Telnet  
**Issue:** #9 — preparar infraestructura de contenido narrativo  
**Base main:** `b882d615dbdea55f6e1bfe2eda32873d6ee82344`  
**Rama:** `junior/vintage-content-validator-issue-9`

## Alcance realizado

Se preparó únicamente infraestructura mecánica/determinista de contenido:

- `vintage-telnet/content/README.md`
- `vintage-telnet/content/manifest.json`
- `scripts/validate-vintage-content.py`
- `vintage-telnet/tests/test_validate_vintage_content.py`
- este handoff

No se añadió geografía, narrativa ni canon real.

## Formato inicial

El manifest queda válido y vacío:

```json
{
  "schema_version": 1,
  "content_version": "0.0.0",
  "files": []
}
```

El README documenta formatos estructurales sintéticos para:

- `species.json`
- `settlements/*.json`
- `narrative/*.json`

Los IDs de ejemplo son `test_*` / sintéticos y no establecen canon.

## Validador

Comando:

```bash
python scripts/validate-vintage-content.py
```

También acepta:

```bash
python scripts/validate-vintage-content.py --content-dir /ruta/al/content
```

No importa Flask ni arranca servidor.

Comprueba como mínimo:

- JSON inválido;
- IDs duplicados;
- salidas hacia salas inexistentes;
- narrativa hacia sala inexistente;
- sala inicial de pueblo inexistente o perteneciente a otro pueblo;
- pueblo/sala inicial de especie inexistente;
- campos obligatorios vacíos;
- manifest incoherente (archivos faltantes/no listados/duplicados/rutas inseguras);
- versión de esquema y `content_version`;
- referencia pública explícita a `private-content`.

Devuelve `0` si es válido y `1` si hay errores.

## Pruebas ejecutadas

Se probó una copia de trabajo equivalente antes de escribir los archivos en GitHub.

Comandos reales:

```bash
python scripts/validate-vintage-content.py
python -m unittest discover -s vintage-telnet/tests -p 'test_*.py' -v
```

Resultado real:

```text
Vintage Telnet content validation OK
Ran 12 tests
OK
```

Casos probados:

1. contenido sintético válido;
2. JSON inválido;
3. ID duplicado;
4. salida a sala inexistente;
5. narrativa a sala inexistente;
6. especie con pueblo inicial inexistente;
7. especie con sala inicial inexistente;
8. campo obligatorio vacío;
9. JSON no listado en manifest;
10. versión de manifest inválida;
11. referencia a private-content;
12. códigos de salida CLI válido/inválido.

Después de la revisión contra la versión más reciente de PR #8 se añadió una **prueba 13** para dirección de salida no permitida. Esa corrección quedó revisada estáticamente en GitHub; esta sesión no dispone de runner/CI del repositorio ni acceso de red desde el contenedor para clonar y reejecutar la suite, por lo que no se afirma falsamente un resultado posterior.

## Límites respetados

No se modificó:

- `vintage-telnet/server/`
- `vintage-telnet/ops/`
- Raspberry Pi
- SQLite viva
- `vintage-telnet.html`
- canon/narrativa/secretos
- Senku
- PR #6

## Actualización automática cada 10 horas

**No implementada en esta entrega.**

La arquitectura de PR #8 la contempla, pero Issue #9 asigna al Junior el carril de contenido y validador. El timer/systemd y despliegue físico pertenecen a la fase operativa/Raspberry y deben quedar bajo el responsable que valide esa arquitectura.

## Dependencia arquitectónica

La implementación sigue el contrato descrito en PR #8 / `CONTENT_RUNTIME_ARCHITECTURE.md`. El Arquitecto debe decidir orden de merge entre PR #8 y la entrega de Issue #9.

## Estado

**LISTO PARA REVISIÓN DEL ARQUITECTO:** SÍ  
**LISTO PARA POBLAR CON CONTENIDO REAL:** después de aprobación/merge; Historiador/Narrador son responsables de ese contenido.


## Corrección tras revisión contra PR #8

La revisión técnica detectó que PR #8 había evolucionado después del inicio de Issue #9.

Se corrigió el contrato para que:

- salas exijan `description` inline en lugar de `description_id`;
- schema v1 acepte únicamente `north`, `south`, `east`, `west` como direcciones de salida;
- exista una prueba sintética específica para rechazar una dirección fuera del conjunto permitido.
