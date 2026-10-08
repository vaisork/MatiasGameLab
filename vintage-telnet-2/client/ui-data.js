// Presentation contracts; these functions never invent world state or actions.
export const speciesNames={humanos:'Humano',humano:'Humano',felaryn:'Felaryn',dravak:'Dravak',marevyn:'Marevyn',vesperi:'Vesperi'};
export const classNames={juramentado:'Juramentado',arcano:'Arcano',sombra:'Sombra',artifice:'Artífice'};
export const regionNames={veyra:'Cuenca de Veyra',edran:'Llanos de Edran',hoshai:'Sierra de Hoshai',korven:'Pedrales de Korven',lethra:'Aguas de Lethra',nhal:'Bosque de Nhal'};
export const kindNames={WORLD:'Entorno',LOCATION:'Lugar',ACTION:'Tu decisión',NPC:'Voz',DIALOGUE:'Conversación',TRACE:'Señal',DANGER:'Peligro',COMBAT:'Encuentro',DAMAGE:'Daño',DISCOVERY:'Descubrimiento',REWARD:'Progreso',MEMORY:'Recuerdo',INFO:'Información',ERROR:'Aviso',CHAT:'Conversación local'};
export function events(value){return Array.isArray(value)?value.filter(event=>event&&typeof event.text==='string'&&event.text.trim()).map(event=>({kind:String(event.kind||'WORLD').toUpperCase(),text:event.text,id:event.id??null})):[];}
export function actions(value){return Array.isArray(value)?value.filter(action=>action&&typeof action.id==='string'&&typeof action.label==='string').map(action=>({...action,disabled:Boolean(action.disabled)})):[];}
export function list(value){if(Array.isArray(value))return value;if(value&&Array.isArray(value.items))return value.items;if(value&&Array.isArray(value.entries))return value.entries;return [];}
export function actionPayload(action,requestId,confirmed=false){if(!action||typeof action.id!=='string'||!action.id)throw Error('Acción no disponible');const payload={id:action.id,request_id:requestId};for(const key of ['target','topic'])if(typeof action[key]==='string')payload[key]=action[key];if(confirmed)payload.confirmed=true;return payload;}
export function knownMap(value){const nodes=list(value?.nodes).filter(node=>node&&typeof node.id==='string'&&typeof node.name==='string'),ids=new Set(nodes.map(node=>node.id));const edges=list(value?.edges).map(edge=>Array.isArray(edge)?{from:edge[0],to:edge[1]}:{from:edge?.from??edge?.source,to:edge?.to??edge?.target}).filter(edge=>ids.has(edge.from)&&ids.has(edge.to));return{nodes,edges};}
export function textLabel(value){if(typeof value==='string')return value;if(value&&typeof value.label==='string')return value.label;return '';}
export function journalEvents(value){return list(value).flatMap(entry=>typeof entry==='string'&&entry.trim()?[{kind:'MEMORY',text:entry,id:null}]:events([entry]));}

// A snapshot is context, not another copy of the entire travel chronicle.
export class NarrativeJournal {
 constructor(){this.entries=[];this.reset();}
 reset(){this.entries.length=0;this.character=null;this.room=null;this.region=null;this.scene=new Set();this.feedback='';this.sequence=0;this.visit=0;this.inCombat=false;}
 consume(snapshot,explicit=false){
  if(!snapshot?.character||!snapshot?.room)return [];
  if(this.character!==snapshot.character.id){this.reset();this.character=snapshot.character.id;}
  const scene=events(snapshot.scene),reply=events(snapshot.narrative),stamp=e=>e.kind+'\n'+e.text;
  if(!scene.length&&snapshot.room.description)scene.push({kind:'WORLD',text:snapshot.room.description});
  const current=new Set(scene.map(stamp)),moved=this.room!==snapshot.room.id,feedbackKey=JSON.stringify(reply.map(stamp));
  const additions=[];
  if(moved){this.visit++;additions.push({kind:'LOCATION',text:(this.room===null?'Estás en ':'Llegas a ')+snapshot.room.name+'.'});if(this.region&&snapshot.room.region&&this.region!==snapshot.room.region)additions.push({kind:'DISCOVERY',text:'Entras en '+(regionNames[snapshot.room.region]||snapshot.room.region)+'.'});additions.push(...scene);}
  // Existing scene details are already in the journal, including explicit observations.
  else if(!explicit)additions.push(...scene.filter(e=>!this.scene.has(stamp(e))));
  if(explicit||feedbackKey!==this.feedback)additions.push(...reply.filter(e=>!current.has(stamp(e))));
  if(explicit&&!moved)additions.push(...scene.filter(e=>!this.scene.has(stamp(e))&&!reply.some(r=>stamp(r)===stamp(e))));
  const urgentReply=new Set(reply.filter(e=>['DANGER','COMBAT','DAMAGE','ACTION','REWARD'].includes(e.kind)).map(stamp));
  const combatReply=this.inCombat||Boolean(snapshot.character.combat)||reply.some(e=>['COMBAT','DAMAGE'].includes(e.kind));
  const unique=new Set(),added=[];
  for(const event of additions){const key=stamp(event);if(unique.has(key))continue;unique.add(key);const entry={...event,key:`${this.character}:${++this.sequence}`,place:snapshot.room.name,room:snapshot.room.id,visit:this.visit,urgent:combatReply&&urgentReply.has(key)};this.entries.push(entry);added.push(entry);}
  if(this.entries.length>100)this.entries.splice(0,this.entries.length-100);
  this.room=snapshot.room.id;this.region=snapshot.room.region;this.scene=current;this.feedback=feedbackKey;this.inCombat=Boolean(snapshot.character.combat);return added;
 }
}

