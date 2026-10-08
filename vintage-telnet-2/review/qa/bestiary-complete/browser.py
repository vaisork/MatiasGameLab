import json,time,pathlib
from playwright.sync_api import sync_playwright
root=pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo');out=root/'review/bestiary-complete';catalog=json.loads((root/'content/world.json').read_text())['creatures'];fauna={k:v for k,v in catalog.items() if v.get('combatant_kind')!='human'}
assert len(fauna)==15
for cid,v in fauna.items():assert (root/v['illustration'].lstrip('/')).is_file(),cid
results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True)
 for width in [320,393,1440]:
  ctx=browser.new_context(viewport={'width':width,'height':800});dm=browser.new_context();base='http://127.0.0.1:8099';page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def post(c,path,data):
   state=c.request.get(base+'/api/state').json();r=c.request.post(base+path,data={**data,'csrf_token':state['csrf_token']});assert r.ok,r.text();return r.json()
  post(ctx,'/api/account/register',{'username':'artcheck'+str(time.time_ns()),'password':'isolated-password'})
  made=post(ctx,'/api/character/create',{'name':'Arte de prueba','species':'humano','class_id':'juramentado'})
  post(dm,'/api/master/login',{'password':'isolated-review-only'});post(dm,'/api/master/approve',{'character_id':made['character']['id']});snap=ctx.request.get(base+'/api/state').json()
  snap['bestiary']=[{'id':k,'name':v['name'],'description':v['description'],'illustration':v['illustration']} for k,v in fauna.items()]
  page.route('**/api/state',lambda r:r.fulfill(json=snap));page.goto(base);page.get_by_role('button',name='Bestiario',exact=True).click();assert page.locator('.bestiary-thumbnail').count()==15
  for cid,v in fauna.items():
   page.get_by_role('button',name='Ver imagen de '+v['name'],exact=True).click();page.locator('dialog img').evaluate('(img)=>img.decode()');assert page.locator('dialog canvas').count()==0
   if cid in ['cornalomo','dorsalodo','rondamusgo']:page.screenshot(path=str(out/f'{width}-{cid}.png'))
   page.get_by_role('button',name='Cerrar',exact=True).click()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors;results.append({'width':width,'images':15,'allDecoded':True,'no3D':True,'noOverflow':True,'errors':errors});ctx.close();dm.close()
 browser.close()
(out/'report.json').write_text(json.dumps({'results':results,'scope':'Display-only fixture based on authoritative creature catalogue; no fabricated discoveries persisted; temporary accounts only.'},indent=2));print(json.dumps(results))
