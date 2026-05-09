from typing import Any
from langgraph.graph import END, StateGraph
from agents.critic_agent import critic_agent
from agents.market_data_agent import market_data_agent
from agents.news_agent import news_agent
from agents.pattern_agent import pattern_agent
from agents.risk_agent import risk_agent
from agents.sentiment_agent import sentiment_agent
from agents.synthesis_agent import synthesis_agent
from graph.state import ResearchState


def fetch_market_data(state: ResearchState) -> dict[str, Any]:
    """
    Fetch raw market metrics for downstream analysis
    """
    ticker = state["ticker"]

    return {
        "market_data_result": market_data_agent(ticker)
    }


def fetch_news(state: ResearchState) -> dict[str, Any]:
    """
    Retrieve recent financial news headlines
    """
    ticker = state["ticker"]

    return {
        "news_result": news_agent(ticker)
    }


def analyze_sentiment(state: ResearchState) -> dict[str, Any]:
    """
    Classify overall market sentiment from news data
    """
    news = state.get("news_result", {}).get("news", [])

    return {
        "sentiment_result": sentiment_agent(news)
    }


def analyze_risk(state: ResearchState) -> dict[str, Any]:
    """
    Evaluate basic market risk indicators
    """
    market_result = state.get("market_data_result", {})

    return {
        "risk_result": risk_agent(market_result)
    }


def detect_patterns(state: ResearchState) -> dict[str, Any]:
    """
    Detect simple price and volume patterns
    """
    market_data = (
        state.get("market_data_result", {})
        .get("market_data", {})
    )

    return {
        "pattern_result": pattern_agent(market_data)
    }


def synthesize_report(state: ResearchState) -> dict[str, Any]:
    """
    Aggregate agent outputs into a structured report
    """
    ticker = state["ticker"]

    combined = {
        "ticker": ticker.upper(),
        "market_data": (
            state.get("market_data_result", {})
            .get("market_data", {})
        ),
        "news": (
            state.get("news_result", {})
            .get("news", [])
        ),
        "sentiment": state.get("sentiment_result", {}),
        "risks": (
            state.get("risk_result", {})
            .get("risks", [])
        ),
        "patterns": (
            state.get("pattern_result", {})
            .get("signals", [])
        ),
    }

    return {
        "combined": combined,
        "report_result": synthesis_agent(combined),
    }


def critique_report(state: ResearchState) -> dict[str, Any]:
    """
    Validate generated report against compliance rules
    """
    report = (
        state.get("report_result", {})
        .get("report", "")
    )

    return {
        "critique_result": critic_agent(report)
    }


def build_graph():
    """
    Build sequential LangGraph orchestration pipeline
    """
    graph = StateGraph(ResearchState)

    graph.add_node("market_data", fetch_market_data)
    graph.add_node("news", fetch_news)
    graph.add_node("sentiment", analyze_sentiment)
    graph.add_node("risk", analyze_risk)
    graph.add_node("patterns", detect_patterns)
    graph.add_node("synthesis", synthesize_report)
    graph.add_node("critic", critique_report)

    graph.set_entry_point("market_data")

    graph.add_edge("market_data", "news")
    graph.add_edge("news", "sentiment")
    graph.add_edge("sentiment", "risk")
    graph.add_edge("risk", "patterns")
    graph.add_edge("patterns", "synthesis")
    graph.add_edge("synthesis", "critic")
    graph.add_edge("critic", END)

    return graph.compile()


research_graph = build_graph()


def run_workflow(ticker: str) -> dict[str, Any]:
    """
    Execute end-to-end research workflow
    """
    result = research_graph.invoke({
        "ticker": ticker.upper()
    })

    return {
        "data": result.get("combined", {}),
        "report": (
            result.get("report_result", {})
            .get("report", "")
        ),
        "critique": (
            result.get("critique_result", {})
        ),
    }