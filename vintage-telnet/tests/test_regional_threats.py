"""Pruebas del motor reusable de amenazas regionales C3 v1 (GAMEPLAY §40 / Issue #335).

Cubre rigurosamente los 12 criterios de §40.11 y los perfiles de REGIONAL_THREAT_PROFILES.md:
1. Perfiles autoritativos exactos y prepared_actions de las 5 amenazas C3.
2. Exclusión estricta de pools C1 ordinarios (GAMEPLAY §40.5).
3. Configuración y registro de zonas de amenaza con threat_zone_id (§40.1).
4. No C3 desde estado 'unknown' (§40.3).
5. Warning obligatorio precede a 'close' (§40.3).
6. Proximidad crítica ('close') no inicia combate forzado; ofrece decisión (§40.4).
7. Tirada especial según modo de presencia y roll fallido conserva rastro (§40.5).
8. Acción 'evitar' / retroceso funciona y activa cooldown de 30 minutos (§40.4, §40.6).
9. Cooldown anti-spam de 30 minutos reales tras evitar, huir, vencer, morir o abandonar (§40.6).
10. Cooldown evita re-roll al entrar y salir; persistencia en base de datos (§40.6, §40.11).
11. Derrota en combate C3 conserva equipo e inventario (§40.9).
12. Aislamiento de estados por personaje y por zona (§40.10, §40.11).
"""

import os
from pathlib import Path
import random
import re
import tempfile
import time
import unittest
from unittest.mock import patch

from server import combat, creatures, encounters, store, threats, world
from server.app import create_app


class FixedRng:
    """Generador pseudoaleatorio determinista para pruebas."""
    def __init__(self, value: float):
        self._val = value

    def random(self) -> float:
        return self._val

    def uniform(self, a: float, b: float) -> float:
        return self._val


