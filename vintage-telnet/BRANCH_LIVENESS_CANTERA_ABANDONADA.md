# WORLD-LIVENESS — Cantera Abandonada superficial

Origen: #558 / ramal superficial CA-01..CA-09.

Objetivo: añadir señales ambientales breves a las 9 salas existentes de Cantera Abandonada sin fijar encuentros, criaturas, loot ni interior.

| room_id | micro-presencia |
| --- | --- |
| `ca_01_desvio_descarte` | “El viento mueve polvo fino entre montones de piedra y deja al descubierto fragmentos más claros.” |
| `ca_02_patio_grava` | “La grava conserva surcos irregulares que el viento borra poco a poco.” |
| `ca_03_plataforma_baja` | “Una esquina de la plataforma está más limpia, como si alguien hubiera apartado piedras para sentarse o apoyar carga.” |
| `ca_04_montones_descarte` | “Pequeños fragmentos ruedan desde un montón y se detienen contra bloques más grandes.” |
| `ca_05_zanja_seca` | “La zanja acumula hojas secas y polvo en los puntos donde ya no corre agua.” |
| `ca_06_plataforma_alta` | “Desde arriba se distingue polvo suspendido sobre el frente de extracción cuando cambia el viento.” |
| `ca_07_frente_quebrado` | “Una pequeña placa de roca se desprendió recientemente y dejó una superficie más clara.” |
| `ca_08_paso_bloques` | “El aire cambia de temperatura al cruzar entre los bloques y el sonido del exterior se vuelve más corto.” |
| `ca_09_cavidad_tras_frente` | “La abertura devuelve menos viento que el exterior y mantiene una sombra más estable entre los bloques.” |

## Reglas

- no fijar presencia de Rompecuña ni otra criatura;
- no convertir polvo, grietas o desprendimientos en derrumbe mecánico;
- no crear minería, crafting ni recurso extraíble;
- no revelar el interior posterior;
- encounter/scripted tiene prioridad;
- clima/daypart puede sustituir la línea.

## Handoff

LISTO PARA INTEGRACIÓN: SÍ.