# Mapa ilustrado con niebla (prueba local)

El candidato v2 del agente de arte **no está aprobado**: algunos ramales menores no calzan del todo y la imagen viene ampliada desde 1145 × 1374. Se usa como prueba, por decisión de Javier: con caminos y con niebla.

- `client/art/map/mundo-anime-v1.webp`: 2400 × 2880 (1,44 MB), reducida desde el PNG de 7000 × 8400. Al estar ampliado desde 1145 px, no se pierde detalle; decodificada ocupa unos 28 MB en lugar de 235.
- **Mapa:** con fondo, las casillas pasan a ser cuadradas (210 × 210) para no deformar el dibujo. El fondo se coloca con las mismas posiciones del atlas.
- **Niebla:** una máscara de degradados radiales sólo deja ver el dibujo alrededor de los lugares que el personaje ya descubrió.
- **Servidor:** se permite servir `art/map/`.
