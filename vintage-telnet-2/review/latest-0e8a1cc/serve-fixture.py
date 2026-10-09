import sys,tempfile,json
sys.path.insert(0,'/tmp/vt2-review-latest/vintage-telnet-2')
from server.app import create_app
from server import mechanics as m
from werkzeug.security import generate_password_hash
import sqlite3
folder=tempfile.mkdtemp(prefix='vt2-combat-qa-');clock=[43200]
app=create_app({'TESTING':True,'DATA_DIR':folder,'CLOCK':lambda:clock[0],'RNG':type('Quiet',(),{'random':lambda self:.01})(),'DM_PASSWORD_HASH':generate_password_hash('temporary-director')})
client=app.test_client()
def post(c,path,data):
 data['csrf_token']=c.get('/api/state').json['csrf_token'];r=c.post(path,json=data);assert 200<=r.status_code<300,(path,r.json);return r.json
post(client,'/api/account/register',{'username':'combatqa','password':'temporary-player'})
r=post(client,'/api/character/create',{'name':'Prueba visual','species':'humano','class_id':'juramentado','gender':'masculino'})
dm=app.test_client();post(dm,'/api/master/login',{'password':'temporary-director'});post(dm,'/api/master/approve',{'character_id':r['character']['id']})
from pathlib import Path
files=list(Path(folder).glob('*.sqlite3'));assert len(files)==1,files
with sqlite3.connect(files[0]) as db:
 s=json.loads(db.execute('select state from characters').fetchone()[0]);s['location']='edran_surcos';s['level']=8;s['attributes'].update(fuerza=20,destreza=20,agilidad=20);s['hp']=m.hp_max(s);s['visits']['edran_surcos']=1
 from server.content import Content
 rooms=Content(Path('/tmp/vt2-review-latest/vintage-telnet-2/content')).rooms
 s['known']=list(rooms)+[s['home']];s['visited']=list(s['known']);s['routes']=[list(pair) for pair in sorted({tuple(sorted((rid,to))) for rid,room in rooms.items() for to in room.get('exits',{}).values()})]
 db.execute('update characters set state=?',(json.dumps(s),))
post(client,'/api/action',{'id':'combatir','target':'espinajo_rastrojo','request_id':'encounter-qa'})
assert client.get('/api/state').json['character']['combat']
with sqlite3.connect(files[0]) as db:
 s=json.loads(db.execute('select state from characters').fetchone()[0]);s['bestiary']={'pinzajunco':{'id':'pinzajunco','name':'Pinzajunco'},'espinajo_rastrojo':{'id':'espinajo_rastrojo','name':'Espinajo de rastrojo'}}
 db.execute('update characters set state=?',(json.dumps(s),))
app.run(host='127.0.0.1',port=8139,use_reloader=False)
