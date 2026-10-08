import {chromium} from '/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import {spawn} from 'node:child_process';
import assert from 'node:assert/strict';
const out=new URL('./',import.meta.url),server=spawn('python3',['-u',new URL('serve.py',out).pathname],{stdio:'ignore'});let browser;
try{
 let ready=false;for(let i=0;i<80;i++){try{if((await fetch('http://127.0.0.1:8121/api/state')).ok){ready=true;break;}}catch{}await new Promise(resolve=>setTimeout(resolve,100));}assert(ready,'fixture server started');
 const snapshot=JSON.parse(fs.readFileSync(new URL('snapshot.json',out))),roadCount=new Set(snapshot.map.routes.map(r=>[r.from,r.to].sort().join('|'))).size;
 browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const results=[];
 for(const width of [393,1440]){
  const page=await browser.newPage({viewport:{width,height:950}}),errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('http://127.0.0.1:8121');await page.waitForLoadState('networkidle');await page.getByRole('button',{name:'Mapa',exact:true}).click();await page.locator('.discovered-roads').waitFor({state:'attached'});
  assert.equal(await page.locator('.discovered-roads path').count(),roadCount);
  const clipped=await page.locator('.discovered-place>span').evaluateAll(nodes=>nodes.filter(n=>n.scrollHeight>n.clientHeight+1).map(n=>n.textContent));assert.deepEqual(clipped,[]);
  for(const town of ['valdren_plaza','khariel_centro','brumak_centro','narevia_centro','velmora_centro','vaisgard_mercado']){
   await page.locator('#map-destination').selectOption(town);await page.waitForTimeout(100);const panel=page.locator('.discovered-panel');await panel.scrollIntoViewIfNeeded();await panel.screenshot({path:new URL(`${width}-${town}.png`,out).pathname});
  }
  await page.getByRole('button',{name:'Ver todo lo descubierto',exact:true}).click();await page.waitForTimeout(150);await page.locator('.discovered-panel').screenshot({path:new URL(`${width}-world.png`,out).pathname});
  const summary=page.getByText('Mapa 3D',{exact:true});await summary.click();await page.locator('.visual-3d.visual-ready canvas').waitFor();await page.waitForTimeout(500);
  const webgl=await page.locator('.world-3d canvas').evaluate(c=>{const gl=c.getContext('webgl2')||c.getContext('webgl');return {width:c.width,height:c.height,active:!!gl&&!gl.isContextLost()};});assert(webgl.active);
  await page.locator('.visual-3d.visual-ready').screenshot({path:new URL(`${width}-3d.png`,out).pathname});await summary.click();await page.waitForTimeout(100);assert.equal(await page.locator('canvas').count(),0);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);results.push({width,rooms:snapshot.map.nodes.length,roads:roadCount,clippedLabels:clipped,webgl,noDocumentOverflow:true,pageErrors:errors});await page.close();
 }
 const home=snapshot.map.nodes.find(n=>n.kind==='home'),homePage=await browser.newPage({viewport:{width:393,height:950}});
 const homeSnapshot={...snapshot,character:{...snapshot.character,location:home.id},map:{...snapshot.map,current:home.id,nodes:[{...home,unexplored_directions:['salir']}],edges:[],routes:[],frontiers:[{from:home.id,direction:'salir'}]}};
 await homePage.route('**/api/state',route=>route.fulfill({json:homeSnapshot}));await homePage.goto('http://127.0.0.1:8121');await homePage.waitForLoadState('networkidle');await homePage.getByRole('button',{name:'Mapa',exact:true}).click();assert.equal(await homePage.locator('.discovered-frontier').count(),0,'abstract home entrance must not invent east/west orientation');await homePage.close();
 fs.writeFileSync(new URL('browser-report.json',out),JSON.stringify({scope:'Isolated Engine diagram fixture, not production or physical mobile gameplay. Separate API walks recorded in cycle-*.json.',abstractHomeFrontier:true,results},null,2)+'\n');console.log(JSON.stringify(results));
}finally{if(browser)await browser.close();server.kill('SIGTERM');}
