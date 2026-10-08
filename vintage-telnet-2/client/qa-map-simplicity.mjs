import assert from 'node:assert/strict';
import fs from 'node:fs';
import {discoveredPaths} from './ui-data.js';
const atlas=JSON.parse(fs.readFileSync(new URL('../content/spatial.json',import.meta.url)));
const changes=points=>{const dirs=[];for(let i=1;i<points.length;i++){const d=points[i].map((v,j)=>Math.sign(v-points[i-1][j])).join(',');if(d!==dirs.at(-1))dirs.push(d);}return dirs.length-1;};
const bends=new Set(atlas.bends.map(b=>[b.from,b.to].sort().join('|')));
let straight=0,curved=0,homes=0;
for(const road of atlas.roads){
 const home=road.from.startsWith('home:')||road.to.startsWith('home:'),bent=bends.has([road.from,road.to].sort().join('|'));
 const turns=changes(road.points);assert.equal(turns,home?0:bent?1:0,`${road.from}: artificial bends`);
 const length=road.points.slice(1).reduce((sum,p,i)=>sum+p.reduce((n,v,j)=>n+Math.abs(v-road.points[i][j]),0),0),direct=road.points[0].reduce((sum,v,j)=>sum+Math.abs(v-road.points.at(-1)[j]),0);
 assert.equal(length,direct,`${road.from}: unnecessary backtracking`);
 if(home)homes++;else if(bent)curved++;else straight++;
}
const positions=new Map([['a',[0,0]],['b',[4,3]]]);
const path=discoveredPaths({routes:[{from:'a',to:'b',direction:'este'},{from:'b',to:'a',direction:'norte'}]},positions)[0];
assert.equal(changes(path.points),1,'equal-length paths prefer one bend over a staircase');
console.log(JSON.stringify({status:'PASS',straight,curved,homes,checks:'Every authored street stays straight, all six real bends turn once, homes do not distort public roads, no unnecessary backtracking'}));
