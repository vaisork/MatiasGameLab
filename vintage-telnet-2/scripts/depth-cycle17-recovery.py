"""Actual death and dungeon recovery through live HTTP; no HP or progress fixtures."""
import json,uuid,time,urllib.request,http.cookiejar,os
from pathlib import Path
from collections import deque
root=Path(__file__).resolve().parents[1];base='http://127.0.0.1:8117';rooms={}
for p in (root/'content/regions').glob('*.json'):rooms.update(json.loads(p.read_text())['rooms'])
def client():return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
dm=client();events=[];summary=[];moves=0

def request(c,path,data=None):
 if data is not None:
  token=json.load(c.open(base+'/api/state'))['csrf_token'];req=urllib.request.Request(base+path,json.dumps({**data,'csrf_token':token}).encode(),{'Content-Type':'application/json'})
 else:req=base+path
 return json.load(c.open(req))
def state(c):return request(c,'/api/state')
def record(label,s,case):events.append({'case':case,'action':label,'room':s['room']['id'],'character':s['character'],'inventory':s['inventory'],'map':s['map'],'narrative':s.get('narrative'),'actions':s['actions']});return s

def act(c,id,target=None,case='death',**kw):
 global moves
 s=request(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4()),**kw});moves+=id=='mover';return record({'id':id,'target':target,**kw},s,case)
def walk(c,dest,case='death'):
 here=state(c)['room']['id']
 if here.startswith('home:'):act(c,'mover','salir',case);here=state(c)['room']['id']
 q=deque([(here,[])]);seen={here}
 while q:
  room,path=q.popleft()
  if room==dest:break
  for direction,to in rooms[room].get('exits',{}).items():
   if to not in seen:seen.add(to);q.append((to,path+[direction]))
 else:raise AssertionError(dest)
 for direction in path:
  s=state(c);move=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
  if move.get('disabled'):
   permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(c,permit['id'],permit.get('target'),case)
  act(c,'mover',direction,case)
 return len(path)
def create(species,cls,suffix):
 c=client();name='recovery17'+str(time.time_ns())+suffix;request(c,'/api/account/register',{'username':name,'password':'isolated-password'});s=request(c,'/api/character/create',{'name':'Recuperación '+suffix,'species':species,'class_id':cls,'gender':'femenino'});request(dm,'/api/master/approve',{'character_id':s['character']['id']});return c
request(dm,'/api/master/login',{'password':'isolated-review-only'})
a=create('felaryn','sombra','death')
walk(a,'hoshai_escalones_sol');act(a,'buscar');walk(a,'vaisgard_mercado');act(a,'hablar','veyra_bela',topic='cuidados');walk(a,'lethra_juncal_abierto');act(a,'buscar');walk(a,'nhal_mercado_setas');act(a,'observar');walk(a,'edran_prado');act(a,'observar');act(a,'acercarse','cornalomo');before=state(a);act(a,'combatir','cornalomo');request(a,'/__isolated/advance',{'seconds':40});fallen=record('combat advanced 40s',state(a),'death');assert fallen['character']['combat'] is None;assert fallen['character']['hp']==60;assert fallen['character']['fatigue']==40;assert fallen['room']['id']=='brumak_centro';assert fallen['map']['edges']==before['map']['edges'];assert fallen['character']['seals']==before['character']['seals'];assert fallen['inventory']==before['inventory'];summary.append({'deathActual':fallen['narrative'],'source':'edran_prado','recovery':'brumak_centro','noFalseRoute':True,'naturalLevel':fallen['character']['level']})
r1=act(a,'descansar');r2=act(a,'descansar')
if os.environ.get('VT_RECOVERY_PHASE')=='after':
 resting=next(action for action in r2['actions'] if action['id']=='descansar');assert resting.get('disabled'),resting
 try:request(a,'/api/action',{'id':'descansar','request_id':str(uuid.uuid4())})
 except urllib.error.HTTPError as error:
  assert error.code==409;rejection=json.loads(error.read())
 else:raise AssertionError('Exhausted rest must be rejected')
 r3=record('rest disabled and rejected 409',state(a),'death');assert r3['character']==r2['character'];assert r3['inventory']==r2['inventory'];assert r3['map']==r2['map']
 rest_check={'thirdRestDisabled':True,'reason':resting.get('reason'),'rejection':rejection,'unchangedAfterRejection':True}
else:
 r3=act(a,'descansar');rest_check={'thirdRestNarrative':r3['narrative']}
summary.append({'restHp':[fallen['character']['hp'],r1['character']['hp'],r2['character']['hp'],r3['character']['hp']],'restFatigue':[fallen['character']['fatigue'],r1['character']['fatigue'],r2['character']['fatigue'],r3['character']['fatigue']],**rest_check,'thirdRestActions':r3['actions']})
walk(a,'korven_sala_cuidados');act(a,'hablar','korven_neru',topic='atención');paid=act(a,'recuperacion');summary.append({'recoveryCost':20-paid['character']['seals'],'hp':paid['character']['hp'],'fatigue':paid['character']['fatigue']});act(a,'descansar');walk(a,'edran_prado');act(a,'observar');act(a,'acercarse','cornalomo');act(a,'retirarse','cornalomo');summary.append({'returnedWalking':True,'hp':state(a)['character']['hp']})
# A second character plays the authored canal, then sells a real road finding.
b=create('humano','arcano','canal');walk(b,'edran_surcos','canal');act(b,'buscar',case='canal');walk(b,'edran_canal_entrada','canal');act(b,'hablar','edran_nela',case='canal',topic='canal');walk(b,'edran_canal_refugio','canal');act(b,'hablar','edran_oren',case='canal',topic='caja');walk(b,'edran_canal_compuerta','canal');act(b,'combatir','forajido_camino',case='canal');request(b,'/__isolated/advance',{'seconds':32});won=record('canal combat advanced 32s',state(b),'canal');assert won['character']['combat'] is None;assert won['character']['xp']>0;assert 'forajido_camino' not in [i['id'] for i in won['bestiary']];walk(b,'edran_canal_repisa','canal');act(b,'edran_recoger_caja',case='canal');walk(b,'edran_canal_entrada','canal');act(b,'edran_devolver_caja',case='canal');walk(b,'valdren_comedor','canal');sold=act(b,'vender','semillas_camino',case='canal');used=act(b,'usar','provision_basica',case='canal');walk(b,'valdren_plaza','canal');act(b,'mover','hogar','canal');summary.append({'canalVictory':won['narrative'],'materialSaleSeals':sold['character']['seals'],'provisionHp':used['character']['hp'],'home':state(b)['room']['id']})
out={'scope':'Two natural level1 characters; real HTTP temporary DB; RNG0, clock43200 and controlled combat advances; no HP/flags/inventory edits','moves':moves,'events':events,'summary':summary,'deathFinal':state(a),'canalFinal':state(b)};(root/os.environ.get('VT_RECOVERY_OUTPUT','review/archive/2026-10-07/depth-cycle17-recovery-before.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({'moves':moves,'actions':len(events),'summaries':len(summary)}))
