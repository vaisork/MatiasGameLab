# Sesión lectora nueva de 20–30 minutos

Preparada; **no ejecutada** en este entorno. La prueba requiere un navegador real en el equipo donde esté iniciado el servidor nuevo. No reutiliza el arnés del juego anterior. El arnés `scripts/browser-review-new.mjs` verifica alta, aprobación real, escena, decisión escrita, relogin y capturas a 320/390/1440 píxeles. No demuestra calidad de una sesión humana ni cobro de encargos. Necesita Playwright instalado en herramientas y contraseña Director privada en entorno; nunca guarda esa contraseña.

## Recorrido humano

1. **0–4 minutos:** registrar una cuenta de prueba, crear personaje y aprobarlo desde `/dm`. Leer el hogar sin saltar párrafos. Anotar qué permite situar puerta, mesa, luz y relación con el exterior. Salir mediante una posibilidad ofrecida.
2. **4–10 minutos:** seguir caminos mediante las direcciones visibles. Antes de cada paso, anticipar qué cambio espacial implica y contrastarlo al llegar. Usar al menos una decisión escrita y una conversación; preguntar un tema disponible. Anotar si se comprende quién habla y qué está haciendo sin depender de una etiqueta.
3. **10–20 minutos:** llegar a Valdren por conexiones reales y visitar la fragua. Aceptar el recado de Daro si está disponible, leer qué solicita y dónde se cobra. Visitar el cobertizo y hablar con Bren sobre la rueda. Volver a Daro y entregar mediante la acción ofrecida. El pago de este encargo es 6 sellos, no un premio por sólo pasar por el cobertizo. Intentar cobrar otra vez y comprobar que no existe un segundo pago. Registrar vitalidad, sellos, texto y recuerdos antes/después; no editar el estado.
4. **20–25 minutos:** regresar a un lugar ya visitado. Comparar reconocimiento con lo efectivamente realizado, releer el historial y visitar el mapa conocido. Debe mantenerse la misma localización al consultar fichas.
5. **25–30 minutos:** salir de la cuenta y volver a entrar. Comprobar personaje, ubicación, mochila, sellos y diario. Repetir lectura en móvil vertical, teclado abierto y desplazamiento; confirmar que escribir conserva el borrador y no tapa la decisión.

Si el ritmo del lector no alcanza Valdren en el tiempo, prolongar el recorrido o registrar el encargo como pendiente; no teletransportar ni convertir el límite temporal en evidencia de cobro. Para revisar noche/lluvia, usar una sesión de prueba con reloj controlado claramente identificado o esperar esos cambios reales. No declarar condiciones que no se observaron.

## Evidencia que debe recoger la persona

- Tres lugares reconocibles por sus usos, materiales y conexiones sin leer sus nombres.
- Una decisión con consecuencia concreta y un retorno que reconozca solamente hechos vividos.
- Una conversación cuyo tono difiera de otra persona.
- Una pausa o detalle que aporte ritmo sin encadenar siempre observar/atribuir/registrar.
- Capturas completas de lectura y controles a 320 y 390 píxeles, errores de consola y cualquier acción ofrecida que contradiga la escena.
- Resultado del encargo y del relogin, con las comprobaciones anteriores; nunca contraseña ni cookie en capturas o informe.

La aprobación de esta revisión necesita evidencia real. Archivos preparados y pruebas API no sustituyen el juicio de la persona que lee.

## Ejecutar la revisión técnica de navegador

En Ubuntu normal, inicia el juego nuevo con `./start.sh`. En otra terminal, desde esta carpeta, instala la herramienta con `npm install --no-save playwright`. El arnés usa el Chrome instalado; no necesita descargar otro navegador. Introduce la credencial del director sin escribirla en el historial:

```bash
read -r -s -p "Contraseña del director: " VT_REVIEW_DM_PASSWORD
printf "\n"
export VT_REVIEW_DM_PASSWORD
VT_REVIEW_OUTPUT="$PWD/review/browser-artifacts" npm run review:browser
unset VT_REVIEW_DM_PASSWORD
```

El arnés crea una cuenta de revisión nueva y aprueba ese personaje mediante la interfaz del director. No cambia posición ni recuerdos directamente. Los resultados sólo cuentan como evidencia después de ejecutarlo; las capturas todavía requieren revisión visual y no equivalen a una lectura humana de20–30minutos.
