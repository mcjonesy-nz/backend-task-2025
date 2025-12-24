from typing import Any, Dict, List

from project.constants import MAX_SENTENCE_LENGTH, MAX_SENTENCES
from project.models import AnalysisMode


class BadRequestError(Exception):
    """Raised when input validation fails."""
    pass


def validate_payload(payload: Dict[str, Any], mode: AnalysisMode) -> None:
    _validate_required_fields(payload)
    _validate_sentences(payload["baseline"], field_name="baseline")

    if mode == AnalysisMode.COMPARATIVE:
        if "comparison" not in payload:
            raise BadRequestError("Missing required field: comparison")
        _validate_sentences(payload["comparison"], field_name="comparison")


def _validate_required_fields(payload: Dict[str, Any]) -> None:
    for field in ("surveyTitle", "theme", "baseline"):
        if field not in payload:
            raise BadRequestError(f"Missing required field: {field}")

        if not isinstance(payload[field], str) and field != "baseline":
            raise BadRequestError(f"{field} must be a string")

        if field != "baseline" and not payload[field].strip():
            raise BadRequestError(f"{field} cannot be empty")


def _validate_sentences(sentences: List[Dict[str, Any]], field_name: str) -> None:
    if not sentences:
        raise BadRequestError(f"{field_name} must be a non-empty list")

    if len(sentences) > MAX_SENTENCES:
        raise BadRequestError(
            f"{field_name} exceeds maximum allowed size of {MAX_SENTENCES}"
        )

    for i, item in enumerate(sentences):
        if "id" not in item or "sentence" not in item:
            raise BadRequestError(
                f"{field_name}[{i}] must contain 'id' and 'sentence'"
            )

        if not isinstance(item["id"], str) or not item["id"].strip():
            raise BadRequestError(
                f"{field_name}[{i}].id must be a non-empty string"
            )

        if not isinstance(item["sentence"], str) or not item["sentence"].strip():
            raise BadRequestError(
                f"{field_name}[{i}].sentence must be a non-empty string"
            )

        if len(item["sentence"]) > MAX_SENTENCE_LENGTH:
            raise BadRequestError(
                f"{field_name}[{i}].sentence exceeds max length of {MAX_SENTENCE_LENGTH}"
            )
