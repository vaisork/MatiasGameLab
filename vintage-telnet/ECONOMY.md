# Vintage Telnet — ECONOMY-01 / economía de sellos v1

**Autoridad de moneda/canon:** Historiador — `DARO_ECONOMY_CANON.md`  
**Autoridad de balance:** Diseñador de Jugabilidad  
**Issue origen:** #384  
**Ámbito inicial:** niveles bajos / primeras rutas / Daro en Valdren

---

# 1. Objetivo

La economía v1 debe conseguir cinco cosas:

1. que el jugador tenga motivos reales para ganar y gastar **sellos**;
2. que una compra importante requiera jugar, no solo crear personaje;
3. que descansar/recuperarse tenga coste de oportunidad sin convertirse en castigo;
4. que vender objetos no cree dinero infinito;
5. que el dinero acumulado no vuelva irrelevantes los precios después de pocas horas.

La economía NO debe convertirse todavía en:
- simulador de mercado;
- subasta entre jugadores;
- bolsa;
- precios dinámicos;
- durabilidad/reparación;
- hambre/sed;
- impuestos complejos.

---

# 2. Moneda

Moneda visible:

- singular: **1 sello**
- plural: **N sellos**

La cartera pertenece al **personaje**, no a la cuenta.

V1:
- entero no negativo;
- no fracciones;
- no transferencia entre personajes;
- no transferencia entre jugadores;
- no interés;
- no ingreso pasivo;
- no pérdida de sellos al morir.

La muerte ya tiene consecuencias de estado/posición y, en jefes específicos, puede tener consecuencias de arma. No se añade pérdida monetaria general.

---

# 3. Saldo inicial

Cada personaje recibe una sola vez:

**20 sellos**

al completar su creación inicial.

Objetivo:
- permitir 1–2 consumos/servicios básicos futuros;
- no permitir comprar inmediatamente un arma alternativa;
- enseñar que existe moneda sin regalar una mejora completa.

Personajes existentes al migrar ECONOMY-CORE reciben también 20 sellos una sola vez para no quedar en desventaja respecto de personajes nuevos.

Este saldo es un faucet inicial fijo y no repetible.

---

# 4. Regla central de creación de dinero

## Los monstruos NO dejan sellos por defecto

Fauna C1, amenazas C3 y fauna mayor C4 no llevan moneda de forma automática.

Derrotar una criatura puede:
- dar XP;
- completar una condición de contrato;
- producir un recurso futuro si contenido lo aprueba;

pero **no crea sellos directamente** por el simple hecho de matar.

Razones:
- coherencia de mundo;
- evita que matar la criatura más rápida sea la mejor fuente económica;
- separa progresión de combate de progresión monetaria;
- limita inflación.

## El dinero entra al mundo principalmente desde personas/instituciones

Fuentes autorizadas:
1. saldo inicial;
2. trabajos/encargos;
3. recompensas monetarias únicas por hitos;
4. venta de objetos ordinarios;
5. contenido futuro que declare explícitamente una recompensa monetaria.

No otorgar sellos automáticamente por:
- entrar a una sala;
- iniciar sesión;
- esperar;
- subir de nivel;
- morir;
- cada descubrimiento genérico;
- cada victoria común.

---

# 5. Presupuesto de recompensas monetarias

Para que Historia/Narrativa puedan crear encargos sin inventar balance:

| Tipo de contenido | Duración activa orientativa | Recompensa v1 |
| --- | ---: | ---: |
| microayuda local | 5–10 min | **4–6 sellos** |
| encargo corto de ruta | 10–20 min | **8–12 sellos** |
| encargo normal | 20–35 min | **14–20 sellos** |
| encargo largo/riesgoso | 35–60 min | **24–35 sellos** |
| hito monetario único excepcional | — | **hasta 40 sellos**, con revisión |

Objetivo de ingreso bruto temprano:

**aprox. 25–40 sellos por hora de juego activo**.

Esto es presupuesto, no salario garantizado.

Explorar, leer, combatir y viajar siguen teniendo valor aunque un tramo concreto no pague.

---

# 6. Trabajo repetible y antifarmeo monetario

La economía v1 debe preferir encargos:
- únicos;
- rotativos;
- o que exijan recorrido real.

Si se introduce un encargo repetible sin límite narrativo, usar antifarmeo por familia de contrato en una ventana móvil aproximada de 60 min:

- completaciones 1–2: **100%**
- completaciones 3–4: **60%**
- completaciones 5+: **30%**

El servidor debe mostrar la recompensa real antes de confirmar entrega cuando sea posible.

No aplicar esta reducción a contenido once-per-character.

No crear un “daily login reward”.

---

# 7. Daro — precios de venta

Daro vende solo el catálogo autorizado por Historia.

