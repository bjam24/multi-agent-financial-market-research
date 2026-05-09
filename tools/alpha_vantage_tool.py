import os
import requests
from dotenv import load_dotenv


load_dotenv()


def get_market_data(ticker: str) -> dict:
    """
    Fetch basic daily market data for a stock ticker using Alpha Vantage.
    """

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        raise ValueError("Missing ALPHA_VANTAGE_API_KEY in .env file")

    ticker = ticker.upper()

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": api_key,
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    if "Error Message" in data:
        raise ValueError(f"Invalid ticker or Alpha Vantage error: {ticker}")

    if "Note" in data:
        raise RuntimeError("Alpha Vantage API limit reached. Try again later.")

    time_series = data.get("Time Series (Daily)")

    if not time_series:
        raise ValueError(f"No market data found for ticker: {ticker}")

    dates = sorted(time_series.keys(), reverse=True)

    latest_date = dates[0]
    previous_date = dates[1] if len(dates) > 1 else dates[0]

    latest = time_series[latest_date]
    previous = time_series[previous_date]

    current_price = float(latest["4. close"])
    previous_close = float(previous["4. close"])

    daily_change = current_price - previous_close
    daily_change_percent = (
        daily_change / previous_close * 100 if previous_close else 0
    )

    return {
        "ticker": ticker,
        "latest_date": latest_date,
        "previous_date": previous_date,
        "current_price": round(current_price, 2),
        "previous_close": round(previous_close, 2),
        "daily_change": round(daily_change, 2),
        "daily_change_percent": round(daily_change_percent, 2),
        "volume": int(latest["5. volume"]),
        "data_source": "alpha_vantage",
        "status": "success",
    }