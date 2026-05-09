from typing import Any

from tools.news_tool import get_news


TOPIC_KEYWORDS = {
    "earnings": ["earnings", "revenue", "profit", "quarter", "guidance"],
    "partnerships": ["partnership", "collaboration", "deal"],
    "layoffs": ["layoff", "job cuts", "workforce"],
    "regulation": ["regulation", "regulator", "sec", "antitrust"],
    "m&a": ["acquisition", "merger", "takeover"],
    "product_launches": ["launch", "product", "release"],
    "macro_events": ["inflation", "rates", "fed", "economy"],
}


def detect_news_topics(news: list[str]) -> list[str]:
    combined_text = " ".join(news).lower()
    topics: list[str] = []

    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in combined_text for keyword in keywords):
            topics.append(topic)

    return topics


def news_agent(ticker: str) -> dict[str, Any]:
    """
    Fetch recent financial news and identify basic news themes.
    """

    normalized_ticker = ticker.upper()
    news = get_news(normalized_ticker)

    return {
        "agent": "news_agent",
        "ticker": normalized_ticker,
        "news": news,
        "topics": detect_news_topics(news),
        "status": "success",
        "metadata": {
            "news_items": len(news),
            "data_source": "newsapi",
        },
    }