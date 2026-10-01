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

## Clasificación visual obligatoria

Toda ficha nueva debe declarar la categoría visual de forma inequívoca tanto en sus campos como al inicio de `prompt` y `art_direction`. El nombre propio nunca basta para inferir qué se dibuja.

Usar estas cabeceras:

- Criatura: `SUBJECT TYPE: CREATURE / LIVING ANIMAL`
- Paisaje o lugar: `SUBJECT TYPE: LOCATION / ENVIRONMENT / LANDSCAPE — NO CREATURE`
- Arquitectura: `SUBJECT TYPE: ARCHITECTURE / BUILT ENVIRONMENT — NO CREATURE`

Para `LOCATION` y `ARCHITECTURE`, las restricciones negativas deben prohibir explícitamente que una criatura, animal, monstruo, personaje o ser vivo se convierta en el sujeto focal. Para `CREATURE`, la ficha debe decir explícitamente que el sujeto focal es un ser vivo y que el entorno es secundario.

La autocrítica debe tratar un **error de categoría** como fallo obligatorio: si una ficha LOCATION produce una criatura, si una ficha ARCHITECTURE produce una criatura como sujeto, o si una ficha CREATURE no representa al ser vivo solicitado, `passes` debe ser falso aunque composición, color o acabado sean buenos. No aprobar visualmente una generación de categoría equivocada.

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

Todo resultado inicia en `draft`. Dirección de Arte registra su decisión en la PR de GitHub: **Approve** cambia `metadata.json` a `approved`; **Request changes** lo cambia a `rejected`. La automatización registra esa decisión en la rama de la PR. Si la revisión se retira, el estado vuelve a `draft`. Un comentario normal no cambia el estado. El comando local también permite registrar `rejected`. `published` sólo registra un estado, no publica ni copia archivos. El Publicador mantiene su flujo de normalización y el Integrador decide las rutas de runtime por separado.

`output_destination` se limita a `vintage-telnet/art_generations/`; la herramienta rechaza rutas dentro de `assets/vintage-telnet/`. La CLI local no hace commits. El workflow de GitHub Actions descrito abajo sí crea una rama y una PR de borrador para revisar el resultado; nada llega al runtime ni se despliega automáticamente.

La Image API puede tardar hasta un par de minutos con instrucciones complejas, y la consistencia entre variantes requiere revisión humana. Una organización puede necesitar completar verificación antes de acceder a los modelos de imagen.

## Operación desde Raspberry

El operador inicia cada solicitud desde la Raspberry; el chat no necesita acceso a GitHub Actions. En el checkout del repositorio, instala GitHub CLI y autentícalo con una cuenta/token que tenga permiso `Actions: write` sobre `vaisork/MatiasGameLab`. Actualiza el checkout para que el lanzador conozca la versión actual. La clave de OpenAI permanece sólo en el secret `OPENAI_API_KEY` de GitHub.

```bash
git pull --ff-only origin main
python3 -m tools.vt_art.dispatch vintage-telnet/art_requests/velozanco-edran-fase2.json
```

El lanzador verifica la sesión de GitHub y que la ficha exista en `main`, pide confirmación escribiendo `GENERAR` y dispara exactamente una ejecución de `vt-art-pilot.yml`. No lee ni imprime credenciales. Para ejecución no interactiva admite `--yes`. No uses `vt-deploy`: este comando genera arte y no instala ni reinicia el servidor.

Actions guardará el resultado en una rama y propondrá una PR de borrador. El repositorio debe permitir que Actions cree PRs en **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**. El workflow sólo crea PRs; no aprueba ninguna. Dirección de Arte revisa la PR y usa **Review changes → Approve** o **Request changes** para registrar su decisión. Un workflow de seguimiento sincroniza `approved`/`rejected` en el `metadata.json` de esa versión. Nada se integra a runtime ni se despliega.

## Piloto desde GitHub Actions

El workflow `.github/workflows/vt-art-pilot.yml` también puede iniciarse manualmente desde Actions. El formulario recibe una ficha de `vintage-telnet/art_requests/` y genera una sola imagen. Para el piloto Velozanco, la referencia aprobada está versionada junto a la solicitud. El workflow abre una PR con imagen, `metadata.json` y ficha bajo `vintage-telnet/art_generations/<asset_id>/`. No sube imágenes a Actions artifacts.

Configuración única del repositorio, en **Settings → Secrets and variables → Actions**:

- Secret `OPENAI_API_KEY`: clave de OpenAI API. No pegarla en chats, fichas, commits ni logs.
La clave de OpenAI se usa sólo como credencial del job; no se guarda en el repositorio ni se imprime. Los borradores sí quedan públicamente visibles en la PR porque el repositorio es público. Puedes descargarlos desde GitHub y cerrar la PR/eliminar su rama para limpiar borradores; si integras la PR, los archivos quedarán en `main` hasta que los borres manualmente.

Cada ejecución factura una generación y crea una PR nueva. Revisa el resultado antes de lanzar otra generación; no hay reintentos automáticos.

Este workflow está limitado al piloto de una imagen. Las futuras fichas no se ejecutan por lote; Dirección de Arte debe seleccionar y autorizar cada alcance antes de extenderlo.
