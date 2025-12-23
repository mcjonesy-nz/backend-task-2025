import unittest

from project.preprocessing import normalize_text, preprocess_sentences
from project.models import SentenceInput


class TestPreprocessing(unittest.TestCase):
    def test_normalize_text_trims_lower_and_collapses_whitespace(self):
        s = "  Hello \nWORLD\t  "
        self.assertEqual(normalize_text(s), "hello world")

    def test_preprocess_sentences_dedup_and_filter(self):
        inputs = [
            SentenceInput(id="1", sentence="  Foo BAR  "),
            SentenceInput(id="2", sentence="foo    bar"),
            SentenceInput(id="3", sentence="   "),
            SentenceInput(id="4", sentence="Unique"),
        ]

        processed = preprocess_sentences(inputs)

        # Expect two unique normalized texts: "foo bar" and "unique"
        self.assertEqual(len(processed), 2)

        # First kept item should contain both ids for the duplicate normalized text
        self.assertEqual(processed[0].ids, ["1", "2"])
        self.assertEqual(processed[0].normalized_text, "foo bar")
        self.assertEqual(processed[0].original_texts, ["  Foo BAR  ", "foo    bar"])

        # Second unique item
        self.assertEqual(processed[1].ids, ["4"])
        self.assertEqual(processed[1].normalized_text, "unique")
        self.assertEqual(processed[1].original_texts, ["Unique"])

    def test_preprocess_preserves_original_text(self):
        inp = [SentenceInput(id="x", sentence="  Mixed CASE ")]
        out = preprocess_sentences(inp)
        self.assertEqual(len(out), 1)
        ps = out[0]
        self.assertEqual(ps.ids, ["x"])
        self.assertEqual(ps.original_texts, ["  Mixed CASE "])
        self.assertEqual(ps.normalized_text, "mixed case")


if __name__ == "__main__":
    unittest.main()
