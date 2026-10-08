"""Document-sourced rules: GAMEPLAY §§20,22,24,27,36,42,43; WEAPON_CATALOG.
All values transcribed from documents, not imported from the former engine.
"""
import math

ATTRIBUTES = ('fuerza','resistencia','agilidad','percepcion','intelecto','voluntad','destreza','presencia')
CLASSES = {
 'juramentado': {'name':'Juramentado','signature':'Guardia Comprometida','effect':'Reduce el daño del próximo golpe que te alcance.','cooldown':2,'weapon':'espada_juramento'},
 'arcano': {'name':'Arcano','signature':'Impulso Arcano','effect':'Rompe la preparación y dificulta que te alcance.','cooldown':4,'weapon':'varita_aprendiz'},
 'sombra': {'name':'Sombra','signature':'Borrar el Foco','effect':'Reduce su precisión; si falla, abre tu siguiente ataque.','cooldown':4,'weapon':'punal_camino'},
 'artifice': {'name':'Artífice','signature':'Tiro de Interrupción','effect':'Un disparo acertado corta la carga o reduce su precisión.','cooldown':2,'weapon':'arco_ruta'},
}
WEAPONS = {
 'espada_juramento': {'id':'espada_juramento','name':'Espada de juramento','kind':'weapon','damage':10,'block':True,'activated':True},
 'varita_aprendiz': {'id':'varita_aprendiz','name':'Varita de aprendiz','kind':'weapon','damage':7,'focus':True,'activated':True},
 'punal_camino': {'id':'punal_camino','name':'Puñal de camino','kind':'weapon','damage':8,'activated':True},
 'arco_ruta': {'id':'arco_ruta','name':'Arco de ruta','kind':'weapon','damage':9,'ranged':True,'activated':True},
}
PROFILES = {
 'mordelinde': {'hp':28,'accuracy':45,'damage':5,'reduction':0,'evasion':15,'level':1,'category':'comparable','family':'mordelinde'},
 'espinajo_rastrojo': {'hp':40,'accuracy':50,'damage':8,'reduction':.10,'level':2,'category':'comparable','prepared':True,'prepared_action':{'id':'embestida_territorial','name':'Embestida territorial','accuracy':60,'interruptible':True,'frontal':True},'family':'espinajo'},
 'cornalomo': {'hp':120,'accuracy':65,'damage':20,'reduction':.20,'level':8,'category':'abrumador','family':'cornalomo'},
}

# Regional fauna reuse the established threat tiers; no new numeric combat scale.
for creature_id in ('dorsalodo','rasgacumbres','quebrarrocas','rasgacorteza'):
 PROFILES[creature_id]=dict(PROFILES['cornalomo'],family=creature_id)
# GAMEPLAY §§36.3,40.7: regional intentions use the same intervention contract.
# The physical tactics are authored extensions; all established numeric tiers stay intact.
REGIONAL_INTENTIONS = {
 'rasgacumbres': {'id':'zarpazo_lateral','name':'Zarpazo lateral','interruptible':True,'frontal':False,'tell':'El Rasgacumbres desplaza el peso hacia una pata delantera y prepara un zarpazo lateral. Puedes interrumpirlo, esquivar o huir; una guardia frontal no cubre ese ángulo.'},
 'quebrarrocas': {'id':'empuje_anclado','name':'Empuje anclado','interruptible':False,'frontal':True,'tell':'El Quebrarrocas afirma el cuerpo contra los bloques y prepara un empuje frontal. El impulso ya está anclado: puedes cubrirte, esquivar o huir, pero no interrumpirlo.'},
 'dorsalodo': {'id':'barrido_pesado','name':'Barrido pesado','interruptible':False,'frontal':False,'tell':'El Dorsalodo extiende el cuerpo entre los juncos para barrer de lado. Su peso ya domina el paso: la guardia frontal y la interrupción no sirven; todavía puedes esquivar o huir.'},
 'rasgacorteza': {'id':'golpe_desde_tronco','name':'Golpe desde el tronco','interruptible':True,'frontal':True,'tell':'El Rasgacorteza separa las patas del tronco y reúne fuerza para un golpe frontal. Puedes interrumpir esa preparación, cubrirte, esquivar o huir.'},
}
for creature_id,intention in REGIONAL_INTENTIONS.items():
 PROFILES[creature_id].update(prepared=True,prepared_action=dict(intention,accuracy=PROFILES[creature_id]['accuracy']))

