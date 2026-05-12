from services.evaluation_service import evaluate_report


def test_evaluate_report_passes_valid_report():
    report = """
    ## Market Summary
    Some market data.

    ## Sentiment Analysis
    Neutral sentiment.

    ## Risk Analysis
    No significant market risks detected.

    ## Disclaimer
    This report is for informational purposes only.
    """

    critique = {
        "issues": []
    }

    result = evaluate_report(report, critique)

    assert result["passed"] is True
    assert result["score"] >= 70