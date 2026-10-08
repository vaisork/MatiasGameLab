"""Regional combat replay: DM approval and high-level fixtures ONLY in temporary DB."""
import sys,json,tempfile,uuid,os,shutil
from pathlib import Path
from collections import deque
root=Path(__file__).resolve().parents[1];sys.path[:0]=[str(root),str(root/'runtime/python-deps')]
from server.app import create_app
from server.content import Content
from server import mechanics as m
from werkzeug.security import generate_password_hash
class Clock:
 now=43200
 def __call__(self):return self.now
class RNG:
 value=.6
 def random(self):return self.value
if os.environ.get('VT_DEPTH7_BASELINE'):
 for cid in ('rasgacumbres','quebrarrocas','dorsalodo','rasgacorteza'):m.PROFILES[cid]=dict(m.PROFILES['cornalomo'],family=cid)
clock=Clock();rng=RNG();rooms=Content(root/'content').rooms;results=[];moves=0
with tempfile.TemporaryDirectory(prefix='vt-depth7-') as tmp:
 app=create_app({'TESTING':True,'DATA_DIR':tmp,'CLOCK':clock,'RNG':rng,'DM_PASSWORD_HASH':generate_password_hash('isolated')});dm=app.test_client();store=app.extensions.get('store')
 if store is None:
  from server.store import Store
  store=Store(Path(tmp)/'world.sqlite3')
 def post(c,p,data):return c.post(p,json={**data,'csrf_token':c.get('/api/state').json['csrf_token']})
 post(dm,'/api/master/login',{'password':'isolated'})
 for species,cid in [('felaryn','rasgacumbres'),('dravak','quebrarrocas'),('marevyn','dorsalodo'),('vesperi','rasgacorteza')]:
  dest=next(k for k,r in rooms.items() if any(s.get('creature')==cid and not s.get('trace_only') for s in [*r.get('signals',[]),*r.get('wildlife_pool',[])]))
  for cls in (['artifice'] if os.environ.get('VT_DEPTH7_ADAPT') else m.CLASSES):
   clock.now+=301;rng.value=.375
   c=app.test_client();name=cid+cls;post(c,'/api/account/register',{'username':name,'password':'isolated-password'});new=post(c,'/api/character/create',{'name':name,'species':species,'class_id':cls}).json;charid=new['character']['id'];post(dm,'/api/master/approve',{'character_id':charid})
   # No administrative stat endpoint exists. Seed only this authorised temporary fixture.
   with store.transaction() as db:
    char=store.load(db.execute('SELECT * FROM characters WHERE id=?',(charid,)).fetchone());char['state']['level']=8;char['state']['attributes']=dict.fromkeys(m.ATTRIBUTES,20);char['state']['hp']=m.hp_max(char['state']);store.save(db,char)
   def state():return c.get('/api/state').json
   def act(id,target=None):
    global moves
    r=post(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4())});assert r.status_code==200,(id,target,r.json);moves+=id=='mover';return r.json
   act('mover','salir');start=state()['room']['id'];q=deque([(start,[])]);seen={start}
   while q:
    here,path=q.popleft()
    if here==dest:break
    for direction,to in rooms[here].get('exits',{}).items():
     if to not in seen:seen.add(to);q.append((to,path+[direction]))
   assert here==dest
   for direction in path:
    move=next(a for a in state()['actions'] if a['id']=='mover' and a.get('target')==direction)
    if move.get('disabled'):
     permit=next(a for a in state()['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'))
    act('mover',direction)
   rng.value=.6;act('observar');evaluation=act('evaluar',cid)['narrative'];act('acercarse',cid);withdraw=act('retirarse',cid)['narrative'];start=act('acercarse',cid);start=act('combatir',cid);cap=next(a for a in start['actions'] if a['id']=='capacidad');hp=start['character']['hp'];prepared=start['character']['combat']['prepared_action'];adapt=bool(os.environ.get('VT_DEPTH7_ADAPT')) and prepared and not prepared.get('interruptible',False);choice='capacidad' if not cap.get('disabled') and not adapt else 'defender';act(choice,None if choice=='capacidad' else 'esquivar');clock.now+=4;response=state();rng.value=0;act('huir');clock.now+=4;escaped=state();rng.value=.6;assert escaped['character']['combat'] is None
   results.append({'creature':cid,'source':'authored dynamic wildlife_pool' if cid in ('rasgacumbres','quebrarrocas') else 'authored static signal','class':cls,'room':dest,'evaluation':evaluation,'withdrawal':withdraw,'prepared':start['character']['combat']['prepared_action'],'startNarrative':start['narrative'],'capability':cap,'choice':choice,'damage':hp-response['character']['hp'],'response':response['narrative'],'escaped':True})
 assert moves>=20,moves
 (root/os.environ.get('VT_DEPTH7_OUTPUT','review/archive/2026-10-07/depth-cycle7-before.json')).write_text(json.dumps({'moves':moves,'fixtures':'DM-approved accounts; level8/attributes20 seeded only temporary Store; ordinary class equipment','cases':results},ensure_ascii=False,indent=2));print('PASS',moves,len(results))
