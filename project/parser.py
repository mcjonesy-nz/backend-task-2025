from typing import Dict, Any, List, Union
from project.models import SentenceInput, StandalonePayload, ComparativePayload
from project.validation import BadRequestError


def parse_payload(payload: Dict[str, Any]) -> Union[StandalonePayload, ComparativePayload]:
    try:
        baseline = parse_sentences(payload["baseline"])

        if "comparison" in payload:
            comparison = parse_sentences(payload["comparison"])
            return ComparativePayload(
                survey_title=payload["surveyTitle"],
                theme=payload["theme"],
                baseline=baseline,
                comparison=comparison,
            )

        return StandalonePayload(
            survey_title=payload["surveyTitle"],
            theme=payload["theme"],
            baseline=baseline,
        )

    except KeyError as e:
        raise BadRequestError(f"Missing required field: {e.args[0]}")


def parse_sentences(items: List[Dict[str, Any]]) -> List[SentenceInput]:
    sentences: List[SentenceInput] = []
    for item in items:
        sentences.append(
            SentenceInput(
                id=item["id"],
                sentence=item["sentence"]
            )
        )
    return sentences
