# MatiasGameLab — Solicitudes de Pixel Art

Esta es la cola común para recursos visuales jugables que todavía necesitan trabajo de Pixel Art.

Antes de añadir una solicitud, revisar `assets/` y las solicitudes existentes para evitar duplicados. Las reglas completas están en `AGENTS.md`.

## Cómo solicitar un recurso

Copiar esta plantilla al final del documento:

```
### [ID o nombre breve] — [recurso]

Juego:
[Senku / Vintage Telnet / otro]

Solicitado por:
[agente o función]

Estado:
SOLICITADO

Objetivo en el juego:
[para qué se necesita]

Recurso:
[personaje / NPC / enemigo / objeto / fondo / traje / icono / animación / otro]

Requisitos conocidos:
- Tamaño o escala:
- Formato:
- Transparencia:
- Frames/poses:
- Dirección/orientación:
- Referencias existentes:
- Ruta relacionada en assets:

Decisiones visuales ya aprobadas:
[solo decisiones realmente aprobadas]

Necesita material de Javier/Matías:
[Sí / No / Por determinar]

Entrega:
- Ruta final:
- Dimensiones:
- Formato:
- Frames/orden:

Observaciones:
[dependencias, dudas o contexto]
```

## Reglas de estado

- **SOLICITADO** — esperando revisión de Pixel Art.
- **PENDIENTE DE JAVIER/MATÍAS** — Pixel Art debe pedir directamente el material o decisión que falta.
- **EN ARTE** — recurso en preparación.
- **LISTO EN ASSETS** — archivo subido; la solicitud debe incluir la ruta exacta.
- **BLOQUEADO** — indicar qué dependencia bloquea.
- **CANCELADO** — indicar brevemente por qué.

## Solicitudes activas

Actualmente no hay solicitudes registradas en esta cola.

## Diagnóstico temporal — flujo de subida de Pixel Art

Solicitado por:
Investigador Técnico y de Implementación — Senku

En la **próxima entrega real de Pixel Art**, antes de cambiar el procedimiento actual, documentar brevemente cómo se está haciendo hoy la subida al repositorio y dónde se consume más tiempo.

Responder al terminar esa próxima subida:

1. ¿Cuántos archivos se subieron en esa entrega?
2. ¿Los PNG se reciben uno por uno, en lote, carpeta o ZIP?
3. ¿Qué pasos manuales se realizan desde que Javier entrega la imagen hasta que queda en `assets/`?
4. ¿Se recorta, transparenta, redimensiona o renombra cada imagen individualmente?
5. ¿Cómo se suben actualmente a GitHub: un archivo/commit por vez, varios archivos en un solo commit, u otro método?
6. ¿Qué paso concreto tarda más?
7. ¿Hay esperas debidas al chat/herramienta, procesamiento de imagen, descarga/subida de archivos, validación o GitHub?
8. Aproximadamente, ¿qué parte del proceso podría hacerse por lote sin perder la validación visual?
9. Si hubo algún error, límite de herramienta o motivo por el que no pudo hacerse en lote, indicarlo exactamente.

**Importante:** esta petición es de diagnóstico. En esa próxima entrega no hace falta cambiar el flujo ni experimentar con una nueva automatización salvo que Javier lo pida. Primero necesitamos medir el proceso real.

Una vez respondido este diagnóstico, el Investigador Técnico podrá proponer una mejora concreta para reducir el tiempo de subida sin comprometer nombres, transparencia, orden de frames ni rutas existentes.

