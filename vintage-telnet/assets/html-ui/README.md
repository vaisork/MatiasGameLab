# Vintage Telnet — HTML UI Assets

Esta carpeta contiene la primera biblioteca modular de arte para la **carcasa HTML exterior** de Vintage Telnet.

## Principio

La terminal sigue siendo **negro + verde fósforo** y continúa como protagonista. Estos recursos pertenecen al exterior HTML: herramientas, navegación, marcos y ambiente.

La dirección de esta primera familia fue ajustada por Javier para ser:
- más juvenil y amigable para niños;
- menos cargada;
- pensada primero para teléfono;
- fantasy/aventura sin caer en un aspecto medieval pesado.

## Estructura

```
html-ui/
├── buttons/
├── ornaments/
├── dividers/
├── backgrounds/
└── previews/
```

## Uso

- Consumir los **assets individuales** desde HTML/CSS.
- No usar la imagen de `previews/` como fondo de toda la aplicación.
- Mantener targets táctiles y texto legible; el PNG no sustituye el elemento HTML accesible.
- El botón **Poderes** es una categoría visual para futuras magias/habilidades; no establece qué poderes existen.
- Para efectos sencillos (sombra, borde, estados hover/focus), preferir CSS cuando sea suficiente.
- Si una integración requiere un tamaño o estado nuevo, Arte HTML debe producir la variante en vez de deformar excesivamente el asset.

## Primera entrega

Ver `ASSET_MANIFEST.md` para rutas, dimensiones y recomendaciones.
