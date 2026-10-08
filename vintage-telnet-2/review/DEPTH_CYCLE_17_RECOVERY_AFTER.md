# C17 — descanso y recuperación después de la corrección

Mismo recorrido HTTP real en DB temporal nueva: 96 movimientos y 122 acciones/registros. Dos personajes naturales de nivel1 sin editar HP, flags, inventario o dinero. Felaryn Sombra muere ante Cornalomo, recupera en Brumak a seis tramos, conserva inventario/sellos/progreso y no fabrica una ruta. Arcano vence al forajido del canal, devuelve la caja, usa provisión y vende semillas antes de volver al hogar.

Antes: descanso60→70→72→72; fatiga40→15→0→0. La tercera acción seguía activa y prometía aflojar fatiga. Después: mismos HP/fatiga, pero tercera acción deshabilitada con explicación de margen agotado y alternativas provisión/cuidados; intento API409 sin alterar personaje, inventario o mapa. Los cuidados siguen costando18 y recuperan a90HP; descanso posterior conserva el margen existente y vuelve a93HP. El personaje puede regresar andando y evitar el peligro. No cambia ninguna cifra ni saldo.

Comparación root: personaje e inventario finales idénticos en ambos casos, incluyendo HP/fatiga/XP/atributos/equipo/sellos. La diferencia deliberada es disponibilidad de acciones sin efecto y claridad. Previsión de descanso reutiliza m.rest sobre copia superficial numérica; no escribe estado al leer acciones. Resultado sólo enumera cambios reales y explica el margen agotado. No se afirma cura completa ni un balance nuevo.

La subtarea alcanzó límite de uso después del BEFORE y preparar el arnés AFTER; root completó el replay. Primer intento HTTP arrancó antes de que el servidor temporal escuchara; terminó sin crear cuentas. Se confirmó mismo proceso vivo/HTTP200 y se ejecutó el arnés, sin reiniciar por un timeout. Evidencia depth-cycle17-recovery-after.json.

Autocrítica: recuperación/margen claros y sin softlock observado; el traslado sigue abstracto y esta sesión no prueba todos los superiores, heridas u horarios. No se valoran como bugs la retirada correcta ni el coste18 canónico. El límite gratuito se conserva: usar provisión no reinicia el presupuesto de descanso.
