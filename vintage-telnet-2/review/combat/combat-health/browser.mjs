import {chromium} from '/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs';
import {readFile,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const baseline=JSON.parse(await readFile('/tmp/vt-desktop-map-state.json','utf8'));
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
const results=[];
try{
 for(const width of [1440,393,320]){
  const page=await browser.newPage({viewport:{width,height:900}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const state=structuredClone(baseline);
  state.character.hp=20;state.character.hp_max=100;
  state.character.combat={name:'Pinzajunco',hp:40,hp_max:100,round:2};
  await page.route('**/api/state',r=>r.fulfill({json:state}));
  await page.goto('http://127.0.0.1:8083');
  const meters=page.getByRole('meter');await meters.first().waitFor();
  assert.equal(await meters.count(),2);
  assert.equal(await page.getByRole('meter',{name:'Salud de Tú'}).getAttribute('aria-valuenow'),'20');
  assert.equal(await page.locator('.health-critical .combat-vital-fill').evaluate(e=>e.style.width),'20%');
  assert.equal(await page.locator('.health-low .combat-vital-fill').evaluate(e=>e.style.width),'40%');
  assert.equal(await meters.first().evaluate(e=>e.getBoundingClientRect().height),3);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.screenshot({path:`review/combat/combat-health/${width}.png`});
  state.character.hp=80;state.character.combat.hp=100;
  await page.reload();await page.locator('.health-good').first().waitFor();
  assert.equal(await page.locator('.health-good').count(),2);
  assert.equal(await page.getByRole('meter',{name:'Salud de Tú'}).getAttribute('aria-valuenow'),'80');
  state.character.combat=null;await page.reload();await page.locator('.room-context').waitFor();
  assert.equal(await meters.count(),0);assert.deepEqual(errors,[]);
  results.push({width,height:3,lowHealthColors:true,healthUpdates:true,hiddenOutsideCombat:true,errors});
  await page.close();
 }
 await writeFile('review/combat/combat-health/browser.json',JSON.stringify({scope:'Read-only intercepted snapshot, no player actions; Chrome with desktop and mobile viewports.',results},null,2));
 console.log(JSON.stringify(results));
}finally{await browser.close()}
