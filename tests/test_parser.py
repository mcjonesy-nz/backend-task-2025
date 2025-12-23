import unittest
from typing import Any, Dict, cast

from project import models, validation, parser

Payload = dict[str, Any]

def make_sentence(id: str = "s1", text: str = "ok") -> Dict[str, Any]:
    return {"id": id, "sentence": text}

class ParserTests(unittest.TestCase):
    def test__parse_sentences_returns_sentenceinput_list(self):
        items = [make_sentence("a", "hello"), make_sentence("b", "world")]
        result = parser.parse_sentences(items)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "a")
        self.assertEqual(result[0].sentence, "hello")

    def test_parse_payload_standalone(self):
        payload: Payload = {"surveyTitle": "S", "theme": "t", "baseline": [make_sentence()]}
        res = parser.parse_payload(payload)
        self.assertIsInstance(res, models.StandalonePayload)
        self.assertEqual(res.survey_title, "S")
        self.assertEqual(res.theme, "t")
        self.assertEqual(len(res.baseline), 1)

    def test_parse_payload_comparative(self):
        payload: Payload = {
            "surveyTitle": "S",
            "theme": "t",
            "baseline": [make_sentence("b1", "ok")],
            "comparison": [make_sentence("c1", "fine")],
        }
        res = parser.parse_payload(payload)
        self.assertIsInstance(res, models.ComparativePayload)
        res = cast(models.ComparativePayload, res)
        self.assertEqual(len(res.baseline), 1)
        self.assertEqual(len(res.comparison), 1)

    def test_missing_field_raises_badrequest(self):
        payload: Payload = {"theme": "t", "baseline": [make_sentence()]}
        with self.assertRaises(validation.BadRequestError) as cm:
            parser.parse_payload(payload)
        self.assertIn("Missing required field", str(cm.exception))

    def test_missing_sentence_key_raises(self):
        # sentence missing 'id' will cause KeyError inside parser
        payload: Payload = {"surveyTitle": "S", "theme": "t", "baseline": [{"sentence": "ok"}]}
        with self.assertRaises(validation.BadRequestError) as cm:
            parser.parse_payload(payload)
        self.assertIn("Missing required field", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
