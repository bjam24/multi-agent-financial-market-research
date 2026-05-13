import streamlit as st
import requests

API_URL = "http://localhost:8000"


def fetch_analysis(ticker: str) -> dict:
    response = requests.get(
        f"{API_URL}/api/analyze/{ticker}",
        timeout=30
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


st.title("AI Multi-Agent Financial Market Research")

st.sidebar.header("Saved Reports")

saved_reports = fetch_saved_reports()

selected_report = st.sidebar.selectbox(
    "Select saved report",
    options=[
        report["filename"]
        for report in saved_reports
    ],
)

ticker = st.text_input("Ticker", "NVDA")

if st.button("Analyze"):

    with st.spinner("Running multi-agent analysis..."):

        try:
            data = fetch_analysis(ticker)

            st.success("Analysis completed")

            st.subheader("Research Report")
            st.markdown(data["report"])

            st.divider()

            st.subheader("Compliance Review")
            st.json(data["critique"])

            st.divider()

            st.subheader("Evaluation")
            st.json(data["evaluation"])

            with st.expander("Raw Workflow Data"):
                st.json(data["data"])
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")


if selected_report:

    saved_report = fetch_saved_report(
        selected_report
    )

    st.divider()

    st.subheader("Saved Report Preview")

    st.markdown(
        saved_report["content"]
    )