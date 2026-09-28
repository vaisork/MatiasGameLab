# VT-NAR — Corredor de Cargallanura (#358)

**Fuente geográfica:** PR #433  
**Capa:** Narrativa  
**Zona:** ramal de ida y vuelta desde la Senda del Viento Bajo, después de Borde de los Cardos y antes de Parada de los Cardos en sentido Valdren.

El corredor tiene **7 ubicaciones significativas**. No es guarida, mazmorra ni territorio de Cornalomo.

## Secuencia

| orden | room_id propuesto | nombre visible | anillo | función |
|---|---|---|---|---|
| 1 | `cargallanura_boca_corredor` | Boca del corredor ancho | I | desvío reconocible y retorno inmediato |
| 2 | `cargallanura_hierba_hundida` | Hierba hundida | I | confirma escala sin mostrar criatura |
| 3 | `cargallanura_senda_ancha` | Senda de las huellas anchas | II | descubrimiento significativo |
| 4 | `cargallanura_loma_baja` | Loma baja | II | observación larga y posible avistamiento |
| 5 | `cargallanura_cruce_antiguo` | Cruce de paso animal | II | punto fuerte de retorno |
| 6 | `cargallanura_descanso_hundido` | Hondonada de descanso | III | proximidad inequívoca, sin combate automático |
| 7 | `cargallanura_paso_abierto` | Paso abierto | III | decisión final antes de cualquier enfrentamiento |

Geometría: 1↔2↔3↔4↔5↔6↔7. El único regreso a la ruta principal es desde 1 al mismo punto de derivación. Desarrollo no debe conectar este ramal con Valdren, Camino de los Campos ni Pastos Altos.

## Anillo I — leer antes de arriesgar

### Boca del corredor ancho
La huella humana sigue clara, pero una franja de hierba aplastada se abre hacia el pastizal. Es demasiado ancha para parecer un sendero de viajeros. Entre los tallos quedan ramas bajas quebradas y varias huellas profundas.

No hay combate. Desde aquí debe ser evidente cómo regresar a la Senda.

### Hierba hundida
La franja continúa sobre pasto poco trabajado. Algunos tallos están doblados en la misma dirección y la fauna menor se oye menos dentro del corredor que fuera de él.

No mostrar Cargallanura aquí, incluso si la fase global indica presencia.

## Anillo II — territorio activo

### Senda de las huellas anchas
Las pisadas aparecen con suficiente separación para revelar el tamaño del animal que repite este paso. El corredor ya parece una ruta animal estable, no un rastro aislado.

Al entrar por primera vez puede registrarse `cargallanura_corredor_descubierto`.

Si Cargallanura está presente, todavía no hace falta mostrarlo: puede haber desplazamiento lejano de hierba o una silueta demasiado distante para iniciar combate.

### Loma baja
Un desnivel suave permite mirar el pastizal abierto. Aquí la presencia puede confirmarse a distancia sin bloquear retirada.

**Presente:** una masa enorme cruza o permanece lejos, con tiempo para observar/evaluar o retroceder.  
**Ausente:** solo se ven franjas de paso reciente y pasto que empieza a levantarse.

### Cruce de paso animal
Dos trazas de tránsito animal se cruzan sobre suelo castigado. Es el último punto cómodo para decidir que ya se vio suficiente.

Punto fuerte de retorno. Nunca inicia combate al entrar.

## Anillo III — proximidad crítica

### Hondonada de descanso
El terreno está hundido por peso repetido. Hay huellas recientes, vegetación aplastada y señales de que un cuerpo enorme descansó aquí, pero el lugar no es un nido.

**Presente:** sonidos pesados, vegetación moviéndose o visión parcial anuncian proximidad antes de avanzar.  
**Ausente:** las mismas señales territoriales permanecen sin convertirlas en aparición falsa.

### Paso abierto
El corredor desemboca en una franja amplia de pastizal. No hay cobertura que justifique una emboscada.

Si está presente, Cargallanura debe ser visible o inequívocamente localizado **antes** de que exista combate. El jugador conserva decisión explícita: apartarse/esperar, retroceder, observar/evaluar o provocar/iniciar.

Solo una decisión que realmente comprometa el encuentro permite pasar al flujo de `cargallanura_charge` de #339/#216. Narrativa no resuelve esa mecánica.

Si está ausente, la sala permanece explorable con rastros recientes y no genera combate.

## Reglas de presentación

- Anillos I y II: cero combate forzado.
- Entrada/salida/reconnect no cambia presencia; Narrativa consume el estado 40/60 fijado por Jugabilidad.
- Las señales persisten tanto con presencia como ausencia.
- No usar señales propias de Cornalomo como si fueran intercambiables.
- No recompensa de jefe, no pérdida de arma y no XP repetida por rastros.
- La primera visita puede terminar en cualquier punto sin ver al animal.
- La retirada previa al combate siempre debe quedar narrativamente legible.

## Handoff

Historia/geografía: PR #433.  
Jugabilidad/presencia: #358; ataque: #339 y dependencia #216.  
Desarrollo puede materializar estos siete IDs cuando Arquitectura libere el motor técnico #335/#216. No implementar lógica paralela para suplir esas dependencias.