class RegionalThreatProfilesTests(unittest.TestCase):
    """1. Perfiles canónicos según REGIONAL_THREAT_PROFILES.md."""

    def test_all_five_threats_exist_with_exact_stats(self):
        expected = {
            "cornalomo": {
                "name": "Cornalomo",
                "family": "cornalomo",
                "reference_level": 8,
                "hp": 120,
                "precision": 65,
                "damage": 20,
                "armor_reduction": 0.20,
            },
            "rasgacumbres": {
                "name": "Rasgacumbres",
                "family": "rasgacumbres",
                "reference_level": 9,
                "hp": 110,
                "precision": 70,
                "damage": 22,
                "armor_reduction": 0.10,
                "flee_agilidad": 18,
                "flee_percepcion": 17,
            },
            "quebrarrocas": {
                "name": "Quebrarrocas",
                "family": "quebrarrocas",
                "reference_level": 10,
                "hp": 150,
                "precision": 55,
                "damage": 24,
                "armor_reduction": 0.30,
                "flee_agilidad": 8,
                "flee_percepcion": 11,
            },
            "dorsalodo": {
                "name": "Dorsalodo",
                "family": "dorsalodo",
                "reference_level": 10,
                "hp": 135,
                "precision": 62,
                "damage": 24,
                "armor_reduction": 0.15,
                "flee_agilidad": 12,
                "flee_percepcion": 16,
            },
            "rasgacorteza": {
                "name": "Rasgacorteza",
                "family": "rasgacorteza",
                "reference_level": 10,
                "hp": 145,
                "precision": 60,
                "damage": 25,
                "armor_reduction": 0.25,
                "flee_agilidad": 10,
                "flee_percepcion": 17,
            },
        }

        for cid, stats in expected.items():
            c = creatures.get_creature(cid)
            self.assertIsNotNone(c, f"Falta criatura {cid}")
            for field_name, expected_value in stats.items():
                self.assertEqual(
                    c.get(field_name), expected_value,
                    f"Divergencia en {cid}.{field_name}: {c.get(field_name)} != {expected_value}"
                )

    def test_prepared_actions_conform_to_profiles_and_sec36(self):
        """Acciones preparadas v1 de Rasgacumbres, Quebrarrocas, Dorsalodo y Rasgacorteza."""
        # Rasgacumbres: rasgacumbres_descenso
        rg = creatures.get_creature("rasgacumbres")["prepared_action"]
        self.assertEqual(rg["id"], "rasgacumbres_descenso")
        self.assertFalse(rg["frontal"])
        self.assertTrue(rg["interruptible"])
        self.assertEqual(rg["precision"], 76)
        self.assertEqual(rg["damage"], 30)

        # Quebrarrocas: quebrarrocas_empuje
        qr = creatures.get_creature("quebrarrocas")["prepared_action"]
        self.assertEqual(qr["id"], "quebrarrocas_empuje")
        self.assertTrue(qr["frontal"])
        self.assertTrue(qr["interruptible"])
        self.assertEqual(qr["precision"], 64)
        self.assertEqual(qr["damage"], 34)

        # Dorsalodo: dorsalodo_arremetida
        dl = creatures.get_creature("dorsalodo")["prepared_action"]
        self.assertEqual(dl["id"], "dorsalodo_arremetida")
        self.assertTrue(dl["frontal"])
        self.assertTrue(dl["interruptible"])
        self.assertEqual(dl["precision"], 72)
        self.assertEqual(dl["damage"], 32)

        # Rasgacorteza: rasgacorteza_arremetida
        rc = creatures.get_creature("rasgacorteza")["prepared_action"]
        self.assertEqual(rc["id"], "rasgacorteza_arremetida")
        self.assertTrue(rc["frontal"])
        self.assertTrue(rc["interruptible"])
        self.assertEqual(rc["precision"], 68)
        self.assertEqual(rc["damage"], 35)

    def test_c3_threats_evaluate_abrumador_for_level_1_character(self):
        """Banda de dificultad: todas las amenazas C3 evalúan 'abrumador' para nivel 1 sano."""
        cg_p1 = combat.competencia_general(1)
        player_dps = combat.expected_dps(10, 10, 10, cg_p1, combat.competencia_general(1), base_arma=10)
        player_hp = 30  # humano base

        for cid in encounters.C3_THREAT_IDS:
            c = creatures.get_creature(cid)
            enemy_dps = combat.fixed_expected_dps(c["precision"], c["damage"])
            category = combat.encounter_category(player_dps, player_hp, enemy_dps, c["hp"])
            self.assertEqual(
                category, "abrumador",
                f"{cid} evaluó como {category}, se esperaba 'abrumador' contra nivel 1"
            )

    def test_c1_pool_integrity_rejects_all_c3_threats(self):
        """GAMEPLAY §40.5: C3 nunca entra en el pool C1 de §33."""
        for cid in encounters.C3_THREAT_IDS:
            bad_pool = {
                "test_pool": {
                    "rooms": {"valdren_sendero"},
                    "chance": 0.20,
                    "creatures": [(cid, 100)],
                }
            }
            with self.assertRaises(encounters.InvalidPoolConfig):
                encounters.validate_pools(bad_pool)


