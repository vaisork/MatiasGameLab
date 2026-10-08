# Crónica continua e impresión progresiva

Corrección tras la observación de Javier: «Texto muy repetido aparece de golpe». Se releen las instrucciones de la fuente autoritativa de Descargas: crónica en vivo, cada nueva línea como impresión de terminal, salida breve y no desesperadamente lenta, separadores, cursor mínimo y posibilidad de releer. No basta una caja con apariencia terminal.

Antes, adventure() concatenaba la última respuesta y una nueva copia completa de la escena en cada actualización. render() sustituía todos esos párrafos inmediatamente. Ahora NarrativeJournal recibe los snapshots autoritativos y conserva una sola secuencia: título/lugar y descripción al llegar, resultado al actuar, cambios ambientales nuevos al actualizar. Un refresh o reintento no vuelve a añadir la escena; observar explícitamente o regresar a un lugar sí permite releer detalles. La secuencia se separa por personaje y conserva hasta100 entradas en esta pestaña. No modifica ni inventa estado del servidor.

El panel de lectura reutiliza sus nodos y mantiene el progreso de impresión al actualizar controles. Los nuevos textos se imprimen en una cola rápida por fragmentos; «Mostrar completo» termina la impresión sin cambiar la aventura. Reducir efectos y la preferencia del sistema muestran texto inmediato. Los lectores de pantalla reciben cada texto completo, sin anunciar cada fragmento ni exponer HTML arbitrario. Volver a vistas o ajustar tipografía no inicia de nuevo lo leído.

Se conserva scroll interno para releer; nuevas entradas siguen el final únicamente si el lector lo estaba siguiendo. El scroll de la página no avanza por cada línea. Combate y botones derivan del snapshot y nunca esperan a la animación para resolver reglas. No se bloquea una decisión por duración del texto.

Pruebas: qa-narrative.mjs12 casos de incorporación y aislamiento, además de los44 contratos existentes y sintaxis. Los tests de fuente no demuestran comodidad visual; faltan navegador y percepción humana del ritmo. No se anuncia revisión visual aprobada ni se sustituye sesión humana por simulación. Estos cambios son cliente y se activan recargando, sin reiniciar servidor ni tocar progreso persistente.

Revisión independiente: CHRONICLE_RENDERER_REVIEW.md. Se corrigió el seguimiento al activar movimiento reducido durante montaje y se añadió «Ir a lo último» sin completar la impresión. Quince comprobaciones adicionales ejecutan las funciones reales del renderer con un DOM/reloj técnico. El seguimiento interno actual es automático; la suavidad visual no está validada en navegador y no se declara aprobada.

Colores reforzados a petición de Javier: entorno verde fósforo, lugar verde brillante, acción cian, rastro/hallazgo/recompensa ámbar, peligro salmón, combate naranja, información secundaria verde apagado y voces lila. Etiquetas del mismo color y líneas laterales ayudan a distinguir bloques sin depender sólo del tono. Los ocho colores de texto superan4.5:1 por cálculo sobre el fondo normal; eso no es una revisión visual en navegador.

## Corrección de repetición y fauna — 2026-10-05

La observación explícita ya no añade otra copia de los detalles presentes en la escena. El renderizador conserva una sola copia textual y proporciona el texto completo mediante la etiqueta accesible del grupo; evita duplicarlo al copiar. La lectura progresiva sigue activa.

Las criaturas presentes ofrecen Examinar con descripción canónica y confirmación del bestiario. Los primeros avistamientos avisan del registro; Evaluar se limita a perfiles de combate existentes. Pinzajunco sigue siendo fauna de observación, sin estadísticas de combate inventadas. Se simplificó el texto nocturno del paso entre los juncos.

Validación: 40 pruebas backend aprobadas, incluida visita real y examen de Pinzajunco sin recompensa ni combate; 15 comprobaciones del diario y 18 del renderizador. La comprobación visual y de lector de pantalla en navegador real queda pendiente. Los cambios Python requieren reiniciar el servidor local; no se detuvo el servidor del usuario.
