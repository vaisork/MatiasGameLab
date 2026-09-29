# WEATHER-01 — presentación narrativa v1

Issue: #138

Esta entrega cierra únicamente la presentación narrativa de hora y clima sobre el contrato ya cerrado por Jugabilidad e Historia.

## Etiquetas visibles

Hora:
- Amanecer
- Día
- Atardecer
- Noche

Clima:
- Despejado
- Nublado
- Lluvia
- Niebla
- Nieve
- Tormenta
- Viento

La interfaz puede mostrar una etiqueta de hora y una de clima de forma simultánea.

## Regla de texto

En v1, hora y clima son contexto ambiental corto.

No:
- reescriben automáticamente la descripción completa de sala;
- disparan eventos;
- cambian fauna;
- alteran estadísticas;
- conceden ventajas de especie;
- crean requisitos de equipo.

Si una vista necesita una frase ambiental breve, usar una sola línea opcional y no acumulativa.

### Frases ambientales base

Despejado: “El cielo está despejado.”
Nublado: “Las nubes cubren buena parte del cielo.”
Lluvia: “La lluvia cae sobre el entorno.”
Niebla: “La niebla reduce la distancia visible.”
Nieve: “La nieve cae o permanece sobre las zonas altas.”
Tormenta: “La tormenta domina el cielo y el sonido.”
Viento: “El viento se hace notar en el entorno.”
Amanecer: “La luz empieza a extenderse por el paisaje.”
Día: “La luz del día domina el entorno.”
Atardecer: “La luz baja y las sombras se alargan.”
Noche: “La oscuridad cubre el paisaje.”

Estas frases son presentacionales. No implican efectos mecánicos.

## Reglas regionales

Consumir únicamente REGIONAL_WEATHER_CANON.md.

Puntos importantes:
- Nieve solo Hoshai en v1.
- Korven no usa Niebla ni Nieve.
- Lethra y Nhal admiten Niebla.
- Edran y Veyra no usan Nieve.
- Despejado en Nhal no implica iluminación intensa bajo el dosel.
- No usar Niebla para representar polvo en Korven.

## Handoff

Narrativa #138: CERRADA.

Desarrollo puede consumir las etiquetas visibles, el contrato temporal/climático de Jugabilidad, el catálogo regional de Historia y estas frases opcionales.

No hace falta nueva decisión narrativa para implementar WEATHER-01 v1.