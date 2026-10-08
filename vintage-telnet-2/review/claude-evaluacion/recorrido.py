"""Recorrido de evaluación narrativa (Prompt Maestro §6 y §34): motor real en memoria, sin base de datos ni partidas.

Uso, desde vintage-telnet-2:  PYTHONPATH=. python3 review/claude-evaluacion/recorrido.py [hora] [salida.txt]
Imprime lo que leería el jugador, en el orden del diario del cliente, con el tipo de cada línea.
"""
import json, random, sys
from pathlib import Path
from server.content import Content
from server.engine import Engine
from server import mechanics as m

HOUR = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
ROUTE = sys.argv[3] if len(sys.argv) > 3 else 'a'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else None
content = Content(Path('content'))
now = [HOUR * 3600.0]
eng = Engine(content, lambda: now[0], random.Random(11))
world = {'flags': [], 'deaths': {}, 'version': 0}
SPECIES = 'dravak' if ROUTE == 'b' else 'humano'
state = m.new_state(SPECIES, 'juramentado', 'home:eval', now[0])
char = {'id': 1, 'name': 'Prueba', 'species': SPECIES, 'class_id': 'juramentado', 'status': 'approved', 'state': state}
state['visits']['home:eval'] = 1
lines = []

class Journal:
    """Mismo criterio que NarrativeJournal.consume del cliente: escena completa al llegar, sólo lo nuevo al quedarse."""
    def __init__(self): self.room = None; self.scene = set(); self.feedback = ''
    def consume(self, snap, explicit):
        stamp = lambda e: e['kind'] + '\n' + e['text']
        scene, reply = list(snap['scene']), list(snap['narrative'])
        current = {stamp(e) for e in scene}; moved = self.room != snap['room']['id']; key = json.dumps([stamp(e) for e in reply])
        add = []
        if moved:
            add.append({'kind': 'LUGAR', 'text': snap['room']['name']}); add += scene
            exits = [a['label'].split(' · ')[0].lower() for a in snap['actions'] if a['id'] == 'mover']
            if exits: add.append({'kind': 'salidas', 'text': ', '.join(exits)})
        elif not explicit: add += [e for e in scene if stamp(e) not in self.scene]
        if explicit or key != self.feedback: add += [e for e in reply if stamp(e) not in current]
        seen = set()
        for e in add:
            if stamp(e) in seen: continue
            seen.add(stamp(e)); lines.append(f"[{e['kind']}] {e['text']}")
        self.room = snap['room']['id']; self.scene = current; self.feedback = key
journal = Journal()

def act(intent, label=None, wait=25):
    lines.append(f"> {label or intent.get('target') or intent['id']}")
    eng.apply(char, world, intent); journal.consume(eng.snapshot(char, world), True)
    state['events'] = []; now[0] += wait

def stay(seconds):
    for _ in range(int(seconds // 30)):
        now[0] += 30; journal.consume(eng.snapshot(char, world), False)

def path(a, b):
    prev = {a: None}; queue = [a]
    for here in queue:
        if here == b: break
        exits = {'salir': eng.region_for(SPECIES)[1]['settlement']} if here.startswith('home:') else content.rooms[here].get('exits', {})
        for d, t in exits.items():
            if t not in prev: prev[t] = (here, d); queue.append(t)
    steps = []
    while prev.get(b): here, d = prev[b]; steps.append(d); b = here
    return steps[::-1]

def go(target):
    for d in path(state['location'], target):
        act({'id': 'mover', 'target': d}, d)
        if state['combat']: return

journal.consume(eng.snapshot(char, world), False)
if ROUTE == 'b':
    # Recorrido de control (no usado para ajustar): Brumak → Paso de las Lajas → sierra → Khariel.
    lines.append('=== Hogar → Brumak'); go('brumak_centro'); stay(120)
    for target in ('korven_meseta_relevo', 'hoshai_garganta_oeste', 'hoshai_hombro_lajas', 'hoshai_aprisco_abierto', 'hoshai_collado_pino', 'hoshai_abrigo_pinas'):
        lines.append(f'=== → {target}'); go(target)
        if any(a['id'] == 'buscar' and not a.get('disabled') for a in eng.actions(char, world)): act({'id': 'buscar'}, 'buscar alrededor')
    go('hoshai_pinar_discontinuo'); stay(160); go('khariel_centro'); stay(120)
    act({'id': 'mirar_direccion', 'target': 'sur'}, 'mirar al sur')
    text = '\n'.join(lines); (OUT.write_text(text, encoding='utf-8') if OUT else print(text)); sys.exit(0)
lines.append('=== Hogar → Valdren')
go('valdren_plaza'); stay(150)
act({'id': 'mirar_direccion', 'target': 'norte'}, 'mirar al norte')
lines.append('=== Valdren → campos → Vado de Juncos (transición Edran → Lethra)')
go('edran_acequia'); act({'id': 'observar'}, 'observar')
go('edran_puente_juncos'); act({'id': 'examinar', 'target': 'apoyos'}, 'examinar apoyos')
lines.append('=== Lethra → Narevia (comercio)')
go('narevia_centro'); stay(120); go('lethra_mercado_hojas')
buy = next((a for a in eng.actions(char, world) if a['id'] == 'comprar' and not a.get('disabled')), None)
if buy: act({'id': 'comprar', 'target': buy['target']}, buy['label'])
lines.append('=== Exploración y encuentro')
go('lethra_juncal_abierto'); act({'id': 'buscar'}, 'buscar alrededor') if any(a['id'] == 'buscar' and not a.get('disabled') for a in eng.actions(char, world)) else None
go('lethra_ribera_oeste')
world.setdefault('wildlife', {})['lethra_ribera_oeste'] = {'signal': next(s for s in content.rooms['lethra_ribera_oeste']['wildlife_pool'] if s['creature'] == 'forajido_camino'), 'until': now[0] + 900}
act({'id': 'mirar'}, 'mirar')
talk = next((a for a in eng.actions(char, world) if a['id'] == 'hablar_adversario'), None)
if talk: act({'id': 'hablar_adversario', 'target': talk['target'], 'topic': talk['topic']}, talk['label'])
lines.append('=== Combate')
act({'id': 'combatir', 'target': 'forajido_camino'}, 'enfrentarte')
for _ in range(20):
    if not state['combat']: break
    eng.apply(char, world, {'id': 'atacar'}); now[0] += 5; eng.tick(char, world); journal.consume(eng.snapshot(char, world), False); state['events'] = []
lines.append('=== Regreso')
go('valdren_plaza')
text = '\n'.join(lines)
(OUT.write_text(text, encoding='utf-8') if OUT else print(text))
