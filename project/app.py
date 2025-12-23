import json
from typing import Any, Dict
from pathlib import Path

from project.parser import parse_payload
from project.validation import validate_payload, BadRequestError
from project.loader import load_sentences


def lambda_handler(event: Dict[str, Any], context):
    raw_payload = parse_json(event)
    mode = determine_mode(raw_payload)
    print(f"Processing mode: {mode}")

    validate_payload(raw_payload, mode)

    payload = parse_payload(raw_payload)

    sentences = load_sentences(payload)

    # sentences = preprocess_sentences(sentences)

    # embeddings = embed_sentences(sentences)

    # clusters = cluster_sentences(sentences, embeddings)

    # if mode == "standalone":
    #     results = build_standalone_results(clusters)
    # else:
    #     results = build_comparative_results(clusters)

    # Minimal success response for now (higher-level processing not implemented)
    return success_response({"message": "loaded " + str(len(sentences)) + " sentences", "mode": mode})


def parse_json(event: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the incoming Lambda event into a JSON payload dict.

    Supports API Gateway proxy events (with `body` string) or a direct dict payload.
    Raises BadRequestError on invalid JSON or missing payload.
    """
    if not event:
        raise BadRequestError("Empty event payload")

    # API Gateway proxy integration: body is a JSON string
    if "body" in event and isinstance(event["body"], str):
        try:
            return json.loads(event["body"]) if event["body"] else {}
        except json.JSONDecodeError as exc:
            raise BadRequestError(f"Invalid JSON in body: {exc}")

    return event


def determine_mode(payload: Dict[str, Any]) -> str:
    """Determine processing mode from payload shape.

    Returns "comparative" if `comparison` list has values in it, otherwise "standalone".
    """

    return "comparative" if "comparison" in payload and payload["comparison"] else "standalone"


def success_response(body: Dict[str, Any]) -> Dict[str, Any]:
    return {"statusCode": 200, "body": json.dumps(body)}


def error_response(message: str, status: int = 400) -> Dict[str, Any]:
    return {"statusCode": status, "body": json.dumps({"error": message})}


if __name__ == "__main__":
    # Simulate a Lambda invocation
    # load data/input_example.json for manual testing
    sample_path = Path(__file__).resolve().parents[1] / "data" / "input_example.json"
    fake_context = None
    fake_event: Dict[str, Any] = {}

    try:
        if sample_path.exists():
            with sample_path.open("r") as fh:
                fake_event = json.load(fh)

        response = lambda_handler(fake_event, fake_context)
    except BadRequestError as exc:
        print(error_response(str(exc), 400))
    except Exception as exc:  # pragma: no cover - safety for manual runs
        print(error_response(str(exc), 500))
    else:
        print(response)
