import json
import tempfile
import unicodedata
import unittest
from pathlib import Path

from turkce_asr_ozel_isim import Lexicon, apply_candidates, correct, find_candidates, select_candidates
from turkce_asr_ozel_isim.cli import main

RECORDS = [
    {"name": "Mustafa Namoğlu", "type": "person", "company": "ikas",
     "misspellings": ["Anamoğlu", "Ulan Moğlu", "Ramoğlu"]},
    {"name": "ikas", "type": "company", "misspellings": ["IKASA"], "context_required": ["İkaz", "ikaz"]},
    {"name": "Ferhat Tuğra Çakır", "type": "person", "misspellings": ["Duraşakır"]},
    {"name": "Oğuz Alper Öktem", "type": "person", "misspellings": ["Alper Öktan", "Öktan"]},
    {"name": "Martı", "type": "company", "misspellings": ["Marta", "Martır"]},
    {"name": "Mustafa Keçeli", "type": "person", "misspellings": ["Keçi"]},
]
LEXICON = Lexicon(RECORDS)


def clip(text):
    return [{"word": w, "start": float(i), "end": i + 1.0} for i, w in enumerate(text.split())]


def candidates(text):
    return find_candidates({"c": clip(text)}, LEXICON)


def accept_all(_system, text):
    return json.dumps({"kabul": [x["no"] for x in json.loads(text)]})


class Candidates(unittest.TestCase):
    def test_keeps_suffix_and_punctuation(self):
        self.assertEqual(candidates("Siz Mustafa Anamoğlu'sunuz. tamam")[0]["new"], ["Namoğlu'sunuz."])

    def test_buffer_letter_after_vowel(self):
        self.assertEqual(candidates("Martır'a değil")[0]["new"], ["Martı'ya"])
        self.assertEqual(candidates("Martır'ın kurucusu")[0]["new"], ["Martı'nın"])

    def test_two_words_to_one(self):
        self.assertEqual(candidates("bu Mustafa Ulan Moğlu kimmiş")[0]["new"], ["Namoğlu"])

    def test_one_word_to_two(self):
        self.assertEqual(candidates("Ben Ferhat Duraşakır. 23")[0]["new"], ["Tuğra", "Çakır."])

    def test_real_word_needs_context(self):
        self.assertEqual(candidates("arabada ikaz lambası yandı"), [])
        found = find_candidates({1: clip("Mustafa Ramoğlu burada"), 2: clip("bu ikaz neymiş")}, LEXICON)
        self.assertEqual([c["new"] for c in found], [["Namoğlu"], ["ikas"]])

    def test_lowercase_ordinary_word_is_ignored(self):
        self.assertEqual(candidates("bir keçi gördüm"), [])

    def test_unseen_misspelling(self):
        c = candidates("Mustafa Namaoğlu geldi")[0]
        self.assertEqual((c["kind"], c["new"]), ("fuzzy", ["Namoğlu"]))

    def test_correct_text_and_other_people(self):
        self.assertEqual(candidates("Mustafa Namoğlu ve ikas"), [])
        self.assertEqual(candidates("Mustafa Keçeli ve Mustafa Yılmaz"), [])

    def test_nfd_input(self):
        text = unicodedata.normalize("NFD", "Mustafa Anamoğlu")
        self.assertEqual(candidates(text)[0]["new"], ["Namoğlu"])


class Apply(unittest.TestCase):
    def run_all(self, text):
        clips = {"c": clip(text)}
        return apply_candidates(clips, find_candidates(clips, LEXICON))["c"]

    def test_merge_keeps_time(self):
        words = self.run_all("bu Mustafa Ulan Moğlu kimmiş")
        self.assertEqual([w["word"] for w in words], ["bu", "Mustafa", "Namoğlu", "kimmiş"])
        self.assertEqual((words[2]["start"], words[2]["end"]), (2.0, 4.0))

    def test_split_keeps_time(self):
        words = self.run_all("Ben Ferhat Duraşakır. tamam")
        self.assertEqual([w["word"] for w in words], ["Ben", "Ferhat", "Tuğra", "Çakır.", "tamam"])
        self.assertEqual((words[2]["start"], words[3]["end"]), (2.0, 3.0))
        self.assertEqual(words[2]["end"], words[3]["start"])

    def test_several_candidates_do_not_shift(self):
        words = self.run_all("Mustafa Ulan Moğlu ve Marta şirketi Mustafa Ramoğlu")
        self.assertEqual(" ".join(w["word"] for w in words),
                         "Mustafa Namoğlu ve Martı şirketi Mustafa Namoğlu")


class Selection(unittest.TestCase):
    def test_rejected_candidate_is_not_applied(self):
        clips = {"c": clip("Mustafa Anamoğlu geldi")}
        fixed, report = correct(clips, LEXICON, lambda *_: '{"kabul":[]}')
        self.assertEqual(fixed["c"][1]["word"], "Anamoğlu")
        self.assertEqual(report["accepted"], [])

    def test_invalid_numbers_are_ignored(self):
        self.assertEqual(select_candidates(candidates("Mustafa Anamoğlu"),
                                           lambda *_: '{"kabul":[99,"1",true]}'), set())

    def test_input_is_not_modified(self):
        clips = {"c": clip("Mustafa Anamoğlu geldi")}
        correct(clips, LEXICON, accept_all)
        self.assertEqual(clips["c"][1]["word"], "Anamoğlu")


class Package(unittest.TestCase):
    def test_default_lexicon_loads(self):
        lexicon = Lexicon.default()
        found = find_candidates({"c": clip("Siz Mustafa Anamoğlu'sunuz.")}, lexicon)
        self.assertEqual(found[0]["new"], ["Namoğlu'sunuz."])

    def test_cli_round_trip(self):
        data = {"segments": [{"text": "Mustafa", "words": [{"word": "Mustafa", "start": 0.0, "end": 1.0}]},
                             {"text": "Ulan Moğlu geldi", "words": [
                                 {"word": "Ulan", "start": 1.0, "end": 1.5},
                                 {"word": "Moğlu", "start": 1.5, "end": 2.0},
                                 {"word": "geldi", "start": 2.0, "end": 3.0}]}]}
        with tempfile.TemporaryDirectory() as d:
            source, target = Path(d, "a.json"), Path(d, "b.json")
            source.write_text(json.dumps(data), encoding="utf-8")
            main([str(source), "-o", str(target), "--selector", "all"])
            out = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(out["segments"][1]["text"], "Namoğlu geldi")
        self.assertEqual(out["segments"][1]["words"][0]["end"], 2.0)
        self.assertNotIn("_segment", out["segments"][1]["words"][0])


if __name__ == "__main__":
    unittest.main()
