"""Real local HTTP process test, not a Raspberry deployment test."""
import http.cookiejar
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request


class HttpProcessTests(unittest.TestCase):
    def test_registration_and_login_after_process_restart(self):
        with tempfile.TemporaryDirectory() as data:
            with socket.socket() as socket_probe:
                socket_probe.bind(("127.0.0.1", 0))
                port = socket_probe.getsockname()[1]
            base = f"http://127.0.0.1:{port}"
            env = {**os.environ, "VT_DATA_DIR": data, "VT_SECRET_KEY": "http-test-" * 8,
                   "VT_HOST": "127.0.0.1", "VT_PORT": str(port), "VT_ALLOW_HTTP": "1",
                   "VT_TRUSTED_HOSTS": "127.0.0.1"}
            identities = []
            for route in ("register", "login"):
                with tempfile.TemporaryFile() as log:
                    process = subprocess.Popen([sys.executable, "-m", "server"], env=env,
                                               stdout=log, stderr=log,
                                               cwd=Path(__file__).resolve().parents[1])
                    try:
                        deadline = time.monotonic() + 15
                        while True:
                            try:
                                with urllib.request.urlopen(base + "/healthz", timeout=1) as response:
                                    self.assertEqual(json.load(response)["status"], "ok")
                                break
                            except (OSError, urllib.error.URLError):
                                if process.poll() is not None or time.monotonic() >= deadline:
                                    log.seek(0)
                                    self.fail(log.read().decode(errors="replace"))
                                time.sleep(.1)
                        client = urllib.request.build_opener(
                            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
                        with client.open(base + "/", timeout=5) as response:
                            page = response.read().decode()
                        csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
                        form = urllib.parse.urlencode(dict(csrf=csrf, username="device_test",
                                                          name="Prueba", password="a process test password")).encode()
                        with client.open(base + "/" + route, form, timeout=10) as response:
                            self.assertIn("Jugador #0001", response.read().decode())
                        with client.open(base + "/api/me", timeout=5) as response:
                            identities.append(json.load(response)["player"]["id"])
                    finally:
                        process.terminate()
                        try:
                            process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait(timeout=5)
            self.assertEqual(identities[0], identities[1])
