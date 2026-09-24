#!/bin/sh
# Instalación única del comando global vt-deploy en la Raspberry Pi.
set -eu

if [ "$(id -u)" -ne 0 ]; then
    echo "Ejecuta este instalador con sudo." >&2
    exit 1
fi

REPO_ROOT="${VT_REPO_ROOT:-/home/jdiaz/MatiasGameLab}"
SOURCE="$REPO_ROOT/vintage-telnet/ops/vt_deploy.py"
LIB_DIR="/usr/local/lib/vintage-telnet"
COMMAND="/usr/local/sbin/vt-deploy"

if [ ! -f "$SOURCE" ]; then
    echo "No existe $SOURCE. Actualiza primero el checkout de MatiasGameLab." >&2
    exit 1
fi

install -d -o root -g root -m 0755 "$LIB_DIR"
install -o root -g root -m 0755 "$SOURCE" "$LIB_DIR/vt_deploy.py"

cat > "$COMMAND" <<'EOF'
#!/bin/sh
exec python3 /usr/local/lib/vintage-telnet/vt_deploy.py "$@"
EOF
chmod 0755 "$COMMAND"
chown root:root "$COMMAND"

python3 "$LIB_DIR/vt_deploy.py" --help >/dev/null

echo "Instalado: $COMMAND"
echo "Uso normal: sudo vt-deploy latest"
echo "También acepta: sudo vt-deploy <SHA-integrado-a-main>"
