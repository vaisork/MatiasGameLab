# Genera TEXTOS.md y propuestas.json a partir de las propuestas de abajo.
# Lee content/ sólo para citar el texto actual; no modifica nada fuera de esta carpeta.
# Uso: python3 docs/colaboracion/claude-narrativa/generar.py  (desde la raíz del proyecto)
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))

def load(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return json.load(f)

def resolve(archivo, tabla, id_, campo):
    """Devuelve el texto actual del campo o None si no existe."""
    node = load(archivo)[tabla][id_]
    for token in campo.split('.'):
        m = re.fullmatch(r'([^\[]+)(?:\[(.+)\])?', token)
        name, sel = m.group(1), m.group(2)
        if not isinstance(node, dict) or name not in node:
            return None
        node = node[name]
        if sel is None:
            continue
        if sel.isdigit():
            node = node[int(sel)] if int(sel) < len(node) else None
        else:
            k, v = sel.split('=', 1)
            node = next((x for x in node if x.get(k) == v), None)
        if node is None:
            return None
    return node if isinstance(node, str) else json.dumps(node, ensure_ascii=False)

W = 'content/world.json'
ED, HO, KO, LE, NH, VE = (f'content/regions/{r}.json' for r in ('edran', 'hoshai', 'korven', 'lethra', 'nhal', 'veyra'))

# Condiciones reutilizadas
C_ACC = 'Al pulsar «Aceptar» en la sala de aceptación con el NPC presente. Sustituye a accept_text en ese momento; el motor añade después la línea del pago de referencia.'
C_TXT = 'Siempre en el diario/encargos (resumen mientras está aceptado) y como narración de aceptación si el NPC no está presente.'
C_READY = 'Una vez, en el lugar donde se cumple la última condición; después es el resumen del encargo en estado «listo».'
C_DEL = 'Al pulsar «Entregar». Narración del mundo; el motor la muestra aunque el NPC no esté presente.'
C_PAY = 'Al pulsar «Entregar», sólo si el NPC está presente; va antes de la línea de sellos.'

E = []  # propuestas
def p(grupo, archivo, tabla, id_, campo, condiciones, texto, por_que, requiere_codigo=False, defecto=None):
    E.append(dict(grupo=grupo, archivo=archivo, tabla=tabla, id=id_, campo=campo, condiciones=condiciones,
                  texto=texto, requiere_codigo=requiere_codigo, por_que=por_que, defecto=defecto))

DEF_ACC = '(no existe: se muestra accept_text como narración)'
DEF_READY = '(no existe: «El encargo ya puede entregarse.»)'
DEF_DEL = '(no existe: sólo «Entregas el encargo… te paga N sellos.»)'
DEF_PAY = '(no existe)'

# ───────────────────────── A1 · Valdren · Daro ─────────────────────────
g = 'A1 · valdren_recado_forja · Daro (Valdren)'
q = 'valdren_recado_forja'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'Bren, el de los carros, tiene una rueda que cruje cuando el carro avanza. Tengo que hacerle una abrazadera, pero si no sé de qué lado cede la rueda, la haré a ciegas. Baja a la plaza y entra en el cobertizo de los carros, al oeste. Pregúntale a Bren por la rueda y tráeme lo que te diga: de qué lado se sale la cuña y cuánto. No tienes que arreglar nada; con la medida me basta.',
  'Quién (Bren), qué (lado y cuánto se sale la cuña), por qué (no fabricar a ciegas), dónde (plaza → oeste) y cuándo está hecho (traer la medida). Sin cifras de pago: el motor ya añade la línea de sellos y el pago baja si se repite.',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Daro, el herrero, necesita saber de qué lado cede la rueda del carro de Bren para ajustar una abrazadera. Baja por la calle hasta la plaza y entra en el cobertizo de los carros, al oeste. Pregunta a Bren por la rueda y vuelve a la fragua con su respuesta. No hace falta reparar nada.',
  'Resumen en voz de narrador; se entiende sin la voz de Daro. El original hablaba de «medida» sin que Bren diera ninguna; ahora el tema de Bren la contiene (ver abajo).')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'Ya sabes de qué lado se sale la cuña y cuánto. Vuelve a la fragua de Daro, al norte de la plaza, para darle la medida.',
  'Se dispara en el cobertizo al hablar con Bren: dice a quién volver y dónde está.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Repites lo que dijo Bren: un dedo, en la rueda izquierda. Daro lo escribe con tiza junto a la abrazadera.',
  'Consecuencia visible que ya existe en los estados de la fragua (marca de tiza tras encargo_pagado).', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Un dedo, lado izquierdo. Con eso ajusto la pieza a esa rueda y no gasto hierro de más. Bren tendrá su abrazadera antes de volver a cargar.',
  'Cierra el motivo de Daro («sin añadir hierro por añadirlo»). Repetible: el texto sigue siendo cierto en otra entrega.', defecto=DEF_PAY)
p(g, ED, 'npcs', 'edran_bren', 'topics.rueda', 'Hablar con Bren · rueda, antes de que nadie haya fijado la cuña (sin edran_rueda_comprobada). Es la acción requerida del encargo.',
  'Cruje cuando el carro avanza, no cuando para. Es la rueda izquierda: la cuña se sale como un dedo por fuera del aro. Si te manda Daro, dile eso: un dedo, lado izquierdo. Si quieres verlo, quédate fuera de la cuerda; yo muevo el carro despacio.',
  'Sin esto el encargo «llevar la medida» se completaba sin que nadie diera una medida. «Un dedo» y «izquierda» son detalle físico nuevo, coherente con el examen («la cuña… ha empezado a salir por un extremo»).')
p(g, ED, 'npcs', 'edran_bren', 'states[0].overrides.topics.rueda', 'Hablar con Bren · rueda, después de que alguien fijó la cuña (edran_rueda_comprobada, mundo).',
  'Ya no cruje: la cuña está sujeta. Para Daro, la medida sigue siendo la misma: se salía un dedo por el lado izquierdo. Con eso puede ajustar la abrazadera. La próxima prueba la haré con el carro cargado.',
  'El encargo se puede aceptar después de que otro jugador arregló la cuña; Bren debe seguir dando la medida.')
p(g, ED, 'rooms', 'valdren_cobertizo', 'examine.rueda', 'Examinar rueda en el cobertizo (antes de fijar la cuña).',
  'La cuña de la rueda izquierda ha empezado a salirse por un extremo, como un dedo. Se nota mejor mientras el carro avanza despacio.',
  'Alinea el examen con lo que Bren dice.')

# ───────────────────────── A2 · Valdren · Elva ─────────────────────────
g = 'A2 · valdren_revision_cobertizos · Elva (Valdren)'
q = 'valdren_revision_cobertizos'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'La última carreta del día trae la harina para el pan de mañana, y a veces llega cuando ya es de noche. Si la descargan en un sitio mojado, la harina se echa a perder. Necesito saber dos cosas: si la puerta baja del paso entre los graneros está seca, y si en el cobertizo de las estacas, pasado el lindero, queda un hueco bajo techo. Mira la esquina del granero y las estacas del cobertizo, y vuelve a contármelo.',
  'El original pedía «comprobar lugar para una carga tardía» pero los exámenes requeridos (esquina, estacas) no decían nada de espacio. Ahora hay un motivo de niño (pan de mañana) y los exámenes responden a la pregunta.',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Elva, la del comedor, espera harina en la última carreta del día. Comprueba dos sitios donde podría descargarse sin mojarse: la esquina junto a la puerta baja, en el paso entre los graneros, y las estacas del cobertizo de campo, pasado el lindero. Examina ambos y vuelve al comedor.',
  'Resumen y alternativa sin voz.')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'Has visto los dos sitios. Vuelve al comedor de Elva, junto al pozo, para decirle dónde puede esperar la harina.',
  'Dirección real: el comedor sale al norte hacia el pozo.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Le cuentas a Elva lo que viste en la esquina del granero y en el cobertizo de las estacas. Ella lo apunta en la lista de cargas, junto a las ollas.',
  'Coincide con el estado posterior del comedor («guarda tus noticias… junto a la lista de cargas»).', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Entonces ya sé dónde mandar la carreta si llega tarde. Mañana habrá pan para todos, también para quien todavía no ha vuelto.',
  'Vale tanto si la esquina estaba despejada como si no: Elva sabe cuál de los dos sitios usar.', defecto=DEF_PAY)
p(g, ED, 'rooms', 'valdren_graneros', 'examine.esquina', 'Examinar esquina mientras la salida sigue tapada (sin edran_granero_despejado). Acción requerida.',
  'La tierra del terraplén tapa la salida del agua. Cuando llueve, el charco llega hasta la puerta baja: ahí no conviene dejar sacos hasta despejarla.',
  'Da la respuesta que Elva necesita y apunta a la acción ya existente de despejar.')
p(g, ED, 'rooms', 'valdren_graneros', 'states[0].overrides.examine.esquina', 'Examinar esquina después de despejarla (edran_granero_despejado, mundo).',
  'La salida queda abierta y la tierra retirada está arriba de la pendiente. La puerta baja se mantiene seca: ya se pueden dejar sacos.',
  'Misma pregunta, respuesta contraria: la consecuencia de despejar se nota en el encargo.')
p(g, ED, 'rooms', 'edran_cobertizo_campo', 'examine.estacas', 'Examinar estacas. Acción requerida.',
  'Las estacas cuelgan ordenadas por tamaño; los números indican medidas, no dueños. Debajo del banco queda un hueco seco y techado, con sitio para unos pocos sacos.',
  'Conserva el dato original (números = tamaños) y añade el hueco que Elva pregunta. Detalle físico nuevo, sin mecánica.')

# ───────────────────────── A3 · Valdren · Bren ─────────────────────────
g = 'A3 · valdren_estado_vado · Bren (Valdren)'
q = 'valdren_estado_vado'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'Mis carros cargados salen hacia Lethra y hacia Veyra, y los dos caminos cruzan agua. Antes de cargar quiero saber si los pasos aguantan. Uno es el Vado de Juncos: sal del pueblo por el este, sigue la acequia y baja por los sauces hasta el puente; mira sus apoyos desde la orilla. El otro está en el Paso hacia Veyra, al final de la calzada, al norte: mira la losa junto al poste. No te metas en el agua ni te acerques a ningún animal. Sólo mira y vuelve a contármelo.',
  'Indicaciones comprobadas con las salidas reales (plaza → este … estanque → sur → sauces → sur → vado → este; vado → oeste … calzada → norte → hito).',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Bren quiere saber si sus carros cargados pueden cruzar dos pasos de agua. Examina los apoyos del puente en el Vado de Juncos (al este, pasados la acequia y los sauces) y la losa del Paso hacia Veyra (al norte, al final de la calzada). No hace falta entrar en el agua ni enfrentarse a ninguna criatura. Después vuelve al cobertizo de los carros.',
  'Resumen.')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'Ya has visto el puente y la losa. Vuelve al cobertizo de Bren, en Valdren, para contarle si sus carros pueden cruzar.',
  'Se dispara lejos del pueblo: nombra el pueblo.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Le explicas a Bren cómo están los apoyos del puente y la losa del poste. Él lo apunta en una tablilla y la cuelga fuera de la cuerda de giro, donde la vean los conductores.',
  'Coincide con el estado posterior del cobertizo (tablilla fuera de la cuerda).', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Bien. Con esto sé por dónde puede ir cada carro sin descargar a medio camino. Se lo diré a cada conductor antes de cargar.',
  'Evita repetir la frase de su memoria posterior («saldrán con el próximo carro»).', defecto=DEF_PAY)
