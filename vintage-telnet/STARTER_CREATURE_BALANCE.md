# Vintage Telnet — Balance inicial de criaturas del piloto

**Estado:** V1 DE IMPLEMENTACIÓN / AFINABLE POR PLAYTEST  
**Escena:** VT-NAR-003 — El lindero roto  
**Canon:** `CREATURES.md`  
**Reglas:** `GAMEPLAY.md` §§20, 22

Este archivo no cambia identidad, comportamiento narrativo ni canon de las criaturas. Solo da a Desarrollo un bloque numérico inicial para probar combate real.

## Principio

Las criaturas comunes no necesitan copiar los ocho atributos completos del jugador para la primera implementación.

El servidor puede representar su comportamiento de combate con un perfil directo:
- HP;
- precisión base;
- daño bruto;
- defensa/reducción;
- conducta especial;
- nivel de referencia de progresión.

Si Arquitectura decide posteriormente derivar estos valores desde un modelo interno más complejo, el resultado visible debe conservar aproximadamente este balance.

## Referencia: personaje nivel 1

Jugador inicial de referencia:
- nivel 1;
- atributos base 10;
- HP 100;
- competencia general 0;
- arma básica de referencia `BaseArma = 10`;
- impacto físico base aproximado 55%.

El objetivo no es que todos los personajes tengan el mismo resultado, sino que estas criaturas ocupen claramente bandas distintas de riesgo.

---

## Mordelinde

**Rol canónico:** criatura menor común que prefiere huir y muerde si queda acorralada.

### Perfil v1
- nivel de referencia XP: **1**
- HP: **28**
- precisión ofensiva: **45%**
- daño bruto por ataque: **5**
- evasión/reducción equivalente: **ligera**, objetivo aproximado 15% de reducción de impacto efectivo por movilidad
- conducta: prioriza huida si dispone de salida; no persigue al jugador fuera de su espacio inmediato

### Comportamiento esperado
Para un personaje nivel 1:
- **Favorable** si el Mordelinde tiene vía de escape y no está acorralado;
- **Comparable bajo** si se fuerza el combate y la criatura responde.

Debe enseñar combate sin dejar al jugador cerca de morir salvo decisiones muy malas o acumulación previa de daño/fatiga.

---

## Espinajo de rastrojo

**Rol canónico:** criatura menor territorial que advierte y embiste cerca de alimento/crías.

### Perfil v1
- nivel de referencia XP: **2**
- HP: **40**
- precisión ofensiva: **50%**
- daño bruto por ataque: **8**
- reducción física equivalente: **10%**
- conducta especial: la primera embestida puede usar **60% precisión** si el jugador ignora una advertencia territorial legible

### Comportamiento esperado
Para un personaje nivel 1:
- **Comparable** si el jugador entiende la conducta y entra preparado;
- **Peligroso** si ignora la advertencia y recibe/permite la embestida inicial.

No debe atacar de manera inevitable al entrar en la habitación. El peligro nace de acercarse/insistir según la escena del Narrador.

---

## Cornalomo

**Rol canónico:** amenaza superior de los Llanos de Edran; no es presa inicial.

### Perfil v1
- nivel de referencia XP: **8**
- HP: **120**
- precisión ofensiva: **65%**
- daño bruto por ataque: **20**
- reducción física equivalente: **20%**
- conducta: pesada, poderosa; no necesita perseguir indefinidamente a un principiante para cumplir su función narrativa

### Comportamiento esperado
Para un personaje nivel 1:
- `evaluar Cornalomo` debe devolver **Abrumador**;
- un combate directo prolongado debe ser claramente desfavorable;
- las señales previas deben dar oportunidad real de evitarlo/retroceder;
- su derrota NO es requisito para completar VT-NAR-003.

El valor de referencia 8 es de balance, no una afirmación de canon o “nivel visible” de la criatura.

---

## Recompensas orientativas

Antes de antifarmeo/grupo:

### Mordelinde referencia 1
- Favorable: ~7 XP;
- Comparable: ~12 XP;
- primera victoria de familia en Edran: +5 XP una vez.

### Espinajo referencia 2
`XP_siguiente(2) ≈ 118`
- Comparable: ~14 XP;
- Peligroso: ~24 XP;
- primera victoria de familia en Edran: ~6 XP una vez.

### Cornalomo referencia 8
La recompensa se calcula normalmente, pero para un nivel 1 queda limitada por el tope de **25% de su nivel actual**. No se usa como objetivo de progreso temprano.

## Criterio de playtest

Ajustar números si ocurre cualquiera de estos extremos:
- Mordelinde mata de forma habitual a un jugador nivel 1 sano;
- Mordelinde tarda tanto en caer que se siente como enemigo importante;
- Espinajo no comunica diferencia clara respecto a Mordelinde;
- Espinajo mata al principiante antes de que pueda tomar una decisión de huida;
- Cornalomo resulta razonablemente farmeable por un personaje nivel 1;
- la opción óptima sigue siendo esperar respawn de Mordelindes en una sola sala.

Los ajustes numéricos posteriores no requieren cambiar el canon.
