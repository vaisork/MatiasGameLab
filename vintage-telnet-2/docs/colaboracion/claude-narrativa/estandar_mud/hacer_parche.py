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
            # Modo breve clásico: la seña del lugar y un solo detalle vivo que cambia de una visita a otra.
            lines=[event('world',brief)];options=[]
            for key in priority:
                if key in layers and key not in options:options.append(key)
            chosen='danger' if 'danger' in layers else options[visits%len(options)] if options else None
            if chosen:lines.append(layers[chosen])
            # Un recuerdo puede nombrar a alguien sin que esté; sólo una capa del presente lo hace innecesario.
            names=[npc['name'] for npc in present]
            if names and not (chosen in ('activity','weather','arrival') and any(name in layers[chosen]['text'] for name in names)):
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

if __name__ == '__main__':
    write_patch('server/engine.py', ENGINE, 'renderer.patch')
    write_patch('client/ui-data.js', CLIENT, 'cliente.patch')
    print('renderer.patch y cliente.patch regenerados')
