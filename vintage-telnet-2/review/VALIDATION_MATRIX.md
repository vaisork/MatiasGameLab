# Validaciones exigidas y evidencia de la construcción nueva

Fuente: Vintage_Telnet_Prompt_Actualizado.pdf, secciones 6–7 y 35–38. Las instrucciones posteriores de Javier prevalecen: canon del prompt sí; historia y narración anteriores no; ninguna imagen. El mundo tiene texto original y código nuevo. Ninguna cantidad de archivos o pruebas sustituye la calidad lectora.

| Validación | Evidencia real | Estado |
|---|---|---|
| Canon, origen de texto y ausencia de imágenes | CANON_EXPANSION.md, catálogos JSON, rutas cliente cerradas y CSP `img-src 'none'` | Inspección realizada; ampliaciones Edran y encuentros cotidianos documentadas |
| Escala y continuidad de rutas | 162 lugares conectados; cinco hogares privados; Content valida enlaces, referencias y tiendas | Prueba estructural aprobada; no aprobación literaria por conteo |
| Recorrido hogar, pueblo, camino, transición, naturaleza y otro pueblo | 65 desplazamientos autenticados de lectura por cinco regiones, sin editar posición ni conocimiento | API real ejecutada; no sesión humana |
| Comercio, encuentro, combate y regreso | tests/test_real_content.py: pago6, compra8, relogin; retirada de fauna; Artífice/Espinajo, material y venta | Pruebas del catálogo real aprobadas |
| Decisiones, memoria y mundo compartido | Guardas de flags/horario/clima/presencia; estados físicos y crédito personal; SQLite e idempotencia | Pruebas reales y aisladas; correcciones y regresos revisados |
| Doce criterios narrativos, >=4/5 cada uno | review/NARRATIVE_INDEPENDENT.md, recorridos repetidos y final distinto de Edran | Once criterios lectores4/5 en la muestra; color semántico pendiente de navegador |
| Segundo recorrido distinto sin usar para ajuste | review/API_READER_EDRAN.json:66 acciones,19 puntos, cuatro fases | Ejecutado como recorrido API/lector técnico; no sesión humana |
| Legibilidad, composición, interacción, color y accesibilidad en escritorio/móvil | client/qa-contracts.mjs y sintaxis; scripts/browser-review-new.mjs preparado | Contratos técnicos aprobados; revisión visual real pendiente |
| Sin errores de navegador ni desbordamientos320/390/1440 | BROWSER_STARTUP.log: Chrome termina133 por setsockopt EPERM | Bloqueado por entorno; no capturas ni aprobación visual |
| Servidor Ubuntu real | scripts/bootstrap.py/serve.py y acceso Nuevo separados del juego antiguo | Preparado; sandbox socket errno1 impide arrancar aquí |
| Sesión humana20–30 minutos y curiosidad sin misión | review/HUMAN_READING_SESSION.md | Pendiente de lectura humana real |
| Multiplayer y ciclo completo de tiempo | Cuatro fases, presencia30s, chat10min, cooperación sin party, enemigo/material únicos | Pruebas autenticadas de varios jugadores aprobadas; alcance de balance inicial documentado |

No se declara terminada la fase. El entorno permite comprobar API y persistencia con Flask en proceso, pero impide sockets y arranque de Chromium. No se elude esa restricción ni se etiqueta una prueba API como navegador o Android. Cada revisión nueva debe referirse al hash del contenido que leyó.

La corrección global retiró65 comentarios de diseño de la prosa, aceptó10 correcciones de orientación y eliminó capas diurnas antiguas que contradecían estados o lluvia. Se conserva la valoración anterior como evidencia del ciclo, no como aprobación del contenido actual. El crítico no amplió un4 de cuatro escenas a todo el mundo: releyó ramales, volvió a rechazar causas globales y sólo aceptó después de la nueva corrección y recorrido distinto.

Resultado técnico final:34 pruebas backend PASS en18.989s,44 contratos cliente PASS. Los scripts de recorridos se pueden ejecutar desde esta construcción y usan sólo distribuciones de terceros del runtime propio.


Actualización por la petición de lenguaje claro: se reescribieron162 descripciones, se simplificaron141 nombres y se aclararon resultados y variantes. Las puntuaciones4/5 anteriores pertenecen al catálogo anterior y no se transfieren automáticamente. La revisión de prosa directa y sus hashes están en PLAIN_PROSE.md; no constituye aprobación visual ni una nueva sesión humana.

Mapa de orientación: ORIENTATION_MAP.md registra brújula local, destinos conocidos, regreso manual, direcciones asimétricas y hogar correcto.39 pruebas backend PASS; contratos de mapa y actualización con foco PASS. La revisión visual sigue pendiente.
