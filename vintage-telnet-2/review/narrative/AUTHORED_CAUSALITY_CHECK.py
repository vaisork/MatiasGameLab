"""Controlled engine fixtures; neither a journey nor human/browser evidence."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from server.content import Content
from server.engine import Engine
c=Content(ROOT/'content');world={'flags':[]};checks=[]
def fixture(room,flags=()):return {'location':room,'flags':list(flags),'species':'humano','home':'private-fixture','visits':{room:2}}
def action(room,id):return next(a for a in c.rooms[room]['actions'] if a['id']==id)
def check_observation(room,id,rain_allowed):
 item=action(room,id);found={}
 for hour in range(72):
  eng=Engine(c,lambda hour=hour:hour*3600+15*60);state=fixture(room)
  ambient=eng.ambient(c.rooms[room],world);phase=ambient['time_of_day'];rain=ambient['weather'].lower() in ['lluvia','tormenta']
  expected=phase=='Día' and (rain_allowed or not rain)
  assert eng.allowed(item,state,world)==expected,(id,ambient,expected)
  found[(phase,rain)]=True
 assert any(k[0]=='Día' for k in found) and any(k[0]=='Noche' for k in found)
 if not rain_allowed:assert ('Día',True) in found and ('Día',False) in found
 checks.append({'action':id,'controlled_hours':72,'observed_conditions':list(map(str,found))})
check_observation('hoshai_mirador_nudo','hoshai_observar_nudo',True)
check_observation('korven_cauce_observacion','korven_atribuir_cambio',False)
check_observation('nhal_raiz_marcada','nhal_atribuir_marcas',False)
for room,id,flags in [('hoshai_caseta_revision','hoshai_comunicar_nudo',['hoshai_nudo_visto']),('korven_registro_cauce','korven_localizar_aviso',['korven_cambio_atribuido']),('lethra_cuidado_barcas','lethra_llevar_invitacion',['lethra_costura_recordada'])]:
 item=action(room,id)
 for hour,expected in [(12,True),(23,False)]:
  eng=Engine(c,lambda hour=hour:hour*3600);state=fixture(room,flags);assert eng.allowed(item,state,world)==expected,(id,hour)
 checks.append({'action':id,'requires_present_scheduled_npc':True})
for room,flag,term in [('veyra_calle_toldos','veyra_costura_acordada','La costura nueva'),('nhal_umbral_elin','nhal_recipiente_devuelto','quedó vacío'),('nhal_patio_relato','nhal_relato_ampliado','atribuida a Elin')]:
 eng=Engine(c,lambda:12*3600);state=fixture(room);before=eng.room({'state':state})
 world2={'flags':[flag]};after=eng.room({'state':state},world2)
 assert after!=before
 assert term in ' '.join(str(after.get(key,'')) for key in ['description','rain','examine'])
 assert state['flags']==[], 'Physical shared state cannot require actor personal flags'
 checks.append({'room':room,'world_effect_visible_to_nonactor':flag})
result={'scope':__doc__,'checks':checks,'result':'PASS'}
(ROOT/'review/narrative/AUTHORED_CAUSALITY_CHECK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
