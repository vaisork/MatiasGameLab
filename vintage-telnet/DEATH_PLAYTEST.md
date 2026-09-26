# Vintage Telnet — Prueba controlada de muerte DEATH-01

**Objetivo:** probar de extremo a extremo la muerte de un personaje mediante combate real, sin usar comandos administrativos de “matar jugador”.

**Issue:** #213  
**Responsable mecánico:** Diseñador de Jugabilidad

## 1. Enemigo de prueba

Usar **Cornalomo**, ya existente en canon y ya balanceado en `STARTER_CREATURE_BALANCE.md` como amenaza superior de Edran.

Perfil aprobado para DEATH-01:

- nivel de referencia XP: **8**
- HP: **120**
- precisión: **65%**
- daño bruto por ataque: **20**
- reducción física: **20%**
- dificultad esperada para nivel 1 sano: **Abrumador**
- no es objetivo normal de progreso temprano

No crear un “enemigo de QA” artificial si Cornalomo puede ejercer el flujo real.

## 2. Acceso

El encuentro debe estar:
- fuera de la ruta obligatoria;
- en un ramal/subcamino opcional;
- precedido por señales fuertes de peligro;
- con posibilidad de retroceder antes de iniciar combate.

El jugador debe elegir conscientemente acercarse/atacar.

## 3. Huida

Cornalomo no debe convertir el test en una trampa.

Para DEATH-01:
- conservar la fórmula general de huida;
- permitir intentos repetidos y el bonus vigente por fallos previos;
- no introducir bloqueo especial de huida.

La muerte se prueba simplemente decidiendo permanecer en combate.

## 4. Consecuencia de muerte durante esta prueba

Al alcanzar **0 HP**:

1. termina inmediatamente el combate;
2. se elimina el encuentro activo del personaje;
3. el jugador reaparece en **`valdren_centro`** para esta primera prueba de Edran;
4. HP al reaparecer: **60% del máximo**;
5. fatiga: **40**;
6. herida: baja un grado;
7. XP/nivel/PA/PP no se pierden;
8. inventario ordinario permanece;
9. armadura permanece;
10. arma equipada **NO se pierde en DEATH-01**.

### Motivo para suspender pérdida de arma

GAMEPLAY §11 permite que una derrota frente a una amenaza excepcional llegue a provocar pérdida de arma, pero ese flujo de recuperación/transferencia todavía no está cerrado.

DEATH-01 valida únicamente:

**combate → 0 HP → muerte → respawn → persistencia**

No mezclar en la misma prueba la mecánica todavía abierta de pérdida de arma.

Una segunda prueba futura podrá validar BOSS-LOSS cuando ese contrato exista.

## 5. Qué debe ver el jugador

La muerte debe ser claramente legible.

Mínimo:
- último golpe/consecuencia;
- mensaje inequívoco de derrota/muerte;
- indicación de que ha reaparecido en un lugar seguro;
- estado posterior visible (HP/fatiga/herida).

No mostrar stack técnico, reset silencioso ni simplemente teletransportar sin explicación.

El texto definitivo pertenece al Narrador.

## 6. Persistencia que debe sobrevivir

Antes de la prueba registrar:
- nivel y XP;
- PA/PP;
- inventario;
- equipo;
- descubrimientos/mapa;
- personaje/cuenta.

Después de morir y después de reconectar, comprobar que permanecen iguales salvo:
- ubicación;
- HP;
- fatiga;
- herida;
- combate activo.

## 7. Pruebas técnicas mínimas

### A. Muerte atacando
Nivel 1 entra al encuentro y continúa atacando hasta 0 HP.

Comprobar:
- outcome defeat;
- encuentro eliminado;
- room = `valdren_centro`;
- HP = round(0.60 × HPmax);
- fatigue = 40;
- herida degradada;
- no arma perdida;
- no XP perdida.

### B. Muerte intentando huir
Forzar RNG reproducible para que falle una huida y el golpe recibido lleve a 0 HP.

Debe producir exactamente el mismo estado de respawn.

### C. Muerte defendiendo
Cubrir al menos una defensa (esquivar/resistir/bloquear cuando aplique) cuyo golpe residual cause 0 HP.

Debe usar el mismo flujo.

### D. Reconexión
Después de morir:
- cerrar sesión o recrear cliente;
- volver a entrar;
- comprobar que sigue en `valdren_centro`;
- no existe combate fantasma;
- estado postmuerte persiste.

### E. Repetición
El jugador debe poder volver posteriormente al mundo sin quedar atascado en estado “muerto”.

## 8. Prueba humana de Javier

Para la primera prueba manual:

1. usar personaje de nivel 1;
2. registrar visualmente HP/equipo antes del encuentro;
3. seguir las señales hasta el ramal opcional;
4. usar `evaluar`: debe comunicar **Abrumador**;
5. iniciar el combate voluntariamente;
6. **no huir**;
7. dejar que Cornalomo derrote al personaje;
8. revisar mensaje de muerte;
9. comprobar respawn en Valdren;
10. abrir Personaje/Inventario y verificar persistencia;
11. recargar/reconectar y verificar de nuevo.

## 9. Criterio de éxito

DEATH-01 está aprobada si Javier puede morir en una pelea normal y sentir claramente:

**“me derrotaron, reaparecí, sigo siendo mi mismo personaje y puedo continuar jugando.”**

No es necesario derrotar a Cornalomo para aprobar la prueba.