p(g, ED, 'rooms', 'edran_puente_juncos', 'examine.apoyos', 'Examinar apoyos en el Vado de Juncos. Acción requerida.',
  'Los apoyos del puente están firmes. El agua empuja unos juncos contra uno de ellos, pero la madera no se mueve. Un carro cargado puede pasar si cruza despacio.',
  'El original sólo decía que los apoyos «pueden revisarse»; el jugador no tenía noticia que llevar.')
p(g, ED, 'rooms', 'edran_hito_campos', 'examine.losa', 'Examinar losa en el Paso hacia Veyra. Acción requerida.',
  'La losa tiene parches de piedras distintas. Una piedra clara, más nueva, sujeta el borde gastado: la losa ya no se mueve al pisarla.',
  'Conserva el detalle original (piedra clara bajo el borde) y lo convierte en noticia.')

# ───────────────────────── A4 · Khariel · Daren ─────────────────────────
g = 'A4 · khariel_polea · Daren y Seran (Hoshai)'
q = 'khariel_polea'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'Me falta una polea del taller, la que usamos para subir cargas cortas por los peldaños. Ha aparecido en un campamento con una lona azul. Desde la plaza, baja dos tramos de escalones hasta la terraza de las cargas y toma el desvío del oeste. Allí acampa un viajero, Seran. Dice que la polea es suya hasta que alguien le pague un transporte. Habla con él antes de tocar nada: quiero la polea, pero también quiero saber qué cuenta reclama. Si vuelves con las dos cosas, habrás hecho el trabajo.',
  'Sustituye «Hablar con Seran permite resolverlo sin combatir» (voz de diseño) por un motivo: Daren quiere la pieza y la verdad de la cuenta.',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Daren, el maestro de reparaciones, necesita recuperar la polea de su taller. Está en el campamento de la lona azul: desde la plaza, baja dos tramos hasta la terraza de las cargas y toma el desvío del oeste. Un viajero llamado Seran la retiene y reclama un pago pendiente. Habla con él, recoge la polea en las cajas del sendero sur y devuélvela al taller junto con lo que Seran reclama.',
  'Resumen con el orden real: hablar (cuenta → acuerdo), recoger en Cajas bajo la terraza, entregar en el taller.')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'La polea ha vuelto al banco de Daren y la cuenta de Seran queda apuntada a su lado. Puedes cerrar el encargo con Daren aquí mismo.',
  'Se cumple dentro del taller (acción hoshai_entregar_polea), por eso «aquí mismo».', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'La polea vuelve a su gancho, encima del banco bajo. Ya pueden subir otra vez cargas cortas por los peldaños sin llevarlas a mano.',
  'No repite la acción de devolver (que ya narra la marca y la tablilla); cuenta para qué sirve haberla recuperado.', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Gracias. La polea es del taller y vuelve a trabajar. Lo de Seran lo miraré con calma: si le debemos un transporte, se lo pagaremos.',
  'Sirve para el camino pacífico y para el de pelea; en el segundo, la memoria hoshai_polea_por_fuerza añade el reproche de Daren.', defecto=DEF_PAY)
p(g, HO, 'npcs', 'hoshai_seran', 'topics.cuenta.text', 'Hablar con Seran · cuenta (fija hoshai_seran_escuchado).',
  'Subí estas cajas hasta aquí porque me dijeron que el taller pagaría al llegar. Nadie me ha pagado. Por eso me quedé la polea: no la quiero, quiero mi pago. Si se la llevas a Daren, dile también quién la trajo y qué se me debe.',
  'Quita las comillas «» dentro de la voz (se leían «Seran: «…»») y explica el motivo: no es un ladrón, es un transportista sin cobrar.')
p(g, HO, 'npcs', 'hoshai_seran', 'topics.acuerdo.text', 'Hablar con Seran · acuerdo (tras cuenta, sin haber peleado). Fija hoshai_polea_acordada.',
  'Está bien. La polea está en las cajas del sendero sur; llévatela. Y llévate esta tablilla: ahí está escrita mi cuenta. Que Daren la lea. No te pido sellos a ti; te pido que no se pierda mi parte.',
  'El original era narración del jugador («Acuerdas devolver…») impresa como «Seran: Acuerdas…». Ahora habla Seran y conserva el hecho: no se pagan sellos.')
p(g, HO, 'rooms', 'hoshai_campamento_lona', 'description', 'Descripción base del campamento (antes del acuerdo o la devolución).',
  'Una lona azul cubre tres cajas de viaje. La terraza queda al este y un sendero corto baja al sur hasta más cajas. Seran, un viajero con un palo corto, vigila la carga y dice que la polea del taller es suya hasta que le paguen. Puedes hablar con él antes de acercarte.',
  'Presenta a Seran por su nombre antes de que aparezca el aviso del salteador: así el niño entiende que es la misma persona.')
p(g, HO, 'rooms', 'hoshai_campamento_lona', 'signals[creature=forajido_camino].text', 'Señal del salteador en el campamento, mientras no hay acuerdo.',
  'Seran golpea una caja con su palo corto para que no te acerques a la carga. No te corta el paso: la terraza sigue libre al este.',
  'Integrable ya. Ver la propuesta de código siguiente: el botón seguirá diciendo «Salteador de cargas».')
p(g, HO, 'rooms', 'hoshai_campamento_lona', 'signals[creature=forajido_camino].dialogue', 'REQUIERE CÓDIGO: diálogo de adversario propio de esta señal (y nombre visible «Seran»), en lugar del diálogo común del Salteador de cargas.',
  json.dumps({'qué quieres': 'Que me paguen el transporte. Mientras no me paguen, la polea se queda conmigo.',
              'por qué': 'Subí estas cajas hasta aquí y nadie me pagó. No soy un ladrón: es lo único que tengo para que me escuchen.',
              'dejar paso': 'La terraza está libre. Si quieres arreglarlo hablando, habla conmigo, no con mi palo.'}, ensure_ascii=False),
  'Hoy el jugador ve a la vez «Seran · cuenta» y «Hablar con Salteador de cargas · exigencia» con el texto genérico «La carga se queda aquí». Son la misma persona con dos voces. Necesita un campo por señal (p. ej. signals[].name y signals[].dialogue) que el motor prefiera al de la criatura.',
  requiere_codigo=True)
p(g, HO, 'rooms', 'hoshai_taller_apoyos', 'actions[id=hoshai_entregar_polea].text', 'Acción «Devolver la polea y explicar la cuenta» con la polea en la mochila y Daren presente.',
  'Pones la polea sobre el banco y le das a Daren la tablilla de Seran. Daren reconoce la marca del mango enseguida. Lee la cuenta despacio y la deja junto al dibujo de los escalones: «Antes de decir quién tiene razón, quiero compararlo con mis notas del transporte.»',
  'Narración con cita breve (no voz «Daren:»), para que no choque con delivery_text y payment_dialogue que llegan justo después.')

# ───────────────────────── A5 · Khariel · Luma ─────────────────────────
g = 'A5 · khariel_cornisa · Luma (Hoshai)'
q = 'khariel_cornisa'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'Mando paquetes a los pueblos de abajo por la cornisa, ese camino estrecho pegado a la roca. El otro día, el observador del balcón apuntó en su cuaderno que una carga desapareció detrás de la roca, y ahora hay quien dice que la cornisa es peligrosa. Puede que sólo la perdiera de vista. Ve al balcón sobre el valle, pasado el depósito de herramientas. Mira la cornisa y deja allí una nota: que sólo pasen cargas pequeñas, o que alguien revise los apoyos antes. Luego vuelve y dímelo.',
  'Une el encargo con un detalle que ya existía y nadie usaba (cuaderno: «se perdió de vista una carga, no la carga»). La ruta detallada (plaza → norte → este → norte → oeste) queda en accept_text para no alargar la voz.',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Luma, la comerciante de cintas, envía paquetes por la cornisa del valle y ha oído que es peligrosa. Ve al balcón sobre el valle (desde la plaza: norte al patio de las casas, este al lavadero, norte al depósito; el balcón está al oeste), examina la cornisa y deja allí tu recomendación: sólo cargas pequeñas, o revisar los apoyos antes de usarla. Después vuelve al mercado y cuéntaselo a Luma.',
  'Quita «Son unos pocos pasos» (no son pocos: cinco tramos).')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'Luma ya tiene tu recomendación. Puedes cerrar el encargo con ella aquí, en el mercado.',
  'La última condición es hablar con Luma en el mercado.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Luma ata una cinta clara a la tablilla de los envíos y escribe al lado lo que recomendaste para la cornisa.',
  'Usa el código de colores de cintas ya descrito en el mercado.', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Cuando alguien vuelva a decir que la cornisa es peligrosa, le enseñaré esta nota. Es mejor que un rumor.',
  'Consecuencia social, válida para las dos recomendaciones.', defecto=DEF_PAY)
p(g, HO, 'npcs', 'hoshai_luma', 'topics.cornisa.text', 'Hablar con Luma · cornisa, tras dejar la nota (hoshai_cornisa_decidida). Fija hoshai_cornisa_informada. Acción requerida.',
  'Así que la viste con tus propios ojos. Eso me sirve más que lo que se oye en la plaza. Las cargas grandes seguirán por el camino principal; para lo demás, haré caso a tu nota.',
  'El original se imprimía como «Luma: Luma escucha tu recomendación…». Ahora es voz; los estados posteriores ya distinguen las dos recomendaciones.')
p(g, HO, 'rooms', 'hoshai_balcon_valle', 'examine.cornisa', 'Examinar cornisa antes de dejar la nota. Acción requerida.',
  'La cornisa es un camino estrecho pegado a la roca. Tiene apoyos para los pies y sitio para una persona con un bulto pequeño; un carro no cabe. Detrás de la roca el camino se pierde de vista un rato y vuelve a aparecer más abajo.',
  'El original («Oculta el paso frío incluso con buena luz») no daba base para decidir. Ahora las dos notas tienen sentido.')

