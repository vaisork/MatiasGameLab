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
antes de atacar" / "resopla con pesadez") para que las criaturas se lean
como distintas antes de que el jugador decida atacar/huir (VT-PSY-004).

Cornalomo (Issue #213 / DEATH-01): perfil v1 aprobado directamente por
Jugabilidad en STARTER_CREATURE_BALANCE.md y DEATH_PLAYTEST.md como amenaza
superior regional de Edran para la prueba de muerte y respawn."""

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
    "cornalomo": {
        "name": "Cornalomo",
        "family": "cornalomo",
        "reference_level": 8,
        "hp": 120,
        "precision": 65,
        "damage": 20,
        "armor_reduction": 0.20,
        "flee_agilidad": 8,
        "flee_percepcion": 9,
        "behavior_text": ("Cornalomo sacude la placa ósea de la frente y resopla con pesadez: "
                           "no busca combate sin motivo, pero su masa y cuernos curvos dominan el terreno."),
    },
    "unapiedra": {
        "name": "Uñapiedra",
        "family": "unapiedra",
        "reference_level": 1,
        "hp": 30,
        "precision": 45,
        "damage": 5,
        "flee_agilidad": 15,
        "flee_percepcion": 12,
        "behavior_text": ("Uñapiedra se aplasta contra la roca y busca una grieta o saliente cercana; "
                           "si la acorralas, sisea y defiende el refugio con una mordida corta."),
    },
    "saltacresta": {
        "name": "Saltacresta",
        "family": "saltacresta",
        "reference_level": 2,
        "hp": 36,
        "precision": 50,
        "damage": 7,
        "flee_agilidad": 16,
        "flee_percepcion": 14,
        "behavior_text": ("Saltacresta flexiona las patas traseras y busca una terraza libre; "
                           "si le cierras la salida, golpea el suelo y se prepara para defenderse con una patada corta."),
    },
    # Fauna regional v1 — contratos mecánicos literales de #298–#303.
    # Sin assets aprobados: estas criaturas dejan el marco de combate neutral.
    "cascapedernal": {
        "name": "Cascapedernal",
        "family": "cascapedernal",
        "reference_level": 1,
        "hp": 34,
        "precision": 42,
        "damage": 5,
        "armor_reduction": 0.10,
        "flee_agilidad": 8,
        "flee_percepcion": 9,
        "behavior_text": ("Cascapedernal se encoge y golpea el suelo con el borde de su caparazón; "
                           "permanece junto a la piedra cálida y busca una hendidura estrecha."),
    },
    "colagrieta": {
        "name": "Colagrieta",
        "family": "colagrieta",
        "reference_level": 2,
        "hp": 33,
        "precision": 52,
        "damage": 7,
        "flee_agilidad": 14,
        "flee_percepcion": 13,
        "behavior_text": ("Colagrieta asoma la cabeza desde una fisura y repliega su cola contra la roca; "
                           "evita permanecer en terreno abierto y retrocede al notar vibraciones."),
    },
    "pinzajunco": {
        "name": "Pinzajunco",
        "family": "pinzajunco",
        "reference_level": 1,
        "hp": 32,
        "precision": 47,
        "damage": 6,
        "armor_reduction": 0.05,
        "flee_agilidad": 8,
        "flee_percepcion": 10,
        "behavior_text": ("Pinzajunco levanta la pinza mayor como advertencia y se mueve de lado "
                           "entre barro, raíces y juncos."),
    },
    "saltalodo": {
        "name": "Saltalodo",
        "family": "saltalodo",
        "reference_level": 2,
        "hp": 38,
        "precision": 50,
        "damage": 7,
        "flee_agilidad": 14,
        "flee_percepcion": 12,
        "behavior_text": ("Saltalodo permanece semisumergido; al asustarse, salta hacia el agua profunda, "
                           "aunque un ejemplar territorial puede defender su charca."),
    },
    "rondamusgo": {
        "name": "Rondamusgo",
        "family": "rondamusgo",
        "reference_level": 1,
        "hp": 29,
        "precision": 44,
        "damage": 5,
        "flee_agilidad": 14,
        "flee_percepcion": 12,
        "behavior_text": ("Rondamusgo se queda inmóvil al oír pasos y corre cuando se siente observado; "
                           "busca hongos y raíces tiernas entre la hojarasca."),
    },
    "hilaria_niebla": {
        "name": "Hilaria de niebla",
        "family": "hilaria_niebla",
        "reference_level": 2,
        "hp": 34,
        "precision": 52,
        "damage": 7,
        "flee_agilidad": 10,
        "flee_percepcion": 14,
        "behavior_text": ("Hilaria de niebla permanece inmóvil junto a su red baja; los filamentos "
                           "vibran antes de que retroceda hacia un hueco de corteza."),
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
    # Issue #180, aprobado por Dirección de Arte y publicado en PR #188.
    "cornalomo": {"src": "/assets/creatures/cornalomo.webp",
                  "alt": "Cornalomo avanzando por los Llanos de Edran con la placa frontal y las estructuras dorsales visibles",
                  "width": 1536, "height": 1024},
}


def get_creature(creature_id):
    return CREATURES.get(creature_id)
