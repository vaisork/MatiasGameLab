# Contexto de continuidad de Vintage Telnet

Actualizado: 7 de octubre de 2026, cierre de sesión en horario de México.
Este documento es el punto de entrada para otro programador. Resume decisiones y estado; el historial detallado de ciclos está en `review/GOAL_HANDOFF_20261007.md`. No contiene contraseñas ni sustituye el canon.

## Estado y autorización actuales

Javier pidió explícitamente **pausa**. No continuar la profundización narrativa, el desarrollo general ni acciones de los agentes hasta que lo indique. Después de la pausa autorizó únicamente aplicar el logo también en el DM y guardar este contexto. La petición de contexto no autoriza reanudar la hora de redacción.

El juego tiene una implementación única que se debe continuar. No reiniciar, no descartar contenido ni crear otro prototipo o arquitectura paralela. Conservar jugadores y progresión. El objetivo general de enriquecer el mundo no se declara terminado; tampoco se afirma haber trabajado diez horas continuas.

Repositorio local: `/home/jdiaz/proyectos/vintage-telnet-2-nuevo`, rama `master`. No hay remoto Git configurado y no se ha publicado en GitHub. Una persona con acceso a esta carpeta ve cambios locales; una copia antigua del paquete no los recibe automáticamente. La conversación del chat no acompaña al repositorio: este archivo y los informes son la continuidad escrita.

## Lo que Javier busca

Juego para sus hijos, de lectura comprensible y entretenida, con estética anime consistente y visuales que ayuden a imaginar el mundo. Decisiones con consecuencias, geografía reconocible, personas con motivos, economía útil, encuentros y combates contextualizados. Lenguaje cotidiano, sin palabras rimbombantes, relleno ni párrafos intercambiables. No basta que funcionen endpoints, Three.js o tests: hay que jugar, criticar, corregir y volver a jugar.

Mandato anterior: al menos cinco ciclos diferentes de viaje/geografía; clima/hora/vida regional; criaturas/combate/bestiario; mapa/personaje/integración visual; sesión larga libre. Registrar autocrítica, corregir defectos no enumerados y probar una ruta nueva al final. Los conteos de movimientos y pruebas no prueban diversión humana. Buscar primero contenido canónico que existe pero no llega al jugador.

Última petición de desarrollo, pendiente por pausa: dedicar aproximadamente una hora y tres o cuatro iteraciones a **redacción narrativa para niños**. Los NPC deben explicar quién necesita ayuda, qué ocurre, por qué importa, qué llevar/hacer, adónde y a quién. Encargos como pequeñas historias, con diálogos detallados y consecuencias reales. Salteadores deben hablar y tener contexto, no limitarse a levantar un palo. Criaturas como Espinajo deben correr, cubrirse entre matas y reaccionar en su entorno; no inventar estados mecánicos que el motor no respalda. Claridad y emoción sin insultos fuertes ni violencia gráfica. No convertir todas las caminatas en bloques largos: mantener ritmo y contraste.

## Canon y fuentes

Prompt maestro autorizado: `/home/jdiaz/Descargas/Vintage_Telnet_Prompt_Actualizado.pdf`. Un PDF adjunto distinto fue expresamente omitido por Javier. Extracto temporal existente: `/tmp/vt-authoritative-reread.txt`; no depender de que sobreviva a otro equipo. El comienzo del PDF contiene información sensible: no volcarlo indiscriminadamente en logs o documentación pública.

Consultar `CONTENT_CONTRACT.md`, `CANON_EXPANSION.md`, `docs/ARCHITECTURE.md`, `content/world.json` y `content/regions/*.json`. No importar módulos ni copiar la narración descartada del juego anterior. Se pueden aprovechar funcionalidades buenas, enlaces/despliegue y conceptos de mapa, preservando el contrato nuevo.

Identidades: Valdren/humanos/campos de Edran; Khariel/Felaryn/terrazas de Hoshai, no Japón; Brumak/Dravak/piedra de Korven en superficie, no ciudad enana subterránea; Narevia/Marevyn/aguas de Lethra con edificios sobre el agua y respiración aérea, no ciudad submarina; Velmora/Vesperi/raíces de Nhal, no murciélagos góticos. Vaisgard/Veyra: reutilización pacífica de estructuras antiguas, constructores desconocidos. No crear habitaciones nuevas para resolver confusión: Javier pidió quitar vueltas y simplificar conexiones, no sumar más.

## Funcionalidades y correcciones ya realizadas

