# Dirección visual y continuidad

Referencia vigente: 13 vistas ambientales en `client/art/places/`: seis pueblos, cinco hogares, fragua de Valdren y escalones de Brumak. Conservar originales aprobados. Comparación visual realizada con hoja de contacto y ampliación de Vaisgard; no equivale a aceptación humana nueva.

Línea común: anime fantástico para niños y adolescentes, línea fina, fondos pintados con sombras de cel, materiales vividos, luz natural, composición legible. Mantener detalle funcional antes que espectáculo. Las figuras son secundarias al entorno.

| Región | Relieve y suelo | Materiales y actividad | Paleta y atmósfera |
|---|---|---|---|
| Veyra | Cuenca de colinas bajas y arroyos | Mampostería antigua reutilizada, reparación de madera, circulación de cargas y convivencia | Caliza miel, tejados terrosos, telas discretas, verde de huertas; sierra sólo distante |
| Edran | Llanura abierta, parcelas, acequias y rodadas | Casas modestas de piedra y madera, cercas bajas, grano y carros | Tierra ocre, trigo y verde cultivado; horizonte ancho |
| Hoshai | Pendiente, grava, pared húmeda, pinos separados y paso estrecho | Terrazas asimétricas, rampas, puentes cortos, apoyos reparados | Piedra clara, azul de distancia y verde alpino; aire fresco, altura convincente |
| Korven | Pedrales fracturados, cauces secos, entrantes que frenan viento | Edificios bajos sobre superficie, carros compactos, cisterna y cerámica | Piedra seca y salvia, sombras duras locales; sin mina enana |
| Lethra | Ribera que se ablanda, juncos, canales y plataformas | Madera sobre agua, amarre, secado de fibras y barcas en seco | Verde húmedo, agua clara azul verdosa, madera cálida; casas y personas al aire |
| Nhal | Dosel denso, hojas, raíces, musgo y puentes bajos | Hogares discretos, luz orientada al trabajo, madera práctica | Verde oscuro, tierra húmeda, cálidos pequeños; sin gótico ni magia inventada |

## Hora y clima

`Engine.ambient` usa cuatro fases: noche antes de 6 y desde 20; amanecer 6–8; día 8–18; atardecer 18–20, sobre su reloj epoch. Clima regional cambia por bloques de dos horas con offset por región. El arte actual resuelve una ruta fija por id o tipo/región en `placeArt`, sin selección por hora o clima. No añadir variantes indiscriminadas ni cambiar motor. Futuras variantes deben proponerse con clave explícita y lectura ambiental como autoridad.

Primero completar cobertura base. Variantes útiles posteriores: lluvia en calle de toldos (desagües y cajas elevadas), noche en entrada de Velmora (luces orientadas), lluvia en cisterna de Korven (escorrentía separada del abastecimiento). Son propuestas pendientes, no imágenes entregadas.

## Riesgos de continuidad existentes

Vaisgard aprobado incluye relieve muy marcado al fondo. No se sustituye esa imagen: las nuevas vistas usan cuenca baja y sierra distante conforme al canon. Se conserva lenguaje de piedra y madera, sin propagar relieve montañoso a toda Veyra.

La vista de escalones de Brumak recuerda terrazas amplias de Hoshai. Conservarla; en nuevas aproximaciones usar entrantes bajos y roca irregular, sin ampliar monumentalidad.

Las 183 salas públicas y las cinco plantillas de hogar son inventarios distintos. Los ids de hogares pertenecen a partidas privadas y no se exportan.
