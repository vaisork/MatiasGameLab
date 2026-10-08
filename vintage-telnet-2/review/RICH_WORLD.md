# Encuentros, búsqueda, capacidades y arte inicial

Cambios autorizados por el usuario el 5 de octubre de 2026: encuentros aleatorios, hallazgos al buscar, más razones para regresar, efectos de clase reconocibles, mayor velocidad de lectura, bifurcaciones del mapa y primera ilustración de bestiario. La autorización posterior de arte se aplica al bestiario; la terminal continúa sin imágenes.

Los hábitats exteriores tienen pools de fauna local. Al llegar o buscar se sortea presencia con probabilidad de 45%; el resultado se conserva cinco minutos en el mundo compartido. GET, mirar, observar y refrescar no vuelven a sortear. Una criatura que ya participa en un combate conserva su presencia. Los avisos usan ecología y conducta del canon; los animales no inician automáticamente una pelea. Los depredadores superiores requieren observar de cerca y permiten retirarse antes del enfrentamiento.

Buscar tiene resultados distintos: material regional, rastro o nada. Cada región tiene material y texto propios; el hallazgo queda en mochila, memoria y conocimiento que puede reconocer un NPC. No entrega dinero ni XP. Espera de 60 segundos entre búsquedas de un mismo personaje en la misma sala; recursos compartidos se reponen tras 30 minutos, evitando duplicación inmediata. El inventario se guarda mediante las transacciones e idempotencia existentes. No se presenta un sistema de fabricación como terminado.

Las cuatro capacidades conservan sus reglas numéricas y ahora explican los efectos: guardia y reducción de daño, impulso y preparación/precisión, sombra y apertura tras fallo, tiro e interrupción al acertar. Los perfiles regionales nuevos reutilizan los dos niveles de amenaza existentes; faltan calibración por criatura y capacidades avanzadas de PP. No se inventaron nuevas escalas numéricas para esta ampliación.

La lectura imprime 3 caracteres cada 24 ms, con pausa de 120 ms entre párrafos. Observar añade un detalle concreto del lugar; Mirar conserva la vista general y Buscar revisa lo que puede recogerse.

Las casillas del mapa muestran direcciones + ? de salidas pendientes en lugares visitados; no exponen destinos ocultos. Las líneas siguen limitadas a rutas recorridas.

Se generó una lámina naturalista de Pinzajunco con la habilidad imagegen. Pinzas desiguales, barro, raíces y hoja arrastrada al refugio respetan el canon. Se conserva el original generado; el WebP de 389 KiB está en client/art/bestiary y se carga perezosamente únicamente en su entrada descubierta. El servidor permite imágenes del propio origen y restringe el directorio de assets; la terminal no carga ilustraciones.

Validación: 46 pruebas backend; pruebas de poderes con consecuencias numéricas distintas; azar presente/ausente, aviso regional, inventario persistente, reposición y reintento sin duplicar; pruebas técnicas de controles/mapa/lectura. Evidencia Chromium de hallazgo regional, combate aleatorio controlado, capacidad Sombra, retirada, bifurcaciones y lámina está en browser-rich/. Emulación, no prueba física de Android ni validación humana de 20–30 minutos.

Actualización posterior: el usuario pidió estilo anime infantil marcado y miniaturas que sólo se amplían al tocar. La versión vigente y su validación están en BESTIARY_ANIME.md; la lámina naturalista describe la primera entrega histórica.