# ───────────────────────── A6 · Velmora · Varo ─────────────────────────
g = 'A6 · velmora_recipiente · Varo, Elin y Desi (Nhal)'
q = 'velmora_recipiente'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'Elin, la artesana, dejó a reparar su recipiente pequeño en el taller de Desi y me pidió que se lo llevara. Yo no puedo dejar el puesto. Ya está arreglado y se está secando en el secadero, al lado de un juguete recién pegado. Comparten apoyo: si lo levantas mal, el juguete se cae. Habla primero con Elin, en su puerta, pasado el patio de reuniones, para saber cuál es el suyo. Luego pregunta a Desi, en el taller, cómo sacarlo. Llévaselo a Elin y vuelve a decirme que lo tiene.',
  'El original mezclaba dos recipientes y nombraba a Leris (otra historia). Ahora: un objeto, una dueña, un peligro concreto (el juguete), el orden real que exige el motor (Elin → Desi → secadero → Elin).',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Varo, el comerciante, te pide llevar a Elin su recipiente pequeño, que se está secando en el taller de Desi junto a un juguete. Pregunta a Elin cuál es (su puerta está al este del patio de reuniones) y a Desi cómo sacarlo sin mover el apoyo del juguete (el taller está al norte del claro). Recógelo en el secadero, entrégaselo a Elin y vuelve al mercado.',
  'Resumen. Quita «Conserva la tabla que sostiene el juguete» sin explicar por qué.')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'Elin ya tiene su recipiente y el juguete sigue secándose en su tabla. Vuelve al mercado de Velmora para contárselo a Varo.',
  'Se dispara en la puerta de Elin.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Le cuentas a Varo que Elin recibió su recipiente y que el juguete sigue en su apoyo del secadero.',
  'Varo no ve nada desde el puesto; la entrega es la noticia.', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Bien hecho. Elin tiene lo suyo y Desi no tendrá que volver a arreglar el juguete. Así me gusta que se hagan los recados.',
  'Consecuencia doble, sin acusar a nadie.', defecto=DEF_PAY)
p(g, NH, 'npcs', 'nhal_varo', 'topics.recipiente', 'Hablar con Varo · recipiente, antes de completar la entrega.',
  'Elin dejó a reparar su recipiente pequeño en el taller de Desi. Ya está arreglado, secándose al lado de un juguete. No lo cojas sin preguntar: primero habla con Elin para saber cuál es, y con Desi para saber cómo sacarlo.',
  'Mismo orden y mismas personas que el encargo; quita a Leris de este hilo.')
p(g, NH, 'npcs', 'nhal_elin', 'topics.entrega.text', 'Hablar con Elin · entrega. Fija nhal_elin_recipiente_reconocido.',
  'El pequeño, el que está en el taller, es mío. No lo confundas con el cuenco grande del patio, que es de todos. El aro y la tabla donde se seca son de Desi. Pregúntale cómo sacarlo sin tirar nada.',
  'Corrige una contradicción: decía «el aro es mío», pero la acción y los estados dejan el aro en el taller. También era narración dentro de la voz.')
p(g, NH, 'npcs', 'nhal_desi', 'topics.apoyo.text', 'Hablar con Desi · apoyo. Fija nhal_desi_apoyo_aclarado.',
  'Llévate sólo el recipiente. El aro y la tabla se quedan: la tabla sostiene el juguete, que todavía está húmedo. Si la mueves, la pata se tuerce y vuelta a empezar.',
  'Decía «el aro puede llevarse», contrario a la acción del secadero. Quita las comillas internas.')
p(g, NH, 'rooms', 'nhal_umbral_elin', 'actions[id=nhal_entregar_recipiente].text', 'Acción «Devolver el recipiente a Elin» con el recipiente en la mochila y Elin presente.',
  'Le das a Elin su recipiente pequeño. Lo gira con la mano buena y sonríe al ver la reparación. Cuando le cuentas que la tabla se quedó sosteniendo el juguete, asiente: «Bien. Que una ayuda no deje otra cosa rota detrás.»',
  'Más concreto (mano buena: su lesión es canon) y la cita queda como narración.')

# ───────────────────────── A7 · Narevia · Tila ─────────────────────────
g = 'A7 · narevia_preparativos · Tila, Nima y el paño (Lethra)'
q = 'narevia_preparativos'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'Mira y su hermana Sola van a cenar con sus familias en la cocina vecinal. Yo llevo los cuencos, pero no sé dónde ponerlos. Mira quiere cubrir la mesa con el paño común, el que tiene costuras de toda la familia, y todavía está secándose en la plataforma. Ve a mirar las costuras: desde la plaza, entra en el taller de fibras y baja a la plataforma de secado. Decide si conviene esperar a que seque o cenar bajo la cubierta y dejarlo tendido. Cuéntaselo a Nima, en la cocina, y vuelve para decirme adónde llevo los cuencos.',
  'Da a Tila un motivo propio (lleva los cuencos) y presenta la cena de las hermanas, que es el corazón de la historia de Lethra. Ruta: mercado → norte → este → sur; cocina: este → sur.',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Tila lleva los cuencos para la cena de Mira y Sola en la cocina vecinal. Mira las costuras del paño común en la plataforma de secado (al sur del taller de fibras) y elige: esperar a que seque para cubrir la mesa, o cenar bajo la cubierta y dejarlo tendido. Lleva tu propuesta a Nima, en la cocina, y vuelve al mercado con Tila.',
  'Resumen. Quita el «Puedes elegir…» abstracto.')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'Nima ya sabe dónde irán los cuencos. Vuelve al mercado de Narevia para decírselo a Tila.',
  'Se dispara en la cocina.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Le dices a Tila lo que acordaste con Nima. Tila cuenta los cuencos y los pasa a la cesta de arriba, la que no se moja.',
  'Usa el detalle del mercado: las cestas se levantan del fondo para no mojarse.', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Entonces ya sé adónde ir. Llevaré los cuencos antes de que empiece la cena.',
  'Breve: la escena fuerte ya ocurrió en la cocina.', defecto=DEF_PAY)
p(g, LE, 'npcs', 'lethra_nima', 'topics.preparativos.text', 'Hablar con Nima · preparativos, tras elegir en la plataforma (lethra_plan_elegido). Fija lethra_reunion_comunicada. Acción requerida.',
  'Bien pensado. Apunto dónde van los cuencos, así no los movemos dos veces. Ahora le aviso a Mira para que sepa qué hacemos con el paño.',
  'Era narración impresa como «Nima: Nima escucha…».')
p(g, LE, 'rooms', 'lethra_plataforma_secado', 'examine.costuras', 'Examinar costuras en la plataforma. Acción requerida.',
  'Distintas manos repararon el paño en distintas reuniones familiares. La costura más corta todavía está húmeda al tocarla; las demás ya secaron.',
  'Da al jugador un dato para elegir entre esperar o cenar bajo cubierta. La costura corta es la de Sola (canon).')

# ───────────────────────── A8 · Vaisgard · Arel ─────────────────────────
g = 'A8 · vaisgard_aviso_carga · Arel, Tov y Nera (Veyra)'
q = 'vaisgard_aviso_carga'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'Ha llegado un rumor: dicen que a Tov, la porteadora de piedra, le han robado la carga. No pienso repetirlo sin saber de dónde viene. Tov está con su carro en la puerta del camino de Korven: desde la plaza de las cinco rutas, cruza el patio de los animales hacia el oeste. Pregúntale qué pasó de verdad. Después lleva su noticia a Nera, en el archivo de cargas, aquí al lado, al este. Vuelve cuando Nera lo haya apuntado.',
  'El rumor de robo se vuelve el problema concreto. Rutas comprobadas (patio de mensajes → oeste ×3; archivo al este).',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Arel, la mensajera, ha oído que robaron la carga de Tov y no quiere repetirlo sin comprobarlo. Pregunta a Tov en la puerta del camino de Korven (al oeste, pasado el patio de los animales) y lleva su noticia a Nera, en el archivo de cargas, al este del patio de mensajes. Vuelve con Arel cuando Nera lo haya apuntado.',
  'Quita «ninguna opción debe inventar un robo» (voz de diseño).')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'Nera ya tiene apuntada la noticia de Tov. Vuelve al patio de mensajes, al oeste, para contárselo a Arel.',
  'Se dispara en el archivo; el patio está justo al oeste.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Le cuentas a Arel lo que dijo Tov y lo que apuntó Nera. Arel copia el aviso en una tablilla nueva y escribe debajo de dónde viene.',
  'Coincide con la memoria posterior de Arel (copia con fuente).', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Separador roto, no robo. Eso es lo que saldrá por los caminos. Si hubiera repetido el rumor, Tov habría tenido que arreglar también su nombre.',
  'Retoma la frase de Tov («tendré que reparar también esa historia»).', defecto=DEF_PAY)
p(g, VE, 'npcs', 'veyra_tov', 'topics.aviso.text', 'Hablar con Tov · aviso. Fija encargo_veyra_demora_conocida. Acción requerida.',
  'Nadie me ha robado nada. La carga está entera, mírala. Se rompió un separador, esta tabla de aquí, y tengo que volver a colocar las piedras antes de entrar. Dile a Nera que llegaré tarde, no que he perdido la carga.',
  'Quita las comillas internas y añade el gesto de mostrar la tabla rota.')
p(g, VE, 'npcs', 'veyra_nera', 'topics.aviso_preciso.text', 'Hablar con Nera · aviso_preciso, tras escuchar a Tov y antes de entregar. Fija encargo_veyra_aviso_entregado y _preciso.',
  'Separador roto, carga entera, llegará tarde. Y lo dice la propia Tov. Lo apunto así, con su nombre. La carga sigue en la lista de llegadas; nadie va a hablar de robo.',
  'Era narración («Nera anota…») dentro de la voz.')
p(g, VE, 'npcs', 'veyra_nera', 'topics.pedir_comprobacion.text', 'Hablar con Nera · pedir_comprobacion (alternativa a la anterior). Fija encargo_veyra_aviso_entregado y _comprobar.',
  'De acuerdo, no cambio nada todavía. Dejo la carga como pendiente. Antes de tocar la lista iré a ver ese separador con Tov. Hasta entonces no está perdida: sólo tarda.',
  'Era narración del jugador («Pides a Nera…»). Mantiene el hecho: queda pendiente, no perdida.')
p(g, VE, 'npcs', 'veyra_nera', 'topics (claves)', 'Etiquetas de los botones «Nera · aviso_preciso» y «Nera · pedir_comprobacion».',
  json.dumps({'aviso_preciso': 'anotar lo que dijo Tov', 'pedir_comprobacion': 'pedir que lo compruebe'}, ensure_ascii=False),
  'Cambio de datos opcional: renombrar las dos claves para que el botón no muestre guiones bajos. Ningún encargo referencia estos temas por clave; revisar tests antes.')

# ───────────────────────── A9 · Vaisgard · Seli ─────────────────────────
g = 'A9 · vaisgard_toldo · Seli (Veyra)'
q = 'vaisgard_toldo'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'El toldo que comparto con mi vecino se ha rasgado por una costura vieja. Cuando llueve, el agua cae justo en la puerta del taller de abajo, y ya hablan de cerrarlo. No hace falta: basta con coser bien y dejar que el agua salga hacia la calle. Primero mira la costura, para ver dónde está el daño. Después puedes ayudarme de dos maneras: traer un haz de junco (Bela, en el mercado de aquí al oeste, presta uno para esto) y lo atamos, o sujetarme las perchas mientras marco la costura, y yo la termino después sin gastar junco.',
  'Qué pasa, a quién perjudica, qué no hay que hacer (cerrar el taller) y las dos formas reales de ayudar que ofrece la sala.',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Seli tiene un toldo rasgado que moja la puerta del taller de abajo. Examina la costura en la calle de los toldos. Luego elige: llevarle un haz de junco (Bela, en el mercado al oeste, presta uno) para atar el desgarro, o sujetar las perchas para que Seli lo termine. El encargo se entrega aquí mismo, a Seli.',
  'Resumen.')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'El toldo ya tiene arreglo y el agua podrá salir hacia la calle. Puedes cerrar el encargo con Seli aquí mismo.',
  'Todo ocurre en la misma calle.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Seli tira del borde del toldo para probarlo. Esta vez, cuando llueva, el agua resbalará hacia la calle y no hacia la puerta del taller.',
  'No depende de que esté lloviendo ahora.', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'El taller de abajo podrá seguir abierto. Ya les diré a los vecinos que no hacía falta cerrar nada: sólo coser bien.',
  'Cierra el motivo de Seli (tema «vecinos»).', defecto=DEF_PAY)
