# Matemáticas históricas: modelos didácticos y validación

**Advertencia:** las ecuaciones aquí son **modelos explicativos independientes**, no transcripciones ni afirmaciones de identidad exacta con código Merc/ROM. Para reproducir un algoritmo histórico, inspeccionar la función concreta y verificar excepciones, límites y modificadores.

## Dados de daño
- Notación `NdS+B`: sumar `N` dados uniformes entre 1 y `S`, luego `B`.
- Ejemplo `2d6+1`: mínimo 3, máximo 13, promedio 8 (porque E[d6]=3.5).
- **Cuidado:** daño final puede incluir fuerza, habilidades, armadura, resistencias, golpes críticos, estados y mínimos.

## THAC0 / AC: modelo didáctico
- `d20 >= THAC0 - AC` para el caso básico, con menor AC = mejor protección.
- Ejemplo: THAC0 15, AC 5 => se necesita 10+ en d20; 11 caras de 20 = 55% de éxito **en este modelo simplificado**.
- Ejemplo: THAC0 15, AC -2 => se necesita 17+; 4 caras de 20 = 20%.
- **No usar como implementación literal sin verificar:** cada motor añade hitroll, efectos, reglas de 1/20 y escalas AC internas (a veces décimas). CircleMUD Builder's Manual §4.2: https://www.circlemud.org/pub/jelson/CircleMUD/3.x/uncompressed/current/doc/building.pdf

## Modificadores de ataque y daño
- `tirada_de_ataque = d20 + bono_precisión` y `daño_base = dados_arma + bono_daño` son modelos genéricos útiles para comparar.
- Los modificadores `hitroll` y `damroll` aparecen en sistemas Merc/ROM; confirmar orden de aplicación, caps, atributos y habilidades en el motor seleccionado.

## Defensa por tipo
- Modelo de datos inspirado en ROM: `defensa = {perforante, contundente, cortante, mágico}`.
- Elegir el componente según el tipo de ataque, luego aplicar la fórmula aprobada. **No sumar cuatro defensas simultáneamente.**
- Una cota puede proteger mejor de corte que de golpe; es una elección de diseño a validar, no una cifra histórica aquí.
- Referencia: https://github.com/avinson/rom24-quickmud/blob/master/doc/Rom2.4.doc

## Crecimiento por nivel
- Interpolación lineal didáctica entre puntos `(L0,T0)` y `(L1,T1)`: `T(L)=T0+(T1-T0)*(L-L0)/(L1-L0)`.
- Merc documenta THAC0 por clase interpolado entre niveles 0 y 32; **redondeos, límites y detalles requieren fuente concreta**: https://github.com/DikuMUDOmnibus/Merc-Cpp/blob/master/README
- Para VT2, evaluar curva de XP, HP, precisión, protección, duración de combate, recuperación y tiempo a siguiente nivel con simulaciones y pruebas.

## Escenarios de aceptación propuestos
1. Misma criatura, misma arma: mejorar defensa cambia tasa de impactos recibidos (o daño recibido, según sistema elegido), sin invulnerabilidad.
2. Espada `1d8` frente a `2d4`: mismo promedio (4.5 vs 5, **no idéntico**), diferente distribución; comparar resultados con precisión y defensa constantes.
3. Escudo + espada vs arma a dos manos: ventaja defensiva contra coste ofensivo medible.
4. Subir de nivel: cambia atributo visible y encuentro de referencia; nunca sólo un mensaje.
5. Equipar pieza incompatible: servidor rechaza y conserva inventario.
6. Reintentar compra con mismo ID de petición: no duplica arma ni gasta dos veces.
7. Vender pieza activa o última arma utilizable: rechazar de acuerdo al contrato VT2.
8. Migrar personaje antiguo: conserva equipo, dinero y progreso; slots nuevos vacíos por defecto.

## Evidencia exigida al programador
Para cada fórmula elegida: URL/version/ruta/función; pseudocódigo escrito de nuevo; tabla de 5 cálculos a mano; prueba determinista de bordes y distribución; comparación de 1000+ encuentros simulados **con semillas y sin modificar producción**; impacto por clase y región; notas de licencia.
