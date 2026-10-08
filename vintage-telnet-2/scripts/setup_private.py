"""Initialize private settings on a fresh checkout without legacy game files."""
import getpass
import os
from pathlib import Path
import secrets
from werkzeug.security import generate_password_hash

root=Path(__file__).resolve().parents[1]
runtime=root/'runtime';runtime.mkdir(mode=0o700,exist_ok=True)
settings=runtime/'server.env'
if settings.exists():
 print('La configuración privada ya existe; se conserva.')
else:
 password=getpass.getpass('Contraseña del director (mínimo 12 caracteres): ')
 if len(password)<12:raise SystemExit('Usa al menos 12 caracteres; no se creó configuración.')
 if password!=getpass.getpass('Repite la contraseña: '):raise SystemExit('Las contraseñas no coinciden; no se creó configuración.')
 fd=os.open(settings,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 with os.fdopen(fd,'w') as f:
  f.write('VT_NEW_SECRET_KEY='+secrets.token_urlsafe(48)+'\n')
  f.write('VT_NEW_DM_PASSWORD_HASH='+generate_password_hash(password)+'\n')
 print('Configuración creada en runtime/server.env; no la publiques.')