p(g, VE, 'rooms', 'veyra_calle_toldos', 'actions[id=veyra_preparar_perchas].text', 'Acción «Preparar las perchas para que Seli termine» con Seli presente.',
  'Sostienes las perchas mientras Seli marca con tiza dónde empieza el desgarro y por dónde debe salir el agua. Ella terminará la costura sin gastar junco. Si Bela te prestó un haz, puedes devolvérselo en el mercado.',
  'Convierte la orden «devuelve cualquier fibra prestada a Bela» en información, y nombra dónde.')

# ───────────────────────── A10 · Brumak · Taren ─────────────────────────
g = 'A10 · brumak_taza · Taren (Korven)'
q = 'brumak_taza'
p(g, W, 'quests', q, 'accept_dialogue', C_ACC,
  'Quiero hacerle una taza a mi madre. La primera me salió tan pequeña que no le cabía nada; la segunda, tan grande que no la puede levantar. Antes de hacer la tercera necesito otra mirada. Pídeme las medidas, ve al horno viejo, aquí al este, y mira el recipiente torcido del banco: ahí se ve qué pasa cuando la base no va de acuerdo con el resto. Marca allí lo que recomiendas y vuelve a decírmelo.',
  'Retoma la gracia del tema «pieza» (taza pequeña, taza enorme) y da un objetivo claro.',
  defecto=DEF_ACC)
p(g, W, 'quests', q, 'accept_text', C_TXT,
  'Taren, la alfarera, quiere hacer una taza para su madre que no sea ni muy pequeña ni muy pesada. Pídele las medidas, examina el recipiente torcido del horno viejo (al este) y marca allí tu recomendación: base más ligera o base más ancha. Vuelve a contárselo. Taren trabaja de día.',
  '«Taren trabaja de día» avisa del horario real (schedule: día).')
p(g, W, 'quests', q, 'ready_text', C_READY,
  'Taren ya tiene tu recomendación. Puedes cerrar el encargo con ella aquí, en el rincón de las muestras.',
  'La última condición es hablar con Taren en su rincón.', defecto=DEF_READY)
p(g, W, 'quests', q, 'delivery_text', C_DEL,
  'Taren pone tu marca junto a las medidas de la mano y aparta un trozo de arcilla para la prueba.',
  'Coincide con su memoria posterior («alinea la arcilla con tu marca»).', defecto=DEF_DEL)
p(g, W, 'quests', q, 'payment_dialogue', C_PAY,
  'Esta vez empiezo por lo que necesita mi madre, no por lo que me sale de las manos. Gracias por mirar con calma.',
  'Prepara el remate cómico ya existente (la taza grande acaba siendo para su hermano).', defecto=DEF_PAY)
p(g, KO, 'npcs', 'korven_taren', 'topics.medidas.text', 'Hablar con Taren · medidas (de día). Fija encargo_korven_taza_medida. Acción requerida.',
  'Mira estas dos marcas: la de la izquierda es la mano de mi madre; la de la derecha, la taza grande. El aro pequeño le queda bien a la mano, eso no lo cambio. Lo que dudo es la base: más ligera, para que pese menos, o más ancha, para que no se vuelque. Mira el recipiente torcido del horno y decide tú.',
  'Las dos opciones del horno no eran opuestas («conservar el aro» frente a «base ancha manteniendo el aro»). Ahora la elección es una sola pregunta: ligera o estable.')
p(g, KO, 'npcs', 'korven_taren', 'topics.recomendación.text', 'Hablar con Taren · recomendación, tras marcar en el horno. Fija encargo_korven_taza_informada. Acción requerida.',
  'Así que esto es lo que viste en el horno. Bien: no elegiste sólo por tamaño, pensaste en quien la va a usar. Haré una prueba con tu marca antes de dársela a mi madre.',
  'Era narración («Taren compara…») dentro de la voz.')
p(g, KO, 'rooms', 'korven_horno_reposo', 'actions[id=korven_recomendar_aro].label', 'Botón en el horno tras pedir las medidas.',
  'Recomendar una base más ligera',
  'Etiqueta simétrica con «Recomendar una base más estable».')
p(g, KO, 'rooms', 'korven_horno_reposo', 'actions[id=korven_recomendar_aro].text', 'Al pulsar el botón anterior.',
  'Comparas el recipiente torcido con las medidas: lo que más pesa es la base, demasiado gruesa. Marcas una base más fina y dejas el aro como está, a la medida de la mano de la madre de Taren.',
  'Relaciona la decisión con lo que se ve en el recipiente.')
p(g, KO, 'rooms', 'korven_horno_reposo', 'actions[id=korven_recomendar_base].text', 'Al pulsar «Recomendar una base más estable».',
  'Comparas el recipiente torcido con las medidas: se inclina porque la base es estrecha. Marcas una base un poco más ancha y dejas el aro pequeño. La taza pesará algo más, pero no se volcará.',
  'Consecuencia comprensible de la otra opción.')

# ───────────────────────── B · Salteador de cargas ─────────────────────────
g = 'B · Salteador de cargas (forajido_camino, común a 5 lugares)'
C_HUM = 'Común a Compuerta abierta (Edran), Campamento de la lona azul (Hoshai), Cruce de los sacos vacíos (Korven), Ribera hacia Edran (Lethra) y Subida entre árboles (Nhal). Debe valer en los cinco.'
p(g, W, 'creatures', 'forajido_camino', 'dialogue', 'Botones «Hablar con Salteador de cargas · …» mientras está presente y no ha empezado el enfrentamiento. ' + C_HUM,
  json.dumps({'qué quieres': 'Lo que lleves en la mochila. Déjala en el suelo y sigue tu camino. No me hace falta pelear contigo.',
              'por qué': 'Este invierno nadie me ha contratado para cargar. Cuando no hay trabajo, el camino parece fácil de cobrar. Ya sé que no está bien. Hoy no se me ocurre otra cosa.',
              'dejar paso': 'Por donde viniste está libre. Si das la vuelta, no te sigo.'}, ensure_ascii=False),
  'Hoy usa el texto del motor («La carga se queda aquí…»). Tres temas: qué pide, por qué (motivo humano sin justificarlo) y la salida real. «No te sigo» es cierto: fuera de combate no hay persecución. No menciona agua, bosque ni piedra para servir en las cinco salas.',
  defecto='(no existe: exigencia / salida del motor)')
p(g, W, 'creatures', 'forajido_camino', 'description', 'Examinar Salteador de cargas. ' + C_HUM,
  'Una persona con ropa de viaje gastada y un palo corto pide el equipaje a quien pasa. Se queda cerca de una salida, por si tiene que irse. Lo que hace es cosa suya: no habla por su pueblo ni por su especie.',
  'Mismo contenido canónico en lenguaje más llano.')
p(g, W, 'creatures', 'forajido_camino', 'combat_intro', 'Al elegir «Enfrentarte a Salteador de cargas».',
  'El salteador aprieta el palo con las dos manos y se planta delante de ti. «Está bien. Si no me das la carga, la tomaré yo.» Vigila el palo.',
  'Una frase suya antes del golpe, sin insultos. Usa «salteador», el nombre que ve el jugador, no «forajido».')
p(g, W, 'creatures', 'forajido_camino', 'defeat_text', 'Al vencer (antes de la línea de XP y sellos). El adversario vuelve a aparecer pasado un tiempo (world.deaths 300 s).',
  'El salteador tropieza y suelta el palo. Levanta las manos: «¡Basta! Ya está.» Lo recoge sin volver a alzarlo y se aparta del camino.',
  'No afirma muerte ni marcha definitiva (el motor lo repone). En Hoshai, Seran sigue en el campamento como NPC: «se aparta del camino» sigue siendo cierto.',
  defecto='(no existe: «… deja de impedirte el paso…» del motor)')

