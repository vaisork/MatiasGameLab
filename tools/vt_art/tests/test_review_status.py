from __future__ import annotations

import unittest
import json
import tempfile
from pathlib import Path

from tools.vt_art.review_status import (
    ReviewStatusError,
    is_current_review,
    metadata_paths,
    status_for_review,
    update_metadata_file,
)


class ArtReviewStatusTests(unittest.TestCase):
    def test_github_review_decisions_map_to_art_metadata(self):
        self.assertEqual(status_for_review("approved"), "approved")
        self.assertEqual(status_for_review("changes_requested"), "rejected")
        self.assertEqual(status_for_review("dismissed"), "draft")
        with self.assertRaises(ReviewStatusError):
            status_for_review("commented")

    def test_stale_reviews_are_ignored_but_dismissal_resets_status(self):
        self.assertFalse(is_current_review("approved", "old-sha", "new-sha"))
        self.assertTrue(is_current_review("approved", "same-sha", "same-sha"))
        self.assertTrue(is_current_review("dismissed", "old-sha", "new-sha"))

    def test_only_art_generation_metadata_files_are_selected(self):
        files = [
            {"filename": "vintage-telnet/art_generations/creature/v001/metadata.json"},
            {"filename": "vintage-telnet/art_generations/creature/v001/request.json"},
            {"filename": "assets/vintage-telnet/creature.png"},
            {"filename": "vintage-telnet/art_generations/../metadata.json"},
        ]
        self.assertEqual(
            metadata_paths(files),
            ["vintage-telnet/art_generations/creature/v001/metadata.json"],
        )

    def test_non_art_pull_request_cannot_change_art_status(self):
        with self.assertRaisesRegex(ReviewStatusError, "no contiene metadata"):
            metadata_paths([{"filename": "vintage-telnet/ART_IMAGE_PIPELINE.md"}])

    def test_metadata_records_approval_or_rejection_without_losing_other_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "metadata.json"
            path.write_text(json.dumps({"asset_id": "creature", "status": "draft"}), encoding="utf-8")
            self.assertTrue(update_metadata_file(path, "rejected"))
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data, {"asset_id": "creature", "status": "rejected"})
            self.assertFalse(update_metadata_file(path, "rejected"))
            with self.assertRaises(ReviewStatusError):
                update_metadata_file(path, "not-a-status")


if __name__ == "__main__":
    unittest.main()
