import unittest
import numpy as np

from project.clustering import cluster_sentences
from project.models import EmbeddedSentence, ProcessedSentence


def make_es(name: str, vec: list[float]) -> EmbeddedSentence:
    ps = ProcessedSentence(ids=[name], original_texts=[name], normalized_text=name)
    return EmbeddedSentence(sentence=ps, vector=np.array(vec))


class TestClustering(unittest.TestCase):
    def test_cluster_two_similar_vectors(self):
        # two identical vectors should cluster together with min_samples=2
        a = make_es("a", [1.0, 0.0, 0.0])
        b = make_es("b", [1.0, 0.0, 0.0])
        c = make_es("c", [0.0, 1.0, 0.0])

        clusters = cluster_sentences([a, b, c], eps=0.1, min_samples=2)

        # expect one cluster (a and b) and c as noise
        self.assertEqual(len(clusters), 1)
        cluster_sentences_texts = [es.sentence.normalized_text for es in clusters[0].sentences]
        self.assertCountEqual(cluster_sentences_texts, ["a", "b"])

    def test_cluster_empty_returns_empty(self):
        self.assertEqual(cluster_sentences([]), [])

    def test_single_point_is_noise_with_min_samples_2(self):
        # single point should be considered noise when min_samples=2
        p = make_es("only", [1.0, 0.0, 0.0])
        clusters = cluster_sentences([p], eps=0.1, min_samples=2)
        self.assertEqual(clusters, [])


if __name__ == "__main__":
    unittest.main()
