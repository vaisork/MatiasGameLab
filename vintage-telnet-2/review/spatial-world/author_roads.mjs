// Development-only authoring. Frozen paths use all real rooms and reserved homes.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {discoveredPaths} from '../../client/ui-data.js';
const spatial=JSON.parse(fs.readFileSync('content/spatial.json','utf8')),rooms={};
for(const file of fs.readdirSync('content/regions'))if(file.endsWith('.json'))Object.assign(rooms,JSON.parse(fs.readFileSync('content/regions/'+file,'utf8')).rooms);
const positions=new Map(Object.entries(spatial.positions)),routes=[];
for(const [from,r] of Object.entries(rooms))for(const [direction,to] of Object.entries(r.exits))routes.push({from,to,direction});
for(const file of fs.readdirSync('content/regions'))if(file.endsWith('.json'))for(const [region,data] of Object.entries(JSON.parse(fs.readFileSync('content/regions/'+file,'utf8')).regions)){
 const home='home:'+region;positions.set(home,spatial.homes[region]);routes.push({from:home,to:data.settlement,direction:'salir'},{from:data.settlement,to:home,direction:'hogar'});
}
const links=discoveredPaths({routes},positions),pairs=new Set(routes.map(r=>[r.from,r.to].sort().join('\n')));assert.equal(links.length,pairs.size);
spatial.roads=links.map(({from,to,direction,reverse,points})=>({from,to,direction,reverse,points}));
fs.writeFileSync('content/spatial.json',JSON.stringify(spatial,null,2)+'\n');
console.log(JSON.stringify({rooms:rooms&&Object.keys(rooms).length,reservedHomes:6,frozenRoads:links.length,crossings:links.reduce((n,l)=>n+l.crossings.length,0)}));
