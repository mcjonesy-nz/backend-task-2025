from typing import List, Union

from project.models import Sentence, StandalonePayload, ComparativePayload


def load_sentences(payload: Union[StandalonePayload, ComparativePayload]) -> List[Sentence]:
    """
    Convert a parsed payload into a flat list of Sentence domain objects.
    """
    sentences: List[Sentence] = []

    # Baseline sentences
    for item in payload.baseline:
        sentences.append(
            Sentence(
                id=item.id,
                text=item.sentence,
                source="baseline"
            )
        )

    # Comparison sentences (if present)
    if isinstance(payload, ComparativePayload):
        for item in payload.comparison:
            sentences.append(
                Sentence(
                    id=item.id,
                    text=item.sentence,
                    source="comparison"
                )
            )

    return sentences
