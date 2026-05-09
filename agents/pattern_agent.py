from typing import Any

PRICE_MOVE_THRESHOLD = 2.0
ELEVATED_MOVE_THRESHOLD = 3.0

HIGH_VOLUME_THRESHOLD = 50_000_000
LOW_VOLUME_THRESHOLD = 1_000_000


def pattern_agent(
    market_data: dict[str, Any],
    sentiment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Detect price, volume, and sentiment divergence signals.
    """

    sentiment = sentiment or {}

    price_change = float(market_data.get("daily_change_percent") or 0)
    volume = int(market_data.get("volume") or 0)
    sentiment_label = sentiment.get("sentiment", "neutral")

    signals: list[str] = []

    if price_change >= PRICE_MOVE_THRESHOLD:
        signals.append("Positive price momentum")
    elif price_change <= -PRICE_MOVE_THRESHOLD:
        signals.append("Negative price momentum")
    else:
        signals.append("Stable price movement")

    if volume >= HIGH_VOLUME_THRESHOLD:
        signals.append("Unusually high trading volume")
    elif volume <= LOW_VOLUME_THRESHOLD:
        signals.append("Low market participation")
    else:
        signals.append("Normal trading volume")

    if abs(price_change) >= ELEVATED_MOVE_THRESHOLD:
        signals.append("Elevated short-term price movement")
    else:
        signals.append("Limited short-term price movement")

    if sentiment_label == "positive" and price_change < 0:
        signals.append(
            "Divergence: positive news sentiment with negative price movement"
        )

    if sentiment_label == "negative" and price_change > 0:
        signals.append(
            "Divergence: negative news sentiment with positive price movement"
        )

    return {
        "agent": "pattern_agent",
        "status": "success",
        "signals": signals,
        "metadata": {
            "price_change_percent": price_change,
            "volume": volume,
            "sentiment_context": sentiment_label,
            "method": "rule_based_signal_detection",
        },
    }