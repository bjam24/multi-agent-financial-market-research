import json
import os

from typing import Any
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


load_dotenv()

MODEL_NAME = "gpt-4o-mini"
DEFAULT_SENTIMENT = "neutral"
DEFAULT_CONFIDENCE = 0.0


def build_sentiment_prompt(news: list[str]) -> str:
    headlines = "\n".join(f"- {item}" for item in news)

    return f"""
        Analyze the overall financial market sentiment from the news headlines below.

        Return only valid JSON using this schema:
        {{
            "sentiment": "positive | neutral | negative",
            "confidence": 0.0,
            "reason": "short explanation"
        }}

        News:
        {headlines}
    """.strip()


def default_response(reason: str, status: str = "success") -> dict[str, Any]:
    return {
        "agent": "sentiment_agent",
        "sentiment": DEFAULT_SENTIMENT,
        "confidence": DEFAULT_CONFIDENCE,
        "reason": reason,
        "status": status,
    }


def sentiment_agent(news: list[str]) -> dict[str, Any]:
    """
    Classify market news sentiment using an LLM-based research assistant.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return default_response(
            reason="Missing OpenAI API key",
            status="failed",
        )

    if not news:
        return default_response(
            reason="No news available for sentiment analysis",
        )

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a cautious financial market research analyst. "
                        "Classify sentiment without giving investment advice."
                    ),
                },
                {
                    "role": "user",
                    "content": build_sentiment_prompt(news),
                },
            ],
            temperature=0,
        )

        content = response.choices[0].message.content or "{}"
        parsed = json.loads(content)

    except (OpenAIError, json.JSONDecodeError, KeyError, IndexError) as error:
        fallback = default_response(
            reason="Sentiment analysis failed",
            status="failed",
        )
        fallback["error"] = str(error)
        return fallback

    return {
        "agent": "sentiment_agent",
        "sentiment": parsed.get("sentiment", DEFAULT_SENTIMENT),
        "confidence": float(parsed.get("confidence", DEFAULT_CONFIDENCE)),
        "reason": parsed.get("reason", ""),
        "status": "success",
        "metadata": {
            "model": MODEL_NAME,
            "method": "llm_sentiment_classification",
            "news_items": len(news),
        },
    }