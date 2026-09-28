# Vintage Telnet — Ecología regional para encuentros aleatorios


**Responsable:** Historiador y Constructor del Mundo  
**Alcance de esta entrega:** Hoshai/Khariel, Korven/Brumak, Lethra/Narevia y Nhal/Velmora.  
**Fuente de fauna:** `CREATURES.md`.  
**Fuente mecánica:** `RANDOM_ENCOUNTER_GAMEPLAY.md` y `GAMEPLAY.md`.


Esta entrega completa la parte de Historia que faltaba después del paquete de Edran ya definido en #166.


No fija:
- porcentajes;
- pesos;
- densidad;
- HP;
- daño;
- precisión;
- XP;
- recargas;
- dificultad numérica;
- reglas de respawn.


Eso corresponde a Jugabilidad.


La responsabilidad de Historia aquí es solamente:
- qué contextos exteriores admiten fauna;
- qué criaturas menores pertenecen a cada hábitat;
- qué amenazas superiores quedan fuera de los pools ordinarios;
- restricciones ecológicas para que el motor no coloque fauna de manera incoherente.


---


# Reglas generales para las cuatro regiones


1. **Pueblos y espacios interiores permanecen sin encuentros aleatorios ordinarios.**
   - Khariel centro, Brumak centro, Narevia centro y Velmora centro no deben funcionar como pools de fauna silvestre.
   - Forjas, mercados, interiores, patios centrales y equivalentes tampoco.


2. **La presencia de fauna no equivale a combate obligatorio.**
   - Uñapiedra puede huir.
   - Saltacresta puede advertir y escapar.
   - Cascapedernal puede replegarse.
   - Colagrieta puede evitar espacios abiertos.
   - Pinzajunco puede defender territorio pequeño sin perseguir.
   - Saltalodo puede saltar al agua.
   - Rondamusgo puede inmovilizarse o huir.
   - Hilaria de niebla puede ignorar al viajero mientras su red no sea alterada.


3. **Las amenazas superiores regionales quedan fuera del pool ordinario inicial.**
   - Rasgacumbres.
   - Quebrarrocas.
   - Dorsalodo.
   - Rasgacorteza.
   Su presencia debe ser scripted, señalizada o habilitada por una capa posterior de Jugabilidad.


4. **No mezclar fauna regional por comodidad técnica.**
   - Una criatura puede aparecer en una franja de transición solo si el entorno todavía soporta su ecología.
   - El cambio de región debe sentirse gradualmente, no como una tabla de monstruos intercambiable.


5. **Las rutas próximas al pueblo deben sentirse más habitadas y menos salvajes que los tramos profundos.**
   Historia no fija la densidad, pero sí el principio ecológico.


6. **Los pools deben usar hábitats, no “clase de monstruo”.**
   Una criatura vive donde puede alimentarse, refugiarse y reproducirse; no aparece solo porque su nivel coincida con el jugador.


---


# 1. Sierra de Hoshai — Khariel


## Identidad ecológica


Hoshai se caracteriza por:
- roca expuesta;
- desnivel;
- terrazas;
- salientes;
- viento;
- refugios pequeños;
- zonas de sol y sombra muy marcadas;
- vegetación de montaña dispersa.


La fauna menor no debe sentirse como variante de Edran.


Aquí importan:
- verticalidad;
- agarre;
- salto;
- refugio en grietas;
- lectura del terreno.


## Contextos exteriores aptos para fauna


### Borde de Khariel
Los primeros tramos fuera del pueblo pueden admitir presencia ocasional de fauna, especialmente en:
- terrazas exteriores;
- zonas de roca calentada por el sol;
- matorral de altura;
- pequeños cambios de nivel.


El contexto no debe sentirse como “criaturas dentro del pueblo”.


### Camino Alto — tramos regionales
Los tramos de Camino Alto que todavía están claramente dentro de Hoshai son apropiados para pools regionales.


Debe priorizarse:
- roca;
- ladera;
- salientes;
- pequeños refugios;
- vegetación de altura.


### Contexto técnico existente
`alto_garganta` → hábitat `hoshai_alto`.


Este punto es adecuado para una primera implementación regional porque ya representa un tramo profundo de la sierra.


## Criatura menor común — Uñapiedra


