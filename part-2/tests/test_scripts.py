import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(module, filename):
    spec = importlib.util.spec_from_file_location(module, ROOT / "scripts" / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

normalise = load("normalise", "normalise_manifest.py").normalise
edit_distance = load("evaluate", "evaluate_cer.py").edit_distance
evaluate = load("evaluate2", "evaluate_cer.py").evaluate
convert = load("eaf", "eaf_to_csv.py").convert

class PipelineTest(unittest.TestCase):
    def test_diacritic_and_tones_preserved(self):
        self.assertEqual(normalise("  mǎ555  ", {"unicode_form": "NFC"}), "mǎ555")

    def test_explicit_replacement(self):
        self.assertEqual(normalise("ma555", {"replacements": {"555": "H"}}), "maH")

    def test_edit_distance(self):
        self.assertEqual(edit_distance("abc", "ac"), 1)
        self.assertEqual(edit_distance(["one", "two"], ["one", "too"]), 1)

    def test_corpus_metrics(self):
        n, cer, wer = evaluate([{"r": "abc", "h": "ac"}, {"r": "go", "h": "go"}], "r", "h")
        self.assertEqual(n, 2)
        self.assertAlmostEqual(cer, 0.2)
        self.assertAlmostEqual(wer, 0.5)

    def test_eaf_parse_tier_and_ms(self):
        xml = """<?xml version="1.0"?>
        <ANNOTATION_DOCUMENT>
          <TIME_ORDER><TIME_SLOT TIME_SLOT_ID="t1" TIME_VALUE="100"/>
          <TIME_SLOT TIME_SLOT_ID="t2" TIME_VALUE="900"/></TIME_ORDER>
          <TIER TIER_ID="tx" PARTICIPANT="SPK01">
            <ANNOTATION><ALIGNABLE_ANNOTATION ANNOTATION_ID="a1"
            TIME_SLOT_REF1="t1" TIME_SLOT_REF2="t2">
            <ANNOTATION_VALUE>ma555</ANNOTATION_VALUE>
            </ALIGNABLE_ANNOTATION></ANNOTATION>
          </TIER>
        </ANNOTATION_DOCUMENT>"""
        with tempfile.TemporaryDirectory() as tmp:
            eaf = Path(tmp) / "sample.eaf"
            wav = Path(tmp) / "sample.wav"
            eaf.write_text(xml)
            wav.touch()
            rows = convert(eaf, "tx", wav)
        self.assertEqual(rows[0]["dur_ms"], 800)
        self.assertEqual(rows[0]["speaker"], "SPK01")
        self.assertEqual(rows[0]["text_original"], "ma555")
        self.assertEqual(rows[0]["text_target"], "ma555")

if __name__ == "__main__":
    unittest.main()
