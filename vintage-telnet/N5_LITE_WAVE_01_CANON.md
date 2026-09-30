# Vintage Telnet — N5-lite Wave 01: funciones y rutas

**Origen:** #557 N5-LITE-WAVE-01  
**Responsable:** Historiador y Constructor del Mundo  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR

Loren permanece como piloto de Edran. Esta ola añade cinco **slots históricos** para viajeros recurrentes.  
Historia define función, especie/origen, ruta y límites; Creador de NPCs define nombre visible, npc_id final, personalidad y relaciones.

## Hoshai — slot `traveler_hoshai_01`
- **especie/origen:** Felaryn de Khariel.
- **función:** lleva avisos cotidianos entre terrazas y revisa el estado de pasos usados.
- **ruta:** `khariel_centro` → `alto_terrazas` → `alto_mirador` → `alto_anclajes` → `alto_escalones` → `alto_terraza_abandonada` → `alto_garganta` → `alto_cruce_alturas` → `alto_puente_viento` → reverse.
- **conoce:** estado visible del camino, clima inmediato, tránsito reciente.
- **no conoce:** secretos, Rompecimas oculto, rutas no recorridas, ubicación de tesoros.
- **exclusiones:** no entra a ramales, no cruza a Veyra en v1, no entrega quests automáticas.

## Korven — slot `traveler_korven_01`
- **especie/origen:** Dravak de Brumak.
- **función:** corredor de herramientas y recados entre Brumak y puntos de trabajo exteriores.
- **ruta:** `brumak_centro` → `piedra_patio_exterior` → `piedra_pared_anclajes` → `piedra_paso_corto` → `piedra_patio_abierto` → `piedra_primer_monton` → `piedra_hendiduras` → `piedra_pared_partida` → `piedra_abrigo_viento` → reverse.
- **conoce:** reparaciones, montones de orientación, viento y pasos usados.
- **no conoce:** cavidades profundas, Hundepedral, secretos mineros inexistentes.
- **exclusiones:** no entra a Cantera/Grieta ni vende herramientas.

## Lethra — slot `traveler_lethra_01`
- **especie/origen:** Marevyn de Narevia.
- **función:** enlace cotidiano entre plataformas y tramos de agua usados por viajeros.
- **ruta:** `narevia_centro` → `juncos_plataformas` → `juncos_postes` → `juncos_pasarela_antigua` → `juncos_isla_refugio` → `juncos_juncal` → `juncos_paso_raices` → `juncos_embarcadero` → `juncos_agua_entre_caminos` → reverse.
- **conoce:** nivel visible del agua, pasos, plataformas y tránsito.
- **no conoce:** interior de Canal Quieto, secretos acuáticos, fauna no observada.
- **exclusiones:** no actúa como barquero de jugador ni comerciante.

## Nhal — slot `traveler_nhal_01`
- **especie/origen:** Vesperi de Velmora.
- **función:** mantiene orientación cotidiana y lleva mensajes breves entre Velmora y puntos conocidos del bosque.
- **ruta:** `velmora_centro` → `sombra_borde` → `sombra_tronco` → `sombra_raices_cruzadas` → `sombra_claro_pequeno` → `sombra_sendero_doble` → `sombra_niebla_baja` → `sombra_arbol_caido` → `sombra_tres_marcas` → `sombra_claro_escucha` → reverse.
- **conoce:** señales de orientación, estado del sendero y condiciones inmediatas.
- **no conoce:** Boca de la Montaña interior, secretos de Nhal, ubicación garantizada de fauna.
- **exclusiones:** no guía al jugador automáticamente ni cambia rutas por conversación.

## Veyra — slot `traveler_veyra_01`
- **especie/origen:** Humano criado entre Vaisgard y caminos de la Cuenca.
- **función:** mensajero informal de tránsito y carga ligera entre la ciudad y el acceso de los Campos.
- **ruta:** `vaisgard` → `cuenca_aproximacion_sur` → `campos_acceso` → `campos_camino_exterior` → `campos_vista_vaisgard` → `campos_almacen` → reverse.
- **conoce:** tránsito visible, estado del almacén de ruta, noticias cotidianas públicas.
- **no conoce:** secretos de Vaisgard, cámaras inferiores, historia verdadera de la ciudad.
- **exclusiones:** no entra a mercados/interiores por esta rutina; no transporta objetos de jugador.

## Regla común
- recurrente no significa persistencia física permanente;
- máximo uno de estos viajeros recurrentes por ruta en v1;
- scripted NPC tiene prioridad;
- combate/ramal peligroso los excluye;
- no venden, curan, dan quests ni cambian economía por defecto;
- terminal = reverse;
- pueden pausar en landmarks, duración para Jugabilidad.

**Historia #557: COMPLETA.**
