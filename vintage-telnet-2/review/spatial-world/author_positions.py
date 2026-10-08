"""Development-only spatial authoring. Runtime reads frozen coordinates, never reflows discovery."""
import json,collections,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from server.content import Content
content=Content(Path('content'));rooms=content.rooms
opposite={'norte':'sur','sur':'norte','este':'oeste','oeste':'este'}
straight=[];bends=[];seen=set()
for a,r in rooms.items():
 for d,b in r['exits'].items():
  if rooms[b]['exits'].get(opposite[d])==a:straight.append((a,d,b))
  elif tuple(sorted((a,b))) not in seen:
   seen.add(tuple(sorted((a,b))));back=next(k for k,v in rooms[b]['exits'].items() if v==a);bends.append((a,d,b,back))
axes=[]
for axis in [0,1]:
 parent={r:r for r in rooms}
 def root(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 for a,d,b in straight:
  if d in (('norte','sur') if axis==0 else ('este','oeste')):parent[root(b)]=root(a)
 groups={r:root(r) for r in rooms};edges=set()
 for a,d,b in straight:
  if d in (('este','oeste') if axis==0 else ('norte','sur')):
   low,high=(a,b) if d in ('este','sur') else (b,a);edges.add((groups[low],groups[high]))
 # A bend's two ports constrain both dimensions, without pretending the entire path is straight.
 for a,d,b,back in bends:
  for from_,direction,to in [(a,d,b),(b,back,a)]:
   if direction in (('este','oeste') if axis==0 else ('norte','sur')):
    low,high=(from_,to) if direction in ('este','sur') else (to,from_);edges.add((groups[low],groups[high]))
 axes.append({'groups':groups,'edges':edges,'gaps':{}})

# Authored street clearances keep cul-de-sacs inside their blocks and indoor wings
# outside neighbouring public streets. These are spacing decisions, not new exits.
clearances=[
 (1,'valdren_cobertizo','valdren_patio_carros',3),
 (1,'lethra_mercado_hojas','lethra_muelle_vecinal',3),
 (1,'hoshai_senda_dosel','hoshai_patio_hogares',2),
 (0,'hoshai_senda_dosel','hoshai_balcon_valle',1),
 (0,'korven_plataforma_escucha','korven_almacen_entrada',1),
 (0,'korven_sala_cuidados','korven_almacen_balanzas',1),
 (0,'korven_horno_reposo','veyra_puerta_campos',1),
 (0,'nhal_secadero_sombra','nhal_calle_hogares',1),
 (1,'edran_parcela_vieja','valdren_fragua',1),
]
for axis,low,high,gap in clearances:
 a=axes[axis];edge=(a['groups'][low],a['groups'][high]);a['edges'].add(edge);a['gaps'][edge]=gap

def solve(a):
 groups=a['groups'];edges=a['edges'];ids=sorted(set(groups.values()));before={k:set() for k in ids};after={k:set() for k in ids}
 for low,high in edges:before[high].add(low);after[low].add(high)
 degree={k:len(before[k]) for k in ids};queue=collections.deque(k for k in ids if degree[k]==0);values=dict.fromkeys(ids,0);order=[]
 while queue:
  k=queue.popleft();order.append(k)
  for n in sorted(after[k]):
   values[n]=max(values[n],values[k]+a['gaps'].get((k,n),1));degree[n]-=1
   if degree[n]==0:queue.append(n)
 assert len(order)==len(ids),'Contradictory straight geometry'
 anchor=groups['vaisgard_mercado'];anchor_value=values[anchor]
 for iteration in range(1200):
  change=0
  for k in order+list(reversed(order)):
   if k==anchor:continue
   targets=[values[n]+a['gaps'].get((n,k),1) for n in before[k]]+[values[n]-a['gaps'].get((k,n),1) for n in after[k]]
   if not targets:continue
   lower=max((values[n]+a['gaps'].get((n,k),1) for n in before[k]),default=-1000);upper=min((values[n]-a['gaps'].get((k,n),1) for n in after[k]),default=1000)
   target=max(lower,min(upper,sum(targets)/len(targets)));change=max(change,abs(target-values[k]));values[k]=target
  assert values[anchor]==anchor_value
  if change<.00001:break
 result={r:round(values[g]) for r,g in groups.items()}
 assert all(round(values[hi])-round(values[lo])>=a['gaps'].get((lo,hi),1) for lo,hi in edges)
 return result

def reachable(edges,a,b):
 after=collections.defaultdict(set)
 for x,y in edges:after[x].add(y)
 queue=[a];seen={a}
 for x in queue:
  if x==b:return True
  for y in after[x]:
   if y not in seen:seen.add(y);queue.append(y)
 return False

for pass_ in range(100):
 coordinates=[solve(a) for a in axes];occupied={};collision=None
 for rid in sorted(rooms):
  cell=tuple(c[rid] for c in coordinates)
  if cell in occupied:collision=(occupied[cell],rid);break
  occupied[cell]=rid
 if not collision:break
 left,right=collision
 choices=[]
 for index,a in enumerate(axes):
  lo,hi=a['groups'][left],a['groups'][right]
  if lo==hi:continue
  if reachable(a['edges'],hi,lo):lo,hi=hi,lo
  assert not reachable(a['edges'],hi,lo)
  # Separate unrelated side branches without changing the cardinal street they belong to.
  choices.append((len(a['edges']),index,lo,hi))
 assert choices,collision
 _,index,lo,hi=min(choices);axes[index]['edges'].add((lo,hi))
else:raise AssertionError('Failed to separate rooms')
positions={rid:[coordinates[0][rid],coordinates[1][rid]] for rid in sorted(rooms)}
# Keep home tiles out of every street: reserve one free adjacent diagonal per settlement.
homes={};taken={tuple(p) for p in positions.values()}
for reg,data in content.regions.items():
 x,y=positions[data['settlement']]
 for distance in [1,2,3]:
  candidates=[(x-distance,y+distance),(x+distance,y+distance),(x-distance,y-distance),(x+distance,y-distance)]
  def on_public_street(p):
   for source,direction,target in straight:
    a,b=positions[source],positions[target]
    if a[0]==b[0]==p[0] and min(a[1],b[1])<p[1]<max(a[1],b[1]):return True
    if a[1]==b[1]==p[1] and min(a[0],b[0])<p[0]<max(a[0],b[0]):return True
   return False
  free=next((p for p in candidates if p not in taken and not on_public_street(p)),None)
  if free:homes[reg]=list(free);taken.add(free);break
 assert reg in homes
out={'version':1,'note':'Frozen schematic geography; units are room spacing, not travel distance. Exits remain authoritative.','positions':positions,'homes':homes,'bends':[{'from':a,'direction':d,'to':b,'reverse':back} for a,d,b,back in bends]}
Path('content/spatial.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rooms':len(positions),'bends':len(bends),'collision_passes':pass_,'width':max(p[0] for p in positions.values())-min(p[0] for p in positions.values()),'height':max(p[1] for p in positions.values())-min(p[1] for p in positions.values()),'settlements':{reg:positions[data['settlement']] for reg,data in content.regions.items()}},ensure_ascii=False))
