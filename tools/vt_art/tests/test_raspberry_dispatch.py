from __future__ import annotations

import unittest
from unittest.mock import call, patch
from unittest.mock import Mock

from tools.vt_art.dispatch import DispatchError, dispatch, main, validate_request_path


class RaspberryDispatchTests(unittest.TestCase):
    def test_accepts_only_direct_request_files(self):
        self.assertEqual(
            validate_request_path("vintage-telnet/art_requests/creature.json"),
            "vintage-telnet/art_requests/creature.json",
        )
        for path in (
            "vintage-telnet/art_requests/template.json",
            "vintage-telnet/art_requests/subdir/creature.json",
            "vintage-telnet/art_requests/../secret.json",
            "/tmp/creature.json",
            "vintage-telnet/art_requests/creature.png",
        ):
            with self.subTest(path=path), self.assertRaises(DispatchError):
                validate_request_path(path)

    def test_requires_authenticated_gh_before_check_or_billable_dispatch(self):
        runner = Mock(return_value=type("Result", (), {"returncode": 1, "stdout": "", "stderr": ""})())
        with self.assertRaisesRegex(DispatchError, "no está autenticado"):
            dispatch("vintage-telnet/art_requests/creature.json", runner=runner)
        runner.assert_called_once_with(["gh", "auth", "status", "--hostname", "github.com"])

    def test_requires_request_on_main_before_dispatch(self):
        from unittest.mock import call

        runner = Mock(side_effect=[
            type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
            type("Result", (), {"returncode": 1, "stdout": "", "stderr": ""})(),
        ])
        with self.assertRaisesRegex(DispatchError, "no existe en main"):
            dispatch("vintage-telnet/art_requests/creature.json", runner=runner)
        self.assertEqual(runner.call_count, 2)
        self.assertNotIn(call(["gh", "workflow", "run"]), runner.call_args_list)

    def test_dispatch_targets_only_the_art_workflow_and_main(self):
        from unittest.mock import call

        runner = Mock(side_effect=[
            type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
            type("Result", (), {"returncode": 0, "stdout": "vintage-telnet/art_requests/creature.json\n", "stderr": ""})(),
            type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
        ])
        dispatch("vintage-telnet/art_requests/creature.json", runner=runner)
        self.assertEqual(runner.call_args_list[1], call([
            "gh", "api", "--method", "GET",
            "repos/vaisork/MatiasGameLab/contents/vintage-telnet/art_requests/creature.json",
            "--field", "ref=main", "--jq", ".path",
        ]))
        self.assertEqual(runner.call_args_list[-1], call([
            "gh", "workflow", "run", "vt-art-pilot.yml",
            "--repo", "vaisork/MatiasGameLab", "--ref", "main",
            "--field", "request_file=vintage-telnet/art_requests/creature.json",
        ]))

    def test_declining_confirmation_does_not_start_generation(self):
        with patch("builtins.input", return_value="NO"), patch("tools.vt_art.dispatch.dispatch") as start:
            self.assertEqual(main(["vintage-telnet/art_requests/creature.json"]), 0)
        start.assert_not_called()

    def test_old_generar_word_no_longer_confirms(self):
        with patch("builtins.input", return_value="GENERAR"), patch("tools.vt_art.dispatch.dispatch") as start:
            self.assertEqual(main(["vintage-telnet/art_requests/creature.json"]), 0)
        start.assert_not_called()

    def test_short_gen_word_confirms(self):
        with patch("builtins.input", return_value="GEN"), patch("tools.vt_art.dispatch.dispatch") as start:
            self.assertEqual(main(["vintage-telnet/art_requests/creature.json"]), 0)
        start.assert_called_once_with("vintage-telnet/art_requests/creature.json")

    def test_yes_flag_starts_one_validated_request_without_an_interactive_prompt(self):
        with patch("tools.vt_art.dispatch.dispatch") as start:
            self.assertEqual(main(["vintage-telnet/art_requests/creature.json", "--yes"]), 0)
        start.assert_called_once_with("vintage-telnet/art_requests/creature.json")

    def test_yes_flag_dispatches_every_file_in_order(self):
        with patch("tools.vt_art.dispatch.dispatch") as start:
            self.assertEqual(main([
                "vintage-telnet/art_requests/a.json",
                "vintage-telnet/art_requests/b.json",
                "--yes",
            ]), 0)
        self.assertEqual(
            [call.args for call in start.call_args_list],
            [("vintage-telnet/art_requests/a.json",), ("vintage-telnet/art_requests/b.json",)],
        )

    def test_invalid_file_among_several_stops_before_dispatching_any(self):
        with patch("tools.vt_art.dispatch.dispatch") as start:
            code = main([
                "vintage-telnet/art_requests/a.json",
                "vintage-telnet/art_requests/template.json",
                "--yes",
            ])
        self.assertEqual(code, 2)
        start.assert_not_called()

    def test_stops_after_first_failure_and_does_not_repeat_completed_ones(self):
        with patch("tools.vt_art.dispatch.dispatch", side_effect=[None, DispatchError("boom")]) as start:
            code = main([
                "vintage-telnet/art_requests/a.json",
                "vintage-telnet/art_requests/b.json",
                "vintage-telnet/art_requests/c.json",
                "--yes",
            ])
        self.assertEqual(code, 2)
        self.assertEqual(start.call_count, 2)


if __name__ == "__main__":
    unittest.main()