PROFILES['cascapedernal']=dict(PROFILES['mordelinde'],family='cascapedernal')
PROFILES['forajido_camino']=dict(PROFILES['mordelinde'],family='forajidos')

# Observable tactics enrich existing tiers without inventing another combat scale.
THREAT_OBSERVATIONS = {
 'mordelinde': 'Busca un hueco por donde escapar. Mantener libre su salida evita arrinconarlo.',
 'espinajo_rastrojo': 'Afirma las patas antes de una embestida frontal. Puedes interrumpir esa preparación o protegerte del golpe.',
 'cascapedernal': 'Sus placas forman una cubierta baja junto a la roca. No prepara una carga: conserva distancia si prefieres evitar el contacto.',
 'cornalomo': 'Afirma el peso dentro de su territorio. Apartarte antes del contacto conserva la distancia segura.',
 'dorsalodo': 'El movimiento del agua revela cuánto espacio ocupa entre los juncos. Dejar libre ese paso permite retroceder.',
 'rasgacorteza': 'Las ramas dobladas muestran su alcance junto al tronco. Puedes salir de ese espacio antes del contacto.',
 'rasgacumbres': 'Ocupa el paso alto. Conviene conservar espacio para retroceder antes del contacto.',
 'quebrarrocas': 'Su peso domina el terreno de piedra. Mantener distancia evita entrar en su alcance.',
 'forajido_camino': 'Bloquea el camino y vigila tu acercamiento. Comprueba los desvíos antes de decidir un enfrentamiento.',
}
PEACEFUL_WITHDRAWALS = {
 'cornalomo': 'Retrocedes fuera del herbazal que ocupa. El Cornalomo deja de orientarse hacia ti y conserva su territorio.',
 'dorsalodo': 'Dejas libre el paso entre los juncos. El Dorsalodo vuelve hacia el agua mientras recuperas distancia.',
 'rasgacorteza': 'Te apartas del tronco y de las ramas dobladas. El Rasgacorteza permanece junto a la corteza.',
 'rasgacumbres': 'Retrocedes por el paso alto sin acercarte más. El Rasgacumbres permanece en su territorio.',
 'quebrarrocas': 'Te apartas del terreno que ocupa. El Quebrarrocas conserva su espacio entre las piedras.',
}

def threat_observation(creature_id):
 text=THREAT_OBSERVATIONS.get(creature_id,'Conserva una salida antes de entrar en su alcance.')
 intention=REGIONAL_INTENTIONS.get(creature_id)
 return text+(' '+intention['tell'] if intention else '')

def peaceful_withdrawal(creature_id):
 return PEACEFUL_WITHDRAWALS.get(creature_id,'Te apartas antes del contacto. La criatura no te persigue.')

def clamp(value, low, high): return max(low,min(high,value))
def rounded(value): return math.floor(value+.5)
def cg(state): return 8*(state['level']-1)/99
def hp_max(state):
 a=state['attributes']; return 100+1.25*(state['level']-1)+2.5*(a['resistencia']-10)+.5*(a['voluntad']-10)
def xp_next(level): return rounded(100+18*(level-1)+.25*(level-1)**2)
def fatigue_cost(state, base):
 multiplier = (1.10 if state['wound']=='leve' else 1.20 if state['wound']=='moderada' else 1.35 if state['wound']=='grave' else 1)
 return base*max(.55,1-.007*(state['attributes']['resistencia']-10))*multiplier

def penalties(state):
 f=state['fatigue']; accuracy=10 if f>=90 else 5 if f>=70 else 0
 accuracy+=10 if state['wound']=='grave' else 5 if state['wound']=='moderada' else 0
 power=(.8 if f>=90 else .9 if f>=70 else 1)*(.9 if state['wound']=='grave' else 1)
 return accuracy,power

