"""Disposable review server. Real clock by default; --fixed-clock enables controlled passive tests.
Never uses runtime/world.sqlite3 or production credentials. Localhost only; configurable review port (default 8099).
"""
import argparse,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path[:0]=[str(root),str(root/'runtime/python-deps')]
from server.app import create_app
from werkzeug.security import generate_password_hash
from waitress import serve
from flask import request
class Clock:
 now=43200
 def __call__(self):return self.now
class RNG:
 def random(self):return 0
parser=argparse.ArgumentParser();parser.add_argument('--fixed-clock',action='store_true');parser.add_argument('--port',type=int,default=8099,choices=range(8090,8120));args=parser.parse_args();clock=Clock()
with tempfile.TemporaryDirectory(prefix='vt-isolated-review-') as directory:
 config={'TESTING':True,'DATA_DIR':directory,'RNG':RNG(),'DM_PASSWORD_HASH':generate_password_hash('isolated-review-only')}
 if args.fixed_clock:config['CLOCK']=clock
 app=create_app(config)
 if args.fixed_clock:
  @app.post('/__isolated/advance')
  def advance():
   seconds=(request.get_json(silent=True) or {}).get('seconds',24)
   if type(seconds) is not int or not 1<=seconds<=300:return {'error':'isolated clock step must be 1–300'},400
   clock.now+=seconds
   return {'advanced_seconds':seconds}
 print(f'Isolated temporary review: http://127.0.0.1:{args.port}',flush=True)
 serve(app,host='127.0.0.1',port=args.port,threads=4)
