# Ciclo 2 · DESPUÉS y comparación

Se repitió `scripts/depth-cycle2-journey.py` sin cambiar objetivos, reloj, RNG ni opciones de viaje: 115 movimientos legales y 104 muestras emparejadas por habitación/fase/clima. Base temporal destruida al terminar. Evidencia `DEPTH_CYCLE_2_AFTER.json`; antes `DEPTH_CYCLE_2_BEFORE.json`. Cambian 65 de 104 escenas, incluyendo correcciones transversales de motor y cambios concurrentes del ciclo 1. No atribuyo las 65 a los ocho lugares de este ciclo.

Implementación: ocho habitaciones conservan descripción, geometría, señales y llegadas. Añadí clima local soportado por su región, amanecer/atardecer en dos tramos y actividades concretas de comida, juego, reparación, relato y fauna pequeña. Recorté explicaciones del autor en Nhal, Narevia y Velmora. El motor compartido, corregido por el agente principal, hace visible `room.weather` también al observar y prioriza el regreso.

## Comparación de mismas condiciones

- **Nhal, suelo de hojas, noche/niebla.** Antes idéntico a noche/viento: sólo hojas oscuras y una interpretación de la observadora. Ahora la niebla borra el extremo del tronco pero deja raíz y hueco próximos; el animal recoge una semilla dentro del círculo visible. Observar conserva esa consecuencia y añade la cáscara escuchada de noche. El viento ofrece otra causa: hojas altas tapan el ruido pequeño. No es reemplazar una etiqueta.
- **Lethra, cruce de canales, día/viento.** Antes observaba exactamente la misma hoja que en cualquier tiempo. Ahora la hoja deriva lateralmente, la planta hundida conserva dirección de corriente y la observadora borra su registro. El cambio altera qué evidencia puede interpretar alguien; mantiene Marevyn respirando aire desde apoyo seco. La escena base y clima todavía se yuxtaponen, pero forman una secuencia compatible de registro/corrección.
- **Velmora, día/niebla.** Antes mover carga y explicación sobre no reproducir plaza abierta. Ahora reparar rueda de juguete, escuchar al niño y acercar el relato cuando el borde del claro desaparece. Hay vínculos domésticos además de mercancía. Persiste metadiscurso en algún detalle de examinar no intervenido: «la plaza no necesita un suelo uniforme».
- **Khariel, nieve.** La rampa junto al muro conserva hielo y las suelas se limpian antes de entrar; la misma plaza permite comparar altura, sombra y paso. El juego de recoger la nuez sin otra mano pertenece a las terrazas y cuerpos Felaryn sin caricatura cultural.
- **Valdren, regreso.** La piedra del banco vuelve a aparecer gracias a prioridad transversal. El viento deja de afirmar que todas las semillas siguen expuestas de noche: tapa del cuenco, lámpara y contraventana dan una acción material compatible con cena o trabajo. Una misma frase meteorológica aún cubre todas las horas; no se implementó simulación doméstica.

## Valoración tras leer el recorrido completo

| Criterio | Antes | Después | Alcance |
|---|---:|---:|---|
| Identidad espacial | 4 | 4 | Conservada; no rediseño de mapa |
| Continuidad | 4 | 4 | Llegadas del ciclo 1 ayudan |
| Ritmo | 3 | 4 | Juego, comida, silencio y herramientas alternan en muestra |
| Vida ambiental | 3 | 4 | Actividad propia y causal en ocho lugares; aún estática |
| Densidad sensorial | 4 | 4 | Más contraste acústico y visibilidad |
| Identidad regional | 4 | 4 | Prueba sin nombres distingue efectos materiales |
| Tiempo y clima | 3 | 4 | Ahora niebla/viento/nieve aparecen y observar los conserva |
| Exploración | 4 | 4 | Leer clima y detalles sin loot ofrece motivo |
| Encuentros | 4 | 4 | Este recorrido no prueba combate |
| Memoria | 3 | 4 | Regreso recupera referencia antes oculta |
| Color semántico | 4* | — | *Antes calificaba kinds API; no prueba visual humana, retiro puntuación visual |
| Curiosidad | 3 | 4 | Invita a contrastar corriente, sombras y reparación |

Puntuaciones de experiencia son juicio editorial del agente en esta muestra, no encuesta humana ni garantía sobre las 150+ habitaciones. Mejoran ocho nodos y la exposición del clima existente. El mundo entero sigue teniendo repetición logística, frases explicativas y actividad estática: no se declara explotación exhaustiva de todos sus sistemas.

Lo mejor después es que el clima dificulta o permite algo específico: observar una hoja, oír una cáscara, escoger rampa o interpretar voz. La debilidad pendiente es el catálogo estático: el animal y el juguete reaparecen sin evolución persistente. No se oculta con más capas. El siguiente ciclo debe probar consecuencias de acciones y regresos con memoria causada por el jugador, manteniendo este paseo como comparación.
