# HANDOFF — Entrega técnica

## ENTREGA PARA CHATGPT

**Estado:** ENTREGA PREPARADA EN RAMA — NO PUBLICADA

### Desarrollador
Desarrollador Junior de Vintage Telnet

### Estado base
`main`: `7d572f09bbd8f8a4edcba55ec113e27ecf3b6398`

### Rama
`junior/vintage-telnet-help-character`

### Objetivo
Aplicar dos decisiones nuevas de Javier:
1. preparar el panel **Personaje** para mostrar una imagen 3D que subirá el Dungeon Master;
2. hacer que **Ayuda** ocupe toda la pantalla.

### Archivos modificados
- `vintage-telnet.html`
- `HANDOFF.md`

### Cambios realizados
- `Ayuda` ahora abre un `<dialog>` de pantalla completa.
- La ayuda está organizada en secciones: movimiento, explorar, combate, herramientas, comandos y estado de la demo.
- En móvil la ayuda usa una sola columna; en pantallas mayores usa dos columnas.
- El panel `Personaje` incluye un área visual preparada para la futura imagen 3D.
- No se inventó ninguna ruta de asset.
- Se documenta explícitamente que el asset lo subirá el Dungeon Master.
- No se modificó Jugabilidad, servidor, persistencia ni canon.

### Dependencia pendiente
**ASSET DEL DUNGEON MASTER:** imagen 3D del personaje y su ruta definitiva en el repositorio.

Cuando el asset exista, Desarrollo podrá reemplazar el placeholder por la imagen real sin rediseñar el panel.

### Pruebas realizadas
- Verificación de que `helpDialog` usa clase `fullscreen`.
- Verificación de ancho 100vw y alto 100dvh.
- Verificación de safe areas en cabecera y cuerpo de ayuda.
- Verificación de layout de ayuda a una columna en móvil.
- Verificación de placeholder de Personaje sin ruta inventada.
- Confirmación de que botones/comandos existentes no fueron modificados.

### Prueba visual para Javier/Matías
1. Abrir Ayuda y comprobar que ocupa toda la pantalla.
2. Cerrar Ayuda con la X.
3. Abrir Personaje y comprobar que el espacio para la imagen 3D se entiende.
4. Confirmar que el resto de la interfaz V2 se mantiene igual.

### Aviso para Integrador
No publicar hasta autorización expresa de Javier.

**LISTO PARA REVISIÓN:** SÍ  
**LISTO PARA PUBLICAR:** SOLO TRAS AUTORIZACIÓN “sube”
