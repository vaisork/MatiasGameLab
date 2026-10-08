"""Gameplay replay in disposable API database; deterministic clock/RNG, no production writes."""
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
with tempfile.TemporaryDirectory(prefix='vt-veyra-review-') as tmp:
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
 s=post(c,'/api/character/create',{'name':'Lector regional','species':'marevyn','class_id':'juramentado','gender':'masculino'})
 post(dm,'/api/master/login',{'password':'temporary-cycle2-only'});post(dm,'/api/master/approve',{'character_id':s['character']['id']});act('mover','salir')
 def talk(npc,topic):
  result=post(c,'/api/action',{'id':'hablar','target':npc,'topic':topic,'request_id':str(uuid.uuid4())});out.append({'type':'conversation','room':state()['room']['id'],'npc':npc,'topic':topic,'narrative':result['narrative']});return result
 walk('veyra_patio_senales');act('aceptar','vaisgard_aviso_carga')
 walk('veyra_puerta_piedra');act('veyra_anotar_demora');talk('veyra_tov','aviso')
 walk('veyra_archivo_cargas');act('veyra_aclarar_demora');talk('veyra_nera','aviso_preciso');talk('veyra_nera','cargas')
 walk('veyra_patio_senales');paid=act('cobrar','vaisgard_aviso_carga');out.append({'type':'payment','narrative':paid['narrative']})
 walk('veyra_puerta_piedra');remembered=talk('veyra_tov','carga');assert 'junto a la puerta' in ' '.join(e['text'] for e in remembered['narrative']);assert not any('señala en el archivo' in e['text'] for e in remembered['narrative']);out.append({'type':'memory-location-check','room':state()['room']['id'],'narrative':remembered['narrative']})
 for phase,start in [('Amanecer',6*3600),('Día',12*3600),('Atardecer',18*3600),('Noche',22*3600)]:
  clock.now+=86400;clock.now=clock.now//86400*86400+start
  for dest in ['veyra_cantera_callada','veyra_patio_agua','veyra_huerta_baja','veyra_colina_vista','veyra_patio_senales','veyra_archivo_cargas']:
   walk(dest);observed=act('observar');
   if dest=='veyra_colina_vista':assert 'Desde la colina ves caminos' not in ' '.join(e['text'] for e in state()['scene'])
   out.append({'type':'observation','room':dest,'ambient':state()['ambient'],'scene':state()['scene'],'observe':observed['narrative']})
 # Choose a dry daylight moment using the existing clock/weather cycle; no flags seeded.
 for hour in range(8,18):
  clock.now=clock.now//86400*86400+hour*3600
  if Engine(content,clock).ambient(content.rooms['veyra_huerta_baja'],{})['weather']!='Lluvia':break
 walk('veyra_huerta_baja');before=state();Path('/tmp/vt-huerta-review-state.json').write_text(json.dumps(before));placed=act('veyra_colocar_tabla_riego')
 assert placed['character']['seals']==before['character']['seals'] and placed['character']['xp']==before['character']['xp']
 assert placed['inventory']==before['inventory']
 assert not any(a['id']=='veyra_colocar_tabla_riego' for a in placed['actions'])
 walk('veyra_colina_vista');walk('veyra_huerta_baja');checked=act('examinar','tabla');assert 'queda sujeta' in checked['narrative'][0]['text'];out.append({'type':'irrigation-return','narrative':checked['narrative']})
 walk('lethra_muelle_vecinal');act('observar')
 walk('narevia_centro');act('mover','hogar');assert not state()['character']['combat']
Path(root/'review/narrative/VEYRA_RETURN_20261007.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Veyra route:',sum(x['type']=='step' for x in out),'movement steps')
