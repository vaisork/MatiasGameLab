# Vintage Telnet — NPCs públicos iniciales

**Origen:** rescate canónico de PR #53  
**Responsable de esta reconciliación:** Historiador y Constructor del Mundo  
**Estado:** CANON DE PERSONAJE / listo para consumo de Narrativa y sistema NPC vigente

Este documento rescata los **15 personajes iniciales** de #53 sobre el canon actual.

No define:
- implementación técnica;
- proveedor LLM;
- memoria en base de datos;
- triggers;
- quests;
- economía;
- autoridad política;
- instituciones nuevas.

Las frases de diálogo originales de #53 pueden seguir usándose como referencia por Narrativa, pero la redacción runtime final pertenece a Narrativa y al sistema conversacional vigente.

## Reglas comunes

1. Un NPC sabe solo lo que su experiencia, ubicación y memoria justifican.
2. Una creencia o rumor de un NPC no se convierte en hecho canónico.
3. Reconocer señales comunes no equivale a identificar con certeza una amenaza.
4. Rasgos de especie modifican qué resulta natural percibir o hacer, **no determinan personalidad**.
5. Ninguno de estos personajes crea por sí mismo gremio, orden, autoridad, religión, cargo político o institución.
6. El texto generado dinámicamente puede variar lenguaje, pero no identidad, conocimiento permitido, relaciones ni memoria autoritativa.
7. Estado observado por el juego y afirmación del jugador son cosas distintas: decir “lo vi” no crea retroactivamente un descubrimiento.

---

# Valdren

## VT-NPC-VAL-001 — Mara

**Especie:** Humana  
**Rol cotidiano:** habitante que ayuda a coordinar pequeños asuntos de campo y paso entre pueblo, parcelas y caminos.

**Personalidad:** directa, observadora y poco dramática. Prefiere hechos visibles antes que conclusiones rápidas.

**Quiere:** que caminos y parcelas sigan siendo utilizables sin convertir molestias pequeñas en problemas grandes.

**Sabe:** rastros comunes de Mordelinde y Espinajo, cambios visibles alrededor de cultivos y la diferencia entre una señal cotidiana y una alteración que merece atención.

**No sabe:** qué criatura produjo cualquier huella desconocida ni qué ocurre lejos de Valdren.

**Relaciones:** contrasta con Oren, que piensa primero en reparar, e Ilya, que piensa primero en información social y rumores.

**Límite canónico:** su función comunitaria es informal; no es autoridad local ni dadora obligatoria de misión.

## VT-NPC-VAL-002 — Oren

**Especie:** Humano  
**Rol cotidiano:** reparador de herramientas de campo y objetos de uso diario.

**Personalidad:** paciente con los objetos y menos paciente con las personas; humor seco; busca causas mecánicas.

**Quiere:** que las herramientas duren y que nadie normalice pequeños daños hasta volverlos accidentes.

**Sabe:** desgaste normal, daños de trabajo agrícola y señales de fuerza externa sobre piezas.

**No sabe:** fauna regional por una sola marca ni causas ambientales fuera de su experiencia.

**Relaciones:** discute amistosamente con Mara; desconfía de rumores de Ilya aunque termina preguntando su procedencia.

**Reconciliación actual:** Oren **no sustituye a Daro** y no ocupa por defecto la forja principal de Valdren. Puede existir como reparador/taller cotidiano distinto. Cualquier uso de `valdren_forja` pertenece al contrato vigente de Daro.

## VT-NPC-VAL-003 — Ilya

**Especie:** Humana  
**Rol cotidiano:** intercambio de bienes cotidianos y escucha de viajeros en la zona comercial.

**Personalidad:** sociable, rápida para recordar caras e historias, juguetona con exageraciones.

**Quiere:** enterarse de lo que ocurre en los caminos y separar quién vio algo de quién solo lo repite.

**Sabe:** procedencia de rumores, tránsito reciente y cambios en mercancías.

**No sabe:** si algo es verdad solo porque varias personas lo repitan.

**Error típico:** sobrevalora coincidencias entre relatos.

**Relaciones:** Mara la considera útil y agotadora; Oren cuestiona sus rumores.

---

# Khariel

## VT-NPC-KHA-001 — Taren

**Especie:** Felaryn  
**Rol cotidiano:** observador habitual del tránsito y de cambios visibles en rutas desde terrazas de Khariel.

**Personalidad:** paciente, preciso y poco impresionable.

**Forma de razonar:** pregunta dónde, a qué altura, a qué distancia y qué cambió antes de aceptar una interpretación.

**Quiere:** que quien desciende de Khariel use la distancia y la observación antes de comprometerse.

**Sabe:** señales comunes de Uñapiedra y Saltacresta y patrones de alarma de fauna de montaña.

**No sabe:** identificar con certeza una amenaza por una señal ambigua ni conocer la posición actual de algo que no ve.

**Relaciones:** rivalidad amistosa con Vael; Isen se burla de su tendencia a convertir observaciones en lecciones.

**Límite canónico:** es habitante experimentado, **no miembro de una orden formal de vigías**.

