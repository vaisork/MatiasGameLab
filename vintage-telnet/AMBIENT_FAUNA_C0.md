# Vintage Telnet — Fauna ambiental C0

**Responsable:** Historiador y Constructor del Mundo  
**Origen:** Issue #333 — AMBIENT-FAUNA-01  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Objetivo:** poblar el mundo con fauna cotidiana no combatible para el motor C0 de GAMEPLAY §39.

Reglas:
- C0 no es encuentro de combate;
- no HP, XP, loot ni estadísticas;
- no reutilizar familias C1+;
- una presencia C0 puede verse, oírse o dejar una acción breve;
- atacar C0 no convierte al animal en enemigo;
- Arte es opcional.

| ambient_id | nombre visible | regiones | habitat_tags | conducta breve | exclusiones |
|---|---|---|---|---|---|
| edran_ala_parda | Ala parda | Edran | campo,pueblo_borde | Ave pequeña que baja a semillas y vuelve a cercas o ramas bajas. | interiores, bosque_denso, humedal_profundo |
| edran_liebre_corta | Liebre corta | Edran | campo,matorral | Herbívoro pequeño que cruza claros con carreras breves y se oculta entre pastos. | pueblo_centro, roca_desnuda, humedal |
| edran_grillo_campana | Grillo campana | Edran | campo,matorral,pueblo_borde | Insecto de canto repetitivo que se oye más que se ve entre hierba seca. | interiores_cerrados, agua |
| hoshai_pico_gris | Pico gris | Hoshai | altura,roca,bosque_montana | Ave de montaña que salta entre piedras y recoge semillas o insectos. | cavernas, pueblo_centro |
| hoshai_orejilla | Orejilla de risco | Hoshai | altura,matorral,roca | Mamífero diminuto que asoma desde grietas y huye al detectar pasos. | caminos_muy_transitados, interiores |
| hoshai_mariposa_fria | Mariposa fría | Hoshai | altura,pradera_alta,agua_fria | Insecto pálido que se concentra cerca de flores de altura en horas templadas. | tormenta, cavernas, roca_sin_vegetacion |
| korven_saltapiedra | Saltapiedra menudo | Korven | roca,hendidura | Lagartija pequeña que corre entre piedras calentadas por el sol y desaparece bajo bloques. | interiores_habitados, sombra_profunda |
| korven_escarabajo_polvo | Escarabajo de polvo | Korven | roca,polvo,hendidura | Escarabajo oscuro que empuja restos secos y se esconde cuando vibra el suelo. | agua, pueblo_centro |
| korven_vencejo_seco | Vencejo seco | Korven | roca,altura,cielo_abierto | Ave rápida que cruza paredes de roca cazando insectos al vuelo. | cavidades_cerradas, interiores |
| lethra_aguja_azul | Aguja azul | Lethra | orilla,humedal,juncos | Insecto alargado que patrulla sobre agua quieta y se posa en juncos. | agua_profunda_sin_vegetacion, interiores |
| lethra_picojunco | Picojunco | Lethra | orilla,juncos,pasarela_borde | Ave pequeña que busca insectos entre tallos y levanta vuelo al acercarse viajeros. | pueblo_centro, canal_profundo_abierto |
| lethra_caracol_liso | Caracol liso | Lethra | orilla,humedal,barro | Molusco pequeño visible sobre madera húmeda, piedra y hojas después de lluvia. | seco, roca_caliente |
| nhal_luzhoja | Luzhoja | Nhal | bosque,niebla_baja,claro | Insecto de brillo tenue natural que aparece entre hojas húmedas; no es mágico. | pleno_dia_abierto, pueblo_centro |
| nhal_pico_sordo | Pico sordo | Nhal | bosque,troncos,dosel | Ave de bosque que golpea madera blanda en series cortas y evita claros abiertos. | humedal_abierto, roca_desnuda |
| nhal_ratona_hoja | Ratona de hoja | Nhal | bosque,hojarasca,raices | Pequeño mamífero que remueve hojas buscando semillas y desaparece bajo raíces. | caminos_limpios, interiores |
| veyra_gorrion_ruta | Gorrión de ruta | Veyra,Edran | camino,pueblo_borde,campo | Ave oportunista acostumbrada al tránsito; picotea restos y se aparta al paso. | bosque_denso, altura_extrema |
| veyra_libelula_clara | Libélula clara | Veyra,Lethra | orilla,curso_agua | Insecto de agua menor que sigue arroyos y zanjas con vegetación. | seco, cavernas |

## Notas canónicas breves

- **Luzhoja** emite un brillo biológico tenue y ordinario; no es Arcane, magia ni fuente de iluminación utilitaria.
- **Orejilla de risco** y **Saltapiedra menudo** no son juveniles de Uñapiedra ni Garralaja; son especies distintas y no combatibles.
- **Ratona de hoja** no es Rondamusgo pequeño.
- **Liebre corta** no es Mordelinde.
- C0 describe presencia cotidiana; no implica que estas especies jamás puedan tener relevancia narrativa futura, pero cualquier cambio de categoría requerirá contrato nuevo.

## Handoff técnico

El catálogo usa tags simples reutilizables:
- campo
- matorral
- pueblo_borde
- altura
- roca
- bosque_montana
- pradera_alta
- agua_fria
- hendidura
- polvo
- cielo_abierto
- orilla
- humedal
- juncos
- pasarela_borde
- barro
- bosque
- niebla_baja
- claro
- troncos
- dosel
- hojarasca
- raices
- camino
- curso_agua

Desarrollo puede mapearlos al catálogo data-driven de #379 sin inventar especies.

**Estado: HISTORIA C0 COMPLETA PARA #333.**
