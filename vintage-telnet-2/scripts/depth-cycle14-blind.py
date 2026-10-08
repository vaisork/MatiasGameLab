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
 post(client,'/api/account/register',{'username':'nightjourney','password':'isolated-test-password'});c=post(client,'/api/character/create',{'name':'Prueba nocturna','species':'marevyn','class_id':'juramentado','gender':'femenino'}).json
 post(dm,'/api/master/login',{'password':'isolated-test-only'});post(dm,'/api/master/approve',{'character_id':c['character']['id']});act('mover','salir')


 samples=[]
 def sample(tag):
  z=state();samples.append({'tag':tag,'room':z['room']['id'],'ambient':z['ambient'],'scene':z['scene'],'actions':z['actions'],'inventory':z['inventory'],'character':z['character']})
 assert state()['character']['gender']=='femenino'
 walk('lethra_mercado_hojas');sample('Narevia initial market');act('hablar','lethra_nera_mercado',topic='comprar');act('hablar','lethra_nera_mercado',topic='reunión');act('aceptar','narevia_preparativos')
 walk('lethra_taller_fibras');act('hablar','lethra_mira',topic='paño');walk('lethra_plataforma_secado');act('examinar','costuras');act('lethra_elegir_cubierto');walk('lethra_cocina_reunion');act('hablar','lethra_nima',topic='caldo');act('hablar','lethra_nima',topic='preparativos');sample('proposal received')
 walk('lethra_mercado_hojas');before=state()['character']['seals'];act('cobrar','narevia_preparativos');assert state()['character']['seals']==before+6;sample('paid Narevia')
 walk('veyra_huerta_baja');act('observar');walk('vaisgard_mercado');act('hablar','veyra_bela',topic='comprar');sample('Vaisgard market comparison');before=state()['character']['seals'];act('comprar','provision_basica');assert state()['character']['seals']==before-8;sample('Vaisgard purchase')
 walk('korven_almacen_grano');act('observar');walk('brumak_centro');walk('korven_patio_lavado');act('observar');sample('rock detour')
 clock.now=max(clock.now,19*3600)
 walk('veyra_cantera_callada');act('observar');walk('lethra_mercado_hojas');act('hablar','lethra_nera_mercado',topic='reunión');sample('Narevia dusk return')
 walk('lethra_cocina_reunion');act('observar');sample('kitchen return')
 clock.now=max(clock.now,23*3600)
 walk('lethra_muelle_vecinal');act('observar');walk('lethra_mercado_hojas');sample('Narevia night return')
 out={'moves':sum(e['action']=='mover' for e in journey),'distinct_rooms':len({e['room'] for e in journey if e['action']=='mover'}),'events':journey,'samples':samples,'gender':state()['character']['gender']}
 (root/(sys.argv[1] if len(sys.argv)>1 else 'review/DEPTH_CYCLE_14_BLIND.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('moves',out['moves'],'distinct',out['distinct_rooms'])