# ───────────────────────── C · Fauna de Edran ─────────────────────────
g = 'C · Fauna de Edran: una señal por lugar'
C_POOL = 'Sorteo de wildlife_pool al llegar o buscar. El animal sigue presente: se puede examinar, evaluar o enfrentar.'
SPOTS = {
 'edran_salida_huertos': ('Salida de las Cercas Bajas',
   'Algo pequeño y espinoso corre pegado a la cerca y se mete bajo una mata del borde. Desde allí asoma el hocico: es un Espinajo, y ese trozo de cerca es suyo.',
   'Una forma baja y alargada corre junto a la acequia y se para con la cabeza hacia un hueco de la cerca. Es un Mordelinde: busca por dónde irse, no a quién morder.',
   'Lejos, más allá de la acequia, un lomo enorme asoma sobre la hierba. Es un Cornalomo. Cada paso suyo hunde la tierra. Mejor mirarlo desde aquí.'),
 'edran_arboleda': ('Arboleda de los tres árboles',
   'Bajo las raíces levantadas del último árbol, un Espinajo escarba la tierra. Al oír tus pasos se pega al suelo con las espinas de punta y se queda quieto, vigilándote.',
   'Un Mordelinde sale de entre las raíces, aparta unas semillas con las manos y se queda quieto, mirando el hueco bajo la raíz más grande.',
   'Entre los troncos se ve, a lo lejos, un Cornalomo arrancando hierba. Es más grande que el banco de tierra entero. No se acerca al sendero.'),
 'edran_camino_carros': ('Camino de carros',
   'Un Espinajo cruza la rodada de la hondonada a toda prisa y se esconde entre las piedras bajas del borde. Las espinas le asoman por encima, quietas.',
   'Un Mordelinde cruza la rodada alta pegado al suelo y se para junto a las piedras bajas, buscando un hueco entre ellas.',
   'En la hondonada, lejos de las rodadas, un Cornalomo se mueve despacio. El suelo tiembla un poco a cada paso.'),
 'edran_terraplen': ('Terraplén de la Subida',
   'Entre las raíces del terraplén, un Espinajo baja la cabeza y eriza las espinas. Se ha quedado con el ensanche de media cuesta y no parece dispuesto a compartirlo.',
   'Un Mordelinde asoma de un agujero entre las raíces del terraplén. Mira el camino, mira el agujero, y espera.',
   'Desde la media cuesta se ve un Cornalomo abajo, en el campo. Su lomo sobresale por encima de la hierba alta. Está lejos y no mira hacia el camino.'),
 'edran_linde_piedra': ('Paso hacia Korven',
   'Entre las últimas matas antes de las piedras, un Espinajo corre unos pasos y se para. Vuelve al mismo borde y se agacha con las espinas hacia ti.',
   'Entre dos piedras, un Mordelinde aparta semillas con las manos delanteras. Al notar tus pasos, gira la cabeza hacia la grieta más cercana.',
   'En el prado, al sur, un Cornalomo levanta la cabeza. Sus huellas son anchas como una rueda de carro. Desde las piedras se le ve bien, y de lejos.'),
 'edran_sendero_juncos': ('Sendero del Agua Oculta',
   'Un Espinajo sale de los juncos, cruza el sendero firme y se agacha en la zona despejada. Se queda ahí, de cara a ti, con las espinas levantadas.',
   'Un Mordelinde corre por el borde firme del sendero y se para a la entrada de los juncos, con el hocico hacia un paso entre los tallos.',
   'Al otro lado de los juncos, un Cornalomo aplasta la hierba al pasar. Su peso se nota hasta en el agua quieta.'),
 'edran_parcela_vieja': ('Parcela vieja',
   'Junto a la piedra de la parcela, un Espinajo da vueltas cortas entre las hileras viejas y siempre regresa al mismo rincón.',
   'Un Mordelinde escarba junto a la piedra, entre los brotes. Cuando te ve, deja de comer y mira hacia el rincón seco.',
   'Más allá de la loma asoma el lomo de un Cornalomo. Va despacio y no se acerca a las hileras.'),
 'edran_sauces': ('Borde de los Sauces Bajos',
   'Un Espinajo bebe entre las raíces del sauce. Al verte, retrocede hasta la hierba y se queda agazapado, con las espinas de punta.',
   'Un Mordelinde corre por la orilla bajo el sauce y se para con la cabeza hacia un hueco entre las raíces. Las aves del sauce ni se mueven.',
   'Al otro lado del agua, un Cornalomo baja la cabeza para beber. Las aves del sauce se callan hasta que vuelve a levantarla.'),
 'edran_calzada': ('Calzada de piedra',
   'Un Espinajo cruza los cantos a saltitos y se mete en el borde de hierba. Desde allí te sigue con la mirada.',
   'Un Mordelinde cruza los cantos a toda prisa y se para en el borde de hierba, mirando un hueco entre las piedras.',
   'Detrás de la curva, fuera de la calzada, un Cornalomo pisa la hierba y la deja aplastada. Un carro espera a que se aleje antes de seguir subiendo.'),
 'edran_sendero_regreso': ('Senda de regreso',
   'Al pie del árbol aislado, un Espinajo husmea el barro. Cuando te acercas, se aplasta contra la tierra y eriza las espinas.',
   'Un Mordelinde aparece entre las raíces del árbol aislado, con semillas en las manos. Se queda quieto, mirando hacia un hueco bajo el tronco.',
   'Lejos, en los campos, se ve el lomo de un Cornalomo por encima de la hierba. Desde el árbol aislado parece pequeño. No lo es.'),
}
for rid, (name, esp, mor, cor) in SPOTS.items():
    for cid, text in (('espinajo_rastrojo', esp), ('mordelinde', mor), ('cornalomo', cor)):
        p(g, ED, 'rooms', rid, f'wildlife_pool[creature={cid}].text', f'{name}. {C_POOL}', text,
          'Hoy la misma frase se repite en 10 lugares, incluida la calzada de piedra («tallos viejos») y el terraplén («sombra sobre el agua»). Ésta usa lo que hay en este sitio.')
p(g, ED, 'rooms', 'edran_surcos', 'signals[creature=espinajo_rastrojo].text', 'Señal fija del Campo de surcos (también la ven quienes buscan).',
  'En la hilera de tallos viejos, un Espinajo corre unos pasos, se para y vuelve al mismo borde. Cuando te mira, eriza las espinas y se agacha entre los tallos.',
  'Movimiento, refugio y reacción, como pidió Javier, sin prometer que se vaya.')
p(g, ED, 'rooms', 'edran_bajo_humedo', 'signals[creature=mordelinde].text', 'Señal fija de la Hondonada húmeda.',
  'Una forma baja cruza la hierba oscura y se para en el borde del barro. El Mordelinde mira hacia un hueco entre las piedras: es la salida que vigila.',
  'La hondonada es barro, no agua abierta: quita la «sombra sobre el agua». No promete que huya (eso depende de cómo se acerque el jugador).')
p(g, ED, 'rooms', 'edran_prado', 'signals[creature=cornalomo].text', 'Señal fija del Prado de las Marcas Anchas.',
  'En la zona aplastada del prado, un Cornalomo arranca hierba con calma. Cuando pisa, la tierra se hunde. Desde el sendero se le ve entero; acercarse ya es otra cosa.',
  'Quita «por encima de una primera formación» (lenguaje de reglas) y deja la advertencia en imagen.')

# ───────────────────────── D · Otras voces corregidas ─────────────────────────
g = 'D · Narración metida en la voz de un NPC (fuera de encargos)'
p(g, ED, 'npcs', 'edran_nela', 'topics.cuerda.text', 'Hablar con Nela · cuerda llevando una cuerda recuperada (la consume).',
  '¡Una cuerda buena! La ato en este tramo de la escalera. Ahora hay dos apoyos: cuando vuelvas a bajar, usa el de la derecha.',
  'Se imprimía «Nela: Nela prueba la cuerda… «…»».')
p(g, ED, 'npcs', 'edran_oren', 'topics.caja.text', 'Hablar con Oren · caja. Fija edran_caja_localizada.',
  'La subí a la repisa cuando entró agua. La repisa queda detrás de la compuerta, al este de la bifurcación. Por eso dejé la taza en el escalón seco.',
  'Sólo quita las comillas internas.')
p(g, ED, 'npcs', 'edran_oren', 'topics.ayuda.text', 'Hablar con Oren · ayuda (una vez). Fija edran_oren_orientado.',
  '¿Nela, la del canal? Si tiene trabajo, prefiero eso a seguir aquí abajo. Recojo la manta y voy a hablar con ella.',
  'Era narración del jugador («Le indicas…») dentro de la voz de Oren.')

# ───────────────────────── E–H · Fauna de las otras regiones ─────────────────────────
WHY_REP = 'Hoy la misma frase sale en {n} lugares de la región. Ésta usa lo que hay en este sitio y mantiene al animal presente (se puede examinar o evaluar).'
WHY_BIG = 'Animal muy superior: se ve de lejos, sin contacto; el aviso de acercarse ya existe aparte. Hoy la misma frase sale en {n} lugares.'
def fauna(grupo, archivo, region_rooms, big, counts):
    for rid, entries in region_rooms.items():
        for cid, text in entries.items():
            name = resolve(archivo, 'rooms', rid, 'name')
            why = (WHY_BIG if cid in big else WHY_REP).format(n=counts[cid])
            p(grupo, archivo, 'rooms', rid, f'wildlife_pool[creature={cid}].text', f'{name}. {C_POOL}', text, why)

fauna('E · Fauna de Hoshai', HO, {
 'hoshai_estribacion': {'unapiedra': 'Junto al arroyo, un Uñapiedra sube por una roca casi lisa. Sus uñas se agarran a bultos que tú ni ves. Se para a media altura y te mira de lado.',
   'rasgacumbres': 'Muy arriba, en la sierra, una forma grande cruza una cornisa y deja caer piedrecitas. Es un Rasgacumbres. Desde aquí abajo parece pequeño.'},
 'hoshai_repecho_raices': {'unapiedra': 'Un Uñapiedra trepa por la roca que asoma entre dos raíces. Cuando pasas, se aplasta contra la piedra y se queda quieto, del mismo color que ella.',
   'rasgacumbres': 'Por encima de los árboles inclinados, unas garras rascan la roca. Un Rasgacumbres asoma en un saliente lejano y vuelve a quedar tapado por la curva.'},
 'hoshai_pared_goteo': {'unapiedra': 'Sobre la pared húmeda, un Uñapiedra avanza por donde gotea el agua. Prueba cada saliente con una uña antes de apoyarse.',
   'rasgacumbres': 'En la ladera de enfrente, al otro lado del valle, un Rasgacumbres baja despacio entre rocas. Las piedras que suelta tardan en dejar de sonar.'},
 'hoshai_pinar_discontinuo': {'unapiedra': 'Un Uñapiedra pasa de un pino a una roca sin pisar las agujas del suelo. Se queda agarrado al lado de la piedra donde no da el viento.',
   'rasgacumbres': 'Desde un claro del pinar se ve, lejos y arriba, un Rasgacumbres sobre un risco. Tiene la cabeza vuelta hacia el valle, no hacia ti.'},
 'hoshai_agua_fria': {'unapiedra': 'En la piedra grande que desvía el agua, un Uñapiedra bebe agarrado al borde. Cuando te acercas a la orilla, sube un palmo y espera.',
   'rasgacumbres': 'Río arriba, en las rocas, hay marcas frescas de garras. Más lejos todavía, un Rasgacumbres se mueve entre las piedras altas.'},
 'hoshai_ladera_hitos': {'unapiedra': 'Un Uñapiedra se queda quieto encima de un grupo de piedras de señal, como si fuera una más. Sólo se le nota cuando cambia una uña de sitio.',
   'rasgacumbres': 'Por encima del paso entre paredes, un Rasgacumbres cruza la ladera de lado. Una piedra suelta rueda desde donde pisó y se para lejos del sendero.'},
 'hoshai_cuello_roca': {'unapiedra': 'En la pared del paso estrecho, un Uñapiedra se pega a la roca por encima de las cabezas. Cuando alguien golpea la piedra de aviso, se queda inmóvil.',
   'rasgacumbres': 'Arriba, en el borde de las paredes, una sombra grande tapa la luz un momento. Un Rasgacumbres mira el paso desde lo alto y sigue de largo.'},
 'hoshai_escalones_sol': {'unapiedra': 'Un Uñapiedra toma el sol en un escalón tallado, lejos del canal. Al ver tus pies, se pasa al borde de una piedra nueva, sin estorbar a nadie.',
   'rasgacumbres': 'Desde los escalones se ve la sierra. En una cornisa lejana, un Rasgacumbres se estira al sol. En los peldaños nadie deja de trabajar por él.'},
 'hoshai_collado_pino': {'unapiedra': 'Un Uñapiedra rodea el pino por las piedras partidas. Se para en la raíz más alta y te sigue con la mirada.',
   'rasgacumbres': 'Por encima del collado, un Rasgacumbres cruza una pared de roca. Cuando se detiene, sus garras dejan un rasguño claro en la piedra.'},
 'hoshai_aprisco_abierto': {'unapiedra': 'Un Uñapiedra se asoma por encima de la pared seca del aprisco. El rebaño no le hace caso, y él tampoco al rebaño.',
   'rasgacumbres': 'El rebaño se aprieta contra el lado protegido de la ladera. Muy arriba, un Rasgacumbres recorre la cresta. La pastora lo mira sin moverse.'},
 'hoshai_garganta_oeste': {'unapiedra': 'En la pared de la garganta, un Uñapiedra se agarra a una roca clara. Sus uñas levantan un poco de polvo.',
   'rasgacumbres': 'Por encima de la garganta, un Rasgacumbres baja hasta media pared y se para. Desde el ensanchamiento sólo se ven sus patas y una lluvia de polvo.'},
 'hoshai_senda_dosel': {'unapiedra': 'Un Uñapiedra sube por una roca con musgo junto al banco seco. Se mueve despacio, una pata cada vez.',
   'rasgacumbres': 'Entre los árboles altos se ve un trozo de montaña. Allí arriba, un Rasgacumbres cruza un paso de roca y se queda mirando el valle.'},
}, {'rasgacumbres'}, {'unapiedra': 12, 'rasgacumbres': 12})

