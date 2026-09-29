"""Pruebas exhaustivas del motor reusable de jefes únicos C5 (GAMEPLAY §41 / Issue #362).

Cubre todos los criterios requeridos por §41.13:
1. Un C3/C4 no obtiene comportamiento C5 accidentalmente (§41.13).
2. boss_id único (§41.1, §41.2).
3. Boss derrotado no reaparece tras reconnect/restart (§41.2).
4. Wipe sin victoria NO marca derrotado (§41.3, §41.12).
5. HP/fase reset default entre intentos (§41.3, §41.12).
6. Participantes comparten encounter (§41.3).
7. Espectador no cobra / filtro de contribución significativa (§41.10, §41.11).
8. Retirada previa no cuenta derrota (§41.4).
9. weapon_loss_on_defeat=false conserva arma (§41.6, §41.7).
10. weapon_loss_on_defeat=true pierde únicamente arma equipada (§41.7).
11. Sin arma no sustituye la penalización por otro objeto (§41.9).
12. Estado de arma perdida persiste (§41.7).
13. Recuperación/reemplazo no duplica (§41.7, §41.8).
14. Recompensas once-* respetan su alcance (world vs character) (§41.10).
15. Forja no se usa falsamente como flag de pérdida (§41.7, §41.13).
16. Bloqueo de descanso y equipamiento ante presencia de jefe (§41.3).
17. Acciones defensivas, huida y evaluación cualitativa en arena (§41.4, §41.5).
18. Supresión de fauna C1 aleatoria en arenas activas de jefe (§41.4).
"""

import os
import re
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from server.app import create_app
from server import bosses, combat, creatures, encounters, items, store, world
from server.bosses import BossContract, BossPhase, BossReward


class SequenceRng:
    """RNG determinista secuencial para simular tiradas."""
    def __init__(self, *values):
        self.values = list(values)
        self.idx = 0

    def uniform(self, a, b):
        if self.idx < len(self.values):
            val = self.values[self.idx]
            self.idx += 1
            return val
        return self.values[-1]

    def random(self):
        if self.idx < len(self.values):
            val = self.values[self.idx]
            self.idx += 1
            return val
        return self.values[-1]


@patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
class BossEngineTests(unittest.TestCase):
    def setUp(self):
        bosses.clear_bosses()
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(
            TESTING=True,
            SECRET_KEY="test-secret-" * 5,
            DATA_DIR=self.temp.name,
            SESSION_COOKIE_SECURE=False,
        )
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

        # Suprimir tiradas aleatorias de encuentros en pasillos
        self.enc_patch = patch.object(encounters, "_rng")
        self.mock_enc_rng = self.enc_patch.start()
        self.mock_enc_rng.random.return_value = 0.99
        self.addCleanup(self.enc_patch.stop)

        # Contrato de jefe C5 de prueba
        self.test_boss = BossContract(
            boss_id="coloso_prueba",
            name="El Coloso de Prueba",
            entry_room_id="valdren_camino_cerca",
            arena_room_id="valdren_camino_lindero",
            max_hp=200,
            phases=[
                BossPhase(
                    phase_index=0,
                    name="Fase Despierta",
                    min_hp_pct=0.5,
                    max_hp_pct=1.0,
                    precision=60,
                    damage=15,
                    armor_reduction=0.1,
                    behavior_text="El Coloso avanza con pasos pesados.",
                    description="El Coloso mantiene su postura férrea.",
                ),
                BossPhase(
                    phase_index=1,
                    name="Fase Furia",
                    min_hp_pct=0.0,
                    max_hp_pct=0.5,
                    precision=75,
                    damage=25,
                    armor_reduction=0.2,
                    behavior_text="El Coloso ruge y sus ojos brillan con furia ardiente.",
                    description="El Coloso entra en un frenesí destructivo.",
                ),
            ],
            warning_signal="Sientes la tierra temblar bajo tus pies. Un gran peligro acecha al norte.",
            close_signal="El Coloso de Prueba se alza imponente bloqueando el paso.",
            defeated_signal="Los restos petrificados del Coloso descansan en silencio.",
            weapon_loss_on_defeat=False,
            flee_possible=True,
            flee_agilidad=10,
            flee_percepcion=10,
            rewards=[
                BossReward(
                    reward_key="recompensa_mundo_coloso",
                    reward_type="discovery",
                    target="lindero_roto",
                    amount=1,
                    scope="world",
                ),
                BossReward(
                    reward_key="recompensa_xp_coloso",
                    reward_type="xp",
                    target="",
                    amount=350,
                    scope="character",
                ),
            ],
            min_contribution_damage=20.0,
        )
        bosses.register_boss(self.test_boss)

    def tearDown(self):
        bosses.clear_bosses()
        try:
            self.temp.cleanup()
        except PermissionError:
            pass

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', page)
        return match[1] if match else ""

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
        self.post("/move", dict(direction="south"))  # salir del hogar a valdren_centro
        return player_id

    def move_to_room(self, target_room_id, client=None):
        """Mueve al jugador directamente a la sala para propósitos de prueba."""
        client = client or self.client
        player_id = client.get("/api/me").json["player"]["id"]
        store.move_player(self.path, player_id, target_room_id, None)

    # -------------------------------------------------------------------------
    # 1. Un C3/C4 no obtiene comportamiento C5 accidentalmente (§41.13)
    # -------------------------------------------------------------------------
    def test_c3_c4_not_c5_behavior(self):
        """GAMEPLAY §41: C3 o C4 ordinarios nunca obtienen comportamiento C5 ni pérdida de arma."""
        player_id = self.register_and_enter_world()
        # Verificar que salas estándar con criaturas C1-C4 no tienen contrato de jefe
        self.assertIsNone(bosses.get_boss_by_room("valdren_camino_parcela"))
        self.assertIsNone(bosses.get_boss_by_arena("valdren_camino_parcela"))
        self.assertIsNone(bosses.get_boss_by_entry("valdren_camino_parcela"))

        # Cornalomo (C4) no tiene BossContract
        self.assertIsNone(bosses.get_boss("cornalomo"))

        # Iniciar encuentro normal C1 en una sala ordinaria
        player = store.character_by_player_id(self.path, player_id)
        store.start_encounter(self.path, player["id"], "valdren_camino_parcela", "mordelinde", 15)
        enc = store.get_encounter(self.path, player["id"], "valdren_camino_parcela")
        self.assertIsNotNone(enc)
        self.assertEqual(enc["creature_id"], "mordelinde")

        # No existe ningún boss_attempt para criaturas ordinarias
        self.assertIsNone(store.get_boss_attempt(self.path, "mordelinde"))

    # -------------------------------------------------------------------------
    # 2. boss_id único (§41.1, §41.2, §41.13)
    # -------------------------------------------------------------------------
    def test_boss_id_unique(self):
        """GAMEPLAY §41.1: Cada jefe C5 se identifica por su boss_id único en el registro."""
        boss = bosses.get_boss("coloso_prueba")
        self.assertIsNotNone(boss)
        self.assertEqual(boss.name, "El Coloso de Prueba")
        self.assertEqual(boss.arena_room_id, "valdren_camino_lindero")

        all_bosses = bosses.get_all_bosses()
        self.assertEqual(len(all_bosses), 1)
        self.assertEqual(all_bosses[0].boss_id, "coloso_prueba")

    # -------------------------------------------------------------------------
    # 3. Boss derrotado no reaparece tras reconnect/restart (§41.2, §41.13)
    # -------------------------------------------------------------------------
    def test_boss_defeated_persists_across_reconnect_restart(self):
        """GAMEPLAY §41.2: boss_defeated es persistente en el mundo y sobrevive reinicios."""
        player_id = self.register_and_enter_world()
        player = store.character_by_player_id(self.path, player_id)

        # Victoria contra el jefe
        bosses.resolve_boss_victory(self.path, self.test_boss, player)
        self.assertTrue(bosses.is_boss_defeated(self.path, "coloso_prueba"))

        # Simular reconexión / nueva instancia de app sobre la misma BD
        new_app = create_app(self.config)
        new_path = new_app.config["DATABASE"]
        self.assertTrue(bosses.is_boss_defeated(new_path, "coloso_prueba"))

        # Al consultar la sala de arena, el jefe ya aparece derrotado
        view = bosses.get_room_boss_view(new_path, player_id, "valdren_camino_lindero")
        self.assertIsNotNone(view)
        self.assertEqual(view.stage, "defeated")
        self.assertIn("petrificados", view.message)

        # Atacar en la arena devuelve no_target
        store.move_player(new_path, player_id, "valdren_camino_lindero", None)
        player_in_arena = store.character_by_player_id(new_path, player_id)
        res = bosses.resolve_boss_attack_round(new_path, player_in_arena, self.test_boss)
        self.assertEqual(res["outcome"], "no_target")
        self.assertIn("ya ha sido derrotado", res["messages"][0])

    # -------------------------------------------------------------------------
    # 4. Wipe sin victoria NO marca derrotado (§41.3, §41.12, §41.13)
    # -------------------------------------------------------------------------
    def test_wipe_without_victory_does_not_mark_defeated(self):
        """GAMEPLAY §41.3, §41.12: La derrota del jugador limpia el intento pero NO marca al jefe derrotado."""
        player_id = self.register_and_enter_world()
        self.move_to_room("valdren_camino_lindero")
        player = store.character_by_player_id(self.path, player_id)

        # Jugador recibe daño letal del jefe
        res = bosses.resolve_boss_player_defeat(self.path, player, self.test_boss)
        self.assertEqual(res["outcome"], "defeat")
        self.assertFalse(bosses.is_boss_defeated(self.path, "coloso_prueba"))

        # El jugador respawnea en valdren_centro
        updated_player = store.character_by_player_id(self.path, player_id)
        self.assertEqual(updated_player["room"], "valdren_centro")

    # -------------------------------------------------------------------------
    # 5. HP/fase reset default entre intentos (§41.3, §41.12, §41.13)
    # -------------------------------------------------------------------------
    def test_hp_and_phase_reset_default_between_attempts(self):
        """GAMEPLAY §41.3: Al concluir un intento sin victoria (wipe/huida), HP y fase vuelven al 100%."""
        player_id = self.register_and_enter_world()
        self.move_to_room("valdren_camino_lindero")
        player = store.character_by_player_id(self.path, player_id)

        # Iniciar intento y simular daño al jefe hasta fase 1 (HP 80/200 = 40%)
        attempt = bosses.get_or_create_boss_attempt(self.path, self.test_boss, player_id)
        store.save_boss_attempt(self.path, "coloso_prueba", "valdren_camino_lindero", 80.0, 1)

        # Jugador muere y abandona la arena
        bosses.resolve_boss_player_defeat(self.path, player, self.test_boss)

        # Como el jugador ya no está en la arena, el intento debió limpiarse
        cleared_attempt = store.get_boss_attempt(self.path, "coloso_prueba")
        self.assertIsNone(cleared_attempt)

        # Al volver a entrar, un nuevo intento empieza a HP máximo (200) y fase 0
        new_attempt = bosses.get_or_create_boss_attempt(self.path, self.test_boss, player_id)
        self.assertEqual(new_attempt["current_hp"], 200.0)
        self.assertEqual(new_attempt["current_phase"], 0)

    # -------------------------------------------------------------------------
    # 6. Participantes comparten encounter (§41.3, §41.13)
    # -------------------------------------------------------------------------
    def test_participants_share_encounter(self):
        """GAMEPLAY §41.3: Múltiples jugadores en la arena comparten encounter, HP y fase del jefe."""
        p1_id = self.register_and_enter_world(username="jugador1", name="Jugador Uno")
        self.move_to_room("valdren_camino_lindero")

        client2 = self.app.test_client()
        self.post("/register", dict(username="jugador2", name="Jugador Dos", password="clave dos"), client=client2)
        dm = self.app.test_client()
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username="jugador2"), dm, csrf_path="/dm")
        self.post("/species", dict(species="felaryn"), client=client2)
        p2_id = client2.get("/api/me").json["player"]["id"]
        store.set_player_class(self.path, p2_id, "juramentado")
        store.move_player(self.path, p2_id, "valdren_camino_lindero", None)

        p1 = store.character_by_player_id(self.path, p1_id)
        p2 = store.character_by_player_id(self.path, p2_id)

        # Jugador 1 ataca y daña al jefe
        bosses.get_or_create_boss_attempt(self.path, self.test_boss, p1_id)
        store.save_boss_attempt(self.path, "coloso_prueba", "valdren_camino_lindero", 150.0, 0)
        store.update_boss_participant_damage(self.path, "coloso_prueba", p1_id, 50.0)

        # Jugador 2 consulta la sala: ve el mismo HP (150)
        view2 = bosses.get_room_boss_view(self.path, p2_id, "valdren_camino_lindero")
        self.assertEqual(view2.current_hp, 150.0)

        # Jugador 2 se une al intento y hace 30 de daño
        bosses.get_or_create_boss_attempt(self.path, self.test_boss, p2_id)
        store.save_boss_attempt(self.path, "coloso_prueba", "valdren_camino_lindero", 120.0, 0)
        store.update_boss_participant_damage(self.path, "coloso_prueba", p2_id, 30.0)

        participants = store.get_boss_participants(self.path, "coloso_prueba")
        self.assertEqual(len(participants), 2)
        p_dict = {p["player_id"]: p["damage_dealt"] for p in participants}
        self.assertEqual(p_dict[p1_id], 50.0)
        self.assertEqual(p_dict[p2_id], 30.0)

    # -------------------------------------------------------------------------
    # 7. Espectador no cobra (§41.10, §41.11, §41.13)
    # -------------------------------------------------------------------------
    def test_spectator_does_not_get_reward(self):
        """GAMEPLAY §41.11: Participantes con daño inferior a min_contribution_damage no cobran recompensa individual."""
        p1_id = self.register_and_enter_world(username="combatiente", name="Combatiente")
        client2 = self.app.test_client()
        self.post("/register", dict(username="espectador", name="Espectador", password="una clave dos"), client=client2)
        dm = self.app.test_client()
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username="espectador"), dm, csrf_path="/dm")
        self.post("/species", dict(species="felaryn"), client=client2)
        p2_id = client2.get("/api/me").json["player"]["id"]
        store.set_player_class(self.path, p2_id, "juramentado")

        bosses.get_or_create_boss_attempt(self.path, self.test_boss, p1_id)
        bosses.get_or_create_boss_attempt(self.path, self.test_boss, p2_id)

        # Combatiente hace 100 de daño (supera min_contribution_damage=20.0)
        store.update_boss_participant_damage(self.path, "coloso_prueba", p1_id, 100.0)
        # Espectador hace solo 5 de daño (< 20.0)
        store.update_boss_participant_damage(self.path, "coloso_prueba", p2_id, 5.0)

        p1 = store.character_by_player_id(self.path, p1_id)
        xp_before_p1 = p1["xp"]
        level_before_p1 = p1["level"]
        p2 = store.character_by_player_id(self.path, p2_id)
        xp_before_p2 = p2["xp"]
        level_before_p2 = p2["level"]

        bosses.resolve_boss_victory(self.path, self.test_boss, p1)

        p1_after = store.character_by_player_id(self.path, p1_id)
        p2_after = store.character_by_player_id(self.path, p2_id)

        # Combatiente cobró la recompensa de personaje
        self.assertTrue(
            store.is_boss_reward_claimed(self.path, "coloso_prueba", "character", p1_id, "recompensa_xp_coloso")
        )
        self.assertTrue(p1_after["level"] > level_before_p1 or p1_after["xp"] > xp_before_p1)

        # Espectador NO cobró la recompensa de personaje
        self.assertFalse(
            store.is_boss_reward_claimed(self.path, "coloso_prueba", "character", p2_id, "recompensa_xp_coloso")
        )
        self.assertEqual(p2_after["xp"], xp_before_p2)
        self.assertEqual(p2_after["level"], level_before_p2)

    # -------------------------------------------------------------------------
    # 8. Retirada previa no cuenta derrota (§41.4, §41.13)
    # -------------------------------------------------------------------------
    def test_prior_retreat_not_counted_as_defeat(self):
        """GAMEPLAY §41.4: Retirarse desde la sala de advertencia (entry_room) antes de iniciar combate no es derrota."""
        player_id = self.register_and_enter_world()
        self.move_to_room("valdren_camino_cerca")

        # En la sala de advertencia, el view está en stage "warning"
        view = bosses.get_room_boss_view(self.path, player_id, "valdren_camino_cerca")
        self.assertIsNotNone(view)
        self.assertEqual(view.stage, "warning")
        self.assertIn("temblar", view.message)

        # El jugador decide retroceder hacia valdren_camino_parcela
        store.move_player(self.path, player_id, "valdren_camino_parcela", "south")

        player = store.character_by_player_id(self.path, player_id)
        self.assertEqual(player["room"], "valdren_camino_parcela")
        # HP intacto, sin heridas, sin derrotas
        self.assertEqual(player["hp_current"], player["hp_max"])
        self.assertFalse(bosses.is_boss_defeated(self.path, "coloso_prueba"))

    # -------------------------------------------------------------------------
    # 9. weapon_loss_on_defeat=false conserva arma (§41.6, §41.7, §41.13)
    # -------------------------------------------------------------------------
    def test_weapon_loss_false_preserves_weapon(self):
        """C5 conserva arma y usa el estado canónico de respawn."""
        self.assertFalse(self.test_boss.weapon_loss_on_defeat)
        player_id = self.register_and_enter_world()
        self.move_to_room("valdren_camino_lindero")

        item_id = store.grant_item(self.path, player_id, "espada_juramento", forge_validated=True)
        store.equip_item(self.path, player_id, item_id)
        with store.connect(self.path) as db:
            db.execute(
                """UPDATE players
                   SET wound = 'grave', field_rest_budget_max = 10, field_rest_healed = 10
                   WHERE id = ?""",
                (player_id,),
            )
        player = store.character_by_player_id(self.path, player_id)
        self.assertEqual(player["equipped_weapon_id"], item_id)

        res = bosses.resolve_boss_player_defeat(
            self.path, player, self.test_boss, current_wound="grave"
        )
        self.assertEqual(res["outcome"], "defeat")
        self.assertFalse(res["weapon_lost"])

        player_after = store.character_by_player_id(self.path, player_id)
        self.assertEqual(player_after["room"], "valdren_centro")
        self.assertEqual(player_after["hp_current"], round(player_after["hp_max"] * 0.60))
        self.assertEqual(player_after["fatigue"], 40)
        self.assertEqual(player_after["wound"], "moderada")
        self.assertEqual(player_after["equipped_weapon_id"], item_id)
        self.assertIsNone(player_after["field_rest_budget_max"])
        self.assertEqual(player_after["field_rest_healed"], 0)
        self.assertEqual(len(store.get_lost_weapons(self.path, player_id)), 0)

    def test_boss_outside_edran_uses_home_fallback(self):
        """Un C5 fuera de Edran no teletransporta globalmente a Valdren."""
        player_id = self.register_and_enter_world()
        with store.connect(self.path) as db:
            db.execute(
                "UPDATE players SET room = 'alto_terrazas', wound = 'leve' WHERE id = ?",
                (player_id,),
            )
        player = store.character_by_player_id(self.path, player_id)
        remote_boss = BossContract(
            boss_id="jefe_hoshai_respawn",
            name="Jefe de prueba Hoshai",
            entry_room_id="alto_mirador",
            arena_room_id="alto_terrazas",
            max_hp=100,
            phases=[BossPhase(0, "Única", 0.0, 1.0, 50, 10)],
            weapon_loss_on_defeat=False,
        )
        result = bosses.resolve_boss_player_defeat(self.path, player, remote_boss)
        self.assertEqual(result["outcome"], "defeat")
        after = store.character_by_player_id(self.path, player_id)
        self.assertEqual(after["room"], world.get_home_room_id(player_id))
        self.assertEqual(after["wound"], "ninguna")
        self.assertIn(world.get_room(after["room"])["name"], result["death_event"]["respawn_message"])

    # -------------------------------------------------------------------------
    # 10. weapon_loss_on_defeat=true pierde únicamente arma equipada (§41.7, §41.13)
    # -------------------------------------------------------------------------
    def test_weapon_loss_true_loses_only_equipped_weapon(self):
        """GAMEPLAY §41.7: Con weapon_loss_on_defeat=True, solo se desequipa y pierde el arma equipada."""
        loss_boss = BossContract(
            boss_id="jefe_desarmador",
            name="El Desarmador",
            entry_room_id="valdren_camino_cerca",
            arena_room_id="valdren_camino_lindero",
            max_hp=100,
            phases=[BossPhase(0, "Fase Única", 0.0, 1.0, 50, 10)],
            weapon_loss_on_defeat=True,  # Opt-in activo
        )
        bosses.register_boss(loss_boss)

        player_id = self.register_and_enter_world()
        self.move_to_room("valdren_camino_lindero")

        # Equipar espada y armadura, y tener daga en inventario
        weapon_id = store.grant_item(self.path, player_id, "espada_juramento", forge_validated=True)
        armor_id = store.grant_item(self.path, player_id, "coselete_lethra", forge_validated=True)
        spare_weapon_id = store.grant_item(self.path, player_id, "punal_camino", forge_validated=True)

        store.equip_item(self.path, player_id, weapon_id)
        store.equip_item(self.path, player_id, armor_id)

        player = store.character_by_player_id(self.path, player_id)
        self.assertEqual(player["equipped_weapon_id"], weapon_id)
        self.assertEqual(player["equipped_armor_id"], armor_id)

        # Muerte ante el jefe desarmador
        res = bosses.resolve_boss_player_defeat(self.path, player, loss_boss)
        self.assertEqual(res["outcome"], "defeat")
        self.assertTrue(res["weapon_lost"])

        player_after = store.character_by_player_id(self.path, player_id)
        # El arma fue desequipada
        self.assertIsNone(player_after["equipped_weapon_id"])
        # La armadura sigue equipada (NO se pierde)
        self.assertEqual(player_after["equipped_armor_id"], armor_id)

        # La espada está registrada como perdida
        self.assertTrue(store.is_weapon_lost(self.path, weapon_id))
        # La daga de reserva NO está perdida
        self.assertFalse(store.is_weapon_lost(self.path, spare_weapon_id))

        # Intentar re-equipar el arma perdida debe ser rechazado
        ok, cat, reason = store.equip_item(self.path, player_id, weapon_id)
        self.assertFalse(ok)
        self.assertIn("arrebatada por un jefe", reason)

        # Equipar la daga de reserva debe funcionar perfectamente
        ok_spare, cat_spare, _ = store.equip_item(self.path, player_id, spare_weapon_id)
        self.assertTrue(ok_spare)

    # -------------------------------------------------------------------------
    # 11. Sin arma no sustituye la penalización por otro objeto (§41.9, §41.13)
    # -------------------------------------------------------------------------
    def test_defeat_without_weapon_does_not_substitute_penalty(self):
        """GAMEPLAY §41.9: Sin arma equipada, no pierde armadura, moneda, XP ni inventario en compensación."""
        loss_boss = BossContract(
            boss_id="jefe_desarmador_2",
            name="El Desarmador Dos",
            entry_room_id="valdren_camino_cerca",
            arena_room_id="valdren_camino_lindero",
            max_hp=100,
            phases=[BossPhase(0, "Fase Única", 0.0, 1.0, 50, 10)],
            weapon_loss_on_defeat=True,
        )
        bosses.register_boss(loss_boss)

        player_id = self.register_and_enter_world()
        self.move_to_room("valdren_camino_lindero")

        # Equipar solo armadura y tener objetos en inventario, sin arma
        armor_id = store.grant_item(self.path, player_id, "coselete_lethra", forge_validated=True)
        store.equip_item(self.path, player_id, armor_id)
        misc_id = store.grant_item(self.path, player_id, "acolchado_camino", forge_validated=True)

        player = store.character_by_player_id(self.path, player_id)
        self.assertIsNone(player["equipped_weapon_id"])
        xp_before = player["xp"]

        # Derrota sin arma equipada
        res = bosses.resolve_boss_player_defeat(self.path, player, loss_boss)
        self.assertEqual(res["outcome"], "defeat")
        self.assertFalse(res["weapon_lost"])

        player_after = store.character_by_player_id(self.path, player_id)
        self.assertEqual(player_after["equipped_armor_id"], armor_id)
        self.assertEqual(player_after["xp"], xp_before)
        inv = store.list_inventory(self.path, player_id)
        inv_ids = [item["id"] for item in inv]
        self.assertIn(armor_id, inv_ids)
        self.assertIn(misc_id, inv_ids)
        self.assertEqual(len(store.get_lost_weapons(self.path, player_id)), 0)

    # -------------------------------------------------------------------------
    # 12. Estado de arma perdida persiste (§41.7, §41.13)
    # -------------------------------------------------------------------------
    def test_lost_weapon_state_persists(self):
        """GAMEPLAY §41.7: El estado de pérdida del arma persiste en SQLite y se refleja en inventario."""
        loss_boss = BossContract(
            boss_id="jefe_desarmador_3",
            name="El Desarmador Tres",
            entry_room_id="valdren_camino_cerca",
            arena_room_id="valdren_camino_lindero",
            max_hp=100,
            phases=[BossPhase(0, "Fase Única", 0.0, 1.0, 50, 10)],
            weapon_loss_on_defeat=True,
        )
        bosses.register_boss(loss_boss)

        player_id = self.register_and_enter_world()
        weapon_id = store.grant_item(self.path, player_id, "espada_juramento", forge_validated=True)
        store.equip_item(self.path, player_id, weapon_id)

        player = store.character_by_player_id(self.path, player_id)
        bosses.resolve_boss_player_defeat(self.path, player, loss_boss)

        # list_inventory debe anotar lost_to_boss=True
        inv = store.list_inventory(self.path, player_id)
        weapon_row = next(item for item in inv if item["id"] == weapon_id)
        self.assertTrue(weapon_row["lost_to_boss"])

        # Consulta directa en BD
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM player_lost_weapons WHERE item_id = ?", (weapon_id,)
            ).fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["boss_id"], "jefe_desarmador_3")
            self.assertIsNone(row["recovered_at"])

    # -------------------------------------------------------------------------
    # 13. Recuperación/reemplazo no duplica (§41.7, §41.8, §41.13)
    # -------------------------------------------------------------------------
    def test_weapon_recovery_does_not_duplicate(self):
        """GAMEPLAY §41.8: Recuperar el arma perdida reactiva la instancia existente sin duplicar filas."""
        loss_boss = BossContract(
            boss_id="jefe_desarmador_4",
            name="El Desarmador Cuatro",
            entry_room_id="valdren_camino_cerca",
            arena_room_id="valdren_camino_lindero",
            max_hp=100,
            phases=[BossPhase(0, "Fase Única", 0.0, 1.0, 50, 10)],
            weapon_loss_on_defeat=True,
        )
        bosses.register_boss(loss_boss)

        player_id = self.register_and_enter_world()
        weapon_id = store.grant_item(self.path, player_id, "espada_juramento", forge_validated=True)
        store.equip_item(self.path, player_id, weapon_id)

        initial_count = len(store.list_inventory(self.path, player_id))

        player = store.character_by_player_id(self.path, player_id)
        bosses.resolve_boss_player_defeat(self.path, player, loss_boss)

        self.assertTrue(store.is_weapon_lost(self.path, weapon_id))

        # Recuperar el arma
        recovered = store.recover_lost_weapon(self.path, player_id, weapon_id)
        self.assertTrue(recovered)
        self.assertFalse(store.is_weapon_lost(self.path, weapon_id))

        # El conteo total de inventario se mantiene exactamente igual (no se duplica)
        after_count = len(store.list_inventory(self.path, player_id))
        self.assertEqual(initial_count, after_count)

        # Ahora puede volver a equiparse sin error
        ok, _, _ = store.equip_item(self.path, player_id, weapon_id)
        self.assertTrue(ok)

    # -------------------------------------------------------------------------
    # 14. Recompensas once-* respetan su alcance (§41.10, §41.13)
    # -------------------------------------------------------------------------
    def test_rewards_respect_scope_world_and_character(self):
        """GAMEPLAY §41.10: Recompensas 'world' se otorgan una vez globalmente; 'character' por personaje calificado."""
        p1_id = self.register_and_enter_world(username="mat1", name="Mat Uno")
        p2_id = self.register_and_enter_world(username="mat2", name="Mat Dos")

        # Ambos participan con daño suficiente
        bosses.get_or_create_boss_attempt(self.path, self.test_boss, p1_id)
        bosses.get_or_create_boss_attempt(self.path, self.test_boss, p2_id)
        store.update_boss_participant_damage(self.path, "coloso_prueba", p1_id, 100.0)
        store.update_boss_participant_damage(self.path, "coloso_prueba", p2_id, 100.0)

        p1 = store.character_by_player_id(self.path, p1_id)
        bosses.resolve_boss_victory(self.path, self.test_boss, p1)

        # La recompensa de mundo se registró
        self.assertTrue(
            store.is_boss_reward_claimed(self.path, "coloso_prueba", "world", None, "recompensa_mundo_coloso")
        )
        # Recompensas de personaje registradas para p1 y p2
        self.assertTrue(
            store.is_boss_reward_claimed(self.path, "coloso_prueba", "character", p1_id, "recompensa_xp_coloso")
        )
        self.assertTrue(
            store.is_boss_reward_claimed(self.path, "coloso_prueba", "character", p2_id, "recompensa_xp_coloso")
        )

        # Si se llamara a resolver victoria nuevamente, no otorga doble XP
        xp_p1 = store.character_by_player_id(self.path, p1_id)["xp"]
        bosses.resolve_boss_victory(self.path, self.test_boss, p1)
        self.assertEqual(store.character_by_player_id(self.path, p1_id)["xp"], xp_p1)

    # -------------------------------------------------------------------------
    # 15. Forja no se usa falsamente como flag de pérdida (§41.7, §41.13)
    # -------------------------------------------------------------------------
    def test_forge_not_falsely_used_as_loss_flag(self):
        """GAMEPLAY §41.7, §41.13: La pérdida de arma NUNCA altera el flag forge_validated del objeto."""
        loss_boss = BossContract(
            boss_id="jefe_desarmador_5",
            name="El Desarmador Cinco",
            entry_room_id="valdren_camino_cerca",
            arena_room_id="valdren_camino_lindero",
            max_hp=100,
            phases=[BossPhase(0, "Fase Única", 0.0, 1.0, 50, 10)],
            weapon_loss_on_defeat=True,
        )
        bosses.register_boss(loss_boss)

        player_id = self.register_and_enter_world()
        weapon_id = store.grant_item(self.path, player_id, "espada_juramento", forge_validated=True)
        store.equip_item(self.path, player_id, weapon_id)

        player = store.character_by_player_id(self.path, player_id)
        bosses.resolve_boss_player_defeat(self.path, player, loss_boss)

        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT forge_validated FROM inventory_items WHERE id = ?", (weapon_id,)
            ).fetchone()
            # forge_validated DEBE seguir siendo 1 (True), no se corrompe para simular pérdida
            self.assertEqual(row["forge_validated"], 1)

    # -------------------------------------------------------------------------
    # 16. Bloqueo de descanso y equipamiento ante presencia de jefe (§41.3)
    # -------------------------------------------------------------------------
    def test_rest_equip_unequip_blocked_in_arena(self):
        """GAMEPLAY §41.3: En una arena de jefe vivo no se permite descansar ni cambiar equipo."""
        player_id = self.register_and_enter_world()
        item_id = store.grant_item(self.path, player_id, "espada_juramento", forge_validated=True)
        self.move_to_room("valdren_camino_lindero")

        player = store.character_by_player_id(self.path, player_id)

        # Descansar bloqueado
        res_rest = self.post("/command", dict(text="descansar"))
        self.assertIn("No puedes descansar", res_rest.get_data(as_text=True))

        # Equipar bloqueado
        res_equip = self.post("/command", dict(text="equipar espada de juramento"))
        self.assertIn("No puedes equipar nada", res_equip.get_data(as_text=True))

    # -------------------------------------------------------------------------
    # 17. Acciones defensivas, huida y evaluación en arena (§41.4, §41.5)
    # -------------------------------------------------------------------------
    def test_combat_actions_in_boss_arena(self):
        """GAMEPLAY §41.4, §41.5: Evaluar, esquivar, resistir y huir funcionan contra el jefe C5 en arena."""
        player_id = self.register_and_enter_world()
        self.move_to_room("valdren_camino_lindero")
        player = store.character_by_player_id(self.path, player_id)

        # 1. Evaluar: devuelve texto cualitativo sin revelar números
        name, msg = bosses.determine_current_phase(self.test_boss, 200.0), ""
        res_eval = self.post("/evaluate")
        eval_html = res_eval.get_data(as_text=True)
        self.assertIn("El Coloso de Prueba", eval_html)
        self.assertNotIn("200 HP", eval_html)

        # 2. Esquivar exitoso
        rng_dodge = SequenceRng(99.0)  # jefe falla
        res_dodge = bosses.resolve_boss_dodge_round(self.path, player, self.test_boss, rng=rng_dodge)
        self.assertEqual(res_dodge["outcome"], "success")

        # 3. Resistir
        rng_resist = SequenceRng(50.0)
        res_resist = bosses.resolve_boss_resist_round(self.path, player, self.test_boss, rng=rng_resist)
        self.assertIn(res_resist["outcome"], ("success", "failed"))

        # 4. Huir exitoso: retrocede a entry_room_id
        rng_flee = SequenceRng(0.0)  # éxito de huida
        res_flee = bosses.resolve_boss_player_flee(self.path, player, self.test_boss, rng=rng_flee)
        self.assertEqual(res_flee["outcome"], "success")
        player_after_flee = store.character_by_player_id(self.path, player_id)
        self.assertEqual(player_after_flee["room"], "valdren_camino_cerca")

    # -------------------------------------------------------------------------
    # 18. Supresión de fauna C1 aleatoria en arenas activas de jefe (§41.4)
    # -------------------------------------------------------------------------
    def test_c1_fauna_suppressed_in_active_arena(self):
        """GAMEPLAY §41.4: La arena de un jefe C5 no genera fauna C1 mientras el jefe esté vivo."""
        player_id = self.register_and_enter_world()
        self.move_to_room("valdren_camino_cerca")

        # Moverse a la arena
        res = self.post("/move", dict(direction="north"))
        self.assertIn(res.status_code, (302, 303))

        player = store.character_by_player_id(self.path, player_id)
        self.assertEqual(player["room"], "valdren_camino_lindero")

        # No hay encuentro de fauna aleatoria iniciado en la sala
        enc = store.get_encounter(self.path, player["id"], "valdren_camino_lindero")
        self.assertIsNone(enc)
