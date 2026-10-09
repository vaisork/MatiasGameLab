#!/bin/bash
# Activación de ef0f7fc (PR #667, #668) en Raspberry. Preparado por Claude; revisar antes de ejecutar.
# Uso (desde Ubuntu):
#   scp /home/jdiaz/proyectos/vt2-deploy-ef0f7fc/activar.sh jdiaz@100.112.10.16:/home/jdiaz/proyectos/vt2-activar-ef0f7fc.sh
#   ssh jdiaz@100.112.10.16 'bash /home/jdiaz/proyectos/vt2-activar-ef0f7fc.sh'
# Requiere el staging ya verificado: /home/jdiaz/proyectos/vt2-staging-ef0f7fc-20261008 (1383 archivos SHA256 OK, 161 tests OK).
# No restaura ni reemplaza SQLite: sólo hace una copia consistente para el respaldo.
set -Eeuo pipefail
APP=/home/jdiaz/proyectos/vintage-telnet-nuevo
ST=/home/jdiaz/proyectos/vt2-staging-ef0f7fc-20261008
TS=$(date -u +%Y%m%dT%H%M%SZ)
BK=/home/jdiaz/backups/vt2-before-ef0f7fc-$TS
SHA=ef0f7fcf49ac3b45a4ac766bf1d9f5a7741f6625
PY=$APP/.venv/bin/python

cd "$ST" && sha256sum --quiet -c MANIFEST.sha256 && echo "0. staging verificado contra su manifiesto"

digest() { "$PY" - "$1" <<'PYEOF'
import sqlite3,sys,hashlib,json
c=sqlite3.connect(sys.argv[1]);out={}
for (t,) in c.execute("select name from sqlite_master where type='table' order by name"):
    h=hashlib.sha256()
    for row in c.execute(f'select * from "{t}" order by 1'):h.update(repr(row).encode())
    out[t]=h.hexdigest()[:16]
print(json.dumps(out,sort_keys=True))
PYEOF
}

mkdir -p "$BK/code" "$BK/private"; chmod 700 "$BK"
rsync -a --exclude runtime --exclude .venv "$APP/" "$BK/code/"
cp -p "$APP/runtime/server.env" "$APP/runtime/deployed-version.txt" "$BK/private/"
echo "1. código y configuración respaldados en $BK"

rollback() {
    trap - ERR
    set +e
    echo "!! fallo: restaurando código anterior desde $BK/code"
    systemctl --user stop vintage-telnet-nuevo.service
    rsync -a --exclude runtime --exclude .venv "$BK/code/" "$APP/"
    cp -p "$BK/private/deployed-version.txt" "$APP/runtime/deployed-version.txt"
    systemctl --user start vintage-telnet-nuevo.service
    systemctl --user is-active vintage-telnet-nuevo.service
    echo "RESPALDO=$BK"
    exit 1
}
trap rollback ERR
systemctl --user stop vintage-telnet-nuevo.service
echo "2. servicio detenido"

"$PY" - "$APP/runtime/world.sqlite3" "$BK/private/world.sqlite3" <<'PYEOF'
import sqlite3,sys
src=sqlite3.connect(sys.argv[1]);dst=sqlite3.connect(sys.argv[2]);src.backup(dst)
assert dst.execute('pragma integrity_check').fetchone()[0]=='ok';print('3. copia SQLite consistente, integrity_check ok')
PYEOF
chmod 600 "$BK/private/"*
BEFORE=$(digest "$APP/runtime/world.sqlite3"); echo "$BEFORE" > "$BK/private/tablas-antes.json"



rsync -a --exclude runtime --exclude .venv "$ST/" "$APP/" || rollback
echo "4. código ef0f7fc copiado (runtime y .venv intactos)"
COPIED=$(digest "$APP/runtime/world.sqlite3")
[ "$BEFORE" = "$COPIED" ] || rollback
cd "$APP" && sha256sum --quiet -c MANIFEST.sha256


systemctl --user start vintage-telnet-nuevo.service
sleep 6
systemctl --user is-active vintage-telnet-nuevo.service >/dev/null || rollback
CODE=$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8083/); [ "$CODE" = 200 ] || rollback
echo "5. servicio activo, localhost $CODE"

AFTER=$(digest "$APP/runtime/world.sqlite3")
if [ "$BEFORE" = "$AFTER" ]; then echo "6. tablas idénticas al respaldo: $AFTER"; else echo "6. AVISO tablas cambiadas: antes $BEFORE después $AFTER"; fi
"$PY" - "$APP/runtime/world.sqlite3" <<'PYEOF'
import sqlite3,sys;c=sqlite3.connect(sys.argv[1])
print('   cuentas:',c.execute('select count(*) from accounts').fetchone()[0],'· personajes:',c.execute('select count(*) from characters').fetchone()[0])
PYEOF

echo "$SHA" > "$APP/runtime/deployed-version.txt"
echo "7. versión registrada: $(cat "$APP/runtime/deployed-version.txt")"
cd "$APP" && sha256sum --quiet -c MANIFEST.sha256 && echo "8. manifiesto verificado en la instalación activa"
trap - ERR
echo "RESPALDO=$BK"
