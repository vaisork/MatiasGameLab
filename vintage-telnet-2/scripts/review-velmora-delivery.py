"""Read-only gameplay evidence in temporary API database; deterministic clock/RNG."""
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
root=Path(__file__).resolve().parents[1];content=Content(root/'content');clock=Clock();out=[]
with tempfile.TemporaryDirectory(prefix='vt-depth-cycle2-') as tmp:
 app=create_app({'TESTING':True,'DATA_DIR':tmp,'CONTENT_DIR':str(root/'content'),'CLOCK':clock,'RNG':RNG(),'DM_PASSWORD_HASH':generate_password_hash('temporary-cycle2-only')});c=app.test_client();dm=app.test_client()
 def post(client,path,data):
  token=client.get('/api/state').json['csrf_token'];r=client.post(path,json=dict(data,csrf_token=token));assert r.status_code in (200,201),(path,r.json);return r.json
 def state():return c.get('/api/state').json
 def act(id,target=None):
  clock.now+=60
  return post(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4())})
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
 s=post(c,'/api/character/create',{'name':'Lector regional','species':'vesperi','class_id':'juramentado','gender':'masculino'})
 post(dm,'/api/master/login',{'password':'temporary-cycle2-only'});post(dm,'/api/master/approve',{'character_id':s['character']['id']});act('mover','salir')
 def talk(npc,topic):
  result=post(c,'/api/action',{'id':'hablar','target':npc,'topic':topic,'request_id':str(uuid.uuid4())});out.append({'type':'conversation','room':state()['room']['id'],'npc':npc,'topic':topic,'narrative':result['narrative']});return result
 walk('nhal_mercado_setas');talk('nhal_varo','recipiente')
 walk('nhal_umbral_elin');talk('nhal_elin','entrega')
 walk(content.npcs['nhal_desi']['home_room']);talk('nhal_desi','apoyo');walk('nhal_secadero_sombra');act('nhal_preparar_recipiente')
 walk('nhal_umbral_elin');act('nhal_entregar_recipiente')
 completed=talk('nhal_elin','entrega');assert 'recipiente que trajiste' in completed['narrative'][0]['text']
 walk('nhal_mercado_setas');completed=talk('nhal_varo','recipiente');assert 'Elin conserva' in completed['narrative'][0]['text']
 for _ in range(3):
  repeated=talk('nhal_varo','recipiente');assert len(repeated['narrative'])==1
 walk('nhal_secadero_sombra');checked=act('examinar','apoyos');assert 'aro quedó libre' in checked['narrative'][0]['text'];out.append({'type':'examination','room':state()['room']['id'],'narrative':checked['narrative']})
 walk('nhal_umbral_elin');checked=act('examinar','recipiente');assert 'aro vacío queda en el secadero' in checked['narrative'][0]['text'];out.append({'type':'examination','room':state()['room']['id'],'narrative':checked['narrative']})
 assert not any(item['id']=='recipiente_elin' for item in state()['inventory'])
 assert not state()['character']['combat']
Path(root/'review/qa/VELMORA_DELIVERY_REPLAY_20261007.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Independent blind route:',sum(x['type']=='step' for x in out),'movement steps')
