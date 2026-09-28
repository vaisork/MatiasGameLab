# Vintage Telnet — Contrato común de playtest para pools regionales v1

**Autoridad:** Diseñador de Jugabilidad  
**Ámbito:** HOSHAI-01, KORVEN-01, LETHRA-01, NHAL-01  
**No sustituye:** canon ecológico, mapping por room_id ni balance individual de criatura.

Este documento define cómo validar cualquier pool regional antes de considerarlo estable.

## 1. Prueba estadística por perfil de densidad

Para cada chance configurada distinta de 0%, ejecutar al menos **200 entradas elegibles** con RNG controlable.

Verificar:
- frecuencia observada razonablemente próxima a la chance declarada;
- distribución de criaturas próxima a los pesos declarados;
- resultado reproducible con semilla/RNG inyectado;
- 0 encuentros aleatorios en salas excluidas.

No se exige igualdad exacta a la probabilidad teórica en una muestra de 200; se busca detectar configuración equivocada, sesgo severo o inclusión indebida.

## 2. Exclusiones obligatorias

Por región comprobar:
- 0 fauna ordinaria en centro del pueblo/interiores/forja/mercado/salas seguras;
- 0 aparición de amenaza superior regional;
- 0 contaminación de encuentros scripted;
- 0 fauna regional en salas ya declaradas transición o región distinta.

Amenazas superiores fuera de pools ordinarios:
- Edran: Cornalomo;
- Hoshai: Rasgacumbres;
- Korven: Quebrarrocas;
- Lethra: Dorsalodo;
- Nhal: Rasgacorteza.

## 3. Recorrido completo

Ejecutar como mínimo **20 recorridos completos** desde el pueblo regional hacia el límite/transición definido y registrar:
- cantidad total de encuentros;
- recorridos sin combate;
- encuentros por cada 10 transiciones;
- concentración anormal en puertas/ida-vuelta;
- repetición excesiva de una sola familia.

Debe seguir siendo normal completar algunos recorridos sin combate.

## 4. Ritmo objetivo

Para v1:
- 10% = borde/presencia ocasional;
- 20% = camino regional activo;
- 30% = tramo tenso/silvestre;
- 35% solo cuando Jugabilidad lo autorice explícitamente.

En una banda de 30% el objetivo práctico a largo plazo sigue siendo aproximadamente **no más de 3–4 encuentros por 10 transiciones**.

No convertir una ruta de lectura/exploración en una secuencia casi continua de combate.

## 5. Combate no obligatorio

El test debe comprobar que “aparece fauna” no equivale necesariamente a “empieza combate”.

Cuando la criatura/canon lo permitan:
- observar;
- continuar;
- retirarse;
- dejar que la criatura huya;
deben seguir siendo desenlaces válidos.

Los pools prueban presencia regional, no una máquina automática de XP.

## 6. Antifarmeo

Validar:
- XP usa familia correcta;
- reglas generales de antifarmeo siguen vigentes;
- entrar/salir repetidamente de dos salas no crea una vía claramente dominante de progreso;
- cooldown/reglas vigentes de encuentros no se saltan por cambiar de región.

## 7. Playtest por criatura

Antes de integrar un pool con criatura nueva, su issue individual debe tener:
- perfil mecánico exacto;
- mínimo 40 combates por clase a nivel 1 cuando esa sea su banda objetivo;
- victoria/derrota;
- rondas;
- HP y fatiga final;
- comportamiento de huida;
- comparación con criatura de referencia.

El pool no corrige un enemigo mal balanceado: primero se corrige la criatura.

## 8. Gate humano

Recorrer la región manualmente al menos ida/vuelta y responder:
1. ¿La fauna parece pertenecer al lugar?
2. ¿Se percibe cambio gradual al alejarse del pueblo?
3. ¿Hay pausas reales?
4. ¿Se repite demasiado una sola criatura?
5. ¿Se puede recordar la ruta por algo más que sus combates?
6. ¿Algún encuentro parece inevitable sin razón narrativa?

Si la ruta se siente como “camino → monstruo → camino → monstruo”, el pool falla aunque las estadísticas coincidan.

## 9. Criterio de aprobación

Un pool regional v1 se aprueba cuando:
- probabilidades/pesos funcionan;
- exclusiones son 100% respetadas;
- amenazas superiores nunca entran;
- existe variación de recorridos;
- existen recorridos sin combate;
- el ritmo no destruye exploración/lectura;
- las criaturas conservan su identidad ecológica;
- no aparecen regresiones en encuentros scripted ni en otras regiones.

**Principio:** un pool regional debe hacer que el mundo parezca vivo, no que parezca una tabla de encuentros.