def new_state(species,class_id,home,now):
 weapon=dict(WEAPONS[CLASSES[class_id]['weapon']],quantity=1)
 return {'species':species,'class_id':class_id,'location':home,'home':home,'level':1,'xp':0,'pa':0,'pp':0,'attributes':dict.fromkeys(ATTRIBUTES,10),
 'hp':100,'fatigue':0,'wound':None,'seals':20,'inventory':[weapon],'equipment':{'weapon':weapon['id'],'armor':None,'block':None},
 'flags':[],'visited':[home],'known':[home],'routes':[],'bestiary':{},'journal':[],'visits':{home:1},'last_room':None,
 'combat':None,'victories':[],'rest_budget':None,'quests':{},'ledger':[],'last_active':now,'events':[], 'arrival':True}


def rest(state):
 missing=hp_max(state)-state['hp']
 if missing>0 and state['rest_budget'] is None: state['rest_budget']=.3*missing
 cap=(.65 if state['wound']=='grave' else .85 if state['wound']=='moderada' else 1)*hp_max(state)
 healed=max(0,min(.1*hp_max(state),state['rest_budget'] or 0,cap-state['hp'],missing))
 state['hp']+=healed
 if state['rest_budget'] is not None: state['rest_budget']-=healed
 state['fatigue']=max(0,state['fatigue']-(25+.2*(state['attributes']['resistencia']-10)))
 return healed


def wound(state,damage):
 ratio=damage/hp_max(state)
 new='grave' if ratio>=.5 else 'moderada' if ratio>=.35 else 'leve' if ratio>=.2 else None
 order={None:0,'leve':1,'moderada':2,'grave':3}
 if order[new]>order[state['wound']]:state['wound']=new


def preparation(combat):
 if not combat.get('prepared'):return None
 return combat['profile'].get('prepared_action',{'name':'Acción preparada','accuracy':60,'interruptible':True,'frontal':True})

def capability_hint(class_id, prepared=None):
 if class_id=='artifice' and prepared:
  if not prepared.get('interruptible',False):return f"{prepared['name']} no puede interrumpirse. El disparo sólo hará daño si acierta; puedes elegir una defensa o huir."
  return f"Si aciertas, interrumpes {prepared['name']}. El rival aún puede responder con su precisión ordinaria."
 if class_id=='arcano' and not prepared:return 'Reduce la precisión de la respuesta ordinaria durante esta ronda.'
 return CLASSES[class_id]['effect']

# Narración de combate: sólo cambia el texto. Daño, precisión y azar no se tocan;
# la variante sale del número de ronda y la intensidad, del daño ya calculado.
WEAPON_PROSE = {
 'espada_juramento': {
  'hit': ['Tajo amplio con la espada', 'La hoja silba en el aire', 'Adelantas la hoja y diriges el golpe', 'Descargas la espada con las dos manos'],
  'miss': ['Tu tajo corta el aire.', 'La espada muerde el suelo; {c} ya no estaba ahí.', 'Estocada: {c} gira y la hoja pasa rozando.'],
  'final': ['Último tajo, firme y limpio. {c} ya no puede seguir: {d} de daño.']},
 'punal_camino': {
  'hit': ['Entras rápido por debajo', 'Amago a un lado, pinchazo al otro', 'Te pegas a su costado con el puñal', 'Golpe corto y seco'],
  'miss': ['El puñal sólo encuentra aire.', '{c} no se cree el amago.', '{c} es más rápido esta vez.'],
  'final': ['Te deslizas a su lado y el puñal decide: {d} de daño a {c}.']},
 'arco_ruta': {
  'hit': ['Tensas, sueltas: la flecha silba', 'Retrocedes un paso y disparas', 'Esperas... ¡ahora! Sueltas la cuerda', 'Disparo rápido, casi sin apuntar'],
  'miss': ['La flecha pasa silbando junto a {c}.', 'Disparas con prisa: la flecha se queda corta.', '{c} se mueve justo al soltar la cuerda.'],
  'final': ['Última flecha, bien apuntada. {c} deja de pelear: {d} de daño.']},
 'varita_aprendiz': {
  'hit': ['Cosquilleo en los dedos: el impulso sale', 'Un círculo en el aire, y el aire empuja', 'Sueltas el impulso de golpe', 'La varita vibra y empuja'],
  'miss': ['El impulso sale torcido y sólo mueve hojas.', 'Pierdes la concentración: un chasquido y nada.', 'El impulso pasa junto a {c}, que ni se inmuta.'],
  'final': ['Toda tu concentración en la punta de la varita: {c} se queda sin fuerzas. {d} de daño.']},
}
# Si un arma nueva no está en la tabla, se elige por sus propiedades.
WEAPON_PROSE_FALLBACK = (('ranged', 'arco_ruta'), ('focus', 'varita_aprendiz'), ('block', 'espada_juramento'))
# Intensidad del acierto según la parte de la vida máxima del rival que quita (como los mensajes de daño clásicos).
HIT_TIERS = ((.10, '. Apenas rozas a {c}: {d} de daño.'), (.20, '. Alcanzas a {c}: {d} de daño.'),
             (.30, '. ¡Das de lleno a {c}! {d} de daño.'), (None, '. ¡Golpe tremendo! {c} se tambalea: {d} de daño.'))
