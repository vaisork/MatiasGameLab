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
 s=post(c,'/api/character/create',{'name':'Lector regional','species':'dravak','class_id':'juramentado','gender':'masculino'})
 post(dm,'/api/master/login',{'password':'temporary-cycle2-only'});post(dm,'/api/master/approve',{'character_id':s['character']['id']});act('mover','salir')
 def talk(npc,topic):
  result=post(c,'/api/action',{'id':'hablar','target':npc,'topic':topic,'request_id':str(uuid.uuid4())});out.append({'type':'conversation','room':state()['room']['id'],'narrative':result['narrative']})
 def note(action,target=None):
  result=act(action,target);out.append({'type':'decision','room':result['room']['id'],'action':action,'ambient':result['ambient'],'narrative':result['narrative'],'scene':result['scene']});return result
 walk('korven_almacen_entrada');talk('korven_ruma','balanza');walk('korven_almacen_balanzas');note('observar');walk('korven_almacen_cruce');note('korven_usar_lateral');walk('korven_almacen_fondo');note('korven_recoger_placa');walk('korven_almacen_entrada');note('korven_devolver_placa');walk('korven_almacen_balanzas');note('examinar','balanza')
 walk('edran_canal_entrada');talk('edran_nela','canal');walk('edran_canal_herramientas');note('examinar','mesa');walk('edran_canal_refugio');note('observar');talk('edran_oren','ayuda');note('examinar','manta');walk('edran_canal_compuerta');note('edran_rodeo_compuerta');note('edran_recoger_caja');walk('edran_canal_entrada');note('edran_devolver_caja');talk('edran_nela','canal')
 assert 'sobre las rodillas' in next(e for e in out if e.get('action')=='examinar' and e['room']=='edran_canal_refugio')['narrative'][0]['text']
 for phase_time in [21600,43200,66600,82800]:
  clock.now=phase_time
  walk('korven_almacen_fondo');note('observar');walk('edran_canal_refugio');note('observar')
 assert not state()['character']['combat']
 assert not any(entry['id']=='forajido_camino' for entry in state()['bestiary'])
Path(root/'review/DUNGEON_REPLAY_20261007.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Independent blind route:',sum(x['type']=='step' for x in out),'movement steps')
