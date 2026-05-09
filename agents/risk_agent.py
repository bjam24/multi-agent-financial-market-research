from typing import Any

HIGH_VOLATILITY_THRESHOLD = 5.0
LOW_VOLUME_THRESHOLD = 1_000_000


def risk_agent(market_data: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate basic market risk indicators using price movement and trading activity heuristics.
    """

    data = market_data.get("market_data", {})

    ticker = market_data.get("ticker")

    daily_change = float(data.get("daily_change_percent") or 0)
    volume = int(data.get("volume") or 0)

    risks: list[str] = []

    if abs(daily_change) >= HIGH_VOLATILITY_THRESHOLD:
        risks.append("Elevated short-term price volatility")

    if data.get("status") != "success":
        risks.append("Market data reliability issue detected")

    if volume <= LOW_VOLUME_THRESHOLD:
        risks.append("Low trading liquidity")

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
            "method": "rule_based_risk_analysis",
        },
    }