- Lectura con cola y controles compactos, tamaño ajustable A−/A+, ritmo acelerado por peticiones sucesivas, colores para clases de texto. Evitar duplicaciones, saltos al pulsar Mirar y acumulación al caminar rápido. Cabecera compacta, direcciones estables, iconos y hasta nueve opciones donde proceda. Combate tiene lectura urgente y barras discretas de salud.
- Mirar presenta la escena y orientación inmediata; Observar atiende detalles, actividad y señales contextuales. No convertir ambos en duplicados. Evaluar/examinar criaturas exige presencia viva: huellas o animales ya vencidos no autorizan evaluación de enemigo vivo. Números de estado se presentan enteros en interfaz aunque existan cálculos fraccionales internos.
- Viajes, permisos de acceso, encuentros regionales, búsqueda/materiales, encargos, memoria de visitas y cambios, mazmorras, comercio, reparación/afinación, recuperación y retorno cercano tras derrota. Poderes deben conservar diferencias reales del contrato.
- Salteadores humanos conceden sellos; recompensa por victoria protegida contra duplicación, sin entradas animales en bestiario. La victoria humana no debe implicar automáticamente muerte. Forajidos tienen ilustraciones separadas.
- Venta visible desde aventura/inventario; compradores y forjas orientan por lugares conocidos, sin revelar destinos no descubiertos. Afinado muestra material, coste y daño antes/después con confirmación; comprar no significa equipar ni curar automáticamente.
- Mapa del mundo descubierto: rutas aprendidas, bifurcaciones desconocidas con líneas punteadas, sin revelar caminos completos. Vista general encuadra los nodos, zoom y centrar ubicación. Posiciones esquemáticas, salidas del servidor como autoridad. Se revisaron 110 nodos y 111 parejas de rutas en un estado de prueba; no es promesa de que todos los jugadores los conocen.
- 3D para especies/personaje y mapa, con alternativas sin WebGL. Javier no quiere bestiario 3D ni animaciones ahora. Modelos Meshy GLB, encuadre y zoom, evitar mostrar primero modelo provisional cuando existe definitivo. Fondos menos cargados y figura grande. Arte de pueblos/hogares en barra superior; bestiario con miniaturas y ampliación al elegir, sin inundar pantalla con imágenes grandes.
- Icono anime de libro/brújula ya aplicado al acceso de inicio, favicon y cabecera compartida de juego y DM. Manifest standalone, iconos Android y apple-touch-icon. La página pública `/dm` fue comprobada cargando el logo de 192px; si una pantalla sigue mostrando V, recargar esa página. No se añade modo sin conexión ni se afirma instalación en dispositivo físico probada.

## Jugadores y arte personalizado

En Raspberry: cuentas Vaison (`vaison`), Senku (`Senku`) y Alivision (`Alivision`), aprobadas. Vaison humano/juramentado; Senku felaryn/arcano; Alivision marevyn/artífice.

Vaison tenía experiencia ganada: tras una solicitud de nivel 1 se corrigió el reinicio excesivo y se restauraron **298 XP acumulados**, quedando nivel 3, XP 80/137 y cuatro puntos de atributo en el momento de la corrección. Son datos históricos, no autorización para imponerlos otra vez: las partidas siguen avanzando. Se retiró armadura de pruebas; no borrar recompensas ganadas ni recursos existentes. El modo de pruebas permite desplazarse a destinos habilitados y recuperarse; no debe convertirse en progreso ficticio o descubrir rutas intermedias.

Referencias originales y PNG de cuerpo completo: `/home/jdiaz/jugadores Vintage Telnet`. Versiones actuales `vaison-anime-nivel-1-v1.png`, `senku-anime-nivel-1-v1.png`, `alivision-anime-nivel-1-v1.png`; prompts correspondientes en la misma carpeta. WebP publicados en `client/art/players/`. Mantener línea anime original, pose frontal normal/A-pose, cuerpo completo, fondo sencillo, poca armadura inicial, especie y clase reconocibles. Vaison usa fotografía frontal nueva; Senku referencia de gato; Alivision conserva identidad de la referencia adaptada a Marevyn. No eliminar fotografías originales.

El personaje muestra su arte personal antes que el genérico de especie, también al ampliar. Campo `portrait` validado contra ruta local permitida. Javier pasará estas imágenes por Meshy y después Bambu Studio; son referencias 2D, no archivos 3D imprimibles. Carpeta Meshy: `/home/jdiaz/Escritorio/Vintage Telnet - Meshy`; se mencionaron Felaryn, Marevyn, Vesperi con esqueleto y Dravak pendiente. Verificar archivos actuales antes de asegurar disponibilidad.

