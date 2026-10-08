const {chromium}=await import(process.env.VT_REVIEW_PLAYWRIGHT||'playwright');
import {mkdir,writeFile} from 'node:fs/promises';
const base=process.env.VT_PLAYTEST_URL||'http://127.0.0.1:8099',out=process.env.VT_PLAYTEST_OUTPUT||'/tmp/vt-night-playtest';
if(!/^http:\/\/(127\.0\.0\.1|localhost):8099$/.test(base))throw Error('Use the isolated playtest server on port 8099, never the live game.');
await mkdir(out,{recursive:true});const browser=await chromium.launch({channel:'chrome',headless:true});const context=await browser.newContext({viewport:{width:393,height:750}});const page=await context.newPage();
async function state(){return (await context.request.get(base+'/api/state')).json();}
async function post(path,data){const s=await state();const r=await context.request.post(base+path,{data:{...data,csrf_token:s.csrf_token}});if(!r.ok())throw Error(await r.text());return r.json();}
async function act(id,target){return post('/api/action',{id,target,request_id:crypto.randomUUID()});}
try{
 await post('/api/account/register',{username:'night'+Date.now(),password:'isolated-night-account'});const c=await post('/api/character/create',{name:'Prueba nocturna',species:'felaryn',class_id:'sombra'});
 const master=await browser.newContext();const ms=await (await master.request.get(base+'/api/state')).json();await master.request.post(base+'/api/master/login',{data:{password:'isolated-review-only',csrf_token:ms.csrf_token}});const mt=await (await master.request.get(base+'/api/state')).json();await master.request.post(base+'/api/master/approve',{data:{character_id:c.character.id,csrf_token:mt.csrf_token}});
 await page.goto(base);await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();
 let s=await state();await act('mover','salir');await page.reload();await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();
 const first=await state(),moves=first.actions.filter(a=>a.id==='mover'&&['norte','sur','este','oeste'].includes(a.target));const forward=moves[0];await page.locator(`[data-direction="${forward.target}"]`).click();await page.waitForTimeout(150);
 const fast=await state();await page.screenshot({path:out+'/rapid-first-step.png'});
 const reading=await page.locator('.terminal-feed').evaluate(n=>({visible:n.innerText,accessible:Array.from(n.querySelectorAll('[aria-label]')).map(x=>({hidden:x.hidden,label:x.getAttribute('aria-label')})),scroll:n.scrollTop,height:n.clientHeight}));
 const visits=[first.room.name,fast.room.name];
 for(let i=0;i<6;i++){
  const snap=await state();const wanted=i%2===0?'norte':'sur';const move=snap.actions.find(a=>a.id==='mover'&&a.target===wanted&&!a.disabled);if(!move)throw Error('Expected open walking route');
  await page.locator(`[data-direction="${wanted}"]`).click();await page.waitForTimeout(100);const next=await state();visits.push(next.room.name);
  const scene=await page.locator('.terminal-feed').evaluate(n=>Array.from(n.querySelectorAll('[aria-label]')).map(x=>x.getAttribute('aria-label')));if(!scene[0]?.includes(next.room.name))throw Error('Current arrival not first in reader: '+JSON.stringify({next:next.room.name,scene}));
 }
 await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();
 const archive=await page.locator('details.history').textContent();if(!visits.every(name=>archive.includes(name)))throw Error('Previous visits lost from archive');
 const feed=page.locator('.terminal-feed');await feed.evaluate(n=>{n.scrollTop=30});const before=await feed.evaluate(n=>n.scrollTop);await page.getByRole('button',{name:'Mirar',exact:true}).click();await page.waitForTimeout(100);const after=await feed.evaluate(n=>n.scrollTop);if(Math.abs(after-before)>2)throw Error('Mirar scroll jumped');
 const widths=[];for(const width of [320,393,1440]){await page.setViewportSize({width,height:750});if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1))throw Error('Horizontal overflow '+width);widths.push(width);await page.screenshot({path:out+'/walking-'+width+'.png'});}
 await page.setViewportSize({width:393,height:750});await page.getByRole('button',{name:'Mapa',exact:true}).click();if(await page.getByText('Dónde estás',{exact:true}).count())throw Error('Redundant map card retained');const stubs=await page.locator('.discovered-frontier').count();if(!stubs)throw Error('No dashed unknown stubs');await page.screenshot({path:out+'/map-dashed.png'});
 await writeFile(out+'/client-report.json',JSON.stringify({status:'PASS',scope:'Six rapid UI steps, immediate current location, archived previous visits, Mirar scroll, three widths, dotted unknown map exits',visits,before,after,widths,stubs},null,2));
 await writeFile(out+'/report.json',JSON.stringify({initialLocation:first.room.id,currentLocation:fast.room.id,currentName:fast.room.name,reading,actions:fast.actions,shops:first.actions.filter(a=>['comprar','vender','reparar'].includes(a.id))},null,2));
}finally{await browser.close();}
