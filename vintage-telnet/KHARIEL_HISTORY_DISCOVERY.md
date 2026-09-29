# #163 — Khariel / Camino Alto: primer hilo histórico jugable

Objetivo: convertir historia pública ya integrada en una secuencia opcional de observación sobre room_id existentes. No añade NPC, recompensa, criatura, geografía ni mecánica nueva.

Fuente canónica: SETTLEMENTS.md — Historia local de Khariel.

## Secuencia

| room_id | lugar | hito observable | texto de mirar/examinar | conocimiento público que aprende | dependencia |
| --- | --- | --- | --- | --- | --- |
| `alto_terrazas` | Terrazas habitadas | muros de apoyo gruesos y reparaciones de épocas distintas | “Las terrazas no fueron levantadas de una sola vez. Bajo reparaciones recientes asoman piedras más antiguas y apoyos de distinta factura.” | Khariel creció por capas; las terrazas permanentes aparecieron conforme los campamentos dejaron de ser temporales. | SETTLEMENTS.md / Khariel |
| `alto_mirador` | Mirador antiguo | posición con líneas de visión anteriores al camino actual | “El mirador no parece colocado para este tramo del camino. Desde aquí se alcanzan otros niveles y salientes que hoy ya no dependen de este punto.” | Los primeros grupos Felaryn se distribuían entre salientes visibles entre sí; observar y mantener contacto entre niveles precede a parte de la infraestructura actual. | SETTLEMENTS.md / Khariel |
| `alto_anclajes` | Anclajes del puente viejo | huecos y fijaciones de un paso sustituido | “En la roca quedan huecos alineados donde alguna vez se sostuvo un paso. El camino actual evita ese cruce, pero las marcas muestran que antes se resolvía de otra manera.” | Khariel fue conectando niveles con puentes cortos, apoyos y senderos; muchas conexiones fueron sustituidas sin borrar todas sus huellas. | SETTLEMENTS.md / Khariel |
| `alto_escalones` | Escalones del viento | escalones y reparaciones que ordenan un desnivel natural | “Los escalones siguen la forma de la montaña más de lo que la corrigen. Algunos parecen antiguos; otros reparan o prolongan trazos anteriores.” | La historia de Khariel está distribuida verticalmente y el asentamiento se adaptó al desnivel en lugar de buscar un gran centro plano. | SETTLEMENTS.md / Khariel |
| `alto_terraza_abandonada` | Terraza abandonada | plataforma sin uso cotidiano con bordes gastados | “La plataforma conserva desgaste de paso y apoyo, aunque ya no tenga una función evidente. No parece una ruina desconocida: parece un lugar que el pueblo dejó de necesitar de la misma manera.” | Algunos espacios actuales conservan funciones anteriores de vigilancia, reunión o tránsito; la historia local no depende de un fundador único ni de una sola obra monumental. | SETTLEMENTS.md / Khariel |

## Ritmo de descubrimiento

- Ninguna observación es obligatoria para avanzar por Camino Alto.
- Una sola sala entrega un fragmento, no una explicación total.
- La combinación de varias observaciones permite inferir que Khariel pasó de campamentos separados a una red de niveles conectados.
- No revelar quién hizo cada reparación concreta ni fechar estructuras.
- No convertir `examinar` en prueba con respuesta correcta.

## Texto de cierre opcional

Tras haber examinado al menos tres de estos hitos, Narrativa puede resumir sin recompensa:

“Empiezas a reconocer un patrón: Khariel no nació alrededor de una plaza única. Creció uniendo alturas que ya estaban habitadas y visibles entre sí.”

Este resumen es conocimiento público; no desbloquea secreto, XP ni item.

## Handoff

Narrativa de este primer bloque de #163: CERRADA.

Desarrollo/Integración puede implementar estos textos usando las acciones de observación ya existentes. No hace falta sistema nuevo.