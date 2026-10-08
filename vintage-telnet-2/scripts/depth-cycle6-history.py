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
 def random(self):return 0
root=Path(__file__).resolve().parents[1]; rooms={}
for p in (root/'content/regions').glob('*.json'):rooms.update(json.loads(p.read_text())['rooms'])
clock=Clock(); evidence=[]; journey=[]
with tempfile.TemporaryDirectory(prefix='vt-night-integration-') as tmp:
 app=create_app({'TESTING':True,'DATA_DIR':tmp,'CLOCK':clock,'RNG':RNG(),'DM_PASSWORD_HASH':generate_password_hash('isolated-test-only')});client=app.test_client();dm=app.test_client()
 def post(c,p,data):
  csrf=c.get('/api/state').json['csrf_token'];return c.post(p,json={**data,'csrf_token':csrf})
 def state():return client.get('/api/state').json
 def act(id,target=None,**extra):
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
 post(client,'/api/account/register',{'username':'nightjourney','password':'isolated-test-password'});c=post(client,'/api/character/create',{'name':'Prueba nocturna','species':'felaryn','class_id':'sombra'}).json
 post(dm,'/api/master/login',{'password':'isolated-test-only'});post(dm,'/api/master/approve',{'character_id':c['character']['id']});act('mover','salir')
 walk('hoshai_escalones_sol');s=act('buscar');assert any(i['id']=='resina_pino' for i in s['inventory']);walk('hoshai_mercado_cintas')
 before=state()['character']['seals'];s=act('vender','resina_pino');assert s['character']['seals']==before+2;s=act('comprar','provision_basica');assert s['character']['seals']==before+2-8;evidence.append({'commerce':'regional finding → local sale → provision purchase','seals':s['character']['seals']})
 act('aceptar','khariel_cornisa');walk('hoshai_balcon_valle');act('examinar','cornisa');act('hoshai_marcar_cornisa');walk('hoshai_mercado_cintas');act('hablar','hoshai_luma',topic='cornisa');s=act('cobrar','khariel_cornisa');assert s['character']['seals']==20;evidence.append({'local_quest':'cornice decision communicated to Luma','paid':6})
 walk('hoshai_taller_apoyos');act('aceptar','khariel_polea');walk('hoshai_campamento_lona');act('hablar','hoshai_seran',topic='cuenta');act('hablar','hoshai_seran',topic='acuerdo');walk('hoshai_cajas_camino');act('hoshai_recoger_polea');walk('hoshai_taller_apoyos');act('hoshai_entregar_polea');s=act('cobrar','khariel_polea');assert s['character']['seals']==28;assert not any(i['id']=='polea_daren' for i in s['inventory']);evidence.append({'local_quest':'Seran peaceful agreement → recovered pulley → Daren delivery','paid':8,'seals':28})
 walk('edran_canal_entrada');s=state();evidence.append({'dungeon_actions':[{'id':a['id'],'target':a.get('target'),'label':a['label']} for a in s['actions']]})
 act('hablar','edran_nela',topic='canal');walk('edran_canal_refugio');act('hablar','edran_oren',topic='caja');walk('edran_canal_compuerta')
 act('combatir','forajido_camino');clock.now+=24;s=state();assert not s['character']['combat'];assert s['character']['hp']>0;assert 'forajido_camino' not in {i['id'] for i in s['bestiary']};evidence.append({'human_combat':'resolved alive, not added to bestiary','hp':s['character']['hp']})
 walk('edran_canal_repisa');act('edran_recoger_caja');walk('edran_canal_entrada');before_qty=sum(i.get('quantity',1) for i in state()['inventory'] if i['id']=='provision_basica');s=act('edran_devolver_caja');assert sum(i.get('quantity',1) for i in s['inventory'] if i['id']=='provision_basica')==before_qty+1;assert not any(i['id']=='caja_cunas' for i in s['inventory']);evidence.append({'dungeon':'Nela dialogue → Oren clue → human combat → box recovery → provision reward'})
 walk('nhal_mercado_setas');act('aceptar','velmora_recipiente');walk('nhal_umbral_elin');act('hablar','nhal_elin',topic='entrega');walk('nhal_taller_cortezas');act('hablar','nhal_desi',topic='apoyo');walk('nhal_secadero_sombra');act('nhal_preparar_recipiente');walk('nhal_umbral_elin');act('nhal_entregar_recipiente');walk('nhal_mercado_setas');before=state()['character']['seals'];s=act('cobrar','velmora_recipiente');assert s['character']['seals']-before==8;evidence.append({'local_quest':'Elin recipient returned without removing toy support','paid':s['character']['seals']-before})
 walk('lethra_mercado_hojas');act('aceptar','narevia_preparativos');walk('lethra_plataforma_secado');act('examinar','costuras');act('lethra_elegir_cubierto');walk('lethra_cocina_reunion');act('hablar','lethra_nima',topic='preparativos');walk('lethra_mercado_hojas');before=state()['character']['seals'];s=act('cobrar','narevia_preparativos');assert s['character']['seals']-before==6;evidence.append({'local_quest':'Drying cloth decision communicated to Nima','paid':s['character']['seals']-before})
 walk('veyra_patio_senales');act('aceptar','vaisgard_aviso_carga');walk('veyra_puerta_piedra');act('hablar','veyra_tov',topic='aviso');walk('veyra_archivo_cargas');act('hablar','veyra_nera',topic='aviso_preciso');walk('veyra_patio_senales');before=state()['character']['seals'];s=act('cobrar','vaisgard_aviso_carga');assert s['character']['seals']-before==6;evidence.append({'local_quest':'Tov witnessed delay → Nera accurate provenance → Arel report','paid':6})
 walk('veyra_calle_toldos');act('aceptar','vaisgard_toldo');act('examinar','costura');inventory_before=state()['inventory'];r=post(client,'/api/action',{'id':'veyra_atar_toldo','request_id':str(uuid.uuid4())});assert r.status_code==409;assert state()['inventory']==inventory_before
 walk('vaisgard_mercado');s=act('veyra_recibir_fibra_toldo');assert sum(i.get('quantity',1) for i in s['inventory'] if i['id']=='junco_prestado_seli')==1;inventory_before=s['inventory'];r=post(client,'/api/action',{'id':'vender','target':'junco_prestado_seli','request_id':str(uuid.uuid4())});assert r.status_code==409;assert state()['inventory']==inventory_before
 walk('veyra_calle_toldos');loan_request=str(uuid.uuid4());s=act('veyra_atar_toldo_prestado',request_id=loan_request);repeat=post(client,'/api/action',{'id':'veyra_atar_toldo_prestado','target':None,'request_id':loan_request});assert repeat.status_code==200;assert repeat.json['inventory']==s['inventory'];assert not any(i['id']=='junco_prestado_seli' for i in s['inventory']);before=s['character']['seals'];s=act('cobrar','vaisgard_toldo');assert s['character']['seals']-before==6;evidence.append({'local_quest':'No ghost material on rejected action; real loan unsellable, consumed once by canopy repair','paid':6})
 walk('korven_entrante_piezas');act('aceptar','brumak_taza');act('hablar','korven_taren',topic='medidas');walk('korven_horno_reposo');act('examinar','recipiente');act('korven_recomendar_base');walk('korven_entrante_piezas');act('hablar','korven_taren',topic='recomendación');before=state()['character']['seals'];s=act('cobrar','brumak_taza');assert s['character']['seals']-before==8;evidence.append({'local_quest':'Measured mug → kiln comparison → base recommendation → Taren delivery','paid':8})

 walk('edran_prado');act('acercarse','cornalomo');act('retirarse','cornalomo')
 walk('edran_surcos');act('combatir','espinajo_rastrojo');act('capacidad');clock.now+=44;s=state();journey.append({'action':'esperar_combate','room':s['room']['id'],'events':s['narrative'],'hp':s['character']['hp']});assert not s['character']['combat'];assert any(i['id']=='fibra_espinajo' for i in s['inventory'])
 walk('valdren_fragua');upgrade=next(a for a in state()['actions'] if a['id']=='afinar');act('afinar',upgrade['target'],confirmed=True)
 act('descansar');walk('khariel_centro');act('mover','hogar');act('descansar')

 # Three original paid errands, without pretending observation repaired the world.
 walk('valdren_fragua');act('aceptar','valdren_recado_forja');walk('valdren_cobertizo');act('hablar','edran_bren',topic='rueda');walk('valdren_fragua');act('cobrar','valdren_recado_forja')
 walk('valdren_comedor');act('aceptar','valdren_revision_cobertizos');walk('valdren_graneros');act('examinar','esquina');walk('edran_cobertizo_campo');act('examinar','estacas');walk('valdren_comedor');act('cobrar','valdren_revision_cobertizos')
 walk('valdren_cobertizo');act('aceptar','valdren_estado_vado');walk('edran_puente_juncos');act('examinar','apoyos');walk('edran_hito_campos');act('examinar','losa');walk('valdren_cobertizo');act('cobrar','valdren_estado_vado')
 walk('korven_almacen_entrada');act('hablar','korven_ruma',topic='balanza');walk('korven_almacen_cruce');act('korven_usar_lateral');walk('korven_almacen_fondo');act('korven_recoger_placa');walk('korven_almacen_entrada');act('korven_devolver_placa')
 walk('edran_acequia');act('edran_despejar_acequia')
 owner=client;other=app.test_client();post(other,'/api/account/register',{'username':'historyobserver','password':'isolated-test-password'});created=post(other,'/api/character/create',{'name':'Observador temporal','species':'felaryn','class_id':'sombra'}).json;post(dm,'/api/master/approve',{'character_id':created['character']['id']});client=other;act('mover','salir');client=owner
 checkpoints=[]
 targets=['edran_canal_entrada','edran_canal_compuerta','edran_canal_repisa','korven_almacen_entrada','korven_almacen_balanzas','korven_almacen_fondo','hoshai_cajas_camino','hoshai_taller_apoyos','hoshai_balcon_valle','nhal_secadero_sombra','nhal_umbral_elin','lethra_plataforma_secado','lethra_cocina_reunion','veyra_archivo_cargas','veyra_calle_toldos','korven_entrante_piezas','valdren_fragua','valdren_comedor','valdren_cobertizo','edran_acequia']
 for target in targets:
  pair={'room':target}
  for role,c in [('owner',owner),('observer',other)]:
   client=c;walk(target);snap=state();pair[role]={'room':snap['room'],'scene':snap['scene'],'actions':snap['actions']}
   options=[a for a in snap['actions'] if a['id']=='hablar' and not a.get('disabled')]
   if options:
    a=options[0];talk=act('hablar',a['target'],topic=a.get('topic'));pair[role]['talk']=talk['narrative']
  if target=='edran_acequia':assert pair['owner']['room']['description']==pair['observer']['room']['description'] and 'La abertura está limpia' in pair['owner']['room']['description']
  checkpoints.append(pair)
 client=owner;walk('khariel_centro');act('mover','hogar')
 with app.extensions['store'].transaction() as db:
  from server.store import Store
  rows=db.execute('SELECT * FROM characters ORDER BY id').fetchall();flags=[Store.load(row)['state']['flags'] for row in rows]
 assert len(flags)==2 and 'edran_caja_recogida' in flags[0] and 'edran_caja_recogida' not in flags[1]
 assert len([f for f in flags[0] if f.startswith('encargo_pagado:')])==10
 assert not any(f.startswith('encargo_pagado:') for f in flags[1])
 assert 'korven_placa_devuelta' in flags[0] and 'korven_placa_devuelta' not in flags[1]
 if os.environ.get('VT_DEPTH6_ASSERT'):
  checks={'edran_canal_repisa':'La repisa quedó vacía','korven_almacen_fondo':'El hueco junto al saco','hoshai_cajas_camino':'El espacio entre las cajas','nhal_secadero_sombra':'El aro del recipiente','veyra_calle_toldos':'El amarre de junco'}
  for pair in checkpoints:
   if pair['room'] in checks:
    text=checks[pair['room']];assert text in pair['owner']['room']['description'],pair['room'];assert text not in pair['observer']['room']['description'],pair['room']
 out={'moves':sum(e.get('action')=='mover' for e in journey),'events':journey,'checkpoints':checkpoints,'flags':flags,'final':state()}
 (root/os.environ.get('VT_DEPTH6_OUTPUT','review/archive/2026-10-07/depth-cycle6-before.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2))
 print('PASS history journey',out['moves'],'moves; ten paid errands, two dungeon recoveries, twenty paired owner/observer checkpoints')
