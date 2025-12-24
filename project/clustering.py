from typing import List
import numpy as np # type: ignore
from sklearn.cluster import DBSCAN # type: ignore

from project.models import EmbeddedSentence, SentenceCluster


def cluster_sentences(
    embedded_sentences: List[EmbeddedSentence],
    eps: float = 0.3,
    min_samples: int = 2,
) -> List[SentenceCluster]:
    """
    Cluster embedded sentences using cosine similarity.
    """
    if not embedded_sentences:
        return []

    vectors = np.vstack([e.vector for e in embedded_sentences]) # type: ignore

    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="cosine",
    ).fit(vectors) # type: ignore

    labels = clustering.labels_ # type: ignore

    clusters: dict[int, list[EmbeddedSentence]] = {}

    for label, embedded in zip(labels, embedded_sentences): # type: ignore
        if label == -1:
            # Noise / outlier — ignore for now
            continue

        clusters.setdefault(label, []).append(embedded) # type: ignore

    return [
        SentenceCluster(sentences=members)
        for members in clusters.values()
    ]
