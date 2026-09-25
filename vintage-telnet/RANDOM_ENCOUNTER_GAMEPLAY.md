# Vintage Telnet — Estrategia de Jugabilidad para Encuentros Aleatorios

**Responsable:** Diseñador de Jugabilidad — Vintage Telnet  
**Estado:** V1 DE TRABAJO PARA EXPANSIÓN DEL MUNDO  
**Motor técnico:** Issue #160 / PR #165  
**Regla base:** `GAMEPLAY.md` §33

## 1. Cambio de enfoque

Con el motor reusable de encuentros, Jugabilidad deja de colocar monstruos sala por sala.

A partir de ahora el trabajo se organiza en tres capas:

1. **Perfil de zona** — Jugabilidad define densidad, riesgo y ritmo.
2. **Ecología canónica** — Historiador define qué criaturas pueden existir allí.
3. **Uso narrativo** — Narrador decide qué encuentros deben seguir siendo scripted, qué señales preceden amenazas y qué momentos tienen valor de escena.

Desarrollo convierte esos contratos en configuración. No decide balance ni hábitat.

---

## 2. Perfiles de densidad

Una sala exterior elegible debe pertenecer a uno de estos perfiles mecánicos.

| Perfil | Probabilidad por entrada | Uso |
| --- | ---: | --- |
| Seguro | 0% | pueblo, hogar, recuperación segura, interior civil |
| Borde habitado | 10% | primeras afueras, campos muy cercanos, tránsito humano frecuente |
| Camino | 20% | viaje normal entre zonas y rutas exteriores |
| Silvestre | 30% | campo, bosque, sierra, humedal o pedral alejados del asentamiento |
| Riesgo alto | 35% | sector exterior explícitamente peligroso y bien señalado |

La banda ordinaria sigue siendo 10–35%. Cualquier tasa mayor necesita revisión explícita de Jugabilidad.

### Objetivo de ritmo

En un trayecto suficientemente largo, la experiencia deseada es aproximadamente:

- **camino normal:** 1–3 encuentros aleatorios por cada 10 transiciones elegibles;
- no convertir cada movimiento en interrupción;
- tampoco permitir que un viaje largo se sienta completamente vacío.

Las probabilidades son medias de largo plazo, no garantías.

---

## 3. Composición de pools iniciales

En zonas de inicio, los pools aleatorios deben favorecer fauna común.

Si una región tiene dos criaturas menores canónicas, referencia inicial:

- criatura común/evasiva: **70% del peso relativo**;
- criatura territorial o más exigente: **30% del peso relativo**.

Esto es un punto de partida de balance, no canon. Puede ajustarse después de playtest.

### Amenazas superiores

Las amenazas regionales superiores —Cornalomo, Rasgacumbres, Quebrarrocas, Dorsalodo, Rasgacorteza y equivalentes— **no entran por defecto en los pools aleatorios ordinarios de las zonas iniciales**.

En la primera etapa deben aparecer mediante:
- señales;
- encuentro scripted;
- zona avanzada explícita;
- pool especial previamente validado.

Un jugador principiante no debe morir porque una tirada común decidió colocar una amenaza superior sin advertencia.

---

## 4. Encuentro no significa combate obligatorio

Que el motor genere una criatura significa que está **presente**.

No significa:
- que ataque automáticamente;
- que el jugador deba matarla;
- que bloquear el camino sea siempre obligatorio.

La conducta canónica sigue importando:
- fauna evasiva puede huir;
- territorial puede advertir;
- oportunista puede ignorar al jugador;
- una criatura puede convertirse en información ambiental antes que en combate.

La decisión de combatir sigue siendo del jugador cuando el contexto lo permita.

---

## 5. Scripted vs. aleatorio

Los encuentros escritos se reservan para momentos donde importa:

- enseñar una mecánica;
- presentar una criatura por primera vez;
- entregar una pista;
- cambiar el estado narrativo;
- mostrar una amenaza superior;
- producir una recompensa/hito;
- garantizar una experiencia concreta.

El motor aleatorio se usa para:
- dar vida al trayecto;
- evitar que todas las criaturas aparezcan siempre en el mismo punto;
- crear incertidumbre ligera;
- hacer que volver a recorrer una ruta no sea idéntico.

**Scripted construye significado; aleatorio construye variación.**

---

## 6. Progresión del riesgo por distancia

No fijamos monstruos por coordenada, pero sí una lógica de riesgo:

**pueblo seguro → borde habitado → camino → zona silvestre → sector de riesgo**

Alejarse debe permitir una transición gradual de:
- menor frecuencia;
- fauna más conocida;
- encuentros más evitables;

hacia:
- mayor frecuencia;
- combinaciones más exigentes;
- menor margen de error;
- amenazas que necesitan lectura previa.

El cambio no debe depender únicamente del nivel numérico del jugador; también del lugar y de la información disponible.

---

## 7. Relación con XP y antifarmeo

Los encuentros aleatorios usan las mismas reglas de XP que cualquier criatura equivalente.

Se mantienen:
- primera victoria de familia;
- categoría de dificultad relativa;
- reducción por repetición;
- cooldown de aproximadamente 5 min por sala después de victoria.

No existe un bonus especial por ser encuentro aleatorio.

El motor no debe convertir entrar/salir repetidamente entre dos salas en la ruta óptima de progreso.

---

## 8. Cómo trabajar cada nueva región

Para cada región o tramo nuevo, Jugabilidad espera un handoff breve con:

### Del Historiador
- contextos/salas exteriores canónicamente elegibles;
- criaturas menores que viven allí;
- amenazas superiores que NO deben entrar en pool ordinario;
- cualquier restricción ecológica relevante.

### Del Narrador
- encuentros que deben permanecer scripted;
- señales previas de amenazas;
- tramos que necesitan sentirse tranquilos o tensos por razones narrativas.

### Jugabilidad devuelve
- perfil de densidad;
- chance concreta;
- pesos relativos;
- límites de dificultad;
- exclusiones;
- criterio de playtest.

### Desarrollo
- solo configura el pool;
- no inventa tasa, peso, criatura ni elegibilidad.

---

## 9. Métricas de playtest

Para ajustar una zona, registrar como mínimo:

- transiciones exteriores;
- encuentros aleatorios generados;
- criatura encontrada;
- combates iniciados por el jugador;
- huidas;
- derrotas;
- HP/fatiga al terminar;
- repeticiones de la misma familia;
- número de transiciones entre encuentros.

Revisar si:
- hay menos de 1 encuentro cada ~10 transiciones durante trayectos largos y el mundo se siente vacío;
- hay más de 3–4 y caminar se vuelve una interrupción constante;
- una criatura domina casi todos los encuentros;
- el jugador aprende a farmear una puerta;
- las amenazas superiores aparecen sin lectura suficiente.

---

## 10. Aplicación inmediata a la región inicial

Mientras Historia/Narrativa no entreguen una asignación nueva:

- centros de pueblo, hogar, forjas y mercados: **Seguro 0%**;
- caminos generales entre asentamientos: candidato inicial a **Camino 20%**;
- afueras inmediatamente pegadas a pueblos: candidato a **Borde habitado 10%**;
- microaventuras scripted como *El lindero roto*: sus encuentros explícitos mantienen prioridad absoluta;
- amenazas superiores: fuera del pool ordinario.

No activar fauna concreta en producción hasta recibir el mapping canónico de Historia/Narrativa.

---

## Principio rector

**El motor decide si el mundo ofrece un encuentro; el canon decide qué puede vivir allí; la narrativa decide qué encuentros no deben dejarse al azar.**
