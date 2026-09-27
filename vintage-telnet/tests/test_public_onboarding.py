import re
import tempfile
import unittest

from server.app import create_app
from server import content_parser, store, world


class PublicOnboardingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = dict(
            TESTING=True,
            SECRET_KEY="test-secret-key-32-chars-long-abcde",
            DATA_DIR=self.temp.name,
            SESSION_COOKIE_SECURE=False,
        )
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.path = self.app.config["DATABASE"]

    def tearDown(self):
        self.temp.cleanup()

    def test_public_landing_shows_three_clear_accesses(self):
        """La portada pública para invitados muestra claramente los 3 accesos:
        1. Conocer el Mundo
        2. Guía del aventurero
        3. Entrar / Crear cuenta
        sin obligar a scroll largo para encontrar Entrar.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        # 1. Enlace / acceso a Conocer el Mundo
        self.assertIn('/mundo', html)
        self.assertIn("Conocer el Mundo", html)

        # 2. Enlace / acceso a Guía del aventurero
        self.assertIn('/guia', html)
        self.assertIn("Guía del aventurero", html)

        # 3. Acceso directo a Entrar y Crear cuenta
        self.assertIn('data-onboarding-go="login"', html)
        self.assertIn('data-onboarding-go="register"', html)
        self.assertIn("Entrar / Crear cuenta", html)

        # No requiere autenticación previa
        self.assertIn("Invitado", html)

    def test_direct_view_param_opens_login_or_register(self):
        """El parámetro view=login o view=register permite acceso directo sin scroll."""
        res_login = self.client.get("/?view=login")
        self.assertEqual(res_login.status_code, 200)
        html_login = res_login.get_data(as_text=True)
        self.assertIn('data-onboarding-view="login"', html_login)
        # El panel de login no debe estar oculto cuando view=login
        self.assertNotIn('data-onboarding-view="login" hidden', html_login)

        res_reg = self.client.get("/?view=register")
        self.assertEqual(res_reg.status_code, 200)
        html_reg = res_reg.get_data(as_text=True)
        self.assertIn('data-onboarding-view="register"', html_reg)
        self.assertNotIn('data-onboarding-view="register" hidden', html_reg)

    def test_world_reader_is_public_and_read_only(self):
        """Conocer el Mundo es accesible para invitados, de solo lectura,
        y no altera la base de datos persistente."""
        response = self.client.get("/mundo")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        self.assertIn("Conocer el Mundo", html)
        self.assertIn("← Volver a portada", html)
        # Comprobar navegación de capítulos
        self.assertIn("1. El Mundo", html)
        self.assertIn("2. Las Especies", html)
        self.assertIn("3. Las Regiones y los Pueblos", html)
        self.assertIn("4. Vaisgard", html)
        self.assertIn("5. Tu Lugar en la Historia", html)
        self.assertIn("Leer todo", html)

        # Base de datos permanece limpia (sin cuentas ni personajes creados)
        with store.connect(self.path) as db:
            count = db.execute("SELECT count(*) FROM players").fetchone()[0]
        self.assertEqual(count, 0)

    def test_world_reader_has_zero_internal_metadata_leaks(self):
        """Garantiza que ninguna nota de diseño, instrucción interna de frontend
        o metadato de archivo se filtre al jugador en /mundo."""
        # Probar vista por capítulo y vista completa
        for url in ("/mundo", "/mundo?capitulo=1", "/mundo?capitulo=2", "/mundo?capitulo=3",
                    "/mundo?capitulo=4", "/mundo?capitulo=5", "/mundo?capitulo=todo"):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            text = response.get_data(as_text=True)

            forbidden_patterns = [
                "Clasificación:",
                "CANON DE ENTRADA",
                "SUBMENÚ DE CONTEXTO",
                "Responsable:",
                "Uso previsto:",
                "Objetivo:",
                "Propósito de este submenú",
                "Estructura sugerida del submenú",
                "Opciones sugeridas dentro del submenú",
                "NOTA DE DISEÑO",
                "INSERTAR IMAGEN CANÓNICA",
                "Reglas de implementación para UI/Frontend",
                "Frontera de canon",
                "Historiador y Constructor del Mundo — Vintage Telnet.",
            ]
            for pattern in forbidden_patterns:
                self.assertNotIn(
                    pattern.lower(),
                    text.lower(),
                    f"Se filtró metadato interno '{pattern}' en {url}",
                )

    def test_world_reader_chapters_navigation(self):
        """Verifica que cada capítulo contenga su contenido narrativo esperado y botones de paginación."""
        res_c1 = self.client.get("/mundo?capitulo=1")
        self.assertEqual(res_c1.status_code, 200)
        h1 = res_c1.get_data(as_text=True)
        self.assertIn("El mundo antes de tu llegada", h1)
        self.assertIn("Cuenca de Veyra", h1)
        self.assertIn("/assets/maps/region-inicial.webp", h1)

        res_c2 = self.client.get("/mundo?capitulo=2")
        self.assertEqual(res_c2.status_code, 200)
        h2 = res_c2.get_data(as_text=True)
        self.assertIn("Humanos", h2)
        self.assertIn("Felaryn", h2)
        self.assertIn("Dravak", h2)
        self.assertIn("Marevyn", h2)
        self.assertIn("Vesperi", h2)
        self.assertIn("/assets/species/comparativa-especies.webp", h2)

        res_c3 = self.client.get("/mundo?capitulo=3")
        self.assertEqual(res_c3.status_code, 200)
        h3 = res_c3.get_data(as_text=True)
        self.assertIn("Valdren", h3)
        self.assertIn("Khariel", h3)
        self.assertIn("Brumak", h3)
        self.assertIn("Narevia", h3)
        self.assertIn("Velmora", h3)
        # Omitido limpiamente porque no hay collage aprobado
        self.assertNotIn("NOTA DE DISEÑO / IMAGEN 3", h3)

        res_c4 = self.client.get("/mundo?capitulo=4")
        self.assertEqual(res_c4.status_code, 200)
        h4 = res_c4.get_data(as_text=True)
        self.assertIn("La ciudad que estaba antes", h4)
        self.assertIn("Las Cinco Rutas", h4)
        self.assertIn("Una ciudad construida sobre otra", h4)
        self.assertIn("/assets/locations/vaisgard.webp", h4)

        res_c5 = self.client.get("/mundo?capitulo=5")
        self.assertEqual(res_c5.status_code, 200)
        h5 = res_c5.get_data(as_text=True)
        self.assertIn("La Era Presente", h5)
        self.assertIn("Tu comienzo", h5)
        self.assertIn("Bienvenido a Vintage Telnet", h5)
        self.assertIn("Cinco especies.", h5)

    def test_world_reader_leer_todo_mode(self):
        """Verifica que el modo Leer todo incluya el índice jump navigation y todos los capítulos."""
        response = self.client.get("/mundo?capitulo=todo")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        self.assertIn('id="indice-todo"', html)
        self.assertIn('href="#capitulo-1"', html)
        self.assertIn('href="#capitulo-5"', html)
        self.assertIn('id="capitulo-1"', html)
        self.assertIn('id="capitulo-5"', html)
        self.assertIn("Bienvenido a Vintage Telnet", html)

    def test_guide_reader_is_public_and_read_only(self):
        """Guía del aventurero es pública, de solo lectura y no altera estado."""
        response = self.client.get("/guia")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        self.assertIn("Guía del aventurero", html)
        self.assertIn("← Volver a portada", html)
        self.assertIn("Vintage Telnet es un mundo que se recorre leyendo", html)

    def test_guide_reader_has_zero_editorial_metadata_leaks(self):
        """Garantiza que metadatos de cabecera editorial no se muestren al jugador."""
        response = self.client.get("/guia")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True).lower()

        forbidden_patterns = [
            "tipo: lectura opcional",
            "autoridad: diseñador de jugabilidad",
            "aprobado por javier para diseño/integración",
            "regla editorial: no revelar nombres",
        ]
        for pattern in forbidden_patterns:
            self.assertNotIn(pattern, text, f"Se filtró metadato editorial '{pattern}' en /guia")

    def test_guide_reader_preserves_all_approved_sections_and_toc(self):
        """Verifica que las 15 secciones aprobadas estén presentes con jump navigation."""
        response = self.client.get("/guia")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        expected_sections = [
            ("tu-personaje", "TU PERSONAJE"),
            ("tu-forma-de-enfrentar-el-mundo", "TU FORMA DE ENFRENTAR EL MUNDO"),
            ("explorar", "EXPLORAR"),
            ("mirar-no-es-lo-mismo-que-observar", "MIRAR NO ES LO MISMO QUE OBSERVAR"),
            ("no-todo-encuentro-es-una-pelea", "NO TODO ENCUENTRO ES UNA PELEA"),
            ("combate", "COMBATE"),
            ("vida-fatiga-y-heridas", "VIDA, FATIGA Y HERIDAS"),
            ("huir-tambien-es-jugar-bien", "HUIR TAMBIÉN ES JUGAR BIEN"),
            ("el-mundo-no-siempre-se-repite", "EL MUNDO NO SIEMPRE SE REPITE"),
            ("crecer", "CRECER"),
            ("equipo", "EQUIPO"),
            ("hablar-con-otros", "HABLAR CON OTROS"),
            ("tu-hogar", "TU HOGAR"),
            ("un-mundo-que-recuerda", "UN MUNDO QUE RECUERDA"),
            ("lo-mas-importante", "LO MÁS IMPORTANTE"),
        ]

        self.assertIn('id="indice"', html)
        for slug, title in expected_sections:
            self.assertIn(f'href="#{slug}"', html, f"Falta enlace en índice para {slug}")
            self.assertIn(f'id="{slug}"', html, f"Falta sección con id {slug}")
            # Verificación del título de la sección
            self.assertTrue(
                title in html or title.replace("É", "E").replace("Á", "A") in html,
                f"Falta título {title} en el contenido de la guía",
            )

        # Frase central aprobada en 'Lo más importante'
        self.assertIn("Acepta las consecuencias.", html)

    def test_login_and_registration_flow_preserved(self):
        """Verifica que el flujo existente de registro y login continúe funcionando exactamente igual."""
        # 1. Registro
        csrf = re.search(r'name="csrf" value="([^"]+)"', self.client.get("/").get_data(as_text=True))[1]
        reg_res = self.client.post("/register", data=dict(
            username="aventurero_nuevo",
            name="Aventurero",
            password="password_seguro_123",
            csrf=csrf,
        ))
        self.assertEqual(reg_res.status_code, 303)

        # 2. Comprobar sesión de invitado aprobando personaje
        me_res = self.client.get("/api/me")
        self.assertEqual(me_res.status_code, 200)
        player_data = me_res.json["player"]
        self.assertEqual(player_data["name"], "Aventurero")
        self.assertEqual(player_data["status"], "pending")

        # 3. Visitar /mundo o /guia estando logueado conserva sesión
        world_res = self.client.get("/mundo")
        self.assertEqual(world_res.status_code, 200)
        self.assertIn("Aventurero", world_res.get_data(as_text=True))

        guide_res = self.client.get("/guia")
        self.assertEqual(guide_res.status_code, 200)
        self.assertIn("Aventurero", guide_res.get_data(as_text=True))

    def test_security_headers_and_csp_nonces_in_readers(self):
        """Verifica que las cabeceras de seguridad y nonces CSP se apliquen a las páginas públicas."""
        for path in ("/mundo", "/guia"):
            res = self.client.get(path)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")
            self.assertEqual(res.headers.get("X-Frame-Options"), "DENY")
            csp = res.headers.get("Content-Security-Policy", "")
            self.assertIn("script-src 'nonce-", csp)
            # En /mundo hay script inline con nonce
            if path == "/mundo":
                m_nonce = re.search(r"script-src 'nonce-([^']+)'", csp)
                self.assertIsNotNone(m_nonce)
                html = res.get_data(as_text=True)
                self.assertIn(f'nonce="{m_nonce.group(1)}"', html)


if __name__ == "__main__":
    unittest.main()
