# TRAVEL-SUSTAIN-01 — mapping narrativo v1 Valdren → Veyra/Vaisgard

**Issue:** #484  
**Objetivo:** hacer legible la expedición usando únicamente salas que ya existen. No se crean checkpoints ni curación gratuita.

## Punto de abastecimiento del pueblo

| room_id | uso narrativo |
| --- | --- |
| `valdren_mercado` | **Punto preferente para consumir #410** porque la sala ya está definida en main como zona de alimentos/comercio y abastecimiento cotidiano. Narrativa no fija aquí provisión, actor, precio ni efecto; esos datos llegan desde Historia/Jugabilidad. |
| `valdren_centro` | nodo de salida/regreso y orientación; no sustituye mercado ni se convierte por sí mismo en tienda. |
| `valdren_forja` | conservar para trabajo/armas; no usar como vendedor genérico de comida/materiales por conveniencia. |

No hace falta crear un restaurante nuevo para que exista el primer loop de recuperación. Si Historia define después un servicio de comida/recuperación específico, puede enlazarse al espacio comercial existente sin abrir geografía adicional.

## Decisiones de expedición sobre la ruta existente

| room_id | función de viaje |
| --- | --- |
| `valdren_cobertizos_viejos` | **primer punto de pausa/retorno**: todavía se siente cercano a Valdren y ya existe como lugar práctico para detenerse. No concede recuperación gratuita. |
| `valdren_cruce_cercas` | **decisión fuerte**: continuar ruta, explorar ramales autorizados o regresar. Los ramales no deben ser requisito para alcanzar Vaisgard. |
| `valdren_parcelas_exteriores` | ramal local que regresa al cruce; buen soporte para contenido corto autorizado, nunca atajo ni checkpoint. |
| `valdren_pastos_altos` | ramal opcional de riesgo. Debe seguir siendo claramente evitable y no alojar servicios básicos. |
| `valdren_arbol_descanso` | **segundo punto de retorno**: hito de descanso conocido por viajeros. “Detenerse” es presentación; cualquier recuperación real sigue las reglas de Jugabilidad. |
| `valdren_vado_menor` | decisión antes de dejar el tramo rural inicial y antes del ramal del Molino Hundido; buen lugar para preguntar “seguir o volver”. |
| `campos_loma` | **tercer punto de retorno**: el propio texto ya permite mirar hacia atrás y medir distancia recorrida. |
| `campos_almacen` | hito de soporte de ruta ya existente. Puede alojar abastecimiento futuro **solo si #410/Historia lo autorizan**; por ahora no se convierte en tienda ni curación. |
| `campos_vista_vaisgard` | hito de compromiso final: la ciudad ya es visible y el jugador entiende que está cerca del siguiente gran nodo. |
| `cuenca_aproximacion_sur` | transición de llegada y convergencia de rutas; no necesita premio adicional. |

## Regla de ritmo

La ruta debe comunicar tres ciclos sin añadir salas:

1. **salir preparado** desde Valdren;
2. **medir desgaste y decidir regresar** en hitos legibles;
3. **volver, abastecerse y salir de nuevo** con mejor preparación.

Los hitos no deben llenar cada sala con recompensa. El valor económico real vendrá de:
- #409 encargos;
- #410 recuperación/provisión;
- #482 materiales vendibles;
- reglas de sostenibilidad que cierre Jugabilidad.

## Encargos #409 — superficies compatibles, no asignación

Sin decidir giver ni payout, estas salas son compatibles con los tres tamaños solicitados:
- local/micro: `valdren_centro` / `valdren_mercado`;
- ruta corta: tramo hasta `valdren_cobertizos_viejos` o `valdren_cruce_cercas`;
- recorrido mayor: hitos posteriores del Camino de los Campos.

La selección final de actor/condición pertenece a #409 y debe consumir canon de Historia.

## Handoff

**Mapping Narrativa: CERRADO v1 para Valdren → Vaisgard.**

**LISTO PARA DESARROLLO: NO** todavía, porque #484 también requiere:
- criterios de sostenibilidad de Jugabilidad;
- binding final de #409/#410;
- contenido económico de #482.

Desarrollo no necesita expansión geográfica para resolver el primer loop.
