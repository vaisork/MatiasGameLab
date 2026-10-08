import json,time,pathlib,uuid,re
from collections import deque
from playwright.sync_api import sync_playwright
base='http://127.0.0.1:8099';out=pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/review/vesperi-ui-final');out.mkdir(exist_ok=True);results=[]
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
  if width==320:
   def act(id,target=None):return post(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4())})
   act('mover','salir');rooms={}
   for f in pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/content/regions').glob('*.json'):rooms.update(json.loads(f.read_text())['rooms'])
   current=c.request.get(base+'/api/state').json()['room']['id'];q=deque([(current,[])]);seen={current}
   while q:
    at,steps=q.popleft()
    if at=='valdren_fragua':break
    for direction,to in rooms[at].get('exits',{}).items():
     if to not in seen:seen.add(to);q.append((to,steps+[direction]))
   for direction in steps:
    s=c.request.get(base+'/api/state').json();move=next(a for a in s['actions'] if a['id']=='mover' and a.get('target')==direction)
    if move.get('disabled'):
     permit=next(a for a in s['actions'] if a['id'].startswith('pedir_permiso'));act(permit['id'],permit.get('target'))
    act('mover',direction)
   page.reload();page.wait_for_load_state('networkidle');page.get_by_role('button',name='Mochila',exact=True).click();hint=page.get_by_text(re.compile(r'^Necesitas 1 '));hint.wait_for();hint.scroll_into_view_if_needed();assert hint.is_visible();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(out/'320-material.png'))
  assert not errors,errors;assert not csp,csp;results.append({'width':width,'actualModel':'vesperi','closedCanvas':0,'noOverflow':True,'pageErrors':errors,'cspErrors':csp,'materialHintChecked':width==320});c.close()
 b.close()
(out/'report.json').write_text(json.dumps({'status':'PASS','results':results,'scope':'Real UI and isolated API accounts 8099; approved static species representation, not gendered geometry'},indent=2));print(json.dumps(results))
