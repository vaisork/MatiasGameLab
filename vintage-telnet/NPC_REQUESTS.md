# Vintage Telnet — Estado de solicitudes de NPCs

**Origen:** rescate operativo de PR #53  
**Propósito:** conservar el contexto útil sin reactivar dependencias obsoletas.

## VT-NPC-001 — población mínima inicial

**Estado de Historia:** CERRADO.

Quince perfiles públicos quedan rescatados en `NPCS.md`:
- Valdren: Mara, Oren, Ilya;
- Khariel: Taren, Vael, Isen;
- Brumak: Neki, Tovo, Piri;
- Narevia: Luma, Sela, Orin;
- Velmora: Sair, Mirel, Dovar.

No se exige que los quince estén implementados simultáneamente.

## VT-NPC-PLAYTEST-001 — Taren

La selección de Taren como primer prototipo conversacional fue una decisión de la etapa de #53.

Se conserva su identidad y su diseño de observación antes de conclusión, pero **ya no define la prioridad técnica actual**. El runtime NPC moderno se coordina mediante los issues vigentes de diálogo/memoria/acciones y el trabajo actual con Daro.

## Contrato vigente que sustituye dependencias técnicas antiguas

#53 no debe redefinir:
- proveedor de diálogo;
- memoria conversacional;
- acciones estructuradas;
- persistencia;
- prioridad de implementación.

Esos frentes pertenecen a los contratos técnicos modernos (#245/#246/#247 y sucesores).

## Restricciones persistentes rescatadas

- `hablar <npc>` y chat entre jugadores son intenciones distintas;
- texto generado no muta estado por sí mismo;
- identidad/conocimiento/memoria son autoritativos;
- un NPC puede decir “no sé”;
- una afirmación del jugador no crea un hecho observado;
- ninguna personalidad justifica omnisciencia;
- especie no determina personalidad;
- instituciones nuevas requieren Historia.

## Estado

**RESCATE DE HISTORIA COMPLETO.**

Este archivo ya no funciona como cola. Las colas vigentes viven en GitHub.
