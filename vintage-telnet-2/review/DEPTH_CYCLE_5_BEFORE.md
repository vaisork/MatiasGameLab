# Ciclo 5 — sesión larga, jugar y criticar

Evaluación de agente, sin prueba humana ni visual. `scripts/depth-cycle5-long.py` reutiliza API y patrones de recorrido existentes, con base temporal destruida al salir; ninguna escritura en cuenta/base reales. RNG=0, mediodía inicial; esperas reales de reloj para dos combates. Evidencia `review/depth-cycle5-before.json`.

Se jugaron 211 movimientos por 107 ubicaciones, 266 acciones: siete misiones de cinco regiones entregadas, doce conversaciones, comprar, vender, afinar consumiendo material ganado, dos descansos, combate humano, combate con Espinajo, retirada previa ante Cornalomo y regreso al hogar. El inventario, pagos y servicios se verificaron mediante respuestas reales; no se alteró el estado para simular recursos. La derrota no se provocó artificialmente: no añadía evidencia al defecto editorial investigado.

Lo mejor: cornisa→recomendación, polea→cuenta pendiente y paño→decisión tienen causa y consecuencia; los NPC recuerdan lo comunicado. Afinar exige el material obtenido del combate y la transacción se integra sin teletransporte. Las transiciones regionales mantienen agua, polvo, apoyos y luz, y los refugios añadidos conservan escala pequeña.

Lo débil: una sesión más larga convierte la repetición en ruido. Saltacresta emite la misma frase 19 veces; Cascapedernal 11, Pinzajunco 10 y Rondamusgo 10. El mecanismo conserva hábitat, pero no reconoce el soporte específico de la sala. RNG=0 maximiza la presencia; esta cifra no es predicción de frecuencia real. Aun si aparece menos, los ejemplos siguen sin distinguir la roca del pinar o el borde acuático del hito.

Aburrimiento: al volver varias veces por plaza y escalones para las dos misiones, el reconocimiento vuelve a explicar «haber vuelto no...» en cada cruce. La memoria se volvió visible en ciclo1, ahora deja expuesta su longitud y tono. Un sistema útil no basta si su contenido comenta las reglas sociales desde fuera del mundo.

Plantilla: «puedes reconocer...», «sin asumir...», «no exige...», «no concede...» se encadenan en barrios, talleres y riberas. Muestra sin nombre: «Haber vuelto no concede acceso a viviendas privadas, pero sí te permite participar en la circulación sin invadir los descansos domésticos». La orientación que contiene puede mostrarse en una frase concreta sobre la rampa y el umbral.

Mundo menos convincente: el antiguo canal es el tramo más vacío de identidad entre lugares con actividad. La misma luz de aberturas se imprime nueve veces en entrada, bifurcación, refugio, compuerta y repisa; varias vueltas repiten «Reconoces los apoyos y la salida que utilizaste antes». La misión de recuperar la caja sí funciona, pero el recorrido subterráneo no usa su propia geometría para sostener tensión y memoria. No afirmamos que deba llenarse de criaturas ni de nuevas misiones: el silencio allí puede ser valioso.

Sistema infrautilizado: `wildlife_pool.text`, `day/night/clear` y `return` permiten edición situada sin nueva arquitectura. Misiones, capacidades, pagos y batallas ya dan estructura suficiente para comprobar el cambio editorial. Canon invisible: las construcciones antiguas del canal apenas muestran uso anterior, agua residual y adaptación; el misterio de fundación de Vaisgard se conserva pero aún no pesa en el paseo de mercado/plaza.

Causas prioritarias y cambio concreto: 1) señales regionales idénticas → dar indicios/presencias ligados a agua, grieta, musgo o pino de salas realmente recorridas; 2) memoria explicativa → sustituir un conjunto acotado de retornos de estos caminos por referencias materiales recordadas; 3) canal genérico → ambiente y retornos propios de cinco salas, conservando oscuridad/silencio y flujo de la misión. No modificar requisitos, números, distribución de fauna ni misiones.

| Criterio | Antes |
|---|---:|
| Identidad espacial | 4 |
| Continuidad | 4 |
| Ritmo | 3 |
| Vida ambiental | 3 |
| Densidad sensorial | 4 |
| Identidad regional | 4 |
| Tiempo/clima | 3 (hora diurna, no jornada completa) |
| Exploración | 3 |
| Encuentros | 2 |
| Memoria | 3 (visible, demasiado explicativa) |
| Color semántico | Sin evaluación visual |
| Curiosidad | 3 |

Pendiente IMPLEMENTAR/REJUGAR/COMPARAR exactamente esta sesión. El guion conecta sistemas y registra eventos; llamarla libre no significa selección humana espontánea ni evaluación ciega de sus objetivos.
