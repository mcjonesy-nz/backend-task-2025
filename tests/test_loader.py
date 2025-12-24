import unittest

from project import loader, models


def make_input(id: str = "s1", text: str = "ok") -> models.SentenceInput:
    return models.SentenceInput(id=id, sentence=text)


class LoaderTests(unittest.TestCase):
    def test_load_sentences_standalone(self):
        baseline = [make_input("b1", "hello"), make_input("b2", "world")]
        payload = models.StandalonePayload(survey_title="S", theme="t", baseline=baseline)

        result = loader.load_sentences(payload)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "b1")
        self.assertEqual(result[0].text, "hello")
        self.assertEqual(result[0].source, models.AnalysisMode.STANDALONE)

    def test_load_sentences_comparative(self):
        baseline = [make_input("b1", "alpha")]
        comparison = [make_input("c1", "beta"), make_input("c2", "gamma")]
        payload = models.ComparativePayload(
            survey_title="S", theme="t", baseline=baseline, comparison=comparison
        )

        result = loader.load_sentences(payload)

        # total sentences = baseline + comparison
        self.assertEqual(len(result), 3)

        # baseline first
        self.assertEqual(result[0].id, "b1")
        self.assertEqual(result[0].text, "alpha")
        self.assertEqual(result[0].source, models.AnalysisMode.STANDALONE)

        # comparison entries
        self.assertEqual(result[1].id, "c1")
        self.assertEqual(result[1].text, "beta")
        self.assertEqual(result[1].source, models.AnalysisMode.COMPARATIVE)


if __name__ == "__main__":
    unittest.main()
