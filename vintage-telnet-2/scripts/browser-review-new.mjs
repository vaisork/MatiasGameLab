import assert from 'node:assert/strict';
/** Fresh external review: npm install playwright in an isolated tooling directory.
 * VT_REVIEW_URL=http://127.0.0.1:8083 VT_REVIEW_DM_PASSWORD=... node scripts/browser-review-new.mjs
 * Requires an isolated server with a deterministic RNG returning 0 for chance assertions.
 * Creates a NEW review account; never modifies SQLite or invents known locations.
 */
const {chromium}=await import(process.env.VT_REVIEW_PLAYWRIGHT||'playwright');
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const base=process.env.VT_REVIEW_URL||'http://127.0.0.1:8083';
const password=process.env.VT_REVIEW_DM_PASSWORD;
if(!password)throw Error('Set VT_REVIEW_DM_PASSWORD privately; it is never written to evidence.');
const output=process.env.VT_REVIEW_OUTPUT||'/tmp/vt-new-browser-review';
await mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true,channel:process.env.VT_REVIEW_BROWSER_CHANNEL||'chrome'});
const context=await browser.newContext({viewport:{width:390,height:844}});
const page=await context.newPage(),failures=[];
page.on('pageerror',error=>failures.push(error.message));
page.on('console',message=>{if(message.type()==='error')failures.push(message.text()+' '+message.location().url);});
const username=`lectora${Date.now()}`,accountPassword=`Review-${Date.now()}-only`;
async function screenshot(name){await page.screenshot({path:`${output}/${name}.png`,fullPage:true});}
async function noOverflow(){if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1))throw Error('Horizontal overflow');}
try{
 await page.goto(base);await page.getByRole('button',{name:'Crear cuenta',exact:true}).click();
 await page.getByLabel('Nombre de cuenta').fill(username);
 await page.getByLabel('Contraseña',{exact:true}).fill(accountPassword);
 await page.locator('form button[type=submit]').click();
 await page.getByLabel('Nombre de tu personaje').fill('Lectora de revisión');
 await page.locator('select[name=species]').selectOption('felaryn');
 await page.locator('select[name=class_id]').selectOption('sombra');
 await page.getByRole('button',{name:'Presentar mi personaje'}).click();
 await page.getByText('Pendiente de aprobación',{exact:true}).waitFor();
 const director=await context.newPage();await director.goto(`${base}/dm`);
 await director.getByLabel('Contraseña del director').fill(password);
 await director.getByRole('button',{name:'Entrar como director'}).click();
 await director.locator('article').filter({hasText:'Lectora de revisión'}).getByRole('button',{name:'Aprobar personaje'}).click();
 await page.getByRole('button',{name:'Comprobar aprobación'}).click();
 await page.getByRole('region',{name:'Crónica de tu aventura'}).waitFor();
 await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();const scene=await page.locator('.reading').first().innerText();if(scene.length<180)throw Error('Initial scene missing or abbreviated');
 for(const [name,width,height] of [['mobile320',320,740],['mobile390',390,844],['desktop',1440,1000]]){
  await page.setViewportSize({width,height});await noOverflow();await screenshot(name);
 }
 await page.getByLabel('Escribe tu decisión').fill('observar');
 await page.getByRole('button',{name:'Decidir',exact:true}).click();
 await page.getByLabel('Escribe tu decisión').waitFor();
 await screenshot('observacion');
 await page.setViewportSize({width:393,height:750});
  const allRooms={};for(const region of ['edran','veyra','hoshai','korven','lethra','nhal']){const data=JSON.parse(await readFile(new URL(`../content/regions/${region}.json`,import.meta.url),'utf8'));if(Array.isArray(data.rooms)){for(const r of data.rooms)allRooms[r.id]=r;}else{Object.assign(allRooms,data.rooms);}}
 async function act(id,target){const current=await (await page.request.get(`${base}/api/state`)).json();const response=await page.request.post(`${base}/api/action`,{data:{id,target,request_id:crypto.randomUUID(),csrf_token:current.csrf_token},headers:{'X-CSRF-Token':current.csrf_token}});if(!response.ok())throw Error(await response.text());return response.json();}
 let current=await (await page.request.get(`${base}/api/state`)).json();if(current.room.id.startsWith('home:'))current=await act('mover','salir');
 const queue=[[current.room.id,[]]],seen=new Set([current.room.id]);let path;
 for(let i=0;i<queue.length;i++){const [id,steps]=queue[i];if(id==='lethra_tierra_esponjosa'){path=steps;break;}for(const [direction,to] of Object.entries(allRooms[id]?.exits||{})){if(!seen.has(to)){seen.add(to);queue.push([to,[...steps,direction]]);}}}
 if(!path)throw Error('No real route to review room');for(const direction of path)await act('mover',direction);
 await page.reload();await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();
 const feed=page.locator('.terminal-feed');await feed.evaluate(n=>{n.scrollTop=45;});await page.waitForTimeout(100);
 const before=await feed.evaluate(n=>({top:n.scrollTop,height:n.clientHeight,scroll:n.scrollHeight}));
 await page.getByRole('button',{name:'Mirar',exact:true}).click();await page.waitForTimeout(500);
 const after=await feed.evaluate(n=>({top:n.scrollTop,height:n.clientHeight,scroll:n.scrollHeight}));
 if(Math.abs(before.top-after.top)>2)throw Error(`Mirar scroll changed: ${JSON.stringify({before,after})}`);
 await page.screenshot({path:`${output}/mobile-reading.png`});
 await page.getByRole('button',{name:/^Buscar alrededor/}).click();await page.waitForTimeout(200);
 const searched=await (await page.request.get(`${base}/api/state`)).json();if(!searched.inventory.some(i=>i.id==='fibra_junco'))throw Error('Expected seeded regional search finding');
 await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();await page.screenshot({path:`${output}/mobile-search.png`});
 await page.getByRole('button',{name:'Mapa',exact:true}).click();await page.waitForTimeout(200);await noOverflow();
 await page.screenshot({path:`${output}/mobile-map-overview.png`});
 await page.getByRole('button',{name:'Volver a tu posición',exact:true}).click();await page.screenshot({path:`${output}/mobile-map-position.png`});
 if(!(await page.locator('.discovered-frontier').count()))throw Error('Unexplored branches missing from discovered map');
 await page.getByRole('button',{name:'Bestiario',exact:true}).click();await page.locator('img.bestiary-thumbnail').first().evaluate(image=>image.decode());
 assert.equal(await page.locator('dialog[open]').count(),0);assert.equal(await page.locator('img.bestiary-art').count(),0);
 const thumb=await page.locator('img.bestiary-thumbnail').first().boundingBox();assert.ok(thumb.height<=56&&thumb.width<=56);
 await page.screenshot({path:`${output}/mobile-bestiary.png`});
 await page.getByRole('button',{name:'Ver imagen de Pinzajunco',exact:true}).click();await page.locator('dialog[open] img.bestiary-art').evaluate(image=>image.decode());
 await page.screenshot({path:`${output}/mobile-bestiary-expanded.png`});await page.keyboard.press('Escape');await page.locator('dialog').waitFor({state:'detached'});
 await page.getByRole('button',{name:'Ver imagen de Pinzajunco',exact:true}).click();await page.getByRole('button',{name:'Cerrar',exact:true}).click();await page.locator('dialog').waitFor({state:'detached'});
 await page.getByRole('button',{name:'Aventura',exact:true}).click();
 await writeFile(`${output}/scroll-proof.json`,JSON.stringify({before,after,actualJourneySteps:path.length,viewport:{width:393,height:750}},null,2));
 current=await (await page.request.get(`${base}/api/state`)).json();
 const backQueue=[[current.room.id,[]]],backSeen=new Set([current.room.id]);let combatPath;
 for(let i=0;i<backQueue.length;i++){const [id,steps]=backQueue[i];if(id==='edran_arboleda'){combatPath=steps;break;}for(const [direction,to] of Object.entries(allRooms[id]?.exits||{})){if(!backSeen.has(to)){backSeen.add(to);backQueue.push([to,[...steps,direction]]);}}}
 if(!combatPath)throw Error('No real path to random combat habitat');for(const direction of combatPath)await act('mover',direction);
 await page.reload();await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();
 await page.getByRole('button',{name:'Enfrentarte a Espinajo de rastrojo',exact:true}).click();
 await page.getByRole('button',{name:/Borrar el Foco/}).click();await page.waitForTimeout(4500);
 await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();
 if(!(await page.locator('.terminal-feed').innerText()).includes('Usas Borrar el Foco'))throw Error('Class power consequence missing in actual reader');
 await page.screenshot({path:`${output}/mobile-power.png`});
 await act('huir');await page.waitForTimeout(4500);const fled=await (await page.request.get(`${base}/api/state`)).json();if(fled.character.combat)throw Error('Retreat did not resolve');await page.reload();await page.getByRole('button',{name:'Mostrar completo',exact:true}).click();
 const previous=(await page.request.get(`${base}/api/state`)).json();const state=await previous;
 await page.getByRole('button',{name:'Salir de la cuenta',exact:true}).click();
 await page.getByLabel('Nombre de cuenta').fill(username);await page.getByLabel('Contraseña',{exact:true}).fill(accountPassword);await page.locator('form button[type=submit]').click();
 await page.getByRole('region',{name:'Crónica de tu aventura'}).waitFor();
 const restored=await (await page.request.get(`${base}/api/state`)).json();
 if(restored.character.id!==state.character.id||restored.character.location!==state.character.location)throw Error('Relogin did not restore same character/location');
 if(await page.locator('.reading img,.reading canvas,.reading svg').count())throw Error('Unexpected graphical asset in reader');
 if(failures.length)throw Error(`Browser errors: ${failures.join('; ')}`);
 const hashes={};for(const file of ['index.html','style.css','app.js','ui-data.js'])hashes[file]=createHash('sha256').update(await readFile(new URL(`../client/${file}`,import.meta.url))).digest('hex');
 await writeFile(`${output}/report.json`,JSON.stringify({status:'PASS',username,scope:'Chromium: registration, approval, observation, 19-step real route to Lethra, preserved Mirar scroll, regional search finding, compact bestiary thumbnails, click-to-expand illustration, Escape/button close, dotted unexplored exit stubs, random habitat encounter, Sombra power, retreat, map overview/current position, logout/relogin, three viewport widths',limits:['Not a 20–30 minute human session','Paid quest must be reviewed separately through real travel'],hashes},null,2));
}catch(error){await page.screenshot({path:`${output}/failure.png`,fullPage:true});throw error;}finally{await browser.close();}