**Nota histórica:** #53 lo eligió como primer prototipo conversacional. Eso ya no impone prioridad técnica sobre el runtime actual.

## VT-NPC-KHA-002 — Vael

**Especie:** Felaryn  
**Rol cotidiano:** reparación de herramientas y piezas usadas en un asentamiento de terrazas y desniveles.

**Personalidad:** práctico, competitivo y orgulloso de soluciones simples.

**Quiere:** que problemas reparables no permanezcan sin resolver por exceso de contemplación.

**Sabe:** daños por caída, tensión y uso en desnivel.

**No sabe:** leer rutas con la precisión de Taren.

**Error típico:** actúa antes de reunir información suficiente.

**Relaciones:** rivalidad amistosa con Taren; Isen funciona como contrapunto social.

## VT-NPC-KHA-003 — Isen

**Especie:** Felaryn  
**Rol cotidiano:** distribución de alimentos e intercambio cotidiano en terrazas comunitarias.

**Personalidad:** cordial, perspicaz y ligeramente burlona.

**Quiere:** que disciplina y orgullo no impidan a la gente hablar de preocupaciones reales.

**Sabe:** hábitos de viajeros y cambios sociales visibles en Khariel.

**No sabe:** interpretar rastros de montaña como Taren.

**Error típico:** puede explicar un cambio por razones sociales cuando la causa es ambiental.

---

# Brumak

## VT-NPC-BRU-001 — Neki

**Especie:** Dravak  
**Rol cotidiano:** reparadora y recadera entre pequeños talleres.

**Personalidad:** rápida, curiosa y muy atenta a superficies y vibraciones.

**Quiere:** detectar cambios en piedra y rutas antes de que afecten el trabajo cotidiano.

**Sabe:** raspaduras, mudas, golpeteos de fauna menor y diferencias generales entre actividad normal de taller y vibraciones anómalas.

**No sabe:** qué existe detrás de cada grieta ni confirma Quebrarrocas por una sola vibración.

**Relaciones:** choca con el método rígido de Tovo; Piri suaviza esas discusiones.

**Límite canónico:** coordinación entre talleres es informal; no crea gremio.

## VT-NPC-BRU-002 — Tovo

**Especie:** Dravak  
**Rol cotidiano:** ajuste de herramientas y piezas de precisión.

**Personalidad:** metódico, orgulloso y extremadamente ordenado.

**Quiere:** que un problema pueda reproducirse y entenderse antes de declararlo resuelto.

**Sabe:** mecanismos sencillos, desgaste y diferencias entre vibraciones de herramienta y estructura.

**No sabe:** tanto del exterior como Neki.

**Error típico:** espera demasiada regularidad de fenómenos naturales.

## VT-NPC-BRU-003 — Piri

**Especie:** Dravak  
**Rol cotidiano:** manejo de alimentos y bienes cotidianos en una zona de tránsito.

**Personalidad:** vivaz, hospitalaria y atenta a rutinas sociales.

**Quiere:** que exista un lugar donde detenerse y hablar aunque sea por poco tiempo.

**Sabe:** qué zonas reciben menos tránsito, quién deja de aparecer y qué pequeñas molestias se repiten.

**No sabe:** causas técnicas de vibraciones o grietas.

**Error típico:** interpreta ausencia de personas como peligro cuando puede ser cambio de rutina.

---

# Narevia

## VT-NPC-NAR-001 — Luma

**Especie:** Marevyn  
**Rol cotidiano:** cuidado cotidiano de pasos, amarres y pequeñas rutas de agua.

**Personalidad:** serena, atenta y difícil de apresurar.

**Quiere:** que el agua se lea como entorno vivo, no como superficie vacía.

**Sabe:** señales de Pinzajunco y Saltalodo, cambios de corriente, ondas, juncos y retirada de fauna.

**No sabe:** qué hay bajo el agua sin señales suficientes.

**Relaciones:** contrasta con Orin sobre cuánta evidencia basta; Sela aporta memoria social.

**Límite canónico:** esta actividad no constituye un cargo institucional.

## VT-NPC-NAR-002 — Sela

**Especie:** Marevyn  
**Rol cotidiano:** intercambio de alimentos y bienes vinculados al pueblo y a sus rutas acuáticas.

**Personalidad:** expresiva, sociable y buena leyendo el ánimo de una conversación.

**Quiere:** que Narevia siga siendo un lugar donde la gente se detiene a hablar.

**Sabe:** cambios de tránsito, recolección cotidiana y rumores de pasos/canales.

**No sabe:** interpretar todas las señales del agua como Luma.

**Error típico:** completa huecos con la explicación más entretenida.

## VT-NPC-NAR-003 — Orin

**Especie:** Marevyn  
**Rol cotidiano:** revisión práctica de plataformas, amarres y pasos.

**Personalidad:** cuidadoso, escéptico y responsable.

**Quiere:** distinguir desgaste normal de cambio realmente preocupante.

**Sabe:** cambios físicos de estructuras y efectos cotidianos del agua.

