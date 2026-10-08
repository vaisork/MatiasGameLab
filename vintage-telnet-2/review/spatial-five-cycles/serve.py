"""Read-only QA fixture: Engine snapshot with all authored rooms known; no DB."""
import json,sys
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from server.content import Content
from server.engine import Engine
from server.mechanics import new_state
content=Content(ROOT/'content');now=43200;s=new_state('humano','juramentado','home:qa-spatial',now);s.update(location='valdren_plaza',known=[s['home'],*content.rooms],visited=[s['home'],*content.rooms],routes=[list(pair) for pair in {tuple(sorted((k,to))) for k,r in content.rooms.items() for to in r.get('exits',{}).values() if to in content.rooms}]);s['routes'].append([s['home'],'valdren_plaza']);char={'id':999,'name':'Fixture mapa completo','species':'humano','class_id':'juramentado','status':'approved','state':s}
snapshot=Engine(content,lambda:now).snapshot(char,{'flags':[],'deaths':{},'weather':{},'version':1});snapshot.update(authenticated=True,csrf_token='fixture-no-post',characters=[],presence=[],chat=[])
Path(__file__).with_name('snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2))
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def do_GET(self):
  if self.path.split('?')[0]=='/api/state':
   body=json.dumps(snapshot).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(body)
  else:
   if self.path=='/':self.path='/client/index.html'
   super().do_GET()
 def do_POST(self):self.send_error(405,'Read-only fixture')
 def log_message(self,*args):pass
print('Read-only spatial fixture on 127.0.0.1:8121, no database',flush=True);ThreadingHTTPServer(('127.0.0.1',8121),Handler).serve_forever()
