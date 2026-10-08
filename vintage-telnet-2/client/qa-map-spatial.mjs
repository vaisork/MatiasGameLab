import assert from 'node:assert/strict';
import fs from 'node:fs';
import {discoveredLayout,discoveredPaths} from './ui-data.js';
const nodes=[{id:'a',position:[-2,4]},{id:'b',position:[-1,4]},{id:'c',position:[-1,3]}],routes=[{from:'a',to:'b',direction:'este'},{from:'b',to:'a',direction:'oeste'},{from:'b',to:'c',direction:'norte'},{from:'c',to:'b',direction:'sur'}];
const canonical=discoveredLayout({nodes,routes});
for(const node of nodes)assert.deepEqual(canonical.get(node.id),node.position);
const permuted=discoveredLayout({nodes:[...nodes].reverse(),routes:[...routes].reverse()});assert.deepEqual(permuted,canonical);
const grown=discoveredLayout({nodes:[{id:'new',position:[20,20]},...nodes],routes});for(const node of nodes)assert.deepEqual(grown.get(node.id),canonical.get(node.id));
assert.deepEqual(discoveredPaths({routes},canonical),discoveredPaths({routes:[...routes].reverse()},permuted));
const spatial=JSON.parse(fs.readFileSync(new URL('../content/spatial.json',import.meta.url))),rooms={};
for(const file of fs.readdirSync(new URL('../content/regions/',import.meta.url)))if(file.endsWith('.json'))Object.assign(rooms,JSON.parse(fs.readFileSync(new URL('../content/regions/'+file,import.meta.url))).rooms);
const map={nodes:Object.entries(rooms).map(([id,r])=>({id,name:r.name,position:spatial.positions[id]})),routes:Object.entries(rooms).flatMap(([from,r])=>Object.entries(r.exits||{}).filter(([,to])=>rooms[to]).map(([direction,to])=>({from,to,direction})))};
const positions=discoveredLayout(map),start=performance.now(),links=discoveredPaths(map,positions),pairs=new Set(map.routes.map(r=>[r.from,r.to].sort().join('\n')));
assert.equal(links.length,pairs.size);const used=new Set();
for(const link of links){
 for(const point of link.points.slice(1,-1))for(const [id,pos] of positions){if(id===link.from||id===link.to)continue;assert.ok(Math.abs(point[0]-pos[0]*4)>1||Math.abs(point[1]-pos[1]*4)>1,`road through ${id}`);}
 for(let i=2;i<link.points.length-1;i++){const key=[link.points[i-1].join(','),link.points[i].join(',')].sort().join('|');assert(!used.has(key),'shared road segment');used.add(key);}
 for(const crossing of link.crossings)assert(link.points.some(p=>p[0]===crossing[0]&&p[1]===crossing[1]));
}
assert.deepEqual(links,discoveredPaths({routes:[...map.routes].reverse()},positions));
const homePositions=new Map([['plaza',[10,10]],['home',[9,11]]]);const homeRoad=discoveredPaths({routes:[{from:'plaza',to:'home',direction:'hogar'},{from:'home',to:'plaza',direction:'salir'}]},homePositions)[0];assert.equal(homeRoad.direction,'salir');assert.ok(homeRoad.points[1][0]>homeRoad.points[0][0],'home salir uses geometric east port');assert.ok(homeRoad.points.at(-2)[0]<homeRoad.points.at(-1)[0],'plaza hogar uses geometric west port');
const legacy=discoveredLayout({nodes:nodes.map(({id})=>({id})),routes});assert.equal(legacy.size,3);
console.log(JSON.stringify({status:'PASS',nodes:map.nodes.length,connections:links.length,crossings:links.reduce((n,l)=>n+l.crossings.length,0),elapsedMs:Math.round(performance.now()-start),checks:'Frozen coordinates, permutation/discovery, all canonical connections, no unrelated room intersection, no shared lane segments, explicit crossings, legacy fallback',limits:'Pure geometry/source, no browser/3D screenshot'}));
// Production frozen atlas, including the six private-home reserves (QA only).
const atlasNodes=[...map.nodes,...Object.entries(spatial.homes).map(([region,position])=>({id:'home:'+region,name:'Reserved home '+region,position}))],atlasRoutes=spatial.roads.flatMap(r=>[{from:r.from,to:r.to,direction:r.direction,points:r.points},{from:r.to,to:r.from,direction:r.reverse,points:[...r.points].reverse()}]);
const atlasPositions=discoveredLayout({nodes:atlasNodes,routes:atlasRoutes}),atlasLinks=discoveredPaths({routes:atlasRoutes},atlasPositions),atlasPairs=new Set(atlasRoutes.map(r=>[r.from,r.to].sort().join('\n'))),atlasUsed=new Set(),vectors={norte:[0,-1],sur:[0,1],este:[1,0],oeste:[-1,0]};
assert.equal(atlasNodes.length,189);assert.equal(atlasPairs.size,202);assert.equal(atlasLinks.length,202);
for(const link of atlasLinks){
 const source=spatial.roads.find(r=>(r.from===link.from&&r.to===link.to)||(r.from===link.to&&r.to===link.from));assert.deepEqual(link.points,source.from===link.from?source.points:[...source.points].reverse());
 const checkPort=(direction,p,center)=>{const v=vectors[direction];if(v)assert((p[0]-center[0])*v[0]+(p[1]-center[1])*v[1]>0,`actual port ${direction}`);};checkPort(link.direction,link.points[1],link.points[0]);checkPort(link.reverse,link.points.at(-2),link.points.at(-1));
 for(const point of link.points.slice(1,-1))for(const [id,pos] of atlasPositions){if(id===link.from||id===link.to)continue;assert.ok(Math.abs(point[0]-pos[0]*4)>1||Math.abs(point[1]-pos[1]*4)>1,`frozen road through ${id}`);}
 for(let i=2;i<link.points.length-1;i++){const key=[link.points[i-1].join(','),link.points[i].join(',')].sort().join('|');assert(!atlasUsed.has(key),'frozen shared lane');atlasUsed.add(key);}
}
assert.deepEqual(atlasLinks,discoveredPaths({routes:[...atlasRoutes].reverse()},discoveredLayout({nodes:[...atlasNodes].reverse(),routes:atlasRoutes})));
console.log(JSON.stringify({status:'PASS',scope:'Production frozen atlas, not player knowledge',atlasRooms:atlasNodes.length,homeReserves:6,frozenRoads:atlasLinks.length,crossings:atlasLinks.reduce((n,l)=>n+l.crossings.length,0),checks:'Canonical points retained, actual cardinal ports, all frozen connections, no room intersection/shared lanes, permutation'}));
