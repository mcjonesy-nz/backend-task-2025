from collections import Counter
from project.models import SentenceCluster, ClusterSummary


def classify_sentiment(text: str) -> str:
    # Placeholder sentiment classification logic. Improve
    text_lower = text.lower()
    if "good" in text_lower or "great" in text_lower or "excellent" in text_lower:
        return "positive"
    elif "bad" in text_lower or "terrible" in text_lower or "poor" in text_lower:
        return "negative"
    else:
        return "neutral"


def summarize_cluster(cluster: SentenceCluster) -> ClusterSummary:
    # ---- sentence IDs ----
    sentence_ids = set[str]()
    normalized_texts = list[str]()

    for embedded in cluster.sentences:
        sentence_ids.update(embedded.sentence.ids)
        normalized_texts.append(embedded.sentence.normalized_text)

    # ---- representative sentence ----
    most_common_text, _ = Counter(normalized_texts).most_common(1)[0]

    title = most_common_text.capitalize()
    if len(title) > 60:
        title = title[:57] + "..."

    # ---- sentiment ----
    sentiments = [
        classify_sentiment(embedded.sentence.original_texts[0])
        for embedded in cluster.sentences
    ]

    sentiment = Counter(sentiments).most_common(1)[0][0]

    # ---- key insights ----
    insights = list[str]()
    seen = set[str]()

    for embedded in cluster.sentences:
        text = embedded.sentence.original_texts[0]
        if text not in seen:
            insights.append(text)
            seen.add(text)
        if len(insights) == 3:
            break

    return ClusterSummary(
        title=title,
        sentiment=sentiment,
        sentence_ids=sorted(sentence_ids),
        key_insights=insights,
    )