| Arma | Daro vende | Precio compra | Motivo de banda |
| --- | --- | ---: | --- |
| Varita de aprendiz | Sí | **40 sellos** | arma común, daño 7 |
| Puñal de camino | Sí | **50 sellos** | común, daño 8 |
| Arco de ruta | Sí | **65 sellos** | daño 9 + identidad de distancia |
| Espada de juramento | Sí | **85 sellos** | daño 10 + Bloquear/desviar |
| Hoja de Hoshai | **No** | — | progreso regional Khariel |
| Martillo de Korven | **No** | — | progreso regional Brumak |

La diferencia de precio NO modifica stats.

Comprar un arma más cara no concede:
- capacidad de clase;
- bono de precisión;
- nivel;
- atributo;
- poder.

## Espada como encargo

En v1 el “encargo simple” de la Espada de juramento se resuelve como compra inmediata a precio fijo.

No:
- espera real;
- materiales;
- crafting;
- stock aleatorio.

La narrativa puede llamarlo encargo/preparación sin introducir temporizador.

---

# 8. Reventa a Daro

Daro compra únicamente armas comunes de su catálogo ordinario.

Precio de reventa:

**35% del precio de compra base, redondeado hacia abajo.**

| Arma | Compra nueva | Daro paga al vender |
| --- | ---: | ---: |
| Varita de aprendiz | 40 | **14** |
| Puñal de camino | 50 | **17** |
| Arco de ruta | 65 | **22** |
| Espada de juramento | 85 | **29** |

Este diferencial del 65% es un **sumidero monetario**.

No hay:
- reembolso completo;
- buyback al mismo precio;
- negociación;
- descuento por Presencia;
- ofertas aleatorias;
en v1.

## Objetos que Daro NO compra

V1:
- Hoja de Hoshai;
- Martillo de Korven;
- objetos `forge_required`;
- recompensas únicas once-per-character;
- objetos de misión/hito;
- piezas cuya venta pueda romper una progresión que no tenga vía de recuperación.

Acolchado de Camino ganado como primera recompensa tampoco debe convertirse automáticamente en sellos hasta existir una vía ordinaria de reposición.

---

# 9. Seguridad al vender

Una venta requiere confirmación explícita.

Daro rechaza venderle:
- un objeto equipado;
- el **último arma utilizable** del personaje.

Para vender el arma equipada:
1. conseguir/poseer otra arma utilizable;
2. desequipar;
3. confirmar venta.

Esto evita que un jugador, especialmente uno joven, quede accidentalmente sin ninguna vía normal de combate.

La venta elimina la instancia del inventario y acredita sellos atómicamente.

Si la operación falla, no desaparece objeto ni cambia saldo.

---

# 10. Compra repetida

Las cuatro armas comunes pueden comprarse varias veces.

Cada compra:
- entrega **una instancia nueva**;
- cobra precio completo;
- no autoequipa;
- no altera clase;
- no concede poder;
- no hereda un estado de otra instancia.

Esto permite:
- reemplazo futuro;
- varias configuraciones;
- recuperación después de sistemas de pérdida autorizados.

No existe descuento por poseer ya una copia.

---

# 11. Inventario lleno

El inventario actual **no tiene límite de capacidad v1**.

Por tanto ECONOMY-01:
- no inventa slots;
- no rechaza compra por “inventario lleno”.

Si en el futuro se crea capacidad:
- comprobar espacio antes de cobrar;
- compra debe ser atómica;
- sin espacio → 0 sellos descontados.

---

# 12. Forja

Comprar y Forja son sistemas separados.

Daro v1 no vende las dos armas regionales `forge_required`.

Regla general futura:
- pagar por un objeto `forge_required` NO debe auto-validarlo;
- la instancia entra `forge_validated=false`;
- validación física sigue su propio flujo.

**Forja no es un impuesto monetario automático.**

No cobrar sellos simplemente por validar una pieza física, salvo que un contenido futuro defina además un servicio distinto y aprobado.

---

# 13. Sumideros monetarios

Sin sumideros, incluso recompensas pequeñas terminan acumulándose.

## Sumideros v1

### A. Compra de armas comunes
40–85 sellos.

Compra ocasional/importante.

### B. Reventa con pérdida
Recupera 35%, destruye 65% del valor nominal original si el objeto se compró con sellos.

### C. Recuperación/provisiones
REST-01 (§24.8–24.9) vuelve necesaria una vía legítima de recuperación completa.

Bandas de precio para contenido futuro:

| Servicio/recurso | Precio objetivo |
| --- | ---: |
| consumible de recuperación menor | **6–10 sellos** |
| consumible/servicio de recuperación media | **12–18 sellos** |
| recuperación completa segura | **24–30 sellos** |

Historia/Narrativa deben definir el objeto/servicio concreto antes de implementarlo.

No introducir hambre/sed.

