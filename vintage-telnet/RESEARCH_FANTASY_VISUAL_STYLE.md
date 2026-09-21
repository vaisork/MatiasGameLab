# Investigación visual — Estética fantasy tabletop para Vintage Telnet

**Fecha:** 2026-09-21  
**Estado:** INVESTIGADO — GUÍA PARA ITERACIÓN VISUAL, NO IMPLEMENTADA  
**Solicitante:** Javier  
**Consumidor:** Desarrollador Junior de Vintage Telnet  
**Decisión conservada:** la terminal Telnet negra con verde gusta y debe permanecer claramente diferenciada.

## PREGUNTA

El fondo/carcasa café actual no convence. ¿Qué lenguaje visual resulta familiar y atractivo en el ecosistema contemporáneo de Dungeons & Dragons, VTTs y RPG de fantasía, y cómo puede Vintage Telnet aprovecharlo sin copiar una marca ni convertirse en un juego gráfico convencional?

## ACLARACIÓN IMPORTANTE

No existe evidencia de que “todos los jugadores de D&D prefieran un color”. El propio ecosistema permite personalización: D&D Beyond ofrece temas/decoraciones y ventanas oscuras (“Underdark mode”), y Roll20 incorporó Dark Mode después de que fuera una petición muy votada.

Por tanto, la conclusión útil no es “a los jugadores de D&D les gusta X color”, sino identificar **patrones visuales recurrentes** en herramientas modernas de fantasy tabletop.

## PATRONES OBSERVADOS

### 1. Superficies oscuras y neutras funcionan muy bien como infraestructura

D&D Beyond Maps, Roll20 en dark mode y muchas interfaces de Foundry VTT usan fondos carbón, gris muy oscuro o negro para las herramientas que rodean el contenido.

Esto consigue:
- que mapas/arte destaquen;
- reducir ruido visual;
- crear sensación de mesa nocturna/pantalla de juego;
- permitir acentos de color sin saturar;
- mantener buena legibilidad durante sesiones largas.

### 2. La fantasía no depende de pintar todo como pergamino

La identidad fantasy suele aparecer mediante:
- marcos;
- filetes/bordes;
- iconos;
- heráldica;
- textura muy contenida;
- tipografía de títulos;
- mapas;
- retratos;
- dados;
- pequeños acentos metálicos.

Una gran superficie marrón no es requisito. Puede producir una sensación más “taberna/pergamino” que “aventura fantástica” y competir con la terminal.

### 3. Los acentos cálidos se usan mejor con moderación

Oro viejo, bronce, cobre, rojo oscuro o marfil aparecen bien como:
- borde activo;
- título;
- selección;
- icono;
- botón importante;
- separador.

Funcionan peor cuando todos los paneles, fondos y botones son simultáneamente marrones/dorados.

### 4. Dark mode es parte real del lenguaje actual de juego

Roll20 llevó dark mode al VTT y a la hoja D&D 5e. D&D Beyond permite personalizar apariencia y usar ventanas oscuras. Interfaces fantasy de Foundry también exploran temas oscuros ornamentados.

Esto respalda una carcasa oscura para Vintage Telnet sin perder la asociación con fantasy tabletop.

## DIRECCIÓN RECOMENDADA PARA VINTAGE TELNET

### Concepto: “terminal arcana dentro de una consola de aventurero”

No hacer “pergamino alrededor de Telnet”.

Hacer una interfaz de fantasía oscura, sobria y moderna que parezca una herramienta de explorador/Dungeon Master, y dentro colocar la terminal retro como objeto visual claramente distinto.

### Paleta propuesta A — Pizarra + metal antiguo + terminal verde

**Recomendada para primera prueba.**

Carcasa:
- fondo profundo: `#101416` — carbón azulado;
- panel: `#181E21` — pizarra;
- panel elevado: `#222A2E`;
- borde: `#465158` — acero apagado;
- texto principal: `#E7E1D5` — marfil suave;
- texto secundario: `#A8B0AD`;
- acento metálico: `#C39A58` — oro/bronce viejo;
- acento secundario opcional: `#7F3940` — vino oscuro, solo para peligro/acción importante.

Terminal:
- fondo: `#020604`;
- verde principal: `#8CFF9B`;
- verde secundario: `#56B967`;
- verde apagado: `#769C7C`;
- borde terminal: `#2D6840`.

