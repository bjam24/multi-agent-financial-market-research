from tools.news_tool import get_news


def news_agent(ticker: str) -> dict:
    """
    Fetch and summarize key news.
    """

    news = get_news(ticker)

    return {
        "agent": "news_agent",
        "ticker": ticker,
        "news": news,
        "status": "success",
    }