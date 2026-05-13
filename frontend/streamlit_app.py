import streamlit as st
import requests


API_URL = "http://localhost:8000"


st.set_page_config(
    page_title="AI Financial Market Research",
    page_icon="📈",
    layout="wide",
)


def fetch_analysis(ticker: str) -> dict:

    response = requests.get(
        f"{API_URL}/api/analyze/{ticker}",
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def fetch_saved_reports() -> list:

    response = requests.get(
        f"{API_URL}/api/reports",
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("reports", [])


def fetch_saved_report(filename: str) -> dict:

    response = requests.get(
        f"{API_URL}/api/reports/{filename}",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# =========================
# Sidebar
# =========================

st.sidebar.title("Saved Reports")

saved_reports = fetch_saved_reports()

selected_report = st.sidebar.selectbox(
    "Select report",
    options=[
        report["filename"]
        for report in saved_reports
    ] if saved_reports else [],
)


# =========================
# Main Header
# =========================

st.title("AI Multi-Agent Financial Market Research")

st.caption(
    """
    Multi-agent financial market intelligence system built with
    LangGraph, OpenAI, FastAPI, and Streamlit.
    """
)

st.divider()


# =========================
# Analysis Section
# =========================

ticker = st.text_input(
    "Ticker",
    value="NVDA",
)

analyze_button = st.button(
    "Run Analysis",
    use_container_width=True,
)


if analyze_button:

    with st.spinner(
        "Running multi-agent market research workflow..."
    ):

        try:
            data = fetch_analysis(ticker)

            st.success(
                "Analysis completed successfully."
            )

            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "Report",
                    "Evaluation",
                    "Critique",
                    "Raw Data",
                ]
            )

            with tab1:

                st.markdown(
                    data["report"]
                )

            with tab2:

                st.json(
                    data["evaluation"]
                )

            with tab3:

                st.json(
                    data["critique"]
                )

            with tab4:

                st.json(
                    data["data"]
                )

        except requests.exceptions.RequestException as error:

            st.error(
                f"API request failed: {error}"
            )


# =========================
# Saved Report Preview
# =========================

if selected_report:

    try:

        saved_report = fetch_saved_report(
            selected_report
        )

        st.divider()

        st.subheader(
            "Saved Report Preview"
        )

        st.markdown(
            saved_report["content"]
        )

    except requests.exceptions.RequestException as error:

        st.error(
            f"Failed to load saved report: {error}"
        )