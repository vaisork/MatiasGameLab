# Vintage Telnet — Perfiles mecánicos de amenazas regionales C3 v1

**Autoridad:** Diseñador de Jugabilidad  
**Motor:** GAMEPLAY §40 / Issue #335  
**Canon físico/narrativo:** `CREATURES.md`

Estas criaturas son **amenazas superiores regionales**, no fauna mayor C4 y no jefes C5.

Reglas comunes:
- fuera de pools C1 ordinarios;
- requieren `threat_zone_id` y advertencia previa;
- retirada antes de compromiso;
- cooldown C3 normal después de resolución;
- muerte del jugador no implica pérdida de arma;
- sin drop especial automático;
- sin escalado automático por nivel.

## Referencia existente — Cornalomo / Edran

Se conserva:
- reference_level: 8
- HP: 120
- precision: 65
- damage: 20
- armor_reduction: 20%
- amenaza C3, no jefe.

---

## Rasgacumbres — Hoshai

**Identidad:** depredador de montaña; presión alta por precisión/movilidad, no por blindaje.

### Perfil
- id: `rasgacumbres`
- family: `rasgacumbres`
- reference_level: **9**
- HP: **110**
- precision: **70**
- damage: **22**
- armor_reduction: **10%**
- flee_agilidad: **18**
- flee_percepcion: **17**

### Acción preparada v1
`rasgacumbres_descenso`
- señal: grava que cae / postura desde altura / reducción rápida de distancia;
- frontal: **false**
- interruptible: **true**
- precision: **76%**
- damage: **30**

No concede caída del jugador ni cambio de sala en v1.

### Conducta
- no persigue largas distancias en terreno llano;
- huida exitosa termina persecución;
- su amenaza debe sentirse ligada a desnivel/señales, no a aparición invisible.

---

## Quebrarrocas — Korven

**Identidad:** amenaza excavadora resistente; gana por masa y blindaje, no por precisión extrema.

### Perfil
- id: `quebrarrocas`
- family: `quebrarrocas`
- reference_level: **10**
- HP: **150**
- precision: **55**
- damage: **24**
- armor_reduction: **30%**
- flee_agilidad: **8**
- flee_percepcion: **11**

### Acción preparada v1
`quebrarrocas_empuje`
- señal: vibración fuerte, piedras desplazándose, cuerpo empujando desde terreno fracturado;
- frontal: **true**
- interruptible: **true**
- precision: **64%**
- damage: **34**

No derrumba la sala ni destruye rutas persistentemente en v1.

### Conducta
- no caza;
- intenta abrir salida si se siente cercado;
- una retirada del jugador debe resolver el conflicto cuando el contenido lo permita.

---

## Dorsalodo — Lethra

**Identidad:** depredador anfibio de borde de agua; peligro por golpe fuerte y lectura tardía del agua.

### Perfil
- id: `dorsalodo`
- family: `dorsalodo`
- reference_level: **10**
- HP: **135**
- precision: **62**
- damage: **24**
- armor_reduction: **15%**
- flee_agilidad: **12**
- flee_percepcion: **16**

### Acción preparada v1
`dorsalodo_arremetida`
- señal: onda amplia, juncos abiertos, línea dorsal/cuerpo alineándose;
- frontal: **true**
- interruptible: **true**
- precision: **72%**
- damage: **32**

No arrastra al jugador al agua ni cambia de sala en v1.

### Conducta
- si el jugador sale de su zona acuática con una huida válida, no persigue por tierra;
- no aparece en canales urbanos/someros incompatibles.

---

## Rasgacorteza — Nhal

**Identidad:** gran territorial resistente; presión por durabilidad, silencio y control local del espacio.

### Perfil
- id: `rasgacorteza`
- family: `rasgacorteza`
- reference_level: **10**
- HP: **145**
- precision: **60**
- damage: **25**
- armor_reduction: **25%**
- flee_agilidad: **10**
- flee_percepcion: **17**

### Acción preparada v1
`rasgacorteza_arremetida`
- señal: cuerpo separándose del entorno, corteza/hojas cayendo, postura de empuje;
- frontal: **true**
- interruptible: **true**
- precision: **68%**
- damage: **35**

No concede camuflaje mecánico, invisibilidad ni ataque gratis.

### Conducta
- domina zona corta;
- no persecución larga;
- ausencia de fauna/señales previas forma parte del warning, pero nunca sustituye la etapa `warned` del motor C3.

---

# Banda de dificultad

Contra un personaje nivel 1 sano con atributos iniciales y arma inicial:
- las cuatro deben evaluar **Abrumador**;
- ninguna está pensada para progresión inicial obligatoria;
- un jugador puede encontrarlas antes de estar preparado y debe poder retirarse;
- la dificultad real debe provenir de stats + contexto, no de pérdida de arma.

## Comparación buscada

- Cornalomo: amenaza base de referencia.
- Rasgacumbres: menor HP, mayor precisión/movilidad.
- Quebrarrocas: máxima durabilidad/blindaje, precisión menor.
- Dorsalodo: equilibrio ofensivo y presión de borde acuático.
- Rasgacorteza: durabilidad alta + golpe fuerte territorial.

# Playtest común

Por especie:
- 100 simulaciones por clase a nivel 1 para confirmar banda Abrumador;
- 40 simulaciones por clase a nivel de referencia aproximado -2 y nivel de referencia para observar transición de banda;
- huida determinista con varios estados de fatiga;
- prepared_action debe respetar §36;
- muerte conserva equipo;
- 0 aparición en pool C1;
- cooldown C3 después de huida/victoria/muerte;
- señales siempre preceden compromiso.

No rebalancear únicamente para que un nivel 1 pueda ganar.

**Principio:** una amenaza superior debe ser reconocible por cómo obliga a decidir, no solo porque tenga más HP.
