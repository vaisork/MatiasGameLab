# Lenguaje claro y avance perceptible

Javier pide sentir que avanza y evitar palabras rimbombantes. Se reescribieron las162 descripciones de sala y se simplificaron141 nombres locales, manteniendo asentamientos y culturas canónicas. Las escenas hablan de caminos, agua, herramientas y personas; no explican lo que el escenario «enseña», «simboliza» o «demuestra». Cada llegada da orientación y un detalle local. Catorce lugares tranquilos tienen textos más breves para conservar aire y variación. No se recorta automáticamente por caracteres.

Los resultados de catorce acciones de Edran/Veyra dicen qué hizo la persona y qué cambió: agua que empieza a bajar, cuña sujeta, aviso corregido. Se simplificaron variantes de clima, horario, memoria y cuatro estados físicos que antes podían devolver párrafos antiguos. La astilla se reconoce por observación anterior; la narración no implica transportar un objeto que se dejó en el camino.

La crónica dice «Llegas a…» al cambiar de sala y «Entras en…» sólo al cruzar realmente de región. No concede XP, moneda, objetos o misiones completadas por imprimir esos mensajes. Una actualización pasiva no repite la llegada. Las reglas de mundo y las acciones disponibles siguen siendo del servidor.

Root escribió58 salas de Edran/Veyra y revisó las104 de Hoshai/Korven/Lethra/Nhal. El revisor escribió esas104 y revisó las58 de root, sus resultados y los nombres finales. Los informes DIRECT_PROSE_ROOT_REVIEW.md y DIRECT_PROSE_REGIONS.json distinguen inspección de fuente y evidencia técnica; no son revisión visual. PLAIN_PROSE_INTEGRITY.json registra longitudes y hashes actuales. No se trasladan a esta prosa las puntuaciones literarias de versiones anteriores.

Validación:34 pruebas backend pasan; el recorrido API actual recorre66 acciones y19 puntos por Edran/Lethra con amanecer, día, atardecer y noche, sin cambiar directamente posición o conocimiento. API_READER_PLAIN_EDRAN.json conserva snapshots y hashes y deja intacta la evidencia anterior. El cliente comprueba impresión, historial, ausencia de duplicados, texto de llegada y aviso de región. Son pruebas en proceso, no20–30 minutos humanos ni navegador. La revisión visual continúa limitada por el entorno.

Recargar activa el cliente nuevo. Los catálogos se leen en cada petición, por lo que los textos nuevos no necesitan reiniciar el servidor ni cambiar los datos guardados de personajes.
