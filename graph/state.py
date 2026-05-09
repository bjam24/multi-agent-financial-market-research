from typing import TypedDict


class ResearchState(TypedDict, total=False):
    ticker: str
    market_data_result: dict
    news_result: dict
    sentiment_result: dict
    risk_result: dict
    pattern_result: dict
    combined: dict
    report_result: dict
    critique_result: dict