// Learned directions only. No coordinates, inferred opposites, or hidden destinations.
export function orientationMap(value,current){
 const map=knownMap(value),ids=new Set(map.nodes.map(n=>n.id)),directions=new Set(['norte','sur','este','oeste','salir','hogar']);
 const legacy=!Array.isArray(value?.routes),routes=[];
 const raw=legacy?map.edges.flatMap(e=>[{from:e.from,to:e.to},{from:e.to,to:e.from}]):value.routes;
 const seen=new Set();
 for(const route of raw){
  if(!route||!ids.has(route.from)||!ids.has(route.to)||route.from===route.to)continue;
  if(!legacy&&!directions.has(route.direction))continue;
  const key=route.from+'\n'+route.to+'\n'+(route.direction||'');if(seen.has(key))continue;seen.add(key);
  routes.push({from:route.from,to:route.to,...(!legacy?{direction:route.direction}:{})});
 }
 const position=ids.has(current)?current:null,frontiers=[],frontierSeen=new Set();
 for(const exit of list(value?.frontiers)){
  if(!exit||exit.from!==position||!directions.has(exit.direction)||frontierSeen.has(exit.direction))continue;
  if(routes.some(route=>route.from===position&&route.direction===exit.direction))continue;
  frontierSeen.add(exit.direction);frontiers.push({from:position,direction:exit.direction});
 }
 return {...map,routes,frontiers,current:position,legacy};
}
export function knownRoute(map,from,to){
 const ids=new Set(list(map?.nodes).map(n=>n.id));if(!ids.has(from)||!ids.has(to))return null;
 if(from===to)return [];
 const queue=[{id:from,steps:[]}],seen=new Set([from]);
 for(let index=0;index<queue.length;index++){
  const current=queue[index];
  for(const edge of list(map.routes)){
   if(edge.from!==current.id||!ids.has(edge.to)||seen.has(edge.to))continue;
   const steps=[...current.steps,{...edge}];if(edge.to===to)return steps;
   seen.add(edge.to);queue.push({id:edge.to,steps});
  }
 }
 return null;
}

// Adapted from the previous map's directional placement; known places only.
// This is a schematic: collisions move a tile farther along its learned exit.
export function discoveredLayout(map){
 const steps={norte:[0,-1],sur:[0,1],este:[1,0],oeste:[-1,0],salir:[1,1],hogar:[-1,-1]},positions=new Map(),taken=new Set();
 let component=0;
 for(const node of map.nodes){
  if(positions.has(node.id))continue;
  let start=[component*3,0];while(taken.has(start.join(',')))start[0]++;
  positions.set(node.id,start);taken.add(start.join(','));component++;
  const queue=[node.id];
  for(let index=0;index<queue.length;index++){
   const from=queue[index],[x,y]=positions.get(from);
   for(const route of map.routes){
    if(route.from!==from||positions.has(route.to)||!map.nodes.some(n=>n.id===route.to))continue;
    const [dx,dy]=steps[route.direction]||[1,0];let cell=[x+dx,y+dy];
    while(taken.has(cell.join(',')))cell=[cell[0]+dx,cell[1]+dy];
    positions.set(route.to,cell);taken.add(cell.join(','));queue.push(route.to);
   }
  }
 }
 return positions;
}

