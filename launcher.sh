#!/bin/bash
# Launcher robusto que garantiza que OPENAI_API_KEY se carga

# Leer OPENAI_API_KEY directamente de .bashrc
if [ -f ~/.bashrc ]; then
    export OPENAI_API_KEY=$(grep "^export OPENAI_API_KEY=" ~/.bashrc | cut -d'"' -f2)
fi

# Verificar que está configurada
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY no encontrada en ~/.bashrc"
    read -p "Presiona Enter para cerrar..."
    exit 1
fi

# Ejecutar desde el directorio del proyecto
cd /home/jdiaz/MatiasGameLab

# Activar venv
source venv/bin/activate

# Ejecutar generador
python3 generate_all_art.py

# Esperar antes de cerrar
read -p "Presiona Enter para cerrar..."
