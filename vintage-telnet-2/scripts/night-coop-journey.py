"""Real authored-world cooperative/withdrawal journey with three isolated accounts."""
import sys,json,tempfile,uuid
from pathlib import Path
from collections import deque
root=Path(__file__).resolve().parents[1];sys.path[:0]=[str(root),str(root/'runtime/python-deps')]
from server.app import create_app
from werkzeug.security import generate_password_hash
class Clock:
 now=43200
 def __call__(self):return self.now
class RNG:
 value=0
 def random(self):return self.value
clock=Clock();rng=RNG();rooms={}
for p in (root/'content/regions').glob('*.json'):rooms.update(json.loads(p.read_text())['rooms'])
with tempfile.TemporaryDirectory(prefix='vt-coop-') as tmp:
 app=create_app({'TESTING':True,'DATA_DIR':tmp,'CLOCK':clock,'RNG':rng,'DM_PASSWORD_HASH':generate_password_hash('isolated')});dm=app.test_client()
 def state(c):return c.get('/api/state').json
 def post(c,p,data):return c.post(p,json={**data,'csrf_token':state(c)['csrf_token']})
 def act(c,id,target=None,**extra):
  r=post(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4()),**extra});assert r.status_code==200,(id,target,r.json);return r.json
 def walk(c,dest):
  q=deque([(state(c)['room']['id'],[])]);seen=set();path=None
  while q:
   here,steps=q.popleft()
   if here==dest:path=steps;break
   for direction,to in rooms.get(here,{}).get('exits',{}).items():
    if to not in seen:seen.add(to);q.append((to,steps+[direction]))
  assert path is not None
  for direction in path:
   move=next(a for a in state(c)['actions'] if a['id']=='mover' and a.get('target')==direction)
   if move.get('disabled'):
    permit=next(a for a in state(c)['actions'] if a['id'].startswith('pedir_permiso'));act(c,permit['id'],permit.get('target'))
   act(c,'mover',direction)
 post(dm,'/api/master/login',{'password':'isolated'});players=[]
 for name,cls in [('front','juramentado'),('partner','artifice'),('observer','sombra')]:
  c=app.test_client();post(c,'/api/account/register',{'username':name,'password':'isolated-password'});r=post(c,'/api/character/create',{'name':name,'species':'felaryn','class_id':cls});post(dm,'/api/master/approve',{'character_id':r.json['character']['id']});act(c,'mover','salir');walk(c,'hoshai_taller_apoyos');act(c,'aceptar','khariel_polea');walk(c,'hoshai_campamento_lona');players.append(c)
 a,b,c=players;act(a,'combatir','forajido_camino');act(b,'combatir','forajido_camino');clock.now+=4;first=[state(p) for p in players]
 assert first[0]['character']['combat']['hp']==first[1]['character']['combat']['hp'];assert first[0]['character']['hp']==95;assert first[1]['character']['hp']==100;assert first[2]['character']['xp']==0
 act(a,'huir');clock.now+=4;resolved=[state(p) for p in players]
 assert all(s['character']['combat'] is None for s in resolved);assert resolved[0]['character']['xp']==0;assert resolved[1]['character']['xp']>0;assert resolved[2]['character']['xp']==0
 assert all(s['character']['seals']==20 and not any(i['id']=='forajido_camino' for i in s['bestiary']) for s in resolved)
 for p in players:walk(p,'hoshai_cajas_camino')
 offered=[any(x['id']=='hoshai_recoger_polea_tras_pelea' for x in state(p)['actions']) for p in players];assert offered==[False,True,False]
 act(b,'hoshai_recoger_polea_tras_pelea');walk(b,'hoshai_taller_apoyos');act(b,'hoshai_entregar_polea');paid=act(b,'cobrar','khariel_polea');assert paid['character']['seals']==28
 for p in (a,c):
  walk(p,'hoshai_taller_apoyos');assert not any(x['id']=='cobrar' and x.get('target')=='khariel_polea' for x in state(p)['actions']);assert state(p)['character']['seals']==20
 report={'status':'PASS','scope':'Three real accounts; two co-op attacks against one human, one retreats before victory, observer remains; only surviving real contributor opens local quest combat branch and earns paid delivery','firstRound':[{'hp':s['character']['hp'],'enemyHp':s['character']['combat']['hp'] if s['character']['combat'] else None} for s in first],'resolvedXP':[s['character']['xp'] for s in resolved],'combatBranchOffered':offered,'questPaidSeals':paid['character']['seals']}
 supporters=[]
 for name,cls in [('focusfront','juramentado'),('focuspartner','sombra')]:
  p=app.test_client();post(p,'/api/account/register',{'username':name,'password':'isolated-password'});created=post(p,'/api/character/create',{'name':name,'species':'marevyn','class_id':cls}).json;post(dm,'/api/master/approve',{'character_id':created['character']['id']});act(p,'mover','salir');walk(p,'lethra_ribera_oeste');supporters.append(p)
 front,shadow=supporters;act(front,'combatir','forajido_camino');act(shadow,'combatir','forajido_camino');act(shadow,'capacidad');rng.value=.39;clock.now+=4;first_focus=[state(p) for p in supporters];assert first_focus[0]['character']['hp']==100;assert first_focus[0]['character']['combat']['hp']==18
 rng.value=.5;clock.now+=4;second_focus=[state(p) for p in supporters];assert second_focus[0]['character']['combat']['hp']==10;assert second_focus[1]['character']['combat']['hp']==10;assert any('8 de daño' in e['text'] for e in second_focus[1]['narrative']);report['supportingSombra']={'firstRoundEnemyHP':18,'secondRoundEnemyHP':10,'primaryHP':100,'normalAttackRollPercent':50,'normalAccuracy':40,'openingAccuracy':55,'scope':'Actual cooperative support power makes enemy response miss and enables supporter next attack with otherwise failing roll'}
 (root/'review/night-playtest/coop-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('PASS cooperative human/withdrawal/quest participant credit')
