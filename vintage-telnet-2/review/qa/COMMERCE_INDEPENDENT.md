# Revisión independiente de comercio y reparación

Se contrastaron el PDF autoritativo releído (acciones comprar/vender como parte de la experiencia), el contrato del servidor nuevo, los temas de Daro y el cliente. No se añadieron mecánicas ni imágenes. La última instrucción explícita de interfaz textual sigue vigente.

La fuente muestra compra con débito y alta de instancia independiente; venta requiere pertenencia/acción disponible y confirmación explícita de arma; una pieza equipada o la última utilizable no se ofrece para venta. El servidor valida disponibilidad antes de aplicar. Reparar requiere servicio/pieza dañada/sellos, cobra ocho y cambia condición sin equipar la pieza. No encontré una operación que venda dos UUID a la vez, autoequipe la compra o repare gratis. La selección escrita con nombres repetidos es ambigua y debe rechazarse: las fichas identifican una instancia por su target, sin mostrar identificadores internos al jugador.

Se corrigió el hueco de interfaz: la mochila muestra sellos, estado dañado, validación pendiente y pieza en uso; incluye reparación disponible y guardar pieza, además de equipar/usar/vender. Dos objetos con igual nombre conservan fichas separadas y números de ejemplar; la confirmación de venta incorpora ese número. Compras disponibles se muestran en una sección del lugar, con precios del servidor. No se infiere precio ni se permite una acción no ofrecida.

El texto de Daro sobre armas distingue procedencias por talleres y viajeros y orienta dónde buscar otras familias. Su tema de reparación explica precio y devolución guardada en palabras del servicio. El tono es coherente con una fragua y con el acto siguiente del jugador; no revela APIs ni UUID y no solicita ilustraciones. Nombrar martillo/hoja regional no se confunde con ofrecer una compra actualmente disponible: los botones proceden de `actions`.

Se señaló al autor que Equipar se ofrecía sobre piezas dañadas/no activadas aun cuando la aplicación lo rechazaba. El autor anunció la corrección a `disabled` y `reason`; debe conservarse como decisión authoritative. El cliente respeta ambas propiedades.

Validación: sintaxis JavaScript, 36 contratos generales y ocho contratos focales de transporte de instancias/confirmación/reparación/reintento. Los ocho usan identificadores de ejemplo para probar el protocolo, no una afirmación de recorrido o economía real. La revisión de invariantes del servidor es de código; sus pruebas y recorridos son evidencia separada del autor. No se hizo revisión visual ni se declara aprobado el flujo de navegador.
