"""Create private runtime settings; never publish the director credential."""
import os
from pathlib import Path
import secrets
import shutil

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'runtime'
def prepare():
 RUNTIME.mkdir(mode=0o700,exist_ok=True)
 settings=RUNTIME/'server.env'
 if not settings.exists():
  reference=Path('/home/jdiaz/proyectos/vintage-telnet-2/vt2/runtime/server.env')
  password_hash=None
  if reference.is_file():
   for line in reference.read_text().splitlines():
    key,sep,value=line.partition('=')
    if sep and key.strip().endswith('PASSWORD_HASH'):
     password_hash=value.strip().strip("'\"");break
  if not password_hash:raise RuntimeError('Falta la configuración privada del director; no se creó una contraseña pública.')
  fd=os.open(settings,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  with os.fdopen(fd,'w') as f:
   f.write('VT_NEW_SECRET_KEY='+secrets.token_urlsafe(48)+'\nVT_NEW_DM_PASSWORD_HASH='+password_hash+'\n')
  os.chmod(settings,0o600)
 cache=RUNTIME/'python-deps'
 reference=Path('/home/jdiaz/proyectos/vintage-telnet-2/runtime/python-deps')
 if not cache.exists() and reference.is_dir():
  # Third-party installed distributions only, never the old game source.
  shutil.copytree(reference,cache,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for line in settings.read_text().splitlines():
  key,sep,value=line.partition('=')
  if sep and key.startswith('VT_NEW_'):os.environ.setdefault(key,value)
 return cache
if __name__=='__main__':
 prepare();print('Configuración privada y dependencias preparadas.')
