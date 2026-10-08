import copy,json,pathlib
from playwright.sync_api import sync_playwright
base='http://127.0.0.1:8099';out=pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/review/sales-ui');out.mkdir(exist_ok=True);baseline=json.load(open('/tmp/vt-depth3-state.json'));results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True)
 for width in [320,393]:
  c=b.new_context(viewport={'width':width,'height':800});page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));snap=copy.deepcopy(baseline)
  snap['actions']=[{'id':'vender','target':snap['inventory'][0]['id'],'label':'Vender Espada de juramento · 29 sellos','confirmation':'¿Vender esta pieza por 29 sellos?'}]
  page.route('**/api/state',lambda route:route.fulfill(json=snap));page.goto(base);page.wait_for_load_state('networkidle');assert page.get_by_role('button',name='Director',exact=True).count()==0
  page.get_by_role('button',name='Ver objetos para vender (1)',exact=True).click();page.get_by_role('heading',name='Vender aquí',exact=True).wait_for();assert page.get_by_role('button',name='Vender Espada de juramento · 29 sellos',exact=True).count()==1
  assert page.evaluate('()=>document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(out/f'{width}-sell.png'),full_page=True)
  snap['actions']=[];snap['map']['nodes']=[{'id':snap['room']['id'],'name':snap['room']['name'],'visited':True,'kind':'settlement','region':'edran'},{'id':'valdren_fragua','name':'Fragua de Daro','visited':True,'kind':'workshop','region':'edran','commerce':{'buys_weapons':True,'buys_materials':False}},{'id':'hidden-buyer','name':'Nombre secreto no visitado','visited':False,'commerce':{'buys_materials':True}}]
  page.reload();page.wait_for_load_state('networkidle');page.get_by_role('button',name='Mochila',exact=True).click();assert page.get_by_role('button',name='Ver camino a Fragua de Daro',exact=True).count()==1;assert page.get_by_text('Nombre secreto no visitado').count()==0
  page.screenshot(path=str(out/f'{width}-find-buyer.png'),full_page=True);assert page.evaluate('()=>document.documentElement.scrollWidth<=innerWidth');assert not errors,errors;results.append({'width':width,'noPlayerDM':True,'saleProminent':True,'knownBuyerOnly':True,'noOverflow':True,'errors':errors});c.close()
 c=b.new_context();page=c.new_page();page.goto(base+'/dm');page.wait_for_load_state('networkidle');assert page.get_by_role('button',name='Entrar como director',exact=True).is_visible();results.append({'separateDMRoute':True});c.close();b.close()
(out/'report.json').write_text(json.dumps({'status':'PASS','scope':'Read-only browser presentation fixtures derived from saved approved API snapshot; sales action is a contract fixture, not transaction proof. Separate /dm uses actual endpoint. No accounts/data changed.','results':results},indent=2));print(results)
