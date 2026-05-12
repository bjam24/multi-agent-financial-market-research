from agents.pattern_agent import pattern_agent


def test_pattern_agent_detects_high_volume():

    market_data = {
        "daily_change_percent": 1.2,
        "volume": 100_000_000,
    }

    sentiment = {
        "sentiment": "positive"
    }

    result = pattern_agent(
        market_data=market_data,
        sentiment=sentiment,
    )

    signals = result["signals"]

    assert "Unusually high trading volume" in signals


def test_pattern_agent_detects_negative_divergence():

    market_data = {
        "daily_change_percent": -3.5,
        "volume": 20_000_000,
    }

    sentiment = {
        "sentiment": "positive"
    }

    result = pattern_agent(
        market_data=market_data,
        sentiment=sentiment,
    )

    signals = result["signals"]

    assert (
        "Divergence: positive news sentiment with negative price movement"
        in signals
    )