"""Real HTTP journey; isolated server only, no database edits or fixtures."""
import json,uuid,time,urllib.request,http.cookiejar,os
from pathlib import Path
from collections import deque
root=Path(__file__).resolve().parents[1];base=os.environ.get('VT_COMMERCE_BASE','http://127.0.0.1:8112');rooms={}
for p in (root/'content/regions').glob('*.json'):rooms.update(json.loads(p.read_text())['rooms'])
def client():return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
c=client();dm=client();log=[];evidence=[];moves=0

def request(client,path,data=None):
 if data is not None:
  token=json.load(client.open(base+'/api/state'))['csrf_token'];data={**data,'csrf_token':token};req=urllib.request.Request(base+path,json.dumps(data).encode(),{'Content-Type':'application/json'})
 else:req=base+path
 return json.load(client.open(req))
def state():return request(c,'/api/state')
def record(label,s):
 log.append({'action':label,'room':s.get('room',{}).get('id'),'character':s.get('character'),'inventory':s.get('inventory'),'narrative':s.get('narrative'),'actions':s.get('actions')})
 return s

def act(id,target=None,**kw):
 global moves
 s=request(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4()),**kw});moves+=id=='mover';return record({'id':id,'target':target,**kw},s)
def walk(dest):
 here=state()['room']['id'];q=deque([(here,[])]);seen={here}
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
 evidence.append({'destination':dest,'steps':len(path)})
name='commerce12'+str(time.time_ns());request(c,'/api/account/register',{'username':name,'password':'isolated-password'});new=request(c,'/api/character/create',{'name':'Regreso de Brumak','species':'dravak','class_id':'juramentado'});request(dm,'/api/master/login',{'password':'isolated-review-only'});request(dm,'/api/master/approve',{'character_id':new['character']['id']});act('mover','salir')
walk('korven_loma_cascajo');act('buscar');walk('korven_taller_juntas');act('hablar','korven_beran',topic='armas');shop=state();evidence.append({'shopBefore':shop['actions'],'inventoryBefore':shop['inventory']})
act('hablar','korven_beran',topic='afinado');weapon=next(i for i in shop['inventory'] if i['kind']=='weapon');damage=weapon['damage'];before=state()['character']['seals'];s=act('afinar',weapon['id'],confirmed=True);assert next(i for i in s['inventory'] if i['id']==weapon['id'])['damage']==damage+1;assert s['character']['seals']==before-12;evidence.append({'honed':weapon['id'],'beforeDamage':damage,'afterDamage':damage+1,'event':s['narrative']})
walk('korven_entrante_piezas');act('buscar');act('hablar','korven_taren',topic='medidas');before=state()['character']['seals'];s=act('vender','piedra_veteada');assert s['character']['seals']==before+2
walk('korven_taller_juntas');s=act('comprar','provision_basica');assert s['character']['seals']==before+2-8
walk('lethra_mercado_hojas');act('observar');act('hablar','lethra_nera_mercado',topic=next(a['topic'] for a in state()['actions'] if a['id']=='hablar' and a['target']=='lethra_nera_mercado'))
walk('korven_roca_cascaron');act('observar');act('examinar_criatura','cascapedernal');act('evaluar','cascapedernal');act('combatir','cascapedernal');request(c,'/__isolated/advance',{'seconds':40});s=record('combat +40s',state());assert not s['character']['combat'];assert s['character']['hp']>0;assert s['character']['xp']>0;evidence.append({'postCombat':s['character'],'loot':s['inventory']})
act('usar','provision_basica');walk('korven_taller_juntas');act('hablar','korven_beran',topic='armas');walk('korven_cauce_duro');act('buscar');walk('korven_entrante_piezas');before=state()['character']['seals'];s=act('vender','piedra_veteada');evidence.append({'postCombatSale':s['character']['seals']-before})
walk('korven_taller_juntas');act('hablar','korven_beran',topic='afinado');walk('brumak_centro');act('mover','hogar')
rest=next(a for a in state()['actions'] if a['id']=='descansar')
if rest.get('disabled'):
 assert state()['character']['hp']==state()['character']['hp_max'] and state()['character']['fatigue']==0
 record('No descanso adicional necesario: recuperación completa',state())
else:act('descansar')
assert moves>=20
out={'scope':'Real HTTP isolated DB; fresh level1 Dravak Juramentado; no fixture/inventory edits','moves':moves,'events':log,'evidence':evidence,'final':state()};out['final'].pop('csrf_token',None);(root/os.environ.get('VT_COMMERCE_OUTPUT','review/depth-cycle12-commerce-before.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({'moves':moves,'actions':len(log),'finalRoom':out['final']['room']['id'],'finalSeals':out['final']['character']['seals']}))
