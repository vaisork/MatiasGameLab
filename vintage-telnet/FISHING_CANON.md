# Vintage Telnet — Pesca v1: fauna y hábitats canónicos

**Origen:** #600 FISHING-01  
**Responsable:** Historiador y Constructor del Mundo  
**Clasificación:** EXPANSIÓN DEL HISTORIADOR  
**Alcance:** cerrar la capa histórica/ecológica necesaria para que Jugabilidad diseñe pesca usando agua y salas que ya existen.

Este documento NO define:
- caña;
- acción;
- duración;
- probabilidad;
- rareza;
- precio;
- cocina;
- crafting;
- stamina;
- XP;
- skill;
- economía.

---

# Principio

Pescar en v1 significa intentar capturar **fauna acuática pequeña ordinaria** de agua dulce.

No convierte automáticamente a:
- Velario;
- Pinzajunco;
- Saltalodo;
- Velacauce;
- Remojunco;
- Tragacauce;
- fauna C0 terrestre/anfibia

en peces pescables.

Las especies de combate o fauna regional con conducta propia no entran en pesca por conveniencia.

---

# Especies pescables v1

## 1. Hebraleta

**fish_id sugerido:** `hebraleta`  
**Región principal:** Aguas de Lethra  
**Tamaño habitual:** 18–28 cm  
**Tipo:** pez de canal lento y vegetación sumergida.

### Aspecto/ecología
- cuerpo alargado y estrecho;
- aleta dorsal baja y continua;
- dos filamentos sensoriales cortos junto a la boca;
- color verde grisáceo / plata apagada;
- se alimenta de larvas, restos vegetales y pequeños organismos entre raíces.

### Hábitat
Compatible con:
- canal lento;
- juncos;
- islas bajas;
- raíces sumergidas;
- agua protegida.

### No es
- Velario juvenil;
- Velacauce juvenil;
- criatura combatible;
- pez mágico.

---

## 2. Raspacanto

**fish_id sugerido:** `raspacanto`  
**Región principal:** Lethra y canales menores hacia Veyra  
**Tamaño habitual:** 22–35 cm  
**Tipo:** pez de fondo firme y piedra húmeda.

### Aspecto/ecología
- cuerpo corto y robusto;
- boca inferior adaptada a raspar superficies;
- pequeñas placas córneas blandas alrededor de vientre y base de aletas;
- color gris claro / oliva apagado / manchas barro;
- consume biofilm, algas blandas y pequeños invertebrados adheridos.

### Hábitat
Compatible con:
- corriente moderada;
- piedra mojada;
- orilla firme;
- canal somero;
- pasos de agua usados por viajeros.

### No es
- Velario;
- Pinzajunco;
- pez de aguas profundas.

---

## 3. Velo de arroyo

**fish_id sugerido:** `velo_arroyo`  
**Regiones:** Edran / transición hacia Veyra  
**Tamaño habitual:** 12–20 cm  
**Tipo:** pez pequeño de arroyos y vados.

### Aspecto/ecología
- cuerpo estrecho;
- aletas pectorales largas pero no alares;
- banda lateral oscura;
- dorso gris pardo;
- forma pequeños grupos sin conducta coordinada compleja.

Se alimenta de:
- insectos caídos;
- larvas;
- semillas pequeñas arrastradas por agua.

### Hábitat
Compatible con:
- arroyo pequeño;
- vado;
- zanja con agua permanente;
- corriente baja a media.

### No es
- fauna de humedal profundo;
- pez de lago;
- criatura de combate.

---

## 4. Fríacola

**fish_id sugerido:** `friacola`  
**Región:** Hoshai  
**Tamaño habitual:** 14–24 cm  
**Tipo:** pez pequeño de corriente fría de montaña.

### Aspecto/ecología
- cuerpo compacto;
- cola ancha;
- aletas cortas;
- color gris azulado mate;
- vientre pálido;
- permanece cerca de remansos pequeños detrás de piedra.

Se alimenta de:
- larvas;
- pequeños insectos;
- materia orgánica arrastrada por corriente.

### Hábitat
Compatible con:
- agua fría;
- corriente estrecha;
- remanso de montaña;
- piedra limpia.

