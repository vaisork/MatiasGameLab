"""Criaturas encontrables de la microaventura piloto VT-NAR-003 (El lindero
roto). El canon narrativo (comportamiento, aspecto, senales) sale de
vintage-telnet/CREATURES.md y no se toca aqui.

CREATURES.md dice explicitamente que no define estadisticas/dano/HP -- eso
"pertenece a Jugabilidad" (GAMEPLAY.md). Las cifras de combate de este
archivo son la calibracion tecnica inicial que Issue #45 pidio a Desarrollo
para que Mordelinde caiga en banda Favorable/Comparable y Espinajo de
rastrojo en banda Comparable/Peligroso contra un personaje nivel 1 recien
creado (atributos base 10, HP 100). GAMEPLAY.md 20.15 marca explicitamente
la dificultad concreta de cada enemigo como "afinable sin rediseñar el
sistema" tras pruebas reales -- estos valores deben tratarse como esa
primera calibracion, no como balance definitivo.

Cornalomo NO tiene entrada aqui: NARRATIVE.md exige pedir su tabla a
Jugabilidad antes de montar combate real contra el, y no aparece como
encuentro jugable en este piloto (solo como senales narrativas)."""

CREATURES = {
    "mordelinde": {
        "name": "Mordelinde",
        "family": "mordelinde",
        "reference_level": 1,
        "hp": 45,
        "fuerza": 11,
        "destreza": 11,
        "percepcion": 11,
        "agilidad": 14,
        "base_ataque": 6,  # mordida
        "flee_agilidad": 14,
        "flee_percepcion": 11,
    },
    "espinajo_rastrojo": {
        "name": "Espinajo de rastrojo",
        "family": "espinajo_rastrojo",
        "reference_level": 2,
        "hp": 70,
        "fuerza": 13,
        "destreza": 10,
        "percepcion": 10,
        "agilidad": 9,
        "base_ataque": 8,  # embestida
        "flee_agilidad": 9,
        "flee_percepcion": 10,
    },
}


def get_creature(creature_id):
    return CREATURES.get(creature_id)
