from typing import List
from sentence_transformers import SentenceTransformer # type: ignore
from project.models import EmbeddedSentence, EmbeddedDataset, AnalysisMode, ProcessedSentence

#  Load once per cold start
_model = SentenceTransformer("all-MiniLM-L6-v2") # type: ignore


def _embed(sentences: List[ProcessedSentence]) -> List[EmbeddedSentence]:
    if not sentences:
        return []

    texts = [s.normalized_text for s in sentences]

    vectors = _model.encode( # type: ignore
        texts,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return [
        EmbeddedSentence(sentence=s, vector=v) # type: ignore
        for s, v in zip(sentences, vectors) # type: ignore
    ]


def embed_sentences(
    *,
    mode: AnalysisMode,
    baseline: List[ProcessedSentence],
    comparison: List[ProcessedSentence] | None = None,
) -> EmbeddedDataset:
    """
    Generate embeddings based on analysis mode.
    """
    if mode == AnalysisMode.STANDALONE:
        return EmbeddedDataset(
            baseline=_embed(baseline),
            comparison=None,
        )

    if mode == AnalysisMode.COMPARATIVE:
        if comparison is None:
            raise ValueError("comparison sentences required for comparative mode")

        return EmbeddedDataset(
            baseline=_embed(baseline),
            comparison=_embed(comparison),
        )

    raise ValueError(f"Unsupported analysis mode: {mode}")


def embed_sentence_list(sentences: List[ProcessedSentence]) -> EmbeddedDataset:
    """
    Generate embeddings for a list of processed sentences.
    """
    return EmbeddedDataset(
        baseline=_embed(sentences),
        comparison=None,
    )
