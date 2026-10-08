"""Isolated authored-world integration journey, without database/player edits."""
import sys, json, tempfile, uuid, os
from pathlib import Path
from collections import deque
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'runtime/python-deps')]
from server.app import create_app
from werkzeug.security import generate_password_hash
class Clock:
 now=12*3600
 def __call__(self):return self.now
class RNG:
 def random(self):return .9
root=Path(__file__).resolve().parents[1]; rooms={}
for p in (root/'content/regions').glob('*.json'):rooms.update(json.loads(p.read_text())['rooms'])
clock=Clock(); evidence=[]; journey=[]
with tempfile.TemporaryDirectory(prefix='vt-night-integration-') as tmp:
 app=create_app({'TESTING':True,'DATA_DIR':tmp,'CLOCK':clock,'RNG':RNG(),'DM_PASSWORD_HASH':generate_password_hash('isolated-test-only')});client=app.test_client();dm=app.test_client()
 def post(c,p,data):
  csrf=c.get('/api/state').json['csrf_token'];return c.post(p,json={**data,'csrf_token':csrf})
 def state():return client.get('/api/state').json
 def act(id,target=None,**extra):
  clock.now+=60
  r=post(client,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4()),**extra});assert r.status_code==200,(id,target,r.json);s=r.json;journey.append({'action':id,'target':target,'room':s['room']['id'],'events':s['narrative'],'seals':s['character']['seals'],'hp':s['character']['hp']});return s
 def walk(dest):
  start=state()['room']['id']
  if start.startswith('home:'):act('mover','salir');start=state()['room']['id']
  q=deque([(start,[])]);seen={start};path=None
  while q:
   here,steps=q.popleft()
   if here==dest:path=steps;break
   for direction,to in rooms.get(here,{}).get('exits',{}).items():
    if to not in seen:seen.add(to);q.append((to,steps+[direction]))
  assert path is not None,(start,dest)
  for direction in path:
   s=state();move=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
   if move.get('disabled'):
    permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'))
   act('mover',direction)
  evidence.append({'walk_to':dest,'steps':len(path)})
 post(client,'/api/account/register',{'username':'nightjourney','password':'isolated-test-password'});c=post(client,'/api/character/create',{'name':'Prueba nocturna','species':'humano','class_id':'juramentado','gender':'femenino'}).json
 post(dm,'/api/master/login',{'password':'isolated-test-only'});post(dm,'/api/master/approve',{'character_id':c['character']['id']});act('mover','salir')



 samples=[]
 def talkset(npc,topics,label):
  for topic in topics:
   result=act('hablar',npc,topic=topic);samples.append({'phase':label,'npc':npc,'topic':topic,'room':result['room']['id'],'ambient':result['ambient'],'narrative':result['narrative']})
 walk('valdren_fragua');act('aceptar','valdren_recado_forja');walk('valdren_cobertizo');act('hablar','edran_bren',topic='rueda');walk('valdren_fragua');act('cobrar','valdren_recado_forja');talkset('edran_daro',['trabajo','armas','pueblo'],'completed')
 walk('korven_entrante_piezas');act('aceptar','brumak_taza');act('hablar','korven_taren',topic='medidas');walk('korven_horno_reposo');act('examinar','recipiente');act('korven_recomendar_base');walk('korven_entrante_piezas');act('hablar','korven_taren',topic='recomendación');act('cobrar','brumak_taza');talkset('korven_taren',['medidas','materiales','horno','pieza'],'completed')
 walk('lethra_mercado_hojas');act('aceptar','narevia_preparativos');walk('lethra_plataforma_secado');act('examinar','costuras');act('lethra_elegir_cubierto');walk('lethra_cocina_reunion');act('hablar','lethra_nima',topic='preparativos');walk('lethra_mercado_hojas');act('cobrar','narevia_preparativos');talkset('lethra_nera_mercado',['reunión','comprar','vender','cuidados'],'completed')

 owner=client;other=app.test_client();post(other,'/api/account/register',{'username':'observer18','password':'isolated-test-password'});created=post(other,'/api/character/create',{'name':'Observadora de camino','species':'humano','class_id':'juramentado','gender':'femenino'}).json;post(dm,'/api/master/approve',{'character_id':created['character']['id']})
 pairs=[]
 for room,npc,topics in [('valdren_fragua','edran_daro',['trabajo','pueblo']),('korven_entrante_piezas','korven_taren',['materiales','horno']),('lethra_mercado_hojas','lethra_nera_mercado',['reunión','comprar'])]:
  pair={'room':room,'npc':npc}
  for role,c in [('owner',owner),('observer',other)]:
   client=c;walk(room);responses=[]
   for topic in topics:
    result=act('hablar',npc,topic=topic);responses.append({'topic':topic,'narrative':result['narrative']})
   pair[role]=responses
   if role=='observer':assert not any(t['kind']=='discovery' for v in responses for t in v['narrative']),(npc,responses)
  pairs.append(pair)
 (root/'review/archive/2026-10-07/DEPTH_CYCLE_18_PRIVATE_PAIR.json').write_text(json.dumps({'pairs':pairs,'moves':sum(e['action']=='mover' for e in journey)},ensure_ascii=False,indent=2)+'\n');print('three owner/observer pairs; no private memory in observer dialogues')
