# Integración: segundos pasos y secretos por especie (encargo del historiador, 2026-10-08)

Fuente estructurada: `secretos_especie.json`, en esta misma carpeta.

## Integrado

Seis segundos pasos de investigación, abiertos a todas las especies. Cada uno aparece sólo después de completar el primero.

| Investigación | Requiere | Acción en | Resultado (bandera) |
|---|---|---|---|
| Cargallanura | `edran_rastro_grande` | `edran_cobertizo_campo` — Comparar las estacas exteriores | `edran_paso_conocido` |
| Conducción vieja | `edran_conduccion_vieja` | `edran_canal_herramientas` — Comparar la cuña con las marcas del conducto | `edran_canal_reparado` |
| Rompecimas | `hoshai_marcas_altas` | `hoshai_escalones_sol` — Comparar las marcas desde abajo | `hoshai_marcas_desde_abajo` (Iria: «raspadura») |
| Hundepedral | `korven_presion_abajo` | `korven_registro_cauce` — Comparar las anotaciones del registro | `korven_fechas_distintas` |
| Dorsalodo | `lethra_rastro_largo` | `lethra_raices_observacion` — Comparar las marcas de barro | `lethra_movimiento_grande` |
| Quebradosel | `nhal_rastro_alto` | `nhal_sendero_altura` — Comparar los brotes altos | `nhal_brotes_elegidos` |

Catorce secretos nuevos: `requires_species` y alcance `player`. Cada uno cuenta en `world.secrets` y queda en el diario.

| Especie | Secretos | Conversación posterior |
|---|---|---|
| humano | H1 `edran_cobertizo_campo`, H2 `valdren_plaza`, H3 `veyra_archivo_cargas` | Nera: «promesa» |
| felaryn | F1 `hoshai_mirador_nudo` (de día), F2 `hoshai_cuello_roca`, F3 `hoshai_terraza_cargas` | Iria: «fibra», «terraza» |
| dravak | D1 `korven_plataforma_escucha`, D2 `korven_entrante_piezas`, D3 `korven_roca_cascaron` | Taren: «peso» |
| marevyn | M1 `lethra_secreto_barquita` (**existente, conservado**), M2 `lethra_cruce_canales`, M3 `lethra_cuidado_barcas` | Sola: «fibras» |
| vesperi | V1 `nhal_arbol_umbral` (con poca luz), V2 `nhal_patio_relato` (con Leris presente), V3 `nhal_relevo_altura` (con poca luz) | Leris: «pausa» |

- **Etiquetas:** describen el gesto («Apoyar la palma en la piedra», «Meter la mano en el agua»), no lo que se descubre.
- **Sin premios:** ningún secreto da XP, sellos, objetos ni estadísticas.
- **Sin personajes concretos:** ninguno se asigna a Vaison, Senku ni Alivision.
- **Consecuencias compartidas:** sólo la barquita (alcance `world`, ya existente). Los demás descubrimientos son observaciones personales, como indica el encargo.
- **Sin duplicados:** se respetan «Observar el roce del nudo», «Describir el espesor desigual» y «Saltar a la repisa alta», que siguen como estaban.

## Comprobación

`SpeciesSecretsTests` comprueba que:
- Cada especie recibe sus tres secretos y ninguna otra los recibe.
- El descubrimiento es individual: dos Dravak, uno lo encuentra y el otro conserva la acción; no se toca el mundo.
- Los seis segundos pasos sólo aparecen después del primero, para las cinco especies.

155 tests OK; QA del cliente OK.

## Pendiente de validar en juego

- V1 y V3 sólo aparecen al amanecer, al atardecer o de noche («luz tenue»). Un Vesperi que juegue sólo de día no los verá.
- F1 sólo aparece de día.
