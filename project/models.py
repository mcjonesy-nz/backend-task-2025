from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SentenceInput:
    id: str
    sentence: str


@dataclass(frozen=True)
class ProcessedSentence:
    ids: List[str]
    original_texts: List[str]
    # not sure if we need to keep original as well
    normalized_text: str


@dataclass
class StandalonePayload:
    survey_title: str
    theme: str
    baseline: List[SentenceInput]


@dataclass
class ComparativePayload:
    survey_title: str
    theme: str
    baseline: List[SentenceInput]
    comparison: List[SentenceInput]


@dataclass
class Sentence:
    id: str
    text: str
    source: str  # "baseline" or "comparison"


@dataclass
class Cluster:
    cluster_id: int
    sentences: list[Sentence]
    embedding_centroid: list[float]


@dataclass
class StandaloneClusterResult:
    title: str
    sentiment: str
    sentence_ids: list[str]
    key_insights: list[str]


@dataclass
class ComparativeClusterResult:
    title: str
    sentiment: str
    baseline_sentence_ids: list[str]
    comparison_sentence_ids: list[str]
    key_similarities: list[str]
    key_differences: list[str]
