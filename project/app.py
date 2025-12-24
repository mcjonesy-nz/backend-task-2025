from dataclasses import asdict
import json
from typing import Any, Dict
from pathlib import Path

from project.clustering import cluster_sentences
from project.embeddings import embed_sentence_list
from project.models import AnalysisMode, ClusterSummary
from project.parser import parse_payload
from project.preprocessing import preprocess_sentences
from project.summarization import summarize_cluster
from project.validation import validate_payload, BadRequestError
from project.loader import load_sentences
from project.logging import setup_logger


logger = setup_logger(__name__)


def lambda_handler(event: Dict[str, Any], context):
    raw_payload = parse_json(event)
    mode = determine_mode(raw_payload)
    logger.info(f"Processing mode: {mode}")

    validate_payload(raw_payload, mode)

    payload = parse_payload(raw_payload)

    sentences = load_sentences(payload)
    logger.info(f"Loaded {len(sentences)} sentences successfully")

    processed_sentences = preprocess_sentences(sentences)
    logger.info(f"Processed {len(processed_sentences)} sentences successfully")

    embeddings = embed_sentence_list(processed_sentences)
    logger.info(f"Generated embeddings for {len(embeddings.baseline)} sentences")

    clusters = cluster_sentences(embeddings.baseline)
    logger.info(f"Formed {len(clusters)} clusters from sentences")

    summary_results = list[ClusterSummary]()
    for cluster in clusters:
        summary = summarize_cluster(cluster)
        summary_results.append(summary)

    logger.info(f"Summarized {len(summary_results)} clusters successfully")

    return success_response({
        "clusters": [asdict(s) for s in summary_results],
    })


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


def determine_mode(payload: Dict[str, Any]) -> AnalysisMode:
    """Determine processing mode from payload shape.

    Returns "comparative" if `comparison` list has values in it, otherwise "standalone".
    """

    return AnalysisMode.COMPARATIVE if "comparison" in payload and payload["comparison"] else AnalysisMode.STANDALONE


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
        json_response = json.loads(response["body"])
        json_response = json.dumps(json_response, indent=4)
        print(json_response)
