# Vintage Telnet — Población ambiental N0 y primer viajero N5-lite

**Responsable:** Historiador y Constructor del Mundo  
**Origen:** Issue #334 — WORLD-POPULATION-01 / #338 — TRAVELER-ROUTINES-01  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Objetivo:** cerrar roles regionales plausibles para población ambiental y entregar un primer viajero canónico sobre una ruta ya existente.

Este documento no crea quests, economía, reputación, horarios complejos ni simulación social.

---

# 1. Tabla N0 canónica

| role_id | rol visible | regiones | room_tags permitidos | exclusiones |
| --- | --- | --- | --- | --- |
| habitante_local | Habitante | Veyra,Edran,Hoshai,Korven,Lethra,Nhal | pueblo_centro,pueblo_borde,camino_local | interiores_privados,mazmorra,amenaza_activa |
| trabajador_local | Trabajador | Edran,Hoshai,Korven,Lethra,Nhal | taller_borde,campo,terraza,roca_trabajada,orilla,juncos,bosque_recoleccion | combate,mazmorra,camino_remoto |
| cargador_ruta | Cargador | Veyra,Edran,Korven,Lethra | camino,mercado_borde,pueblo_borde,cruce,embarcadero | Hoshai_altura_extrema,Nhal_profundo,mazmorra |
| viajero_ruta | Viajero | Veyra,Edran,Hoshai,Korven,Lethra,Nhal | camino,cruce,pueblo_borde,refugio_ruta | interiores_privados,mazmorra,ramal_peligroso |
| recolector_local | Recolector | Edran,Hoshai,Lethra,Nhal | campo,matorral,bosque_montana,orilla,juncos,bosque,claro | Korven_roca_desnuda,pueblo_centro,mazmorra,amenaza_activa |

## Lectura regional

### Habitante
Es el rol más general.

Puede aparecer en cualquier pueblo o borde de asentamiento.

No representa automáticamente a una especie concreta: la presentación visual debe respetar la población del lugar si el sistema conoce ese contexto.

### Trabajador
Su actividad debe derivarse del entorno:
- Edran: parcela, reparación simple, carga agrícola;
- Hoshai: mantenimiento de terraza, madera, piedra;
- Korven: piedra, metal, ajuste de herramientas;
- Lethra: embarcadero, fibra, pesca/recolección;
- Nhal: fibra, madera recogida con cuidado, mantenimiento discreto.

No usar “trabajador” como excusa para inventar fábrica, gremio o industria.

### Cargador
Más plausible en rutas con tránsito de bienes.

Se prioriza:
- Veyra;
- Edran;
- Korven;
- Lethra.

No se usa de forma ordinaria en:
- Hoshai de gran desnivel;
- Nhal profundo.

Eso no significa que nadie transporte bienes allí; solo evita que el arquetipo N0 genérico parezca absurdo en esas salas.

### Viajero
Puede aparecer a lo largo de las Cinco Rutas y bordes de pueblos.

No debe aparecer dentro de ramales peligrosos como si fueran trayecto cotidiano.

### Recolector
Debe corresponder a recursos naturales visibles.

No implica mecánica activa de recolección.

---

# 2. Exclusiones globales N0

N0 no aparece como presencia ambiental en:
- hogar personal;
- interiores privados;
- sala con combate activo;
- mazmorra/interior peligroso no autorizado;
- proximidad crítica de amenaza C3/C4;
- escena scripted que requiera aislamiento;
- lugar cuya narrativa explícita dependa de estar vacío.

Un NPC scripted siempre tiene prioridad sobre un N0 ambiental.

---

# 3. Primer viajero N5-lite

## Identidad mínima

**npc_id:** `viajero_loren`  
**Nombre visible:** **Loren**  
**Rol:** viajero de camino y mensajero informal entre Valdren y las rutas hacia Veyra.  
**Nivel técnico:** N5-lite para movimiento; su conversación puede permanecer N1/fija en el piloto.  
**persistent_traveler:** **no**

Loren no es:
- comerciante;
- quest giver;
- autoridad;
- personaje central;
- portador de secretos.

Su función es hacer visible que las rutas son utilizadas por otras personas.

## Contexto cultural

Loren transporta noticias cotidianas y pequeños encargos entre viajeros y hogares sin constituir un servicio postal formal.

No se define:
- organización;
- sueldo;
- gremio;
- ruta comercial exclusiva;
- mercancía persistente.

---

# 4. Ruta piloto de Loren

**route_id:** `valdren_camino_corto_01`

Lista ordenada de `room_id` reales de `server/world.py`:

1. `valdren_centro`
2. `valdren_sendero`
3. `valdren_camino_parcela`
4. `valdren_camino_cerca`
5. `valdren_camino_lindero`
6. `valdren_lindero_tres_piedras`
7. `valdren_camino_hundido`
8. `valdren_cobertizos_viejos`
9. `valdren_cruce_cercas`
10. `valdren_campo_rastrojo`
11. `valdren_zanja_vieja`
12. `valdren_arbol_descanso`

## Comportamiento terminal

**invertir**.

Al llegar a `valdren_arbol_descanso`, Loren inicia el recorrido de regreso por la misma secuencia en sentido inverso.

No desaparece ni teleporta.

Como `persistent_traveler=false`, su posición puede derivarse de tiempo/ruta sin persistencia individual, según GAMEPLAY §39.

---

# 5. Pausas narrativas autorizadas

Sin modificar la cadencia mecánica base, los landmarks adecuados para una eventual pausa explícita son:

- `valdren_centro`
- `valdren_cobertizos_viejos`
- `valdren_arbol_descanso`

Historia no fija duración.

Jugabilidad/Desarrollo pueden omitir pausas en el primer piloto si simplifica la implementación.

---

# 6. Límites de Loren

Loren no debe:
- entrar a `valdren_forja`;
- entrar a `valdren_mercado`;
- tomar `valdren_parcelas_exteriores`;
- tomar `valdren_pastos_altos`;
- desviarse hacia combate por decisión de LLM;
- cambiar de ruta porque el jugador se lo pida;
- vender o entregar objetos;
- iniciar una quest.

Su ruta es autoritativa y simple.

---

# 7. Integración con Narrativa existente

`WORLD_POPULATION_NARRATIVE.md` ya incluye voz fallback de **Viajero**.

Narrativa puede ahora añadir 3–5 barks específicos para `viajero_loren`.

Hasta entonces, usar la voz fallback de Viajero no cambia su identidad histórica ni su ruta.

---

# 8. Handoff a Desarrollo

## Para #380 N0
Historia entrega:
- role_id;
- label;
- regiones;
- room_tags;
- exclusiones.

Narrativa ya entrega `bark_key` mediante sus familias de voz.

## Para #338 N5-lite
Historia entrega:
- npc_id = `viajero_loren`
- route_id = `valdren_camino_corto_01`
- ruta ordenada real;
- persistent_traveler = false;
- terminal = reverse/invertir.

No hace falta otra ronda conceptual de Historia para construir el primer piloto.

---

# Estado

**HISTORIA DE #334 COMPLETA PARA V1.**

**#338 queda desbloqueable por contenido** una vez Narrativa añada, si se desea, las líneas específicas de Loren.