## Director del mundo

DM separado en `/dm`, sin enlace prominente en pantalla de juego. Lista buscable por nombre/cuenta con filtros, paginación y un solo botón Ver jugador. Seleccionar abre ficha y herramientas dentro de ella; no volver a poner todos los botones de cada jugador en el listado.

Ficha muestra imagen actual ampliable, nivel/especie/clase/cuenta y estado. Galería visual de imágenes propias y otras plegadas; no dropdown de nombres de archivos para gestionar retratos. Menú principal azul oscuro, submenús más tranquilos e indentados, controles coherentes. Actualizar jugadores sólo en listado, no en ficha; actualizar ficha está dentro de gestión.

Herramientas: aprobar; habilitar pruebas; añadir XP por progresión normal; regalar sellos/objetos; corregir regalos registrados; curar/recuperar; trasladar a lugar existente; seleccionar retrato; cambiar contraseña de cuenta; expulsar/readmitir. No borrar partida para expulsar. La expulsión revoca sesiones mediante versión, bloquea login y conserva progreso. No almacenar ni mostrar contraseñas en claro. Regalos tienen instancias únicas y registro para no retirar después objetos ganados. Mutaciones requieren DM, CSRF, confirmación y request_id idempotente; reintento de resultado incierto persiste en sessionStorage con intención exacta. Historial y auditoría sin secretos.

El navegador recuerda usuario; contraseñas las conserva el gestor nativo cuando lo ofrece. Nunca guardar contraseña en localStorage.

## Despliegue y datos: precauciones indispensables

Juego oficial: https://raspberrypi.tail3d212e.ts.net/ ; DM: https://raspberrypi.tail3d212e.ts.net/dm . Raspberry Tailscale 100.112.10.16; SSH como jdiaz y root previamente autorizado. Ubuntu Tailscale histórico 100.100.196.125, móvil 100.64.137.31; no confundir instancias.

Producción Raspberry: `/home/jdiaz/proyectos/vintage-telnet-nuevo`. Servicio de usuario `vintage-telnet-nuevo.service`, enabled, Linger=yes, escucha 127.0.0.1:8083, Tailscale Funnel hacia ese puerto. Servicio antiguo de sistema `vintage-telnet.service` stopped/disabled; instalación antigua conservada, respaldo `/var/backups/vintage-telnet-retired-20261007`. No tocar otros servicios de Raspberry.

**La DB Raspberry es autoridad. Nunca sustituirla por la copia Ubuntu.** Archivos privados `runtime/server.env` y `runtime/world.sqlite3` fuera de Git, permisos restrictivos. Respaldar SQLite correctamente antes de migraciones o cambios de datos autorizados. No imprimir env ni hashes/secretos. Acceso público seguro depende de `VT_NEW_PUBLIC_ORIGIN=https://raspberrypi.tail3d212e.ts.net`; conservar comprobación Origin y CSRF. Sólo ProxyFix no resolvía el Origin de Funnel. La comprobación con credenciales intencionadamente incorrectas demuestra que llega al login (401), no que se conoce contraseña real.

Instancia Ubuntu puede seguir usando módulo Python anterior en memoria; archivos estáticos nuevos no prueban que el backend local esté actualizado. Pruebas de backend: servidor aislado con DB temporal o producción sólo lectura. No usar partidas de Javier como fixtures. Reiniciar servicio Raspberry sólo al desplegar Python aprobado; estáticos no precisan reinicio.

Documentos operativos: `ops/RASPBERRY_HANDOFF.md`, `review/raspberry-deploy/DEPLOYMENT.md`. Entrega local `/home/jdiaz/Escritorio/Vintage Telnet - Entrega`: tar.gz, git.bundle, manual e icono. Paquetes se generaron antes de los últimos cambios de esta sesión; reconstruir cuando se acuerde entrega, sin incluir secretos ni cambios narrativos no revisados accidentalmente.

## Estado exacto de Git y trabajo narrativo interrumpido

Últimos commits de funcionalidad: `d0ca7ee` gestión DM y Alivision; `19752c0` controles/galería; `ab92d21` jerarquía y quitar actualizar listado en ficha; `49e0b9e` icono/manifest; `8a8e682` emblema en cabecera. Este documento se confirma aparte, sin incluir modificaciones narrativas.

