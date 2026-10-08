import json,time,pathlib,uuid
from collections import deque
from playwright.sync_api import sync_playwright
base='http://127.0.0.1:8099'; out=pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/review/gender-browser');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True)
 checks=[]; errors=[]
 def post(c,path,data):
  s=c.request.get(base+'/api/state').json();r=c.request.post(base+path,data={**data,'csrf_token':s['csrf_token']});assert r.ok,r.text();return r.json()
 for index,gender in enumerate(['masculino','femenino',None]):
  c=b.new_context(viewport={'width':320 if index!=1 else 393,'height':800});page=c.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
  post(c,'/api/account/register',{'username':'gender'+str(time.time_ns()),'password':'isolated-test-password'})
  if gender is None:
   created=post(c,'/api/character/create',{'name':'Persona previa','species':'humanos','class_id':'juramentado'})
  else:
   page.goto(base);page.wait_for_load_state('networkidle');page.get_by_label('Nombre de tu personaje').fill('Persona prueba')
   field=page.get_by_label('Género',exact=True);assert field.input_value()=='';assert not field.evaluate('(e)=>e.checkValidity()');checks.append('required blank '+gender)
   field.select_option(gender);page.get_by_role('button',name='Presentar mi personaje').click();page.get_by_text('Pendiente de aprobación',exact=True).wait_for()
   created=c.request.get(base+'/api/state').json()
  dm=b.new_context();post(dm,'/api/master/login',{'password':'isolated-review-only'});post(dm,'/api/master/approve',{'character_id':created['character']['id']});dm.close()
  page.goto(base);page.wait_for_load_state('networkidle');page.get_by_role('button',name='Personaje',exact=True).click()
  page.get_by_role('button',name='Guardar género',exact=True).wait_for();field=page.get_by_label('Género',exact=True)
  assert field.input_value()==(gender or '')
  if gender is None:assert page.get_by_text('Sin elegir',exact=True).count()==1
  wanted='femenino' if gender!='femenino' else 'masculino';field.select_option(wanted);page.get_by_role('button',name='Guardar género',exact=True).click()
  page.wait_for_function('(g)=>document.querySelector("select[name=gender]")?.value===g',arg=wanted)
  page.wait_for_timeout(500);assert c.request.get(base+'/api/state').json()['character']['gender']==wanted
  page.reload();page.wait_for_load_state('networkidle');page.get_by_role('button',name='Personaje',exact=True).click();assert page.get_by_label('Género',exact=True).input_value()==wanted
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'horizontal overflow'
  page.screenshot(path=str(out/f'{index}-{320 if index!=1 else 393}.png'),full_page=True);checks.append('profile persisted '+str(gender))
  if gender is None:
   def act(id,target=None):return post(c,'/api/action',{'id':id,'target':target,'request_id':str(uuid.uuid4())})
   act('mover','salir');rooms={}
   for f in pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/content/regions').glob('*.json'):rooms.update(json.loads(f.read_text())['rooms'])
   dest=next(key for key,r in rooms.items() if 'edran_daro' in r.get('npcs',[]))
   current=c.request.get(base+'/api/state').json()['room']['id'];q=deque([(current,[])]);seen={current};steps=None
   while q:
    at,path=q.popleft()
    if at==dest:steps=path;break
    for direction,to in rooms[at].get('exits',{}).items():
     if to not in seen:seen.add(to);q.append((to,path+[direction]))
   assert steps is not None
   for direction in steps:act('mover',direction)
   page.reload();page.wait_for_load_state('networkidle');page.get_by_role('button',name='Mochila',exact=True).click()
   purchase=page.locator('button').filter(has_text='Comprar').first;purchase.wait_for()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert purchase.locator('small.action-reason').count()>0
   page.screenshot(path=str(out/'purchases-320.png'),full_page=True);checks.append('purchase reason visible and no overflow 320')
  c.close()
 assert not errors,errors
 (out/'report.json').write_text(json.dumps({'status':'PASS','checks':checks,'pageerrors':errors,'scope':'Isolated 8099 accounts; real UI creation and legacy profile, 320/393px, refresh persistence; no production accounts'},indent=2));b.close()
 print('PASS',checks)
