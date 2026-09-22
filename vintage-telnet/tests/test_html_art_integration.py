from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "vintage-telnet.html"


class VintageHtmlAssetIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.html = HTML.read_text(encoding="utf-8")

    def test_referenced_html_ui_assets_exist(self):
        refs = sorted(set(re.findall(
            r'vintage-telnet/assets/html-ui/[A-Za-z0-9_./-]+\.png',
            self.html,
        )))
        self.assertTrue(refs, "expected Vintage Telnet HTML UI assets")
        missing = [ref for ref in refs if not (ROOT / ref).is_file()]
        self.assertEqual(missing, [], f"missing referenced assets: {missing}")

    def test_preview_images_are_not_used_as_live_ui(self):
        self.assertNotIn(
            "vintage-telnet/assets/html-ui/previews/",
            self.html,
        )

    def test_art_buttons_remain_real_html_buttons(self):
        for action in ("mapa", "inventario", "huir", "poderes"):
            self.assertRegex(
                self.html,
                rf'<button[^>]+data-action="{action}"[^>]*>',
            )

    def test_terminal_palette_is_preserved(self):
        self.assertIn("--term:#030806", self.html)
        self.assertIn("--green:#8dff9f", self.html)

    def test_help_is_fullscreen_and_character_has_3d_placeholder(self):
        self.assertIn('id="helpDialog" class="fullscreen"', self.html)
        self.assertIn('id="characterPreview"', self.html)


if __name__ == "__main__":
    unittest.main()
