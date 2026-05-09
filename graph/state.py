from typing import Any, TypedDict


class ResearchState(TypedDict, total=False):
    ticker: str

    plan_result: dict[str, Any]

    market_data_result: dict[str, Any]
    news_result: dict[str, Any]
    sentiment_result: dict[str, Any]
    risk_result: dict[str, Any]
    pattern_result: dict[str, Any]

    combined: dict[str, Any]
    report_result: dict[str, Any]
    critique_result: dict[str, Any]