### No es
- Uñapiedra acuática;
- especie mágica;
- pez de nieve/hielo.

---

# Mapping inicial a salas existentes

## Lethra — pesca claramente compatible

| room_id | especies v1 | nota |
|---|---|---|
| `juncos_agua_entre_caminos` | Hebraleta, Raspacanto | agua estructurada y paso terrestre interrumpido |
| `juncos_islas_bajas` | Hebraleta, Raspacanto | islas bajas y agua protegida |
| `juncos_canal_ancho` | Hebraleta, Raspacanto | canal suficientemente legible |
| `juncos_corrientes` | Raspacanto, Velo de arroyo | canales menores hacia Veyra |

## Edran

| room_id | especies v1 | nota |
|---|---|---|
| `valdren_vado_menor` | Velo de arroyo, Raspacanto | arroyo pequeño y paso de piedra |

## Hoshai

| room_id | especies v1 | nota |
|---|---|---|
| `alto_agua_fria` | Fríacola | corriente estrecha de montaña |

---

# Salas explícitamente NO pescables en v1

No basta con que una descripción mencione humedad o agua.

No pescar en:
- `juncos_plataformas` — presencia de agua no implica punto de pesca;
- `juncos_postes` — hito de marcas de nivel;
- `juncos_pasarela_antigua` — foco histórico/estructural;
- `juncos_isla_refugio` — no se declara agua accesible suficiente;
- `juncos_juncal` — juncos altos no equivalen a punto pescable;
- `juncos_paso_raices` — tránsito elevado/raíces;
- `juncos_embarcadero` — embarcadero no habilita pesca automáticamente;
- `juncos_pasarela_larga` — paso de tránsito, no punto v1;
- `juncos_ultimos` — salida del corazón acuático;
- `juncos_suelo_firme` — explícitamente tierra firme;
- cualquier sala de Nhal sin agua abierta claramente definida;
- cualquier sala de Korven;
- cualquier interior/cavidad sin ecosistema acuático canónico.

---

# Relación con fauna acuática ya existente

## Velario
Existe en la columna de agua entre raíces.  
**No es pescable en v1.**

Razón:
- tamaño 45–65 cm;
- conducta especializada;
- identidad regional propia;
- ya es fauna canónica distinta.

Puede verse cerca de zonas de pesca sin ser captura.

## Pinzajunco
No pescable. Es fauna de orilla/caparazón y no pez.

## Saltalodo
No pescable. Es fauna anfibia/de barro.

## Velacauce
No pescable. Tiene contrato de criatura regional/ramal.

## Remojunco
No pescable. Tiene identidad y contrato propio.

## Tragacauce
No pescable. Es fauna mayor de Lethra.

---

# Qué significa una captura en canon

Una captura representa un ejemplar individual de fauna ordinaria.

Historia no declara todavía:
- si se consume;
- si se vende;
- si se conserva como item;
- si tiene calidad;
- si puede soltarse;
- si pesa distinto;
- si cuenta como recurso.

Eso pertenece a Jugabilidad/Economía.

---

# Límites de expansión

V1 NO incluye:
- pesca marina;
- pesca mágica;
- peces legendarios;
- jefes acuáticos;
- tesoros por pescar;
- botas/armas/objetos basura como tabla de pesca;
- cebos especiales;
- domesticación;
- acuarios;
- cocina;
- profesión de pescador.

Todo eso requiere contrato posterior.

---

# Handoff

## Jugabilidad
Puede cerrar ahora:
- acción de pescar;
- requisito de herramienta o no;
- duración;
- éxito/fallo;
- repetición;
- antifarmeo;
- persistencia/captura;
- relación con inventario;
- valor si aplica.

## Narrativa
Puede escribir:
- lectura del agua;
- espera;
- tirón;
- fallo;
- captura;
- presencia no capturable de Velario u otra fauna.

## Desarrollo
Debe usar solo los room_id declarados como pescables hasta nueva expansión.

---

# Estado

**HISTORIA #600: COMPLETA PARA PESCA V1.**

Huecos cerrados:
1. especies pescables;
2. hábitats y room_id;
3. exclusiones y relación con fauna acuática existente.
