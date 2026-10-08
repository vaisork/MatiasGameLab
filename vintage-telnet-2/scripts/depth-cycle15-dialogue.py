"""Live HTTP quest/dialogue replay with private observers, temporary server 8115."""
import json,uuid,time,urllib.request,http.cookiejar,os
from pathlib import Path
from collections import deque
root=Path(__file__).resolve().parents[1];base='http://127.0.0.1:8115';rooms={}
for p in (root/'content/regions').glob('*.json'):rooms.update(json.loads(p.read_text())['rooms'])
def client():return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
c=client();dm=client();events=[];checks=[];moves=0

def request(client,path,data=None):
 if data is not None:
  token=json.load(client.open(base+'/api/state'))['csrf_token'];req=urllib.request.Request(base+path,json.dumps({**data,'csrf_token':token}).encode(),{'Content-Type':'application/json'})
 else:req=base+path
 return json.load(client.open(req))
def state(who=c):return request(who,'/api/state')
def act(id,target=None,who=c,**kw):
 global moves
 s=request(who,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4()),**kw});moves+=id=='mover';events.append({'id':id,'target':target,**kw,'actor':'worker' if who==c else 'observer','room':s.get('room',{}).get('id'),'narrative':s.get('narrative'),'seals':s.get('character',{}).get('seals')});return s

def walk(dest,who=c):
 here=state(who)['room']['id']
 if here.startswith('home:'):act('mover','salir',who);here=state(who)['room']['id']
 q=deque([(here,[])]);seen={here}
 while q:
  room,path=q.popleft()
  if room==dest:break
  for direction,to in rooms[room].get('exits',{}).items():
   if to not in seen:seen.add(to);q.append((to,path+[direction]))
 else:raise AssertionError(dest)
 for direction in path:
  s=state(who);move=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
  if move.get('disabled'):
   permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'),who)
  act('mover',direction,who)
def talk(npc,topic,stage,who=c):
 s=state(who);available=any(a['id']=='hablar' and a['target']==npc and a.get('topic')==topic for a in s['actions'])
 if available:s=act('hablar',npc,who,topic=topic)
 row={'npc':npc,'topic':topic,'stage':stage,'available':available,'room':s['room']['id'],'narrative':s.get('narrative') if available else []};checks.append(row);return row

def create(who,suffix):
 name='dialogue15'+str(time.time_ns())+suffix;request(who,'/api/account/register',{'username':name,'password':'isolated-password'});s=request(who,'/api/character/create',{'name':'Revisión '+suffix,'species':'humano','class_id':'juramentado','gender':'masculino'});request(dm,'/api/master/approve',{'character_id':s['character']['id']})
def main():
 request(dm,'/api/master/login',{'password':'isolated-review-only'});create(c,'worker');observer=client();create(observer,'observer')
 # Edran: paid delivery and two actual shared physical changes.
 walk('valdren_fragua');talk('edran_daro','trabajo','initial');act('aceptar','valdren_recado_forja');walk('valdren_cobertizo');talk('edran_bren','rueda','initial');act('edran_comprobar_rueda');talk('edran_bren','rueda','resolved');walk('valdren_fragua');act('cobrar','valdren_recado_forja');talk('edran_daro','trabajo','paid')
 walk('valdren_casa_semillas');talk('edran_iria','tablilla','initial');walk('edran_cobertizo_campo');act('edran_leer_caja');walk('edran_lindero');act('edran_hallar_tablilla');walk('valdren_casa_semillas');act('edran_aclarar_cuenta');talk('edran_iria','tablilla','resolved')
 # Hoshai: peaceful return and recommendation actually delivered.
 walk('hoshai_taller_apoyos');talk('hoshai_daren','polea','initial');act('aceptar','khariel_polea');walk('hoshai_campamento_lona');act('hablar','hoshai_seran',topic='cuenta');act('hablar','hoshai_seran',topic='acuerdo');walk('hoshai_cajas_camino');act('hoshai_recoger_polea');walk('hoshai_taller_apoyos');act('hoshai_entregar_polea');act('cobrar','khariel_polea');talk('hoshai_daren','polea','paid')
 walk('hoshai_mercado_cintas');talk('hoshai_luma','cornisa','initial');act('aceptar','khariel_cornisa');walk('hoshai_deposito_comun');walk('hoshai_balcon_valle');act('examinar','cornisa');act('hoshai_marcar_cornisa');walk('hoshai_mercado_cintas');talk('hoshai_luma','cornisa','first_report');act('cobrar','khariel_cornisa');talk('hoshai_luma','cornisa','paid')
 # Korven: local decision and physical quest item returned without a fight.
 walk('korven_entrante_piezas');act('aceptar','brumak_taza');talk('korven_taren','medidas','initial');walk('korven_horno_reposo');act('examinar','recipiente');act('korven_recomendar_base');walk('korven_entrante_piezas');talk('korven_taren','recomendación','first_report');act('cobrar','brumak_taza');talk('korven_taren','medidas','paid');talk('korven_taren','recomendación','paid')
 walk('korven_almacen_entrada');talk('korven_ruma','balanza','initial');walk('korven_almacen_fondo');act('korven_recoger_placa');walk('korven_almacen_entrada');act('korven_devolver_placa');talk('korven_ruma','balanza','resolved')
 # Veyra: perches prepared, not a falsely completed fabric repair; sourced message.
 walk('veyra_calle_toldos');talk('veyra_seli','reparación','initial');act('aceptar','vaisgard_toldo');act('examinar','costura');act('veyra_preparar_perchas');act('cobrar','vaisgard_toldo');talk('veyra_seli','reparación','paid')
 walk('veyra_patio_senales');talk('veyra_arel','mensajes','initial');act('aceptar','vaisgard_aviso_carga');walk('veyra_puerta_piedra');talk('veyra_tov','aviso','initial');walk('veyra_archivo_cargas');talk('veyra_nera','cargas','initial');act('hablar','veyra_nera',topic='aviso_preciso');talk('veyra_nera','cargas','resolved');walk('veyra_patio_senales');act('cobrar','vaisgard_aviso_carga');talk('veyra_arel','mensajes','paid');walk('veyra_puerta_piedra');talk('veyra_tov','aviso','paid')
 # Uninvolved observer visits the same people only after worker progression.
 for room,npc,topic in [('valdren_fragua','edran_daro','trabajo'),('valdren_cobertizo','edran_bren','rueda'),('valdren_casa_semillas','edran_iria','tablilla'),('hoshai_taller_apoyos','hoshai_daren','polea'),('hoshai_mercado_cintas','hoshai_luma','cornisa'),('korven_entrante_piezas','korven_taren','medidas'),('korven_almacen_entrada','korven_ruma','balanza'),('veyra_calle_toldos','veyra_seli','reparación'),('veyra_puerta_piedra','veyra_tov','aviso'),('veyra_archivo_cargas','veyra_nera','cargas'),('veyra_patio_senales','veyra_arel','mensajes')]:walk(room,observer);talk(npc,topic,'observer',observer)
 walk('valdren_plaza');act('mover','hogar');out={'moves':moves,'checks':checks,'events':events,'final':state(),'observer':state(observer),'scope':'HTTP real, fresh temporary DB, natural six paid errands; no state fixtures'};(root/os.environ.get('VT_DIALOGUE_OUTPUT','review/archive/2026-10-07/depth-cycle15-dialogue-before.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({'moves':moves,'checks':len(checks),'actions':len(events),'seals':out['final']['character']['seals']}))

if __name__=='__main__':main()
