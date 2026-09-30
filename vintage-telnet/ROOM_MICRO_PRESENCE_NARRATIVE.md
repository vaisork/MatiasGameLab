# WORLD-LIVENESS — micro-presencia en hubs existentes

Origen: cola de Narrativa #284 / ola #558.

Objetivo: enriquecer `mirar`/`examinar` en lugares ya existentes que hoy pueden sentirse vacíos. No crea salas, NPCs persistentes, tiendas nuevas, quests ni acciones.

Cada línea es una micro-presencia opcional. Puede mostrarse junto a la descripción base cuando no haya combate ni escena scripted que requiera aislamiento.

## Valdren

- `valdren_centro`: “Alguien cruza la plaza con una cesta, otro se detiene a intercambiar unas palabras y el paso vuelve a quedar libre.”
- `valdren_forja`: “Entre golpes de herramienta y piezas apoyadas contra la pared, el trabajo sigue aunque nadie te esté atendiendo directamente.”
- `valdren_mercado`: “Hay voces cortas, manos que pasan alimentos y gente que entra y sale sin quedarse demasiado.”

## Khariel

- `khariel_centro`: “En distintos niveles se ven figuras que se detienen, miran hacia otra terraza y continúan por su propio paso.”
- `khariel_forja`: “El sonido del trabajo llega por intervalos, separado por pausas en las que alguien comprueba un ajuste antes de seguir.”
- `khariel_mercado`: “Pequeños intercambios ocurren entre terrazas próximas; nada obliga a concentrar toda la actividad en un solo punto plano.”

## Brumak

- `brumak_centro`: “Personas pequeñas atraviesan pasos estrechos y desaparecen entre huecos que desde aquí apenas parecen suficientes.”
- `brumak_forja`: “Herramientas, piezas y superficies de trabajo ocupan casi todo el espacio útil sin volverlo caótico.”
- `brumak_mercado`: “Los intercambios son rápidos y compactos; la gente deja libre el paso apenas termina.”

## Narevia

- `narevia_centro`: “Una figura cruza una plataforma mientras otra revisa un amarre junto al agua. El pueblo se mueve tanto por sus pasos como por sus bordes.”
- `narevia_forja`: “El trabajo se organiza para mantener piezas y herramientas lejos del agua abierta sin separarse del resto del asentamiento.”
- `narevia_mercado`: “Alimentos, fibras y pequeños bienes pasan de mano en mano cerca de plataformas donde el agua nunca queda del todo fuera de la escena.”

## Velmora

- `velmora_centro`: “No hay una multitud visible de golpe; pequeñas presencias aparecen al acercarse a cruces, refugios y señales del sendero.”
- `velmora_forja`: “El trabajo se concentra en un espacio protegido, con herramientas recogidas y poco ruido innecesario.”
- `velmora_mercado`: “La actividad existe sin convertirse en bullicio: conversaciones bajas, pasos próximos y objetos que cambian de manos.”

## Vaisgard

- `vaisgard`: “Viajeros, habitantes y cargas de procedencias distintas se cruzan durante unos instantes antes de separarse hacia otros sectores de la ciudad.”

## Reglas

- no nombrar personas salvo que exista NPC scripted;
- no implicar una misión oculta;
- no crear venta/compra nueva por el hecho de describir un mercado;
- no prometer interacción con cada figura;
- scripted NPC tiene prioridad sobre esta capa;
- combate o escena de aislamiento puede ocultarla;
- daypart/clima pueden sustituir o matizar una línea, no acumular tres párrafos.

## Handoff

LISTO PARA INTEGRACIÓN: SÍ.

Este archivo puede alimentar `mirar` o una línea secundaria de `room_view` para centros/forjas/mercados existentes.