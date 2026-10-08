#!/usr/bin/env bash
set -euo pipefail
if cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && python3 scripts/serve.py --open "$@"; then
    exit 0
else
    launch_status=$?
    printf '\nEl juego terminó con un error (código %s). El detalle está arriba.\n' "$launch_status"
    if [[ -t 0 ]]; then
        read -r -p 'Pulsa Enter para cerrar esta ventana.' || true
    fi
    exit "$launch_status"
fi
