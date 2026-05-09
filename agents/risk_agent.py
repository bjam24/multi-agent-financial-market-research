from typing import Any

HIGH_VOLATILITY_THRESHOLD = 5.0
LOW_VOLUME_THRESHOLD = 1_000_000


def risk_agent(
    market_data_result: dict[str, Any],
    sentiment: dict[str, Any] | None = None,
    news_topics: list[str] | None = None,
) -> dict[str, Any]:
    """
    Evaluate basic market, sentiment, and data reliability risks.
    """

    sentiment = sentiment or {}
    news_topics = news_topics or []

    data = market_data_result.get("market_data", {})
    ticker = market_data_result.get("ticker")

    daily_change = float(data.get("daily_change_percent") or 0)
    volume = int(data.get("volume") or 0)

    risks: list[str] = []

    if data.get("status") != "success":
        risks.append("Market data reliability issue detected")

    if abs(daily_change) >= HIGH_VOLATILITY_THRESHOLD:
        risks.append("Elevated short-term price volatility")

    if volume <= LOW_VOLUME_THRESHOLD:
        risks.append("Low trading liquidity")

    if sentiment.get("sentiment") == "negative":
        risks.append("Negative news sentiment")

    if "regulation" in news_topics:
        risks.append("Potential regulatory risk")

    if "macro_events" in news_topics:
        risks.append("Potential macroeconomic risk")

    if not risks:
        risks.append("No significant market risks detected")

    return {
        "agent": "risk_agent",
        "ticker": ticker,
        "status": "success",
        "risks": risks,
        "metadata": {
            "daily_change_percent": daily_change,
            "volume": volume,
            "sentiment": sentiment.get("sentiment"),
            "news_topics": news_topics,
            "method": "rule_based_risk_analysis",
        },
    }