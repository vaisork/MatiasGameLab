#!/bin/bash
# Generador de arte de Vintage Telnet con sincronización automática al deploy

set -e

cd /home/jdiaz/MatiasGameLab
source venv/bin/activate

echo "🎨 Iniciando generador de arte..."
python3 generate_all_art.py

echo ""
echo "=========================================="
echo "✅ GENERACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "  1. Los WebP están listos en:"
echo "     • assets/vintage-telnet/creatures/"
echo "     • assets/vintage-telnet/locations/"
echo ""
echo "  2. Para llevarlos a producción, ejecuta:"
echo "     sudo vt-deploy main"
echo ""
echo "  3. El deploy automáticamente sincronizará"
echo "     los assets con el servidor."
echo ""
echo "=========================================="
echo ""
