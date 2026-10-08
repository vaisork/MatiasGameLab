import sys,json,tempfile,secrets
from pathlib import Path
root=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(root/'runtime/python-deps'),str(root)]
from server.app import create_app
from werkzeug.security import generate_password_hash
root=next(p for p in Path(__file__).resolve().parents if (p/'CONTENT_CONTRACT.md').exists())
class Clock:
 now=14*3600
 def __call__(self):return self.now
clock=Clock();records=[]
master_password=secrets.token_urlsafe(24);account_password=secrets.token_urlsafe(24)
with tempfile.TemporaryDirectory(prefix='new-reader-') as data:
 app=create_app({'TESTING':True,'DATA_DIR':data,'CLOCK':clock,'DM_PASSWORD_HASH':generate_password_hash(master_password)});client=app.test_client();master=app.test_client()
 def post(who,path,payload):
  csrf=who.get('/api/state').json['csrf_token'];response=who.post(path,json=dict(payload,csrf_token=csrf));assert response.status_code in(200,201),(path,response.status_code,response.json);return response.json
 post(client,'/api/account/register',{'username':'readeronly','password':account_password})
 char=post(client,'/api/character/create',{'name':'Lectora','species':'humanos','class_id':'sombra'})['character']
 post(master,'/api/master/login',{'password':master_password});post(master,'/api/master/approve',{'character_id':char['id']})
 sequence=0
 def action(id,target=None,topic=None):
  global sequence
  sequence+=1;payload={'id':id,'request_id':f'new-reader-action-{sequence}'}
  if target is not None:payload['target']=target
  if topic is not None:payload['topic']=topic
  if topic is not None:payload['topic']=topic
  snapshot=post(client,'/api/action',payload);records.append({'step':sequence,'action':payload,'snapshot':snapshot});return snapshot
 state=action('mover','salir')

 from server.content import Content
 from collections import deque
 content=Content(root/'content');checks=[]
 def travel(destination):
  global state
  queue=deque([(state['room']['id'],[])]);seen=set()
  while queue:
   node,path=queue.popleft()
   if node==destination:break
   if node in seen:continue
   seen.add(node)
   for direction,target in content.rooms[node]['exits'].items():queue.append((target,path+[direction]))
  else:raise AssertionError(destination)
  for direction in path:state=action('mover',direction)
 def condition(label,actionid,present,phase=None,weather=None):
  global state
  for hour in range(24,120):
   clock.now=hour*3600;state=client.get('/api/state').json
   ambient=state['ambient']
   if (not phase or ambient['time_of_day'].lower()==phase) and (not weather or ambient['weather'].lower()==weather):break
  else:raise AssertionError((phase,weather))
  offered=any(a['id']==actionid for a in state['actions']);assert offered==present,(label,ambient,state['actions'])
  if not present:
   response=client.post('/api/action',json={'id':actionid,'request_id':'guard-'+label,'csrf_token':state['csrf_token']});assert response.status_code>=400,(label,response.json)
  checks.append({'case':label,'expected_available':present,'snapshot':state})

 checkpoints=[]
 destinations=['valdren_pozo','valdren_comedor','valdren_patio_ropa','valdren_cuidado','valdren_patio_carros','valdren_graneros','edran_estanque','edran_bajo_humedo','edran_estanque','edran_sauces','edran_puente_juncos','lethra_hito_tierra','lethra_escucha_aves','lethra_ribera_oeste','narevia_centro','lethra_cuidado_barcas','lethra_orilla_silente','lethra_banco_barro']
 for index,destination in enumerate(destinations):
  clock.now=(48+index)*3600;travel(destination);state=client.get('/api/state').json
  checkpoint={'room':destination,'arrival':state}
  state=action('observar');checkpoint['observation']=state
  for a in state['actions']:
   if a['id']=='hablar':state=action('hablar',a['target'],a['topic']);checkpoint['conversation']=state;break
  checkpoints.append(checkpoint)
 clock.now=66*3600;state=client.get('/api/state').json;checkpoints.append({'room':state['room']['id'],'dusk':state});state=action('observar')
 def sanitize(value):
  if isinstance(value,dict):return {k:sanitize(v) for k,v in value.items() if k not in ('csrf_token','account','characters')}
  if isinstance(value,list):return [sanitize(v) for v in value]
  return value
 import hashlib
 evidence={'scope':'Independent quiet Edran reader route followed by Lethra branches; public authenticated API, isolated DB; guided by authored topology, controlled test clock, no direct position/knowledge/flag writes; no browser or human-session claim','species':'humanos','checkpoints':checkpoints,'records':records,'hashes':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'content').rglob('*.json')}}
 (root/'review/narrative/API_READER_EDRAN.json').write_text(json.dumps(sanitize(evidence),ensure_ascii=False,indent=2))
 print('FINAL PASS',len(records),'actions',len(checkpoints),'checkpoints',sorted({r['snapshot']['ambient']['time_of_day'] for r in records}))
