"""Prueba acotada del estándar MUD en Valdren.

Copia server/, content/ y tests/ a un directorio temporal, aplica allí el parche de renderizador
(renderer.patch) y la propuesta de texto (valdren_propuesta.json), y recorre rutas reales con el
Engine en proceso. No modifica el proyecto. Imprime métricas y deja transcripciones en ./salida/.

Uso, desde la raíz del proyecto:
  PYTHONPATH=runtime/python-deps python3 docs/colaboracion/claude-narrativa/estandar_mud/prueba.py
"""
import copy, importlib, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'salida'

def build(tmp, patched):
    dst = Path(tmp) / ('prop' if patched else 'base')
    for d in ('server', 'content', 'tests', 'client'):
        shutil.copytree(ROOT / d, dst / d, ignore=shutil.ignore_patterns('__pycache__'))
    if patched:
        for name in ('renderer.patch', 'cliente.patch'):
            subprocess.run(['patch', '-s', '-p1', '-d', str(dst), '-i', str(HERE / name)], check=True)
    return dst

def load(dst):
    for k in [k for k in sys.modules if k == 'server' or k.startswith('server.')]:
        del sys.modules[k]
    sys.path.insert(0, str(dst))
    try:
        content_mod = importlib.import_module('server.content')
        engine_mod = importlib.import_module('server.engine')
        mech = importlib.import_module('server.mechanics')
    finally:
        sys.path.pop(0)
    return content_mod.Content, engine_mod.Engine, mech

def apply_text(content, proposal):
    for rid, fields in proposal['rooms'].items():
        room = content.rooms[rid]
        for field, value in fields.items():
            m = re.fullmatch(r'states\[(\d+)\]\.overrides\.(\w+)', field)
            if m:
                room['states'][int(m.group(1))]['overrides'][m.group(2)] = value
            else:
                room[field] = value

class Journal:
    """Port en Python de NarrativeJournal.consume (client/ui-data.js)."""
    def __init__(self, exits=False):
        self.exits = exits; self.room = None; self.scene = set(); self.feedback = ''; self.printed = []
    def consume(self, snap, explicit=False):
        stamp = lambda e: e['kind'] + '\n' + e['text']
        scene = list(snap['scene']); reply = list(snap['narrative'])
        current = {stamp(e) for e in scene}; moved = self.room != snap['room']['id']
        key = json.dumps([stamp(e) for e in reply], ensure_ascii=False); add = []
        if moved:
            add.append({'kind': 'location', 'text': ('Estás en ' if self.room is None else 'Llegas a ') + snap['room']['name'] + '.'})
            add += scene
            if self.exits:
                ex = [(a['target'] + (f" ({a['label'].split(' · ')[1]})" if ' · ' in a['label'] and a['label'].split(' · ')[1] != 'Salida por explorar' else '')) for a in snap['actions'] if a['id'] == 'mover' and a['target'] != 'hogar']
                if ex: add.append({'kind': 'info', 'text': 'Salidas: ' + ', '.join(ex) + '.'})
        elif not explicit:
            add += [e for e in scene if stamp(e) not in self.scene]
        if explicit or key != self.feedback:
            add += [e for e in reply if stamp(e) not in current]
        if explicit and not moved:
            add += [e for e in scene if stamp(e) not in self.scene and not any(stamp(r) == stamp(e) for r in reply)]
        seen = set()
        for e in add:
            if stamp(e) in seen: continue
            seen.add(stamp(e)); self.printed.append(e)
        self.room = snap['room']['id']; self.scene = current; self.feedback = key

def sentences(t):
    return [s.strip() for s in re.split(r'(?<=[.!?»])\s+', t) if s.strip()]

def words(t):
    return len(re.findall(r'\w+', t))

TOUR = ['norte', 'norte', 'sur', 'oeste', 'oeste', 'este', 'este', 'sur',          # fragua, patio de ropa, cuidados
        'sur', 'sur', 'norte', 'norte',                                            # pozo, comedor
        'este', 'norte', 'sur', 'oeste',                                           # huertos, semillas
        'oeste', 'sur', 'este', 'oeste', 'norte', 'este',                          # cobertizo, patio, graneros
        'norte', 'norte', 'sur', 'sur']                                            # segunda vuelta a la fragua