DEFENSE_PROSE = {
 'esquivar': ['Te mueves de lado, ligero.', 'Rodillas dobladas, listo para saltar.', 'Un paso atrás y otro al lado.'],
 'bloquear': ['Te cubres con los brazos firmes.', 'Pones el arma delante del cuerpo.', 'Pies firmes: esperas el choque.'],
 'resistir': ['Aprietas los dientes y te plantas.', 'Bajas el cuerpo, tenso.', 'Respiras hondo y aguantas.'],
}
# Ataque propio de cada rival. {n} es el nombre mostrado (incluye nombres locales como Seran).
CREATURE_PROSE = {
 'mordelinde': {'hit': ['{n} se lanza a tus tobillos y te muerde antes de retroceder', '{n} te araña con las manos delanteras y vuelve a mirar su hueco', '{n} se escurre por un lado y te muerde la mano'],
                'miss': ['{n} amaga hacia tus pies, pero sólo muerde el aire.', '{n} da un salto corto y se queda a medio camino, mirando su salida.']},
 'espinajo_rastrojo': {'hit': ['{n} embiste agachado y sus espinas te pinchan las piernas', '{n} gira de golpe y te golpea con el lomo erizado', '{n} carga desde los tallos con las espinas por delante'],
                       'miss': ['{n} carga, pero te apartas y pasa de largo entre los tallos.', 'Las espinas de {n} se quedan a un palmo de ti.']},
 'cornalomo': {'hit': ['{n} baja la cabeza y te empuja con el cuerno; sales despedido hacia atrás', '{n} pisa fuerte y te alcanza con el costado, como chocar contra un muro', '{n} da un cabezazo que te deja sin aire'],
               'miss': ['{n} embiste, pero sólo levanta tierra donde estabas.', 'El cuerno de {n} pasa rozándote el hombro.']},
 'dorsalodo': {'hit': ['{n} barre los juncos con el cuerpo y te tira al suelo con el agua', 'La espalda rugosa de {n} te golpea de lado', '{n} sale del agua de golpe y te empuja hacia la orilla'],
               'miss': ['{n} levanta una ola de barro, pero no llega a tocarte.', 'El cuerpo de {n} pasa a tu lado y el agua te salpica hasta las rodillas.']},
 'rasgacumbres': {'hit': ['{n} lanza un zarpazo de lado y sus garras te alcanzan', '{n} salta desde la roca y te derriba con las patas', 'Las garras de {n} te raspan el brazo antes de que puedas apartarlo'],
                  'miss': ['Las garras de {n} arañan la piedra donde estabas hace un momento.', '{n} salta, pero calcula mal y cae a un paso de ti.']},
 'quebrarrocas': {'hit': ['{n} te empuja con todo su peso, como una pared que se mueve', '{n} lanza una piedra con el hombro y te golpea', '{n} avanza y te arrincona contra las rocas'],
                  'miss': ['{n} empuja, pero te apartas y sólo mueve un bloque.', 'Una piedra lanzada por {n} rebota a tu lado.']},
 'rasgacorteza': {'hit': ['{n} se separa del tronco y te golpea con un brazo duro como la madera', 'Las ramas crujen y {n} te alcanza desde arriba', '{n} te empuja contra un tronco'],
                  'miss': ['{n} golpea el tronco en vez de a ti, y caen hojas por todas partes.', 'El golpe de {n} pasa por encima de tu cabeza.']},
 'cascapedernal': {'hit': ['{n} se lanza de lado y su caparazón te golpea la pierna', 'El borde del caparazón de {n} te da un golpe seco en la mano', '{n} choca contra tu bota con un ruido de piedra'],
                   'miss': ['{n} golpea la roca con el caparazón, lejos de ti.', '{n} se lanza, pero se queda corto y se recoge.']},
 'forajido_camino': {'hit': ['{n} te da un golpe con el palo en el hombro', '{n} barre con el palo a la altura de las piernas y te alcanza', '{n} amaga arriba y golpea abajo con el palo'],
                     'miss': ['{n} descarga un golpe con el palo, pero lo esquivas por poco.', 'El palo de {n} silba junto a tu oreja sin tocarte.']},
}