**Sensación:** fantasía oscura + herramienta de aventura + computadora antigua. Separa muy bien exterior e interior sin recurrir al café dominante.

### Paleta propuesta B — Medianoche + plata + violeta arcano

Carcasa:
- `#0E1018`;
- `#171B27`;
- `#252B39`;
- texto `#E8E5DF`;
- plata `#9AA6B2`;
- violeta arcano `#7667A8`;
- oro tenue `#B99A62`.

Terminal mantiene negro/verde.

**Sensación:** más magia/arcano y menos medieval rústico. Buena candidata futura si Javier quiere que Vintage Telnet se sienta misterioso.

### Paleta propuesta C — Hierro + marfil + rojo profundo

Carcasa:
- `#111213`;
- `#1C1D1F`;
- `#292A2D`;
- marfil `#E5DED0`;
- acero `#777D82`;
- rojo profundo `#7A3034`;
- oro viejo `#B58D50`.

Terminal negro/verde.

**Sensación:** más dungeon, combate y peligro. Debe cuidarse para no acercarse demasiado a identidades visuales de marcas existentes.

## RECOMENDACIÓN ENTRE LAS TRES

Probar primero **Paleta A — Pizarra + metal antiguo + terminal verde**.

Razones:
1. elimina el café dominante que Javier no disfruta;
2. conserva calidez fantasy mediante bronce/oro viejo;
3. no compite con el verde de terminal;
4. da suficiente separación entre carcasa y Telnet;
5. funciona con mapas, retratos y futuros iconos;
6. tiene identidad propia sin copiar el rojo/negro de D&D;
7. debería funcionar bien en teléfono con poco espacio porque no necesita texturas grandes para comunicar jerarquía.

## REGLA 70/20/10 COMO PUNTO DE PARTIDA

No es una ley de diseño, sino una guía práctica para evitar saturación:

- ~70% superficies oscuras neutras;
- ~20% superficies/contornos secundarios;
- ~10% acentos (bronce, estado, selección).

El verde de terminal se trata como un sistema propio dentro de su pantalla y no como color general de todos los botones HTML.

## QUÉ HACER CON EL CAFÉ

No eliminar necesariamente toda referencia cálida.

Mover el café/madera desde **“fondo dominante”** hacia **“detalle material”**:
- pequeñas líneas bronce;
- iconos;
- marcos;
- una textura apenas perceptible;
- títulos o separadores;
- quizá elementos concretos del mapa/inventario.

Así conservamos sensación artesanal/fantasy sin bañar toda la aplicación en marrón.

## TIPOGRAFÍA

### Exterior HTML
Para títulos se puede usar una serif de aire editorial/fantasy, pero debe seguir siendo muy legible. El cuerpo y botones pueden usar una sans limpia.

No usar tipografías “medievales” ornamentadas en texto funcional; en teléfono pierden claridad.

