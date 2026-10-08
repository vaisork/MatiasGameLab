# Revisión técnica de la crónica progresiva

Inspección independiente de `NarrativeJournal` y de las funciones reales de impresión del cliente. Sin navegador ni aprobación de comodidad visual.

El diario separa el contexto del resultado y conserva cambios o actos explícitos; un poll idéntico no añade otra copia de la sala. Cambiar de personaje reinicia su historial y las entradas tienen claves nuevas y un límite de cien. Las observaciones deliberadas y las revisitas pueden repetir una descripción con intención, no por cada refresco.

Se corrigió un caso de movimiento reducido: la impresión instantánea se completaba mientras el feed se insertaba en un contenedor todavía desconectado. Después de conectar la lectura se aplica otra vez el seguimiento al final, únicamente cuando el lector lo mantiene activado. También se añadió «Ir a lo último»: vuelve a seguir el texto sin completar ni cancelar la impresión pendiente. «Mostrar completo» sí completa la cola actual. El lector que está arriba no recibe scroll automático.

`client/qa-printing.mjs` ejecuta las funciones reales con un adaptador mínimo de nodos y temporizadores: orden de impresión, sincronización sin duplicar la cola, desconexión y reanudación, completar, preservar relectura, retirar entradas vencidas, movimiento reducido y reinicio. Quince comprobaciones pasan. Este adaptador no modela layout, física de scroll, foco real o accesibilidad de un navegador. Los 36 contratos generales y ocho de comercio también pasan; el autor verifica por separado el diario.

Se mantiene scroll incremental inmediato durante la impresión. No se añadió una interpolación suave sin evidencia de navegador: los eventos intermedios del scroll programático pueden aparentar que el lector dejó de seguir el final y cortar ese seguimiento. La adecuación visual y un desplazamiento suave al terminar bloques siguen necesitando prueba real; no se declaran resueltos por el adaptador.
