import {chromium} from '/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs';
import {readFile,writeFile} from 'node:fs/promises';
const states=JSON.parse(await readFile('/tmp/vt-combat-choice-states.json','utf8'));
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
const results=[];
try{for(const width of [1440,393,320]){const state=states[0],tell=state.character.combat.prepared_action.tell,page=await browser.newPage({viewport:{width,height:900}});await page.route('**/api/state',r=>r.fulfill({json:state}));await page.goto('http://127.0.0.1:8083');await page.locator('.terminal-feed').waitFor();const start=Date.now();await page.waitForFunction(t=>document.querySelector('.terminal-feed')?.textContent.includes(t),tell);const elapsed=Date.now()-start;assert.ok(elapsed<1000);
const gradual=await page.locator('.terminal-feed .event-world').first().evaluate(e=>e.textContent.length<e.getAttribute('aria-label').length);assert.equal(gradual,true);
await page.waitForTimeout(80);
const visible=await page.locator('.terminal-feed').evaluate((feed,tell)=>{const node=[...feed.querySelectorAll('.event')].find(e=>e.getAttribute('aria-label')===tell),a=node.getBoundingClientRect(),b=feed.getBoundingClientRect();return a.bottom<=b.bottom+2&&a.bottom>b.top},tell);assert.equal(visible,true);
await page.screenshot({path:`review/combat-timing/initial-${width}.png`});
await page.waitForFunction(()=>{const e=document.querySelector('.terminal-feed');return e.scrollHeight-e.clientHeight>60});const scroll=await page.locator('.terminal-feed').evaluate(e=>{e.scrollTop=0;e.dispatchEvent(new Event('scroll'));return {top:e.scrollTop,overflow:e.scrollHeight>e.clientHeight}});await page.waitForTimeout(100);assert.equal(await page.locator('.terminal-feed').evaluate(e=>e.scrollTop),scroll.top);
await page.screenshot({path:`review/combat-timing/${width}.png`});results.push({width,tellCompleteMs:elapsed,roundWindowMs:4000,ambientStillProgressive:gradual,tacticalTellVisibleWhileFollowing:visible,manualScrollPreserved:true,feedOverflow:scroll.overflow});await page.close();}await writeFile(process.argv[2]||'review/combat-timing/after.json',JSON.stringify({scope:'Readonly real Chrome, actual isolated encounter snapshot, normal progressive reading; no production mutations',results},null,2));console.log(results)}finally{await browser.close()}
