"""Prueba de mirar en una dirección, ecos y contador de secretos sobre una copia de la base desplegada.

Uso: python3 prueba_extras.py [ruta_base]
No modifica el proyecto: copia server/, content/, tests/ y client/ a un directorio temporal.
"""
import copy, importlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/jdiaz/proyectos/vt2-mud-piloto/vintage-telnet-2')
DEPS = '/home/jdiaz/proyectos/vintage-telnet-2-nuevo/runtime/python-deps'
results = {}

def check(name, ok, detail=''):
    results[name] = 'OK' if ok else f'FALLA {detail}'

with tempfile.TemporaryDirectory() as tmp:
    dst = Path(tmp) / 'base'
    for d in ('server', 'content', 'tests', 'client'):
        shutil.copytree(BASE / d, dst / d, ignore=shutil.ignore_patterns('__pycache__'))
    for p in ('extras_motor.patch', 'extras_contenido.patch', 'extras_cliente.patch'):
        subprocess.run(['patch', '-s', '-p1', '-d', str(dst), '-i', str(HERE / p)], check=True)
    # Datos en la copia del contenido.
    look = json.loads((HERE / 'mirar_direcciones.json').read_text(encoding='utf-8'))['rooms']
    echoes = json.loads((HERE / 'ecos.json').read_text(encoding='utf-8'))['rooms']
    for f in (dst / 'content' / 'regions').glob('*.json'):
        doc = json.loads(f.read_text(encoding='utf-8'))
        for rid, room in doc['rooms'].items():
            if rid in look: room['look'] = look[rid]
            if rid in echoes: room['echoes'] = echoes[rid]
        f.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    world = json.loads((dst / 'content' / 'world.json').read_text(encoding='utf-8'))
    world['secrets'] = json.loads((HERE / 'secretos.json').read_text(encoding='utf-8'))['secrets']
    (dst / 'content' / 'world.json').write_text(json.dumps(world, ensure_ascii=False, indent=1), encoding='utf-8')

    sys.path.insert(0, str(dst))
    Content = importlib.import_module('server.content').Content
    Engine = importlib.import_module('server.engine').Engine
    m = importlib.import_module('server.mechanics')
    content = Content(dst / 'content')
    now = [10 * 3600.0]
    eng = Engine(content, lambda: now[0])
    w = {'flags': [], 'deaths': {}, 'version': 0}
    st = m.new_state('humano', 'juramentado', 'home:p', now[0])
    st.update(location='valdren_calle_alta', known=['valdren_calle_alta', 'valdren_plaza'], visited=['valdren_calle_alta', 'valdren_plaza'])
    st['visits'].update(valdren_calle_alta=1, valdren_plaza=1)
    ch = {'id': 1, 'name': 'P', 'species': 'humano', 'class_id': 'juramentado', 'status': 'approved', 'state': st}

    # 1. Mirar hacia una dirección
    eng.apply(ch, w, {'id': 'mover', 'target': 'sur'})
    acts = eng.actions(ch, w)
    labels = [a['label'] for a in acts if a['id'] == 'mirar_direccion']
    check('mirar: 4 direcciones en la plaza', len(labels) == 4, labels)
    parsed = eng.parse_intent(ch, w, {'text': 'mirar al norte'})
    check('mirar: «mirar al norte» se entiende', parsed == {'id': 'mirar_direccion', 'target': 'norte'}, parsed)
    eng.apply(ch, w, parsed)
    check('mirar: devuelve el texto de la dirección', st['events'][0]['text'] == look['valdren_plaza']['norte'])
    check('mirar: no mueve al personaje', st['location'] == 'valdren_plaza')

    # 2. Ecos al quedarse
    arrived = st['arrived_at']
    def scene_at(t):
        now[0] = arrived + t
        before = copy.deepcopy(ch)
        texts = [e['text'] for e in eng.snapshot(ch, w)['scene']]
        return texts, before == ch
    plaza_echoes = set(echoes['valdren_plaza'])
    t10, pure10 = scene_at(10); t70, pure70 = scene_at(70); t150, pure150 = scene_at(150); t400, _ = scene_at(400)
    e70 = plaza_echoes & set(t70); e150 = plaza_echoes & set(t150)
    check('ecos: nada al llegar', not (plaza_echoes & set(t10)))
    check('ecos: aparece uno al quedarse 70 s', len(e70) == 1, t70)
    check('ecos: cambia a los 150 s', len(e150) == 1 and e150 != e70)
    check('ecos: se agotan (no infinitos)', not (plaza_echoes & set(t400)))
    check('ecos: consultar no modifica el estado', pure10 and pure70 and pure150)
    # Con peligro presente no hay eco (Campo de surcos tiene señal fija de Espinajo).
    st.update(location='edran_surcos', arrived_at=now[0]); st['visited'].append('edran_surcos'); st['visits']['edran_surcos'] = 1
    now[0] += 100
    surcos = [e['text'] for e in eng.snapshot(ch, w)['scene']]
    check('ecos: no tapan un peligro', not (set(echoes['edran_surcos']) & set(surcos)))

    # 3. Contador de secretos
    check('secretos: empieza en 0', eng.snapshot(ch, w)['secrets']['found'] == 0)
    st['flags'].append('edran_lio_dibujo_fragua'); st['flags'].append('participated:lethra_barquita_rescatada')
    check('secretos: cuenta flags propios y participados', eng.snapshot(ch, w)['secrets']['found'] == 2)

    # 4. Contenido inválido se rechaza
    bad = copy.deepcopy(content.rooms['valdren_pozo']); bad['look'] = {'este': 'x'}
    try:
        doc = json.loads((dst / 'content/regions/edran.json').read_text(encoding='utf-8'))
        doc['rooms']['valdren_pozo']['look'] = {'este': 'x'}
        (dst / 'content/regions/edran.json').write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
        Content(dst / 'content'); check('contenido: rechaza dirección sin salida', False)
    except ValueError:
        check('contenido: rechaza dirección sin salida', True)
        doc['rooms']['valdren_pozo'].pop('look'); (dst / 'content/regions/edran.json').write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')

    # 5. Tests y cliente
    r = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-q'], cwd=dst, capture_output=True, text=True,
                       env={**os.environ, 'PYTHONPATH': f'{dst}:{DEPS}'})
    results['tests'] = (r.stderr.strip().splitlines() or ['?'])[-1] + ' · ' + next((l for l in r.stderr.splitlines() if l.startswith('Ran')), '')
    results['cliente sintaxis app.js'] = 'OK' if subprocess.run(['node', '--check', 'client/app.js'], cwd=dst).returncode == 0 else 'FALLA'
    for qa in ('qa-narrative.mjs', 'qa-printing.mjs', 'qa-passive.mjs'):
        q = subprocess.run(['node', qa], cwd=dst / 'client', capture_output=True, text=True)
        results[f'cliente {qa}'] = 'PASS' if q.returncode == 0 else (q.stdout + q.stderr).strip().splitlines()[-1:]

print(json.dumps(results, ensure_ascii=False, indent=1))
(HERE / 'salida').mkdir(exist_ok=True)
(HERE / 'salida' / 'extras.json').write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding='utf-8')
