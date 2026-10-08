"""Five separate real API walks, isolated SQLite; no production state or teleportation."""
import json,sys
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from test_real_content import RealContentTests
from server.content import Content
CYCLES={
 1:('Pueblos y calles', ['valdren_cobertizo','valdren_patio_carros','valdren_graneros','valdren_pozo','nhal_patio_relato','nhal_calle_hogares','velmora_centro']),
 2:('Regiones y orientación', ['khariel_centro','korven_meseta_relevo','brumak_centro','edran_linde_piedra','vaisgard_mercado','narevia_centro']),
 3:('Campos, curvas y riberas', ['edran_era','edran_zanja_antigua','edran_arboleda','edran_sendero_regreso','edran_sauces','lethra_raices_observacion','lethra_relevo_raices']),
 4:('Interiores y callejones', ['edran_canal_repisa','edran_canal_refugio','korven_almacen_balanzas','korven_almacen_lateral','korven_almacen_fondo','korven_registro_cauce']),
 5:('Ruta de control independiente', ['hoshai_cajas_camino','hoshai_balcon_valle','nhal_umbral_elin','lethra_cocina_reunion','veyra_cantera_callada','korven_entrante_piezas'])}
def geometry(content):
 rows=[]
 for road in content.spatial['roads']:
  points=road['points'];directions=[]
  for a,b in zip(points,points[1:]):
   direction=tuple((y>x)-(y<x) for x,y in zip(a,b))
   if not directions or directions[-1]!=direction:directions.append(direction)
  distance=sum(sum(abs(x-y) for x,y in zip(a,b)) for a,b in zip(points,points[1:]));direct=sum(abs(x-y) for x,y in zip(points[0],points[-1]))
  rows.append({'from':road['from'],'to':road['to'],'turns':len(directions)-1,'detour_ratio':round(distance/direct,3)})
 return {'roads':len(rows),'max_turns':max(r['turns'] for r in rows),'public_turns_over_two':sum(r['turns']>2 and not r['from'].startswith('home:') and not r['to'].startswith('home:') for r in rows),'worst':sorted(rows,key=lambda r:(r['turns'],r['detour_ratio']),reverse=True)[:15]}
def run(number):
 fixture=RealContentTests('test_real_errand_social_economy_home_and_reconnect');fixture.setUp();trace=[];saved={};label,targets=CYCLES[number]
 try:
  fixture.create();fixture.action('mover','salir')
  destinations=[*targets,'valdren_plaza']
  if number==5:
   # Plan nearest-first coverage independently of the selected audit waypoints.
   covered={'valdren_plaza'};cursor='valdren_plaza'
   for destination in targets:
    queue=deque([(cursor,[])]);seen={cursor}
    while queue:
     room,path=queue.popleft()
     if room==destination:break
     for target in fixture.content.rooms[room]['exits'].values():
      if target not in seen:seen.add(target);queue.append((target,path+[target]))
    covered.update(path);cursor=destination
   while len(covered)<len(fixture.content.rooms):
    queue=deque([(cursor,[])]);seen={cursor}
    while queue:
     room,path=queue.popleft()
     if room not in covered:break
     for target in fixture.content.rooms[room]['exits'].values():
      if target not in seen:seen.add(target);queue.append((target,path+[target]))
    destinations.insert(-1,room);covered.update(path);cursor=room
  for destination in destinations:
   current=fixture.client.get('/api/state').json['room']['id'];queue=deque([(current,[])]);seen={current}
   while queue:
    room,path=queue.popleft()
    if room==destination:break
    for direction,target in fixture.content.rooms[room]['exits'].items():
     if target not in seen:seen.add(target);queue.append((target,path+[(room,direction,target)]))
   else:raise AssertionError(destination)
   for source,direction,target in path:
    before=fixture.client.get('/api/state').json
    action=next(a for a in before['actions'] if a['id']=='mover' and a['target']==direction)
    if action.get('disabled'):
     permission=next(a for a in before['actions'] if a['id'].startswith('pedir_permiso') and not a.get('disabled'));fixture.action(permission['id'])
    after=fixture.action('mover',direction);assert after['room']['id']==target
    origin=fixture.content.spatial['positions'][source];point=fixture.content.spatial['positions'][target];axis,sign={'norte':(1,-1),'sur':(1,1),'este':(0,1),'oeste':(0,-1)}[direction];assert (point[axis]-origin[axis])*sign>0
    for route in after['map']['routes']:
     key=(route['from'],route['to']);assert key not in saved or saved[key]==route['points'];saved[key]=route['points']
    trace.append({'from':source,'direction':direction,'to':target,'position':point,'description':fixture.content.rooms[target]['description'],'narrative':after['narrative']})
  fixture.action('mover','hogar');assert fixture.client.get('/api/state').json['room']['id'].startswith('home:')
  assert len(trace)>=20
  report={'cycle':number,'focus':label,'movements':len(trace),'regions':sorted({fixture.content.rooms[row['to']]['region'] for row in trace}),'unique_rooms':len({row['to'] for row in trace}),'home_return':True,'stable_learned_roads':True,'no_direction_sign_contradiction':True,'geometry':geometry(fixture.content),'walk':trace}
  path=ROOT/f'review/spatial-five-cycles/cycle-{number}.json';path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('walk','geometry')},ensure_ascii=False))
 finally:fixture.doCleanups()
if __name__=='__main__':run(int(sys.argv[1]))
