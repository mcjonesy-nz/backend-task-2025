import unittest
import numpy as np

import project.embeddings as emb
from project.models import ProcessedSentence, AnalysisMode, EmbeddedDataset


class FakeModel:
    def __init__(self):
        self.calls = []

    def encode(self, texts, **kwargs):
        # record the call and return a deterministic vector per text
        self.calls.append(list(texts))
        # Each vector will be length-3 with first element = len(text)
        return np.array([[len(t), 0.0, 0.0] for t in texts])


class TestEmbeddings(unittest.TestCase):
    def setUp(self):
        # swap in fake model and keep original
        self.orig_model = getattr(emb, "_model", None)
        emb._model = FakeModel()

    def tearDown(self):
        emb._model = self.orig_model

    def make_ps(self, nid: str, text: str) -> ProcessedSentence:
        return ProcessedSentence(ids=[nid], original_texts=[text], normalized_text=text.strip().lower())

    def test_embed_sentence_list_baseline_only(self):
        a = self.make_ps("1", " Foo BAR ")
        b = self.make_ps("2", "Another")

        ds = emb.embed_sentence_list([a, b])
        self.assertIsInstance(ds, EmbeddedDataset)
        self.assertEqual(len(ds.baseline), 2)
        self.assertIsNone(ds.comparison)

        # vectors deterministic: first element is len(text)
        self.assertEqual(int(ds.baseline[0].vector[0]), len(a.normalized_text))
        self.assertEqual(int(ds.baseline[1].vector[0]), len(b.normalized_text))

    def test_embed_sentences_comparative_and_calls(self):
        base1 = self.make_ps("b1", "Alpha")
        base2 = self.make_ps("b2", "Beta")
        comp1 = self.make_ps("c1", "Gamma")

        ds = emb.embed_sentences(mode=AnalysisMode.COMPARATIVE, baseline=[base1, base2], comparison=[comp1])

        self.assertEqual(len(ds.baseline), 2)
        self.assertEqual(len(ds.comparison), 1)

        # FakeModel should have recorded two encode calls: baseline then comparison
        self.assertEqual(len(emb._model.calls), 2)
        self.assertListEqual(emb._model.calls[0], [base1.normalized_text, base2.normalized_text])
        self.assertListEqual(emb._model.calls[1], [comp1.normalized_text])

    def test_embed_sentences_comparative_requires_comparison(self):
        with self.assertRaises(ValueError):
            emb.embed_sentences(mode=AnalysisMode.COMPARATIVE, baseline=[self.make_ps("x", "t")], comparison=None)

    def test_embed_sentence_list_empty_returns_empty(self):
        ds = emb.embed_sentence_list([])
        self.assertIsInstance(ds, EmbeddedDataset)
        self.assertEqual(ds.baseline, [])
        self.assertIsNone(ds.comparison)


if __name__ == "__main__":
    unittest.main()
