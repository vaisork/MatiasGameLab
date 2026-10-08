// Read-only review of a saved map snapshot and species UI; never submits player actions.
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
const {chromium}=await import(process.env.VT_REVIEW_PLAYWRIGHT||'playwright');
const state=JSON.parse(await readFile(process.env.VT_REVIEW_STATE,'utf8'));
const output=process.env.VT_REVIEW_OUTPUT||'/tmp/vt-map-species-review';await mkdir(output,{recursive:true});
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:393,height:750}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/api/state',r=>r.fulfill({json:state}));
 await page.goto(process.env.VT_REVIEW_URL||'http://127.0.0.1:8098');
 await page.getByRole('button',{name:'Mapa',exact:true}).click();
 assert.ok(await page.locator('.discovered-place').count()<=state.map.nodes.length);assert.equal(await page.locator('.discovered-current').count(),1);
 assert.equal(await page.locator('.map-route-direction').count(),0);assert.ok(await page.locator('.discovered-frontier').count()>0);assert.equal(await page.getByText('Dónde estás',{exact:true}).count(),0);
 await page.getByRole('button',{name:'Ver todo lo descubierto',exact:true}).click();assert.equal(await page.locator('.discovered-place').count(),state.map.nodes.length);await page.screenshot({path:`${output}/map-overview.png`});
 await page.getByRole('button',{name:'Volver a tu posición',exact:true}).click();await page.screenshot({path:`${output}/map-current.png`});
 await page.getByRole('button',{name:'Personaje',exact:true}).click();await page.locator('.species-art-button img').evaluate(i=>i.decode());await page.screenshot({path:`${output}/character.png`});
 await page.getByRole('button',{name:/Ver representación de/}).click();await page.locator('dialog[open] img').evaluate(i=>i.decode());await page.keyboard.press('Escape');await page.locator('dialog').waitFor({state:'detached'});
 await page.getByText('Las cinco especies',{exact:true}).click();
 for(const name of ['Humano','Felaryn','Dravak','Marevyn','Vesperi']){
  await page.getByRole('button',{name:`Ver especie ${name}`,exact:true}).click();await page.locator('dialog[open] img').evaluate(i=>i.decode());await page.screenshot({path:`${output}/${name.toLowerCase()}.png`});
  await page.getByRole('button',{name:'Cerrar',exact:true}).click();await page.locator('dialog').waitFor({state:'detached'});
 }
 await page.locator('.species-gallery').scrollIntoViewIfNeeded();await page.screenshot({path:`${output}/species-gallery.png`});
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
 await writeFile(`${output}/report.json`,JSON.stringify({status:'PASS',scope:'Read-only Chromium: saved known map, orthogonal links and actual direction labels; character portrait and five species gallery; decode, expand and close; mobile overflow',knownNodes:state.map.nodes.length,limits:['State intercepted for read-only UI review','Emulated mobile, not physical Android']},null,2));
}finally{await browser.close();}
