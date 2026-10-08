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
   if sum(e['action']=='mover' for e in journey)>=24:return
   s=state();move=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
   if move.get('disabled'):
    permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'))
   act('mover',direction)
  evidence.append({'walk_to':dest,'steps':len(path)})
 post(client,'/api/account/register',{'username':'nightjourney','password':'isolated-test-password'});c=post(client,'/api/character/create',{'name':'Prueba nocturna','species':'humano','class_id':'juramentado','gender':'femenino'}).json
 post(dm,'/api/master/login',{'password':'isolated-test-only'});post(dm,'/api/master/approve',{'character_id':c['character']['id']});act('mover','salir')



 snapshots=[]
 def snap(tag):
  z=state();snapshots.append({'tag':tag,'room':z['room']['id'],'ambient':z['ambient'],'scene':z['scene'],'character':z['character'],'actions':z['actions']})
 walk('valdren_fragua');act('hablar','edran_daro',topic='trabajo');snap('forge initial');act('aceptar','valdren_recado_forja');walk('valdren_cobertizo');act('hablar','edran_bren',topic='rueda');walk('valdren_fragua');act('cobrar','valdren_recado_forja');act('hablar','edran_daro',topic='trabajo');snap('forge paid return')
 clock.now=max(clock.now,19*3600)
 walk('edran_reparo');act('observar');snap('western road dusk');walk('edran_ladera_piedra');act('observar');snap('final trail')
 moves=sum(e['action']=='mover' for e in journey)
 assert moves==24
 out={'moves':moves,'actions':len(journey),'events':journey,'samples':snapshots}
 (root/(sys.argv[1] if len(sys.argv)>1 else 'review/archive/2026-10-07/DEPTH_CYCLE_14_FINAL_BLIND.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(moves,len(journey))
