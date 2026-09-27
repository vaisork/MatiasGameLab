# LETHRA-01 — Mapping narrativo del Camino de los Juncos

**Origen:** #305 / #166  
**Capa:** Narrador  
**Fuente de room_id:** `server/world.py` en main. El issue contiene varios nombres desactualizados; este documento usa los IDs autoritativos actuales.

| room_id | estado | exclusión deliberada | señal previa |
|---|---|---:|---|
| juncos_plataformas | tranquila | sí | no |
| juncos_postes | presencia | no | no |
| juncos_pasarela_antigua | tranquila | sí | no |
| juncos_isla_refugio | tranquila | sí | no |
| juncos_juncal | presencia | no | no |
| juncos_paso_raices | territorial | no | sí |
| juncos_embarcadero | tranquila | sí | no |
| juncos_agua_entre_caminos | territorial | no | sí |
| juncos_pasarela_larga | presencia | no | sí |
| juncos_islas_bajas | presencia | no | no |
| juncos_canal_ancho | territorial | no | sí |
| juncos_ultimos | territorial | no | sí |
| juncos_suelo_firme | tranquila | sí | no |
| juncos_corrientes | presencia | no | no |
| juncos_entrada_veyra | tranquila | sí | no |

## Ritmo

**Narevia segura → señales de agua → memoria del camino → refugio → humedal abierto → presión entre raíces → pausa humana → agua interrumpe el camino → exposición larga → rutas visuales → canal tenso → último humedal profundo → suelo firme → transición → Veyra.**

## Exclusiones

Se preservan como pausas sin fauna:
- `juncos_plataformas`: borde cotidiano;
- `juncos_pasarela_antigua`: lectura histórica del camino;
- `juncos_isla_refugio`: refugio;
- `juncos_embarcadero`: landmark;
- `juncos_suelo_firme`: contraste importante tras el humedal;
- `juncos_entrada_veyra`: transición regional.

## Señales

Los tramos territoriales deben anunciar presencia antes de comprometer al jugador. Usar cambios visibles/audibles del humedal — movimiento de juncos, barro alterado, agua desplazada, vibración de pasarela — sin adjudicar aún la señal a Pinzajunco o Saltalodo.

`juncos_pasarela_larga` no se marca territorial, pero requiere señal previa si aparece fauna: la exposición del lugar hace injusto que una amenaza surja sin lectura.

## Handoff

Historia completa compatibilidad Pinzajunco/Saltalodo y tipo de hábitat usando estos IDs vigentes. Jugabilidad fija después perfiles, porcentajes y pesos. No se crean mecánicas acuáticas nuevas.
