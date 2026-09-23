# Vintage Telnet — Simulación de armaduras v1

**Estado:** evidencia de balance para GAMEPLAY §30  
**Objetivo:** comprobar que aumentar protección reduce daño sin convertir la armadura máxima en elección gratuita.

## Perfiles mecánicos probados

Estos perfiles no son objetos canónicos.

| Perfil | Reducción física | Multiplicador de fatiga física |
| --- | ---: | ---: |
| Sin armadura | 0% | ×1.00 |
| Protección ligera | 10% | ×1.10 |
| Protección media | 20% | ×1.20 |
| Protección alta | 30% | ×1.30 |
| Límite v1 | 35% | ×1.35 |

La regla probada es:

`Fatiga = CosteBase × ModResistencia × (1 + armor_reduction_total)`

## Prueba de combate intenso

Secuencia ilustrativa de 10 acciones físicas con:
- ataques básicos;
- dos esquivas;
- una huida;
- 80 puntos de daño físico bruto conectado antes de armadura.

| Perfil | Daño recibido | Fatiga acumulada |
| --- | ---: | ---: |
| Sin armadura | 80 | 48.0 |
| 10% | 72 | 52.8 |
| 20% | 64 | 57.6 |
| 30% | 56 | 62.4 |
| 35% | 52 | 64.8 |

Conclusión:
- la protección alta produce una diferencia real de supervivencia;
- su coste aparece como menor capacidad de sostener muchas acciones físicas;
- no hace falta aplicar una penalización artificial directa a Agilidad o precisión.

## Defensa + armadura

Las reducciones se multiplican.

Ejemplo con Bloquear 25%:

| Armadura | Reducción total efectiva |
| ---: | ---: |
| 0% | 25.0% |
| 10% | 32.5% |
| 20% | 40.0% |
| 30% | 47.5% |
| 35% | 51.2% |

Ejemplo con Resistir 30%:

| Armadura | Reducción total efectiva |
| ---: | ---: |
| 0% | 30.0% |
| 10% | 37.0% |
| 20% | 44.0% |
| 30% | 51.0% |
| 35% | 54.5% |

El máximo v1 de armadura, combinado con una buena defensa, sigue dejando pasar una fracción importante del daño.

## Decisiones de simplificación

Para v1:
- no durabilidad;
- no reparación rutinaria;
- no penalización universal directa de Agilidad/Destreza;
- no evasión añadida por armadura;
- no tabla universal de resistencias elementales;
- no pérdida de armadura al morir;
- máximo total 35%;
- varias piezas pueden sumar contribuciones, pero nunca superar el máximo.

## Criterio de playtest

Revisar el modelo si:
- 30–35% de armadura resulta siempre mejor incluso para personajes centrados en esquiva/huida;
- la carga lleva a fatiga 70+ demasiado rápido en combates ordinarios;
- Resistencia + armadura alta produce supervivencia desproporcionada;
- armadura ligera/media no ofrece ningún nicho útil;
- los jugadores no comprenden la relación protección ↔ fatiga.

Los valores pueden afinarse sin cambiar la regla central de §30.