Al guardar este contexto, **`server/engine.py` está modificado sin commit y sin desplegar** por la tarea narrativa recién iniciada. Existe archivo nuevo `tests/test_narrative_results.py` que debe revisar quien reanude. El agente backend reportó tres pasadas y 40 pruebas focales más cinco narrativas; el agente principal todavía no realizó revisión integral ni contraste de contenido de ese parche: no considerarlo entrega final.

Parche reportado: conversación humana precombate `hablar_adversario`, campos opcionales de contenido `accept_dialogue`, `delivery_text`, `payment_dialogue`, `dialogue`, `defeat_text`; aceptación distingue voz NPC de texto de acción, encargos/compra/venta indican consecuencias y saldo, conversación no cobra ni compromete combate, victoria humana evita afirmar muerte. Verificar API/cliente y compatibilidad antes de continuar. No inventar voz si NPC está ausente ni escena si enemigo no está presente.

Otro agente de fauna estaba revisando sólo `rooms.signals` y `wildlife_pool` en regiones, fue interrumpido por pausa; el estado Git comprobado no mostraba cambios regionales. No atribuir a esa tarea resultados inexistentes. Todos los agentes fueron detenidos; reanudar sólo con petición de Javier.

## Validación y límites de evidencia

Suite completa de referencia: 126 pruebas aprobadas en la entrega de gestión DM; después se añadió prueba de manifest/iconos aprobada por separado. No afirmar suite completa actual 127 pasada sin ejecutarla. Navegador Chrome real con Playwright en tamaños 320/393/1440 según informe. Algunas pruebas usan estado API interceptado para UI y otras recorren API/motor real contra DB temporal: distinguirlas, no llamarlas sesiones productivas auténticas.

Revisiones: `review/dm-management/`, `review/dm-controls/`, `review/dm-password/`, `review/dm-access/`, `review/player-portraits/`, `review/home-icon/`, mapas/lectura/comercio/mazmorras y el handoff histórico. Scripts dejan evidencia de rutas, acciones y errores. No agregar indiscriminadamente screenshots no rastreados ni estados privados de `/tmp`.

Herramientas locales de comprobación: `PYTHONPATH=runtime/python-deps python3 -m unittest ...`; Playwright `/tmp/vt-new-browser-tools/node_modules/playwright/index.mjs`, navegador `/usr/bin/google-chrome`. Evitar colisiones de puertos y cerrar servidores temporales propios. Mantener instrucciones de AGENTS/skills aplicables, comunicación en español y permiso ya existente; no pedir confirmación rutinaria por acciones reversibles autorizadas.

## Al reanudar con autorización

Leer este archivo, contrato y canon seguro; revisar diff actual, validar campo/voz/estado y continuar sobre implementación existente. Profundizar los motivos particulares de encargos y conversaciones en todas las regiones, luego releer secuencias completas y contrastar antes/después. Comprobar que acciones, recompensas, horarios, presencia, memoria, derrota y fauna corresponden realmente al texto. El estado de pausa actual prevalece sobre esta descripción de continuidad.

## Actualización: repositorio preparado para colaboradores

Por petición posterior de Javier, se guardó también el parche narrativo interrumpido junto a sus pruebas, sin desplegarlo. El estado descrito anteriormente como «sin commit» pasa a ser histórico: consultar Git para su commit de preservación. La redacción de contenido y revisión narrativa integral siguen en pausa, no se declaran terminadas. Código, contenido, arte de juego y los cinco modelos de especie están versionados; nuevas herramientas/informes de revisión se incorporan para continuidad. Se quitaron tokens CSRF del informe de fauna temporal antes de guardarlo. Las fotografías originales familiares y los secretos/partidas de producción no forman parte del repositorio distribuible. Las imágenes anime del juego sí.

Validación de la preservación: suite completa actual de 132 pruebas aprobada en 54,122 segundos. Esto comprueba regresiones automatizadas, no completa la revisión narrativa ni autoriza su despliegue.

## Publicación en MatiasGameLab

Por autorización explícita de Javier, esta implementación se incorpora al repositorio `https://github.com/vaisork/MatiasGameLab` en la carpeta `vintage-telnet-2`. Los comentarios anteriores sobre falta de remoto/publicación son históricos. La copia Ubuntu de trabajo conserva su historial independiente; esta entrega incorpora una instantánea revisada sobre el main existente, sin reemplazar los otros proyectos. Antes de publicar se retiraron tokens de sesión de informes de fixtures. No se publican bases de datos, configuración privada ni fotografías familiares originales.
