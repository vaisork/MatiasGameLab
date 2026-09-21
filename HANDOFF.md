# HANDOFF — Entrega técnica

## ENTREGA PARA CHATGPT

**Estado:** PUBLICADA EN `main`

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
**PUBLICADA EN `main`:** SÍ — autorización “Sube” recibida el 2026-09-21  
**MERGE COMMIT:** `c156fce377203534f7d9cb14632ef4f36815310c`


## INTEGRACIÓN DE ARTE HTML — Vintage Telnet

**Fecha:** 2026-09-21  
**Estado:** INTEGRADO EN `main`

### Origen de la entrega
- Rama: `art/vintage-telnet-html-assets`
- Commit de arte revisado: `886314bfd9be648938cc7668e2527a079050d231`
- Estado antes de integrar: rama 1 commit adelante de `main` y 0 atrás.

### Qué se integró
Biblioteca modular de arte para la carcasa HTML de Vintage Telnet en:
`vintage-telnet/assets/html-ui/`

Incluye:
- botones para Inventario, Mapa, Huir y Poderes;
- ornamento de esquina;
- divisor horizontal dorado;
- textura azul/pizarra repetible;
- preview móvil de referencia;
- `README.md` y `ASSET_MANIFEST.md` con instrucciones de uso, tamaños y alcance.

### Criterio de revisión aplicado
- Los PNG son assets modulares; no sustituyen controles HTML reales.
- La terminal Telnet negro/verde debe mantenerse separada de la carcasa visual exterior.
- El arte sigue una dirección más juvenil/mobile-first y menos recargada.
- El botón `Poderes` queda como categoría visual; no define mecánicas ni poderes concretos.
- No se modificó `vintage-telnet.html` durante esta integración.
- No se modificó Senku.

### Pendiente
La siguiente tarea separada será adaptar `vintage-telnet.html` para consumir estos assets sin romper la lógica existente ni la ruta única de acciones del cliente.

### Resultado
- Arte integrado a `main`: SÍ.
- HTML actualizado para usar el arte: NO, pendiente de una tarea posterior.
- Publicación/servidor Raspberry: sin cambios por esta integración.


## PREPARACIÓN DE BASE DE DATOS Y JUGABILIDAD REAL — Vintage Telnet

**Fecha:** 2026-09-21  
**Estado:** PREPARACIÓN DOCUMENTADA; SERVIDOR V2 NO INTEGRADO

### Trabajo realizado
- Revisada la rama `claude/vintage-telnet-server-v2`.
- Commit revisado: `ca7be621cc7862cf4cbb7a34eaea0a787820cf63`.
- La entrega reporta SQLite real, cuentas/sesiones, aprobación del Dungeon Master, especies, ubicación persistente, movimiento N/S/E/O, chat local y API estructurada.
- La rama está divergida respecto a `main`; no se integró automáticamente.
- Se creó `vintage-telnet/DATABASE_GAMEPLAY_PREP.md` con el primer vertical slice jugable real, requisitos mínimos de persistencia, contrato cliente-servidor necesario, seguridad, pruebas y secuencia recomendada.

### Primer hito jugable acordado para preparación
`Abrir → entrar → aprobar cuenta → elegir especie → aparecer en pueblo → moverse → ver otro jugador → hablar → cerrar → volver → conservar ubicación.`

### Importante
- No se implementó ni inventó combate.
- No se modificó `vintage-telnet.html`.
- No se desplegó nada a Raspberry Pi.
- No se integró la rama de servidor V2.
- La siguiente acción técnica corresponde a revisión/actualización del servidor V2 contra el `main` vigente y cierre del contrato cliente-servidor.


## PRIORIDAD P0 — PRIMER SLICE JUGABLE REAL

Javier fijó la prioridad del siguiente hito:

**ENTRAR → ELEGIR ESPECIE → MOVERSE POR EL PUEBLO**

Se creó `vintage-telnet/FIRST_PLAYABLE_SLICE.md` con el alcance completo, contrato mínimo requerido, persistencia, responsabilidades y prueba de aceptación.

Por decisión de alcance, quedan fuera de este primer slice: chat, combate, PvP, clases, estadísticas, inventario, Arcanes, poderes, economía, monstruos, secretos y mapa completo.

El objetivo es llegar antes a una versión realmente persistente y jugable en teléfono.
