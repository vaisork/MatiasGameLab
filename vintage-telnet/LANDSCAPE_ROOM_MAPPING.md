# Mapping narrativo de paisajes aprobados a room_id

Origen: cola #284; arte aprobado #203/#215 y assets publicados por #255/#259.  
Criterio: asignar únicamente a salas cuyo texto y función narrativa corresponden al encargo original del arte. No se crean salas.

## Hoshai — paso alto interior

Asset/contexto: `assets/vintage-telnet/locations/hoshai-paso-alto.webp`

Consumidores:
- `alto_escalones` — desnivel, roca próxima y viento; ya fuera del borde cotidiano.
- `alto_terraza_abandonada` — plataforma de roca gastada dentro del recorrido alto; la imagen no debe convertirla en ruina.
- `alto_garganta` — corredor geológico estrecho, roca lateral próxima y horizonte reducido.
- `alto_cruce_alturas` — trazados alrededor de desnivel que vuelven a encontrarse.

No consumir en `alto_terrazas` ni `alto_mirador`: el encargo no es borde habitado ni panorama.  
No consumir en `alto_puente_viento`: su puente expuesto es un landmark propio y no debe quedar visualmente convertido en el paso geológico genérico.  
No extender después de `alto_pinar`: cambia la lectura de terreno y comienza otra fase del camino.

## Lethra — canal bajo entre islas

Asset/contexto: `assets/vintage-telnet/locations/lethra-canal-bajo-islas.webp`

Consumidores:
- `juncos_agua_entre_caminos` — agua interrumpe el trazado terrestre y obliga a leer pasos.
- `juncos_islas_bajas` — correspondencia directa con islas pequeñas/bajas y múltiples lecturas de paso.
- `juncos_canal_ancho` — tránsito condicionado por canal y recuperación de dirección.

No consumir en `juncos_plataformas`, `juncos_postes` o `juncos_pasarela_antigua`: todavía dominan huellas funcionales de Narevia.  
No consumir en `juncos_pasarela_larga`: la pasarela larga es su landmark principal y el encargo visual solo permite infraestructura mínima.  
No consumir en `juncos_suelo_firme` ni más adelante: el contraste narrativo exige que el canal bajo ya haya quedado atrás.

## Handoff

Integración visual puede enlazar estos room_id al asset/contexto correspondiente. Esta tabla no cambia exits, descripciones, fauna, encuentros ni descubrimientos.
