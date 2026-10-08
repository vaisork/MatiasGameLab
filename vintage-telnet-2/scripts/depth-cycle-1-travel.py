"""Travel criticism evidence via real API and throwaway store only."""
import sys,json,tempfile,uuid
from pathlib import Path
from collections import deque,Counter
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root),str(root/'runtime/python-deps')]
from server.app import create_app
from werkzeug.security import generate_password_hash
class Clock:
 now=12*3600
 def __call__(self):return self.now
class RNG:
 def random(self):return float(sys.argv[1]) if len(sys.argv)>1 else 0
rooms={}
for p in (root/'content/regions').glob('*.json'):rooms.update(json.loads(p.read_text())['rooms'])
all_runs=[]
routes=[('A','humano',['narevia_centro','velmora_centro','valdren_plaza']),('B','felaryn',['brumak_centro','valdren_plaza','khariel_centro'])]
if len(sys.argv)>3 and sys.argv[3]=='blind':routes=[('C','marevyn',['velmora_centro','khariel_centro','narevia_centro'])]
for label,species,targets in routes:
 with tempfile.TemporaryDirectory(prefix='vt-depth-travel-') as tmp:
  clock=Clock();app=create_app({'TESTING':True,'DATA_DIR':tmp,'CONTENT_DIR':str(root/'content'),'CLOCK':clock,'RNG':RNG(),'DM_PASSWORD_HASH':generate_password_hash('isolated-travel-test')});client=app.test_client();master=app.test_client();log=[]
  def state():return client.get('/api/state').json
  def post(c,path,data):return c.post(path,json={**data,'csrf_token':c.get('/api/state').json['csrf_token']})
  def act(action,target=None):
   before=state()['room']['id'];r=post(client,'/api/action',{'id':action,'target':target,'request_id':str(uuid.uuid4())});assert r.status_code in (200,201),(action,target,r.json)
   s=r.json;log.append({'action':action,'target':target,'from':before,'room':s['room'],'narrative':s['narrative'],'ambient':s['ambient'],'scene':s['scene']});clock.now+=60;return s
  r=post(client,'/api/account/register',{'username':'isolatedtravel'+label.lower(),'password':'isolated-test-password'});assert r.status_code in (200,201),r.json
  r=post(client,'/api/character/create',{'name':'Recorrido temporal','species':species,'class_id':'juramentado'});assert r.status_code in (200,201),r.json
  post(master,'/api/master/login',{'password':'isolated-travel-test'});r=post(master,'/api/master/approve',{'character_id':r.json['character']['id']});assert r.status_code in (200,201),r.json
  home=state()['room']['id'];act('mover','salir')
  def walk(destination):
   current=state()['room']['id'];q=deque([(current,[])]);seen={current}
   while q:
    here,path=q.popleft()
    if here==destination:break
    for direction,to in rooms.get(here,{}).get('exits',{}).items():
     if to not in seen:seen.add(to);q.append((to,path+[direction]))
   else:raise AssertionError(destination)
   for direction in path:
    s=state();move=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
    if move.get('disabled'):
     permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'))
    act('mover',direction)
  for target in targets:
   walk(target);act('observar')
  act('mover','hogar');assert state()['room']['id']==home
  moves=[e for e in log if e['action']=='mover'];assert len(moves)>=20
  all_runs.append({'route':label,'targets':targets,'movement_count':len(moves),'returned_home':True,'events':log})
(root/('review/depth-cycle-1/'+(sys.argv[2] if len(sys.argv)>2 else 'travel-before.json'))).write_text(json.dumps(all_runs,ensure_ascii=False,indent=2))
for run in all_runs:
 print('ROUTE',run['route'],'MOVES',run['movement_count'])
 for i,e in enumerate(run['events']):
  print(i,e['action'],e['room']['id']);print('\n'.join(n['text'] for n in e['narrative']))
