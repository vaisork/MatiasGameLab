# Debug Plan: generate_with_params() Not Executing

## Status
- ✅ Lamelón v002: APROBADA (PR #590)
- ✅ Agujaumbría v002: APROBADA (PR #594)
- ❌ Velozanco v002: RECHAZADA (PR #593)
- ❌ WebP/PNG-high no están llegando a assets/ ni art-masters/

## El Problema
En `github_runner.py` líneas 67-92, cuando `critique.passes == True`, debería ejecutar:
1. `pipeline.generate_with_params()` para WebP
2. `pipeline.generate_with_params()` para PNG high-quality
3. Pero el output "✅ Generado WebP" nunca aparece en los logs

## Investigación Hecha
1. ✅ Verificó que `generate_with_params()` existe en pipeline.py (línea 315)
2. ✅ Verificó que el código de github_runner.py tiene indentación correcta
3. ✅ Verificó que critique.passes es True en metadata
4. ✅ Agregó debug logging (línea 70: "DEBUG: critique exists = ...")
5. ❌ El debug logging tampoco aparece → El código NO se ejecuta

## Hipótesis Más Probable
GitHub Actions cachea archivos Python compilados. Aunque se commiteó el código a main, GitHub Actions podría estar usando:
- Una versión compilada (.pyc) vieja
- Un checkout en caché

## Soluciones para Mañana

### Opción A: Forzar recarga del código (Simple, rápido)
1. Cambiar nombre de la función `github_runner.py:run()` a `github_runner.py:run_v2()`
2. Cambiar `__main__` para llamar `run_v2()` en lugar de `run()`
3. Commitear
4. Regenerar UNA ficha aprobada (Lamelón) para ver el debug output
5. Una vez visto el output, sabemos dónde falla exactamente

### Opción B: Script de Post-Procesamiento (Backup)
Si Opción A no funciona, usar `/tools/vt_art/publish_approved.py`:
- No requiere OpenAI API
- Solo convierte PNG → WebP con `cwebp` (herramienta local)
- Se ejecuta automáticamente cada hora hasta terminar

Scripts:
- `tools/vt_art/publish_approved.py` — convertir PNGs aprobados a WebP
- Crear workflow GitHub Actions que corra esto cada hora en main

### Opción C: Reescribir workflow
Si nada funciona:
- Eliminar la lógica de `generate_with_params()` del workflow
- Crear un step separado en bash que:
  1. Busque metadatas con `passes: true`
  2. Convierta PNG → WebP con `cwebp`
  3. Copie a `assets/`
  4. Commitee cambios

## Próximos Pasos (Mañana)
1. **Primero:** Intentar Opción A (cambiar nombre de función)
2. Regenerar Lamelón
3. Revisar logs buscando "DEBUG:" prefix
4. Una vez veamos el debug output, sabemos si el if se ejecuta o no
5. Si no se ejecuta → problema de caché/compilación
6. Si se ejecuta pero falla generate_with_params → problema de function call
7. Una vez identificado el problema, arreglarlo o usar Opción B

## Recursos
- Lamelón aprobada: art_generations/lamelon_korven/v002/
- Agujaumbría aprobada: art_generations/agujaumbria_nhal/v002/
- Velozanco rechazada: art_generations/velozanco_edran/v002/

## Gastos Esperados
- Opción A: 1-2 regeneraciones (2-4 USD aprox)
- Opción B: 0 USD (solo herramientas locales)
- Opción C: 0 USD (solo bash/git)

## Nota para Mañana
El usuario pedirá NO gastar más del 15% de capacidad semanal.
- 1-2 regeneraciones = ~0.2% de la semana
- ✅ Está bien presupuestado