**Elegible en:**
- roca expuesta;
- laderas;
- terrazas naturales;
- entradas de grietas;
- repisas soleadas;
- piedra protegida del viento.


**No elegible en:**
- interiores;
- suelos agrícolas;
- humedales;
- bosque cerrado;
- espacios urbanos;
- rutas completamente abiertas sin roca/refugio.


**Comportamiento ecológico relevante:**
- permanece inmóvil sobre roca calentada;
- huye en ráfagas cortas hacia grietas;
- puede defender un refugio;
- no persigue a larga distancia;
- usa desniveles y salientes mejor que un viajero ordinario.


**Resultado narrativo esperado:**
Muchos encuentros con Uñapiedra pueden terminar en observación o huida de la criatura, no necesariamente combate.


## Criatura menor territorial — Saltacresta


**Elegible en:**
- terrazas naturales con brotes;
- matorral de altura;
- bordes de camino con vegetación;
- zonas cercanas a puntos de agua de montaña;
- espacios con posibilidad real de salto/escape.


**No elegible en:**
- grietas estrechas sin alimento;
- roca completamente desnuda;
- interiores;
- bosque denso;
- humedal.


**Comportamiento ecológico relevante:**
- herbívoro;
- observa desde altura;
- salta entre terrazas;
- alerta a otros;
- patea si queda atrapado;
- no caza al jugador.


**Restricción:**
No presentar grupos de Saltacrestas como una “manada de combate”. Su comportamiento colectivo es principalmente alerta y huida.


## Amenaza superior excluida — Rasgacumbres


**NO entra en el pool ordinario inicial.**


Puede existir en:
- caminos secundarios;
- cornisas;
- zonas altas;
- territorios alejados del tráfico habitual.


**Señales previas obligatorias cuando se use:**
- marcas profundas;
- restos de presas en altura;
- llamadas de alarma de Saltacresta;
- silencio repentino;
- piedras desplazadas desde cornisas.


Historia recomienda que su primera aparición siga siendo señalizada y no aleatoria.


---


# 2. Pedrales de Korven — Brumak


## Identidad ecológica


Korven se caracteriza por:
- piedra fracturada;
- hendiduras;
- cavidades;
- zonas secas;
- superficies cálidas;
- corredores de viento;
- espacios estrechos.


La fauna de Korven debe aprovechar huecos y fisuras.


No debe sentirse como fauna de campo trasladada a roca.


## Contextos exteriores aptos para fauna


### Borde de Brumak
El exterior inmediato puede tener:
- pequeñas criaturas en piedra cálida;
- movimiento entre hendiduras;
- rastros de caparazón o escamas.


No colocar fauna silvestre ordinaria dentro de los espacios compactos habitados del pueblo.


### Camino de Piedra — tramos regionales
Aptos cuando:
- hay roca fracturada;
- hendiduras;
- cavidades;
- depósitos de líquenes;
- restos orgánicos o refugios.


### Contexto técnico existente
`piedra_hendiduras` → hábitat `korven_piedra`.


Es el contexto prioritario para primera implementación.


## Criatura menor común — Cascapedernal


**Elegible en:**
- piedra cálida;
- depósitos de líquenes;
- bordes de hendiduras;
- zonas secas con refugio inmediato.


**No elegible en:**
- barro;
- agua;
- bosque húmedo;
- campo abierto sin roca;
- interiores urbanos.


**Comportamiento ecológico relevante:**
- se agrupa donde hay alimento;
- se introduce en fisuras estrechas;
- se encoge ante amenaza;
- golpea el suelo con el caparazón;
- puede pellizcar si se intenta retirar de su refugio.


**Restricción:**
No convertir su presencia en ataque automático. Un grupo de Cascapedernales puede ser simplemente fauna observable.


## Criatura menor oportunista — Colagrieta


**Elegible en:**
- fisuras;
- grietas;
- rocas con sombra;
- bordes de camino donde pueda retirarse;
- zonas con restos de alimento o pequeñas presas.


**No elegible en:**
- explanadas sin refugio;
- agua profunda;
- campos abiertos;
- interiores habitados.


**Comportamiento ecológico relevante:**
- observa desde una fisura;
- roba comida abandonada;
- sale poco tiempo a terreno expuesto;
- retrocede hacia roca;
- responde a vibraciones fuertes abandonando el lugar.


