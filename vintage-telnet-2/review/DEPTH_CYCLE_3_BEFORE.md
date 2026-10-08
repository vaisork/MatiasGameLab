# Ciclo 3: fauna, peligro y capacidades — antes

Prueba reproducible: `python3 scripts/depth-cycle3-journey.py`. Cuenta y personaje aislados, `TemporaryDirectory`, reloj de mediodía y RNG determinista; ninguna escritura en la base real. 91 movimientos por Edran, Korven, Lethra y Nhal, observación de nueve destinos y regreso efectivo a `valdren_plaza`. Evidencia completa: `review/depth-cycle3-before.json`.

## Lo jugado y lo que funciona

Observé y examiné Espinajo en los surcos, comparé su peligro y luché como Arcano. Impulso Arcano rompe la preparación, aparece en la narración y permite una respuesta ordinaria: primera ronda 8 de daño, en lugar de embestida. Quedé con 44 HP tras resolver el encuentro sin intervenir de nuevo. Luego observé Cornalomo, Mordelinde, Cascapedernal, Pinzajunco, Dorsalodo, Hilaria y Rasgacorteza en sus regiones. Cornalomo, Dorsalodo y Rasgacorteza permiten acercamiento con aviso específico y retirada antes del combate. Regresé con nueve criaturas registradas; fauna observada y humano no equivalen a enemigos obligatorios. El canon PDF exige ecología, rastros y retirada: estas bases sí existen.

## Autocrítica de la experiencia

El trayecto fue largo, pero los tres encuentros superiores producen exactamente el mismo resultado de retirada («La criatura no te persigue»), y evaluar sólo entrega la etiqueta Comparable/Abrumador. No explica comportamiento, respuesta preparada ni razón contextual de la evaluación. Los avisos de acercamiento sí difieren y merecen conservarse. Cuatro amenazas superiores heredan todos los valores y el comportamiento de Cornalomo; el nombre regional y la frase del aviso prometen mayor diferencia que la que el combate cumple. Cascapedernal clona Mordelinde. No hacen falta escalas nuevas: faltan intenciones distintas visibles sobre la escala existente.

El poder Arcano funcionó y se vio. Esta pasada no demuestra comparativamente las cuatro clases: no afirmar que sean iguales; hay efectos, equipo requerido y recargas distintas en mechanics.py. Sí falta que la evaluación anticipada conecte la embestida interrumpible de Espinajo con una decisión de formación. En encuentros sin preparación, el texto del Arcano menciona romper una preparación que podría no existir.

La inspección de arte real confirma escenas ricas y cálidas en Mordelinde y Espinajo; ambos recuerdan demasiado a roedor/erizo real. El PDF pide criaturas originales, así que calidad pictórica no basta para validar anatomía. Vesperi anime actual comunica orejas grandes y aspecto amable; su lectura exacta debe cotejarse con descripción de especie, no con el viejo modelo.

## Causas prioritarias y propuesta mínima

1. Evaluación usa solamente `profile.category`. Añadir a perfiles existentes una intención breve y una oportunidad observable, mostradas por evaluar. Espinajo: embestida frontal interrumpible; Mordelinde: busca salida, evitar arrinconarlo; Cascapedernal: repliega placas antes de saltar. Mantener números y economía.
2. Retirada usa una única frase global. Reutilizar campos de criatura para una retirada local: Dorsalodo recupera paso de agua; Cornalomo vuelve al herbazal; Rasgacorteza afloja el tronco. Sin recompensa ni loot y sin arquitectura nueva.
3. Mensajes de capacidad deben informar resultado real en lugar de explicación condicional genérica. Rejugar Arcano contra Espinajo y Cascapedernal y comparar preparación, HP y narración. No retocar clases sin evidencia.

## Evaluación visual de GLB antiguos

Nueve `v2.glb` cargados y renderizados realmente con ThreeJS/GLTFLoader locales, Chrome headless y servidor de sólo lectura aislado 8107. Capturas inspeccionadas en `review/depth-cycle3-models/`. Todos cargaron; todos reportan cero clips de animación. No se importa motor ni narrativa anterior.

Los cinco personajes comparten ropa azul/morada sencilla, pose inmóvil y pedestal circular. Felaryn distingue cabeza felina y cola; Marevyn piel azul pero silueta humana; Vesperi carece de las orejas amplias del retrato actual y parece humano gris con ojos negros; Dravak es voluminoso pero sin definición anatómica suficiente; Humano es una figura genérica. Ninguno iguala la calidad anime actual. No recomiendo integrarlos ni sustituir retratos.

Espinajo sí tiene silueta de espinas y patas marcadas; Cornalomo comunica masa y cuernos; Mordelinde y Uñapiedra son cuerpos simples, bajos y con escaso detalle. Son bocetos volumétricos reutilizables sólo como referencia de silueta, previa comprobación del canon; no como arte visible terminado. Pedestales incorporados y ausencia de animación impiden tratarlos como criaturas listas para escena. ThreeJS y GLTFLoader funcionan y son recursos técnicos reutilizables si luego se autoriza una necesidad 3D concreta; añadirlos al cliente ahora no resuelve la profundidad jugable.

Límite: capturas con iluminación neutral y un ángulo por modelo, no un análisis de todas las caras ni animación procedural. Estas observaciones evalúan lo renderizado, no archivos por su nombre.
