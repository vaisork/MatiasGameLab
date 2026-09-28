"""Pruebas del Issue #216 (VT-GAME/DEV): capacidades firma de clase + intencion
enemiga v1 (GAMEPLAY.md seccion 36).

Cubre:
1. Formulas puras en server/combat.py:
   - Coste base de fatiga: FATIGUE_BASE_COST["capacidad_firma"] = 5 (36.2).
   - Guardia Comprometida (36.4): ReduccionGuardia, eliminacion del bono de carga frontal.
   - Impulso Arcano (36.5): cancelacion de prepared_action interruptible (-10% prec)
     o desestabilizacion general (-20% prec).
   - Borrar el Foco (36.6): -25% prec enemigo, concesion de Apertura (+15% en prox basico) tras fallo.
   - Tiro de Interrupcion (36.7): 75% dano base, cancelacion de prepared_action interruptible
     o -15% prec enemigo si no habia accion preparada.
2. Estado de combate y persistencia:
   - Decremento determinista de recargas (2 rondas Juramentado/Artifice, 4 rondas Arcano/Sombra).
   - Apertura vive solo durante el combate y se consume en el primer ataque basico.
   - prepared_action enemiga visible (telegraph) antes de la intervencion y resuelta en el turno.
3. Integracion end-to-end (rutas, intenciones, /api/character, /api/room, /api/intent).
"""
import re
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import combat, creatures, items, store, world


class FixedRoll:
    """RNG determinista para tests."""
    def __init__(self, value):
        self.value = value

    def uniform(self, a, b):
        return self.value


class SignatureSkillsMathTests(unittest.TestCase):
    def test_fatigue_base_cost_signature_ability(self):
        self.assertEqual(combat.FATIGUE_BASE_COST["capacidad_firma"], 5)

    def test_guardia_reduction_formula(self):
        # Base destreza=10, resistencia=10 -> 30%
        self.assertAlmostEqual(combat.guardia_reduction(10, 10), 0.30)
        # destreza=20, resistencia=20 -> 30% + 0.25%*10 + 0.15%*10 = 34%
        self.assertAlmostEqual(combat.guardia_reduction(20, 20), 0.34)
        # Cap a 45%
        self.assertAlmostEqual(combat.guardia_reduction(100, 100), 0.45)

    def test_guardia_comprometida_attack_roll_mitigates_charge(self):
        # Embestida frontal: 60% prec, 8 dano. Base Espinajo: 50% prec.
        # Guardia Comprometida devuelve la precision a la base (50%).
        # Tirada 55 falla contra 50 (pero habria acertado contra 60).
        hits, dmg = combat.resolve_guardia_comprometida_attack_roll(
            enemy_precision=60, enemy_damage=8, destreza=10, resistencia=10,
            is_frontal_charge=True, creature_base_precision=50, rng=FixedRoll(55))
        self.assertFalse(hits)
        self.assertEqual(dmg, 0.0)

        # Tirada 20 acierta contra 50. Aplica reduccion de guardia (30% con atributos 10).
        hits, dmg = combat.resolve_guardia_comprometida_attack_roll(
            enemy_precision=60, enemy_damage=8, destreza=10, resistencia=10,
            is_frontal_charge=True, creature_base_precision=50, rng=FixedRoll(20))
        self.assertTrue(hits)
        self.assertAlmostEqual(dmg, 8.0 * (1 - 0.30))

    def test_impulso_arcano_effect(self):
        # Con accion preparada interruptible
        prep = {"id": "embestida_territorial", "interruptible": True}
        res = combat.resolve_impulso_arcano_effect(prep)
        self.assertTrue(res["interrupted"])
        self.assertEqual(res["enemy_accuracy_penalty"], 10)

        # Sin accion preparada o no interruptible
        res_none = combat.resolve_impulso_arcano_effect(None)
        self.assertFalse(res_none["interrupted"])
        self.assertEqual(res_none["enemy_accuracy_penalty"], 20)

    def test_borrar_el_foco_effect(self):
        res = combat.resolve_borrar_el_foco_effect()
        self.assertEqual(res["enemy_accuracy_penalty"], 25)

    def test_tiro_de_interrupcion_attack_roll(self):
        # Impacto contra accion preparada interruptible -> 75% dano y cancela especial
        prep = {"id": "embestida_territorial", "interruptible": True}
        hits, dmg, eff = combat.resolve_tiro_de_interrupcion_attack_roll(
            attacker_destreza=10, attacker_percepcion=10, attacker_fuerza=10,
            attacker_cg=0, defender_cg=0, base_arma=10,
            prepared_action=prep, rng=FixedRoll(10))
        self.assertTrue(hits)
        self.assertAlmostEqual(dmg, 10 * 0.75)
        self.assertTrue(eff["interrupted"])
        self.assertEqual(eff["enemy_accuracy_penalty"], 0)

        # Impacto sin accion preparada -> 75% dano y -15% precision enemigo
        hits, dmg, eff = combat.resolve_tiro_de_interrupcion_attack_roll(
            attacker_destreza=10, attacker_percepcion=10, attacker_fuerza=10,
            attacker_cg=0, defender_cg=0, base_arma=10,
            prepared_action=None, rng=FixedRoll(10))
        self.assertTrue(hits)
        self.assertFalse(eff["interrupted"])
        self.assertEqual(eff["enemy_accuracy_penalty"], 15)

        # Fallo de disparo -> no dano, no interrupcion
        hits, dmg, eff = combat.resolve_tiro_de_interrupcion_attack_roll(
            attacker_destreza=10, attacker_percepcion=10, attacker_fuerza=10,
            attacker_cg=0, defender_cg=0, base_arma=10,
            prepared_action=prep, rng=FixedRoll(99))
        self.assertFalse(hits)
        self.assertEqual(dmg, 0.0)
        self.assertFalse(eff["interrupted"])


class SignatureSkillsIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def register_and_enter_world(self, player_class="juramentado", username="matias", name="Matías"):
        self.post("/register", dict(username=username, name=name, password="una clave de prueba"))
        dm = self.app.test_client()
        with patch.dict("os.environ", {"VT_DM_PASSWORD": "dm-secret-value"}):
            self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
            self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class=player_class))

    def enter_combat_with_espinajo(self):
        # Spawns Espinajo directly in current room for testing
        player = self.client.get("/api/me").json["player"]
        store.start_encounter(self.path, player["id"], player["room"], "espinajo_rastrojo", 40)

    def test_api_character_exposes_signature_ability(self):
        self.register_and_enter_world(player_class="juramentado")
        char = self.client.get("/api/character").json
        self.assertIsNotNone(char.get("signature_ability"))
        self.assertEqual(char["signature_ability"]["id"], "guardia_comprometida")
        self.assertEqual(char["signature_ability"]["cooldown"], 2)

    def test_juramentado_guardia_comprometida_lifecycle(self):
        self.register_and_enter_world(player_class="juramentado")
        self.enter_combat_with_espinajo()

        room = self.client.get("/api/room").json["room"]
        self.assertIsNotNone(room.get("signature_ability"))
        sig = room["signature_ability"]
        self.assertEqual(sig["id"], "guardia_comprometida")
        self.assertTrue(sig["ready"])
        self.assertEqual(sig["cooldown_remaining"], 0)

        # Intencion enemiga visible
        enc = room["encounter"]
        self.assertIsNotNone(enc.get("prepared_action"))
        self.assertEqual(enc["prepared_action"]["id"], "embestida_territorial")
        self.assertTrue(enc["prepared_action"]["frontal"])
        self.assertIn("embestida frontal", enc["telegraph"])

        # Acciones disponibles incluyen capacidad
        action_names = [a["action"] for a in room["available_actions"]]
        self.assertIn("capacidad", action_names)

        # Ejecuta Guardia Comprometida
        resp = self.post("/command", dict(text="guardia comprometida"))
        self.assertEqual(resp.status_code, 200)

        # Tras usarla, entra en recarga de 2 rondas
        room2 = self.client.get("/api/room").json["room"]
        sig2 = room2["signature_ability"]
        self.assertFalse(sig2["ready"])
        self.assertEqual(sig2["cooldown_remaining"], 2)
        self.assertIn("recarga", sig2["disabled_reason"])
        action_names2 = [a["action"] for a in room2["available_actions"]]
        self.assertNotIn("capacidad", action_names2)

        # Intentar usarla en recarga es rechazado
        fail_resp = self.post("/command", dict(text="capacidad"))
        self.assertIn("está en recarga", fail_resp.get_data(as_text=True))

        # Intervencion 1: atacar (decrementa cd de 2 a 1)
        self.post("/command", dict(text="atacar"))
        room3 = self.client.get("/api/room").json["room"]
        self.assertEqual(room3["signature_ability"]["cooldown_remaining"], 1)

        # Intervencion 2: esquivar (decrementa cd de 1 a 0)
        self.post("/command", dict(text="esquivar"))
        room4 = self.client.get("/api/room").json["room"]
        self.assertEqual(room4["signature_ability"]["cooldown_remaining"], 0)
        self.assertTrue(room4["signature_ability"]["ready"])

    def test_juramentado_unarmed_cannot_use_guardia(self):
        self.register_and_enter_world(player_class="juramentado")
        # Desequipa espada
        self.post("/command", dict(text="desequipar Espada de juramento"))
        self.enter_combat_with_espinajo()

        room = self.client.get("/api/room").json["room"]
        self.assertFalse(room["signature_ability"]["ready"])
        self.assertIn("bloquear", room["signature_ability"]["disabled_reason"])

        res = self.post("/command", dict(text="guardia"))
        self.assertIn("Requiere un arma u objeto", res.get_data(as_text=True))

    def test_arcano_impulso_arcano_interrupts_embestida(self):
        self.register_and_enter_world(player_class="arcano")
        self.enter_combat_with_espinajo()

        room = self.client.get("/api/room").json["room"]
        self.assertEqual(room["signature_ability"]["id"], "impulso_arcano")
        self.assertTrue(room["signature_ability"]["ready"])

        # Usa Impulso Arcano via /ability
        resp = self.post("/ability")
        self.assertEqual(resp.status_code, 200)
        page = resp.get_data(as_text=True)
        self.assertIn("desbarata la embestida territorial", page)

        # Recarga es de 4 rondas
        room2 = self.client.get("/api/room").json["room"]
        self.assertEqual(room2["signature_ability"]["cooldown_remaining"], 4)

    def test_sombra_borrar_el_foco_grants_apertura_on_miss(self):
        self.register_and_enter_world(player_class="sombra")
        self.enter_combat_with_espinajo()

        # Forzar fallo del enemigo con FixedRoll(99)
        with patch("server.combat.random.Random") as mock_rng_cls:
            mock_rng = FixedRoll(99)
            mock_rng_cls.return_value = mock_rng
            resp = self.post("/command", dict(text="borrar el foco"))
            self.assertIn("Ganas Apertura", resp.get_data(as_text=True))

        # Comprobar que en base de datos apertura = 1
        player = self.client.get("/api/me").json["player"]
        enc = store.get_encounter(self.path, player["id"], player["room"])
        self.assertEqual(enc["apertura"], 1)

        # Siguiente ataque basico consume apertura (+15% precision)
        with patch("server.combat.random.Random") as mock_rng_cls:
            mock_rng_cls.return_value = FixedRoll(10)
            atk_resp = self.post("/command", dict(text="atacar"))
            self.assertIn("Aprovechas la apertura", atk_resp.get_data(as_text=True))

        enc2 = store.get_encounter(self.path, player["id"], player["room"])
        self.assertEqual(enc2["apertura"], 0)

    def test_artifice_tiro_de_interrupcion(self):
        self.register_and_enter_world(player_class="artifice")
        self.enter_combat_with_espinajo()

        # Disparo certero que impacta (FixedRoll(10))
        with patch("server.combat.random.Random") as mock_rng_cls:
            mock_rng_cls.return_value = FixedRoll(10)
            resp = self.post("/command", dict(text="tiro de interrupcion"))
            page = resp.get_data(as_text=True)
            self.assertIn("Tiro de Interrupción", page)
            self.assertIn("desbarata la embestida territorial", page)

        room2 = self.client.get("/api/room").json["room"]
        self.assertEqual(room2["signature_ability"]["cooldown_remaining"], 2)

    def test_api_intent_signature_ability(self):
        self.register_and_enter_world(player_class="juramentado")
        self.enter_combat_with_espinajo()

        csrf = self.csrf()
        resp = self.client.post(
            "/api/intent",
            json={"text": "capacidad", "csrf": csrf},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json
        self.assertTrue(data["accepted"])
        self.assertEqual(data["intent"], "signature_ability")
        self.assertIn("Guardia Comprometida", " ".join(data["messages"]))

    def test_fatigue_gained_from_signature_ability(self):
        self.register_and_enter_world(player_class="juramentado")
        self.enter_combat_with_espinajo()

        player_before = self.client.get("/api/me").json["player"]
        self.post("/command", dict(text="guardia"))
        player_after = self.client.get("/api/me").json["player"]

        fatigue_diff = player_after["fatigue"] - player_before["fatigue"]
        # Coste base 5, modificado por resistencia y armadura de juramentado
        self.assertGreaterEqual(fatigue_diff, 4)
        self.assertLessEqual(fatigue_diff, 7)
