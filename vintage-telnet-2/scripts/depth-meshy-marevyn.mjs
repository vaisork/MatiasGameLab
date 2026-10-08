import assert from 'node:assert/strict';
import {chromium} from '/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs';
import {mkdir,writeFile} from 'node:fs/promises';
const phase=process.env.VT_MODEL_PHASE||'original',base=process.env.VT_MODEL_BASE||'http://127.0.0.1:8083';
const out=`/home/jdiaz/proyectos/vintage-telnet-2-nuevo/review/meshy-marevyn-${phase}`;
await mkdir(out,{recursive:true});
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
const errors=[],results=[];
for(const width of [320,393,1100]){
 const page=await browser.newPage({viewport:{width,height:720}});page.on('pageerror',e=>errors.push(e.message));
 if(phase==='original')await page.route('**/client/models/species/marevyn.glb',route=>route.fulfill({path:'/home/jdiaz/Escritorio/Vintage Telnet - Meshy/marevyn.glb',contentType:'model/gltf-binary'}));
 await page.goto(base);await page.evaluate(async()=>{const figure=document.createElement('div');figure.id='figure';figure.style.height='540px';figure.style.position='relative';document.body.replaceChildren(figure);document.body.style.margin='8px';window.api=await import('/client/world3d.js');window.dispose=window.api.mountFigure3D(document.querySelector('#figure'),{kind:'species',id:'marevyn',time:'Día'});});
 await page.waitForFunction(()=>document.querySelector('#figure').dataset.modelAsset==='marevyn',null,{timeout:120000});await page.waitForTimeout(500);
 await page.locator('#figure').screenshot({path:`${out}/${width}-front.png`});
 for(let i=0;i<4;i++)await page.getByRole('button',{name:'Girar miniatura',exact:true}).click();await page.waitForTimeout(100);
 await page.locator('#figure').screenshot({path:`${out}/${width}-back.png`});
 await page.evaluate(()=>window.dispose());assert.equal(await page.locator('canvas').count(),0);
 // Force a late completion and verify that it never reinstates a released view.
 await page.evaluate(()=>{window.dispose=window.api.mountFigure3D(document.querySelector('#figure'),{kind:'species',id:'marevyn'});window.dispose();});await page.waitForTimeout(1500);assert.equal(await page.locator('canvas').count(),0);
 await page.route('**/client/models/species/marevyn.glb',route=>route.fulfill({status:404,body:'Not available'}));await page.evaluate(()=>{window.dispose=window.api.mountFigure3D(document.querySelector('#figure'),{kind:'species',id:'marevyn'});});await page.waitForFunction(()=>document.querySelector('#figure').dataset.modelAsset==='fallback');assert.equal(await page.locator('canvas').count(),1);await page.evaluate(()=>window.dispose());results.push({width,loaded:true,canvasesAfterDispose:0,lateLoadDidNotRemount:true,errorPreservesProceduralFallback:true});await page.close();
}
assert.deepEqual(errors,[]);await writeFile(`${out}/report.json`,JSON.stringify({phase,results,errors,limits:'No animation clips supplied. Visual canon requires screenshot inspection.'},null,2));console.log(JSON.stringify({phase,results,errors}));await browser.close();
