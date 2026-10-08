# Herramientas y rutas compatibles

El portal `index.html` y `matiasgamelab.webmanifest` pertenece a MatiasGameLab. Los iconos del portal son compartidos; los assets de cada juego no.

| Ruta preservada | Propietario | Condición |
|---|---|---|
| `tools/publish-assets.py`, `tests/asset_publisher/` | publicación de assets VT1 | No reutilizar en VT2 sin adaptar contrato/rutas. |
| `tools/vt_art/` | pipeline VT1 | Conservado; no fuente operativa de VT2. |
| `scripts/validate-vintage-content.py` | VT1 | Valida catálogo antiguo, no VT2. |
| `generate_all_art.py`, `generar-arte`, `launcher.sh`, `run-art-generator.sh` | pipeline VT1 | Compatibilidad de accesos Ubuntu/Raspberry; no ejecutar durante reorganización. |
| `assets/vintage-telnet/`, `art-masters/` | VT1 | Preservados para rollback y arte recuperable. |
| `assets/senku/`, `backgrounds/`, `perro/`, `rata/`, `trajes/`, `asset-map.json` | Senku legacy | URLs históricas; nunca contexto para VT2. |
| `assets/icon/` | portal + iconos de juegos | Compartido sólo por presentación del portal. |

Senku v2 y VT2 no dependen de herramientas VT1. VT2 usa `client/art/`, `client/models/`, `scripts/`, `ops/` y `tests/` propios.
