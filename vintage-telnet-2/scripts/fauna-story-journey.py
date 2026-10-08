"""Live HTTP fauna reading; authored fields, RNG and route explicit, no combat fixtures."""
import json,uuid,time,urllib.request,http.cookiejar,os
from pathlib import Path
from collections import deque
root=Path(__file__).resolve().parents[1];base='http://127.0.0.1:8119';stage=os.environ.get('VT_FAUNA_STAGE','pass1-before');pass_id=int(stage[4]);rooms={}
for p in (root/'content/regions').glob('*.json'):rooms.update(json.loads(p.read_text())['rooms'])
def client():return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
c=client();dm=client();events=[];observations=[];moves=0

def request(client,path,data=None):
 if data is not None:
  token=json.load(client.open(base+'/api/state'))['csrf_token'];req=urllib.request.Request(base+path,json.dumps({**data,'csrf_token':token}).encode(),{'Content-Type':'application/json'})
 else:req=base+path
 return json.load(client.open(req))
def state():return request(c,'/api/state')
def act(id,target=None,**kw):
 global moves
 s=request(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4()),**kw});moves+=id=='mover';events.append({'action':id,'target':target,'room':s['room']['id'],'narrative':s.get('narrative'),'hp':s['character']['hp']});return s

def walk(dest):
 here=state()['room']['id']
 if here.startswith('home:'):act('mover','salir');here=state()['room']['id']
 q=deque([(here,[])]);seen={here}
 while q:
  room,path=q.popleft()
  if room==dest:break
  for direction,to in rooms[room].get('exits',{}).items():
   if to not in seen:seen.add(to);q.append((to,path+[direction]))
 else:raise AssertionError(dest)
 for direction in path:
  s=state();move=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
  if move.get('disabled'):
   permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'))
  act('mover',direction)
species={1:'humano',2:'marevyn',3:'dravak'}[pass_id];name='faunastory'+str(time.time_ns());request(c,'/api/account/register',{'username':name,'password':'isolated-password'});created=request(c,'/api/character/create',{'name':'Fauna paso '+str(pass_id),'species':species,'class_id':'juramentado','gender':'femenino'});request(dm,'/api/master/login',{'password':'isolated-review-only'});request(dm,'/api/master/approve',{'character_id':created['character']['id']})
selected={1:['edran_salida_huertos','edran_surcos','edran_arboleda','edran_camino_carros','edran_terraplen','edran_linde_piedra','edran_sendero_juncos','edran_parcela_vieja','edran_sauces','edran_calzada','edran_sendero_regreso'],2:['lethra_ribera_seca','lethra_tierra_esponjosa','lethra_juncal_abierto','lethra_tablas_primeras','lethra_ribera_firme','lethra_pasarela_curva','lethra_senda_elevada','lethra_banco_barro','lethra_hito_tierra','lethra_ribera_sombra','nhal_arbol_umbral','nhal_suelo_hojas','nhal_tronco_acostado','nhal_corteza_clara','nhal_raices_altas','nhal_piedras_musgo','nhal_helechos_bajos','nhal_umbral_velmora','nhal_claro_silencio','nhal_ribera_relevo','nhal_senda_recipiente','nhal_rincon_semillas','nhal_agua_sombreada','lethra_orilla_silente','nhal_raiz_marcada'],3:['korven_loma_cascajo','korven_meseta_baja','korven_cauce_observacion','korven_desvio_horno','korven_roca_cascaron','hoshai_estribacion','hoshai_repecho_raices','hoshai_pared_goteo','hoshai_pinar_discontinuo','hoshai_agua_fria','hoshai_ladera_hitos','hoshai_cuello_roca','hoshai_escalones_sol','hoshai_collado_pino','hoshai_aprisco_abierto','hoshai_garganta_oeste','hoshai_senda_dosel','edran_prado']}[pass_id]
for roll in ([0,.2,.375] if pass_id==3 else [0]):
 request(c,'/__isolated/roll',{'value':roll})
 if roll:request(c,'/__isolated/advance',{'seconds':300});request(c,'/__isolated/advance',{'seconds':1})
 for dest in selected:
  walk(dest);s=act('observar');observations.append({'room':dest,'roll':roll,'narrative':s['narrative'],'actions':[a for a in s['actions'] if a['id'] in ['examinar_criatura','evaluar','acercarse','retirarse','combatir']],'bestiary':[e['id'] for e in s['bestiary']]})
  for choice in [a for a in s['actions'] if a['id']=='examinar_criatura']:act('examinar_criatura',choice['target'])
  if pass_id==2:
   for choice in [a for a in state()['actions'] if a['id']=='acercarse']:act('acercarse',choice['target']);act('retirarse',choice['target'])
assert moves>=20,moves
out={'stage':stage,'moves':moves,'actions':len(events),'observations':observations,'events':events,'final':state(),'scope':'Live API and fresh temporary DB; constant RNG rolls declared; no HP/flags edits, no mandatory fights'};outdir=root/'review/fauna-stories';outdir.mkdir(exist_ok=True);(outdir/(stage+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({'stage':stage,'moves':moves,'observations':len(observations),'actions':len(events)}))
