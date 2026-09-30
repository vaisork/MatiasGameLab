# Vintage Telnet — N5-LITE-WAVE-01

**Origen:** #557  
**Responsable:** Historiador y Constructor del Mundo  
**Objetivo:** cuatro viajeros recurrentes ligeros para regiones fuera de Edran, usando rutas existentes.

Loren permanece como piloto de Edran.

Ninguno de estos NPC:
- entrega quest automáticamente;
- vende;
- conoce secretos;
- altera combate;
- cambia de ruta por petición del jugador.

## Hoshai — Sira

**npc_id:** `viajera_sira`  
**Nombre:** Sira  
**Especie/origen:** Felaryn de Khariel  
**Función cotidiana:** lleva mensajes, pequeños paquetes no persistentes y noticias locales entre Khariel y tramos bajos del Camino Alto.

**route_id:** `hoshai_camino_corto_01`

Ruta:
1. `khariel_centro`
2. `alto_terrazas`
3. `alto_mirador`
4. `alto_anclajes`
5. `alto_escalones`
6. `alto_terraza_abandonada`
7. `alto_garganta`

Terminal: reverse.

Conoce:
- Khariel;
- estado visible del Camino Alto;
- clima local;
- tránsito cotidiano.

No conoce:
- secretos de Vaisgard;
- Rompecimas como certeza si no está públicamente documentado;
- rutas ocultas;
- contenido DM.

Exclusión: no entra a Boca de la Montaña ni ramales peligrosos.

## Korven — Torvek

**npc_id:** `viajero_torvek`  
**Nombre:** Torvek  
**Especie/origen:** Dravak de Brumak  
**Función cotidiana:** transporta piezas pequeñas de herramienta y mensajes de taller entre Brumak y puntos de descanso del Camino de Piedra.

**route_id:** `korven_camino_corto_01`

Ruta:
1. `brumak_centro`
2. `piedra_patio_exterior`
3. `piedra_pared_anclajes`
4. `piedra_paso_corto`
5. `piedra_patio_abierto`
6. `piedra_primer_monton`
7. `piedra_hendiduras`
8. `piedra_abrigo_viento`

Terminal: reverse.

Conoce:
- Brumak;
- marcas de ruta;
- reparaciones ordinarias;
- condiciones visibles del camino.

No conoce:
- origen antiguo de cavidades;
- secretos de cantera;
- Rompecuña;
- rutas ocultas.

Exclusión: no entra en Cantera Abandonada ni otros ramales.

## Lethra — Mirea

**npc_id:** `viajera_mirea`  
**Nombre:** Mirea  
**Especie/origen:** Marevyn de Narevia  
**Función cotidiana:** recorre plataformas y tramos de juncos llevando noticias entre familias y viajeros.

**route_id:** `lethra_camino_corto_01`

Ruta:
1. `narevia_centro`
2. `juncos_plataformas`
3. `juncos_postes`
4. `juncos_pasarela_antigua`
5. `juncos_isla_refugio`
6. `juncos_juncal`
7. `juncos_paso_raices`
8. `juncos_embarcadero`

Terminal: reverse.

Conoce:
- Narevia;
- niveles/estado visible del agua;
- plataformas y tránsito cotidiano;
- cambios ordinarios de ruta.

No conoce:
- secretos sumergidos;
- interiores no públicos;
- contenido DM;
- Canal Quieto como atajo.

Exclusión: no entra a Canal Quieto ni Molino Hundido.

## Nhal — Vaela

**npc_id:** `viajera_vaela`  
**Nombre:** Vaela  
**Especie/origen:** Vesperi de Velmora  
**Función cotidiana:** mantiene contacto entre el borde de Velmora y referencias seguras del Camino de la Sombra Verde.

**route_id:** `nhal_camino_corto_01`

Ruta:
1. `velmora_centro`
2. `sombra_borde`
3. `sombra_tronco`
4. `sombra_raices_cruzadas`
5. `sombra_claro_pequeno`
6. `sombra_sendero_doble`
7. `sombra_niebla_baja`

Terminal: reverse.

Conoce:
- Velmora;
- señales públicas de orientación;
- estado visible del sendero;
- clima y tránsito local.

No conoce:
- secretos del bosque profundo;
- rutas ocultas;
- Boca de la Montaña como paso confirmado;
- contenido DM.

Exclusión: no entra a Boca de la Montaña ni ramales peligrosos.

## Reglas compartidas

- N5-lite, no NPC completo todavía.
- Movimiento por ruta autoritativa.
- Sin teletransporte.
- Sin desvíos LLM.
- 1 recurrente máximo por ruta por defecto.
- Puede coexistir con N0 solo si Jugabilidad lo autoriza; scripted/recurrente tiene prioridad visual.
- Narrativa debe aportar 4–6 barks por persona.
- Creador de NPCs completará identidad persistente/knowledge_allowed/forbidden.

**HISTORIA #557: COMPLETA PARA OLA V1.**
