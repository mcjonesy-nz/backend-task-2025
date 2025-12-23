import re
from typing import List
from project.models import Sentence, ProcessedSentence

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """
    Normalize sentence text for clustering.
    """
    text = text.strip().lower()
    text = _WHITESPACE_RE.sub(" ", text)
    return text

# If we have the same sentence but with different ids, we keep them all
# We do this so that we can trace back to original inputs after clustering,
# but don't want to treat each as unique as it would overweight clustering


def preprocess_sentences(sentences: List[Sentence],) -> List[ProcessedSentence]:
    """
    Clean and normalize sentences for downstream processing.

    - Strips whitespace
    - Lowercases
    - Deduplicates by normalized text
    - Filters empty results
    """
    grouped: dict[str, ProcessedSentence] = {}

    for sentence in sentences:
        normalized = normalize_text(sentence.text)
        if not normalized:
            continue

        if normalized not in grouped:
            grouped[normalized] = ProcessedSentence(
                normalized_text=normalized,
                original_texts=[sentence.text],
                ids=[sentence.id],
            )
        else:
            if sentence.id not in grouped[normalized].ids:
                grouped[normalized].ids.append(sentence.id)
            grouped[normalized].original_texts.append(sentence.text)

    return list(grouped.values())
