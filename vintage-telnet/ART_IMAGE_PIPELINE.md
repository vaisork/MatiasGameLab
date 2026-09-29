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

`output_destination` se limita a `vintage-telnet/art_generations/`; la herramienta rechaza rutas dentro de `assets/vintage-telnet/`. Nada llega al juego, se commitea, publica o despliega automáticamente.

La Image API puede tardar hasta un par de minutos con instrucciones complejas, y la consistencia entre variantes requiere revisión humana. Una organización puede necesitar completar verificación antes de acceder a los modelos de imagen.

## Piloto manual desde GitHub Actions

El workflow `.github/workflows/vt-art-pilot.yml` permite ejecutar el piloto aprobado de Velozanco desde GitHub, en un runner hospedado por GitHub. Sólo se activa manualmente desde `main`, hace una generación individual y copia la imagen, `metadata.json` y la ficha a `Mi unidad/Matias Game Lab - Arte/02_APROBADO/Vintage-Telnet`. Aunque se guarde en esa carpeta, el estado registrado sigue siendo `draft`; no aprueba, publica, integra al juego ni despliega. No sube imágenes a Actions artifacts ni al repositorio.

Configuración única del repositorio, en **Settings → Secrets and variables → Actions**:

- Secret `OPENAI_API_KEY`: clave de OpenAI API. No pegarla en chats, fichas, commits ni logs.
- Secret `VT_ART_DRIVE_OAUTH_JSON`: credencial OAuth de usuario de Drive en JSON, con refresh token, autorizada para el mismo Google Drive. Se necesita porque los archivos deben quedar en una carpeta de **Mi unidad**: las cuentas de servicio no tienen cuota de almacenamiento y no pueden ser dueñas de esos archivos.

Para preparar OAuth de Drive: en Google Cloud crea un proyecto, habilita Drive API, configura el consentimiento OAuth y crea un cliente OAuth tipo **Desktop app**. Descarga su JSON, instala `tools/vt_art/requirements-drive-auth.txt` en un virtualenv y ejecuta:

```bash
python -m tools.vt_art.authorize_drive ~/Downloads/client_secret_xxx.json
```

El navegador abrirá Google para autorizar la cuenta que ya tiene acceso a la carpeta y a la referencia Fase 1. El comando guarda el JSON con refresh token en `vintage-telnet/drive-oauth-user.json` y limita sus permisos locales; el archivo está excluido de Git. Copia su contenido localmente al secreto `VT_ART_DRIVE_OAUTH_JSON` en GitHub. No lo pegues en este chat. Si la app OAuth queda en estado **Testing**, Google caduca el refresh token tras siete días; para uso periódico hay que completar la publicación/verificación de OAuth que Google requiera o usar una carpeta de Shared Drive con un service account.

La clave de OpenAI se usa como credencial del job; no se instala ni se guarda dentro del repositorio. La credencial OAuth de Drive autoriza al usuario dueño de la carpeta y el workflow nunca imprime el contenido de los secretos. Para repetir el piloto: abre **Actions → Vintage Telnet — piloto de arte → Run workflow** y elige `main`. Cada ejecución factura una generación; no vuelvas a pulsar para reintentar sin revisar primero el resultado y el uso de la ejecución anterior.

Este workflow está limitado al piloto de una imagen. Las futuras fichas no se ejecutan por lote; Dirección de Arte debe seleccionar y autorizar cada alcance antes de extenderlo.
