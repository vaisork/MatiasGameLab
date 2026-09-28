# Vintage Telnet — Primer jefe C5: Rompecuña

**Origen:** #363  
**Responsable:** Historiador y Constructor del Mundo  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Alcance:** identidad canónica del primer jefe único. Sin estadísticas, fases mecánicas, recompensa ni balance.

---

## Identidad

**boss_id canónico sugerido:** `rompecuna`  
**Nombre visible:** **Rompecuña**

Rompecuña es un **ejemplar único** de gran fauna pétrea no catalogada como especie regional ordinaria.

No es:
- Cornalomo;
- Quebrarrocas;
- Cargallanura;
- Arcane;
- constructo;
- criatura mágica;
- representante de una nueva familia que deba entrar a pools.

En el conocimiento actual del mundo no existen otros ejemplares confirmados.

---

## Forma física

Rompecuña es un cuadrúpedo muy pesado adaptado a empujar y fracturar material suelto.

Rasgos canónicos:
- cuerpo bajo y ancho;
- extremidades delanteras especialmente robustas;
- cuello corto;
- cráneo en forma de cuña ancha, sin cuerno independiente;
- placas dérmicas gruesas concentradas en hombros, frente y dorso anterior;
- superficie corporal mate, gris oscura y terrosa;
- patas posteriores más cortas que las delanteras;
- ojos pequeños laterales;
- respiración audible y vibración del suelo al cargar peso contra roca.

Sus placas son tejido biológico endurecido.  
No son piedra, metal, cristal ni armadura fabricada.

No excava túneles largos. Puede:
- apartar grava;
- empujar bloques;
- ensanchar grietas cortas;
- romper material ya fracturado.

---

## Territorio

Primer territorio canónico:

**Cantera Abandonada — detrás del frente de extracción, más allá del umbral CA-09.**

La cantera superficial permanece exactamente como ya fue definida.

Rompecuña ocupa una **cavidad natural posterior** conectada al hueco detrás del frente.

La existencia de Rompecuña:

- NO explica quién abrió la cantera;
- NO explica por qué fue abandonada;
- NO convierte la cantera en mina;
- NO prueba que la criatura haya vivido allí durante toda la historia del lugar.

Su llegada o permanencia en la cavidad es posterior o indeterminada.

---

## Por qué es C5

Rompecuña es C5 porque el encuentro representa **un individuo concreto cuya eliminación cambia persistentemente ese lugar**.

No porque su especie sea superior por categoría.

Rasgos que lo separan de C3/C4:

1. hay un solo Rompecuña;
2. su territorio final está ligado a una cámara concreta;
3. derrotarlo es irreversible;
4. muerto, no reaparece;
5. el estado de su cámara cambia para todos los jugadores;
6. su encuentro requiere cruzar deliberadamente el último retorno del ramal.

Quebrarrocas sigue siendo amenaza C3 regional.  
Cargallanura sigue siendo fauna mayor C4.  
Ninguna de esas categorías cambia por existir Rompecuña.

---

## Conducta

Rompecuña no caza viajeros por la región.

Dentro de su cavidad:
- tolera presencia lejana durante poco tiempo;
- bloquea físicamente la continuidad profunda;
- reacciona a aproximación directa;
- usa masa y empuje;
- intenta arrinconar antes que perseguir largas distancias.

No sale a recorrer la Senda del Viento Bajo.

No aparece aleatoriamente en la Cantera Abandonada.

---

## Señales canónicas

Antes del compromiso pueden existir:

- polvo desprendido sin viento;
- marcas anchas de arrastre sobre grava;
- bloques movidos recientemente;
- raspaduras bajas en piedra;
- vibraciones espaciadas;
- ausencia relativa de Cavapolvo y Colagrieta cerca del umbral final;
- respiración grave cuando el viajero ya está cerca de la cámara.

Estas señales no obligan a combate.

---

## Relación con fauna local

Cascapedernal, Colagrieta y Cavapolvo evitan la proximidad inmediata de la cámara cuando Rompecuña está activo.

No son subordinados ni crías.

Rompecuña no controla otras criaturas.

Su presencia crea una zona de exclusión por tamaño, ruido y desplazamiento físico.

---

## Cambio persistente al morir

Cuando Rompecuña muere:

1. **`rompecuna_defeated=true`** queda como estado mundial persistente.
2. Rompecuña no reaparece.
3. Cesan las vibraciones y señales frescas atribuidas al individuo.
4. La cámara deja de estar territorialmente bloqueada por él.
5. El paso posterior de la cavidad puede quedar disponible para futura expansión, **sin definir todavía qué existe más allá**.
6. Narrativa puede mostrar con el tiempo retorno de fauna menor al entorno exterior del umbral.

La muerte NO:
- revela el origen de la cantera;
- abre automáticamente una civilización/ruina secreta;
- entrega tesoro por canon;
- transforma la región;
- extingue una especie.

---

## Compatibilidad con BOSS-LOSS-01

Historia confirma que Rompecuña es compatible con:

`weapon_loss_on_defeat = true`

pero no define aquí la mecánica exacta.

Lectura física permitida:
- durante una derrota, un arma puede quedar perdida dentro del espacio de compromiso al ser separada del personaje por el empuje/caída del enfrentamiento;
- Rompecuña **no colecciona armas**;
- no consume ni destruye mágicamente el objeto;
- la pérdida no implica que el boss sea inteligente o ladrón.

Esto deja a Narrativa/Jugabilidad definir una ruta clara y recuperable sin contradecir la criatura.

---

## Límites

No definir desde Historia:
- HP;
- precisión;
- daño;
- armadura;
- fases mecánicas;
- nivel recomendado;
- XP;
- recompensa;
- chance de huida;
- condición exacta de pérdida/recuperación del arma.

---

## Handoff

### Narrativa
Ya puede definir:
- aproximación desde CA-09;
- último retorno;
- entrada/compromiso;
- fases narrativas;
- derrota/victoria;
- recuperación legible del arma.

### Jugabilidad
Puede cerrar el perfil C5 y BOSS-LOSS-01.

### Desarrollo
No debe implementar contenido concreto hasta recibir Narrativa + Jugabilidad cerradas.

---

## Estado

**HISTORIA #363 COMPLETA.**
