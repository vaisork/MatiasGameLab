#!/bin/bash
# Script wrapper que carga config y ejecuta el generador

# Cargar .bashrc usando login shell
exec bash --login -c 'cd /home/jdiaz/MatiasGameLab && source venv/bin/activate && python3 generate_all_art.py; bash -i'
