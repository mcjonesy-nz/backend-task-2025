import unittest
from typing import Any
from project import constants, validation

Payload = dict[str, Any]

def make_sentence(id: str = "s1", text: str = "ok"):
    return {"id": id, "sentence": text}

class ValidationTests(unittest.TestCase):   
    def test_valid_standalone_payload_does_not_raise(self):
        payload: Payload = {"surveyTitle": "T", "theme": "account", "baseline": [make_sentence()]}
        # should not raise
        validation.validate_payload(payload, mode="standalone")

    def test_missing_required_field_raises(self):
        payload: Payload = {"theme": "t", "baseline": [make_sentence()]}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn("Missing required field", str(cm.exception))

    def test_nonstring_field_raises(self):
        payload: Payload = {"surveyTitle": "T", "theme": 123, "baseline": [make_sentence()]}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn("theme must be a string", str(cm.exception))

    def test_empty_string_field_raises(self):
        payload: Payload = {"surveyTitle": "  ", "theme": "t", "baseline": [make_sentence()]}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn("surveyTitle cannot be empty", str(cm.exception))

    def test_baseline_empty_list_raises(self):
        payload: Payload = {"surveyTitle": "T", "theme": "t", "baseline": []}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn("baseline must be a non-empty list", str(cm.exception))

    def test_baseline_exceeds_max_sentences_raises(self):
        too_many = [make_sentence(str(i), "ok") for i in range(constants.MAX_SENTENCES + 1)]
        payload: Payload = {"surveyTitle": "T", "theme": "t", "baseline": too_many}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn(f"exceeds maximum allowed size of {constants.MAX_SENTENCES}", str(cm.exception))

    def test_sentence_missing_keys_raises(self):
        payload: Payload = {"surveyTitle": "T", "theme": "t", "baseline": [{"id": "1"}]}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn("must contain 'id' and 'sentence'", str(cm.exception))

    def test_sentence_id_empty_raises(self):
        payload: Payload = {"surveyTitle": "T", "theme": "t", "baseline": [{"id": "", "sentence": "ok"}]}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn(".id must be a non-empty string", str(cm.exception))

    def test_sentence_sentence_empty_raises(self):
        payload: Payload = {"surveyTitle": "T", "theme": "t", "baseline": [{"id": "1", "sentence": "   "}]}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn(".sentence must be a non-empty string", str(cm.exception))

    def test_sentence_too_long_raises(self):
        long_text = "x" * (constants.MAX_SENTENCE_LENGTH + 1)
        payload: Payload = {"surveyTitle": "T", "theme": "t", "baseline": [{"id": "1", "sentence": long_text}]}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="standalone")
        self.assertIn(f"exceeds max length of {constants.MAX_SENTENCE_LENGTH}", str(cm.exception))

    def test_comparative_mode_requires_comparison(self):
        payload: Payload = {"surveyTitle": "T", "theme": "t", "baseline": [make_sentence()]}
        with self.assertRaises(validation.BadRequestError) as cm:
            validation.validate_payload(payload, mode="comparative")
        self.assertIn("Missing required field: comparison", str(cm.exception))

    def test_comparative_valid_does_not_raise(self):
        payload: Payload = {
            "surveyTitle": "T",
            "theme": "t",
            "baseline": [make_sentence("b1", "ok")],
            "comparison": [make_sentence("c1", "fine")],
        }
        validation.validate_payload(payload, mode="comparative")

