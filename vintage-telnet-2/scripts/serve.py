"""Launch the new game in the user's ordinary Ubuntu terminal."""
from pathlib import Path
import argparse
import sys
import threading
import webbrowser
from bootstrap import prepare
ROOT=Path(__file__).resolve().parents[1]
cache=prepare();sys.path[:0]=[str(ROOT),str(cache)]
from server.app import create_app
from waitress import serve
parser=argparse.ArgumentParser();parser.add_argument('--host',default='127.0.0.1');parser.add_argument('--port',type=int,default=8083)
parser.add_argument('--open',action='store_true',help='Abrir el juego en el navegador de Ubuntu')
args=parser.parse_args()
if args.open:
 threading.Timer(1.5,lambda:webbrowser.open(f'http://localhost:{args.port}')).start()
print(f'Vintage Telnet 2 — nuevo: http://{args.host}:{args.port}',flush=True)
print('Director: /dm · Mantén esta terminal abierta.',flush=True)
serve(create_app(),host=args.host,port=args.port,threads=4)
