"""Chromium display QA of full-world Engine fixture; no human journey claim."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent;results=[];fixture=json.loads((OUT/'snapshot.json').read_text());roomCount=len(fixture['map']['nodes']);roadCount=len({tuple(sorted((r['from'],r['to']))) for r in fixture['map']['routes']})
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True)
 for width in [393,1440]:
  page=browser.new_page(viewport={'width':width,'height':950});errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('http://127.0.0.1:8121');page.wait_for_load_state('networkidle');page.get_by_role('button',name='Mapa',exact=True).click();page.locator('.discovered-roads').wait_for(state='attached')
  assert page.locator('.discovered-roads path').count()==roadCount
  clipped=page.locator('.discovered-place>span').evaluate_all('(nodes)=>nodes.filter(n=>n.scrollHeight>n.clientHeight+1).map(n=>n.textContent)')
  assert not clipped,clipped
  for town in ['valdren_plaza','khariel_centro','brumak_centro','narevia_centro','velmora_centro','vaisgard_mercado']:
   if page.locator('#map-destination option[value="'+town+'"]').count()==0:continue
   page.locator('#map-destination').select_option(town);page.wait_for_timeout(100);panel=page.locator('.discovered-panel');panel.scroll_into_view_if_needed();panel.screenshot(path=str(OUT/f'{width}-{town}.png'));assert page.locator('.discovered-road-selected').count()>0 or town=='valdren_plaza'
  page.get_by_role('button',name='Ver todo lo descubierto',exact=True).click();page.wait_for_timeout(150);page.locator('.discovered-panel').screenshot(path=str(OUT/f'{width}-world.png'))
  assert page.evaluate('()=>document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  results.append({'width':width,'knownRooms':roomCount,'drawnRoads':roadCount,'svgGapMasks':page.locator('.discovered-roads mask').count(),'clippedRoomLabels':clipped,'routeHighlighted':True,'noPageErrors':True,'noHorizontalPageOverflow':True});page.close()
 browser.close()
(OUT/'browser-report.json').write_text(json.dumps({'scope':'Read-only full-map Engine.snapshot fixture at8121, not a player session. All authored rooms deliberately known in isolated in-memory state; no DB.','results':results},indent=2));print(results)
