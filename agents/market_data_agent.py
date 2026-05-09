from typing import Any

from tools.alpha_vantage_tool import get_market_data


def market_data_agent(ticker: str) -> dict[str, Any]:
    """
    Fetch and structure daily market data from Alpha Vantage.
    """

    normalized_ticker = ticker.upper()
    market_data = get_market_data(normalized_ticker)

    return {
        "agent": "market_data_agent",
        "ticker": normalized_ticker,
        "market_data": market_data,
        "status": market_data.get("status", "unknown"),
    }