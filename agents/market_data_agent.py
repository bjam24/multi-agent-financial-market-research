from tools.alpha_vantage_tool import get_market_data


def market_data_agent(ticker: str) -> dict:
    """
    Agent responsible for fetching and structuring market data.
    """

    market_data = get_market_data(ticker)

    return {
        "agent": "market_data_agent",
        "ticker": ticker.upper(),
        "market_data": market_data,
        "status": market_data.get("status", "unknown"),
    }