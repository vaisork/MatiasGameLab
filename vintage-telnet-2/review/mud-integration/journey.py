"""Replay real actions with isolated in-memory state; never reads player databases."""
import json,re,sys
from pathlib import Path
source=Path(sys.argv[1]).resolve();sys.path.insert(0,str(source))
from server.content import Content
from server.engine import Engine
from server import mechanics as m
clock=[43200]
class Rng:
 value=.99
 def random(self):return self.value
rng=Rng();content=Content(source/'content');engine=Engine(content,lambda:clock[0],rng)
world={'version':0,'flags':[],'deaths':{},'encounters':{}}
character={'id':1,'name':'Lector de prueba','species':'humano','class_id':'juramentado','status':'approved','state':m.new_state('humano','juramentado','review-home',clock[0])}
rows=[]
def capture(label,movement=False):
 s=engine.snapshot(character,world)
 rows.append({'label':label,'movement':movement,'room':s['room']['id'],'name':s['room']['name'],'description':s['room']['description'],'scene':s['scene'],'actions':s['actions'],'exits':s['room']['exits'],'combat':s['character']['combat'],'words':sum(len(re.findall(r'\S+',e['text'])) for e in s['scene'])})
def act(id,target=None):
 intent={'id':id}
 if target is not None:intent['target']=target
 reply=engine.apply(character,world,intent);clock[0]+=1
 capture(f'{id}:{target}',id=='mover')
 if id=='mirar':assert any(e['text']==engine.room(character,world)['description'] for e in engine.narrative(character,world,'mirar'))
for direction in ['salir','oeste','este','este','norte','sur','este','sur']:act('mover',direction)
act('examinar','esquina');act('edran_despejar_granero');assert 'edran_granero_despejado' in world['flags']
for direction in ['oeste','norte','sur','sur','este','oeste','oeste','sur']:act('mover',direction)
act('examinar','tallos');act('observar');act('mirar')
for direction in ['este','este','sur','norte','este','sur']:act('mover',direction)
engine.apply(character,world,{'id':'hablar','target':'edran_oren','topic':'caja'});capture('hablar:oren')
for direction in ['norte','oeste','oeste','oeste']:act('mover',direction)
character['state']['attributes'].update(fuerza=55,destreza=50);character['state']['hp']=m.hp_max(character['state']);rng.value=.01
act('combatir','espinajo_rastrojo')
for _ in range(8):
 if not character['state']['combat']:break
 engine.apply(character,world,{'id':'atacar'});clock[0]+=4;engine.tick(character,world);capture('combat_round')
assert character['state']['combat'] is None
assert 'victoria:edran_surcos:espinajo_rastrojo' in character['state']['flags']
assert not any(a.get('target')=='espinajo_rastrojo' and a['id'] in ('evaluar','combatir','examinar_criatura') for a in rows[-1]['actions'])
rng.value=.99
for direction in ['sur','oeste','oeste','oeste']:act('mover',direction)
for label,phase,weather in [('night','Noche',None),('rain','Día','Lluvia'),('wind','Día','Viento')]:
 for hour in range(168):
  clock[0]=hour*3600;a=engine.ambient(engine.room(character,world),world)
  if a['time_of_day']==phase and (weather is None or a['weather']==weather):capture(label);break
 else:raise AssertionError(label)
Path(sys.argv[2]).write_text(json.dumps({'moves':sum(r['movement'] for r in rows),'rows':rows,'state':character['state'],'world':world},ensure_ascii=False,indent=2))
print(json.dumps({'moves':sum(r['movement'] for r in rows),'snapshots':len(rows),'output':sys.argv[2]}))