fauna('F · Fauna de Korven', KO, {
 'korven_loma_cascajo': {'colagrieta': 'Del montón de cascajo asoma una cabeza alargada. El Colagrieta mira la pala y retrocede hacia una grieta, apoyándose en la cola gruesa.',
   'cascapedernal': 'En el cascajo, un Cascapedernal se recoge contra una piedra grande cuando tu sombra lo cubre. Su caparazón da un golpe seco contra la roca.',
   'quebrarrocas': 'Hacia el oeste, entre las rocas del cauce, un bloque se mueve. Detrás, un Quebrarrocas sigue empujando. El polvo sube hasta la loma.'},
 'korven_cauce_duro': {'colagrieta': 'Un Colagrieta toma el sol en una piedra del cauce. Al notar tus pasos en la arena, se mete de golpe en una junta; sólo queda fuera la punta de la cola.',
   'quebrarrocas': 'Cauce abajo se oye piedra contra piedra. Un Quebrarrocas aparta bloques del fondo seco, lejos del cuenco de las herramientas.'},
 'korven_meseta_baja': {'colagrieta': 'A la sombra de una de las dos piedras, un Colagrieta asoma la cabeza por una fisura. Cuando la sombra se mueve, él se mueve con ella.',
   'cascapedernal': 'Al pie de la otra piedra, un Cascapedernal raspa liquen. Cuando le cae tu sombra, recoge las patas y se queda pegado a la roca.',
   'quebrarrocas': 'Bajo la pared de la meseta, lejos de las dos piedras, un Quebrarrocas empuja una losa con el hombro. La losa cae de lado y el golpe rebota en la roca.'},
 'korven_hitos_paso': {'colagrieta': 'En la base de un mojón, un Colagrieta saca la cabeza de un hueco. Mira la pila de piedras y vuelve a meterse.',
   'quebrarrocas': 'Lejos de los mojones, un Quebrarrocas abre paso entre rocas que nadie ha marcado. Cada empujón deja una franja de polvo nueva.'},
 'korven_hendidura_transito': {'colagrieta': 'Por una grieta alta del paso estrecho asoma un Colagrieta. Cuando una rueda golpea la tabla, se esconde de golpe y luego vuelve a asomar.',
   'quebrarrocas': 'Al otro lado de la pared se oye arrastrar piedra. Por un hueco alto se ve el lomo de un Quebrarrocas empujando un bloque, lejos del sendero.'},
 'korven_cauce_observacion': {'colagrieta': 'Entre las piedras movidas, un Colagrieta busca una grieta. Prueba una, no cabe, y prueba otra.',
   'cascapedernal': 'Bajo una piedra de cara limpia, un Cascapedernal se mete de lado. El borde del caparazón roza la roca con un golpe breve.',
   'quebrarrocas': 'Al fondo del cauce, un Quebrarrocas apoya el cuerpo contra un bloque y lo hace rodar. Así se ven las piedras de cara limpia: alguien las ha movido.'},
 'korven_desvio_horno': {'colagrieta': 'Entre los trozos de recipientes, un Colagrieta asoma por encima del muro corto. Cuando un fragmento cruje bajo tu pie, retrocede.',
   'cascapedernal': 'Un Cascapedernal cruza la tierra quemada y se refugia bajo un fragmento grande de recipiente. El borde del caparazón asoma por un lado.',
   'quebrarrocas': 'Más allá del muro corto, lejos del horno, un Quebrarrocas empuja piedras. El temblor llega hasta los fragmentos del suelo.'},
 'korven_meseta_relevo': {'colagrieta': 'Junto a la pared baja, un Colagrieta asoma entre las lajas. Mira la mesa de las notas un momento y vuelve a su hueco.',
   'quebrarrocas': 'Hacia la garganta, lejos del refugio, un Quebrarrocas aparta piedras bajadas de la sierra. Desde la mesa se oye cada golpe.'},
 'korven_senda_viento': {'colagrieta': 'Con el viento llega polvo, y un Colagrieta se pega a la pared más baja: la cabeza dentro de una grieta, la cola fuera.',
   'quebrarrocas': 'Detrás del almacén, un Quebrarrocas empuja un bloque cuesta abajo. El viento se lleva el polvo antes de que llegue a las cubiertas.'},
 'korven_borde_tierra': {'colagrieta': 'En la zanja, un Colagrieta busca grieta entre las últimas rocas. Aquí hay más tierra que piedra y le cuesta encontrar dónde meterse.',
   'quebrarrocas': 'Al norte, donde todavía hay bloques grandes, un Quebrarrocas empuja una roca. Desde los pastos de la parada, el ruido llega flojo.'},
 'korven_peldanos_cortos': {'colagrieta': 'Bajo la repisa de las cuñas, un Colagrieta saca la cabeza. Una vecina lo ve, sonríe y aparta el pie.',
   'quebrarrocas': 'Lejos de las casas, fuera del camino, un Quebrarrocas mueve piedras en la ladera. Desde los escalones sólo se ve su polvo.'},
}, {'quebrarrocas'}, {'colagrieta': 11, 'quebrarrocas': 11, 'cascapedernal': 4})

fauna('G · Fauna de Lethra', LE, {
 'lethra_ribera_seca': {'pinzajunco': 'En el borde del cauce, un Pinzajunco camina de lado con una hoja seca en la pinza grande. Al llegar a su agujero, la mete dentro.',
   'saltalodo': 'Un Saltalodo hincha la bolsa del cuello entre las hierbas de la orilla. Su llamada suena hondo, como una gota grande al caer.',
   'dorsalodo': 'En la parte ancha del cauce, una espalda rugosa asoma del agua y vuelve a hundirse. Un Dorsalodo descansa en lo hondo; sus ondas llegan hasta la orilla.'},
 'lethra_tierra_esponjosa': {'pinzajunco': 'Junto a las varas del paso estrecho, un Pinzajunco levanta la pinza mayor hacia tus pies. No retrocede: ésa es su orilla.',
   'saltalodo': 'Sobre el barro, un Saltalodo moteado infla el cuello y llama. Cuando pisas, salta a una mancha de hojas y vuelve a llamar desde allí.',
   'dorsalodo': 'Más allá, hacia el juncal, la hierba alta queda aplastada en una franja ancha. Un Dorsalodo se arrastra hacia el agua, lento y pesado.'},
 'lethra_tablas_primeras': {'saltalodo': 'Bajo las tablas, un Saltalodo llama entre los apoyos. Su voz suena por todo el tramo de madera.',
   'dorsalodo': 'En uno de los dos canales, el agua se levanta en una ola sin viento. Un Dorsalodo pasa por debajo, lejos de las tablas.'},
 'lethra_ribera_firme': {'pinzajunco': 'Bajo un apoyo de madera, un Pinzajunco arrastra una hoja que se cayó de una envoltura. Nadie se la quita.',
   'saltalodo': 'Un Saltalodo salta de un recipiente vacío al barro y llama una vez. Una vecina se sobresalta y luego se ríe.',
   'dorsalodo': 'Lejos, donde el agua se ensancha, la espalda de un Dorsalodo asoma como una isla de barro. Quienes descargan siguen trabajando de este lado.'},
 'lethra_pasarela_curva': {'pinzajunco': 'Abajo, junto a un poste de la pasarela, un Pinzajunco corta una hoja con la pinza pequeña y sujeta el resto con la grande.',
   'saltalodo': 'En el agua quieta, junto a la baranda, un Saltalodo llama. Al oír tus pasos en la madera, salta a una hoja flotante.',
   'dorsalodo': 'En medio del agua quieta, una ola ancha avanza hacia la orilla. Un Dorsalodo nada por debajo, sin acercarse a la pasarela.'},
 'lethra_senda_elevada': {'saltalodo': 'Entre dos plataformas, un Saltalodo llama desde una hoja. Desde una ventana, alguien le contesta imitándolo.',
   'dorsalodo': 'Por un canal ancho entre las viviendas pasa despacio una espalda rugosa: un Dorsalodo. Las vecinas suben las cestas a las ventanas mientras pasa.'},
 'lethra_banco_barro': {'pinzajunco': 'En el barro firme, un Pinzajunco excava su agujero con la pinza grande. Se para y la apunta hacia ti.',
   'saltalodo': 'Un Saltalodo llama desde el borde del canal profundo. Después se queda quieto, mirando las ondas.',
   'dorsalodo': 'Las ondas que van contra el viento las mueve un cuerpo grande. En el canal profundo, un Dorsalodo asoma los ojos y un trozo de espalda.'},
 'lethra_ribera_oeste': {'pinzajunco': 'Un Pinzajunco cruza de lado por el barro, fuera de la cubierta, y arrastra un trozo de envoltura hasta su agujero.',
   'saltalodo': 'En el borde del barro, un Saltalodo llama hacia los pastos del oeste. Desde allí no le contesta ninguno.'},
 'lethra_hito_tierra': {'saltalodo': 'Entre las dos piedras del hito, un Saltalodo infla el cuello y llama. Otro le contesta desde el terreno inundable.',
   'dorsalodo': 'Abajo, en el terreno inundable, la hierba está aplastada en una franja ancha. Un Dorsalodo descansa en el barro, medio hundido.'},
 'lethra_ribera_sombra': {'saltalodo': 'Bajo la pasarela corta, un Saltalodo llama entre dos troncos. Su voz suena distinta debajo de los árboles.',
   'dorsalodo': 'En el canal, a la sombra, una espalda rugosa parece un tronco más. Hasta que se mueve: es un Dorsalodo.'},
}, {'dorsalodo'}, {'pinzajunco': 6, 'saltalodo': 10, 'dorsalodo': 9})

