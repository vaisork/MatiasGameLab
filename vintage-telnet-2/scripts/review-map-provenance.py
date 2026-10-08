"""Map provenance replay in disposable API database; no production writes."""
import sys,json,tempfile,uuid
from pathlib import Path
from collections import deque
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'runtime/python-deps')]
from server.app import create_app
from server.content import Content
from server.engine import Engine
from werkzeug.security import generate_password_hash
class Clock:
 now=43200
 def __call__(self):return self.now
class RNG:
 def random(self):return .9
root=Path(__file__).resolve().parents[1];content=Content(root/'content');clock=Clock();out=[];walked=set()
with tempfile.TemporaryDirectory(prefix='vt-map-provenance-') as tmp:
 app=create_app({'TESTING':True,'DATA_DIR':tmp,'CONTENT_DIR':str(root/'content'),'CLOCK':clock,'RNG':RNG(),'DM_PASSWORD_HASH':generate_password_hash('temporary-cycle2-only')});c=app.test_client();dm=app.test_client()
 def post(client,path,data):
  token=client.get('/api/state').json['csrf_token'];r=client.post(path,json=dict(data,csrf_token=token));assert r.status_code in (200,201),(path,r.json);return r.json
 def state():return c.get('/api/state').json
 def act(id,target=None):
  before=state()['character']['location'];clock.now+=60
  result=post(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4())})
  if id=='mover':walked.add(frozenset((before,result['character']['location'])))
  snapshot=result['map'];known={n['id'] for n in snapshot['nodes']};home=result['character']['home'] if 'home' in result['character'] else 'home:'+str(result['character']['id'])
  origin=content.regions['korven']['settlement']
  def exits(roomid):
   if roomid==home:return {'salir':origin}
   value=dict(content.rooms[roomid]['exits'])
   if roomid==origin:value['hogar']=home
   return value
  for edge in snapshot['edges']:assert frozenset(edge) in walked and set(edge)<=known
  for route in snapshot['routes']:
   assert route['from'] in known and route['to'] in known
   assert exits(route['from'])[route['direction']]==route['to']
   assert frozenset((route['from'],route['to'])) in walked
  for frontier in snapshot['frontiers']:assert set(frontier)=={'from','direction'}
  return result
 def walk(dest):
  start=state()['room']['id'];q=deque([(start,[])]);seen={start}
  while q:
   here,path=q.popleft()
   if here==dest:break
   for direction,to in content.rooms[here]['exits'].items():
    if to not in seen:seen.add(to);q.append((to,path+[direction]))
  else:raise AssertionError(dest)
  for direction in path:
   s=state();move=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
   if move.get('disabled'):
    permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'))
   result=act('mover',direction)
   out.append({'type':'step','room':result['room']['id'],'ambient':result['ambient'],'scene':result['scene']})
 post(c,'/api/account/register',{'username':'depthcycle2','password':'temporary-cycle2-password'})
 s=post(c,'/api/character/create',{'name':'Lector regional','species':'dravak','class_id':'juramentado','gender':'masculino'})
 post(dm,'/api/master/login',{'password':'temporary-cycle2-only'});post(dm,'/api/master/approve',{'character_id':s['character']['id']});act('mover','salir')
 targets=['hoshai_lavadero_roca','nhal_umbral_elin','lethra_muelle_vecinal','valdren_fragua','veyra_colina_vista','brumak_centro']
 milestones=[]
 for target in targets:
  walk(target);observed=act('observar');snapshot=state();out.append({'type':'observation','room':target,'scene':snapshot['scene'],'observe':observed['narrative']});milestones.append({'room':target,'map':snapshot['map']})
 act('mover','hogar');final=state();assert not final['character']['combat'];milestones.append({'room':final['room']['id'],'map':final['map']})
Path(root/'review/map/MAP_PROVENANCE_20261007.json').write_text(json.dumps({'moves':sum(x['type']=='step' for x in out)+2,'scope':'New level1 character in temporary DB; all moves ordinary API; permission requests honoured; no player flags/inventory seeded. Every exposed map edge verified against actual walked pairs; directions against canonical exits; frontiers expose no destination names.','journey':out,'milestones':milestones},ensure_ascii=False,indent=2)+'\n')
print('Map journey:',sum(x['type']=='step' for x in out)+2,'moves;',len(final['map']['nodes']),'known places')