### Terminal
Monoespaciada inequívoca:
`ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.

La tipografía es tan importante como el color para marcar la frontera entre cliente fantasy y Telnet.

## MATERIALES Y TEXTURAS

### Sí
- metal oscuro;
- piedra/pizarra;
- cuero únicamente como pequeño detalle;
- oro/bronce envejecido;
- grabados finos;
- esquinas/marcos discretos.

### No como superficie dominante
- pergamino amarillo;
- madera café en todos los paneles;
- cuero marrón en toda la UI;
- gradientes dorados brillantes;
- texturas fotográficas pesadas.

En móvil, la “fantasía” debe sobrevivir incluso si quitamos casi todas las texturas. La estructura, tipografía, bordes e iconografía deben cargar la identidad.

## ESTADOS DE INTERACCIÓN

Usar color con significado consistente:

- **normal:** pizarra/acero;
- **hover/focus/selección:** bronce/oro viejo;
- **acción primaria:** acento cálido controlado;
- **peligro:** vino/rojo apagado;
- **éxito/terminal:** no reutilizar el verde Telnet indiscriminadamente fuera de terminal;
- **deshabilitado:** gris pizarra, pero con suficiente contraste.

Esto preserva el verde como firma de “estoy dentro de Telnet”.

## TERMINAL COMO PIEZA HERO

La terminal debería ser el elemento de mayor contraste del juego:
- negro casi absoluto;
- verde luminoso;
- marco oscuro/metal;
- quizá un pequeño indicador de conexión;
- sin grandes decoraciones café alrededor.

El resultado buscado es que el ojo piense:
**“esta es una interfaz de fantasía; esa pantalla verde es el portal al mundo Telnet”.**

## REFERENCIAS CONTEMPORÁNEAS

### D&D Beyond
La hoja digital permite personalizar Theme, Backdrop y Frames, además de ventanas oscuras mediante Underdark mode. Maps usa una interfaz oscura y funcional alrededor de mapas y tokens coloridos.

### Roll20
Dark Mode fue una petición muy votada y se extendió al VTT y a hojas como D&D 5e. La hoja D&D moderna usa fondos muy oscuros, texto claro y acentos limitados.

### Foundry VTT
Su ecosistema incluye temas “Fantasy UI” y “Fantasy RPG UI”, demostrando interés en aplicar lenguaje fantasy a una base oscura sin depender únicamente de pergamino.

## INSTRUCCIONES PARA EL DESARROLLADOR JUNIOR

Esta guía complementa `RESEARCH_MOBILE_TELNET_UI.md`.

Para la siguiente iteración visual:

1. **Conservar terminal negra/verde.**
2. Reemplazar el café dominante exterior por la **Paleta A** como primera propuesta.
3. Mantener bronce/oro viejo solo como acento y borde.
4. Mantener marfil para texto exterior, no verde.
5. Hacer que mapa/personaje/inventario pertenezcan visualmente a la carcasa pizarra/metal.
6. No teñir botones HTML de verde salvo que formen parte de la terminal.
7. Mantener peligro con rojo/vino discreto.
8. Reducir gradientes marrones existentes.
9. Evitar texturas pesadas; primero resolver jerarquía con colores planos, borde, sombra y tipografía.
10. No copiar logotipos, iconos, composición exacta ni rojo de marca de D&D/Roll20/Foundry.
11. Preparar la iteración para que Javier compare visualmente **actual café vs propuesta pizarra/metal**, conservando el mismo contenido y comportamiento. El objetivo es evaluar estética, no introducir nuevas mecánicas.

## PRUEBA VISUAL PROPUESTA

Antes de pulir toda la interfaz, modificar únicamente variables CSS y superficies principales para obtener una prueba A/B:

**A — actual café**  
vs  
**B — pizarra/metal + bronce + terminal negro/verde**

Javier y Matías deberían observar ambas en el mismo teléfono y responder:
- ¿cuál hace que la terminal destaque mejor?;
- ¿cuál parece más aventura/fantasía y menos “sitio web café”?;
- ¿cuál cansa menos después de varios minutos?;
- ¿en cuál se entiende mejor qué es juego y qué es herramienta?;
- ¿el bronce aporta fantasía suficiente sin llenar la pantalla de marrón?

Solo después conviene añadir ornamentación.

## FUENTES

- D&D Beyond — Character Header / personalización de Theme, Backdrop, Frames y Underdark mode: https://dndbeyond-support.wizards.com/hc/en-us/articles/7747193980820-Character-Header
- D&D Beyond — Official Character Builder/Sheet y personalización de color themes: https://www.dndbeyond.com/en/players
- D&D Beyond — Maps VTT: https://www.dndbeyond.com/posts/1816-the-official-d-d-vtt-navigating-maps-on-d-d-beyond
- Roll20 — Character Sheets in Dark Mode: https://blog.roll20.net/posts/roll20-character-sheets-in-dark-mode/
- Roll20 — New D&D Character Sheet: https://blog.roll20.net/posts/introducing-the-new-roll20-dungeons-dragons-character-sheet/
- Foundry VTT — Fantasy UI: https://foundryvtt.com/packages/fantasy-ui
- Foundry VTT — Fantasy RPG UI: https://foundryvtt.com/packages/fantasy-rpg-ui

## CONCLUSIÓN

Vintage Telnet no necesita una carcasa café para comunicar “fantasía”.

Una dirección más cercana a muchas interfaces actuales de fantasy tabletop es **oscura, neutral y modular**, dejando que la fantasía aparezca en detalles de metal, marcos, tipografía, iconos y arte. Para nuestro juego, esto además resuelve una oportunidad única: el exterior puede sentirse como una herramienta de aventurero moderna, mientras el negro/verde de la terminal conserva toda la personalidad retro.

La primera variante que merece probarse es:

**Pizarra/carbón + acero + bronce viejo + marfil**  
rodeando una  
**terminal negro + verde fósforo**.
