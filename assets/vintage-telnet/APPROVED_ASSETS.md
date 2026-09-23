# Vintage Telnet — Biblioteca visual aprobada

**Estado:** lote aprobado por Dirección de Arte para publicación técnica.
**Rama de preparación:** `art-director/vintage-approved-visual-library`

Este inventario contiene únicamente las referencias que deben conservarse para la primera presentación visual del juego. No incluye iteraciones descartadas.

## Localizaciones aprobadas

Destino previsto:

- `assets/vintage-telnet/locations/valdren.webp`
- `assets/vintage-telnet/locations/khariel.webp`
- `assets/vintage-telnet/locations/brumak.webp`
- `assets/vintage-telnet/locations/narevia.webp`
- `assets/vintage-telnet/locations/velmora.webp`
- `assets/vintage-telnet/locations/vaisgard.webp`

Estado visual:

- Valdren — APROBADA
- Khariel — APROBADA tras corrección arquitectónica
- Brumak — APROBADA
- Narevia — APROBADA
- Velmora — APROBADA
- Vaisgard — APROBADA

Los textos incidentales, carteles y elementos decorativos de las imágenes no crean canon por sí mismos.

## Especies jugables — láminas individuales aprobadas

Destino previsto:

- `assets/vintage-telnet/species/humano.webp`
- `assets/vintage-telnet/species/felaryn.webp`
- `assets/vintage-telnet/species/dravak.webp`
- `assets/vintage-telnet/species/marevyn.webp`
- `assets/vintage-telnet/species/vesperi.webp`

Estado visual:

- Humano — APROBADA
- Felaryn — APROBADA
- Dravak — APROBADA
- Marevyn — APROBADA
- Vesperi — APROBADA

Estas láminas son referencias visuales iniciales. El canon escrito en `SPECIES.md` y `ART_WORLD_GUIDE.md` conserva autoridad si existe cualquier discrepancia.

## Comparativa de especies

Destino previsto:

- `assets/vintage-telnet/species/comparativa-especies.webp`

Estado: APROBADA como referencia comparativa inicial.

## Mapa

Destino previsto:

- `assets/vintage-telnet/maps/region-inicial.webp`

Estado: base visual aprobada para continuar el sistema de descubrimiento progresivo.

El mapa no debe convertirse por sí solo en fuente de verdad de movimiento ni revelar información no descubierta. La lógica de revelado corresponde a Jugabilidad/Desarrollo.

## Piloto técnico de Vaisgard

Ya existe una salida piloto preparada desde el máster aprobado:

- 1536 × 1024 px
- WebP
- RGB, sin transparencia
- 440,406 bytes
- SHA-256: `4a60f67d065cf47c58a75baa82b1768914cd3bbccb9f5ad41cec26242768fda3`

Este archivo sirve para validar el circuito del Publicador de Assets y no fija todavía el perfil final de toda la biblioteca.

## Orden oficial de publicación

### Lote 1 — piloto obligatorio

Publicar **un solo archivo**:

- `assets/vintage-telnet/locations/vaisgard.webp`

Debe ser exactamente el WebP piloto aprobado:

- 1536 × 1024 px
- 440,406 bytes
- SHA-256: `4a60f67d065cf47c58a75baa82b1768914cd3bbccb9f5ad41cec26242768fda3`

No añadir ninguna otra imagen en este lote.

Objetivo: validar de punta a punta el flujo real

`Arte → Publicador de Assets → rama/PR → validación → repo → interfaz`

Si este lote falla, no avanzar con la biblioteca completa hasta corregir el problema.

### Lote 2 — biblioteca aprobada restante

Solo después de que el piloto de Vaisgard quede validado, publicar estos **12 archivos**:

#### Localizaciones

- `assets/vintage-telnet/locations/valdren.webp`
- `assets/vintage-telnet/locations/khariel.webp`
- `assets/vintage-telnet/locations/brumak.webp`
- `assets/vintage-telnet/locations/narevia.webp`
- `assets/vintage-telnet/locations/velmora.webp`

#### Especies

- `assets/vintage-telnet/species/humano.webp`
- `assets/vintage-telnet/species/felaryn.webp`
- `assets/vintage-telnet/species/dravak.webp`
- `assets/vintage-telnet/species/marevyn.webp`
- `assets/vintage-telnet/species/vesperi.webp`
- `assets/vintage-telnet/species/comparativa-especies.webp`

#### Mapa

- `assets/vintage-telnet/maps/region-inicial.webp`

No incluir:
- iteraciones anteriores;
- bocetos;
- versiones descartadas de Khariel o Vaisgard;
- primeras filminas sustituidas por las corregidas;
- ZIPs como formato final;
- imágenes Base64 embebidas.

## Másters artísticos

Los másters originales no forman parte automáticamente del lote jugable.

Para esta fase:
- el juego consume derivados WebP optimizados;
- conservar PNG/otros másters en GitHub será una política separada si Arquitectura la considera necesaria;
- no duplicar archivos pesados sin una decisión explícita.

## Regla de publicación

No publicar versiones descartadas o intermedias.

El lote técnico final debe seguir el flujo:

`arte aprobado → conversión/validación → Publicador de Assets → repo → interfaz`

El publicador debe resolver nombres, formato, dimensiones/peso y publicación sin pedir a Javier que transporte imágenes una por una.

## Siguiente arte

Dirección de Arte da por suficiente, para esta fase, la producción de:

- especies jugables;
- cinco pueblos;
- Vaisgard;
- mapa regional.

La siguiente producción visual significativa puede concentrarse en una tanda pequeña de criaturas/monstruos iniciales, evitando crear una biblioteca innecesariamente grande antes del primer juego real.
