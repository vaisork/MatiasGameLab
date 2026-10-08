import fs from 'node:fs';
import {chromium} from '/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs';
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
fs.mkdirSync('review/tester-travel-browser',{recursive:true});
for(const width of [320,393,1440]){
 const context=await browser.newContext({viewport:{width,height:900}}),page=await context.newPage();let errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8119');
 await page.evaluate(async width=>{const post=async(path,data)=>{const s=await(await fetch('/api/state')).json();const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':s.csrf_token},body:JSON.stringify(data)});if(!r.ok)throw Error(path+' '+r.status);return r.json();};await post('/api/account/register',{username:'tester'+width+Date.now(),password:'isolatedtest123'});let r=await post('/api/character/create',{name:'Tester'+width,species:'felaryn',class_id:'juramentado'});await post('/api/master/login',{password:'isolated-tester-only'});await post('/api/master/approve',{character_id:r.character.id});await post('/api/master/tester',{character_id:r.character.id,enabled:true});},width);
 await page.reload();await page.getByRole('button',{name:'Personaje',exact:true}).click();await page.getByText('Pruebas: cambiar de lugar',{exact:true}).click();
 await page.screenshot({path:`review/tester-travel-browser/panel-${width}.png`,fullPage:true});
 const checks=[];
 for(const destination of ['narevia_centro','valdren_fragua','lethra_mercado_hojas','edran_canal_entrada','korven_almacen_entrada']){
  if(destination!=='narevia_centro'){await page.getByRole('button',{name:'Personaje',exact:true}).click();await page.getByText('Pruebas: cambiar de lugar',{exact:true}).click();}
  await page.locator('select[name=destination]').selectOption(destination);await page.getByRole('button',{name:'Ir al destino de prueba',exact:true}).click();await page.waitForTimeout(600);
  const s=await page.evaluate(async()=> (await fetch('/api/state')).json());if(s.character.location!==destination||s.map.edges.length!==0)throw Error('Travel/map invalid');if(!(await page.getByRole('region',{name:'Crónica de tu aventura'}).isVisible()))throw Error('Did not return adventure');if(errors.length)throw Error(errors.join(','));
  if(!s.narrative.some(e=>e.kind==='world'&&e.text===s.room.description))throw Error('Arrival missing '+destination);
  if(s.character.xp!==0||s.character.seals!==20)throw Error('Tester granted rewards');
  if(['valdren_fragua','lethra_mercado_hojas'].includes(destination)&&!s.actions.some(a=>a.id==='comprar'))throw Error('Shop not usable');
  checks.push({destination,name:s.room.name,npcs:s.room.npcs.map(n=>n.name),actions:s.actions.map(a=>a.id),edges:s.map.edges.length,xp:s.character.xp,seals:s.character.seals});
  await page.screenshot({path:`review/tester-travel-browser/${destination}-${width}.png`,fullPage:true});
 }
 console.log(JSON.stringify({width,checks,pageErrors:errors}));fs.writeFileSync(`review/tester-travel-browser/results-${width}.json`,JSON.stringify({width,checks,pageErrors:errors},null,2));await context.close();
}
await browser.close();
