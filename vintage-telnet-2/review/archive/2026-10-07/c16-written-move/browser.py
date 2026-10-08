import json,time,pathlib,uuid
from playwright.sync_api import sync_playwright
base='http://127.0.0.1:8099';out=pathlib.Path('/home/jdiaz/proyectos/vintage-telnet-2-nuevo/review/c16-written-move');out.mkdir(exist_ok=True);results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True)
 for width in [320]:
  c=b.new_context(viewport={'width':width,'height':800});dm=b.new_context();page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def state():return c.request.get(base+'/api/state').json()
  def post(ctx,path,data):
   s=ctx.request.get(base+'/api/state').json();r=ctx.request.post(base+path,data={**data,'csrf_token':s['csrf_token']});assert r.ok,r.text();return r.json()
  post(c,'/api/account/register',{'username':'fastwalk'+str(time.time_ns()),'password':'isolated-test-password'});made=post(c,'/api/character/create',{'name':'Paso rápido','species':'humanos','class_id':'juramentado','gender':'masculino'});post(dm,'/api/master/login',{'password':'isolated-review-only'});post(dm,'/api/master/approve',{'character_id':made['character']['id']});dm.close()
  post(c,'/api/action',{'id':'mover','target':'salir','request_id':str(uuid.uuid4())});page.goto(base);page.wait_for_load_state('networkidle');records=[];inverse={'norte':'sur','sur':'norte','este':'oeste','oeste':'este'}
  first=next(a for a in state()['actions'] if a['id']=='mover' and a.get('target') in inverse and not a.get('disabled'));direction=first['target']
  for i in range(2):
   before=state();target=direction if i%2==0 else inverse[direction];control=page.locator('button[data-direction="'+target+'"]');control.wait_for(state='visible');t=time.monotonic();control.click()
   page.wait_for_function('(old)=>document.querySelector(".room-context h1")?.textContent!==old',arg=before['room']['name'])
   after=state();metrics=page.evaluate('''()=>({room:document.querySelector('.room-context h1')?.textContent,scrollY,contextTop:document.querySelector('.room-context').getBoundingClientRect().top,readingTop:document.querySelector('.reading').getBoundingClientRect().top,navTop:document.querySelector('#navigation').getBoundingClientRect().top,shown:document.querySelector('.terminal-feed').innerText,paragraphs:Array.from(document.querySelectorAll('.terminal-feed .event')).map(p=>({hidden:p.hidden,total:p.getAttribute('aria-label').length,shown:p.querySelector('span:last-child')?.textContent.length})),canvases:document.querySelectorAll('canvas').length,overflow:document.documentElement.scrollWidth>innerWidth})''')
   records.append({'step':i+1,'direction':target,'room':after['room']['id'],'latency':round(time.monotonic()-t,3),**metrics})
   if i in [0,1,19]:page.screenshot(path=str(out/f'{width}-step{i+1}.png'))
  for command in [direction]:
   page.locator('input[name=decision]').fill(command);page.get_by_role('button',name='Decidir',exact=True).click();page.wait_for_timeout(300)
  page.screenshot(path=str(out/f'{width}-observe.png'));page.wait_for_timeout(100);assert abs(page.locator('.room-context').bounding_box()['y'])<=1;finalMetrics=page.evaluate('()=>({scrollY,readerTop:document.querySelector(".reading").getBoundingClientRect().top,readerBottom:document.querySelector(".reading").getBoundingClientRect().bottom,navTop:document.querySelector("#navigation").getBoundingClientRect().top,feedTop:document.querySelector(".terminal-feed").getBoundingClientRect().top,feedBottom:document.querySelector(".terminal-feed").getBoundingClientRect().bottom})');page.screenshot(path=str(out/f'{width}-settled.png'));results.append({'width':width,'moves':records,'errors':errors,'afterWrittenDecision':finalMetrics,'finalRoom':state()['room']['id'],'canvasCount':page.locator('canvas').count()});c.close()
 b.close()
(out/'report.json').write_text(json.dumps({'scope':'BEFORE real browser/mobile and 20 legal repeated route moves per width plus mirar/observar; isolated accounts8099, no edits','results':results},indent=2));print(json.dumps([{'width':r['width'],'moves':len(r['moves']),'errors':r['errors'],'scrolls':[m['scrollY'] for m in r['moves']],'latencies':[m['latency'] for m in r['moves']]} for r in results]))
