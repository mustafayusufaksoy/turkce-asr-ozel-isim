"""Rules every lexicon record must pass. CI runs these on each pull request."""
import json
import re
import unittest
from collections import Counter
from importlib import resources

from turkce_asr_ozel_isim import spelling_key

TYPES = {"person", "company"}
SOURCES = {"wikidata", "youtube-title", "youtube-channel", "news", "company-site"}
FIELDS = {"name", "type", "company", "misspellings", "context_required", "source"}
RECORDS = json.loads(resources.files("turkce_asr_ozel_isim")
                     .joinpath("data/lexicon.json").read_text(encoding="utf-8"))


class LexiconRules(unittest.TestCase):
    def test_fields_and_values(self):
        for r in RECORDS:
            with self.subTest(r["name"]):
                self.assertLessEqual(set(r), FIELDS)
                self.assertIn(r["type"], TYPES)
                self.assertTrue(r["name"].strip())
                self.assertTrue(r["source"], "a public source is required")
                self.assertLessEqual(set(r["source"]), SOURCES)

    def test_no_contact_details_or_links(self):
        pattern = re.compile(r"https?:|www\.|@|\d{4,}")
        for r in RECORDS:
            for value in [r["name"], r.get("company") or ""] + r.get("misspellings", []):
                self.assertIsNone(pattern.search(value), value)

    def test_people_have_full_names(self):
        for r in RECORDS:
            if r["type"] == "person":
                self.assertGreaterEqual(len(r["name"].split()), 2, r["name"])

    def test_no_duplicates(self):
        repeated = [k for k, n in Counter(spelling_key(r["name"]) + r["type"] for r in RECORDS).items() if n > 1]
        self.assertEqual(repeated, [])

    def test_misspelling_differs_from_name(self):
        for r in RECORDS:
            for spelling in r.get("misspellings", []) + r.get("context_required", []):
                self.assertNotEqual(spelling, r["name"])


if __name__ == "__main__":
    unittest.main()
