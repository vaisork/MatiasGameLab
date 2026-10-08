# Ciclo 14 · ruta ciega de Narevia

Marevyn femenina/juramentado creada con gender=femenino y aprobada en API real, DB temporal destruida al terminar. 96 movimientos legales, 42 salas distintas, 120+ acciones con conversaciones, observaciones y comercio. RNG .9; cada acción avanza 60 segundos; espera monotónica hasta atardecer y noche. No usuarios reales, teleport, flags insertados ni edición de contenido. Script depth-cycle14-blind.py y evidencia JSON/READABLE. El primer intento usó por error el tópico inexistente costuras de Mira; fue rechazado y se sustituyó por el tópico público paño antes de completar el paseo. No se corrigió prosa para favorecer resultado.

Secuencia distinta a C13: Narevia→mercado→Mira/paño→plan cubierto→Nima/caldo y preparativos→cobro→huerta y mercado Vaisgard→almacén/Brumak/lavado→cantera→regreso mercado y cocina Narevia→muelle→mercado nocturno. No se usa acequia ni secadero del ciclo13. Hay más de veinte salas distintas entre comienzo y regreso.

La información comercial coincide con las acciones: Narevia ofrece puñal 50, varita 40 y provisión 8; Bela explica las cuatro armas comunes y el mercado de Vaisgard añade arco 65/espada 85. La provisión explica recuperación antes de compra. El encargo suma seis sellos, de 20 a 26; comprar consume ocho y queda18. No se confunde recompensa con riqueza para comprar cualquier arma. No se probó vender ni precio de todos los materiales.

Las conversaciones añaden motivo doméstico: Mira sitúa una costura de su hermana; Nima bromea sobre las hojas amargas que puso su padre. La elección cubierta se comunica mediante acción real y conserva cuencos cubiertos al regresar. Al atardecer hay caldo antes que hermanas y ventana del padre; el retorno recuerda la plataforma donde sigue secándose el paño. Vida cotidiana y estado del encargo coexisten sin nueva recompensa al mirar.

La ruta cambia de agua y tablas curvadas a cuenca con muros viejos, cantera y roca con lavado. Hay viento en Narevia inicial, niebla en Vaisgard, lluvia en Korven; vuelta nocturna Narevia trae niebla y voces entre recipientes. Las descripciones de clima son locales reales, no clima impuesto. La noche cambia actividad del puesto; no se comprobó todas las horas ni cada clima disponible. La ruta mantiene mucho traslado de recipientes/cargas, aunque comida, humor, fruta, hongos/animales y cantera rompen la plantilla.

## Defecto observado que impide cierre completo

Después de cobro, volver y preguntar reunión a Tila produce dos mensajes incompatibles en la misma respuesta. Primero «Mira las costuras… decide… Nima necesita la noticia antes de poner los cuencos»; después discovery contextual «Nima ya recibió tu propuesta; llevaré la entrega al lugar que acordasteis». C6 conserva historia, pero la añade detrás del tópico inicial sin sustituir su instrucción obsoleta. No se afirma que falta contexto ni se ignora el segundo mensaje: el fallo es pedir otra vez una decisión ya comunicada.

Prioridad siguiente: override del tópico reunión condicionado a comunicado/pagado, o selección equivalente que sustituya únicamente el tópico relevante. Mantener los temas comprar/vender/cuidados independientes, las recompensas y acciones existentes. Validar tres momentos (antes de decisión, comunicado, pagado) y respuesta de observador sin flags. No editar esta ruta para renombrarla PASS; necesita ciclo siguiente y otra evidencia.

| Criterio | Valoración | Límite |
|---|---:|---|
| Identidad y continuidad | 4 | Agua→cuenca→roca coherente en42salas; no seis regiones |
| Ritmo y vida | 4 | Humor doméstico, cocina, mercado, cantera y lavado; logística frecuente |
| Hora y clima | 4 | Actividad nocturna y climas locales distintos; no barrido exhaustivo |
| Precio e información comercial | 4 | Etiquetas, oferta regional y aritmética reales; venta no probada |
| Contexto después del encargo | 3 | Tópico antiguo y contexto nuevo se contradicen en respuesta de Tila |
| Estilo | 4 | Mayoría gesto y material; todavía frases interpretativas aisladas |
| Género persistente | confirmado | API conserva femenino; no prueba variantes de toda prosa ni 3D |
| Cliente/3D | — | Esta prueba API no acredita representación visual |

Resultado: FAIL en contexto de diálogo después de misión. Las mejoras C13 no regresan en esta ruta, pero el paseo revela otro defecto concreto. Evidencia conservada sin editar contenido ni rebajar criterio.
