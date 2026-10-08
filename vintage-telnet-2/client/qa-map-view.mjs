// Real mapView executed through a tiny node adapter; no layout/browser claims.
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {orientationMap,knownRoute,actions,regionNames,discoveredLayout} from './ui-data.js';
const source=await readFile(new URL('./app.js',import.meta.url),'utf8'),mapSource=source.slice(source.indexOf('function mapView()'),source.indexOf('function journalView()'));
function el(tag,attrs={},...children){const node={tag,attrs,children:[],classList:{add(...values){node.attrs.class=[node.attrs.class,...values].filter(Boolean).join(' ');}},append(...items){this.children.push(...items.flat(Infinity).filter(x=>x!=null));},replaceChildren(...items){this.children=[];this.append(...items);},querySelector(){return {focus(){}};}};node.append(...children);return node;}
const button=(label,handler,attrs={})=>el('button',{...attrs,onclick:handler},label),main=el('main'),sent=[];
const nodes=[{id:'town',name:'Plaza',region:'edran',kind:'settlement'},{id:'road',name:'Camino',region:'edran',kind:'route'},{id:'home',name:'Tu hogar',region:'edran',kind:'home'},{id:'island',name:'Apartado',region:'nhal',kind:'route'}];
const data={nodes,edges:[['town','road'],['home','town']],routes:[{from:'town',to:'road',direction:'norte'},{from:'road',to:'town',direction:'oeste'},{from:'town',to:'home',direction:'hogar'},{from:'home',to:'town',direction:'salir'},{from:'town',to:'secret',direction:'sur'}],frontiers:[{from:'town',direction:'este',to:'secret',name:'Nombre oculto'},{from:'road',direction:'sur'}]};
const context=vm.createContext({el,button,main,orientationMap,knownRoute,actions,regionNames,Map,discoveredLayout,visual3D:()=>el('details'),discoveredMap:()=>el('section'),state:{character:{location:'town'},map:data,actions:[{id:'mover',target:'norte',label:'Norte'},{id:'mover',target:'este',label:'Este'},{id:'mover',target:'hogar',label:'Hogar'}]},selectedPlace:'road',card:(...children)=>el('section',{},...children),title:(label,name)=>el('h1',{},name),subtitle:text=>el('p',{},text),actionButton:action=>button(action.label,()=>sent.push(action),{disabled:action.disabled}),render:()=>vm.runInContext('mapView()',context)});
vm.runInContext(mapSource+'\nmapView();',context);
const all=(node,tag)=>typeof node==='object'?[...(node.tag===tag?[node]:[]),...node.children.flatMap(child=>all(child,tag))]:[];
const text=node=>typeof node==='object'?node.children.map(text).join(' '):String(node);
assert(!text(main).includes('Nombre oculto'));assert(!text(main).includes('secret'));
let next=all(main,'button').find(node=>text(node).startsWith('Dar siguiente paso'));assert(next);next.attrs.onclick();assert.equal(sent[0].target,'norte');assert.equal(sent.length,1);
assert(!text(main).includes('Dónde estás'));
assert(all(main,'optgroup').some(node=>node.attrs.label==='Hogar'));
context.selectedPlace='town';context.render();assert(text(main).includes('Ya estás en este lugar.'));assert(!all(main,'button').some(node=>text(node).startsWith('Dar siguiente paso')));
context.selectedPlace='island';context.render();assert(text(main).includes('No hay un recorrido conocido'));
context.selectedPlace='road';context.state.actions=[];context.render();assert(text(main).includes('Ese paso no está disponible ahora.'));assert(!all(main,'button').some(node=>text(node)==='Explorar este'));
context.state.map={nodes,edges:data.edges};context.render();assert(text(main).includes('Reinicia el juego'));assert(!all(main,'button').some(node=>text(node).startsWith('Dar siguiente paso')));
context.state.map=data;context.state.character.location='road';context.state.actions=[{id:'mover',target:'oeste',label:'Oeste'}];context.selectedPlace='town';context.render();next=all(main,'button').find(node=>text(node).startsWith('Dar siguiente paso'));next.attrs.onclick();assert.equal(sent.at(-1).target,'oeste');
console.log(JSON.stringify({checks:13,scope:'Actual mapView: no hidden names, manual single-step action, no redundant location card, home groups, arrived, disconnected, unavailable, legacy and asymmetric directions',limits:['Technical node adapter','No browser or layout approval']}));