### D. Servicios futuros
Pueden convertirse en sinks:
- viaje especial;
- alojamiento/recuperación;
- encargos de taller;
- cosméticos;
- servicios sociales.

Cada uno requiere contrato propio.

---

## Primer bucle P0 de recuperación

Para PLAYABLE-LOOP-01, los primeros valores ejecutables quedan fijados:

| Recurso/servicio | Precio | Efecto resumido |
| --- | ---: | --- |
| Provisión básica de camino | **8 sellos** | +18% HPmax, -20 fatiga, no reset field-rest |
| Servicio seguro de recuperación | **18 sellos** | hasta 90% HPmax, fatiga0, herida -1 grado, reset field-rest |

Los nombres visibles quedan para Historia/Narrativa; los números son de Jugabilidad.

La recuperación completa a100% permanece como servicio futuro de **24–30 sellos** y no bloquea el P0.

# 14. Relación con REST-01

El descanso gratuito es deliberadamente incompleto.

La economía no debe convertir esto en “paga o no puedes jugar”.

Objetivo:
- descanso de campo = recuperación parcial gratuita;
- provisiones = permiten continuar una expedición;
- recuperación completa = opción más cara/segura;
- muerte/respawn sigue siendo una salida, no una estrategia económica óptima.

Una provisión futura que reinicie el presupuesto de descanso debe tener coste suficiente para que repetirla sea un sink real.

No permitir una comida de 1–2 sellos que reinicie ilimitadamente REST-01.

---

# 15. Flujo de moneda

Flujo esperado temprano:

```
creación de personaje
        ↓ +20
      cartera
        ↓
encargos / hitos ────────→ +sellos
        ↓
      cartera
   ↙      ↓       ↘
armas  provisión  servicio
 -40..85  -6..18   -24..30
   ↓
inventario/recuperación

inventario común
        ↓ vender
     +35% valor
        ↓
      cartera
```

Fauna/combate alimentan el flujo **indirectamente** cuando forman parte de un encargo, no imprimiendo moneda por cada muerte.

---

# 16. Inflación v1

En una economía sin mercado de jugadores, el problema inicial no es inflación de precios entre personas; es **exceso de poder adquisitivo por personaje**.

Por eso v1 NO usa precios dinámicos.

## No hacer

- subir precio porque el servidor tenga muchos sellos;
- precios distintos por jugador;
- inflación diaria automática;
- descuentos RNG;
- multiplicadores por nivel;
- interés bancario.

Eso vuelve la economía difícil de comprender y castiga a jugadores nuevos.

## Controlar la masa monetaria mediante

1. faucets limitados;
2. payout por tiempo/riesgo;
3. no dinero directo de monstruos;
4. reventa al 35%;
5. sinks recurrentes;
6. sin transferencias/player market v1;
7. telemetría de ledger.

---

# 17. Objetivos cuantitativos de balance

Para niveles bajos:

- ingreso bruto activo esperado: **25–40 sellos/h**;
- gasto recurrente de un jugador que viaja/recibe daño: **8–20 sellos/h**;
- ahorro neto típico: **10–25 sellos/h**.

Resultado buscado:
- Varita/Puñal alternativo: alcanzable en ~1–2 h si se ahorra;
- Arco: compra deliberada, no instantánea;
- Espada: objetivo de ahorro temprano de ~2–4 h según gasto;
- usar provisiones retrasa compras, creando decisión real.

No todos los jugadores deben seguir exactamente esta curva.

---



# 17.1 Escenarios de ahorro temprano

Los precios se validan contra tres perfiles, partiendo de **20 sellos iniciales**.

## A. Jugador ahorrador
- ingreso: 35–40 sellos/h;
- gasto en recuperación: 5–10 sellos/h;
- ahorro neto: 25–35 sellos/h.

Tiempo aproximado desde creación:
- Varita 40 → **<1 h**
- Puñal 50 → **~1 h**
- Arco 65 → **~1.5 h**
- Espada 85 → **~2 h**

Este jugador elige posponer recuperación/consumo y debe progresar más rápido económicamente.

## B. Jugador normal
- ingreso: 30–35 sellos/h;
- gasto: 10–15 sellos/h;
- ahorro neto: 15–25 sellos/h.

Tiempo aproximado:
- Varita → **1–1.5 h**
- Puñal → **1.5–2 h**
- Arco → **2–3 h**
- Espada → **3–4 h**

Esta es la curva objetivo principal.

## C. Jugador castigado / mucha recuperación
- ingreso: 25–30 sellos/h;
- gasto: 18–20 sellos/h;
- ahorro neto: 5–12 sellos/h.

Puede tardar bastante más en comprar un arma, pero:
- ya posee un arma inicial funcional;
- comprar otra arma no es requisito para seguir jugando;
- puede mejorar su economía reduciendo daño, huyendo mejor o escogiendo encargos.

