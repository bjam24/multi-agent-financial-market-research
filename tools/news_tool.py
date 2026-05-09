import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_news(ticker: str) -> list:
    """
    Fetch real financial news for a ticker using NewsAPI.
    """

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": ticker,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return [f"Failed to fetch news: {response.status_code}"]

    data = response.json()

    articles = data.get("articles", [])

    news = []

    for article in articles:
        title = article.get("title")
        if title:
            news.append(title)

    return news