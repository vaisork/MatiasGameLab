# Vintage Telnet — Población N0 por hora del día

**Origen:** #554 DAYPART-POPULATION-01  
**Responsable:** Historiador y Constructor del Mundo  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Alcance:** compatibilidad cotidiana. Sin porcentajes.

Valores:
- **normal** = presencia cotidiana plausible;
- **reducida** = plausible pero menos habitual;
- **improbable** = rara, no debe sostener densidad ordinaria;
- **excluida** = no presentar por defecto.

| rol / lugar | Amanecer | Día | Atardecer | Noche |
| --- | --- | --- | --- | --- |
| habitante_local / pueblo_centro | reducida | normal | normal | reducida |
| habitante_local / pueblo_borde | normal | normal | normal | reducida |
| trabajador_local / campo-terraza-orilla | normal | normal | reducida | excluida |
| trabajador_local / taller_borde | reducida | normal | normal | improbable |
| cargador_ruta / mercado-pueblo_borde | reducida | normal | normal | improbable |
| cargador_ruta / camino-cruce | reducida | normal | reducida | improbable |
| viajero_ruta / camino-cruce | reducida | normal | normal | reducida |
| viajero_ruta / refugio_ruta | normal | reducida | normal | normal |
| recolector_local / campo-orilla-bosque | normal | normal | reducida | improbable |
| recolector_local / bosque Nhal | reducida | normal | reducida | reducida |

## Ajustes regionales

### Edran
Amanecer y día concentran trabajo agrícola. Atardecer favorece retorno por caminos locales. De noche, campos y parcelas deben sentirse mucho menos ocupados.

### Hoshai
Actividad exterior baja antes de que haya buena visibilidad, excepto tareas breves cerca de Khariel. Noche reduce fuertemente tránsito expuesto; refugios de ruta pueden conservar presencia.

### Korven
Trabajo y carga se concentran de día. Viento/exposición hacen improbable la actividad ordinaria nocturna fuera de Brumak y abrigos.

### Lethra
Amanecer mantiene actividad en orilla, plataformas y pasos de agua. Noche reduce tránsito abierto, pero refugios/plataformas habitadas no quedan vacíos por regla.

### Nhal
No equiparar noche con vacío: Vesperi y habitantes locales siguen moviéndose en zona habitada. En bosque profundo la población N0 sigue siendo escasa por distancia, no por oscuridad.

### Veyra
Día/atardecer son los periodos de mayor tránsito. Amanecer y noche conservan viajeros y cargadores ocasionales cerca de Vaisgard y cruces.

## Reglas

- scripted NPC > N0;
- combate oculta N0;
- máximo 1 N0 por sala sigue vigente;
- no crear guardias como rol nuevo por inferencia;
- no crear hogares iluminados como NPCs;
- noche no vacía todos los pueblos;
- daypart modifica plausibilidad, no identidad ni memoria.

**Historia #554: COMPLETA.**
