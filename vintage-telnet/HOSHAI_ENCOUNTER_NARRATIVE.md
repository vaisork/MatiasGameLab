# HOSHAI-01 — Mapping narrativo del Camino Alto

**Origen:** #289 / #166  
**Responsable de esta capa:** Narrador  
**Alcance:** tensión, reservas y señalización. La compatibilidad ecológica de Uñapiedra/Saltacresta corresponde a Historia; porcentajes y pesos corresponden a Jugabilidad.

| room_id | estado narrativo | fauna deliberadamente ausente | nota |
|---|---|---:|---|
| alto_terrazas | tranquila | sí | Último espacio cotidiano de Khariel. Debe funcionar como salida legible, no como presión inmediata. |
| alto_mirador | tranquila | sí | Hito de orientación. Conviene permitir mirar el trazado sin interrupción. |
| alto_anclajes | normal | no | Primer tramo donde la ruta puede empezar a sentirse exterior. |
| alto_escalones | normal | no | El viento y el cambio de nivel ya sostienen identidad sin exigir encuentro. |
| alto_terraza_abandonada | tensa | no | El abandono permite elevar expectativa sin convertirlo en encuentro scripted. |
| alto_garganta | tensa | no | Paso estrecho: la presencia potencial de fauna pesa más aquí. |
| alto_cruce_alturas | normal | no | Cruce legible y recuperable; evitar convertir cada hito en pico de peligro. |
| alto_puente_viento | tranquila | sí | Landmark fuerte de orientación. El cruce debe poder recordarse por sí mismo. |
| alto_pinar | normal | no | Cambio de suelo/vegetación apropiado para recuperar fauna regional. |
| alto_descenso | tensa | no | Khariel ya no es visible; buen tramo para aumentar sensación de exposición. |
| alto_agua_fria | tranquila | sí | Pausa natural explícita en la descripción actual. Preservarla como respiro. |
| alto_ultimo_risco | tensa | no | Último tramo claramente serrano antes de abrirse hacia la Cuenca. |
| alto_camino_falda | normal | no | Transición usada por viajeros; bajar presión antes de abandonar Hoshai. |

## Rasgacumbres

Rasgacumbres **no entra al pool ordinario**.

Si más adelante se coloca un encuentro fijo o ramal relacionado con esta amenaza, debe existir advertencia previa y separada del propio combate. Los mejores puntos narrativos para comenzar esa señalización son los tramos de mayor exposición serrana:

- `alto_garganta`
- `alto_descenso`
- `alto_ultimo_risco`

La advertencia debe aparecer antes de que el jugador quede comprometido con el encuentro. No usar la aparición de Rasgacumbres como la primera señal de que el lugar es peligroso.

## Ritmo buscado

Salida segura → exterior normal → primera tensión → landmark/respiro → exterior → tensión profunda → pausa → última tensión → transición.

Esto evita que Hoshai sea una cadena uniforme de tiradas de fauna. Las salas tranquilas siguen siendo importantes incluso cuando el hábitat pudiera aceptar una criatura.

## Handoff

Historia completa en #289 las columnas de compatibilidad:
- `unapiedra: sí/no`
- `saltacresta: sí/no`
- `regional_habitat: sí/no`
- restricción ecológica

Después Jugabilidad puede combinar ambas capas para publicar chance, perfil 0/10/20/30/35, pesos y exclusiones.
