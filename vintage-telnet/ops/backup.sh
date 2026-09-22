#!/bin/sh
# Respaldo periodico de vintage.sqlite3, pensado para correr como
# vintage-telnet-backup.service (via el timer .timer).
#
# Usa server.admin backup, que ya verifica integridad de la copia
# (PRAGMA integrity_check) y nunca sobrescribe un backup existente.
# Falla con exit code != 0 si algo sale mal, para que systemd/journal
# lo registren como fallo real, no un exito silencioso.
set -eu

ENV_FILE="${VT_BACKUP_ENV_FILE:-/etc/vintage-telnet/server.env}"
RELEASE_DIR="${VT_BACKUP_RELEASE_DIR:-/opt/vintage-telnet/current/vintage-telnet}"
BACKUP_DIR="${VT_BACKUP_DIR:-/var/backups/vintage-telnet}"
KEEP_DAYS="${VT_BACKUP_KEEP_DAYS:-14}"

# shellcheck source=/dev/null
. "$ENV_FILE"

if [ -z "${VT_DATA_DIR:-}" ]; then
    echo "VT_DATA_DIR no esta definida (revisar $ENV_FILE)" >&2
    exit 1
fi

mkdir -p "$BACKUP_DIR"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
destination="$BACKUP_DIR/vintage-$timestamp.sqlite3"

"$RELEASE_DIR/.venv/bin/python" -m server.admin --data-dir "$VT_DATA_DIR" backup "$destination"

# Poda de backups viejos; no falla el respaldo de hoy si la poda no encuentra nada.
find "$BACKUP_DIR" -maxdepth 1 -name 'vintage-*.sqlite3' -mtime "+$KEEP_DAYS" -delete || true

echo "Backup verificado: $destination"
