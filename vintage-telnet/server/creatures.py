"""Criaturas encontrables de la microaventura piloto VT-NAR-003 (El lindero
roto). El canon narrativo (comportamiento, aspecto, senales) sale de
vintage-telnet/CREATURES.md y no se toca aqui.

CREATURES.md dice explicitamente que no define estadisticas/dano/HP -- eso
"pertenece a Jugabilidad" (GAMEPLAY.md). Los valores de combate de este
archivo (hp/precision/damage) son el perfil v1 aprobado directamente por
Jugabilidad en vintage-telnet/STARTER_CREATURE_BALANCE.md -- no un modelo
derivado de atributos genericos. La revision de Arquitectura de PR #49
senalo que una version anterior de este archivo, que derivaba HP/precision/
dano de un modelo de atributos generico (20.4), divergia demasiado de esa
tabla aprobada; por eso los tres numeros de combate se copian aqui tal
cual, y `server/combat.py` los resuelve con `resolve_fixed_attack_roll`/
`fixed_expected_dps` en vez de `resolve_attack_roll`/`expected_dps`.
GAMEPLAY.md 20.15 marca explicitamente la dificultad concreta de cada
enemigo como "afinable sin rediseñar el sistema" tras pruebas reales --
estos valores deben tratarse como esa primera calibracion, no como balance
definitivo.

`behavior_text` reformula sin inventar el comportamiento ya descrito en
CREATURES.md ("corre en zigzag hacia agujeros o maleza" / "eriza las puas
antes de atacar") para que Mordelinde y Espinajo se lean como criaturas
distintas antes de que el jugador decida atacar/huir (VT-PSY-004).

Cornalomo NO tiene entrada aqui: NARRATIVE.md exige pedir su tabla a
Jugabilidad antes de montar combate real contra el, y no aparece como
encuentro jugable en este piloto (solo como senales narrativas)."""

CREATURES = {
    "mordelinde": {
        "name": "Mordelinde",
        "family": "mordelinde",
        "reference_level": 1,
        "hp": 28,
        "precision": 45,
        "damage": 5,
        "flee_agilidad": 14,
        "flee_percepcion": 11,
        "behavior_text": ("Mordelinde no te persigue: si detecta movimiento, corre en zigzag "
                           "buscando una madriguera o la maleza."),
    },
    "espinajo_rastrojo": {
        "name": "Espinajo de rastrojo",
        "family": "espinajo_rastrojo",
        "reference_level": 2,
        "hp": 40,
        "precision": 50,
        "damage": 8,
        "flee_agilidad": 9,
        "flee_percepcion": 10,
        "behavior_text": ("Espinajo de rastrojo eriza las puas del lomo y se mantiene firme: "
                           "vigila su territorio y no huye con facilidad."),
    },
}


# Ilustración de cada criatura para el marco de arte durante el combate
# (petición de Javier, 2026-09-25). Solo criaturas con imagen aprobada y
# publicada en assets/vintage-telnet/creatures/; una criatura sin fila deja
# el marco vacío y quieto en combate, nunca muestra una imagen ajena.
# Formato de cada fila: {"src": "/assets/creatures/<id>.webp", "alt": ...,
# "width": ..., "height": ...}.
CREATURE_ART = {
    # Issue #151, aprobados por Dirección de Arte y publicados en las PR #161
    # (SHA-256 036ab079...) y #170 (SHA-256 abd4187d...).
    "mordelinde": {"src": "/assets/creatures/mordelinde.webp",
                   "alt": "Mordelinde acorralado en una parcela removida",
                   "width": 1536, "height": 1024},
    "espinajo_rastrojo": {"src": "/assets/creatures/espinajo_rastrojo.webp",
                          "alt": "Espinajo de rastrojo con la cresta de púas erizada",
                          "width": 1536, "height": 1024},
}


def get_creature(creature_id):
    return CREATURES.get(creature_id)
