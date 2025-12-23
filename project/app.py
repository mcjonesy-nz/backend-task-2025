import json
from typing import Any, Dict

from project.parser import parse_payload
from project.validation import validate_payload, BadRequestError


def lambda_handler(event: Dict[str, Any], context):
    raw_payload = parse_json(event)
    mode = determine_mode(raw_payload)

    validate_payload(raw_payload, mode)

    parse_payload(raw_payload)

    # sentences = load_sentences(payload, mode)

    # sentences = preprocess_sentences(sentences)

    # embeddings = embed_sentences(sentences)

    # clusters = cluster_sentences(sentences, embeddings)

    # if mode == "standalone":
    #     results = build_standalone_results(clusters)
    # else:
    #     results = build_comparative_results(clusters)

    # Minimal success response for now (higher-level processing not implemented)
    return success_response({"message": "payload validated", "mode": mode})


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

    Returns "comparative" if `comparison` key is present, otherwise "standalone".
    """

    return "comparative" if "comparison" in payload else "standalone"


def success_response(body: Dict[str, Any]) -> Dict[str, Any]:
    return {"statusCode": 200, "body": json.dumps(body)}


def error_response(message: str, status: int = 400) -> Dict[str, Any]:
    return {"statusCode": status, "body": json.dumps({"error": message})}


if __name__ == "__main__":
    # Simulate a Lambda invocation
    fake_event: Dict[str, Any] = {}
    fake_context = None

    response = lambda_handler(fake_event, fake_context)
    print(response)
