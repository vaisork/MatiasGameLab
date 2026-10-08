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
 post(client,'/api/account/register',{'username':'nightjourney','password':'isolated-test-password'});c=post(client,'/api/character/create',{'name':'Prueba nocturna','species':'felaryn','class_id':'sombra'}).json
 post(dm,'/api/master/login',{'password':'isolated-test-only'});post(dm,'/api/master/approve',{'character_id':c['character']['id']});act('mover','salir')

 samples=[]
 def sample(tag):
  snap=state();samples.append({'tag':tag,'room':snap['room']['id'],'ambient':snap['ambient'],'scene':snap['scene']})
 walk('edran_acequia');sample('before repair');act('edran_despejar_acequia');sample('repair complete')
 walk('nhal_mercado_setas');act('aceptar','velmora_recipiente');walk('nhal_umbral_elin');act('hablar','nhal_elin',topic='entrega');walk('nhal_taller_cortezas');act('hablar','nhal_desi',topic='apoyo');walk('nhal_secadero_sombra');act('nhal_preparar_recipiente');walk('nhal_umbral_elin');act('nhal_entregar_recipiente');sample('delivery complete')
 for hour in [15,19,23,6,12]:
  next_time=(clock.now//86400)*86400+hour*3600
  if next_time<=clock.now:next_time+=86400
  clock.now=next_time
  for dest in ['nhal_secadero_sombra','nhal_umbral_elin','edran_acequia','edran_terraplen']:
   walk(dest);sample('return at '+str(hour));observed=act('observar');samples[-1]['observe']=observed['narrative']
 if len(sys.argv)>2 and sys.argv[2]=='rain_probe':
  walk('edran_acequia')
  for _ in range(168):
   if state()['ambient']['weather']=='Lluvia':break
   clock.now+=3600
  assert state()['ambient']['weather']=='Lluvia'
  for turn in range(3):
   sample('later rain '+str(turn));act('mover','oeste');act('mover','este')
 out={'moves':sum(e['action']=='mover' for e in journey),'events':journey,'samples':samples}
 (root/(sys.argv[1] if len(sys.argv)>1 else 'review/DEPTH_CYCLE_13_BEFORE.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('moves',out['moves'])
 for v in samples:print(v['tag'],v['room'],v['ambient'],v['scene'])
