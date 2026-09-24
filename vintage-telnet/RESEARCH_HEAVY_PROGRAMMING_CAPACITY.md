# Investigación — capacidad de programación pesada y automatización Raspberry

**Fecha:** 2026-09-24  
**Responsable:** Investigador Técnico y de Implementación — Vintage Telnet  
**Estado:** INVESTIGADO; NO IMPLEMENTADO / NO AUTORIZADO A CONECTAR SERVICIOS

## Problema
Codex está temporalmente fuera de circulación, Claude/Cloud disponible pero su cuota se consume rápido, y los Programadores Junior 1/2 están entrando en bucles ante tareas complejas. Se necesita:
1. reducir el uso de IA fuerte en operaciones repetitivas de Raspberry;
2. disponer de capacidad real para programación pesada sin depender de un único proveedor;
3. decidir si conservar Google AI Pro o trasladar gasto a ChatGPT/Claude.

## Hallazgo 1 — Raspberry no debe consumir un programador fuerte para operaciones mecánicas
Separar:
- **decisión/diagnóstico**: IA;
- **ejecución repetible**: scripts + GitHub Actions.

Candidatos deterministas: fetch/checkout de SHA autorizado, backup, instalación controlada de dependencias, tests, migraciones seguras, restart, healthcheck, lectura acotada de logs y rollback.

GitHub Actions soporta workflows por push/PR/manual (`workflow_dispatch`), environments, protección/aprobación y self-hosted runners. Propuesta: un carril de despliegue explícito con aprobación, no un agente IA escribiendo comandos distintos cada vez.

No instalar un runner ni abrir Raspberry a Internet sin diseño de seguridad. Arquitectura/Ops debe decidir entre runner autohospedado y un mecanismo pull más restringido. Mantener secretos fuera de repo y privilegios mínimos.

## Hallazgo 2 — NO cancelar Google AI Pro todavía
En 2026 el antiguo acceso consumidor Gemini Code Assist/CLI fue retirado y migrado hacia la familia Antigravity. Google AI Pro actualmente incluye herramientas muy relevantes:

### Jules
- agente de programación asíncrono integrado con GitHub;
- lee `AGENTS.md`;
- clona repo en VM;
- planifica, modifica, prueba y puede publicar rama/PR;
- un issue puede activar trabajo aplicando label `jules`;
- AI Pro anuncia hasta 100 tareas/día y 15 concurrentes;
- usuarios Pro tienen Gemini 3.1 Pro como modelo disponible/default actual para trabajo complejo;
- CI Fixer puede corregir fallos de CI de PR creadas por Jules.

Esto encaja directamente con Dispatcher: Arquitecto prepara issue -> label `jules` -> Jules trabaja -> PR -> Integrador revisa.

### Antigravity
Google AI Pro incluye acceso mejorado a Antigravity: entorno de desarrollo agéntico para planear, ejecutar y verificar tareas complejas sobre editor/terminal/navegador, con cuotas mayores y posibilidad de comprar puntos de IA adicionales.

### Seguridad
Si se prueba Jules, autorizar **solo** `vaisork/MatiasGameLab`, no todos los repositorios. No entregar secretos de Raspberry. Jules trabaja en VM cloud y debe seguir rama/PR; no darle autoridad de merge ni producción.

## Hallazgo 3 — alternativas pagadas

### GitHub Copilot
Muy alineado porque ya trabajamos en GitHub.
- Pro: USD 10/mes, cloud agent + review + selección de modelos.
- Pro+: USD 39/mes, modelos premium (incluido Opus según GitHub) y 7,000 AI credits/mes publicados.
- Max: USD 100/mes, orientado a alto volumen y 20,000 AI credits/mes publicados.
Puede ser un segundo proveedor/agente sin cambiar fuente de verdad.

**Uso recomendado:** candidato de segundo nivel si Jules no resuelve la carga; no contratar antes de probar lo ya pagado.