**Restricción:**
Debe existir una salida/refugio razonable. No usar Colagrieta como depredador que persigue al jugador por grandes distancias.


## Amenaza superior excluida — Quebrarrocas


**NO entra en el pool ordinario inicial.**


Su presencia debe sentirse antes de verse.


**Señales:**
- vibraciones;
- grietas recientes;
- piedras desplazadas;
- Cascapedernales abandonando zonas;
- derrumbes en pequeñas cavidades.


Su función es volver al terreno parte de la advertencia.


---


# 3. Aguas de Lethra — Narevia


## Identidad ecológica


Lethra combina:
- agua poco profunda;
- canales;
- barro;
- raíces;
- islas;
- juncos;
- orillas;
- vegetación acuática.


Los pools deben distinguir:
- borde de agua;
- barro;
- canal;
- pasarela;
- terreno relativamente seco.


No toda sala de Lethra debe implicar fauna acuática.


## Contextos exteriores aptos para fauna


### Borde de Narevia
Fauna menor puede aparecer fuera de las áreas habitadas, especialmente:
- orillas;
- raíces;
- canales laterales;
- barro cercano a vegetación.


No usar pools silvestres en plataformas centrales, mercado o zonas residenciales.


### Camino de los Juncos — tramos regionales
Elegible cuando:
- el camino ya convive con agua;
- hay orillas;
- juncos;
- barro;
- raíces;
- pasarelas cercanas a hábitat natural.


### Contexto técnico existente
`juncos_juncal` → hábitat `lethra_juncos`.


Prioridad para primera implementación de fauna de Lethra.


## Criatura menor común — Pinzajunco


**Elegible en:**
- orillas poco profundas;
- raíces;
- juncos;
- barro;
- agua tranquila de poca profundidad.


**No elegible en:**
- agua profunda sin refugio;
- suelo seco alejado del agua;
- bosque;
- montaña;
- interiores.


**Comportamiento ecológico relevante:**
- defiende pequeños territorios;
- eleva una pinza como advertencia;
- arrastra materia vegetal;
- se mueve lateralmente;
- no persigue lejos de su refugio.


**Restricción:**
Un Pinzajunco territorial puede escalar a combate si el jugador invade, pero no debe aparecer como cazador.


## Criatura menor común/territorial — Saltalodo


**Elegible en:**
- charcas;
- barro;
- hojas flotantes;
- bordes de canal;
- zonas con insectos.


**No elegible en:**
- roca seca;
- bosque sin agua;
- campos;
- interiores.


**Comportamiento ecológico relevante:**
- permanece semisumergido;
- salta al agua al asustarse;
- puede defender una charca;
- se agrupa donde hay alimento;
- es más activo en momentos apropiados del día, sin que Historia fije regla horaria.


**Restricción:**
No hacer que todos los Saltalodos sean agresivos. La territorialidad debe depender del contexto.


## Amenaza superior excluida — Dorsalodo


**NO entra en el pool ordinario inicial.**


**Señales previas:**
- juncos aplastados;
- marcas de arrastre;
- desaparición de fauna menor;
- ondas grandes;
- restos de presas.


Debe utilizarse en canales profundos, orillas tranquilas o ramales peligrosos, nunca como sorpresa trivial en una pasarela central.


---


# 4. Bosque de Nhal — Velmora


## Identidad ecológica


Nhal se caracteriza por:
- poca luz;
- raíces;
- niebla;
- hojas;
- troncos caídos;
- senderos difíciles de leer;
- sonido amortiguado;
- microhábitats ocultos.


La fauna debe apoyarse en:
- camuflaje;
- quietud;
- redes;
- huecos entre raíces;
- señales discretas.


## Contextos exteriores aptos para fauna


### Borde de Velmora
Puede existir fauna en senderos exteriores y raíces alejadas de las zonas habitadas.


No usar encuentros ordinarios en:
- viviendas;
- espacios comunitarios;
- zonas claramente mantenidas por habitantes.


### Camino de la Sombra Verde — tramos regionales
Aptos cuando:
- el dosel ya es denso;
- hay raíces;
- niebla;
- troncos;
- poca luz;
- cobertura.


### Contexto técnico existente
`sombra_niebla_baja` → hábitat `nhal_bosque`.


Es el mejor primer punto para implementación.


## Criatura menor común — Rondamusgo


