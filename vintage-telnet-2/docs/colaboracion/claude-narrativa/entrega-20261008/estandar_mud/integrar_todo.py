"""Integra TODAS las entregas de Claude sobre una base de VT2 (un checkout de vintage-telnet-2).

Uso: python3 integrar_todo.py /ruta/a/vintage-telnet-2 [--informe salida/integracion.json]

- Código: aplica por anclaje las ediciones de hacer_parche.py (combate) y hacer_parche_extras.py (mirar, ecos,
  secretos). Si un anclaje ya no existe, lo informa y no lo aplica (no adivina).
- Contenido: aplica descripciones/señas/regresos/estados de *_propuesta.json, escenas por visita, vistas, ecos,
  secretos y los bloques de propuestas.json (TEXTOS A–I). Los estados se buscan por sus condiciones, no por índice.
- No hace commit, push ni despliegue.
"""
import importlib.util, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/content')   # contenido sobre el que se indexaron las propuestas
BASE = Path(sys.argv[1]).resolve()
REPORT = {'codigo': {}, 'contenido': {}, 'omitido': []}

def load_module(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f'{name}.py'); mod = importlib.util.module_from_spec(spec)
    sys.argv_backup = sys.argv; sys.argv = [name]; spec.loader.exec_module(mod); sys.argv = sys.argv_backup
    return mod

def apply_code(rel, pairs, label):
    path = BASE / rel; text = path.read_text(encoding='utf-8'); done = 0
    for old, new in pairs:
        if new in text: done += 1; continue                      # ya integrado
        if text.count(old) != 1:
            REPORT['omitido'].append(f'{label}: anclaje ausente en {rel}: {old[:70]!r}'); continue
        text = text.replace(old, new); done += 1
    path.write_text(text, encoding='utf-8'); REPORT['codigo'][label] = f'{done}/{len(pairs)}'

# ───────── código
parche = load_module('hacer_parche'); extras = load_module('hacer_parche_extras')
apply_code('server/mechanics.py', parche.COMBAT, 'combate')
apply_code('server/engine.py', parche.COMBAT_ENGINE, 'combate_motor')
apply_code('server/engine.py', extras.ENGINE, 'extras_motor')
apply_code('server/content.py', extras.CONTENT, 'extras_contenido')
apply_code('client/app.js', extras.CLIENT, 'extras_cliente')
if 'Salidas: ' not in (BASE / 'client/ui-data.js').read_text(encoding='utf-8'):
    apply_code('client/ui-data.js', parche.CLIENT, 'linea_salidas')

# ───────── contenido
regions = {f: json.loads(f.read_text(encoding='utf-8')) for f in (BASE / 'content/regions').glob('*.json')}
world_path = BASE / 'content/world.json'; world = json.loads(world_path.read_text(encoding='utf-8'))
rooms = {rid: r for d in regions.values() for rid, r in d['rooms'].items()}
npcs = {nid: n for d in regions.values() for nid, n in d['npcs'].items()}
ref_rooms = {}
for f in (REF / 'regions').glob('*.json'): ref_rooms.update(json.loads(f.read_text(encoding='utf-8'))['rooms'])
count = lambda key: REPORT['contenido'].__setitem__(key, REPORT['contenido'].get(key, 0) + 1)

def signature(state):
    return json.dumps({k: state.get(k) for k in ('requires_flags', 'forbids_flags', 'requires_time', 'requires_weather', 'requires_visits')}, sort_keys=True)

def find_state(rid, ref_index):
    ref = ref_rooms.get(rid, {}).get('states', [])
    if ref_index >= len(ref): return None
    sig = signature(ref[ref_index])
    return next((s for s in rooms[rid].get('states', []) if signature(s) == sig), None)

# a) descripciones, señas, regresos y estados reescritos
for f in sorted(HERE.glob('*_propuesta.json')):
    for rid, fields in json.loads(f.read_text(encoding='utf-8'))['rooms'].items():
        if rid not in rooms: REPORT['omitido'].append(f'sala inexistente {rid}'); continue
        for field, value in fields.items():
            m = re.fullmatch(r'states\[(\d+)\]\.overrides\.(\w+)', field)
            if m:
                state = find_state(rid, int(m.group(1)))
                if state is None: REPORT['omitido'].append(f'estado no encontrado {rid}:{field}'); continue
                state.setdefault('overrides', {})[m.group(2)] = value; count('estados')
            else:
                rooms[rid][field] = value; count(field)

