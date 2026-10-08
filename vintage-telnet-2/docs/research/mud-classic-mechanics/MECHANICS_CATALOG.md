# Catálogo comparativo de sistemas de jugabilidad

**Evidencia:** fuente histórica indicada en cada apartado. **No afirmar equivalencia exacta** entre Diku, Merc, Circle y ROM: divergen por versión.

## 1. Combate: acierto, defensa y daño
- **Diku/Circle:** THAC0 (tirada necesaria para impactar AC 0) + AC del defensor + d20; menor AC favorece defensa. Builder Manual CircleMUD §4.2: https://www.circlemud.org/pub/jelson/CircleMUD/3.x/uncompressed/current/doc/building.pdf
- **Merc:** THAC0 por clase y nivel, hitroll, damroll, daño de arma; estudiar código concreto de `fight.c`, `const.c`, `merc.h` en https://github.com/benjamin-small/Merc . **No asumir** que un ejemplo simplificado replica sus modificadores y excepciones.
- **ROM 2.4:** AC separada en pierce/bash/slash/exotic o mágico en documentación de móviles; daños elementales y resistencias/vulnerabilidades. https://github.com/avinson/rom24-quickmud/blob/master/doc/Rom2.4.doc
- **Decisión VT2 pendiente:** probabilidad de acierto, mínimo/máximo, reducción de daño o evasión, legibilidad, balance de enemigos, protección acumulada.

## 2. Equipamiento y progresión
- Ranuras típicas: cabeza, torso, brazos, manos, piernas, pies, cintura, cuello, anillos, muñecas, arma, escudo y objeto sostenido; **confirmar slots y límites en versión seleccionada**.
- Armas: dados de daño, categoría, tipo de ataque, hitroll/damroll, nivel requerido, peso y compatibilidad de clase; dos manos vs escudo.
- Armaduras: AC por tipo en ROM, restricciones de nivel/clase, resistencia específica y efectos especiales. **No traducir automáticamente AC negativa en porcentaje de mitigación.**
- Objetos especiales: modificadores de atributos, resistencia, rareza, maldiciones, peso y requisitos. Recomendación: primeras entregas sólo efectos explicables y comprobables.
- Fuente: https://github.com/MUDOmnibus/Rom24b6 ; https://github.com/DikuMUDOmnibus/Merc-Cpp

## 3. Experiencia y crecimiento
- Tablas de experiencia y curvas por nivel; HP/mana por clase, constitución y aprendizaje de habilidades.
- Merc C++ README documenta `thac0_00`, `thac0_32` interpolados y `hp_min`/`hp_max` por clase: https://github.com/DikuMUDOmnibus/Merc-Cpp/blob/master/README
- No trasplantar curvas sin simular tiempo de progresión VT2 (campaña de 6–8 horas prevista) y mortalidad temprana.

## 4. Habilidades y clases
- Habilidades por nivel y clase; ataque extra, parar, esquivar, rescatar, desarmar, embestir, retroceder, magia y resistencias.
- Las capacidades de los monstruos de ROM incluyen bash, dodge, parry, rescue, disarm, fast y más; no todas activas en todas las versiones. https://github.com/avinson/rom24-quickmud/blob/master/doc/Rom2.4.doc
- Adaptar únicamente al roster vigente de VT2: **Juramentado, Sombra, Arcano y Artífice**. Las referencias históricas a **Vigía e Invocador están superseded** y no autorizan su implementación.

## 5. Economía, botín y equipo
- Tiendas: compra/venta, valor, nivel y disponibilidad; inventario por instancia, no duplicar materiales.
- Distribución: compras básicas, objetos hallados y recompensas con fuente física o narrativa coherente; evitar caída arbitraria de dinero.
- Requisitos VT2: Daro, precios canónicos, venta confirmada, no vender arma activa ni última arma utilizable, condiciones `damaged_event` excepcionales; no habilitar Forja regional por inferencia.

## 6. NPCs y monstruos
- Perfiles por nivel, HP, daño en dados, THAC0/AC, oro/XP, conducta ofensiva, resistencias; el builder de Circle ofrece un esquema verificable.
- VT2 exige encuentros compartidos con una salud/ronda y recompensa física única; no importar combate por jugador si rompe concurrencia.

## 7. Recuperación, muerte y dificultad
- Analizar descanso, regeneración, penalizaciones, retirada, muerte, reaparición y pérdida de equipo de cada variante antes de adoptar.
- **No adoptar automáticamente** pérdida permanente de inventario, experiencia negativa o corpse retrieval: debe existir decisión creativa explícita y migración segura.

## 8. UX textual histórica
- `score`, `equipment`, `inventory`, `consider`, `compare`, `examine`, `help` y mensajes de impacto: verificar disponibilidad exacta por motor/versión.
- VT2: comparación de armas/armaduras con números y explicación del efecto real; nunca un botón cliente que invente resultado.

## Matriz de decisión
| Tema | Recuperar como inspiración | Requiere contrato cerrado | Riesgo principal |
|---|---|---|---|
| Dados de arma | Sí | Daño y balance | Varianza excesiva |
| THAC0 / AC | Evaluar | Fórmula y progresión | Confusión al jugador |
| Cuatro AC ROM | Evaluar | Tipos y resistencias | Complejidad de UI |
| Ranuras de equipo | Sí | Modelo, compatibilidad, persistencia | Migración de personajes |
| Habilidades por clase | Sí | Desbloqueo, costes, límites | Desequilibrio entre clases |
| Encantamientos | Más adelante | Rareza, límites, fuentes | Inflación de poder |
| Tiendas / venta | Sí, respetando VT2 | Precio, validación, instancias | Duplicación o pérdida |
| Muerte con pérdida | No por defecto | Decisión explícita | Frustración y pérdida de datos |
