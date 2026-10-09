"""Simulación del ciclo MUD: viaje real con búsquedas y peleas; cuenta peleas, botín, sellos y compras posibles.

Uso, desde vintage-telnet-2:  PYTHONPATH=. python3 review/claude-evaluacion/simular_viaje.py [semilla]
"""
import random, sys, collections
from pathlib import Path
from server.content import Content
from server.engine import Engine, RuleError
from server import mechanics as m

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
content = Content(Path('content')); now = [10 * 3600.0]; rng = random.Random(seed)
engine = Engine(content, lambda: now[0], rng)
world = {'flags': [], 'deaths': {}, 'version': 0}
state = m.new_state('humano', 'juramentado', 'home:sim', now[0]); state['location'] = 'valdren_plaza'
char = {'id': 1, 'name': 'Sim', 'species': 'humano', 'class_id': 'juramentado', 'status': 'approved', 'state': state}
stats = collections.Counter(); loot = collections.Counter()

def act(intent):
    state['events'] = []
    try: engine.apply(char, world, intent)
    except RuleError: stats['acciones rechazadas'] += 1
    now[0] += 6
    return state['events']

def fight(target):
    act({'id': 'combatir', 'target': target}); stats['peleas'] += 1
    while state['combat']:
        hurt = state['hp'] < .35 * m.hp_max(state)
        potion = next((i for i in state['inventory'] if i.get('effect') == 'potion' and i.get('heal')), None)
        act({'id': 'usar', 'target': potion['id']} if hurt and potion else {'id': 'atacar'})
        now[0] += 5; engine.tick(char, world)
    if state['hp'] <= 0: stats['derrotas'] += 1
    state['hp'] = m.hp_max(state); state['wound'] = None; state['fatigue'] = 0  # descansa tras cada pelea
    if any('Vences' in e['text'] for e in state['events']): stats['victorias'] += 1

def visit_room():
    for a in engine.actions(char, world):
        if a['id'] == 'buscar' and not a.get('disabled'):
            before = {i['id']: i.get('quantity', 1) for i in state['inventory']}
            act({'id': 'buscar'}); stats['búsquedas'] += 1
            for i in state['inventory']:
                if i.get('quantity', 1) > before.get(i['id'], 0): loot[i['name']] += 1; stats['hallazgos'] += 1
    for a in engine.actions(char, world):
        if a['id'] == 'combatir' and m.PROFILES[a['target']]['category'] == 'comparable' and state['hp'] > .5 * m.hp_max(state):
            seals = state['seals']; before = {i['id']: i.get('quantity', 1) for i in state['inventory']}
            fight(a['target']); stats['sellos de combate'] += state['seals'] - seals
            for i in state['inventory']:
                if i.get('quantity', 1) > before.get(i['id'], 0): loot[i['name']] += 1
            stats['nivel máximo rival'] = max(stats['nivel máximo rival'], int(a['label'].split('nivel ')[-1]) if 'nivel' in a['label'] else 1)

def goto(target):
    prev = {state['location']: None}; queue = [state['location']]
    for here in queue:
        for d, t in content.rooms[here]['exits'].items():
            if t in content.rooms and t not in prev: prev[t] = (here, d); queue.append(t)
    steps = []; node = target
    while prev.get(node): here, d = prev[node]; steps.append(d); node = here
    for d in reversed(steps):
        if state['hp'] <= 0: state['hp'] = m.hp_max(state); state['wound'] = None
        act({'id': 'mover', 'target': d})

path = []
main = ['valdren_plaza']
prev = {'valdren_plaza': None}; queue = ['valdren_plaza']
for here in queue:
    for d, t in content.rooms[here]['exits'].items():
        if t in content.rooms and t not in prev: prev[t] = (here, d); queue.append(t)
node = 'vaisgard_mercado'; chain = []
while node: chain.append(node); node = prev[node][0] if prev[node] else None
# A thorough trip: every room on the way, plus each neighbour as a short detour.
for room in reversed(chain):
    goto(room); path.append(room); visit_room()
    for side in list(content.rooms[room]['exits'].values()):
        if side in chain or side not in content.rooms: continue
        goto(side); visit_room(); goto(room)
    if state['hp'] < .5 * m.hp_max(state): state['hp'] = m.hp_max(state); state['wound'] = None  # descanso entre tramos
value = sum(content.items[i.get('catalog_id', i['id'])].get('sell_price', 0) * i.get('quantity', 1) for i in state['inventory'] if i.get('kind') == 'material')
print(f"semilla {seed} · salas en ruta {len(path)} · nivel final {state['level']} · sellos {state['seals']} · materiales vendibles por {value} sellos")
print(dict(stats)); print('botín:', dict(loot))
