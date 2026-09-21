# HANDOFF — Entrega técnica

## ENTREGA PARA CHATGPT

**Estado:** ENTREGA PREPARADA EN RAMA — NO PUBLICADA

### Desarrollador
Desarrollador Junior de Vintage Telnet

### Estado base
Commit/HEAD de `main`:
`4f015d48a7cfbc7cdf0fbac0e1fd7afe70876270`

### Rama
`junior/vintage-telnet-mobile-v2`

### Objetivo
Aplicar la investigación `VT-RES-002` para optimizar la interfaz HTML de Vintage Telnet en celular y separar visualmente la carcasa HTML café de la terminal Telnet negra/verde.

### Archivos modificados
- `vintage-telnet.html`
- `HANDOFF.md`

### Investigación consumida
- `vintage-telnet/RESEARCH_MOBILE_TELNET_UI.md`

### Cambios realizados
- Terminal Telnet convertida en una zona visual inequívoca: negro casi puro, texto verde y tipografía monoespaciada.
- Carcasa HTML conservada en tonos café/ocre para distinguir herramientas web de la sesión Telnet.
- Layout móvil rehecho como shell de alto visible con terminal flexible y scroll interno.
- En teléfono, mapa/estado dejan de ocupar espacio permanente; mapa/personaje/inventario/ayuda se abren en dialogs.
- Controles principales compactados sin reducirlos por debajo de objetivos táctiles prácticos.
- Cruceta N/O/Mirar/E/S mantenida con relación espacial clara.
- Atacar y Huir permanecen visibles como acciones principales de demo.
- Entrada de comandos conserva 16 px, añade `enterkeyhint="send"` y permanece próxima a la terminal.
- Safe areas incorporadas para notch/home indicator.
- Se eliminó `scrollIntoView` del documento: ahora solo se desplaza el log interno de terminal.
- Añadido soporte `prefers-reduced-motion`.
- Responsive reorganizado: compacto <=640 px, intermedio hasta 959 px, lateral persistente desde 960 px.
- No se añadieron frameworks ni lógica paralela de botones.

### Qué es funcional
- Navegación local de demo por N/S/E/O.
- Mirar.
- Entrada escrita de comandos y alias n/s/e/o.
- Botones y comandos siguen entrando por la misma función `perform()`.
- Mapa/personaje/inventario/ayuda mediante dialogs.
- Scroll interno de terminal.
- Layout compacto para teléfono y dos columnas en escritorio.
- Indicadores locales de última acción y combate.

### Qué sigue siendo demostración
- Ubicación y conectividad de la microzona.
- Mapa mostrado.
- Estado de sesión.
- Combate.
- Inventario/personaje.
- Todo continúa sin Raspberry Pi ni persistencia real.

### NECESIDAD DEL SERVIDOR
- Sin cambios respecto a la entrega anterior: contrato de acciones, estado persistente, ubicación real, inventario, combate, descubrimiento y resincronización.

### NECESIDAD DE JUGABILIDAD
- Sin cambios respecto a la entrega anterior: objetivo de ataque, huida, vocabulario definitivo y datos exactos de combate/personaje/mapa.

### Pruebas realizadas
- Comprobación estructural de terminal negra/verde.
- Comprobación de media query móvil <=640 px.
- Comprobación de terminal con scroll interno.
- Comprobación de targets táctiles de 44–46 px o mayores.
- Comprobación de safe areas superior e inferior.
- Comprobación de dialogs para mapa/personaje/inventario/ayuda.
- Comprobación de `enterkeyhint="send"`.
- Comprobación de ruta única `perform()` para botón y comando.
- Comprobación de ausencia de `scrollIntoView`.
- Comprobación de `prefers-reduced-motion`.
- Confirmación de que no se añadió framework externo.

### Prueba visual que Javier/Matías deben hacer
1. Abrir en teléfono vertical.
2. Confirmar que se percibe inmediatamente la separación: café = cliente HTML; negro/verde = Telnet.
3. Revisar cuántas líneas de texto caben sin scroll de página.
4. Moverse con una mano usando N/S/E/O.
5. Probar Mirar, Atacar y Huir.
6. Escribir 5–10 comandos seguidos con el teclado abierto.
7. Abrir/cerrar mapa, personaje, inventario y ayuda.
8. Girar teléfono a horizontal y regresar.
9. Probar en iPad vertical/horizontal.
10. Decidir si los controles siguen ocupando demasiado o si la proporción ya se siente correcta.

### Riesgos/conflictos
- Validación visual final requiere teléfono/iPad real.
- La terminal usa scroll interno en móvil; Javier/Matías deben confirmar que esta interacción resulta natural.
- Si `main` cambia antes de integrar, el Integrador debe volver a comparar la rama.

### Aviso para el Integrador/Publicador
No publicar hasta autorización expresa de Javier. Comparar esta rama contra el HEAD vigente de `main` antes de integrar.

**LISTO PARA REVISIÓN:** SÍ  
**LISTO PARA PUBLICAR:** SOLO TRAS AUTORIZACIÓN “sube”