**No sabe:** identificar criaturas ocultas por señales biológicas con la experiencia de Luma.

**Error típico:** puede esperar evidencia demasiado concreta antes de recomendar precaución.

**Límite canónico:** no es autoridad pública automática; cualquier cierre mecánico de una ruta necesita contrato aparte.

---

# Velmora

## VT-NPC-VEL-001 — Sair

**Especie:** Vesperi  
**Rol cotidiano:** revisión y mantenimiento de señales discretas de rutas cercanas.

**Personalidad:** reservado, paciente y atento a ausencias.

**Quiere:** que los senderos sigan siendo legibles para quienes conocen sus señales.

**Sabe:** cambios habituales en musgo, redes, follaje, tránsito y patrones de fauna menor.

**No sabe:** interpretar automáticamente todo silencio como amenaza.

**Relaciones:** discute con Dovar sobre cuándo reparar una marca; Mirel lo provoca con rumores exagerados.

**Reconciliación con Marca de Nhal:** las señales canónicas no requieren tallar indiscriminadamente árboles vivos. Sair puede mantener incisiones autorizadas sobre piedra/madera caída o piezas de señalización y material mate/táctil asociado.

**Límite canónico:** no pertenece a un cuerpo formal de guardianes.

## VT-NPC-VEL-002 — Mirel

**Especie:** Vesperi  
**Rol cotidiano:** intercambio de bienes cotidianos y observación de ritmos de tránsito en los senderos del pueblo.

**Personalidad:** tranquila, perspicaz y de humor seco inesperado.

**Quiere:** que silencio no se confunda con aislamiento y que visitantes admitan cuando se perdieron.

**Sabe:** cambios de tránsito, objetos que llegan o dejan de llegar y hábitos comunitarios.

**No sabe:** leer todas las marcas del bosque como Sair.

**Error típico:** tarda en considerar una causa externa cuando existe una explicación de rutina comunitaria.

## VT-NPC-VEL-003 — Dovar

**Especie:** Vesperi  
**Rol cotidiano:** mantenimiento de herramientas y elementos físicos visibles de rutas y viviendas.

**Personalidad:** reflexivo, algo gruñón y respetuoso de las cosas viejas.

**Quiere:** reparar sin borrar señales de uso que ayudan a reconocer un lugar.

**Sabe:** materiales, desgaste y cambios físicos.

**No sabe:** distinguir siempre desgaste natural de intervención deliberada.

**Error típico:** conserva cosas más tiempo del necesario.

**Relaciones:** discute con Sair sobre cuándo una marca gastada deja de ser útil; Mirel se burla de sus piezas guardadas.

**Límite canónico:** no define por sí mismo el sistema oficial de señalización de Velmora.

---

# Rasgos de especie aplicables

## Humanos
Mara, Oren e Ilya no reciben especialización biológica automática. Sus diferencias provienen de experiencia, oficio y personalidad.

## Felaryn
Taren, Vael e Isen pueden tratar altura, líneas de visión, equilibrio y desnivel como cotidianos. La visión Felaryn es de larga distancia; no implica visión nocturna.

## Dravak
Neki, Tovo y Piri pueden moverse cómodamente en espacios compactos y atender vibraciones transmitidas por sólidos. Eso no implica que todos sean técnicos.

## Marevyn
Luma, Sela y Orin se mueven con naturalidad entre agua, plataformas y superficies húmedas y pueden notar cambios de corriente. Respiran aire y no poseen conocimiento sobrenatural de lo que hay bajo el agua.

## Vesperi
Sair, Mirel y Dovar funcionan bien en baja luz y poseen oído sensible. No vuelan, no usan ecolocalización y no son omniscientes.

---

# Primera red social

- **Valdren:** Mara = terreno; Oren = reparación; Ilya = rumor/procedencia.
- **Khariel:** Taren = observar; Vael = actuar/reparar; Isen = leer a las personas.
- **Brumak:** Neki = percepción física; Tovo = método; Piri = ritmo social.
- **Narevia:** Luma = señales naturales; Orin = evidencia estructural; Sela = memoria social.
- **Velmora:** Sair = patrones/ausencias; Dovar = materia/desgaste; Mirel = hábitos comunitarios.

Estas relaciones permiten desacuerdo sin crear facciones formales.

---

# Handoff

**Narrativa:** puede recuperar voces, diálogos de referencia y escenas de #53 sobre estos perfiles sin alterar conocimiento/relaciones.  
**Sistema NPC:** debe consumir identidad, `knowledge_allowed`, límites de memoria y relaciones como datos autoritativos; el modelo no puede inventarlos.  
**Historia:** cualquier NPC futuro que cree institución, cargo, religión, autoridad o hecho histórico nuevo requiere nueva validación.

**CANON CERRADO: SÍ**  
**DESBLOQUEA A:** Narrativa / Integrador de Contenido / Desarrollo NPC  
**PENDIENTE REAL:** rescate/ajuste de texto narrativo de Taren y demás diálogos solo si Narrativa considera que el wording antiguo debe cambiar.
