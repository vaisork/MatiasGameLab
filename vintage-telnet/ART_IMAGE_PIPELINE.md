# Generación de borradores de arte con OpenAI

Esta herramienta permite a Dirección de Arte generar y versionar borradores de Vintage Telnet desde fichas JSON. Requiere una cuenta de API con acceso y crédito disponible. **La clave nunca va en la ficha, en la línea de comandos ni en el repositorio.** En GitHub Actions se entrega exclusivamente como secret cifrado al job autorizado.

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

`output_destination` se limita a `vintage-telnet/art_generations/`; la herramienta rechaza rutas dentro de `assets/vintage-telnet/`. La CLI local no hace commits. El workflow de GitHub Actions descrito abajo sí crea una rama y una PR de borrador para revisar el resultado; nada llega al runtime ni se despliega automáticamente.

La Image API puede tardar hasta un par de minutos con instrucciones complejas, y la consistencia entre variantes requiere revisión humana. Una organización puede necesitar completar verificación antes de acceder a los modelos de imagen.

## Piloto manual desde GitHub Actions

El workflow `.github/workflows/vt-art-pilot.yml` se ejecuta manualmente desde `main` en un runner hospedado por GitHub. El formulario recibe una ficha aprobada de `vintage-telnet/art_requests/` y genera una sola imagen. Para el piloto Velozanco, sube también la referencia aprobada como `vintage-telnet/art_requests/references/velozanco-edran-fase1-anatomia.png`; las referencias se versionan junto a su solicitud para que el runner no dependa de Drive. El workflow abre una PR con imagen, `metadata.json` y ficha bajo `vintage-telnet/art_generations/<asset_id>/`. El estado sigue siendo `draft`; la PR no aprueba ni integra el asset al juego y no despliega. No sube imágenes a Actions artifacts.

Configuración única del repositorio, en **Settings → Secrets and variables → Actions**:

- Secret `OPENAI_API_KEY`: clave de OpenAI API. No pegarla en chats, fichas, commits ni logs.
La clave de OpenAI se usa sólo como credencial del job; no se guarda en el repositorio ni se imprime. Los borradores sí quedan públicamente visibles en la PR porque el repositorio es público. Puedes descargarlos desde GitHub y cerrar la PR/eliminar su rama para limpiar borradores; si integras la PR, los archivos quedarán en `main` hasta que los borres manualmente.

Para ejecutar: abre **Actions → Vintage Telnet — piloto de arte → Run workflow**, elige `main` y selecciona la ficha aprobada. Cada ejecución factura una generación y crea una PR nueva. Revisa el resultado antes de lanzar otra generación; no hay reintentos automáticos.

Este workflow está limitado al piloto de una imagen. Las futuras fichas no se ejecutan por lote; Dirección de Arte debe seleccionar y autorizar cada alcance antes de extenderlo.
