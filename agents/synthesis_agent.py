from typing import Any

HIGH_CONFIDENCE_THRESHOLD = 0.7
MEDIUM_CONFIDENCE_THRESHOLD = 0.4


def get_research_insight(sentiment: str | None) -> str:
    if sentiment == "positive":
        return (
            "Recent signals indicate positive momentum, "
            "although further confirmation is required."
        )

    if sentiment == "negative":
        return (
            "Recent signals suggest increased downside risk "
            "and near-term uncertainty."
        )

    return "Market signals appear mixed, with no clear directional bias."


def get_confidence_reason(confidence: float) -> str:
    if confidence >= HIGH_CONFIDENCE_THRESHOLD:
        return "High confidence due to consistent sentiment signals."

    if confidence >= MEDIUM_CONFIDENCE_THRESHOLD:
        return "Moderate confidence due to partially mixed signals."

    return "Low confidence due to weak or unclear signals."


def format_bullet_list(items: list[Any], fallback: str) -> str:
    if not items:
        return f"- {fallback}\n"

    return "".join(f"- {item}\n" for item in items)


def synthesis_agent(data: dict[str, Any]) -> dict[str, Any]:
    """
    Build a structured research report from agent outputs.
    """

    ticker = data.get("ticker", "UNKNOWN")

    market_data = data.get("market_data", {})
    risks = data.get("risks", [])
    news = data.get("news", [])
    sentiment = data.get("sentiment", {})
    patterns = data.get("patterns", [])

    sentiment_label = sentiment.get("sentiment", "neutral")
    confidence = float(sentiment.get("confidence") or 0)

    report = f"""
        # Financial Market Research Report: {ticker}

        ## Market Summary
        - Current price: {market_data.get("current_price", "N/A")}
        - Previous close: {market_data.get("previous_close", "N/A")}
        - Daily change: {market_data.get("daily_change", "N/A")} ({market_data.get("daily_change_percent", "N/A")}%)
        - Volume: {market_data.get("volume", "N/A")}

        ## Key News
        {format_bullet_list(news, "No relevant news available.")}

        ## Sentiment Analysis
        - Sentiment: {sentiment_label}
        - Confidence: {confidence}
        - Reason: {sentiment.get("reason", "No sentiment explanation available.")}

        ## Market Signals
        {format_bullet_list(patterns, "No market signals detected.")}

        ## Risk Analysis
        {format_bullet_list(risks, "No significant risks detected.")}

        ## Research Insight
        {get_research_insight(sentiment_label)}

        ## Confidence Score
        - Score: {confidence}
        - Reason: {get_confidence_reason(confidence)}

        ## Disclaimer
        This report is for informational purposes only and does not constitute financial advice.
        """.strip()

    return {
        "agent": "synthesis_agent",
        "status": "success",
        "report": report,
        "metadata": {
            "ticker": ticker,
            "news_items": len(news),
            "risk_items": len(risks),
            "signal_items": len(patterns),
            "method": "template_based_synthesis",
        },
    }