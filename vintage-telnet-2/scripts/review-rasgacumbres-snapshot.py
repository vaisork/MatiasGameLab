"""Discover Rasgacumbres through real API in a throwaway account/store."""
import sys,json,tempfile,uuid
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path[:0]=[str(root),str(root/'runtime/python-deps')]
from server.app import create_app
from werkzeug.security import generate_password_hash
class Clock:
 def __call__(self):return 43200
class RNG:
 def random(self):return .4
with tempfile.TemporaryDirectory(prefix='vt-rasgacumbres-art-') as directory:
 app=create_app({'TESTING':True,'DATA_DIR':directory,'CLOCK':Clock(),'RNG':RNG(),'DM_PASSWORD_HASH':generate_password_hash('isolated-art-only')});client=app.test_client();dm=app.test_client()
 def state(c=client):return c.get('/api/state').json
 def post(c,path,payload):return c.post(path,json={**payload,'csrf_token':state(c)['csrf_token']})
 def act(action,target=None):
  response=post(client,'/api/action',{'id':action,'target':target,'request_id':str(uuid.uuid4())});assert response.status_code==200,response.json;return response.json
 post(client,'/api/account/register',{'username':'isolatedart','password':'isolated-art-password'});created=post(client,'/api/character/create',{'name':'Arte temporal','species':'felaryn','class_id':'sombra'}).json
 post(dm,'/api/master/login',{'password':'isolated-art-only'});post(dm,'/api/master/approve',{'character_id':created['character']['id']})
 act('mover','salir');act('mover','sur');snapshot=state();entry=next(e for e in snapshot['bestiary'] if e['id']=='rasgacumbres')
 assert entry['illustration']=='/client/art/bestiary/rasgacumbres-anime-v2.webp';assert snapshot['character']['combat'] is None
 snapshot['bestiary']=[entry] # Read-only UI focus: entry is genuinely API-discovered, not fabricated.
 (root/'review/rasgacumbres-v2/api-state.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2))
 print('PASS real API discovery; temporary store; new illustration reference; no combat')
