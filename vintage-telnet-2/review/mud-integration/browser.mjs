import {chromium,request} from '/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs';
import {spawn} from 'node:child_process';
import {mkdtemp,rm,writeFile,readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import assert from 'node:assert/strict';
const data=await mkdtemp(join(tmpdir(),'vt-mud-pilot-')),base='http://127.0.0.1:8119';
const code="from server.app import create_app;from werkzeug.security import generate_password_hash;import os;app=create_app({'TESTING':True,'DATA_DIR':os.environ['VT_REVIEW_DATA'],'CLOCK':lambda:43200,'RNG':type('Quiet',(),{'random':lambda self:.99})(),'DM_PASSWORD_HASH':generate_password_hash('temporary-pilot-director')});app.run(host='127.0.0.1',port=8119,use_reloader=False)";
const server=spawn('python3',['-u','-c',code],{env:{...process.env,PYTHONPATH:'/home/jdiaz/proyectos/vintage-telnet-2-nuevo/runtime/python-deps',VT_REVIEW_DATA:data},stdio:'ignore'});
const rooms={};for(const r of ['edran','veyra','hoshai','korven','lethra','nhal'])Object.assign(rooms,JSON.parse(await readFile(`content/regions/${r}.json`,'utf8')).rooms);
let browser;const rows=[];
try{
 let ready=false;for(let i=0;i<80;i++){try{if((await fetch(base)).ok){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,100));}assert.ok(ready);
 browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const dm=await request.newContext({baseURL:base});
 const post=async(c,path,body)=>{const csrf_token=(await(await c.get(base+'/api/state')).json()).csrf_token;const response=await c.post(base+path,{data:{...body,csrf_token}});assert.ok(response.ok(),await response.text());return response.json();};
 await post(dm,'/api/master/login',{password:'temporary-pilot-director'});
 for(const width of [320,393,1440]){
  const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'}),c=context.request;
  await post(c,'/api/account/register',{username:`pilot${width}`,password:'temporary-pilot-player'});
  const created=await post(c,'/api/character/create',{name:`Lector ${width}`,species:'humano',class_id:'juramentado'});
  await post(dm,'/api/master/approve',{character_id:created.character.id});
  const act=(id,target)=>post(c,'/api/action',{id,target,request_id:crypto.randomUUID()});
  await act('mover','salir');
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(base);await page.locator('.room-context h1').waitFor();
  const feed=page.locator('.terminal-feed');assert.ok((await feed.innerText()).includes(rooms.valdren_plaza.description));assert.equal(await feed.locator('.event-location').count(),0);
  const s=await(await c.get(base+'/api/state')).json();const exit=s.room.exits.find(e=>e.direction!=='hogar');assert.ok(exit);
  await act('mover',exit.direction);const away=await(await c.get(base+'/api/state')).json();const back=Object.entries(rooms[away.room.id].exits).find(([,to])=>to==='valdren_plaza');assert.ok(back);await act('mover',back[0]);
  await page.reload();await page.locator('.room-context h1').waitFor();assert.ok((await feed.innerText()).includes(rooms.valdren_plaza.brief));assert.ok(!(await feed.innerText()).includes(rooms.valdren_plaza.description));
  await page.getByRole('button',{name:'Mirar',exact:true}).click();await feed.getByText(rooms.valdren_plaza.description,{exact:true}).waitFor();assert.equal(await feed.locator('.event-look').count(),1);
  await page.waitForTimeout(1600);assert.equal(await feed.locator('.event-look').count(),1);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
  await page.screenshot({path:`review/mud-integration/${width}-mirar.png`});
  const current=(await(await c.get(base+'/api/state')).json()).room.id,queue=[[current,[]]],seen=new Set([current]);let path;
  for(let i=0;i<queue.length;i++){const [id,p]=queue[i];if(id==='valdren_huertos'){path=p;break;}for(const [d,to] of Object.entries(rooms[id].exits||{}))if(!seen.has(to)){seen.add(to);queue.push([to,[...p,d]]);}}
  assert.ok(path);for(const d of path)await act('mover',d);await page.reload();await page.getByRole('button',{name:'Ver vista de Corredor de los Huertos',exact:true}).click();
  const image=page.locator('dialog[open] img');await image.evaluate(i=>i.decode());assert.equal(await image.evaluate(i=>i.naturalWidth),1200);await page.screenshot({path:`review/mud-integration/${width}-arte.png`});
  assert.deepEqual(errors,[]);rows.push({width,fullFirstVisit:true,briefReturn:true,explicitLook:true,noLocationDuplicate:true,noPassiveLookRepeat:true,artWidth:1200,noOverflow:true,errors});await context.close();
 }
 await dm.dispose();await writeFile('review/mud-integration/browser.json',JSON.stringify({scope:'Fresh temporary database, real game/API and Chrome. Reduced motion tests layout and content, not reading speed.',rows},null,2));console.log(JSON.stringify(rows));
}finally{if(browser)await browser.close();server.kill('SIGTERM');await rm(data,{recursive:true,force:true});}