// Route through the spaces between tiles; endpoint directions are actual learned exits.
export function discoveredPaths(map,positions){
 const vectors={norte:[0,-1],sur:[0,1],este:[1,0],oeste:[-1,0],salir:[1,0],hogar:[-1,0]},blocked=new Set(),links=[],seen=new Set();
 for(const [x,y] of positions.values())for(let dx=-1;dx<=1;dx++)for(let dy=-1;dy<=1;dy++)blocked.add([x*4+dx,y*4+dy].join(','));
 const cells=[...positions.values()],minX=Math.min(...cells.map(p=>p[0]*4))-3,maxX=Math.max(...cells.map(p=>p[0]*4))+3,minY=Math.min(...cells.map(p=>p[1]*4))-3,maxY=Math.max(...cells.map(p=>p[1]*4))+3;
 for(const route of map.routes){
  if(!positions.has(route.from)||!positions.has(route.to))continue;
  const key=[route.from,route.to].sort().join('\n');if(seen.has(key))continue;seen.add(key);
  const reverse=map.routes.find(r=>r.from===route.to&&r.to===route.from),from=positions.get(route.from).map(v=>v*4),to=positions.get(route.to).map(v=>v*4),out=vectors[route.direction]||[1,0],back=vectors[reverse?.direction]||out.map(v=>-v);
  const start=from.map((v,i)=>v+out[i]*2),end=to.map((v,i)=>v+back[i]*2),queue=[start],parent=new Map([[start.join(','),null]]),goal=end.join(',');
  for(let index=0;index<queue.length&&!parent.has(goal);index++){
   const current=queue[index];
   const next=Object.values(vectors).slice(0,4).map(v=>current.map((n,i)=>n+v[i])).sort((a,b)=>Math.abs(a[0]-end[0])+Math.abs(a[1]-end[1])-Math.abs(b[0]-end[0])-Math.abs(b[1]-end[1]));
   for(const cell of next){const k=cell.join(',');if(cell[0]<minX||cell[0]>maxX||cell[1]<minY||cell[1]>maxY||blocked.has(k)||parent.has(k))continue;parent.set(k,current);queue.push(cell);}
  }
  if(!parent.has(goal))continue;
  const path=[];for(let cell=end;cell;cell=parent.get(cell.join(',')))path.unshift(cell);
  links.push({from:route.from,to:route.to,direction:route.direction,reverse:reverse?.direction,points:[from,...path,to]});
 }
 return links;
}

export const speciesPortraits=Object.fromEntries(['humano','felaryn','dravak','marevyn','vesperi'].map(id=>[id,`/client/art/species/${id}-anime-v1.webp`]));

export const placeIllustrations={"valdren_plaza":{"name":"Valdren","illustration":"/client/art/places/valdren-anime-v1.webp","caption":"Representación del pueblo; la hora y el clima se describen en la lectura."},"khariel_centro":{"name":"Khariel","illustration":"/client/art/places/khariel-anime-v1.webp","caption":"Representación del pueblo; la hora y el clima se describen en la lectura."},"brumak_centro":{"name":"Brumak","illustration":"/client/art/places/brumak-anime-v1.webp","caption":"Representación del pueblo; la hora y el clima se describen en la lectura."},"narevia_centro":{"name":"Narevia","illustration":"/client/art/places/narevia-anime-v1.webp","caption":"Representación del pueblo; la hora y el clima se describen en la lectura."},"velmora_centro":{"name":"Velmora","illustration":"/client/art/places/velmora-anime-v1.webp","caption":"Representación del pueblo; la hora y el clima se describen en la lectura."},"vaisgard_mercado":{"name":"Vaisgard","illustration":"/client/art/places/vaisgard-anime-v1.webp","caption":"Representación del pueblo; la hora y el clima se describen en la lectura."}};

const townArtKeys={edran:'valdren_plaza',hoshai:'khariel_centro',korven:'brumak_centro',lethra:'narevia_centro',nhal:'velmora_centro',veyra:'vaisgard_mercado'};
const homeArtNames={edran:'valdren',hoshai:'khariel',korven:'brumak',lethra:'narevia',nhal:'velmora'};
placeIllustrations.valdren_fragua={name:'Fragua de Valdren',illustration:'/client/art/places/valdren-fragua-anime-v1.webp',caption:'La fragua compra armas sobrantes y permite mejorar el filo; las acciones disponibles dependen de lo que llevas.'};
export function placeArt(room){
 if(!room)return null;
 if(room.kind==='home'&&homeArtNames[room.region])return {name:room.name,illustration:`/client/art/places/${homeArtNames[room.region]}-home-anime-v1.webp`,thumbnail:`/client/art/places/${homeArtNames[room.region]}-home-thumb-v1.webp`,caption:'Representación de tu hogar. La hora, el clima y el equipo actual se consultan en el juego.'};
 if(room.id==='korven_peldanos_cortos')return {name:room.name,illustration:'/client/art/places/brumak-escalones-anime-v1.webp',thumbnail:'/client/art/places/brumak-escalones-thumb-v1.webp',caption:'Escalones bajos de Brumak. La hora y el clima actuales se describen en la lectura.'};
 const art=placeIllustrations[room.id]||(room.kind==='settlement'?placeIllustrations[townArtKeys[room.region]]:null);
 return art?{...art,thumbnail:art.illustration.replace('-anime-v1.webp','-thumb-v1.webp')}:null;
}