fauna('H · Fauna de Nhal', NH, {
 'nhal_arbol_umbral': {'rasgacorteza': 'Más adentro, bajo las copas, los pájaros se callan de golpe. Junto a un tronco lejano, algo con piel de corteza levanta la cabeza: un Rasgacorteza.'},
 'nhal_suelo_hojas': {'rasgacorteza': 'Hacia el este, un árbol tiene arañazos muy por encima de la altura de una persona. A su lado, quieto como otro tronco, hay un Rasgacorteza.'},
 'nhal_tronco_acostado': {'rasgacorteza': 'Al otro lado del tronco caído, entre los árboles, un Rasgacorteza se rasca contra la corteza. Las ramas altas tiemblan a cada movimiento.'},
 'nhal_corteza_clara': {'rasgacorteza': 'Lejos del árbol claro, entre troncos oscuros, un Rasgacorteza está inmóvil. Se le distingue porque los animales pequeños dan un rodeo para no pasar a su lado.',
   'rondamusgo': 'Un Rondamusgo hurga entre las hojas al pie del árbol claro. Al oírte se queda quieto, con una seta en la boca, y corre a una raíz hueca. Desde allí asoma el hocico.'},
 'nhal_raices_altas': {'rasgacorteza': 'Entre las raíces altas, lejos del sendero, un Rasgacorteza se separa un poco de su tronco y vuelve a pegarse a él.',
   'rondamusgo': 'Un Rondamusgo sale de entre dos raíces con semillas pegadas al pelo. Al verte se para en seco y espera, sin moverse.'},
 'nhal_piedras_musgo': {'rasgacorteza': 'Detrás de las piedras, hacia el puente, se oye romperse una corteza. Un Rasgacorteza deja marcas nuevas en un árbol, muy arriba.',
   'rondamusgo': 'Sobre una piedra con musgo, un Rondamusgo se confunde con la piedra. Sólo se le nota cuando se rasca y le caen semillas.'},
 'nhal_helechos_bajos': {'rasgacorteza': 'Entre los helechos altos, lejos de la franja elevada, asoma el lomo de un Rasgacorteza. No se acerca hacia los golpes de madera que llegan de las casas.'},
 'nhal_umbral_velmora': {'rasgacorteza': 'Muy al fondo, detrás de las primeras casas, un Rasgacorteza asoma entre los troncos. La luz de las lámparas no llega hasta allí.'},
 'nhal_claro_silencio': {'rasgacorteza': 'Lejos del claro, donde los árboles se juntan, una forma grande se mueve despacio: un Rasgacorteza. Junto a la raíz sólo se oye caer alguna semilla.',
   'rondamusgo': 'Un Rondamusgo cruza el claro con prisa, se para junto a la raíz donde podrías sentarte y te mira. Después sigue buscando hongos.'},
 'nhal_ribera_relevo': {'rasgacorteza': 'Al otro lado del canal, un Rasgacorteza se apoya en un tronco grueso. Las ramas se doblan sobre el agua con su peso.'},
 'nhal_senda_recipiente': {'rasgacorteza': 'Lejos de la casa de Elin, más allá de la cesta remendada, los pájaros dejan de cantar. Entre los troncos, un Rasgacorteza levanta la cabeza y vuelve a quedarse quieto.'},
 'nhal_sendero_altura': {'rondamusgo': 'Un Rondamusgo baja la cuesta entre raíces con la boca llena de semillas. Al verte se mete en el descanso de raíces y espera a que pases.'},
}, {'rasgacorteza'}, {'rasgacorteza': 11, 'rondamusgo': 5})

# ───────────────────────── I · Secretos para descubrir ─────────────────────────
# Patrón: pista (examen condicionado, también sale al Observar) → acción que revela y escribe en el diario
# → tema nuevo con un personaje. Todo usa guardas existentes: requires_time, requires_visits,
# requires_species, requires_flags, forbids_flags, scope, journal. Sin objetos, sellos ni XP.
J = lambda o: json.dumps(o, ensure_ascii=False)
NEW = '(nuevo)'
def secret(grupo, archivo, tabla, id_, campo, cond, obj, why, code=False):
    p(grupo, archivo, tabla, id_, campo, cond, obj if isinstance(obj, str) else J(obj), why, requiere_codigo=code, defecto=NEW)

g = 'I1 · Secreto: los Espinajos de Lio (Valdren, cualquier especie)'
WHY_LIO = 'Lio ya existe en el canon (taza pequeña, cuentas de graneros, se entretiene ayudando). Un dibujo suyo repetido es un easter egg que el niño reconoce de un sitio a otro.'
secret(g, ED, 'rooms', 'valdren_fragua', 'examine.taza', 'Sólo de noche. El texto nocturno de la fragua ya menciona «una taza vacía espera en el banco»: ésa es la pista.',
  {'requires_time': ['noche'], 'text': 'Por dentro, alguien dibujó con tiza un Espinajo muy redondo, con más espinas que cuerpo. Debajo hay una L.'}, WHY_LIO)
secret(g, ED, 'rooms', 'valdren_fragua', 'actions[id=edran_secreto_lio_fragua]', 'Botón visible sólo de noche y sólo hasta encontrarlo.',
  {'id': 'edran_secreto_lio_fragua', 'label': 'Mirar de cerca el dibujo de la taza', 'requires_time': ['noche'], 'forbids_flags': ['edran_lio_dibujo_fragua'], 'set_flags': ['edran_lio_dibujo_fragua'], 'scope': 'player',
   'text': 'Acercas la taza a la línea roja del carbón. La tiza está más gruesa en las espinas, como si quien dibujaba hubiera tenido mucho tiempo. La L está hecha de un solo trazo.',
   'journal': 'Un Espinajo de tiza dentro de una taza de la fragua de Daro, firmado con una L.'}, WHY_LIO)
secret(g, ED, 'rooms', 'edran_cobertizo_campo', 'examine.banco', 'Desde la segunda visita (requires_visits min 2).',
  {'requires_visits': {'min': 2}, 'text': 'En la pata del banco hay otro dibujo pequeño: un Espinajo escondido detrás de una estaca pintada. Al lado, otra L.'}, WHY_LIO)
secret(g, ED, 'rooms', 'edran_cobertizo_campo', 'actions[id=edran_secreto_lio_banco]', 'Desde la segunda visita, hasta encontrarlo.',
  {'id': 'edran_secreto_lio_banco', 'label': 'Mirar el dibujo de la pata del banco', 'requires_visits': {'min': 2}, 'forbids_flags': ['edran_lio_dibujo_banco'], 'set_flags': ['edran_lio_dibujo_banco'], 'scope': 'player',
   'text': 'Te agachas. El Espinajo de la pata asoma por detrás de la estaca, igual que uno de verdad en los tallos. Quien lo hizo esperaba sentado justo aquí.',
   'journal': 'Otro Espinajo con una L, escondido en la pata del banco del cobertizo de las estacas.'}, WHY_LIO)
secret(g, ED, 'rooms', 'valdren_pozo', 'examine.brocal', 'De día (con luz para ver la raya).',
  {'requires_time': ['día'], 'text': 'En la piedra del brocal hay un Espinajo rayado con otra piedra, asomado al pozo como si quisiera beber. Éste no se borra con la lluvia. Al lado, una L.'}, WHY_LIO)
secret(g, ED, 'rooms', 'valdren_pozo', 'actions[id=edran_secreto_lio_pozo]', 'De día, hasta encontrarlo.',
  {'id': 'edran_secreto_lio_pozo', 'label': 'Seguir con el dedo el dibujo del brocal', 'requires_time': ['día'], 'forbids_flags': ['edran_lio_dibujo_pozo'], 'set_flags': ['edran_lio_dibujo_pozo'], 'scope': 'player',
   'text': 'La raya es vieja: el agua del cubo la ha suavizado. Este Espinajo es más pequeño y más torpe que los otros. Quien lo hizo dibujaba Espinajos desde hace mucho.',
   'journal': 'El Espinajo más antiguo de la L está rayado en el brocal del pozo.'}, WHY_LIO)
secret(g, ED, 'npcs', 'edran_elva', 'topics.dibujos', 'Hablar con Elva tras encontrar los tres dibujos.',
  {'requires_flags': ['edran_lio_dibujo_fragua', 'edran_lio_dibujo_banco', 'edran_lio_dibujo_pozo'],
   'text': '¿Has encontrado los Espinajos de Lio? Los dibuja cuando le toca esperar. El del pozo lo hizo de pequeño, el día que no le dejaban sacar agua solo. Si has visto los tres, ya sabes cuánto espera mi Lio. No se lo cuentes a Daro: cree que el de la taza se lo dibujó a él.',
   'journal': 'Elva te contó que los Espinajos con una L son de Lio, que los dibuja cuando espera.'},
  'Remate: quien firma, por qué, y una broma que invita a hablar con Daro.')
secret(g, ED, 'npcs', 'edran_daro', 'topics.dibujo', 'Hablar con Daro tras ver el dibujo de la taza.',
  {'requires_flags': ['edran_lio_dibujo_fragua'], 'text': '¿El de la taza? No la lavo. Me gusta ese bicho: tiene cara de estar esperando a que alguien le dé trabajo.'},
  'Pequeña recompensa inmediata por el primer hallazgo, antes de completar los tres.')

g = 'I2 · Secreto Felaryn: la repisa de las marcas (Hoshai)'
WHY_REP = 'Sólo un Felaryn puede saltar a la repisa (anatomía canónica: equilibrio y salto). Senku tiene algo propio; los demás reciben la pista y pueden preguntarle.'
secret(g, HO, 'rooms', 'hoshai_cuello_roca', 'examine.repisa', 'Para cualquier especie: pista.',
  'Muy arriba, en la pared del paso, hay una repisa estrecha. Desde abajo se ven rayas en la roca. Para llegar haría falta saltar como un Felaryn.', WHY_REP)
secret(g, HO, 'rooms', 'hoshai_cuello_roca', 'actions[id=hoshai_secreto_repisa]', 'Sólo personajes Felaryn (requires_species), una vez.',
  {'id': 'hoshai_secreto_repisa', 'label': 'Saltar a la repisa alta', 'requires_species': ['felaryn'], 'forbids_flags': ['hoshai_marca_repisa'], 'set_flags': ['hoshai_marca_repisa'], 'scope': 'player',
   'text': 'Tomas impulso en la piedra plana y alcanzas la repisa de un salto. Está llena de rayas de altura: cada una tiene al lado un nombre, una cola dibujada o las dos cosas. Son marcas de los niños de Khariel, de muchos años. Con una piedra haces la tuya, un poco más arriba de lo que esperabas.',
   'journal': 'Dejaste tu marca de altura en la repisa alta del paso entre paredes, entre las de los niños de Khariel.'}, WHY_REP)
secret(g, HO, 'npcs', 'hoshai_luma', 'topics.repisa', 'Hablar con Luma tras dejar la marca.',
  {'requires_flags': ['hoshai_marca_repisa'], 'text': '¿Subiste a la repisa del paso? Mi marca es la tercera por abajo, la de la cola torcida. No la mires mucho: entonces era muy pequeña y muy orgullosa.'},
  'Luma es Felaryn de Khariel: tiene sentido que su marca esté allí.')

g = 'I3 · Secreto Marevyn: la barquita del fondo (Lethra)'
WHY_BAR = 'Usa la habilidad acuática Marevyn (mirar bajo el agua, sin respirar en ella) y la historia de las hermanas Mira y Sola. Lo saca un Marevyn y lo ven todos.'
secret(g, LE, 'rooms', 'lethra_orilla_silente', 'examine.fondo', 'Sólo Marevyn. La descripción ya dice «no ves el fondo»: ésa es la pista para los demás.',
  {'requires_species': ['marevyn'], 'text': 'Acercas la cara al agua y tus ojos se acostumbran enseguida. En el fondo, entre el barro, hay una barquita de juguete con la vela rota. En el casco, rayado con cuidado: SOLA.'}, WHY_BAR)
secret(g, LE, 'rooms', 'lethra_orilla_silente', 'actions[id=lethra_secreto_barquita]', 'Sólo Marevyn, una vez para todo el mundo (scope world).',
  {'id': 'lethra_secreto_barquita', 'label': 'Sacar la barquita y dejarla en la raíz', 'requires_species': ['marevyn'], 'forbids_flags': ['lethra_barquita_rescatada'], 'set_flags': ['lethra_barquita_rescatada'], 'scope': 'world',
   'text': 'Metes el brazo hasta el codo, sin moverte del borde. La barquita sale llena de barro y agua. La vacías y la dejas en la raíz seca, con la vela hacia el sol.',
   'journal': 'Sacaste del canal una barquita de juguete con el nombre de Sola y la dejaste secando en la raíz.'}, WHY_BAR)
