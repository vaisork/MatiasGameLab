"""#379: fixtures C0 sintéticos; no son fauna ni mapping canónicos."""
import copy
from dataclasses import asdict, replace
import json
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

from server import ambient


CATALOG = (
    {"ambient_id": "fixture_a", "name": "Fauna de prueba A",
     "regions": ["fixture_region"], "habitat_tags": ["campo"],
     "behavior_text": "Observación sintética A.", "exclusions": []},
    {"ambient_id": "fixture_b", "name": "Fauna de prueba B",
     "regions": ["fixture_region"], "habitat_tags": ["campo", "orilla"],
     "behavior_text": "Observación sintética B.", "exclusions": []},
)
HABITAT = ambient.Habitat("fixture_room", "fixture_habitat", "fixture_region",
                          frozenset({"campo"}), "ambient_normal")


def zero_hash(_key):
    return bytes(32)


class SelectionTests(unittest.TestCase):
    def select(self, habitat=HABITAT, **kwargs):
        return ambient.select_presence(habitat, catalog=CATALOG, **kwargs)

    def test_production_catalog_is_empty_and_no_event_is_emitted(self):
        self.assertEqual(ambient.CATALOG, ())
        self.assertIsNone(ambient.select_presence(HABITAT, hash_fn=zero_hash))
        self.assertEqual(ambient.validate_catalog(()), ())

    def test_contract_profiles_are_exact(self):
        self.assertEqual(ambient.DENSITY, {"ambient_none": 0, "ambient_sparse": .15,
                                          "ambient_normal": .30, "ambient_rich": .45})

    def test_zero_profile_never_rolls(self):
        with patch.object(ambient, "stable_hash", side_effect=AssertionError):
            self.assertIsNone(self.select(replace(HABITAT, profile="ambient_none"),
                                          hash_fn=ambient.stable_hash))

    def test_time_is_injectable_and_epoch_boundary_is_exact(self):
        before = self.select(now=599.999, hash_fn=zero_hash)
        after = self.select(now=600, hash_fn=zero_hash)
        self.assertEqual(before.epoch, 0)
        self.assertEqual(after.epoch, 1)
        with patch.object(ambient.time, "time", return_value=600):
            self.assertEqual(self.select(hash_fn=zero_hash), after)

    def test_same_room_epoch_and_catalog_produce_same_event(self):
        for epoch in range(100):
            first = self.select(now=epoch * 600)
            self.assertEqual(first, self.select(now=epoch * 600 + 599))
            self.assertEqual(first, ambient.select_presence(
                HABITAT, catalog=tuple(reversed(CATALOG)), now=epoch * 600))

    def test_room_and_habitat_are_part_of_unambiguous_hash_key(self):
        keys = []
        def capture(key):
            keys.append(json.loads(key))
            return bytes(32)
        self.select(now=1200, hash_fn=capture)
        self.assertEqual(keys, [["c0-presence", 2, "fixture_room", "fixture_habitat"],
                                ["c0-species", 2, "fixture_room", "fixture_habitat"]])

    def test_determinism_across_python_process_hash_seeds(self):
        script = ("from server.ambient import stable_hash; "
                  "print(stable_hash(b'[1,\"room\",\"habitat\"]').hex())")
        results = [subprocess.check_output([sys.executable, "-c", script],
                   env={**os.environ, "PYTHONHASHSEED": seed}, text=True)
                   for seed in ("1", "9876")]
        self.assertEqual(results[0], results[1])

    def test_distribution_respects_each_profile_and_changes_across_epochs(self):
        for profile, chance in ambient.DENSITY.items():
            with self.subTest(profile=profile):
                habitat = replace(HABITAT, profile=profile)
                results = [self.select(habitat, now=epoch * 600) for epoch in range(5000)]
                hits = [p for p in results if p is not None]
                self.assertAlmostEqual(len(hits) / len(results), chance, delta=.02)
                if chance:
                    self.assertEqual({p.ambient_id for p in hits}, {"fixture_a", "fixture_b"})
                    self.assertIn(None, results)

    def test_catalog_size_does_not_multiply_presence_probability(self):
        for epoch in range(100):
            one = ambient.select_presence(HABITAT, catalog=CATALOG[:1], now=epoch * 600)
            many = self.select(now=epoch * 600)
            self.assertEqual(one is None, many is None)

    def test_at_most_one_event_without_combat_fields(self):
        event = self.select(now=0, hash_fn=zero_hash)
        self.assertIsInstance(event, ambient.Presence)
        self.assertEqual(set(asdict(event)),
                         {"ambient_id", "name", "behavior_text", "room_id", "epoch"})

    def test_profile_threshold_is_exclusive(self):
        for profile, chance in ambient.DENSITY.items():
            if not chance:
                continue
            threshold = int(chance * (1 << 256))
            habitat = replace(HABITAT, profile=profile)
            self.assertIsNone(self.select(habitat, now=0,
                              hash_fn=lambda _: threshold.to_bytes(32, "big")))
            self.assertIsNotNone(self.select(habitat, now=0,
                                 hash_fn=lambda _: (threshold - 1).to_bytes(32, "big")))

    def test_region_and_habitat_compatibility_are_required(self):
        for habitat in (replace(HABITAT, region="other_region"),
                        replace(HABITAT, tags=frozenset({"roca"})),
                        replace(HABITAT, tags=frozenset())):
            self.assertIsNone(self.select(habitat, now=0, hash_fn=zero_hash))

    def test_exclusions_override_compatible_region_and_tags(self):
        for exclusion in (HABITAT.room_id, HABITAT.habitat_id, HABITAT.region, "campo"):
            catalog = ({**CATALOG[0], "exclusions": [exclusion]},)
            self.assertIsNone(ambient.select_presence(HABITAT, catalog=catalog,
                                                     now=0, hash_fn=zero_hash))

    def test_combat_scripted_and_c1_suppress_c0_without_consuming_hash(self):
        for flag in ("combat_active", "scripted", "encounter"):
            with self.subTest(priority=flag), patch.object(
                    ambient, "stable_hash", side_effect=AssertionError("no C0 roll")):
                self.assertIsNone(self.select(now=0, hash_fn=ambient.stable_hash, **{flag: True}))

    def test_selection_does_not_mutate_catalog_or_habitat(self):
        original = copy.deepcopy(CATALOG)
        habitat_before = asdict(HABITAT)
        self.select(now=0, hash_fn=zero_hash)
        self.assertEqual(CATALOG, original)
        self.assertEqual(asdict(HABITAT), habitat_before)

    def test_invalid_catalog_fails_closed(self):
        invalid = [({},), (CATALOG[0], CATALOG[0]),
                   ({**CATALOG[0], "regions": []},),
                   ({**CATALOG[0], "habitat_tags": "campo"},),
                   ({**CATALOG[0], "exclusions": [None]},),
                   ({**CATALOG[0], "name": ""},),
                   ({**CATALOG[0], "hp": 100},)]
        for catalog in invalid:
            with self.subTest(catalog=catalog), self.assertRaises(ValueError):
                ambient.select_presence(HABITAT, catalog=catalog, now=0, hash_fn=zero_hash)

    def test_invalid_context_time_and_hash_are_rejected(self):
        for change in ({"profile": "inventado"}, {"room_id": ""}, {"tags": "campo"}):
            with self.assertRaises(ValueError):
                replace(HABITAT, **change)
        for timestamp in (-1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                self.select(now=timestamp, hash_fn=zero_hash)
        with self.assertRaises(ValueError):
            self.select(now=0, hash_fn=lambda _: b"short")


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.event = ambient.select_presence(HABITAT, catalog=CATALOG, now=600, hash_fn=zero_hash)
        self.session = {"other_feature": "unchanged"}

    def test_repeated_render_and_round_trip_do_not_spam(self):
        self.assertEqual(ambient.observe(self.event, self.session), self.event)
        other = replace(self.event, room_id="other_room")
        self.assertEqual(ambient.observe(other, self.session), other)
        self.assertIsNone(ambient.observe(self.event, self.session))
        self.assertIsNone(ambient.observe(self.event, self.session))

    def test_explicit_observation_can_repeat_but_does_not_reset_auto_spam_guard(self):
        ambient.observe(self.event, self.session)
        self.assertEqual(ambient.observe(self.event, self.session, explicit=True), self.event)
        self.assertIsNone(ambient.observe(self.event, self.session))

    def test_new_epoch_prunes_old_rooms_and_allows_new_observation(self):
        ambient.observe(self.event, self.session)
        next_event = replace(self.event, epoch=2, room_id="next_room")
        self.assertEqual(ambient.observe(next_event, self.session), next_event)
        self.assertEqual(self.session[ambient.SESSION_KEY],
                         {"epoch": 2, "rooms": {"next_room": "seen"}})

    def test_reconnect_with_new_session_gets_same_presence_not_persistent_identity(self):
        ambient.observe(self.event, self.session)
        fresh_session = {}
        again = ambient.select_presence(HABITAT, catalog=CATALOG, now=1199, hash_fn=zero_hash)
        self.assertEqual(ambient.observe(again, fresh_session), self.event)
        self.assertIsNone(ambient.observe(again, self.session))

    def test_attempted_attack_only_withdraws_local_presentation(self):
        before = copy.deepcopy(CATALOG)
        result = ambient.withdraw(self.event, self.session)
        self.assertEqual(result, {"outcome": "ambient_withdrawn", "ambient_id": "fixture_a",
                                  "name": "Fauna de prueba A"})
        self.assertIsNone(ambient.observe(self.event, self.session, explicit=True))
        self.assertIsNone(ambient.withdraw(self.event, self.session))
        self.assertEqual(ambient.observe(self.event, {}), self.event)
        self.assertEqual(CATALOG, before)
        self.assertEqual(self.session["other_feature"], "unchanged")

    def test_withdrawal_expires_next_epoch(self):
        ambient.withdraw(self.event, self.session)
        later = replace(self.event, epoch=2)
        self.assertEqual(ambient.observe(later, self.session), later)

    def test_no_presence_does_not_mutate_session(self):
        before = self.session.copy()
        self.assertIsNone(ambient.observe(None, self.session))
        self.assertIsNone(ambient.withdraw(None, self.session))
        self.assertEqual(self.session, before)

    def test_state_is_json_serializable_and_reassigned_for_cookie_session(self):
        ambient.observe(self.event, self.session)
        previous = self.session[ambient.SESSION_KEY]
        ambient.withdraw(self.event, self.session)
        self.assertIsNot(self.session[ambient.SESSION_KEY], previous)
        restored = json.loads(json.dumps(self.session))
        self.assertIsNone(ambient.observe(self.event, restored, explicit=True))


if __name__ == "__main__":
    unittest.main()