// Presentation only: preserve the resolved result and every combat number.
export function combatReading(event){
 const text=event.text||'',kind=String(event.kind||'').toUpperCase();
 if(!['COMBAT','DAMAGE','REWARD','ACTION','DANGER'].includes(kind))return text;
 let hash=0;for(const ch of String(event.key||event.id||text))hash=(hash*31+ch.charCodeAt(0))>>>0;
 const choose=variants=>variants[hash%variants.length];
 const hit=text.match(/^Tu golpe alcanza a (.+): ([\d.]+) de daño\.$/);if(hit){const [,name,damage]=hit;return choose([`¡Das en el blanco! ${name} recibe ${damage} de daño.`,`Tu golpe conecta con ${name}: ${damage} de daño.`,`Aciertas el ataque: ${damage} de daño a ${name}.`]);}
 const hurt=text.match(/^(.+) te alcanza: ([\d.]+) de daño\.$/);if(hurt){const [,name,damage]=hurt;return choose([`${name} te alcanza. El impacto te sacude: ${damage} de daño.`,`¡${name} conecta su ataque! Recibes ${damage} de daño.`,`${name} te golpea: ${damage} de daño. Toca recuperar el ritmo.`]);}
 const miss=text.match(/^La respuesta de (.+) pasa sin alcanzarte\.$/);if(miss){const name=miss[1];return choose([`¡${name} falla! Su ataque no te alcanza.`,`${name} responde, pero no consigue alcanzarte.`,`El ataque de ${name} pasa de largo. Esta vez no te alcanza.`]);}
 if(text==='Tu ataque no encuentra un ángulo limpio.')return choose(['Buscas el hueco, pero el golpe no conecta. Tu ataque no encuentra un ángulo limpio.','Lanzas el ataque y no logras alcanzarlo. Tu ataque no encuentra un ángulo limpio.']);
 if(/^Vences a .+\. Ganas \d+ XP;/.test(text))return choose(['La tensión afloja: ese enfrentamiento termina. ','¡Lo conseguiste! Has vencido a este rival. ','El intercambio termina con tu victoria. '])+text;
 const powers={'Guardia Comprometida':'Afirmas los pies y sostienes la guardia. ','Impulso Arcano':'Concentras el impulso y lo sueltas hacia tu rival. ','Borrar el Foco':'Cambias el ritmo y buscas salir de su foco. ','Tiro de Interrupción':'Apuntas, ajustas y sueltas el disparo. '};
 for(const [name,lead] of Object.entries(powers))if(text.startsWith('Usas '+name+'.'))return lead+text;
 return text;
}

// Compact decision cues summarize the server's reason; they never decide eligibility.
export function capabilityReadingHint(action){
 if(action.id!=='capacidad')return null;
 const reason=action.reason||'';
 if(action.disabled){
  if(reason==='Esta acción preparada no es frontal; la guardia no puede responderla.')return 'No cubre ese ángulo';
  if(reason==='Esta acción preparada no puede interrumpirse.')return 'No interrumpible';
  if(reason==='Tu equipo o posición no permite esa respuesta.')return 'Revisa equipo y posición';
  return null;
 }
 if(reason==='Reduce el daño del próximo golpe que te alcance.')return 'Reduce el daño recibido';
 if(reason==='Rompe la preparación y dificulta que te alcance.')return 'Rompe su preparación';
 if(reason==='Reduce la precisión de la respuesta ordinaria durante esta ronda.')return 'Reduce su precisión';
 if(reason==='Reduce su precisión; si falla, abre tu siguiente ataque.')return 'Rival menos preciso; apertura si falla';
 if(reason.includes('no puede interrumpirse. El disparo sólo hará daño si acierta;'))return 'Sólo daño si aciertas';
 if(reason.startsWith('Si aciertas, interrumpes '))return 'Corta preparación si aciertas';
 if(reason==='Un disparo acertado corta la carga o reduce su precisión.')return 'Menos precisión si aciertas';
 return null;
}
