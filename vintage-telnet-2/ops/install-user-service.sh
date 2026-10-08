#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -x "$project_dir/.venv/bin/python" || ! -f "$project_dir/runtime/server.env" ]]; then
  echo 'Primero crea .venv, instala requirements.txt y ejecuta scripts/setup_private.py.' >&2
  exit 1
fi
mkdir -p "$HOME/.config/systemd/user"
unit_path="$HOME/.config/systemd/user/vintage-telnet-nuevo.service"
cat > "$unit_path" <<EOF
[Unit]
Description=Vintage Telnet nuevo
After=network-online.target

[Service]
Type=simple
WorkingDirectory=$project_dir
ExecStart="$project_dir/.venv/bin/python" "$project_dir/scripts/serve.py" --host 127.0.0.1 --port 8083
Environment=VT_NEW_TRUST_PROXY_PROTO=1
Restart=on-failure
RestartSec=3
UMask=0077

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now vintage-telnet-nuevo.service
systemctl --user is-active vintage-telnet-nuevo.service
