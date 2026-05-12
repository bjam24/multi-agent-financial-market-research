from agents.critic_agent import critic_agent


def test_critic_agent_passes_valid_report():

    report = """
    ## Market Summary
    Stable market activity with moderate momentum and balanced trading conditions.
    The company shows mixed short-term signals, with price movement remaining within
    a reasonable range compared with recent trading activity. Volume appears adequate
    for basic market interpretation, although additional confirmation would be needed
    before drawing stronger conclusions.

    ## Sentiment Analysis
    Neutral market sentiment with mixed short-term signals. Recent headlines do not
    indicate a clear directional bias, and the overall tone remains cautious.

    ## Risk Analysis
    Moderate volatility risk detected with some uncertainty in the sector. Investors
    should be aware of changing market conditions, liquidity changes, and possible
    news-driven price reactions.

    ## Confidence Score
    Confidence score: 0.72

    ## Disclaimer
    This report is for informational purposes only and does not constitute financial advice.
    """

    result = critic_agent(report)

    assert result["status"] == "passed"
    assert len(result["issues"]) == 0


def test_critic_agent_detects_advisory_language():

    report = """
    Strong buy opportunity.

    ## Disclaimer
    This report is for informational purposes only and does not constitute financial advice.
    """

    result = critic_agent(report)

    assert result["status"] == "needs_review"
    assert len(result["issues"]) > 0