**Elegible en:**
- raíces huecas;
- hojarasca;
- zonas con hongos;
- claros pequeños;
- bordes de sendero con cobertura.


**No elegible en:**
- terreno sin vegetación;
- roca desnuda;
- agua abierta;
- interiores.


**Comportamiento ecológico relevante:**
- busca alimento lentamente;
- se inmoviliza al oír pasos;
- huye hacia raíces;
- puede morder si se intenta sacar de su refugio;
- transporta semillas sin intención.


**Restricción:**
No convertirlo en perseguidor. Su identidad es evasiva y defensiva.


## Criatura menor territorial — Hilaria de niebla


**Elegible en:**
- redes entre raíces;
- arbustos;
- troncos caídos;
- pasos estrechos;
- zonas donde la niebla marca los filamentos.


**No elegible en:**
- caminos muy abiertos;
- espacios mantenidos/limpios;
- zonas sin puntos de anclaje para red;
- interiores habitados.


**Comportamiento ecológico relevante:**
- permanece inmóvil;
- repara la red;
- retrocede ante vibraciones grandes;
- ataca principalmente si la red es destruida o si algo queda atrapado.


**Restricción:**
No presentar Hilaria como depredador que corre detrás del jugador fuera de su red.


## Amenaza superior excluida — Rasgacorteza


**NO entra en pool ordinario inicial.**


Debe permanecer como amenaza mayor del bosque y usarse con señalización.


Historia recomienda que su presencia altere el entorno antes del encuentro:
- marcas en corteza;
- rutas de fauna menor alteradas;
- silencio;
- restos o señales coherentes con su conducta definida en `CREATURES.md`.


---


# Contrato mínimo para primera implementación de #229


Para poblar el mundo rápidamente sin esperar arte, Historia considera listos estos primeros cuatro contextos:


| Región | Contexto técnico existente | Fauna menor canónica |
| --- | --- | --- |
| Hoshai | `alto_garganta` / `hoshai_alto` | Uñapiedra, Saltacresta |
| Korven | `piedra_hendiduras` / `korven_piedra` | Cascapedernal, Colagrieta |
| Lethra | `juncos_juncal` / `lethra_juncos` | Pinzajunco, Saltalodo |
| Nhal | `sombra_niebla_baja` / `nhal_bosque` | Rondamusgo, Hilaria de niebla |


Esto permite cumplir la intención de #229:
- al menos una familia combatible por región;
- rutas menos vacías;
- fauna regional diferenciada;
- sin depender de arte.


Historia no decide cuál de las dos criaturas entra primero a implementación. Jugabilidad puede priorizar una por región y añadir la segunda después.


---


# Amenazas superiores — exclusión explícita


Fuera de pools ordinarios iniciales:


- **Rasgacumbres** — Hoshai.
- **Quebrarrocas** — Korven.
- **Dorsalodo** — Lethra.
- **Rasgacorteza** — Nhal.
- **Cornalomo** — Edran, ya tratado aparte como amenaza superior opcional.


Regla:


**“Amenaza superior” no significa “jefe”.**


No debe inferirse pérdida de arma, recompensa especial o respawn diferente por esa etiqueta. Ésas son decisiones separadas de Jugabilidad.


---


# Dependencias para Narrativa


Narrativa debe decidir:
- qué encuentros siguen scripted;
- dónde introducir señales antes de fauna territorial;
- qué tramos deben sentirse tranquilos;
- cómo presentar observación/huida sin convertir todo en combate.


Historia recomienda:
- fauna común puede aparecer con poca señal previa;
- fauna territorial debe ofrecer lenguaje corporal o rastro;
- amenaza superior debe ofrecer señales fuertes antes del encuentro.


---


# Dependencias para Jugabilidad


Jugabilidad debe devolver:
- perfil de densidad;
- pesos;
- dificultad;
- números de criatura;
- familia de XP;
- límites de encuentro;
- reglas de fuga;
- tests de pool.


No modificar el canon de conducta para acomodar números.


---


# Estado final de esta entrega


**HISTORIA COMPLETA PARA #166 EN LAS CUATRO REGIONES RESTANTES.**


Con Edran ya entregado anteriormente, las cinco regiones iniciales tienen ahora contrato ecológico suficiente para que Jugabilidad y Desarrollo pueblen rutas sin esperar arte.


**LISTO PARA TRANSFERENCIA.**