### Cursor
- Pro USD 20;
- Pro+ USD 60;
- Ultra USD 200;
- agentes cloud y acceso a modelos de frontera.
Es potente, pero agrega otra superficie/IDE y otra facturación. Para MatiasGameLab aporta menos ventaja estructural que Jules/Copilot, que se integran directamente con GitHub.

**Uso recomendado:** no prioritario ahora.

### Claude
Claude Code sigue siendo una opción fuerte para tareas complejas.
- Max 5x: USD 100/mes;
- Max 20x: USD 200/mes;
- créditos de uso permiten continuar con pago por consumo al alcanzar límites.
Como Claude ya demostró utilidad en este proyecto, aumentar capacidad puede ser razonable **solo después de sacar de Claude las tareas mecánicas y medir el consumo restante**.

### ChatGPT
Plus: USD 20/mes. Pro actual tiene niveles superiores; OpenAI documenta Pro USD 100 con 5x la asignación de Plus y Pro USD 200 con 20x, aunque nuevas altas/cambios al nivel USD 200 están temporalmente pausados al 2026-09-24. Codex/Work y otras funciones agénticas pueden compartir asignaciones/créditos según plan.

**Riesgo:** concentrar programación, Work, investigación y coordinación en el mismo pool vuelve a crear un único punto de agotamiento.

## Recomendación
No comprar/cancelar hoy. Orden recomendado:

1. **Automatizar Raspberry** para dejar de gastar IA en ejecución repetitiva.
2. **Probar Jules**, ya incluido en Google AI Pro, como Programador Pesado GitHub.
3. **Probar Antigravity** para tareas pesadas interactivas cuando haga falta.
4. Mantener Junior 1/2 solo para cambios pequeños, acotados y verificables; si repiten intento/fallo, escalar en vez de entrar en bucle.
5. Mantener Claude como especialista fuerte mientras haya cuota.
6. Después de 5–7 días medir: tareas completadas, reintentos, PR aceptables, consumo y tiempo de Javier.
7. Si falta capacidad:
   - primera compra candidata: GitHub Copilot Pro+ (USD 39) por integración/coste;
   - si Claude sigue siendo claramente el mejor ejecutor para este repo: subir Claude a Max 5x o habilitar créditos;
   - subir ChatGPT a Pro si el cuello real es simultáneamente Work/Codex/razonamiento dentro de ChatGPT, no solo programación.
8. Cancelar Google AI Pro solo si Jules + Antigravity fallan la prueba real o no aportan valor suficiente.

## Regla de escalamiento para Juniors
Propuesta para Arquitectura:
- Junior intenta una tarea acotada.
- Si falla por la misma causa dos veces, **STOP**.
- Documenta: objetivo, HEAD, archivos, prueba, error, intentos.
- Cambia estado a `NEEDS_HEAVY_PROGRAMMER`.
- No seguir regenerando parches.
- Programador pesado consume ese paquete y trabaja en rama.
- Integrador conserva gate final.

## Piloto recomendado
Sin conectar nada todavía:
1. Arquitectura selecciona **un issue real, no crítico y suficientemente complejo** que Junior no haya podido cerrar.
2. Javier autoriza acceso de Jules únicamente a `vaisork/MatiasGameLab`.
3. Jules recibe issue vía label `jules`.
4. Exigir rama/PR + tests; sin merge.
5. Comparar con resultado del Junior/Claude: calidad, número de ciclos, tiempo, tests y consumo humano.
6. Solo después decidir si Jules entra al Dispatcher estable.

## Fuentes consultadas
Documentación oficial de GitHub Actions/Environments/Self-hosted runners; GitHub Copilot plans/billing; Google AI Pro, Jules, Antigravity y deprecación de Gemini Code Assist consumidor; Anthropic Claude plans/usage credits; OpenAI ChatGPT/Codex plans and usage; Cursor pricing.
