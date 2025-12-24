from dataclasses import dataclass
from typing import List
from enum import Enum
import numpy as np # type: ignore


class AnalysisMode(str, Enum):
    STANDALONE = "standalone"
    COMPARATIVE = "comparative"


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
    # Do we need to know the source of the sentence?
    source: AnalysisMode


@dataclass
class EmbeddedSentence:
    sentence: ProcessedSentence
    vector: np.ndarray # type: ignore


@dataclass
class EmbeddedDataset:
    baseline: List[EmbeddedSentence]
    comparison: List[EmbeddedSentence] | None = None


@dataclass
class SentenceCluster:
    sentences: list[EmbeddedSentence]


@dataclass
class ClusterSummary:
    title: str
    sentiment: str
    sentence_ids: list[str]
    key_insights: list[str]
