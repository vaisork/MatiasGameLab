from pathlib import Path
import json
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent;results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True)
 for width in [393,1440]:
  page=b.new_page(viewport={'width':width,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8121');page.wait_for_load_state('networkidle');page.get_by_role('button',name='Mapa',exact=True).click();summary=page.get_by_text('Mapa 3D',exact=True);summary.click();page.locator('.visual-3d.visual-ready canvas').wait_for();page.wait_for_timeout(800)
  canvas=page.locator('.world-3d canvas');assert canvas.count()==1;context=canvas.evaluate('(c)=>{const gl=c.getContext("webgl2")||c.getContext("webgl");return {width:c.width,height:c.height,webgl:!!gl,lost:gl?.isContextLost()}}');assert context['webgl'] and not context['lost'] and context['width']>0 and context['height']>0
  panel=page.locator('.visual-3d.visual-ready');panel.scroll_into_view_if_needed();panel.screenshot(path=str(OUT/f'{width}-map3d.png'));summary.click();page.wait_for_timeout(150);assert page.locator('canvas').count()==0;assert not errors,errors;results.append({'width':width,'actualWebGL':context,'closedCanvases':0,'pageErrors':errors});page.close()
 b.close()
(OUT/'browser-3d-report.json').write_text(json.dumps({'scope':'Real Chromium WebGL rendering of isolated184-room/197-road Engine snapshot fixture, not physical mobile or gameplay session; no production actions','results':results},indent=2));print(results)