def run(Content, Engine, mech, dst, proposal, hour, patched=False):
    content = Content(dst / 'content')
    if proposal: apply_text(content, proposal)
    now = [hour * 3600.0]
    eng = Engine(content, lambda: now[0], __import__('random').Random(7))
    world = {'flags': [], 'deaths': {}, 'version': 0}
    st = mech.new_state('humano', 'juramentado', 'home:prueba', now[0])
    st.update(location='valdren_plaza', known=['valdren_plaza'], visited=['valdren_plaza']); st['visits']['valdren_plaza'] = 1
    ch = {'id': 1, 'name': 'Prueba', 'species': 'humano', 'class_id': 'juramentado', 'status': 'approved', 'state': st}
    j = Journal(exits=patched); log = []
    def act(intent, explicit=True):
        eng.apply(ch, world, intent); snap = eng.snapshot(ch, world); j.consume(snap, explicit)
        st['events'] = []; log.append(intent)
        now[0] += 20
        return snap
    j.consume(eng.snapshot(ch, world))
    for d in TOUR:
        act({'id': 'mover', 'target': d})
    act({'id': 'mirar'})                                   # mirar en una sala ya visitada: debe dar la descripción completa
    act({'id': 'observar'})
    act({'id': 'examinar', 'target': 'banco'})
    # Exploración y combate fuera del pueblo (plaza → huertos → salida de las cercas), y regreso.
    snap = act({'id': 'mover', 'target': 'este'}); snap = act({'id': 'mover', 'target': 'este'})
    combat_ok = None
    world.setdefault('wildlife', {})['edran_salida_huertos'] = {'signal': {'creature': 'espinajo_rastrojo', 'text': content.rooms['edran_salida_huertos']['wildlife_pool'][0]['text']}, 'until': now[0] + 600}
    snap = act({'id': 'mirar'})
    acts = eng.actions(ch, world)
    if any(a['id'] == 'combatir' for a in acts):
        act({'id': 'combatir', 'target': 'espinajo_rastrojo'})
        for _ in range(40):
            if not st['combat']: break
            if not st['combat'].get('intervention'):
                eng.apply(ch, world, {'id': 'atacar'})
            now[0] += 5; eng.tick(ch, world); snap = eng.snapshot(ch, world); j.consume(snap, False); st['events'] = []
        combat_ok = st['combat'] is None
    snap = act({'id': 'mover', 'target': 'oeste'}); snap = act({'id': 'mover', 'target': 'oeste'})   # regreso a la plaza
    return j.printed, combat_ok, st['location']

def metrics(printed):
    seen = {}; total = rep = 0
    for e in printed:
        if e['text'].startswith('Salidas: '):
            continue  # navegación: se cuenta aparte
        for s in sentences(e['text']):
            w = words(s); total += w
            if s in seen: rep += w
            seen[s] = seen.get(s, 0) + 1
    return total, rep

def coverage(base_content, proposal):
    """Palabras con contenido de la descripción original que no quedan en ningún texto visible de la sala."""
    stop = set('para entre desde hasta donde sobre junto queda quedan llegas vuelves sigue puedes hacia otra otro otros otras están está esta este ambas cada'.split())
    report = {}
    for rid, fields in proposal['rooms'].items():
        old = base_content.rooms[rid]
        new = dict(old); new.update({k: v for k, v in fields.items() if not k.startswith('states')})
        pool = ' '.join([new['description'], new.get('brief', ''), new.get('return', ''), *[v if isinstance(v, str) else v.get('text', '') for v in new.get('examine', {}).values()],
                         *[base_content.rooms[t]['name'] for t in new['exits'].values()], *[new.get(k, '') for k in ('day', 'night', 'dawn', 'dusk', 'rain')]]).lower()
        lost = [w for w in re.findall(r'\w{5,}', old['description'].lower()) if w not in stop and w not in pool and w not in ('norte', 'oeste')]
        report[rid] = sorted(set(lost))
    return report

def main():
    OUT.mkdir(exist_ok=True)
    proposal = json.loads((HERE / 'valdren_propuesta.json').read_text(encoding='utf-8'))
    results = {}
    with tempfile.TemporaryDirectory() as tmp:
        for patched in (False, True):
            dst = build(tmp, patched)
            Content, Engine, mech = load(dst)
            for label, prop in (('texto actual', None), ('texto propuesto', proposal)):
                if not patched and prop: continue
                name = ('renderizador propuesto + ' if patched else 'renderizador actual + ') + label
                for hour, phase in ((10, 'día'), (22, 'noche')):
                    printed, combat_ok, loc = run(Content, Engine, mech, dst, prop, hour, patched)
                    total, rep = metrics(printed)
                    results[f'{name} · {phase}'] = {'palabras': total, 'repetidas': rep, 'combate_resuelto': combat_ok, 'termina_en': loc, 'eventos': len(printed)}
                    slug = re.sub(r'\W+', '_', f'{name}_{phase}').strip('_')
                    (OUT / f'{slug}.txt').write_text('\n'.join(f"[{e['kind']}] {e['text']}" for e in printed), encoding='utf-8')
            if patched:
                base_content = Content(dst / 'content')
                results['cobertura'] = coverage(base_content, proposal)
                r = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-q'], cwd=dst, capture_output=True, text=True,
                                   env={**os.environ, 'PYTHONPATH': f"{dst}:{ROOT/'runtime'/'python-deps'}"})
                results['tests_con_parche'] = (r.stderr.strip().splitlines() or ['?'])[-1]
                r2 = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-q'], cwd=Path(tmp) / 'base', capture_output=True, text=True,
                                    env={**os.environ, 'PYTHONPATH': f"{Path(tmp)/'base'}:{ROOT/'runtime'/'python-deps'}"})
                results['tests_sin_parche'] = (r2.stderr.strip().splitlines() or ['?'])[-1]
                for qa in ('qa-narrative.mjs', 'qa-printing.mjs', 'qa-passive.mjs'):
                    q = subprocess.run(['node', qa], cwd=dst / 'client', capture_output=True, text=True)
                    results[f'cliente {qa}'] = 'PASS' if q.returncode == 0 else (q.stdout + q.stderr).strip().splitlines()[-1:]
    (OUT / 'metricas.json').write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(results, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
