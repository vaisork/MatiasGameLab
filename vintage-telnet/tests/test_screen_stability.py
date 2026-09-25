"""La pantalla no debe reacomodarse (petición de Javier, 2026-09-25): la
ilustración se guarda en el celular, el marco de arte siempre existe con el
mismo tamaño y el texto se revela sin cambiar de altura."""
import re
import tempfile
import unittest

from server.app import create_app
from server import store


class ScreenStabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-" * 5,
                                   DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()
        self.post("/register", dict(username="matias", name="Matías", password="una clave de prueba"))
        store.set_status(self.app.config["DATABASE"], "matias", "approved")
        self.post("/species", dict(species="humano"))
        self.post("/class", dict(player_class="sombra"))

    def tearDown(self):
        self.temp.cleanup()

    def post(self, route, data):
        page = self.client.get("/").get_data(as_text=True)
        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
        return self.client.post(route, data={**data, "csrf": csrf})

    def test_art_is_cached_but_pages_and_api_are_not(self):
        art = self.client.get("/assets/locations/valdren.webp")
        self.assertEqual(art.status_code, 200)
        self.assertEqual(art.headers["Cache-Control"], "public, max-age=86400")
        self.assertEqual(self.client.get("/").headers["Cache-Control"], "no-store")
        self.assertEqual(self.client.get("/api/room").headers["Cache-Control"], "no-store")

    def test_art_frame_is_always_present(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('<figure class="location-art" data-swap="art"', html)
        self.assertIn('fetchpriority="high"', html)
        self.assertNotIn('loading="lazy" decoding="async">\n          <div class="location-art-fallback"', html)
        self.post("/move", dict(direction="north"))  # sendero: sin arte aprobado
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('<figure class="location-art no-art" data-swap="art"', html)
        self.assertIn('<div class="art-placeholder" aria-hidden="true"></div>', html)

    def test_text_reveal_reserves_full_height(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('hiddenPart.style.visibility = "hidden"', html)
        self.assertIn(".game-shell .log{height:36dvh;height:36svh}", html)


if __name__ == "__main__":
    unittest.main()


class CombatReadingTests(ScreenStabilityTests):
    def test_combat_shows_only_the_fight_and_results_go_inside_the_log(self):
        self.post("/move", dict(direction="north"))
        self.post("/move", dict(direction="north"))  # Parcela removida: Mordelinde
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("¡COMBATE!", html)
        self.assertNotIn("<p data-room-description", html)  # no se repite cómo es el lugar
        self.assertNotIn('class="entry exits-entry"', html)
        html = self.post("/attack", {}).get_data(as_text=True)
        self.assertIn("data-result-entry>", html)
        self.assertNotIn('<div class="alert-note"', html)  # nada empuja la pantalla desde arriba

    def test_exploration_results_also_go_inside_the_log(self):
        html = self.post("/command", dict(text="examinar huellas")).get_data(as_text=True)
        self.assertIn("data-result-entry>", html)
        self.assertNotIn('<div class="alert-note"', html)
        self.assertIn("<p data-room-description", html)


class CombatLogTests(ScreenStabilityTests):
    def enter_combat(self):
        self.post("/move", dict(direction="north"))
        self.post("/move", dict(direction="north"))  # Parcela removida: Mordelinde
        self.player_id = self.client.get("/api/me").json["player"]["id"]
        self.path = self.app.config["DATABASE"]

    def test_fight_is_told_turn_by_turn_and_only_while_it_lasts(self):
        self.enter_combat()
        self.post("/evaluate", {})
        self.post("/dodge", {})
        self.post("/command", dict(text="resistir"))  # por comando también cuenta
        log = store.get_combat_log(self.path, self.player_id, "valdren_camino_parcela")
        self.assertEqual([line["action"] for line in log], ["evaluar", "esquivar", "resistir"])
        html = self.client.get("/").get_data(as_text=True)
        self.assertEqual(html.count('class="entry combat-line'), 3)
        self.assertIn('class="entry combat-line result-entry" role="status" data-result-entry', html)
        # Al terminar la pelea (aquí, huyendo o ganando) el relato se borra.
        store.clear_encounter(self.path, self.player_id, "valdren_camino_parcela")
        self.assertEqual(store.get_combat_log(self.path, self.player_id, "valdren_camino_parcela"), [])

    def test_log_never_grows_beyond_the_limit(self):
        self.enter_combat()
        for i in range(store.COMBAT_LOG_KEEP + 15):
            store.append_combat_log(self.path, self.player_id, "valdren_camino_parcela", "atacar", f"turno {i}")
        with store.connect(self.path) as db:
            count = db.execute("SELECT COUNT(*) FROM combat_log").fetchone()[0]
        self.assertEqual(count, store.COMBAT_LOG_KEEP)
        shown = store.get_combat_log(self.path, self.player_id, "valdren_camino_parcela")
        self.assertEqual(len(shown), 20)
        self.assertEqual(shown[-1]["text"], f"turno {store.COMBAT_LOG_KEEP + 14}")

    def test_actions_without_a_creature_are_not_logged(self):
        self.path = self.app.config["DATABASE"]
        self.post("/attack", {})
        with store.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM combat_log").fetchone()[0], 0)


class NoFlashTests(ScreenStabilityTests):
    def test_enemy_status_is_pinned_below_the_story(self):
        self.post("/move", dict(direction="north"))
        self.post("/move", dict(direction="north"))
        html = self.client.get("/").get_data(as_text=True)
        log_end = html.index('<div class="enemy-status">')
        self.assertLess(html.index('class="log"'), log_end)          # debajo del relato…
        self.assertLess(log_end, html.index('terminal-alert terminal-hint'))  # …y encima de la pista
        self.assertEqual(html.count('class="condition-bar"'), 1)

    def test_game_regions_can_be_swapped_without_reloading(self):
        html = self.client.get("/").get_data(as_text=True)
        for key in ("place", "art", "terminal", "controls", "side"):
            self.assertIn(f'data-swap="{key}"', html)
        self.assertIn('document.addEventListener("submit"', html)
        self.assertIn('form.closest(".game-shell")', html)  # solo acciones del juego, no login/logout
        self.assertIn("afterRender();", html)
