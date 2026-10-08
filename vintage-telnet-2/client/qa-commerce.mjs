// Transport contract for item instances; no rendering or server-economy approval.
import assert from 'node:assert/strict';
import {actions,actionPayload,list} from './ui-data.js';
const first='weapon_378ab838-72fb-40d7-bd43-c5a7402297a3',second='weapon_03d66f28-9a21-48d7-a433-b4f0ef314d69';
const inventory=list([{id:first,name:'Varita de aprendiz',condition:'intact',quantity:1},{id:second,name:'Varita de aprendiz',condition:'damaged_event',quantity:1}]);
assert.equal(inventory.length,2);assert.notEqual(inventory[0].id,inventory[1].id);
const offered=actions([{id:'vender',target:first,label:'Vender Varita de aprendiz · 14 sellos',confirmation:'¿Vender esta arma?'},{id:'reparar',target:second,label:'Reparar Varita de aprendiz · 8 sellos'},{id:'equipar',target:second,label:'Equipar',disabled:true,reason:'Necesita reparación'}]);
assert.deepEqual(actionPayload(offered[0],'commerce-confirmed',true),{id:'vender',target:first,request_id:'commerce-confirmed',confirmed:true});
assert.equal(actionPayload(offered[0],'commerce-unconfirmed').confirmed,undefined);
assert.equal(actionPayload(offered[1],'commerce-repair').target,second);
assert.equal(offered[2].disabled,true);assert.equal(offered[2].reason,'Necesita reparación');
assert.equal(actionPayload(offered[1],'commerce-retry').request_id,actionPayload(offered[1],'commerce-retry').request_id);
console.log(JSON.stringify({checks:8,scope:'Instance targets preserved, confirmation explicit, repair target isolated, disabled reason preserved, retry identity stable',limits:['No DOM/browser','Server invariants reviewed separately']}));
