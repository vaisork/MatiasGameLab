"""Town entry and return replay in disposable API database; no production writes."""
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
  previous=state();before=previous['character']['location'];clock.now+=60
  result=post(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4())})
  if id.startswith('pedir_permiso'):
   assert result['character']['seals']==previous['character']['seals']
   assert id not in [a['id'] for a in result['actions']]
   out.append({'type':'permission','room':before,'narrative':result['narrative']})
  if id=='mover':walked.add(frozenset((before,result['character']['location'])))
  snapshot=result['map'];known={n['id'] for n in snapshot['nodes']};home=result['character']['home'] if 'home' in result['character'] else 'home:'+str(result['character']['id'])
  origin=content.regions['lethra']['settlement']
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
 s=post(c,'/api/character/create',{'name':'Lector regional','species':'marevyn','class_id':'juramentado','gender':'masculino'})
 post(dm,'/api/master/login',{'password':'temporary-cycle2-only'});post(dm,'/api/master/approve',{'character_id':s['character']['id']});act('mover','salir')
 targets=['edran_salida_huertos','valdren_huertos','edran_salida_huertos','korven_peldanos_cortos','brumak_centro','korven_peldanos_cortos','brumak_centro']
 milestones=[]
 for target in targets:
  walk(target);
  if target in ('edran_salida_huertos','korven_peldanos_cortos'):
   npc='edran_lina' if target=='edran_salida_huertos' else 'korven_ved'
   reply=post(c,'/api/action',{'id':'hablar','target':npc,'topic':'entrada','request_id':str(uuid.uuid4())})
   out.append({'type':'conversation','room':target,'narrative':reply['narrative']})
   available=next((a for a in state()['actions'] if a['id'].startswith('pedir_permiso')),None)
   if available:act(available['id'],available.get('target'))
  observed=act('observar');snapshot=state();out.append({'type':'observation','room':target,'scene':snapshot['scene'],'observe':observed['narrative']});milestones.append({'room':target,'map':snapshot['map']})
 walk(content.regions['lethra']['settlement']);act('mover','hogar');final=state();assert not final['character']['combat'];milestones.append({'room':final['room']['id'],'map':final['map']})
print('Permission requests:',[e['room'] for e in out if e['type']=='permission']);assert sum(e['type']=='permission' for e in out)==2
assert any('Tu nombre ya está en la tablilla' in str(e.get('narrative')) for e in out)
assert any('Tu nombre ya está en la lista' in str(e.get('narrative')) for e in out)
Path(root/'review/narrative/TOWN_ENTRIES_20261007.json').write_text(json.dumps({'moves':sum(x['type']=='step' for x in out)+2,'scope':'Permission and return journey; New level1 character in temporary DB; all moves ordinary API; permission requests honoured; no player flags/inventory seeded. Every exposed map edge verified against actual walked pairs; directions against canonical exits; frontiers expose no destination names.','journey':out,'milestones':milestones},ensure_ascii=False,indent=2)+'\n')
print('Town entry journey:',sum(x['type']=='step' for x in out)+2,'moves;',len(final['map']['nodes']),'known places')
