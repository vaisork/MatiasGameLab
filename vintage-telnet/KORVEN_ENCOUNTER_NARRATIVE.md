# KORVEN-01 — Mapping narrativo del Camino de Piedra

**Origen:** #304 / #166  
**Capa:** Narrador

| room_id | estado | exclusión deliberada | señal previa |
|---|---|---:|---|
| piedra_patio_exterior | tranquila | sí | no |
| piedra_pared_anclajes | presencia posible | no | no |
| piedra_paso_corto | territorial | no | sí |
| piedra_patio_abierto | presencia posible | no | no |
| piedra_primer_monton | tranquila | sí | no |
| piedra_hendiduras | territorial | no | sí |
| piedra_pared_partida | presencia posible | no | no |
| piedra_abrigo_viento | tranquila | sí | no |
| piedra_meseta_baja | presencia posible | no | no |
| piedra_cruce_montones | presencia posible | no | no |
| piedra_cavidades | territorial | no | sí |
| piedra_clara | tranquila | sí | no |
| piedra_ultimo_corredor | territorial | no | sí |
| piedra_suelo_quebrado | presencia posible | no | no |

## Lectura del recorrido

El Camino de Piedra no debe sentirse hostil desde la puerta de Brumak. Su ritmo es:

**salida segura → roca cerrada → primera presión → orientación → presión entre corredores → landmark → refugio → exposición → decisión de ruta → cavidades tensas → pausa → último corredor tenso → apertura hacia Veyra.**

Las cuatro exclusiones deliberadas preservan orientación y respiración:
- `piedra_patio_exterior`: borde cotidiano de Brumak;
- `piedra_primer_monton`: hito de orientación;
- `piedra_abrigo_viento`: pausa explícita para viajeros;
- `piedra_clara`: marcador de progreso.

## Señales previas

En salas marcadas **territorial**, cualquier criatura que vaya a iniciar una interacción territorial debe poder anunciar presencia antes de que el jugador quede comprometido. Las señales deben apoyarse en el terreno: movimiento entre piedra, roce, grava desplazada, eco cercano o interrupción visible del paso.

No atribuir una señal concreta a Cascapedernal o Colagrieta hasta que Historia confirme compatibilidad por sala.

## Scripted / reservas

No fijo encuentros scripted nuevos en este paquete. Si una sala recibe después una escena fija, esa escena tiene prioridad narrativa sobre el pool y debe revisarse antes de mezclar fauna aleatoria.

## Handoff

Historia completa en #304:
- Cascapedernal sí/no;
- Colagrieta sí/no;
- Korven/transición;
- incompatibilidad ecológica.

Jugabilidad combina después ambas capas para porcentajes, pesos y perfiles. Narrativa no fija esos números.
