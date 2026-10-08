import json,time,pathlib,uuid,re
from collections import deque
from playwright.sync_api import sync_playwright
base='http://127.0.0.1:8099';out=pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/review/bestiary-species-regression');out.mkdir(exist_ok=True);results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True)
 for width in [320,393]:
  c=b.new_context(viewport={'width':width,'height':800});dm=b.new_context();page=c.new_page();errors=[];csp=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:csp.append(m.text) if 'Content Security Policy' in m.text else None)
  def post(ctx,path,data):
   s=ctx.request.get(base+'/api/state').json();r=ctx.request.post(base+path,data={**data,'csrf_token':s['csrf_token']});assert r.ok,r.text();return r.json()
  post(c,'/api/account/register',{'username':'vesperiui'+str(time.time_ns()),'password':'isolated-test-password'})
  made=post(c,'/api/character/create',{'name':'Prueba Vesperi','species':'vesperi','class_id':'juramentado','gender':'femenino'})
  post(dm,'/api/master/login',{'password':'isolated-review-only'});post(dm,'/api/master/approve',{'character_id':made['character']['id']});dm.close()
  page.goto(base);page.wait_for_load_state('networkidle');page.get_by_role('button',name='Personaje',exact=True).click();page.get_by_role('button',name='Ver representación de Vesperi',exact=True).click()
  dialog=page.locator('dialog');dialog.get_by_text('Ver representación 3D de la especie',exact=True).click()
  page.wait_for_function('()=>document.querySelector("dialog .figure-3d")?.dataset.modelAsset==="vesperi"',timeout=60000)
  assert dialog.locator('canvas').count()==1;dialog.locator('.visual-3d').scroll_into_view_if_needed();page.wait_for_timeout(400)
  page.screenshot(path=str(out/f'{width}-vesperi.png'));dialog.get_by_role('button',name='Girar miniatura',exact=True).click();dialog.get_by_role('button',name='Cerrar',exact=True).click();page.wait_for_timeout(200)
  assert page.locator('canvas').count()==0
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  snap=c.request.get(base+'/api/state').json();catalog=json.loads(pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/content/world.json').read_text())['creatures']
  with_art=next((cid,v) for cid,v in catalog.items() if v.get('illustration'));without_art=next((cid,v) for cid,v in catalog.items() if not v.get('illustration'))
  snap['bestiary']=[{'id':cid,'name':v['name'],'description':v.get('description','Criatura conocida.'),'status':'avistado',**({'illustration':v['illustration']} if v.get('illustration') else {})} for cid,v in [with_art,without_art]]
  page.route('**/api/state',lambda route:route.fulfill(json=snap))
  page.reload();page.wait_for_load_state('networkidle');page.get_by_role('button',name='Bestiario',exact=True).click()
  assert page.locator('.bestiary-thumbnail').count()==1
  assert page.get_by_text('Ver miniatura 3D',exact=True).count()==0
  page.screenshot(path=str(out/f'{width}-bestiary-list.png'))
  page.get_by_role('button',name='Ver imagen de '+with_art[1]['name'],exact=True).click();page.locator('dialog img').evaluate('(img)=>img.decode()')
  assert page.locator('dialog canvas').count()==0;assert page.locator('dialog .visual-3d').count()==0;assert page.locator('dialog summary').count()==0
  page.screenshot(path=str(out/f'{width}-bestiary-2d.png'));page.get_by_role('button',name='Cerrar',exact=True).click()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors;assert not csp,csp
  results.append({'width':width,'actualSpeciesModel':'vesperi','canvasAfterClose':0,'bestiary2DOnly':True,'withoutArtTextOnly':True,'noOverflow':True,'pageErrors':errors,'cspErrors':csp});c.close()
 b.close()
(out/'report.json').write_text(json.dumps({'status':'PASS','results':results,'scope':'Species real account/API8099; bestiary display-only intercepted state derived from current authoritative world creature catalog, one with art and one without; no discovery claim and no persisted fabricated knowledge'},indent=2));print(json.dumps(results))
