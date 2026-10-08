// Read-only UI review: VT_REVIEW_STATE is a temporary snapshot; never writes player data.
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
const {chromium}=await import(process.env.VT_REVIEW_PLAYWRIGHT||'playwright');
const state=JSON.parse(await readFile(process.env.VT_REVIEW_STATE,'utf8'));
const output=process.env.VT_REVIEW_OUTPUT||'/tmp/vt-bestiary-review';await mkdir(output,{recursive:true});
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:393,height:750}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/api/state',r=>r.fulfill({json:state}));
 await page.goto(process.env.VT_REVIEW_URL||'http://127.0.0.1:8083');
 await page.getByRole('button',{name:'Bestiario',exact:true}).click();
 assert.equal(await page.locator('.bestiary-thumbnail').count(),state.bestiary.length);
 assert.equal(await page.locator('.bestiary-art').count(),0);
 for(const entry of state.bestiary){
  const thumb=page.getByRole('button',{name:`Ver imagen de ${entry.name}`,exact:true});
  await thumb.locator('img').evaluate(i=>i.decode());const box=await thumb.boundingBox();assert.ok(box.width<=56&&box.height<=56);
  await thumb.click();await page.locator('dialog[open] img').evaluate(i=>i.decode());
  await page.screenshot({path:`${output}/${entry.id}-expanded.png`});
  await page.getByRole('button',{name:'Cerrar',exact:true}).click();await page.locator('dialog').waitFor({state:'detached'});
 }
 await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${output}/bestiary-list.png`});
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
 await writeFile(`${output}/report.json`,JSON.stringify({status:'PASS',scope:'Read-only Chromium UI review using saved discovered bestiary: five thumbnails, real asset decoding, click-to-expand, close, mobile overflow',creatures:state.bestiary.map(e=>e.id),limits:['Emulated mobile, not physical Android','API state intercepted for read-only display; no player actions performed']},null,2));
}finally{await browser.close();}
