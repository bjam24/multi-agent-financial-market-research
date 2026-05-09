import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_API_URL = "https://newsapi.org/v2/everything"

DEFAULT_PAGE_SIZE = 5
REQUEST_TIMEOUT = 20


def get_news(ticker: str) -> list[str]:
    """
    Fetch recent financial news headlines using NewsAPI.
    """

    if not NEWS_API_KEY:
        raise ValueError(
            "Missing NEWS_API_KEY in .env file"
        )

    normalized_ticker = ticker.upper()

    params = {
        "q": normalized_ticker,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": DEFAULT_PAGE_SIZE,
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(
            NEWS_API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data: dict[str, Any] = response.json()

    except requests.RequestException as error:
        return [
            f"News API request failed: {error}"
        ]

    articles = data.get("articles", [])

    headlines: list[str] = []

    for article in articles:

        title = article.get("title")

        if title:
            headlines.append(title)

    if not headlines:
        return [
            "No relevant financial news found."
        ]

    return headlines