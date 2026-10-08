"""Genera extras_*.patch contra la base desplegada (vt2-mud-piloto): mirar en una dirección, ecos al quedarse
y contador de secretos. Falla si el código de anclaje ya no existe.

Uso: python3 hacer_parche_extras.py [ruta_base]   (por defecto /home/jdiaz/proyectos/vt2-mud-piloto/vintage-telnet-2)
"""
import difflib, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/jdiaz/proyectos/vt2-mud-piloto/vintage-telnet-2')

def write_patch(rel, pairs, out):
    before = (BASE / rel).read_text(encoding='utf-8'); after = before
    for old, new in pairs:
        assert after.count(old) == 1, f'{rel}: anclaje no único o ausente: {old[:90]!r}'
        after = after.replace(old, new)
    diff = difflib.unified_diff(before.splitlines(True), after.splitlines(True), f'a/{rel}', f'b/{rel}')
    (HERE / out).write_text(''.join(diff), encoding='utf-8')

ENGINE = [
 # Hora de llegada: los ecos sólo aparecen si te quedas. Se escribe al moverse (POST), nunca al consultar.
 ("state['last_room']=previous;state['location']=destination;state['arrival']=True",
  "state['last_room']=previous;state['location']=destination;state['arrival']=True;state['arrived_at']=self.clock()"),
 # Acción «Mirar hacia …» por cada salida real que tenga texto en look.
 ("""        actions += [{'id':'examinar','target':key,'label':f'Examinar {key}'} for key,value in room.get('examine',{}).items() if not isinstance(value,dict) or self.allowed(value,state,world)]""",
  """        actions += [{'id':'examinar','target':key,'label':f'Examinar {key}'} for key,value in room.get('examine',{}).items() if not isinstance(value,dict) or self.allowed(value,state,world)]
        actions += [{'id':'mirar_direccion','target':direction,'label':f'Mirar hacia el {direction}'} for direction in room.get('look',{}) if direction in room.get('exits',{})]"""),
 ("""            elif id=='examinar':aliases.add(normalize('examinar '+target))""",
  """            elif id=='examinar':aliases.add(normalize('examinar '+target))
            elif id=='mirar_direccion':aliases.update(normalize(v) for v in ('mirar '+target,'mirar al '+target,'mirar hacia el '+target))"""),
 ("""        if action in ('mirar','observar','examinar'):
            if action in ('mirar','observar'):self.observe(state,room,world)""",
  """        if action=='mirar_direccion':
            state['events']=[event('world',room['look'][target])]
        elif action in ('mirar','observar','examinar'):
            if action in ('mirar','observar'):self.observe(state,room,world)"""),
 # Ecos: microescenas al quedarse, fuera del límite de capas, nunca encima de un peligro y nunca infinitas.
 ("""            if len(lines)>=limit:break
        return lines

    @staticmethod""",
  """            if len(lines)>=limit:break
        echoes=[item.get('text') if isinstance(item,dict) else item for item in room.get('echoes',[]) if not isinstance(item,dict) or self.allowed(item,state,world)]
        stayed=self.clock()-state.get('arrived_at',self.clock())
        if mode=='navigation' and echoes and stayed>=60 and 'danger' not in layers:
            window=int((stayed-60)//75)
            if window<len(echoes):lines.append(event('world',echoes[(window+visits)%len(echoes)]))
        return lines

    @staticmethod"""),
 # Contador de secretos: sólo un número, sin lista ni total.
 ("""'journal':state['journal'],""",
  """'journal':state['journal'],'secrets':{'found':sum(1 for secret in getattr(self.content,'secrets',{}).values() if secret.get('flag') in state['flags'] or 'participated:'+str(secret.get('flag')) in state['flags'])},"""),
]

CONTENT = [
 ("""TABLES = ('regions','rooms','npcs','creatures','stories','items','quests')""",
  """TABLES = ('regions','rooms','npcs','creatures','stories','items','quests','secrets')"""),
 ("""            for destination in room.get('exits',{}).values():
                if destination not in self.rooms:
                    raise ValueError(f'Unknown exit from {key}: {destination}')""",
  """            for destination in room.get('exits',{}).values():
                if destination not in self.rooms:
                    raise ValueError(f'Unknown exit from {key}: {destination}')
            for direction in room.get('look',{}):
                if direction not in room.get('exits',{}):
                    raise ValueError(f'Look direction without exit in {key}: {direction}')"""),
]

CLIENT = [
 ("""subtitle('Sólo hechos y observaciones que has vivido.'),""",
  """subtitle('Sólo hechos y observaciones que has vivido.'),state.secrets?.found?subtitle(`Secretos encontrados: ${state.secrets.found}. El mundo guarda más.`):null,"""),
]

if __name__ == '__main__':
    write_patch('server/engine.py', ENGINE, 'extras_motor.patch')
    write_patch('server/content.py', CONTENT, 'extras_contenido.patch')
    write_patch('client/app.js', CLIENT, 'extras_cliente.patch')
    print('extras_motor.patch, extras_contenido.patch y extras_cliente.patch generados contra', BASE)
