/* Transport/presentation contract QA. No browser rendering or story-quality claim. */
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {events,actions,actionPayload,knownMap,journalEvents} from './ui-data.js';
const fixture=JSON.parse(await readFile(process.argv[2],'utf8'));
let checks=0;
for(const state of fixture.states){
 assert(state.authenticated&&state.character.status==='approved');
 assert(events(state.scene).length>0,'Authored current situation remains readable after a short action reply');
 for(const action of actions(state.actions)){const encoded=JSON.parse(JSON.stringify(actionPayload({...action,csrf_token:'not-part-of-intent',world:'forged-state'},'contract-request-123')));assert.equal(encoded.id,action.id);assert.equal(encoded.target,action.target);assert.equal(encoded.topic,action.topic);assert.deepEqual(Object.keys(encoded).sort(),['id','request_id',...['target','topic'].filter(k=>typeof action[k]==='string')].sort());checks++;}
 const map=knownMap(state.map),visible=new Set(map.nodes.map(n=>n.id));assert(map.edges.every(edge=>visible.has(edge.from)&&visible.has(edge.to)));assert(!visible.has('secret'));checks++;
}
const repaired=fixture.states.find(s=>s.journal.length);assert(journalEvents(repaired.journal).some(e=>e.kind==='MEMORY'&&e.text.includes('Aseguraste')));checks++;
const observed=fixture.states.find(s=>s.bestiary.length);assert(observed.bestiary.some(c=>typeof c.name==='string'&&typeof c.description==='string'));checks++;
const known=knownMap({nodes:[{id:'visible',name:'Lugar leído'}],edges:[['visible','secret'],{from:'secret',to:'visible'},['visible','visible']]});assert.equal(known.edges.length,1);checks++;
assert.equal(events([{kind:'WORLD',text:' '},{kind:'DANGER',text:'Señal real'},null,{text:10}]).length,1);checks++;
assert.throws(()=>actionPayload({},'id'),/Acción/);checks++;
console.log(JSON.stringify({checks,scope:'Real in-process new API journeys plus adversarial presentation contracts',limitations:['No browser or screenshot','Technical fixture text is not game content']}));