secret(g, LE, 'rooms', 'lethra_orilla_silente', 'states[+]', 'Para todos, después del rescate.',
  {'requires_flags': ['lethra_barquita_rescatada'], 'overrides': {'examine': {'raíces': 'En la raíz seca hay una barquita de juguete con la vela rota. Alguien la sacó del canal; en el casco pone SOLA.'}}},
  'El hallazgo de un hermano cambia el mundo del otro: buen motivo para hablar entre ellos.')
secret(g, LE, 'npcs', 'lethra_sola', 'topics.barquita', 'Hablar con Sola cuando la barquita está fuera (flag de mundo).',
  {'requires_flags': ['lethra_barquita_rescatada'], 'text': '¿Mi barquita? ¡La hundió Mira! Teníamos siete y ocho años. Dijo que quería ver si flotaba con piedras dentro. No flotaba.'},
  'Primera versión de la historia.')
secret(g, LE, 'npcs', 'lethra_mira', 'topics.barquita', 'Hablar con Mira cuando la barquita está fuera.',
  {'requires_flags': ['lethra_barquita_rescatada'], 'text': 'Eso no es verdad. La hundió ella sola y luego me echó la culpa. Pregúntale por qué le rayó su nombre tan grande: era para que nadie más pudiera jugar con ella.'},
  'Segunda versión, contradictoria a propósito. El niño decide a quién creer; ninguna mecánica depende de ello.')

g = 'I4 · Secreto: la figura de corteza viaja (Nhal)'
WHY_FIG = 'Tras sostener la figura para Desi (nhal_figura_firme, mundo), el sobrino la lleva de paseo. Un único objeto, en un sitio distinto según la hora, para no estar en tres lugares a la vez.'
for rid, key, time, ex, act_text in (
  ('nhal_rincon_semillas', 'figura', 'día',
   'Entre las semillas de verdad hay una figura de corteza con forma de Rondamusgo, con una pata atada con una tira. Alguien le ha puesto tres semillas delante, como si fuera a comer.',
   'Miras la figura sin moverla. Las tres semillas están colocadas en fila. Un poco más allá, entre las raíces, hay pelo áspero de un Rondamusgo de verdad. Parece que la han traído a conocerlo.'),
  ('nhal_claro_silencio', 'figura', 'atardecer',
   'Sobre la piedra del claro está la figura de corteza, mirando la abertura del cielo. Tiene al lado una hoja doblada, como una manta.',
   'La figura mira hacia arriba, donde la luz entra entre las hojas. Alguien la ha dejado aquí para que viera el atardecer. La hoja doblada está bien remetida por debajo.'),
  ('nhal_patio_relato', 'figura', 'noche',
   'Bajo el banco del relato asoma la figura de corteza, de cara a donde Leris lee. Como si escuchara.',
   'La dejas donde está. Desde aquí la figura oye entero el relato de Leris. Quien la puso eligió el mejor sitio del patio.')):
    flag = f'nhal_figura_vista_{rid.split("_")[-1]}'
    secret(g, NH, 'rooms', rid, f'examine.{key}', f'Tras nhal_figura_firme y sólo en fase {time}.',
      {'requires_flags': ['nhal_figura_firme'], 'requires_time': [time], 'text': ex}, WHY_FIG)
    secret(g, NH, 'rooms', rid, f'actions[id={flag}]', f'Tras nhal_figura_firme, en fase {time}, una vez.',
      {'id': flag, 'label': 'Mirar la figura de corteza', 'requires_flags': ['nhal_figura_firme'], 'requires_time': [time], 'forbids_flags': [flag], 'set_flags': [flag], 'scope': 'player',
       'text': act_text, 'journal': f'Viste la figura de corteza del sobrino de Desi: {ex[0].lower() + ex[1:60].rstrip()}…'}, WHY_FIG)
secret(g, NH, 'npcs', 'nhal_desi', 'topics.paseo', 'Hablar con Desi tras ver la figura en los tres sitios.',
  {'requires_flags': ['nhal_figura_vista_semillas', 'nhal_figura_vista_silencio', 'nhal_figura_vista_relato'],
   'text': '¿La has visto en el claro? ¿Y en el rincón de las semillas, y en el patio? Mi sobrino dice que la está llevando a conocer a los Rondamusgos de verdad. Todavía no ha conseguido que ninguno se quede quieto para saludarla.'},
  'Remate y guiño a la frase inicial de Desi («el de verdad tampoco quiso [quedarse quieto]»).')

g = 'I5 · Secreto: piedras para quien levantó el muro (Vaisgard)'
WHY_PIE = 'Respeta el canon: nadie sabe quién construyó lo antiguo. El secreto no lo resuelve; muestra una costumbre de la gente de hoy.'
secret(g, VE, 'rooms', 'veyra_patio_senales', 'examine.hueco', 'Desde la segunda visita. El examen «armazon» ya dice «cabe una mano»: es la pista.',
  {'requires_visits': {'min': 2}, 'text': 'Metes la mano entre el armazón y la pared antigua. Tocas piedrecitas lisas, muchas, de colores distintos. Alguien las ha ido dejando ahí, una a una.'}, WHY_PIE)
secret(g, VE, 'rooms', 'veyra_patio_senales', 'actions[id=veyra_secreto_piedra]', 'Desde la segunda visita, una vez por personaje.',
  {'id': 'veyra_secreto_piedra', 'label': 'Dejar una piedrecita en el hueco', 'requires_visits': {'min': 2}, 'forbids_flags': ['veyra_piedra_hueco'], 'set_flags': ['veyra_piedra_hueco'], 'scope': 'player',
   'text': 'Buscas en el suelo una piedra pequeña y lisa y la dejas con las demás, al fondo del hueco. Al sacar la mano notas que la pared antigua está fría, aunque el patio esté al sol.',
   'journal': 'Dejaste una piedrecita en el hueco de la pared antigua del patio de mensajes.'}, WHY_PIE)
secret(g, VE, 'npcs', 'veyra_arel', 'topics.hueco', 'Hablar con Arel tras dejar la piedra.',
  {'requires_flags': ['veyra_piedra_hueco'], 'text': '¿Tú también has dejado una? Lo hacemos desde pequeños. Nadie sabe quién levantó esa pared. Así que le dejamos algo, para que sepa que seguimos aquí.'},
  'Emoción sin respuesta inventada.')

g = 'I6 · Secreto de regreso: el dibujo que crece (Refugio de Lajas, Korven)'
WHY_DIB = 'Premia volver: el texto cambia con requires_visits, sin flags. La sala ya cuenta que dos viajeros dibujan «el último pino».'
secret(g, KO, 'rooms', 'korven_meseta_relevo', 'examine.dibujo', 'Primeras visitas.',
  'En el margen de una nota hay un pino dibujado, con la copa doblada por el viento.', WHY_DIB)
for n, txt in ((3, 'El pino del margen tiene ahora piñas. Y raíces, sujetando un poco de tierra. Lo ha dibujado más de una mano.'),
               (5, 'Alguien ha colgado un Uñapiedra de una rama del pino. Debajo, con otra letra, pone: «¿Quién dibuja esto?»'),
               (8, 'Debajo de la pregunta hay respuesta, con una letra nueva: «Todos.» El pino ya casi no cabe en el margen.')):
    secret(g, KO, 'rooms', 'korven_meseta_relevo', f'states[+] (visitas ≥ {n})', f'Desde la visita {n}; colocar después de los anteriores para que gane el último.',
      {'requires_visits': {'min': n}, 'overrides': {'examine': {'dibujo': txt}}}, WHY_DIB)
secret(g, KO, 'rooms', 'korven_meseta_relevo', 'actions[id=korven_secreto_dibujo]', 'Desde la visita 5, una vez por personaje.',
  {'id': 'korven_secreto_dibujo', 'label': 'Añadir algo al dibujo del pino', 'requires_visits': {'min': 5}, 'forbids_flags': ['korven_dibujo_aportado'], 'set_flags': ['korven_dibujo_aportado'], 'scope': 'player',
   'text': 'Buscas un hueco libre en el margen y dibujas algo pequeño junto al pino. Cuando vuelvas, quizá alguien le haya añadido algo a lo tuyo.',
   'journal': 'Añadiste tu propio dibujo al pino del margen, en el Refugio de Lajas.'},
  '«Quizá» no promete una mecánica: sólo invita a volver.')

g = 'I7 · Para que el niño sepa que hay más (requiere código)'
secret(g, 'client/app.js + server/engine.py', 'snapshot', 'journal', 'secretos',
  'Diario: una línea «Secretos encontrados: N» calculada con los flags de los secretos de este bloque. Sin total ni lista, para no estropear la sorpresa.',
  'Secretos encontrados: {n}. El mundo guarda más.',
  'Un contador es lo que hace que un niño vuelva a mirar de noche, en la lluvia o en la tercera visita. Sin él, los secretos sólo los encuentra quien ya busca. Necesita una lista de flags marcados como secreto y una línea en el snapshot.',
  code=True)

# ───────────────────────── salida ─────────────────────────
for e in E:
    try:
        actual = resolve(e['archivo'], e['tabla'], e['id'], e['campo'])
    except (ValueError, KeyError, OSError, IndexError, AttributeError):
        actual = None  # campos nuevos (states[+], claves renombradas) o destinos de código
    e['actual'] = actual if actual is not None else (e['defecto'] or '(no existe)')

keys = ('archivo', 'tabla', 'id', 'campo', 'condiciones', 'texto', 'requiere_codigo')
with open(os.path.join(HERE, 'propuestas.json'), 'w', encoding='utf-8') as f:
    json.dump([{k: e[k] for k in keys} for e in E], f, ensure_ascii=False, indent=1)
    f.write('\n')

out = ['# Textos propuestos — Vintage Telnet 2', '',
       'Generado por `generar.py` a partir de las mismas propuestas que `propuestas.json`. El «texto actual» se lee del contenido en el momento de generar.',
       'Bloques con **requiere código: sí** no se pueden integrar sólo como texto. El resto encaja en campos que el motor ya lee.', '']
group = None
for e in E:
    if e['grupo'] != group:
        group = e['grupo']; out += ['', f'## {group}', '']
    out += [f"### `{e['id']}` · `{e['campo']}`", '',
            f"- **Archivo:** `{e['archivo']}` → `{e['tabla']}`",
            f"- **Aparece:** {e['condiciones']}",
            f"- **Requiere código:** {'sí' if e['requiere_codigo'] else 'no'}", '',
            f"**Actual:** {e['actual']}", '', f"**Propuesto:** {e['texto']}", '',
            f"**Por qué:** {e['por_que']}", '']
with open(os.path.join(HERE, 'TEXTOS.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

# Comprobación mínima: cada campo existente se resolvió y ningún texto vacío.
assert all(e['texto'].strip() for e in E)
missing = [f"{e['id']}.{e['campo']}" for e in E if e['actual'] == '(no existe)' and not e['campo'].endswith(('dialogue', 'description'))]
print(len(E), 'propuestas;', 'campos nuevos:', missing)
