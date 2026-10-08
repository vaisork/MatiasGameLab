"""Genera renderer.patch (server/engine.py) y cliente.patch (client/ui-data.js) desde el código actual.

Uso, desde la raíz del proyecto: python3 docs/colaboracion/claude-narrativa/estandar_mud/hacer_parche.py
Si una cadena de anclaje ya no existe (Codex cambió el código), falla con el texto que no encuentra.
"""
import difflib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def edit(src, pairs):
    for old, new in pairs:
        assert src.count(old) == 1, f'anclaje no único o ausente: {old[:80]!r}'
        src = src.replace(old, new)
    return src

def write_patch(rel, pairs, out):
    before = (ROOT / rel).read_text(encoding='utf-8')
    after = edit(before, pairs)
    diff = difflib.unified_diff(before.splitlines(True), after.splitlines(True), f'a/{rel}', f'b/{rel}')
    (HERE / out).write_text(''.join(diff), encoding='utf-8')

ENGINE = [
 # 1. Un estado de la sala puede cambiar también su seña breve.
 ("if key not in ('description','dawn','day','dusk','night','rain','clear','weather','return','examine','focus'):continue",
  "if key not in ('description','brief','dawn','day','dusk','night','rain','clear','weather','return','examine','focus'):continue"),
 # 2. «Llegada» sólo tras moverse. Se limpia después de validar: una acción rechazada no cambia nada.
 ("""        if not candidate or candidate.get('disabled'):raise RuleError((candidate or {}).get('reason') or 'Esa acción no está disponible en tu situación actual.',409)
        state['events']=[]""",
  """        if not candidate or candidate.get('disabled'):raise RuleError((candidate or {}).get('reason') or 'Esa acción no está disponible en tu situación actual.',409)
        state['events']=[];state['arrival']=False"""),
 # 3. Quién está aquí queda fuera del presupuesto de capas.
 ("""        for npc in self.people(room,state,world,ambient):
            activity=npc.get(phase_key) or npc.get('night' if phase_key=='night' else 'day')
            if activity:layers['people']=event('world',activity);break""",
  """        present=self.people(room,state,world,ambient);people_line=None
        for npc in present:
            activity=npc.get(phase_key) or npc.get('night' if phase_key=='night' else 'day')
            if activity:people_line=event('world',activity);break"""),
 # 4. Modo breve al volver caminando: seña + una sola capa que rota con las visitas (el peligro siempre gana).
 ("""        lines=[event('world',room['description'])];seen={room['description']}""",
  """        brief=room.get('brief') if state.get('arrival') and visits>1 else None
        if brief:
            # Al volver: la seña del lugar y hasta tres capas vivas. El orden rota con las visitas para que
            # cada regreso abra con un detalle distinto; el peligro siempre va primero.
            lines=[event('world',brief)];options=[]
            for key in priority:
                if key in layers and key!='danger' and key not in options:options.append(key)
            if options:shift=visits%len(options);options=options[shift:]+options[:shift]
            chosen=(['danger'] if 'danger' in layers else [])+options
            for key in chosen[:3]:
                if layers[key]['text'] not in [line['text'] for line in lines]:lines.append(layers[key])
            # Un recuerdo puede nombrar a alguien sin que esté; sólo una capa del presente lo hace innecesario.
            names=[npc['name'] for npc in present]
            if names and not any(key in ('activity','weather','arrival') and any(name in layers[key]['text'] for name in names) for key in chosen[:3]):
                lines.append(event('world',' y '.join(names)+(' está aquí.' if len(names)==1 else ' están aquí.')))
            return lines
        lines=[event('world',room['description'])];seen={room['description']}"""),
 ("""            if len(lines)>=limit:break
        return lines""",
  """            if len(lines)>=limit:break
        if people_line and people_line['text'] not in seen and not any(npc['name'] in line['text'] for npc in present for line in lines):lines.append(people_line)
        return lines"""),
]

CLIENT = [
 # Línea de salidas al llegar, construida con las acciones de movimiento que ya envía el servidor (sin revelar destinos).
 ("""additions.push(...scene);}""",
  """additions.push(...scene);const exits=list(snapshot.actions).filter(a=>a.id==='mover'&&a.target!=='hogar').map(a=>{const name=String(a.label||'').split(' · ')[1];return name&&name!=='Salida por explorar'?`${a.target} (${name})`:a.target;});if(exits.length)additions.push({kind:'INFO',text:'Salidas: '+exits.join(', ')+'.'});}"""),
]

PROSE = r"""
# Narración de combate: sólo cambia el texto. Daño, precisión y azar no se tocan;
# la variante sale del número de ronda y la intensidad, del daño ya calculado.
WEAPON_PROSE = {
 'espada_juramento': {
  'hit': ['Tajo amplio con la espada', 'La hoja silba en el aire', 'Paras y devuelves el golpe', 'Descargas la espada con las dos manos'],
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
                     'miss': ['{n} lanza el palo, pero lo esquivas por poco.', 'El palo de {n} silba junto a tu oreja sin tocarte.']},
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
"""

COMBAT = [
 ("""def resolve_round(state, creature, rng, respond=True):""", PROSE.strip('\n') + """\n\ndef resolve_round(state, creature, rng, respond=True):"""),
 ("""   damage=max(1,rounded(raw*power*(1-profile['reduction'])));combat['hp']-=damage
   events.append({'kind':'combat','text':f"Tu golpe alcanza a {creature['name']}: {damage} de daño."})""",
  """   damage=max(1,rounded(raw*power*(1-profile['reduction'])));combat['hp']-=damage
   events.append({'kind':'combat','text':weapon_prose(weapon,'final' if combat['hp']<=0 else 'hit',creature['name'],damage,combat['round'],profile['hp'])})"""),
 ("""  else:events.append({'kind':'combat','text':'Tu ataque no encuentra un ángulo limpio.'})""",
  """  else:events.append({'kind':'combat','text':weapon_prose(weapon,'miss',creature['name'],0,combat['round'])})"""),
 ("""\n if action=='esquivar':enemy_accuracy-=""",
  """\n if action in DEFENSE_PROSE:events.append({'kind':'action','text':defense_prose(action,creature['name'],combat['round'])})
 if action=='esquivar':enemy_accuracy-="""),
 ("""  events.append({'kind':'combat','text':f"{creature['name']} te alcanza: {damage} de daño."})""",
  """  events.append({'kind':'combat','text':creature_prose(creature,'hit',damage,combat['round'])})"""),
 ("""  events.append({'kind':'combat','text':f"La respuesta de {creature['name']} pasa sin alcanzarte."})""",
  """  events.append({'kind':'combat','text':creature_prose(creature,'miss',0,combat['round'])})"""),
]

# Combate compartido: la respuesta enemiga se narra en engine.tick_shared.
COMBAT_ENGINE = [
 ("""state['events'].append(event('combat',f"{creature['name']} te alcanza: {damage} de daño."))""",
  """state['events'].append(event('combat',m.creature_prose(creature,'hit',damage,combat['round'])))"""),
 ("""                state['events'].append(event('combat',f"La respuesta de {creature['name']} pasa sin alcanzarte."))""",
  """                state['events'].append(event('combat',m.creature_prose(creature,'miss',0,combat['round'])))"""),
]

if __name__ == '__main__':
    write_patch('server/mechanics.py', COMBAT, 'combate.patch')
    write_patch('server/engine.py', COMBAT_ENGINE, 'combate_motor.patch')
    write_patch('server/engine.py', ENGINE, 'renderer.patch')
    write_patch('client/ui-data.js', CLIENT, 'cliente.patch')
    print('renderer.patch y cliente.patch regenerados')
