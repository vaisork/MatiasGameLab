# Generación de borradores de arte con OpenAI

Esta herramienta permite a Dirección de Arte generar y versionar borradores de Vintage Telnet desde fichas JSON. Requiere una cuenta de API con acceso y crédito disponible. **La clave nunca va en la ficha, en la línea de comandos ni en GitHub.**

## Preparación única

Desde la carpeta raíz del repositorio, guarda la clave en `vintage-telnet/Imagenesapykey.env`:

```dotenv
OPENAI_API_KEY=pega_aqui_tu_clave
VT_ART_MODEL=gpt-image-2.5-flare
```

En Linux/macOS puedes crearla y protegerla así:

```bash
touch vintage-telnet/Imagenesapykey.env
chmod 600 vintage-telnet/Imagenesapykey.env
```

En Windows, crea y edita `vintage-telnet/Imagenesapykey.env` con un editor local. Ese archivo y la carpeta de generaciones están excluidos de Git. Por compatibilidad también se lee `vintage-telnet/.env`; una variable ya exportada tiene prioridad sobre ambos archivos.

Instala el cliente oficial de forma aislada, sin añadir dependencias al servidor:

```bash
python3 -m venv .venv-art
.venv-art/bin/python -m pip install -r tools/vt_art/requirements.txt
```

En PowerShell:

```powershell
py -m venv .venv-art
.venv-art\Scripts\python.exe -m pip install -r tools/vt_art/requirements.txt
```

## Ficha y comandos

Copia `vintage-telnet/art_requests/template.json` a una ficha propia, por ejemplo `vintage-telnet/art_requests/daro-retrato.json`. Completa el canon y las decisiones visuales; esta herramienta no inventa ni aprueba esos contenidos. Las rutas de referencia se interpretan respecto a la ficha y deben apuntar a imágenes locales PNG, JPEG o WebP.

Desde la raíz del repositorio:

```bash
.venv-art/bin/python -m tools.vt_art generate vintage-telnet/art_requests/daro-retrato.json
.venv-art/bin/python -m tools.vt_art variants vintage-telnet/art_requests/daro-retrato.json --count 3
.venv-art/bin/python -m tools.vt_art batch vintage-telnet/art_requests/lote-inicial
.venv-art/bin/python -m tools.vt_art status daro_retrato
.venv-art/bin/python -m tools.vt_art status daro_retrato --set review
.venv-art/bin/python -m tools.vt_art status daro_retrato --set approved --version v002
```

`generate` crea una versión. `variants` hace solicitudes independientes para poder conservar cada resultado si una posterior falla; permite entre 1 y 10. `batch` procesa fichas JSON y conserva generaciones completas aunque otra ficha falle. No hay reintento automático de solicitudes facturables. El modelo se configura en `.env` o con `--model`; `gpt-image-2.5-flare` es el valor inicial para borradores y generación general. Para edición precisa, Dirección de Arte puede probar `gpt-image-2.5-sunburst` con `--model`.

## Resultados, estados y costos

Cada asset se guarda sin sobrescribir versiones anteriores en `vintage-telnet/art_generations/<asset_id>/v001/`, con imagen y `metadata.json`. Los resúmenes `batch-<id>.json` registran requests intentados, imágenes generadas, uso que la API haya devuelto, fallos y sus request IDs. No se inventa un costo si la respuesta no entrega una métrica suficiente; en ese caso `cost_estimate` queda `null`.

Todo resultado inicia en `draft`. Dirección de Arte revisa visualmente y es quien decide `review` o `approved`; el comando registra la decisión explícita y nunca autoaprueba. `published` sólo registra un estado, no publica ni copia archivos. El Publicador mantiene su flujo de normalización y el Integrador decide las rutas de runtime por separado.

`output_destination` se limita a `vintage-telnet/art_generations/`; la herramienta rechaza rutas dentro de `assets/vintage-telnet/`. Nada llega al juego, se commitea, publica o despliega automáticamente.

La Image API puede tardar hasta un par de minutos con instrucciones complejas, y la consistencia entre variantes requiere revisión humana. Una organización puede necesitar completar verificación antes de acceder a los modelos de imagen. El piloto real de #559 queda pendiente de las fichas seleccionadas por Dirección de Arte y una clave local válida.
