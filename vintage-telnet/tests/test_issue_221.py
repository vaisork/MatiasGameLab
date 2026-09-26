import unittest
import tempfile
from server.app import create_app
import re
from server import store

class EntryAuthTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app(dict(TESTING=True, SECRET_KEY="test-secret-test-secret-test-secret", DATA_DIR=self.temp.name, SESSION_COOKIE_SECURE=False))
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def get_csrf(self, route="/"):
        page = self.client.get(route).get_data(as_text=True)
        match = re.search(r'name="csrf" value="([^"]+)"', page)
        return match.group(1) if match else ""

    def test_unauthenticated_user_cannot_access_protected_routes(self):
        # API protection
        response = self.client.get('/api/me')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/move', data=dict(direction='north', csrf=self.get_csrf()))
        self.assertEqual(response.status_code, 401)

    def test_invalid_login_fails_safely(self):
        response = self.client.post('/login', data=dict(username='nonexistent', password='bad', csrf=self.get_csrf()))
        self.assertEqual(response.status_code, 401)
        self.assertIn('Usuario o contraseña incorrectos', response.get_data(as_text=True))

    def test_public_route_returns_onboarding(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data-onboarding', response.get_data(as_text=True))

    def test_logout_removes_session(self):
        # Register and login
        csrf = self.get_csrf()
        response = self.client.post('/register', data=dict(username='matias', name='Matias', password='test-password', csrf=csrf))
        self.assertEqual(response.status_code, 303)

        # Logout
        csrf = self.get_csrf()
        response = self.client.post('/logout', data=dict(csrf=csrf))
        self.assertEqual(response.status_code, 303)

        # Verify access denied
        response = self.client.get('/api/me')
        self.assertEqual(response.status_code, 401)

    def test_public_flow_does_not_modify_state(self):
        # To test if the public flow does not modify persistent character state,
        # we can ensure that viewing the homepage does not implicitly create an account
        # and a failed login doesn't create anything.
        with store.connect(self.app.config["DATABASE"]) as db:
            initial_count = db.execute("SELECT COUNT(*) FROM players").fetchone()[0]

        self.client.get('/')
        self.client.post('/login', data=dict(username='fake', password='fake', csrf=self.get_csrf()))

        with store.connect(self.app.config["DATABASE"]) as db:
            final_count = db.execute("SELECT COUNT(*) FROM players").fetchone()[0]

        self.assertEqual(initial_count, final_count)
