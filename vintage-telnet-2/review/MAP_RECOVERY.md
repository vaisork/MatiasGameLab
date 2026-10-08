# Conexiones y recuperación tras derrota

Se revisaron 162 lugares y 344 salidas: todos los destinos existen y todas las conexiones tienen regreso. Cinco pares de Edran salen y regresan por puntos cardinales que no son opuestos. Se mantienen sus salidas existentes y se aclaran los giros en las descripciones de Senda de regreso, Salida de las Cercas Bajas, Zanja seca y Borde de los Sauces Bajos. No se inventan túneles para justificar una derrota.

El mapa trazaba líneas rectas que atravesaban casillas de otros lugares. Ahora los caminos salen por el lado indicado por su dirección real y pasan por los espacios entre casillas; las letras N/S/E/O señalan las salidas. La vista inicial se centra en el lugar elegido y sus conexiones conocidas a un máximo de tres pasos. Ver todo conserva el panorama de lo descubierto. No se revelan destinos de bifurcaciones pendientes. El panorama completo sigue siendo un esquema, sin coordenadas geográficas canónicas.

La derrota antes seleccionaba siempre el asentamiento de la región del encuentro. Ahora se calcula el pueblo más próximo en número de pasos por salidas reales, incluso al otro lado de una frontera. Conserva vitalidad de recuperación al 60%, fatiga y progreso según las reglas vigentes. No añade una ruta entre el lugar de derrota y el pueblo. El mensaje y el mapa guardan origen, destino y distancia del último traslado nuevo; no se inventa retrospectivamente esa información para derrotas anteriores.

Prueba concreta: Primera subida de Hoshai lleva al Mercado de Vaisgard (4 pasos); Puente de las Tablas Separadas a Plaza de Narevia (3); Relevo de altura a Plaza de Khariel (4); meseta de Korven a Patio de Brumak (3). Se verifican conservación de progreso y ausencia de ruta falsa tras derrota.

Validación: 47 pruebas backend pasan; pruebas técnicas de conexiones, trayectorias que evitan casillas ajenas, retornos no opuestos y nodos ocultos. Chromium revisa el mapa de 89 lugares conocidos y el recorrido de exploración anterior en servidor aislado. Evidencia en world-map-species/ y map-species-browser/. No equivale a prueba física Android ni a sesión humana de 20–30 minutos.
