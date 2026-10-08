import {chromium,request} from '/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs';
import assert from 'node:assert/strict';import {writeFile} from 'node:fs/promises';
const base='https://raspberrypi.tail3d212e.ts.net',api=await request.newContext({baseURL:base}),rows=[];
for(const p of ['/','/dm','/client/art/places/valdren_huertos-anime-v1-thumb.webp','/client/art/places/valdren_huertos-anime-v1.webp','/client/art/places/hoshai_agua_fria-anime-v1.webp']){
 const r=await api.get(p);assert.equal(r.status(),200,p);rows.push({path:p,status:r.status()});
}
const state=await(await api.get('/api/state')).json();
for(const [p,data] of [['/api/master/login',{password:'intentionally-invalid-deployment-check'}],['/api/account/login',{username:'nonexistent-deployment-check',password:'intentionally-invalid-deployment-check'}]]){
 const r=await api.post(p,{data:{...data,csrf_token:state.csrf_token},headers:{Origin:base}});assert.equal(r.status(),401,`${p}: ${await r.text()}`);rows.push({path:p,status:r.status(),meaning:'Origin and CSRF accepted; invalid credentials rejected.'});
}
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
try{
 for(const width of [393,1440]){
  const context=await browser.newContext({viewport:{width,height:900}}),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.getByRole('button',{name:'Crear cuenta',exact:true}).waitFor();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
  await page.goto(base+'/dm');await page.getByLabel('Contraseña del director').waitFor();assert.deepEqual(errors,[]);rows.push({width,gameAndDM:true,noOverflow:true,errors});await context.close();
 }
}finally{await browser.close();await api.dispose();}
await writeFile('review/qa/raspberry-deploy/update-d5ee227/public-check.json',JSON.stringify({version:'d5ee22799c83e7c32cb076fd70df1b1885e45d9f',rows},null,2));console.log(JSON.stringify(rows));