# b) escenas por visita: tras la última variante sólo de hora/visita, antes de clima o misión
plain = lambda s: set(s) - {'overrides'} <= {'requires_time', 'requires_visits'}
for name in ('escenas_visita.json', 'escenas_visita_2.json'):
    for rid, spec in json.loads((HERE / name).read_text(encoding='utf-8')).items():
        if rid.startswith('_') or rid not in rooms: continue
        states = rooms[rid].setdefault('states', [])
        existing = {signature(s) for s in states}
        new = [s for s in spec['estados'] if signature(s) not in existing]
        idx = max([i + 1 for i, s in enumerate(states) if plain(s)], default=0)
        states[idx:idx] = new; REPORT['contenido']['escenas_visita'] = REPORT['contenido'].get('escenas_visita', 0) + len(new)

# c) vistas, ecos, secretos
for rid, look in json.loads((HERE / 'mirar_direcciones.json').read_text(encoding='utf-8'))['rooms'].items():
    rooms[rid]['look'] = {d: t for d, t in look.items() if d in rooms[rid].get('exits', {})}; count('look')
for rid, echo in json.loads((HERE / 'ecos.json').read_text(encoding='utf-8'))['rooms'].items():
    rooms[rid]['echoes'] = echo; count('echoes')
world['secrets'] = json.loads((HERE / 'secretos.json').read_text(encoding='utf-8'))['secrets']

# d) propuestas.json (TEXTOS A–I)
TABLES = {'quests': world['quests'], 'creatures': world['creatures'], 'rooms': rooms, 'npcs': npcs}
def step(node, token, create):
    m = re.fullmatch(r'([^\[]+)(?:\[(.+)\])?', token); name, sel = m.group(1), m.group(2)
    if name not in node:
        if not create: return None
        node[name] = [] if sel else {}
    node = node[name]
    if sel is None: return node
    if sel == '+': return None
    if sel.isdigit(): return node[int(sel)] if int(sel) < len(node) else None
    k, v = sel.split('=', 1)
    return next((x for x in node if x.get(k) == v), None)

def apply_proposal(p):
    table, field, text = p['tabla'], p['campo'], p['texto']
    if table not in TABLES or field.startswith('topics (') or p['archivo'].startswith('client'): return 'código/clave'
    target = TABLES[table].get(p['id'])
    if target is None: return 'id inexistente'
    value = json.loads(text) if text.startswith('{') and field != 'description' else text
    # Diálogo propio de una señal → mecanismo adversary_prose de la base.
    m = re.fullmatch(r'signals\[creature=(\w+)\]\.dialogue', field)
    if m:
        target.setdefault('adversary_prose', {}).setdefault(m.group(1), {}).setdefault('dialogue', value); return 'ok'
    if field.startswith('states[+]'):
        if signature(value) not in {signature(s) for s in target.setdefault('states', [])}: target['states'].append(value)
        return 'ok'
    m = re.fullmatch(r'actions\[id=(\w+)\](?:\.(\w+))?', field)
    if m:
        actions = target.setdefault('actions', []); action = next((a for a in actions if a.get('id') == m.group(1)), None)
        if m.group(2):
            if action is None: return 'acción inexistente'
            action[m.group(2)] = value
        elif isinstance(value, dict):
            if action is None: actions.append(value)
            else: action.update(value)
        return 'ok'
    tokens = field.split('.')
    node = target
    for token in tokens[:-1]:
        node = step(node, token, create=True)
        if node is None: return 'ruta inexistente'
    last = tokens[-1]
    m = re.fullmatch(r'([^\[]+)\[(.+)\]', last)
    if m:  # p. ej. wildlife_pool[creature=x] sin .text no se usa
        return 'ruta no soportada'
    if last == 'text' and isinstance(node, dict): node['text'] = value; return 'ok'
    if isinstance(node.get(last), dict) and isinstance(value, str): node[last]['text'] = value; return 'ok'
    node[last] = value; return 'ok'

for p in json.loads((HERE.parent / 'propuestas.json').read_text(encoding='utf-8')):
    # wildlife_pool/signals por criatura: localizar el elemento y fijar su texto
    m = re.fullmatch(r'(wildlife_pool|signals)\[creature=(\w+)\]\.text', p['campo'])
    if m and p['tabla'] == 'rooms':
        room = rooms.get(p['id']); item = next((x for x in (room or {}).get(m.group(1), []) if x.get('creature') == m.group(2)), None)
        result = 'ok' if item is not None else 'elemento inexistente'
        if item is not None: item['text'] = p['texto']
    else:
        result = apply_proposal(p)
    if result == 'ok': count('propuestas')
    else: REPORT['omitido'].append(f"propuesta {p['id']}.{p['campo']}: {result}")

for f, d in regions.items(): f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
world_path.write_text(json.dumps(world, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

out = HERE / 'salida' / 'integracion.json'; out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(REPORT, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps({k: (v if k != 'omitido' else len(v)) for k, v in REPORT.items()}, ensure_ascii=False, indent=1))