Si este perfil queda bloqueado para continuar la historia por falta de dinero, la economía falla.

## Conclusión de precios

Los precios **40 / 50 / 65 / 85** se mantienen para v1.

No bajarlos antes de playtest porque:
- el jugador empieza equipado;
- la compra es alternativa/mejora horizontal temprana, no acceso básico al combate;
- el saldo inicial de 20 reduce la primera barrera;
- la recuperación crea una decisión real entre seguridad y ahorro.

No subirlos mientras no exista evidencia de inflación real.

# 18. Alarmas de inflación

Registrar y revisar:

- sellos creados por personaje-hora;
- sellos destruidos por personaje-hora;
- saldo mediano por nivel;
- porcentaje de jugadores que pueden comprar Espada de juramento;
- fuente de cada crédito;
- destino de cada débito;
- volumen de reventa.

## Señales de exceso de dinero

Revisar balance si durante playtest real:

1. ratio `sellos_creados / sellos_destruidos` permanece > **2.0** en sesiones activas;
2. saldo mediano de nivel 1–5 supera **~170 sellos** sin ahorro deliberado;
3. saldo mediano hacia nivel 10 supera **~255 sellos**;
4. provisiones dejan de sentirse como decisión porque el saldo crece constantemente;
5. comprar todas las armas comunes se vuelve trivial.

Antes de subir precios:
1. identificar faucet excesivo;
2. reducir recompensa repetible;
3. añadir/ajustar sink útil;
4. solo después reconsiderar precios nominales.

---

# 19. Ledger autoritativo

Toda modificación de sellos debe pasar por una capa transaccional única.

Estado mínimo:
- `players.sellos INTEGER NOT NULL DEFAULT 20 CHECK(sellos >= 0)`

Ledger recomendado:
- transaction_id
- player_id
- delta
- balance_after
- reason_code
- source_key/ref_id opcional
- created_at

Reason codes mínimos:
- `starting_purse`
- `contract_reward`
- `milestone_reward`
- `shop_purchase`
- `shop_sale`
- `recovery_consumable`
- `recovery_service`
- `admin_adjustment`

Para recompensas one-shot:
- usar `source_key` idempotente;
- reconectar/repetir request nunca duplica pago.

El cliente nunca envía el precio autoritativo.

---

# 20. Atomicidad

## Compra

Una transacción:
1. validar catálogo;
2. validar saldo;
3. validar reglas de objeto;
4. debitar;
5. crear instancia;
6. registrar ledger;
7. commit.

Cualquier fallo → rollback completo.

## Venta

1. validar instancia pertenece al personaje;
2. validar no equipada;
3. validar vendible;
4. validar que no deja al personaje sin arma utilizable;
5. borrar/transferir instancia;
6. acreditar;
7. registrar ledger;
8. commit.

Cualquier fallo → rollback.

---

# 21. Relación con XP

XP y sellos son progresiones distintas.

No definir:
`1 XP = X sellos`.

Un contenido puede conceder ambas cosas, pero se balancean por separado.

Razón:
- XP mide progreso del personaje;
- sellos miden capacidad de intercambio.

Esto permite que explorar/leer/descubrir otorgue XP sin necesariamente imprimir dinero y que un trabajo cotidiano pague sellos sin requerir matar criaturas.

---

# 22. Relación con armas regionales

Hoja de Hoshai y Martillo de Korven:
- 0 precio en Daro;
- no son “caras”: **no están a la venta**;
- no se compran saltándose su contenido;
- no se venden a Daro v1.

El dinero no reemplaza reputación, acceso regional ni Forja.

Este principio debe mantenerse para futuras mejoras culturales importantes.

---

# 23. Fase de implementación

## ECONOMY-CORE-01

Implementar primero:
- cartera de sellos;
- saldo inicial 20;
- ledger;
- compra Daro;
- reventa Daro;
- atomicidad;
- UI de saldo;
- tests.

## ECONOMY-INCOME-01

Después:
- primeras recompensas monetarias reales en Valdren;
- usando presupuestos §5;
- sin money drops.

## RECOVERY-ECONOMY-01

Después:
- provisiones/servicios compatibles con REST-01;
- precios dentro de §13;
- contenido/canon separado.

---

# 24. Criterio de éxito

La economía v1 funciona si un jugador entiende:

- **cómo gana sellos**;
- **qué puede comprar**;
- **qué no puede comprar aunque tenga dinero**;
- **cuánto pierde al revender**;
- **por qué gastar en recuperación retrasa una compra**;
- **por qué matar fauna indefinidamente no imprime dinero**.

Y, después de varias horas, sigue existiendo una decisión entre:
- guardar;
- comprar equipo;
- pagar recuperación;
- continuar con recursos actuales.

**Principio:** el sello debe circular porque el jugador toma decisiones, no porque el servidor lo imprime con cada monstruo.
