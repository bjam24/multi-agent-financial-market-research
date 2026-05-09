from typing import Any
from graph.workflow import run_workflow


POSITIVE_SENTIMENT_WEIGHT = 2.0
NEGATIVE_SENTIMENT_WEIGHT = -2.0
NEUTRAL_SENTIMENT_WEIGHT = 1.0

RISK_PENALTY = 0.5
VOLATILITY_PENALTY = 0.5


def compare_tickers(
    ticker_a: str,
    ticker_b: str,
) -> dict[str, Any]:
    """
    Compare two tickers using aggregated research signals
    """

    result_a = run_workflow(ticker_a)
    result_b = run_workflow(ticker_b)

    data_a = result_a.get("data", {})
    data_b = result_b.get("data", {})

    score_a = score_result(data_a)
    score_b = score_result(data_b)

    stance_a = get_research_stance(
        data_a.get("sentiment", {}).get("sentiment"),
        float(
            data_a.get("sentiment", {})
            .get("confidence", 0)
        ),
    )

    stance_b = get_research_stance(
        data_b.get("sentiment", {}).get("sentiment"),
        float(
            data_b.get("sentiment", {})
            .get("confidence", 0)
        ),
    )

    if score_a > score_b:
        winner = ticker_a.upper()
    elif score_b > score_a:
        winner = ticker_b.upper()
    else:
        winner = "TIE"

    return {
        "ticker_a": ticker_a.upper(),
        "ticker_b": ticker_b.upper(),
        "score_a": score_a,
        "score_b": score_b,
        "winner": winner,
        "stance_a": stance_a,
        "stance_b": stance_b,
        "result_a": data_a,
        "result_b": data_b,
        "metadata": {
            "method": "heuristic_signal_scoring",
        },
    }


def score_result(data: dict[str, Any]) -> float:
    """
    Calculate heuristic research score from agent outputs
    """
    score = 0.0

    sentiment = data.get("sentiment", {})
    sentiment_label = sentiment.get("sentiment")
    confidence = float(sentiment.get("confidence", 0))

    if sentiment_label == "positive":
        score += POSITIVE_SENTIMENT_WEIGHT * confidence

    elif sentiment_label == "neutral":
        score += NEUTRAL_SENTIMENT_WEIGHT * confidence

    elif sentiment_label == "negative":
        score += NEGATIVE_SENTIMENT_WEIGHT * confidence

    risks = data.get("risks", [])

    if "No significant market risks detected" in risks:
        score += 1

    else:
        score -= len(risks) * RISK_PENALTY

    patterns = data.get("patterns", [])

    for pattern in patterns:

        pattern_lower = pattern.lower()

        if "positive price momentum" in pattern_lower:
            score += 1

        if "negative price momentum" in pattern_lower:
            score -= 1

        if "elevated short-term price movement" in pattern_lower:
            score -= VOLATILITY_PENALTY

    return round(score, 2)


def get_research_stance(
    sentiment: str | None,
    confidence: float,
) -> str:
    """
    Derive simplified research stance from sentiment strength
    """

    if sentiment == "positive" and confidence >= 0.7:
        return "favorable"

    if sentiment == "negative" and confidence >= 0.7:
        return "cautious"

    return "neutral"