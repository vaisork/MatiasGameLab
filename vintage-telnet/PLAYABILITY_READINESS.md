# Vintage Telnet — Readiness de Jugabilidad

**Responsable:** Diseñador de Jugabilidad — Vintage Telnet  
**Objetivo:** distinguir lo que realmente falta para jugar de lo que puede esperar a fases posteriores.  
**Fuente normativa:** `GAMEPLAY.md`

## Definición práctica de “jugable”

Para esta fase, Vintage Telnet se considera jugable cuando una persona puede, durante una sesión de 20–30 minutos:

1. entrar con un personaje persistente;
2. elegir especie;
3. salir de un pueblo;
4. leer/observar/examinar el entorno;
5. reconocer peligro;
6. combatir o evitar;
7. huir si corresponde;
8. recibir daño/fatiga/heridas;
9. descansar o morir/reaparecer;
10. ganar XP por combate y descubrimiento;
11. subir de nivel y conservar PA/PP;
12. regresar y continuar después de recargar/reconectar;
13. comprender qué cambió en su personaje y por qué.

No exige todavía tiendas, economía, crafting, Arcanes, poderes avanzados ni un mapa enorme.

---

## YA CERRADO POR JUGABILIDAD

- atributos y crecimiento;
- niveles 1–100;
- XP y antifarmeo;
- PA/PP;
- combate físico;
- daño/precisión;
- defensa;
- huida;
- HP;
- fatiga;
- heridas;
- descanso y recuperación segura;
- muerte/respawn;
- cooperación local;
- chat local;
- evaluación de peligro;
- mapa progresivo;
- rasgos de especies;
- Arcanes como vínculo/compañía/poder único;
- armadura y carga;
- catálogo inicial de armaduras validado;
- estado cualitativo de enemigos;
- inventario/equipamiento mínimo como regla (§32);
- comandos fundamentales.

---

## P0 — BLOQUEA EL PRIMER PLAYTEST JUGABLE

### 1. Terminar PR #49 — El lindero roto

Quedan correcciones ya detectadas por Arquitectura/Psicopedagogía:

- alinear Mordelinde/Espinajo con `STARTER_CREATURE_BALANCE.md`;
- no identificar nominalmente criatura sin evidencia/conocimiento legítimo;
- no conceder el descubrimiento mayor del lindero con evidencia insuficiente;
- hacer visible la diferencia conductual entre Mordelinde y Espinajo;
- no mostrar HP exacto de enemigo; usar GAMEPLAY §31;
- conservar P0 de Ayuda/chat;
- suite completa verde.

Una vez corregido, este PR ya representa el primer bucle real de juego.

### 2. Prueba real en teléfono/iPad/computadora

La prueba debe verificar:
- lectura legible;
- controles accesibles;
- Atacar/Huir no dominan cuando no aplican;
- inspección funciona sin teclado incómodo;
- estado del personaje no tapa la narración;
- recarga mantiene posición/progreso/descubrimientos.

Esto es prueba, no un nuevo sistema.

---

## P1 — NECESARIO PARA QUE DEJE DE SENTIRSE COMO DEMO Y EMPIECE A SENTIRSE RPG

### 3. Inventario/equipamiento real

GAMEPLAY §32 ya define la regla.

Falta implementación de:
- inventario persistente;
- arma activa;
- armadura activa;
- objeto de bloqueo activo;
- equipar/desequipar fuera de combate;
- estado de Forja;
- panel Inventario/Equipo.

Sin esto, una armadura o arma real no puede tener una consecuencia completa dentro del juego.

### 4. Sustituir BaseArma=10 por armas canónicas

El piloto puede usar BaseArma=10 internamente, pero el RPG real necesita:
- primer catálogo de armas;
- `base_damage` propuesto;
- si permiten bloquear;
- pequeñas propiedades explícitas;
- obtención narrativa/canónica.

Historiador propone objetos; Jugabilidad valida números.

### 5. Gasto de PA desde interfaz

La regla existe en §25, pero la experiencia necesita:
- ver PA disponibles;
- ver coste del siguiente punto;
- confirmar;
- resultado persistente;
- no permitir gasto durante combate.

### 6. Recuperación pasiva de fatiga

§24.7 está aprobada (~1 punto cada 10 s fuera de combate), pero el PR inicial la dejó pendiente técnica.

No bloquea El lindero roto, pero sí debe existir antes de considerar §24 completamente implementada.

### 7. Mapa visible mínimo

La lógica de conocimiento está cerrada en §23.

Falta una representación usable que muestre solamente:
- lugares conocidos/visitados;
- rutas conocidas/recorridas;
- sin secretos filtrados.

No necesita ser un mapa artístico complejo para ser útil.

---

## P1.5 — MUY VALIOSO PARA SENTIR MUNDO VIVO, PERO NO BLOQUEA EL PRIMER COMBATE

### 8. Primer NPC conversable

Ya existe contrato de NPC/Ollama y comando `hablar`.

Para una siguiente salida jugable conviene integrar al menos un NPC real con:
- ficha autoritativa;
- personalidad persistida;
- conocimiento limitado;
- memoria mínima de conversación/estado;
- Presencia sin auto-persuasión.

### 9. Primera recompensa de objeto

No hace falta crear loot aleatorio.

Basta una recompensa autoritativa de contenido que:
- entre al inventario;
- pueda equiparse si corresponde;
- se conserve entre sesiones.

Esto prueba el ciclo:
**descubrir/ganar → recibir objeto → equipar → notar diferencia**.

---

## P2 — EXPANSIÓN, NO BLOQUEAR PLAYTEST

No abrir como requisito de “jugable” todavía:

- moneda/oro;
- tiendas completas;
- comprar/vender;
- crafting/recetas;
- durabilidad/reparación;
- peso de mochila;
- intercambio libre entre jugadores;
- soltar objetos al suelo;
- party formal/guilds;
- chat global;
- quests tradicionales/diario de misiones;
- árbol completo de poderes;
- Arcanes implementados;
- comercio;
- economía de drops;
- transferencia/recuperación final de armas perdidas;
- recompensas físicas masivas;
- viaje rápido.

Estos sistemas pueden llegar después de observar la primera partida.

---

## Riesgo principal actual

El riesgo ya no es falta de diseño matemático.

El riesgo es **seguir definiendo sistemas sin probar el bucle que ya existe**.

Después de cerrar P0, la prioridad debe cambiar a:

**implementar → jugar → observar → ajustar**

antes de abrir más sistemas grandes.

## Próximo corte recomendado

1. corregir/integrar El lindero roto;
2. ejecutar playtest cerrado;
3. en paralelo implementar Inventario/Equipo;
4. Historiador entrega armas reales;
5. integrar una primera recompensa de objeto;
6. volver a jugar.

Ese ciclo convierte el prototipo técnico en RPG incremental sin inflar el alcance.
