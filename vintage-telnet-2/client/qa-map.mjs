import assert from 'node:assert/strict';
import {orientationMap,knownRoute} from './ui-data.js';
const nodes=['home','town','road','well','island'].map(id=>({id,name:id}));
const raw={nodes,edges:[['home','town'],['town','road'],['town','well']],routes:[
 {from:'home',to:'town',direction:'salir'},{from:'town',to:'home',direction:'hogar'},
 {from:'town',to:'road',direction:'norte'},{from:'road',to:'town',direction:'oeste'},
 {from:'town',to:'well',direction:'sur'},{from:'well',to:'town',direction:'norte'},
 {from:'town',to:'secret',direction:'este'},{from:'secret',to:'home',direction:'oeste'},
 {from:'well',to:'home',direction:'teleport'}],frontiers:[
 {from:'town',direction:'este',to:'secret',name:'Hidden place'},
 {from:'road',direction:'sur'}, {from:'town',direction:'norte'},
 {from:'town',direction:'este'}, {from:'town',direction:'teleport'}]};
const map=orientationMap(raw,'town');
assert.equal(map.legacy,false);assert.equal(map.current,'town');assert.equal(map.routes.length,6);
assert.deepEqual(map.frontiers,[{from:'town',direction:'este'}]);
assert(!JSON.stringify(map).includes('secret'));
assert.deepEqual(knownRoute(map,'well','road').map(s=>s.direction),['norte','norte']);
assert.deepEqual(knownRoute(map,'road','home').map(s=>s.direction),['oeste','hogar']);
assert.deepEqual(knownRoute(map,'town','town'),[]);
assert.equal(knownRoute(map,'home','island'),null);assert.equal(knownRoute(map,'home','secret'),null);
const directed=orientationMap({...raw,routes:[{from:'town',to:'road',direction:'norte'}]},'road');
assert.equal(knownRoute(directed,'road','town'),null);
const legacy=orientationMap({nodes,edges:raw.edges},'town');
assert.equal(legacy.legacy,true);assert.equal(knownRoute(legacy,'home','road').length,2);
assert(knownRoute(legacy,'home','road').every(step=>!('direction' in step)));
assert.equal(orientationMap(raw,'secret').current,null);
console.log(JSON.stringify({checks:15,scope:'Known-only oriented routes, actual asymmetric directions, home, shortest route, one-way, disconnected, frontier sanitization, old server without guessing directions',limits:['No browser']}));
