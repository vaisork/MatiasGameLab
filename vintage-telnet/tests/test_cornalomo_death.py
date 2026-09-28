"""Pruebas de la amenaza superior Cornalomo y flujo completo de muerte / respawn (Issue #213 / DEATH-01).

Contrato validado:
1. Perfil autoritativo de Cornalomo (HP 120, precisión 65, daño 20, reducción 20%, nivel ref 8).
2. Arte aprobado de Cornalomo visible durante el combate.
3. Ramal opcional en Pastos altos fuera del recorrido obligatorio a Vaisgard.
4. Señales de peligro antes del combate conforme al canon de CREATURES.md.
5. Retirada libre antes de iniciar combate (la criatura no ataca primero).
6. Evaluación de nivel 1 -> 'Abrumador' ('te supera claramente').
7. Aplicación de la reducción física del 20% al ser golpeado.
8. Flujo completo de derrota en combate:
   - 0 HP -> termina combate -> elimina encuentro activo de BD/store.
   - Reaparición autoritativa en valdren_centro.
   - 60% HP, 40 fatiga, herida degradada 1 grado.
   - Nivel, XP, PA, PP intactos.
   - Inventario y equipo intactos (NO pérdida de arma).
   - Reconexión limpia recupera exactamente el estado persistido.
9. Derrota al huir y al defender produce el mismo respawn seguro.
10. Huida con fórmula normal permitida.
11. Exploración continua post-respawn sin quedar atascado.
12. Sin regresión en pools aleatorios ni en la ruta principal.
"""
import os
import re
import tempfile
import unittest
from unittest.mock import Mock, patch

from server.app import RESPAWN_MESSAGE, create_app
from server import combat, creatures, encounters, store, world


class SequenceRng:
    """RNG determinista secuencial para simular tiradas de combate y huida."""
    def __init__(self, *values):
        self.values = list(values)
        self.idx = 0

    def uniform(self, a, b):
        if self.idx < len(self.values):
            val = self.values[self.idx]
            self.idx += 1
            return val
        return self.values[-1]


@patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
class CornalomoDeathTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                           DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False)
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

        # Controlar _rng de encuentros aleatorios (#207) para que las salas de paso
        # no generen encuentros espurios durante la navegación.
        self.enc_patch = patch.object(encounters, "_rng")
        self.mock_enc_rng = self.enc_patch.start()
        self.mock_enc_rng.random.return_value = 0.50
        self.addCleanup(self.enc_patch.stop)

    def tearDown(self):
        try:
            self.temp.cleanup()
        except PermissionError:
            pass

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def register_and_enter_world(self, username="matias", name="Matías"):
        self.post("/register", dict(username=username, name=name, password="una clave de prueba"))
        dm = self.app.test_client()
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.path, player_id, "juramentado")
        self.post("/move", dict(direction="south"))  # salir del hogar al centro de Valdren
        return player_id

    def character(self, client=None):
        client = client or self.client
        return client.get("/api/character").json

    def inventory(self, client=None):
        client = client or self.client
        return client.get("/api/inventory").json

    def assert_death_presentation(self, html):
        self.assertIn('<section class="death-event" data-death-event', html)
        self.assertIn("HAS MUERTO", html)
        self.assertIn("Las fuerzas te abandonan", html)
        self.assertIn("REAPARICIÓN", html)
        self.assertIn("Vuelves en ti en", html)
        self.assertIn("Estado al volver", html)
        self.assertIn("Salud", html)
        self.assertIn("Fatiga", html)
        self.assertIn("Herida", html)
        self.assertIn("Equipo", html)
        self.assertIn("Inventario", html)
        self.assertIn("Conservas tu equipo e inventario", html)

    def reach_pastos_altos(self):
        """Camina desde valdren_centro hasta valdren_pastos_altos por la ruta canónica."""
        directions = ["north", "north", "north", "north", "east", "north", "east", "east", "east"]
        for d in directions:
            res = self.post("/move", dict(direction=d))
            self.assertEqual(res.status_code, 303)
        room = self.client.get("/api/room").json["room"]
        self.assertEqual(room["id"], "valdren_pastos_altos")
        return room

    # --- 1. Perfil y canon de la criatura ---

    def test_cornalomo_authoritative_profile(self):
        c = creatures.get_creature("cornalomo")
        self.assertIsNotNone(c)
        self.assertEqual(c["name"], "Cornalomo")
        self.assertEqual(c["family"], "cornalomo")
        self.assertEqual(c["reference_level"], 8)
        self.assertEqual(c["hp"], 120)
        self.assertEqual(c["precision"], 65)
        self.assertEqual(c["damage"], 20)
        self.assertEqual(c["armor_reduction"], 0.20)
        self.assertEqual(c["flee_agilidad"], 8)
        self.assertEqual(c["flee_percepcion"], 9)
        self.assertIn("placa ósea", c["behavior_text"])
        self.assertIn("cuernos curvos", c["behavior_text"])
        art = creatures.CREATURE_ART.get("cornalomo")
        self.assertEqual(art["src"], "/assets/creatures/cornalomo.webp")
        self.assertEqual((art["width"], art["height"]), (1536, 1024))

    def test_cornalomo_art_is_shown_during_combat_and_served(self):
        self.register_and_enter_world()
        self.reach_pastos_altos()

        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('class="place-bar combat"', html)
        self.assertIn('data-location-art src="/assets/creatures/cornalomo.webp"', html)

        response = self.client.get("/assets/creatures/cornalomo.webp")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/webp")

    # --- 2. Ubicación opcional, ramal y señales previas ---

    def test_cornalomo_location_and_danger_cues(self):
        # Conectado fuera del recorrido obligatorio a Vaisgard
        self.assertEqual(world.get_room_encounter("valdren_pastos_altos"), "cornalomo")
        self.assertNotIn("valdren_pastos_altos", world.ROUTE_A_CHAIN)
        self.assertEqual(world.ROOMS["valdren_pastos_altos"]["exits"], {"west": "valdren_cruce_cercas"})
        self.assertEqual(world.ROOMS["valdren_cruce_cercas"]["exits"]["east"], "valdren_pastos_altos")

        # Señales de peligro canónicas de CREATURES.md
        self.assertIn("quebrados hacia afuera", world.get_examine_text("valdren_pastos_altos", "cerca"))
        self.assertIn("pezuñas grandes", world.get_examine_text("valdren_pastos_altos", "huellas"))
        self.assertIn("raspada", world.get_examine_text("valdren_pastos_altos", "arboles"))
        self.assertIn("aplastado", world.get_examine_text("valdren_pastos_altos", "pasto"))

    def test_player_can_enter_pastos_altos_and_retreat_without_fighting(self):
        pid = self.register_and_enter_world()
        self.reach_pastos_altos()

        room = self.client.get("/api/room").json["room"]
        self.assertEqual(room["id"], "valdren_pastos_altos")
        self.assertEqual(room["encounter"]["name"], "Cornalomo")

        # La criatura no ataca primero; el jugador puede retroceder a valdren_cruce_cercas
        res = self.post("/move", dict(direction="west"))
        self.assertEqual(res.status_code, 303)
        room_after = self.client.get("/api/room").json["room"]
        self.assertEqual(room_after["id"], "valdren_cruce_cercas")
        self.assertIsNone(room_after.get("encounter"))

    # --- 3. Evaluación cualitativa: Abrumador ---

    def test_level_1_evaluates_cornalomo_as_abrumador(self):
        pid = self.register_and_enter_world()
        self.reach_pastos_altos()

        res = self.post("/command", dict(text="evaluar Cornalomo"))
        html = res.get_data(as_text=True)
        self.assertIn("Cornalomo te supera claramente", html)

        # Validación matemática interna de la categoría
        c = creatures.get_creature("cornalomo")
        char = self.character()
        cg_p = combat.competencia_general(char["level"])
        cg_e = combat.competencia_general(c["reference_level"])
        p_dps = combat.expected_dps(10, 10, 10, cg_p, cg_e, base_arma=10)
        e_dps = combat.fixed_expected_dps(c["precision"], c["damage"])
        category = combat.encounter_category(p_dps, char["hp_current"], e_dps, c["hp"])
        self.assertEqual(category, "abrumador")

    # --- 4. Reducción física de armadura de la criatura (20%) ---

    def test_cornalomo_armor_reduction_in_combat(self):
        pid = self.register_and_enter_world()
        self.reach_pastos_altos()

        # Forzar impacto del jugador con tirada 0.0 y fallo de Cornalomo con 99.0
        with patch("server.combat.random.Random", return_value=SequenceRng(0.0, 99.0)):
            res = self.post("/command", dict(text="atacar"))

        # Daño base nivel 1 con espada base 10 contra Cornalomo:
        # raw damage = 10, con 20% reducción = 8 de daño aplicado
        enc = store.get_encounter(self.path, pid, "valdren_pastos_altos")
        self.assertIsNotNone(enc)
        self.assertEqual(enc["hp_current"], 120 - 8)

    # --- 5. Flujo completo de derrota en combate, persistencia y reconexión ---

    @patch("server.combat.random.Random")
    def test_defeat_attacking_terminates_encounter_and_persists_respawn_state_on_reconnect(self, mock_random):
        """DEATH_PLAYTEST.md §7.A: Muerte atacando."""
        # Tirada 1: 99.0 (jugador falla ataque)
        # Tirada 2: 0.0 (Cornalomo impacta)
        mock_random.return_value = SequenceRng(99.0, 0.0)

        pid = self.register_and_enter_world()

        # Equipar y configurar estado previo rico
        store.grant_item(self.path, pid, "espada_juramento")
        store.grant_item(self.path, pid, "acolchado_camino")
        store.grant_item(self.path, pid, "punal_camino")
        self.post("/command", dict(text="equipar Espada de juramento"))
        self.post("/command", dict(text="equipar Acolchado de Camino"))

        with store.connect(self.path) as db:
            db.execute("UPDATE players SET xp = 60, pa_unspent = 4, pp_unspent = 2, wound = 'moderada' WHERE id = ?",
                       (pid,))

        char_before = self.character()
        inv_before = self.inventory()
        hp_max = char_before["hp_max"]

        self.assertEqual(char_before["level"], 1)
        self.assertEqual(char_before["xp"], 60)
        self.assertEqual(char_before["pa_unspent"], 4)
        self.assertEqual(char_before["pp_unspent"], 2)
        self.assertEqual(char_before["wound"], "moderada")
        self.assertEqual(inv_before["equipped"]["weapon"]["item_key"], "espada_juramento")
        self.assertEqual(inv_before["equipped"]["armor"]["item_key"], "acolchado_camino")
        self.assertEqual(len(inv_before["items"]), 3)

        self.reach_pastos_altos()
        self.assertIsNotNone(store.get_encounter(self.path, pid, "valdren_pastos_altos"))

        # Bajar HP para que el golpe de 20 (menos 10% armadura = 18) de Cornalomo derrote al jugador
        store.update_combat_state(self.path, pid, hp_current=15)

        response = self.post("/command", dict(text="atacar"))
        html = response.get_data(as_text=True)
        self.assertIn("Cornalomo te derrota", html)
        self.assertNotIn(RESPAWN_MESSAGE, html)
        self.assert_death_presentation(html)

        # La presentación es efímera: refrescar/reconectar muestra el estado
        # persistido, pero no reproduce indefinidamente la muerte consumida.
        refreshed = self.client.get("/").get_data(as_text=True)
        self.assertNotIn('<section class="death-event" data-death-event', refreshed)
        self.assertNotIn("HAS MUERTO", refreshed)

        # 1 y 2: Encuentro terminado y sin encuentro fantasma en store/SQLite
        self.assertIsNone(store.get_encounter(self.path, pid, "valdren_pastos_altos"))
        self.assertIsNone(store.get_encounter(self.path, pid, "valdren_centro"))
        with store.connect(self.path) as db:
            active_cornalomo = db.execute(
                "SELECT count(*) FROM room_encounters WHERE player_id = ? AND room_id = 'valdren_pastos_altos'",
                (pid,)).fetchone()[0]
            self.assertEqual(active_cornalomo, 0)
            active_safe = db.execute(
                "SELECT count(*) FROM room_encounters WHERE player_id = ? AND room_id = 'valdren_centro'",
                (pid,)).fetchone()[0]
            self.assertEqual(active_safe, 0)

        # 3, 4: Reaparición segura en valdren_centro con 60% HP, 40 fatiga, herida degradada
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")

        char_after = self.character()
        expected_hp = round(hp_max * 0.60)
        self.assertEqual(char_after["hp_current"], expected_hp)
        self.assertEqual(char_after["fatigue"], 40)
        self.assertEqual(char_after["wound"], "leve")  # degradada de moderada a leve
        self.assertFalse(char_after["in_combat"])

        # 5: Progresión intacta (nivel, XP, PA, PP)
        self.assertEqual(char_after["level"], char_before["level"])
        self.assertEqual(char_after["xp"], char_before["xp"])
        self.assertEqual(char_after["pa_unspent"], char_before["pa_unspent"])
        self.assertEqual(char_after["pp_unspent"], char_before["pp_unspent"])

        # 6: NO pérdida de arma: inventario y equipo completos intactos
        inv_after = self.inventory()
        self.assertEqual(inv_after["items"], inv_before["items"])
        self.assertEqual(inv_after["equipped"]["weapon"]["item_key"], "espada_juramento")
        self.assertEqual(inv_after["equipped"]["armor"]["item_key"], "acolchado_camino")
        self.assertEqual(inv_after["equipped"], inv_before["equipped"])

        # 7: Reconexión en nueva sesión recupera exactamente el estado persistido
        session_cookie = self.client.get_cookie("vt_session").value
        new_client = self.app.test_client()
        new_client.set_cookie("vt_session", session_cookie)

        reconnected_me = new_client.get("/api/me").json["player"]
        self.assertEqual(reconnected_me["room"], "valdren_centro")

        reconnected_char = self.character(new_client)
        self.assertEqual(reconnected_char["level"], char_before["level"])
        self.assertEqual(reconnected_char["xp"], char_before["xp"])
        self.assertEqual(reconnected_char["pa_unspent"], char_before["pa_unspent"])
        self.assertEqual(reconnected_char["pp_unspent"], char_before["pp_unspent"])
        self.assertEqual(reconnected_char["hp_current"], expected_hp)
        self.assertEqual(reconnected_char["fatigue"], 40)
        self.assertEqual(reconnected_char["wound"], "leve")
        self.assertFalse(reconnected_char["in_combat"])

        inv_reconnected = self.inventory(new_client)
        self.assertEqual(inv_reconnected["items"], inv_before["items"])
        self.assertEqual(inv_reconnected["equipped"], inv_before["equipped"])

        reconnected_room = new_client.get("/api/room").json["room"]
        self.assertEqual(reconnected_room["id"], "valdren_centro")
        self.assertIsNone(reconnected_room["encounter"])

    # --- 6. Muerte intentando huir ---

    @patch("server.app.random.Random")
    def test_defeat_while_fleeing_terminates_encounter_and_triggers_safe_respawn(self, mock_random):
        """DEATH_PLAYTEST.md §7.B: Muerte intentando huir."""
        # Tirada 1: 99.0 para fallar huida (99 > flee_chance)
        # Tirada 2: 0.0 para que el contragolpe de Cornalomo impacte
        mock_random.return_value = SequenceRng(99.0, 0.0)
        pid = self.register_and_enter_world()
        self.reach_pastos_altos()

        store.update_combat_state(self.path, pid, hp_current=10)

        response = self.post("/command", dict(text="huir"))
        html = response.get_data(as_text=True)
        self.assertIn("Cornalomo te derrota", html)
        self.assert_death_presentation(html)

        self.assertIsNone(store.get_encounter(self.path, pid, "valdren_pastos_altos"))
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")

        char = self.character()
        self.assertEqual(char["hp_current"], round(char["hp_max"] * 0.60))
        self.assertEqual(char["fatigue"], 40)
        self.assertFalse(char["in_combat"])

    # --- 7. Muerte defendiendo ---

    @patch("server.app.random.Random")
    def test_defeat_while_defending_terminates_encounter_and_triggers_safe_respawn(self, mock_random):
        """DEATH_PLAYTEST.md §7.C: Muerte defendiendo (esquivar)."""
        # Tirada 0.0: el ataque de Cornalomo impacta a pesar de esquivar
        mock_random.return_value = SequenceRng(0.0)
        pid = self.register_and_enter_world()
        self.reach_pastos_altos()

        store.update_combat_state(self.path, pid, hp_current=10)

        response = self.post("/command", dict(text="esquivar"))
        html = response.get_data(as_text=True)
        self.assertIn("Cornalomo te derrota", html)
        self.assert_death_presentation(html)

        self.assertIsNone(store.get_encounter(self.path, pid, "valdren_pastos_altos"))
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")

        char = self.character()
        self.assertEqual(char["hp_current"], round(char["hp_max"] * 0.60))
        self.assertEqual(char["fatigue"], 40)
        self.assertFalse(char["in_combat"])

    @patch("server.app.random.Random")
    def test_defeat_while_resisting_uses_same_visible_death_presentation(self, mock_random):
        mock_random.return_value = SequenceRng(0.0)
        pid = self.register_and_enter_world()
        self.reach_pastos_altos()
        store.update_combat_state(self.path, pid, hp_current=10)

        html = self.post("/command", dict(text="resistir")).get_data(as_text=True)
        self.assert_death_presentation(html)
        self.assertEqual(self.client.get("/api/me").json["player"]["room"], "valdren_centro")

    @patch("server.app._can_block", return_value=True)
    @patch("server.app.random.Random")
    def test_defeat_while_blocking_uses_same_visible_death_presentation(self, mock_random, _can_block):
        mock_random.return_value = SequenceRng(0.0)
        pid = self.register_and_enter_world()
        self.reach_pastos_altos()
        store.update_combat_state(self.path, pid, hp_current=10)

        html = self.post("/command", dict(text="bloquear")).get_data(as_text=True)
        self.assert_death_presentation(html)
        self.assertEqual(self.client.get("/api/me").json["player"]["room"], "valdren_centro")

    # --- 8. Huida exitosa con fórmula normal ---

    @patch("server.app.random.Random")
    def test_flee_chance_normal_formula_allows_escape(self, mock_random):
        """DEATH_PLAYTEST.md §3: Huida normal permitida con fórmula estándar."""
        # Tirada 0.0: huida exitosa (0.0 < flee_chance)
        mock_random.return_value = SequenceRng(0.0)
        pid = self.register_and_enter_world()
        self.reach_pastos_altos()

        # Iniciar combate con atacar
        with patch("server.combat.random.Random", return_value=SequenceRng(99.0, 99.0)):
            self.post("/command", dict(text="atacar"))

        response = self.post("/command", dict(text="huir"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Consigues alejarte de Cornalomo", response.get_data(as_text=True))

        room = self.client.get("/api/room").json["room"]
        # Retrocede hacia el cruce de las cercas
        self.assertEqual(room["id"], "valdren_cruce_cercas")

    # --- 9. Continuación de exploración post-respawn ---

    def test_player_can_continue_exploring_world_after_respawn(self):
        """DEATH_PLAYTEST.md §7.E: El personaje no queda atascado en estado muerto y puede seguir jugando."""
        with patch("server.combat.random.Random", return_value=SequenceRng(99.0, 0.0)):
            pid = self.register_and_enter_world()
            self.reach_pastos_altos()
            store.update_combat_state(self.path, pid, hp_current=10)
            self.post("/command", dict(text="atacar"))

        # El jugador reapareció en valdren_centro y puede volver a caminar al norte
        me = self.client.get("/api/me").json["player"]
        self.assertEqual(me["room"], "valdren_centro")

        move_res = self.post("/move", dict(direction="north"))
        self.assertEqual(move_res.status_code, 303)
        current_room = self.client.get("/api/room").json["room"]
        self.assertEqual(current_room["id"], "valdren_sendero")

    # --- 10. No regresión en pools aleatorios ni exclusión de Cornalomo ---

    def test_random_encounter_pools_remain_unaffected_and_exclude_cornalomo(self):
        for pool in encounters.RANDOM_ENCOUNTER_POOLS.values():
            self.assertNotIn("cornalomo", [cid for cid, _ in pool["creatures"]])
            self.assertNotIn("valdren_pastos_altos", pool["rooms"])


if __name__ == "__main__":
    unittest.main()
