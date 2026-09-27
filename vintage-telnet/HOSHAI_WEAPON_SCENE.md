# Vintage Telnet — HOSHAI-WEAPON-01: microayuda de reconocimiento

**Origen:** #287  
**Responsable:** Narrador  
**Estado:** entrega narrativa lista para Desarrollo

## Propósito
Dar al jugador una forma breve y legítima de ganarse el acceso a una **Hoja de Hoshai** sin tienda, dinero, crafting, requisito de especie/clase ni gran misión.

La escena debe sentirse como una ayuda cotidiana de Khariel: pequeña, concreta y suficiente para que alguien del lugar decida confiarle una pieza física pendiente de Forja.

## Escena: El amarre del paso

En una zona cotidiana de Khariel cercana al tránsito local, un amarre que mantiene despejado un paso de carga se ha soltado. No es una emergencia épica ni una amenaza. Una carga ligera y varios elementos de sujeción ocupan parte del paso y dificultan el tránsito.

Un habitante de Khariel pide una mano para **volver a asegurar el paso**.

### Presentación breve
> Un amarre se ha soltado junto al paso. La carga no ha caído, pero ocupa el lugar por donde normalmente se cruza. Alguien de Khariel intenta mantenerla estable mientras vuelve a ordenar las sujeciones.

### Petición
> —Si vas a quedarte un momento, sujeta desde ahí. Con eso basta para dejar libre el paso.

No exigir conocimiento Felaryn ni capacidad racial. Cualquier personaje puede ayudar.

## Acción estructurada
La escena debe tener un único hito inequívoco para Desarrollo:

`hoshai_paso_ayudado`

Se completa cuando el jugador:
1. acepta ayudar;
2. participa en asegurar la carga/sujeción;
3. deja nuevamente transitable el paso.

No hay puzzle, tirada obligatoria ni combate.

### Resolución
> Entre ambos vuelven a tensar el amarre. La carga queda estable y el paso recupera su espacio. No fue una hazaña, pero alguien tenía que detenerse a hacerlo.

## Reconocimiento y acceso
Después del hito, el jugador recibe una respuesta sobria. Khariel no necesita proclamarlo héroe por una tarea pequeña.

> —Bien. No todos los que pasan se detienen cuando hace falta una mano.

La ayuda permite que el personaje sea recibido con confianza suficiente en el punto de taller definido para la recompensa.

## Entrega de la Hoja de Hoshai
La recompensa ocurre una sola vez por personaje y únicamente después de `hoshai_paso_ayudado`.

Hito de recompensa recomendado:

`hoshai_hoja_recibida`

Texto de entrega:

> Te confían una Hoja de Hoshai todavía pendiente de Forja. Puedes conservarla, pero antes de usarla tendrá que pasar por ese proceso.

No describir bonificaciones ni estadísticas. No equiparla automáticamente. La instancia entra al inventario con `forge_validated=false`, según #287.

Si el jugador vuelve después:
> Ya cumpliste aquí. La pieza que te confiaron sigue siendo la misma; no hay otra esperando por repetir el favor.

## Límites
- No convertir el favor en misión heroica.
- No inventar nueva institución, gremio ni personaje histórico.
- No exigir ser Felaryn.
- No exigir clase.
- No dar una segunda Hoja.
- No validar Forja automáticamente.
- No añadir dinero, tienda o crafting.
- No vincular la recompensa a matar fauna.

## Criterio de implementación
Desarrollo puede implementar la escena donde resulte compatible con el Khariel actual, sin crear geografía nueva si existe una sala cotidiana apropiada.

Estados mínimos persistentes:
- `hoshai_paso_ayudado`
- `hoshai_hoja_recibida`

La segunda marca evita duplicación por conversación repetida, reconexión o revisita.

## Criterio de experiencia
La secuencia completa debe sentirse como una pausa breve dentro del viaje: el jugador ayuda porque está allí, obtiene confianza local y descubre que poseer una buena pieza no significa que ya pueda usarla. La Forja queda como siguiente paso natural.
