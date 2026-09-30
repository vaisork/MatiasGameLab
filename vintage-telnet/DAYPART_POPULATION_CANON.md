# Vintage Telnet — DAYPART-POPULATION-01

**Origen:** #554  
**Responsable:** Historiador y Constructor del Mundo  
**Fuente:** WORLD_POPULATION_CANON.md

Escala:
- **normal**: presencia cotidiana esperable;
- **reducida**: plausible pero menos común;
- **improbable**: excepción;
- **excluida**: no usar N0 genérico.

## Matriz base por rol

| role_id | Amanecer | Día | Atardecer | Noche |
| --- | --- | --- | --- | --- |
| habitante_local | reducida | normal | normal | reducida |
| trabajador_local | reducida | normal | reducida | excluida |
| cargador_ruta | reducida | normal | reducida | improbable |
| viajero_ruta | reducida | normal | normal | reducida |
| recolector_local | normal | normal | reducida | excluida |

## Ajustes por lugar

### pueblo_centro / pueblo_borde
- Amanecer: habitantes preparando actividad; trabajadores empiezan a aparecer.
- Día: máxima actividad ordinaria.
- Atardecer: regreso, cierre de trabajo, conversación local.
- Noche: habitantes reducidos; trabajadores y recolectores fuera.

### mercado
- Amanecer: montaje/reparto reducido.
- Día: normal.
- Atardecer: cierre y últimas cargas.
- Noche: N0 comercial genérico excluido salvo evento específico.

### forja / taller
- Amanecer: preparación reducida.
- Día: normal.
- Atardecer: trabajo de cierre reducido.
- Noche: trabajador_local excluido por defecto.

### camino / cruce / refugio_ruta
- Amanecer: viajeros reducidos.
- Día: viajeros/cargadores normales.
- Atardecer: viajeros normales, cargadores reducidos.
- Noche: viajeros reducidos; cargadores improbables.

### campo / terraza / orilla / juncos / bosque_recoleccion
- Amanecer: recolectores normales; trabajadores reducidos.
- Día: ambos normales.
- Atardecer: ambos reducidos.
- Noche: ambos excluidos.

## Ajustes regionales

### Hoshai
En noche, reducir todavía más cargadores y viajeros en pasos expuestos. No vaciar Khariel.

### Korven
Cargadores pueden seguir apareciendo al atardecer en bordes protegidos y cruces; noche sigue improbable.

### Lethra
Recolectores/orilla son especialmente plausibles al amanecer, sin crear mecánica de pesca.

### Nhal
Actividad profunda cae antes: al atardecer tratar recolector_local en bosque profundo como improbable; noche excluida. Velmora puede seguir teniendo habitantes reducidos.

### Edran
Trabajadores/recolectores especialmente plausibles al amanecer y día en campo; noche solo habitantes/viajeros reducidos.

### Veyra
Viajeros y habitantes pueden mantenerse reducidos de noche en accesos y zonas urbanas; no convertir la ciudad en vacía.

## Exclusiones globales preservadas

Siguen prevaleciendo:
- combate activo;
- interiores privados;
- mazmorra;
- amenaza C3/C4;
- escena scripted aislada;
- lugares narrativamente vacíos.

Scripted NPC > N0.

## Regla de implementación

Daypart modifica **elegibilidad/densidad**, no crea identidad persistente ni horarios individuales.

Máximo 1 N0 por sala se mantiene.

**HISTORIA #554: COMPLETA.**
