"""Replay actual alternative choices through the existing live HTTP helpers."""
import importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('journey',Path(__file__).with_name('depth-cycle15-dialogue.py'));j=importlib.util.module_from_spec(spec);spec.loader.exec_module(j)
j.request(j.dm,'/api/master/login',{'password':'isolated-review-only'});j.create(j.c,'choices')
j.walk('hoshai_mercado_cintas');j.act('aceptar','khariel_cornisa');j.walk('hoshai_deposito_comun');j.walk('hoshai_balcon_valle');j.act('examinar','cornisa');j.act('hoshai_pedir_revision');j.walk('hoshai_mercado_cintas');j.talk('hoshai_luma','cornisa','first_report');j.act('cobrar','khariel_cornisa');j.talk('hoshai_luma','cornisa','paid')
j.walk('korven_entrante_piezas');j.act('aceptar','brumak_taza');j.talk('korven_taren','medidas','initial');j.walk('korven_horno_reposo');j.act('examinar','recipiente');j.act('korven_recomendar_aro');j.walk('korven_entrante_piezas');j.talk('korven_taren','recomendación','first_report');j.act('cobrar','brumak_taza');j.talk('korven_taren','recomendación','paid')
j.walk('veyra_calle_toldos');j.talk('veyra_seli','reparación','initial');j.act('aceptar','vaisgard_toldo');j.act('examinar','costura');j.walk('vaisgard_mercado');j.act('veyra_recibir_fibra_toldo');j.walk('veyra_calle_toldos');j.act('veyra_atar_toldo_prestado');j.act('cobrar','vaisgard_toldo');j.talk('veyra_seli','reparación','paid')
j.walk('veyra_patio_senales');j.act('aceptar','vaisgard_aviso_carga');j.walk('veyra_puerta_piedra');j.talk('veyra_tov','aviso','initial');j.walk('veyra_archivo_cargas');j.act('hablar','veyra_nera',topic='pedir_comprobacion');j.talk('veyra_nera','cargas','resolved');j.walk('veyra_patio_senales');j.act('cobrar','vaisgard_aviso_carga');j.walk('veyra_puerta_piedra');j.talk('veyra_tov','aviso','paid')
expected={('hoshai_luma','cornisa'):'pedido de revisión',('korven_taren','recomendación'):'conservará el aro',('veyra_seli','reparación'):'atadura que hiciste',('veyra_nera','cargas'):'pendiente de comprobación',('veyra_tov','aviso'):'comprobar aquí mismo'}
for key,phrase in expected.items():
 row=next(r for r in j.checks if (r['npc'],r['topic'])==key and r['stage'] in ['paid','resolved']);assert any(phrase in e['text'] for e in row['narrative']),(key,row)
assert not any(i['id']=='junco_prestado_seli' for i in j.state()['inventory'])
(j.root/'review/archive/2026-10-07/depth-cycle15-dialogue-alternatives.json').write_text(json.dumps({'moves':j.moves,'checks':j.checks,'events':j.events,'final':j.state()},ensure_ascii=False,indent=2));print(json.dumps({'moves':j.moves,'checks':len(j.checks),'branches':len(expected)}))
