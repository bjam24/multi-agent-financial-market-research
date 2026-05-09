from typing import Any


def planner_agent(ticker: str) -> dict[str, Any]:
    """
    Prepare a deterministic research plan for the selected ticker.
    """

    normalized_ticker = ticker.upper()

    steps = [
        "fetch_market_data",
        "fetch_news",
        "analyze_sentiment",
        "detect_patterns",
        "analyze_risk",
        "synthesize_report",
        "critique_report",
    ]

    required_data = [
        "current_price",
        "previous_close",
        "daily_change",
        "daily_change_percent",
        "volume",
        "financial_news",
    ]

    return {
        "agent": "planner_agent",
        "ticker": normalized_ticker,
        "steps": steps,
        "required_data": required_data,
        "status": "success",
    }