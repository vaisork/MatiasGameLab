# DEATH-PRESENTATION-01 — texto narrativo de muerte y reaparición

Origen: #366. Responsable: Narrador. No cambia reglas de muerte, respawn ni penalizaciones.

## Secuencia v1

1. El relato normal conserva el último golpe que llevó HP a 0.

2. Encabezado inequívoco y separado del log:

**HAS MUERTO**

3. Caída, texto base:

> Las fuerzas te abandonan. El combate desaparece a tu alrededor y pierdes la conciencia.

Variantes breves permitidas:
- Ya no puedes mantenerte en pie. Todo se apaga por un momento.
- El cuerpo deja de responder. Lo último que percibes del combate se pierde en la oscuridad.

No describir cadáver, mutilación, alma, resurrección ni causa sobrenatural.

4. Transición visual clara. Backend puede resolver muerte y respawn en la misma acción; no crear un estado intermedio persistente ni botón obligatorio.

5. Reaparición:

> Vuelves en ti en un lugar seguro.

Cuando el servidor conozca el nombre:

> Vuelves en ti en {nombre_del_lugar}.

No fijar Valdren en el texto genérico.

6. Estado posterior:

**Estado al volver**
- Salud: {hp_actual}
- Fatiga: {fatiga_actual}
- Herida: {herida_actual}
- Equipo: {estado_equipo}
- Inventario: {estado_inventario}

Si el contrato aplicable indica conservación:
> Conservas tu equipo e inventario.

No afirmar conservación si una futura regla de muerte aplica otra consecuencia.

## Reglas UX

- HAS MUERTO nunca queda enterrado en una frase larga.
- Muerte aparece antes que reaparición aunque ambas ocurran en una respuesta.
- Debe funcionar si la muerte ocurre atacando, huyendo o en otra resolución.
- Refrescar/reconectar no repite indefinidamente una muerte consumida.
- No requiere imagen, animación ni sonido.
- El contrato base no depende de Cornalomo.

## Handoff UI / Desarrollo

Preferir datos estructurados: outcome defeat, evento de muerte, evento de respawn y estado posterior. La UI presenta el bloque diferenciado y luego la sala segura. No debe inferir muerte buscando palabras en el log.

## Prueba humana

Pasa si Javier provoca una muerte y distingue sin duda:
1. que murió;
2. que después reapareció;
3. dónde reapareció;
4. en qué estado quedó.

No modifica pérdida de arma, punto de respawn, HP, fatiga, heridas ni otras consecuencias mecánicas.
