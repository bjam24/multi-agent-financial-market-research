from typing import Any

from langgraph.graph import END, StateGraph

from agents.critic_agent import critic_agent
from agents.market_data_agent import market_data_agent
from agents.news_agent import news_agent
from agents.pattern_agent import pattern_agent
from agents.planner_agent import planner_agent
from agents.risk_agent import risk_agent
from agents.sentiment_agent import sentiment_agent
from agents.synthesis_agent import synthesis_agent
from graph.state import ResearchState


# Prepare deterministic analysis plan
def plan_analysis(state: ResearchState) -> dict[str, Any]:
    ticker = state["ticker"]

    return {
        "plan_result": planner_agent(ticker)
    }


# Fetch market metrics
def fetch_market_data(state: ResearchState) -> dict[str, Any]:
    ticker = state["ticker"]

    return {
        "market_data_result": market_data_agent(ticker)
    }


# Fetch financial news
def fetch_news(state: ResearchState) -> dict[str, Any]:
    ticker = state["ticker"]

    return {
        "news_result": news_agent(ticker)
    }


# Analyze sentiment from news
def analyze_sentiment(state: ResearchState) -> dict[str, Any]:
    news = state.get("news_result", {}).get("news", [])

    return {
        "sentiment_result": sentiment_agent(news)
    }


# Detect market signals
def detect_patterns(state: ResearchState) -> dict[str, Any]:
    market_data = (
        state.get("market_data_result", {})
        .get("market_data", {})
    )

    sentiment = state.get("sentiment_result", {})

    return {
        "pattern_result": pattern_agent(
            market_data=market_data,
            sentiment=sentiment,
        )
    }


# Evaluate market risks
def analyze_risk(state: ResearchState) -> dict[str, Any]:
    market_result = state.get("market_data_result", {})
    sentiment = state.get("sentiment_result", {})

    news_topics = (
        state.get("news_result", {})
        .get("topics", [])
    )

    return {
        "risk_result": risk_agent(
            market_data_result=market_result,
            sentiment=sentiment,
            news_topics=news_topics,
        )
    }


# Generate final report
def synthesize_report(state: ResearchState) -> dict[str, Any]:
    ticker = state["ticker"]

    combined = {
        "ticker": ticker.upper(),
        "plan": state.get("plan_result", {}),
        "market_data": (
            state.get("market_data_result", {})
            .get("market_data", {})
        ),
        "news": (
            state.get("news_result", {})
            .get("news", [])
        ),
        "news_topics": (
            state.get("news_result", {})
            .get("topics", [])
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


# Validate final report
def critique_report(state: ResearchState) -> dict[str, Any]:
    report = (
        state.get("report_result", {})
        .get("report", "")
    )

    return {
        "critique_result": critic_agent(report)
    }


# Build LangGraph orchestration pipeline
def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", plan_analysis)
    graph.add_node("market_data", fetch_market_data)
    graph.add_node("news", fetch_news)
    graph.add_node("sentiment", analyze_sentiment)
    graph.add_node("patterns", detect_patterns)
    graph.add_node("risk", analyze_risk)
    graph.add_node("synthesis", synthesize_report)
    graph.add_node("critic", critique_report)

    graph.set_entry_point("planner")

    # Fan-out: market data and news can run independently
    graph.add_edge("planner", "market_data")
    graph.add_edge("planner", "news")

    # Fan-in before sentiment-dependent analysis
    graph.add_edge("market_data", "sentiment")
    graph.add_edge("news", "sentiment")

    # Parallel downstream analysis
    graph.add_edge("sentiment", "patterns")
    graph.add_edge("sentiment", "risk")

    # Fan-in before report synthesis
    graph.add_edge("patterns", "synthesis")
    graph.add_edge("risk", "synthesis")

    graph.add_edge("synthesis", "critic")
    graph.add_edge("critic", END)

    return graph.compile()


research_graph = build_graph()


# Execute workflow
def run_workflow(ticker: str) -> dict[str, Any]:
    result = research_graph.invoke({
        "ticker": ticker.upper()
    })

    return {
        "plan": result.get("plan_result", {}),
        "data": result.get("combined", {}),
        "report": (
            result.get("report_result", {})
            .get("report", "")
        ),
        "critique": result.get("critique_result", {}),
    }