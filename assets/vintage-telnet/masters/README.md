# Másters artísticos — Vintage Telnet

Esta carpeta contiene únicamente **fuentes artísticas aprobadas** que deban conservarse para poder regenerar derivados web sin depender del chat original.

## Estructura

- `locations/` — másters aprobados de pueblos, regiones y Vaisgard.
- `species/` — másters aprobados de especies y comparativas.
- `maps/` — másters aprobados de mapas.

Las subcarpetas se crean únicamente cuando exista un archivo real que guardar.

## Regla de nombres

El máster conserva el mismo nombre base que el asset jugable.

Ejemplo:

`assets/vintage-telnet/masters/locations/vaisgard.png`

produce:

`assets/vintage-telnet/locations/vaisgard.webp`

No usar nombres como `final2`, `nuevo-final`, `definitivo3` o equivalentes.

## Qué entra

- únicamente arte aprobado por Dirección de Arte;
- preferentemente PNG para másters raster;
- solo la versión vigente elegida para producir el asset jugable.

## Qué no entra

- bocetos;
- generaciones descartadas;
- versiones intermedias;
- ZIPs de transporte;
- Base64;
- PSD/TIFF u otros archivos muy pesados sin autorización explícita de Arquitectura.

## Consumo del juego

El HTML/cliente **no debe cargar archivos desde `masters/`**.

Los archivos de esta carpeta son fuente artística. El juego consume derivados optimizados publicados mediante el Publicador de Assets en:

- `assets/vintage-telnet/locations/`
- `assets/vintage-telnet/species/`
- `assets/vintage-telnet/maps/`

El canon escrito continúa teniendo autoridad sobre cualquier discrepancia visual.
