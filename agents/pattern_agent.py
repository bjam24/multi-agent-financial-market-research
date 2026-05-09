from typing import Any

PRICE_MOVE_THRESHOLD = 2.0
ELEVATED_MOVE_THRESHOLD = 3.0

HIGH_VOLUME_THRESHOLD = 50_000_000
LOW_VOLUME_THRESHOLD = 1_000_000


def pattern_agent(market_data: dict[str, Any]) -> dict[str, Any]:
    """
    Identify basic market behaviour signals using price movement
    and trading volume heuristics.
    """

    price_change = float(market_data.get("daily_change_percent") or 0)
    volume = int(market_data.get("volume") or 0)

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

    return {
        "agent": "pattern_agent",
        "status": "success",
        "signals": signals,
        "metadata": {
            "price_change_percent": price_change,
            "volume": volume,
            "method": "rule_based_heuristics",
        },
    }