def weapon_prose(weapon, kind, creature_name, damage, combat_round, max_hp=1):
    key = str(weapon.get('catalog_id', weapon.get('id', ''))).split(':')[0]
    if key not in WEAPON_PROSE:
        key = next((wid for flag, wid in WEAPON_PROSE_FALLBACK if weapon.get(flag)), 'punal_camino')
    options = WEAPON_PROSE[key][kind]
    text = options[combat_round % len(options)]
    if kind == 'hit':
        share = damage / max(1, max_hp)
        text += next(tail for limit, tail in HIT_TIERS if limit is None or share < limit)
    return text.format(c=creature_name, d=damage)

def defense_prose(action, creature_name, combat_round):
    options = DEFENSE_PROSE[action]
    return options[combat_round % len(options)].format(c=creature_name)

def creature_prose(creature, kind, damage, combat_round):
    options = CREATURE_PROSE.get(creature.get('id'), {}).get(kind)
    if not options:
        return f"{creature['name']} te alcanza: {damage} de daño." if kind == 'hit' else f"La respuesta de {creature['name']} pasa sin alcanzarte."
    text = options[combat_round % len(options)].format(n=creature['name'])
    return text + f": {damage} de daño." if kind == 'hit' else text

def resolve_round(state, creature, rng, respond=True):
 combat=state['combat']; profile=combat['profile']; intervention=combat.pop('intervention',None) or {'id':'atacar'}
 action=intervention['id']; target=intervention.get('target'); a=state['attributes']; penalty,power=penalties(state)
 weapon=next((i for i in state['inventory'] if i['id']==state['equipment']['weapon']),None)
 accuracy=clamp(55+.45*(a['destreza']-10)+.18*(a['percepcion']-10)+.5*(cg(state)-8*(profile['level']-1)/99)-penalty-profile.get('evasion',0),25,90)
 raw=(weapon['damage'] if weapon else 0)+.48*(a['fuerza']-10)+.12*(a['destreza']-10)+.25*cg(state)
 prepared=preparation(combat)
 enemy_accuracy=prepared.get('accuracy',60) if prepared else profile['accuracy']
 reduction=0; guard=0; events=[]; signature=False; costs={'atacar':4,'esquivar':6,'bloquear':5,'resistir':3,'huir':8,'capacidad':5}
 if action=='defender':action=target
 if action=='huir':
  chance=clamp(50+.45*(a['agilidad']-10)+.15*(a['percepcion']-10)+min(30,.6*max(0,profile['level']-state['level']))+15*combat.get('failed_flee',0)-penalty,20,95)
  if rng.random()*100<chance:
   state['fatigue']=min(100,state['fatigue']+fatigue_cost(state,8));state['combat']=None
   return [{'kind':'action','text':'Te apartas del alcance de tu rival y recuperas distancia.'}], 'fled'
  combat['failed_flee']=combat.get('failed_flee',0)+1;events.append({'kind':'danger','text':'Tu rival corta tu retirada; ahora reconoces mejor su ritmo.'})
 if action=='capacidad':
  signature=True;cls=state['_class'];combat['cooldown']=CLASSES[cls]['cooldown']+1
  if cls=='juramentado' and (not prepared or prepared.get('frontal',False)):guard=min(.45,.30+.0025*(a['destreza']-10)+.0015*(a['resistencia']-10));enemy_accuracy=min(enemy_accuracy,profile['accuracy'])
  elif cls=='arcano':
   if prepared and prepared.get('interruptible',False):enemy_accuracy=profile['accuracy']-10;combat['prepared']=False
   elif not prepared:enemy_accuracy=profile['accuracy']-20
  elif cls=='sombra':enemy_accuracy-=25
  elif cls=='artifice':raw*=.75
  effects={'juramentado':('Afirmas la guardia. Si el golpe llega, recibes menos daño.' if not prepared or prepared.get('frontal',False) else 'El ataque viene de lado: tu guardia frontal no reduce este golpe.'),
           'arcano':('Rompes su preparación y reduces la precisión de su respuesta.' if prepared and prepared.get('interruptible',False) else 'Desvías su respuesta con un impulso. Pierde precisión en esta ronda.'),
           'sombra':'Sales de su foco. Su siguiente respuesta pierde precisión; si falla, tendrás una apertura para atacar.',
           'artifice':(f"Disparas hacia {prepared['name']}. "+('El impacto decidirá si consigues interrumpirlo.' if prepared.get('interruptible',False) else 'No puedes interrumpirlo; el impacto sólo dañará a tu rival.') if prepared else 'Disparas para desviar su respuesta. Necesitas acertar para reducir su precisión.')}
  if cls=='arcano' and prepared and not prepared.get('interruptible',False):effects[cls]='Esta preparación no puede ser interrumpida; mantiene su respuesta.'
  events.append({'kind':'action','text':f"Usas {CLASSES[cls]['signature']}. {effects[cls]}"})
 attack=action=='atacar' or (signature and state['_class']=='artifice')
 if attack and not weapon:
  attack=False;events.append({'kind':'action','text':'Sin un arma activa no puedes ejecutar el ataque físico de tu formación.'})
 if attack:
  if combat.pop('opening',False):accuracy=min(90,accuracy+15)
  if rng.random()*100<accuracy:
   damage=max(1,rounded(raw*power*(1-profile['reduction'])));combat['hp']-=damage
   events.append({'kind':'combat','text':weapon_prose(weapon,'final' if combat['hp']<=0 else 'hit',creature['name'],damage,combat['round'],profile['hp'])})
   if signature and state['_class']=='artifice':
    if prepared and prepared.get('interruptible',False):
     combat['prepared']=False;enemy_accuracy=profile['accuracy'];events.append({'kind':'combat','text':f"Tu disparo interrumpe {prepared['name']}."})
    elif not prepared:
     enemy_accuracy-=15;events.append({'kind':'combat','text':'El disparo le hace perder precisión en su siguiente respuesta.'})
  else:events.append({'kind':'combat','text':weapon_prose(weapon,'miss',creature['name'],0,combat['round'])})
 state['fatigue']=min(100,state['fatigue']+fatigue_cost(state,costs.get(action,4)))
 if combat['hp']<=0:return events,'victory'
 if action in DEFENSE_PROSE:events.append({'kind':'action','text':defense_prose(action,creature['name'],combat['round'])})
 if action=='esquivar':enemy_accuracy-=.48*(a['agilidad']-10)+.12*(a['percepcion']-10)-penalty
 elif action=='bloquear':reduction=max(0,min(.32,.10+.0035*(a['destreza']-10))-penalty/100)
 elif action=='resistir':reduction=max(0,min(.38,.0055*(a['resistencia']-10))-penalty/100)
 combat['_response']={'accuracy':enemy_accuracy,'reduction':reduction,'guard':guard,'signature':signature}
 if not respond:
  combat['round']+=1;combat['cooldown']=max(0,combat.get('cooldown',0)-1)
  return events,'ongoing'
 connected=rng.random()*100<clamp(enemy_accuracy,20,90)
 if connected:
  damage=max(1,rounded(profile['damage']*(1-reduction)*(1-state.get('armor_reduction',0))*(1-guard)));state['hp']-=damage;wound(state,damage)
  events.append({'kind':'combat','text':creature_prose(creature,'hit',damage,combat['round'])})
 else:
  events.append({'kind':'combat','text':creature_prose(creature,'miss',0,combat['round'])})
  if signature and state['_class']=='sombra':combat['opening']=True
 combat['prepared']=False;combat['round']+=1;combat['cooldown']=max(0,combat.get('cooldown',0)-1)
 return events,'death' if state['hp']<=0 else 'ongoing'
