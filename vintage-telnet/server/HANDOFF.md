# Handoff — Programador Jules — Vintage Telnet

**Desarrollador:** Jules — Programador.
**Estado:** LISTO PARA REVISIÓN.
**Tarea asignada:** PR #209 — Implementar la pantalla pública inicial de Vintage Telnet y PR #211 (Conocer el mundo).
**Rama:** `jules-pr209`.
**HEAD base de esta entrega:** `76f83d7` (`origin/main`).

## Objetivo

Implementar la pantalla pública inicial de Vintage Telnet, antes de registro/login, ofreciendo 3 accesos: "Conocer el Mundo", "Guía del aventurero" y "Entrar / Crear cuenta". Las dos lecturas son opcionales y están parseadas directamente de sus archivos Markdown correspondientes, sin exponer contenido de uso interno.

## Cambios

### `server/content_parser.py` (Nuevo)
Se agregó una utilidad en Python que lee `KNOW_THE_WORLD_MENU.md` y `ENTRY_ADVENTURER_GUIDE.md` desde la raíz. El parser recorta todo el *frontmatter* y la metadata directiva del documento original (como los bloques de `NOTA DE DISEÑO / IMAGEN`) para servir al jugador únicamente el texto narrativo aprobado. Estructura el texto y lo convierte a HTML a través de `markdown`.

### `server/app.py`
Se integró `content_parser.py` para cargar el contenido de los dos markdowns de la guía y el mundo en el arranque del servidor, inyectándolos dentro de `app.jinja_env.globals["world_content"]` y `guide_content` para poder renderizarlos de manera sencilla desde las vistas públicas.

### `server/templates/entry.html` y `server/templates/_onboarding_guest.html`
- Se modificó la "Portada Pública" para mostrar 3 grandes botones de acción según el requerimiento.
- Se mantuvieron las vistas de Login y Register dentro del flujo `Entrar / Crear cuenta`.
- Se crearon dos modales/vistas (`data-onboarding-view="world"` y `guide`) que muestran el contenido renderizado, un índice navegable ("Leer todo"), sin forzar paredes de texto gigantes en un modal estrecho de móvil.
- Se agregó CSS en `entry.html` para la legibilidad de este Markdown generado dinámicamente (`.markdown-body`).

### `tests/test_entry.py`
Se añadió la prueba `test_onboarding_new_routes_and_content_are_present` que asegura que la vista principal tiene los textos requeridos y confirma que no se filtran "NOTAS DE DISEÑO" dentro del HTML renderizado final.

## Pruebas

```
cd vintage-telnet && .venv/bin/python3 -m unittest discover -s tests -v
```

**306/306 OK**.

## Trabajo previo afectado

Las PR #209 y #211 definen el contenido del front. Para completar esto se hizo merge local de la rama PR #211 sobre esta rama.

## Pendientes / NECESIDADES
No hay pendientes de implementación sobre este issue en particular. El parser maneja texto Markdown general con HTML de manera robusta. Las imágenes placeholder están presentes y pueden ser sustituidas mediante CSS o inyección cuando los assets definitivos estén confirmados.

