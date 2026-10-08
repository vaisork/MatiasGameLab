import sys,json,tempfile,uuid,os
from pathlib import Path
from collections import deque
root=Path(__file__).resolve().parents[1];sys.path[:0]=[str(root),str(root/'runtime/python-deps')]
from server.app import create_app
from server.content import Content
from werkzeug.security import generate_password_hash
class Clock:
 now=43200
 def __call__(self):return self.now
class RNG:
 def random(self):return 0
clock=Clock();rooms=Content(root/'content').rooms;log=[];moves=0
with tempfile.TemporaryDirectory(prefix='vt-depth3-') as tmp:
 app=create_app({'TESTING':True,'DATA_DIR':tmp,'CLOCK':clock,'RNG':RNG(),'DM_PASSWORD_HASH':generate_password_hash('isolated')});c=app.test_client();dm=app.test_client()
 def state():return c.get('/api/state').json
 def post(client,path,data):return client.post(path,json={**data,'csrf_token':client.get('/api/state').json['csrf_token']})
 def act(id,target=None):
  global moves
  r=post(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4())});assert r.status_code==200,(id,target,r.json)
  s=r.json;log.append({'action':id,'target':target,'room':s['room']['id'],'events':s.get('narrative'), 'hp':s['character']['hp'],'combat':s['character'].get('combat')});moves+=id=='mover';return s
 def walk(dest):
  q=deque([(state()['room']['id'],[])]);seen=set()
  while q:
   here,path=q.popleft()
   if here==dest:break
   for direction,to in rooms[here].get('exits',{}).items():
    if to not in seen:seen.add(to);q.append((to,path+[direction]))
  assert here==dest,(here,dest)
  for direction in path:
   s=state();a=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
   if a.get('disabled'):
    permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'))
   act('mover',direction)
 post(c,'/api/account/register',{'username':'cycle3','password':'isolated-password'});new=post(c,'/api/character/create',{'name':'Ciclo fauna','species':'humano','class_id':'arcano'}).json
 post(dm,'/api/master/login',{'password':'isolated'});post(dm,'/api/master/approve',{'character_id':new['character']['id']});act('mover','salir')
 for dest in ['edran_surcos','edran_prado','edran_bajo_humedo','korven_roca_cascaron','lethra_juncal_abierto','lethra_orilla_silente','nhal_agua_sombreada','nhal_raiz_marcada','valdren_plaza']:
  walk(dest);act('observar');s=state();log.append({'available':s['actions'],'room':dest,'bestiary':s['bestiary']})
  for a in [a for a in s['actions'] if a['id']=='examinar_criatura']:act(a['id'],a['target'])
  for a in [a for a in state()['actions'] if a['id']=='evaluar']:act(a['id'],a['target'])
  if dest in ['edran_prado','lethra_orilla_silente','nhal_raiz_marcada']:
   for a in [a for a in state()['actions'] if a['id']=='acercarse']:act(a['id'],a['target']);act('retirarse',a['target'])
  if dest=='edran_surcos':
   act('combatir','espinajo_rastrojo');act('capacidad');clock.now+=4;s=state();log.append({'after_signature':s});clock.now+=40;log.append({'after_fight':state()})
 assert moves>=20,moves
 (root/os.environ.get('VT_DEPTH3_OUTPUT','review/depth-cycle3-before.json')).write_text(json.dumps({'moves':moves,'events':log,'final':state()},ensure_ascii=False,indent=2));print('PASS',moves)
