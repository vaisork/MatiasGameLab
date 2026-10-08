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
 count=0
 def random(self):self.count+=1;return self.value
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
  return len(path)
 post(dm,'/api/master/login',{'password':'isolated'});cases=[]
 for index,(species,region,target,bypass,origin,care,distance) in enumerate([('vesperi','nhal','nhal_sendero_altura','nhal_rodeo_visible_conocido','velmora_centro','nhal_sala_cuidados',3),('marevyn','lethra','lethra_ribera_oeste','lethra_rodeo_cubierta_conocido','narevia_centro','lethra_sala_cuidados',1)]):
  pair=[]
  for role in ('avoid','fight'):
   p=app.test_client();name=f'{role}{index}';post(p,'/api/account/register',{'username':name,'password':'isolated-password'});created=post(p,'/api/character/create',{'name':name,'species':species,'class_id':'sombra'}).json;post(dm,'/api/master/approve',{'character_id':created['character']['id']});act(p,'mover','salir');actual_distance=walk(p,target);assert actual_distance==distance;pair.append(p)
  a,b=pair;assert any(x['id']=='combatir' and x.get('target')=='forajido_camino' for x in state(a)['actions']);act(a,'examinar_criatura','forajido_camino');act(a,'evaluar','forajido_camino');before=state(a);s=act(a,bypass)
  assert s['character']['xp']==before['character']['xp']==0;assert s['inventory']==before['inventory'];assert s['character']['seals']==20;assert not any(i['id']=='forajido_camino' for i in s['bestiary']);assert not any(x['id']=='combatir' and x.get('target')=='forajido_camino' for x in s['actions']);assert any(x['id']=='combatir' and x.get('target')=='forajido_camino' for x in state(b)['actions'])
  walk(a,origin);walk(a,target);assert not any(x['id']=='combatir' and x.get('target')=='forajido_camino' for x in state(a)['actions'])
  act(b,'combatir','forajido_camino');clock.now+=20;s=state(b);assert s['character']['combat'] is None;assert s['character']['xp']>0;assert s['character']['seals']==20;assert not any(i['id']=='forajido_camino' for i in s['bestiary']);walk(b,care);beforecare=state(b);s=act(b,'recuperacion');assert s['character']['seals']==2 and s['character']['hp']>=90 and s['character']['fatigue']==0
  clock.now+=301;walk(a,origin);walk(a,target);walk(b,origin);walk(b,target);global_after=any(x['id']=='combatir' and x.get('target')=='forajido_camino' for x in state(b)['actions']);assert global_after
  cases.append({'species':species,'target':target,'distanceFromTown':distance,'examinedHumanNotBestiary':True,'personalBypassNoXPItems':True,'secondPlayerThreatPreservedBeforeExpiry':True,'careCost':18,'hpBeforeCare':beforecare['character']['hp'],'hpAfterCare':s['character']['hp'],'secondPlayerThreatAfterExpiryFirstVisitorBypass':global_after})
 rng.value=.9;clock.now+=301;p=app.test_client();post(p,'/api/account/register',{'username':'emptyarrival','password':'isolated-password'});created=post(p,'/api/character/create',{'name':'No forced encounter','species':'marevyn','class_id':'sombra'}).json;post(dm,'/api/master/approve',{'character_id':created['character']['id']});act(p,'mover','salir');walk(p,'lethra_ribera_oeste');count=rng.count
 for _ in range(5):assert not any(x['id']=='combatir' for x in state(p)['actions'])
 assert rng.count==count;assert state(p)['character']['hp']==100
 (root/'review/night-playtest/nearby-encounters.json').write_text(json.dumps({'status':'PASS','scope':'Real arrival/examine/evaluate/personal bypass, second account minor fight, local care and no-encounter roll caching','cases':cases,'snapshotTriggeredEncounterRerolls':False,'rngCallsBeforeSnapshots':count,'rngCallsAfterSnapshots':rng.count},ensure_ascii=False,indent=2));print('PASS nearby human and care journeys; personal cache observations recorded')
