// Executes the real passive-update function with a small technical focus adapter.
// Not a browser, keyboard/IME or scroll-layout approval.
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=await readFile(new URL('./app.js',import.meta.url),'utf8');
const fn=source.slice(source.indexOf('function applyPassiveSnapshot('),source.indexOf('let lastPassiveRefresh=0;'));
function node(tag,{id='',name='',value='',label='',disabled=false,start=null,end=null}={}){return {tagName:tag,id,name,value,textContent:label,type:tag==='INPUT'?'text':null,disabled,selectionStart:start,selectionEnd:end,isConnected:true,options:[{value:'road'},{value:'town'}],getAttribute:key=>key==='name'?name:null,focus(){document.activeElement=this;},setSelectionRange(a,b){this.selectionStart=a;this.selectionEnd=b;}};}
const document={activeElement:null,getElementById:id=>elements.find(n=>n.id===id),querySelectorAll:()=>elements};let elements=[],renderCount=0,recorded=[];
const main={querySelector:()=>null,contains:n=>elements.includes(n),querySelectorAll:selector=>selector==='details'?[]:elements};
const window={scrollY:57,scrollTo({top}){this.scrollY=top;}};
const state=()=>({authenticated:true,csrf_token:'old',version:1,character:{id:1,status:'approved',location:'town',combat:null},room:{id:'town'},scene:[],actions:[]});
const context=vm.createContext({document,main,navigation:{contains:()=>false},window,Array,JSON,busy:false,view:'map',state:state(),following:false,terminalFeed:{scrollTop:23},commandDraft:'',recordNarrative:next=>recorded.push(next),render:()=>{renderCount++;for(const n of elements)n.isConnected=false;elements=elements.map(old=>node(old.tagName,{id:old.id,name:old.name,value:old.name==='decision'?context.commandDraft:old.value,label:old.textContent,disabled:old.tagName==='BUTTON'&&Boolean(context.state.character.combat)}));}});
vm.runInContext(fn+'\nglobalThis.apply=applyPassiveSnapshot;',context);
// Focused map selector must receive fresh location and keep the chosen destination.
elements=[node('SELECT',{id:'map-destination',name:'destination',value:'road'})];document.activeElement=elements[0];let next=state();next.character.location='road';next.room.id='road';assert.equal(context.apply(next),true);assert.equal(context.state,next);assert.equal(document.activeElement,elements[0]);assert.equal(elements[0].value,'road');assert.equal(window.scrollY,57);assert.equal(context.terminalFeed.scrollTop,23);
// Typed decision/caret survives an actual narrative change and DOM replacement.
context.view='adventure';context.state=state();elements=[node('INPUT',{name:'decision',value:'examinar rueda',start:8,end:8})];document.activeElement=elements[0];next=state();next.scene=[{kind:'world',text:'Está lloviendo.'}];context.apply(next);assert.equal(context.commandDraft,'examinar rueda');assert.equal(elements[0].value,'examinar rueda');assert.equal(document.activeElement,elements[0]);assert.equal(elements[0].selectionStart,8);assert.equal(recorded.at(-1),next);
// A passive defeat moves to a new room: keep the draft/caret, reset that room's reader.
context.state=state();context.view='adventure';context.following=false;context.terminalFeed.scrollTop=55;next=state();next.character.location='recovery';next.room.id='recovery';context.apply(next);assert.equal(context.terminalFeed.scrollTop,0);assert.equal(context.following,true);assert.equal(elements[0].value,'examinar rueda');assert.equal(elements[0].selectionStart,8);
// Combat state replaces stale actions while a travel button had focus.
context.view='map';context.state=state();elements=[node('BUTTON',{label:'Dar siguiente paso · Norte'})];document.activeElement=elements[0];next=state();next.character.combat={intervention_pending:true};next.actions=[{id:'defender',label:'Bloquear'}];context.apply(next);assert.equal(context.state.character.combat.intervention_pending,true);assert.equal(context.state.actions[0].id,'defender');assert.equal(elements[0].disabled,true);assert.equal(document.activeElement.isConnected,false);
// Heartbeat/token refresh adopts the response without unnecessary reconstruction.
const count=renderCount;next=JSON.parse(JSON.stringify(context.state));next.version=2;next.csrf_token='fresh';assert.equal(context.apply(next),false);assert.equal(renderCount,count);assert.equal(context.state.csrf_token,'fresh');
context.view='master';assert.equal(context.apply(state()),false);assert.equal(renderCount,count);
console.log(JSON.stringify({cases:4,additional:'stable token refresh and director guard',scope:'Actual passive function with technical DOM/focus adapter: selector freshness, typed draft/caret, authoritative combat actions',limits:['No browser','No keyboard/IME or visual approval']}));