class RegionalThreatEngineUnitTests(unittest.TestCase):
    """2. Pruebas unitarias de threats.py y persistencia en store.py."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "test_threats.sqlite3")
        store.initialize(self.db_path)
        threats.clear_threat_zones()

        self.player_id = "test_player_threat_1"
        now = store.utcnow()
        with store.connect(self.db_path) as db:
            db.execute("INSERT INTO accounts (id, username, password_hash, created_at) VALUES ('a1', 'u1', 'p1', ?)", (now,))
            db.execute(
                """INSERT INTO players (id, account_id, username, name, name_key, password_hash, room,
                                       hp_current, hp_max, fatigue, wound, status, created_at, last_access_at)
                   VALUES (?, 'a1', 'u1', 'Heroe', 'heroe', '', 'valdren_centro', 30, 30, 0, 'ninguna', 'approved', ?, ?)""",
                (self.player_id, now, now)
            )

    def tearDown(self):
        threats.load_canonical_threat_zones()
        self.temp_dir.cleanup()

    def test_threat_zone_registration_and_lookup(self):
        zone = threats.ThreatZone(
            threat_zone_id="tz_test_zone",
            region="test_region",
            creature_id="rasgacumbres",
            warning_rooms={"room_warn_1", "room_warn_2"},
            encounter_rooms={"room_enc_1"},
            cooldown_seconds=1800.0,
            presence_mode="threat_rare",
        )
        threats.register_threat_zone(zone)
        self.assertEqual(threats.get_threat_zone("tz_test_zone"), zone)
        self.assertIn(zone, threats.get_threat_zones_for_room("room_warn_1"))
        self.assertIn(zone, threats.get_threat_zones_for_room("room_enc_1"))
        self.assertEqual(threats.get_threat_zones_for_room("room_unrelated"), [])

    def test_no_c3_from_unknown_state(self):
        """Criterio §40.3 / §40.11: NUNCA inicia C3 desde 'unknown'."""
        zone = threats.ThreatZone(
            threat_zone_id="tz_korven_test",
            region="korven",
            creature_id="quebrarrocas",
            warning_rooms={"room_warn"},
            encounter_rooms={"room_enc"},
            presence_mode="threat_scripted",
        )
        threats.register_threat_zone(zone)

        # Jugador entra directamente a encounter_room sin haber pasado por warning_rooms
        eval_result = threats.evaluate_room_threat(self.db_path, self.player_id, "room_enc")
        self.assertIsNotNone(eval_result)
        self.assertEqual(eval_result.stage, "none")
        self.assertFalse(eval_result.close_encounter)

        # Estado en BD debe permanecer unknown
        rec = store.get_threat_state(self.db_path, self.player_id, "tz_korven_test")
        self.assertIsNone(rec)

    def test_warning_precedes_close_and_updates_db(self):
        """Criterio §40.3 / §40.11: warning precede a close."""
        zone = threats.ThreatZone(
            threat_zone_id="tz_edran_test",
            region="edran",
            creature_id="cornalomo",
            warning_rooms={"room_warn"},
            encounter_rooms={"room_enc"},
            presence_mode="threat_scripted",
            warning_signal="Hierba aplastada y temblor leve.",
            close_signal="Cornalomo te mira desafiante.",
        )
        threats.register_threat_zone(zone)

        # 1. Entrada a sala de advertencia
        warn_eval = threats.evaluate_room_threat(self.db_path, self.player_id, "room_warn")
        self.assertEqual(warn_eval.stage, "warning")
        self.assertEqual(warn_eval.message, "Hierba aplastada y temblor leve.")
        self.assertFalse(warn_eval.close_encounter)

        rec = store.get_threat_state(self.db_path, self.player_id, "tz_edran_test")
        self.assertIsNotNone(rec)
        self.assertEqual(rec["state"], "warned")

        # 2. Ahora entra a encounter_room: con presencia scripted, pasa a 'close'
        enc_eval = threats.evaluate_room_threat(self.db_path, self.player_id, "room_enc")
        self.assertEqual(enc_eval.stage, "close")
        self.assertTrue(enc_eval.close_encounter)
        self.assertEqual(enc_eval.message, "Cornalomo te mira desafiante.")
        self.assertEqual(len(enc_eval.available_actions), 3)

        rec2 = store.get_threat_state(self.db_path, self.player_id, "tz_edran_test")
        self.assertEqual(rec2["state"], "close")

    def test_failed_roll_in_warned_zone_does_not_erase_tracks(self):
        """Criterio §40.5 / §40.11: roll fallido no borra rastros."""
        zone = threats.ThreatZone(
            threat_zone_id="tz_lethra_test",
            region="lethra",
            creature_id="dorsalodo",
            warning_rooms={"room_warn"},
            encounter_rooms={"room_enc"},
            presence_mode="threat_rare",  # 10%
        )
        threats.register_threat_zone(zone)

        # Advertir al jugador
        threats.evaluate_room_threat(self.db_path, self.player_id, "room_warn")

        # Roll de 0.50 (> 0.10 chance): debe fallar la aparición
        enc_eval = threats.evaluate_room_threat(
            self.db_path, self.player_id, "room_enc", rng=FixedRng(0.50)
        )
        self.assertEqual(enc_eval.stage, "warning")
        self.assertFalse(enc_eval.close_encounter)
        self.assertIn("Señales frescas", enc_eval.message)

        # Estado en BD sigue siendo 'warned', no se borra
        rec = store.get_threat_state(self.db_path, self.player_id, "tz_lethra_test")
        self.assertEqual(rec["state"], "warned")

    def test_avoid_activates_cooldown_and_prevents_reroll(self):
        """Criterio §40.4, §40.6, §40.11: evitar funciona y activa cooldown de 30 min."""
        zone = threats.ThreatZone(
            threat_zone_id="tz_nhal_test",
            region="nhal",
            creature_id="rasgacorteza",
            warning_rooms={"room_warn"},
            encounter_rooms={"room_enc"},
            presence_mode="threat_scripted",
            cooldown_seconds=1800.0,
            inactive_trail_signal="Huellas viejas pero la criatura no está.",
        )
        threats.register_threat_zone(zone)

        now = 1000.0
        # Advertir y entrar en close
        threats.evaluate_room_threat(self.db_path, self.player_id, "room_warn", now=now)
        threats.evaluate_room_threat(self.db_path, self.player_id, "room_enc", now=now)

        # Ejecutar 'evitar' / retroceso
        cooldown_until = threats.resolve_threat_avoid(self.db_path, self.player_id, "tz_nhal_test", now=now)
        self.assertEqual(cooldown_until, 1000.0 + 1800.0)

        # BD debe persistir resolved y cooldown_until
        rec = store.get_threat_state(self.db_path, self.player_id, "tz_nhal_test")
        self.assertEqual(rec["state"], "resolved")
        self.assertEqual(rec["cooldown_until"], 2800.0)

        # Re-entrar / salir / re-roll durante cooldown: NO reaparece la criatura
        for step_now in (1010.0, 1500.0, 2799.0):
            eval_during_cd = threats.evaluate_room_threat(
                self.db_path, self.player_id, "room_enc", now=step_now
            )
            self.assertEqual(eval_during_cd.stage, "cooldown")
            self.assertTrue(eval_during_cd.cooldown_active)
            self.assertFalse(eval_during_cd.close_encounter)
            self.assertEqual(eval_during_cd.message, "Huellas viejas pero la criatura no está.")

        # Tras expirar cooldown (> 2800): el cooldown ya no bloquea
        eval_expired = threats.evaluate_room_threat(
            self.db_path, self.player_id, "room_warn", now=2801.0
        )
        self.assertEqual(eval_expired.stage, "warning")

    def test_state_isolation_between_distinct_players_and_zones(self):
        """Criterio §40.11: amenaza distinta y jugadores distintos mantienen estado aislado."""
        p2_id = "test_player_threat_2"
        now = store.utcnow()
        with store.connect(self.db_path) as db:
            db.execute(
                """INSERT INTO players (id, account_id, username, name, name_key, password_hash, room,
                                       hp_current, hp_max, fatigue, wound, status, created_at, last_access_at)
                   VALUES (?, 'a1', 'u2', 'Companero', 'companero', '', 'valdren_centro', 30, 30, 0, 'ninguna', 'approved', ?, ?)""",
                (p2_id, now, now)
            )

        zone_edran = threats.ThreatZone("tz_edran", "edran", "cornalomo", {"w_edran"}, {"e_edran"})
        zone_korven = threats.ThreatZone("tz_korven", "korven", "quebrarrocas", {"w_korven"}, {"e_korven"})
        threats.register_threat_zone(zone_edran)
        threats.register_threat_zone(zone_korven)

        now = 500.0
        # Jugador 1 es advertido y entra en cooldown en Edran
        threats.evaluate_room_threat(self.db_path, self.player_id, "w_edran", now=now)
        threats.resolve_threat_avoid(self.db_path, self.player_id, "tz_edran", now=now)

        # Jugador 2 en Edran sigue en unknown
        self.assertIsNone(store.get_threat_state(self.db_path, p2_id, "tz_edran"))

        # Jugador 1 en Korven sigue en unknown
        self.assertIsNone(store.get_threat_state(self.db_path, self.player_id, "tz_korven"))

        # Advertir a Jugador 1 en Korven no afecta el cooldown de Edran
        threats.evaluate_room_threat(self.db_path, self.player_id, "w_korven", now=now)
        rec_korven = store.get_threat_state(self.db_path, self.player_id, "tz_korven")
        self.assertEqual(rec_korven["state"], "warned")
        self.assertIsNone(rec_korven["cooldown_until"])

        rec_edran = store.get_threat_state(self.db_path, self.player_id, "tz_edran")
        self.assertEqual(rec_edran["state"], "resolved")
        self.assertEqual(rec_edran["cooldown_until"], 2300.0)


@patch.dict(os.environ, {"VT_DM_PASSWORD": "dm-secret-value"})
class RegionalThreatIntegrationTests(unittest.TestCase):
    """3. Pruebas de integración HTTP / Flask / Motor de combate C3."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config = dict(
            TESTING=True,
            SECRET_KEY="test-secret-" * 5,
            DATA_DIR=self.temp_dir.name,
            SESSION_COOKIE_SECURE=False,
        )
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.db_path = self.app.config["DATABASE"]

        # Controlar rng de encuentros aleatorios para que no interfieran en salas de paso
        self.enc_patch = patch.object(encounters, "_rng")
        self.mock_enc_rng = self.enc_patch.start()
        self.mock_enc_rng.random.return_value = 0.50
        self.addCleanup(self.enc_patch.stop)

        # Configurar zona C3 de prueba con salas existentes en el mundo
        threats.clear_threat_zones()
        self.test_zone = threats.ThreatZone(
            threat_zone_id="tz_integration_test",
            region="edran",
            creature_id="cornalomo",
            warning_rooms={"valdren_camino_parcela"},
            encounter_rooms={"valdren_camino_cerca"},
            cooldown_seconds=1800.0,
            presence_mode="threat_scripted",
            warning_signal="El suelo vibra y hay ramas quebradas.",
            close_signal="Un imponente Cornalomo te corta el paso.",
            inactive_trail_signal="Quedan pisadas secas, pero la bestia se ha marchado.",
        )
        threats.register_threat_zone(self.test_zone)

    def tearDown(self):
        threats.load_canonical_threat_zones()
        try:
            self.temp_dir.cleanup()
        except PermissionError:
            pass

    def csrf(self, path="/", client=None):
        client = client or self.client
        page = client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', page)[1]

    def post(self, route, data=None, client=None, csrf_path="/"):
        client = client or self.client
        return client.post(route, data={**(data or {}), "csrf": self.csrf(csrf_path, client)})

    def register_and_enter_world(self, username="threat_hero", name="Guerrero Valdren"):
        self.post("/register", dict(username=username, name=name, password="una clave de prueba 123"))
        dm = self.app.test_client()
        self.post("/dm/login", dict(dm_password="dm-secret-value"), dm, csrf_path="/dm")
        self.post("/dm/approve", dict(username=username), dm, csrf_path="/dm")
        self.post("/species", dict(species="humano"))
        player_id = self.client.get("/api/me").json["player"]["id"]
        store.set_player_class(self.db_path, player_id, "juramentado")
        self.post("/move", dict(direction="south"))  # salir del hogar a valdren_centro
        # Caminar a valdren_sendero
        self.post("/move", dict(direction="north"))
        return player_id

    def test_full_warning_close_and_avoid_cycle_via_terminal_and_api(self):
        """Ciclo completo: aviso ambiental -> proximidad crítica -> decisión evitar."""
        pid = self.register_and_enter_world()

        # 1. Moverse a la sala de advertencia: 'valdren_camino_parcela' (north desde sendero)
        res = self.post("/move", dict(direction="north"))
        self.assertEqual(res.status_code, 303)

        room_data = self.client.get("/api/room").json["room"]
        self.assertEqual(room_data["id"], "valdren_camino_parcela")
        self.assertEqual(room_data.get("threat_signal"), "El suelo vibra y hay ramas quebradas.")
        self.assertIsNone(room_data.get("threat_c3"))

        rec = store.get_threat_state(self.db_path, pid, "tz_integration_test")
        self.assertEqual(rec["state"], "warned")

        # 2. Moverse a la sala de proximidad crítica: 'valdren_camino_cerca' (north)
        res = self.post("/move", dict(direction="north"))
        self.assertEqual(res.status_code, 303)

        room_data = self.client.get("/api/room").json["room"]
        self.assertEqual(room_data["id"], "valdren_camino_cerca")
        self.assertIsNone(room_data.get("encounter"), "No debe auto-iniciar combate forzado (§40.4)")
        self.assertIsNotNone(room_data.get("threat_c3"))
        self.assertEqual(room_data["threat_c3"]["creature_id"], "cornalomo")

        action_names = [a["action"] for a in room_data["available_actions"]]
        self.assertIn("atacar", action_names)
        self.assertIn("evaluar", action_names)
        self.assertIn("evitar", action_names)
        self.assertNotIn("descansar", action_names)

        # 3. Evaluar cualitativamente sin empezar combate
        eval_res = self.client.post("/api/intent", json={"text": "evaluar cornalomo", "csrf": self.csrf()})
        self.assertEqual(eval_res.status_code, 200)
        self.assertTrue(eval_res.json["accepted"])
        self.assertIn("supera claramente", eval_res.json["message"])

        # Sigue sin combate activo
        self.assertIsNone(store.get_encounter(self.db_path, pid, "valdren_camino_cerca"))

        # Intentar descansar debe ser bloqueado
        rest_res = self.client.post("/api/intent", json={"text": "descansar", "csrf": self.csrf()})
        self.assertFalse(rest_res.json["accepted"])
        self.assertEqual(rest_res.json["outcome"], "blocked")

        # 4. Decisión 'evitar' / retroceder
        avoid_res = self.client.post("/api/intent", json={"text": "evitar", "csrf": self.csrf()})
        self.assertEqual(avoid_res.status_code, 200)
        self.assertTrue(avoid_res.json["accepted"])
        self.assertEqual(avoid_res.json["outcome"], "avoided")
        self.assertIn("retroceder con cautela", " ".join(avoid_res.json["messages"]))

        # Cooldown de 30 minutos activo en BD
        rec_avoid = store.get_threat_state(self.db_path, pid, "tz_integration_test")
        self.assertEqual(rec_avoid["state"], "resolved")
        self.assertIsNotNone(rec_avoid["cooldown_until"])
        self.assertGreater(rec_avoid["cooldown_until"], time.time())

        # El jugador retrocedió a 'valdren_camino_parcela'
        cur_room = self.client.get("/api/room").json["room"]
        self.assertEqual(cur_room["id"], "valdren_camino_parcela")

        # Reingreso a 'valdren_camino_cerca': cooldown no muestra amenaza C3
        res = self.post("/move", dict(direction="north"))
        self.assertEqual(res.status_code, 303)
        room_revisit = self.client.get("/api/room").json["room"]
        self.assertIsNone(room_revisit.get("threat_c3"))
        self.assertEqual(
            room_revisit.get("threat_signal"),
            "Quedan pisadas secas, pero la bestia se ha marchado."
        )

    def test_attack_engages_combat_and_flee_triggers_cooldown(self):
        """Atacar inicia combate normal (§40.7) y huir exitosamente activa cooldown (§40.8)."""
        pid = self.register_and_enter_world()

        # Avanzar hasta proximidad crítica
        self.post("/move", dict(direction="north"))
        self.post("/move", dict(direction="north"))

        # Atacar al Cornalomo desde 'close'
        atk_res = self.client.post("/api/intent", json={"text": "atacar cornalomo", "csrf": self.csrf()})
        self.assertEqual(atk_res.status_code, 200)
        self.assertTrue(atk_res.json["accepted"])

        # Ahora el combate está formalmente activo en store
        enc = store.get_encounter(self.db_path, pid, "valdren_camino_cerca")
        self.assertIsNotNone(enc)
        self.assertEqual(enc["creature_id"], "cornalomo")

        # Huir con éxito (forzando RNG favorable 0.0)
        with patch("random.Random.uniform", return_value=0.0):
            flee_res = self.client.post("/api/intent", json={"text": "huir", "csrf": self.csrf()})
            self.assertEqual(flee_res.status_code, 200)
            self.assertEqual(flee_res.json["outcome"], "success")

        # Encuentro limpiado y cooldown de 30 min activado
        self.assertIsNone(store.get_encounter(self.db_path, pid, "valdren_camino_cerca"))
        rec = store.get_threat_state(self.db_path, pid, "tz_integration_test")
        self.assertEqual(rec["state"], "resolved")
        self.assertGreater(rec["cooldown_until"], time.time())

    def test_defeat_by_c3_preserves_equipment_and_triggers_cooldown(self):
        """Derrota contra C3 respawnea, conserva equipo/inventario y activa cooldown (§40.9)."""
        pid = self.register_and_enter_world()

        self.post("/move", dict(direction="north"))
        self.post("/move", dict(direction="north"))

        # Iniciar combate
        self.post("/attack")

        # Bajar HP del jugador a 1 para asegurar derrota en el siguiente golpe del Cornalomo
        with store.connect(self.db_path) as db:
            db.execute("UPDATE players SET hp_current = 1 WHERE id = ?", (pid,))

        # Ronda donde Cornalomo golpea y derriba al jugador (RNG forzado para impacto de Cornalomo)
        with patch("random.Random.uniform", return_value=0.0):
            res = self.post("/attack")
            self.assertEqual(res.status_code, 200)

        html = res.get_data(as_text=True)
        self.assertIn("HAS MUERTO", html)
        self.assertIn("Conservas tu equipo e inventario", html)

        # Respawn en Valdren
        player_now = store.character_by_player_id(self.db_path, pid)
        self.assertEqual(player_now["room"], "valdren_centro")

        # Cooldown C3 activo en BD
        rec = store.get_threat_state(self.db_path, pid, "tz_integration_test")
        self.assertEqual(rec["state"], "resolved")
        self.assertGreater(rec["cooldown_until"], time.time())

    def test_abandoning_close_encounter_zone_activates_cooldown(self):
        """Abandonar la zona de proximidad crítica activada activa cooldown (§40.6)."""
        pid = self.register_and_enter_world()

        self.post("/move", dict(direction="north"))
        self.post("/move", dict(direction="north"))

        rec_close = store.get_threat_state(self.db_path, pid, "tz_integration_test")
        self.assertEqual(rec_close["state"], "close")

        # El jugador simplemente se mueve hacia el sur sin interactuar
        res = self.post("/move", dict(direction="south"))
        self.assertEqual(res.status_code, 303)

        rec_abandoned = store.get_threat_state(self.db_path, pid, "tz_integration_test")
        self.assertEqual(rec_abandoned["state"], "resolved")
        self.assertGreater(rec_abandoned["cooldown_until"], time.time())


if __name__ == "__main__":
    unittest.main()
